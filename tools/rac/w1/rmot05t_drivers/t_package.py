# RM-OT-05T compact sculptor release: build + clean-extraction verification (repeatable).
#   build : stage gorrund_05T_sculpt_handoff/ (entry files at the root + repository-relative inputs / tools needed for the
#           local edit and its validation; historical race evidence is cited, not duplicated), write PACKAGE_MANIFEST.sha256
#           (every file except itself), PACKAGE_FILES.tsv, DECODED_HASHES.txt; zip (split into <= --volume_mb volumes if larger)
#   verify: copy the archive (volumes) into an isolated empty dir, rejoin if split, unzip -t, extract, check manifest
#           completeness / hashes / unlisted files, decoded mesh hashes, relative markdown links, and run the release's own
#           check_return.sh on an unchanged copy of the packaged scene (expects ACCEPTED + S3-identical gate scores)
# Usage (repository root): python3 tools/rac/w1/rmot05t_drivers/t_package.py build|verify --out DIR [--receipt R.json]
import argparse, glob, gzip, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
ap = argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('--name', default='gorrund_05T_sculpt_handoff'); ap.add_argument('--out'); ap.add_argument('--volume_mb', type=int, default=24); ap.add_argument('--receipt'); a = ap.parse_args()
REL = 'reviews/rac-rmot05t-release'
ROOT_FROM_REL = ['START_HERE.md', 'BRIEF.md', 'REQUIREMENTS.txt', 'scene', 'views']
PAYLOAD = ['reviews/chatgpt-rac-rm-ot-05t-gorrund-direct-sculpt-handoff-validation-stop-order.md', 'reviews/chatgpt-rac-rm-ot-05t1-execute-handoff-validation-order.md',
           'reviews/claude-rac-rm-ot-05t-gorrund-direct-sculpt-handoff-validation-closure.md',
           REL + '/validation', REL + '/tests',
           'reviews/rac-rmot05q-evidence/source/F1_working.obj.gz', 'reviews/rac-rmot05q-evidence/source/PROVENANCE.md', 'reviews/rac-rmot05q-evidence/source/extraction_record.json',
           'reviews/rac-rmot05q-evidence/plan/patch_selection.json', 'reviews/rac-rmot05q-evidence/plan/patch_face_sets.npz',
           'reviews/rac-rmot05s-evidence/repair/S3', 'reviews/rac-rmot05s-evidence/plan/PLAN.md', 'reviews/rac-rmot05s-evidence/plan/interface_sets.npz',
           'reviews/rac-rmot05s-evidence/plan/design_posterior.npz', 'reviews/rac-rmot05s-evidence/plan/design_anterior.npz', 'reviews/rac-rmot05s-evidence/handoff/HANDOFF.md',
           'tools/rac/w1/rmot05t_drivers', 'tools/rac/w1/rmot05s_drivers/s_lib.py', 'tools/rac/w1/rmot05s_drivers/s_design.py', 'tools/rac/w1/rmot05s_drivers/s_verify.py',
           'tools/rac/w1/rmot05s_drivers/s_rematch.py', 'tools/rac/w1/rmot05q_drivers/q_render.py', 'tools/rac/w1/rmot05r_drivers/r_compare.py', 'tools/rac/w1/rmot05r_drivers/r_profiles.py']
EXCLUDE = re.compile(r'(__pycache__|\.pyc$|_return\.npz$|/package/)')
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def files_under(root):
    return sorted(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/') for dp, dn, fn in os.walk(root) for f in fn)
def cp(src, dst):
    if os.path.isdir(src):
        for f in files_under(src):
            if not EXCLUDE.search(src + '/' + f): cp(os.path.join(src, f), os.path.join(dst, f))
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
README = '''# {name}: RM-OT-05T compact direct-sculpt release

**Start with [START_HERE.md](START_HERE.md).** The closure report is [here](reviews/claude-rac-rm-ot-05t-gorrund-direct-sculpt-handoff-validation-closure.md).

**State:** Gorrund UNACCEPTED / DIRECT SCULPT REQUIRED. Grask E3 FROZEN. RM-OT-05 OPEN. Stage C BLOCKED.

## Integrity

- `PACKAGE_MANIFEST.sha256` is THIS release's own manifest, in `sha256sum -c` format. It covers every file except itself.
- `PACKAGE_FILES.tsv` gives sizes; `DECODED_HASHES.txt` gives the compressed and decoded SHA-256 of every `.obj.gz`.

## Contents

| Contents | Where |
|---|---|
| Entry files | At the root: START_HERE, BRIEF, REQUIREMENTS, `scene/`, `views/` |
| Validation and test evidence | `reviews/rac-rmot05t-release/validation/` and `tests/`. The per-test `*_return.npz` exports are in the repository only, for size |
| Inputs for the check | F1 working mesh (`reviews/rac-rmot05q-evidence/source/`), S3 (`reviews/rac-rmot05s-evidence/repair/S3/`), the 05Q frame / protected sets and the 05S interface definition, at their repository paths |
| Tools | `tools/rac/w1/...`, at their repository paths |

**Frozen provenance cited, not duplicated:**
- `racebodies_v121`–`v123` and the repository `Jambi92/wayfarer-design` (05Q / 05R / 05S evidence);
- the 05S handoff scene `GO-05S_interface_handoff.blend`, sha256 `114e69cf8f9745762d792e2dcca8a1cab5b80b1253c3f185ac79d3a2555f4d89`, which is unchanged;
- `base.glb`, external, sha256 `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b`.
'''
if a.mode == 'build':
    stage = os.path.join(a.out, a.name); shutil.rmtree(stage, ignore_errors=True); os.makedirs(stage)
    for f in ROOT_FROM_REL: cp(os.path.join(REL, f), os.path.join(stage, f))
    for p in PAYLOAD: cp(p, os.path.join(stage, p))
    open(os.path.join(stage, 'README.md'), 'w').write(README.format(name=a.name))
    lines = []
    for f in files_under(stage):
        if f.endswith('.obj.gz'):
            raw = gzip.open(os.path.join(stage, f), 'rb').read(); lines.append('%s\t%s\t%s\t%d' % (f, sha(os.path.join(stage, f)), hashlib.sha256(raw).hexdigest(), len(raw)))
    open(os.path.join(stage, 'DECODED_HASHES.txt'), 'w').write('path\tsha256_compressed\tsha256_decoded\tdecoded_bytes\n' + '\n'.join(lines) + '\n')
    allf = [f for f in files_under(stage) if f not in ('PACKAGE_MANIFEST.sha256', 'PACKAGE_FILES.tsv')]
    open(os.path.join(stage, 'PACKAGE_FILES.tsv'), 'w').write('path\tbytes\n' + '\n'.join('%s\t%d' % (f, os.path.getsize(os.path.join(stage, f))) for f in allf + ['PACKAGE_FILES.tsv']) + '\n')
    allf = [f for f in files_under(stage) if f != 'PACKAGE_MANIFEST.sha256']
    open(os.path.join(stage, 'PACKAGE_MANIFEST.sha256'), 'w').write(''.join('%s  %s\n' % (sha(os.path.join(stage, f)), f) for f in allf))
    for old in glob.glob(os.path.join(a.out, a.name + '.z*')): os.remove(old)
    subprocess.run(['zip', '-q', '-r', '-X', a.name + '.zip', a.name], cwd=a.out, check=True)
    if os.path.getsize(os.path.join(a.out, a.name + '.zip')) > a.volume_mb * 1024 * 1024:
        os.remove(os.path.join(a.out, a.name + '.zip')); subprocess.run(['zip', '-q', '-r', '-X', '-s', '%dm' % a.volume_mb, a.name + '.zip', a.name], cwd=a.out, check=True)
    vols = sorted(glob.glob(os.path.join(a.out, a.name + '.z*')))
    print(json.dumps(dict(files_in_manifest=len(allf), volumes=[dict(file=os.path.basename(v), bytes=os.path.getsize(v), sha256=sha(v)) for v in vols]), indent=1))
else:
    vols = sorted(glob.glob(os.path.join(a.out, a.name + '.z*'))); iso = tempfile.mkdtemp(prefix='clean_extract_05T_'); res = dict(isolated_dir=iso, checked_at=time.strftime('%Y-%m-%dT%H:%M:%S%z'))
    for v in vols: shutil.copy2(v, iso)
    res['volumes'] = [dict(file=os.path.basename(v), bytes=os.path.getsize(v), sha256=sha(v)) for v in vols]
    z = os.path.join(iso, a.name + '.zip')
    if len(vols) > 1:
        subprocess.run(['zip', '-q', '-s', '0', a.name + '.zip', '--out', a.name + '_joined.zip'], cwd=iso, check=True); z = os.path.join(iso, a.name + '_joined.zip'); res['joined_zip'] = dict(bytes=os.path.getsize(z), sha256=sha(z))
    t = subprocess.run(['unzip', '-tq', z], capture_output=True, text=True); res['zip_crc_test'] = (t.stdout + t.stderr).strip()
    ex = os.path.join(iso, 'x'); subprocess.run(['unzip', '-q', z, '-d', ex], check=True); root = os.path.join(ex, a.name)
    man = [l.rstrip('\n').split('  ', 1) for l in open(os.path.join(root, 'PACKAGE_MANIFEST.sha256'))]
    listed = set(p for _, p in man); actual = set(files_under(root)) - {'PACKAGE_MANIFEST.sha256'}
    res['manifest'] = dict(entries=len(man), all_present=all(os.path.exists(os.path.join(root, p)) for _, p in man), all_hashes_equal=all(os.path.exists(os.path.join(root, p)) and sha(os.path.join(root, p)) == h for h, p in man),
                           unlisted_files=sorted(actual - listed), listed_but_missing=sorted(listed - actual))
    dec = [l.rstrip('\n').split('\t') for l in open(os.path.join(root, 'DECODED_HASHES.txt'))][1:]
    res['decoded_meshes'] = dict(count=len(dec), all_equal=all(hashlib.sha256(gzip.open(os.path.join(root, p), 'rb').read()).hexdigest() == hd and sha(os.path.join(root, p)) == hc for p, hc, hd, _ in dec))
    bad = []; n = 0
    for md in [f for f in actual if f.endswith('.md')]:
        for m in re.finditer(r'\]\(([^)#\s]+)\)', open(os.path.join(root, md), encoding='utf-8').read()):
            tg = m.group(1)
            if re.match(r'^[a-z]+://', tg): continue
            n += 1
            if not os.path.exists(os.path.normpath(os.path.join(root, os.path.dirname(md), tg))): bad.append(md + ' -> ' + tg)
    res['relative_links'] = dict(checked=n, unresolved=bad)
    shutil.copy2(os.path.join(root, 'scene', 'GO-05T_sculpt_handoff.blend'), os.path.join(root, 'scene', 'fixture_test.blend'))
    r = subprocess.run(['bash', 'tools/rac/w1/rmot05t_drivers/check_return.sh', 'scene/fixture_test.blend', 'checks/fixture'], cwd=root, capture_output=True, text=True)
    out = r.stdout; res['check_return_unchanged_fixture'] = dict(returncode=r.returncode, accepted='reintegration: ACCEPTED_FOR_VERIFICATION' in out,
        verdict_line=[l for l in out.splitlines() if 's_verify verdict' in l], tail=out[-1200:], stderr_tail=r.stderr[-600:])
    try:
        vj = json.load(open(os.path.join(root, 'checks/fixture/result_verify.json'))); s3 = json.load(open(os.path.join(root, 'reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_verify.json')))
        res['check_return_unchanged_fixture']['scores_identical_to_S3'] = vj == s3
    except Exception as e: res['check_return_unchanged_fixture']['scores_identical_to_S3'] = 'not available: %s' % e
    res['limitations'] = 'headless bpy 5.0.1 module only; Blender desktop UI (brushes, mask display, face-set isolation) not exercised -> START_HERE Step 0 PENDING'
    res['pass'] = bool(res['manifest']['all_present'] and res['manifest']['all_hashes_equal'] and not res['manifest']['unlisted_files'] and not res['manifest']['listed_but_missing']
                       and res['decoded_meshes']['all_equal'] and not bad and r.returncode == 0 and res['check_return_unchanged_fixture']['accepted'] and res['check_return_unchanged_fixture'].get('scores_identical_to_S3') is True)
    json.dump(res, open(a.receipt, 'w'), indent=1); print(json.dumps({k: v for k, v in res.items() if k != 'check_return_unchanged_fixture'}, indent=1)); print(res['check_return_unchanged_fixture'])

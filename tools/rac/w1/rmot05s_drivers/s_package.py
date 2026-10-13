# RM-OT-05S release packaging + clean-extraction verification (repeatable; derived from the 05R r_package.py).
#   build : stage the release tree with repository-relative paths, write DECODED_HASHES.txt, PACKAGE_FILES.tsv and
#           PACKAGE_MANIFEST.sha256 (every packaged payload file except the manifest itself), zip it, and split it into
#           volumes of at most --volume_mb (the delivery channels accept <= 30 MB per file).
#   verify: copy the volumes to an isolated empty directory, rejoin (zip -s 0), unzip, and check: manifest entries present
#           and hashes equal; every extracted file listed (manifest itself excepted); decoded mesh hashes; relative markdown
#           links and replay inputs resolve; then run the S3 verification + handoff rematch self-test from the extracted package and compare it with the
#           packaged result. Writes a receipt JSON.
# Usage (repository root):  python3 tools/rac/w1/rmot05s_drivers/s_package.py build  --name racebodies_v123 --out DIR
#                           python3 tools/rac/w1/rmot05s_drivers/s_package.py verify --name racebodies_v123 --out DIR --receipt R.json
import argparse, glob, gzip, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time
ap = argparse.ArgumentParser(); ap.add_argument('mode'); ap.add_argument('--name', default='racebodies_v123'); ap.add_argument('--out'); ap.add_argument('--volume_mb', type=int, default=24)
ap.add_argument('--receipt'); a = ap.parse_args()
PAYLOAD = ['reviews/chatgpt-rac-rm-ot-05q-gorrund-source-surface-patch-feasibility-order.md', 'reviews/chatgpt-rac-rm-ot-05r-gorrund-patch-junction-repair-package-order.md',
           'reviews/chatgpt-rac-rm-ot-05s-gorrund-direct-band-axilla-interface-order.md',
           'reviews/claude-rac-rm-ot-05q-gorrund-source-surface-patch-feasibility-gate.md', 'reviews/claude-rac-rm-ot-05r-gorrund-patch-junction-repair-package-gate.md',
           'reviews/claude-rac-rm-ot-05s-gorrund-direct-band-axilla-interface-gate.md',
           'reviews/rac-rmot05q-evidence', 'reviews/rac-rmot05r-evidence', 'reviews/rac-rmot05s-evidence',
           'tools/rac/w1/rmot05q_drivers', 'tools/rac/w1/rmot05r_drivers', 'tools/rac/w1/rmot05s_drivers']
EXCLUDE = re.compile(r'(__pycache__|\.pyc$|rac-rmot05s-evidence/package/)')
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def files_under(root):
    out = []
    for dp, dn, fn in os.walk(root):
        for f in fn: out.append(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/'))
    return sorted(out)
README = r'''# {name}: RM-OT-05S release (Gorrund direct band-to-axilla interface study + direct-edit handoff)

Read first: [05S gate report](reviews/claude-rac-rm-ot-05s-gorrund-direct-band-axilla-interface-gate.md).

**Study result: S3, automated verdict UNRESOLVED.**
- Anterior: plausible.
- Posterior: the fold-edge crinkle is not credible.

A direct-edit handoff is included. Gorrund UNACCEPTED, Grask E3 FROZEN, RM-OT-05 OPEN, Stage C BLOCKED.

## Delivery and integrity

- This release is ONE zip archive split into volumes: `{name}.zip` plus `{name}.z01`, `.z02`, and so on, each 25 MB or less.
  - To rejoin: `zip -s 0 {name}.zip --out {name}_joined.zip`.
  - Or open `{name}.zip` with 7-Zip, with all volumes in one folder.
- `PACKAGE_MANIFEST.sha256` is THIS package's own manifest, in `sha256sum -c` format. It covers every packaged file except itself.
- `PACKAGE_FILES.tsv` gives sizes; `DECODED_HASHES.txt` gives the compressed and decoded SHA-256 of every `.obj.gz`.
- The `SHA256SUMS.txt` files inside `reviews/rac-rmot05q-evidence/`, `reviews/rac-rmot05r-evidence/` and `reviews/rac-rmot05s-evidence/` are the **repository evidence manifests**, copied verbatim. They are not the package manifest.
- All evidence files are original bytes: PNG stays PNG, with no conversions and no omissions.
- The 05R `package/` receipt folder is included as committed. The 05S package receipt is committed to the repository after this build, so it is not inside.

## Contents (repository-relative paths)

| Item | Path |
|---|---|
| Orders | [05Q](reviews/chatgpt-rac-rm-ot-05q-gorrund-source-surface-patch-feasibility-order.md), [05R](reviews/chatgpt-rac-rm-ot-05r-gorrund-patch-junction-repair-package-order.md), [05S](reviews/chatgpt-rac-rm-ot-05s-gorrund-direct-band-axilla-interface-order.md) |
| Reports | [05Q](reviews/claude-rac-rm-ot-05q-gorrund-source-surface-patch-feasibility-gate.md), [05R](reviews/claude-rac-rm-ot-05r-gorrund-patch-junction-repair-package-gate.md), [05S](reviews/claude-rac-rm-ot-05s-gorrund-direct-band-axilla-interface-gate.md) |
| Plans | [05Q](reviews/rac-rmot05q-evidence/plan/PLAN.md), [05R](reviews/rac-rmot05r-evidence/plan/PLAN.md), [05S](reviews/rac-rmot05s-evidence/plan/PLAN.md) |
| Source F1 working mesh (replay input) | [F1_working.obj.gz](reviews/rac-rmot05q-evidence/source/F1_working.obj.gz); [PROVENANCE.md](reviews/rac-rmot05q-evidence/source/PROVENANCE.md); [extraction_record.json](reviews/rac-rmot05q-evidence/source/extraction_record.json); [F1_face_indices.npz](reviews/rac-rmot05q-evidence/source/F1_face_indices.npz) |
| B2 baseline | [GO-05Q-B2.obj.gz](reviews/rac-rmot05q-evidence/repair/GO-05Q-B2.obj.gz) |
| 05S result and checkpoints | `reviews/rac-rmot05s-evidence/repair/S1`, `S2` and `S3` (S3 is final): meshes, pre-flip checkpoints, records, labels, maps, verification |
| 05S interface sets / labels / design | [interface_sets.npz](reviews/rac-rmot05s-evidence/plan/interface_sets.npz), `design_*.npz` |
| Direct-edit handoff | [HANDOFF.md](reviews/rac-rmot05s-evidence/handoff/HANDOFF.md), [GO-05S_interface_handoff.blend](reviews/rac-rmot05s-evidence/handoff/GO-05S_interface_handoff.blend) |
| Images | [05S compare](reviews/rac-rmot05s-evidence/compare/), [05S plan views](reviews/rac-rmot05s-evidence/plan/) |
| Earlier evidence | `reviews/rac-rmot05q-evidence/` (attempts A1–B3) and `reviews/rac-rmot05r-evidence/` (R1–R3) |
| Tools | `tools/rac/w1/rmot05q_drivers/`, `rmot05r_drivers/`, `rmot05s_drivers/` (including this packager, `s_package.py`) |
| Replay | [05S REPLAY.md](reviews/rac-rmot05s-evidence/REPLAY.md), `replay_package.sh`, [REQUIREMENTS.txt](REQUIREMENTS.txt) |

## Original source (external)

`base.glb` is 43,012,652 bytes, sha256 `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b`.
- **Verified location:** `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Male\Gorrund-Male_Rodin_base.glb.zip`. The zip's own sha256 is `b3fbfb2a381e5300239227c4ceb533d40aa53e057ccfacf8eb0740bdb4bb482e`.
- **Not needed for this release:** the bundled F1 working mesh is enough for patch replay and handoff inspection.
- **Separate prerequisite:** to re-verify the extraction itself, run `tools/rac/w1/rmot05q_drivers/q_extract.py` (see the 05Q REPLAY).

## Replay from this package

Run `bash replay_package.sh`.
- It decodes the inputs and checks their hashes.
- It re-runs the S3 verification and compares it with the packaged result.
- It runs the handoff rematch self-test.

Renders and the `.blend` rebuild need bpy and are not part of the scripted replay.
'''
REPLAY_SH = '''#!/usr/bin/env bash
# Replay check from the extracted package root (bpy not needed).
set -euo pipefail
Q=reviews/rac-rmot05q-evidence; S=reviews/rac-rmot05s-evidence; T=tools/rac/w1/rmot05s_drivers; OUT=${OUT:-replay_out}; mkdir -p "$OUT"
gunzip -c $Q/source/F1_working.obj.gz > "$OUT/F1_working.obj"; gunzip -c $Q/repair/GO-05Q-B2.obj.gz > "$OUT/B2.obj"; gunzip -c $S/repair/S3/GO-05S-S3.obj.gz > "$OUT/GO-05S-S3.obj"
echo "17591025c24fd080e7fd45e3dc88dccc4707a0bee9efcb3fd70ef5ab6da453b0  $OUT/F1_working.obj" | sha256sum -c -
echo "0ed458b72e6481377aa829d70f8f7896381634e9fc7cca09bc325a91b420962a  $OUT/B2.obj" | sha256sum -c -
echo "1d50383376dc5dd2e249778c7b7d8330f4ec16daa21303656a146c0b4d81ac4c  $OUT/GO-05S-S3.obj" | sha256sum -c -
python3 $T/s_verify.py --src "$OUT/F1_working.obj" --q05 $Q --plan $S/plan --res "$OUT/GO-05S-S3.obj" --maps $S/repair/S3/GO-05S-S3_maps.npz --labels $S/repair/S3/GO-05S-S3_face_labels.npy --out "$OUT/S3" > /dev/null
python3 - "$OUT/S3_verify.json" $S/repair/S3/GO-05S-S3_verify.json <<'PY'
import json, sys
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
same = a == b
print('replayed S3 verification identical to packaged result:', same, '| verdict', a['verdict_automated'])
sys.exit(0 if same else 1)
PY
python3 $T/s_rematch.py --edited "$OUT/GO-05S-S3.obj" --src "$OUT/F1_working.obj" --plan $S/plan --out "$OUT/rematch" > /dev/null
python3 -c "import json,sys; r=json.load(open(sys.argv[1])); print('handoff rematch self-test:', r); sys.exit(0 if r['protected_faces_missing_or_moved']==0 else 1)" "$OUT/rematch_rematch.json"
'''
REQ = '''Python 3.11.15
numpy 1.26.4
scipy 1.17.1
trimesh 5.1.1
matplotlib 3.10.9
Pillow 12.2.0
libigl 2.6.3 (import igl)
triangle 20250106
bpy 5.0.1 (renders only; Blender as a Python module)
System tools: gzip, sha256sum, zip / unzip (Info-ZIP 3.0 / 6.0) or 7-Zip for the split archive
'''
if a.mode == 'build':
    stage = os.path.join(a.out, a.name); shutil.rmtree(stage, ignore_errors=True); os.makedirs(stage)
    for p in PAYLOAD:
        if os.path.isdir(p):
            for f in files_under(p):
                if EXCLUDE.search(p + '/' + f): continue
                d = os.path.join(stage, p, f); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(os.path.join(p, f), d)
        else:
            d = os.path.join(stage, p); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(p, d)
    open(os.path.join(stage, 'README.md'), 'w').write(README.format(name=a.name)); open(os.path.join(stage, 'REQUIREMENTS.txt'), 'w').write(REQ)
    open(os.path.join(stage, 'replay_package.sh'), 'w').write(REPLAY_SH); os.chmod(os.path.join(stage, 'replay_package.sh'), 0o755)
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
    subprocess.run(['zip', '-q', '-r', '-X', '-s', '%dm' % a.volume_mb, a.name + '.zip', a.name], cwd=a.out, check=True)
    vols = sorted(glob.glob(os.path.join(a.out, a.name + '.z*')))
    print(json.dumps(dict(stage=stage, files_in_manifest=len(allf), volumes=[dict(file=os.path.basename(v), bytes=os.path.getsize(v), sha256=sha(v)) for v in vols]), indent=1))
elif a.mode == 'verify':
    vols = sorted(glob.glob(os.path.join(a.out, a.name + '.z*'))); iso = tempfile.mkdtemp(prefix='clean_extract_'); res = dict(isolated_dir=iso, checked_at=time.strftime('%Y-%m-%dT%H:%M:%S%z'))
    for v in vols: shutil.copy2(v, iso)
    res['volumes'] = [dict(file=os.path.basename(v), bytes=os.path.getsize(v), sha256=sha(v)) for v in vols]
    subprocess.run(['zip', '-q', '-s', '0', a.name + '.zip', '--out', a.name + '_joined.zip'], cwd=iso, check=True)
    j = os.path.join(iso, a.name + '_joined.zip'); res['joined_zip'] = dict(bytes=os.path.getsize(j), sha256=sha(j))
    t = subprocess.run(['unzip', '-tq', j], capture_output=True, text=True); res['zip_integrity_test'] = t.stdout.strip() or t.stderr.strip()
    ex = os.path.join(iso, 'x'); subprocess.run(['unzip', '-q', j, '-d', ex], check=True); root = os.path.join(ex, a.name)
    man = [l.rstrip('\n').split('  ', 1) for l in open(os.path.join(root, 'PACKAGE_MANIFEST.sha256'))]
    present = [os.path.exists(os.path.join(root, p)) for _, p in man]; equal = [os.path.exists(os.path.join(root, p)) and sha(os.path.join(root, p)) == h for h, p in man]
    listed = set(p for _, p in man); actual = set(files_under(root)) - {'PACKAGE_MANIFEST.sha256'}
    res['manifest'] = dict(entries=len(man), all_present=all(present), all_hashes_equal=all(equal), unlisted_files=sorted(actual - listed), listed_but_missing=sorted(listed - actual))
    dec = [l.rstrip('\n').split('\t') for l in open(os.path.join(root, 'DECODED_HASHES.txt'))][1:]
    res['decoded_meshes'] = dict(count=len(dec), all_equal=all(hashlib.sha256(gzip.open(os.path.join(root, p), 'rb').read()).hexdigest() == hd and sha(os.path.join(root, p)) == hc for p, hc, hd, _ in dec))
    bad = []; nlinks = 0
    for md in [f for f in actual if f.endswith('.md')]:
        for m in re.finditer(r'\]\(([^)#\s]+)\)', open(os.path.join(root, md), encoding='utf-8').read()):
            tgt = m.group(1)
            if re.match(r'^[a-z]+://', tgt): continue
            nlinks += 1
            if not os.path.exists(os.path.normpath(os.path.join(root, os.path.dirname(md), tgt))): bad.append(md + ' -> ' + tgt)
    res['relative_links'] = dict(checked=nlinks, unresolved=bad)
    inputs = ['reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3.obj.gz', 'reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_maps.npz', 'reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_face_labels.npy',
              'reviews/rac-rmot05s-evidence/plan/interface_sets.npz', 'reviews/rac-rmot05s-evidence/plan/design_posterior.npz', 'reviews/rac-rmot05s-evidence/plan/design_anterior.npz',
              'reviews/rac-rmot05s-evidence/handoff/GO-05S_interface_handoff.blend', 'reviews/rac-rmot05s-evidence/handoff/HANDOFF.md', 'tools/rac/w1/rmot05s_drivers/s_verify.py',
              'tools/rac/w1/rmot05s_drivers/s_rematch.py', 'tools/rac/w1/rmot05s_drivers/s_repair.py', 'tools/rac/w1/rmot05s_drivers/s_handoff_blend.py',
              'reviews/rac-rmot05q-evidence/source/F1_working.obj.gz', 'reviews/rac-rmot05q-evidence/repair/GO-05Q-B2.obj.gz', 'reviews/rac-rmot05q-evidence/plan/patch_selection.json',
              'reviews/rac-rmot05q-evidence/plan/patch_face_sets.npz', 'reviews/rac-rmot05q-evidence/repair/GO-05Q-B2_vertex_map.npy', 'reviews/rac-rmot05q-evidence/repair/GO-05Q-B2_face_labels.npy',
              'reviews/rac-rmot05r-evidence/plan/junction_sets.npz', 'reviews/rac-rmot05r-evidence/plan/junction_selection.json', 'reviews/rac-rmot05r-evidence/repair/R3/GO-05R-R3_maps.npz',
              'reviews/rac-rmot05r-evidence/repair/R3/GO-05R-R3_face_labels.npy', 'tools/rac/w1/rmot05r_drivers/r_verify.py', 'tools/rac/w1/rmot05r_drivers/r_repair.py', 'tools/rac/w1/rmot05r_drivers/r_select.py',
              'reviews/rac-rmot05q-evidence/source/F1_face_indices.npz', 'tools/rac/w1/rmot05q_drivers/q_extract.py']
    res['replay_inputs_exist'] = {p: os.path.exists(os.path.join(root, p)) for p in inputs}
    r = subprocess.run(['bash', 'replay_package.sh'], cwd=root, capture_output=True, text=True, env=dict(os.environ, OUT=os.path.join(iso, 'replay_out')))
    res['replay_from_package'] = dict(returncode=r.returncode, stdout=r.stdout.strip()[-1500:], stderr=r.stderr.strip()[-800:],
                                      limitations='renders and the .blend rebuild (bpy) and the base.glb extraction check are not part of the scripted replay; base.glb is external')
    res['pass'] = bool(res['manifest']['all_present'] and res['manifest']['all_hashes_equal'] and not res['manifest']['unlisted_files'] and not res['manifest']['listed_but_missing']
                       and res['decoded_meshes']['all_equal'] and not bad and all(res['replay_inputs_exist'].values()) and r.returncode == 0)
    json.dump(res, open(a.receipt, 'w'), indent=1); print(json.dumps(res, indent=1))

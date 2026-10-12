# RAC RM-OT-05G SCULPTOR RELEASE packager + clean-copy verifier (repeatable; no Blender needed).
#
#   python3 tools/rac/w1/rmot05g_blender/g_release.py build  [--out DIR]     -> DIR/gorrund-sculpt-release-<commit12>.zip (+ .sha256)
#                                                                              and reviews/rac-rmot05g-release/RELEASE_MANIFEST.json
#   python3 tools/rac/w1/rmot05g_blender/g_release.py verify ZIP            -> extracts into an empty temp folder OUTSIDE the repository
#                                                                              and checks it there (exit 0 = release complete)
# The release is exactly the committed folder reviews/rac-rmot05f-handoff/ (which contains START_HERE.md and an exact frozen copy of the
# production brief) plus RELEASE_MANIFEST.json at the archive root. The build refuses to run if that folder has uncommitted changes, so the
# manifest's source commit is the true content. The zip is deterministic: sorted entries, fixed timestamps and permissions, deflate.
# Verify (clean copy, no repository access): every manifest file present with its SHA-256; required paths present; frozen hashes (template,
# brief copy, regions, joints) as recorded; blender/scripts/SHA256SUMS.txt matches; every Markdown link and every package-internal path
# named in back-ticks in the .md files resolves inside the copy; the standalone preflight runs from the copy (isolated Python) on the copy's
# own template and passes, with and without --package.
import os, sys, json, hashlib, zipfile, subprocess, tempfile, re, shutil
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
SRC = 'reviews/rac-rmot05f-handoff'
FROZEN = {'template/GO_ref_route_r6.obj': 'd0eb0d1643d135f3d5bd0920a9d6007f6dec8d1238530b30b298f3a1b2034eee',
          'template/GO_true_floor_r6.obj': 'c6edbb98a8c4a93dd4c4cb0c615a29c5ba9133b4ce05aa7feef58d9190b288c2',
          'data/regions.json': '62833d43f79e7e1efeb9a64f4c8452a182db39b548392dfcc01da285be5b3ae2',
          'data/joints_r6.json': 'f23a676c13b4b60da02e5a2f4ce6f543a9f4212def579494fc8f0faf524e0d1c',
          'brief/gorrund-rm-ot-05f-hand-sculpt-production-brief.md': '22bedaa07ee3020996df3f608e6ec3470812953ae4d2f9d3fac5ece23c61db0c'}
REQUIRED = ['START_HERE.md', 'README.md', 'brief/gorrund-rm-ot-05f-hand-sculpt-production-brief.md', 'template/GO_ref_route_r6.obj',
            'template/GO_true_floor_r6.obj', 'template/GO_low_route_r6.obj', 'template/GO_old_lean_r6.obj', 'data/regions.json', 'data/joints_r6.json',
            'data/stations.json', 'figures/region_map.png', 'figures/floor_margin.png', 'blender/README.md', 'blender/CHECKLIST_SCULPTOR.md',
            'blender/CHECKLIST_DELIVERY.md', 'blender/MANIFEST_TEMPLATE.json', 'blender/scripts/g_setup.py', 'blender/scripts/g_export.py',
            'blender/scripts/g_preview.py', 'blender/scripts/g_views.py', 'blender/scripts/g_preflight.py', 'blender/scripts/SHA256SUMS.txt'] + \
           ['blender/transport/GO_%s_%s' % (s, f) for s in ('low', 'narrow', 'broad') for f in ('route_r6.obj', 'true_floor_r6.obj', 'transport.npz')]
TOP = ('template', 'data', 'figures', 'evidence', 'blender', 'brief', 'validator_selftest', 'START_HERE.md', 'README.md')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, check=True).stdout.strip()
def build(out):
    dirty = git('status', '--porcelain', '--', SRC)
    if dirty: sys.exit('REFUSED: uncommitted changes under %s:\n%s' % (SRC, dirty))
    commit = git('rev-parse', 'HEAD'); date = git('show', '-s', '--format=%cI', commit)
    root = os.path.join(REPO, SRC); files = []
    for d, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f); files.append((os.path.relpath(p, root).replace(os.sep, '/'), p))
    files.sort()
    rid = 'gorrund-sculpt-release-' + commit[:12]
    man = {'release_id': rid, 'order': 'reviews/chatgpt-rac-rm-ot-05g-handoff-acceptance-sculptor-release-order.md', 'source_repository': 'Jambi92/wayfarer-design',
           'source_commit': commit, 'source_commit_date': date, 'source_folder': SRC, 'entry_point': 'rac-rmot05f-handoff/START_HERE.md',
           'status': 'Gorrund EXTERNAL SCULPT REQUIRED - AWAITING ASSET; RM-OT-05 OPEN; Stage C blocked; Grask E3 frozen. Not an accepted body.',
           'frozen_sha256': FROZEN, 'repository_brief_sha256': sha(os.path.join(REPO, 'reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md')),
           'required_paths': REQUIRED, 'files': [{'path': r, 'sha256': sha(p), 'bytes': os.path.getsize(p)} for r, p in files]}
    for r, h in FROZEN.items():
        got = next(x['sha256'] for x in man['files'] if x['path'] == r)
        if got != h: sys.exit('REFUSED: frozen file changed: %s %s != %s' % (r, got, h))
    if man['repository_brief_sha256'] != FROZEN['brief/gorrund-rm-ot-05f-hand-sculpt-production-brief.md']: sys.exit('REFUSED: brief copy differs from the repository brief')
    os.makedirs(out, exist_ok=True); zp = os.path.join(out, rid + '.zip'); mj = json.dumps(man, indent=1).encode()
    ts = (2026, 10, 12, 0, 0, 0)
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        def add(name, data):
            zi = zipfile.ZipInfo(name, ts); zi.compress_type = zipfile.ZIP_DEFLATED; zi.external_attr = 0o644 << 16; z.writestr(zi, data)
        add(rid + '/RELEASE_MANIFEST.json', mj)
        for r, p in files: add(rid + '/rac-rmot05f-handoff/' + r, open(p, 'rb').read())
    zsha = sha(zp); open(zp + '.sha256', 'w').write('%s  %s\n' % (zsha, os.path.basename(zp)))
    md = os.path.join(REPO, 'reviews/rac-rmot05g-release'); os.makedirs(md, exist_ok=True); open(os.path.join(md, 'RELEASE_MANIFEST.json'), 'wb').write(mj)
    print(json.dumps({'release': zp, 'zip_sha256': zsha, 'zip_bytes': os.path.getsize(zp), 'files': len(files), 'source_commit': commit}, indent=1))
def links(md_path, root):
    """Markdown links must resolve; back-ticked package-internal paths must resolve (relative to the file, else to the package root)."""
    txt = open(md_path).read(); here = os.path.dirname(md_path); bad, ok, external = [], 0, []
    for m in re.finditer(r'\]\(([^)\s]+)\)', txt):
        t = m.group(1).split('#')[0]
        if not t or t.startswith(('http://', 'https://', 'mailto:')): continue
        (ok := ok + 1) if os.path.exists(os.path.normpath(os.path.join(here, t))) else bad.append(('link', t))
    for m in re.finditer(r'`([^`\s]+)`', txt):
        t = m.group(1).rstrip('.,;:')
        if any(c in t for c in '<>*{}|') or '/' not in t or t.startswith(('http', '-')): continue
        if t.startswith('reviews/rac-rmot05f-handoff/'): t2 = t[len('reviews/rac-rmot05f-handoff/'):]
        elif t.startswith(('tools/', 'reviews/', 'specs/', 'decisions/')): external.append(t); continue
        else: t2 = t
        first = t2.split('/')[0]
        if first not in TOP and first not in ('..', '.', 'scripts', 'transport', 'tooling_evidence', 'views', '05d', '05e'): continue
        cand = [os.path.normpath(os.path.join(here, t2)), os.path.normpath(os.path.join(root, t2)), os.path.normpath(os.path.join(root, 'blender', t2))]
        if t2.startswith('views/'): continue                     # produced by the sculptor next to the working .blend
        (ok := ok + 1) if any(os.path.exists(c) for c in cand) else bad.append(('path', t))
    return ok, bad, sorted(set(external))
def verify(zp):
    tmp = tempfile.mkdtemp(prefix='rac_release_clean_')     # outside the repository; no repository access needed
    try:
        with zipfile.ZipFile(zp) as z: z.extractall(tmp)
        rid = os.listdir(tmp)[0]; base = os.path.join(tmp, rid); root = os.path.join(base, 'rac-rmot05f-handoff')
        man = json.load(open(os.path.join(base, 'RELEASE_MANIFEST.json'))); res = {'zip_sha256': sha(zp), 'release_id': man['release_id'], 'source_commit': man['source_commit']}
        res['files_hash_match'] = all(os.path.exists(os.path.join(root, f['path'])) and sha(os.path.join(root, f['path'])) == f['sha256'] for f in man['files'])
        res['no_extra_files'] = sorted(os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/') for d, _, fs in os.walk(root) for f in fs) == sorted(f['path'] for f in man['files'])
        res['required_present'] = {r: os.path.exists(os.path.join(root, r)) for r in man['required_paths'] if not os.path.exists(os.path.join(root, r))} or 'all'
        res['frozen_hashes'] = {r: sha(os.path.join(root, r)) == h for r, h in man['frozen_sha256'].items()}
        sums = {l.split()[1]: l.split()[0] for l in open(os.path.join(root, 'blender/scripts/SHA256SUMS.txt')) if l.strip()}
        res['script_sums_match'] = all(sha(os.path.join(root, 'blender/scripts', f)) == h for f, h in sums.items())
        lk = {}
        for d, _, fs in os.walk(root):
            for f in fs:
                if f.endswith('.md'):
                    ok, bad, ext = links(os.path.join(d, f), root); lk[os.path.relpath(os.path.join(d, f), root)] = {'resolved': ok, 'unresolved': bad, 'repository_side_references': ext}
        res['links'] = lk; res['links_all_resolve'] = all(not v['unresolved'] for v in lk.values())
        pf = os.path.join(root, 'blender/scripts/g_preflight.py'); tpl = os.path.join(root, 'template/GO_ref_route_r6.obj')
        r1 = subprocess.run([sys.executable, '-I', pf, tpl, '--package', root], capture_output=True, text=True, cwd=tmp)
        r2 = subprocess.run([sys.executable, '-I', pf, tpl], capture_output=True, text=True, cwd=tmp)
        res['preflight_from_copy'] = {'with_package_arg': r1.stdout.strip().splitlines()[-1] if r1.stdout else r1.stderr[-300:],
                                      'auto_root': r2.stdout.strip().splitlines()[-1] if r2.stdout else r2.stderr[-300:]}
        res['COMPLETE'] = bool(res['files_hash_match'] and res['no_extra_files'] and res['required_present'] == 'all' and all(res['frozen_hashes'].values())
                               and res['script_sums_match'] and res['links_all_resolve'] and res['preflight_from_copy']['with_package_arg'] == 'PREFLIGHT PASS'
                               and res['preflight_from_copy']['auto_root'] == 'PREFLIGHT PASS')
        return res
    finally: shutil.rmtree(tmp, ignore_errors=True)
if __name__ == '__main__':
    if sys.argv[1] == 'build':
        build(sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.join(REPO, 'build_release'))
    elif sys.argv[1] == 'verify':
        r = verify(sys.argv[2]); print(json.dumps(r, indent=1)); print('RELEASE', 'COMPLETE' if r['COMPLETE'] else 'INCOMPLETE'); sys.exit(0 if r['COMPLETE'] else 1)

# du2_immutables.py OUT.txt BASE_COMMIT : RP4 v002 immutable-input check (order 8080f9f §17.15 / §16.13). Every accepted source, frozen family-base
# input and frozen-race record is re-hashed and compared with (a) the RP4 pilot record (immutable_hashes.txt) and (b) the file at BASE_COMMIT (git), and
# the working tree diff of those paths since BASE_COMMIT is listed (must be empty).
import sys, hashlib, subprocess, os
OUT, BASE = sys.argv[1:3]; R = '/home/claude/wayfarer-design'
sha = lambda p: hashlib.sha256(open(os.path.join(R, p), 'rb').read()).hexdigest()
def git_sha(p):
    try: b = subprocess.run(['git', '-C', R, 'show', '%s:%s' % (BASE, p)], capture_output=True, check=True).stdout; return hashlib.sha256(b).hexdigest()
    except subprocess.CalledProcessError: return None
prior = {}
for l in open(os.path.join(R, 'reviews/rac-rp4-evidence/durrim/immutable_hashes.txt')):
    if l.startswith('#') or not l.strip(): continue
    h, p = l.split()[:2]; prior[p] = h
P = ['reviews/reference-assets/builds/%s_build.json' % i for i in ('DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT', 'MF-M-R', 'MF-F-R')] + \
    ['reviews/reference-assets/r6/%s_r6.npz' % i for i in ('DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT', 'MF-M-R', 'MF-F-R')] + \
    ['reviews/rac-rp4-evidence/durrim/partA/DUF137C-NAT_build.json', 'reviews/rac-rp4-evidence/durrim/partA/DUF137C-NAT_r6.npz', 'reviews/rac-rp4-evidence/durrim/partA/MF152-NAT_build.json',
     'reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/MPFB_FAMILY_BASE_v005_FREEZE.json', 'reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/maps/MPFB_FAMILY_BASE_v005_hm08_map.npz',
     'reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/maps/MPFB_FAMILY_BASE_v005_core.npz'] + \
    [l for l in subprocess.run(['git', '-C', R, 'ls-files'], capture_output=True, text=True).stdout.split() if l.endswith('_FREEZE.json')]
lines = ['# RP4 Durrim v002 revision / closure: immutable inputs (sha256) vs RP4 pilot record and vs %s' % BASE]; ok = True
for p in sorted(set(P)):
    h = sha(p); g = git_sha(p); pr = prior.get(p); st = 'UNCHANGED' if (g == h and (pr is None or pr == h)) else 'CHANGED'; ok &= st == 'UNCHANGED'
    lines.append('%s  %s  %s%s' % (h, p, st, '' if pr is None else ' (= pilot record)' if pr == h else ' (PILOT RECORD %s)' % pr))
lines.append('# v005 production blend MF_M_REF_RP3_retopo_v005.blend: not re-read in this cloud session (never opened for writing; E: untouched); its hm08 map and face core '
             'above are the frozen values (map = %s)' % ('frozen' if sha('reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/maps/MPFB_FAMILY_BASE_v005_hm08_map.npz') == prior.get('/mnt/user-data/outputs/rp5/MF_M_REF_RP3_retopo_v005_hm08_map.npz') else 'MISMATCH'))
d = subprocess.run(['git', '-C', R, 'diff', '--name-only', BASE, '--'] + sorted(set(P)), capture_output=True, text=True).stdout.split()
lines.append('# working-tree changes to these paths since %s: %s' % (BASE, d or 'none')); lines.append('# ALL UNCHANGED: %s' % (ok and not d))
open(OUT, 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines[-3:]))

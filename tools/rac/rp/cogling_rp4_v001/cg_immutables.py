# cg_immutables.py OUT.txt [REF] [EXTRA_PATH...] : RP4 Cogling gate (order 9424c72 §22.17) -- immutable inputs vs the order commit 9424c72 (git): every path checked by the Pipkin freeze
# closure (MPFB Family Base v005, frozen Durrim RP4, all *_FREEZE.json records incl. Pipkin RP4, Skarn family freeze report, accepted Pipkin sources) + the frozen
# Pipkin RP4 production files and branch, + the accepted Cogling sources (CGJ7 / CG76H-NAT / CG107-NAT r6 + build records; CG76-NAT provenance) and Cogling canon.
import re, glob, hashlib, subprocess, sys
R = '/home/claude/wayfarer-design'; OUT = sys.argv[1]; REF = sys.argv[2] if len(sys.argv) > 2 else '9424c72'
paths = [l.split()[1] for l in open(R + '/reviews/rac-rp4-evidence/pipkin/final/immutable_hashes_freeze_closure.txt') if re.match(r'^[0-9a-f]{64}\s', l)]
paths += ['reviews/rac-rp4-evidence/pipkin/final/PIPKIN_RP4_FREEZE.json', 'reviews/rac-rp4-evidence/pipkin/branch/MPFB_PIPKIN_COMPACT_BRANCH_v001.json',
          'reviews/rac-rp4-evidence/durrim/v002/branch/MPFB_COMPACT_BRANCH_v002.json', 'specs/cogling/COGLING_V1.md', 'specs/pipkin/PIPKIN_V1.md']
for i in ('CGJ7', 'CG76H-NAT', 'CG107-NAT', 'CG76-NAT'): paths += ['reviews/reference-assets/r6/%s_r6.npz' % i, 'reviews/reference-assets/builds/%s_build.json' % i]
paths += sorted(p[len(R) + 1:] for p in glob.glob(R + '/reviews/rac-rp4-evidence/pipkin/final/production/*'))
paths += sys.argv[3:]; paths = list(dict.fromkeys(paths)); out = ['# RP4 Cogling gate: immutable inputs vs %s (git)' % REF]; bad = 0
for p in paths:
    h = hashlib.sha256(open(R + '/' + p, 'rb').read()).hexdigest(); g = hashlib.sha256(subprocess.run(['git', '-C', R, 'show', '%s:%s' % (REF, p)], capture_output=True).stdout).hexdigest()
    ok = h == g; bad += not ok; out.append('%s  %s  %s' % (h, p, 'UNCHANGED' if ok else 'CHANGED'))
out.append('# %d / %d UNCHANGED' % (len(paths) - bad, len(paths))); open(OUT, 'w').write('\n'.join(out) + '\n'); print(out[-1])

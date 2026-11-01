# cr_head.py : accepted head creator-support states on the canonical base face list (order 236dddc §12), built with the accepted W3B route
#   (level-set transfer of the canonical head vertices onto the modified skull SDF; same topology):
#   orbit spacing IOD -8 % (dx local -0.372) / +3 % (dx +0.128) (W3B tables: IOD -4.4 % @ -0.20, -8.6 % @ -0.40, +4.7 % @ +0.20; linear interpolation);
#   ridge strength m = 0.90 (lower usable at canonical relief) / 1.30 (upper accepted) on every structural-ridge family (W3B1 final acceptance §2).
import sys, os, numpy as np; np.trapz = np.trapezoid
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w3b_drivers')
import w3b_common as C, w3b_ridge as RG
out = '/tmp/claude-0/rt/sa/'
for tag, dx in (('ORB-8', -0.372), ('ORB+3', 0.128)):
    f = out + 'cr_%s.npy' % tag
    if not os.path.exists(f):
        P = C.level_set_transfer(lambda Q: C.sdf(Q, eye_dx=dx), pre=lambda Q: C.orbit_shift_points(Q, dx)); np.save(f, P.astype(np.float32)); print(tag, flush=True)
for tag, m in (('RDG0.90', 0.90), ('RDG1.30', 1.30)):
    f = out + 'cr_%s.npy' % tag
    if not os.path.exists(f):
        P = RG.build({k: m for k in RG.FAMS}); np.save(f, P.astype(np.float32)); print(tag, flush=True)
print('DONE')
# display-root states (§12): accepted Cranial Keratin Display family structures of head65 (frozen-skull display variants, Gate 7 closure) added to the
# W3B skull field as smin(skull, keratin, 0.5) in the same head-local frame; transferred onto the canonical head vertices along their normals
# (W3B ridge convention, no tangential sliding). LOW = minimal_ridges (near-naked end); HIGH STRUCTURAL = restrained crest (CREST_H 2.40 cm, accepted 2.43 cm).
os.environ['BROW_INT'] = '5'
sys.path.insert(0, '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w2i/rodin/g1')
import wf_saurin_head65 as H65
from wf_saurin_head61 import smin
for tag, name in (('DSP-LOW', 'minimal_ridges'), ('DSP-HIGH', 'crest')):
    f = out + 'cr_%s.npy' % tag
    if os.path.exists(f): continue
    D = H65.build(name)
    def fn(Q, D=D):
        d = C.sdf(Q); X, Fh, U = Q[:, 0], Q[:, 1], Q[:, 2]; k = (np.abs(X) < 9) & (Fh > -22) & (Fh < 9) & (U > 2)
        if k.any(): d = d.copy(); d[k] = smin(d[k], D(X[k], Fh[k], U[k]), 0.5)
        return d
    P = C.level_set_transfer(fn, along_normal=True, iters=8); np.save(f, P.astype(np.float32)); print(tag, flush=True)
print('DONE2')

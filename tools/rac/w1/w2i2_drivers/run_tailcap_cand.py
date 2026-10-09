# RAC W2I2 §10 (tail-base / coupling regression on the combined candidate): runs the unchanged W2I1 sa_tailcap2.py (same-state D2 rule) with the
# accepted build replaced IN MEMORY by build + candidate limb warps (sa_cand fa_remap / leg_remap at the reference stature).
# Usage: CAND=L1+F2 STATES=.. TGT=rsi119 python3 run_tailcap_cand.py OUT.json
import sys, os, runpy
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_cand as SC, sa_w2i2_build as WB, sa_joints as SJ
cand = WB.combo(os.environ.get('CAND', 'L1+F2')); _orig = SC.C.build
def build(q):
    P, q2 = _orig(q)
    if cand.get('fa_delta'):
        J, _ = SJ.transport(P, SC.JW); P, _ = SC.fa_remap(P, J, cand['fa_delta'])
    if cand.get('G'): P, q2, _ = SC.leg_remap(P, q2, cand['G'], cand.get('FT', 0.4))
    return P, q2
SC.C.build = build
sys.argv = [os.path.join(os.path.dirname(D), 'w2i_drivers', 'sa_tailcap2.py')] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')

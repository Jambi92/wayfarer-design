# RAC W2I5 §10 tail-coupling regression (W2I4 route + W2I5 sculpt delta); W2I4 header:
# RAC W2I4 §13 tail-coupling confirmation: runs the unchanged W2I1 sa_tailcap2.py (same-state D2 rule) with the accepted build replaced IN MEMORY
# by the W2I4 final asset build (W2I3 rebuild fields fa_rebuild / leg_rebuild + W2I4 finish delta). Usage: TGT=rsi119 [SCULPT=0] python3 run_tailcap_fin.py OUT.json
import sys, os, runpy
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import sa_sculpt as SC5; import sa_finish as FN; _BUILD4 = FN.build_f; FN.build_f = SC5.build_s   # W2I5: final route = W2I4 route + W2I5 sculpt delta
import sa_joints as SJ
RB = FN.RB; _orig = FN.C.build; DF = FN.finish_delta()[0] + SC5.final_delta()[0] * float(os.environ.get('SCULPT', '1'))   # SCULPT=0: W2I4 control
def build(q):
    P, q2 = _orig(q)
    J, _ = SJ.transport(P, RB.JW); P, _ = RB.fa_rebuild(P, J, RB.TARGET['fa_delta'])
    P, q2, _ = RB.leg_rebuild(P, q2, RB.TARGET['G'], RB.TARGET['FT'])
    return P + DF, q2
FN.C.build = build
sys.argv = [os.path.join(os.path.dirname(D), 'w2i_drivers', 'sa_tailcap2.py')] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')

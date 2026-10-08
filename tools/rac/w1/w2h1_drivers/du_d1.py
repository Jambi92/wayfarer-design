# RAC W2H1 (W2H closure): the author-approved bounded Durrim correction D1 (reviews/chatgpt-rac-w2h1-durrim-pelvic-closure-order.md §2):
# Durrim-specific pelvic AP depth write = pelvis bone Z x1.04 on the DU-NAT construction (the W2H diagnostic probe DU152P4 construction; DU-NAT
# pelvis [1, 0.9, 1] -> [1, 0.9, 1.04]). Nothing else changes: same targets, same native short-adult route, same frame rule (Broad pelvis X x1.08),
# same composition states. Bodies: corrected family DU122C / DU137C / DU152C, frames, composition at 137, Narrow-low named body, DU-P4 composition
# bodies at 152. Usage: python3 du_d1.py JOBSET (stature | frames | comp | named | p4)
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'w2h_drivers'))
_argv = sys.argv; sys.argv = ['x', 'none']
import sr_build as M
sys.argv = _argv
from concurrent.futures import ThreadPoolExecutor
M.W = M.S + '/w2h1'; W = M.W
D1 = [1.0, 0.9, 1.04]
def dcfg(h, nid):
    c = M.native_cfg("DU", h, nid); bs = dict(c.get("bone_scales", {})); assert bs.get("pelvis") == [1.0, 0.9, 1.0], bs
    bs["pelvis"] = D1; c["bone_scales"] = bs; c["d1"] = "W2H1 D1: pelvis bone Z x1.04 (author-approved bounded Durrim correction)"; return c
B = lambda h: W + '/st/DU%dC-NAT_build.json' % h
def jobs(which):
    J = []
    if which == 'stature':
        for h in (122, 137, 152): J.append((M.native, (dcfg(h, 'DU%dC' % h), W + '/st')))
    if which == 'frames':
        for h in (122, 137, 152):
            for tag in ("N", "B"): J.append((M.variant, (B(h), M.frame(B(h), M.FR["DU"][tag]), W + '/fr', 'DU%s%dC' % (tag, h))))
    if which == 'comp':
        for nm, m, w in M.COMP: J.append((M.variant, (B(137), {"muscle": m, "weight": w}, W + '/comp', 'DU137C-' + nm)))
    if which == 'named':
        J.append((M.variant, (W + '/fr/DUN137C_build.json', {"muscle": 0.25, "weight": 0.25}, W + '/nm', 'DUNLOWC')))
    if which == 'p4':
        for nm, m, w in (("LOW", 0.25, 0.25), ("MIN", 0, 0), ("HIBOTH", 1, 1)): J.append((M.variant, (B(152), {"muscle": m, "weight": w}, W + '/p4', 'DU152C-' + nm)))
    return J
if __name__ == '__main__':
    os.makedirs(W + '/logs', exist_ok=True)
    J = jobs(sys.argv[1])
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
    print('DONE', sys.argv[1], len(J))

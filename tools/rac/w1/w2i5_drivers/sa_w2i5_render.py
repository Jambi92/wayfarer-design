# RAC W2I5 §5 sheets (accepted rclose.py Workbench shaded reference with cavity, via the W2I4 render helpers). Thigh comparison W2I3 (stretched)
# / W2I4 (partial finish) / W2I5 (final) at matched camera and scale for SA-M188 and SA-F188 - front, lateral, rear, medial / adductor,
# hip-to-thigh, knee-to-thigh, front 3/4, rear 3/4 - on base meshes (relief read directly) and on the surfaced finals; final SA-M188 /
# SA-F188 sheets and the 168 / 188 / 203 / 208 family on the W2I5 surfaced asset. Usage: python3 sa_w2i5_render.py all
import sys, os, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import sa_sculpt as SC5; import sa_finish as FN
import sa_w2i4_render as R4
RB = FN.RB; B = FN.B; S = FN.C.S
R4.W = S + '/w2i5/rend'; R4.SH = S + '/w2i5/sheets'; os.makedirs(R4.W, exist_ok=True); os.makedirs(R4.SH, exist_ok=True)
Fu = R4.Fu; _s5 = None
def relief5():
    global _s5
    if _s5 is None:
        Vu = np.load(S + '/w2i5/surf/fin_up.npz')['V'].astype(float); d = np.load(S + '/w2i5/surf/saurin_w2i5_surface_delta.npz')['d'].astype(float)
        _s5 = (d * igl.per_vertex_normals(Vu, Fu)).sum(1)
    return _s5
def fin5(p, h=None): return R4.surfaced(SC5.build_s(p, h)[0], relief5())
def fin4(p, h=None): return R4.surfaced(FN.build_f(p, h)[0], w4relief())
_s4 = None
def w4relief():
    global _s4
    if _s4 is None:
        Vu = np.load(S + '/w2i4/surf/fin_up.npz')['V'].astype(float); d = np.load(S + '/w2i4/surf/saurin_w2i4_surface_delta.npz')['d'].astype(float)
        _s4 = (d * igl.per_vertex_normals(Vu, Fu)).sum(1)
    return _s4
TH = ("tfront:0:0:12:0:80:46;tlat:90:0:14:0:80:46;trear:180:0:12:0:80:46;tmed:-60:0:6:0:78:40;thip:150:15:12:-6:92:40;tknee:15:-10:14:0:62:36;"
      "tf34:35:0:12:0:80:50;tr34:145:0:12:0:80:50")
THL = ['front thigh', 'lateral thigh', 'rear thigh', 'medial / adductor', 'hip-to-thigh (gluteal / crease)', 'knee-to-thigh', 'front 3/4', 'rear 3/4']
def thigh_sheet(sx, p, surfaced):
    rows = []
    sfx = 'S' if surfaced else 'B'
    for tag, lab, fn_ in (('W2I3', 'W2I3 rebuild (stretched thigh relief x1.5)', (lambda: R4.surfaced(RB.build_r(p, RB.TARGET)[0], R4.relief_frozen())) if surfaced else (lambda: RB.build_r(p, RB.TARGET)[0])),
                          ('W2I4', 'W2I4 partial finish (anterior / lateral native; medial / posterior stretched)', (lambda: fin4(p)) if surfaced else (lambda: FN.build_f(p)[0])),
                          ('W2I5', 'W2I5 evaluated candidate (medial / posterior band re-formed under the fold guard; see report part 3)', (lambda: fin5(p)) if surfaced else (lambda: SC5.build_s(p)[0]))):
        b = R4.mesh('W2I5-TH%s-%s-SA-%s188' % (sfx, tag, sx), fn_); rows.append(R4.row(R4.views(b, TH, 500), THL, lab, 420))
    R4.sheet('w2i5_thigh_%s_SA-%s188.jpg' % ('surfaced' if surfaced else 'base', sx), rows,
             'Thigh W2I3 / W2I4 / W2I5, SA-%s188, matched camera and scale (%s)' % (sx, 'surfaced with each version\'s scale field' if surfaced else 'base meshes: relief read directly'), 0.55)
if __name__ == '__main__':
    FV = ['front', 'side (left)', 'side (right)', 'front 3/4', 'rear 3/4', 'rear']
    for sx, p in (("M", {}), ("F", B.CEN)):
        thigh_sheet(sx, p, False); thigh_sheet(sx, p, True)
        b = R4.mesh('W2I5-SA-%s188-FINAL' % sx, lambda p=p: fin5(p))
        R4.sheet('w2i5_SA-%s188_final.jpg' % sx, [R4.row(R4.views(b, R4.FULL), FV, 'W2I5 evaluated candidate SA-%s188 (NOT canonicalized; neutral carriage)' % sx),
                                                 R4.row(R4.views(b, R4.close(188.0)), R4.CL, 'close views')], 'W2I5 evaluated candidate SA-%s188 (not canonical) — shaded reference (Workbench + cavity)' % sx, 0.55)
    fam = []
    for h in (168, 188, 203, 208):
        b = R4.mesh('W2I5-SA-M%d-FINAL' % h, lambda h=h: fin5({}, float(h) if h != 188 else None)); fam.append(R4.row(R4.views(b, R4.FULL), FV, 'SA-M%d W2I5 candidate (regional route)' % h, 400))
    R4.sheet('w2i5_family.jpg', fam, 'W2I5 evaluated candidate family 168 / 188 / 203 / 208 (same regional construction route; surfaced)', 0.7)

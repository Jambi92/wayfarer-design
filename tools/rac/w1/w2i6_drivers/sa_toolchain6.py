# RAC W2I6 §5 tool-chain reconciliation for the canonical W2 reference = the accepted W2I4 candidate (sa_finish.build_f); the W2I5
# procedural thigh delta is NOT used (no sa_sculpt import). Derived from the prepared W2I5 sa_toolchain5.py. Original header:
# RAC W2I5 §13 tool-chain reconciliation (run only after the §12 conditions pass). Writes the W2 counterparts BESIDE the W1 tool-chain
# files (W1 files are provenance and stay unchanged) into tools/rodin/w2/:
#   ref_metrics_w2.json      Part 7 reference metrics (the keys of tools/rodin/creator-biology/ref_metrics.json) measured on W2 SA-M188
#   axis_w2.npy              Gate 8 tail centreline of the W2 reference (the build's carried axis; tail system unchanged, pelvis-carried)
#   g7geo_w2_points.json     g7geo ARM / LEG construction points (S / E / W, H / K / A) on the W2 reference (J-2 affine transport; hip also
#                            given at the pelvic station) + the hand pad / claw anchor offset used by g7surfc_moved
#   lbase_w2_stations.json   Lbase stations: indices unchanged (identical topology), W2 heights
#   s263_w2.json             §263 accounting re-verification on the W2 reference: lower trunk, external pelvic width, thoracic d/w, head
#                            length / H (geometry) and the front-silhouette waist / shoulder, waist / hip (W1 torsosil.py method; bands
#                            carried with the stations) for male centre, female centre and reference female, W1 vs W2
# Usage: python3 sa_toolchain5.py OUTDIR
import sys, os, json, subprocess, numpy as np
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers')); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i2_drivers'))
import sa_finish as FN; import sa_cand as SCc
RB = FN.RB; B = FN.B; L = FN.L; V0 = FN.V0; S = FN.C.S
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
REFK = list(json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(D))), 'rodin', 'creator-biology', 'ref_metrics.json'))).keys())
P, q, k, _ = FN.build_f({}); M = B.measure(P, q, k); M0 = B.measure(*RB.build_r({}, {})[:3])
json.dump({kk: float(M[kk]) for kk in REFK}, open(OUT + '/ref_metrics_w2.json', 'w'), indent=1)
np.save(OUT + '/axis_w2.npy', np.asarray(q['_C2'], float))
J, U = SCc.joints_c(P); J0, _ = SCc.joints_c(RB.build_r({}, {})[0])
pts = {}
for sg, nm in ((1, 'L'), (-1, 'R')):
    hand = (L.hand > 0.5) & (L.side == sg) if hasattr(L, 'hand') else (L.arm > 0.95) & (L.side == sg) & (V0[:, 2] < 100)
    pts[str(sg)] = dict(ARM={kk: J[kk + nm].round(3).tolist() for kk in ('S', 'E', 'W')}, LEG={'H_B1_axis': J['HB' + nm].round(3).tolist(), 'H_pelvic_station': J['H' + nm].round(3).tolist(),
                        'K': J['K' + nm].round(3).tolist(), 'A': J['A' + nm].round(3).tolist()},
                        hand_anchor_offset_cm=(P[hand] - V0[hand]).mean(0).round(3).tolist(), W1_ARM={kk: J0[kk + nm].round(3).tolist() for kk in ('S', 'E', 'W')},
                        W1_LEG={kk: J0[kk + nm].round(3).tolist() for kk in ('K', 'A')})
json.dump(dict(note='W2 counterparts of tools/rodin/gate1/g7geo.py ARM / LEG (key +1 = +x side); W1 g7geo.py unchanged (provenance)', points=pts), open(OUT + '/g7geo_w2_points.json', 'w'), indent=1)
json.dump(dict(note='Lbase station vertex indices are unchanged (identical topology); heights are the W2 reference values', indices={kk: int(v) for kk, v in B.ST.items()},
               W1_u={kk: float(M0['u_' + kk]) for kk in B.ST}, W2_u={kk: float(M['u_' + kk]) for kk in B.ST}), open(OUT + '/lbase_w2_stations.json', 'w'), indent=1)
# §263 re-verification
import fsets3
RC = S + '/w2i/rodin/g1/rclose.py'; R = S + '/w2i6/s263'; os.makedirs(R, exist_ok=True)
def render(tag, Pb):
    fn = R + '/%s.npz' % tag; np.savez(fn, P=Pb.astype(np.float32), f=FN.F0.astype(np.int32))
    subprocess.run(['python3', RC], env=dict(os.environ, VIEWS='front:0:0:0:0:94:216', NPZ=fn, TAG=R + '/' + tag, RES='600'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return np.array(Image.open(R + '/%s_front.png' % tag).convert('RGBA'))[:, :, 3] > 127
def sil(a, H, bands):
    PX = 216 / 600.0; rows = np.where(a.any(1))[0]; top, bot = rows.min(), rows.max(); cx = 300; W = np.zeros(600)
    for r in range(600):
        if not a[r, cx]: continue
        l = cx
        while l > 0 and a[r, l - 1]: l -= 1
        rr = cx
        while rr < 599 and a[r, rr + 1]: rr += 1
        W[r] = (rr - l + 1) * PX
    u = (bot - np.arange(600)) * PX * H / ((bot - top) * PX)
    g = lambda ab, f: f(W[(u > ab[0]) & (u < ab[1])])
    sh = g(bands['sh'], np.max); wa = g(bands['wa'], np.min); hp = g(bands['hp'], np.max)
    return dict(shoulder=float(sh), waist=float(wa), hip=float(hp), waist_sh=float(wa / sh), waist_hip=float(wa / hp))
res = {}
for tag, p in (('male_centre', {}), ('female_centre', fsets3.CEN), ('reference_female', fsets3.REF)):
    P1, q1, k1, _ = RB.build_r(p, {}); P2, q2, k2, _ = FN.build_f(p); m1 = B.measure(P1, q1, k1); m2 = B.measure(P2, q2, k2)
    W1b = dict(sh=(140, 152), wa=(104, 124), hp=(84, 98))                                  # W1 torsosil bands
    dsh = m2['u_inlet'] - m1['u_inlet']; dlo = m2['u_platform'] - m1['u_platform']
    W2b = dict(sh=(140 + dsh, 152 + dsh), wa=(104 + dlo, 124 + dlo), hp=(84 + dlo, 98 + dlo))   # same anatomy: bands carried with the stations
    s1 = sil(render('W1_' + tag, P1), m1['height'], W1b); s2 = sil(render('W2_' + tag, P2), m2['height'], W2b)
    res[tag] = dict(W1=dict(lower_trunk=m1['lower_trunk'], pelvis_w=m1['pelvis_w'], thorax_d_over_w=m1['thorax_d_over_w'], head_len_over_H=m1['head_len_over_H'], **s1),
                    W2=dict(lower_trunk=m2['lower_trunk'], pelvis_w=m2['pelvis_w'], thorax_d_over_w=m2['thorax_d_over_w'], head_len_over_H=m2['head_len_over_H'], **s2), bands_W2=W2b)
    print(tag, {kk: (round(res[tag]['W1'][kk], 4), round(res[tag]['W2'][kk], 4)) for kk in res[tag]['W1']}, flush=True)
json.dump(res, open(OUT + '/s263_w2.json', 'w'), indent=1)
print('toolchain written', OUT)

# RM-OT-05V Group C2: canon-enforcement forefoot step generator (GORRUND_V1 Part 2 §50-58 / Part 2 status line:
# large plantigrade humanoid feet, FIVE toes per foot, toes humanoid and non-prehensile, never clawed / extremely long / ape-like,
# ordinary protective toenails). The source forefoot (4 distinct pointed toes) is replaced inside a bounded forefoot region by:
#   smoothed source foot cut back behind the toe line  U  metatarsal-head ball pad  U  five toe round-cones  U  five nail plates.
# Foot scale is preserved: medial / lateral edges and the longest toe tip are measured on the CURRENT foot and reused.
# Every number below is a BUILDER-CHOSEN reference-construction value (REFERENCE_ANATOMY_V1 §7 / R-14), recorded in the step JSON.
# Usage: python3 v_feet.py --state STATE.npz --side +1|-1 --out STEP.json
import argparse, json, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('--state'); ap.add_argument('--side', type=int); ap.add_argument('--out'); a = ap.parse_args()
d = np.load(a.state); V = d['V'].astype(float); s = a.side
P = V[(np.sign(V[:, 0]) == s) & (V[:, 2] < 9) & (np.abs(V[:, 0]) > 5)]
ball = P[(P[:, 1] > 12) & (P[:, 1] < 22)]
xm = ball[:, 0].min() if s > 0 else ball[:, 0].max()          # medial edge (toward the midline)
xl = ball[:, 0].max() if s > 0 else ball[:, 0].min()          # lateral edge
tip = float(P[:, 1].max()); W = abs(xl - xm)
X = lambda f: float(xm + s * f * W)
# builder-chosen layout (fractions of forefoot width / cm), humanoid order: hallux medial and longest, digits 2-5 shortening laterally
frac = [0.165, 0.395, 0.580, 0.750, 0.905]
dtip = [0.0, 1.2, 3.0, 5.2, 7.8]                  # tip set-back from the longest toe (cm)
length = [11.0, 10.5, 9.5, 8.5, 7.5]              # free toe length, base (MTP region) to tip (cm)
rb = [3.30, 2.55, 2.40, 2.25, 2.10]; rt = [2.85, 2.15, 2.00, 1.90, 1.80]   # base / tip radii (cm)
prims = []; toes = []
# lateral layout: hallux 0.6 cm inside the medial edge, then digits side by side with a 0.5 cm cleft; radii scaled so digit 5
# stays >= 0.8 cm inside the lateral edge (symmetric rule for both feet)
gap = 0.5; need = 0.6 + 2 * sum(rb) + 4 * gap + 0.8; scl = min(1.0, W / need)
rb = [r * scl for r in rb]; rt = [r * scl for r in rt]
xs = [0.6 + rb[0]]
for i in range(1, 5): xs.append(xs[-1] + rb[i - 1] + rb[i] + gap)
for i in range(5):
    ty = tip - dtip[i] - rt[i] * 0.0; by = ty - length[i]; x = float(xm + s * xs[i])
    toes.append(dict(digit=i + 1, x=round(x, 2), base_y=round(by, 2), tip_y=round(ty, 2), r_base=round(rb[i], 3), r_tip=round(rt[i], 3)))
    prims.append(dict(op='union', k=0.35, sdf=dict(type='cone', a=[x, by, rb[i] + 0.9], b=[x, ty - rt[i], rt[i]], ra=rb[i], rb=rt[i])))
    # nail plate: thin flattened ellipsoid on the distal dorsum (raised ~0.2 cm), no blend so its edge reads
    prims.append(dict(op='union', k=0.0, sdf=dict(type='ellipsoid', c=[x, ty - rt[i] - 0.25 * length[i] * 0.45, 2 * rt[i] - 0.05],
                                                  radii=[0.78 * rt[i], 0.22 * length[i], 0.18])))
y1 = toes[0]['base_y']; y5 = toes[4]['base_y']
# cut-back line through the toe bases (source toes removed in front of it), smooth k
n = np.array([-(y5 - y1), (X(1.0) - X(0.0)), 0.0]) * (1 if s > 0 else -1); n = n / np.linalg.norm(n)
if n[1] < 0: n = -n
p0 = np.array([X(0.0), y1 + 0.5, 0]); dcut = float(n @ p0)
cut = dict(op='sub', k=1.0, sdf=dict(type='halfspace', n=[float(-n[0]), float(-n[1]), 0.0], d=float(-dcut)))   # region n.p >= dcut removed
# dorsal taper: tilted plane through the toe-base line at the toe-root height, rising backwards at beta (removes the dorsum step)
beta = np.radians(28.0); z0 = 2 * rb[0] + 0.4; nt = np.array([n[0] * np.sin(beta), n[1] * np.sin(beta), np.cos(beta)])
pt = np.array([X(0.0), y1 - 1.0, z0]); dt = float(nt @ pt)
taper = dict(op='sub', k=2.0, sdf=dict(type='halfspace', n=[float(-nt[0]), float(-nt[1]), float(-nt[2])], d=float(-dt)))
ballpad = dict(op='union', k=2.2, sdf=dict(type='cone', a=[toes[0]['x'], y1 - 1.5, 3.7], b=[toes[4]['x'], y5 - 1.5, 3.0], ra=3.7, rb=3.0))
ymin = min(y1, y5) - 8.0
step = dict(name='C2_%s_forefoot_five_toes' % ('+X' if s > 0 else '-X'), group_code=3,
            region=dict(type='box', lo=[min(xm, xl) - 3, ymin, -6], hi=[max(xm, xl) + 3, tip + 6, 15]),
            box=[[min(xm, xl) - 6, ymin - 4, -3], [max(xm, xl) + 6, tip + 9, 18]], res=0.35, t=3.0, h=1.0, seam_cm=2.0,
            field=dict(blur_cm=0.8, offset_cm=0.0, primitives=[cut, taper, ballpad] + prims, ground_z=0.0),
            builder_values=dict(medial_x=round(float(xm), 2), lateral_x=round(float(xl), 2), forefoot_width=round(float(W), 2), longest_tip_y=round(tip, 2),
                                toes=toes, note='five-digit humanoid forefoot; values are builder-chosen reference-construction values (R-14), not canon'))
json.dump(step, open(a.out, 'w'), indent=1); print(json.dumps(step['builder_values']))

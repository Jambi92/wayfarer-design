# RAC RM-OT-05L GO-RS2-REF: the ONE direct revision of GO-RS1 (order §17). Clay record = RS1 with the revisions marked 'RS2:'; the
# surface is then finished with the hand-drawn brush pass in l_rs2_brush.py (bony landmarks, planes, grooves).
# (RS1 header follows)
# RAC RM-OT-05L GO-RS1-REF: blank-slate Gorrund reference sculpt record (order §2-§17).
# Digital clay only (l_clay.py): every form below is one hand-placed sculpt stroke (position / size chosen by the sculptor for this
# body); the left half is sculpted and mirrored (bilateral symmetry). No race skeleton, no human donor mesh, no donor weights or joint
# centres, no composition algorithm, no parameter search. The forms follow the Gorrund canon (GORRUND_V1 Parts 1-2, 05L §7-§15):
# one load-bearing chain neck root -> girdle -> deep thorax -> lower axial trunk -> deep pelvis -> proximal femur -> knee -> shank
# -> ankle -> foot, and shoulder -> elbow -> forearm -> wrist -> hand; structure dominant, neutral soft tissue.
# Usage: python3 l_rs1.py OUT_PREFIX [voxel_cm]   -> OUT_PREFIX_raw.obj (voxel remesh of the clay)
import sys, numpy as np
from l_clay import *
E, C = ellipsoid, cone
c = Clay()
# ---------------- axial: the trunk as hand-drawn section templates (one sweep), plus surface forms ----------------------------------
#        z     cy   half-b  front  back   exp       (cm; front = +Y)
# sections (z, cy, half-breadth, front depth, back depth, exponent):
#   z103: pelvic floor (legs take over below)
#   z110: hip level: hip joints under the load path
#   z118: sacral platform: deep, flat-backed posterior pelvis
#   z126: iliac crest
#   z134: lower axial trunk (recessed anterior wall, no belly)
#   z141: natural lower-axial minimum (radiused, not pinched)
#   z147: costal margin: the rib cage steps forward and out over the lower trunk
#   z152: lower rib cage
#   z160: rib cage: broad, deep, planar lateral walls (structural, not a barrel)
#   z170: rib cage maximum, rounded posterior thorax
#   z179: upper thorax carrying the girdle
#   z186: shoulder level (girdle slopes from the neck root)
#   z191: broad neck base
TRUNK = [(103,  -1.0, 14.0,  9.0, 11.0, 2.10),
         (110,  -1.0, 17.8, 10.5, 14.0, 2.15),
         (118,  -1.0, 18.4, 11.0, 15.0, 2.15),
         (126,  -1.0, 17.8, 11.0, 13.5, 2.10),
         (134,  -0.5, 17.0, 10.5, 12.5, 2.05),
         (141,   0.0, 16.8, 11.0, 12.5, 2.05),
         (147,   0.5, 18.0, 14.0, 13.8, 2.10),
         (152,   1.0, 20.0, 17.0, 15.0, 2.20),
         (160,   1.0, 21.6, 18.8, 16.5, 2.30),
         (170,   1.0, 22.2, 18.8, 17.2, 2.30),
         (178,   0.5, 21.4, 16.5, 17.0, 2.20),
         (184,   0.0, 18.0, 13.5, 15.0, 2.10),
         (190,  -0.5, 13.0,  9.0, 11.0, 2.05),
         (196,   0.0, 10.0,  7.5,  8.0, 2.00)]
c.add(lambda P: section_sweep(P, TRUNK), 0, 'trunk section templates: neck root -> girdle -> deep thorax -> lower axial trunk -> deep pelvis')
c.add(lambda P: E(P, (0, 0, 106), (8.0, 6.0, 5.0)), 4, 'pelvic floor fill')
# ---------------- neck root / girdle / head ----------------------------------------------------------------------------------------
c.add(lambda P: C(P, (0, -0.5, 189), (0, 1.5, 208), 12.0, 7.8), 4, 'neck: moderate length, broad root, strongly integrated')
c.add(lambda P: E(P, (10.0, -2.5, 186.5), (11.5, 8.0, 5.0)), 6, 'neck-to-girdle slope: skeletal shoulder line, no trap bulk')
c.add(lambda P: C(P, (3.5, 6.5, 189.5), (21.5, 3.0, 184.5), 2.4, 2.4), 3, 'clavicle: long, carries the girdle forward-lateral')
c.add(lambda P: E(P, (21.5, 0.0, 177.5), (7.2, 8.2, 8.0)), 5, 'shoulder articulation: large, carried by the thorax')
c.add(lambda P: E(P, (0, 3.5, 216), (9.0, 10.5, 12.5)), 4, 'head (neutral placeholder; hidden in body-only review)')
c.add(lambda P: E(P, (0, 8.0, 207), (6.8, 5.5, 5.0)), 4, 'jaw (neutral placeholder)')
# ---------------- upper limb: bone scale large, joints broad, reach not dominant ----------------------------------------------------
c.add(lambda P: C(P, (24.2, -0.5, 175), (29.5, -2.0, 148), 8.2, 6.8, (1.0, 0.92, 1)), 4, 'upper arm: scaled to the girdle')
c.add(lambda P: E(P, (27.0, 2.6, 167), (5.6, 4.6, 11)), 5, 'anterior upper-arm mass (neutral)')
c.add(lambda P: E(P, (27.8, -5.4, 165), (5.8, 4.6, 13)), 5, 'posterior upper-arm mass (neutral)')
c.add(lambda P: E(P, (30.0, -2.2, 148.5), (7.0, 6.4, 6.0)), 4, 'elbow: broad humeral condyles')
c.add(lambda P: E(P, (30.2, -7.2, 149.0), (3.0, 2.2, 3.4)), 2, 'olecranon (integrated, not a knob)')
c.add(lambda P: E(P, (30.8, -0.5, 139), (6.0, 6.6, 9.0)), 4, 'proximal forearm mass (neutral)')
c.add(lambda P: C(P, (30.3, -1.8, 146), (33.0, 0.5, 116), 6.8, 5.4, (0.82, 1, 1)), 4, 'forearm: structured, broad at both ends')
c.add(lambda P: E(P, (33.2, 0.6, 114), (4.2, 5.9, 4.2)), 2.5, 'wrist: broad, functional (no cuff)')
c.add(lambda P: E(P, (33.8, 1.0, 104.5), (3.2, 6.4, 8.6)), 2.0, 'palm: large (faces the thigh)')
for (dy, z0, z1, r) in ((5.2, 97.0, 84.0, 1.7), (1.8, 96.5, 82.5, 1.75), (-1.6, 97.0, 83.5, 1.7), (-4.8, 98.0, 86.5, 1.55)):
    c.add(lambda P, dy=dy, z0=z0, z1=z1, r=r: C(P, (34.0, 1.0 + dy, z0), (32.6, 1.6 + dy, z1), r, r * 0.85), 0.7, 'finger')
c.add(lambda P: C(P, (32.6, 6.6, 109.0), (30.4, 9.6, 97.5), 2.2, 1.7), 0.9, 'thumb')
# ---------------- lower limb: large femoral / tibial scale, integrated knees and ankles, large plantigrade feet -------------------
c.add(lambda P: E(P, (14.5, -0.5, 109.0), (6.0, 9.0, 10.0)), 5, 'proximal femur / greater trochanter: lateral hip plane under the load path')
c.add(lambda P: C(P, (13.4, 0.0, 109), (13.2, 2.0, 63), 10.4, 9.6), 4, 'RS2: thigh: large femoral scale')
c.add(lambda P: E(P, (14.3, 6.0, 92), (8.0, 6.6, 20)), 5, 'anterior thigh mass (neutral)')
c.add(lambda P: E(P, (13.8, -5.0, 88), (8.0, 6.4, 19)), 5, 'RS2: posterior thigh mass (lowered: no gluteal ledge), continuous with the sacral platform')
c.add(lambda P: E(P, (13.2, 2.4, 61.0), (8.0, 7.4, 6.0)), 8, 'RS2: knee: broad condyles and tibial plateau, integrated (bulb removed)')
c.add(lambda P: E(P, (13.2, 8.6, 62.0), (5.0, 2.0, 5.6)), 4, 'patellar plane')
c.add(lambda P: C(P, (13.2, 2.2, 58.5), (12.8, -0.6, 12.5), 9.0, 6.0), 5, 'RS2: shank: tibial body, load-bearing')
c.add(lambda P: E(P, (11.8, -3.8, 45), (6.4, 5.8, 13)), 5, 'calf, medial head: moderate, mid-shank')
c.add(lambda P: E(P, (14.9, -3.0, 48), (5.4, 5.0, 12)), 5, 'calf, lateral head: higher and smaller')
c.add(lambda P: E(P, (12.8, -0.6, 10.5), (6.6, 6.0, 5.4)), 4, 'ankle: substantial, tapers from the calf')
c.add(lambda P: E(P, (18.6, -1.8, 10.2), (1.8, 2.4, 2.6)), 1.5, 'lateral malleolus')
c.add(lambda P: E(P, (7.2, -0.2, 11.2), (1.8, 2.4, 2.6)), 1.5, 'medial malleolus')
c.add(lambda P: E(P, (13.0, -6.0, 5.0), (5.8, 6.8, 5.0)), 3, 'heel')
c.add(lambda P: C(P, (13.0, -2.0, 5.0), (14.0, 17.0, 3.6), 5.6, 4.8, (0.8, 1, 1)), 3, 'mid-foot / arch body')
c.add(lambda P: E(P, (13.8, 17.5, 3.4), (8.4, 6.0, 3.3)), 2.5, 'forefoot / metatarsal heads')
for (x, y0, y1, r) in ((8.4, 20.0, 30.0, 2.6), (11.6, 21.0, 29.0, 1.95), (14.2, 20.8, 27.8, 1.85), (16.6, 20.0, 26.4, 1.7), (18.7, 19.0, 24.6, 1.6)):
    c.add(lambda P, x=x, y0=y0, y1=y1, r=r: C(P, (x, y0, 2.8), (x + (0.3 if x > 9 else -0.2), y1, 2.1), r, r * 0.85), 0.5, 'toe')
c.cut(lambda P: plane_below(P, 0.0), 0.4, 'sole: plantigrade ground contact')
if __name__ == '__main__':
    out = sys.argv[1]; h = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    V, F = remesh(c, (-44, -26, -0.5), (44, 34, 231), h)
    write_obj(out + '_raw.obj', V, F, 'GO-RS2 clay voxel remesh (l_rs2.py), h=%.2f cm' % h); print(len(V), len(F), V.min(0), V.max(0))

# RM-OT-05Q garment / body face-label inventory (RAC frame, F1 working copy). Zone labels are COARSE boxes and contain
# body faces as well as garment faces unless stated; only the +X armband exposed arc has a verified face set
# (q_select.py). Classes: a separate geometry over intact body | b fused, locally removable, underlying surface
# recoverable | c garment replaces the body surface (anatomy absent) | d ambiguous.
# Usage: python3 q_inventory.py --mesh F1_working.obj --sel patch_face_sets.npz --out DIR
import argparse, json, numpy as np, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--mesh'); ap.add_argument('--sel'); ap.add_argument('--out'); a = ap.parse_args()
m = trimesh.load(a.mesh, process=False); c = m.triangles_center; x, y, z = c.T; ax_ = np.abs(x); A = m.area_faces
Z = [  # id, name, mask, class, confidence, evidence, known errors
 (1, 'belt + loincloth (waist band z 112-140)', (z >= 112) & (z <= 140) & (ax_ <= 26), 'c', 'medium',
  'S_belt z118/z126/z132: one outer contour (belt, buckle discs, fringe) and no inner pelvis/abdomen loop', 'box includes lower abdomen skin above the belt and flank skin'),
 (2, 'loincloth flaps (z 72-112)', (z >= 72) & (z < 112) & (ax_ <= 26), 'a/b', 'medium',
  'S_belt z100: separate thigh loops lie inside the open skirt contour; sag_x0 / sag_x10: flaps are thin sheets hanging free of the thighs below z ~105, fused to the belt above',
  'box includes the thighs, crotch and buttocks (body); crotch/pelvis under the belt is absent (class c above z ~105)'),
 (3, 'forearm bracers (both arms)', (z >= 106) & (z <= 141) & (ax_ >= 30) & (ax_ <= 53), 'c', 'high',
  'S_bracer z112-136: single closed forearm loop, no inner forearm loop; sag/cor: strap relief is the outer surface', 'box includes wrist/hand top and elbow; -X forearm is cut open by the 05N slab seam (zm124 open)'),
 (4, '+X upper-arm armband (exposed arc, VERIFIED face set G)', None, 'c', 'high',
  'S_armband long_* and perp: band is a single outward step (lip / undercut) with no skin surface beneath; medial arc runs into the fused arm/trunk axillary contact (perp s>=0 open loops)',
  'G contains enclosed islands at the sector ends; some band-top faces at the sector ends are labelled seam band S (both are removed)'),
 (5, '-X upper-arm armband', (z >= 155) & (z <= 172) & (x <= -18) & (x >= -45), 'd', 'low',
  'not sectioned in detail: the -X arm is open at the F1/F2 seam (05N contact slab), so separability cannot be read', 'box includes deltoid / axilla skin'),
 (6, 'shin + ankle wraps (both legs)', (z >= 8) & (z <= 50) & (ax_ >= 8) & (ax_ <= 40), 'c', 'high',
  'S_shin z24-z46 / zm32: single closed loop per leg, no inner shin loop; sag/cor: wrap folds are the outer surface', 'box includes knee bottom and foot top'),
 (7, 'necklace + pendant teeth', (z >= 165) & (z <= 190) & (ax_ <= 16) & (y >= 6), 'd', 'medium',
  'sag0_front / sag8_front: pendant relief fused onto the chest/neck profile; a single surface, no skin beneath; relief is shallow so a local fill is plausible but unproven', 'box includes chest, throat and the front braids'),
 (8, 'front braids', (z >= 140) & (z <= 205) & (ax_ >= 4) & (ax_ <= 26) & (y >= 14), 'a', 'medium',
  'S_neck_mane z170 (earlier sweep) and z165: braids are separate small loops in front of the chest below their attachment; chest contour continuous behind them', 'box includes pectoral skin; attachment at the head is fused'),
 (9, 'back braid', (z >= 125) & (z <= 178) & (ax_ <= 8) & (y <= -22), 'a', 'medium',
  'S_neck_mane z150 / z165: back braid is a separate loop behind the back below its attachment; back contour continuous', 'box includes back skin at the spine'),
 (10, 'mane over neck / upper back', (z >= 175) & (y <= -4), 'c', 'medium',
  'S_neck_mane z185 / z195 / sag0_back: the outer contour is the mane; no neck / trapezius surface inside it', 'box includes the back of the skull (head is out of scope)'),
]
lab = np.zeros(len(c), np.int16); out = []
sel = np.load(a.sel)
for zid, name, mask, cls, conf, ev, err in Z:
    if mask is None: mask = np.zeros(len(c), bool); mask[sel['G']] = True
    mask = mask & (lab == 0) if zid != 4 else mask
    lab[mask] = zid
    out.append(dict(id=zid, item=name, class_=cls, confidence=conf, faces=int(mask.sum()), area_cm2=round(float(A[mask].sum()), 1), evidence=ev, known_errors=err))
np.save(a.out + '/inventory_face_zone.npy', lab); json.dump(out, open(a.out + '/inventory.json', 'w'), indent=1)
for o in out: print(o['id'], o['class_'], o['confidence'], o['faces'], o['item'])

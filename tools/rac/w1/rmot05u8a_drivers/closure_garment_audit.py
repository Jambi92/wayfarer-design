# RM-OT-05 closure audit (read-only): map the 05Q garment / hair inventory zones onto the selected U8 cp1 geometry and record
# presence, edit status and vertical extent. Usage: python3 closure_garment_audit.py --s3 GO-05S-S3.obj --out JSON
import argparse, json, numpy as np, trimesh
ap = argparse.ArgumentParser(); ap.add_argument('--s3'); ap.add_argument('--out'); a = ap.parse_args()
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
R = np.load('reviews/rac-rmot05u8-evidence/return/checks/return.npz'); i = R['s3_vid1'] - 1; W = np.zeros_like(Vs, dtype=np.float32); W[i] = R['V']; V = Vs.copy(); mv = ~np.all(W == Vs.astype(np.float32), 1); V[mv] = W[mv]
zone = np.load('reviews/rac-rmot05q-evidence/separability/inventory_face_zone.npy'); inv = json.load(open('reviews/rac-rmot05q-evidence/separability/inventory.json'))
P05S = np.load('reviews/rac-rmot05s-evidence/plan/interface_sets.npz')['P05S_src_ordered']; z3 = np.full(len(F), -1); z3[:len(P05S)] = zone[P05S]
fmv = np.isin(F, np.where(mv)[0]).any(1)
rows = [dict(id=it['id'], item=it['item'], class_=it['class_'], confidence=it['confidence'], f1_faces=int((zone == it['id']).sum()), present_in_selected=int((z3 == it['id']).sum()),
             edited_in_05Q_to_U8=int(((z3 == it['id']) & fmv).sum()), zone_box_known_errors=it.get('known_errors')) for it in inv]
z = V[:, 2]; top = int(np.argmax(z))
out = dict(selected='U8 cp1 (GO-05U8_cp1.blend 2341d554...)', garment_zones=rows, vertical_extent_cm=dict(min=round(float(z.min()), 3), max=round(float(z.max()), 3), top_vertex=top, top_xyz=np.round(V[top], 3).tolist()),
           note='zone boxes include some adjacent skin (05Q known errors); the counts show presence, not exact garment area. Vertical extent includes any head crest / hair; it is not the R-13 skull-vertex stature.')
json.dump(out, open(a.out, 'w'), indent=1); print(json.dumps({k: v for k, v in out.items() if k != 'garment_zones'})); [print(r['id'], r['class_'], r['present_in_selected'], r['edited_in_05Q_to_U8'], r['item']) for r in rows]

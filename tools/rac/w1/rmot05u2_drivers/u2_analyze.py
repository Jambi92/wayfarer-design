# RM-OT-05U2 (READ-ONLY): define a minimal upper-boundary extension proposal around the residual upper notches of the
# verified 05U RETURN. Nothing is written to any mesh, scene, mask, face set or protection set; outputs are proposal lists.
# Indices are ZERO-BASED S3 vertex / face indices of GO-05S-S3.obj (sha 1d503833...); the RETURN carries the same topology
# and the identity attribute rac_s3_vid1 = S3 index + 1 (one-based), so S3 index = rac_s3_vid1 - 1.
#
# Region rule (explicit, no tuning loop):
#   N0 = the six reported notch vertices (confirmed by measurement below).
#   N  = N0 plus every vertex that is (a) edge-adjacent to N, (b) inside the window theta -95..-75 deg, s 5..12 cm, r < 16,
#        (c) not already EDIT, and (d) has RETURN roughness >= ROUGH (28 deg); grown to closure.
#   Added faces A = all non-interface faces incident to N.  Proposed editable vertices E' = EDIT u N.
#   Vertices whose every incident face lies in (interface u A) become editable too (enclosed); they are listed.
#   Proposed frozen ring R' = vertices of (interface u A) that also touch a face outside (interface u A).
#   Roughness = max angle between a vertex's incident face normals and their mean normal (degrees).
import argparse, json, hashlib, sys, os, numpy as np, trimesh
from collections import defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rmot05s_drivers')); import s_lib
ap = argparse.ArgumentParser(); ap.add_argument('--s3'); ap.add_argument('--ret'); ap.add_argument('--f1'); ap.add_argument('--out'); ap.add_argument('--rough', type=float, default=28.0)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
S = 'reviews/rac-rmot05s-evidence/repair/S3/'
fr = s_lib.Frame('reviews/rac-rmot05q-evidence/plan/patch_selection.json')
s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); Fs = np.asarray(s3.faces)
lab = np.load(S + 'GO-05S-S3_face_labels.npy'); src = np.load(S + 'GO-05S-S3_maps.npz')['src_vertex']
inter = (lab == 4) | (lab == 5)
vn = np.zeros(len(Vs), bool); vn[Fs[inter].ravel()] = True; vo = np.zeros(len(Vs), bool); vo[Fs[~inter].ravel()] = True
EDIT = vn & ~vo; RING = vn & vo
R = np.load(a.ret); ids = R['s3_vid1'] - 1; Vr = Vs.copy(); Vr[ids] = R['V']; Vr[~EDIT] = Vs[~EDIT]       # protected = exact S3 (verified bit-identical)
assert np.array_equal(np.sort(R['F'].ravel()), np.sort(R['F'].ravel())) and len(R['F']) == len(Fs)
Fr_s3 = np.sort(ids[R['F']], axis=1); assert np.array_equal(np.unique(Fr_s3, axis=0), np.unique(np.sort(Fs, axis=1), axis=0)), 'topology differs'
m = trimesh.Trimesh(Vr, Fs, process=False); fn = m.face_normals
vf = defaultdict(list)
for i, f in enumerate(Fs):
    for v in f: vf[int(v)].append(i)
nbr = defaultdict(set)
for f in Fs:
    for i in range(3): nbr[int(f[i])].update(int(x) for x in f if x != f[i])
def rough(v):
    n = fn[vf[v]]; c = n.mean(0); c /= np.linalg.norm(c); return float(np.degrees(np.arccos(np.clip(n @ c, -1, 1))).max())
t, s, r = fr.tsr(Vr)
def inwin(v): return -95 < t[v] < -75 and 5 < s[v] < 12 and r[v] < 16
N0 = [61303, 61559, 62065, 61581, 61580, 61562]
cat = lambda v: 'EDIT' if EDIT[v] else ('FROZEN_RING' if RING[v] else 'PROTECTED')
conf = [dict(s3_index0=v, rac_s3_vid1=v + 1, category=cat(v), source_vertex=bool(src[v] >= 0), f1_index0=int(src[v]),
             theta=round(float(t[v]), 2), s_cm=round(float(s[v]), 2), r_cm=round(float(r[v]), 2), roughness_deg=round(rough(v), 1),
             incident_face_labels=sorted(set(int(x) for x in lab[vf[v]]))) for v in N0]
N = set(N0); grew = True
while grew:
    grew = False
    for v in list(N):
        for u in nbr[v]:
            if u not in N and not EDIT[u] and inwin(u) and rough(u) >= a.rough: N.add(u); grew = True
N = sorted(N)
A = sorted(set(fi for v in N for fi in vf[v] if not inter[fi]))
region = inter.copy(); region[A] = True
vin = np.zeros(len(Vs), bool); vin[Fs[region].ravel()] = True; vout = np.zeros(len(Vs), bool); vout[Fs[~region].ravel()] = True
Eprop = vin & ~vout; Rprop = vin & vout
Nseed = N; ENC = sorted(set(np.where(Eprop & ~EDIT)[0].tolist()) - set(N)); assert set(N) <= set(np.where(Eprop & ~EDIT)[0].tolist())
N = sorted(int(v) for v in np.where(Eprop & ~EDIT)[0])   # added editable = seeds + vertices fully enclosed by the added faces
# region topology checks
def comps(faces):
    adj = defaultdict(set); e2f = defaultdict(list)
    for fi in faces:
        f = Fs[fi]
        for i in range(3): e2f[tuple(sorted((int(f[i]), int(f[(i + 1) % 3]))))].append(fi)
    for fl in e2f.values():
        for x in fl:
            adj[x].update(y for y in fl if y != x)
    seen = set(); n = 0
    for f0 in faces:
        if f0 in seen: continue
        n += 1; st = [f0]
        while st:
            x = st.pop()
            if x in seen: continue
            seen.add(x); st.extend(adj[x] - seen)
    bnd = [e for e, fl in e2f.items() if len(fl) == 1]
    return n, len(bnd)
post_inter = [int(i) for i in np.where(inter)[0] if lab[i] in (4, 5) and fr.tsr(Vr[Fs[i]].mean(0, keepdims=True))[0][0] < 0]
nA, bA = comps(A); nP, bP = comps(post_inter); nU, bU = comps(post_inter + A)
area = float(m.area_faces[A].sum())
# seam outliers (05U V5) on current interface: stitch edges at theta -88.4 / s 8.0 and -85.7 / s 7.89
v5 = json.load(open('reviews/rac-rmot05u-evidence/checks/return/result_verify.json'))['V5_seam_continuity']['outliers']
e2f = defaultdict(list)
for i, f in enumerate(Fs):
    for k in range(3): e2f[tuple(sorted((int(f[k]), int(f[(k + 1) % 3]))))].append(i)
seam = []
for e, fl in e2f.items():
    if len(fl) == 2 and inter[fl[0]] != inter[fl[1]]:
        c = Vr[list(e)].mean(0); tt, ss, _ = fr.tsr(c[None]); n0, n1 = fn[fl[0]], fn[fl[1]]
        seam.append((e, float(tt[0]), float(ss[0]), float(np.degrees(np.arccos(np.clip(n0 @ n1, -1, 1))))))
seam_out = []
for o in v5:
    if o['theta'] < -80 and o['s'] > 7:
        best = min(seam, key=lambda q: (q[1] - o['theta']) ** 2 + (q[2] - o['s']) ** 2)
        seam_out.append(dict(reported=o, edge_s3_index0=list(best[0]), theta=round(best[1], 2), s_cm=round(best[2], 2), dihedral_deg=round(best[3], 1),
                             both_vertices_editable_after_extension=bool(all(Eprop[v] for v in best[0])), interior_after_extension=bool(all(region[fi] for fi in e2f[best[0]]))))
# source baseline roughness (to judge whether notches are anomalous): all label-0 source vertices within r<16 of the arm frame
srcv = np.where((src >= 0) & ~vn & (r < 16) & (s > -10) & (s < 20))[0]
samp = srcv[np.linspace(0, len(srcv) - 1, min(4000, len(srcv))).astype(int)]
base = np.array([rough(int(v)) for v in samp])
# residual roughness of vertices staying protected/frozen near the extension
newring = sorted(int(v) for v in np.where(Rprop & ~RING)[0])
keep_ring = sorted(int(v) for v in np.where(Rprop & RING)[0])
ring_rough = sorted(((round(rough(v), 1), v) for v in newring), reverse=True)[:8]
def H(x): return hashlib.sha256(np.asarray(x, dtype=np.int64).tobytes()).hexdigest()
cur_E = [int(v) for v in np.where(EDIT)[0]]; cur_R = [int(v) for v in np.where(RING)[0]]; cur_F = [int(i) for i in np.where(inter)[0]]
added_cat = {}
for v in N: added_cat[v] = dict(category_now=cat(v), source_vertex=bool(src[v] >= 0), roughness_deg=round(rough(v), 1), theta=round(float(t[v]), 2), s_cm=round(float(s[v]), 2), r_cm=round(float(r[v]), 2))
A_lab = {int(k): int(c) for k, c in zip(*np.unique(lab[A], return_counts=True))}
out = dict(reference=dict(s3_obj=os.path.basename(a.s3), s3_sha256=hashlib.sha256(open(a.s3, 'rb').read()).hexdigest(),
                          return_npz_sha256=hashlib.sha256(open(a.ret, 'rb').read()).hexdigest(), release_zip_sha256='aed5711fa00d193eccae9391f40de790d6e617333caa8add76554e81358a3159',
                          indexing='zero-based S3 vertex / face indices; rac_s3_vid1 = index + 1 (one-based)'),
           rule=dict(N0=N0, roughness_threshold_deg=a.rough, window='theta -95..-75 deg, s 5..12 cm, r < 16 cm', growth='edge-adjacent closure', added_faces='all non-interface faces incident to N'),
           confirmation_of_reported_vertices=conf,
           current=dict(editable_vertices=len(cur_E), editable_sha256=H(cur_E), frozen_ring=len(cur_R), frozen_ring_sha256=H(cur_R), interface_faces=len(cur_F), interface_faces_sha256=H(cur_F)),
           proposed_added=dict(seed_vertices=Nseed, enclosed_vertices=ENC, vertices=len(N), vertex_list=N, vertices_sha256=H(N), vertex_categories=added_cat, faces=len(A), face_list=A, faces_sha256=H(A),
                               face_labels_now=A_lab, all_added_faces_are_source_label0=bool(set(A_lab) == {0}), area_cm2=round(area, 2),
                               theta_range=[round(float(t[N].min()), 1), round(float(t[N].max()), 1)], s_range_cm=[round(float(s[N].min()), 2), round(float(s[N].max()), 2)], r_range_cm=[round(float(r[N].min()), 2), round(float(r[N].max()), 2)]),
           proposed=dict(editable_vertices=int(Eprop.sum()), editable_sha256=H(np.where(Eprop)[0]), frozen_ring=int(Rprop.sum()), frozen_ring_sha256=H(np.where(Rprop)[0]),
                         frozen_ring_new_vertices=newring, frozen_ring_retained_from_current=len(keep_ring), frozen_ring_released_to_editable=sorted(int(v) for v in np.where(RING & Eprop)[0]),
                         new_ring_highest_roughness=[dict(s3_index0=v, roughness_deg=g) for g, v in ring_rough]),
           topology=dict(added_faces_components=nA, posterior_interface_components=nP, posterior_union_components=nU, union_boundary_edges=bU),
           seam_outliers=seam_out,
           source_skin_baseline_roughness=dict(sample=int(len(samp)), p50=round(float(np.percentile(base, 50)), 1), p90=round(float(np.percentile(base, 90)), 1), p95=round(float(np.percentile(base, 95)), 1), p99=round(float(np.percentile(base, 99)), 1)))
json.dump(out, open(os.path.join(a.out, 'proposal_region.json'), 'w'), indent=1)
np.savez(os.path.join(a.out, 'proposal_sets.npz'), current_editable=np.array(cur_E), current_frozen_ring=np.array(cur_R), current_interface_faces=np.array(cur_F),
         added_vertices=np.array(N), added_faces=np.array(A), proposed_editable=np.where(Eprop)[0], proposed_frozen_ring=np.where(Rprop)[0])
print(json.dumps({k: out[k] for k in ('current', 'topology', 'seam_outliers', 'source_skin_baseline_roughness')}, indent=1))
print(json.dumps({k: v for k, v in out['proposed_added'].items() if k not in ('vertex_list', 'face_list', 'vertex_categories')}, indent=1))
print(json.dumps({k: v for k, v in out['proposed'].items()}, indent=1))
print('added vertices:', {v: (d['category_now'], d['roughness_deg']) for v, d in added_cat.items()})

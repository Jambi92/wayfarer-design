# ear_zones.py : order 0d9c70b -- per-face zone labels for a Fenn ear-branch realization (v001 or v002 layout), and T-4 / aspect per zone.
# Zones: sheet blocks (bridge / F1 crescent / F2 upper extension) x (front / back), rim, cuff band k (regular or count-transition quad),
# root band, transition (v005 faces touching the faired transition ring); 'upper_extension' = F2 front + back + rim faces with s >= S_UP.
# CLI: python3 ear_zones.py WORK OUT.json [KEYS...]  (layout = ear_branch_lib.canonical_layout() of EAR_TOPO; WORK/canon_branch_topology.json)
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E

def face_zones(Lo, z):
    """returns (face index array, zone label array, corner-cell flag) for every branch face of a realization npz z"""
    Q = z['Q']; part = z['part']; side = z['side']; nV = len(z['V'])
    blocks = Lo.get('face_block')                       # per layout face: 'bridge' / 'F1' / 'F2' / ... (sheet) or 'rim'
    nF_sheet = len(Lo['F']); out_f = []; out_z = []
    npf = len(Lo['F']) + sum(c for _, c, _ in Lo['_cuff_counts']) + Lo['_root_faces']
    n_kept = len(Q) - 2 * npf                            # kept v005 faces come first, then patch l, patch r
    # patch faces: identify the first face of each side's patch by the first sheet vertex
    firsts = {s: int(np.nonzero(side == s)[0][0]) for s in ('l', 'r')}
    st = Lo['st']; npatch = int((side == 'l').sum())
    # faces after the kept v005 block, in patch order: sheet+rim (nF_sheet), cuff bands (per canon), root band
    nb = z['meta']  # unused
    fi = n_kept
    canon_counts = Lo.get('_cuff_counts')
    for s in ('l', 'r'):
        for k in range(nF_sheet):
            out_f.append(fi); out_z.append(blocks[k]); fi += 1
        for b, cnt, ntr in canon_counts:
            for j in range(cnt):
                out_f.append(fi); out_z.append('cuff_b%d' % b + ('_tr' if j in ntr else '')); fi += 1
        nroot = Lo['_root_faces']
        for j in range(nroot): out_f.append(fi); out_z.append('root_band'); fi += 1
    out_f = np.array(out_f); out_z = np.array(out_z, dtype='<U16')
    # transition faces: v005 faces with a transition vertex
    tr = np.nonzero((part[Q[:n_kept]] == 'transition').any(1))[0]
    out_f = np.r_[out_f, tr]; out_z = np.r_[out_z, np.array(['transition'] * len(tr), dtype='<U16')]
    return out_f, out_z

def label_layout(Lo, canon_side, root_faces):
    """attach per-face block labels to the canonical layout (sheet faces are emitted block by block, front then back; rim last)"""
    if 'face_block' not in Lo:
        Lo['face_block'] = np.array(Lo['face_block_list'], dtype='<U16')
    Lo['_cuff_counts'] = []
    for b, bd in enumerate(canon_side['bands']):
        ntr = {j for j, f in enumerate(bd['faces']) if sum(1 for t, _ in f if t == 't') != 2}
        Lo['_cuff_counts'].append((b, len(bd['faces']), ntr))
    Lo['_root_faces'] = root_faces

def quad_metrics(X, q):
    P = X[q]; ang = []; L = np.linalg.norm(P - np.roll(P, -1, 1), axis=2)
    for k in range(4):
        u = P[:, (k - 1) % 4] - P[:, k]; w = P[:, (k + 1) % 4] - P[:, k]
        c = np.einsum('ij,ij->i', u, w) / (np.linalg.norm(u, axis=1) * np.linalg.norm(w, axis=1) + 1e-12); ang.append(np.degrees(np.arccos(np.clip(c, -1, 1))))
    return np.stack(ang, 1), L.max(1) / np.maximum(L.min(1), 1e-9)

def zone_report(Lo, z, canon_side, root_faces):
    label_layout(Lo, canon_side, root_faces)
    f, zl = face_zones(Lo, z); ang, asp = quad_metrics(z['V'], z['Q'][f]); bad = ((ang < 45) | (ang > 135)).any(1)
    R = {}
    for zz in sorted(set(zl)):
        m = zl == zz; R[zz] = dict(faces=int(m.sum()), angle_viol=int((bad & m).sum()), aspect_gt4=int(((asp > 4) & m).sum()), aspect_max=float(asp[m].max()), min_angle=float(ang[m].min()))
    groups = dict(front=[k for k in R if k.endswith('_front')], back=[k for k in R if k.endswith('_back')], rim=['rim'] + [k for k in R if k.startswith('rim')],
                  cuff=[k for k in R if k.startswith('cuff') or k == 'root_band'], transition=['transition'],
                  upper_extension=[k for k in R if k.startswith('F2_') or k.startswith('leaf') or k == 'rim_up'], root_band=['root_band'],
                  cuff_count_transitions=[k for k in R if k.startswith('cuff') and k.endswith('_tr')])
    # geometric groups (identical definitions for v001 / v002): s-based upper extension, attachment-corner and lobe-cusp neighbourhoods
    V = z['V']; Q = z['Q']; side = z['side']; firsts = {s_: int(np.nonzero(side == s_)[0][0]) for s_ in ('l', 'r')}; ns = len(Lo['st'])
    cs = Lo['info']['corners']; geo_masks = {}
    sface = np.zeros(len(f), bool); smean = np.full(len(f), -1.0)
    for s_ in ('l', 'r'):
        loc = Q[f] - firsts[s_]; ok = ((loc >= 0) & (loc < ns)).all(1) & (side[Q[f]] == s_).all(1)
        smean[ok] = Lo['st'][loc[ok]][:, :, 0].mean(1); sface |= ok
    geo_masks['upper_extension_s'] = sface & (smean >= E.S_UP)
    C = V[Q[f]].mean(1)
    def near(keys, r):
        m = np.zeros(len(f), bool)
        for s_ in ('l', 'r'):
            for k_ in keys: m |= np.linalg.norm(C - V[firsts[s_] + cs[k_]], axis=1) < r
        return m
    geo_masks['attachment_corners'] = near(('c0', 'c1'), 0.5); geo_masks['lobe_cusp'] = near(('c0f',), 0.8)
    G = {}
    for g, m in geo_masks.items():
        G[g] = dict(faces=int(m.sum()), angle_viol=int((bad & m).sum()), aspect_gt4=int(((asp > 4) & m).sum()), union=int(((bad | (asp > 4)) & m).sum()),
                    aspect_max=float(asp[m].max()) if m.any() else None, min_angle=float(ang[m].min()) if m.any() else None, max_angle=float(ang[m].max()) if m.any() else None)
    for g, ks in groups.items():
        ks = sorted(set(k for k in ks if k in R)); m = np.isin(zl, ks)
        G[g] = dict(faces=int(m.sum()), angle_viol=int((bad & m).sum()), aspect_gt4=int(((asp > 4) & m).sum()), union=int(((bad | (asp > 4)) & m).sum()),
                    aspect_max=float(asp[m].max()) if m.any() else None, min_angle=float(ang[m].min()) if m.any() else None, max_angle=float(ang[m].max()) if m.any() else None)
    tot = dict(faces=int(len(f)), angle_viol=int(bad.sum()), rate=float(bad.mean()), aspect_gt4=int((asp > 4).sum()), aspect_gt10=int((asp > 10).sum()), union=int((bad | (asp > 4)).sum()),
               aspect_max=float(asp.max()), min_angle=float(ang.min()))
    return dict(total=tot, groups=G, zones=R), f, zl, ang, asp, bad

if __name__ == '__main__':
    import json, sys as _s
    W_, OUT_ = _s.argv[1], _s.argv[2]; keys = _s.argv[3:] or ['FNL4-CF2_E2', 'FNF181-CF2_E2']; Lo = E.canonical_layout(); canon = json.load(open(W_ + '/canon_branch_topology.json'))
    res = dict(version=Lo.get('version'), work=W_)
    for k in keys:
        z = np.load('%s/build/%s_branch.npz' % (W_, k)); rec = json.load(open('%s/build/%s_branch.json' % (W_, k)))
        ncuff = sum(len(b['faces']) for b in canon['l']['cuff']['bands']); nroot = rec['patch_faces'] - len(Lo['F']) - ncuff
        R, *_ = zone_report(Lo, z, canon['l']['cuff'], nroot); res[k] = R
    json.dump(res, open(OUT_, 'w'), indent=1); print('zones', OUT_, {k: res[k]['total']['angle_viol'] for k in keys})

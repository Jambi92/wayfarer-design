# ear_measure.py BRANCH.npz OUT.json : order bdcd6a6 §10 / §17 measured ear dimensions and anatomy presence for one branch realization
# (left ear; the right ear is the same construction in its own root frame, its numbers are reported for symmetry).
# Frame: root frame of each side (O root centroid, n lateral, b posterior, u up). Side view = projection on the (b, u) plane.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E
z = np.load(sys.argv[1]); rec = json.load(open(sys.argv[1].replace('.npz', '.json'))); V = z['V']; part = z['part']; side = z['side']
Lo = E.canonical_layout(); st = Lo['st']; ns = len(st); cs = Lo['info']['corners']; p = dict(rec['params']); p['taper'] = tuple(p['taper']); p['helix'] = tuple(p['helix'])
_, _, parts = E.relief(st[:, 0], st[:, 1], p)
out = dict(head=rec['head'], cand=rec['cand'], head_HH_cm=rec['HH_cm'], head_scale=rec['head_scale'], construction=dict(L_ref=p['L'], wb_ref=p['wb'], proj_deg=p['proj'],
           tilt_deg=p['tilt'], sweep_ref=p['sweep'], thickness_ref=p['thick'], lobe_fraction=p['lobe'], taper=list(p['taper'])), sides={})
fr = part == 'front'
for sd in ('l', 'r'):
    first = np.nonzero(side == sd)[0][0]; X = V[first:first + ns]; f = rec['sides'][sd]['frame']; O, n, b, u = [np.array(f[k]) for k in ('O', 'n', 'b', 'u')]
    pf = Lo['part'][:ns] == 'front'; pb = Lo['part'][:ns] == 'back'
    lat = (X - O) @ n; B = (X - O) @ b; U = (X - O) @ u
    lobe = np.nonzero(pf & (st[:, 0] < 1e-9))[0]; lobe_v = lobe[np.argmin(U[lobe])] if len(lobe) else int(np.argmin(np.where(pf, U, 1e9)))
    tip = cs['tip']; L3 = float(np.linalg.norm(X[tip] - X[lobe_v]))
    # width across the ear at each s: anterior (t=-1) to posterior (t=+1) outline points of the front sheet
    edge = pf & (np.abs(np.abs(st[:, 1]) - 1) < 1e-9); ws = []
    for s0 in np.linspace(0.05, 0.95, 46):
        a_ = np.nonzero(edge & (st[:, 1] < 0))[0]; p_ = np.nonzero(edge & (st[:, 1] > 0))[0]
        if not len(a_) or not len(p_): continue
        ia = a_[np.argmin(np.abs(st[a_, 0] - s0))]; ip_ = p_[np.argmin(np.abs(st[p_, 0] - s0))]; ws.append((s0, float(np.linalg.norm(X[ia] - X[ip_]))))
    wmax = max(ws, key=lambda x: x[1])
    # auricle-body angle: best-fit plane of the free front surface (behind the attachment notch, i.e. the front copy of the back sheet)
    bkkeys = {(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)) for v in np.nonzero(pb)[0]}
    free = np.array([v for v in np.nonzero(pf)[0] if (round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)) in bkkeys])
    P = X[free] - X[free].mean(0); nrm = np.linalg.svd(P)[2][2]; ang = float(np.degrees(np.arccos(min(1.0, abs(nrm @ n)))))
    # side-view (b,u) angles from vertical (positive = backward)
    sv = lambda v: float(np.degrees(np.arctan2(v @ b, v @ u)))
    chord = X[tip] - X[lobe_v]; c1 = X[cs['c1']]; c0 = X[cs['c0']]
    att = sv(c1 - c0); upper = sv(X[tip] - 0.5 * (X[cs['c1f']] + X[cs['P_up']]))
    # sweep: max distance of the side-view axis (mid-outline points) from the lobe -> tip chord
    mids = []
    for s0, _w in ws:
        a_ = np.nonzero(edge & (st[:, 1] < 0))[0]; p_ = np.nonzero(edge & (st[:, 1] > 0))[0]
        mids.append(0.5 * (X[a_[np.argmin(np.abs(st[a_, 0] - s0))]] + X[p_[np.argmin(np.abs(st[p_, 0] - s0))]]))
    mids = np.array(mids); c2 = np.array([chord @ b, chord @ u]); c2 /= np.linalg.norm(c2)
    rel2 = np.c_[(mids - X[lobe_v]) @ b, (mids - X[lobe_v]) @ u]; dev = rel2[:, 0] * c2[1] - rel2[:, 1] * c2[0]
    # thickness: front vertex to its back twin (same s, t)
    key = {(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9)): v for v in np.nonzero(pb)[0]}
    th = np.array([np.linalg.norm(X[v] - X[key[(round(float(st[v, 0]), 9), round(float(st[v, 1]), 9))]]) for v in free])
    thr = st[free]; up = thr[:, 0] > 0.85
    # tip angle in the ear plane: anterior / posterior outline points ~1 cm below the tip
    a_ = np.nonzero(edge & (st[:, 1] < 0))[0]; p_ = np.nonzero(edge & (st[:, 1] > 0))[0]
    def back_pt(cands):
        d = np.linalg.norm(X[cands] - X[tip], axis=1); return X[cands[np.argmin(np.abs(d - 1.0))]]
    va = back_pt(a_) - X[tip]; vp = back_pt(p_) - X[tip]; tipang = float(np.degrees(np.arccos(va @ vp / np.linalg.norm(va) / np.linalg.norm(vp))))
    ear = np.nonzero(np.isin(Lo['part'][:ns], ['front', 'back', 'rim']))[0]
    out['sides'][sd] = dict(
        length_lobe_to_tip_cm=L3, auricle_height_cm=float(U[ear].max() - U[ear].min()), auricle_height_over_HH=float((U[ear].max() - U[ear].min()) / rec['HH_cm']),
        max_width_cm=wmax[1], max_width_at_s=wmax[0], auricle_body_angle_deg=ang, total_lateral_extent_from_root_plane_cm=float(lat[ear].max()),
        tip_lateral_cm=float(lat[tip]), tip_back_of_root_cm=float(B[tip]), tip_above_root_cm=float(U[tip]),
        side_view_chord_lobe_to_tip_deg=sv(chord), side_view_attachment_line_deg=att, side_view_upper_extension_deg=upper, sweep_max_axis_deviation_cm=float(np.abs(dev).max()),
        thickness_cm=dict(median=float(np.median(th)), min=float(th.min()), p05=float(np.percentile(th, 5)), upper_extension_median=float(np.median(th[up])) if up.any() else None),
        tip_in_plane_angle_deg_at_1cm=tipang)
# anatomy presence: peak relief amplitude per system (cm) on the front sheet and the share of front vertices where it dominates
amp = {k: float(np.abs(v[fr[:ns] if len(fr) >= ns else Lo['part'] == 'front']).max()) for k, v in parts.items()} if False else {k: float(np.abs(v[Lo['part'] == 'front']).max()) for k, v in parts.items()}
out['anatomy_relief_peak_cm'] = amp
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps(out['sides']['l'], indent=0)[:1500]); print(amp)

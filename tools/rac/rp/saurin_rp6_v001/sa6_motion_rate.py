# sa6_motion_rate.py OUTDIR BODYDIR NAME [ARTDIR|-] [POSE] [F0] [F1] [STEP] : corrective-rate spike inspected in motion (offline bake validation order 8e3b7b4d §2.2).
#   The sweep's rate ratio is max |d corrective| per degree between NEIGHBOURING SWEEP SAMPLES over the sweep median; on poses outside the heavy-joint set the
#   samples are 0.125 apart, so a ratio is an average over up to ~16 deg.  Here the pose is played densely (default elbow_130_xneg, 0.50 -> 1.00, step 0.0025
#   = 0.33 deg) and per step the VISIBLE corrective motion is measured: the speed (cm/deg, max over the mesh) of the corrected surface relative to the
#   plain-LBS surface in posed space, for the packaged blend v004 ('prod') and, with ARTDIR, the baked artifact; plus the rest-space corrective rate and the
#   vertex / region where each peaks.  A pop = a narrow spike of relative speed; a smooth ramp = a broad rise.  extra_travel_per_30fps_frame = peak relative
#   speed x (full angle / 30), i.e. the corrective's own surface motion in one frame when the full move takes 1 s.  The neighbouring sweep metric
#   (peak / median over the dense playback) is recorded too, and frame_window = the EXACT relative travel over one 30 fps frame (max over the mesh).  -> OUTDIR/MR_<NAME>_<POSE>.json + .png (curves + filmstrip of the joint region at the peak).
import sys, os, json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
import sa6_correctives as CC, sa6_layer_harness as H, sa6_blend as BL
OD, BD, nm = sys.argv[1:4]; AD = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
pn = sys.argv[5] if len(sys.argv) > 5 else 'elbow_130_xneg'; F0 = float(sys.argv[6]) if len(sys.argv) > 6 else 0.50; F1 = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
ST = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0025; os.makedirs(OD, exist_ok=True)
b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); K = CC.Correctives.load(R, os.path.join(AD, 'BK_%s.json' % nm)) if AD else None
spec = R.suite('anat')[pn]; full = max(abs(dg) for _, _, _, dg in spec); FR = np.round(np.arange(F0, F1 + 1e-9, ST), 5); deg = ST * full
cols = ['prod'] + (['bake'] if K else [])
def frame(f):
    T = R.pose([(bb, p, a, dg * f) for bb, p, a, dg in spec]); dP = P0.delta(T); L = R.skin(T); o = {}
    for c in cols:
        d = dP + (K.delta(T) if c == 'bake' else 0); o[c] = (R.skin(T, R.V + d) - L, d)
    return L, o
rv = {c: [] for c in cols}; rvv = {c: [] for c in cols}; cr = {c: [] for c in cols}; crv = {c: [] for c in cols}; prev = None
W = max(1, int(round((full / 30.0) / deg))); hist = []; fw = {c: [] for c in cols}   # exact relative travel over one 30 fps frame window (W steps)
for f in FR:
    L, o = frame(f); hist.append({c: o[c][0] for c in cols}); hist = hist[-(W + 1):]
    if len(hist) == W + 1:
        for c in cols: fw[c].append(float(np.linalg.norm(hist[-1][c] - hist[0][c], axis=1).max()))
    if prev is not None:
        for c in cols:
            dv = np.linalg.norm(o[c][0] - prev[c][0], axis=1); dc = np.linalg.norm(o[c][1] - prev[c][1], axis=1)
            rv[c].append(dv.max() / deg); rvv[c].append(int(dv.argmax())); cr[c].append(dc.max() / deg); crv[c].append(int(dc.argmax()))
    prev = o
def region(v): return str(R.ql[np.nonzero((R.Q == v).any(1))[0][0]])
out = dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, pose=pn, artifact=os.path.join(AD, 'BK_%s.json' % nm) if AD else None, fractions=[float(x) for x in FR],
           degrees_full=float(full), step_deg=float(deg), columns={})
for c in cols:
    a = np.array(rv[c]); k = int(a.argmax()); med = float(np.median(a)); q = np.array(cr[c]); kq = int(q.argmax())
    out['columns'][c] = dict(relative_speed_cm_per_deg=[round(float(x), 5) for x in a], corrective_rate_cm_per_deg=[round(float(x), 5) for x in q],
        relative_speed=dict(peak_cm_per_deg=round(float(a.max()), 5), at=[float(FR[k]), float(FR[k + 1])], at_deg=[round(float(FR[k] * full), 2), round(float(FR[k + 1] * full), 2)],
                            vertex=rvv[c][k], region=region(rvv[c][k]), median_cm_per_deg=round(med, 5), peak_over_median=round(float(a.max() / max(med, 1e-9)), 3),
                            extra_travel_per_30fps_frame_cm=round(float(a.max()) * full / 30.0, 4), note='30 fps frame = the full %.0f deg move in 1 s (%.2f deg / frame)' % (full, full / 30.0)),
        frame_window=dict(steps=W, deg=round(W * deg, 4), max_relative_travel_cm=round(max(fw[c]) if fw[c] else float('nan'), 4),
                          at=(float(FR[int(np.argmax(fw[c]))]) if fw[c] else None), median_relative_travel_cm=round(float(np.median(fw[c])) if fw[c] else float('nan'), 4),
                          note='max over the mesh of |relative(f + one frame) - relative(f)|, exact, one frame = full angle / 30'),
        corrective_rate_peak=dict(value=round(float(q.max()), 5), at=[float(FR[kq]), float(FR[kq + 1])], vertex=crv[c][kq], region=region(crv[c][kq]), median=round(float(np.median(q)), 5)))
json.dump(out, open(os.path.join(OD, 'MR_%s_%s.json' % (nm, pn)), 'w'), indent=1)
c = cols[-1]; pk = out['columns'][c]['relative_speed']; vi = pk['vertex']; ks = int(np.searchsorted(FR, pk['at'][0]))
fig = plt.figure(figsize=(16, 9)); ax = fig.add_subplot(2, 1, 1); xs = (FR[:-1] + FR[1:]) / 2 * full
for cc, sty in zip(cols, ('b-', 'r-')): ax.plot(xs, out['columns'][cc]['relative_speed_cm_per_deg'], sty, label='corrective motion vs plain LBS (posed) ' + cc)
for cc, sty in zip(cols, ('b:', 'r:')): ax.plot(xs, out['columns'][cc]['corrective_rate_cm_per_deg'], sty, label='rest-space corrective rate ' + cc)
ax.set_xlabel('%s angle (deg of %.0f)' % (pn, full)); ax.set_ylabel('cm / deg'); ax.legend(fontsize=8); ax.grid(alpha=.3)
ax.set_title('%s %s: peak %.4f cm/deg at %.1f-%.1f deg (%s), %.2fx the playback median; %.3f cm per 30 fps frame' % (nm, pn, pk['peak_cm_per_deg'], pk['at_deg'][0], pk['at_deg'][1], pk['region'],
             pk['peak_over_median'], pk['extra_travel_per_30fps_frame_cm']), fontsize=9)
near = np.linalg.norm(R.V - R.V[vi], axis=1) < 9.0; sel = sorted({max(0, ks - 8), max(0, ks - 4), ks, min(len(FR) - 2, ks + 4), min(len(FR) - 2, ks + 8)})
for j, k in enumerate(sel):
    L0, o0 = frame(FR[k]); L1, o1 = frame(FR[k + 1]); Y = (L0 + o0[c][0])[near]; sp_ = np.linalg.norm((o1[c][0] - o0[c][0])[near], axis=1) / deg
    a2 = fig.add_subplot(2, len(sel), len(sel) + 1 + j); a2.scatter(Y[:, 1], Y[:, 2], c=sp_, s=1, cmap='inferno', vmin=0, vmax=max(0.02, pk['peak_cm_per_deg']))
    a2.set_aspect('equal'); a2.set_xticks([]); a2.set_yticks([]); a2.set_title('%.1f deg' % (FR[k] * full), fontsize=9)
fig.suptitle('%s in motion (%s; colour = corrective motion relative to plain LBS, cm/deg; side view of the joint region)' % (pn, c), fontsize=10); plt.tight_layout()
plt.savefig(os.path.join(OD, 'MR_%s_%s.png' % (nm, pn)), dpi=110); print(nm, pn, {cc: out['columns'][cc]['relative_speed'] for cc in cols}, flush=True)

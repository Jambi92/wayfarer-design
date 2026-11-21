# sa6_motion_gif.py OUT.gif BODYDIR NAME [ARTDIR|-] [POSE] [DEG0] [DEG1] [STEPDEG] : playback of a joint region for visual review in motion
#   (offline bake validation order 8e3b7b4d §2.2 elbow corrective-rate spike).  Side view of the joint region (9 cm around the vertex where the corrective's
#   visible motion peaks, from sa6_motion_rate.py), two panels per frame: the corrected surface (baked if ARTDIR else packaged blend v004) coloured by the
#   corrective's own displacement from plain LBS (cm), and the same vertices under plain LBS.  Default elbow_130_xneg 80 -> 100 deg in 0.5 deg steps.
import sys, os, json, io, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v005.json' if os.environ.get('RP6_RIG') == 'v002' else 'SA_RP6_creator_layers_v004.json')   # rig v002: layers v005
import sa6_correctives as CC, sa6_layer_harness as H, sa6_blend as BL
OUT, BD, nm = sys.argv[1:4]; AD = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None; pn = sys.argv[5] if len(sys.argv) > 5 else 'elbow_130_xneg'
D0 = float(sys.argv[6]) if len(sys.argv) > 6 else 80.0; D1 = float(sys.argv[7]) if len(sys.argv) > 7 else 100.0; SD = float(sys.argv[8]) if len(sys.argv) > 8 else 0.5
b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); K = CC.Correctives.load(R, os.path.join(AD, 'BK_%s.json' % nm)) if AD else None
spec = R.suite('anat')[pn]; full = max(abs(dg) for _, _, _, dg in spec); tag = 'baked' if K else 'packaged blend v004'
mr = os.path.join(os.path.dirname(OUT), 'MR_%s_%s.json' % (nm, pn)); vi = json.load(open(mr))['columns']['bake' if K else 'prod']['relative_speed']['vertex'] if os.path.exists(mr) else None
frames = []; degs = np.arange(D0, D1 + 1e-9, SD); sel = None; lim = None
for dgv in degs:
    f = dgv / full; T = R.pose([(bb, p, a, dg * f) for bb, p, a, dg in spec]); L = R.skin(T); d = P0.delta(T) + (K.delta(T) if K else 0); Pc = R.skin(T, R.V + d)
    if sel is None:
        c = vi if vi is not None else int(np.linalg.norm(Pc - L, axis=1).argmax()); sel = np.linalg.norm(R.V - R.V[c], axis=1) < 9.0
    dis = np.linalg.norm((Pc - L)[sel], axis=1)
    if lim is None: Y = Pc[sel]; lim = (Y[:, 1].min() - 2, Y[:, 1].max() + 2, Y[:, 2].min() - 2, Y[:, 2].max() + 2)
    fig, ax = plt.subplots(1, 2, figsize=(9, 4.6))
    for a_, P_, cc, t in ((ax[0], Pc, dis, '%s (colour = corrective displacement, cm)' % tag), (ax[1], L, None, 'plain LBS')):
        Y = P_[sel]; a_.scatter(Y[:, 1], Y[:, 2], c=(cc if cc is not None else '0.4'), s=1.2, cmap='inferno', vmin=0, vmax=1.5)
        a_.set_xlim(lim[0] - 6, lim[1] + 6); a_.set_ylim(lim[2] - 6, lim[3] + 6); a_.set_aspect('equal'); a_.set_xticks([]); a_.set_yticks([]); a_.set_title(t, fontsize=8)
    fig.suptitle('%s  %s  %.1f deg  (max corrective %.3f cm)' % (nm, pn, dgv, dis.max()), fontsize=10); buf = io.BytesIO(); plt.savefig(buf, dpi=80, format='png'); plt.close(fig)
    buf.seek(0); frames.append(Image.open(buf).convert('P', palette=Image.ADAPTIVE))
frames[0].save(OUT, save_all=True, append_images=frames[1:] + frames[::-1], duration=80, loop=0); print('wrote', OUT, len(frames), 'frames (forward + reverse)', flush=True)

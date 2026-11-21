# sa6_bake_playback.py OUTDIR BODYDIR NAME ARTDIR POSE [VERTEX|-] [RADIUS_CM] : visual playback review of a per-body bake (standards approval order c65e6c93 §3).
#   The approved provisional motion rule is a regression check; before a bake is accepted its worst motion cases are also reviewed in playback.
#   Playback speed = the motion rule's test speed: the pose's full range in 1 s at 30 fps (31 frames, 0 -> 1, frame k = k/30 of the full angle), played
#   forward then reversed (the evaluator is stateless, so reverse = forward).  Region = shaded mesh within RADIUS (default 10 cm) of VERTEX (default: the
#   local-rule worst vertex of MO_<NAME>.json in ARTDIR), viewed along that vertex's posed normal at the worst frame.  Two panels per frame:
#   baked (packaged blend v004 + K) and the packaged blend alone; colour = this frame's surface change relative to plain LBS since the previous frame
#   (|rel(k) - rel(k-1)|, cm, per-quad mean, 0 -> 0.5 cm), i.e. the per-frame excursion the motion rule measures, so a pop shows as a bright patch in one frame.
#   Writes  PB_<NAME>_<POSE>.gif (real time, 33 ms per frame), PB_<NAME>_<POSE>_slow.gif (x4 slower), PB_<NAME>_<POSE>_sheet.png (the 4 frames either side
#   of the worst frame pair, still), PB_<NAME>_<POSE>_curve.png (per-frame region maximum, bake vs blend), PB_<NAME>_<POSE>_break_sheet.png (frames around the largest
#   change of the per-frame rate, i.e. a slope break), PB_<NAME>_<POSE>.json (per-frame max change in the region and over the mesh, bake and blend).
import sys, os, io, json, ast, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
import sa6_correctives as CC, sa6_layer_harness as H, sa6_blend as BL
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa6_render.py')).read()   # shaded mesh = sa6_render.draw (not re-implemented)
exec(compile(ast.Module([n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in ('view_basis', 'draw')], []), 'sa6_render', 'exec'))
OD, BD, nm, AD, pn = sys.argv[1:6]; os.makedirs(OD, exist_ok=True)
VX = sys.argv[6] if len(sys.argv) > 6 else '-'; RAD = float(sys.argv[7]) if len(sys.argv) > 7 else 10.0; NF = 30
b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; R, z = BL.rig_of(nm, b, BD)
P0 = H.Blend(H.load_base(R, b['cfg']), [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); K = CC.Correctives.load(R, os.path.join(AD, 'BK_%s.json' % nm))
spec = R.suite('anat')[pn]; full = max(abs(dg) for _, _, _, dg in spec)
mo = os.path.join(AD, 'MO_%s.json' % nm); mrec = json.load(open(mo))['poses'].get(pn) if os.path.exists(mo) else None
v = int(VX) if VX != '-' else int((mrec['local'] if mrec and 'local' in mrec else mrec['bake'])['vertex'])
fr = np.arange(NF + 1) / NF; rel = {'bake': [], 'prod': []}; PC = []
for f in fr:
    T = R.pose([(bb, p, a, dg * f) for bb, p, a, dg in spec]); L = R.skin(T); dP = P0.delta(T); dK = K.delta(T)
    Pb = R.skin(T, R.V + dP + dK); Pp = R.skin(T, R.V + dP); rel['bake'].append(Pb - L); rel['prod'].append(Pp - L); PC.append((Pb, Pp))
ch = {c: np.array([np.zeros(R.nv)] + [np.linalg.norm(rel[c][k] - rel[c][k - 1], axis=1) for k in range(1, NF + 1)]) for c in rel}
reg = np.linalg.norm(R.V - R.V[v], axis=1) < RAD
kw = int(ch['bake'][:, reg].max(1).argmax())      # worst frame (bake) in the region
Pb = PC[kw][0]; nrm = np.zeros(3)
for q in np.nonzero((R.Q == v).any(1))[0]:
    a_ = Pb[R.Q[q]]; nrm += np.cross(a_[2] - a_[0], a_[3] - a_[1])
view = nrm / (np.linalg.norm(nrm) + 1e-12)
def frame(k, dpi=70):
    fig, ax = plt.subplots(1, 2, figsize=(9, 4.8))
    for j, (c, t) in enumerate((('bake', 'baked'), ('prod', 'packaged blend v004'))):
        P_ = PC[k][j]; draw(ax[j], R, P_, view, centre=P_[v], rad=RAD, vals=ch[c][k][R.Q].mean(1), vmax=0.5, cmap='YlOrRd')   # per-quad mean of the vertex change
        ax[j].set_title('%s  frame change max %.3f cm' % (t, ch[c][k][reg].max()), fontsize=8); ax[j].set_xticks([]); ax[j].set_yticks([]); ax[j].set_aspect('equal')
    fig.suptitle('%s  %s  frame %d/%d = %.1f deg  (30 fps, full range in 1 s; colour 0-0.5 cm change since previous frame)' % (nm, pn, k, NF, fr[k] * full), fontsize=8)
    buf = io.BytesIO(); plt.savefig(buf, dpi=dpi, format='png'); plt.close(fig); buf.seek(0); return Image.open(buf).convert('RGB')
ims = [frame(k) for k in range(NF + 1)]; pal = [im.convert('P', palette=Image.ADAPTIVE) for im in ims]
base = os.path.join(OD, 'PB_%s_%s' % (nm, pn))
pal[0].save(base + '.gif', save_all=True, append_images=pal[1:] + pal[::-1], duration=33, loop=0)
pal[0].save(base + '_slow.gif', save_all=True, append_images=pal[1:] + pal[::-1], duration=133, loop=0)
ks = list(range(max(0, kw - 4), min(NF, kw + 4) + 1)); W, Hh = ims[0].size; cols = 3; rows = (len(ks) + cols - 1) // cols
sheet = Image.new('RGB', (W * cols, Hh * rows), 'white')
for i, k in enumerate(ks): sheet.paste(ims[k], ((i % cols) * W, (i // cols) * Hh))
sheet.save(base + '_sheet.png')
rb = ch['bake'][1:, reg].max(1); kb = int(np.abs(np.diff(rb)).argmax()) + 2      # largest frame-to-frame change of the per-frame rate (slope break), bake
ks2 = list(range(max(1, kb - 3), min(NF, kb + 2) + 1)); sheet2 = Image.new('RGB', (W * cols, Hh * ((len(ks2) + cols - 1) // cols)), 'white')
for i, k in enumerate(ks2): sheet2.paste(ims[k], ((i % cols) * W, (i // cols) * Hh))
sheet2.save(base + '_break_sheet.png')
fig, ax = plt.subplots(figsize=(7, 3)); x = fr * full
for c, col, t in (('bake', 'r', 'baked'), ('prod', 'b', 'packaged blend v004')): ax.plot(x[1:], ch[c][1:, reg].max(1), col + '.-', lw=1, ms=3, label=t)
ax.axhline(0.5, color='k', ls='--', lw=0.8, label='0.50 cm cap'); ax.set_xlabel('angle at frame end (deg)'); ax.set_ylabel('region max change per frame (cm)')
ax.set_title('%s %s: per-frame surface change vs plain LBS (30 fps, full range in 1 s)' % (nm, pn), fontsize=8); ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(base + '_curve.png', dpi=90); plt.close(fig)
out = dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, pose=pn, artifact=os.path.join(AD, 'BK_%s.json' % nm), vertex=v, radius_cm=RAD, playback='full range in 1 s at 30 fps (frame = 1/30 of %.1f deg), forward + reverse' % full,
           worst_frame=kw, worst_frame_deg=round(float(fr[kw] * full), 2), rate_break_frame=kb, rate_break_deg=round(float(fr[kb] * full), 2),
           rate_break_cm_per_frame=[round(float(rb[kb - 2]), 4), round(float(rb[kb - 1]), 4)], motion_record=mrec and {k_: mrec[k_] for k_ in ('local', 'bake', 'prod', 'k') if k_ in mrec},
           per_frame={c: dict(region_max_cm=[round(float(x), 4) for x in ch[c][:, reg].max(1)], mesh_max_cm=[round(float(x), 4) for x in ch[c].max(1)]) for c in ch})
json.dump(out, open(base + '.json', 'w'), indent=1)
print(nm, pn, 'vertex', v, 'worst frame', kw, '%.1f deg' % (fr[kw] * full), 'region max bake %.3f blend %.3f' % (ch['bake'][kw][reg].max(), ch['prod'][kw][reg].max()), flush=True)

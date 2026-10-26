# nail_plate_inspect.py WDIR LANDMARKS.json OUTDIR : documented cap selection (WN-cap) vs groove-bounded plate correction (WN plate), rest v003,
# zoomed clay (no wire) + face classes + wireframe, per digit, both hands (order b303b9e §3 visual inspection).
#   red = plate faces (all 4 verts bound); dark red = plate boundary faces; blue = removed groove ring; orange = removed fold skin beyond the groove.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/tmp/claude-0/rt'); from common import PARTS
WD, LMF, O = sys.argv[1:4]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3'); os.makedirs(O + '/p', exist_ok=True)
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V = Z['V']; Q = np.asarray(Z['Q']); FP = Z['FP']
LM = json.load(open(LMF))['joints']; J = lambda k: np.array(LM[k]['position_source_frame_cm']); FIT5 = json.load(open('/tmp/claude-0/rt/rpr/fit_v005.json'))
CAP = json.load(open(WD + '/weights_WNcap_log.json'))['digits']; PL = json.load(open(WD + '/weights_WN_log.json'))['digits']
CL = [0.80, 0.77, 0.73]; rows = []
for s in 'lr':
    hp = [i for i, n in enumerate(PARTS) if n.endswith('_' + s) and n.startswith(('hand', 'thumb', 'index', 'middle', 'ring', 'pinky'))]
    Qh = Q[np.isin(FP, hp)]; mesh = O + '/p/hand_%s.npz' % s
    if not os.path.exists(mesh): np.savez(mesh, V=V, Q=Qh)
    np.save(O + '/p/clay.npy', np.tile(CL, (len(V), 1)).astype(np.float32))
    for fg in ('index', 'middle', 'ring', 'pinky', 'thumb'):
        k = '%s_%s' % (fg, s); cap = np.array(CAP[k]['vertex_ids']); pl = np.array(PL[k]['vertex_ids'])
        jd = '%s_dip_%s' % (fg, s) if fg != 'thumb' else 'thumb_ip_' + s; D, tp = J(jd), J('%s_tip_%s' % (fg, s)); dor = np.array(FIT5['cx_' + jd]['dorsal'])
        L3 = np.linalg.norm(tp - D); u = (tp - D) / L3; dor = dor - (dor @ u) * u; dor /= np.linalg.norm(dor); lat = np.cross(u, dor)
        cls = np.zeros(len(V), int); cls[cap] = 2; cls[pl] = 1
        removed = np.setdiff1d(cap, pl); conc = np.zeros(len(V));
        g = np.array(PL[k]['groove_ring_ids']) if 'groove_ring_ids' in PL[k] else np.array([], int)
        cls[g] = 3
        fc = cls[Qh]; c = np.tile(CL, (len(Qh), 1))
        c[(fc == 2).any(1)] = [1.0, 0.62, 0.15]; c[(fc == 3).any(1)] = [0.15, 0.35, 0.95]; c[(fc == 1).any(1)] = [0.45, 0.05, 0.05]; c[(fc == 1).all(1)] = [0.95, 0.38, 0.38]
        np.save(O + '/p/c_%s.npy' % k, c.astype(np.float32))
        ctr = D + u * 0.7 * L3; h = 0.85 * L3
        vs = ';'.join('%s:%.4f,%.4f,%.4f:%.3f,%.3f,%.3f:%.2f' % (nm, *dv, *ctr, h) for nm, dv in (('dorsal', dor), ('lat', lat + 0.3 * dor), ('med', -lat + 0.3 * dor), ('tip', u + 0.5 * dor)))
        for tg, cf, wf in (('clay', O + '/p/clay.npy', '0'), ('cls', O + '/p/c_%s.npy' % k, '0'), ('wire', O + '/p/c_%s.npy' % k, '1')):
            if not os.path.exists(O + '/p/%s_%s_tip.png' % (k, tg)):
                subprocess.run([BP, T + '/render_attr.py', '--', mesh, cf, O + '/p', '%s_%s' % (k, tg), vs, wf, '500'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        rows.append((k, len(cap), len(pl), len(g), len(removed) - len(g), PL[k]))
cell = 230; S = Image.new('RGB', (12 * cell + 10, 76 + len(rows) * (cell + 30)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'WN nail selection inspection, frozen v003 rest: documented distal-cap set vs groove-bounded plate correction (subset only; nothing added)', fill=(0, 0, 0), font=f(18, True))
x = 10
for nm, cc in (('plate: bound 100 % to distal bone (WN)', (0.95, 0.38, 0.38)), ('plate boundary face', (0.45, 0.05, 0.05)), ('removed: groove ring (keeps W0)', (0.15, 0.35, 0.95)), ('removed: fold / tip skin beyond groove (keeps W0)', (1.0, 0.62, 0.15))):
    dr.rectangle([x, 40, x + 14, 54], fill=tuple(int(255 * v) for v in cc)); dr.text((x + 18, 39), nm, fill=(0, 0, 0), font=f(13)); x += 40 + int(dr.textlength(nm, font=f(13)))
dr.text((10, 58), 'columns: clay dorsal / lateral / medial / tip | classes (same 4 views) | classes + wireframe (same 4 views)', fill=(60, 60, 60), font=f(12))
for ri, (k, nc, npl, ng, nf, d) in enumerate(rows):
    y = 76 + ri * (cell + 30); dr.text((6, y + 2), '%s -> %s : documented cap %d verts, plate %d, removed groove ring %d + beyond-groove skin %d' % (k, d['bone'], nc, npl, ng, nf), fill=(150, 20, 20), font=f(13, True))
    for gi, tg in enumerate(('clay', 'cls', 'wire')):
        for vi, v in enumerate(('dorsal', 'lat', 'med', 'tip')):
            S.paste(Image.open(O + '/p/%s_%s_%s.png' % (k, tg, v)).convert('RGB').resize((cell, cell), Image.LANCZOS), (5 + (gi * 4 + vi) * cell, y + 24))
S.save(O + '/N_nail_selection_cap_vs_plate.jpg', quality=86); print('sheet', O + '/N_nail_selection_cap_vs_plate.jpg')

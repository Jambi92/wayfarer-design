# RAC W3D: matched-camera FPI comparison sheet (Saurin W2 reference + Part 7 coupled minimum corner, most projecting valid MF / GR / GO,
# Skarn C1R and C2). Same ortho scale (44 cm) for every head; camera centred mid-way between FAL and Op (f) and 3 cm below the eye centres (u).
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.dirname(D))
import w3b_common as C, w3b_sheet as SS, w3b_orbit_run as OR, arm_measure as AM
S = C.S; R = S + '/w3d/rend'; os.makedirs(R, exist_ok=True); RV = '/home/claude/wayfarer-design/reviews'
SF = json.load(open(S + '/w3d/saurin_fpi.json')); HF = json.load(open(S + '/w3d/human_fpi.json'))
L = OR.labels(); E = np.array([C.head_world(np.array([s * C.EYE0['x'], C.EYE0['f'], C.EYE0['u']])) for s in (1, -1)]).mean(0)
ROWS = [('sa_ref', 'saurin', S + '/w3d/W2_reference.npy', 'Saurin W2 reference\nr3 FPI %.4f' % SF['W2_reference']['pitch+0']['FPI']),
        ('sa_min', 'saurin', S + '/w3d/W2_coupled_min_corner.npy', 'Saurin min-valid corner\n(Part 7 0.255) r3 %.4f' % SF['W2_coupled_min_corner']['pitch+0']['FPI']),
        ('mf_max', 'human', RV + '/rac-w1c-evidence/geometry/MF-FACE-PROJ-MAX', 'MF-FACE-PROJ-MAX\n(accepted max-valid) %.4f' % HF['MF-FACE-PROJ-MAX']['FPI']),
        ('gr', 'human', S + '/w2c/b/GR239/GR239', 'Grask GR239 (W2 body)\nGR-FACE-14 NOT RUN %.4f' % HF['GR239 (W2 body max)']['FPI']),
        ('go', 'human', S + '/w2d/b/GO251/GO251', 'Gorrund GO251 (W2 body)\nGOR-FACE-05 NOT RUN %.4f' % HF['GO251 (W2 body max)']['FPI']),
        ('sk_c1r', 'human', S + '/w3d/b/SK208-C1R', 'Skarn SK208-C1R\n(central reference) %.4f' % HF['SK208-C1R']['FPI']),
        ('sk_c2', 'human', S + '/w3c/b/SKM190-C2', 'Skarn SKM190-C2\n(stronger valid) %.4f' % HF['SKM190-C2']['FPI'])]
def prep(tag, kind, p):
    if kind == 'saurin':
        P = np.load(p).astype(float); Fa = C.F0; hd = L.head > 0.5; e = E
        fal = P[hd & (np.abs(P[:, 0]) < 1)][:, 1].max(); op = P[hd & (P[:, 2] > 176)][:, 1].min(); box = lambda Q: hd
    else:
        d = np.load(p + '_r6.npz', allow_pickle=True); P = d['V'].astype(float); Fa = d['F']; keep = d['keep'].astype(bool); c = AM.cranio(d, P, Fa, keep)
        e = 0.5 * (d['eye_l'] + d['eye_r']); fal = c['FAL'][1]; op = c['Op'][1]; me = c['Me'][2]; box = lambda Q: keep & (Q[:, 2] > me - 7)
    cf = 0.5 * (fal + op); cu = e[2] - 3.0
    v = "F:0:0:0:%.2f:%.2f:44;P:90:0:0:%.2f:%.2f:44;Q:35:6:0:%.2f:%.2f:44" % ((cf, cu) * 3)
    if not all(os.path.exists('%s/%s_%s.png' % (R, tag, n)) for n in 'FPQ'):
        C.save_head_npz(R + '/%s.npz' % tag, P, Fa, box); C.render(R + '/%s.npz' % tag, R + '/' + tag, v, 700); os.remove(R + '/%s.npz' % tag)
for t, k, p, _ in ROWS: prep(t, k, p)
cell = 300; lw = 260; top = 130; cols = ['P', 'Q', 'F']
img = Image.new('RGB', (lw + cell * 3, top + cell * len(ROWS) + 10), 'white'); d = ImageDraw.Draw(img)
d.text((14, 12), 'W3D - RM-CF-05 FPI comparison (matched camera, 44 cm ortho)', font=SS.font(24), fill='black')
d.text((14, 48), 'r3 FPI = (FAL.f - eye-centre.f) / HL. Saurin: naked W2 base; humans: R-6 ARM skin. Neutral grey, no hair.', font=SS.font(15), fill=(70, 70, 70))
d.text((14, 70), 'Gap to the Saurin minimum corner is the RM-CF-05 quantity; the margin itself is an author decision.', font=SS.font(15), fill=(70, 70, 70))
for j, l in enumerate(['profile', 'three-quarter', 'front']): d.text((lw + j * cell + 6, top - 24), l, font=SS.font(15), fill=(70, 70, 70))
for i, (t, _, _, lab) in enumerate(ROWS):
    d.multiline_text((10, top + i * cell + cell // 2 - 20), lab, font=SS.font(15), fill='black', spacing=4)
    for j, n in enumerate(cols):
        f = '%s/%s_%s.png' % (R, t, n)
        if os.path.exists(f):
            im = Image.open(f).convert('RGBA').resize((cell, cell), Image.LANCZOS); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); img.paste(bg, (lw + j * cell, top + i * cell))
img.save(S + '/w3d/sheets/w3d_3_fpi_comparison.jpg', quality=88); print(S + '/w3d/sheets/w3d_3_fpi_comparison.jpg')

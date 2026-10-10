# RAC W3B1 section 9 (extreme-body transport): close views of failing fields on the composition extremes.
# Columns: unsurfaced body base (inverted base faces = composition deformation fold), R0 carried relief (W2 convention, raw normals),
# R3 carried relief along smoothed-base normals (minimal transport fix), R2 re-evaluated core + smoothed normals. Camera re-centred on the body.
# Also: distance from residual 'clean-base' folds (R3) to the nearest inverted base face.
import os, sys, json, numpy as np, igl
from scipy.spatial import cKDTree
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG, w3b_bodies as BD, w3b_sheet as SS, w3b1_transport as TR
CASES = [('SA-M188-MUHI', 'S_dorsal_tail'), ('SA-M188-MUHI', 'A_axilla'), ('SA-M188-FAHI', 'S_shin'), ('SA-M188-FAHI', 'S_lateral_trunk'),
         ('SA-M188-FAHI', 'A_lower_trunk_flexion'), ('SA-M188-N-FAHI', 'S_dorsal_hand')]
COLS = [('base', 'unsurfaced body base'), ('R0', 'R0 carried (W2)'), ('R3', 'R3 carried + smoothed normals'), ('R2', 'R2 re-evaluated + smoothed N')]
Z = SC.ref(); Fu = Z['Fu']; Vc = Z['Vu']; masks = RG.masks(); dist = {}; built = {}
for bid, f in CASES:
    if bid not in built:
        P = BD.build(bid); Vu, _ = igl.upsample(P, C.F0); built = {bid: (Vu, igl.per_vertex_normals(Vu, Fu), TR.smooth_normals(Vu, Fu), bid.split('-')[-1])}
    Vu, Nr, Ns, _ = built[bid]; k = {b: hh for b, _, hh in BD.bodies()}[bid] / 188.0
    core = SC.weight(masks[f]) >= 0.9
    if (Vc[core, 0] > 1.0).mean() > 0.3 and (Vc[core, 0] < -1.0).mean() > 0.3: core = core & (Vc[:, 0] > 1.0)
    Pc = Vu[core]; n = Nr[core].mean(0); n /= np.linalg.norm(n); c = np.median(Pc, 0); ext = np.percentile(np.linalg.norm(Pc - c, axis=1), 80)
    sc = float(np.clip(2.0 * ext, 2.5, 16.0)); a = np.degrees(np.arctan2(n[0], n[1])); e = np.degrees(np.arcsin(np.clip(n[2], -0.95, 0.95)))
    view = 'c:%.1f:%.1f:%.2f:%.2f:%.2f:%.2f' % (a, e, c[0], c[1], c[2], sc); box = lambda X, c=c, sc=sc: np.linalg.norm(X - c, axis=1) < 0.9 * sc
    aff = np.unique(Fu[np.where((SC.weight(masks[f]) >= 0.9)[Fu].all(1))[0]].ravel())
    rel1 = Z['disp'].copy(); rel1[aff] = Z['disp'][aff] + Z['ATT'][aff] * (TR.reeval(Vu, Nr, aff, k) - TR.reeval(Vc, Z['N'].astype(float), aff, 1.0))
    S = {'base': Vu, 'R0': Vu + Z['disp'][:, None] * Nr, 'R3': Vu + Z['disp'][:, None] * Ns, 'R2': Vu + rel1[:, None] * Ns}
    for nm, X in S.items(): SS.ensure('tr_%s_%s_%s' % (bid, f, nm), X, Fu, view, res=700, box=box)
    fm = np.where((SC.weight(masks[f]) >= 0.9)[Fu].all(1))[0]; cr = lambda Q: np.cross(Q[Fu[fm, 1]] - Q[Fu[fm, 0]], Q[Fu[fm, 2]] - Q[Fu[fm, 0]])
    nb = cr(Vu); binv = (nb * cr(Vc)).sum(1) < 0; fl = ((cr(S['R3']) * nb).sum(1) < 0) & ~binv; cen = Vu[Fu[fm]].mean(1)
    if binv.any() and fl.any():
        d = cKDTree(cen[binv]).query(cen[fl])[0]; dist['%s/%s' % (bid, f)] = dict(n=int(fl.sum()), median_cm=float(np.median(d)), p90_cm=float(np.percentile(d, 90)), within_2cm=float((d < 2).mean()))
    else: dist['%s/%s' % (bid, f)] = dict(n=int(fl.sum()), base_inverted=int(binv.sum()))
    print(bid, f, dist['%s/%s' % (bid, f)], flush=True)
json.dump(dist, open(C.W + '/w3b1_transport_dist.json', 'w'), indent=1)
cell = 300; lw = 240; top = 110
img = Image.new('RGB', (lw + cell * len(COLS), top + cell * len(CASES) + 10), 'white'); d = ImageDraw.Draw(img)
d.text((14, 12), 'W3B1 - extreme-body surface transport: carried vs reconstructed (close views, canonical relief x1)', font=SS.font(22), fill='black')
d.text((14, 44), 'Same field identity, size / relief multipliers and seed indices on every route. Diagnostic copies only.', font=SS.font(15), fill=(70, 70, 70))
for j, (_, l) in enumerate(COLS): d.text((lw + j * cell + 6, top - 26), l, font=SS.font(15), fill=(70, 70, 70))
for i, (bid, f) in enumerate(CASES):
    d.multiline_text((10, top + i * cell + cell // 2 - 20), '%s\n%s' % (bid.replace('SA-M188-', 'SA-M188 '), f), font=SS.font(15), fill='black')
    for j, (nm, _) in enumerate(COLS):
        p = '%s/tr_%s_%s_%s_c.png' % (SS.R, bid, f, nm)
        if os.path.exists(p):
            im = Image.open(p).convert('RGBA').resize((cell, cell), Image.LANCZOS); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); img.paste(bg, (lw + j * cell, top + i * cell))
img.save(SS.SH + '/w3b1_extreme_transport.jpg', quality=88); print(SS.SH + '/w3b1_extreme_transport.jpg')

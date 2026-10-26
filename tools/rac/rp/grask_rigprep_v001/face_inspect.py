# face_inspect.py WORKDIR OUTDIR SPEC... : representative flagged-face inspection panels (order b303b9e §5).
# SPEC = label:pose:tag:face_id   (pose/tag -> WORKDIR/diag/posed/{pose}_full_{tag}.npz or {pose}{tag}.npz, ids alongside)
# Per face: local crop (faces within 3 cm of the face centre in the posed mesh), three orthographic views (face normal, two 60-deg obliques)
# with wireframe; flagged face = red, edge-adjacent faces = yellow, faces it intersects = blue, other flagged faces of the same class = pink;
# vertex indices projected on the image. Text: quad vertex ids, both triangulations (areas rest/posed, the two triangle normals' dot),
# normal vs skinned-reference normal, vs neighbour-normal sum, dihedral to each neighbour, intersection partners, and a
# DEMONSTRATED / SUSPECTED statement derived from those numbers.
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from common import PARTS
W, O = sys.argv[1:3]; SPECS = sys.argv[3:]; T = os.path.dirname(os.path.abspath(__file__)); BP = os.environ.get('BP', '/home/claude/stc/bin/python3'); os.makedirs(O + '/fi', exist_ok=True)
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q']); FP = Z['FP']
Es = np.sort(np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]), 1); ue, inv = np.unique(Es, axis=0, return_inverse=True); inv = inv.ravel()
o = np.argsort(inv, kind='stable'); EF = np.tile(np.arange(len(Q)), 4)[o].reshape(-1, 2)
NB = {}
for a, b in EF: NB.setdefault(a, []).append(b); NB.setdefault(b, []).append(a)
def qn(V, q): n = np.cross(V[q[2]] - V[q[0]], V[q[3]] - V[q[1]]); return n / max(np.linalg.norm(n), 1e-12)
def tri(V, a, b, c): x = np.cross(V[b] - V[a], V[c] - V[a]); return 0.5 * np.linalg.norm(x), x / max(np.linalg.norm(x), 1e-12)
cell = 470; panels = []
import textwrap
for sp in SPECS:
    lab, pose, tag, fid = sp.split(':'); fid = int(fid)
    base = '%s/diag/posed/%s%s.npz' % (W, pose, tag); V = np.load(base)['V'].astype(float); ids = np.load('%s/diag/ids/%s%s.npz' % (W, pose, tag))
    q = Q[fid]; c = V[q].mean(0); n = qn(V, q); n0 = qn(V0, q)
    C = V[Q].mean(1); near = np.nonzero(np.linalg.norm(C - c, axis=1) < 3.0)[0]
    adj = NB[fid]; prs = ids['pairs']; partners = sorted(set(prs[prs[:, 0] == fid, 1].tolist()) | set(prs[prs[:, 1] == fid, 0].tolist())) if len(prs) else []
    cls_of = {}
    if len(prs):
        for (a_, b_), k in zip(prs, ids['pair_class']):
            if fid in (a_, b_): cls_of[int(b_ if a_ == fid else a_)] = ['non-contact', 'crease', 'contact'][k]
    near = np.unique(np.r_[near, partners, adj]).astype(int)
    col = np.tile([0.80, 0.77, 0.73], (len(near), 1)); pos = {g: i for i, g in enumerate(near)}
    for g in ids['orientation_fail_faces']:
        if g in pos: col[pos[g]] = [0.98, 0.72, 0.85]
    for g in ids['inversion_faces']:
        if g in pos: col[pos[g]] = [0.6, 0.9, 0.95]
    for g in adj: col[pos[g]] = [1.0, 0.85, 0.2]
    for g in partners: col[pos[g]] = [0.2, 0.4, 0.95]
    col[pos[fid]] = [0.9, 0.1, 0.1]
    m = O + '/fi/%s.npz' % lab; np.savez(m, V=V, Q=Q[near]); np.save(m[:-4] + '_c.npy', col.astype(np.float32))
    up = np.array([0, 0, 1.0]) if abs(n[2]) < 0.9 else np.array([0, 1.0, 0]); t1 = np.cross(n, up); t1 /= np.linalg.norm(t1)
    views = (('n', n), ('o1', 0.5 * n + 0.866 * t1), ('o2', 0.5 * n - 0.866 * t1)); h = float(np.clip(7 * np.sqrt(max(tri(V0, q[0], q[1], q[2])[0] * 2, 1e-6)), 0.7, 1.8))
    vs = ';'.join('%s:%.5f,%.5f,%.5f:%.4f,%.4f,%.4f:%.2f' % (nm, *dv, *c, h) for nm, dv in views)
    subprocess.run([BP, T + '/render_attr.py', '--', m, m[:-4] + '_c.npy', O + '/fi', lab, vs, '1', '700'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=dict(os.environ, WIRE_T='0.00012'))
    imgs = []
    for nm, _ in views:
        im = Image.open('%s/fi/%s_%s.png' % (O, lab, nm)).convert('RGB'); cam = json.load(open('%s/fi/%s_%s.json' % (O, lab, nm))); dr = ImageDraw.Draw(im)
        cx, cy, ch = np.array(cam['c']), np.array(cam['y']), cam['h']; cxv = np.array(cam['x']); px = cam['px']; dd = np.array(cam['d'])
        for v in q:
            p = V[v] - cx
            if p @ dd < -0.3: continue
            X = px / 2 + (p @ cxv) / ch * px / 2; Y = px / 2 - (p @ cy) / ch * px / 2; dr.ellipse([X - 3, Y - 3, X + 3, Y + 3], fill=(0, 0, 0)); dr.text((X + 4, Y - 14), str(v), fill=(0, 0, 0), font=f(15, True))
        imgs.append(im.resize((cell, cell), Image.LANCZOS))
    # numbers
    L = []
    a1, n1 = tri(V, q[0], q[1], q[2]); a2, n2 = tri(V, q[0], q[2], q[3]); b1, m1 = tri(V, q[1], q[2], q[3]); b2, m2 = tri(V, q[1], q[3], q[0])
    A1, _ = tri(V0, q[0], q[1], q[2]); A2, _ = tri(V0, q[0], q[2], q[3]); B1, _ = tri(V0, q[1], q[2], q[3]); B2, _ = tri(V0, q[1], q[3], q[0])
    ns = sum(qn(V, Q[g]) for g in adj); ns0 = sum(qn(V0, Q[g]) for g in adj)
    dih = [(int(g), float(np.degrees(np.arccos(np.clip(qn(V, Q[g]) @ n, -1, 1)))), float(np.degrees(np.arccos(np.clip(qn(V0, Q[g]) @ n0, -1, 1))))) for g in adj]
    is_or = fid in set(ids['orientation_fail_faces'].tolist()); is_inv = fid in set(ids['inversion_faces'].tolist())
    folded_tri = (n1 @ n2) < 0 or (m1 @ m2) < 0
    L += ['%s  —  face %d (%s) in %s [%s]' % (lab, fid, PARTS[FP[fid]], pose, tag.strip('_')),
          'quad vertices %s; flags: orientation failure %s, local fold/inversion indicator %s, intersects %d faces' % (q.tolist(), is_or, is_inv, len(partners)),
          'triangulation 0-2: areas %.3f / %.3f cm2 (rest %.3f / %.3f), tri-normal dot %+.2f' % (a1, a2, A1, A2, n1 @ n2),
          'triangulation 1-3: areas %.3f / %.3f cm2 (rest %.3f / %.3f), tri-normal dot %+.2f' % (b1, b2, B1, B2, m1 @ m2),
          'quad area posed/rest %.2f; normal . rest normal %+.2f; normal . neighbour-sum %+.2f (rest %+.2f)' % ((a1 + a2) / max(A1 + A2, 1e-12), n @ n0, n @ ns / max(np.linalg.norm(ns), 1e-12), n0 @ ns0 / max(np.linalg.norm(ns0), 1e-12)),
          'dihedral to neighbours posed (rest) deg: ' + ', '.join('%d %.0f (%.0f)' % x for x in dih),
          'intersecting faces: ' + (', '.join('%d %s [%s]' % (g, PARTS[FP[g]], cls_of.get(g, '?')) for g in partners[:8]) or 'none')]
    dem = []; sus = []
    if partners: dem.append('surface self-intersection (BVH overlap with %d non-adjacent faces)' % len(partners))
    if folded_tri: dem.append('the quad itself is folded (its two triangles face opposite ways in at least one triangulation)')
    if is_inv and any(x[1] > 120 for x in dih): dem.append('local fold: dihedral > 120 deg to an edge neighbour')
    if is_or and not is_inv and not folded_tri and not partners: sus.append('orientation disagreement only: the face turned away from its skinned reference normal but is consistent with its neighbours — a tilted, compressed sheet, not proven inverted')
    if is_or and (n @ n0) > 0: sus.append('normal still within 90 deg of its rest normal: the disagreement is with the skinned reference (LBS rotation of the rest normal), not with rest geometry')
    ar = (a1 + a2) / max(A1 + A2, 1e-12)
    if ar < 0.25: dem.append('the quad collapsed to %.0f %% of its rest area (loop compression)' % (100 * ar))
    if not dem: dem.append('no inversion or intersection is demonstrated for this face by the measurements above')
    L += textwrap.wrap('DEMONSTRATED: ' + '; '.join(dem), 175) + textwrap.wrap('SUSPECTED: ' + ('; '.join(sus) if sus else '—'), 175, subsequent_indent='   ')
    panels.append((imgs, L))
S = Image.new('RGB', (3 * cell + 20, 60 + len(panels) * (cell + 260)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'Representative flagged faces — indexed wireframe, triangulation / area, adjacent faces and intersections, 3 views each (posed, 3 cm crop)', fill=(0, 0, 0), font=f(17, True))
x = 10
for nm, cc in (('flagged face', (0.9, 0.1, 0.1)), ('edge neighbours', (1.0, 0.85, 0.2)), ('faces it intersects', (0.2, 0.4, 0.95)), ('other orientation-disagreement faces', (0.98, 0.72, 0.85)), ('other local fold/inversion indicator faces', (0.6, 0.9, 0.95))):
    dr.rectangle([x, 36, x + 14, 50], fill=tuple(int(255 * v) for v in cc)); dr.text((x + 18, 35), nm, fill=(0, 0, 0), font=f(13)); x += 40 + int(dr.textlength(nm, font=f(13)))
for i, (imgs, L) in enumerate(panels):
    y = 60 + i * (cell + 260)
    for j, im in enumerate(imgs): S.paste(im, (5 + j * (cell + 5), y))
    for k, l in enumerate(L): dr.text((10, y + cell + 6 + 22 * k), l, fill=(150, 20, 20) if k == 0 else ((0, 90, 0) if l.startswith('DEMON') else ((120, 60, 0) if l.startswith(('SUSP', '   ')) else (0, 0, 0))), font=f(13, k == 0 or l.startswith(('DEMON', 'SUSP'))))
S.save(O + '/I_flagged_face_inspection.jpg', quality=86); print('sheet', O + '/I_flagged_face_inspection.jpg')

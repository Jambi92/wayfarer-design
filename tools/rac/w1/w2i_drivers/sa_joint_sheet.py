# RAC W2I1 D3: author-review sheet of the J-2 construction joints on the frozen SA-M188 (front / profile / rear 3/4; joints drawn as 1.6 cm
# marker spheres merged into a COPY of the mesh for display only; nothing is written back). Usage: python3 sa_joint_sheet.py JOINTS.json
import sys, json, os, numpy as np, trimesh
from PIL import Image, ImageDraw
import sa_render as R
J = json.load(open(sys.argv[1]))['base']; P = np.load(R.W + '/npz/SA-M188.npz')['v'].astype(float); f = R.F.copy()
for k, r in J.items():
    s = trimesh.creation.icosphere(2, 1.6); f = np.vstack([f, s.faces + len(P)]); P = np.vstack([P, s.vertices + np.array(r['point'])])
fn = R.W + '/rend/_tmpj.npz'; np.savez(fn, P=P.astype(np.float32), f=f.astype(np.int32)); tag = R.W + '/rend/SA-M188-J2'
# x-ray-ish: render the joints alone too, then overlay with transparency
R.subprocess.run(['python3', R.RC], env=dict(os.environ, VIEWS=R.VIEWS, NPZ=fn, TAG=tag, RES='700'), stdout=R.subprocess.DEVNULL, stderr=R.subprocess.DEVNULL)
Q = np.zeros((0, 3)); g = np.zeros((0, 3), int)
for k, r in J.items():
    s = trimesh.creation.icosphere(2, 1.6); g = np.vstack([g, s.faces + len(Q)]); Q = np.vstack([Q, s.vertices + np.array(r['point'])])
Q = np.vstack([Q, [[0, 0, 0], [0, 0, 187.88]]]); fn2 = R.W + '/rend/_tmpj2.npz'; np.savez(fn2, P=Q.astype(np.float32), f=g.astype(np.int32)); tag2 = R.W + '/rend/SA-M188-J2only'
R.subprocess.run(['python3', R.RC], env=dict(os.environ, VIEWS=R.VIEWS, NPZ=fn2, TAG=tag2, RES='700'), stdout=R.subprocess.DEVNULL, stderr=R.subprocess.DEVNULL)
row = []
for v in ('front', 'profile', 'rear34'):
    a = Image.open('%s_%s.png' % (tag, v)).convert('RGBA'); bg = Image.new('RGBA', a.size, 'white'); bg.alpha_composite(a)
    b = Image.open('%s_%s.png' % (tag2, v)).convert('RGBA'); al = np.array(b)[..., 3] > 0; arr = np.array(bg); arr[al] = (0.45 * arr[al] + 0.55 * np.array([210, 30, 30, 255])).astype(np.uint8)
    row.append(Image.fromarray(arr).convert('RGB'))
w, h = row[0].size; out = Image.new('RGB', (w * 3, h + 40), 'white')
for i, im in enumerate(row): out.paste(im, (i * w, 40))
ImageDraw.Draw(out).text((8, 10), 'W2I1 D3 J-2 construction joints on frozen SA-M188 (Gate 4 / 5 B1 axes: shoulder, elbow, wrist, MCP-III, hip, knee, ankle; red = joint centres seen through the body)', fill='black')
out.save(R.W + '/sheets/sa_j2_joints.jpg', quality=88); print('saved')

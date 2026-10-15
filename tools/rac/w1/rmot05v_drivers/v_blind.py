# RM-OT-05V replicated neutralized structural-readability gate: sheet builder (additive; k_blind.py / o_gate_eval.py unchanged).
# Protocol carried from 05K / 05N / 05O (PREREGISTRATION in reviews/rac-rmot05o-evidence/blind):
#   the SAME frozen control tiles (8 human-family controls MF/SK x ref/nar/brd/low + Grask E3 ref + low; headless F + P renders
#   cached by the 05O run) + the Gorrund candidate under the fixed key name GO-S-ref; body only (head and neck removed at the
#   source-lineage neck root z 191, the 05N cut), tail not shown (05O: "the tail is not part of the REF / LOW meshes"),
#   height-normalized front + profile, neutral grey + black silhouette, fresh shuffle per run, codes only, key kept separately.
# DIFFERENCE (disclosed): no Gorrund LOW exists (variants are authorized only after ARM acceptance, order §9), so each sheet has 11 bodies
#   and criterion C1 (REF and LOW group together) and the LOW half of C5 cannot be evaluated.
# Usage: python3 v_blind.py STATE.npz TAIL.obj CONTROL_TILE_DIR OUTDIR run1|run2
import sys, os, json, subprocess, tempfile, numpy as np, trimesh
from PIL import Image, ImageDraw, ImageFont
st, tailp, ctl, out, run = sys.argv[1:6]; os.makedirs(out, exist_ok=True)
CTRL = ['MF-ref', 'MF-nar', 'MF-brd', 'MF-low', 'SK-ref', 'SK-nar', 'SK-brd', 'SK-low', 'GR-E3-ref', 'GR-E3-low']
CTAG = 'K05a_GO-RD3'                    # the 05O run-1 cache (identical frozen controls in every 05K/05N/05O run)
SEED, LET = {'run1': (20261401, 'V'), 'run2': (20261402, 'W')}[run]
d = np.load(st); V = d['V'].astype(float); F = d['F']
keep = V[F].mean(1)[:, 2] <= 191.0                                        # head and neck removed at the neck root
tm = trimesh.load(tailp, process=False); from scipy.spatial import cKDTree
c = V[F].mean(1); dt = cKDTree(np.asarray(tm.vertices)).query(c)[0]; keep &= ~((dt < 2.5) & (c[:, 1] < -13.0))   # tail not shown
Fk = F[keep]; u = np.unique(Fk); mp = -np.ones(len(V), int); mp[u] = np.arange(len(u)); Vk = V[u]; Fk = mp[Fk]
tmp = tempfile.mkdtemp(); np.savez(os.path.join(tmp, 'b.npz'), V=Vk, F=Fk)
BL = r'''
import bpy, sys, json, numpy as np
from mathutils import Vector
A = json.loads(sys.argv[sys.argv.index('--') + 1]); d = np.load(A['npz']); V, F = d['V'], d['F']
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
me = bpy.data.meshes.new('b'); me.vertices.add(len(V)); me.vertices.foreach_set('co', V.ravel().astype(np.float32))
me.loops.add(F.size); me.loops.foreach_set('vertex_index', F.ravel().astype(np.int32)); me.polygons.add(len(F))
me.polygons.foreach_set('loop_start', (np.arange(len(F)) * 3).astype(np.int32)); me.update(); me.polygons.foreach_set('use_smooth', np.ones(len(F), bool))
ob = bpy.data.objects.new('b', me); sc.collection.objects.link(ob)
sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'
sc.display.shading.single_color = (0.62, 0.62, 0.62); sc.render.film_transparent = True
sc.render.resolution_x = sc.render.resolution_y = 750
cam = bpy.data.cameras.new('c'); cam.type = 'ORTHO'; cam.ortho_scale = 250.0; co = bpy.data.objects.new('c', cam); sc.collection.objects.link(co); sc.camera = co
cz = float((V[:, 2].min() + V[:, 2].max()) / 2); cx = float((V[:, 0].min() + V[:, 0].max()) / 2); cy = float((V[:, 1].min() + V[:, 1].max()) / 2)
for name, pos in (('F', (cx, cy + 400, cz)), ('P', (cx + 400, cy, cz))):
    co.location = pos; co.rotation_euler = (Vector((cx, cy, cz)) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = A['out'] + '_' + name + '.png'; bpy.ops.render.render(write_still=True)
'''
bp = os.path.join(tmp, 'r.py'); open(bp, 'w').write(BL)
tagdir = os.path.join(out, 'tiles'); os.makedirs(tagdir, exist_ok=True); gop = os.path.join(tagdir, 'GO-S-ref_nh')
subprocess.run([sys.executable, bp, '--', json.dumps(dict(npz=os.path.join(tmp, 'b.npz'), out=gop))], check=True, capture_output=True)
def tilepath(k, v): return gop + '_' + v + '.png' if k == 'GO-S-ref' else os.path.join(ctl, '%s:%s_nh_%s.png' % (CTAG, k, v))
SET = CTRL + ['GO-S-ref']
rng = np.random.default_rng(SEED); order = [str(k) for k in rng.permutation(sorted(SET))]; codes = {k: LET + '%02d' % (i + 1) for i, k in enumerate(order)}
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
except Exception: font = ImageFont.load_default()
def tile(p, sil):
    im = Image.open(p).convert('RGBA')
    if sil: a = im.split()[3].point(lambda x: 255 if x > 20 else 0); im = Image.merge('RGBA', (Image.new('L', im.size, 0),) * 3 + (a,))
    a = np.array(im.split()[3]); cols = np.where(a.max(0) > 0)[0]; rows = np.where(a.max(1) > 0)[0]
    return im.crop((max(cols[0] - 10, 0), rows[0], min(cols[-1] + 10, im.width), rows[-1] + 1))
for mode in ('grey', 'sil'):
    th = 360; tiles = []
    for k in order:
        pair = []
        for v in ('F', 'P'):
            im = tile(tilepath(k, v), mode == 'sil'); s = th / im.height; pair.append(im.resize((max(1, int(im.width * s)), th), Image.LANCZOS))
        tiles.append((codes[k], pair))
    rows = [tiles[i:i + 4] for i in range(0, len(tiles), 4)]; W = max(sum(a.width + b.width + 46 for _, (a, b) in r) for r in rows) + 20
    img = Image.new('RGB', (W, len(rows) * (th + 50) + 50), 'white'); dr = ImageDraw.Draw(img)
    dr.text((10, 8), 'Blind set %s - body only, height-normalized, front + profile, %s' % (LET, 'neutral grey' if mode == 'grey' else 'black silhouette'), font=font, fill='black')
    for ri, r in enumerate(rows):
        x = 10; y = 40 + ri * (th + 50)
        for code, (a, b) in r:
            img.paste(a, (x, y), a); img.paste(b, (x + a.width + 6, y), b); dr.text((x + 4, y + th + 6), code, font=font, fill='black'); x += a.width + b.width + 46
    img.save(os.path.join(out, 'blind_%s_%s.jpg' % (LET, mode)), quality=90)
json.dump(dict(run=run, seed=SEED, codes=codes, controls_cache_tag=CTAG, neck_cut_z=191.0, bodies=len(SET), note='KEY - never shown to scorers'),
          open(os.path.join(out, 'key_%s.json' % LET), 'w'), indent=1)
print(json.dumps(dict(sheets=[os.path.join(out, 'blind_%s_%s.jpg' % (LET, m)) for m in ('grey', 'sil')], codes=len(codes))))

# rig.py (bpy python) -- PROD.npz SKEL.json OUTDIR : diagnostic hand rig on a DERIVED copy of the production mesh.
# Builds hand crops (both hands, forearm stump), a diagnostic armature from the skel2 joint estimates, explicit
# connected-surface skin weights (claws rigid with their distal phalanx), and saves rig.blend + weights. Not a game rig.
import sys, json, numpy as np, bpy, mathutils, os, pickle
sys.path.insert(0, '/tmp/claude-0/hand/tools'); from hm import edges_q, graph, geod, load107
from scipy.spatial import cKDTree
import igl
a = sys.argv[sys.argv.index('--') + 1:]
z = np.load(a[0]); V = z['V'] * np.array([1, -1, 1]); Q = z['Q']; SK = json.load(open(a[1])); out = a[2]; os.makedirs(out, exist_ok=True)
D = json.load(open('/tmp/claude-0/hand/digits.json'))
LM = json.load(open('/home/claude/stc/rp1/landmarks_source.json'))
wrist = {s: np.array(LM['wrist_' + s]['centroid']) * np.array([1, -1, 1]) for s in 'LR'}
# --- keratin labels from the accepted sculpt materials (nearest rev107 face)
R, F, mat = load107()
digs = {'L': ['A_L17', 'A_L18', 'A_L19', 'A_L20', 'A_Lthumb'], 'R': ['A_R21', 'A_R22', 'A_R23', 'A_R24', 'A_Rthumb']}
E = edges_q(Q); G = graph(V, E)

def smooth(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

hands = {}
for side, sg in (('L', 1), ('R', -1)):
    w = wrist[side]
    # crop: the hand + 12 cm of forearm (connected component below the cut that contains the wrist ring)
    cand = (np.sign(V[:, 0]) == sg) & (V[:, 2] < w[2] + 12) & (np.abs(V[:, 0]) > 15)
    qm = cand[Q].all(1); Qc = Q[qm]
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components
    Ec = np.vstack([Qc[:, [i, (i + 1) % 4]] for i in range(4)])
    A = sp.coo_matrix((np.ones(len(Ec)), (Ec[:, 0], Ec[:, 1])), shape=(len(V), len(V)))
    _, lab = connected_components(A, directed=False)
    seed = int(np.argmin(np.linalg.norm(V - np.array(SK[digs[side][2]]['centerline'][0]), axis=1)))
    Qc = Qc[lab[Qc[:, 0]] == lab[seed]]
    vid = np.unique(Qc); mp = -np.ones(len(V), int); mp[vid] = np.arange(len(vid)); Vh = V[vid]; Qh = mp[Qc]
    # keratin per crop vertex
    sd, ti, _ = igl.point_mesh_squared_distance(Vh, R, F); ker = (mat[ti] == 1) & (np.sqrt(sd) < 0.05)
    Eh = edges_q(Qh); Gh = graph(Vh, Eh)
    # --- joints per digit
    joints = {}; regions = {}
    gfield = {}
    for k in digs[side]:
        s = SK[k]; C = np.array(s['centerline']); gs = np.array(s['geod']); ip = s['ip_idx']
        apex = np.array(D[k]['claw_tip']); si = int(np.argmin(np.linalg.norm(Vh - apex, axis=1)))
        g = geod(Gh, [si], limit=30.0); gfield[k] = g
        rootC = np.array(s['root_point'])
        ax_root = C[-1] - C[-6] if len(C) > 6 else C[-1] - C[0]; ax_root /= np.linalg.norm(ax_root)  # pointing proximal
        rad = np.sqrt(np.mean(np.array(s['spread'])[-10:] ** 2))
        # arc-length along the ring centerline (index 0 = claw/skin boundary, end = digit root)
        arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))]
        def at(L_from_tipend):
            L_from_tipend = np.clip(L_from_tipend, 0, arc[-1]); i = np.searchsorted(arc, L_from_tipend); i = min(max(i, 1), len(C) - 1)
            f = (L_from_tipend - arc[i - 1]) / max(arc[i] - arc[i - 1], 1e-9); return C[i - 1] * (1 - f) + C[i] * f
        if 'thumb' in k:
            # thumb: MCP just proximal of the thumb root ring, IP at the P1:P2 = 32:24 split of MCP -> distal skin end,
            # CMC (base of the first metacarpal) 46/56 of a P1+P2 length further proximally toward the wrist
            mcp = rootC + 0.6 * rad * ax_root; Lf = arc[-1] + 0.6 * rad
            ipj = at(arc[-1] - (32.0 / 56.0) * Lf + 0.6 * rad)
            towr = wrist[side] - mcp; towr /= np.linalg.norm(towr)
            cmc = mcp + (46.0 / 56.0) * Lf * towr
            joints[k] = dict(base=cmc, j1=mcp, j2=ipj, tip=apex)
        else:
            # fingers: MCP 0.9 ring-radius proximal of the web ring; PIP / DIP from the human P1:P2:P3 = 1:0.58:0.40 split of
            # MCP -> distal skin end (the distal phalanx ends under the claw root)
            mcp = rootC + 0.9 * rad * ax_root; Lf = arc[-1] + 0.9 * rad
            pip = at(arc[-1] + 0.9 * rad - Lf * 1.0 / 1.98); dip = at(arc[-1] + 0.9 * rad - Lf * 1.58 / 1.98)
            joints[k] = dict(base=mcp, j1=pip, j2=dip, tip=apex)
        regions[k] = (g < s['root_ring_geod'])
    # exclusive digit ownership by smallest geodesic among digits whose region claims the vertex
    own = -np.ones(len(Vh), int)
    gstack = np.stack([np.where(regions[k], gfield[k], np.inf) for k in digs[side]], 1)
    has = np.isfinite(gstack).any(1); own[has] = np.argmin(gstack[has], 1)
    hands[side] = dict(vid=vid, Vh=Vh, Qh=Qh, ker=ker, joints=joints, own=own, gfield=gfield, Gh=Gh)
    print(side, 'crop verts', len(Vh), 'quads', len(Qh), 'keratin verts', int(ker.sum()), 'owned by digits', [int((own == i).sum()) for i in range(5)])

# --- weights
def seg_param(P, a_, b_):
    d = b_ - a_; t = ((P - a_) @ d) / (d @ d); return t

for side in 'LR':
    h = hands[side]; Vh = h['Vh']; own = h['own']; n = len(Vh)
    bones = ['hand']; W = {'hand': np.zeros(n)}
    palm = own < 0
    for i, k in enumerate(digs[side]):
        j = h['joints'][k]; names = [k + '_0', k + '_1', k + '_2']
        for nm in names: W[nm] = np.zeros(n); bones.append(nm)
        m = own == i; P = Vh[m]
        # piecewise param along base->j1->j2->tip by nearest segment
        segs = [(j['base'], j['j1']), (j['j1'], j['j2']), (j['j2'], j['tip'])]
        dist = []; ts = []
        for (a_, b_) in segs:
            t = np.clip(seg_param(P, a_, b_), 0, 1); q = a_ + t[:, None] * (b_ - a_); dist.append(np.linalg.norm(P - q, axis=1)); ts.append(t)
        dist = np.stack(dist, 1); seg = np.argmin(dist, 1)
        # blended weights across j1 and j2 by signed distance to the joint plane (normal = mean of adjacent bone dirs)
        def jplane(p, d1, d2):
            nrm = d1 / np.linalg.norm(d1) + d2 / np.linalg.norm(d2); return nrm / np.linalg.norm(nrm)
        n1 = jplane(j['j1'], j['j1'] - j['base'], j['j2'] - j['j1']); n2 = jplane(j['j2'], j['j2'] - j['j1'], j['tip'] - j['j2'])
        hw1 = 0.55 if 'thumb' not in k else 0.6; hw2 = 0.45
        s1 = (P - j['j1']) @ n1; s2 = (P - j['j2']) @ n2
        b1 = smooth((s1 + hw1) / (2 * hw1)); b2 = smooth((s2 + hw2) / (2 * hw2))
        w0 = 1 - b1; w1 = b1 * (1 - b2); w2 = b1 * b2
        # base joint: blend with the hand near the digit root (finger side)
        n0 = (j['j1'] - j['base']); n0 /= np.linalg.norm(n0); s0 = (P - j['base']) @ n0
        hb = 0.9 if 'thumb' not in k else 1.3
        bb = smooth((s0 + hb) / (2 * hb))
        W['hand'][m] += (1 - bb); W[names[0]][m] += w0 * bb; W[names[1]][m] += w1 * bb; W[names[2]][m] += w2 * bb
    # palm vertices near digit roots: small share of the proximal phalanx, decaying geodesically
    Gh = h['Gh']; W['hand'][palm] = 1.0
    for i, k in enumerate(digs[side]):
        fv = np.where(own == i)[0]
        dpal = geod(Gh, fv, limit=2.0)
        j = h['joints'][k]; n0 = (j['j1'] - j['base']); n0 /= np.linalg.norm(n0)
        sel = palm & np.isfinite(dpal)
        share = 0.5 * (1 - smooth(dpal[sel] / (1.2 if 'thumb' not in k else 1.8)))
        # only where the palm vertex is distal of the base joint plane - 1 cm
        sel_idx = np.where(sel)[0]; side_ok = ((Vh[sel_idx] - j['base']) @ n0) > -1.0
        share = share * side_ok
        W[k + '_0'][sel_idx] += share; W['hand'][sel_idx] -= share
    # harmonic transition: palm vertices within 4 cm (geodesic) of a digit, and digit vertices within 1.5 cm of their base
    # joint plane, are re-solved as a Laplace interpolation of all weight channels (removes the owner-boundary seam)
    allf = np.where(own >= 0)[0]; dpal = geod(Gh, allf, limit=4.0)
    free = palm & np.isfinite(dpal)
    for i, k in enumerate(digs[side]):
        j = h['joints'][k]; n0 = (j['j1'] - j['base']); n0 /= np.linalg.norm(n0); m = own == i
        free[np.where(m)[0][((Vh[m] - j['base']) @ n0) < 1.5]] = True
    import scipy.sparse.linalg as sla
    Ehh = edges_q(h['Qh']); Aj = sp.coo_matrix((np.ones(2 * len(Ehh)), (np.r_[Ehh[:, 0], Ehh[:, 1]], np.r_[Ehh[:, 1], Ehh[:, 0]])), shape=(n, n)).tocsr()
    deg = np.asarray(Aj.sum(1)).ravel(); Lp = sp.diags(deg) - Aj
    fi = np.where(free)[0]; ci = np.where(~free)[0]
    lu = sla.splu(Lp[fi][:, fi].tocsc()); Lfc = Lp[fi][:, ci]
    for nm in list(W):
        W[nm][fi] = np.clip(lu.solve(-(Lfc @ W[nm][ci])), 0, 1)
    tot = sum(W.values())
    for nm in W: W[nm] = W[nm] / tot
    print(side, 'harmonic transition vertices', len(fi))
    # claws: rigid with the distal phalanx
    for i, k in enumerate(digs[side]):
        m = (own == i) & h['ker']
        for nm in [k + '_0', k + '_1', 'hand']: W[nm][m] = 0
        W[k + '_2'][m] = 1.0
    tot = sum(W.values()); assert (tot > 0.999).all() and (tot < 1.001).all(), (tot.min(), tot.max())
    h['W'] = W; h['bones'] = bones

pickle.dump({s: dict(vid=hands[s]['vid'], joints={k: {kk: vv.tolist() for kk, vv in j.items()} for k, j in hands[s]['joints'].items()},
                     W={k: v.astype(np.float32) for k, v in hands[s]['W'].items()}, ker=hands[s]['ker'], own=hands[s]['own']) for s in 'LR'},
            open(os.path.join(out, 'rig_data.pkl'), 'wb'))

# --- Blender scene: two crop meshes + armatures
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
for side in 'LR':
    h = hands[side]; Vh = h['Vh'] / 100.0; Qh = h['Qh'][:, ::-1]  # metres, outward winding
    me = bpy.data.meshes.new('GO_hand_%s_DIAG' % side); me.vertices.add(len(Vh)); me.vertices.foreach_set('co', Vh.ravel().astype(np.float32))
    me.loops.add(Qh.size); me.loops.foreach_set('vertex_index', Qh.ravel().astype(np.int32)); me.polygons.add(len(Qh))
    me.polygons.foreach_set('loop_start', np.arange(0, Qh.size, 4)); me.polygons.foreach_set('loop_total', np.full(len(Qh), 4)); me.update()
    me.polygons.foreach_set('use_smooth', np.ones(len(Qh), bool))
    ob = bpy.data.objects.new('GO_hand_%s_DIAG' % side, me); sc.collection.objects.link(ob)
    arm = bpy.data.armatures.new('GO_hand_%s_RIG' % side); ao = bpy.data.objects.new('GO_hand_%s_RIG' % side, arm); sc.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode='EDIT')
    w = wrist[side] / 100.0; J = h['joints']
    mid = np.mean([J[k]['base'] for k in digs[side][:4]], 0) / 100.0
    hb = arm.edit_bones.new('hand'); hb.head = w; hb.tail = mid
    # dorsal direction per hand: from palm centre outward (crop vertex normal average on the knuckle side) ~ lateral x
    lat = np.array(J[digs[side][0]]['base']) - np.array(J[digs[side][3]]['base']); lat /= np.linalg.norm(lat)
    ventral_hand = np.array([-1.0, 0, 0]) if side == 'L' else np.array([1.0, 0, 0])   # palms face the thighs
    for i_, k in enumerate(digs[side]):
        j = {kk: np.array(vv) / 100.0 for kk, vv in J[k].items()}
        # digit dorsal direction: from the distal joint toward the centroid of the digit's keratin (claw root sits dorsally)
        kv = h['Vh'][(h['own'] == i_) & h['ker']] / 100.0
        dors = kv.mean(0) - j['j2'] if len(kv) else -ventral_hand
        prev = hb
        for bi, (a_, b_) in enumerate([(j['base'], j['j1']), (j['j1'], j['j2']), (j['j2'], j['tip'])]):
            eb = arm.edit_bones.new('%s_%d' % (k, bi)); eb.head = a_; eb.tail = b_; eb.parent = prev; eb.use_connect = (bi > 0)
            yv = (b_ - a_) / np.linalg.norm(b_ - a_)
            if 'thumb' in k:
                # thumb: local X = flexion across the palm (axis ~ palm normal); thumb_0 local Z = palmar abduction
                ref = ventral_hand * (-1.0 if side == 'L' else 1.0)   # mirrored so +X folds the thumb toward the fingers on both hands
            else:
                # fingers: flexion axis = the across-the-hand direction (index -> little MCP) made perpendicular to the bone
                ref = lat
            xv = ref - (ref @ yv) * yv; xv /= np.linalg.norm(xv)
            zv = np.cross(xv, yv); eb.align_roll(mathutils.Vector(zv)); prev = eb
            eb['dorsal'] = list(map(float, dors))
    bpy.ops.object.mode_set(mode='OBJECT')
    for nm, wv in h['W'].items():
        vg = ob.vertex_groups.new(name=nm); idx = np.where(wv > 1e-4)[0]
        for i in idx: vg.add([int(i)], float(wv[i]), 'REPLACE')
    mod = ob.modifiers.new('Armature', 'ARMATURE'); mod.object = ao; mod.use_deform_preserve_volume = True
    ob.parent = ao
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, 'hand_rig_DIAG.blend'))
print('saved rig')

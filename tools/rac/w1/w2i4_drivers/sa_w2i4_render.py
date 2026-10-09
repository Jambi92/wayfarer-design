# RAC W2I4 §11 sheets (shaded Workbench reference with cavity, the accepted rclose.py renderer; the tool chain has no material / texture
# path, so "shaded" is the material-free reference). Final assets are the SURFACED meshes: igl.upsample(finished base) + regenerated scale
# relief (SA-M188 = the generated field; other states / statures carry the same per-vertex relief along their own normals).
# Sheets: final SA-M188 / SA-F188 (front, side, front 3/4, rear 3/4, rear + close thigh / hip, knee, neck / shoulder, axilla / forearm,
# caudal base, strict front orthographic provenance), 168 / 188 / 203 / 208 family, W2I3 vs W2I4 at 188, thigh relief before / after,
# scale field before / after. Usage: python3 sa_w2i4_render.py all
import sys, os, subprocess, numpy as np, igl
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_finish as FN
RB = FN.RB; B = FN.B; S = FN.C.S; RC = S + '/w2i/rodin/g1/rclose.py'; W = S + '/w2i4/rend'; SH = S + '/w2i4/sheets'
os.makedirs(W, exist_ok=True); os.makedirs(SH, exist_ok=True)
Fu = np.load(S + '/w2i4/surf/fin_up.npz')['F'].astype(np.int64)
_sf = None
def relief():
    """scalar scale relief per upsampled vertex (normal component of the W2I4 surface delta on the finished SA-M188 base)"""
    global _sf
    if _sf is None:
        Vu = np.load(S + '/w2i4/surf/fin_up.npz')['V'].astype(float); d = np.load(S + '/w2i4/surf/saurin_w2i4_surface_delta.npz')['d'].astype(float)
        _sf = (d * igl.per_vertex_normals(Vu, Fu)).sum(1)
    return _sf
_fr = None
def relief_frozen():
    global _fr
    if _fr is None:
        up = np.load(S + '/w2i/rodin/c12/g15up.npz'); V = up['V'].astype(float)
        _fr = (np.load('/mnt/attach/outputs/racebodies_v35/saurin_final_surface_delta.npz')['d'].astype(float) * igl.per_vertex_normals(V, Fu)).sum(1)
    return _fr
def surfaced(P, field):
    Vu, _ = igl.upsample(P.astype(float), FN.F0.astype(np.int64)); return Vu + field[:, None] * igl.per_vertex_normals(Vu, Fu)
def mesh(bid, fn_):
    f = W + '/%s.npz' % bid
    if not os.path.exists(f):
        P = fn_(); FF = Fu if len(P) > len(FN.V0) else FN.F0
        np.savez(f, P=P.astype(np.float32), f=FF.astype(np.int32))
    return bid
def views(bid, spec, res=560):
    tag = W + '/' + bid; names = [s.split(':')[0] for s in spec.split(';')]
    todo = ';'.join(s for s, n in zip(spec.split(';'), names) if not os.path.exists('%s_%s.png' % (tag, n)))
    if todo: subprocess.run(['python3', RC], env=dict(os.environ, VIEWS=todo, NPZ=W + '/%s.npz' % bid, TAG=tag, RES=str(res)), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return [Image.open('%s_%s.png' % (tag, n)).convert('RGBA') for n in names]
FULL = "front:0:0:0:-40:110:300;sideL:270:0:0:-40:110:300;side:90:0:0:-40:110:300;front34:35:0:0:-40:110:300;rear34:150:0:0:-40:110:300;rear:180:0:0:-40:110:300"
def close(h):
    k = h / 188.0; c = lambda u: u * k
    return ("cthigh:0:0:%.1f:0:%.1f:%.1f;cknee:0:0:%.1f:0:%.1f:%.1f;cneck:30:5:0:0:%.1f:%.1f;carm:0:0:%.1f:0:%.1f:%.1f;ccaud:150:-10:0:%.1f:%.1f:%.1f;orthofront:0:0:0:0:%.1f:%.1f"
            % (11 * k, c(84), 42 * k, 15 * k, c(62), 40 * k, c(150), 55 * k, 27 * k, c(118), 55 * k, -15 * k, c(95), 60 * k, c(85), 70 * k))
CL = ['close thigh / hip', 'close knee', 'close neck / shoulder', 'close axilla / forearm', 'close caudal base (rear 3/4 below)', 'strict front ortho (provenance only)']
def row(ims, labels, title, w=560):
    r = Image.new('RGB', (w * len(ims), w + 46), 'white'); d = ImageDraw.Draw(r); d.text((8, 6), title, fill='black')
    for i, (im, lb) in enumerate(zip(ims, labels)):
        im = im.resize((w, w)); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); r.paste(bg, (i * w, 46)); d.text((i * w + 8, 26), lb, fill=(90, 90, 90))
    return r
def sheet(name, rows, title, scale=0.6):
    Wd = max(r.size[0] for r in rows); out = Image.new('RGB', (Wd, sum(r.size[1] for r in rows) + 40), 'white'); ImageDraw.Draw(out).text((8, 12), title, fill='black'); y = 40
    for r in rows: out.paste(r, (0, y)); y += r.size[1]
    out = out.resize((int(out.size[0] * scale), int(out.size[1] * scale))); out.save(SH + '/' + name, quality=88); print('saved', name, out.size, flush=True)
def fin(p, h=None, field=None):
    P = FN.build_f(p, h)[0]; return surfaced(P, relief() if field is None else field)
if __name__ == '__main__':
    FV = ['front', 'side (left)', 'side (right)', 'front 3/4', 'rear 3/4', 'rear']
    for sx, p in (("M", {}), ("F", B.CEN)):
        b = mesh('W2I4-SA-%s188-FINAL' % sx, lambda p=p: fin(p))
        sheet('w2i4_SA-%s188_final.jpg' % sx, [row(views(b, FULL), FV, 'W2I4 final SA-%s188 candidate (L1 + F2, finished, regenerated scale field; neutral carriage)' % sx),
                                              row(views(b, close(188.0)), CL, 'close views')], 'W2I4 final Saurin reference candidate SA-%s188 — shaded reference (Workbench + cavity); COPIES, canonical SA-M / SA-F unchanged' % sx, 0.55)
    fam = []
    for h in (168, 188, 203, 208):
        b = mesh('W2I4-SA-M%d-FINAL' % h, lambda h=h: fin({}, float(h) if h != 188 else None)); fam.append(row(views(b, FULL), FV, 'SA-M%d final (regional route)' % h, 400))
    sheet('w2i4_family.jpg', fam, 'W2I4 final candidate family 168 / 188 / 203 / 208 (same regional construction route; surfaced)', 0.7)
    for sx, p in (("M", {}), ("F", B.CEN)):
        a = mesh('W2I4-SA-%s188-W2I3' % sx, lambda p=p: surfaced(RB.build_r(p, RB.TARGET)[0], relief_frozen()))
        b = 'W2I4-SA-%s188-FINAL' % sx
        sheet('w2i4_before_after_%s188.jpg' % sx, [row(views(a, FULL), FV, 'BEFORE: W2I3 rebuild SA-%s188 with the accepted (frozen) scale field carried by vertex index' % sx),
                                                   row(views(b, FULL), FV, 'AFTER: W2I4 finished SA-%s188 with the regenerated scale field' % sx)], 'W2I3 rebuild vs W2I4 finished asset, SA-%s188' % sx, 0.55)
    TH = "tfront:0:0:14:0:80:46;tside:90:0:14:0:80:46;trear:180:0:14:0:80:46;tmed:-60:0:6:0:78:40"
    rows = []
    for bid, lab, fn_ in (('W2I4-TH-FROZEN', 'frozen SA-M188 base (accepted thigh, shorter)', lambda: FN.V0.astype(float)), ('W2I4-TH-W2I3', 'W2I3 rebuild base (thigh relief stretched x1.5)', lambda: RB.build_r({}, RB.TARGET)[0]),
                          ('W2I4-TH-W2I4', 'W2I4 finished base (native-scale relief re-model + fairing)', lambda: FN.build_f({})[0])):
        rows.append(row(views(mesh(bid, fn_), TH), ['front', 'lateral', 'rear', 'medial (adductor)'], lab))
    sheet('w2i4_thigh_relief.jpg', rows, 'Thigh relief before / after (base meshes, SA-M188; un-surfaced so the muscle / tendon relief is read directly)', 0.6)
    SF = "sthigh:90:0:14:0:78:24;sknee:20:0:16:0:58:20;sneck:30:5:0:0:158:24;sfore:60:-5:34:0:100:22;sshould:40:5:18:0:146:24;shead:35:5:0:6:178:34"
    rows = []
    for bid, lab, fn_ in (('W2I4-SF-FROZEN', 'accepted field on the frozen body (control)', lambda: surfaced(FN.V0.astype(float), relief_frozen())),
                          ('W2I4-SF-BEFORE', 'BEFORE: accepted field carried onto the L1 + F2 body (stretched / compressed)', lambda: surfaced(FN.build_f({})[0], relief_frozen())),
                          ('W2I4-SF-AFTER', 'AFTER: W2I4 regenerated field on the L1 + F2 body', lambda: fin({}))):
        rows.append(row(views(mesh(bid, fn_), SF), ['lateral thigh', 'knee', 'neck', 'forearm', 'shoulder', 'head (unchanged geometry; new realization)'], lab))
    sheet('w2i4_scale_field.jpg', rows, 'Scale field before / after (SA-M188, close; same scale per column)', 0.6)

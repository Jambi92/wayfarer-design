"""RAC W1f: draw the SKELETAL PROXY over the reference body (front | left side | back orthographic; 10 cm ticks), for AD-G14
before/after evidence and the GR-G2 qualitative scapular review.

Proxy elements (all from skeletal_proxy.py geometry: rig joints + skeletal-envelope surface inset by t = 0.5 cm x H/173):
spine column (rig joints pelvis -> head), ribcage hoops (skeletal-envelope trunk sections between the costal-margin proxy and
the girdle, inset), lumbar section (S4), pelvic rings (crest S5 and hip level S6), hip-joint centres, trochanters, femoral
neck/shaft lines, clavicles, glenohumeral centres (sphere fit), acromions, and the SCAPULA PROXY plate.

Scapula proxy (BUILDER-CHOSEN construction, R-14; GR-G2 is a qualitative render review per RMQ RM-LR-02 (h)):
  superior angle at the suprasternal-proxy level + SUP x thoracic vertical (TV); inferior angle at suprasternal - INF x TV;
  medial border at MED x (half thoracic breadth) from the midline; lateral point = acromion; the plate is laid on the posterior
  skeletal-envelope surface (inset), i.e. close-seated (no winging).
  MF / every non-Grask body: SUP 0.05, INF 0.50, MED 0.35.  Grask (accepted GR-G2 departure, AD-G2): INF 0.62 (vertically
  extended along the ribcage), MED 0.28 (spine-coupled), same seating.
Usage: python3 skeleton_sheet.py out.jpg "title" envelope_npz lean_npz [GR] [envelope_npz lean_npz [GR] ...]"""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence as EV
import skeletal_proxy as SP
from arm_measure import load, measure
import tempfile

SCAP = {"default": (0.05, 0.50, 0.35), "GR": (0.05, 0.62, 0.28)}

def back_surface_point(V, trunk, x, u, tol):
    """posterior surface point nearest to (x, u): candidates in a 2.5 x tol window behind the slab's mid-depth"""
    m = trunk & (np.abs(V[:, 0] - x) < 2.5 * tol) & (np.abs(V[:, 2] - u) < 2.5 * tol)
    if not m.any(): return None
    P = V[m]; P = P[P[:, 1] < np.median(P[:, 1])] if len(P) > 2 else P[P[:, 1] <= P[:, 1].min()]
    return P[np.argmin(np.hypot(P[:, 0] - x, P[:, 2] - u))]

def proxy(env_path, lean_path, kind):
    tmp = tempfile.mkdtemp(); al = os.path.join(tmp, "al.npz")
    SP.align(lean_path, env_path, al); d = load(al); m = measure(al)
    V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; w = lambda k: d["w_" + k]
    H = measure(env_path)["stature"]; t = 0.5 * H / 173.14
    armw = np.maximum.reduce([w(x) for x in ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")])
    trunk = keep & (armw < 0.2)
    g = SP.girdle_femur(d, H)
    el = {"lines": [], "pts": [], "hoops": [], "plates": []}
    sp = [J[k][0] for k in ("pelvis", "spine_01", "spine_02", "spine_03", "neck_01", "head")]
    el["lines"].append(("spine", sp))
    sst = (J["clavicle_l"][0] + J["clavicle_r"][0]) / 2; s03 = J["spine_03"][0][2]; s01 = J["spine_01"][0][2]
    hip = (J["thigh_l"][0] + J["thigh_r"][0]) / 2
    def hoop(z, half=0.8):
        mm = trunk & (np.abs(V[:, 2] - z) < half); P = V[mm]
        if len(P) < 8: return None
        c = P.mean(0); ang = np.arctan2(P[:, 1] - c[1], P[:, 0] - c[0]); out = []
        for a in np.linspace(-np.pi, np.pi, 37):
            k = np.abs(((ang - a + np.pi) % (2 * np.pi)) - np.pi) < 0.12
            if k.any():
                Q = P[k]; r = np.hypot(Q[:, 0] - c[0], Q[:, 1] - c[1]).max() - t
                out.append([c[0] + r * np.cos(a), c[1] + r * np.sin(a), z])
        return out
    for z in np.linspace(s03, sst[2] - 2, 6): el["hoops"].append(("rib", hoop(z)))
    zs = np.linspace(s01, s03, 9); k = int(np.argmin([np.ptp(V[trunk & (np.abs(V[:, 2] - z) < 0.8), 0]) for z in zs]))
    el["hoops"].append(("lumbar", hoop(zs[k]))); el["hoops"].append(("crest", hoop(s01))); el["hoops"].append(("hip", hoop(hip[2])))
    TB = m["thorax_breadth_max"] - 2 * t; TV = m["thoracic_vertical"]
    SUP, INF, MED = SCAP.get(kind, SCAP["default"])
    for s, sg in (("l", 1), ("r", -1)):
        hp, kn = J["thigh_" + s][0], J["calf_" + s][0]; tr = np.array(g["trochanter_" + s]); gh = np.array(g["gh_" + s]); ac = np.array(g["acromion_" + s])
        el["pts"] += [("hip", hp), ("troch", tr), ("gh", gh), ("acromion", ac)]
        el["lines"] += [("neck", [hp, tr]), ("femur", [tr, kn]), ("clavicle", [J["clavicle_" + s][0], J["clavicle_" + s][1]])]
        tol = 1.2 * H / 173.14; xm = sg * MED * TB / 2
        backm = keep & (armw < 0.6)                                   # back surface incl. posterior girdle region
        sa = back_surface_point(V, backm, xm, sst[2] + SUP * TV, tol); ia = back_surface_point(V, backm, xm * 1.05, sst[2] - INF * TV, tol)
        if sa is not None and ia is not None:
            ins = np.array([0, t, 0]); el["plates"].append([sa + ins, ia + ins, ac + np.array([0, 0, -t])])
    el["meta"] = {"t": t, "SUP_INF_MED": (SUP, INF, MED), "TV": TV, "TB": TB}
    return el

def draw(env_path, el, label):
    D = np.load(env_path, allow_pickle=True); V = D["V"].astype(float); F = D["F"]; x, f, u = V.T
    pp = 2.6; Hh = int(245 * pp); views = []
    specs = [("front", lambda P: (P[..., 0], P[..., 2]), (x, u, f), (-55, -2), 110),
             ("left side", lambda P: (P[..., 1], P[..., 2]), (f, u, x), (-40, -2), 80),
             ("back", lambda P: (-P[..., 0], P[..., 2]), (-x, u, -f), (-55, -2), 110)]
    for name, proj, (hx, hy, dep), org, wcm in specs:
        im = EV.render(V, F, hx, hy, dep, pp, org, (int(wcm * pp), Hh), 10, shade_col=(232, 232, 228), amb=0.6)
        dr = ImageDraw.Draw(im)
        def P2(p):
            a, b = proj(np.asarray(p, float)); return ((a - org[0]) * pp, Hh - (b - org[1]) * pp)
        for kind, pts in el["hoops"]:
            if pts: dr.line([P2(p) for p in pts], fill=(40, 90, 200) if kind == "rib" else (200, 60, 40), width=2)
        for kind, pts in el["lines"]:
            dr.line([P2(p) for p in pts], fill=(30, 30, 30) if kind != "clavicle" else (120, 30, 160), width=3)
        for tri in el["plates"]:
            dr.polygon([P2(p) for p in tri], outline=(0, 140, 60), fill=None); dr.line([P2(tri[0]), P2(tri[1])], fill=(0, 140, 60), width=3)
        for kind, p in el["pts"]:
            a, b = P2(p); r = 4; dr.ellipse([a - r, b - r, a + r, b + r], fill={"hip": (200, 0, 0), "troch": (230, 120, 0), "gh": (120, 30, 160), "acromion": (0, 140, 60)}[kind])
        views.append((name, im))
    W = sum(v[1].width for v in views) + 20; S = Image.new("RGB", (W, Hh + 30), "white"); d = ImageDraw.Draw(S); d.text((4, 4), label, fill=(0, 0, 0)); xo = 0
    for name, im in views: S.paste(im, (xo, 30)); d.text((xo + 4, 18), name, fill=(0, 0, 0)); xo += im.width + 10
    return S

def main(out, title, items):
    tiles = []; i = 0
    while i < len(items):
        env, lean = items[i], items[i + 1]; i += 2; kind = "default"
        if i < len(items) and items[i] == "GR": kind = "GR"; i += 1
        el = proxy(env, lean, kind); tiles.append(draw(env, el, "%s  [scapula proxy %s: SUP %.2f INF %.2f MED %.2f]" % (os.path.basename(env), kind, *el["meta"]["SUP_INF_MED"])))
    W = max(t.width for t in tiles); S = Image.new("RGB", (W, sum(t.height for t in tiles) + 30), "white"); d = ImageDraw.Draw(S); d.text((4, 6), title, fill=(0, 0, 0)); y = 30
    for t in tiles: S.paste(t, (0, y)); y += t.height
    S.save(out, quality=85)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])

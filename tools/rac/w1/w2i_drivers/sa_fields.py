# RAC W2I §18 (RM-UB-08 body portion): as-built per-field scale spacing / relief on the frozen SA-M surface (field labels regenerated with the
# accepted gate-1 g7regs.py on the upsampled frozen base, HEAD_SCALE 1.08 as in final-brow build15.sh; claw diagnostic reproduces the Part 7 values
# exactly). Area-weighted distributions per family; the regional stature route scales absolute spacing by the local linear factor (reported).
# Usage: python3 sa_fields.py OUT.json
import sys, json, numpy as np, igl
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2i/rodin'
z = np.load(W + '/c12/g15up.npz'); V = z['V'].astype(float); F = z['F'].astype(np.int64); g = np.load(W + '/c12/g15reg.npz')
A = igl.massmatrix(V, F, igl.MASSMATRIX_TYPE_VORONOI).diagonal()
NAMES = {1: "structural", 2: "transitional / articulation", 3: "fine expressive", 4: "ventral", 5: "contact (palm / sole)", 6: "claw keratin", 7: "eye"}
u = V[:, 2]; body = u < 166          # body portion only (head fields are RM-UF-04, out of scope)
def wq(x, w, qs):
    o = np.argsort(x); c = np.cumsum(w[o]); c /= c[-1]; return [float(np.interp(q, c, x[o])) for q in qs]
out = {"source": "g15reg (regenerated) on g15up", "families": {}}
for k, nm in NAMES.items():
    m = (g['FAM'] == k) & body
    if m.sum() < 50: continue
    out["families"][nm] = dict(area_cm2=float(A[m].sum()), spacing_cm_p5_50_95=wq(g['R'][m], A[m], (0.05, 0.5, 0.95)), relief_cm_p5_50_95=wq(g['H'][m], A[m], (0.05, 0.5, 0.95)),
                               elongation_p5_50_95=wq(g['EL'][m], A[m], (0.05, 0.5, 0.95)))
BETA = json.load(open('/home/claude/wayfarer-design/tools/rac/w1/native_short_allometry.json'))["betas"]
out["stature_route_linear_factor"] = {str(h): {"trunk / limb girth": (h / 187.881) ** BETA["girth"], "vertical": h / 187.881, "hands": (h / 187.881) ** BETA["hand"], "feet": (h / 187.881) ** BETA["foot"], "tail": h / 187.881} for h in (168, 203, 208)}
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for nm, d in out["families"].items(): print('%-28s area %8.0f  spacing %s  relief %s' % (nm, d['area_cm2'], [round(x, 2) for x in d['spacing_cm_p5_50_95']], [round(x, 3) for x in d['relief_cm_p5_50_95']]))

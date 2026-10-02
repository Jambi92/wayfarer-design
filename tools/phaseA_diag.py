# Phase A diagnostics: midsagittal continuity section with axis path, transverse sections, measurements.
import numpy as np, json, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from skimage import measure as skm
import wf_saurin_phaseA as A
H = 188.0
OUT = "/tmp/claude-0/rb/sheets_pa"; import os; os.makedirs(OUT, exist_ok=True)

def grid2(axes, rng, step=0.25):
    a = np.arange(rng[0], rng[1], step); b = np.arange(rng[2], rng[3], step)
    A_, B_ = np.meshgrid(a, b, indexing="ij"); return a, b, A_, B_

def plane(kind, val, rng, step=0.25):
    a, b, P1, P2 = grid2(None, rng, step)
    if kind == "U": X, F, U = P1, P2, np.full_like(P1, val)
    if kind == "X": X, F, U = np.full_like(P1, val), P1, P2
    if kind == "F": X, F, U = P1, np.full_like(P1, val), P2
    d = A.sdf(X.ravel(), F.ravel(), U.ravel()).reshape(P1.shape)
    return a, b, d

def extents(a, b, d):
    m = d < 0
    if not m.any(): return None
    ii, jj = np.nonzero(m)
    return dict(a0=a[ii.min()], a1=a[ii.max()], b0=b[jj.min()], b1=b[jj.max()], ca=a[ii].mean(), cb=b[jj].mean(), area=m.sum() * (a[1] - a[0]) * (b[1] - b[0]))

res = {}
# --- midsagittal section with axis path and region marks
a, b, d = plane("X", 0.0, (-66, 28, 24, 192), 0.25)
fig, ax = plt.subplots(1, 2, figsize=(17, 10), gridspec_kw=dict(width_ratios=[1.25, 1]))
ax[0].contourf(a, b, (d < 0).T, levels=[0.5, 1.5], colors=["#b9bcc4"])
ax[0].contour(a, b, d.T, levels=[0], colors="#33363d", linewidths=1.2)
ax[0].plot(A.PATH[:, 1], A.PATH[:, 2], color="#d0542a", lw=2.2, label="axial centreline (one continuous sweep)")
cols = {"cervical": "#c9a227", "thoracic shell": "#3f9a5a", "lower axial trunk": "#3a7fc0", "pelvis / sacral platform": "#7a5ac2", "caudal base + proximal tail": "#c2457a"}
spans = [("cervical", 183, 155), ("thoracic shell", 155, 121), ("lower axial trunk", 121, 101), ("pelvis / sacral platform", 101, 93.5), ("caudal base + proximal tail", 93.5, 0)]
for nm, u0, u1 in spans:
    m = (A.PATH[:, 2] <= u0) & (A.PATH[:, 2] > u1)
    if nm.startswith("caudal"): m = A.PATH[:, 1] < -12.5
    if nm.startswith("pelvis"): m = (A.PATH[:, 2] <= u0) & (A.PATH[:, 1] >= -12.5)
    ax[0].plot(A.PATH[m, 1], A.PATH[m, 2], color=cols[nm], lw=7, alpha=0.55, solid_capstyle="butt", label=nm)
ax[0].scatter([A.HIP[1]], [A.HIP[2]], s=80, c="k", zorder=5, label="hip joint (femoral socket)")
for u, lab in ((140, "T: thorax"), (112, "L: lower trunk"), (98, "P: pelvis")):
    ax[0].axhline(u, color="#888", ls=":", lw=1); ax[0].text(-64, u + 0.8, lab, fontsize=9, color="#555")
ax[0].axvline(-24, color="#888", ls=":", lw=1); ax[0].text(-23.5, 72, "C: caudal base section", fontsize=9, color="#555", rotation=90)
ax[0].set_aspect("equal"); ax[0].set_xlabel("F (cm, + forward)"); ax[0].set_ylabel("U (cm)"); ax[0].legend(loc="lower left", fontsize=8)
ax[0].set_title("Midsagittal section (X = 0): thorax → lower trunk → pelvis → caudal base → tail is one body")
# sagittal centroid offsets
for u, key in ((140, "thorax"), (112, "lower_trunk"), (98, "pelvis")):
    aa, bb, dd = plane("U", u, (-26, 26, -40, 30), 0.25); e = extents(aa, bb, dd)
    res[key] = dict(u=u, width=e["a1"] - e["a0"], depth=e["b1"] - e["b0"], centroid_F=e["cb"], back_F=e["b0"], front_F=e["b1"], area=e["area"])
# thorax max depth over 125-150
dmax = 0
for u in np.arange(124, 152, 2):
    aa, bb, dd = plane("U", u, (-26, 26, -40, 30), 0.3); e = extents(aa, bb, dd); dmax = max(dmax, e["b1"] - e["b0"])
res["thorax_max_depth"] = dmax
aa, bb, dd = plane("F", -24.0, (-26, 26, 60, 120), 0.25); e = extents(aa, bb, dd)
res["caudal_base"] = dict(F=-24.0, width=e["a1"] - e["a0"], height=e["b1"] - e["b0"], centroid_U=e["cb"], area=e["area"])
# pelvis cross-section area for ratio (U = 98 axial only, excluding femora -> evaluate axial part)
aa, bb, P1, P2 = grid2(None, (-26, 26, -40, 30), 0.25)
dax = A.axial((P1.ravel(), P2.ravel(), np.full(P1.size, 98.0))).reshape(P1.shape)
res["pelvis_axial_area_U98"] = float((dax < 0).sum() * 0.25 * 0.25)
res["tail_base_to_pelvis_area"] = res["caudal_base"]["area"] / res["pelvis_axial_area_U98"]
# arc lengths
s_base = A.ARC[np.argmin(np.abs(A.PATH[:, 1] - (-12.5)))]
res["proximal_tail_arc_cm"] = float(A.ARC[-1] - s_base)
res["hip_spacing_cm"] = 2 * A.HIP[0]
res["hip_F"] = A.HIP[1]
res["head_centroid_F"] = 3.0 + 2.0
ax[0].text(-64, 186, "Sagittal centroids (cm): thorax %+.1f · lower trunk %+.1f · pelvis %+.1f · hip %+.1f · caudal base %+.1f" % (
    res["thorax"]["centroid_F"], res["lower_trunk"]["centroid_F"], res["pelvis"]["centroid_F"], A.HIP[1], -24.0), fontsize=8.5)
# transverse sections panel
ax2 = ax[1]; ax2.axis("off")
sub = [("T  thorax U=140", "U", 140, (-26, 26, -30, 30)), ("L  lower trunk U=112", "U", 112, (-26, 26, -30, 30)),
       ("P  pelvis + femoral roots U=98", "U", 98, (-26, 26, -30, 30)), ("C  caudal base F=-24 (X-U plane)", "F", -24, (-26, 26, 66, 120))]
for k, (lab, kind, val, rng) in enumerate(sub):
    axs = fig.add_axes([0.60 + (k % 2) * 0.2, 0.52 - (k // 2) * 0.42, 0.18, 0.36])
    aa, bb, dd = plane(kind, val, rng, 0.2)
    axs.contourf(aa, bb, (dd < 0).T, levels=[0.5, 1.5], colors=["#b9bcc4"]); axs.contour(aa, bb, dd.T, levels=[0], colors="#33363d", linewidths=1.2)
    axs.set_aspect("equal"); axs.set_title(lab, fontsize=9); axs.tick_params(labelsize=7)
    axs.set_xlabel("X (cm)", fontsize=7); axs.set_ylabel("F (cm, + fwd)" if kind == "U" else "U (cm)", fontsize=7)
fig.suptitle("Saurin post-Rodin Phase A — axial continuity and sections (DIAGNOSTIC / NOT FINAL)", fontsize=13)
fig.savefig(OUT + "/pa_02_sections_continuity.jpg", dpi=115); plt.close(fig)
for k in ("thorax", "lower_trunk", "pelvis"):
    for q in ("width", "depth"): res[k][q + "_H"] = res[k][q] / H
res["thorax_max_depth_H"] = dmax / H
res["caudal_base"]["width_H"] = res["caudal_base"]["width"] / H; res["caudal_base"]["height_H"] = res["caudal_base"]["height"] / H
json.dump(res, open(OUT + "/pa_measurements.json", "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=lambda x: round(float(x), 3)))

# RAC RM-OT-05F brief figure: the six hard-form families (A-F) and the no-touch zones painted on the START MESH (unorganized accepted-route
# Gorrund reference, R-6) in the four matched views (front, front 3/4, profile, rear 3/4), plus the true-floor margin map (how far the start
# mesh sits above the 05D true skeletal floor = the maximum depth the sculpt may cut, per vertex). Flat-shaded painter's-algorithm render.
# Usage: python3 f_regionmap.py   -> HANDOFF/figures/region_map.png, floor_margin.png
import os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from f_common import *
COL = {'A_trunk_section_S2_S5': '#1f77b4', 'B_posterior_axial_load_path': '#d62728', 'C_pelvis_to_thigh': '#9467bd', 'D_knee_shank_ankle': '#2ca02c',
       'E_elbow_forearm_wrist': '#ff7f0e', 'F_shoulder_girdle_neck_root': '#17becf', 'NO_TOUCH_head_neck': '#444444', 'NO_TOUCH_hands_digits': '#444444', 'NO_TOUCH_toes_forefoot': '#444444'}
VIEWS = (('front', 0), ('front 3/4', 35), ('profile', 90), ('rear 3/4', 145))
def render(ax, V, F, fc, yaw, title):
    a = np.radians(yaw); Rz = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    P = V @ Rz.T                                   # camera looks along -y' (from the front toward the back)
    tri = P[F]; depth = tri[:, :, 1].mean(1); order = np.argsort(depth)
    nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); nrm /= np.maximum(np.linalg.norm(nrm, axis=1), 1e-9)[:, None]
    shade = np.clip(0.35 + 0.65 * np.abs(nrm[:, 1]), 0, 1)
    cols = fc * shade[:, None]
    tri2 = tri[:, :, [0, 2]].copy(); tri2[:, :, 0] *= -1; pc = PolyCollection(tri2[order], facecolors=np.clip(cols[order], 0, 1), edgecolors='none'); ax.add_collection(pc)
    ax.set_xlim(-P[:, 0].max() - 5, -P[:, 0].min() + 5); ax.set_ylim(-2, P[:, 2].max() + 4); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=11)
if __name__ == '__main__':
    out = HANDOFF + '/figures'; os.makedirs(out, exist_ok=True)
    V, B, L, J, f, z0 = route_state(SKELETON_BODY); F = B['F']; keep = B['keep'].astype(bool); Fk = F[keep[F].all(1)]
    R = regions(B, V, J)
    vc = np.tile(np.array([0.82, 0.82, 0.82]), (len(V), 1))
    for k, m in R.items(): vc[m] = matplotlib.colors.to_rgb(COL[k])
    fc = vc[Fk].mean(1)
    fig, axs = plt.subplots(1, 4, figsize=(20, 11))
    for ax, (t, y) in zip(axs, VIEWS): render(ax, V, Fk, fc, y, t)
    hs = [plt.Rectangle((0, 0), 1, 1, color=COL[k]) for k in list(COL)[:7]]
    fig.legend(hs, ['A trunk section S2-S5', 'B posterior axial load path', 'C pelvis -> thigh', 'D knee / shank / ankle', 'E elbow / forearm / wrist', 'F shoulder girdle / neck root', 'NO-TOUCH (head / neck, hands / digits, toes / forefoot)'], loc='lower center', ncol=4, fontsize=11)
    fig.suptitle('RM-OT-05F Gorrund hand-sculpt: hard-form families on the START MESH (accepted route, 230.9 cm, R-6). Regions are approximate guides from rig weights; the brief text governs.', fontsize=12)
    fig.tight_layout(rect=[0, 0.06, 1, 0.95]); fig.savefig(out + '/region_map.png', dpi=90); plt.close(fig)
    Fl = floor_in_body_frame(L, f, z0); n = TE.outward_normals(Fl, F, keep); m_ = np.einsum('ij,ij->i', V - Fl, n)
    ext = np.clip(B['w_head'] + B['w_neck_01'] + B['w_hand_l'] + B['w_hand_r'] + B['w_fingers_l'] + B['w_fingers_r'], 0, 1) >= 0.3
    cm = plt.get_cmap('viridis'); vc = cm(np.clip(m_ / 8.0, 0, 1))[:, :3]; vc[ext] = 0.55
    fig, axs = plt.subplots(1, 4, figsize=(20, 11))
    for ax, (t, y) in zip(axs, VIEWS): render(ax, V, Fk, vc[Fk].mean(1), y, t)
    sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(0, 8)); fig.colorbar(sm, ax=axs, orientation='horizontal', fraction=0.03, pad=0.02, label='start mesh height above the 05D true skeletal floor (cm) = maximum inward sculpt depth (grey = no-touch)')
    fig.suptitle('RM-OT-05F Gorrund hand-sculpt: inward sculpt budget on the START MESH (reference composition). The low-composition route has less: check GO_low_route_r6.obj.', fontsize=12)
    fig.savefig(out + '/floor_margin.png', dpi=90, bbox_inches='tight'); plt.close(fig)
    print('ok', {k: int(m.sum()) for k, m in R.items()})

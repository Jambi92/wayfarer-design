# RM-OT-05AI evidence: whole-body F / P / B / 3/4 point-shaded views, 05AI baseline (top row) vs 05AI AC1 (bottom row).
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
B = np.load('after_VF.npz'); V0, F = B['V'] * 100, B['F']; V1 = np.load('ac1_VF.npz')['V'] * 100
def view(V, yaw):
    c, s = np.cos(np.radians(yaw)), np.sin(np.radians(yaw)); R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]]); W = V @ R.T
    T = W[F]; n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]); n /= np.maximum(np.linalg.norm(n, axis=1), 1e-20)[:, None]; ct = T.mean(1)
    m = -n[:, 1] > 0; o = np.argsort(ct[m, 1])[::-1]; return ct[m, 0][o], ct[m, 2][o], np.clip(-n[m, 1][o], 0, 1)
fig, ax = plt.subplots(2, 4, figsize=(20, 14), facecolor='#222')
for r, (V, lab) in enumerate([(V0, '05AI baseline'), (V1, '05AI AC1 (PASS)')]):
    for c, (yaw, t) in enumerate([(0, 'front'), (90, 'profile'), (180, 'back'), (35, '3/4')]):
        u, v, s = view(V, yaw); a = ax[r, c]; a.scatter(u, v, c=s, cmap='gray', s=0.04, vmin=0, vmax=1, linewidths=0)
        a.set_aspect('equal'); a.axis('off'); a.set_facecolor('#222'); a.set_title(f'{lab} - {t}', color='w', fontsize=10)
plt.tight_layout(); plt.savefig('ai_whole_FPB34.jpg', dpi=80, facecolor='#222', pil_kwargs=dict(quality=85))

# cg_t7_scaled.py R6.npz CAND.npz OUT.json [CAND2.npz ...] : DIAGNOSTIC T-7 cross-check for the compact Cogling bodies (order 9424c72 §11). The authoritative T-7
# (marchfolk_rp3_v001/anatomy.py) rasterises both silhouettes at a FIXED 3 px / cm and requires IoU >= 0.995. A 76 cm body covers ~44 % of the pixels of a
# 173 cm body, so the same sub-millimetre surface agreement loses IoU to edge quantisation alone (profile of a thin 76 cm body). Here the resolution is scaled
# by 173.143 / stature (each body occupies the Marchfolk pixel extent); everything else is exactly the anatomy.py silhouette method. The authoritative
# value is reported unchanged next to it.
import sys, json, numpy as np
from PIL import Image, ImageDraw
a = sys.argv[1:]; r6 = np.load(a[0]); OUT = a[2]; cands = [a[1]] + a[3:]
SV = r6['V'].astype(float); SF = r6['F']; keep = r6['keep']; H = float(SV[keep][:, 2].max() - SV[keep][:, 2].min())
def run(px, Vp, TP):
    ZT = max(185.0 * H / 173.143 if px > 3.0 else 185.0, float(np.ceil(SV[keep][:, 2].max() + 5))); XO = max(60.0 * (H / 173.143 if px > 3.0 else 1.0), float(np.ceil(np.abs(SV[keep][:, :2]).max() + 10)))
    def sil(V, F, yaw, ss=4):
        an = np.radians(yaw); Rm = np.array([[np.cos(an), -np.sin(an), 0], [np.sin(an), np.cos(an), 0], [0, 0, 1]]); P = V @ Rm.T; q = px * ss
        u = (P[:, 0] + XO) * q; v = (ZT - P[:, 2]) * q; W_, H_ = int(2 * XO * px), int((ZT + 5) * px)
        im = Image.new('L', (W_ * ss, H_ * ss), 0); dr = ImageDraw.Draw(im)
        for t in F: dr.polygon([(u[t[0]], v[t[0]]), (u[t[1]], v[t[1]]), (u[t[2]], v[t[2]])], fill=255)
        a_ = np.array(im, float).reshape(H_, ss, W_, ss).mean((1, 3)); return a_ >= 127.5
    iou = {}
    for nm, yaw in (('front', 0), ('rear', 180), ('profile_left', 90), ('profile_right', -90)):
        A = sil(SV, SF, yaw); B = sil(Vp, TP, yaw); iou[nm] = round(float((A & B).sum() / (A | B).sum()), 6)
    return iou
res = dict(source=a[0].split('/')[-1], stature_cm=round(H, 3), px_scaled=round(3.0 * 173.143 / H, 4), candidates={})
for c in cands:
    cz = np.load(c); Vp = cz['V'].astype(float); Q = cz['Q']; TP = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]
    s = run(3.0 * 173.143 / H, Vp, TP); res['candidates'][c.split('/')[-1]] = dict(iou_scaled=s, T7_scaled_pass=bool(min(s.values()) >= 0.995))
    print(c.split('/')[-1], s, min(s.values()) >= 0.995)
json.dump(res, open(OUT, 'w'), indent=1)

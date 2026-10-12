# RAC RM-OT-05K §18 neutralized body-only review sheet: head / neck removed, height-normalized, neutral grey + silhouette,
# front / front 3-4 / profile / rear 3-4, GO-RF candidates beside the human-family controls (Marchfolk, Skarn reference + Broad) and the
# frozen Grask E3 (protocol renderer of RM-OT-05A/05F: ot05r_package.ensure / tile).   Usage: python3 k_review.py OUT.jpg TAG=PATHPREFIX ...
import os, sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05_drivers')
import ot05r_package as PK
S = PK.S; PK.R = S + '/rmot05k/rend'; os.makedirs(PK.R, exist_ok=True)
CTRL = [] if os.environ.get('NOCTRL') else [('MF-ref', S + '/w1f/final/MF-M-R'), ('SK-ref', S + '/w1f/final/SK'), ('SK-brd', S + '/w2b/fr/SKMBroad'), ('GR-E3', S + '/w2c/b/GR5DE3/GR5DE3')]
out = sys.argv[1]; items = CTRL + [tuple(a.split('=', 1)) for a in sys.argv[2:]]
views = os.environ.get('VIEWS', 'F,Q,P,RQ').split(','); sil = os.environ.get('SIL') == '1'; th = 420
rows = []
for lab, p in items:
    PK.BODIES['K:' + lab] = (p, lab); t = PK.ensure('K:' + lab, headless=True); ims = []
    for v in views:
        im = PK.tile(t, v, sil=sil); a = np.array(im.split()[3]); rr = np.where(a.max(1) > 0)[0]; im = im.crop((0, rr[0], im.width, rr[-1] + 1))
        s = th / im.height; ims.append(im.resize((max(1, int(im.width * s)), th), Image.LANCZOS))
    rows.append((lab, ims))
W = sum(sum(i.width for i in ims) + 30 for _, ims in rows) + 20; img = Image.new('RGB', (W, th + 50), 'white'); d = ImageDraw.Draw(img); x = 10
for lab, ims in rows:
    d.text((x, 6), lab, fill='black'); xx = x
    for im in ims: img.paste(im, (xx, 30), im); xx += im.width
    x = xx + 30
img.save(out, quality=85); print(out, img.size)

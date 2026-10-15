# RM-OT-05W (order §6): contamination check for blind-sheet tiles, run BEFORE any sheet is assembled or shown to a scorer.
# 05V's tail mask left a detached tail fragment beside the candidate profile; every 05V scorer noticed it. This check makes that
# failure mechanical: each body tile must be ONE connected silhouette (alpha > threshold, 8-connectivity). Any extra island larger
# than MIN_PX pixels (fragment, floating tail piece, stray debris) fails the tile, and a failing tile blocks the sheet.
# Read-only; additive (v_blind.py / k_blind.py unchanged).
# Usage: python3 w_tile_check.py OUT.json TILE.png [TILE.png ...]   -> exit 0 all clean, 3 any contaminated
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
MIN_PX = 12          # islands smaller than this are anti-aliasing specks, not geometry
res = []
for p in sys.argv[2:]:
    a = np.array(Image.open(p).convert('RGBA'))[:, :, 3] > 20
    lab, n = ndimage.label(a, structure=np.ones((3, 3)))
    sizes = np.bincount(lab.ravel())[1:] if n else np.array([], int)
    big = sorted([int(s) for s in sizes if s >= MIN_PX], reverse=True)
    res.append(dict(tile=p.split('/')[-1], islands=len(big), island_px=big[:6], clean=len(big) == 1))
ok = all(r['clean'] for r in res)
json.dump(dict(min_island_px=MIN_PX, all_clean=ok, tiles=res), open(sys.argv[1], 'w'), indent=1)
for r in res:
    if not r['clean']: print('CONTAMINATED', r['tile'], r['island_px'])
print('ALL CLEAN' if ok else 'CONTAMINATION FOUND', len(res), 'tiles'); sys.exit(0 if ok else 3)

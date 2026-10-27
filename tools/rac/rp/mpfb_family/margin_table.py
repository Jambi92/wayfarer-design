# margin_table.py WORK OUTDIR : order a18371c §11 -- family margin table. For every station and each of the four family configurations: loops (D1+D3+D4,
# authoritative), contract minimum, margin = loops - minimum, crease poles (all / own digit), loop mode (fallback), status; frozen v003 vs successor v004;
# plus the PROPOSED D5 verdicts on v004 (reported separately, never authoritative). Writes JSON + CSV + a heat-table sheet.
import sys, os, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from v004_lib import *
from val2lib import evaluate, REF_STATURE_CM
W, O = sys.argv[1:3]; os.makedirs(O, exist_ok=True)
V3J = {'MF-M-R': '/tmp/claude-0/rt/m3/v4/MF-M-R_v003_validator_v2_D4.json', 'MF-F-R': '/tmp/claude-0/rt/m3/v4/MF-F-R_v003_validator_v2_D4.json',
       'SK208-C1R': '/tmp/claude-0/rt/sk/val/SK208-C1R_fam_validator_v2_D4.json', 'SKF208': '/tmp/claude-0/rt/sk/val/SKF208_fam_validator_v2_D4.json'}
T = {}; D5 = {}
for cid in CFG:
    v3 = json.load(open(V3J[cid]))['stations']; v4 = json.load(open('%s/val/%s_v004_validator_v2_D4.json' % (W, cid)))['stations']
    cz = np.load('%s/cand/%s_v004.npz' % (W, cid)); e5 = evaluate(cz['V'].astype(float), np.asarray(cz['Q']), json.loads(str(cz['meta'])), REF_STATURE_CM, d5=True)
    json.dump(e5, open('%s/val/%s_v004_validator_v2_D4_D5proposed.json' % (W, cid), 'w'), indent=1); D5[cid] = e5['summary']
    for k in v4:
        r3, r4, r5 = v3[k], v4[k], e5['stations'][k]
        T.setdefault(k, {})[cid] = dict(required=r4['required'], v003_loops=r3['loops_v2'], v003_margin=r3['loops_v2'] - r3['required'], v003_firm=r3['firm_D1_D3'],
                                        v004_loops=r4['loops_v2'], v004_margin=r4['margin'], v004_firm=r4['firm_D1_D3'], v004_status=r4['status_D1_D3'], loop_mode=r4['loop_mode'],
                                        crease_poles=len(r4['crease_poles']), crease_poles_own_digit=len(r4['crease_poles_own_digit']), crease_poles_adjacent_digit=len(r4['crease_poles_adjacent_digit']),
                                        D5_loops=r5['loops_v2'], D5_margin=r5['margin'], D5_firm=r5['firm_D1_D3'], D5_status=r5['status_D1_D3'])
summ = {cid: dict(v004_firm=sum(T[k][cid]['v004_firm'] for k in T), v003_firm=sum(T[k][cid]['v003_firm'] for k in T), D5_firm=sum(T[k][cid]['D5_firm'] for k in T),
                  v004_margin0=sorted(k for k in T if T[k][cid]['v004_margin'] == 0), v003_margin0=sorted(k for k in T if T[k][cid]['v003_margin'] == 0),
                  v004_fail=sorted(k for k in T if not T[k][cid]['v004_firm']), D5_fail=sorted(k for k in T if not T[k][cid]['D5_firm'])) for cid in CFG}
shared0 = sorted(k for k in T if all(T[k][c]['v004_margin'] == 0 for c in CFG)); any0 = sorted(k for k in T if any(T[k][c]['v004_margin'] <= 0 for c in CFG))
json.dump(dict(stations=T, summary=summ, shared_margin0_all_four=shared0, margin_le0_any=any0, D5_summary=D5), open(O + '/MPFB_FAMILY_v004_margin_table.json', 'w'), indent=1)
with open(O + '/MPFB_FAMILY_v004_margin_table.csv', 'w') as fh:
    fh.write('station,required,' + ','.join('%s_v003_loops,%s_v004_loops,%s_v004_margin,%s_v004_status,%s_mode,%s_crease_own,%s_D5_loops' % ((c,) * 7) for c in CFG) + '\n')
    for k in T: fh.write('%s,%d,' % (k, T[k]['MF-M-R']['required']) + ','.join('%d,%d,%d,%s,%s,%d,%d' % (T[k][c]['v003_loops'], T[k][c]['v004_loops'], T[k][c]['v004_margin'], T[k][c]['v004_status'], T[k][c]['loop_mode'], T[k][c]['crease_poles_own_digit'], T[k][c]['D5_loops']) for c in CFG) + '\n')
# ---- sheet: station x configuration heat table (v003 margin | v004 margin), margin 0 amber, < 0 red
from PIL import Image, ImageDraw, ImageFont
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
ks = list(T); rh = 17; cw = 34; gap = 16; x0 = 120; blkw = x0 + 4 * (2 * cw + gap); half = (len(ks) + 1) // 2
S = Image.new('RGB', (max(1180, 20 + 2 * blkw + 30), 100 + half * rh), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), 'MPFB family margin table, D1 + D3 + D4 (authoritative). Cell = loops / contract minimum; left = frozen v003 fit, right = successor v004.', fill=(0, 0, 0), font=f(12, True))
d.text((10, 26), 'green = margin >= 1, amber = margin 0, red = FAIL (loops < minimum or own-digit crease pole). Blue outline + "->n" = loops under the PROPOSED D5 rule where it differs (not authoritative).', fill=(60, 60, 60), font=f(11))
def col(m, firm): return (230, 80, 70) if (m < 0 or not firm) else ((245, 200, 80) if m == 0 else ((200, 235, 200) if m == 1 else (150, 215, 150)))
LAB = {'MF-M-R': 'MF-M', 'MF-F-R': 'MF-F', 'SK208-C1R': 'SK-C1R', 'SKF208': 'SK-F'}
for blk in range(2):
    bx = 10 + blk * (blkw + 20)
    for j, c in enumerate(CFG): d.text((bx + x0 + j * (2 * cw + gap), 52), LAB[c] + ' v3|v4', fill=(0, 0, 0), font=f(10, True))
    for i, k in enumerate(ks[blk * half:(blk + 1) * half]):
        y = 70 + i * rh; d.text((bx, y), k, fill=(0, 0, 0), font=f(11))
        for j, c in enumerate(CFG):
            t = T[k][c]; xx = bx + x0 + j * (2 * cw + gap)
            for q, (m, fm, lp) in enumerate(((t['v003_margin'], t['v003_firm'], t['v003_loops']), (t['v004_margin'], t['v004_firm'], t['v004_loops']))):
                d.rectangle([xx + q * cw, y, xx + q * cw + cw - 2, y + rh - 2], fill=col(m, fm)); d.text((xx + q * cw + 2, y + 1), '%d/%d' % (lp, t['required']), fill=(0, 0, 0), font=f(10))
            if t['D5_loops'] != t['v004_loops'] or t['D5_firm'] != t['v004_firm']: d.rectangle([xx + cw, y, xx + 2 * cw - 2, y + rh - 2], outline=(20, 60, 220), width=2); d.text((xx + 2 * cw, y + 1), '>%d' % t['D5_loops'], fill=(20, 60, 220), font=f(10, True))
S.save(O + '/MPFB_v004_margin_table.jpg', quality=90)
print(json.dumps(summ, indent=1)); print('shared margin-0 (all four):', shared0)

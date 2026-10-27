# sg_margin_sheet.py OUT.jpg OUT.csv LABEL=VALIDATOR.json ... : order d921903 -- final 69-station margin heat table + CSV under the authoritative
# D1 + D3 + D4 + D5 + D6 validator for every family realization.
import sys, json
from PIL import Image, ImageDraw, ImageFont
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; f = lambda n, b=False: ImageFont.truetype(FB if b else FN, n)
OJ, OC = sys.argv[1:3]; VAL = dict(a.split('=') for a in sys.argv[3:]); VV = {k: json.load(open(p))['stations'] for k, p in VAL.items()}; cols = list(VAL); names = sorted(VV[cols[0]])
cw2 = 92; half = (len(names) + 1) // 2; S = Image.new('RGB', (2 * (180 + len(cols) * cw2 + 10) + 20, 80 + half * 17 + 30), 'white'); d = ImageDraw.Draw(S)
d.text((10, 8), '69-station margin table — D1 + D3 + D4 + D5 + D6 (authoritative, d921903); cell = loops / minimum, margin; * = a D6 foreign-segment side excluded', fill=(0, 0, 0), font=f(14, True))
mc = lambda m: (200, 30, 30) if m < 0 else ((235, 150, 40) if m == 0 else ((240, 220, 90) if m == 1 else (120, 200, 120)))
for h in range(2):
    xo = 10 + h * (180 + len(cols) * cw2 + 10)
    for j, c in enumerate(cols): d.text((xo + 180 + j * cw2, 34), c, fill=(0, 0, 0), font=f(10, True))
    for i, nm in enumerate(names[h * half:(h + 1) * half]):
        y = 52 + i * 17; d.text((xo, y + 2), nm, fill=(0, 0, 0), font=f(11))
        for j, c in enumerate(cols):
            r = VV[c][nm]; m = r['margin']; d.rectangle([xo + 180 + j * cw2, y, xo + 180 + (j + 1) * cw2 - 3, y + 15], fill=mc(m) if r['firm_D1_D3'] else (200, 30, 30))
            d.text((xo + 184 + j * cw2, y + 2), '%d/%d %+d%s%s' % (r['loops_v2'], r['required'], m, '*' if r.get('D6_undefined_sides') else '', '' if r['firm_D1_D3'] else ' FAIL'), fill=(0, 0, 0), font=f(10))
d.text((10, 60 + half * 17), 'firm: ' + '   '.join('%s %d / 69' % (c, sum(v['firm_D1_D3'] for v in VV[c].values())) for c in cols), fill=(0, 0, 0), font=f(12, True))
S.save(OJ, quality=88)
with open(OC, 'w') as fo:
    fo.write('station,' + ','.join('%s_loops,%s_required,%s_margin,%s_status,%s_D6_sides' % ((c,) * 5) for c in cols) + '\n')
    for nm in names: fo.write(nm + ',' + ','.join('%d,%d,%d,%s,%s' % (VV[c][nm]['loops_v2'], VV[c][nm]['required'], VV[c][nm]['margin'], VV[c][nm]['status_D1_D3'], '|'.join(VV[c][nm]['D6_undefined_sides'])) for c in cols) + '\n')
print('margin sheet', {c: sum(v['firm_D1_D3'] for v in VV[c].values()) for c in cols})

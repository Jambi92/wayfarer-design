# RM-OT-05W (order §4 / §5): labelled NEGATIVE-reference exhibit for the new Gorrund source brief. Images document what to avoid ONLY;
# none of these bodies may be used as a shape target, donor or disguised starting point. Built from already-committed evidence renders.
# Usage: python3 w_negative_sheet.py U8_vs_N1_vs_R6.jpg cmb_GO_fin.jpg OUT.jpg
import sys, textwrap
from PIL import Image, ImageDraw, ImageFont
a_p, c_p, out = sys.argv[1:4]
A = Image.open(a_p).convert('RGB'); rh = A.height // 3                 # rows: U8cp1 / GO-ARM-N1 / N1_R6
u8 = A.crop((0, 0, A.width, rh)); n1 = A.crop((0, rh, A.width, 2 * rh)); c = Image.open(c_p).convert('RGB')
W = 1800
def fit(im): return im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
panels = [(fit(u8), 'AVOID 1 - U8 cp1 (recovered Rodin source lineage): fused loincloth / belt / bracers / wraps / necklace, mane hiding neck and back, '
                      'bodybuilder definition, oversized feet. Presentation and composition, not structure, carry the read.'),
          (fit(n1), 'AVOID 2 - GO-ARM-N1 (05V procedural neutralization, 93 % reconstructed): field-blend lumps, bent knees, zig-zag leg profile, '
                    'giant feet, muscle masses read as "massive hunched brute" by 6/6 blind scorers.'),
          (fit(c), 'AVOID 3 - 05C code-built race-base candidates (solver / SDF surface): clean but generic; blind-read as "heavy / stocky human".')]
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22); big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
except Exception: font = big = ImageFont.load_default()
H = 70 + sum(p.height + 70 for p, _ in panels); sheet = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(sheet)
d.text((12, 14), 'NEGATIVE REFERENCES ONLY - never shape targets, donors or starting points (RM-OT-05W §4)', font=big, fill=(170, 0, 0))
y = 70
for p, lab in panels:
    for i, ln in enumerate(textwrap.wrap(lab, 140)[:2]): d.text((12, y + 6 + 28 * i), ln, font=font, fill='black')
    sheet.paste(p, (0, y + 64)); y += p.height + 70
sheet.save(out, quality=88); print(out)

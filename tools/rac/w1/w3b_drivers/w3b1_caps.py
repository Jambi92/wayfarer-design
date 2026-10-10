# RAC W3B1 section 6: large-unit visual brackets for the size ends W3B did not bound with a metric failure (x2.5 'not reached').
# Matched close cameras per field (w3b_scale_sheets.cam), size x1.0 / 1.25 / 1.5 / 1.75 / 2.0 on the reseeded field (rng 7, relief x1),
# surfaced copies; grid sheet rows = fields, columns = multipliers. Fields: one per class / failure mode - cranial structural, dorsal trunk,
# dorsal tail, knee (articulation), chest / abdomen (ventral), dorsal hand, dorsal foot, wrist (articulation, finest bend), tail underside.
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG, w3b_sheet as SS, w3b_scale_sheets as SH
FIELDS = ['face_cranial_structural', 'S_dorsal_trunk', 'S_dorsal_tail', 'S_dorsal_hand', 'S_dorsal_foot', 'A_knee', 'A_wrist', 'V_chest_abdomen', 'V_tail_underside']
MULT = [1.0, 1.25, 1.5, 1.75, 2.0]
def run():
    Z = SC.ref()
    for k in FIELDS:
        v, c, sc = SH.cam(k, 'c'); w = SC.weight(RG.masks()[k])
        for s in MULT:
            t = 'cap_%s_s%.2f' % (k, s)
            rel = SC.variant(w, s, 1.0, reseed=True)[0]
            SS.ensure(t, Z['Vu'] + rel[:, None] * Z['N'], Z['Fu'], v, res=700, box=lambda X, c=c, sc=sc: np.linalg.norm(X - c, axis=1) < 0.9 * sc)
        print(k, flush=True)
    cell = 300; lw = 220; top = 120
    img = Image.new('RGB', (lw + cell * len(MULT), top + cell * len(FIELDS) + 10), 'white'); d = ImageDraw.Draw(img)
    d.text((14, 12), 'W3B1 - large-unit visual brackets (scale-unit size multiplier, relief x1, reseeded field rng 7)', font=SS.font(24), fill='black')
    d.text((14, 48), 'Matched close camera per row. Columns x1.0 (reseeded reference) / 1.25 / 1.5 / 1.75 / 2.0. Diagnostic only.', font=SS.font(15), fill=(70, 70, 70))
    for j, s in enumerate(MULT): d.text((lw + j * cell + 6, top - 26), 'x%.2f' % s, font=SS.font(17), fill=(70, 70, 70))
    for i, k in enumerate(FIELDS):
        d.text((10, top + i * cell + cell // 2 - 10), k, font=SS.font(15), fill='black')
        for j, s in enumerate(MULT):
            p = '%s/cap_%s_s%.2f_c.png' % (SS.R, k, s)
            if os.path.exists(p):
                im = Image.open(p).convert('RGBA').resize((cell, cell), Image.LANCZOS); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); img.paste(bg, (lw + j * cell, top + i * cell))
    img.save(SS.SH + '/w3b1_large_unit_caps.jpg', quality=88); print(SS.SH + '/w3b1_large_unit_caps.jpg')
if __name__ == '__main__': run()

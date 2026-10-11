# RAC RM-OT-05: common-world-scale lineups. Every body is an accepted (or accepted-route) R-6 / reference-stance mesh; one ground plane
# (u = 0), one orthographic scale (4 px per cm), neutral grey Workbench material, front and profile. No uniform scaling anywhere: MPFB
# bodies come from the accepted macro / native routes, Saurin from the W2 regional route (sa_finish.build_f on the canonical W2 plan).
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w3b_drivers'))
import w3b_common as C, w3b_sheet as SS, w3b_bodies as BD
S = C.S; R = S + '/rmot05/rend'; SH = S + '/rmot05/sheets'; os.makedirs(R, exist_ok=True); os.makedirs(SH, exist_ok=True); RV = '/home/claude/wayfarer-design/reviews'
PX = 4.0; SCALE = 280.0; RES = int(SCALE * PX)
B = {  # id: (source, label)
 'MF-M-R': (S + '/w1f/final/MF-M-R', 'Marchfolk'), 'SK208-C1R': (RV + '/rac-w3d-evidence/geometry/SK208-C1R', 'Skarn'), 'SG': (S + '/w1f/final/SG', 'Sagekin'),
 'FNL4': (S + '/w1p/cand/FNL4', 'Fenn'), 'AEL1': (S + '/w1m/legs/AEL1', 'Aelari'), 'VAL4': (S + '/w1n/cand/VAL4', 'Vael'), 'HVC1': (S + '/w1s/probe/HVC1', 'Halvren'),
 'DU137C': (S + '/w2h1/st/DU137C-NAT', 'Durrim'), 'GR218R': (S + '/w2c/b/GR218R/GR218R', 'Grask'), 'GOREF': (S + '/w2d/b/GOREF/GOREF', 'Gorrund'),
 'PK-NAT': (S + '/w1f/final/PK-NAT', 'Pipkin'), 'CGJ7': (S + '/w1r/probe/CGJ7', 'Cogling'), 'SA-M188': ('saurin', 'Saurin'),
 'MFM147': (S + '/w2a/st/MFM147-NAT', 'Marchfolk'), 'SKM183-C1R': (S + '/w3d/b/SKM183-C1R', 'Skarn'), 'SG152': (S + '/w2e/st/SG152-NAT', 'Sagekin'), 'FN157': (S + '/w2f/st/FN157-NAT', 'Fenn'),
 'AE168': (S + '/w2f/rt/AE168N-NAT', 'Aelari'), 'VA157': (S + '/w2f/st/VA157-NAT', 'Vael'), 'HV152': (S + '/w2g/st/HV152N-NAT', 'Halvren (central env.)'),
 'HL147p2C': (S + '/w3a/lo/HL147p2C-NAT', 'Halvren (MF-supported reach)'), 'DU122C': (S + '/w2h1/st/DU122C-NAT', 'Durrim'), 'GR198': (S + '/w2c/b/GR198/GR198', 'Grask'),
 'GO208': (S + '/w2d/b/GO208/GO208', 'Gorrund'), 'PK91': (S + '/w2h/st/PK91-NAT', 'Pipkin'), 'CG76': (S + '/w2h/st/CG76-NAT', 'Cogling'), 'SA-M168': ('saurin', 'Saurin'),
 'MFM203': (S + '/w2a/st/MFM203', 'Marchfolk'), 'SKM229-C1R': (S + '/w3d/b/SKM229-C1R', 'Skarn'), 'SG208': (S + '/w2e/st/SG208', 'Sagekin'), 'FN211': (S + '/w2f/st/FN211', 'Fenn'),
 'AE221': (S + '/w2f/st/AE221', 'Aelari'), 'VA203': (S + '/w2f/st/VA203', 'Vael'), 'HV213M': (S + '/w2g/st/HV213M', 'Halvren (central env.)'),
 'HU228p8Sc': (S + '/w3a1/up/HU228p8Sc', 'Halvren (SK-supported reach)'), 'DU152C': (S + '/w2h1/st/DU152C-NAT', 'Durrim'), 'GR239': (S + '/w2c/b/GR239/GR239', 'Grask'),
 'GO251': (S + '/w2d/b/GO251/GO251', 'Gorrund'), 'PK122': (S + '/w2h/st/PK122-NAT', 'Pipkin'), 'CG107': (S + '/w2h/st/CG107-NAT', 'Cogling'), 'SA-M208': ('saurin', 'Saurin'),
 'MFM190': (S + '/w2b/st/MFM190', 'Marchfolk'), 'HV190M': (S + '/w2g/st/HV190M', 'Halvren'), 'SKM190-C1R': (S + '/w3d/b/SKM190-C1R', 'Skarn'), 'SKM203-C1R': (S + '/w3d/b/SKM203-C1R', 'Skarn'),
 'HV203M': (S + '/w2g/st/HV203M', 'Halvren'), 'FN190': (S + '/w2f/st/FN190', 'Fenn'), 'VA190': (S + '/w2f/st/VA190', 'Vael'), 'FN203': (S + '/w2f/st/FN203', 'Fenn'), 'AE203': (S + '/w2f/st/AE203', 'Aelari'),
 'GR208': (S + '/w2c/b/GR208/GR208', 'Grask'), 'GR229': (S + '/w2c/b/GR229/GR229', 'Grask'), 'GO229': (S + '/w2d/b/GO229/GO229', 'Gorrund'), 'CG91': (S + '/w2h/st/CG91R-NAT', 'Cogling'), 'PK107': (S + '/w2h/st/PK107R-NAT', 'Pipkin')}
def mesh(bid):
    src = B[bid][0]
    if src == 'saurin': P = BD.build(bid); return P, C.F0, np.ones(len(P), bool)
    d = np.load(src + '_r6.npz', allow_pickle=True); return d['V'].astype(float), d['F'], d['keep'].astype(bool)
def ensure(bid):
    if all(os.path.exists('%s/%s_%s.png' % (R, bid, n)) for n in 'FP'): return
    P, F, keep = mesh(bid); cf = 0.5 * (P[keep, 1].min() + P[keep, 1].max())
    v = "F:0:0:0:0:%.2f:%.1f;P:90:0:0:%.2f:%.2f:%.1f" % (SCALE / 2 - 5, SCALE, cf, SCALE / 2 - 5, SCALE)
    C.save_head_npz(R + '/%s.npz' % bid, P, F, lambda Q: keep); C.render(R + '/%s.npz' % bid, R + '/' + bid, v, RES); os.remove(R + '/%s.npz' % bid)
def stature(bid):
    P, F, keep = mesh(bid); return float(P[keep, 2].max() - P[keep, 2].min())
def crop(im):
    a = np.array(im.split()[3]); cols = np.where(a.max(0) > 0)[0]; return im.crop((max(cols[0] - 12, 0), 0, min(cols[-1] + 12, im.width), im.height))
def lineup(out, title, ids, views='FP', note=''):
    for b in ids: ensure(b)
    tiles = []
    for b in ids:
        for v in views:
            im = crop(Image.open('%s/%s_%s.png' % (R, b, v)).convert('RGBA')); tiles.append((b, v, im))
    W = sum(t[2].width for t in tiles) + 120; top = 110; Hc = RES; img = Image.new('RGB', (W, top + Hc + 70), 'white'); d = ImageDraw.Draw(img)
    d.text((14, 12), title, font=SS.font(26), fill='black')
    d.text((14, 50), 'One ground plane, one orthographic scale (4 px / cm), matched neutral reference stance, neutral grey. ' + note, font=SS.font(15), fill=(70, 70, 70))
    g = top + Hc - int((SCALE / 2 - 5 - (-SCALE / 2 + SCALE / 2 - 5)) * 0)   # ground row in the render: camera centre at u = SCALE/2 - 5
    ground = top + int(Hc / 2 + (SCALE / 2 - 5) * PX)
    for cm in range(0, 261, 20):
        y = ground - int(cm * PX); d.line((0, y, W, y), fill=(232, 232, 232) if cm else (120, 120, 120), width=1); d.text((4, y - 16), '%d' % cm, font=SS.font(13), fill=(110, 110, 110))
    x = 60
    for b, v, im in tiles:
        bg = Image.new('RGBA', im.size, (255, 255, 255, 0)); img.paste(im, (x, top), im)
        if v == views[0]: d.multiline_text((x, ground + 8), '%s\n%s %.0f cm' % (B[b][1], b, stature(b)), font=SS.font(13), fill='black')
        x += im.width
    img.save(SH + '/' + out, quality=86); print(out, flush=True)
if __name__ == '__main__':
    REF = ['CGJ7', 'PK-NAT', 'DU137C', 'MF-M-R', 'VAL4', 'SG', 'HVC1', 'FNL4', 'SA-M188', 'AEL1', 'SK208-C1R', 'GR218R', 'GOREF']
    MIN = ['CG76', 'PK91', 'DU122C', 'HL147p2C', 'MFM147', 'HV152', 'SG152', 'FN157', 'VA157', 'AE168', 'SA-M168', 'SKM183-C1R', 'GR198', 'GO208']
    MAX = ['CG107', 'PK122', 'DU152C', 'MFM203', 'VA203', 'SG208', 'SA-M208', 'FN211', 'HV213M', 'AE221', 'HU228p8Sc', 'SKM229-C1R', 'GR239', 'GO251']
    lineup('ot05_A_reference_lineup.jpg', 'RM-OT-05 A - full-roster reference / central lineup (front)', REF, 'F', 'Accepted reference ARMs (Skarn with the C1R central face).')
    lineup('ot05_A2_reference_lineup_profile.jpg', 'RM-OT-05 A - full-roster reference / central lineup (profile)', REF, 'P', 'Saurin tail extends behind the body (tail excluded from stature).')
    lineup('ot05_B_minimum_lineup.jpg', 'RM-OT-05 B - full-roster minimum lineup (front)', MIN, 'F', 'Accepted minimum-stature realizations; Halvren central-envelope 152 and the MF-supported reach 147.2 both shown.')
    lineup('ot05_C_maximum_lineup.jpg', 'RM-OT-05 C - full-roster maximum lineup (front)', MAX, 'F', 'Accepted maximum-stature realizations; Halvren central-envelope 213 and the SK-supported reach 228.8 both shown.')
    lineup('ot05_D_world_extremes.jpg', 'RM-OT-05 D - world-scale extremes: Cogling 76 cm, Marchfolk 173 cm reference, Gorrund 251 cm', ['CG76', 'MF-M-R', 'GO251'], 'FP')
    lineup('ot05_E1_mf_hv_sk.jpg', 'RM-OT-05 E1 - Marchfolk / Halvren / Skarn at matched 190 and 203 cm', ['MFM190', 'HV190M', 'SKM190-C1R', 'MFM203', 'HV203M', 'SKM203-C1R'], 'FP')
    lineup('ot05_E2_elves_halvren.jpg', 'RM-OT-05 E2 - Fenn / Aelari / Vael / Halvren at matched 190 and 203 cm', ['FN190', 'AEL1', 'VA190', 'HV190M', 'FN203', 'AE203', 'VA203', 'HV203M'], 'FP')
    lineup('ot05_E3_short_races.jpg', 'RM-OT-05 E3 - short races at matched 91 / 107 / 122 cm (Cogling / Pipkin / Durrim)', ['CG91', 'PK91', 'CG107', 'PK107', 'PK122', 'DU122C'], 'FP')
    lineup('ot05_E4_large_races.jpg', 'RM-OT-05 E4 - Skarn / Grask / Gorrund at matched 208 and 229 cm', ['SK208-C1R', 'GR208', 'GO208', 'SKM229-C1R', 'GR229', 'GO229'], 'FP')

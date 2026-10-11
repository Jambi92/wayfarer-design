# RAC W3C (RM-CF-09): Skarn vs Marchfolk craniofacial tendency metrics on R-6 ARM meshes (x lateral, f = y anterior, u = z up, cm).
# Reuses the W1c cranio() landmark set (arm_measure.py: G*, N*, prn, sn, sto, Pg, Me, Gn, V, Op, Po*, Eu, Zy, Or*, Os*, Mf*, Ec*) and adds:
#  skull  : HH/H, HL/H, Eu/HH (breadth), HL/HH (depth), lower-cranial breadth at Po* level / HH (ears excluded)
#  brow   : BGP = (G*.f - N*.f)/HL (glabellar projection over nasion); BSO = supraorbital projection over the corneal apex
#           (front-most surface 0.6-2.4 cm above the eye centre within +-0.5 cm of the eye's x, minus eye centre f - R) / HL;
#           BOR = supraorbital front minus infraorbital (Or* level) front / HL (brow over cheek depth)
#  jaw    : Go* = lateral-most head-surface point in the gonial band (u between Me+0.8 and sto-0.6, f behind the cheek: f < Ec*.f - 2,
#           f > Po*.f + 0.5, ears excluded); BGB = bigonial breadth / HH and / Zy; MDH = (sto.u - Me.u)/HH (mandibular body depth);
#           ramus proxy RAM = (Po*.u - Go*.u)/HH; chin width CW = surface breadth at Pg.u within 1.2 cm behind Pg / Zy (secondary)
#  neck   : NJT = neck breadth 3 cm below Me (neck-weighted skin) / bigonial breadth (neck-to-jaw transition)
#  midface: BZY = Zy/HH; MAL = anterior malar breadth (0.10-0.19 HH below the eye centres, anterior to 0.10 HH behind them) / HH; MPI (W1c); CHK = cheek front (maxillo-zygomatic band 1.6-3.2 cm below eye centre, |x| = eye x +-0.5) minus
#           Po*.f / HL; NOSE: nasal height NH = (N*.u - sn.u)/HH, nasal projection NP = (prn.f - sn.f)/HL, alar breadth AB / Zy
#  FPI / MPI / MdPI reported for the RM-CF-05 input appendix.
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(D))
import arm_measure as AM
def load(p):
    d = np.load(p, allow_pickle=True); return d, d['V'].astype(float), d['F'], d['keep'].astype(bool)
def metrics(p):
    d, V, F, keep = load(p); c = AM.cranio(d, V, F, keep); H = V[keep, 2].max() - V[keep, 2].min()
    hw = d['w_head']; ew = d['w_ears']; nw = d['w_neck_01']; el, er = d['eye_l'].astype(float), d['eye_r'].astype(float); R = float(d['eye_diam']) / 2
    hv = keep & (hw > 0.5) & (ew < 0.2); P = lambda k: np.array(c[k])
    HL, HH = c['HL'], c['HH']; po = P('Po*'); me = P('Me'); sto = P('sto'); sn = P('sn'); prn = P('prn'); g = P('G*'); n = P('N*'); pg = P('Pg')
    out = dict(H=float(H), HL=HL, HH=HH, Eu=c['Eu_Eu'], Zy=c['Zy_Zy'], FPI=c['FPI'], MPI=c['MPI'], MdPI=c['MdPI'])
    out['HH_H'] = HH / H; out['HL_H'] = HL / H; out['Eu_HH'] = c['Eu_Eu'] / HH; out['HL_HH'] = HL / HH
    band = hv & (np.abs(V[:, 2] - po[2]) < 0.6) & (V[:, 1] > po[1] - 3) & (V[:, 1] < po[1] + 3)
    out['LCB_HH'] = float((V[band, 0].max() - V[band, 0].min()) / HH)
    # brow
    out['BGP'] = float((g[1] - n[1]) / HL)
    so, orf = [], []
    for e in (el, er):
        m = keep & (hw > 0.5) & (np.abs(V[:, 0] - e[0]) < 0.5) & (V[:, 2] > e[2] + 0.6) & (V[:, 2] < e[2] + 2.4) & (V[:, 1] > e[1] - 1)
        so.append(V[m, 1].max() - (e[1] + R))
        m2 = keep & (hw > 0.5) & (np.abs(V[:, 0] - e[0]) < 0.5) & (V[:, 2] < e[2] - 1.2) & (V[:, 2] > e[2] - 2.6) & (V[:, 1] > e[1] - 1)
        orf.append(V[m, 1].max() - V[m2, 1].max())
    out['BSO'] = float(np.mean(so) / HL); out['BOR'] = float(np.mean(orf) / HL)
    # jaw
    ecf = np.nanmean([c['aperture'][s]['Ec*'][1] for s in ('l', 'r') if c['aperture'][s].get('Ec*')])
    gb = hv & (V[:, 2] > me[2] + 0.8) & (V[:, 2] < sto[2] - 0.6) & (V[:, 1] < ecf - 2.0) & (V[:, 1] > po[1] + 0.5)
    gl = V[gb & (V[:, 0] > 0)]; gr = V[gb & (V[:, 0] < 0)]; Gl = gl[np.argmax(gl[:, 0])]; Gr = gr[np.argmin(gr[:, 0])]
    bgb = Gl[0] - Gr[0]; out['Go_l'] = Gl.tolist(); out['Go_r'] = Gr.tolist(); out['BGB_cm'] = float(bgb)
    out['BGB_HH'] = float(bgb / HH); out['BGB_Zy'] = float(bgb / c['Zy_Zy']); out['MDH'] = float((sto[2] - me[2]) / HH)
    out['RAM'] = float((po[2] - 0.5 * (Gl[2] + Gr[2])) / HH)
    cw = keep & (np.abs(V[:, 2] - pg[2]) < 0.3) & (V[:, 1] > pg[1] - 1.2); out['CW_Zy'] = float((V[cw, 0].max() - V[cw, 0].min()) / c['Zy_Zy'])
    nb = keep & (nw > 0.5) & (np.abs(V[:, 2] - (me[2] - 3.0)) < 0.4)
    out['NJT'] = float((V[nb, 0].max() - V[nb, 0].min()) / bgb)
    # midface
    out['BZY'] = float(c['Zy_Zy'] / HH)
    ck = []
    for e in (el, er):
        m = keep & (hw > 0.5) & (np.abs(V[:, 0] - e[0]) < 0.5) & (V[:, 2] < e[2] - 1.6) & (V[:, 2] > e[2] - 3.2)
        ck.append(V[m, 1].max() - po[1])
    out['CHK'] = float(np.mean(ck) / HL)
    ez = 0.5 * (el[2] + er[2]); ef = 0.5 * (el[1] + er[1])
    mb = hv & (V[:, 2] < ez - 0.10 * HH) & (V[:, 2] > ez - 0.19 * HH) & (V[:, 1] > ef - 0.10 * HH)
    out['MAL'] = float((V[mb, 0].max() - V[mb, 0].min()) / HH)
    out['NH'] = float((n[2] - sn[2]) / HH); out['NP'] = float((prn[1] - sn[1]) / HL)
    ab = keep & (V[:, 2] > sn[2] + 0.2) & (V[:, 2] < sn[2] + 1.0) & (V[:, 1] > sn[1] - 1.0) & (np.abs(V[:, 0]) < 3)
    out['AB_Zy'] = float((V[ab, 0].max() - V[ab, 0].min()) / c['Zy_Zy'])
    out['landmarks'] = {k: c[k] for k in ('G*', 'N*', 'prn', 'sn', 'sto', 'Pg', 'Me', 'Po*', 'V', 'Op')}
    return out
KEYS = ['HH_H', 'HL_H', 'Eu_HH', 'HL_HH', 'LCB_HH', 'BGP', 'BSO', 'BOR', 'BGB_HH', 'BGB_Zy', 'MDH', 'RAM', 'CW_Zy', 'NJT', 'BZY', 'MAL', 'CHK', 'MPI', 'NH', 'NP', 'AB_Zy', 'FPI', 'MdPI']
if __name__ == '__main__':
    for p in sys.argv[1:]:
        m = metrics(p); print(os.path.basename(p), ' '.join('%s %.4f' % (k, m[k]) for k in KEYS), 'H %.1f HH %.2f' % (m['H'], m['HH']))

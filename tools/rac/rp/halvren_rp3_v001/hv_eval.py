# hv_eval.py OUT.json CFG ITEM:PREFIX ... : Halvren body / face source order (2026-10-29) §7 / §8 / §12 / §13 -- evaluation of source candidates
# (PREFIX = path without _r6.npz / _meas.json) at matched stature 178 cm against Marchfolk, Sagekin, Skarn (178 cm diagnostic), frozen Fenn, frozen Aelari,
# frozen Vael (the parent-gate comparator builds in /tmp/claude-0/rt/hv/partA/cmp), with the parent gate's 31-metric architecture (hv_partA.py):
#   body  material metric differences vs every source (>= 1 % and > 2x the human baseline |SG - MF|), groups departing from Marchfolk, nearest source,
#         arithmetic-average audit per human / elf pair (t positions, one-parameter scalar-blend fit) and a global single-elf blend test;
#   face  (ears excluded) per-region aligned RMS vs every source, regions departing from Marchfolk (RMS > max(0.5 % HH, 3x human baseline, 0.3 mm)),
#         regions distinct from each frozen elf, craniofacial descriptors vs Marchfolk and their human0 / elf1 position, anti-beauty indicators
#         (eye aperture / orbit size, nose, jaw width, lower-face height vs Marchfolk; the mixed read must not come mainly from these).
import sys, os, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import fn_face_metrics as F
OUT, CFG = sys.argv[1:3]; ITEMS = [a.split(':', 1) for a in sys.argv[3:]]; PA = '/tmp/claude-0/rt/hv/partA'
CMP = {'c1': dict(MF='MFM178', SG='SGM178', SK='SKM178', FN='FNM178', AE='AEM178', VA='VAM178'), 'c2': dict(MF='MFF178', SG='SGF178', SK='SKF178', FN='FNF178', AE='AEF178', VA='VAF178')}[CFG]
SRC = ('MF', 'SG', 'SK', 'FN', 'AE', 'VA'); ELF = ('FN', 'AE', 'VA'); PAIRS = [('MF', 'FN'), ('MF', 'AE'), ('MF', 'VA'), ('SG', 'FN'), ('SG', 'AE'), ('SK', 'VA')]
GROUPS = json.load(open(PA + '/HV_partA.json'))['groups']; KEYS = [k for g in GROUPS.values() for k in g]
mz = lambda p: json.load(open(p + '_meas.json'))['combined']
def R(m, k):
    r = m['ratio']
    if k in r: return r[k]
    if k == 'thoracic_vertical_share': return m['thoracic_vertical'] / m['stature']
    if k == 'cranial_vertical_share': return (m['cranio']['V'][2] - m['cranio']['OC_l'][2]) / m['stature']
    if k == 'shin_over_thigh': return r['shin_share'] / r['thigh_share']
    if k == 'foot_breadth_over_length': return m['mean']['foot_breadth'] / m['mean']['foot_len']
    if k == 'neck_over_torso': return r['neck_share'] / r['torso_share']
    raise KeyError(k)
pct = lambda a, b: 100 * (a / b - 1)
SM = {s: mz('%s/cmp/%s' % (PA, n)) for s, n in CMP.items()}; SD = {s: F.load('%s/cmp/%s_r6.npz' % (PA, n)) for s, n in CMP.items()}
def desc(V, m):
    d = F.descriptors(V); g = lambda k: V[F.LM[k]]; zy = abs(g('zygion_l')[0] - g('zygion_r')[0]); HH = d['head_height_cm']
    d['cranial_height_over_stature'] = (g('vertex')[2] - g('nasion')[2]) / (V[:, 2].max() - V[:, 2].min())
    d['face_height_over_bizygomatic'] = (g('nasion')[2] - g('menton')[2]) / zy; d['forehead_to_chin_over_bizygomatic'] = (g('forehead')[2] - g('menton')[2]) / zy
    d['brow_projection_over_HH'] = (g('glabella')[1] - g('nasion')[1]) / HH
    return d
SDES = {s: desc(SD[s]['V'], SM[s]) for s in SRC}
res = dict(config=CFG, comparators=CMP, items={})
for item, pre in ITEMS:
    m = mz(pre); v = {k: dict({s: R(SM[s], k) for s in SRC}, HV=R(m, k)) for k in KEYS}; hb = {k: abs(pct(v[k]['SG'], v[k]['MF'])) for k in KEYS}
    mat = lambda k, a, b: abs(pct(a, b)) >= 1.0 and abs(pct(a, b)) > 2 * hb[k]
    rows = {k: dict(HV=round(v[k]['HV'], 5), HV_vs_pct={s: round(pct(v[k]['HV'], v[k][s]), 2) for s in SRC}, material_vs={s: bool(mat(k, v[k]['HV'], v[k][s])) for s in SRC},
                    nearest=min(SRC, key=lambda s: abs(v[k]['HV'] - v[k][s]))) for k in KEYS}
    prot = {s: dict(material=sum(rows[k]['material_vs'][s] for k in KEYS), of=len(KEYS), by_group={g: sum(rows[k]['material_vs'][s] for k in ks) for g, ks in GROUPS.items()},
                    rms_pct=round(float(np.sqrt(np.mean([rows[k]['HV_vs_pct'][s] ** 2 for k in KEYS]))), 2)) for s in SRC}
    # departure from Marchfolk per group (any metric beyond the human baseline: |d| > max(0.5 %, 1x baseline)) -- the "meaningful signal" read of §7
    sig = {g: [k for k in ks if abs(rows[k]['HV_vs_pct']['MF']) > max(0.5, hb[k])] for g, ks in GROUPS.items()}
    avg = {}
    for H, E_ in PAIRS:
        ts = {}; X = []; Y = []
        for k in KEYS:
            if abs(pct(v[k][E_], v[k][H])) >= 1.0 and abs(pct(v[k][E_], v[k][H])) > 2 * hb[k]:
                ts[k] = (v[k]['HV'] - v[k][H]) / (v[k][E_] - v[k][H]); X.append((v[k][E_] - v[k][H]) / v[k][H]); Y.append((v[k]['HV'] - v[k][H]) / v[k][H])
        X = np.array(X); Y = np.array(Y); a = float((X @ Y) / (X @ X)) if len(X) else float('nan'); rr = Y - a * X; r2 = float(1 - (rr @ rr) / (Y @ Y)) if len(X) and (Y @ Y) > 0 else float('nan')
        tv = np.array(list(ts.values()))
        avg['%s-%s' % (H, E_)] = dict(n=len(ts), t={k: round(x, 3) for k, x in ts.items()}, t_median=round(float(np.median(tv)), 3) if len(tv) else None, t_iqr=[round(float(np.percentile(tv, q)), 3) for q in (25, 75)] if len(tv) else None,
                                      near_midpoint=int(np.sum(np.abs(tv - 0.5) <= 0.15)), outside_pair=int(np.sum((tv < 0) | (tv > 1))), alpha=round(a, 3), r2=round(r2, 3),
                                      residual_rms_pct=round(float(np.sqrt(np.mean(rr ** 2)) * 100), 3) if len(X) else None,
                                      t_by_group={g: [round(ts[k], 2) for k in ks if k in ts] for g, ks in GROUPS.items()})
    best = max(((k_, a_) for k_, a_ in avg.items() if not k_.startswith('SK')), key=lambda kv: (kv[1]['r2'] if kv[1]['r2'] == kv[1]['r2'] else -9))   # SK pairs reported, excluded: the 178 cm Skarn diagnostic is far from every body (t ~ 1 for any non-Skarn)
    body = dict(rows=rows, source_protection=prot, signal_vs_MF_by_group={g: len(x) for g, x in sig.items()}, signal_keys_vs_MF=sig, groups_with_signal_vs_MF=sum(1 for x in sig.values() if x),
                nearest_count={s: sum(1 for k in KEYS if rows[k]['nearest'] == s) for s in SRC}, arithmetic_average_audit=avg,
                scalar_blend_firewall=dict(best_pair=best[0], best_r2=best[1]['r2'], best_alpha=best[1]['alpha'], passes=bool(not (best[1]['r2'] >= 0.8 and best[1]['n'] >= 8))),
                distinct_from_elves={s: prot[s]['material'] >= 6 for s in ELF})
    # face (ears excluded): aligned onto the candidate head
    D = F.load(pre + '_r6.npz'); Vh = D['V']; HH = F.descriptors(Vh)['head_height_cm']; hd = F.HEAD; maps = {s: F.procrustes(SD[s]['V'][hd], Vh[hd]) for s in SRC}; fsm = F.procrustes(SD['SG']['V'][hd], SD['MF']['V'][hd])
    face = {}
    for r, msk in F.REG.items():
        rm = lambda X, Y: float(np.sqrt((np.linalg.norm(X[msk] - Y[msk], axis=1) ** 2).mean()) * 10)
        x = {s: rm(Vh, maps[s](SD[s]['V'])) for s in SRC}; sm = rm(SD['MF']['V'], fsm(SD['SG']['V'])); thr = max(0.005 * HH * 10, 3 * sm, 0.3)
        face[r] = dict(**{'vs_%s_mm' % s: round(y, 2) for s, y in x.items()}, human_baseline_mm=round(sm, 2), threshold_mm=round(thr, 2), departs_from_MF=bool(x['MF'] > thr),
                       distinct_from={s: bool(x[s] > thr) for s in ELF}, nearest=min(x, key=x.get))
    dd = desc(Vh, m); dk = [k for k in sorted(dd) if k in SDES['MF'] and isinstance(dd[k], (int, float))]
    descs = {}
    for k in dk:
        h = np.mean([SDES[s][k] for s in ('MF', 'SG')]); e = np.mean([SDES[s][k] for s in ELF]); gap = e - h
        descs[k] = dict(HV=round(dd[k], 4), MF=round(SDES['MF'][k], 4), elf_mean=round(e, 4), HV_vs_MF_pct=round(pct(dd[k], SDES['MF'][k]), 2), position_human0_elf1=round((dd[k] - h) / gap, 3) if abs(gap) > 1e-9 else None,
                        departs_from_MF=bool(abs(pct(dd[k], SDES['MF'][k])) >= 1.0), **{'vs_%s_pct' % s: round(pct(dd[k], SDES[s][k]), 2) for s in ELF})
    ab = {k: descs[k]['HV_vs_MF_pct'] for k in ('eye_aperture_area_over_HH2', 'jaw_width_over_bizygomatic', 'lower_face_height_over_HH', 'lower_face_width_over_bizygomatic', 'nose_width_over_bizygomatic', 'nose_length_over_HH') if k in descs}
    fr = dict(regions=face, regions_departing_from_MF=sum(v_['departs_from_MF'] for v_ in face.values()), regions_of=len(face),
              regions_distinct_from={s: sum(v_['distinct_from'][s] for v_ in face.values()) for s in ELF}, descriptors=descs, descriptors_departing_from_MF=sum(v_['departs_from_MF'] for v_ in descs.values()),
              anti_beauty_indicators_vs_MF_pct=ab)
    res['items'][item] = dict(prefix=pre, stature=m['stature'], body=body, face=fr)
    print(item, CFG, 'stat %.2f' % m['stature'], '| mat', {s: prot[s]['material'] for s in SRC}, '| sig groups %d' % body['groups_with_signal_vs_MF'], {g: n for g, n in body['signal_vs_MF_by_group'].items()},
          '| blend', body['scalar_blend_firewall'], '| face dep %d/%d' % (fr['regions_departing_from_MF'], fr['regions_of']), 'distinct', fr['regions_distinct_from'], 'desc %d' % fr['descriptors_departing_from_MF'], '| ab', ab)
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))

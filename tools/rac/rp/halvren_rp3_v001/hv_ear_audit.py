# hv_ear_audit.py DOMAINS.json OUT.json : Halvren mixed-ear order §17 EAR-ONLY FIREWALL and §18 ARITHMETIC-AVERAGE EAR FIREWALL on the measured ear-domain
# coordinates (hv_ear_domains.py; one common Halvren head, one root frame, identical rule for the Marchfolk human auricle and every branch ear).
# Normalisation: each domain / its pooled standard deviation over the four sources (MF, FN, AE, VA), floored at the measurement resolution (hv_ear_domains.FLOOR).
#   midpoint audit, per Halvren ear x pair (MF-FN, MF-AE, MF-VA): domains where the pair differs by > 0.5 SD; position t = (HV - MF) / (E - MF);
#     near-midpoint count (|t - 0.5| <= 0.15), outside-pair count (t < 0 or > 1); single-alpha fit HV - MF = alpha (E - MF) on the normalised
#     coordinates, R^2 = 1 - |res|^2 / |HV - MF|^2. FAIL if any pair has R^2 >= 0.8 with >= 6 domains ("well explained by one alpha").
#   ear-only firewall: HE1 not 'Marchfolk + tip' (>= 3 domains outside length / upward extension / tip angle depart from MF by > 0.5 SD);
#     HE3 / diagnostics not a source duplicate (>= 4 domains differ by > 0.5 SD from every frozen elf, and nearest-source RMS distance > 0.5 SD);
#     family coherence (HE1 < HE2 < HE3 on the composite elf-ward score; >= 2 domains non-monotone across HE1 -> HE3, i.e. not lockstep).
# Also the DESIGN-PARAMETER audit (same rules) on the authored domain parameters (W1 MF-human / frozen elf parameters vs the HE definitions).
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'); import ear_branch_lib as E
IN, OUT = sys.argv[1:3]; d = json.load(open(IN)); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001'); import hv_ear_domains as HD; FL = HD.FLOOR; FLM = dict(HD.FLOOR); DOM = d['domains']; I = d['items']; SRC = ['MF', 'FN', 'AE', 'VA']; ELF = ['FN', 'AE', 'VA']
PFL = dict(L=0.2, wb=0.05, taper_start=0.03, taper_ex=0.05, shoulder=0.02, lobe=0.01, proj=2.0, tilt=2.0, sweep=0.1, concha=0.02, trag=0.01, helix_h=0.01)
def audit(I, DOM, tag):
    X = {k: np.array([I[k][q] for q in DOM], float) for k in I}; S = np.array([X[s] for s in SRC]); sd = np.maximum(S.std(0), np.array([FL.get(q, 1e-9) for q in DOM]))
    Z = {k: v / sd for k, v in X.items()}; res = dict(kind=tag, domains=DOM, pooled_sd=dict(zip(DOM, sd.round(5).tolist())), items={})
    HV = [k for k in I if k not in SRC]
    for h in HV:
        r = dict(midpoint={}, distance={}); y0 = Z[h] - Z['MF']
        for e in ELF:
            dx = Z[e] - Z['MF']; m = np.abs(dx) > 0.5; t = y0[m] / dx[m]; x = dx[m]; y = y0[m]; a = float(x @ y / (x @ x)); rr = y - a * x; r2 = float(1 - rr @ rr / (y @ y)) if y @ y > 0 else float('nan')
            r['midpoint']['MF-' + e] = dict(n=int(m.sum()), t={q: round(float(v), 3) for q, v in zip(np.array(DOM)[m], t)}, near_midpoint=int(np.sum(np.abs(t - 0.5) <= 0.15)),
                                          outside_pair=int(np.sum((t < 0) | (t > 1))), t_median=round(float(np.median(t)), 3), alpha=round(a, 3), r2=round(r2, 3))
        for s in SRC:
            dz = Z[h] - Z[s]; r['distance'][s] = dict(rms_sd=round(float(np.sqrt(np.mean(dz ** 2))), 3), domains_gt_half_sd=int(np.sum(np.abs(dz) > 0.5)),
                                                     differing=[q for q, v in zip(DOM, dz) if abs(v) > 0.5])
        best = max(r['midpoint'].items(), key=lambda kv: kv[1]['r2']); r['scalar_fit'] = dict(best_pair=best[0], best_r2=best[1]['r2'], best_alpha=best[1]['alpha'],
                                                                                         passes=bool(not (best[1]['r2'] >= 0.8 and best[1]['n'] >= 6)))
        r['nearest_source'] = min(SRC, key=lambda s: r['distance'][s]['rms_sd'])
        r['distinct_from_every_elf'] = bool(all(r['distance'][e]['domains_gt_half_sd'] >= 4 for e in ELF) and min(r['distance'][e]['rms_sd'] for e in ELF) > 0.5)
        mfx = [q for q in r['distance']['MF']['differing'] if q not in ('length_over_HH', 'upward_ext_over_HH', 'tip_angle_deg', 'L', 'taper_start', 'taper_ex')]
        r['not_MF_plus_tip'] = dict(non_tip_domains_departing_MF=mfx, passes=len(mfx) >= 3)
        res['items'][h] = r
    # composite elf-ward score: mean over domains of the position between MF (0) and the elf mean (1), sign-aligned
    em = np.mean([Z[e] for e in ELF], 0); dv = em - Z['MF']; m = np.abs(dv) > 0.5
    comp = {h: round(float(np.mean((Z[h][m] - Z['MF'][m]) / dv[m])), 3) for h in HV}; res['composite_elfward'] = comp
    if all(k in I for k in ('HE1', 'HE2', 'HE3')):
        P = np.array([Z[k] for k in ('HE1', 'HE2', 'HE3')]); mono = [(P[0, i] <= P[1, i] <= P[2, i]) or (P[0, i] >= P[1, i] >= P[2, i]) for i in range(len(DOM))]
        res['family'] = dict(composite_order_ok=bool(comp['HE1'] < comp['HE2'] < comp['HE3']), non_monotone_domains=[q for q, mo in zip(DOM, mono) if not mo],
                             lockstep=bool(sum(not x for x in mono) < 2), position_per_domain={q: [round(float((P[j, i] - Z['MF'][i]) / (dv[i] if abs(dv[i]) > 1e-9 else 1)), 2) for j in range(3)] for i, q in enumerate(DOM)})
    return res
R = dict(order='chatgpt-rac-rp3-halvren-central-accept-ear-architecture-order §17 / §18', measured=audit(I, DOM, 'measured ear-domain coordinates (hv_ear_domains.py)'))
# design parameters (authored): MF-human = W1 v2 reference (rounded top: taper start = its rounding start 0.55, exponent 0.5 ~ circular, no shoulder term)
PD = ['L', 'wb', 'taper_start', 'taper_ex', 'shoulder', 'lobe', 'proj', 'tilt', 'sweep', 'concha', 'trag', 'helix_h']
def pv(p): t = p['taper']; return dict(L=p['L'], wb=p['wb'], taper_start=t[1], taper_ex=t[2], shoulder=t[3] if len(t) > 3 else 0.0, lobe=p['lobe'], proj=p['proj'], tilt=p['tilt'], sweep=p['sweep'],
                                       concha=p['concha'], trag=p['trag'], helix_h=p['helix'][0])
MFH = dict(L=6.4, wb=1.75, taper_start=0.55, taper_ex=0.5, shoulder=0.0, lobe=0.18, proj=22, tilt=12, sweep=0.4, concha=0.85, trag=0.30, helix_h=0.30)
PI = {'MF': MFH, 'FN': pv(E.CAND['E2']), 'AE': pv(E.CAND['AE-E2']), 'VA': pv(E.CAND['VA-E2-RI3'])}
for k in I:
    if k not in SRC and k in E.CAND: PI[k] = pv(E.CAND[k])
FL = PFL; R['design_parameters'] = audit(PI, PD, 'authored domain parameters (ear_branch_lib.CAND)'); R['design_parameters']['values'] = PI
mp = R['measured']['items']
# topology control: Marchfolk-PARAMETER ears (W1 MF-human values) realized on the shared engineering topology -- where the topology's human end sits
Xc = {k: np.array([I[k][q] for q in DOM], float) for k in I}; emx = np.mean([Xc[e] for e in ELF], 0); dvx = emx - Xc['MF']
sdx = np.maximum(np.array([Xc[s] for s in SRC]).std(0), np.array([FLM.get(q, 1e-9) for q in DOM])); sig = np.abs(dvx) > 0.5 * sdx
R['topology_control'] = {k: dict(t_vs_elf_mean={q: round(float(v), 2) for q, v in zip(DOM, (Xc[k] - Xc['MF']) / np.where(sig, dvx, 1)) if sig[DOM.index(q)]},
                                 median_t=round(float(np.median(((Xc[k] - Xc['MF']) / np.where(sig, dvx, 1))[sig])), 2)) for k in I if k.startswith('CTRL')}
R['gates'] = dict(HE2_not_scalar_blend_measured=mp['HE2']['scalar_fit']['passes'] if 'HE2' in mp else None,
                  HE2_not_scalar_blend_design=R['design_parameters']['items']['HE2']['scalar_fit']['passes'] if 'HE2' in R['design_parameters']['items'] else None,
                  all_HE_not_scalar_blend_measured=all(mp[k]['scalar_fit']['passes'] for k in mp if k.startswith('HE')),
                  HE1_not_MF_plus_tip=mp['HE1']['not_MF_plus_tip']['passes'] if 'HE1' in mp else None,
                  HE3_not_source_duplicate=mp['HE3']['distinct_from_every_elf'] if 'HE3' in mp else None,
                  diagnostics_remain_halvren={k: mp[k]['distinct_from_every_elf'] for k in mp if k.startswith('HV-D')},
                  family_coherent=bool(R['measured'].get('family', {}).get('composite_order_ok') and not R['measured'].get('family', {}).get('lockstep', True)))
json.dump(R, open(OUT, 'w'), indent=1)
for k, v in mp.items(): print(k, 'best', v['scalar_fit'], 'nearest', v['nearest_source'], 'distinct', v['distinct_from_every_elf'], 'notMF+tip', v['not_MF_plus_tip']['passes'])
print('composite', R['measured']['composite_elfward']); print('family', R['measured'].get('family', {}).get('non_monotone_domains')); print('gates', R['gates'])

# RAC W3B scale-field envelope evaluation: re-applies the diagnostic guards (w3b_scale_run header) to the stored sweep metrics, adds the
# relief side of the hierarchy (a structural field's relief must stay >= the relief of the finer fields it borders), the floor tolerance
# (3 %), the GENERATOR-LIMIT resolution guard S7 (unit >= 1.7 mean surface edges of the upsampled W2 mesh, or the field's own canonical
# resolution when already finer - plantar 1.57, palmar 1.73 edges), and brackets each
# field's valid SIZE and RELIEF multiplier interval (first demonstrated invalid points + limiting guard). Writes scratch w3b/scale/envelope.json
import os, sys, json, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_regions as RG
CAN = json.load(open(C.W + '/scale_canon_metrics.json'))
def edges():
    p = C.W + '/scale_field_edge.json'
    if os.path.exists(p): return json.load(open(p))
    import w3b_scale as SC
    Z = SC.ref(); V = Z['Vu']; F = Z['Fu']; out = {}
    for k, m in RG.masks().items():
        core = SC.weight(m) >= 0.9; f = F[core[F].all(1)]
        out[k] = float(np.mean(np.linalg.norm(V[f[:, 0]] - V[f[:, 1]], axis=1)))
    json.dump(out, open(p, 'w'), indent=1); return out
EDGE = edges()
FLOOR = min(v['relief_cm'] for v in CAN.values())
def regrade(x):
    k = x['region']; g = dict(x['guards']); fm = x['metrics']
    if fm.get('size_cm') is None: return {'S0_units': False}
    if 'folds_canonical' in x['values']: g['S4_topology'] = x['values']['flips'] <= max(2, 0.10 * x['values']['folds_canonical'])
    else: g['S4_topology'] = x['values']['flips'] <= 2                   # legacy rows (new-face count; only kept where S4 did not bind)
    g['S3_floor'] = fm['relief_cm'] >= 0.97 * FLOOR                       # 3 % tolerance: reseed noise on the floor field (mouth margin)
    g["S7_resolution"] = fm["size_cm"] >= 0.95 * min(1.7, CAN[k]["size_cm"] / EDGE[k]) * EDGE[k]       # 5 % reseed tolerance
    g["S3_aspect"] = fm["aspect"] <= max(0.30, 1.05 * CAN[k]["aspect"])                                       # 5 % reseed tolerance                     # GENERATOR LIMIT: a unit must span >= 1.7 mean surface edges (finest canonically expressed field: palmar 1.73)
    finer = [j for j, a in RG.ADJ.items() if a == k]
    if finer:
        g['S2_relief_hierarchy'] = fm['relief_cm'] >= max(CAN[j]['relief_cm'] for j in finer) - 1e-9
    return g
def bracket(rows, key):
    rows = sorted(rows, key=lambda r: r[key]); ok = [r for r in rows if r['ok']]
    if not ok: return None
    ref = [r for r in rows if abs(r[key] - 1.0) < 1e-9]
    # contiguous valid interval containing 1.0
    i0s = [i for i, r in enumerate(rows) if abs(r[key] - 1.0) < 1e-9]
    if not i0s: return None
    i0 = i0s[0]; lo = hi = i0
    if not rows[i0]['ok']: return {"valid": None, "note": "reference itself fails: " + ','.join(rows[i0]['fails'])}
    while lo - 1 >= 0 and rows[lo - 1]['ok']: lo -= 1
    while hi + 1 < len(rows) and rows[hi + 1]['ok']: hi += 1
    f_lo = rows[lo - 1] if lo - 1 >= 0 else None; f_hi = rows[hi + 1] if hi + 1 < len(rows) else None
    return {"min_valid": rows[lo][key], "max_valid": rows[hi][key], "min_valid_abs": rows[lo]['abs'], "max_valid_abs": rows[hi]['abs'],
            "first_invalid_low": (f_lo[key], f_lo['fails']) if f_lo else "not reached", "first_invalid_high": (f_hi[key], f_hi['fails']) if f_hi else "not reached (max tested)"}
if __name__ == '__main__':
    R = {}
    for f in ('results.json', 'results_sizebody.json'):
        if os.path.exists(C.W + '/scale/' + f): R.update(json.load(open(C.W + '/scale/' + f)))
    env = {}
    for k in CAN:
        rel = [dict(r=x['r'], abs=x['metrics'].get('relief_cm'), ok=all(regrade(x).values()), fails=[a for a, b in regrade(x).items() if not b]) for t, x in R.items() if x['region'] == k and x['s'] == 1.0 and not x.get('reseeded') and x['rng'] == 7]
        siz = [dict(s=x['s'], abs=x['metrics'].get('size_cm'), ok=all(regrade(x).values()), fails=[a for a, b in regrade(x).items() if not b]) for t, x in R.items() if x['region'] == k and x.get('reseeded') and x['r'] == 1.0 and x['rng'] == 7]
        env[k] = {"class": [c for c, ks in RG.CLASS.items() if k in ks][0], "reference": {"size_cm": CAN[k]['size_cm'], "relief_cm": CAN[k]['relief_cm'], "aspect": CAN[k]['aspect'], "span_deg": CAN[k]['span_deg']},
                  "relief": bracket(rel, 'r') if rel else None, "size": bracket(siz, 's') if siz else None}
        e = env[k]; print(k, 'RELIEF', None if not e['relief'] else (e['relief'].get('min_valid'), e['relief'].get('max_valid'), e['relief'].get('first_invalid_low'), e['relief'].get('first_invalid_high')),
                          '| SIZE', None if not e['size'] else (e['size'].get('min_valid'), e['size'].get('max_valid'), e['size'].get('first_invalid_low'), e['size'].get('first_invalid_high')))
    json.dump(env, open(C.W + '/scale/envelope.json', 'w'), indent=1)

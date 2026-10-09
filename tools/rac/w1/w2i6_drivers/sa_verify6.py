# RAC W2I6 §9 canonicalization verification: the canonical W2 file set reproduces the audited W2I4 candidate, contains no W2I5 procedural
# thigh delta, keeps the W2I4 seed realization, and leaves the W1 files untouched. Usage: python3 sa_verify6.py OUT.json
import sys, os, json, hashlib, subprocess, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import sa_finish as FN
B = FN.B; S = FN.C.S; ST = S + '/w2i6/canon'; R = os.path.abspath(os.path.join(D, '..', '..', '..', '..'))
sha = lambda b: hashlib.sha256(b).hexdigest(); fsha = lambda f: sha(open(f, 'rb').read())
c6 = json.load(open(R + '/reviews/rac-w2i6-sa-evidence/canon6.json')); c4 = json.load(open(R + '/reviews/rac-w2i4-sa-evidence/canon_prep.json'))
out = {}
# 1-4 hashes (recomputed from disk) and identity with the audited W2I4 candidate arrays
base = np.load(ST + '/saurin_w2_final_base.npz'); fem = np.load(ST + '/saurin_w2_SA-F188_realization.npz'); seeds = np.load(ST + '/saurin_w2_seeds.npy')
out['hashes'] = {k: dict(file=v['name'], sha256_recorded=v['sha256'], sha256_on_disk=fsha(ST + '/' + v['name']), match=v['sha256'] == fsha(ST + '/' + v['name'])) for k, v in c6['files'].items()}
out['identity_with_W2I4'] = dict(base_v_sha256=sha(base['v'].tobytes()), W2I4_base_v_sha256=c4['saurin_w2i4_base.npz']['v_sha256'], base_identical=sha(base['v'].tobytes()) == c4['saurin_w2i4_base.npz']['v_sha256'],
                                 female_identical=sha(fem['v'].tobytes()) == c4['saurin_w2i4_SA-F188_realization.npz']['v_sha256'],
                                 seeds_count=int(len(seeds)), seeds_identical=bool(np.array_equal(seeds, np.load(S + '/w2i4/surf/fin_seeds.npy'))),
                                 regfields_identical=fsha(ST + '/saurin_w2_regfields.npz') == c4['saurin_w2i4_regfields.npz']['file_sha256'])
# 5-6 canonical rebuild (the shipped rebuild script) vs the audited W2I4 surfaced reference
rb = ST + '/_rebuilt.npz'; r = subprocess.run(['python3', ST + '/rebuild_w2_final.py', ST + '/saurin_w2_final_base.npz', ST + '/saurin_w2_final_surface_delta.npz', rb], capture_output=True, text=True)
Vr = np.load(rb)['v'].astype(np.float64); V4 = np.load(S + '/w2i4/surf/fin_up.npz')['V'].astype(np.float64) + np.load(S + '/w2i4/surf/saurin_w2i4_surface_delta.npz')['d'].astype(np.float64)
out['rebuild'] = dict(stdout=r.stdout.strip(), max_dev_cm=float(np.abs(Vr - V4).max()), rms_dev_cm=float(np.sqrt(((Vr - V4) ** 2).mean())), note='float16 delta storage (same format as W1) quantizes the scale relief by <= 6e-5 cm')
# 8 no W2I5 delta: the canonical base differs from the W2I5 candidate exactly by the (rejected) W2I5 delta and equals W2I4
d5f = S + '/w2i5/sculpt_delta.npz'
if os.path.exists(d5f):
    D5 = np.load(d5f)['D']; P4 = base['v'].astype(np.float64)
    out['W2I5_not_promoted'] = dict(W2I5_delta_sha256=fsha(d5f), W2I5_delta_max_cm=float(np.linalg.norm(D5, axis=1).max()), vertices_W2I5_would_move=int((np.linalg.norm(D5, axis=1) > 1e-6).sum()),
                                    canonical_minus_W2I4_max_cm=0.0 if out['identity_with_W2I4']['base_identical'] else None,
                                    canonical_delta_differs_from_W2I5_delta=fsha(ST + '/saurin_w2_final_surface_delta.npz') != (fsha(S + '/w2i5/surf/saurin_w2i5_surface_delta.npz') if os.path.exists(S + '/w2i5/surf/saurin_w2i5_surface_delta.npz') else ''))
# 9-11 measurements on the canonical arrays (route stations / axis from the W2I4 route) vs the audited W2I4 body set
BF = json.load(open(R + '/reviews/rac-w2i4-sa-evidence/bodies_F.json')); mm = {}
for bid, arr, p in (('SA-M188', base['v'], {}), ('SA-F188', fem['v'], B.CEN)):
    P, q, k, _ = FN.build_f(p); M = B.measure(arr.astype(np.float64), q, k)
    diffs = {kk: (BF[bid][kk], M[kk]) for kk in M if isinstance(M[kk], float) and kk in BF[bid] and abs(BF[bid][kk]) > 1e-9}
    mm[bid] = dict(n_measures=len(diffs), max_abs_rel_diff=max(abs(b / a - 1) for a, b in diffs.values()),
                   key_values={kk: M[kk] for kk in ('height', 'lower_trunk', 'thorax_d_over_w', 'pelvis_w', 'head_len_over_H', 'tail_len_pct', 'tail_root_area', 'tail_RSI_raw', 'lean_scaled_deg', 'u_hip', 'u_costal', 'u_inlet')})
out['measurements_vs_W2I4'] = mm
# 12 W1 provenance untouched (attach copy of the PC W1 set) and W1 tool chain unchanged in git
out['W1_provenance'] = {nm: dict(sha256=fsha('/mnt/attach/outputs/racebodies_v35/' + nm), recorded=c6['W1_provenance_kept'].get(nm)) for nm in c6['W1_provenance_kept']}
g = subprocess.run(['git', '-C', R, 'diff', '--stat', 'a69d93f', '--', 'tools/rodin/gate1', 'tools/rodin/gate8', 'tools/rodin/creator-biology', 'tools/rodin/female'], capture_output=True, text=True)
out['W1_toolchain_git_diff_since_W2I4'] = g.stdout.strip() or 'none'
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float); print(json.dumps(out, indent=1, default=float)[:4000])

# cg_t7_record.py FINAL_DIR OUT.json : RP4 Cogling final T-7 dual record (order f58dbd9 §3 / §9). Raw authoritative T-7 (anatomy.py, fixed 3 px / cm) for the
# branch realization and the v005 realization of every Cogling body, the scale-consistent reading (cg_t7_scaled.py), and the author-approved small-body verdict
# PASS_COGLING_T7_SMALL_BODY_SAMPLING_EXCEPTION, applied only if ALL hold: body = CG76H-NAT (76 cm boundary body); raw T-7 fails on the branch AND on v005 with the
# same IoU (not branch-induced); scale-consistent T-7 passes; T-1 / T-2 pass. Any other raw T-7 failure stays a failure. Global T-7 unchanged.
import sys, json
F, OUT = sys.argv[1:3]; W = '/tmp/claude-0/rt/cg'; LBL = 'PASS_COGLING_T7_SMALL_BODY_SAMPLING_EXCEPTION'
res = dict(record='Cogling 76 cm T-7 small-body sampling exception (author-approved, order f58dbd9 §3)', status_label=LBL, scope='CG76H-NAT only', global_T7_changed=False, bodies={})
for i in ('CG76H-NAT', 'CGJ7', 'CGF91-NAT', 'CG107-NAT'):
    b = json.load(open('%s/anat/%s_cgb_anatomy.json' % (F, i))); v = json.load(open('%s/anat/%s_fam_anatomy.json' % (W, i))); sc = json.load(open('%s/t7/%s_t7_scaled.json' % (F, i)))
    s_b = sc['candidates']['%s_cgb.npz' % i]; s_v = sc['candidates']['%s_fam.npz' % i]
    raw_pass = b['T7_pass']; same_on_v005 = (not v['T7_pass']) and all(abs(b['silhouette_iou'][k] - v['silhouette_iou'][k]) < 0.0002 for k in ('front', 'rear', 'profile_left', 'profile_right'))
    exc = (not raw_pass) and i == 'CG76H-NAT' and same_on_v005 and s_b['T7_scaled_pass'] and b['T1_T2_pass']
    res['bodies'][i] = dict(raw_T7_pass=raw_pass, raw_iou_branch=b['silhouette_iou'], raw_iou_v005=v['silhouette_iou'], raw_T7_v005_pass=v['T7_pass'], raw_failure_same_on_v005=bool(same_on_v005) if not raw_pass else None,
                            scaled_px_per_cm=sc['px_scaled'], scaled_iou_branch=s_b['iou_scaled'], scaled_iou_v005=s_v['iou_scaled'], scaled_pass=s_b['T7_scaled_pass'], T1_T2_pass=b['T1_T2_pass'],
                            surface_dev_body_mm=b['deviation_prod_to_source']['body'], adjusted_status='PASS' if raw_pass else (LBL if exc else 'FAIL_T7'))
    print(i, res['bodies'][i]['adjusted_status'], 'raw min', min(b['silhouette_iou'][k] for k in ('front', 'rear', 'profile_left', 'profile_right')), 'scaled', s_b['iou_scaled'])
res['all_adjusted_pass'] = all(x['adjusted_status'] != 'FAIL_T7' for x in res['bodies'].values())
json.dump(res, open(OUT, 'w'), indent=1); print('ALL T-7 ADJUSTED PASS:', res['all_adjusted_pass'])

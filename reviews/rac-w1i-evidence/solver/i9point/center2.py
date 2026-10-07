# RAC W1i post-solve centering probe C2: move each value toward the side its +/-2 % sensitivity shows to be safe (sensitivity_w1i.json
# of the I9 point), half a step (1 %), then evaluate with the ordinary rule on the reference + stature series + cross pairs (sens6.evaluate)
import sys, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1i_drivers'); import sens6, gn6
x0 = json.load(open(sys.argv[1]))["x"]; mv = {"pelvisX": 1.01, "pelvisY": 1.01, "pelvisZ": 1.01, "clavY": 0.99, "s03Y": 1.005, "kb18": 0.99, "kb31": 0.99, "thorX": 1.003}
x = [v * mv.get(n, 1.0) for n, v in zip(gn6.NAMES, x0)]
r = sens6.evaluate(x, 'C2'); r["x"] = x; r["moves"] = mv
json.dump(r, open(sys.argv[2], 'w'), indent=1, default=float)
print('not_pass', {k: v for k, v in r['not_pass'].items() if v}, 'TB %.2f' % (100 * r['skin_TB_vs_SK']), 'flare %.4f' % r['flank_flare'], 'clr %.2f' % r['arm_clearance_cm'], 'waist %.4f' % r['low_comp_waist_rise'], r['skeleton'])

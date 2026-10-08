# W2G probe HVXAEc (REPORT, not applied): HVXAE with the three measures whose reading response ran past / against Aelari 178 bounded in READING space
# (neck-height target 0.30 -> 0.10; wrist circumference decrease kept at HVC1's 0.15; upper-leg height 0.125 -> 0.06). Diagnostic only.
import sys, json; sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w2g_drivers'); sys.argv = ['x', 'none']
import hv_build as H
t = H.expr_targets("AE"); t.update({"measure-neck-height-incr": 0.1, "measure-wrist-circ-decr": 0.15, "measure-upperleg-height-incr": 0.06})
H.variant(H.HVB, {"targets": t, "resolve_stature": True, "stature": 178.0}, H.W + '/probe', 'HVXAEc')

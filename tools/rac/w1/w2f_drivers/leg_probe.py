# RAC W2F diagnostic probes (NOT applied; for the author ruling): Aelari lower-limb target strength and Vael lower-leg target, at matched heights.
# AEPxxx_h = Aelari with its own upper-leg / lower-leg height targets scaled by xxx/100 (foot unchanged), stature re-solved to h;
# VAP0_h = Vael with its own lower-leg decrease target removed, stature re-solved to h.   Usage: python3 leg_probe.py
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import el_build as B
from concurrent.futures import ThreadPoolExecutor
if len(sys.argv) == 1:
  J = []
  for f in (1.75, 2.0, 2.5):
      for h in (173, 190, 203):
        J.append((B.variant, (B.BASE["AE"], {"targets": B.scaled("AE", ("measure-upperleg-height-incr", "measure-lowerleg-height-incr"), f), "resolve_stature": True, "stature": float(h)}, B.W + '/probe', 'AEP%d_%d' % (round(f * 100), h))))
  for h in (178, 190):
    J.append((B.variant, (B.BASE["VA"], {"targets": {"measure-lowerleg-height-decr": None}, "resolve_stature": True, "stature": float(h)}, B.W + '/probe', 'VAP0_%d' % h)))
  with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
  print('PROBES_DONE')
# second set (run with argv[1] == 'route'): native-route cross-checks where the re-solved macro falls in the generator's short-femur zone,
# and the FN-09 strength probe x0.75
if len(sys.argv) > 1 and sys.argv[1] == 'route':
    J = []
    for r, h in (("AE", 173), ("FN", 163), ("VA", 163)):
        c = dict(B.cfg(B.BASE[r])); c.update(stature=float(h), id="%s%dN" % (r, h), base_height_macro=json.load(open(B.BASE[r]))["height_macro"])
        J.append((B.native, (c, B.W + '/rt', '%s%dN' % (r, h))))
    J.append((B.variant, (B.BASE["FN"], {"targets": B.scaled("FN", ("measure-upperarm-length-incr", "measure-lowerarm-length-incr", "measure-upperleg-height-incr", "measure-lowerleg-height-incr"), 0.75), "resolve_stature": True, "stature": 181.0}, B.W + '/nm', 'FN09x75')))
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
    print('ROUTE_DONE')

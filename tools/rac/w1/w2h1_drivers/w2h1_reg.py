# RAC W2H1 registry: the W2H registry (w2h_drivers/w2h_reg.py) with every Durrim body replaced by its D1-corrected rebuild (pelvis bone Z x1.04;
# w2h1_drivers/du_d1.py) under the SAME name, and the uncorrected W2H Durrim bodies kept under '<name>-W2H' as the BEFORE state.
# Usage: python3 w2h1_reg.py OUT.json
import sys, json, os, subprocess
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2h1'; T = '/home/claude/wayfarer-design/tools/rac/w1'
tmp = W + '/reg_w2h.json'; subprocess.run(['python3', T + '/w2h_drivers/w2h_reg.py', tmp], check=True, capture_output=True); R = json.load(open(tmp))
G = lambda n: W + '/g/%s/skp' % n
NEW = {"DU122": (W + '/st/DU122C-NAT', G("DU122C-NAT"), "DU122C-NAT"), "DU137": (W + '/st/DU137C-NAT', G("DU137C-NAT"), "DU137C-NAT"),
       "DU152": (W + '/st/DU152C-NAT', G("DU152C-NAT"), "DU152C-NAT"), "DUNLOW": (W + '/nm/DUNLOWC', G("DUN137C"), "DUNLOWC")}
for t in ("N", "B"):
    for h in (122, 137, 152): NEW["DU%s%d" % (t, h)] = (W + '/fr/DU%s%dC' % (t, h), G("DU%s%dC" % (t, h)), "DU%s%dC" % (t, h))
for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN"): NEW["DU137-" + c] = (W + '/comp/DU137C-' + c, G("DU137C-NAT"), "DU137C-" + c)
for c in ("LOW", "MIN", "HIBOTH"): NEW["DU152-" + c] = (W + '/p4/DU152C-' + c, G("DU152C-NAT"), "DU152C-" + c)
for k, (meas, grid, joint) in NEW.items():
    old = dict(R[k]); old["race"] = None; R[k + "-W2H"] = old          # BEFORE (uncorrected W2H body), no slot rows
    R[k] = {"meas": meas, "skp": grid, "skp_id": "MF-M-R", "joint": joint, "race": "DU"}
json.dump(R, open(sys.argv[1], 'w'), indent=1); print(len(R), "bodies")

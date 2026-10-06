# RAC W1h driver: Aelari vertical budget (AD-W1H-5). Recomputes the budget rows from the "current" shares in
# ae_vertical_budget.json (read from the W1g AE / VA / FN / MF measurements), checks them against the stored rows, and adds the
# largest uniform margin reachable at the current remaining share (head above neck_01 + suprasternal-to-neck_01 offset).
# Relations (AD-G10 1 % convention): AE leg >= 1.01 VA leg, VA leg >= 1.01 MF leg, AE torso >= 1.01 FN torso, AE neck >= 1.01 MF neck;
# AE leg + torso + neck + remaining = 1.  Usage: python3 ae_budget.py ae_vertical_budget.json
import sys, json
from scipy.optimize import brentq
p = sys.argv[1]; d = json.load(open(p)); c = d["current"]
def mins(m):
    k = 1.01 * (1 + m); va = c["MF_leg"] * k
    return {"AE_leg_min": va * k, "VA_leg_min": va, "AE_torso_min": c["FN_torso"] * k, "AE_neck_min": c["MF_neck"] * k}
for r in d["rows"]:
    q = mins(r["margin_over_each_1pct_threshold"]); rem = 1 - q["AE_leg_min"] - q["AE_torso_min"] - q["AE_neck_min"]
    assert abs(rem - r["max_remaining_share_head_and_neck_base"]) < 1e-9 and abs(rem / c["remaining_share"] - 1 - r["change_vs_current_remaining_share"]) < 1e-9, r
f = lambda m: 1 - sum(v for k, v in mins(m).items() if k != "VA_leg_min") - c["remaining_share"]
d["max_uniform_margin_at_current_remaining_share"] = brentq(f, -0.01, 0.05)
d["current_margins"] = {"AE_leg_over_VA": c["AE_leg"] / c["VA_leg"] / 1.01 - 1, "VA_leg_over_MF": c["VA_leg"] / c["MF_leg"] / 1.01 - 1,
                        "AE_torso_over_FN": c["AE_torso"] / c["FN_torso"] / 1.01 - 1, "AE_neck_over_MF": c["AE_neck"] / c["MF_neck"] / 1.01 - 1}
json.dump(d, open(p, "w"), indent=1); print("rows verified; max uniform margin %.5f" % d["max_uniform_margin_at_current_remaining_share"], d["current_margins"])

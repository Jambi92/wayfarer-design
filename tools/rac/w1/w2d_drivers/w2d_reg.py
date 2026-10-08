# RAC W2D (Gorrund W2) body registry: every Gorrund body built in this pass (w2d_drivers/go_body.py, go_comp.py) and the accepted comparator
# bodies (Grask W2C, Skarn W2B with the W2C1 knee revert at 229 cm, Broad Skarn 208 / 218 / 229, Marchfolk W1 / W2A). Joint keys point at
# exact-plane joint sections (w2c1_drivers/joint_section.py output). Writes REGISTRY.json.   Usage: python3 w2d_reg.py OUT.json
import sys, json, os
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
W2C = json.load(open(S + '/w2c/registry.json'))
R = {}
GO = ["GO208", "GO218", "GO229", "GOREF", "GO239", "GO251", "GON5", "GOB7", "GON5_218", "GOB7_218", "GOD14_9", "GOD14_9_218", "GOLP218",
      "GON", "GONF", "GOB", "GOBF", "GON3", "GON4", "GOB3", "GOB4", "GOB5", "GOB6", "GON3_218", "GON4_218"]
for n in GO:
    d = S + '/w2d/b/' + n
    R[n] = {"meas": d + '/' + n, "skp": d + '/skp_' + n, "skp_id": n, "joint": n, "gorrund": True, "dir": d}
for n in ["GOR-BODY-06", "GOR-BODY-07", "GOR-BODY-08", "GOR-BODY-09", "GOR-BODY-10", "GOR-BODY-11", "GOR-BODY-16"] + \
         ["GOR-BODY-%s_%s" % (c, h) for h in ("208", "218") for c in ("06", "07", "09", "10", "16")]:
    d = S + '/w2d/b/' + n
    R[n] = {"meas": d + '/' + n, "skp": None, "joint": n, "gorrund": True, "comp": True, "dir": d}
JK = {"SK198": "SKM198", "SK218": "SKM218", "SK208": "SK", "SKB208": "SKMBroad", "SKB218": "SKMB218", "MF173": "MF-M-R", "MF203": "MFM203",
      "GR198": "GR198", "GR208": "GR208", "GR218": "GR218R", "GR229": "GR229", "GR239": "GR239", "GRB2": "GRB2", "GRN5": "GRN5", "GR-BODY-10": "GR-BODY-10",
      "GOH208": "GO-H208", "GO217": "GO217", "GO224": "GO224", "SG": "SG"}
for k in ("GR198", "GR208", "GR218", "GR229", "GR239", "GRB2", "GRN5", "GR-BODY-10", "SK198", "SK208", "SK218", "SKB208", "SKB218", "MF173", "MF203", "SG",
          "GO217", "GO224", "GOH208", "GR-BODY-06", "GR-BODY-07", "GR-BODY-08", "GR-BODY-09", "GR-LOW", "SK-LOWMUS", "SK-HIMUS", "SK-HIFAT", "SK-HIBOTH", "MF-LOW", "SK-LOW"):
    e = dict(W2C[k]); e["joint"] = JK.get(k); e.pop("jbw", None); e.pop("grask", None); R[k] = e
# Skarn 229 configuration 1: the original W2B body (W2C1 reverted the W2B1 knee-only correction; author confirmed)
R["SK229"] = {"meas": S + '/w2b/st/SKM229', "skp": S + '/s7n/w2b_g_SKM229', "skp_id": "MF-M-R", "joint": "SKM229"}
R["SKB229"] = {"meas": S + '/w2d/sk/SKMB229', "skp": S + '/w2d/g/SKMB229/skp', "skp_id": "MF-M-R", "joint": "SKMB229"}
# Marchfolk 203 configuration 1: the uncorrected height-macro body (W2C1 knee-only revert; author confirmed)
R["MF203"]["meas"] = S + '/w2a/st/MFM203'
json.dump(R, open(sys.argv[1], 'w'), indent=1); print(len(R), "bodies")

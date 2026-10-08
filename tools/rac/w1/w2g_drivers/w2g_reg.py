# RAC W2G (Halvren central envelope) body registry: the Halvren bodies built in this pass (w2g_drivers/hv_build.py; grids by w2a_drivers/mfm_grid.py),
# the accepted W1 anchor HVC1 (skeletal proxy = the S7-normalized accepted HV body: HVC1 only removes the eye-scale target), and the ACCEPTED W2
# source families: Marchfolk (W2A / W2B / W2E / W2F matched comparators, W2C1 knee reverts applied), Sagekin W2E, Skarn W2B, Fenn / Aelari / Vael W2F
# (closure registry: R2 native bodies at 157-173 cm, FN-09 x0.75).   Usage: python3 w2g_reg.py OUT.json
import sys, json, os, glob
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2g'; N = S + '/s7n'
F = json.load(open('/home/claude/wayfarer-design/reviews/rac-w2f-elf-evidence/closure/registry_closure.json'))
R = {}
def hv(name, d, nid, grid=True):
    R[name] = {"meas": W + '/%s/%s' % (d, nid), "skp": (W + '/g/%s/skp' % nid) if grid else None, "skp_id": "MF-M-R", "joint": nid, "race": "HV"}
# central family: native route where the re-solved macro < ~0.40 (HV152: 0.19, HV163: 0.34), macro elsewhere; macro builds at 152 / 163 kept as route check
hv("HV152", "st", "HV152N-NAT"); hv("HV163", "st", "HV163N-NAT")
for h in (173, 181, 190, 203, 213): hv("HV%d" % h, "st", "HV%dM" % h)
for h in (152, 163): hv("HV%dM" % h, "st", "HV%dM" % h, grid=False); R["HV%dM" % h]["race"] = None
R["HV178"] = {"meas": S + '/w1s/probe/HVC1', "skp": N + '/w1s_hv', "skp_id": "HV", "joint": "HVC1", "race": "HV"}
for p in sorted(glob.glob(W + '/fr/*_build.json')) + sorted(glob.glob(W + '/ex/*_build.json')):
    n = os.path.basename(p)[:-11]; hv(n, os.path.basename(os.path.dirname(p)), n)
for p in sorted(glob.glob(W + '/comp/*_build.json')) + sorted(glob.glob(W + '/stress/*_build.json')):
    n = os.path.basename(p)[:-11]; hv(n, os.path.basename(os.path.dirname(p)), n, grid=False)
# probe (REPORT, not applied): reading-bounded Aelari-influenced body (aec_probe.py)
if os.path.exists(W + '/probe/HVXAEc_meas.json'): hv("HVXAEc", "probe", "HVXAEc")
# W1 expression panel (accepted diagnostic points): human-leaning HVH3, elf-leaning HVE3
for n in ("HVH3", "HVE3"):
    p = glob.glob(S + '/w1s/panel/%s_meas.json' % n)
    if p: R["W1" + n] = {"meas": p[0][:-10], "joint": None}
# accepted source families (W2F closure registry carries MF, SG, SK and the elves with their keys)
for k, e in F.items():
    if k[:2] in ("MF", "SG", "SK", "FN", "AE", "VA") and not k.endswith("M") and "x50" not in k and not k.startswith(("AEP", "VAP")):
        e = dict(e); e.pop("race", None); R[k] = e
E = S + '/w2e'
R["MF152"] = {"meas": S + '/w1t/bnd/MF152-NAT', "skp": N + '/w1t_g152mf', "skp_id": "MF-M-R", "joint": "W1T-MF152-NAT"}
R["SG152"] = {"meas": E + '/st/SG152-NAT', "skp": E + '/g/SG152-NAT/skp', "skp_id": "MF-M-R", "joint": "SG152-NAT"}
R["SG163"] = {"meas": E + '/st/SG163', "skp": E + '/g/SG163/skp', "skp_id": "MF-M-R", "joint": "SG163"}
R["SG208"] = {"meas": E + '/st/SG208', "skp": E + '/g/SG208/skp', "skp_id": "MF-M-R", "joint": "SG208"}
R["SK183"] = {"meas": S + '/w2b/st/SKM183', "skp": N + '/w2b_g_SKM183', "skp_id": "MF-M-R", "joint": "SKM183"}
R["SKB208"] = {"meas": S + '/w2b/fr/SKMBroad', "skp": N + '/w2b_g_SKMBroad', "skp_id": "MF-M-R", "joint": "SKMBroad"}
json.dump(R, open(sys.argv[1], 'w'), indent=1); print(len(R), "bodies")

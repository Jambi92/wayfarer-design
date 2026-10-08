# RAC W2E (Sagekin W2) body registry: every Sagekin body built in this pass (w2e_drivers/sg_build.py; CIB grids by w2a_drivers/mfm_grid.py,
# files named by the Marchfolk id inside each grid) and the accepted comparators: Marchfolk W1 / W2A / W2B (W2C1 knee reverts applied: Marchfolk
# 190 and 203 configuration 1 are the uncorrected bodies), Marchfolk 163 / 178 built here on the accepted macro route (matched-height comparators
# only; Marchfolk unchanged), the W1t 152 cm native bodies (Marchfolk, Durrim, Sagekin route cross-check), Skarn W2B, Fenn / Aelari W1.
# Usage: python3 w2e_reg.py OUT.json
import sys, json, os
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2e'; N = S + '/s7n'
R = {}
def sg(name, d, nid=None, grid=True):
    nid = nid or name
    R[name] = {"meas": W + '/%s/%s' % (d, nid), "skp": (W + '/g/%s/skp' % nid) if grid else None, "skp_id": "MF-M-R", "joint": nid, "sagekin": True}
sg("SG152", "st", "SG152-NAT"); sg("SG163", "st"); sg("SG173", "st"); sg("SG181", "st"); sg("SG190", "st"); sg("SG203", "st"); sg("SG208", "st")
R["SG178"] = {"meas": S + '/w1f/final/SG', "skp": N + '/w1i_base', "skp_id": "SG", "joint": "SG", "sagekin": True}
for n in ("SGB178", "SGN178", "SGN208", "SGB208", "SGB152", "SGN152"): sg(n, "fr")
sg("SG04", "nm", "SG04x150")     # SG-04 = Sagekin limb / hand targets x1.5 (see the gate: x2.0 / x1.75 probes)
sg("SG04x200", "nm", "SG04"); sg("SG04x175", "nm", "SG04x175", grid=False)
for n in ("SG09", "SG10"): sg(n, "nm")
for n in ("SG163N",): R[n] = {"meas": W + '/rt/%s-NAT' % n, "sagekin": True}
R["MF163N"] = {"meas": W + '/rt/MF163N-NAT'}
R["MF181"] = {"meas": W + '/mf/MF181', "joint": "MF181"}
for n in ("SG173-LOWMUS", "SG173-HIMUS", "SG173-HIFAT", "SG173-HIBOTH", "SG173-LOW", "SG173-MIN", "SG06", "SG07", "SG08"): sg(n, "comp", grid=False)
R["SG152-W1T"] = {"meas": S + '/w1t/bnd/SG152-NAT', "skp": None, "joint": "W1T-SG152-NAT", "sagekin": True}
R["MF152"] = {"meas": S + '/w1t/bnd/MF152-NAT', "skp": N + '/w1t_g152mf', "skp_id": "MF-M-R", "joint": "W1T-MF152-NAT"}
R["DU152"] = {"meas": S + '/w1t/bnd/DU152-NAT', "skp": N + '/w1t_g152du', "skp_id": "DU-NAT", "joint": "W1T-DU152-NAT"}
R["MF147"] = {"meas": S + '/w2a/st/MFM147-NAT', "skp": N + '/w2a_g_MFM147', "skp_id": "MF-M-R", "joint": "MFM147-NAT"}
R["MF163"] = {"meas": W + '/mf/MF163', "skp": W + '/g/MF163/skp', "skp_id": "MF-M-R", "joint": "MF163"}
R["MF173"] = {"meas": S + '/w1f/final/MF-M-R', "skp": N + '/w1i_base', "skp_id": "MF-M-R", "joint": "MF-M-R"}
R["MF178"] = {"meas": W + '/mf/MF178', "skp": W + '/g/MF178/skp', "skp_id": "MF-M-R", "joint": "MF178"}
R["MF190"] = {"meas": S + '/w2b/st/MFM190', "skp": N + '/w2b_g_MFM190', "skp_id": "MF-M-R", "joint": "MFM190"}
R["MF203"] = {"meas": S + '/w2a/st/MFM203', "skp": N + '/w2a_g_MFM203', "skp_id": "MF-M-R", "joint": "MFM203"}
R["MFB173"] = {"meas": S + '/w2a1/p/MBX', "skp": N + '/w2a1_g_MBX', "skp_id": "MF-M-R", "joint": "MBX"}
R["MFN173"] = {"meas": S + '/w2a1/p/MNX', "skp": N + '/w2a1_g_MNX', "skp_id": "MF-M-R", "joint": "MNX"}
for k, f in (("MF-LOWMUS", "MFM-LOWMUS"), ("MF-HIMUS", "MFM-HIMUS"), ("MF-HIFAT", "MFM-HIFAT"), ("MF-HIBOTH", "MFM-HIBOTH")): R[k] = {"meas": S + '/w2a/comp/' + f}
R["MF-LOW"] = {"meas": S + '/w1f/low/MF-M-R-LOW'}; R["MF-MIN"] = {"meas": W + '/mf/MF-M-R-LEAN'}
R["SK183"] = {"meas": S + '/w2b/st/SKM183', "skp": N + '/w2b_g_SKM183', "skp_id": "MF-M-R", "joint": "SKM183"}
R["SK190"] = {"meas": S + '/w2b/st/SKM190', "skp": N + '/w2b_g_SKM190', "skp_id": "MF-M-R", "joint": "SKM190"}
R["SK203"] = {"meas": S + '/w2b/st/SKM203', "skp": N + '/w2b_g_SKM203', "skp_id": "MF-M-R", "joint": "SKM203"}
R["SK208"] = {"meas": S + '/w1f/final/SK', "skp": N + '/w1i_base', "skp_id": "SK", "joint": "SK"}
R["SKB208"] = {"meas": S + '/w2b/fr/SKMBroad', "skp": N + '/w2b_g_SKMBroad', "skp_id": "MF-M-R", "joint": "SKMBroad"}
R["FN181"] = {"meas": S + '/w1p/cand/FNL4', "skp": N + '/w1p_fnl4', "skp_id": "FN", "joint": "FNL4"}
R["AE190"] = {"meas": S + '/w1m/legs/AEL1', "skp": N + '/w1m_ael1', "skp_id": "AE", "joint": "AEL1"}
json.dump(R, open(sys.argv[1], 'w'), indent=1); print(len(R), "bodies")

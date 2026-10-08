# RAC W2F (Elf family W2) body registry: the Fenn / Aelari / Vael bodies built in this pass (w2f_drivers/el_build.py; CIB grids by
# w2a_drivers/mfm_grid.py, files named by the Marchfolk id inside each grid), the accepted W1 references FNL4 / AEL1 / VAL4 (S7-normalized
# skeletal proxies), and the accepted comparators: Marchfolk W1 / W2A / W2B / W2E-built matched bodies (W2C1 knee reverts applied), Marchfolk 157 / 168
# built here on the accepted route rule (comparators only), Sagekin W2E (accepted), Skarn W2B (large-human guard).   Usage: python3 w2f_reg.py OUT.json
import sys, json, os, glob
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2f'; E = S + '/w2e'; N = S + '/s7n'
R = {}
def el(name, d, race, nid=None, grid=True):
    nid = nid or name
    R[name] = {"meas": W + '/%s/%s' % (d, nid), "skp": (W + '/g/%s/skp' % nid) if grid else None, "skp_id": "MF-M-R", "joint": nid, "race": race}
for p in sorted(glob.glob(W + '/st/*_build.json')):
    nid = os.path.basename(p)[:-11]; name = nid.replace('-NAT', ''); el(name, "st", name[:2], nid)
for p in sorted(glob.glob(W + '/fr/*_build.json')):
    nid = os.path.basename(p)[:-11]; el(nid, "fr", nid[:2])
for p in sorted(glob.glob(W + '/comp/*_build.json')) + sorted(glob.glob(W + '/fcomp/*_build.json')):
    nid = os.path.basename(p)[:-11]; el(nid, os.path.basename(os.path.dirname(p)), nid[:2], grid=False)
for p in sorted(glob.glob(W + '/nm/*_build.json')):
    nid = os.path.basename(p)[:-11]; el(nid, "nm", nid[:2])
R["FN181"] = {"meas": S + '/w1p/cand/FNL4', "skp": N + '/w1p_fnl4', "skp_id": "FN", "joint": "FNL4", "race": "FN"}
R["AE190"] = {"meas": S + '/w1m/legs/AEL1', "skp": N + '/w1m_ael1', "skp_id": "AE", "joint": "AEL1", "race": "AE"}
R["VA178"] = {"meas": S + '/w1n/cand/VAL4', "skp": N + '/w1n_val4', "skp_id": "VA", "joint": "VAL4", "race": "VA"}
for n in ("AE168N", "AE173N", "FN163N", "VA163N"): R[n] = {"meas": W + '/rt/%s-NAT' % n, "joint": n + "-NAT"}
for p in sorted(glob.glob(W + '/probe/*_build.json')):
    nid = os.path.basename(p)[:-11]; R[nid] = {"meas": W + '/probe/' + nid, "joint": nid}
R["MF157"] = {"meas": W + '/mf/MF157-NAT', "skp": W + '/g/MF157-NAT/skp', "skp_id": "MF-M-R", "joint": "MF157-NAT"}
R["MF168"] = {"meas": W + '/mf/MF168', "skp": W + '/g/MF168/skp', "skp_id": "MF-M-R", "joint": "MF168"}
R["MF163"] = {"meas": E + '/mf/MF163', "skp": E + '/g/MF163/skp', "skp_id": "MF-M-R", "joint": "MF163"}
R["MF173"] = {"meas": S + '/w1f/final/MF-M-R', "skp": N + '/w1i_base', "skp_id": "MF-M-R", "joint": "MF-M-R"}
R["MF178"] = {"meas": E + '/mf/MF178', "skp": E + '/g/MF178/skp', "skp_id": "MF-M-R", "joint": "MF178"}
R["MF181"] = {"meas": E + '/mf/MF181', "skp": W + '/g/MF181/skp', "skp_id": "MF-M-R", "joint": "MF181"}
R["MF190"] = {"meas": S + '/w2b/st/MFM190', "skp": N + '/w2b_g_MFM190', "skp_id": "MF-M-R", "joint": "MFM190"}
R["MF203"] = {"meas": S + '/w2a/st/MFM203', "skp": N + '/w2a_g_MFM203', "skp_id": "MF-M-R", "joint": "MFM203"}
for k, f in (("MF-LOWMUS", "MFM-LOWMUS"), ("MF-HIMUS", "MFM-HIMUS"), ("MF-HIFAT", "MFM-HIFAT"), ("MF-HIBOTH", "MFM-HIBOTH")): R[k] = {"meas": S + '/w2a/comp/' + f}
R["MF-LOW"] = {"meas": S + '/w1f/low/MF-M-R-LOW'}; R["MF-MIN"] = {"meas": E + '/mf/MF-M-R-LEAN'}
for h in (173, 181, 190, 203): R["SG%d" % h] = {"meas": E + '/st/SG%d' % h, "skp": E + '/g/SG%d/skp' % h, "skp_id": "MF-M-R", "joint": "SG%d" % h}
R["SG178"] = {"meas": S + '/w1f/final/SG', "skp": N + '/w1i_base', "skp_id": "SG", "joint": "SG"}
for c in ("LOWMUS", "HIMUS", "HIFAT", "HIBOTH", "LOW", "MIN"): R["SG173-" + c] = {"meas": E + '/comp/SG173-' + c}
R["SK190"] = {"meas": S + '/w2b/st/SKM190', "skp": N + '/w2b_g_SKM190', "skp_id": "MF-M-R", "joint": "SKM190"}
R["SK203"] = {"meas": S + '/w2b/st/SKM203', "skp": N + '/w2b_g_SKM203', "skp_id": "MF-M-R", "joint": "SKM203"}
R["SK208"] = {"meas": S + '/w1f/final/SK', "skp": N + '/w1i_base', "skp_id": "SK", "joint": "SK"}
R["SK229"] = {"meas": S + '/w2b/st/SKM229', "skp": N + '/w2b_g_SKM229', "skp_id": "MF-M-R", "joint": "SKM229"}
json.dump(R, open(sys.argv[1], 'w'), indent=1); print(len(R), "bodies")

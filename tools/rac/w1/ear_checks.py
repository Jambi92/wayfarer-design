"""RAC W1e: canon-direction checks on the ear-family v2 sculpt-detail set (E-D1...E-D6, order §4) plus the attached-ear readings.
Reads ear_families_v2.json (ear-local frame, MF-M-R head scale for MF/elves/HV/GR/GO; PK/CG at their own head scale) and
ears_attached.json. Tip vector = (lateral, back, up) cm from the root. Strict inequalities on unrounded values; relative margin
< 5 % = marginal (schematic geometry; same rule as the W1d packet's 2 % note, stated here explicitly).
basis = "measured" (read from the built mesh landmarks) or "construction" (a builder input parameter: confirms the input encodes
the canon direction, not an independent measurement).
Usage: python3 ear_checks.py ear_families_v2.json ears_attached.json meas_dir out.json"""
import sys, os, json

def main(ef, ea, md, out):
    E = json.load(open(ef)); A = json.load(open(ea)); C = []
    L = lambda k: E[k]["landmarks"]; P = lambda k: E[k]["outline_params"]; Q = lambda k: E[k]["relief_params"]
    HH = {b: json.load(open(os.path.join(md, b + "_meas.json")))["combined"]["cranio"]["HH"] for b in A}
    def add(cand, chk, src, va, op, vb, b, report=False, basis="measured"):
        ok = True if report else {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
        C.append({"cand": cand, "check": chk, "canon": src, "va": va, "op": op, "vb": vb, "b": b, "pass": ok,
                  "marginal": bool(ok and not report and abs(va - vb) / max(abs(vb), 1e-9) < 0.05), "report_only": report, "basis": basis})
    ext = lambda k: L(k)["auricle_projection_cm"]; tip = lambda k: L(k)["tip_lateral_back_up_cm"]
    for o in ("VA-elven", "AE-elven"):
        add("FN", "total lateral extent > %s (FN greatest average projection; E-D3 widened)" % o[:2], "ECR L283; FENN L196; E-D3", ext("FN-elven"), ">", ext(o), o[:2])
    add("AE", "tip more upward than FN", "ECR L109, L283", tip("AE-elven")[2], ">", tip("FN-elven")[2], "FN")
    add("AE", "tip more backward than FN", "ECR L109, L283", tip("AE-elven")[1], ">", tip("FN-elven")[1], "FN")
    add("VA", "tip more lateral than AE", "ECR L110; VAEL L297", tip("VA-elven")[0], ">", tip("AE-elven")[0], "AE")
    add("VA", "tip more backward than AE", "ECR L110; VAEL L297", tip("VA-elven")[1], ">", tip("AE-elven")[1], "AE")
    for o in ("FN-elven", "AE-elven"):
        add("VA", "base half-width > %s (somewhat broader base)" % o[:2], "ECR L110; VAEL L297", P("VA-elven")["wb"], ">", P(o)["wb"], o[:2], basis="construction")
    add("AE", "taper starts earlier than VA (longer, more gradual)", "ECR L109, L110", P("AE-elven")["taper"][1], "<", P("VA-elven")["taper"][1], "VA", basis="construction")
    add("GR", "taper start fraction > elven maximum (late taper, sustained body)", "GRASK L469, L475; E-D1", P("GR-folded")["taper"][1], ">", max(P(k)["taper"][1] for k in ("FN-elven", "AE-elven", "VA-elven")), "elves", basis="construction")
    add("GR", "fold count > 0 (folded-cartilage system)", "GRASK L469", float(Q("GR-folded")["folds"][0]), ">", 0.0, "-", basis="construction")
    add("GO", "auricle-body angle < MF (close-set; E-D4 identity variable)", "GORRUND L375; E-D4", L("GO-bowl")["auricle_body_angle_deg"], "<", L("MF-human")["auricle_body_angle_deg"], "MF")
    add("GO", "tip-from-root < every elven ear (short-to-moderate extent)", "GORRUND L375, L476, L491", L("GO-bowl")["tip_distance_from_root_cm"], "<", min(L(k)["tip_distance_from_root_cm"] for k in ("FN-elven", "AE-elven", "VA-elven")), "elves")
    add("GO", "tip-from-root < GR", "GORRUND L375, L476, L491", L("GO-bowl")["tip_distance_from_root_cm"], "<", L("GR-folded")["tip_distance_from_root_cm"], "GR")
    add("GO", "concha depth > MF (deep bowl)", "GORRUND L375, L476, L491", Q("GO-bowl")["concha"], ">", Q("MF-human")["concha"], "MF", basis="construction")
    add("GO", "RA §11 total lateral extent vs MF (REPORT ONLY, E-D4)", "E-D4", ext("GO-bowl"), "vs", ext("MF-human"), "MF", report=True)
    add("PK", "auricle-body angle < MF (compact attachment integrating closely)", "PK L351", L("PK-compact")["auricle_body_angle_deg"], "<", L("MF-human")["auricle_body_angle_deg"], "MF")
    add("PK", "concha depth < MF (clear but not deep bowl)", "PK L351", Q("PK-compact")["concha"], "<", Q("MF-human")["concha"], "MF", basis="construction")
    add("PK", "rounded top (no taper)", "PK L351", 1.0 if P("PK-compact")["taper"] is None else 0.0, ">", 0.5, "-", basis="construction")
    add("CG", "cartilage thickness < PK (finer cartilage)", "CG L1327, L1366ff", Q("CG-finefolded")["thick"], "<", Q("PK-compact")["thick"], "PK", basis="construction")
    add("CG", "cartilage thickness < MF", "CG L1327", Q("CG-finefolded")["thick"], "<", Q("MF-human")["thick"], "MF", basis="construction")
    add("CG", "rounded top (no taper, non-pointed)", "CG L1327, L1364", 1.0 if P("CG-finefolded")["taper"] is None else 0.0, ">", 0.5, "-", basis="construction")
    add("CG", "concha depth < GO (no broad deep bowl)", "CG L1366ff", Q("CG-finefolded")["concha"], "<", Q("GO-bowl")["concha"], "GO", basis="construction")
    # attached readings: ear height / HH (report only: canon gives no ratio)
    for b, r in A.items():
        add(b, "attached auricle height / HH vs MF-M-R (REPORT ONLY)", "-", r["l"]["auricle_height_cm"] / HH[b], "vs", A["MF-M-R"]["l"]["auricle_height_cm"] / HH["MF-M-R"], "MF-M-R", report=True)
    json.dump(C, open(out, "w"), indent=1)
    g = [c for c in C if not c["report_only"]]
    print(len(g), "checks;", sum(not c["pass"] for c in g), "fail;", sum(c["marginal"] for c in g), "marginal;", len(C) - len(g), "report-only")
    for c in C:
        if not c["pass"] or c["marginal"] or c["report_only"]: print("REPORT" if c["report_only"] else ("FAIL" if not c["pass"] else "marg"), c["cand"], c["check"], round(c["va"], 4), c["op"], round(c["vb"], 4))

if __name__ == "__main__":
    main(*sys.argv[1:5])

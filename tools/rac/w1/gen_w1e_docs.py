"""Generate the W1e ARM records and evidence tables from the evidence JSON (no hand-typed numbers).
Writes reviews/rac-w1e-evidence/tables.md and reviews/rac-w1e-arm/claude-rac-w1e-arm-<ID>.md."""
import json, os, hashlib
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
EV = os.path.join(R, "reviews", "rac-w1e-evidence"); ARM = os.path.join(R, "reviews", "rac-w1e-arm")
C1 = os.path.join(R, "reviews", "rac-w1c-evidence"); D1 = os.path.join(R, "reviews", "rac-w1d-evidence", "native-short")
CFG = os.path.join(R, "tools", "rac", "w1", "cfg")
REBUILT = ["FN", "AE", "VA", "GR", "GO", "DU-NAT", "PK-NAT"]
CARRIED = ["HV", "CG-NAT"]
CHK = {"DU-NAT": "DU", "PK-NAT": "PK", "CG-NAT": "CG"}          # candidate key used inside the check files
PREV = {"FN": (C1, "FN"), "AE": (C1, "AE"), "VA": (C1, "VA"), "GR": (C1, "GR"), "GO": (C1, "GO"), "DU-NAT": (C1, "DU"),
        "PK-NAT": (D1, "PK-NAT"), "HV": (C1, "HV"), "CG-NAT": (D1, "CG-NAT")}
EAR = {"FN": "FN-elven", "AE": "AE-elven", "VA": "VA-elven", "HV": "HV-mixed", "GR": "GR-folded", "GO": "GO-bowl",
       "PK-NAT": "PK-compact", "CG-NAT": "CG-finefolded", "DU-NAT": None}
NAME = {"FN": "Fenn central", "AE": "Aelari central", "VA": "Vael central", "HV": "Halvren central (no-lineage general envelope)",
        "DU-NAT": "Durrim central (native short-adult route)", "GR": "Grask central", "GO": "Gorrund central",
        "PK-NAT": "Pipkin central (native short-adult route)", "CG-NAT": "Cogling central (native short-adult route)"}
KEYS = ["torso_share", "leg_share", "crest_share", "bitroch_share", "hip_joint_breadth_share", "pelvic_depth_share",
        "pelvic_vertical_share", "pelvic_depth_over_crest", "waist_interval_over_torso", "shoulder_joint_share",
        "thorax_breadth_share", "thorax_d_over_b", "HH_share"]
# Verdict lines: judgement by the inspector; every number they rest on is in the check files rendered below.
V = {
 "FN": ["Pelvic architecture (E-A1/E-A2/E-A3, PV-D3a, PV-D4a, FN-P6): skin diagnostics pass. Canon validation needs skeletal / bony-landmark geometry (PV-D16), not built.",
        "Bony orbit: the O-1 ring proposal (FN = MF x head size x 1.02) waits on author confirmation of the increment (O-D2); RM-CF-08 FN ORB stays NOT DEMONSTRATED (O-D4). The E-proxy directional check still reads FN < MF and stays a diagnostic until O-1 is accepted.",
        "Ear: FN-elven v2 attached (W1 reference centre, E-D2; FN-VA projection gap widened per E-D3)."],
 "AE": ["Pelvic architecture (E-A, PV-D3a, PV-D5, AE-P6): skin diagnostics pass except **hip-joint height > MF (E-A2), NOT DEMONSTRATED** (+0.4 %, inside the 1 % threshold). A trial raising the leg targets demonstrated it but broke the forearm and foot directions, so it was not kept. Skeletal validation pending (PV-D16).",
        "Ear: AE-elven v2 attached."],
 "VA": ["Rebuilt after the W1e audit without the pelvic depth increase: PV-D6 (a) treats ≈ MF as the minimum and says not to author VA > MF without need. VA depth now reads −0.6 % vs MF (MARGINAL, not a failure) and stays > FN and > AE.",
        "**Hip-joint height > MF and < AE (E-A2, VA-P2a): both NOT DEMONSTRATED** — at the central AE leg share the window MF < VA < AE is narrower than two 1 % margins. Natural lordosis (PV-D7) not modelled beyond the generator spine. Skeletal validation pending (PV-D16).",
        "Ear: VA-elven v2 attached."],
 "HV": ["Geometry unchanged from W1c (hash identical); re-measured with the W1e readings. Source-span checks re-run against the rebuilt FN/AE/VA: all pass. Sources are still CONSTRAINED, so HV stays CONSTRAINED.",
        "The no-lineage general envelope stays BUILDER-CHOSEN as a whole (E-D6: the HV ear is one example, not a centre).", "Ear: HV-mixed v2 attached."],
 "DU-NAT": ["**Route is a builder choice needing acceptance (BM-2):** PV-D21 (c) names regional deformation for DU; the body uses the native short-adult source (regional factors, W1d finding that the minimum-height model is implausible) plus a regional pelvic bone scale. Identity-relevant shifts vs W1c are large (`tables.md` §2).",
            "PV-D8, PV-D9 and DU-P2b/P3/P5 skin diagnostics pass; skeletal validation pending (PV-D16). Landmark globe 2.12 cm: a 2.3 cm adult globe touches the socket skin (`globe_fit_pkcg.json`).",
            "Ear: Durrim keeps the generator's human auricle (broadly humanoid compact range; no family built)."],
 "GR": ["Girdle / pelvis (AD-G1...G4, PV-D12): skin diagnostics pass, but the girdle readings use the generator shoulder joint, not the anatomical acromial / glenohumeral landmarks AD-G10 requires. **The ordered AD-G14 rebuild (skeletal-trunk proxy + sculpted envelope) was not executed.** GR vs MF shoulder breadth / stature kept UNDETERMINED (AD-G4).",
        "Ear: GR-folded v2 attached."],
 "GO": ["**FAIL — eight skin diagnostics fail**: pelvic AP depth / crest > MF and > SK (PV-D14), bitrochanteric / crest ≈ MF (GO-P2b), pelvic vertical / stature ≥ GR (GO-P3), ALPC-1 lumbar depth, ALPC-2a pelvic AP / thoracic depth, and two ALPC-7 depth items. GO-P2a and ALPC-3/5/6/8 are NOT RUN. A skin-only trial removes six of the eight but leaves two and produces a buttock/abdomen bulge (`go_skin_trial_*`).",
        "**The ordered AD-G14 rebuild (skeletal-trunk proxy + sculpted envelope) was not executed** in this pass; it is the route to resolve these items. Visual (PV-D17): the trunk still reads as a large lean human, not a structurally massive axial trunk.",
        "Ear: GO-bowl v2 attached (close-set by auricle-body angle, E-D4)."],
 "PK-NAT": ["Pelvis rebuilt (PV-D10 >= MF, PV-D11, PK-P3...P6): skin diagnostics pass. The pelvis vertical scale was tested for need after the audit: without it PK leg share exceeds MF (directional FAIL) and pelvic vertical / stature is marginal, so it is kept. Skeletal validation pending (PV-D16).",
            "**S-D3 contradiction:** an ordinary adult globe (2.2-2.4 cm) does not fit the authored socket; fitting one needs orbits about 1.25-1.3 x MF relative to head height. Flagged, head canon not altered; the landmark globe stays the socket-derived placeholder and is NOT biological eye canon.",
            "Ear: PK-compact v2 attached (built at its own head scale)."],
 "CG-NAT": ["Geometry unchanged from W1d (hash identical); re-measured with the W1e readings; all directional checks pass incl. the narrow thorax.",
            "**S-D3 contradiction** (as PK, stronger: about 1.7-1.8 x MF orbit relative to head height; two 2.3 cm globes leave 0.71 cm between them). Flagged; head canon not altered.",
            "Ear: CG-finefolded v2 attached (built at its own head scale)."],
}
STATUS = {k: "CONSTRAIN" for k in ("FN", "AE", "VA", "HV", "DU-NAT", "GR", "PK-NAT", "CG-NAT")}; STATUS["GO"] = "FAIL"

def jl(p): return json.load(open(p))
def f4(x): return ("[%.4f, %.4f]" % tuple(x)) if isinstance(x, list) else "%.4f" % x
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]

def meas(i):
    p = os.path.join(EV, "candidates", i + "_meas.json")
    return jl(p if os.path.exists(p) else os.path.join(EV, "remeasured", i + "_meas.json"))

def checks_for(i, rows):
    k = CHK.get(i, i); return [x for x in rows if x["cand"] == k]

STRICT = (">", "<")
def dir_result(x):
    """directional_checks rows: apply the AD-G10 1 % rule as in w1e_checks (strict holds by < 1 % = NOT DEMONSTRATED)."""
    if "result" in x: return x["result"]
    if x.get("report_only"): return "REPORT"
    if not x["pass"]: return "FAIL"
    if x["op"] in STRICT and isinstance(x["vb"], float) and abs(x["va"] - x["vb"]) / max(abs(x["vb"]), 1e-9) < 0.01: return "NOT DEMONSTRATED"
    return "PASS"

def fmt_rows(rows, extra=False):
    out = ["| Cand | Check | Canon | Value | Op | Comparator | Result |", "|---|---|---|---|---|---|---|"]
    for x in rows:
        res = dir_result(x)
        if x.get("basis") == "construction": res += " (construction input)"
        res = "**%s**" % res if res.startswith(("FAIL", "NOT DEM", "MARGINAL")) else res
        va = "—" if x["va"] is None else f4(x["va"]); vb = "" if x["vb"] is None else f4(x["vb"])
        out.append("| %s | %s | %s | %s | %s | %s %s | %s |" % (x["cand"], x["check"], x["canon"], va, x["op"], x.get("b", ""), vb, res))
    return out

def counts(rows):
    from collections import Counter
    c = Counter(dir_result(x) for x in rows); return ", ".join("%s %d" % (k, c[k]) for k in ("PASS", "NOT DEMONSTRATED", "MARGINAL", "FAIL", "NOT RUN", "REPORT") if c[k])

def main():
    os.makedirs(ARM, exist_ok=True)
    DC = jl(os.path.join(EV, "directional_checks.json")); WC = jl(os.path.join(EV, "w1e_checks.json"))
    EC = jl(os.path.join(EV, "ears", "ear_checks.json")); EA = jl(os.path.join(EV, "ears", "ears_attached.json"))
    OR = jl(os.path.join(EV, "orbit", "orbit_rings.json")); GF = jl(os.path.join(EV, "globe_fit_pkcg.json"))
    T = ["# RAC W1e — evidence tables", "", "Generated by `tools/rac/w1/gen_w1e_docs.py` from the JSON in this folder. Skin readings are diagnostics (PV-D16); nothing here is canon.", ""]
    # builds
    T += ["## 1. Rebuilt candidates (BUILDER-CHOSEN construction magnitudes, R-14)", "", "| ID | Route | Stature R-6 (cm) | Height macro | bone_scales (X lateral, Y length, Z depth) | Regional factors (native route) |", "|---|---|---|---|---|---|"]
    for i in REBUILT:
        b = jl(os.path.join(EV, "candidates", i + "_build.json")); cfg = jl(os.path.join(CFG, "w1e", i + ".json"))
        route = "native short-adult (`native_short.py`)" if "native_factors" in b else "native height solve (`build_arm.py`)"
        nf = ", ".join("%s %.3f" % kv for kv in b.get("native_factors", {}).items()) or "—"
        bs = "; ".join("%s %s" % (k, v) for k, v in cfg.get("bone_scales", {}).items())
        T.append("| %s | %s | %.2f | %.4f | %s | %s |" % (i, route, b["stature_r6"], b["height_macro"], bs, nf))
    T += ["", "Generator-target changes against the W1c / W1d configs (cfg diff):", ""]
    for i in REBUILT:
        new = jl(os.path.join(CFG, "w1e", i + ".json")); old = jl(os.path.join(CFG, (i if i.endswith("NAT") else i) + ".json")) if os.path.exists(os.path.join(CFG, i + ".json")) else jl(os.path.join(CFG, "DU.json"))
        ch = []
        for k in sorted(set(new.get("targets", {})) | set(old.get("targets", {}))):
            a, b_ = old.get("targets", {}).get(k), new.get("targets", {}).get(k)
            if a != b_: ch.append("`%s` %s → %s" % (k, a, b_))
        T.append("- **%s**: %s" % (i, "; ".join(ch) if ch else "no target change (bone_scales only%s)" % ("; route changed from the W1c height-macro build to native short-adult" if i == "DU-NAT" else "")))
    # key readings
    T += ["", "## 2. Key readings (combined state; W1c/W1d value in brackets where the body was rebuilt)", ""]
    ids = REBUILT + CARRIED
    T += ["| Reading | MF-M-R | " + " | ".join(ids) + " |", "|---|---|" + "---|" * len(ids)]
    mf = meas("MF-M-R")["combined"]["ratio"]
    for k in KEYS:
        row = ["| %s | %s" % (k, f4(mf[k]))]
        for i in ids:
            v = meas(i)["combined"]["ratio"].get(k)
            pdir, pid = PREV[i]; pm = jl(os.path.join(pdir, pid + "_meas.json"))["combined"]["ratio"].get(k)
            s = f4(v) if v is not None else "—"
            if i in REBUILT and pm is not None and v is not None and abs(pm - v) > 5e-5: s += " (%s)" % f4(pm)
            row.append(s)
        T.append(" | ".join(row) + " |")
    # checks
    T += ["", "## 3. Accepted pelvic / girdle / ALPC relations (`w1e_checks.json`; %d rows: %s)" % (len(WC), counts(WC)), "",
          "Rule (AD-G10, PV-D10): strict > / < must hold by at least 1 %, otherwise NOT DEMONSTRATED; non-strict >= / <= missing by under 1 % is MARGINAL (not a failure); '~' is the W1c absolute ±0.010 tolerance (a ±6–8 % band on these shares — wide). NOT RUN = needs geometry the skin route does not have.", ""] + fmt_rows(WC)
    fails = [x for x in DC if dir_result(x) != "PASS"]
    T += ["", "## 4. Cross-race directional checks (`directional_checks.json`; %d checks: %s; same 1 %% rule applied to strict directions)" % (len(DC), counts(DC)), ""] + fmt_rows(fails)
    hv = [x for x in DC if x["cand"] == "HV"]
    T += ["", "HV source-span checks (sources: MF, SG and the rebuilt FN, AE, VA):", ""] + fmt_rows(hv)
    # ears
    T += ["", "## 5. Ear families v2 (`ears/ear_checks.json`)", "", "| Family | Height (cm) | Tip from root (cm) | Total lateral extent (cm) | Auricle-body angle (deg) | Tip lateral / back / up (cm) |", "|---|---|---|---|---|---|"]
    ef = jl(os.path.join(EV, "ears", "ear_families_v2.json"))
    for k, v in ef.items():
        lm = v["landmarks"]; T.append("| %s | %.2f | %.2f | %.2f | %.1f | %s |" % (k, lm["auricle_height_cm"], lm["tip_distance_from_root_cm"], lm["auricle_projection_cm"], lm["auricle_body_angle_deg"], " / ".join("%.2f" % t for t in lm["tip_lateral_back_up_cm"])))
    T += ["", "Ear checks: %s. 'construction input' rows confirm that a builder parameter encodes the canon direction; they are not independent measurements." % counts(EC), ""] + fmt_rows(EC)
    T += ["", "Attached (body frame, left ear): scale factor, auricle height, lateral extent from the skull root", "", "| Body | Family | Scale | Height (cm) | Lateral extent (cm) |", "|---|---|---|---|---|"]
    for b, r in EA.items(): T.append("| %s | %s | %.3f | %.2f | %.2f |" % (b, r["family"], r["l"]["scale"], r["l"]["auricle_height_cm"], r["l"]["lateral_extent_from_skull_root_cm"]))
    # orbit
    T += ["", "## 6. Landmark orbital-margin rings (O-1; `orbit/orbit_rings.json`)", "", "Source: " + OR["source"] + ". Placement: centre %.1f cm anterior of the globe centre, plane turned %.0f deg (BUILDER-CHOSEN)." % (OR["placement"]["forward_cm"], OR["placement"]["turn_deg"]), "",
          "| Body | Ring breadth × height (cm) | HL | HH | ORB breadth / HL | ORB height / HH | Ring inside skin (L / R) | Min clearance to globe (cm) |", "|---|---|---|---|---|---|---|---|"]
    for i in ("MF-M-R", "MF-F-R", "FN"):
        r = OR[i]; T.append("| %s | %.3f × %.3f | %.2f | %.2f | %s | %s | %.0f %% / %.0f %% | %.2f |" % (i, r["breadth_cm"], r["height_cm"], r["HL"], r["HH"], f4(r["ORB_breadth_over_HL"]), f4(r["ORB_height_over_HH"]), 100 * r["fit_l"]["ring_points_inside_skin_frac"], 100 * r["fit_r"]["ring_points_inside_skin_frac"], r["fit_l"]["min_clearance_to_globe_cm"]))
    u = OR["uncertainty"]; fv = OR["FN_vs_MF"]
    T += ["", "FN / MF-M-R (matched configuration): breadth ratio %.4f, height ratio %.4f at δ = %.2f. Normalisation uncertainty: HL %.2f %%, HH %.2f %% (%s). FN / MF-F-R: breadth %.4f, height %.4f." % (fv["breadth_ratio"], fv["height_ratio"], fv["delta"], 100 * u["HL_rel"], 100 * u["HH_rel"], u["note"], OR["FN"]["ORB_breadth_over_HL"] / OR["MF-F-R"]["ORB_breadth_over_HL"], OR["FN"]["ORB_height_over_HH"] / OR["MF-F-R"]["ORB_height_over_HH"])]
    # globe fit
    T += ["", "## 7. S-D3 adult-globe fit (`globe_fit_pkcg.json`)", "", "| Body | HH (cm) | Socket capacity (cm) | Capacity / HH | Skin verts inside a centred 2.2 / 2.3 / 2.4 cm globe | 2.3 cm / HH | Inter-ocular (cm) | Current landmark globe (cm) |", "|---|---|---|---|---|---|---|---|"]
    for i, r in GF.items():
        s = r["skin_verts_inside_at"]; T.append("| %s | %.2f | %.3f | %s | %d / %d / %d | %s | %.2f | %.3f |" % (i, r["HH"], r["socket_capacity_cm"], f4(r["capacity_over_HH"]), s["2.2"], s["2.3"], s["2.4"], f4(r["adult_globe_2.3_over_HH"]), r["interocular_cm"], r["landmark_globe_cm"]))
    # GO trial
    gt = jl(os.path.join(EV, "go_skin_trial_checks.json")); gcfg = jl(os.path.join(EV, "go_skin_trial_cfg.json"))
    T += ["", "## 8. GO skin-only trial (rejected; AD-G14 demonstration)", "", "bone_scales: " + "; ".join("%s %s" % kv for kv in gcfg["bone_scales"].items()) + ". GO rows with the trial body: %s." % counts(gt), ""] + fmt_rows([x for x in gt if dir_result(x) == "FAIL"])
    open(os.path.join(EV, "tables.md"), "w").write("\n".join(T) + "\n")
    # ARM records
    for i in REBUILT + CARRIED:
        m = meas(i); c = m["combined"]; cr = c["cranio"]
        geo = os.path.join(EV, "geometry", i + "_r6.npz") if i in REBUILT else (os.path.join(C1, "geometry", "HV_r6.npz") if i == "HV" else os.path.join(D1, "CG-NAT_r6.npz"))
        rigid = max(v["max_abs_change_cm"] for v in m["invariance"]["rigid_sets"].values())
        dc = checks_for(i, DC); wc = checks_for(i, WC); ec = [x for x in EC if x["cand"] in (CHK.get(i, i), i)]
        L = ["# RAC W1e ARM record — %s (%s)" % (i, NAME[i]), "", "Generated by `tools/rac/w1/gen_w1e_docs.py`. Order: `reviews/chatgpt-rac-w1d-author-decisions-continuation-order.md`.", "",
             "**Gate status: %s** (W1 candidate, not an accepted ARM). Skin readings are composition-inclusive diagnostics (PV-D16)." % STATUS[i], "",
             "- Geometry: `%s` (sha256 %s)%s" % (os.path.relpath(geo, R), sha(geo), "" if i in REBUILT else " — unchanged, carried forward"),
             "- Config: `tools/rac/w1/cfg/%s.json`" % ("w1e/" + i if i in REBUILT else ("HV" if i == "HV" else "w1e/CG-NAT")),
             "- Stature (R-6): %.2f cm; HH %.2f cm; HL %.2f cm; landmark globe %.3f cm" % (m["stature_r6"], cr["HH"], cr["HL"], cr["eye_diam_cm"]),
             "- Pose invariance: largest rigid-set change %.3f cm" % rigid,
             "- Ear family: %s" % (EAR[i] + " (`reviews/rac-w1e-evidence/ears/`)" if EAR[i] else "generator human auricle"), "", "## Verdict notes", ""]
        L += ["- " + s for s in V[i]]
        L += ["", "## Directional checks (%d: %s)" % (len(dc), counts(dc)), ""] + fmt_rows(dc)
        if wc: L += ["", "## Accepted pelvic / girdle / ALPC relations (%d: %s)" % (len(wc), counts(wc)), ""] + fmt_rows(wc)
        if ec: L += ["", "## Ear checks", ""] + fmt_rows(ec)
        L += ["", "## Key readings", "", "| Reading | %s | MF-M-R |" % i, "|---|---|---|"] + ["| %s | %s | %s |" % (k, f4(c["ratio"][k]), f4(mf[k])) for k in KEYS]
        open(os.path.join(ARM, "claude-rac-w1e-arm-%s.md" % i), "w").write("\n".join(L) + "\n")
    print("tables + %d ARM records" % len(REBUILT + CARRIED))

if __name__ == "__main__":
    main()

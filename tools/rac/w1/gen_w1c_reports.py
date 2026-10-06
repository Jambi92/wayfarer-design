"""Generate reviews/claude-rac-w1c-measurements.md and -cross-race-audit.md from the evidence (numbers pulled from JSON)."""
import json, os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
EV = os.path.join(R, "reviews", "rac-w1c-evidence")
ids = ["MF-M-R", "MF-F-R", "MF-FACE-PROJ-MAX", "SK", "SG", "FN", "AE", "VA", "HV", "DU", "GR", "GO", "PK", "CG"]
M = {i: json.load(open(os.path.join(EV, i + "_meas.json"))) for i in ids}
C = json.load(open(os.path.join(EV, "directional_checks.json")))
T = open(os.path.join(EV, "tables.md")).read()
sec = {m.group(1): m.group(2) for m in re.finditer(r"## (T\d) [^\n]*\n\n(.*?)(?=\n## T|\Z)", T, re.S)}
cr = lambda i, k: M[i]["combined"]["cranio"][k]
inv = lambda i: M[i]["invariance"]
def fmt(x): return "%.3f" % x
npass = sum(c["pass"] for c in C); fails = [(n, c) for n, c in enumerate(C, 1) if not c["pass"]]
marg = []
for n, c in enumerate(C, 1):
    if not c["pass"]: continue
    if isinstance(c["vb"], list): m = min(c["va"] - c["vb"][0], c["vb"][1] - c["va"]) / max(abs(c["va"]), 1e-9)
    elif c["op"].startswith("≈"): m = (0.010 - abs(c["va"] - c["vb"])) / 0.010
    else: m = abs(c["va"] - c["vb"]) / abs(c["vb"])
    if m < 0.01: marg.append((n, c, m))
def ck(cand, frag):
    return [c for c in C if c["cand"] == cand and frag in c["check"]][0]
pd = [inv(i)["trunk_cm"]["pelvic_depth"][2] for i in ids]; bt = [inv(i)["trunk_cm"]["bitrochanteric_breadth"][2] for i in ids]
meas = f"""# RAC W1 Continuation — Diagnostic Measurements

**Author:** Claude **Date / pass:** October 5, 2026, W1c pass 1 (after the independent audit corrections)

**Status:** **DIAGNOSTIC ONLY.**
- No value is canon, no envelope is adopted and no bound is moved.
- Every value is derived from **builder-chosen reference values that are not yet accepted** (REFERENCE_ANATOMY_V1 §7). Measuring these candidates confirms the builder's inputs; it cannot discover canon.

**Method:** `reviews/claude-rac-w1c-build-method.md`. Anatomy is read on the generator-authored rest geometry; shares use the R-6 stature.

**Raw data:**
- `reviews/rac-w1c-evidence/<ID>_meas.json`: full precision, rest and R-6 readings, ±3° pitch sensitivity, eye fit.
- `<ID>_inv.json`: rest vs R-6 invariance.

**Identification:**
- Pass W1c-1, October 5, 2026.
- Surface E-layer landmarks.
- Configuration 1 (MPFB gender 1.0) except MF-F-R.
- Geometry hashes are in each ARM record.

**Read with care:**
- **PK and CG are non-compliant uniform-scale proxies (R-2 FAIL).**
- FN, AE, VA, HV, DU, GR and GO are CONSTRAIN: their body proportions are measured, but their non-human ear and pelvis anatomy is not instantiated.

## 1. Shares and ratios (rest anatomy ÷ R-6 stature)

{sec['T1']}
## 2. Raw dimensions (cm; mean of left and right; the builds are mirrored, so see §4)

{sec['T2']}
## 3. Craniofacial (r3, E layer; body frame as the FH\\*-equivalent frame)

{sec['T3']}
**Notes:**
- **FAL** follows r3 L40 literally: the more anterior of subnasale and the soft-tissue alveolar point A'.
  - On every candidate it is subnasale.
  - An earlier draft took the anterior-most point of a 75 % upper-lip window. FAL then always fell on the window edge, so FPI was set by the window. That was replaced after the audit.
  - FPI moved by about −0.01 on every candidate: MF-M-R {fmt(cr('MF-M-R','FPI'))}.
- **Pr** is a method choice: the cutaneous upper lip at 75 % from subnasale to labrale superius. MPI depends on it.
- The orbit E-proxies are **low confidence**: they read a soft-tissue rim, not bone.
- The globe diameter is DER from the generator socket: 2.76–3.03 cm in SK, GR and GO (generator allometry; gate item) and 1.30–1.62 cm in the PK and CG proxies.
- The Po\\* proxy is the deepest concha point (no ear canal in the generator). The implied FH\\* tilt is reported, not used.

## 4. Left / right readings (cm)

{sec['T5']}
## 5. Pose-invariance readings that bear on measurement (rest → R-6)

- Joint-to-joint segment lengths are unchanged (≤ 2e-5 cm).
- Foot length changes +0.08 to +0.20 cm and foot breadth −0.05 to −0.21 cm.
- Head is unchanged except CG (HL {inv('CG')['head']['HL'][2]:+.4f} cm, from the proxy's rigid-set residual).
- **Pelvic depth changes {min(pd):+.2f} to {max(pd):+.2f} cm and bitrochanteric breadth {min(bt):+.2f} to {max(bt):+.2f} cm.** The gluteal and hip soft tissue moves when the thighs are re-aimed.
- **Maximum thorax breadth changes −0.84 to −3.22 cm** (axilla).

These are why anatomy is read on the rest geometry (gate D-W1c-1).

## 6. Items each candidate unlocks (W1 manifest) — status

| Item | Candidates | Status |
|---|---|---|
| RM-UB-07 (central, both configurations) | MF-M-R, MF-F-R | Measured (tables 1–2) |
| RM-LR-01 / 02 (ref) / 05 / 07 | MF-M-R, SK, GR, GO | Measured; directions in the audit. GR/GO pelvis and girdle not instantiated |
| RM-LR-06 (ALPC) | GO | **Not demonstrated** (qualitative; the evidence sheet reads lean) |
| RM-OT-01 | SG vs MF-M-R | Measured; all SG directions pass |
| RM-CF-02 (central + maximum) | MF-M-R / MF-F-R / MF-FACE-PROJ-MAX | FPI {fmt(cr('MF-M-R','FPI'))} / {fmt(cr('MF-F-R','FPI'))} / {fmt(cr('MF-FACE-PROJ-MAX','FPI'))} (maximum builder-chosen) |
| RM-CF-03 / 04 central face | GR, GO | FPI {fmt(cr('GR','FPI'))} / {fmt(cr('GO','FPI'))} vs MF {fmt(cr('MF-M-R','FPI'))} |
| RM-CF-06 (CBH) | DU, GO vs MF | CBH {fmt(cr('DU','CBH'))} / {fmt(cr('GO','CBH'))} vs {fmt(cr('MF-M-R','CBH'))}; TBP not run (no Go / Ec–Ec landmark set) |
| RM-CF-07 (FVB with MVI) | GR, AE, SK, MF | Table 3; audit |
| RM-CF-08 (ORB, aperture) | FN | **Not demonstrated:** ORB breadth ÷ HL {fmt(cr('FN','ORB_breadth_over_HL'))} vs MF {fmt(cr('MF-M-R','ORB_breadth_over_HL'))} (lower), ORB height ÷ HH {fmt(cr('FN','ORB_height_over_HH'))} vs {fmt(cr('MF-M-R','ORB_height_over_HH'))} (higher); aperture more open |
| RM-CF-10 / RM-SR-04 (HSR) | DU, GR, GO, PK\\*, CG\\* | HH ÷ H in table 1 (\\* proxies); CG HH {cr('CG','HH'):.2f} cm |
| RM-UF-01 (MF aperture vs orbit) | MF-M-R | Aperture {M['MF-M-R']['combined']['cranio']['aperture']['l']['width']:.2f} × {M['MF-M-R']['combined']['cranio']['aperture']['l']['height']:.2f} cm; ratios in table 3 |
| RM-UB-01 | SK, SG, FN, AE, VA, HV, DU | Measured (table 1). **SA blocked** (no verified D-2 copy) |
| RM-UB-06 (PK pelvis) | PK\\* | Proxy only; pelvis morphology OPEN |
| RM-SR-01 / 02 / 03 | PK\\*, CG\\*, DU | Proxies for PK and CG; DU measured |

— Claude
"""
open(os.path.join(R, "reviews", "claude-rac-w1c-measurements.md"), "w").write(meas)
ml = "\n".join("| %d | %s | %s | %.2f %% |" % (n, c["cand"], c["check"], 100 * m) for n, c, m in marg)
fl = "\n".join("| %d | %s | %s | %s | %.4f %s %.4f |" % (n, c["cand"], c["check"], c["canon"], c["va"], c["op"], c["vb"]) for n, c in fails)
grp = ck("GR", "projection")
aud = f"""# RAC W1 Continuation — Cross-Race Audit

**Author:** Claude **Date:** October 5, 2026 **Status:** DIAGNOSTIC

**Result: {npass} of {len(C)} directional checks pass on the final candidates; {len(fails)} fail.**

**Read with care:**
1. **§7 circularity.** The candidates were built and then **corrected until these canon directions held**. That took six rounds, plus one more after the independent audit. A pass shows that the builder-chosen inputs instantiate canon. It is not independent evidence about the races.
2. **{len(marg)} passes are marginal** (relative margin under 1 %, inside landmark uncertainty), so they count as not demonstrated.
3. **The check set is not exhaustive.** The independent audit found directions the first check set had missed: AE hands and feet, FN feet, DU arm contribution, VA leg share vs AE, and AE neck vs VA. It also found that AE, FN and DU **failed** some of them. Those candidates were rebuilt, and the checks are now included. **Other canon directions may still be untested.** The author pass should treat this list as a minimum.
4. **PK and CG checks run on non-compliant proxies.**
5. **"≈" checks** all use one declared tolerance of ±0.010 in ratio units. This is a method choice. An earlier draft silently used ±0.050 on one AE check; that was removed, and AE was rebuilt.

## 1. Failing checks

| # | Candidate | Check | Source | Value |
|---|---|---|---|---|
{fl}

## 2. §7 checks — summary

| §7 check | Outcome |
|---|---|
| Marchfolk as normalized human comparator | MF-M-R / MF-F-R native at 173 cm; one-configuration races paired with MF-M-R |
| Skarn vs Marchfolk robustness/power | All SK directions pass |
| Sagekin vs Marchfolk linearity, hands, ribcage | All SG directions pass; "never elven" (SG L435) has no numeric test |
| Fenn vs Aelari vs Vael elf separation | Body directions pass. **FN bony orbit not demonstrated** (§1). **Ears not instantiated**, so head separation is untested |
| Durrim vs Pipkin vs Cogling short-race identity | DU directions pass, including lower arm contribution after the rebuild. PK/CG proxy directions pass; structural-mass axis CG < PK < DU |
| Skarn vs Grask vs Gorrund large-race identity | GR limb-dominant; GO torso > GR, limbs < GR, deepest thorax, joints > GR. **SK vs GO and SK vs GR depth/joints: no pass condition (AD-4, AD-R15)** |
| Grask central projection ≈ Marchfolk; vertical midface | FPI GR {grp['va']:.3f} vs MF {grp['vb']:.3f}; FVB and MVI > MF and SK |
| Gorrund projection comparator | FPI GO {fmt(cr('GO','FPI'))} vs MF central {fmt(cr('MF-M-R','FPI'))} and MF maximum {fmt(cr('MF-FACE-PROJ-MAX','FPI'))}. Inside the MF range, but that range rests on a builder-chosen maximum |
| Halvren no-lineage, source-plausible, not 50/50 | Ratios inside the MF–SG–FN–AE–VA span. **Order deviation:** the sources are CONSTRAIN, not PASS. "Not 50/50" has no numeric test |
| Saurin outside the human rostral range; tail mandatory | MF-FACE-PROJ-MAX FPI {fmt(cr('MF-FACE-PROJ-MAX','FPI'))} < Saurin coupled corner 0.292 (r3) and < centre 0.325. The required margin is RM-CF-05 (author). Tail: W1 pass 1 PASS |
| Not tested | PK span (RA L131: "no racial span tendency"; not a direction). PK span ÷ H {M['PK']['combined']['ratio']['span_der']:.3f} vs MF {M['MF-M-R']['combined']['ratio']['span_der']:.3f} — reported only |

## 3. Marginal passes (not demonstrated)

| # | Candidate | Check | Relative margin |
|---|---|---|---|
{ml}

## 4. All checks

{sec['T4']}
— Claude
"""
open(os.path.join(R, "reviews", "claude-rac-w1c-cross-race-audit.md"), "w").write(aud)
print("ok", npass, len(C), len(marg), len(fails))

# RAC W3A1 — Halvren tail canonicalization and closure — FINAL CLOSURE REPORT

**Order:** `reviews/chatgpt-rac-w3a1-halvren-tail-closure-order.md` (W3A author ruling, AD-W3A-1…4)
**Author:** Claude (closure pass; returned for ChatGPT author review)
**Evidence:** `reviews/rac-w3a1-hv-evidence/` · drivers `tools/rac/w1/w3a1_drivers/` · cfg `tools/rac/w1/cfg/w3a/HV-tails.json` (`w3a1` section)
**Builds:** 83 new generator bodies; 49 new skeletal-proxy grids; 1,484 evaluator checks. Everything builds on the accepted W2G / W3A machinery, unchanged.

---

## 0. Verdicts (§10)

| Item | Verdict |
|---|---|
| **AD-W3A-1 source-conditioned leg-development coupling** | **PASS** |
| **AD-W3A-2 lower-tail bound-limited ruling** | **PASS** |
| **AD-W3A-3 boundary-stature coherence rule** | **PASS** |
| **AD-W3A-4 source-duplicate hidden validity rule** | **PASS** |
| **HV-49 lower tail** | **FINAL ACCEPT** (bound-limited, as ruled) |
| **HV-50 Skarn-supported upper tail** | **FINAL ACCEPT** |
| **HV-50 Aelari-supported upper tail** | **FINAL ACCEPT** |
| **RM-OT-03 source-passing result** | **FINAL ACCEPT** (with the stated sample-size limits) |
| **RM-UB-05 reachability portion** | **FINAL ACCEPT** |
| **RM-UB-05 frequency portion** | **CLOSED AS NAMED DEPENDENCY.** The frequencies themselves stay OPEN (§7). |
| **W3A Halvren overall** | **FINAL ACCEPT** |

**Required statements**
- **Final demonstrated lower reach:** **147.2 cm** (Marchfolk-supported; unchanged from W3A). 147 cm stays excluded by H-5. No biological minimum was discovered, and 147.2 cm is not a species minimum.
- **Final demonstrated Skarn-supported upper reach:** **228.8 cm**, on the coupled system. Every class tested passes: Skarn-expressed, central anatomy, and Skarn + Aelari. 229 cm stays excluded (H-5).
- **Final demonstrated Aelari-supported upper reach:** **221.0 cm**. This is the valid Aelari adult maximum, so Aelari support stops at its source ceiling and is not extrapolated.
- **Resolved coupling method:** §1.
- **Continuity evidence:** §2.
- **Central-range source-duplication result:** §5.
- **Sample accounting:** §4–§6.
- **Caveats:** every MARGINAL, NOT DEMONSTRATED, REPORT-only and NOT RUN item is in §9.
- **Persistent files changed:** §11.
- **Prior Halvren or source-population canon reopened:** **none** (§10).

---

## 1. AD-W3A-1 — resolved developmental-coupling method

This is a hidden Halvren developmental dependency. It is not a control, not a percentage, and not visible genealogy.

- **When it operates:** only above the central envelope (h > 213 cm), and only for the source that supplies the tail stature under H-1:
  - Skarn up to 229 cm;
  - Aelari up to 221 cm;
  - in a Skarn + Aelari body, Skarn supplies the stature through the whole upper tail. Aelari's anatomy is kept, but Aelari is never credited with stature support above 221 cm.
- **What it carries:** only the source's *stature-relevant* leg-segment development, and only as a partial interpolation:
  - **Skarn:** the accepted short-femur development. The signed femur-length system is interpolated from whatever the Halvren already carries toward the Skarn value: v = (1 − k)·v₀ + k·(−1.0).
  - **Aelari:** the accepted W1m thigh / calf development (thigh 1 − 0.0125 k, calf 1 + 0.0523 k).
  - **Not carried:** Skarn girth (leg horizontal / depth scales), the Skarn or Aelari torso and joint systems beyond the canon-named HV-13…17 expression, and the Aelari pelvis, spine or neck scales.
- **Strength:** k_s(h) = min(1, β_s · (h − 213 cm)).
  - The rule is continuous, zero at the central ceiling, and monotone in stature.
  - The source decides which development is carried; stature decides how much.
- **How the rate is chosen ("smallest coherent"):** β_s is the smallest linear rate that keeps the most demanding supported class (central Halvren anatomy) at or above the Halvren's own accepted lower-leg share at the top of its central envelope. That target is HV213, shin / leg 0.4804. The boundary-stature span floor (SG208) is 0.4799.
  - The rates come from the W3A responses at k = 0 and k = 0.5: Skarn −dL/dk 0.025–0.026, Aelari 0.0176.
  - Result: **β_SK = 0.030 / cm** (k = 0.474 at 228.8 cm) and **β_AE = 0.052 / cm** (k = 0.417 at 221 cm).
  - These are **diagnostic construction parameters, not species constants**. The W3A half-strength probe value (0.5) is not used.

| Body | k | shin / leg | leg share | Matched supporting source shin / leg | Separating readings (of 17 or 24) vs matched Skarn / Aelari |
|---|---|---|---|---|---|
| HV213 (W2G, uncoupled) | 0 | 0.4804 | 0.5522 | — | — |
| HU215Sc | 0.060 | 0.4810 | 0.5473 | SK 0.5026 | 17/17 · 13/17 |
| HU221Sc | 0.240 | 0.4808 | 0.5471 | SK 0.4969 | 23/24 · 20/24 |
| HU225Sc | 0.360 | 0.4807 | 0.5469 | SK 0.4933 | 23/24 · 21/24 (D1) |
| **HU228.8Sc** | 0.474 | **0.4806** | 0.5468 | SK 0.4900 | **22/24 · 22/24 (D1)** |
| **HU228.8Cc** (central anatomy) | 0.474 | **0.4801** | 0.5512 | SK 0.4900 | 20/24 · 16/24 (D1) |
| **HU228.8SAc** | 0.474 | **0.4833** | 0.5433 | SK 0.4900 | 23/24 · 19/24 (D1) |
| HU215Ac | 0.105 | 0.4802 | 0.5518 | AE 0.4928 | 16/17 · 10/17 |
| HU220.8Ac | 0.405 | 0.4810 | 0.5547 | AE 0.4883 | 23/24 · 16/24 |
| **HU221Ac** | 0.417 | **0.4810** | 0.5549 | AE 0.4881 | **23/24 · 16/24** |
| HU221Ca (central anatomy, Aelari-supported) | 0.415 | 0.4814 | 0.5562 | AE 0.4881 | 16/17 · 11/17 |

The W3A uncoupled values at 228.8 cm were: central 0.4684, Skarn-expressed 0.4688, Skarn + Aelari 0.4686, all FAIL. Aelari-expressed at 220.8 cm was 0.4738, FAIL.

**Results**
- **Coherence:** every coupled body passes all 8 scored readings inside the boundary-stature span: 21 bodies, 168 PASS, 0 MARGINAL, 0 FAIL.
- **No source copying:** every coupled body stays below its supporting source's lower-leg share (21/21 PASS). The coupling holds the Halvren near its own 213 cm value rather than moving it to Skarn or Aelari proportions.
- **Halvren identity:** the coupling does not change torso, arm, joint or thorax identity. Against matched Skarn the knee / segment reads −16 to −28 % and the wrist / segment −17 %. Against Aelari, the crest, thoracic-depth and neck separations persist.
- **Skarn + Aelari:** this body sits slightly above the minimum (0.483). Aelari's named systems already lengthen its lower leg, and it receives the same Skarn rate. This is reported, not tuned.

## 2. Continuity evidence (§2.1, §7A)

- **Coupling onset at 213 cm** (k = 0): HV213 → HU215Cc, HU213S → HU215Sc and HU213A → HU215Ac all hold every tested length, share and joint reading within 1 % (30/30 PASS; maximum step 0.66 %).
- **Stature series** (`C` rows, 187 PASS):
  - HV-Cc: HV190 → … → HV213 → 215 → 217 → 221 → 225 → 228.8;
  - HV-Sc: 213 → 215 → … → 228.8, in 2 cm steps;
  - HV-Ac: 213 → 215 → 217 → 219 → 220.8 → 221;
  - HV-SAc: 221 → 225 → 228.8.
- **No segment reversal or joint inversion** appears in any coupled series.
  - Femur / leg changes ≤ 0.02 % per step.
  - Knee / segment changes ≤ 0.6 % per step.
  - The larger HV190 → HV203 → HV213 steps are the accepted W2G central series (10–13 cm intervals).
- **Coupling-strength sweep** at 228.8 cm (k = 0, 0.25, 0.474, 0.5, 0.75, 1.0) is monotone and close to linear:
  - shin / leg 0.4688 → 0.4750 → 0.4806 → 0.4813 → 0.4876 → 0.4940;
  - knee / segment +2.0 to +2.4 % per 0.25 k.
  - At **k = 1.0** the Halvren lower leg would *exceed* Skarn's (0.4940 vs 0.4900). This shows why the rule must stay partial. The rule never goes above k = 0.474.
- **One measurement artifact is carried, not new:** the skin thoracic-breadth station step at 219 → 221 cm (Sc −3.1 %, Cc −2.2 %, SAc −3.2 %). The same step appears in the Skarn source family (SK208 → 215 −4.6 %), and skeletal thoracic breadth is smooth. The W3A §9 classification applies unchanged.
- **No new route junction.** The upper tail stays on the macro route. The W2G native ↔ macro junction (163 → 173 cm) remains the carried creator-interpolation dependency.

## 3. Endpoint stress (§7B)

Narrow and Broad frames plus LOWMUS, HIMUS, LOWFAT and HIFAT composition were built at HU228.8Sc, HU221Ac and HU228.8SAc. Balanced is the reference body.
- **Frames:**
  - All 30 breadth rows move by at least 1 % in the correct direction.
  - All 60 length rows hold within 0.5 %, including shin / leg and femur / leg, so the coupling does not depend on frame.
  - All 24 joint-scale rows hold within 1 %.
  - All 6 framed bodies stay inside the boundary-stature span (48/48 rows).
  - All 12 framed source-protection rows PASS: 21–24/24 vs Skarn, 17–22/24 vs Aelari.
- **Composition:**
  - All 12 invariance rows PASS: proportions and coupling are unchanged within 1 %.
  - All 12 same-composition source-protection rows PASS: 17/17 vs same-composition Skarn 228.8, 9–11/17 vs same-composition Aelari 221.
- **Collision guards:**
  - **Q6:** Broad Halvren vs Broad Skarn 22/24 separate; high-muscle Halvren vs high-muscle Skarn 17/17.
  - **Q7:** Narrow Halvren vs Aelari 221 17–22/24, vs Narrow Aelari 221 16–22/24; low-fat Halvren vs low-fat Aelari 11/17.

The coupling is independent of frame and composition. The settled W3A stress matrices were not rerun.

## 4. AD-W3A-4 — hidden complete-body validity rule; lower-tail re-evaluation (§7C)

**Rule as implemented** (`w3a1_rs.py`): after neutralization, the body is compared with every valid source population at matched height using the 24-reading complete-body protocol (13 skin, 4 exact-plane joint, 7 skeletal-proxy readings).
- A reading counts as separating when it differs by at least 1 %.
- **Near-duplicate:** fewer than 2 readings separate. Under the rule, a near-duplicate is **INVALID**.
- **Ambiguous:** 2–3 readings separate. **VALID.**
- **Distinct:** 4 or more readings separate. **VALID.**
- Comparisons with endpoint sources are never grounds for rejection.
- No coordinate threshold is used anywhere.

**W3A lower-tail samples** (n = 68). All 22 that W3A had classed as near-duplicate or ambiguous were re-gridded and scored on the full 24 readings.

| W3A class (17 readings) | n | Now INVALID (duplicate) | Now valid, ambiguous | Now valid, distinct |
|---|---|---|---|---|
| near-duplicate | 9 | **5** (RLMF11, RLMF23, RLMF24, VLMF0, VLMF5) | 4 (RLMF06, RLMF50, RLMF54, VLMF1) | 0 |
| ambiguous | 13 | 0 | 9 | 4 (RLMF09, RLMF20, RLMF34, RLMF52) |
| distinct | 46 | 0 | 0 | 46 (17-reading separation ≥ 4 can only grow with 24) |
| **Total** | **68** | **5 rejected (7.4 %; 95 % CI ≈ 3–16 %)** | **13 valid ambiguous** | **50 valid distinct** |

- **Four W3A near-duplicates are now valid.** On the full protocol, skeletal pelvic vertical and thoracic depth separate them from Marchfolk. The 17-reading call was conservative, as W3A stated.
- **The rejected five** sit at hidden Marchfolk coordinates 0.82–0.93. The criterion is still the anatomy result, not that coordinate.
- **No new failure appeared.** Every rejection is against Marchfolk. There are 0 near-duplicates of Fenn, Vael, Sagekin, Skarn or Aelari, and 0 adult-read failures.
- **The lower-tail reachable result does not change.** HL147.2C separates 10/24 from matched Marchfolk, and the Marchfolk-expressed HL147.2M 4/24 (distinct), so both stay valid.

## 5. Focused central native-range confirmation (§5.1, §7D)

The native route was run at **152, 157 and 163 cm**, with Marchfolk expression 0.6, 0.8, 0.9 and 1.0, against matched Marchfolk (MF152, MF157 built in W3A1, MF163), on the full 24 readings.

| Marchfolk expression | 152 cm | 157 cm | 163 cm |
|---|---|---|---|
| 0.6 | 2/24 ambiguous, **valid** | 2/24 **valid** | 2/24 **valid** |
| 0.8 | 1/24 near-duplicate, **INVALID** | 1/24 **INVALID** | 1/24 **INVALID** |
| 0.9 | 1/24 **INVALID** | 1/24 **INVALID** | 1/24 **INVALID** |
| 1.0 | 3/24 ambiguous, **valid** | 3/24 **valid** | 3/24 **valid** |

- **Confirmed.** The rule catches the same duplication in the native central range. As W3A predicted, the behaviour does not change with stature; the result is identical at all three statures.
- **Strongly Marchfolk-leaning Halvren survive.** At 0.6 and at full expression (1.0) they are ambiguous and valid. At 1.0 the shin share and knee / ankle sections diverge from Marchfolk.
- **The pattern argues for an anatomy rule.** Duplication is not monotone in the hidden coordinate, so a coordinate cutoff would be wrong. The author's ruling to judge the anatomy result is supported directly.
- **Against all other sources** (matched or endpoint) these bodies separate 9–22/24. Vael at 9 is the closest.
- **No central-envelope redesign is required.** W2G central anatomy was not touched. The duplicate corner exists only under extreme hidden Marchfolk expression, and the validity rule rejects those outputs.

## 6. Upper-tail source protection under the coupling (§7A)

The 16 W3A RM-OT-03 upper samples with the strongest supporting-source coordinate were rebuilt under the coupling: 8 Skarn-supported, 4 Aelari-supported and 4 Skarn + Aelari.
- **All 16 are valid and distinct.** There are 0 near-duplicates and 0 ambiguous bodies against any source.
- **Minimum separations:** vs Skarn 16–17/17, vs Aelari 9–16/17.
- The coupled and uncoupled twins differ by 0–2 readings vs the supporting source (for example U-AE vs Aelari 9 → 9, 10 → 9).

The other 96 W3A upper samples were not rebuilt. Their W3A result was 0/112 duplicates, with a minimum separation of 8 readings vs Aelari and 15 vs Skarn, and the coupling moves the supporting-source separation by at most 2 readings. That is the basis for carrying them.

**RM-OT-03 final accounting (real builds, 196 bodies):**

| Group | n | Rejected | Valid ambiguous | Valid distinct |
|---|---|---|---|---|
| Lower tail | 68 | 5 | 13 | 50 |
| Upper tail, W3A uncoupled | 112 | 0 | 0 | 112 |
| Upper tail, coupled recheck | 16 | 0 | 0 | 16 |
| Central confirmation | 12 | 6 | 6 | 0 |

Rates are conditional on the coverage design. They are not prevalence (§7).

## 7. RM-UB-05 frequency firewall (§6)

1. **Biological reachability:** established. Lower 147.2 cm (bound-limited); Skarn upper 228.8 cm; Aelari upper 221.0 cm (source cap).
2. **Conditional developmental validity:** established inside each tail class (§4–§6).
3. **Population-wide frequency:** **not identifiable.** No within-class stature-development distribution and no Halvren genealogy-prevalence model exists.
   - Exact lower and upper frequencies stay OPEN, and so does the lower-vs-upper ordering.
   - Equal source prevalence was not assumed.
   - Diagnostic coordinates and creator randomization are not demography.

**Canon carries only the structural rule:** tails are minority outcomes relative to 152–213 cm and require the appropriate supporting-source development condition. Tail randomization weights stay deferred.

## 8. Canonicalization (§8)

`specs/halvren/HALVREN_V1.md` gets a W3A1 block under the stature-tail authorship, plus the HV-49 / HV-50 rows and the height summary row. It separates three kinds of statement:
- **Canon / accepted design rules:** the 152–213 cm central envelope; conditional tails; lower tail Marchfolk-supported; upper tail Skarn- and Aelari-supported within each source's valid stature; above 221 cm only Skarn supports stature; source-supported exceptional stature may carry the source-linked leg-segment development needed for coherence, as Halvren mixed development and not copied source anatomy; generated Halvren source duplicates are invalid under the hidden complete-body rule; ambiguous source-leaning Halvren stay valid; no ancestry-percentage UI; tails are minority outcomes.
- **Diagnostic / measurement evidence (not canon numbers):**
  - 147.2 cm demonstrated lower body;
  - 228.8 cm demonstrated Skarn-supported body;
  - 221.0 cm demonstrated Aelari-supported body;
  - β_SK, β_AE, the HV213 target, every k, coordinate and measurement.
- **Still OPEN:** the true biological lower minimum above H-5; genealogy-conditioned stature distributions; genealogy prevalence; exact tail frequencies; creator randomization weights; runtime interpolation and clamping; UE5.

UCCA_V1 (RM-UB-05 bullet) and REFERENCE_ANATOMY_V1 (W3 row) get one-line pointers. No numeric construction parameter was promoted to a species constant.

## 9. MARGINAL / NOT DEMONSTRATED / REPORT-only / NOT RUN

- **MARGINAL:** none.
- **NOT DEMONSTRATED:**
  - a true biological lower minimum (bound-limited, as ruled);
  - any Skarn-supported reach at or above 229 cm (excluded by authorship, not tested);
  - Aelari support above 221 cm (excluded source-first).
- **REPORT-only:**
  - **G rows** (accepted W1 Halvren directional rows at fixed W1 173 cm references) at the three coupled endpoints are NOT ALL PASS, as at every tail endpoint in W3A. These rows are not stature-matched. The stature-matched boundary-stature span governs (AD-W3A-3).
  - The **matched-supporting-source-only span** (diagnostic source-relationship report). Coupled bodies sit below the Skarn / Aelari lower-leg interval. This is expected and is not a fail under AD-W3A-3.
  - **Skarn guard (K) rows.**
  - **k = 0.75 and k = 1.0** sweep points (beyond the rule; still distinct, 14/17).
  - Composition bodies vs reference-composition sources.
  - Narrow bodies vs Fenn 211.
  - The SAc lower-leg share above the minimum target (0.483).
  - The thoracic-breadth skin-station artifact (§2).
- **NOT RUN:**
  - skeletal-proxy grids for the non-endpoint coupled family bodies, so their protocol uses 17 readings (conservative);
  - 42 K skeletal guard rows on those bodies;
  - the 16 coupled upper samples were scored on 17 readings;
  - the 96 remaining W3A upper samples were not rebuilt under the coupling (justified in §6);
  - stress at points other than the three final endpoints;
  - the central confirmation used pure Marchfolk expression only (by design; the order said not to broaden it).

## 10. Collision / canon audit (§9)

| Reference | Result |
|---|---|
| HALVREN_V1 | Consistent. Central envelope intact. H-4 mixed development is satisfied by a partial coupling. The system-level "exact source duplication prevented" rule is implemented as AD-W3A-4. No ancestry slider. |
| H-1…H-6 | **H-1:** coupling only from the supporting source; Fenn / Vael / Sagekin controls unchanged from W3A. **H-2:** lower tail 4.8 cm vs upper 15.8 cm (Skarn) / 8 cm (Aelari). **H-3:** protection holds at every point. **H-4:** whole-body coherence. **H-5:** 147 < tail < 229 cm. **H-6:** structural minority only. |
| UCCA_V1 | No player-facing control. Frame and composition stay independent of ancestry (§3). No hard clip at 152 / 213 cm. |
| REFERENCE_ANATOMY_V1 | Measurement method unchanged. Results are recorded as diagnostic evidence. |
| Marchfolk / Skarn / Aelari W2 | Used as accepted. The coupling borrows only accepted Skarn / Aelari leg rules, and no source body was changed. |
| Fenn / Vael / Sagekin ranges | Unchanged negative controls. Neither tail is extended. |
| W2G Halvren closure | Unchanged. The central range was confirmed, not redesigned. |
| D1–D3 | Aelari 221 cm is used only as a D1 endpoint above its range. |
| No-ancestry-slider rule | Kept. k is hidden and stature-driven. |
| Frame / composition independence | Demonstrated at the coupled endpoints (§3). |

**No contradiction found, and no prior accepted race canon was reopened.**

## 11. Persistent files changed

- `reviews/claude-rac-w3a1-halvren-tail-final-closure-report.md` (this report)
- `reviews/rac-w3a1-hv-evidence/` (README, w3a1.json, spec.json, registry.json, construction.json, joint_sections.json, rs.json, sheets/)
- `tools/rac/w1/w3a1_drivers/`: w3a1_build.py, w3a1_post.py, w3a1_reg.py, w3a1_spec.py, w3a1_rs.py, render_AS_RUN.sh, AS_RUN.sh
- `tools/rac/w1/cfg/w3a/HV-tails.json` (`w3a1` section)
- `specs/halvren/HALVREN_V1.md` (W3A1 tail-closure block; HV-49 / HV-50 rows; height summary row)
- `decisions/UCCA_V1.md` (RM-UB-05 pointer)
- `decisions/REFERENCE_ANATOMY_V1.md` (W3 row pointer)
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md` (status lines)

## 12. Stop

W3A1 stops here. Nothing else was started: no Saurin RM-UF-03 / RM-UF-04 / RM-UB-08, RM-CF-09, RM-CF-05, RM-UF-05, roster-wide review, creator, UE5, rigging, animation, equipment or gameplay work.

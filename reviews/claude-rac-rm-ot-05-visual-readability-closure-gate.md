# RAC RM-OT-05 — neutralized racial-readability closure gate

**Order:** `reviews/chatgpt-rac-rm-ot-05-visual-readability-correction-order.md`
**Source gate:** `reviews/claude-rac-rm-ot-05-world-scale-author-gate.md`
**Evidence:** `reviews/rac-rmot05-evidence/readability/`:
- 41 sheets;
- `blind_key.json`, `blind_scores.json`;
- `probes.json`, `sagekin_c2.json`.

**Reference-asset manifest:** `reviews/reference-assets/` (`manifest.json`, `r6/`, `builds/`).
**Drivers:** `tools/rac/w1/rmot05_drivers/` — `ot05r_package.py`, `ot05r_blind.py`, `ot05r_probes.py`, `ot05r_probe_sheet.py`.

---

## 0. Verdicts

| Item | Verdict |
|---|---|
| **RM-OT-05 numeric / stature register** | **ACCEPTED IN PRINCIPLE** (unchanged) |
| **Grask current neutralized body readability** | **FAIL.** With head / neck removed, the accepted reference and its frame / composition states read as a **tall, slender human**: longer legs and forearms, narrower girdle. That is exactly the GRASK L99 failure ("looks like a very tall thin human"). The canon-named non-human scapular and pelvic organization (GR-G2, GR-P2b / P3) is not visible in the surface. |
| **Gorrund current neutralized body readability** | **FAIL.** Body-only, it reads as a **broad, heavy tall human**. Breadth and depth are present, but joint presence, axial load-path continuity and pelvic integration do not read as a distinct non-human architecture (GORRUND L11, L86, L147). In the blind test the Gorrund reference was assigned to human-family, and Broad Skarn was assigned to Gorrund. |
| **Grask vs Gorrund contrast** | **CONSTRAIN.** They are always told apart from each other, but the contrast is essentially **thin vs broad**. It is not reach-dominant vs axial / load-bearing architecture. |
| **Wide-lineup presentation was the main problem** | **NO.** The 4 px / cm full-roster sheet compressed detail, but the matched close views (front, profile, front 3/4, rear 3/4), body-only views and silhouettes at 208 / 218 / 229 show the same human read. |
| **Geometry changed** | **NO** for every accepted asset. Diagnostic correction probes were built (§3) and are not promoted. |
| **Canonical directions used (probes only)** | **Grask:** torso contribution down; forearm and upper-arm contribution up; femur slightly down at held stature; large integrated hands and feet (GRASK L54, L59, L164–174, L233–253; inside the accepted GR-BODY-11 valid-extreme region). **Gorrund:** joint structural presence (knee / ankle / wrist / elbow); long-bone cross-section; proximal femur; thoracic depth; lower-trunk continuity; larger hands and feet (GORRUND L19, L63, L74–76, L179–189; ALPC). |
| **Every affected validator rerun** | No accepted geometry changed, so no accepted W2 validator was invalidated. Probes were measured on the skin layer only (`probes.json`). The full W2C / W2D chain (CIB, skeletal proxy, ALPC, contour clearance) was **not** rerun on probes because they are not candidates for promotion (§3). |
| **Any accepted W2 relationship broken** | **NO** |
| **Sagekin configuration-2 152 / 208** | **PASS.** SGF152-NAT (152.00 cm, native route) and SGF208 (208.01 cm, macro route) were built on the accepted routes. Every configuration-1 Sagekin-vs-Marchfolk direction replicates in configuration 2 with near-identical magnitude (§4). Full W2E skeletal-proxy chain not rerun. |
| **Cogling 76 cm corrected head ≥ 11.0 cm** | **PASS.** CG76H-NAT: head height **11.04 cm** (was 10.91), stature 76.00. Body unchanged outside head / neck (≤ 0.08 cm). Anti-juvenile and short-race checks pass (§5). It is a candidate pending author acceptance as the canonical 76 cm body. |
| **Gorrund 229 nominal / 230.9 ARM bookkeeping recorded** | **YES** (GORRUND_V1 status block; REFERENCE_ANATOMY R-2) |
| **Gorrund 251 current upper-end qualifier preserved** | **YES** (GORRUND_V1: current world-validation / creator upper end, not a permanent maximum) |
| **Halvren frequency remains OPEN** | **YES** (no distribution inferred from reach bodies) |
| **Later-wave accepted reference geometries committed** | **YES.** 49 R-6 assets with build / measurement records, SHA-256 and provenance in `reviews/reference-assets/manifest.json`. RM-OT-05 candidates are flagged PENDING AUTHOR. Skarn C1R faces and the Saurin canonical-asset location are pointed to. |
| **Race-spec stature writeback ready** | **YES**, drafted in §6 and **not applied**. Per D4 it waits for RM-OT-05 final closure, which this readability FAIL blocks. |
| **Contradictions requiring author decision** | §7 (one structural: the large-race reference realizations vs the neutralized-readability canon) |

---

## 1. Neutralized large-race package

All bodies are the current accepted ones:
- Marchfolk 203: the Marchfolk maximum, shown at the 208 slot as an endpoint; 208+ is not valid for Marchfolk.
- Skarn: SK208-C1R, SKM218, SKM229-C1R.
- Grask: GR208, GR218R, GR229.
- Gorrund: GO208, GO218, GO229.

Presentation:
- matched ground, orthographic scale (3 px / cm), stature, R-6 stance and reference composition;
- one grey material.

Sheets, at each of 208, 218 and 229 cm, `r_<H>_<view>_<mode>.jpg`:

| View | Neutral grey | Body only (head and neck removed by skin weight) | Black silhouette, body only |
|---|---|---|---|
| front (F) | ✓ | ✓ | ✓ |
| profile (P) | ✓ | ✓ | ✓ |
| front 3/4 (Q) | ✓ | ✓ | ✓ |
| rear 3/4 (RQ) | ✓ | ✓ | ✓ |

A skeletal-proxy overlay was not added: the CIB proxies already exist in W2C / W2D evidence and would not change the surface read.

**Measured ratios at matched height** (accepted W2 measurements, skin layer). They are real, but small for a "non-human architecture" read:

| Ratio | Marchfolk 203 | Skarn 208 | Grask 208 | Gorrund 208 |
|---|---|---|---|---|
| torso share | 0.278 | 0.296 | **0.266** | 0.304 |
| leg share | 0.545 | 0.524 | **0.561** | 0.517 |
| arm share | 0.410 | 0.402 | **0.432** | 0.369 |
| forearm ÷ arm | 0.362 | 0.355 | **0.381** | 0.363 |
| shoulder breadth share | 0.261 | 0.282 | 0.248 | 0.287 |
| thorax breadth share | 0.170 | 0.181 | 0.163 | **0.200** |
| thorax depth ÷ breadth | 0.736 | 0.785 | 0.753 | **0.839** |
| crest share | 0.159 | 0.165 | 0.150 | **0.192** |
| pelvic depth share | 0.125 | 0.129 | 0.124 | **0.149** |
| knee ÷ femur | 0.208 | 0.292 | 0.253 | 0.289 |
| hand / foot share | 0.111 / 0.150 | 0.118 / 0.161 | 0.119 / **0.147** | 0.109 / 0.151 |

**The question in each comparison was whether the canon-named non-human architecture is visible, not just the difference in proportion.**

### 1.1 Grask vs Skarn / Marchfolk (head removed)

1. *Different skeletal organization rather than a tall thin human?*
   **No.** The read is a slender, long-legged human. Torso −10 % vs Skarn and limbs +7 % are visible together, but they look like a stretched human proportion set, not a different girdle / pelvis organization.
2. *Lower leg, femur / lower-leg relation, arm, forearm, torso, shoulder origin and pelvis organization visible together?*
   - Leg, arm and forearm lengths: yes.
   - Shoulder origin and pelvis organization: **no**. The MPFB surface keeps a human pectoral / deltoid girdle and a human iliac / gluteal pelvis surface.
   - Hands and feet: absolute hands are about equal to Skarn, and **feet are smaller than Skarn** (foot share 0.147 vs 0.161). That works against GRASK L62 / L253, "large in absolute terms".
3. *One coherent rangy anatomy?*
   It is coherent, but as human anatomy.
4. *Distinguishable from Skarn at 208 / 229 without height?*
   Only by slenderness. The blind test confused a Broad Grask with human-family and a low-muscle Skarn with Grask (§2).

### 1.2 Gorrund vs Skarn / Marchfolk (head removed)

1. *Non-human load-bearing architecture rather than a broad tall human?*
   **No.** It reads as a broad, heavy tall human.
2. *Thoracic depth / breadth, lower-trunk continuity, pelvic integration, proximal limbs and joints coordinated?*
   - Breadth and depth are coordinated, with thorax depth ÷ breadth 0.84 vs 0.79.
   - Joint presence (knee ÷ femur 0.289) **equals Skarn (0.292)**, so the "strongest body signal" (GORRUND L74–76) is not carried.
3. *ALPC visually distinct without block / barrel / ogre?*
   The trunk is continuous, but it reads as human waist-to-hip continuity, not a distinct axial chain.
4. *Distinguishable from Skarn at 208 / 229 without muscle or height?*
   Weakly. In the blind test, Broad Skarn was read as Gorrund and the Gorrund reference as human-family.

### 1.3 Grask vs Gorrund

- The contrast reads as thin vs broad.
- Reach-dominant vs axial / load-bearing is not legible as architecture.
- Both remain plausible, upright, non-caricatured humanoids: no hunch, ape proportions or ogre features.

## 2. Blind / low-information silhouette diagnostic (supporting evidence only)

- **Bodies:** 16 — Marchfolk, Skarn, Grask and Gorrund, each as reference, Narrow, Broad and low-muscle / minimum-composition.
- **Presentation:** body-only black silhouettes, front and profile, **height-normalized** so stature carries no information.
- **Blinding:** order shuffled with seed 20261010 and codes only. Scoring was written down **before** opening the key (`blind_scores.json`).

**Result: 12 / 16.** Confusions:

| True | Assigned | Case |
|---|---|---|
| Gorrund reference | human-family | B04 |
| Grask Broad | human-family | B10 |
| Skarn Broad | Gorrund | B12 |
| Skarn low-muscle | Grask | B03 |

**Pattern:**
- The diagnostic separates **slender vs broad**, not architecture. Any human-family body that is slender or broad enough is assigned to Grask or Gorrund, and a reference Gorrund that is not extreme in width is assigned to human-family.
- The assigner was not uninformed: Claude built the bodies. This is a supporting diagnostic, not a calibrated classifier, and it sets no percentage threshold.
- The minimum-composition Grask / Gorrund bodies show a pinched-waist silhouette artifact (B06 / B07). The skeleton envelope at zero composition is not an ordinary low-muscle body. It is reported, not used.

## 3. Correction search — accepted-route levers saturate

Four quick probes were built on the accepted W2 routes (`gr_body.quick`, `go_body.quick`), using only canon-named directions and staying inside the accepted valid-extreme region:

| Probe | Changes | Key skin-layer result |
|---|---|---|
| GRQ1 | napetowaist −0.5, forearm +0.9, upper-arm +0.1, hands +0.3, feet +0.25 | torso 0.263, arm 0.448, forearm ÷ arm 0.386, hand 0.122, foot 0.155 |
| GRQ2 | napetowaist −0.65, forearm +1.0, upper-arm +0.15, hands +0.35, feet +0.3, femur −0.45 | torso 0.262, arm 0.458, forearm ÷ arm 0.388, hand 0.124, foot 0.158 |
| GOQ1 | limb-bone cross-section ×1.08; knee / ankle / wrist circumference +0.5 / +0.4 / +0.4; hands / feet +0.15 | knee ÷ femur 0.295, elbow ÷ humerus 0.370 |
| GOQ2 | cross-section ×1.10, thigh ×1.04, thoracic depth sculpt ×1.05, lower-trunk breadth sculpt ×1.06; joints +0.6 / +0.5 / +0.5; hands / feet +0.2 | knee ÷ femur 0.305, thorax d ÷ b 0.821 (probe convention), elbow ÷ humerus 0.375 |

**Visual result** (`probe_F.jpg`, `probe_Q.jpg`, `probe_P.jpg`, body only): the probes move the ratios in the canon direction, but **the read barely changes**. Grask stays a tall thin human with longer arms; Gorrund stays a broad human with thicker joints.

**Why** (diagnosis, not a canon change):
- Both races are built on the MPFB human base mesh and skin anatomy: human pectoral / deltoid girdle surface, human iliac / gluteal pelvis surface, human joint shapes.
- The authored non-human organization lives in *how* the girdle, pelvis and axial chain are organized:
  - Grask: GR-G2 vertically extended close-seated scapula; GR-P2b long-lever hip apparatus.
  - Gorrund: ALPC; pelvis integration; joint architecture.
- Accepted-route levers only re-proportion and re-thicken a human surface.

Pushing the same levers further would leave the accepted valid envelope and head toward the caricatures canon forbids: stretched human, ape arms, bodybuilder bulk. So **the smallest coherent correction that materially changes the read is not available inside the accepted MPFB route.** It needs a race-specific body-architecture rebuild of the reference realizations — sculpted girdle, pelvis, axial chain and joint architecture, comparable to the Saurin W2I reference rebuild.

**That is an author-level scope decision (§7), so no geometry was changed.**

The probe geometry is kept in scratch and the measurements in `probes.json`, as provenance for that decision.

## 4. Sagekin configuration 2 at 152 / 208 (D2)

**Builds:**
- SGF178: the MF-F-R base plus the accepted Sagekin targets, stature re-solved. This is the configuration-2 central construction base.
- SGF208: same route, stature re-solved, 208.01 cm.
- SGF152-NAT: native short-adult route from the SGF178 macro, as the configuration-1 SG152 was built from SG178, 152.00 cm.
- Matched comparators MFF152-NAT / MFM152-NAT were built on the accepted Marchfolk native route, the same as the W2A 147 bodies.

**Sagekin − Marchfolk at matched stature (%):**

| Pair | torso | leg | arm | head | hand | thorax depth | shoulder | span |
|---|---|---|---|---|---|---|---|---|
| configuration 1, 152 | −2.32 | +1.74 | +2.65 | −0.66 | +5.0 | −3.20 | −1.28 | +1.80 |
| **configuration 2, 152** | **−2.37** | **+1.85** | **+2.99** | **−0.64** | **+5.74** | **−3.31** | **−1.20** | **+2.14** |
| configuration 1, 208 (vs MF 203 endpoint) | −1.94 | +1.47 | +2.21 | −1.20 | +4.07 | −3.45 | −1.25 | +1.52 |
| **configuration 2, 208 (vs MF 203 endpoint)** | **−1.95** | **+1.53** | **+2.44** | **−1.20** | **+4.61** | **−3.53** | **−1.18** | **+1.76** |

- Every direction and magnitude replicates.
- No sex-specific bound or Sagekin sex stereotype is introduced.
- **PASS**; Sagekin can move from CONSTRAINED to SUPPORTED on author acceptance.
- Limit: the full W2E grid / CIB / skeletal-proxy chain was not rerun on configuration 2.

## 5. Cogling 76 cm head (D3)

**The fix:**
- The W2H build used the native route's quick rest-pose head check with a target of 11.0 cm. The R-6 cranio convention (vertex − menton) read 10.91 cm on that body.
- CG76H-NAT uses the same route and cfg with the head target set to 11.12 cm in the quick convention.

**Result:**

| | Head height (R-6) | Stature | Head share | FVI | FPI |
|---|---|---|---|---|---|
| CG76-NAT | 10.91 cm | 76.00 | 0.1435 | 0.867 | 0.1435 |
| **CG76H-NAT** | **11.04 cm** | **76.00** | **0.1452** | **0.864** | **0.1435** |

Body vertices outside head / neck move ≤ 0.08 cm (neck-blend fringe).

**Checks rerun:**

| Check | Result |
|---|---|
| COG-BODY-11 anti-juvenile vs toddler CHILD1 (76 cm) | head share 0.145 vs 0.247 → **PASS** |
| CG76 vs PK91 normalized minimum relation | head share 0.145 < 0.159 (unchanged direction) → **PASS** |
| Canon 11–13 cm (COGLING L1589) | **PASS** |
| CG76 FVI named dependency (W2H) | unchanged |

**PASS**, pending author acceptance of CG76H-NAT as the canonical 76 cm body (manifest flags it PENDING AUTHOR).

## 6. Race-spec stature writeback — drafted, not applied (D4)

The text below is ready to append to each race spec after RM-OT-05 final closure. Each block cites the RM-OT-05 gates and preserves the qualifiers.

| Race | Status line to add |
|---|---|
| Marchfolk | hard bounds 147–203 cm (W2A, both configurations); reference 173; frequency OPEN |
| Skarn | 183–229 cm (W2B / W2B1, both configurations); reference 208 with C1R central face |
| Sagekin | 152–208 cm, both configurations (configuration 2 per this gate, once accepted) |
| Fenn | 157–211 cm |
| Aelari | 168–221 cm |
| Vael | 157–203 cm |
| Halvren | central envelope 152–213; ancestry-conditional reach 147.2 / 228.8 / 221.0 (W3A1); frequency OPEN, no distribution inferred |
| Durrim | 122–152 cm |
| Grask | 198–239 cm; neutralized-readability FAIL open (§7) |
| Gorrund | 208–251 cm; 229 nominal / 230.9 ARM; 251 = current world-validation upper end, not permanent; neutralized-readability FAIL open (§7) |
| Pipkin | 91–122 cm |
| Cogling | 76–107 cm; 76 cm body CG76H pending |
| Saurin | 168–208 cm (tail excluded), already written back |

In every row, "first-pass / provisional" stature wording becomes "accepted W2 / RM-OT-05 envelope", and frequency stays OPEN.

## 7. Contradictions / decisions requiring the author

1. **Large-race reference realizations vs the neutralized-readability canon (structural).**
   - Grask (GRASK L78, L98–99, L104) and Gorrund (GORRUND L86, L109, L147) both require a non-human body read with the head neutralized.
   - The accepted W2 references meet the numeric relations, but they **fail the visual identity gate**, and accepted-route levers cannot fix that (§3).
   - Options:
     - **(a)** Authorize a dedicated **Grask / Gorrund body-architecture reference rebuild** (girdle, pelvis, axial chain and joint architecture sculpted beyond the MPFB human surface). This is like the Saurin W2I rebuild, with all W2C / W2D validators rerun.
     - **(b)** Accept the current references as **proportion references only**, with neutralized readability recorded as an OPEN production / art dependency for the final body meshes.
     - **(c)** Revisit canon. Not recommended: canon is explicit.
   - **Claude's advisory: (a).** RM-OT-05 cannot finally close while this remains.
2. **Grask feet** are smaller than Skarn's in absolute and relative terms (foot share 0.147 vs 0.161 at 208), against GRASK L62 / L253. Fold this into decision 1.
3. **Gorrund joint presence** (knee ÷ femur) equals Skarn's at matched height, against GORRUND L74–76. Fold this into decision 1.
4. **Accept CG76H-NAT** (§5) and **SGF152-NAT / SGF208** (§4) as canonical.
5. **Apply the D4 writeback** after closure (§6).

## 8. Persistent files changed

- `reviews/claude-rac-rm-ot-05-visual-readability-closure-gate.md` (this gate)
- `reviews/rac-rmot05-evidence/readability/` (41 sheets; blind key and scores; probes; Sagekin configuration-2 comparison)
- `reviews/reference-assets/` (new: `manifest.json`, 49 R-6 assets, build / measurement records)
- `specs/gorrund/GORRUND_V1.md` (D1 / D5 bookkeeping block)
- `decisions/REFERENCE_ANATOMY_V1.md` (R-2: Gorrund 229 nominal / 230.9 ARM)
- `tools/rac/w1/rmot05_drivers/ot05r_*.py`
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md` (status lines)
- **Not changed:** every accepted body geometry; every other race spec (D4 waits for closure).

## 9. Stop

Stopped after the corrective closure gate. Not begun: posture, locomotion, equipment, environmental scale, collision, camera, UE5 creator, MetaHuman, rigging, animation and gameplay.

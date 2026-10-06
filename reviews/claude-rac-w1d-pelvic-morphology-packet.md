# RAC W1d — Pelvic Morphology Authorship Packet

**Author:** Claude (builder/coordinator) **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §7 (B-3), work-order item 2 (§11)
**Status:** AUTHOR DECISION PACKET. **No canonical race spec is edited** (order §7 last line). Every "PROPOSAL" line is **BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED**. No number is introduced; every direction is relational (vs Marchfolk "MF" or vs a named population).
**Populations:** Fenn (FN), Aelari (AE), Vael (VA), Durrim (DU), Grask (GR), Gorrund (GO), Pipkin (PK).
**Context populations:** Marchfolk (MF, human reference), Skarn (SK), Sagekin (SG), Cogling (CG), Halvren (HV), Saurin (SA, closed).

---

## 0. Citation key, method and firewall

### 0.1 Citation key (all paths repo-relative; line numbers checked against the current files)

| Key | File |
|---|---|
| FN | `specs/fenn/FENN_V1.md` |
| AE | `specs/aelari/AELARI_V1.md` |
| VA | `specs/vael/VAEL_V1.md` |
| DU | `specs/durrim/DURRIM_V1.md` |
| GR | `specs/grask/GRASK_V1.md` |
| GO | `specs/gorrund/GORRUND_V1.md` |
| PK | `specs/pipkin/PIPKIN_V1.md` |
| MF / SK / SG / CG / HV / SA | `specs/marchfolk/MARCHFOLK_V1.md`, `specs/skarn/SKARN_V1.md`, `specs/sagekin/SAGEKIN_V1.md`, `specs/cogling/COGLING_V1.md`, `specs/halvren/HALVREN_V1.md`, `specs/saurin/SAURIN_V1.md` |
| ECR | `reviews/elf-comparative-review.md` (Elf Comparative Review v1.0, canonical comparative authority for FN/AE/VA, ECR L302) |
| SRR | `reviews/short-race-comparative-anatomy-v1.md` (Short-Race Comparative Anatomy Review v1.0) |
| LRR | `reviews/claude-pass2-r2-large-race-comparative-review.md` (Large-Race Comparative Review; accepted, LRR L153) |
| RA | `decisions/REFERENCE_ANATOMY_V1.md` |
| UCCA | `decisions/UCCA_V1.md` |
| PR | `decisions/PROJECT_RULES.md` |
| RAC-03 | `reviews/claude-rac-03-pelvis-axial-closure.md` (adopted as AD-R6, RA L136) |
| RAC-04 | `reviews/claude-rac-04-segment-stature-closure.md` (adopted as AD-R10/AD-R12, RA L137) |
| W1c-GATE / W1c-MEAS / W1c-METH / W1c-AUD | `reviews/claude-rac-w1c-author-acceptance-gate.md`, `…-measurements.md`, `…-build-method.md`, `…-cross-race-audit.md` |
| ARM-xx | `reviews/rac-w1c-arm/claude-rac-w1c-arm-<xx>.md` |

Line drift note: RAC-03 cites a few Gorrund ALPC rows as "GO L719–720"; the same rows are now GO L723–724. Content is unchanged. This packet cites current lines.

### 0.2 Universal rules that bind every section (quoted once, applied everywhere)

- RA L122: "**Obstetric firewall** | No pelvic inlet/outlet, birth-canal, gestation or fertility geometry is authored or measured for any race. Pelvic measurement uses external skeletal landmarks only".
- PR L65: "**Obstetric firewall:** no pelvic inlet/outlet, gestation or fertility geometry is authored or measured; pelvic measurement uses external skeletal landmarks only."
- RAC-03 L53: "ARMs and RM-UB-06 measure **external skeletal landmarks only** (iliac crest breadth, bi-trochanteric breadth, anteroposterior pelvic depth, pelvic vertical contribution)."
- UCCA L119: "Skeletal Frame is the continuous configuration of a character's skeletal breadth, depth, joint and robusticity variables (shoulder/clavicular breadth, thoracic width, thoracic depth where bound, pelvic width and depth where canon names it, joint scale, long-bone robusticity, plus race-specific extras)".
- UCCA L156: "composition never edits the skeleton; thoracic depth is never faked by fat or muscle; pelvic breadth is never fat; frame never edits composition."
- RA L124 (AD-R7/E-6): "Curvature is never a racial identity carrier, except Vael's "natural lumbar curve". ARMs use neutral adult curvature".
- RA L35 (R-4): "**Current Muscularity and Body-Fat Amount at the population centre, neutral (untilted) fat distribution, no regional muscle offsets.**"
- RA L53 (R-SEX): "**Durrim, Grask, Gorrund, Pipkin, Cogling** | **One configuration** for the Wave 1 bootstrap. Skeleton and composition carry **no authored sex shift** (R-SEX "no shift" is complete)."
- RA L52: "**Fenn, Aelari, Vael** | **One configuration** for now. Detailed external sex-related biology is **deferred**; human or humanoid soft tissue is **not** imported by assumption."
- PR L107: "Reproductive biology is never inferred from creator architecture."
- RA L84/L166 (circularity): "A mesh built from **numeric targets chosen by a builder** … returns those targets when measured. Measuring it **cannot discover** canon" / "**No measured value becomes canon merely because a candidate mesh embodies it.**"
- RA L106: "Directional canon … is a **constraint the measurement must satisfy**, never permission to invent a magnitude."
- Order §12: "Do not manufacture biological differences solely for silhouette separation."

### 0.3 What "pelvic architecture" means in this packet (method vocabulary, not biology)

Six descriptors, all **external-landmark-readable or frame-level**; none touches inlet/outlet geometry:

| Code | Descriptor | External landmark reading (RM-UB-06 or derived) |
|---|---|---|
| P-1 | Pelvis-to-spine / sacral relationship (lumbosacral junction level and orientation relative to the lumbar column; sacral robusticity) | Not directly in RM-UB-06; frame-level statement, visible in side render |
| P-2 | Hip-joint organization (inter-acetabular spacing, hip-joint vertical placement relative to iliac crest, hip-joint scale, femoral convergence) | Bitrochanteric breadth; hip-joint height; crest-to-hip-joint vertical |
| P-3 | Iliac structure (iliac height, flare, crest robusticity) | Iliac-crest breadth; pelvic vertical contribution |
| P-4 | AP depth | AP pelvic depth |
| P-5 | Transverse breadth | Iliac-crest breadth, bitrochanteric breadth |
| P-6 | Lower-trunk relationship (waist / lumbar interval between costal margin and iliac crest; pelvis-to-thorax proportion) | Derived: crest breadth ÷ thorax breadth; (proposed) costal-margin-to-crest interval |

### 0.4 What "human-homologous" means here, and why it is not "a simply widened / enlarged / scaled human pelvis"

Where canon does not motivate a departure from MF in a descriptor, this packet's default is:

> **"Human-homologous architecture with the race's existing proportional relationships."** The pelvis keeps the ordinary adult humanoid bone plan (paired ilia, sacrum, pubic and ischial regions, two acetabula, upright-biped orientation). **Each descriptor P-1…P-6 is set separately from the race's own canon relationships (torso share, thoracic breadth/depth, leg share, femur relationship, joint scale, robusticity), not by one scale factor or one breadth/depth morph applied to the MF pelvis.**

It differs from the prohibited forms as follows:

| Prohibited form (canon wording) | What it is | Why the default is not it |
|---|---|---|
| "a scaled human one" (FN L111); "a narrowed or scaled human pelvis" (GR L45); "uniformly enlarged human pelvis" (GO L49) | MF pelvis × one factor (all ratios = MF) | The default changes intra-pelvic **ratios** (breadth : depth : vertical : hip-joint spacing : construction) wherever canon motivates it, and its construction (robusticity/gracility) follows the race's skeleton, not the scale factor |
| "a simply widened human pelvis" (DU L32); "No human pelvis plus a slider" (VA L124); "a stock human pelvis with longer legs attached" (AE L126) | MF pelvis + one axis morph (this is exactly what the W1c candidates carry: e.g. FN/AE `hip-scale-horiz-decr 0.10`, DU `hip-scale-horiz-incr 0.15`, GO `hip-scale-horiz-incr 0.30, hip-scale-depth-incr 0.30`, PK `hip-scale-*-incr`; GR no hip target, i.e. generator pelvis scaled with the body; ARM-FN L36, ARM-AE L35, ARM-DU L35, ARM-GO L36, ARM-PK L35) | The default requires the **coupled** relationships each spec names (torso-pelvis continuity, pelvis-femur coordination, hip-joint scale, thorax-pelvis proportion) to be expressed jointly; a single-axis morph cannot satisfy two or more coupled descriptors at once |

**Honest limit (flagged):** whether a relational-only pelvis satisfies the canon word "distinct / non-human" for FN, AE, VA, GR, GO is itself an author decision (Decision PV-D1). This packet does **not** invent a morphological "marker" (e.g. an elf-specific iliac blade shape) because no canon line motivates one; Option PV-D1(b) lists what would have to be invented if the author wants one.

---

## 1. Fenn (FN)

### 1.1 Canon quotes

**Body architecture / skeleton**
- FN L3: "Fenn are the first playable race with a genuinely non-human skeleton, and they are never thin humans with pointed ears."
- FN L32–38: "- a more gracile skeleton, with lower skeletal mass for their height / - narrower joints and slenderer long bones / - longer limbs relative to the torso / … / - different pelvis-to-leg relationships"
- FN L40: "Gracile never means fragile. The anatomy looks naturally adapted, not like weakened human anatomy."
- FN L44: "Narrow, Balanced and Broad all apply inside Fenn anatomy. A Broad Fenn is still biologically Fenn, and Narrow isn't the only authentic look."
- FN L138: "Fenn have a genuinely different elven skeleton. The difference comes from long-bone relationships, joint scale, hands, feet, ribcage, shoulders and clavicles, and pelvis and legs combined, never just from longer human sliders."

**Lower trunk / torso-pelvis**
- FN L50: "Torso | Slightly smaller torso share of height, somewhat less ribcage depth, more compact chest, longer waist transition | Torso length, ribcage width and depth, shoulder width, waist, pelvis width"
- FN L110: "Ribcage and spine | Somewhat shallower front to back, moderately narrow for height, somewhat vertically compact, with a relatively longer waist and lumbar transition | Enough thoracic volume, never an implausibly tiny chest"
- ECR L45: "Fenn | Compact-centered torso, where the ribcage-to-pelvis transition may be relatively gradual or extended within the Fenn proportional system. This does not mean Fenn have a longer absolute or proportional waist transition than Aelari"
- AE L114: "Fenn | Concentrated in the extremities, around a compact-centered torso"

**Pelvis directly**
- FN L111: "Pelvis and hips | A distinct elven pelvis, not a scaled human one, supporting longer femurs, stable hips, light visual build, Narrow to Broad frames, plausible muscle attachment and natural locomotion | Exact shape awaits prototyping, and not every Fenn has narrow hips"
- ECR L32: "Pelvis (§13–14) | Not a stock human pelvis, reflects shared ancestry (A). Exact shared shape is E | Supports compact center and long extremities (E in detail) | …"
- ECR L37: "Pelvis is recorded as A plus E: shared non-human ancestry is locked, but the three pelvises aren't claimed to be identical, with the pattern being a shared foundation that diverges by population."
- ECR L59: "The combination is greater gracility than humans, non-human torso, shoulder and clavicle relationships, a non-human pelvis foundation, elongated limbs, elven joints, elongated hands and fingers, and distinct feet."
- ECR L21: "Elves are more gracile than equivalent humans, expressed through long-bone proportions, joint scale, wrists and ankles, shoulder articulation, hands and feet and overall skeletal mass."
- ECR L312, L316 (final consistency, gracility ordering): "Fenn | Greatest average skeletal gracility of the three elven populations" and "The provisional average ordering, from greater gracility toward greater structural presence, is **Fenn, then Aelari, then Vael.**"

**Legs / femur / hip**
- FN L52: "Legs and feet | Greater leg share of height, slightly longer lower legs, narrower ankles, somewhat longer feet than same-height humans"
- FN L123: "Legs | Greater leg share, slightly greater lower-leg share | … Hip, knee and ankle relationships are kept"
- FN L115: "Wrists, elbows, knees and ankles look smaller relative to limb length than on same-height humans, with minimum anatomical boundaries."

**Stance / locomotion / validation**
- FN L66: "Longer limbs, different torso proportions, a lighter skeleton and different joints may change balance, center of mass and locomotion."
- FN L78: "The Fenn must still stand out through limb proportions, joint scale, hands, feet, torso, shoulders, pelvis and legs, and craniofacial anatomy. If a Fenn looks human with ears hidden, the anatomy needs more work."
- FN L130: "High-body-fat Fenn are validated too, and soft tissue never erases the Fenn skeleton."
- FN L341: "Randomized Fenn keep … shoulder and ribcage, pelvis and leg … relationships."

**Sex / composition firewall**
- FN L552: "**Sex-related external biology is deferred** to a later focused pass; human or humanoid soft tissue is not imported by assumption; independence rules stand (AD-R21)."
- FN L58: "Fenn identity never depends on thinness, and muscle and fat modify the Fenn foundation rather than replace it."

### 1.2 Canon already implies

1. The pelvis is **not** a uniformly scaled MF pelvis and **not** MF + one breadth slider (FN L111; ECR L32; FN L138 "never just from longer human sliders").
2. **Construction is gracile**: lower skeletal mass for height applies to the whole skeleton (FN L32; ECR L21), and FN is the most gracile elf (ECR gracility ordering). So pelvic **construction** (crest robusticity, trochanteric/landmark relief) trends lighter than MF at matched stature — but "never fragile" (FN L40).
3. **The pelvis serves a greater leg share and longer femora**: hip-joint height ÷ stature > MF (FN L52, L123; RAC-04 L25 "FN | < MF | > MF"); the pelvis must keep hips stable under longer levers (FN L111 "supporting longer femurs, stable hips").
4. **Pelvis-to-leg relationship differs from MF** (FN L38) — i.e. some P-2 descriptor must differ, not only femur length.
5. **The pelvis sits under a smaller, compact-centred torso with a relatively gradual waist/lumbar transition** (FN L50, L110; ECR L45) — the iliac crest must not close up the waist interval; but the FN waist interval is not longer than AE's (ECR L45).
6. **Breadth is not the identifier**: "not every Fenn has narrow hips" (FN L111) and all three frames apply (FN L44).
7. Sex-related pelvic shape: none authored; human soft tissue not imported (FN L552; RA L52).

### 1.3 Genuinely OPEN

- Central pelvic **transverse breadth** relative to stature vs MF (canon gives "light visual build" and "not every Fenn has narrow hips" — no direction).
- **AP depth** vs MF (only the ribcage is said to be shallower, FN L110; RA L128 "thoracic depth and breadth are independent" does not extend to the pelvis).
- **Pelvic vertical contribution** vs MF.
- **Which P-2 descriptor** carries "different pelvis-to-leg relationships" (FN L38).
- Iliac flare/orientation; sacral proportion.
- "Exact shape awaits prototyping" (FN L111); shared elven pelvis exact shape is ECR class E (ECR L32, L281, L298).

### 1.4 PROPOSAL — minimum positive pelvic architecture (BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED)

| # | Descriptor | Proposal | Derived from |
|---|---|---|---|
| FN-P1 | Spine/sacral | Human-homologous lumbosacral relationship; neutral adult curvature (no identity in curvature). | RA L124; no FN line motivates a departure |
| FN-P2a | Hip-joint vertical placement | Hip joints placed so leg share (hip-joint height ÷ stature) is > MF, achieved by **femur and lower-leg length coordinated with pelvic vertical contribution**, not by shortening the pelvis below the hip joints (no "high crotch" by truncation). | FN L34, L52, L123; FN L138 "never just from longer human sliders" |
| FN-P2b | Hip-joint spacing ("pelvis-to-leg relationship") | Inter-acetabular spacing is **not reduced in proportion to the gracile construction**: bitrochanteric breadth ÷ iliac-crest breadth is **not lower than MF**, so longer femora sit on a stable hip base. This is the proposed concrete reading of "different pelvis-to-leg relationships … supporting longer femurs, stable hips". | FN L38, L111 |
| FN-P2c | Hip-joint scale | Hip-joint scale follows Fenn joint gracility (smaller relative to limb length than MF) **above the J-1 floor**. | FN L33, L115 (lists knees/ankles; hips by the general "narrower joints", FN L33); RA L125 (J-1) |
| FN-P3 | Iliac structure | Iliac construction **lighter** than MF at matched stature (less crest robusticity / landmark relief), shape (flare, height) human-homologous. | FN L32; ECR L21; ECR gracility ordering |
| FN-P4 | AP depth | **Option A (recommended, minimum):** AP depth ÷ stature ≈ MF (no authored departure). **Option B:** AP depth ÷ stature modestly < MF, following the shallower ribcage. Builder does not choose; author decides (PV-D3). | FN L110 (ribcage only); RA L128 |
| FN-P5 | Transverse breadth | Central iliac-crest breadth ÷ stature: **no mandated narrowing** — "light visual build" is carried by construction (FN-P3) and by limb share, not by a narrowed pelvis. Narrow–Broad frame range applies. (Author option PV-D4: ≈ MF, or modestly < MF.) | FN L111 "not every Fenn has narrow hips"; FN L44; VA L124 prohibition logic ("No human pelvis plus a slider") |
| FN-P6 | Lower trunk | Crest level leaves a **relatively gradual waist/lumbar interval** within the compact torso (costal margin–crest interval ÷ torso length ≥ MF), and **< AE** at matched stature. | FN L50, L110; ECR L45 |

### 1.5 Skeleton vs composition

- **Frame (skeleton):** P-1…P-6 above; pelvic breadth is a frame variable (FN L50 lists "pelvis width"; UCCA L119).
- **Composition:** hip/gluteal soft tissue, external hip width, waist fat. "soft tissue never erases the Fenn skeleton" (FN L130); "pelvic breadth is never fat" (UCCA L156).
- **Sex/obstetric:** no sex-related pelvic shape; no human sex soft tissue imported (FN L552; RA L52); no inlet/outlet (RA L122).

### 1.6 Build implication and verification

A compliant reference build must:
- replace the generator human pelvis + `hip-scale-horiz-decr 0.10` (ARM-FN L36) — that is "human pelvis plus a slider" — with a pelvis whose breadth, hip spacing, construction and vertical placement are set per FN-P2…P6;
- read the pelvis at R-4 composition and R-6 stance.

RM-UB-06 verification (external skeletal landmarks, at matched stature vs MF-M-R):
- iliac-crest breadth ÷ stature: per PV-D4 (≈ MF, or < MF);
- bitrochanteric ÷ iliac-crest breadth: **≥ MF** (FN-P2b);
- AP depth ÷ stature: per PV-D3;
- pelvic vertical contribution: no direction (OPEN); hip-joint height ÷ stature > MF (already RAC-04);
- construction (FN-P3) is **not** measurable by RM-UB-06 → visual check on orthographic renders, or an author-accepted robusticity proxy (PV-D17).
- FN-P6 needs the proposed costal-margin-to-crest interval (PV-D15).

---

## 2. Aelari (AE)

### 2.1 Canon quotes

**Body architecture**
- AE L33: "Aelari are built around whole-body vertical elongation, distributed coherently through the cranium, neck, torso, arms and legs. They're never a uniformly scaled human or Fenn with stretched legs."
- AE L115: "Aelari | Distributed continuously through the neck, torso, arms and legs"
- AE L19: "- non-human shoulder, ribcage and pelvis relationships"
- AE L130: "Shoulders, elbows, wrists, hips, knees and ankles are gracile compared with humans but structurally sufficient. Gracile never means fragile, and hard minimum boundaries prevent implausibly tiny joints."
- ECR L313 (gracility ordering): "Aelari | Strong average skeletal gracility, with somewhat greater average skeletal structural presence than Fenn when comparing otherwise equivalent individuals"

**Lower trunk / torso-pelvis**
- AE L48: "Torso | Longer than Fenn relative to height, longer waist transition, moderate chest breadth, relatively shallow depth, elven ribcage relationships | Believable thoracic volume, never implausibly shallow"
- AE L124: "Torso and spine | Longer overall torso and waist transition than Fenn. Controls: torso length, ribcage length, width and depth, waist and lumbar length, shoulder width, pelvic width | Spine and ribcage relationships stay coherent"
- ECR L46: "Aelari | The greatest average vertical torso continuity of the three, including a longer average ribcage-to-pelvis (waist-transition) region than Fenn and Vael, which supports whole-body vertical elongation"

**Pelvis directly**
- AE L126: "Pelvis | A distinct elven pelvis, not a stock human pelvis with longer legs attached. Stable with long femurs, coherent with the spine, Narrow to Broad variation, plausible muscle attachment, natural locomotion | Exact shape awaits prototyping. No mandatory hip width by race or sex-related anatomy"
- AE L134: "Narrow, Balanced and Broad change the real skeleton: clavicle, ribcage and pelvic breadth, joint relationships and overall skeletal presence. Frame stays separate from muscle, fat, sex-related anatomy, height and presentation."
- AE L143: "Pelvic width sets hip articulation and upper-leg alignment."
- AE L448–449: "- spine and pelvis / - pelvis and upper-leg alignment"
- ECR L32 (AE column): "Supports vertical elongation and long femurs (E in detail)"; ECR L37 (as in §1.1).

**Legs / femur**
- AE L58: "Legs and feet | Distinctly long-legged while keeping the longer torso, with even elongation through thigh and lower leg (not lower leg alone)"
- AE L154: "Legs | Elongation spread evenly, not one extremely long segment | … Hip, knee, ankle and foot stay coherent"

**Comparisons / validation**
- AE L169: "Fenn more compact-centered with stronger extremities. Aelari more vertically continuous, with a longer torso and neck and evenly spread limb elongation. Related, not identical"
- AE L170: "Aelari never read as the tallest end of human customization. Check robustness, joints, ribcage, clavicles, pelvis, limbs, hands, feet, and neck and torso"
- AE L482: "Sagekin stay fully human. Aelari have elven skeletal and craniofacial architecture: joints, ribcage, clavicles, pelvis, neck and torso, limb segmentation, hands, feet, face."
- AE L483: "Neither is a scaled version of the other"

**Sex**
- AE L618: "**Sex-related external biology is deferred** to a later focused pass; human or humanoid soft tissue is not imported by assumption; independence rules stand (AD-R21)."

### 2.2 Canon already implies

1. Not a stock MF pelvis with long legs attached (AE L126): **the pelvis itself** must carry an Aelari relationship, not only the legs.
2. **Coherent whole-body vertical elongation** (AE L33, L115): no axial region is excluded from the elongated distribution; the pelvis sits inside a longer torso **and** under long, evenly elongated legs (AE L48, L58, L124).
3. **Greatest waist (ribcage-to-pelvis) interval of the elves** (ECR L46; AE L48, L124).
4. Gracile hips (AE L130), less gracile than FN, more than VA (ECR ordering).
5. "Stable with long femurs" and "Pelvic width sets hip articulation and upper-leg alignment" (AE L126, L143): breadth and hip-joint organization are coupled.
6. **No mandatory hip width by race or by sex** (AE L126): breadth cannot be the race or sex identifier.

### 2.3 Genuinely OPEN

- Breadth, AP depth, vertical contribution vs MF (none stated).
- Whether the pelvis **itself** is vertically proportioned (AE L33 names "torso"; the pelvis is not named separately).
- Iliac flare; sacral proportion; "Exact shape awaits prototyping" (AE L126).

### 2.4 PROPOSAL (BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED)

| # | Descriptor | Proposal | Derived from |
|---|---|---|---|
| AE-P1 | Spine/sacral | Human-homologous lumbosacral relationship "coherent with the spine"; neutral curvature. | AE L126; RA L124 |
| AE-P2a | Hip-joint vertical placement | Leg share > MF via **even** thigh and lower-leg elongation; the pelvis is not truncated below the hip joints to add leg length. | AE L58, L154; AE L126 "not … longer legs attached" |
| AE-P2b | Hip-joint spacing | Bitrochanteric ÷ iliac-crest breadth **not lower than MF** (stable with long femurs). Same shared-elven reading as FN-P2b. | AE L126, L143 |
| AE-P2c | Hip-joint scale | Gracile vs MF, structurally sufficient; ≥ FN at matched stature (ordering, not magnitude). | AE L130; ECR gracility ordering |
| AE-P3 | Iliac structure | **Pelvis participates in the vertical elongation:** pelvic vertical contribution ÷ iliac-crest breadth **> MF** and **> FN** (a vertically proportioned pelvis, achieved by iliac height, not by narrowing). Construction gracile (lighter than MF, ≥ FN). **Inference flagged:** AE L33 names "torso", not "pelvis"; author confirms (PV-D5). | AE L33, L115; ECR L46; AE L126 |
| AE-P4 | AP depth | AP depth ÷ stature ≈ MF (no authored departure); "relatively shallow" is a ribcage statement and is **not** transferred (author may choose otherwise under PV-D3). | AE L48, L123 (ribcage only); RA L128 |
| AE-P5 | Transverse breadth | No mandated breadth direction vs MF; "No mandatory hip width by race". | AE L126 |
| AE-P6 | Lower trunk | Costal-margin–crest interval ÷ torso length **> FN and > VA** (and ≥ MF). | ECR L46; AE L48, L124 |

### 2.5 Skeleton vs composition

As FN §1.5. Additionally, AE L134 "Frame stays separate from muscle, fat, sex-related anatomy, height and presentation" and AE L126 "No mandatory hip width by race or sex-related anatomy": external hip width carries no Aelari or sex identity.

### 2.6 Build implication and verification

- Replace generator pelvis + `hip-scale-horiz-decr 0.10` (ARM-AE L35).
- The elongation must reach the pelvis (AE-P3), so the build cannot reach the AE torso share only through ribcage and lumbar length.
- RM-UB-06: pelvic vertical contribution ÷ crest breadth > MF and > FN (AE-P3); bitrochanteric ÷ crest ≥ MF (AE-P2b); AP depth ÷ stature ≈ MF (AE-P4); crest breadth no direction; waist interval > FN, VA (PV-D15 landmark).

---

## 3. Vael (VA)

### 3.1 Canon quotes

**Body architecture**
- VA L27: "Vael | More compact, deeper-bodied, with somewhat more structural presence through torso, joints and extremity bases"
- VA L29: ""Compact" never means short, dwarven, stocky or automatically muscular."
- VA L110: "Vael have more compact structural continuity, a deeper torso and somewhat more skeletal presence, still recognizably elven. Vael never become stocky or dwarf-like elves, shortened Skarn, muscular by default, or humans with pointed ears."
- VA L37: "Skeletal robustness | Gracile next to humans (especially Skarn), but more joint presence than Fenn or Aelari at wrists, elbows, knees, ankles, shoulders and hand and foot bases | Never compact Skarn"
- VA L132: "Shoulders, elbows, wrists, hips, knees and ankles are gracile compared with humans, with somewhat more presence than Fenn or Aelari, always in proportion."
- ECR L314 (gracility ordering): "Vael | Generally gracile relative to equivalent robust human populations, with the greatest average joint, base and skeletal structural presence of the three"

**Lower trunk / torso-pelvis**
- VA L35: "Torso | Greater torso share than Fenn, deeper ribcage than Fenn or Aelari, moderate width, strong torso-to-pelvis continuity, less elongated than Aelari"
- VA L114: "Vael torso depth comes from ribcage depth and curvature, the spine-to-ribcage relationship, shoulder placement and the torso-to-pelvis transition. It's never faked with body fat, muscle, an oversized chest or uniform torso scaling. A Narrow, lean Vael keeps it."
- VA L121: "Spine and waist | Moderate torso length, less extended waist than Aelari, strong torso-to-pelvis continuity, natural lumbar curve. Controls: … shoulder and pelvic breadth are Skeletal Frame variables because frame changes them (below; T-10, UCCA Phase 2; no ranges added)"
- ECR L47: "Vael | Less vertical waist elongation than Aelari and stronger compact continuity between torso and pelvis. The deeper ribcage must not be mistaken for a longer waist"
- VA L165: "Vael | Deeper torso, more compact torso-to-limb continuity, more joint presence, … moderate elongation, lower center of mass than Aelari"

**Pelvis directly**
- VA L38: "Pelvis | Their own elven pelvis (not human, Fenn or Aelari): stable leg articulation, torso-to-pelvis continuity, Narrow to Broad support, plausible muscle attachment, natural locomotion | Exact shape awaits prototyping"
- VA L124: "Pelvis | A distinct elven pelvis: torso-to-pelvis continuity, stable with long legs, all three frames, plausible muscle attachment, natural locomotion | No human pelvis plus a slider. Awaits prototype validation"
- VA L128: "Frame changes the clavicles, ribcage, pelvis, joints and skeletal presence … The coupled relationships are … torso length and waist, waist and pelvis, and pelvis and hip."
- UCCA L133: "**Vael:** shoulder and pelvic breadth are Skeletal Frame variables because Vael canon says frame changes them (T-10)."
- ECR L32 (VA column): "Supports deeper torso continuity and Vael legs (E in detail)"

**Legs**
- VA L46: "Legs | Long relative to humans, somewhat smaller leg share of height than Fenn or Aelari, balanced femur and lower leg, more knee and ankle presence | Hip, knee, ankle and foot stay coherent"
- VA L140: "Compactness never comes from just shortening legs"

**Comparisons**
- VA L178: "Vael keep elven ancestry, gracility, limb segmentation, hands and feet, and torso and pelvis relationships"
- VA L179: "Durrim anatomy is never used to solve Vael compactness."

### 3.2 Canon already implies

1. Must differ from **human, Fenn and Aelari** pelves (VA L38) — the only elf whose pelvis is explicitly required to differ from the other two.
2. **The torso-to-pelvis transition contributes to Vael torso depth** (VA L114): the upper pelvis / lower-trunk junction participates in front-to-back depth → pelvic AP depth (at least at the crest/upper pelvis) trends **greater than FN and AE** at matched stature.
3. **Short, compact waist interval vs AE** (VA L121; ECR L47).
4. **Natural lumbar curve** is the only authored racial curvature (VA L121; RA L124).
5. More hip-joint presence than FN/AE, still gracile vs MF (VA L132; ECR ordering).
6. Leg share < FN and AE, still > MF ("Long relative to humans", VA L46; RAC-04 L27) — hip-joint height ÷ stature between MF and FN/AE.
7. Breadth is a frame variable (UCCA L133), "moderate width" (VA L35) — no direction vs MF.
8. Compactness never from Durrim anatomy (VA L179) or leg-shortening alone (VA L140).

### 3.3 Genuinely OPEN

- AP depth **vs MF** (canon orders VA only against FN/AE).
- Lumbar-curve magnitude vs MF ("natural" ≠ "greater"; RA L124 only exempts it from neutralization).
- Breadth vs MF; iliac shape; vertical contribution; sacral proportion; "Awaits prototype validation" (VA L124).

### 3.4 PROPOSAL (BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED)

| # | Descriptor | Proposal | Derived from |
|---|---|---|---|
| VA-P1 | Spine/sacral | **Natural (present, not flattened) lumbar lordosis** carried into a lumbosacral junction oriented coherently with it; magnitude human-homologous unless author chooses "greater than MF" (PV-D7). This is the only race in this packet where the ARM does not use neutral curvature. | VA L121; RA L124 |
| VA-P2a | Hip-joint vertical placement | Hip-joint height ÷ stature > MF but < FN and AE, with femur and lower leg balanced. | VA L46, L140; RAC-04 L27 |
| VA-P2b | Hip-joint spacing | Bitrochanteric ÷ crest ≥ MF (shared elven reading, as FN-P2b/AE-P2b). | VA L38 "stable leg articulation"; VA L124 |
| VA-P2c | Hip-joint scale | Greater than FN and AE at matched stature; gracile vs MF; "always in proportion". | VA L132; ECR ordering |
| VA-P3 | Iliac structure | Construction greatest of the three elves, still lighter than MF; iliac height human-homologous (no vertical elongation, unlike AE-P3). | ECR ordering; VA L35 "less elongated than Aelari" |
| VA-P4 | AP depth | AP depth ÷ stature **> FN and > AE**, continuous with the deeper thorax (no step-in at the waist). Vs MF: **Option A** ≈ MF (minimum); **Option B** > MF. Author decides (PV-D6). | VA L114, L121; ECR L47 |
| VA-P5 | Transverse breadth | "Moderate"; no direction vs MF; frame variable. | VA L35; UCCA L133 |
| VA-P6 | Lower trunk | Costal-margin–crest interval ÷ torso length **< AE** (compact continuity); the thorax-to-pelvis transition reads as continuous in profile. | VA L121; ECR L47; VA L114 |

### 3.5 Skeleton vs composition

- VA L114 is explicit that depth "never faked with body fat, muscle … or uniform torso scaling. A Narrow, lean Vael keeps it." → VA-P4 must be skeletal and survive Narrow + low fat.
- External hip width and gluteal tissue are composition (UCCA L156). Sex: deferred, none imported (VA L624; RA L52). Obstetric: none.

### 3.6 Build implication and verification

- ARM-VA L27: "Vael's 'natural lumbar curve' is not modelled (generator neutral spine)." A compliant build must model VA-P1.
- RM-UB-06: AP depth ÷ stature > FN and AE (VA-P4); bitrochanteric ÷ crest ≥ MF; crest breadth no direction; waist interval < AE (PV-D15); lumbar curve checked on the side render (not an RM-UB-06 item; propose a lordosis landmark read only if PV-D7 = "greater than MF").

---

## 4. Durrim (DU)

### 4.1 Canon quotes

**Body architecture**
- DU L9: "> **Durrim are not humans scaled down to dwarf height.**"
- DU L11: "Population tendencies: short overall stature; high skeletal structural presence relative to height; broad torso relationships; substantial thoracic depth; strong shoulder and pelvic integration; relatively substantial joints; shorter limb contribution to total height than the human reference; large hands and feet relative to stature; a low center of mass. … Durrim are never made by uniformly scaling a Marchfolk down, shortening only the legs, enlarging only the torso or head, making a human broad and calling them a dwarf, or combining short height with maximum muscle."
- DU L21: "**Compact doesn't mean compressed.** Durrim never look like a vertically squashed human skeleton … **Adults read unmistakably as adults**, with no childlike head-body or facial proportions, hands, shoulders, pelvis, limbs or movement"
- DU L91: "> **No individual body part should look shortened, widened or enlarged in isolation.**"
- SRR L17: "**Durrim** | **Compact Structural Concentration** | short adult stature → high skeletal structural presence → broad/deep vertically compact torso → substantial joints → reduced limb contribution → relatively substantial hands/feet"
- DU L514: "Durrim are a distinct compact humanoid population defined by short adult stature, high skeletal structural presence relative to height, a broad/deep and vertically compact torso architecture …"

**Torso-pelvis / lower trunk**
- DU L25: "The torso carries a major part of Durrim identity: a broad skeletal thorax relative to stature, substantial thoracic depth relative to stature, strong ribcage-spine integration, compact vertical torso relationships, and strong torso-pelvis continuity."
- DU L97: "The torso stays vertically compact, never an extremely long torso on short legs, a vertically compressed human torso or a near-square block, with recognizable thorax, abdomen, waist and pelvis transitions."
- DU L104: "Abdomen and waist | No required large belly, fat-thick waist, straight waist or barrel silhouette. … a narrow waist is valid with coherent ribcage and pelvis"
- DU L33: "Spine | Supports compact stature, deep and broad thorax, substantial upper-body mass potential, functional flexibility and stable locomotion | Never inherently stiff"
- DU L34: "Center of mass | Lower than equivalently proportioned taller humanoids, from stature, compact torso, shorter limbs, pelvis and mass distribution"

**Pelvis directly**
- DU L32: "Pelvis | A distinct architecture for compact stature, broad foundation, shorter lower limbs, low center of mass and stable locomotion | **OPEN, requires detailed anatomical design.** Never a simply widened human pelvis"
- DU L108: "Pelvis | Exact morphology stays OPEN. Only strong torso-pelvis integration, a compact-stature pelvis, stable hip placement, coherent support for shorter legs and broad variation are set"
- DU L109: "Pelvic breadth | Frame preset may shift skeletal pelvic breadth, which stays distinct from hip fat, glutes and thigh muscle, and external hip width never stands in for skeletal width"
- DU L52: "A Durrim can have a broad ribcage, substantial joints, robust long bones and a broad pelvis with low muscularity … A **Broad Durrim** may strongly express shoulder, thoracic and pelvic breadth and structural presence, but Broad never automatically means muscular, fat, male or every skeletal dimension at maximum."
- DU L127: "Narrow | May reduce ribcage, shoulder, pelvic and long-bone breadth and joint scale relative to other Durrim, while staying inside Durrim-specific minimum structural relationships and never collapsing into short Marchfolk anatomy"
- DU L129: "Broad | May increase skeletal ribcage, shoulder and pelvic breadth and joint presence within coherent limits, never every dimension equally"

**Legs / hip joints**
- DU L38: "Legs are a major part of the silhouette: shorter contribution to height than equivalently tall Marchfolk, functional long bones, adult knees and coherent hip-knee-ankle relationships, never made by shortening only the femur or lower leg."
- DU L40: "Joints (shoulders, elbows, wrists, hips, knees, ankles) trend toward substantial scale relative to limb length and stature, integrated with adjacent bones and never enlarged independently."
- DU L119: "Legs are proportionally shorter relative to stature than equivalent-height Marchfolk, through coordinated pelvis, femur, knee, lower leg, ankle and foot relationships, never one bone alone. The femur trends toward reduced absolute length and contribution to height with substantial structure relative to length … with functional hips and knees."
- DU L121: "The foot, pelvis and leg architecture gives a broad potential base of support that may affect movement appearance, never automatically gameplay stability"

**Stance / locomotion**
- DU L430: "The neutral resting alignment is an ordinary relaxed stance, never a permanent crouch, hunch, bowed legs, wide combat stance or forward lean, and individual variation in spinal posture, shoulder and head carriage, pelvic orientation, foot orientation and stance width never erases Durrim skeletal identity."
- DU L436: "Walking | Accounts for shorter absolute legs, the leg-to-torso relationship, Durrim pelvis, knee and ankle structure, feet …"

**Validation / sex**
- DU L19 / L72: at 152 cm a Durrim and a Marchfolk "stay clearly distinct in head-body relationship, neck, shoulders, ribcage, torso, pelvis, arms, legs, joints, hands and feet" (L72).
- DU L58: "Durrim sex-related anatomy isn't finalized … with no sex automatically broad, narrow, tall, short, muscular or bearded … Durrim magnitudes stay OPEN"
- DU L520: "These stay OPEN …: exact pelvic morphology, sex-related anatomy …"

### 4.2 Canon already implies

1. **Broad foundation**: skeletal pelvic breadth relative to stature trends **> equal-height MF** (DU L32 "broad foundation"; DU L11 "broad torso relationships"; L52 "broad pelvis with low muscularity").
2. **Not breadth alone** ("Never a simply widened human pelvis", L32; "No individual body part should look … widened … in isolation", L91): breadth must come with coordinated changes in other descriptors.
3. **Strong torso-pelvis continuity/integration** with a broad, deep thorax (L25, L108) → the pelvis is not a narrow or shallow step below a broad, deep thorax.
4. **Substantial hip joints** relative to limb length and stature (L40), "stable hip placement" (L108).
5. **The pelvis participates in the reduced leg share** (L119 "through coordinated pelvis, femur…"), and in the low centre of mass (L34).
6. **High skeletal structural presence** applies to the pelvis (L11; SRR L17) → robust construction (≠ PK light construction).
7. **Vertically compact but not compressed**, with recognizable waist and pelvis transitions (L21, L97) → a waist interval exists; it is not removed.
8. Pelvic orientation is posture, not identity (L430). Sex: no authored shift (RA L53).

### 4.3 Genuinely OPEN

- **AP depth** of the pelvis vs MF (the thorax is "substantial … depth"; the pelvis depth is not stated).
- **Pelvic vertical contribution** vs MF, and the **height-to-breadth** proportion.
- **Pelvic breadth relative to thoracic breadth** vs MF.
- **How the pelvis "coordinates" the shorter legs** (L119): hip-joint vertical placement, inferior pelvic extent.
- Iliac flare; sacral proportion. "Exact morphology stays OPEN" (L108).

### 4.4 PROPOSAL (BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED)

| # | Descriptor | Proposal | Derived from |
|---|---|---|---|
| DU-P1 | Spine/sacral | Robust lumbosacral junction integrated with a strong ribcage–spine column; human-homologous orientation; neutral curvature. | DU L25, L33; RA L124 |
| DU-P2a | Hip-joint placement | Hip-joint height ÷ stature **< MF** as the joint result of shorter femur + lower leg; the pelvis keeps a full adult vertical extent below the hip joints (no truncation, no squashed acetabular region). | DU L38, L119, L21 |
| DU-P2b | Hip-joint spacing | Inter-acetabular spacing ÷ stature **> MF** (the "broad foundation / stable hip placement"), with the femora converging to an ordinary relaxed stance (no built-in wide stance, bowing or splay). | DU L32, L108, L121, L430 |
| DU-P2c | Hip-joint scale | Hip-joint scale **> MF** relative to stature and femur length; integrated, never enlarged independently. | DU L40 |
| DU-P3 | Iliac structure | Robust construction (greater crest/landmark structural presence than MF at matched stature). Iliac height **not** raised to match breadth: pelvic vertical contribution ÷ iliac-crest breadth **< MF** (a broad, compact pelvis, not a tall one). | DU L11, L21, L32, L97; SRR L17 |
| DU-P4 | AP depth | AP depth ÷ stature **> MF**, continuous with the deep thorax (no abrupt shallow step at the lower trunk). **Inference flagged** (pelvic depth is not named; derived from "strong torso-pelvis continuity" + "substantial thoracic depth" + L91 no widening in isolation). Author confirms (PV-D8). | DU L25, L29, L91, L108 |
| DU-P5 | Transverse breadth | Iliac-crest breadth ÷ stature **> MF**; frame shifts it (Narrow keeps a Durrim minimum; Broad "never every dimension equally"). | DU L32, L52, L109, L127, L129 |
| DU-P6 | Lower trunk | **Thorax-led concentration:** iliac-crest breadth ÷ thoracic breadth **not above MF** (the broad pelvis is continuous with, not more prominent than, the broad thorax). Waist interval present but compact. **Proposed to separate DU from PK** (PK L150 is the opposite direction). Author decides (PV-D9). | DU L25 "The torso carries a major part of Durrim identity"; DU L97; PK L150, L162 |

**Why this is not "a simply widened human pelvis":** breadth (P-5) moves together with hip spacing (P-2b), hip-joint scale (P-2c), robustness (P-3), AP depth (P-4) and a compact height-to-breadth proportion (P-3), each tied to a separate DU line; a widened MF pelvis changes P-5 only.

### 4.5 Skeleton vs composition

- Skeleton: P-1…P-6. Composition: hip fat, glutes, thigh muscle, belly (DU L104, L109; UCCA L156). "external hip width never stands in for skeletal width" (DU L109). A low-muscle, low-fat Durrim must show DU-P4/P5 (DU L52).
- Sex: no authored shift (RA L53; DU L532). Obstetric: none.

### 4.6 Build implication and verification

- Replace generator pelvis + `hip-scale-horiz-incr 0.15` (ARM-DU L35), which ARM-DU L26 itself names "exactly the prohibited form".
- RM-UB-06 (vs MF at matched stature, and at the 152 cm equal-height case DU L72): crest breadth ÷ stature > MF; bitrochanteric ÷ stature > MF; AP depth ÷ stature > MF (if PV-D8); vertical ÷ crest breadth < MF; crest ÷ thoracic breadth ≤ MF (if PV-D9; uses existing thorax breadth reading).
- Hip-joint scale and robusticity are not RM-UB-06 items → render check / RM joint-breadth readings.

---

## 5. Grask (GR)

### 5.1 Canon quotes

**Body architecture**
- GR L9: "Grask are a distinct tall humanoid population defined by elongated, rangy skeletal architecture, substantial functional reach, a relatively slender skeletal silhouette for its stature (a skeletal proportion, not low body fat; §6–7) …"
- GR L11: "The silhouette emphasizes … a compact-to-moderate torso contribution compared with limb length, distinct shoulder and pelvic architecture, … It avoids gorilla caricature, ape posture, a hunched monster silhouette, a giant human silhouette, an extremely narrow stick figure and a bodybuilder troll."
- GR L188: "> **Grask anatomy must read as a coordinated rangy skeletal system, not a human skeleton with individually stretched limbs.**"
- GR L192: "> **Tall stature combined with increased limb contribution to total height, increased arm span relative to height, and coordinated elongation of multiple limb segments without equivalent elongation of every axial body region.**"

**Torso / lower trunk**
- GR L37: "Torso contribution | Trends toward a lower contribution to standing height than Marchfolk and Skarn, producing the long-limbed silhouette, while staying functional, organically proportioned and open to broad composition; never a tiny torso on giant limbs"
- GR L198: "A Grask torso can be large in absolute dimensions while contributing proportionally less to height, so **proportionally reduced torso contribution** never means **small torso**."
- GR L38: "Thorax | Moderate skeletal breadth, meaningful thoracic depth, a relatively elongated but not oversized ribcage …"
- GR L203–204: "Thoracic breadth | May be substantial in absolute terms at reference height, but generally reads less broad relative to stature than Skarn" / "Thoracic depth | Meaningful: never paper-thin for a rangy look, and never approaching Durrim proportional depth"
- GR L207: "Waist and abdomen | Broad variation in skeletal waist relationship …; no required extremely narrow waist, V-shaped torso or gaunt abdomen"
- GR L44: "Spine | Supports upright bipedal resting alignment; spinal curvature is never the source of troll identity"

**Pelvis directly**
- GR L45: "Pelvis | Distinct and suited to tall stature, long legs, bipedal locomotion and center-of-mass relationships; exact morphology **OPEN**, never a narrowed or scaled human pelvis"
- GR L208: "Pelvis | Locked functional requirement: **Grask pelvis geometry must coordinate long lower limbs, upright bipedal locomotion and the Grask torso without being created by simply scaling or narrowing a human pelvis.** Exact morphology **OPEN**"
- GR L209: "Pelvic breadth | Supports Narrow, Balanced and Broad frames, with external hip width kept distinct from skeletal pelvic breadth, gluteal muscle and fat distribution"
- GR L716: "The Grask stays Grask through non-limb carriers: thoracic and shoulder breadth relative to stature, non-human girdle and pelvic organization, neck relationship, hand and digit relationships, craniofacial verticality and ear architecture"

**Legs / femur / hip**
- GR L52: "Legs | A major identifier: greater lower-limb contribution to standing height than the Marchfolk Human Reference Population and Skarn at matched normalized height …, coordinated with pelvis, torso, spine, arms and feet"
- GR L53: "Femur | Long in absolute terms and a strong contributor to leg length, but never simply stretched; coherent with hip, knee, muscle attachment and locomotion"
- GR L213: "Femora trend toward long absolute length and greater contribution to stature than human reference anatomy, coordinated with pelvis, knee, lower leg and muscle distribution."
- GR L217: "Leg elongation fails if it creates stilt-like anatomy, an extremely high crotch, a tiny-looking torso, fragile knees or an unnatural hip transition. Knees are substantial in absolute structure for Grask stature and long lever arms … (**visually narrow never means structurally weak**)."

**Comparisons**
- GR L267: "Grask keep larger absolute structure, a different torso and pelvis system and greater rangy reach organization" (vs Fenn).
- GR L708: "Grask limb-dominant elongation with different torso, pelvis, joints, reach and craniofacial and ear anatomy; fails as "heavier Aelari""
- LRR L57: "Pelvis | "more substantial" (S L77) | Distinct, non-human; morphology OPEN (GR L45, L208) | Load-bearing, integrated with the axial body; OPEN … | Architectural difference only; morphology OPEN for Grask and Gorrund"
- GR L740: "**Sex-related anatomy:** no authored shift in skeleton, stature, frame or composition; magnitude stays OPEN"

### 5.2 Canon already implies

1. **Not scaled and not narrowed** (L45, L208): the slender silhouette (L9) cannot be produced by narrowing the MF pelvis, nor by scaling it with stature.
2. **Pelvis coordinates three things**: long lower limbs, upright bipedal locomotion, the Grask torso (L208) → its size follows the torso (large in absolute terms, proportionally lower contribution, L198), and its hip organization follows the long femora (L53, L213).
3. **Leg share > MF and SK without a "high crotch" or "unnatural hip transition"** (L52, L217) → the pelvis below the hip joints is not truncated to gain leg length.
4. **Joints substantial in absolute structure for long lever arms** (L217 states this for knees; L53 for "coherent with hip").
5. **"Non-human … pelvic organization"** is a named identity carrier vs Skarn (L716) — an architectural, not size, difference (LRR L57).
6. Curvature is not identity (L44). No sex shift (L740).

### 5.3 Genuinely OPEN

- **What** makes the organization "non-human" (L716) — no feature named.
- Breadth, AP depth, vertical contribution vs MF and SK (only the thorax is ordered: less broad relative to stature than SK, L203).
- Hip-joint scale relative to pelvis; femoral-neck/trochanter relation; iliac shape; sacrum. "Exact morphology OPEN" (L45, L208, L728).

### 5.4 PROPOSAL (BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED)

| # | Descriptor | Proposal | Derived from |
|---|---|---|---|
| GR-P1 | Spine/sacral | Human-homologous lumbosacral relationship supporting upright alignment; neutral curvature. | GR L44; RA L124 |
| GR-P2a | Hip-joint placement | Hip-joint height ÷ stature > MF and SK through femur + lower-leg length; **pelvic inferior extent below the hip joints is kept in full adult relation to the pelvis** (no truncation; no high crotch). | GR L52, L213, L217 |
| GR-P2b | Hip-joint organization ("leverage") | Hip-joint scale and proximal-femur structure **substantial in absolute terms and not reduced relative to femur length** (long-lever hips), even where the pelvis reads slender relative to stature; bitrochanteric ÷ crest breadth **≥ MF**. Proposed reading of "non-human … pelvic organization": **the pelvis is proportioned to the Grask torso while the hip apparatus is proportioned to the long femora.** | GR L53, L208, L217, L716 |
| GR-P3 | Iliac structure | Iliac breadth and height proportioned to the Grask torso (large absolute, proportionally reduced like the torso); construction "visually narrow never means structurally weak". | GR L198, L217 |
| GR-P4 | AP depth | AP depth "meaningful", continuous with the meaningful thoracic depth; ÷ stature not > MF (follows the reduced torso share; never Durrim-like). **Inference flagged.** | GR L38, L204, L198 |
| GR-P5 | Transverse breadth | Crest breadth ÷ stature **not greater than MF**, as a **consequence** of torso-proportioning (GR-P3), never of a narrowing operation on an MF pelvis; Narrow–Broad frames. | GR L9, L45, L198, L208, L209 |
| GR-P6 | Lower trunk | Waist interval "broad variation" — no Grask direction; pelvis-to-thorax breadth ≈ MF (no authored departure). | GR L207 |

**Why this is not "scaled or narrowed human":** a scaled MF pelvis keeps the MF ratio between pelvic size and hip-apparatus size; a narrowed one reduces hip spacing with breadth. GR-P2b/P3 **decouple** them: the pelvis follows the torso, the hip apparatus follows the femora. **Flag:** whether this decoupling is enough to be "non-human pelvic organization" is Decision PV-D1 / PV-D12.

### 5.5 Skeleton vs composition

- GR L209 separates skeletal breadth from external hip width, glutes and fat; GR L9 "slender … (a skeletal proportion, not low body fat)". Composition never creates or erases GR-P5.
- Sex: no shift (RA L53). Obstetric: none.

### 5.6 Build implication and verification

- ARM-GR L27: "Pelvis and shoulder girdle: non-human morphology not authored; generator human structure carried." The GR candidate has **no hip target** (generator pelvis scaled with the body), i.e. the "scaled human pelvis" form. A compliant build sizes the pelvis to the torso and the hip apparatus to the femora.
- RM-UB-06 (vs MF and SK at matched normalized stature): crest breadth ÷ stature ≤ MF (GR-P5); bitrochanteric ÷ crest ≥ MF (GR-P2b); AP depth ÷ stature ≤ MF (GR-P4); pelvic vertical contribution follows the torso share (no independent direction); hip-joint height ÷ stature > MF and SK (existing RAC-04). Hip-joint scale ÷ femur length: not RM-UB-06 → joint-breadth reading.
- This packet runs alongside the §8 shoulder-girdle packet; the girdle has the same "visibly distinct from widened human" wording (GR L206).

---

## 6. Gorrund (GO)

### 6.1 Canon quotes

**Body architecture**
- GO L9: "Gorrund are a distinct large humanoid population defined by massive load-bearing skeletal architecture, high absolute structural scale, broad/deep body organization, substantial joints and strong axial-to-limb integration."
- GO L19: ""Massive" means biological structural scale first (skeletal breadth and depth, joint dimensions, axial scale, pelvic structure, limb-bone structural dimensions), never automatically muscular, fat or heavy-looking from clothing."
- GO L165: "> **Gorrund anatomy must read as a coordinated massive load-bearing skeletal system, not as a human body enlarged uniformly or as independent width/depth sliders applied to a generic humanoid.**"
- GO L167: "The body signature comes from the combination of high absolute skeletal scale, broad and deep axial construction, substantial shoulder and pelvic architecture, large load-bearing joints … "Axial" means structural emphasis through spine, ribcage, shoulder girdle, pelvic integration and torso-to-limb transitions, never a torso that visually overwhelms the limbs."
- GO L39: "Axial skeleton | A major identifier: broad skeletal thorax, substantial thoracic depth, strong vertebral and torso integration, substantial shoulder girdle and pelvis, strong neck-to-torso integration; never a rectangular block"

**Torso / lower trunk**
- GO L42: "Thoracic depth | A major dimension: **Gorrund trend toward substantial thoracic skeletal depth relative to stature and breadth, producing a genuinely three-dimensional load-bearing torso rather than a wide but shallow body**"
- GO L175: "Thoracic breadth, depth and vertical length, abdominal vertical contribution, waist skeletal relationships, and pelvic breadth and depth are independent, never one Torso Mass concept."
- GO L169: "> **Gorrund generally possess a greater proportional torso contribution to total standing height than Grask at matched height, while retaining fully adult, functional limb lengths.**"
- GO L188: "Shoulder-to-pelvis | Continuous variation from more shoulder-dominant through balanced to more pelvis-present, not subtypes"
- GO L191: "Spine | Supports the torso without permanent forward lean, exaggerated lumbar arch or hunch; neutral posture stays upright"
- GO L737: "Torso verticality | … Not compact: substantial ribcage vertical length and large axial vertical contribution suited to a tall body, so a Gorrund is never a vertically scaled Durrim"

**Pelvis directly**
- GO L49: "Pelvis | Distinct, suited to high structural scale, broad and deep torso, large lower limbs and upright locomotion; morphology **OPEN** for Part 2 and validation, never a uniformly enlarged human pelvis"
- GO L50: "Pelvic breadth | May trend substantial, with external hip width kept separate from muscle, fat and sex-related anatomy"
- GO L189: "Pelvis | **Gorrund pelvises possess substantial load-bearing skeletal dimensions and strong integration with both the deep axial torso and large lower limbs**, with meaningful breadth, depth and hip-joint scale; exact morphology **OPEN**. Not every pelvis is extremely broad, and a narrower valid pelvis still supports large hip joints and femora, upright gait and axial integration"
- GO L190: "Pelvis vs hips | Skeletal pelvic breadth, gluteal muscle and regional fat stay separate; external hip circumference is never a proxy"

**ALPC**
- GO L715: "> **Gorrund possess pronounced axial load-path continuity: the shoulder girdle, thoracic structure, lower axial trunk, pelvis and proximal lower limbs form a strongly integrated vertical load-bearing chain, with skeletal transitions that preserve substantial structural continuity from the upper torso through the pelvis into the legs.**"
- GO L717: "The body reads as one load-bearing system, **shoulder girdle → thorax → lower axial trunk → pelvis → hip and proximal femur** … It never means uniform torso width, no waist, a rectangular or barrel body, a giant pelvis or shoulders, a thick abdomen, high fat or muscle, column-shaped legs or one "massiveness" slider."
- GO L722: "Thorax to lower trunk | The broad, deep thorax transitions without abrupt skeletal collapse, while visible waist definition, narrower frames, low fat and athletic composition stay valid; the relationship is skeletal load paths, not circumference"
- GO L723: "Lower trunk to pelvis | The pelvis reads as integrated with the axial body, not an independently widened hip structure; morphology stays **OPEN** but its relationship to the torso is now positively constrained"
- GO L724: "Pelvis to leg | Hip-joint scale, proximal femur, pelvis and upper-leg dimensions suit receiving load from the pelvis and axial skeleton, never mandatory enormous thighs"
- GO L725: "Narrow frame | Keeps the continuity: reduced breadth never removes thoracic depth, joint scale, pelvic and proximal-limb integration or structural continuity (a critical identity test)"

**Frame / composition / legs**
- GO L220: "**Narrow** Gorrund may reduce relative thoracic, shoulder and pelvic breadth within valid limits but keep meaningful thoracic depth, substantial joints, large long-bone scale and strong axial integration."
- GO L222: "> **Narrow skeletal breadth does not automatically mean low skeletal depth.**"
- GO L76: "This is one of the strongest body signals across shoulders, elbows, wrists, hips, knees and ankles."
- GO L196: "**Gorrund lower limbs generally contribute less proportionally to standing height than Grask lower limbs at equal height**, never meaning short-legged. Femora have large absolute length and cross-sectional scale with strong hip and knee integration"

**Comparisons**
- GO L239: "Gorrund: a distinct non-human load-bearing system with greater axial depth and structural scale beyond "big human" and distinct joint, torso and pelvis relationships. Fails as "extra-broad Skarn""
- GO L238: "Gorrund: greater axial contribution, thoracic breadth and depth, joint presence, larger load-bearing relationships and pelvis-torso integration. Fails if the distinction depends on muscle or fat" (vs Grask)
- GO L739: "Durrim and Gorrund with similar normalized torso breadth stay distinct through torso vertical relationships, limb contribution, pelvic relationships and shoulder-thorax and pelvis-leg integration, never breadth alone."
- SA L145: "- no Gorrund-like massive load-bearing pelvis;"
- GO L757: "Skarn–Gorrund torso/limb separation stays undetermined by design (AD-4)."

### 6.2 Canon already implies

1. Not uniformly enlarged (L49), not an "independently widened hip structure" (L723), not "a giant pelvis" (L717).
2. **Meaningful breadth, depth and hip-joint scale** (L189) — depth is named for the pelvis.
3. **Integrated with the deep axial torso**: thorax → lower trunk → pelvis without abrupt skeletal collapse (L715, L722, L723) → pelvic AP depth is continuous with the substantial thoracic depth.
4. **Hip joints and proximal femora sized to receive axial load** (L724; L189 "large hip joints and femora" even in a narrower pelvis) → hip-joint scale is **not** proportional to pelvic breadth; it stays large when breadth is low.
5. **Narrow keeps ALPC**: reduced breadth never removes depth, joint scale or integration (L220, L222, L725).
6. Breadth "may trend substantial" (L50) but not every pelvis is extremely broad (L189).
7. Large axial vertical contribution; torso share > GR (L169, L737). Torso share vs SK undetermined (AD-4) → **no** pelvic vertical direction vs SK may be authored.
8. Spine: no exaggerated lumbar arch (L191). Sex: no shift (L757).

### 6.3 Genuinely OPEN

- Pelvic depth-to-breadth proportion vs MF/SK (thoracic depth "relative to … breadth" is stated, L42; the pelvis is not).
- Pelvic breadth relative to lower-trunk breadth (how wide the pelvis may be while staying "integrated, not independently widened").
- Sacral breadth/robusticity (the lumbosacral link in the load path is implied by L717 but not described).
- Iliac shape; vertical contribution. "morphology OPEN" (L49, L189, L703).

### 6.4 PROPOSAL (BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED)

| # | Descriptor | Proposal | Derived from |
|---|---|---|---|
| GO-P1 | Spine/sacral | **Robust lumbosacral link in the load path:** sacrum and lumbosacral junction broad and robust relative to the lumbar column so the lower axial trunk transfers into the pelvis without a structural "neck"; human-homologous orientation; no exaggerated lumbar arch. **Inference flagged** (sacrum not named). | GO L715, L717, L191 |
| GO-P2a | Hip-joint scale | Hip-joint and proximal-femur scale **large in absolute terms and relative to pelvic breadth** (hip-joint scale ÷ crest breadth ≥ MF and ≥ SK); held at Narrow frame. | GO L76, L189, L724, L725 |
| GO-P2b | Hip-joint placement | Hip joints placed **under the axial load path** (bitrochanteric ÷ crest breadth ≈ MF, no lateral outrigging); leg share < GR, never short-legged. | GO L723, L724, L196 |
| GO-P3 | Iliac structure | Iliac breadth **bounded by the lower trunk**: crest breadth continuous with lower-trunk breadth (the pelvis does not project laterally as an independent hip structure); robust construction; vertical contribution supports "large axial vertical contribution" (≥ GR relative to stature). | GO L717, L723, L737, L169 |
| GO-P4 | AP depth | **Depth-led pelvis:** AP depth ÷ crest breadth **> MF and > SK**, continuous with the deep thorax; held at Narrow frame. **Inference flagged** (transfers L42's thoracic "depth relative to … breadth" to the pelvis through L722–723 continuity). Author confirms (PV-D14). | GO L42, L189, L222, L722, L723, L725 |
| GO-P5 | Transverse breadth | "May trend substantial"; no single breadth identity; Narrow valid. Breadth is **not** the ALPC carrier. | GO L50, L189, L220 |
| GO-P6 | Lower trunk | Thorax → lower trunk → pelvis with **no abrupt step in breadth or depth** (waist definition allowed); shoulder-to-pelvis balance free (L188). | GO L188, L722, L723 |

**Why this is not "a uniformly enlarged human pelvis":** uniform enlargement keeps the MF depth : breadth and hip-joint : breadth ratios. GO-P2a and GO-P4 move both ratios upward, and GO-P3 bounds breadth by the trunk — so the GO pelvis grows **in depth and hip-joint scale more than in breadth**. That is the pelvic share of ALPC.

### 6.5 Skeleton vs composition

- GO L190: "Skeletal pelvic breadth, gluteal muscle and regional fat stay separate; external hip circumference is never a proxy". GO L726–727: ALPC "fails if it appears only once muscle is added"; "Low fat reveals rather than creates the structure".
- Sex: no shift (RA L53). Obstetric: none.

### 6.6 Build implication and verification

- Replace generator pelvis + `hip-scale-horiz-incr 0.30, hip-scale-depth-incr 0.30` (ARM-GO L36; ARM-GO L27 "prohibited form").
- Coordinate with the §8 large-race girdle/ALPC packet: the pelvis is the lower half of RM-LR-06.
- RM-UB-06 (vs MF, SK, GR at matched normalized stature; plus the Narrow GOR-BODY-12/14 variant): AP depth ÷ crest breadth > MF and SK (GO-P4); bitrochanteric ÷ crest ≈ MF (GO-P2b); crest breadth ÷ lower-trunk breadth not above MF (GO-P3; needs a lower-trunk breadth reading at the costal margin, PV-D15); hip-joint scale ÷ crest breadth ≥ MF/SK (joint-breadth reading). **No pelvic-vertical direction vs SK** (AD-4).

---

## 7. Pipkin (PK)

### 7.1 Canon quotes

**Body architecture (LSCTA)**
- PK L133: "> **Pipkin possess a low-set compact trunk architecture in which a mature, structurally broad pelvis contributes strongly to the central body silhouette while the thorax remains comparatively moderate in breadth and depth and the limbs retain substantial proportional contribution to total stature.**"
- PK L135: "The core relationship is **moderate thorax → compact lower trunk → mature structurally broad pelvis → proportionally sustained limbs** … **Low-set** means the relative structural importance of the lower trunk and pelvis within the adult body, never a sagging torso, low posture, short legs, crouching, low shoulders or a heavy belly. **Compact trunk** never means Durrim-like vertical compression, no waist, a barrel or round body or high fat; Pipkin stay less vertically compact than Durrim."
- PK L137: "Pipkin trend toward a **modestly reduced vertical central-trunk contribution to total stature**, a compact lumbar/waist transition, and a mature pelvis whose vertical height, depth and three-dimensional structural participation remain substantial relative to the thorax. This lower-trunk-centered organization persists even when pelvic breadth approaches Marchfolk-like values. … The reduced trunk share is absorbed primarily through **sustained limb contribution and pelvic vertical contribution, not through enlargement of the head**."
- PK L139: "The numeric split between limb and pelvic contribution stays deferred (UCCA RM-UB-01; short-race RM-SR items); no winner is invented."
- PK L141: "Pipkin show more compact central trunk organization, greater pelvic structural contribution relative to thoracic scale, proportionally sustained limbs despite short stature and a distinct thorax-to-pelvis relationship."
- PK L37: "Body identity emerges from short adult stature, light construction, moderate torso compactness, preserved functional limb contribution, smaller joints …"
- SRR L18: "**Pipkin** | **Low-Set Compact Trunk Architecture** | light compact adult skeleton → moderate thorax → compact lower trunk → mature structurally broad pelvis → proportionally sustained limbs"

**Pelvis directly**
- PK L50: "Pelvis | Distinct and adult, suited to short stature, lighter construction and preserved limbs, morphology **OPEN**; **never a scaled-down juvenile pelvis** (mandatory) and never Durrim pelvic proportions reused because both are short"
- PK L150: "Thorax vs pelvis | **The pelvis carries greater structural importance relative to the thorax than in Marchfolk reference anatomy** (a tendency, not a fixed ratio)"
- PK L151: "Pelvic breadth | Meaningful adult breadth relative to torso scale, never extremely wide hips, feminized anatomy, high fat or one hourglass silhouette; this is skeletal anatomy"
- PK L152: "Pelvic depth | Appropriate adult three-dimensional depth, never a widened scaled human pelvis (morphology **OPEN**)"
- PK L153: "Pelvic maturity | Fully mature adult anatomy, especially important for the adult Pipkin and human child test"
- PK L156: "Thorax-to-pelvis transition | A coherent adult transition through lower ribcage, waist, abdomen and pelvis, never an abrupt "small chest → huge hips""
- PK L162: "Pelvis | Participates in **compact structural concentration** | Participates in **low-set compact trunk architecture with sustained limb contribution**; the two never share one pelvis (morphology for later prototyping)"
- PK L168: "Frame may influence pelvic breadth, but Narrow never erases the Pipkin pelvic relationship and Broad never exaggerates it into caricature. Pipkin stay lightly constructed relative to Durrim at matched height across long bones, joints, thorax, shoulder girdle and pelvis, while the mature pelvis may still be prominent relative to their own thorax; these are compatible."
- PK L198: "Lower valid pelvic breadth stays Pipkin, so pelvic width alone isn't the identifier"
- PK L234–235: "PIP-STRESS-06 | Greater pelvic contribution with lower thoracic breadth, coherent" / "PIP-STRESS-07 | Lower pelvic breadth with greater thoracic breadth, still Pipkin (the race isn't one hip-width ratio)"
- PK L1537: "- detailed pelvic morphology, including depth and implementation-ready dimensional relationships;"

**Legs / hip / gait / posture**
- PK L56: "Femora are never uniformly shortened human femora"
- PK L166: "Legs contribute more to standing height than Durrim legs at matched height but never automatically exceed ordinary human adult proportions"
- PK L49: "Spine | **Upright adult humanoid spinal alignment**, no mandatory hunch, crouch or lean"
- PK L703–709: "Low-Set Compact Trunk Architecture does **not** require: … - permanently flexed hips or knees, … - exaggerated lumbar arch,"
- PK L714: "Standing posture must remain compatible with the mature pelvis, moderate thorax, compact lumbar/waist transition and sustained limb contribution"
- PK L746: "Despite the mature pelvis's strong structural role, ordinary Pipkin walking retains an **adult narrow-base gait**: foot placement converges appropriately toward the line of progression relative to hip width rather than translating pelvic breadth into a toddler-like wide base or waddle."
- PK L750: "The mature pelvis is a major part of Pipkin body architecture, but movement must not turn that into exaggerated side-to-side hip motion."

**Durrim boundary**
- PK L194: "Pelvic breadth is not the primary discriminator. … The boundary is carried jointly by torso vertical organization, thoracic breadth/depth and axial presence, limb contribution, joint dimensions, long-bone robusticity, extremity integration and the two distinct trunk systems."

**Composition / sex**
- PK L155: "External hip width | Skeletal breadth, gluteal muscle, fat distribution and external circumference stay separate"
- PK L184: "> **Pelvic skeletal contribution is not wide hips caused by body fat.**"
- PK L186: "Low-fat Pipkin are validated so the pelvic architecture stays readable"
- PK L154: "Where sex-related anatomy materially affects pelvis or thorax, compare like-for-like anatomical configurations …; racial identity is never defined by shoulder-to-hip ratio or external hip circumference"
- PK L1491–1494: "Sex-related physical anatomy may influence relevant pelvic, thoracic, facial, soft-tissue and other biological relationships, but: … - racial identity is not defined by external shoulder-to-hip ratio or sex-coded presentation."

### 7.2 Canon already implies

1. **Pelvis-to-thorax prominence > MF** (L150, L141) across **vertical height, depth and 3-D participation**, not breadth alone (L137 lists "vertical height, depth"; L198, L235 make breadth non-identifying).
2. **Pelvic vertical contribution participates in absorbing the reduced trunk share** (L137) — direction toward greater pelvic vertical contribution relative to the thorax; **relative to stature the split is deferred** (L139, T-2: "no winner is invented"). *Uncertainty flag:* W1c-AUD row 106 tested "pelvic vertical contribution / stature > MF" as a canon direction; strictly, canon fixes only "substantial relative to the thorax" plus non-zero absorption — the per-stature magnitude is T-2.
3. **Compact lumbar/waist transition** (L137, L714) but a coherent transition, not abrupt (L156).
4. **Light construction**, lighter than DU at matched height (L37, L50, L168; SRR L18).
5. **Fully mature, never juvenile** (L50, L153).
6. **Never DU proportions; never one pelvis with DU** (L50, L162).
7. **Narrow-base adult gait under a broad pelvis** (L746) → femora converge from the hip joints toward the midline.
8. Upright spine, no exaggerated lumbar arch (L49, L709).
9. Sex regions named (L1491) but no direction; R-SEX no shift for the W1 configuration (RA L53).

### 7.3 Genuinely OPEN

- Depth and "implementation-ready dimensional relationships" (L152, L1537).
- Pelvic vertical contribution **relative to stature** (T-2 split, L139).
- Breadth relative to stature vs MF (canon: "meaningful adult breadth relative to torso scale"; persists near MF values).
- Iliac shape; sacrum; femur-to-lower-leg balance (L56, L166 OPEN).

### 7.4 PROPOSAL (BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED)

| # | Descriptor | Proposal | Derived from |
|---|---|---|---|
| PK-P1 | Spine/sacral | Upright adult lumbosacral relationship; neutral curvature; no exaggerated lumbar arch. | PK L49, L709; RA L124 |
| PK-P2a | Hip-joint placement | Hip joints set below a **vertically substantial** pelvis; leg share > DU at matched height and not above MF. | PK L137, L166; RAC-04 L31 |
| PK-P2b | Hip-joint organization | **Broad pelvis, convergent femora:** femoral shafts converge medially from the hip joints so knees and feet sit on an adult narrow base (bitrochanteric breadth does not translate into a wide stance). Hip-joint scale lighter than DU at matched height, adult, above J-1. | PK L746, L68, L168; RA L125 |
| PK-P3 | Iliac structure | **Iliac height substantial relative to the thorax:** pelvic vertical contribution ÷ thoracic vertical length **> MF**; pelvic vertical contribution ÷ stature **≥ MF** (direction only; magnitude deferred to T-2/RM-SR-01; PV-D10). Light construction (lighter than DU); fully mature form. | PK L137, L139, L150, L168, L50 |
| PK-P4 | AP depth | AP depth ÷ thoracic depth **> MF** (pelvis 3-D participation substantial relative to a moderate thorax); AP depth ÷ stature: no direction (OPEN). | PK L137, L149, L152 |
| PK-P5 | Transverse breadth | Crest breadth ÷ thoracic breadth **> MF** at the population centre; crest breadth ÷ stature **not a carrier** (may approach MF); never extreme. | PK L133, L137, L150, L151, L198 |
| PK-P6 | Lower trunk | **Compact waist interval** (costal margin–crest ÷ torso length < MF), with a coherent, non-abrupt transition. | PK L137, L156, L714 |

**Why this is not "a widened scaled human pelvis" (L152) or a juvenile one (L50):** the PK pelvis is defined by its **proportion to the thorax in three dimensions** (P-3, P-4, P-5) and by a compact waist (P-6), with mature form and convergent femora; breadth alone may sit near MF and the identity persists (L137, L198).

### 7.5 Skeleton vs composition

- PK L155, L184, L186: skeletal breadth ≠ hip fat/glutes; low-fat Pipkin must show the pelvic architecture. "never … feminized anatomy, high fat or one hourglass silhouette" (L151).
- Sex: regions named, no direction; like-for-like comparisons (L154); PIP-BODY-29 waits (RA L53). Obstetric: none.

### 7.6 Build implication and verification

- B-1 (native short-adult base, order §5) is a prerequisite: the W1c PK is a ×0.7675 uniform-scale proxy (W1c-GATE L42) with generator `hip-scale-depth/horiz/vert-incr` targets (ARM-PK L35). Its pelvic readings are proxy-only.
- RM-UB-06 + RM-SR-01: crest ÷ thoracic breadth > MF (PK-P5); AP depth ÷ thoracic depth > MF (PK-P4); pelvic vertical ÷ thoracic vertical length > MF (PK-P3; needs a thoracic-vertical landmark); vertical ÷ stature ≥ MF (direction only, PV-D10); waist interval < MF (PV-D15); femoral convergence on the front render (knee/ankle spacing < bitrochanteric).

---

## 8. Collision checks — short races (DU–PK–CG)

### 8.1 Comparative canon

- SRR L21: "These are different anatomical mechanisms, not three settings on a single short-body slider."
- SRR L53: "### Durrim / Broad/deep, vertically compact thoracic architecture with strong torso-pelvis continuity and high structural presence."
- SRR L56: "### Pipkin / Moderate thorax transitioning through a compact lower trunk into a mature pelvis that carries strong silhouette importance."
- SRR L59: "### Cogling / Comparatively narrow stable central core with adult axial/trunk contribution broadly near the Marchfolk adult proportional range; the pelvis is mature but not the primary silhouette anchor."
- SRR L61: "**Boundary rule:** a Broad Cogling cannot become Durrim by increasing width; a Narrow Durrim cannot become Cogling by reducing muscle; a Pipkin cannot be reduced to the midpoint between them."
- SRR L41: "**Cogling → Pipkin → Durrim** broadly progresses from finer to greater skeletal structural presence." / SRR L43: "This is not a universal linear morph"
- SRR L226: "Pipkin low-set trunk/pelvic relationships"
- SRR L261: "> **Durrim concentrate structure. Pipkin organize a light adult body around a low-set compact trunk and mature pelvic foundation. Cogling redistribute fine-scale articulation distally within a narrow stable adult body.**"
- PK L50, L162, L194 (quoted in §7.1).
- CG L102: "The pelvis is mature and integrated without becoming the dominant silhouette anchor."
- CG L258–262: "The pelvis must provide adult locomotor and sex-related anatomy without becoming: - childlike/narrow through immaturity; - Pipkin's primary lower-trunk identity mechanism; - Durrim-like structural mass; - or an external hip-width stereotype."
- CG L649: "At normalized height, Cogling trend toward a comparatively narrow transverse core while retaining sufficient depth and pelvic maturity for a healthy adult body."
- CG L685–687: "Compared with Pipkin, the pelvis does not carry the same primary silhouette role relative to the thorax. / Compared with Durrim, it has lower structural mass and breadth/depth emphasis."
- CG L691: "Exact pelvic breadth, depth, height, inlet/outlet morphology and external soft-tissue expression remain OPEN."
- CG L705: "Cogling do not require a shortened spine, long waist or compressed vertebral column."

### 8.2 Cogling (context only; no proposal authored here)

Canon-implied CG pelvis: narrow transverse core with the thorax (CG L100, L649); mature (L256); pelvis-to-thorax role ≤ PK (L685); lower structural mass and breadth/depth than DU (L687); torso share ≈ MF, no shortened spine or long waist (L100, L705). Default per §0.4: **human-homologous, narrow-core, fine construction, pelvis-to-thorax ≈ MF.** Inlet/outlet stays class D (CG L691; RAC-03 L52).

### 8.3 Pairwise checks of the proposals

| Pair | Proposals compared | Separate? | Contradiction with canon? | Residual risk |
|---|---|---|---|---|
| **DU–PK** | DU: thorax-led, crest ÷ thorax breadth ≤ MF (DU-P6), squat pelvis (vertical ÷ breadth < MF, DU-P3), robust, deep, waist compact-but-present. PK: pelvis-led, crest ÷ thorax breadth > MF (PK-P5), pelvic vertical ÷ thoracic vertical > MF (PK-P3), light, waist compact. | **Yes**, on two opposite-signed ratios (pelvis÷thorax breadth; pelvic vertical÷breadth) plus construction. Breadth ÷ stature may coincide — allowed, since "Pelvic breadth is not the primary discriminator" (PK L194). | None. Matches PK L162 "the two never share one pelvis", PK L50 "never Durrim pelvic proportions reused", SRR L53/L56. | **High if PV-D9 is rejected.** W1c diagnostic evidence (generator human pelvis + breadth targets; PK is a proxy): DU vs PK crest ÷ H 0.187 vs 0.190, bitrochanteric ÷ H 0.228 vs 0.227, vertical ÷ H 0.063 vs 0.062, AP depth ÷ H 0.147 vs 0.139 (W1c-MEAS L51–54) — near-identical external pelvic ratios. What separates them in W1c is the thorax: crest ÷ thoracic breadth DU ≈ 0.80 (0.187 ÷ 0.235, W1c-MEAS L42, L51) vs PK 0.912 (W1c-AUD L161), MF 0.869. These are builder-forced (RA L84) and **not** canon; they only show that a breadth-target method converges the two pelves and that the pelvis÷thorax relation is the carrier. Composition stress (SRR L126 "Broad/high-muscle Pipkin becoming Durrim") is handled by DU-P3/PK-P3 construction and the vertical proportion, not by breadth. |
| **PK–CG** | PK: pelvis-led, compact waist. CG: narrow core, pelvis-to-thorax ≈ MF, waist not shortened (CG L705). | **Yes**: pelvis÷thorax PK > MF vs CG ≈ MF; waist interval PK < MF vs CG ≈ MF. | None. Matches CG L260 ("not … Pipkin's primary lower-trunk identity mechanism"), CG L685, SRR L133 (SR-COMP-01: "near-Marchfolk Cogling axial/trunk share versus modestly reduced Pipkin vertical central-trunk share"). | **Medium at 91–107 cm overlap** (SRR L31): a Narrow-frame PK (PK L168 "Narrow never erases the Pipkin pelvic relationship") vs a Broad CG. Carrier must be the pelvic **vertical/depth** relation to thorax (PK-P3, PK-P4), not breadth (SRR L127 "Narrow/low-fat Pipkin becoming Cogling"). |
| **DU–CG** | DU: broad, deep, robust, squat. CG: narrow core, fine. | **Yes** on every descriptor. | None. CG L261, L687; SRR L61. | Low (no stature overlap, SRR L33). SR-COMP-04 normalized test: Broad CG vs Narrow DU separated by robusticity and depth (DU-P4), not breadth (SRR L61). |

**Midpoint check (SRR L61, "a Pipkin cannot be reduced to the midpoint between them"):** on pelvis÷thorax breadth the proposals order DU ≤ MF ≈ CG < PK, i.e. PK is an **end**, not a midpoint — consistent. On construction they order CG < PK < DU (SRR L41) — PK is in the middle there, which canon itself states and limits ("not a universal linear morph", SRR L43). No contradiction.

---

## 9. Collision checks — large races (SK–GR–GO)

### 9.1 Comparative canon

- GO L13–17: "Skarn | **Large-scale powerful human architecture** … / Grask | **Rangy reach-oriented non-human architecture** … / Gorrund | **Massive load-bearing non-human architecture** …"
- LRR L57: "Pelvis | "more substantial" (S L77) | Distinct, non-human; morphology OPEN (GR L45, L208) | Load-bearing, integrated with the axial body; OPEN (GO L49, L187, L711) | Architectural difference only; morphology OPEN for Grask and Gorrund"
- LRR L73–77: "**Skarn–Gorrund:** **no proportional ordering exists** apart from axial depth and breadth at equal height. Canon separates them by **architecture**: - human skeletal family vs non-human ALPC; … - and by degree of depth and structural scale."
- LRR L71: "**Grask–Gorrund:** fully ordered and opposite on every proportional axis canon names."
- SK L23: "- a more substantial neck base and pelvis"; SK L75: "- a slightly larger torso share of total height and greater torso depth"; SK L77: "- a thicker neck base and a more substantial pelvis"; SK L94: "The pelvis, hips, thighs, knees, calves, ankles and feet plausibly carry the greater mass at every setting. There is no default "huge upper body, tiny legs" silhouette."; SK L114: "- Pelvis width sets upper-leg alignment."
- RAC-03 L26: Skarn "Stays OPEN | Which pelvic dimension "more substantial" means (breadth, depth, height)".
- GR L716; GO L238, L239, L244 (quoted in §5.1, §6.1). GO L244: "Lower-breadth / lower-depth Gorrund (GOR-BODY-12, GOR-BODY-14) vs Broad Grask at matched height … The Gorrund stays Gorrund through body architecture: lower relative limb contribution than the Grask distribution, greater axial contribution, joint presence and Axial Load-Path Continuity."
- UCCA L131: "Broad Skarn ≠ Gorrund; Broad Grask ≠ Skarn/Gorrund; Narrow Gorrund keeps ALPC".

Note: the **SK reference (accepted W1 ARM, order §2)** carries the generator human pelvis with `hip-scale-depth-incr 0.10, hip-scale-horiz-incr 0.15` (ARM-SK L34). For Skarn this is canon-compliant (human family, "more substantial"), and it fixes the SK comparator as **a human pelvis enlarged in breadth and depth**.

### 9.2 Pairwise checks

| Pair | Proposals compared | Separate? | Contradiction? | Residual risk |
|---|---|---|---|---|
| **SK–GO** | SK: human pelvis, "more substantial" (depth and breadth both enlarged, human ratios). GO: depth-led (AP ÷ breadth > SK, GO-P4), hip-joint scale ÷ breadth > SK (GO-P2a), breadth bounded by lower trunk (GO-P3), robust sacral link (GO-P1). | **Yes, architecturally** — the only kind of separation LRR L73 allows. No proportional (torso-share/pelvic-vertical) direction vs SK is proposed (AD-4 respected, GO L757). | None. Matches GO L239 "distinct joint, torso and pelvis relationships. Fails as "extra-broad Skarn"". | **High if PV-D14 is rejected**: without GO-P4/GO-P2a the GO pelvis is "SK pelvis, more so" = "uniformly enlarged human pelvis" (GO L49). Also open: SK's "more substantial" is undetermined (RAC-03 L26); if the author later reads it as "deeper", GO-P4 must still exceed it **relative to breadth**, not absolutely. |
| **SK–GR** | SK: human, substantial, torso-share > MF. GR: torso-proportioned pelvis (≤ MF relative to stature), long-lever hip apparatus (GR-P2b), legs > SK. | **Yes**: opposite on pelvic size relative to stature (SK ≥ MF; GR ≤ MF) and on hip-apparatus-to-pelvis relation. | None. Matches LRR L72 ("Grask is limb-dominant and less broad; Skarn is torso-dominant and broad"), GR L716 (non-human pelvic organization as a carrier vs SK at GR-BODY-10). | **Medium at GR-BODY-10** (shortest-limbed Grask vs SK, AD-2): limb share converges, so the pelvic carrier must be GR-P2b (hip apparatus large relative to a torso-proportioned pelvis). If PV-D1/PV-D12 is "relational only", that carrier is a ratio, measurable by joint breadth ÷ crest breadth. |
| **GR–GO** | GR: pelvis ≤ MF relative to stature, AP depth ≤ MF, hip apparatus large relative to pelvis. GO: depth-led, breadth bounded by trunk, hip-joint scale large relative to breadth, vertical ≥ GR. | **Partly.** Opposite on AP depth (GR ≤ MF; GO depth ÷ breadth > MF), vertical contribution, construction. **Shared:** both proposals make hip-joint scale large relative to pelvic breadth (GR-P2b, GO-P2a). | None. GO L238 "pelvis-torso integration" (GO) vs GR L208 "coordinate long lower limbs" (GR) are different functional anchors. | **Medium, flagged:** the "large hip apparatus relative to pelvis" feature appears in both. They differ in *why* (GR: long lever; GO: axial load) and in what surrounds it (GR shallow/torso-proportioned; GO deep/trunk-continuous), so the external RM-UB-06 set still separates them (AP depth ÷ crest breadth GO > GR). At the AD-3 corner (GOR-BODY-12/14 vs Broad GR, GO L244) separation rests on depth and ALPC continuity, consistent with canon. Author may prefer to drop GR-P2b's relative clause (PV-D12 option b) to remove the shared feature. |

### 9.3 Cross-group checks (brief)

- **DU–GO** (GO L739 "never breadth alone"; GO L241 "the same proportion recipe is never reused at a different scale"): DU squat (vertical ÷ breadth < MF), thorax-led, compact; GO vertically developed (≥ GR), depth-led, trunk-bounded breadth. Not a rescaled recipe. **Pass.**
- **SA** (closed): SA L145 "no Gorrund-like massive load-bearing pelvis; no Pipkin low-set compact-trunk specialization" — the GO and PK proposals keep exactly those two features; SA keeps its posterior/caudal organization (SA L154). **Pass.**

---

## 10. Elf triad check (FN–AE–VA)

### 10.1 Comparative canon

- ECR L32, L37 (quoted in §1.1): shared non-stock-human foundation (A); exact shapes E; "the three pelvises aren't claimed to be identical, with the pattern being a shared foundation that diverges by population."
- ECR L281: "Pelvis | Shared non-stock-human foundation, exact morphology E | Prototype validation | Prototype validation | Prototype validation"
- ECR L49: "Fenn, a compact torso center with a relatively gradual transition within that compact system; Aelari, the greatest average vertical torso and waist continuity; Vael, a deeper torso with more compact torso-to-pelvis continuity."
- ECR L294: "**Related but distinct.** … never identical except for color or ears, three unrelated fantasy species, or human presets with pointed ears."
- VA L38: "Their own elven pelvis (not human, Fenn or Aelari)".
- AE L483: "Neither is a scaled version of the other".
- HV L506: "Shared elven pelvic anatomy, the sex-related anatomy system | Never invented inside Halvren." (dependency).

### 10.2 Proposed shared elven pelvic foundation (A) — PROPOSAL

| Shared item | Derivation |
|---|---|
| E-A1: Construction gracile relative to MF at matched stature (ordering FN > AE > VA in gracility) | ECR L21; ECR gracility ordering |
| E-A2: Hip apparatus serving relatively long femora: hip-joint height ÷ stature > MF; bitrochanteric ÷ crest breadth not lower than MF (hip base not reduced with gracility) | FN L111 "supporting longer femurs, stable hips"; AE L126 "Stable with long femurs"; VA L124 "stable with long legs" |
| E-A3: No breadth identity; all three frames; no mandatory hip width by race or sex | FN L111; AE L126; VA L38 |

### 10.3 Divergence (B/C/D) as proposed

| Descriptor | FN | AE | VA |
|---|---|---|---|
| Vertical proportion (vertical ÷ crest breadth) | human-homologous | **> MF and > FN** (AE-P3) | human-homologous |
| AP depth ÷ stature | ≈ MF (or < MF, PV-D3) | ≈ MF | **> FN and AE** (VA-P4) |
| Waist interval ÷ torso | gradual, < AE | **greatest** | **< AE**, continuous profile |
| Hip-joint scale | lightest | intermediate | greatest of the three |
| Lumbar curve | neutral | neutral | **natural lordosis** (VA-P1) |
| Leg share | > MF, ≥ AE (FN L52) | > MF | > MF, < FN and AE |

### 10.4 Checks

- **Identical?** No: each pair differs on at least two descriptors (FN–AE: vertical proportion, waist interval, gracility; AE–VA: vertical proportion, AP depth, waist, curve; FN–VA: AP depth, joint scale, curve, leg share). Satisfies VA L38 and ECR L37.
- **Manufactured?** Each divergence row cites a race line or ECR line; the only inferential steps are AE-P3 (pelvis inside the vertical elongation) and VA-P4 (pelvis inside the torso depth, VA L114 "torso-to-pelvis transition"). Both flagged for author decision (PV-D5, PV-D6).
- **FN–AE least separated:** FN-P5/AE-P5 share "no breadth direction"; FN-P4/AE-P4 both ≈ MF under option A. Separation rests on AE-P3 and the waist interval. **If PV-D5 is rejected, FN and AE pelves differ only in gracility and waist interval** — still "related, not identical" (AE L169), but thin. Flagged.
- **Elf vs human (SG/MF):** the shared items E-A1/E-A2 plus per-race divergence make a non-uniform, non-single-slider departure from MF. Whether that suffices for "non-human pelvis foundation" (ECR L59) is PV-D1.
- **Elf vs GR** (GR L267, L708): GR hip apparatus is large in absolute terms and torso-proportioned pelvis with robust-for-lever construction; elves are gracile (E-A1). Pass.
- **Halvren:** acceptance of §10.2 supplies the "shared elven pelvic anatomy" dependency (HV L506) for HV pelvic inheritance; the sex-related-anatomy dependency remains (PV-D18).

---

## 11. Summary table

| Population | Canon already implies | Genuinely OPEN | Proposal headline | Collision risk |
|---|---|---|---|---|
| **FN** | Not scaled human; gracile construction; serves greater leg share / longer femora with stable hips; differs in pelvis-to-leg relation; gradual waist within compact torso; breadth not identity | Breadth, AP depth, vertical vs MF; which hip descriptor differs; shape | Gracile, human-homologous plan; hip base not reduced with gracility (bitroch ÷ crest ≥ MF); gradual waist < AE; breadth/depth per PV-D3/PV-D4 | FN–AE: **medium** (thin if PV-D5 rejected) |
| **AE** | Not stock human + long legs; whole-body vertical elongation; greatest elven waist interval; gracile hips; no mandatory hip width | Whether pelvis itself is vertically proportioned; breadth/depth vs MF | Pelvis joins the vertical elongation (vertical ÷ breadth > MF, FN); longest waist; hip base ≥ MF | FN–AE medium; AE–VA low |
| **VA** | Must differ from human, FN, AE; torso-to-pelvis transition contributes to depth; compact waist vs AE; natural lumbar curve; more hip presence | Depth vs MF; lumbar-curve magnitude; breadth | Depth-continuous pelvis (> FN, AE); natural lordosis; short waist vs AE; most hip presence of elves | Low |
| **DU** | Broad foundation; not widened in isolation; strong torso-pelvis continuity; substantial hip joints; pelvis coordinates shorter legs; high structural presence | Pelvic AP depth; vertical : breadth; pelvis ÷ thorax | Broad + deep + robust + squat; wide hip base; thorax-led (crest ÷ thorax ≤ MF) | DU–PK: **high if PV-D9 rejected** (W1c shows convergence) |
| **GR** | Not scaled/narrowed; coordinates long legs, upright gait, Grask torso; no high crotch; non-human pelvic organization is a carrier | What "non-human organization" is; breadth/depth/vertical vs MF/SK | Pelvis proportioned to torso, hip apparatus to femora (decoupled); breadth ≤ MF as consequence, not narrowing | GR–GO medium (shared hip-apparatus clause); SK–GR medium at GR-BODY-10 |
| **GO** | Not uniformly enlarged / not independently widened; meaningful breadth, depth, hip-joint scale; ALPC continuity; Narrow keeps it | Depth : breadth; breadth vs lower trunk; sacrum | Depth-led, trunk-bounded breadth, large hip joints relative to breadth, robust sacral link | SK–GO: **high if PV-D14 rejected** |
| **PK** | Pelvis more prominent vs thorax than MF (vertical, depth, 3-D); breadth not identity; compact waist; light; mature; never DU; narrow-base gait | Depth details; pelvic vertical ÷ stature (T-2); breadth vs MF | Pelvis-led in 3-D relative to a moderate thorax; compact waist; convergent femora; light, mature | DU–PK high (as DU); PK–CG medium at 91–107 cm |
| *CG (context)* | Narrow core; mature; not dominant anchor; < DU mass; torso ≈ MF | All dimensions; inlet/outlet (D) | Human-homologous narrow-core default (not authored here) | PK–CG medium |

---

## 12. Explicit author decisions needed

Each is answerable yes/no or by choosing an option. "Recommended" marks the builder's preference only.

1. **PV-D1 — Meaning of "distinct / non-human / not a scaled human" pelvis (FN, AE, VA, GR, GO).** (a) Satisfied by a human-homologous bone plan whose descriptors P-1…P-6 are set separately from canon relationships (≥ two canon-motivated intra-pelvic ratios differ from MF, plus construction) — *recommended*; or (b) additionally require a race-specific morphological marker (e.g. iliac blade orientation, sacral proportion), which would be **builder-invented** and needs separate authorship per race.
2. **PV-D2 — Shared elven foundation (§10.2):** adopt E-A1 (gracile construction, ordering FN > AE > VA), E-A2 (hip apparatus for long femora: bitrochanteric ÷ crest not lower than MF) and E-A3 (no breadth identity) as the shared elven pelvic signal? Yes/no.
3. **PV-D3 — FN (and AE) pelvic AP depth:** (a) ≈ MF relative to stature — *recommended*; (b) modestly < MF following the shallower ribcage.
4. **PV-D4 — FN pelvic breadth relative to stature:** (a) ≈ MF, light build carried by construction — *recommended*; (b) modestly < MF.
5. **PV-D5 — AE pelvis participates in vertical elongation** (pelvic vertical ÷ crest breadth > MF and > FN)? Yes/no.
6. **PV-D6 — VA pelvic AP depth:** > FN and AE (yes/no); and vs MF: (a) ≈ MF — *recommended minimum*; (b) > MF.
7. **PV-D7 — VA "natural lumbar curve" magnitude:** (a) human-homologous natural lordosis, present (not neutralized) in the ARM — *recommended*; (b) greater than MF (then a lordosis landmark is added to measurement).
8. **PV-D8 — DU pelvic AP depth ÷ stature > MF**, continuous with the deep thorax? Yes/no.
9. **PV-D9 — DU thorax-led relation:** crest breadth ÷ thoracic breadth not above MF? Yes/no. (If no, state another DU–PK pelvic carrier; PK L194 says breadth is not the primary one.)
10. **PV-D10 — PK pelvic vertical contribution ÷ stature ≥ MF** as a direction only, magnitude left to T-2 / RM-SR-01? Yes/no. (Also: confirm or correct W1c-AUD row 106, which tested "> MF" as a canon direction.)
11. **PV-D11 — PK convergent-femur organization** (adult narrow-base under a broad pelvis) as a frame statement? Yes/no.
12. **PV-D12 — GR "non-human pelvic organization":** (a) pelvis proportioned to torso, hip apparatus proportioned to femora, including "hip apparatus large relative to pelvic breadth" — builder's draft; (b) the same without the relative clause (removes the feature shared with GO-P2a); (c) defer to PV-D1(b) marker.
13. **PV-D13 — GR and elves: no pelvic truncation below the hip joints** (leg share never gained by shortening the inferior pelvis)? Yes/no.
14. **PV-D14 — GO depth-led pelvis:** AP depth ÷ crest breadth > MF and > SK; hip-joint scale ÷ crest breadth ≥ MF and SK; crest breadth bounded by lower-trunk breadth? Yes/no (or accept a subset).
15. **PV-D15 — Add one external skeletal landmark interval to RM-UB-06:** costal margin (lowest rib) to iliac crest ("waist interval"), plus a lower-trunk breadth reading at the costal margin and a thoracic vertical length reading? Needed for FN-P6, AE-P6, VA-P6, PK-P3/P6, DU-P6, GO-P3. Yes/no. (Not obstetric; external skeletal only.)
16. **PV-D16 — RM-UB-06 reading layer:** read pelvic landmarks on skeletal/bony-landmark geometry, treating the W1c skin-surface readings (W1c-METH L85; soft tissue included; hip skinning shifts bitrochanteric up to −1.40 cm, W1c-METH L62) as composition-inclusive diagnostics only? Yes/no.
17. **PV-D17 — Construction (gracile/robust) verification:** accept visual orthographic check for pelvic robusticity, or define a proxy (e.g. crest thickness at a fixed landmark)? Choose: visual / proxy / defer.
18. **PV-D18 — Halvren:** confirm that accepting PV-D2 supplies the "shared elven pelvic anatomy" dependency (HV L506) while HV pelvic inheritance stays blocked on the sex-related system? Yes/no.
19. **PV-D19 — Sacral statements (GO-P1 robust sacral link; others human-homologous):** accept as frame-level statements not measured by RM-UB-06? Yes/no.
20. **PV-D20 — Sex/obstetric:** confirm no sex-related pelvic shift is authored for any of the seven populations in this packet (RA L52–53), and that no inlet/outlet geometry is implied by any proposal (RA L122)? Yes/no.
21. **PV-D21 — Build route after acceptance:** (a) sculpt each pelvis on the generator base by non-uniform regional deformation to the accepted directions, declared as builder-chosen (R-14); (b) purpose-built pelvic geometry per race; (c) (a) for DU/GR/GO/elves, (b) for PK inside the native short-adult base (order §5). Choose.
22. **PV-D22 — Canon edit scope after acceptance:** record accepted proposals as a "Pelvic architecture (author-accepted W1d)" row in each race spec's pelvis entry (FN L111, AE L126, VA L124, DU L108, GR L208, GO L189, PK L152), leaving "exact morphology/numbers OPEN"? Yes/no.

---

## 13. What this packet does not do

- No race spec, decision document or review is edited (order §7).
- No number is authored; W1c values appear only as builder-forced diagnostics (RA L88).
- No inlet/outlet, gestation or fertility geometry (RA L122).
- No sex-related pelvic shape (RA L52–53).
- No posture or curvature identity except Vael's authored lumbar curve (RA L124).
- No Skarn–Gorrund proportional direction (AD-4).

— Claude (draft for ChatGPT author acceptance)

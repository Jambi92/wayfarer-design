# Large-Race Comparative Anatomy Review — Skarn / Grask / Gorrund

**Author:** Claude (auditor). **Order:** `reviews/chatgpt-pass2-resolution-sequence-order.md` §5. **Required by:** `decisions/PROJECT_RULES.md` ("Reviews"). **Phase:** design only.

**Inputs:**
- Read in full: `specs/skarn/SKARN_V1.md` (cited **S Lnn**), `specs/grask/GRASK_V1.md` (**GR Lnn**), `specs/gorrund/GORRUND_V1.md` (**GO Lnn**) and the Marchfolk reference (**MF**).
- Line numbers are HEAD eb837b8. The evidence pack with every quote is kept in the session working notes.

**Scope rules from the order:**
- Clarify relationships; do not redesign.
- No invented numbers.
- Return explicit PASS/FAIL collision tests and narrowly scoped author decisions.

**Result:** **no genuine anatomical contradiction** among the three specs. **No redesign is needed.** Two coverage gaps need narrowly scoped author decisions (§5).

---

## 1. Stature overlap

| Band (cm) | Populations | Note |
|---|---|---|
| 183–198 | Skarn only, of the three (overlaps Marchfolk to 203) | — |
| 198–208 | Skarn, Grask | — |
| **208–229** | **all three** | Skarn reference (208) = Gorrund minimum; Gorrund reference (229) = Skarn maximum; Grask reference (218) sits mid-band |
| 229–239 | Grask, Gorrund | — |
| 239–251 | Gorrund only | — |

**Sources:** S L11–15; GR L15–19, L152–160; GO L27–31, L109–110.

Each spec states that height cannot carry identity:
- S L15, L285;
- GR L148 ("Height alone must never determine Grask racial readability");
- GO L31 ("height alone must never establish Gorrund identity").

## 2. Positive anatomical carriers, independent of absolute height

| Population | Named specialization | Size-independent carriers in canon |
|---|---|---|
| **Skarn** | Human-derived robust, powerful skeletal architecture: "large, robust humans" (S L291) on a human skeletal family | Relative to Marchfolk: larger torso share and greater torso depth (S L73–75); broader clavicles, wider and deeper ribcage, broader upper back (S L76); more substantial neck base and pelvis (S L77); larger joints, hands and feet (S L78–79); skeletal robustness (S L26). Face: human, with robust tendencies "not requirements" (S L147–154). **Biologically human** |
| **Grask** | Elongated skeletal leverage and reach (GR L23, L192) | Lower torso share than Marchfolk and Skarn (GR L37, L198); greater leg, arm and arm-span contribution relative to stature than Marchfolk and Skarn (GR L164, L213, L221–223); forearm and lower-leg emphasis (GR L215, L227); greater finger:palm ratio (GR L235); thoracic and shoulder breadth less relative to stature than Skarn (GR L42, L203); neck moderate-to-long relative to Skarn (GR L43); non-human scapula, clavicle and pelvis (GR L41, L45, L206); facial and midface verticality (GR L349, L358); folded late-taper ear (GR L443–457) |
| **Gorrund** | Massive load-bearing non-human architecture; **Axial Load-Path Continuity** (ALPC) (GO L17, L703–715) | ALPC from shoulder girdle → thorax → lower trunk → pelvis → proximal femur, surviving Narrow frame and low muscle (GO L713–714); thoracic depth "relative to stature and breadth" (GO L42, L178); greater torso share than Grask (GO L167); less limb and arm-span contribution than Grask (GO L194, L198); joint presence (GO L74–76); **Transverse Structural Continuity** face (GO L419–431); deep-bowl ear (GO L445–454); non-human status (GO L237) |

## 3. Dimension comparison and derived ordering

All entries are **population tendencies**, not individual guarantees.

Notation:
- "GO > GR" means Gorrund trends higher than Grask. Gorrund–Grask claims hold at matched height (GO L40, L167, L194).
- "n.d." means **not determinable from canon**. These are the cases where no chain of stated relations fixes an order.

| Dimension | Skarn vs Marchfolk | Grask | Gorrund | Derived three-way order |
|---|---|---|---|---|
| Torso share of stature | S > MF (S L75, L86) | GR < MF, GR < S (GR L37, L198) | GO > GR (GO L167) | MF, S > GR; GO > GR; **GO vs S n.d.; GO vs MF n.d.** |
| Thoracic / axial breadth (equal height or relative) | S > MF (S L76) | GR < S relative to stature (GR L203) | GO > GR (GO L40, L236); GO > S "axial breadth" (GO L109, Part 1 only) | **GO > S > GR** |
| Thoracic depth | S > MF (S L21, L75) | "meaningful", non-directional vs Skarn (GR L38–39) | GO > GR (GO L40); GO > S "greater axial depth" (GO L109, L237) | GO > S; GO > GR; **S vs GR n.d.** |
| Shoulder architecture | Broader clavicles and upper back (S L76) | Less broad relative to height than Skarn; non-human scapula and clavicle (GR L41–42, L206) | Substantial skeletal girdle, integrated into ALPC (GO L45, L709) | S > GR (breadth); GO vs S **n.d.** (difference is architectural: human vs ALPC) |
| Pelvis | "more substantial" (S L77) | Distinct, non-human; morphology OPEN (GR L45, L208) | Load-bearing, integrated with the axial body; OPEN (GO L49, L187, L711) | Architectural difference only; morphology OPEN for Grask and Gorrund |
| Arm / span contribution | n.s. | GR > MF, S (GR L164, L223) | GR > GO (GO L198); "not a defining trait" (GO L273) | GR highest; **GO vs S n.d.** |
| Leg contribution | n.s. ("long-legged Skarn possible", S L86) | GR > MF, S (GR L213) | GO < GR (GO L194) | GR highest; **GO vs S n.d.** |
| Forearm / lower-leg emphasis | n.s. | GR > MF, S (GR L215, L227) | "never copying Grask" (GO L62, L67, L200) | GR highest; **GO vs S n.d.** |
| Joint scale | S > MF (S L24, L78) | "substantial in absolute terms … relatively lean" (GR L31, L217) | GO > GR (GO L222, L236) | GO > GR; **S vs GO n.d.** ("distinct … relationships", GO L237); S vs GR n.d. |
| Hands / feet | Larger than MF (S L79) | Large; greater finger:palm (GR L233–235, L243) | Very large, palm breadth and depth (GO L204–214) | Finger:palm GR > S, MF; GO **n.d.** |
| Skeletal structural presence | Robust (S L26) | Leverage, not compact mass (GR L23, L31) | "Massive" = skeletal structural scale (GO L19, L76) | Qualitative: GO and S high, GR rangy. GO vs S is a difference of degree and architecture |
| Neck | "more substantial neck base" (S L77) | Moderate-to-long relative to Skarn (GR L43) | Moderate, highly integrated (GO L46) | GR > S (relative length); GO **n.d.** |
| Head / neck, head scale | Skull "suited to body size" (S L147) | No head-to-height ratio locked (GR L429) | Ratio OPEN; "tiny-head giant" fails (GO L295, L401–403) | All **n.d.**; measurement queued |
| Posture | n.s. as anatomy | Upright; no hunch (GR L44, L90) | Upright; no hunch (GO L48, L189) | All upright; posture never carries identity (GR L716; GO L155) |
| Face | Human; robust tendencies; ranges never delivered (S L48) | Vertical organization, long midface (GR L340–358) | Transverse continuity, breadth and depth (GO L289, L320) | GR vertical vs GO transverse (GO L327, L399); Skarn human |
| Ears | Human auricle (by family; S is silent) | Folded, late taper | Deep bowl, broad rim | Three distinct families |

**Summary by pair:**
- **Grask–Gorrund:** fully ordered and opposite on every proportional axis canon names. This is the large-race triangle working as designed (GO L13–17).
- **Skarn–Grask:** mostly ordered. Grask is limb-dominant and less broad; Skarn is torso-dominant and broad. Thoracic depth and joints are n.d.
- **Skarn–Gorrund:** **no proportional ordering exists** apart from axial depth and breadth at equal height. Canon separates them by **architecture**:
  - human skeletal family vs non-human ALPC;
  - human face vs Transverse Structural Continuity;
  - human auricle vs deep-bowl ear;
  - and by degree of depth and structural scale.

This is a deliberate choice in the Gorrund Final Clarification (FC L701–731), not a contradiction.

## 4. Collision tests

**Statuses:**
- **PASS:** canon states size-independent carriers *and* an explicit test or requirement.
- **PASS (carriers; test absent):** carriers exist but no canonical test pairs the cases.
- **UNDETERMINED:** canon does not guarantee separation.
- **FAIL:** a canonical requirement cannot be met. None found.

| ID | Test | Status | Basis |
|---|---|---|---|
| LR-01 | Gorrund vs Skarn at equal height, 208–229 cm, composition matched | **PASS** | ALPC, thoracic depth, axial breadth, TSC face, ears, non-human status (GO L109, L237, L328, L398, L703–731). Fails "if Gorrund need more muscle to be distinguished" (GO L671) |
| LR-02 | Low-end Gorrund (208 cm, Broad) vs Broad Skarn (208 cm) | **PASS** | GRR-BODY-02 "Fails if it becomes Skarn" (GO L150); "about 208 cm with a Broad frame stays Gorrund without becoming Skarn" (GO L222); GRR-STRESS-04 (GO L246); Skarn side S L32, L293 |
| LR-03 | Low-end Gorrund (208 cm) vs a **taller** Broad Skarn (up to 229 cm) | **PASS (carriers; test absent)** | Every Skarn–Gorrund test is equal-height only. The applicable carriers are ratios or architecture (thoracic depth relative to stature and breadth, ALPC, face, ears), so absolute size cannot rescue the Skarn. No canonical test exists → **AD-1** |
| LR-04 | Narrow / low-breadth Gorrund (GRR-BODY-12) vs Broad Skarn at equal height | **PASS (carriers; test absent)** | Breadth can invert here. Canon then relies on "depth, joints, axial integration and overall skeletal scale" (GO L177) and on ALPC surviving Narrow (GO L713). Numeric validator queued (RM-LR-03) |
| LR-05 | Grask vs Skarn at equal height (198–229 cm) | **PASS** | GR L104, L265, L701 (fails "if skin or ears alone separate them"); high-muscle Grask "Fails if it becomes Skarn with longer arms" (GR L100) |
| LR-06 | Short-limbed valid Grask (GR-BODY-10) vs Skarn | **PASS (carriers; test absent)** | Non-limb carriers: thoracic and shoulder breadth relative to stature (GR L42, L203, "surviving composition neutralization"); non-human girdle and pelvis; neck; finger:palm; facial verticality (GR L349, L358); ear. No GR-BODY-10 × Skarn test → **AD-2** |
| LR-07 | **Short-limbed valid Grask (GR-BODY-10) vs Gorrund, especially Gorrund's "slightly more limb-present" proportion family (GO L230)** | **UNDETERMINED** | Gorrund's distinction from Grask rests mainly on limb contribution (GO L57, L194, L198, L236), which is exactly the axis GR-BODY-10 weakens. The GR-BODY-10 floor is "enough limb contribution to read Grask" with no reference (GR L259). Remaining carriers (thoracic breadth and depth, joints, ALPC, face, ears) are population tendencies. No test pairs GR-BODY-10 or Broad Grask with Gorrund, or GRR-BODY-12/14 with Grask → **AD-3** |
| LR-08 | Grask vs Gorrund central tendencies at equal height (208–239 cm) | **PASS** | Fully ordered (§3); GO L110, L236, L672 ("fails if it becomes 'thin vs muscular'") |
| LR-09 | Narrow Gorrund (GRR-BODY-04) vs Grask at matched height; Narrow Gorrund at 251 cm vs a tall Grask | **PASS** | GO L148, L222 |
| LR-10 | Composition inversion (muscular Skarn vs low-muscle Gorrund; low-muscle Grask vs muscular Skarn; high-fat Grask vs lean Gorrund) | **PASS** | GO L109, L236, L671; GR L100, L259 ("never read as a skeletal difference"); GR L251 |
| LR-11 | Face only: Gorrund vs Skarn, Grask vs Skarn, Gorrund vs Grask | **PASS** | GO L398 (fails if it needs tusks, a huge brow or fantasy skin); GR L424; GO L399 (fails if reduced to vertical-vs-horizontal sliders). Skarn's own craniofacial ranges were never delivered (S L48) — informational |
| LR-12 | Proportional (torso / limb) separation of Skarn and Gorrund independent of architecture | **UNDETERMINED by design** | Canon states no Gorrund torso or limb relation to Skarn or Marchfolk; "not a defining trait" (GO L273) ≠ "human-equal". Identity is assigned to architecture (FC). → **AD-4** (confirm by-design status) |

## 5. Narrowly scoped author decisions

None of these redesigns a race. Each closes a coverage gap with a test or a directional relationship.

**AD-1. Add a Skarn–Gorrund Cross-Population Boundary Test**
- At the 208 cm Gorrund minimum, against Broad Skarn at **equal and greater** height (to 229 cm).
- It passes on ratio and architecture carriers only (thoracic depth relative to stature and breadth, ALPC, face, ears), never on absolute size or muscle.
- This mirrors the boundary tests Gorrund already labels for Aelari, Fenn and Sagekin (GO L262–264).
- **Recommendation:** adopt.

**AD-2. Add a GR-BODY-10 × Skarn test**
- The short-limbed Grask must remain distinct from Skarn by its non-limb carriers (GR L42, L203; face; ear).
- **Recommendation:** adopt.

**AD-3. Resolve the GR-BODY-10 vs Gorrund gap.** Two options; no numbers are proposed.
- **(a) Directional floor (recommended).** Interpret GR-BODY-10's "enough limb contribution to read Grask" relative to the **Gorrund distribution at matched height**: the shortest-limbed valid Grask still trends above Gorrund's limb-present proportion family. Add a GR-BODY-10 × Gorrund ("slightly more limb-present" family) test, and a GRR-BODY-12/14 × Broad Grask test.
- **(b) Architectural separation only.** Accept that at this corner separation rests on thoracic breadth and depth, joints, ALPC, face and ears. Add the same two tests on that basis.
- Either way, the numeric floor comes from reference meshes (RM-LR-04).

**AD-4. Confirm Skarn–Gorrund proportional separation is "undetermined by design"**
- Confirm that Skarn–Gorrund proportional separation is **undetermined by design**: identity is architectural (FC L701–731), and Gorrund torso and limb shares relative to Marchfolk and Skarn stay unconstrained.
- The alternative would be adding a directional torso or limb relation to Skarn. That would be new Gorrund canon, which this review does not recommend.

**AD-5 (conforming, optional). Give the Skarn spec a Grask pointer for symmetry**
- Add one line: Skarn–Grask separation is carried by Grask P1 §60–70 and P5 tests.
- The Skarn spec currently never mentions Grask (zero occurrences). It needs no anatomy change.

## 6. Contradiction check

Eleven candidate conflicts were tested. **None is genuine.** The notable ones:

| Candidate | Verdict |
|---|---|
| Grask "currently tallest" 239 cm (GR L178, L671) vs Gorrund 251 cm | Time-bounded by Grask itself ("Gorrund may exceed it"). Stale wording; conforming edits E7-21/22 |
| Grask placeholder clause (GR L316) vs Gorrund "greater breadth and depth than Grask" (GO L40, L236) | GR L316 disclaims that *Grask's wording* sets Gorrund properties; it does not deny them |
| Skarn "more natural muscle volume" (S L26, L80) vs Gorrund reading it as approved "muscle-volume potential" (GO L237) | An interpretive dependency on ambiguous Skarn text. Resolved by the adopted Muscular Development Capacity term; conforming edits E1-01/02/05 |
| Shared Skarn and Gorrund scale carriers (hands, feet, joints, torso: S L40 vs GO L74, L208) | Same direction, a difference of degree. A **convergence risk**, not a contradiction. Covered by LR-01–04 and the architectural carriers |
| Breadth inversion (Broad Skarn vs Narrow Gorrund) | Population vs individual; covered by LR-04 |

## 7. Numeric validators deferred to reference meshes

Per order §5.6, these validators come from approved reference meshes. They are listed in the Reference-Mesh Measurement Queue (`claude-pass2-r5-reference-mesh-queue.md`) as RM-LR-01 to RM-LR-06:
- torso share;
- leg, arm and span share;
- thoracic depth/stature and depth/breadth;
- joint-to-long-bone scale;
- the GR-BODY-10 limb floor relative to Gorrund;
- the ALPC proxy measurements.

**AD-3 measurement closure (October 8, 2026; `reviews/chatgpt-rac-w2d-gorrund-final-acceptance-w2e-sagekin-order.md`):** RAC W2D measured the floor at real overlap — the limb-present Gorrund family stays below GR-BODY-10 in leg, arm and span share while keeping greater torso contribution (`reviews/claude-rac-w2d-gorrund-boundary-gate.md` §8). AD-3 / LR-07 / RM-LR-04 CLOSED; Grask 198 vs Gorrund NOT APPLICABLE.

**Review status:** performed. No contradiction, no redesign. **Accepted October 5, 2026:** AD-1, AD-2, AD-4 and AD-5 approved; AD-3 option (a) approved (`reviews/chatgpt-pass2-author-closure-canonicalization-order.md`). All five are reconciled into the specs.

— Claude

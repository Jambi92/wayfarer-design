# Reference Anatomy Method v1

**Status:** **CANONICAL: RAC Phase 2** (October 5, 2026; `reviews/chatgpt-reference-anatomy-closure-phase2-order.md`). Biological authorship canonicalized; **measurement not started**.
**Phase:** DESIGN AND MEASUREMENT METHOD ONLY. This document defines what an approved reference mesh is and how reference anatomy is measured. It does not choose mesh topology, skeleton family, rig, morphs, engine, file format or runtime use (§12).
**Sources:**
- Phase 1 package: `reviews/claude-rac-01…12`
- Evidence: `reviews/rac-evidence/`
- Author resolutions: AD-R1…AD-R46 (`reviews/chatgpt-reference-anatomy-closure-phase2-order.md`)

## 1. Purpose and authority

This is the single method document for **reference anatomy**: the approved meshes from which the Reference-Mesh Measurement Queue (`reviews/claude-pass2-r5-reference-mesh-queue.md`, "RMQ") derives numbers.

**Authority:**
- Authority level 2, as a companion to PROJECT_RULES alongside UFCA and UCCA.
- It governs **method**: what counts as an approved reference mesh (ARM), its state, its acceptance and how values derived from it gain authority.
- Race specs (level 1) keep governing each population's anatomy. Race-specific clarifications accepted in RAC Phase 2 live in the race specs; this document only points to them.
- **Nothing here sets a numeric anatomical envelope.** No value becomes canon because a mesh embodies it (§7).

## 2. Approved Reference Mesh (ARM)

An **ARM** is a mesh of **one adult individual** of one population, in the state defined in §3, that has passed the acceptance test (§6) **and been accepted by the author**.

- Measurements taken from an ARM are **diagnostic envelopes first** (§8).
- **Variants** (§5) are measured but are not ARMs.
- One ARM exists per **sex-related configuration** the race validates (§4).

## 3. ARM state

| # | Requirement | Content |
|---|---|---|
| R-1 | **Central-tendency adult anatomy** | The population's central tendencies as stated in its spec. Every positive tendency is present; every prohibition is absent. Adult read; Apparent Biological Age at a mid-adult value |
| R-2 | **Stature** | The race **reference height**: MF 173, SK 208, SG 178, FN 181, AE 190, VA 178, HV 178, DU 137, GR 218, GO 229, PK 107, CG 91, SA 188 cm (race height tables). Reached by proportion, **never by uniform scaling** from another population or stature |
| R-3 | **Skeletal Frame reference state** | The population's **central skeletal values** for every frame variable. Recorded as central values, **not** as a "Balanced" state: Balanced is not the default body and frame has no persistent state (UCCA §7) |
| R-4 | **Reference composition** | **Current Muscularity and Body-Fat Amount at the population centre, neutral (untilted) fat distribution, no regional muscle offsets.** Saurin: fat placed by the canonical depot ordering (SAURIN §258). This defines the "moderate composition" and "reference composition" wording in race specs. **Reference composition is a measurement state, never a body preset, composition starting operation or creator default** |
| R-5 | **Natural asymmetry** | Zero; bilaterally symmetric |
| R-6 | **Measurement stance** | Upright anatomical standing: head in neutral carriage; arms hanging with a small fixed abduction, palms toward the thighs; feet at hip width, parallel, full plantigrade contact; hips and knees extended without lock or crouch; spine in neutral adult curvature. **Saurin:** the frozen reference stance, tail at reference carriage with no ground contact. The stance is a **measurement convention**, not Anatomical Resting Alignment and not an idle |
| R-7 | **Neutralization** | Body at UCCA **N3**: no clothing (or a neutral fitted proxy that never covers a measured landmark), no jewellery, no Applied markings, no Body Language preset, no equipment. **N-Head** only where a body test requires it. Equipment never validates a body |
| R-8 | **Hair** | No scalp hair over measured landmarks (removed, or a zero-thickness cap); no facial hair; no body hair. Saurin: cranial display at the frozen reference state, excluded from head-length measurement |
| R-9 | **Surface** | One neutral, matte, uniform material. No Environmental, Applied or Acquired layer. No normal or displacement detail that changes the measured silhouette. **Structural anatomy lives in geometry** (§10 rule R-SKIN-1) |
| R-10 | **Sex-related configuration** | Per §4 |
| R-11 | **Mandatory race anatomy** | Present at reference: Saurin tail (measured from the caudal-base landmark, the posterior-pelvic-plane axis point; SAURIN §265 list), E/B at the configuration's centre, claws, scale-field topology; each race's ear family at its centre (UFCA §10.2) |
| R-12 | **No contamination** | No culture, class, occupation, equipment, weathering, scars, grime, posture-coded personality or stereotype bundle |
| R-13 | **Scale and units** | Real-world metres; ground plane at the sole; vertical up axis; stature to the skull vertex, excluding hair and keratin display. Saurin stature excludes the tail |
| R-14 | **Provenance record** | Source; build method; every input value; and every value **chosen by a builder** rather than taken from canon (§7) |

## 4. Sex-related configurations (R-SEX)

| Population(s) | Configurations available for ARMs | Basis |
|---|---|---|
| **Marchfolk, Skarn, Sagekin** | Both, using **ordinary human sex-related anatomy**, no race-specific shift unless separately authored | AD-R20, AD-R22 |
| **Fenn, Aelari, Vael** | **One configuration** for now. Detailed external sex-related biology is **deferred**; human or humanoid soft tissue is **not** imported by assumption. Independence rules stand | AD-R21 |
| **Durrim, Grask, Gorrund, Pipkin, Cogling** | **One configuration** for the Wave 1 bootstrap. Skeleton and composition carry **no authored sex shift** (R-SEX "no shift" is complete). Second-configuration external biology needs **per-race authorship**; human patterns are **never transferred**. Like-for-like and second-configuration tests wait (e.g. PIP-BODY-29; the Cogling reference-preset rule) | AD-R18, AD-R19, AD-R22 |
| **Halvren** | Follows source and development rules; no internal rule is invented | AD-R22 |
| **Saurin** | Male centre and female centre exactly per SAURIN §263; no mammalian anatomy | AD-R22 |

Skeletal measurement is unaffected by these limits: under "no shift", a second configuration would share every skeletal and composition value.

## 5. Variants

| Variant | Definition | Purpose |
|---|---|---|
| Frame | ARM with frame variables written to the race's Narrow / Broad starting values | RM-LR-02, RM-UB-03 |
| Stature | Race minimum and maximum, by proportion and allometry, **never by scaling the ARM** | RM-UB-02; boundary tests |
| Composition | Low / high muscularity and fat on the central skeleton | Identity-under-composition tests |
| Named extreme | A race's named validation case (e.g. GR-BODY-10, GOR-BODY-12/14, PIP-BODY-02, COG-BODY-11) | AD-1/2/3, anti-juvenile and boundary items |
| Diagnostic face | A named craniofacial case: MF-FACE-PROJ-MAX, GR-FACE-14, GOR-FACE-05 | RM-CF-02/03/04 |

A variant that FAILs its race's tests is corrected. **The population distribution is never weakened to fit a variant.**

## 6. Candidate acceptance test

A candidate (new build or existing asset) becomes an ARM only if:
1. R-1…R-14 hold, verified on orthographic front, side and 3/4 renders with a common ground line and grid;
2. every permanent race test applicable to a central body passes (UCCA §24 tiers A, E, I at least), including N3 neutralization;
3. pairwise boundary tests involving the central body pass, at shared stature or matched scale (tier B);
4. every builder-chosen value is declared (R-14) and accepted explicitly (§7);
5. the author accepts it, recorded in the RMQ and the race spec's status line.

**Existing assets are not ARMs by existing.** Hyper3D/Rodin GLBs, Iteration 3 MPFB references and the Saurin closure reference must each pass this test.

## 7. Provenance and circularity rule

A mesh built from **numeric targets chosen by a builder** (a solver, a sculptor or an AI) returns those targets when measured. Measuring it **cannot discover** canon; it can only confirm the builder's choices.

- Where an ARM embodies builder-chosen values, its acceptance is an **authorship decision about those values**, recorded as such.
- Envelopes derived from it are labelled "derived from builder-chosen reference values accepted on <date>".
- **No measured value becomes canon merely because a candidate mesh embodies it.**

**Current candidates (AD-R46):**

| Candidate | Status |
|---|---|
| Iteration 3 **Marchfolk** references | **Starting human-baseline candidate only.** MPFB's generic adult human at 173 cm with no race multipliers. Must be re-posed to R-6, normalized to R-1…R-14 and pass §6 before acceptance |
| Other Iteration 3 references | **Not measurement truth** (solver-built to builder-chosen multipliers; uniform-scaled to height; reference height only) |
| Other populations | **Purpose-built ARM candidates** from canonical anatomy |
| Saurin closure reference aff1b52 | Strongest **male-centre** candidate; its **female-centre** configuration (§263 centres; the reference accounting's female-centre column) is the second candidate. The validated +10 % "reference female" is a valid individual above the female centre, not the centre (SAURIN §263). Both still need the §6 record |
| **Saurin W2 reference (canonical, RAC W2I6, October 9, 2026)** | **Canonical Saurin ARM:** the accepted W2I4 candidate promoted unchanged — SA-M `saurin_w2_final_base.npz` `f86ae800…` (+ `saurin_w2_final_surface_delta.npz` `f32286c4…`, seeds `saurin_w2_seeds.npy` `a1d07b8d…`); SA-F = §263 female centre on it (`saurin_w2_SA-F188_realization.npz` `8019420a…`). aff1b52 and the historical SA-F remain W1 / W2I provenance. Deferred production art-pass item: medial / posterior thigh relief (non-biological). |
| Hyper3D/Rodin GLBs | Not canon by existing. The only ones found (Vael source masters) are relief reconstructions of 2D sheets and cannot be measured (RAC-12 §5) |

## 8. Derived values are diagnostic first

1. Derive envelopes only from accepted ARMs and validated variants; never back-fit to a prototype (RMQ rule 1).
2. A boundary needs valid maxima and minima; **central values alone never establish a boundary** (RMQ rule 2).
3. A clamp exposed by measurement is creator behaviour (CONSTRAIN), not a reason to weaken a distribution (RMQ rule 3).
4. Every derived value is recorded as a **diagnostic envelope** and becomes canon **only by author acceptance** (RMQ rule 4; the Saurin Part 7 model).
5. Directional canon (e.g. "Grask arm span > Marchfolk") is a **constraint the measurement must satisfy**, never permission to invent a magnitude.

## 9. Measurement waves

| Wave | Content | Gate |
|---|---|---|
| **W0** | Author method and authorship decisions | Done: RAC Phase 2 |
| **W1** | Central bootstrap: one ARM per population (one configuration), plus the second configuration for Marchfolk and Saurin; the Marchfolk head variant MF-FACE-PROJ-MAX. Skarn and Sagekin second configurations are available but not required in W1. **Marchfolk baseline (RM-UB-07) first.** RM-CF-01 can run at once (no biological dependency). Manifest: `reviews/claude-rac-wave1-execution-manifest.md` | ARM acceptance per §6 |
| **W2** | Boundaries: frame, stature and composition variants; named extremes; diagnostic faces GR-FACE-14 and GOR-FACE-05; ear-family envelopes | W1 accepted |
| **W3** | Dependent items: Halvren genealogy-conditioned references (RM-UB-05, RM-OT-03; W3A / W3A1 closure returned October 9, 2026, `reviews/claude-rac-w3a1-halvren-tail-final-closure-report.md`), Saurin rebuilt brow planes (RM-UF-03), scale fields (RM-UF-04, RM-UB-08), RM-CF-09; then the **RM-CF-05 FPI-margin author decision** | W2 accepted |
| **LB / LS** | Later biology; later systems (generator diversity RM-UF-05, world scale RM-OT-05, posture, equipment) | — |

## 10. Universal method rules adopted in RAC Phase 2

| Rule | Content | Source |
|---|---|---|
| **Obstetric firewall** | No pelvic inlet/outlet, birth-canal, gestation or fertility geometry is authored or measured for any race. Pelvic measurement uses external skeletal landmarks only | AD-R9 |
| **R-SKIN-1** | Structural anatomy lives in geometry. Skin texture, pores, roughness, oiliness and fine lines are surface detail. No skin-thickness difference is modelled geometrically unless a race authors one. Durability never has an effect | AD-R26 |
| **Spinal curvature** | Curvature is never a racial identity carrier, except Vael's "natural lumbar curve". ARMs use neutral adult curvature | AD-R7 (E-6) |
| **J-1 joint floor** | Joints are never implausibly tiny relative to the bones they connect, nor oversized as a cosmetic marker. A race's own minimum wording governs where stated | AD-R14 |
| **J-3 absolute vs relative joints** | Joint scale is read relative to the adjacent long bone **and** absolutely | AD-R14 |
| **J-4** | Bone robusticity never follows muscularity | AD-R14 |
| **J-5** | Thoracic depth and breadth are independent; narrow never implies shallow | AD-R14 |
| **Capacity default** | Where a race states no capacity tendency, capacity is a VAL ceiling with no population shift | AD-R17 |
| **Composition sex default** | Races that state no sex-related composition tendency have no authored sex shift in muscle, fat amount or fat distribution (current default; distributions OPEN where race canon says so). Saurin §263 tissue (E/B) is not composition | AD-R17 |
| **Arm span** | Span is always DER from shoulder and segment anatomy; Pipkin, Skarn and Cogling have **no racial span tendency**; Grask span > Marchfolk and Skarn and > Gorrund (direction only) | AD-R11, RAC-04 |

**Pelvic clarifications (RAC W1d, author-accepted October 5, 2026; `reviews/chatgpt-rac-w1d-author-decisions-continuation-order.md` §2):**
- **Distinct / non-human pelvis (PV-D1):** a human-homologous underlying bone plan satisfies a race's "distinct / non-human / not a scaled human" pelvis wording when the pelvic descriptors (spine–sacral relation, hip-joint organization, iliac structure, AP depth, transverse breadth, lower-trunk relation) are resolved independently from race canon with at least two canon-motivated relational departures plus construction. Decorative pelvic markers are never invented to make a population look different.
- **Validation layer (PV-D16):** pelvic canon is validated on skeletal / bony-landmark geometry. Skin-surface pelvic readings are composition-inclusive diagnostics only.
- **Sex and obstetric firewall (PV-D20):** no sex-related pelvic shift is authored by the RAC W1d pelvic architecture; the obstetric firewall above stays absolute.

Per-race architecture lives in each race spec ("Pelvic architecture (RAC W1d)"); exact morphology and numeric envelopes remain OPEN.

**Measurement standards adopted during RAC Wave 2** (author-accepted; method clarifications, not biology):
- **Exact-plane sections (S7):** the femoral subtrochanteric station S7 is read as the composition infimum on an exact plane section of the thigh faces, never on a vertex slab (a slab misses whole vertex rings where the mesh is stretched; the W1h trunk-station rule extended). Vertex-slab S7 values are historical / reproduction evidence only. Ruling: `reviews/chatgpt-rac-s7-skarn-final-acceptance-w2c-grask-order.md`; code `tools/rac/w1/s7_station.py`; record `reviews/claude-rac-s7-normalization-skarn-w2-final-gate.md`.
- **Joint breadths:** newly scored elbow, wrist, knee and ankle breadth decisions use an exact plane section through the anatomical joint centre, perpendicular to the limb axis (`tools/rac/w1/w2c1_drivers/joint_section.py`). The stature-scaled slab breadth is not an authority where a section is available: its error is body-dependent (knee 0.81–1.02 of the section; elbow ≈ 1.01–1.03, wrist ≈ 1.02–1.10, ankle ≈ 1.04–1.17). Existing accepted elbow / wrist / ankle conclusions stand unless a later phase depends on them or a named re-check applies (elf W1 wrist / ankle rows before elf W2). Slab-derived allometry slopes (e.g. the old 0.575 knee slope) are not authorities. Ruling: `reviews/chatgpt-rac-final-grask-w2-acceptance-gorrund-w2-order.md` §2; record `reviews/claude-rac-w2c1-grask-joint-normalization-gate.md`.
- **Boundary statures:** within the real overlap of two populations, stature-matched comparison is the primary boundary diagnostic. A W1 relation authored against a central / reference body is a reference-state validation relation, not an invariant clamp at every stature extreme when the comparator itself changes with stature; extrapolated comparator values beyond a comparator's valid range are report-only. Ruling: `reviews/chatgpt-rac-w2c1-grask-joint-normalization-order.md` §1.
- **Coupled elf vertical-share relations (RAC W2F ruling R1, October 8, 2026; `reviews/chatgpt-rac-w2f-elf-family-closure-order.md`):** E-A2 (elf hip-joint height above Marchfolk), VA-P2a (Vael leg share below Aelari and Fenn) and the Aelari longer-leg relation are **population / reference-state directional relations**, not mandatory ≥ 1 % separations at every identical matched stature. At matched height a difference below 1 % that keeps (or effectively equals) the intended direction is accepted when the complete anatomical package stays distinct. An isolated scalar overlap with Sagekin is not a racial failure (W2E complete-anatomy rule). Later audits, creator-envelope work and implementation must not re-read these rows as matched-height ≥ 1 % requirements.
- **Short-stature construction route (RAC W2F ruling R2):** the native short-adult route is used wherever the re-solved generator height macro falls below ~0.40 (not only below 159 cm). Construction / generator rule only; not biology.
- **Construction-route junction (RAC W2F final acceptance 1C, October 8, 2026; `reviews/chatgpt-rac-w2f-final-acceptance-w2g-halvren-order.md`):** native ↔ macro route junctions are generator / construction limits, not biological discontinuities. **Permanent implementation dependency:** a construction boundary must never produce a visible anatomical pop in the eventual continuous character-creator height control; creator-envelope / implementation work must use interpolation, blending, a unified solver or another continuity-preserving method (not solved in RAC W2).
- **Unavailable matched source endpoint (RAC W2G D1, October 8, 2026; `reviews/chatgpt-rac-w2g-final-acceptance-w2h-short-race-order.md` §1A):** when a mixed-ancestry population is tested at a valid stature outside one contributing source population's adult range, the nearest valid endpoint of that source (e.g. FN157 / VA157 for Halvren 152 cm) may be used as a source-family boundary diagnostic, labeled as an endpoint comparison and never as matched-height evidence. Source anatomy is never extrapolated beyond its valid range. Comparison method only, no biological magnitude.
- **Expression specification space (RAC W2G D2, October 8, 2026; §1B):** source-influenced mixed-ancestry expression is specified and validated in anatomical reading / relationship space (move toward the source tendency, stay inside mixed-development validity, do not overshoot the matched source where source and canon agree, never a copied source body, ancestry percentage or player-facing "50 % toward X" slider), not as a fraction of generator target values.
- **Reference-state tendency precedence (RAC W2G D3, October 8, 2026; §1C):** D2 governs when the matched source reading and the canonical / reference-state tendency agree; D3 takes precedence when matched-height allometry makes the source reading disagree with the accepted tendency (e.g. Aelari-influenced wrist gracility). Sub-1 % moves with the intended direction preserved, or with a canon relation that is effectively flat, are not failures; no percentage gaps are manufactured.
- **Real-height precedence for structural mass (RAC W2H D4, October 8, 2026; `reviews/chatgpt-rac-w2h1-durrim-pelvic-closure-order.md` §8):** where two populations share a valid adult stature, real-height comparisons govern structural-mass (robusticity / joint) claims; normalized cross-stature comparisons stay diagnostic and a normalized inversion does not override a clean real-height ordering. Named dependency: relative robusticity behaviour across each short-race creator envelope is resolved explicitly in creator-envelope work so no interpolation path creates an unintended structural inversion.
- **Same-state balance reference (RAC W2I D2(c), October 8, 2026; `reviews/chatgpt-rac-w2i1-saurin-closure-order.md` §3):** a relative balance / lean guard on an appendage or tail variant is judged primarily against the same-stature, same-frame / composition reference body carrying the reference appendage; a frozen reference at another stature or state is a secondary continuity diagnostic only. Interim guard values remain diagnostic until a density / posture model exists.
- **Measurement-only construction landmarks (RAC W2I D3, J-2, October 8, 2026; §4):** on a rig-less mesh, joint centres for measurement may be taken only from already-existing construction geometry of the accepted tool chain (recorded limb axes, builder frames), never fitted by eye or from a humanoid default skeleton; they deform nothing and require an invariance audit (mesh hash, stature, axial / tail / head / hand / foot readings, no pose edit, deterministic placement) before use. Joints that cannot be derived defensibly stay UNRESOLVED; segment values so obtained are reference construction values, not population canon. Surface sections of such a mesh are not skeletal-mass proxies unless a skeletal envelope exists.
- **Surface sections are not skeletal mass on rig-less meshes (RAC W2I D-D, October 8, 2026; `reviews/chatgpt-rac-w2i2-saurin-canon-restoration-order.md` §16):** external joint and S7 surface sections on Saurin cannot be scored as internal skeletal mass because the rig-less Saurin model lacks a separable internal skeletal envelope and includes substantial canonical caudofemoral tissue. Final Saurin-vs-Gorrund / Durrim skeletal-mass scoring requires a dedicated internal skeletal model; raw surface sections stay diagnostic.
- **Orthographic end-on projection is presentation context, not anatomy (RAC W2I3 SAU-SILHOUETTE ruling, October 8, 2026; `reviews/chatgpt-rac-w2i4-saurin-final-asset-order.md` §2-§3):** a dark or rounded read produced only by a strict dead-flat orthographic camera looking end-on along an accepted appendage (e.g. the Saurin free tail seen through the thigh gap) is not a biological defect once bounded anatomical levers have been exhausted. Such reads are judged with complete front / 3/4 / profile context, material definition, lighting and natural motion; they are recorded as presentation dependencies and never reopen accepted anatomy.
- **Reference-asset surface finish is not biology (RAC W2I5 ruling, October 9, 2026; `reviews/chatgpt-rac-w2i5-saurin-final-thigh-canonicalization-order.md` §2-§4, §14):** when an accepted proportion change stretches inherited surface relief, the relief may be re-sculpted locally to native anatomical scale (longer muscles over a longer bone, not a stretched pattern), with every measurement-bearing relationship held and re-verified; the frozen reference serves only as the native relief-scale reference, never as a body-form target. A lost procedural seed layout may be replaced by an author-accepted regenerated realization whose seeds are then saved as the reproducible reference.
- **Art debt does not block race-design closure (RAC W2I6 ruling, October 9, 2026; `reviews/chatgpt-rac-w2i6-saurin-canonicalize-w2i4-order.md` §1, §3):** once a reference asset's biology, measurements, scale-field logic and coupling are accepted, a remaining localized surface-relief defect is recorded as a DEFERRED PRODUCTION ART-PASS ITEM (non-biological, non-measurement-bearing, regression-tested when done) and the asset may be canonicalized; a rejected procedural asset experiment is kept as provenance and never promoted.

## 11. Consolidated directional constraints

Phase 1 consolidated the race-by-race directional constraints that every measurement must satisfy. They are adopted as **constraints, not magnitudes**:
- **Pelvic-axial requirement per race:** `reviews/claude-rac-03-pelvis-axial-closure.md` §2, "close now (directional)" column (AD-R6).
- **Segment, neck, head-share, hand and foot directions:** `reviews/claude-rac-04-segment-stature-closure.md` §2 and §5 (AD-R10). Pipkin T-2 constraints (§3; AD-R12); the split stays deferred.
- **Frame, joint and robusticity directions:** `reviews/claude-rac-05-frame-joint-robusticity.md` §2 (AD-R14). SK–GR and SK–GO orderings stay undetermined (AD-R15).
  - **AD-R15 scope (RAC W1d clarification, AD-G13, October 5, 2026):** AD-R15 covers only Skarn–Grask thoracic depth and Skarn–Gorrund / Skarn–Grask joint scale. Gorrund > Skarn thoracic depth remains canon and a pass condition (R2 L55; RAC-05 §2).
- **Ear landmarks (method):**
  - **superaurale**: the highest point of the auricle's free margin;
  - **subaurale**: the lowest point of the auricle (lobule where present);
  - **auricle tip**: the most distal point of the free margin from the attachment root, per ear family;
  - **auricle projection**: the perpendicular distance from the lateral skull surface at the attachment root to the most lateral point of the auricle.
  These are defined per ear family at the E layer; never a cross-family pointiness continuum (UFCA §10.2) (AD-R44).

Race-specific clarifications accepted in RAC Phase 2 are recorded in each race spec's **Reference-anatomy status** note.

## 12. Implementation firewall

This document does not decide or authorize: UE5 work; mesh topology; skeleton family; rigging; morph targets; animation, IK or retargeting; camera or first-person geometry; equipment fitting; save serialization; gameplay. ARMs are **reference and measurement assets**, not runtime assets. **Canonical status is not permission to begin measurement execution, mesh generation or UE5 implementation**; each needs its own order.

— Claude, canonicalized under `reviews/chatgpt-reference-anatomy-closure-phase2-order.md`

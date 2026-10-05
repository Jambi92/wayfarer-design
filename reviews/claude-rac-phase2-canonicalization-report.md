# RAC Phase 2 Canonicalization Report

**Author:** Claude
**Order:** `reviews/chatgpt-reference-anatomy-closure-phase2-order.md`
**Canonicalization commit:** `f514324`
**Recommendation:** **REFERENCE ANATOMY READY FOR MEASUREMENT** (§9).

## 1. Canonical method document

`decisions/REFERENCE_ANATOMY_V1.md`, at authority level 2 (PROJECT_RULES companion). It covers every §5 item:

| Order §5 item | Section |
|---|---|
| ARM definition and authority | §1–§2 |
| Reference composition | §3 R-4 |
| Measurement stance | §3 R-6 |
| Neutralization and surface | §3 R-7…R-9 |
| Sex-related configurations | §4 |
| Variants | §5 |
| Acceptance test | §6 |
| Provenance and circularity | §7 |
| Diagnostic-first rule | §8 |
| W0–W3 waves | §9 |
| Universal method rules | §10 |
| Consolidated constraints, ear landmarks | §11 |
| Implementation firewall | §12 |

## 2. Canonical files changed (commit f514324)

| File | Change |
|---|---|
| `decisions/REFERENCE_ANATOMY_V1.md` | **New** |
| `decisions/PROJECT_RULES.md` | New "Reference anatomy status" section (7 universal rules); authority line 2 names the companion; Reviews line |
| `decisions/UCCA_V1.md` | Three dated **pointer notes only**: §13 body-hair binding update, §22 Halvren authorship, §25 BIO OPEN list. The §13 rule ("bound only where canon supports it") and all substance are unchanged |
| `specs/<race>/<RACE>_V1.md` × 13 | One Reference-anatomy status note each, plus in-place clarifications (§4). Scripted by `tools/rac/apply_phase2.py` (assert-unique anchors) |
| `reviews/claude-pass2-r5-reference-mesh-queue.md` | RM-UB-06, -07, -08; Durrim added to RM-CF-10 and RM-SR-04; RM-CF-02/03/04 and RM-UF-02 prerequisites marked authored; RM-UB-05 authorship done; citation refresh (GO L232) |
| `reviews/claude-pass2-r3-craniofacial-framework.md` | Citation refresh: GR L362, GO L312, GO L301 |
| `reviews/claude-rac-wave1-execution-manifest.md` | **New** Wave 1 manifest |
| `specs/STATUS.md` | "REFERENCE ANATOMY: BIOLOGICAL AUTHORSHIP CANONICALIZED / MEASUREMENT PHASE READY", added **after** the regression audit |
| `tools/rac/apply_phase2.py` | New edit script |

**Not changed:** `decisions/UFCA_V1.md` (empty diff); every GLB and mesh; `register/`.

## 3. AD-R1…R46 disposition map

| AD-R | Disposition | Where |
|---|---|---|
| R1–R5 | ACCEPT (ARM definition, reference composition, stance, bootstrap, circularity) | REFERENCE_ANATOMY §2–§9 |
| R6 | ACCEPT (pelvic-axial consolidation as constraints) | REFERENCE_ANATOMY §11; race status notes |
| R7 | ACCEPT (editorial items) | DU wording (E-1); PK neck (E-3) and FN neck (E-4) in status notes; DU terminology (E-5); spinal-curvature rule (E-6) in §10 / PROJECT_RULES. E-2: no edit; Sagekin note records that Sagekin governs |
| R8 | ACCEPT | RMQ RM-UB-06, -07 |
| R9 | ACCEPT (obstetric firewall) | §10; PROJECT_RULES |
| R10 | ACCEPT (segment constraints) | §11 |
| R11 | ACCEPT (arm span) | §10; SK, PK, CG notes |
| R12 | ACCEPT (Pipkin T-2 constraints; split deferred) | §11; PK note |
| R13 | ACCEPT S-1 and S-3; **S-2 (Cogling head dimension) unanswered → OPEN question** | SA metric note; RMQ; CG note |
| R14, R15 | ACCEPT (J-1…J-6; SK–GR / SK–GO undetermined) | §10–§11 |
| R16, R17 | ACCEPT (capacity D; C-1…C-4) | §3 R-4; §10 (default limited to races that state no tendency) |
| R18, R19 | ACCEPT (no-shift defaults) | §4; DU/GR/GO/PK/CG notes |
| R20 | ACCEPT (MF/SK/SG ordinary human sex anatomy) | §4; notes |
| **R21** | **DEFER** (elven external sex biology OPEN) | §4; FN/AE/VA notes |
| **R22** | **X-2** as modified by the order | §4; all notes |
| **R23** | **ACCEPT** DU/GR/GO body-hair baseline | DU, GR, GO in place; GO approved-list line updated |
| **R24** | **ACCEPT** MF/SK/SG body hair | MF/SK/SG notes |
| Elven body hair | Hidden / deferred; facial-hair permission not extended | FN/AE/VA notes |
| R25 | Superseded by the order's elven body-hair ruling (same result) | — |
| R26 | ACCEPT (R-SKIN-1) | §3 R-9, §10; PROJECT_RULES |
| R27 | ACCEPT (PK L383 stale pointer fixed; MF/SK facial hair is biology) | PK in place; MF/SK notes |
| R28–R31, R33 | ACCEPT (H-1…H-4, H-6, under H-5) | HALVREN tail section |
| **R32** | **ACCEPT H-5** (outer bound 147–229 cm, not a final range) | HALVREN; UCCA §22 pointer; RMQ RM-UB-05 |
| **R34** | **Y-2** | HALVREN; UCCA §22 pointer |
| R35 | ACCEPT (caudal-base landmark) | SAURIN §265 list |
| R36 | ACCEPT (lower-trunk test; interim never-Gorrund rule) | SAURIN §265 list |
| R37 | ACCEPT (+15 % foot-claw coupling stated) | SA note |
| R38 | ACCEPT (RM-UB-08) | RMQ; SAURIN §265 list |
| R39 | **Not applied.** It was optional in Phase 1, and the order neither selects nor modifies it. Tail-equipment coverage extent stays OPEN (E) | Carry-forward §5 |
| R40 | ACCEPT (MF projection rule; MF-FACE-PROJ-MAX) | MF note; RMQ RM-CF-02 |
| **R41** | **ACCEPT; (b) = approximately Marchfolk**; GR-FACE-14 defined as a measurement case | GRASK Prognathism row |
| R42 | ACCEPT (comparator Marchfolk; GOR-FACE-05) | GORRUND after the projection paragraph |
| R43 | ACCEPT (ear variables) | GR, GO in place; RMQ RM-UF-02 |
| R44 | ACCEPT (ear landmarks, Fenn orbit reading, Durrim HSR scope) | §11; FN row; RMQ |
| R45 | ACCEPT (citation refresh) | RMQ, r3 |
| **R46** | **ACCEPT recommendation** (MF Iteration 3 as starting candidate only; others purpose-built; Saurin aff1b52 and female centre; GLBs not canon by existing) | §7; manifest |

## 4. In-place race-spec clarifications

| Race | Clarification |
|---|---|
| DU | L93 wording (E-1); body-hair baseline |
| GR | Prognathism row: central ≈ Marchfolk, not a carrier, vertical midface never prognathism, GR-FACE-14; ear-length reading; body-hair baseline |
| GO | Projection comparator + GOR-FACE-05; two ear variables; body-hair baseline (and the Part 3 approved-list line) |
| PK | L383 stale pointer |
| FN | Orbit row reading (ORB vs aperture) |
| HV | Stature-tail authorship H-1…H-6, H-5, Y-2 |
| SA | Head-metric note; §265 caudal landmark resolved; lower-trunk test and interim never-Gorrund rule; body scale fields queued |
| All 13 | Reference-anatomy status note (sex-configuration handling, body hair, arm span, neck and other race items as ruled) |

## 5. OPEN / deferred carry-forward register

Everything in order §6 stays OPEN, plus:

| Item | Status |
|---|---|
| Numeric segment, pelvic, joint, robusticity, head-share, ear, projection envelopes | OPEN (C) |
| GR/GO/PK/CG capacity distributions | OPEN (D) |
| Non-Saurin fat-distribution tendencies | OPEN (D) |
| Sex-dimorphism magnitude where unauthored; PK/CG direction | OPEN (D / B) |
| External sex-related biology: elves, DU, GR, GO, PK, CG | OPEN; second-configuration ARMs and like-for-like tests (PIP-BODY-29, Cogling multi-configuration preset rule) **wait** |
| Body-hair sex and population distributions (DU/GR/GO/MF/SK/SG) | OPEN (D) |
| Reproductive biology, lifecycle | OPEN (D) |
| Halvren pelvic inheritance; shared elven pelvis shapes | OPEN (D; B → C) |
| Skin thickness / durability | OPEN (D) / firewalled (E) |
| Saurin posture and density, claw ranges, world-space tail limits, acquired loss, thermoregulation, tail-equipment construction **and coverage extent (R39 not applied)** | OPEN (D / E) |
| Skarn–Gorrund torso/limb separation | Undetermined by design (AD-4) |
| SK–GR, SK–GO joint/depth orderings | OPEN until measured (C) |
| Tusk-like canines; ear mobility | OPEN (D / E) |
| RM-CF-05 FPI margin | Author decision after RM-CF-01…04 |
| Final Halvren tail cm limits and frequencies | OPEN (RM-UB-05) |
| **Cogling head-size dimension** (is "roughly 11–13 cm" height or length?) | **New OPEN question** (R13 S-2 unanswered) |

## 6. Regression audit (order §8)

An independent agent audited the uncommitted changes read-only. I verified its findings against the files, fixed them, and only then updated STATUS.

| # | Check | Result |
|---|---|---|
| 1 | 13 populations remain distinct | PASS: notes only; no identity text removed |
| 2 | No frozen Pass 2 decision weakened | PASS |
| 3 | UFCA, UCCA unchanged in substance | PASS: UFCA diff empty; UCCA has three pointer notes, consistent with its §13 rule |
| 4 | No numeric result invented | PASS: 147–229, reference statures, §263 values, +15 %, −10 %, d/w ≤ 1.00 all trace to canon |
| 5 | No diagnostic quantity became a control | PASS (§1, §12; RMQ rule) |
| 6 | No human sex anatomy leaked into a nonhuman race | PASS: "never transfers human patterns" in DU/GR/GO/PK/CG; elves deferred; Saurin §263 only |
| 7 | R-SEX intact | PASS (after fixes 1 and 9 below) |
| 8 | Halvren: no ancestry slider; 152–213 central, not hard | PASS |
| 9 | H-5 only an outer bound | PASS ("not the final Halvren minimum or maximum") |
| 10 | Grask vertical midface not converted to prognathism | PASS |
| 11 | Saurin tail, §256 / §258 / §263 intact | PASS (landmark ratification changes no number) |
| 12 | Body hair not a stereotype or gameplay trait | PASS ("never a racial identifier") |
| 13 | Reference composition not a body preset | PASS (R-4) |
| 14 | No canon by circular measurement | PASS (§7) |
| 15 | Every C/D/E item still deferred unless ruled | PASS after fixes (R39 disposition recorded; UCCA §25 pointer added) |
| 16 | No implementation decision | PASS (§12; manifest header) |

**Audit findings fixed (all verified first):**
1. The composition sex default read as all races; now limited to races that state no tendency. MF/SK/SG keep ordinary human anatomy.
2. The W1 wording implied 17 bodies; now matches the 15-body manifest.
3. The manifest's Gorrund neutralized-recognition citation was wrong: L685 corrected to L691.
4. **The Saurin second candidate was wrong.** The validated "+10 % reference female" is above the female centre (SA §263); the candidate is now the **female-centre configuration** (spec note, method doc and manifest).
5. The caudal-landmark citation pointed to a nonexistent "§256 note"; it now cites the §265 list.
6. A missed r3 citation (GO L297) was refreshed to L301.
7. The stale Gorrund approved-list line "body hair OPEN" now carries the authored baseline.
8. The UCCA §25 BIO OPEN list had no pointer; one was added.
9. The PROJECT_RULES human-anatomy line now says "directly only to MF/SK/SG (Halvren via its sources)".
10. Minor fixes:
    - the Grask row gained the omitted envelope clause and a GR-FACE-14 definition;
    - a Wave 1 planning sentence was removed from the Halvren spec;
    - Saurin's "no numeric envelope" now reads "no **new** numeric envelope";
    - R39 now has a disposition.

## 7. Wave 1 execution manifest

`reviews/claude-rac-wave1-execution-manifest.md`: **15 bodies + 1 Marchfolk head variant**.
- **Existing candidates:** Marchfolk ×2 (Iteration 3, starting candidates only) and Saurin ×2 (aff1b52 male centre; §263 female-centre configuration).
- **Purpose-built:** the other 11 populations and MF-FACE-PROJ-MAX.
- **Order of work:** RM-CF-01 first; then the Marchfolk baseline (RM-UB-07).

## 8. Commits

- `f514324`: canonicalization.
- This report: the next commit.

## 9. Recommendation

**REFERENCE ANATOMY READY FOR MEASUREMENT.** No blocking contradiction. Wave 1 can start whenever an order authorizes it. Known waits are **not** Wave 1 blockers:
- second-configuration ARMs for the elves and DU/GR/GO/PK/CG need per-race authorship;
- the Cogling head-dimension question.

Stopping here: no mesh generation, no measurement and no UE5 work.

— Claude

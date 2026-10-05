# UFCA Phase 2: Canonicalization Report

**Author:** Claude (auditor / reconciliation executor)
**Order:** `reviews/chatgpt-ufca-phase2-canonicalization-order.md` (6a70b2c)
**Phase:** design only. No UE5, rigging, morph, animation, camera, clothing or gameplay work was begun.

## 1. Canonical UFCA document

**`decisions/UFCA_V1.md`.** It sits at authority level 2 as the facial-creator companion to PROJECT_RULES:
- UFCA governs facial creator organization.
- Race specs keep governing anatomy.

All 20 required contents of order §5 are present:

| Order item | UFCA_V1 section |
|---|---|
| 1 Purpose and authority | §1 |
| 2 Slot/binding model | §2 |
| 3 16-slot hierarchy | §3 |
| 4 Bound / Bound-locked / Absent | §4 |
| 5 Taxonomy | §5 |
| 6 Dependencies and resolution order | §6 |
| 7 F-1 and G-1…G-5 | §7 |
| 8 Quick vs Detailed | §8 |
| 9 Simple Mode | §9 |
| 10 Binding and exception principles | §10 (including §10.3 coverage bindings and §10.4 Pipkin asymmetry) |
| 11 Halvren | §11 |
| 12 Saurin | §12 |
| 13 Presets and randomization | §13 |
| 14 Strengths | §14 |
| 15 Frequency vocabulary | §15 |
| 16 N0–N4 | §16 |
| 17 Validation tiers and harness | §17 |
| 18 Measurement-deferred policy and RM-UF | §18 |
| 19 OPEN / provisional | §19 |
| 20 Implementation firewall | §20 |

## 2. Exact canonical files changed

| File | Change |
|---|---|
| `decisions/UFCA_V1.md` | **New** canonical document |
| `decisions/PROJECT_RULES.md` | Authority line 2 names UFCA as companion. "Facial architecture status" now holds 7 concise universal UFCA rules (not a dump). Reviews line updated |
| `specs/STATUS.md` | UFCA Phase 1 accepted; Phase 2 completed; **UFCA NOT CLOSED** pending author review |
| `reviews/claude-pass2-r5-reference-mesh-queue.md` | New §3A with RM-UF-01…05 |
| All 13 race specs (`specs/<race>/<RACE>_V1.md`) | Minimal conforming edits (§3) |
| `tools/ufca/apply_phase2.py` | Edit script; every anchor asserts exactly one occurrence |

## 3. Race-spec conforming edits

Each spec gets **one inserted "UFCA status" paragraph** directly after its old provisional-organization status line. The old line is preserved as history. The paragraph:
- points to `decisions/UFCA_V1.md` and UFCA-08 Appendix A (the slot home for every Pass 1 control item);
- states that anatomy, tendencies, validators, tests and OPEN items are unchanged.

| Spec | Additional content in the pointer paragraph, or other edit |
|---|---|
| Marchfolk | Levels → Starting Face / Quick / Detailed; orbit and midface bound; forehead hidden pending confirmation |
| Skarn | Mouth and lips bound as human-family coverage ("not new Skarn anatomy"); human-auricle family; AC-U1 eye-size reading |
| Sagekin | Human-auricle family; AC-U1 |
| Fenn | Brow structure and brow-to-eye distance bound; forehead and further brow dimensions hidden; AC-U1 |
| Aelari | AC-U1 |
| Vael | AC-U1; Naturalize Face provisional |
| Halvren | "Overall relationships" → slot 1 soft tissue; no relationship tools (AD-U3); A / B / C per UFCA §11 |
| Durrim | Binds regional controls where anatomy states variation; depth domains A–E are DIAG / VAL under F-1 (spec wording "never five fully independent sliders" kept); sclera not a player control. In the OPEN list, "the Universal Facial Customization Architecture" is removed, with an annotation: canonicalized, closure pending; facial technical architecture stays OPEN |
| Grask | Coverage and invalid combinations bound; prognathism and tusk-like canines OPEN; projection held at authored central values |
| Gorrund | Coverage bound; projection held; TSC is a validator, not a slider; prognathism and tusks OPEN |
| Pipkin | Pointer; **new AC-U3 natural-asymmetry paragraph** after the §15 control list. OPEN-list items annotated "canonicalized; UFCA closure pending author review" |
| Cogling | Pointer + AC-U2 (no face-level sex slider; magnitude OPEN). §207B review-dependency item annotated "performed; closure pending" |
| Saurin | Pointer + §12 homologous routing + AC-U4; orbital spacing Bound-locked by §259. §265 carry-forward line now reads "Statistical calibration of soft distributions (UFCA canonicalized; closure pending)" |

**Nothing removed:** no facial anatomy section was rewritten, no requirement was erased, and no number was added.

## 4. AD-U implementation map

| Decision | Implementation |
|---|---|
| AD-U1 | UFCA §2–§4. Saurin structural ridges in Cranium & Forehead; keratin display in Hair / Cranial Display; rostral projection under Rostrum & Lateral Face; Facial Hair & Brows slot; Acquired sub-domain (§3, slot 12). "Shared navigation never implies anatomical equivalence" (§2) |
| AD-U2 | §6. CONSTRAIN "must be reported and biologically deterministic"; PROJECT_RULES rule 4 |
| AD-U3 (a) | §7 G-3; PROJECT_RULES rule 2; Halvren pointer |
| AD-U4 (a) | §5: non-Saurin head scale VAL / DIAG; Saurin ±8 % kept; no qualitative range invented |
| AD-U5 (a) | §5: no dentition controls; Acquired wear and loss; tusks OPEN |
| AD-U6 | §7 F-1, G-1…G-5; PROJECT_RULES rule 3 |
| AD-U7 (a) | §14: player-facing Subtle / Diverse / Extreme with the author's definitions; full manual range kept |
| AD-U8 (a) | §15: internal Very Common / Common / Uncommon / Rare, weighting only |
| AD-U9 | §19.1: Naturalize Face provisional; requirement preserved |
| AD-U10 | §16, §17: race tests authoritative; harness fills gaps |
| AD-U11 | §18 and queue §3A. RM-UF-02 dependency on authored Grask and Gorrund ranges is explicit |
| AD-U12 | §10.1(4), §10.3 bind-now table, §19.2 hidden list; PROJECT_RULES rule 1 ("a shared slot never by itself authorizes a control") |

## 5. AC-U implementation map

| Confirmation | Implementation |
|---|---|
| AC-U1 | §5. Pointers in Skarn, Sagekin, Fenn, Aelari and Vael, the specs that use "eye size" or "size" for eyes. PROJECT_RULES rule 5 |
| AC-U2 | §5; Cogling pointer |
| AC-U3 | §10.4; new Pipkin §15 paragraph |
| AC-U4 | §12; Saurin pointer |

## 6. Coverage-completion mapping (order §4)

### Bound

| Population | Item | Where recorded |
|---|---|---|
| Skarn | Mouth and lips (coverage clarification) | §10.3; Skarn pointer |
| Skarn, Sagekin | Human-auricle ear controls | §10.3; pointers |
| Marchfolk | Orbit and midface (v1.5 face validation) | §10.3; pointer |
| Durrim | Regional controls where anatomy states variation | §10.3; pointer |
| Grask, Gorrund | Coverage-list controls | §10.3; pointers |
| Fenn | Brow structure, brow-to-eye distance (stated) | §10.3; pointer |
| Pipkin | Natural asymmetry (AC-U3) | §10.4; Pipkin §15 |

### Hidden pending confirmation (§19.2)

| Population | Item | Note |
|---|---|---|
| Fenn | Forehead height / slope | See §9 Q-1 |
| Fenn | Further brow dimensions | — |
| Marchfolk | Forehead | Never mentioned in the spec (checked) |
| Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Halvren | Eyebrow-hair biology | Canon silent in all seven (checked) |
| Durrim | Sclera as a player control | Canon describes a derived appearance, kept DER in slot 4b |

**Canon passages checked.** For each held item, Claude and the independent auditor searched the current spec text for a passage that clearly resolves it. None was found, except the borderline Fenn forehead (§9 Q-1).

## 7. RM-UF queue additions

Added to `reviews/claude-pass2-r5-reference-mesh-queue.md` §3A:

| Item | What it measures |
|---|---|
| RM-UF-01 | Aperture vs orbit |
| RM-UF-02 | Ear-family envelopes; **depends on authored Grask ear-length and Gorrund projection ranges** |
| RM-UF-03 | Saurin orbital spacing tolerance |
| RM-UF-04 | Saurin structural-ridge and facial scale-field ranges |
| RM-UF-05 | Batch diversity threshold |

**Semantics only:** no numbers, and priority is unassigned.

## 8. Regression audit

**Method.** An independent agent that had not written the changes audited the full diff against order §5, §6 and §8.

**Result:** no anatomy, bound, test or OPEN item was altered, no requirement was erased and no number was invented. It found 2 medium and 8 low issues. **All were fixed** before this commit:

| # | Issue | Fix |
|---|---|---|
| 1 | (Medium) Pipkin, Saurin, Cogling and Durrim OPEN-list annotations said UFCA was "resolved", although UFCA is not closed | Changed to "canonicalized … UFCA closure pending author review" |
| 2 | (Medium) The bind-now decisions, including the Skarn mouth clarification, were not recorded in UFCA_V1 | Added §10.3 |
| 3 | Durrim pointer overstated the depth-domain rule | Now cites the spec's "never five fully independent sliders" |
| 4 | Gorrund pointer lacked a coverage-bound statement | Added |
| 5 | Frequency vocabulary was missing the author's word "internal" | Added in UFCA_V1 §15 and PROJECT_RULES |
| 6 | Skarn and Sagekin identity were listed as population validators without qualification | Qualified: Skarn "SOFT, never mandatory"; Sagekin "population-sample validation only" |
| 7 | F-1 was missing "only" ("whose only purpose is comparison") | Restored |
| 8 | Durrim ears were placed inside the human auricle family | Now: its own broadly humanoid compact range, routed to the human-auricle variable set |
| 9 | Stale Fenn line citation | Section citation used instead |
| 10 | "Saved characters store DIR values" overstated a schema still OPEN | Now: "the appearance record resolves to DIR values (schema implementation OPEN)" |

The PROJECT_RULES reference to this report is satisfied by this file.

### Order §8 checks (after fixes)

| # | Check | Result |
|---|---|---|
| 1 | Every requirement has a home | PASS: UFCA-08 Appendix A + pointers + §10.3 |
| 2 | No identity carrier lost | PASS: §10.1(2) |
| 3 | No shared-anatomy implication | PASS: §2 |
| 4 | No diagnostic index became a slider | PASS: F-1 |
| 5 | No OPEN biology silently resolved | PASS (after fix 1) |
| 6 | R-SEX respected | PASS: §5 SOFT only; Saurin none |
| 7 | Halvren not an ancestry-percentage face | PASS: §11, G-4 |
| 8 | Saurin has no human topology | PASS: §12 Absent list |
| 9 | Durrim / Grask / Gorrund / Pipkin / Cogling validators intact | PASS |
| 10 | Elf distinctions intact | PASS |
| 11 | Sagekin statistical | PASS (fix 6) |
| 12 | Marchfolk is the HRP, not a template | PASS |
| 13 | No preset-only anatomy | PASS: §13 |
| 14 | Randomization stays in envelope | PASS: §13 reject and resample |
| 15 | Extreme means valid tails | PASS: §14 |
| 16 | Pipkin asymmetry is not an identifier | PASS: §10.4 |
| 17 | Acquired ≠ asymmetry | PASS: slots 12 / 13 |
| 18 | Naturalize Face provisional | PASS: §19.1 |
| 19 | Measurement deferred | PASS: §18 |
| 20 | No UE5 assumptions canonized | PASS: §20 |

### Phase 1 audit questions, rerun on the canonical result

| Question | Result |
|---|---|
| Every requirement has a home | Yes |
| Identity weakened | No |
| Pass 1 item lost | No; all routed via Appendix A, and specs keep their lists |
| OPEN item silently resolved | No |
| Diagnostic turned into a control | No |
| Hidden ancestry / culture / personality / gameplay control | No |
| Simple and Advanced both supported | Yes |
| Presets as valid outputs | Yes |
| Halvren and Saurin without human topology | Yes |
| Author decisions still required | Only §9 |

### Stop conditions

None was triggered:
- no race was redesigned;
- no two accepted rules conflict;
- no biological answer or number was invented;
- no UE5 decision was needed.

## 9. Remaining OPEN / DEFERRED / PROVISIONAL, and author decisions

| Category | Items |
|---|---|
| **Provisional** | Naturalize Face (AD-U9) |
| **OPEN** (UFCA_V1 §19.1) | Low-light and pupil morphology (non-Saurin); Grask / Gorrund prognathism and separately-OPEN tusk-like canines; dentition counts; ear mobility; Grask / Gorrund ear ranges; sex-related facial magnitude (DU, GR, GO, PK, CG); non-Saurin head-to-stature; scleral tint; Saurin ocular, spacing, ridge, scale and display-beyond-family numerics; frequencies; lifecycle; Halvren genetics depth and ancestry UI; soft-distribution calibration; technical architecture |
| **Deferred** | RM-CF-01…10, RM-SR-04 / 05, RM-OT-03 / 04, RM-UF-01…05. The Saurin provisional rostral floor stays protective canon; no margin |

**Author decisions genuinely required** (confirmations, not contradictions):

| ID | Question | Detail |
|---|---|---|
| **Q-1** | Fenn forehead | FENN §2–7 pairs "smoother forehead-to-cranium line" with "Broad individual variation" for the cranium but never names forehead dimensions. **Options:** (a) keep hidden; (b) bind only a forehead-to-cranium transition contour; (c) bind forehead height / slope |
| **Q-2** | Eyebrow-hair biology for Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Halvren | Canon is silent, so it is hidden. These populations currently have eyebrow **grooming** (Presentation) but no eyebrow **biology** controls. Confirm whether their canon should state ordinary eyebrow variation |
| **Q-3** | Marchfolk forehead | Confirm whether Marchfolk canon should state forehead variation |
| **Q-4** | Fenn further brow dimensions (beyond brow structure and brow-to-eye distance) | Confirm or leave hidden |

## 10. Commit

The commit SHA is the commit containing this report; it is given in the delivery summary.

## 11. Recommendation

**UFCA READY TO CLOSE.** There is no architectural blocker. Q-1…Q-4 are race-canon coverage confirmations that the architecture already handles safely (hidden until confirmed). They can be answered at closure or carried as named OPEN coverage items without blocking it.

UFCA is **not** marked closed. STATUS records "Phase 2 completed; not closed; awaiting author review".

**STOP.**

— Claude

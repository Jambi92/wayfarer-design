# UCCA Phase 2 Canonicalization Report

**Author:** Claude (auditor / canonicalization agent)
**Order:** `reviews/chatgpt-ucca-phase2-canonicalization-order.md`
**Canonicalization commit:** `72d2888`
**Recommendation:** **UCCA READY TO CLOSE**, subject to two small author confirmations (§9).

## 1. Canonical document

`decisions/UCCA_V1.md`: 26 sections, matching the order's §4 minimum contents one-to-one (purpose and authority … implementation firewall). Authority level 2, as the whole-character companion to PROJECT_RULES alongside UFCA.

## 2. Canonical files changed (commit 72d2888)

| File | Change |
|---|---|
| `decisions/UCCA_V1.md` | **New** canonical document |
| `decisions/PROJECT_RULES.md` | New "Whole-character architecture status" section (11 universal rules); authority line 2 names UCCA; Reviews line; T-11 sentence under Technical authority |
| `specs/<race>/<RACE>_V1.md` × 13 | One UCCA status pointer each (end of spec), plus the T-rulings below. Scripted by `tools/ucca/apply_phase2.py` (assert-unique anchors) |
| `register/decision-register.md` | T-8 four-layer line; T-7 two Grask "tallest" lines; Aelari preset line (T-3) |
| `reviews/claude-pass2-r5-reference-mesh-queue.md` | New §3B RM-UB-01…05; RM-SR-05 case set to 152 cm (T-6) |
| `specs/STATUS.md` | UCCA canonicalized (closure pending), added **after** the regression audit passed |
| `tools/ucca/apply_phase2.py` | New edit script |

**Not changed:** `decisions/UFCA_V1.md`; the 13 race specs' anatomy, numbers, tests and OPEN items; `plan/` and `rules/` (level 6 / historical).

## 3. AD-C implementation mapping

| Ruling | Where implemented |
|---|---|
| AD-C1 15 slots | UCCA §2; PROJECT_RULES |
| AD-C2 no frame state | UCCA §7, §19 P-1…P-5; PROJECT_RULES |
| AD-C3 race-relative storage | UCCA §4, §6; PROJECT_RULES |
| **AD-C3b** Halvren tails | UCCA §22 (central envelope, tails supported, never hard-clipped, limits BIO/MEAS deferred, interim scope must be labelled non-canonical); RM-UB-05; HALVREN pointer and T-5 |
| AD-C4 capacity, option (a) | UCCA §10 (Detailed only for Saurin and Cogling; VAL ceiling elsewhere; no invented shifts; no gameplay); COGLING pointer; PROJECT_RULES |
| AD-C5 composition operations | UCCA §10 ("Custom" is a UI state); PROJECT_RULES |
| AD-C6 sex SOFT input | UCCA §11 |
| AD-C7 body hair | UCCA §13; PROJECT_RULES; every pointer cites §13 |
| **AD-C8** universal subtle asymmetry | UCCA §16 (near-zero default; no numbers; never injury/deformity/identity); asymmetry validator in §24; every pointer; PROJECT_RULES |
| **AD-C9** Environmental subtypes | UCCA §14; GORRUND and DURRIM notes; PROJECT_RULES |
| AD-C10 neck | UCCA §2, §4 |
| AD-C11 Body Language | UCCA §17 |
| AD-C12 scopes and locks | UCCA §20 |
| AD-C13 record domains, S-1…S-7 | UCCA §21 |
| AD-C14 pairwise harness | UCCA §24 |
| AD-C15 universal validators | UCCA §24 (plus the asymmetry test needed by AD-C8) |
| AD-C16 tensions | §4 below |
| AD-C17 slot ≠ authorization | UCCA §3, §4; PROJECT_RULES |

## 4. T-1…T-12 resolution mapping

| # | Resolution | Location |
|---|---|---|
| T-1 | §55 stature-share wording marked as reference/central morphology; §258 ±8 % governs creator variation. No new number | SAURIN §55 note; UCCA §23 |
| T-2 | Absorption is relationship-aware behaviour inside the leg rule; positive identity preserved; numeric split deferred (RM-UB-01, RM-SR) | PIPKIN note after the trunk paragraph |
| T-3 | One Aelari presentation-preset system: union of both lists (9 entries) in v1.4 §4; v1.3 §24 now points to it | AELARI; register |
| T-4 | §145 "muscularity" marked superseded by §256.6 | SAURIN §145; UCCA §9 |
| T-5 | Old "provisional height range" wording reconciled to central envelope + OPEN tails | HALVREN Part 2 summary and height table |
| T-6 | 152 cm canonical; "about 150–152" kept as history only | DURRIM equal-height row and comparison methods; RM-SR-05 |
| T-7 | Absolute "tallest" replaced: Grask are a very tall population; Gorrund sets the tallest | GRASK world-validation paragraph; register (2 lines) |
| T-8 | Four Skin Appearance Layers | register |
| T-9 | Ordinary callusing = Environmental-persistent; permanent history-like change = Acquired | UCCA §14; GORRUND note |
| T-10 | Vael shoulder and pelvic breadth bound through Skeletal Frame; no ranges | VAEL torso row; UCCA §7 |
| T-11 | Canon supersedes the prototype age-speed and record wording | PROJECT_RULES; UCCA §15, §21. The plan file itself was not edited (level 6, Tyler's document) |
| T-12 | Central-only testing allowed only if labelled non-canonical | UCCA §22 |

## 5. RM-UB / deferred queue mapping

| ID | Status |
|---|---|
| RM-UB-01 segment-share bands | Queued (§3B); also carries the Pipkin T-2 numeric split |
| RM-UB-02 allometry | Queued |
| RM-UB-03 joint / robusticity envelopes | Queued |
| RM-UB-04 Saurin reachable tail cap | Queued |
| **RM-UB-05** Halvren inherited stature tails | **New**, queued with an authorship-first dependency (AD-C3b) |
| RM-LR, RM-SR, RM-OT, RM-CF, RM-UF | Carried unchanged; only RM-SR-05's comparison stature corrected to 152 cm (T-6) |

## 6. 20-question regression audit

An independent agent audited the uncommitted canonicalization read-only. Its findings were verified against the specs before any fix.

| # | Question | Result |
|---|---|---|
| 1 | Every non-facial requirement has a home | PASS (Phase 1 Appendix A, routed by the 13 pointers) |
| 2 | Positive identity not weakened | PASS |
| 3 | No Pass 1 requirement lost | PASS |
| 4 | No OPEN silently closed | PASS (UCCA §25; T-2 numeric kept deferred) |
| 5 | No diagnostic became a slider | PASS (§4 firewall) |
| 6 | No hidden ancestry/culture/personality/gameplay control | PASS |
| 7 | Simple and Advanced supported | PASS (§2; equivalence validator §24) |
| 8 | Presets legitimate | PASS (§19) |
| 9 | Saved appearance complete and semantic | PASS (§21) |
| 10 | No uniform scaling | PASS (§6, §24) |
| 11 | Frame / Composition independent | PASS (§7 write scope incl. Saurin; §10) |
| 12 | Height relationship-aware | PASS (§6) |
| 13 | R-SEX and age separation | PASS (§11, §15) |
| 14 | Halvren: no percentage slider, no invented tail numbers | PASS (§22) |
| 15 | Saurin nonhuman, tail mandatory | PASS (§9, §23) |
| 16 | Clean UFCA integration | PASS (after the head-scale fix, §7) |
| 17 | Surface / hair systems preserved | PASS |
| 18 | UE5 deferred | PASS (§26) |
| 19 | New author decisions | §9 |
| 20 | No conflict with frozen Pass 2 / closed UFCA | PASS (UFCA_V1 has no diff) |

**Order §7 checklist extras:** all 13 populations PASS; body-hair silences hidden PASS; asymmetry never deformity, injury or race identity PASS; Environmental vs Acquired coherent PASS (after the Durrim fix).

**Stop-condition audit:** **no genuine biological incompatibility.** T-1 and T-2 were reconciled without new numbers or a winner.

**Numbers:** every number in UCCA_V1 traces to canon (Saurin §256, §258, §263; Halvren §10–14; Durrim 152 cm).

## 7. Audit findings fixed (all verified first)

| Finding | Fix |
|---|---|
| UCCA §5 cited §256.9 for REDISTRIBUTE; §256.9 says stature is isometric for tail relationships, so the tail is not in stature accounting | Rewritten: head, neck, thorax, lower trunk and legs sum to stature (SAURIN §55; SAU-FACE-22) |
| Possible double head control: UFCA slot 1 "Head scale (Saurin)" and UCCA Slot 2 head-to-body are the same §258 control | UCCA §12 states it is one variable shown in both places |
| UCCA §6.6 said distributions are OPEN/SILENT for every race | Narrowed to stature/proportion distributions; Saurin §263 centres noted |
| Register still said the Aelari v1.4 list "replaces" v1.3 §24 | Updated to the T-3 union |
| DURRIM still called sun exposure and weathering "transient", next to the new AD-C9 note | Sentence reworded to "environmental states … persistent and transient subtypes below" |
| RM-SR-05 still used ~150–152 cm | Set to 152 cm |

## 8. Remaining OPEN / DEFERRED / PROVISIONAL

- **BIO OPEN:** the full list in UCCA §25 (pelvic morphology, segment numbers, head-to-stature outside Saurin, capacity and fat distributions, dimorphism magnitude, reproductive biology, lifecycle, body hair for DU/GR/GO, Halvren stature tails, Saurin §265 items including acquired tail loss and thermoregulation, skin durability).
- **Measurement-deferred:** RM-UB-01…05 plus all existing RM queues.
- **Implementation-deferred:** everything in UCCA §26.
- **Later gameplay review:** legacy racial traits.
- **Housekeeping noticed, not changed (outside this order's scope):** five lines still say "UFCA closure pending author review" although UFCA is CLOSED: COGLING L3217, PIPKIN L1556 and L1651, DURRIM L522, SAURIN L4275 (line numbers before this commit). A one-word status update would fix them if the author wants it.

## 9. Author confirmations requested (small)

1. **Aelari union naming (T-3):** the merged list keeps both **Arcane Institutional** and **Institutional Practical**, and merges "Artisan Practical"/"Artisan", "Military Formal"/"Military" and "Rural/Provincial"/"Provincial" into one entry each. Confirm, or name the entries to drop.
2. **Saurin head scale:** confirm that UFCA slot 1 head scale and UCCA Slot 2 head-to-body are one §258 variable shown in two places (this matches UFCA AD-U4's citation of §258; no new rule).

Neither blocks closure.

## 10. Commits

- `72d2888`: canonicalization (UCCA_V1, PROJECT_RULES, 13 specs, register, RM queue, STATUS, script).
- This report: the following commit.

## 11. Recommendation

**UCCA READY TO CLOSE.** No stop condition, no unimplemented ruling, no invented numbers, UFCA unchanged. Stopping here: no UE5, mesh, animation, camera, equipment, first-person, save-serialization or gameplay work.

— Claude

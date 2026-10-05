# Pass 2 Closure Audit

**Author:** Claude (auditor). **Order:** `reviews/chatgpt-pass2-resolution-sequence-order.md` §9. **Deliverable 6.** This audit maps every Pass 2 finding (`claude-pass2-06-findings.md`) to its state after the resolution sequence.

**Status classes** (order §9.6):
- **RESOLVED**
- **RESOLVED BY AUTHORITY / conforming edit pending**
- **DEFERRED WITH NAMED INPUT**
- **Genuinely OPEN**

Where a finding has parts in more than one class, the primary class is listed first and the residual follows.

**Deliverables of this sequence:**
- r1 — `claude-pass2-r1-authority-terminology.md`
- r2 — `claude-pass2-r2-large-race-comparative-review.md`
- r3 — `claude-pass2-r3-craniofacial-framework.md`
- r4 — `claude-pass2-r4-conforming-edit-plan.md` (166 rows plus AC-1…AC-10)
- r5 — `claude-pass2-r5-reference-mesh-queue.md`
- r6 — this audit

## 1. Finding map

| Finding | Sev. | State | Basis / residual |
|---|---|---|---|
| F-01 Large-Race review missing | MAJOR | **RESOLVED** (review performed; no contradiction; no redesign) | r2. Residual: **author decisions AD-1–AD-4** (genuinely OPEN, §2). Numeric validators **DEFERRED WITH NAMED INPUT** RM-LR-01…07 |
| F-02 Saurin rostral floor depends on non-existent ranges | MAJOR | **DEFERRED WITH NAMED INPUT** | Framework built (r3). Cross-race numeric closure needs RM-CF-01…05; the Grask and Gorrund projection distributions must be authored first. Saurin floor kept, not weakened |
| F-03 No roster sex-related rule | MAJOR | **RESOLVED** | R-SEX adopted and recorded in PROJECT_RULES; the 13-spec audit found no conflict (r1 §3). Terminology rows E12 pending |
| F-04 Skarn muscle trait in skeleton | MAJOR | **RESOLVED BY AUTHORITY / edit pending** | Muscular Development Capacity adopted (PROJECT_RULES); rows E1-01, -02, -05 |
| F-05 Unnamed comparators / "baseline" | MAJOR | **RESOLVED BY AUTHORITY / edit pending** | "Unqualified human" rule plus baseline retirement adopted; rows E2, E3. Residual **AC-1** ("near-human"), **AC-2** (Saurin "baseline" sense) |
| F-06 Unquantified identity envelopes | MAJOR | **DEFERRED WITH NAMED INPUT** | Order §8: qualitative design closes now; validators come from RM-SR-01…06, RM-LR-01…07, RM-OT-01/02 |
| F-07 Saurin "ridge" ambiguity | MAJOR | **RESOLVED BY AUTHORITY / edit pending** | Structural vs keratin ridge adopted; rows E5 (36) |
| F-08 Authority documents drifted | MAJOR | **RESOLVED** | Hierarchy recorded in PROJECT_RULES; precedence notice applied to the register. Residual: register *content* reconciliation is optional while it is historical (genuinely OPEN, non-blocking) |
| F-09 "race" overloaded | MAJOR | **RESOLVED** | Population / playable lineage / culture / social identity adopted (PROJECT_RULES) |
| F-10 Stale brief | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Level 6 in the hierarchy; banner row E8-01 plus 18-item contradiction list |
| F-11 Stale status / process wording | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Rows E7 (30). E7-08 applied through the PROJECT_RULES Reviews rewrite; E7-09 superseded by this audit's STATUS update |
| F-12 Dangling references | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Rows E11 |
| F-13 Saurin internal residuals | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Later canon governs (§249 convention); rows E5, E9 (process tokens incl. "RSI"), E10-01…09. E10-05 (§36a status) and E10-06 (§44 vs §259) are marked AUTHOR CONFIRM |
| F-14 Skin Appearance Layers count | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Four layers adopted; rows E6 (16, incl. Vael's missing Acquired). Residual **AC-3** ("dirt") |
| F-15 Simple vs Basic | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Rows E4 |
| F-16 Layer wording leaks | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Frame-word reservation adopted; rows E13. Fat amount/distribution is governed by PROJECT_RULES |
| F-17 Legacy gameplay traits | MINOR | **DEFERRED WITH NAMED INPUT** | Race → Biology → Gameplay review (register R:40, R:419). Out of Pass 2 scope (order §8 of the Pass 2 order) |
| F-18 Ear-anatomy gaps | MINOR | **Genuinely OPEN** (author confirm) | **AC-4** (Skarn and Sagekin follow the Marchfolk human auricle), **AC-5** (Fenn ear tendency pointer). Fenn content is already settled by the elf review (level 3) |
| F-19 Sagekin tensions | MINOR | **Genuinely OPEN** (author confirm) | **AC-6** (hands and ribcage reading), **AC-7** (activate the elf-boundary test). Numbers: RM-OT-01. Pigmentation disclaimer recommendation stands |
| F-20 Elf-family residuals | MINOR | **RESOLVED BY AUTHORITY / edit pending** | The elf review governs its interpretations; row E10-15 (Fenn low-light restored to the review's register). Orbit numbers: RM-CF-08 |
| F-21 Section and ID schemes | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Rows E11 (Gorrund GOR- throughout; Grask "§70" → P5 §61–72) |
| F-22 Cogling residuals | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Rows E10-10…13. Residual **AC-8** (FD-HAIR), **AC-9** (frame vs robusticity) |
| F-23 Halvren residuals | MINOR | **RESOLVED BY AUTHORITY / edit pending** | Rows E1-04, E2-11, E2-12 |
| F-24 Muscular Development Capacity absent from PROJECT_RULES | MINOR | **RESOLVED** | Added to PROJECT_RULES terminology |
| F-25 Saurin cross-race coverage | MINOR | **DEFERRED WITH NAMED INPUT** | RM-OT-04; add Saurin–Sagekin and Saurin–Halvren matched-height tests when the measurements exist. Low risk |
| I-01…I-07 | INFO | No action | — |

**Counts:**

| Class | Findings |
|---|---|
| RESOLVED | F-01, F-03, F-08, F-09, F-24 (5) |
| RESOLVED BY AUTHORITY / edit pending | F-04, F-05, F-07, F-10–F-16, F-20–F-23 (14) |
| DEFERRED WITH NAMED INPUT | F-02, F-06, F-17, F-25 (4) |
| Genuinely OPEN | F-18, F-19 (2, author confirmation only) |

## 2. Genuinely OPEN items created or exposed by this sequence

All of these need author decisions. None is an anatomical contradiction.

| ID | Item | Source |
|---|---|---|
| AD-1 | Add a Skarn–Gorrund boundary test, including a taller Broad Skarn | r2 LR-03 |
| AD-2 | Add a GR-BODY-10 × Skarn test | r2 LR-06 |
| **AD-3** | **Short-limbed Grask vs Gorrund separation:** a directional floor (recommended) or architectural separation only | r2 **LR-07, UNDETERMINED** |
| AD-4 | Confirm Skarn–Gorrund proportional separation is "undetermined by design" | r2 LR-12 |
| AD-5 | Optional Skarn → Grask pointer | r2 |
| AC-1…AC-10 | Terminology and interpretation confirmations | r4 §0 |
| RM-CF-05 | The FPI margin between the Saurin floor and other populations' valid maxima | r3 §7 |
| — | Approval or rejection of the 166 conforming-edit rows | r4 |

## 3. Stop-condition check (order §10)

| Condition | Result |
|---|---|
| A resolution would materially redesign an approved race | **No.** No row or decision alters positive anatomy |
| The Large-Race review finds a genuine contradiction | **No.** 11 candidates tested, none genuine (r2 §6) |
| A craniofacial metric cannot compare populations without imposing the wrong anatomy | **No.** Homologous landmarks with N/A flags; FAL defined without a nasal pyramid, lips or chin (r3 §6) |
| A missing number would have to be invented | **Avoided.** Every number is deferred to RM-* with named inputs |

## 4. Actual state, and the STATUS update

**The Pass 2 resolution sequence is complete as a deliverable set.** It is **not yet closed**, because closure needs author action on:
- AD-1–AD-4;
- AC-1–AC-10;
- the conforming-edit rows.

Per order, the **UFCA does not begin** until ChatGPT closes the sequence.

`specs/STATUS.md` is updated to say exactly this (order §9.7). PROJECT_RULES "Reviews" already records the Large-Race review as performed with author decisions pending.

— Claude

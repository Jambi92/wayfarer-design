# RAC RM-OT-05I — Gorrund S3 trunk re-sculpt, protection patch and Stage C gate

Order: `reviews/chatgpt-rac-rm-ot-05i-gorrund-s3-trunk-resculpt-stage-c-order.md`. Sculptor: Claude, working by hand in desktop Blender 5.2.2 LTS on Windows. Date: 2026-10-12.

Evidence:
- `reviews/rac-rmot05i-evidence/` (hashes in `SHA256SUMS.txt`);
- `reviews/rac-rmot05i-protection/`;
- tools in `tools/rac/w1/rmot05i_drivers/`.

## Gate lines

| Line | Status |
|---|---|
| 05H author dispositions applied | **YES** |
| Hand/digit protection overlay | **PASS** |
| Final sculpt revision | **S3** (no S4; see §8) |
| Family A canon-form audit | **PASS (marginal) before export.** The blind evidence later contradicts it (§7). |
| B/C integration | **PASS** |
| E/F symmetry cleanup | **PASS** (E fixed; F within inherited tolerance) |
| Exporter | **PASS** |
| Preflight | **PASS** |
| 05F re-entry | **PASS** |
| Low-composition structural read | **FAIL** (blind run 1 reads it as an obese human) |
| Replicated blind gate | **FAIL** |
| Blind-reason canon audit | **FAIL** |
| Gorrund structural readability | **REJECT** |
| Grask E3 Stage C | **NOT RUN** |
| Gorrund Stage C | **NOT RUN** |
| Combined Stage C | **NOT RUN** |
| RM-OT-05 | **OPEN** |
| Canon promotion | **NOT PERFORMED** |
| D4 | **NOT STARTED** |
| UE5 | **NOT STARTED** |

Nothing in the validation chain was changed:
- re-entry validator, guards and thresholds;
- scorer prompt;
- tally rules;
- canon rules.

`f_reentry.py`, `f_blind.py`, `f_tally.py` and `f_scorer_prompt.md` are byte-identical to `main`. The frozen RM-OT-05G release was not rewritten. Grask E3 was not touched.

## 1. 05H dispositions applied

- **Base:** S2 is the working base. S3 continues the same `GO_sculpt_S1_work.blend`, which was at the S2 state in backup 14.
- **Frozen items:** Grask E3 stays frozen and RM-OT-05 stays open.
- **Protection:** the protection ruling (§3) and the symmetry ruling (§4) are both applied.
- **Symmetry method:** edits were applied per side, and asymmetry is measured relative to the source template. No world-X mirror was used and no symmetrize was applied.

## 2. Hand/digit protection overlay — PASS

**Source rule:** the `f_guard.py hand_foot_topology` mask, i.e. `clip(w_hand_l + w_hand_r + w_fingers_l + w_fingers_r + w_ball_l + w_ball_r, 0, 1) > 0.5`. It is taken on keep vertices of the accepted skeleton route GO5DE1, restricted to body vertices 0..13379. This is the same criterion the guard uses.

| Item | Count |
|---|---|
| Guard hand/digit mask | 3 182 |
| Guard foot mask | 1 486 |
| Old `NO_TOUCH_hands_digits` | 2 378 |
| Added | **804** |
| New protected hand/digit total | 3 182 |
| Foot part already fully inside `NO_TOUCH_toes_forefoot` | 0 added |

**Family overlap:** 42 of the added vertices are FAM_E (wrist). They are now protected.

**How the overlay is delivered**
- **Data:** `reviews/rac-rmot05i-protection/regions_05i.json`, SHA-256 `f5ef813f…113f35`. It contains the frozen 05G regions unchanged plus one key, `NO_TOUCH_hands_digits_guard05i`.
- **Exporter and preflight:** they run from a derivative copy of the 05G package with this `regions.json`. Exporter X9 and preflight P4 iterate every `NO_TOUCH_*` key, so they cover the added vertices with the unchanged 0.5 cm limit.
- **Blender:** `i_blender_overlay.py` adds the vertex group, adds it to `NO_TOUCH_all` and re-installs the sculpt mask. It never touches coordinates.

**Verification** (`overlay_verify.json`, headless bpy 5.0.1; script `i_verify.py`):

| Check | Result |
|---|---|
| V1 unedited round trip | Export PASS, X9 0.0 on every key, preflight PASS with both packages |
| V2 masking | All 804 added vertices masked (8 963 masked in total) |
| V3 negative fixture: vertex 3549 (FAM_E wrist) moved 1.0 cm | **Overlay export refused (X9) and overlay preflight FAIL; the frozen 05G package passed the same edit.** The gap is closed. |
| V4 scope | Frozen keys identical, only the one key added, template identical |

**Desktop:** the overlay was applied to the working sculpt in Blender 5.2.2. Every S3 WIP and final export ran through the overlay package.

## 3. S3 sculpt (bounded, on the S2 working sculpt)

**Method:** standard Blender edit operators on selections made by vertex group, coordinate box or index from the Blender console. The operators used:
- translate or resize with proportional editing;
- Shrink/Fatten;
- Smooth Vertices;
- Blend from Shape, using temporary shape keys from `GO_SOURCE_REFERENCE` or from earlier backups of the same sculpt. The keys were removed before every export.

Each step was checked by a WIP export (true floor, cross-sections, close renders). Several WIP states were run through the full unchanged re-entry as WIP IDs (W5 to W8), which is how one Broad-frame hand/hip contact was found and fixed. Backups 14 to 24 are on the PC.

**Family A rebuild**
- Lower-trunk lateral planes narrowed from \|x\| 24 to about 22.7, with a gentle convex rib-cage side (about 23.6 at z 140–152) instead of a straight slab side.
- Antero- and postero-lateral corners radiused using partial reference blends plus smoothing. Cross-sections are now a broad front plane, oblique transitions and a lateral plane.
- The chest-plate top edge (the S2 "V plate" border at z 172–180) was removed by receding the upper chest and smoothing the clavicular transition.
- The abdomen is recessed below the rib cage, with a subcostal arch at the midline. The costal border reads as a sloped transition, not a horizontal shelf. The lower midline is kept above the true floor.
- Nipple, navel and plate-edge creases were smoothed. The nipple was a crowded vertex clump left from S1; it is now 0.22 cm above its ring.
- The hip-front "belt" band was smoothed.

**Other families**
- **B:** columns kept; one over-smoothing pass reverted; part of the inherited left sacral drift reduced.
- **C:** hip-front floor margins restored, and the lateral hip beside the hanging hand restored to reference (Broad-frame contact).
- **D:** unchanged.
- **E:** inner upper-arm/elbow vertices beside the trunk restored to reference, which removed the one-sided 3.1 cm drift. The two wrist vertices over 0.5 cm were restored, and all 804 overlay vertices are at 0.0.
- **F:** unchanged.

## 4. Canon-form self-audit (before export)

Evidence: `audit/S2_vs_S3_audit_sheet.jpg` (F/Q/P/RQ grey and silhouette, plus the S3 low preview) and `audit/S3_family_close_views.jpg`. This audit did not use any blind scorer output.

| # | Question | Answer |
|---|---|---|
| 1 | Trunk still rectangular? | NO, marginal: corners radiused and sides convex, but the front silhouette still has fairly straight sides and no waist |
| 2 | Still boxy? | NO |
| 3 | Mechanically slab-sided? | NO |
| 4 | Belt or shelf over the pelvis? | NO |
| 5 | Chest top border a plate edge? | NO |
| 6 | Low composition reads as a protruding belly or obese chest? | NO, marginal: the authoritative GO5FS3-LOW shows a deep rib cage over a recessed abdomen, but the low donor's navel and one nipple stay visible |
| 7 | Thorax deep and structurally Gorrund? | YES |
| 8 | Anterior / transition / lateral planes legible? | YES, marginal: softer than S2 |
| 9 | Pelvis-to-thigh step without a trunk-to-pelvis discontinuity? | YES |
| 10 | B–F still the S2 hard-form families? | YES |

Under §10 this allowed export. §7 shows that the marginal answers to 1 and 6 were wrong as far as observers are concerned.

## 5. Export, preflight and final hashes

| Artifact | SHA-256 |
|---|---|
| `GO_sculpt_S3_r6.obj` | `753355ce4d872eff19dab29a3cc00e1d31d0a1eeb6d3f79bee0e0629dce2bf7d` |
| `GO_sculpt_S3_r6_export_report.json` | `4c7c725d1eace0893e49804d5b7b72de12ecf48895acd1df8ec3b8fee0c3997e` |
| `GO_sculpt_S1_work.blend` at S3 | `0629dae92abf118cc5aad313d6679d856bd3ff2b527db31646bff223a5d02c3a` |
| `regions_05i.json` (protection overlay) | `f5ef813f1cf9296e69c9780b7f192962644a41460c9b6497520681485e113f35` |

**Export:** RAC_EXPORT PASS. X9 is 0.0 on all four `NO_TOUCH` keys, including guard05i. 2 785 vertices moved. Family maxima:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| 5.17 cm | 6.03 cm | 4.04 cm | 3.45 cm | 1.66 cm | 5.54 cm |

**Preflight:** PREFLIGHT PASS with the overlay package, and also with the frozen package. P6 true floor: 0 vertices inside, minimum −0.18 cm.

**Preview console (advisory):**

| Preview | Inside the true floor (0.2 cm) | New ones caused by the sculpt |
|---|---|---|
| Low | 21 | 7 |
| Narrow | 0 | 0 |
| Broad | 1 | 1 |

**Files:**
- Views: 32 on the PC (`…/sculpt/S3/views`). Committed: the 8 `GO_SCULPT_BASE` views plus grey and silhouette contact sheets.
- Manifest: `S3/GO_sculpt_S3_manifest.json`, including the desktop-verification block and the overlay hash.
- The working `.blend` is not committed (4.7 MB).

## 6. 05F re-entry (unchanged) — PASS

Command: `python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_S3_r6.obj S3` → RE-ENTRY PASS.
- Ingest I1–I6 all pass.
- Every 05D/05E guard passes in GO5FS3, -LOW, N and B, including composition and frame ordering.

| State | Piercing edges vs route | Floor | Hand/digit change | Arm–trunk gap |
|---|---|---|---|---|
| Reference | 71 vs 67 | 0 inside | 0.00 cm | 0.60 cm |
| Low | 74 vs 78 | 0 inside | 0.00 cm | 0.77 cm |
| Narrow | 60 vs 57 | 0 inside | 0.00 cm | 0.84 cm |
| Broad | 53 vs 53 | 0 inside | 0.00 cm | 0.87 cm |

- **Volume ratio:** 0.9999999.
- **Reproduction of the delivered surface:** p90 0.20 cm, max 0.37 cm.

Retention (median / p10), reference state:

| Family | Median | p10 |
|---|---|---|
| A | 0.97 | 0.81 |
| B | 1.00 | 0.83 |
| C | 0.90 | 0.75 |
| D | 0.83 | 0.66 |
| E | 1.00 | 1.00 |
| F | 1.00 | 1.00 |

Low, Narrow and Broad are similar. Files are in `reentry/`.

**Low-composition special review** (`audit/S3_low_composition_sheet.jpg`, rendered from the authoritative GO5FS3-LOW build):
- The deep rib cage, the costal transition to a recessed abdomen, the posterior columns and the pelvis-to-thigh step survive.
- The belly no longer protrudes the way S2-LOW did.
- The low donor's navel and one nipple remain visible, and the front still reads soft.

The blind run (§7) confirms observers read this state as fat. Line: **FAIL**.

## 7. Replicated blind gate — FAIL; blind-reason audit — FAIL

**Protocol**
- `f_blind.py S3 run1` (set P) and `run2` (set Q). Each set has 12 bodies: 8 human controls, Grask E3 reference and low, and the S3 reference and low.
- **Scorers:** 6 new subagents with no context from RM-OT-05H, 3 per run, each given only the `f_scorer_prompt.md` text verbatim and the two sheets. The sheets were copied to neutral folders.
- **Run 1 key:** S3 reference P11, S3 low P01, Grask P09/P02.
- **Run 2 key:** S3 reference Q07, S3 low Q12, Grask Q10/Q08.

| Line | Run 1 | Run 2 |
|---|---|---|
| G1 reference C | **0/3 ✘** | 3/3 ✔ |
| G2 low C | **0/3 ✘** | 3/3 ✔ |
| G3 stable ref+low group | 2/3 ✔ | **0/3 ✘** |
| G4 distinct from Grask | 3/3 ✔ | 3/3 ✔ |
| G5 organization basis | **0/3 ✘** | 2/3 ✔ |
| G6 axial + limb cues | 3/3 ✔ | 3/3 ✔ |
| G7 no control collapse | ✔ | ✔ |
| Run | **FAIL** | **FAIL** |

- **Posture read:** 0 for the sculpt.
- **Grask E3:** C 3/3 at reference and low in both runs, distinct from Gorrund in both.

**Blind-reason audit** (verbatim excerpts; full JSONs in `blind/`):

**Run 1** — all three scorers put S3 in **B (fatness ×2, bulk ×1)**:
- "Thick, blocky trunk with a soft belly that sticks out in profile; wide waist with little taper; heavy thighs."
- "Very wide, flat, blocky trunk with a heavy belly and deep back … Reads as a heavy or obese human."
- "Most likely a heavy or stocky human, but it could be a stocky dwarf-like race."

**Run 2** — all three scorers put S3 in C, but for canon-forbidden reasons:
- "Boxy rectangular trunk with almost no waist, flat straight back, very thick columnar legs … stocky dwarf-like build."
- "Boxy, straight-sided trunk … segments read as blocks."
- "Boxy, rectangular trunk with flat front and very deep, slab-like profile."
- The low body Q12 was read as "could be an obese/heavy human" by all three, and the group was marked unstable by all three.

So run 1 fails as an obesity read, and run 2's C votes rest on "rectangular / boxy / slab" trunk reads, which author ruling Q1 and order §15 count as failure even when the numbers pass.

## 8. Why there is no S4

§16 allows S4 only for one localized, diagnosable weakness, or for a trunk-legality correction that is clear and bounded. The S3 evidence fails both conditions:

1. **The two failure modes point in opposite directions.** Rounding and softening the trunk (S2 → S3) moved the read from "boxy race" to "obese human". The remaining "rectangular, no waist" read comes from the overall width, depth and silhouette of the accepted route, and from the "thick columnar legs" every scorer cites. Pulling the trunk back toward planes reintroduces the forbidden box; rounding it further strengthens the fat read.
2. **The weakness is not localized.** Scorers cite trunk silhouette, trunk depth, limb thickness and the waist-less front outline together. The limb and trunk proportions belong to the accepted skeleton and proportion route, which §17 says not to reopen.

I judged that another bounded revision would be tuning toward scorer wording, which the order forbids, so I stopped at S3.

## 9. Left/right audit (source-relative)

Pairs come from nearest-neighbour mirror correspondence on the unchanged template. The template's own mirror error is p50 0.0, p90 0.09 and max 1.16 cm. Files are in `symmetry/`.

| Family | S2 asym p90 / max | S3 asym p90 / max | Mean displacement L / R (S3) |
|---|---|---|---|
| A | 0.63 / 2.21 | 0.87 / 2.56 | 2.04 / 2.03 |
| B | 0.75 / 1.87 | 0.79 / 1.84 | 2.10 / 2.10 |
| C | 1.30 / 2.35 | 1.24 / 2.56 | 1.25 / 1.32 |
| D | 0.05 / 0.42 | 0.05 / 0.42 | 0.36 / 0.36 |
| E | 0.00 / 3.13 | **0.00 / 0.03** | 0.08 / 0.08 |
| F | 0.21 / 1.06 | 0.21 / 1.06 | 0.98 / 1.01 |

**Residual:** a few A/C vertices at the hip-front corner and lower abdomen (z 119–132) differ by up to about 2.6 cm between sides. The causes are an S1-inherited left medial drift (partly corrected) and side-specific floor-margin pushes. Overall mean displacement per side is balanced.

## 10. Remaining failures, marginals and blockers

1. **Blind gate FAIL and blind-reason FAIL.** The Gorrund reference at S3 reads either as an obese or stocky human, or as a boxy dwarf-like race. Neither read is canon-legal.
2. **Low composition** keeps the low donor's navel and one nipple. Observers read it as a soft human.
3. **Design-level blocker for the author.** At the accepted route proportions (wide, deep trunk; thick limbs; no waist), a hand-sculpted surface layer has not yet found a canon-legal non-human read: planar gives "box", rounded gives "fat". The author may want to rule on which non-human cue family the Gorrund reference should carry, within canon, before any S4/S5. Candidates include more pronounced costal and sternal structural articulation, the posterior load path, and limb joint architecture.
4. **Marginal:** the arm–trunk gap at the reference state is 0.60 cm (it passes; no interpenetration).
5. **Residual asymmetry:** A/C hip-front, as in §9.
6. **Leftover desktop files:** the old DT desktop-check files are still in `…/sculpt/work_desktop_check/_to_delete/` for the author to delete.

## 11. Confirmation

No validator threshold, guard, scorer prompt, tally rule or canon rule was changed. The protection overlay only adds protection and is verified by a negative fixture. No procedural body, remesh or new base mesh was used. Stopping at the RM-OT-05I author gate: no Stage C, no canon promotion, no RM-OT-05 closure, no D4, no UE5.

# RAC RM-OT-05H — Claude-direct Gorrund sculpt / re-entry / Stage C gate

Order: `reviews/chatgpt-rac-rm-ot-05h-claude-direct-sculpt-stage-c-order.md`. Sculptor: Claude, by hand in desktop Blender 5.2.2 LTS on Windows. Date: 2026-10-12. Evidence: `reviews/rac-rmot05h-evidence/`, with SHA-256 sums in `SHA256SUMS.txt`.

## Gate lines

| Line | Status |
|---|---|
| Desktop Blender / direct-manual capability | **PASS** |
| Desktop verification | **PASS** |
| Final sculpt revision ID | **S2** (S1 failed re-entry) |
| Exporter | **PASS** (S1 and S2) |
| Preflight | **PASS** (S1 and S2) |
| 05F re-entry | **PASS** for S2 (S1 FAIL) |
| Replicated blind gate | **FAIL** (run1 PASS, run2 FAIL on G3) |
| Gorrund structural readability | **REJECT** |
| Grask E3 Stage C status | **NOT RUN** |
| Gorrund Stage C status | **NOT RUN** |
| Grask ↔ Gorrund combined Stage C | **NOT RUN** |
| RM-OT-05 | **OPEN** |
| Canon promotion | **NOT PERFORMED** |
| D4 | **NOT STARTED** |
| UE5 | **NOT STARTED** |

No acceptance threshold, guard, scorer prompt, tally rule or canon rule was changed. `f_reentry.py`, `f_blind.py`, `f_tally.py` and `f_scorer_prompt.md` were run unchanged and are byte-identical to `main`. Grask E3 was not touched.

## 1. Release / hash verification

- **Release zip:** `gorrund-sculpt-release-8b76d2eae245.zip` (the copy delivered in package v111) hashes to `287884f0da90df18cc9bd51e2291b8c602d88df0517fcfb8556513ce2f191bcd`, which matches `reviews/rac-rmot05g-release/`. Unpacked fresh, all 81 manifest files match `RELEASE_MANIFEST.json`.
- **Scripts:** the five Blender scripts match `blender/scripts/SHA256SUMS.txt` (`sha256sum -c` OK).
- **Frozen files:** the template, true floor, `regions.json`, `joints_r6.json` and the brief all match.
- **Working copy on the PC:** every tool, data and template file matches. 31 documentation images (figure PNGs and the evidence/tooling JPGs and PNGs) differ in bytes and size from the zip, so they were re-encoded at some point after extraction. No tool reads them, so they have no effect on the sculpt or on validation. The zip itself is intact.

## 2. Desktop verification (checklist §0, fixture ID DT)

- **Environment:** Blender 5.2.2 LTS on Windows.
- **Step 2, start state: PASS.**
  - Transforms locked at identity.
  - Masks on the head, hands and feet.
  - `GO_VIEW_ANATOMICAL` faces the viewer in Front view, with body left on the viewer's right.
- **Step 3, small stroke: PASS.**
- **Step 4: PASS.**
  - RAC_EXPORT PASS, output `4a8eafec…a545a`.
  - PREFLIGHT PASS.
- **Step 5: PASS.** Only family D moved (max 1.97 cm), and every NO_TOUCH max is 0.0.
- **Cleanup:** the DT outputs and `DESKTOP_CHECK_disposable.blend` are in `E:\…\sculpt\work_desktop_check\_to_delete\`. This session is not permitted to delete files, so the author deletes them. The report and preflight are in `desktop_check/`.

## 3. Sculpt revision history

### S1: the direct manual sculpt

All work was done in `GO_sculpt_S1_work.blend`, with backups 01–11 kept. Tools used:

- **Sculpt brushes:** Clay Strips, Draw and Layer in Subtract direction (the template winding points the normals inward), Scrape/Fill, Flatten, Inflate and Grab.
- **Edit-mode planes:** box selection, then Scale 0 about a typed 3D-cursor plane, with proportional editing.

What each family received:

| Family | Work | Max displacement |
|---|---|---|
| A | Flat sternal plate with a V-shaped top border, lateral planes, a straight anterior line, pectoral and navel relief reduced | 5.75 cm |
| B | Stepped, inclined posterior line, paraspinal columns, sacral border | 6.03 cm |
| C | Lateral thigh flattened, hip plate filled | 3.71 cm |
| D | Faceted shank with a tibial crest, knee flattened, malleolar mass | 3.45 cm |
| E | Front of the forearm flattened, wrist slightly broadened (light) | 3.13 cm |
| F | Deltoid flattened, clavicular region raised | 5.54 cm |

The export moved 3 189 vertices.

**Re-entry FAIL.** Ingest I1–I6 passed, but four guards failed in all four built states:

| Guard | S1 result | What caused it |
|---|---|---|
| `true_floor` | 10 vertices up to 0.31 cm inside after the build | Hip front, lateral knee and anterior ankle |
| `hand_foot_topology` | Hand/digit vertices moved up to 1.49 cm (limit < 1.0) | 46 thumb-base vertices carry finger weight above 0.5 but are not in `NO_TOUCH_hands_digits`; edit-mode plane operations moved them |
| `self_intersection` | 131 vs ≤ 77 allowed | The lateral planes at \|x\| = 24 met the hanging upper arm at z 155–169, plus the thumb-base fold |
| `arm_clearance` | 4 vertices per side inside the trunk section | Same lateral-plane contact |

The diagnostic scripts are in `diagnostics/`.

### S2: bounded manual correction on the same working sculpt

There was no new body and no procedural step. Corrections:

1. **Hand vertices.** The hand and hand-adjacent unassigned vertices were returned to the template with Blender's *Blend from Shape*:
   - selection: `NO_TOUCH_hands_digits` grown by 3 rings, with every FAM_A–F member removed;
   - source: a temporary shape key joined from `GO_SOURCE_REFERENCE`, removed afterwards.
2. **Lateral trunk planes.** The A/B vertices were moved inward to \|x\| 22.9 at z 155–169.5 and to 23.8 at z 149–155.
3. **Axilla.**
   - 42 unassigned axillary seam vertices were blended back to the reference.
   - The axillary A/B vertices were capped at \|x\| 22.0 for z 165.5–172.
4. **Floor margins.** The 10 floor-margin vertices were moved out 0.5 cm with Shrink/Fatten (proportional, 3 cm, connected).

Selections were made by vertex group, coordinate box or index from the Blender console. Every deformation is a standard Blender edit operator.

**Abandoned attempt.** A chest smoothing and partial-reference blend (WIP W3) fixed the low-composition chest fold but broke the reference, Narrow and Broad states. It was reverted through Undo History; the revert was confirmed bit-identical to the earlier state.

**Crash.** Blender crashed once while picking the blend-from-shape source in the redo panel. Nothing was lost, because the file had been saved at S1.

The S2 export moved 2 872 vertices. Backups 12 and 13 are on the PC.

## 4. Final artifact hashes

| Artifact | SHA-256 |
|---|---|
| `GO_sculpt_S1_r6.obj` | `64667338789ed5b40b7190b0b3c81094143c6473d5519d69352794d00433ccb5` |
| `GO_sculpt_S1_r6_export_report.json` | `c1d8621b…f2ce612` |
| `GO_sculpt_S1_work.blend` at S1 | `033fd520…dce8817` |
| `GO_sculpt_S2_r6.obj` | `5b9db47c802f75625d962470ac6bb38eb574ecc50d2bab08468b7193af5323af` |
| `GO_sculpt_S2_r6_export_report.json` | `f8f090cf…1033ef` |
| `GO_sculpt_S1_work.blend` at S2 | `8a5af838…b36474` |

- The working `.blend` (4.7 MB) and its backups are not committed. They stay at `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/sculpt/S1/`, with S2 outputs in `…/sculpt/S2/`.
- Manifests: `S1/GO_sculpt_S1_manifest.json` and `S2/GO_sculpt_S2_manifest.json`. Each includes the desktop_verification block.
- Every committed evidence file is listed in `rac-rmot05h-evidence/SHA256SUMS.txt`.

## 5. Required views

The 32 matched views for each revision are on the PC:

- base and low / Narrow / Broad previews;
- F/Q/P/RQ angles;
- grey and silhouette.

Committed copies:

- `S2/views/GO_SCULPT_BASE_*` (8 files, full size);
- contact sheets `S2/S2_views_{grey,sil}_sheet.jpg`;
- contact sheets `S1/S1_views_{grey,sil}_sheet.jpg`. Only 16 S1 views were pulled into this workspace, so the S1 sheets show a subset.

Preview console for S2:

| Preview | Inside the true floor (0.2 cm) | New ones caused by the sculpt | Max displacement |
|---|---|---|---|
| Low | 21 | 7 | 6.03 cm |
| Narrow | 0 | 0 | — |
| Broad | 0 | 0 | — |

The low-preview count is advisory.

## 6. Preflight evidence

- `S1/GO_sculpt_S1_preflight.txt`: PREFLIGHT PASS.
- `S2/GO_sculpt_S2_preflight.txt`: PREFLIGHT PASS. P1–P7 all pass, including P4 no-touch and P6 true floor.

## 7. Re-entry evidence for S2

Command: `python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_S2_r6.obj S2` → **RE-ENTRY PASS**. Files: `reentry/ingest_S2.json`, `reentry_S2.json`, `guard_S2.json` and `reentry_S2.log`. The S1 files are alongside.

- **Ingest:** I1–I6 all pass.
- **Guards:** every guard passes in GO5FS2, -LOW, N and B, including composition ordering and frame ordering.

| State | Piercing edges vs route | Min floor margin | Arm–trunk gap |
|---|---|---|---|
| Reference | 48 vs 67 | −0.17 cm | 1.14 cm |
| Low | 62 vs 78 | −0.13 cm | 1.19 cm |
| Narrow | 35 vs 57 | −0.19 cm | 1.28 cm |
| Broad | 35 vs 53 | −0.12 cm | 1.37 cm |

- **True floor:** 0 vertices inside 0.2 cm in every state.
- **Hand/digit change:** 0.52 cm (limit < 1.0).
- **Volume ratio vs route:** 1.0000004.
- **Reproduction of the delivered surface:** p90 0.29 cm, max 0.29 cm.

Retention (median / p10), reference state:

| Family | Median | p10 |
|---|---|---|
| A | 0.90 | 0.80 |
| B | 0.97 | 0.68 |
| C | 1.13 | 0.67 |
| D | 1.25 | 0.67 |
| E | 1.00 | 1.00 |
| F | 1.00 | 0.94 |

The low, Narrow and Broad states are similar; low-state p10 drops to 0.65–0.66 for B, C and D.

## 8. Blind-gate evidence for S2

- **Sheets:** `f_blind.py S2 run1` (set P) and `run2` (set Q). Each set has 12 bodies: 8 human controls, Grask E3 reference and low, and the S2 reference and low.
- **Scorers:** 3 fresh, uninformed scorers per run, given the `f_scorer_prompt.md` text verbatim and nothing else. They had no key, names, intent, prior results or indication of which body was which. The images were copied to neutral folders before scoring.
- **Files:** sheets, keys, the six scorer JSONs and `tally_S2.json` are in `blind/`.

| Line | Run 1 | Run 2 |
|---|---|---|
| G1 reference C | 3/3 ✔ | 2/3 ✔ |
| G2 low C | 3/3 ✔ | 2/3 ✔ |
| G3 stable ref+low group | 2/3 ✔ | **0/3 ✘** |
| G4 distinct from Grask | 3/3 ✔ | 3/3 ✔ |
| G5 organization basis | 3/3 ✔ | 2/3 ✔ |
| G6 axial + limb cues | 3/3 ✔ | 3/3 ✔ |
| G7 no control collapse | ✔ | ✔ |
| Run | PASS | **FAIL** |

**Gate: FAIL.** One run passing and the other failing is a fail under §14.

- **Posture read:** 0 posture reads for the sculpt.
- **Grask E3:** C 3/3 at both reference and low in both runs.

**Run-2 detail.**

- Every scorer grouped S2 reference and low together, but all three marked that group *unstable*.
- One scorer read the low composition as **B / fatness** ("large protruding belly and soft chest") and the reference as **B / bulk**.
- The other two called the low body "could be an obese human".

## 9. Stage C

**NOT RUN.** §16 requires both gates to pass, and the blind gate failed. Grask E3 stays frozen and was not modified.

## 10. Remaining failures and blockers

1. **Canon guardrail violation (structural readability REJECT).** The scorers who read S2 as non-human did so because of a "rectangular slab trunk", "flat front plate", "boxy", "slab-sided", "hard step at the hip". Author ruling Q1 forbids exactly this: the trunk is meant to be planar anatomical zones on a radiused, anatomically shaped section, never rectangular, boxy, slab-sided or cylindrical. S2 earns its C votes for a reason the canon rejects, so it is not a valid Gorrund even where G1 and G2 pass. The views confirm a boxy trunk, a lower-trunk overhang ("belt" ledge) at the hip, and a lumpy back.
2. **Low-composition obesity read (the G3 failure).**
   - At muscle 0 / weight 0.5 the sculpted trunk volume reads as soft fat.
   - The nipple and navel relief is still visible in the low preview.
   - The chest plate's top border crowds the pectoral vertices upward by about 2 cm (the source of the low-state chest fold); this was cleared only by the axilla change, not resolved.
3. **E and F lightly addressed.** Some left/right asymmetry remains: up to about 3 cm in E, from early one-sided strokes.
4. **Low preview advisory.** 7 vertices fall inside the true floor at low composition because of the sculpt.
5. **Tooling observations, not rule changes:**
   - The release's `NO_TOUCH_hands_digits` group omits vertices that the 05D guard counts as hand/digit (finger weight > 0.5). Exporter X9 and ingest I4 therefore pass edits that the build-side guard rejects.
   - Edit-mode X-mirror does not pair this template, because it is up to 1.16 cm asymmetric.

   For the author: should the release's protected group be widened to the guard's hand/digit mask?
6. **Next iteration (§15).** I did not start S3 in this pass because the failing family is the trunk section itself (A). Fixing it means re-sculpting the trunk from a radiused section rather than tuning toward the scorers. I recommend the author rule on whether S3 continues with me as sculptor in a fresh session that rebuilds family A from the S2 state (radius the corners, remove the plate step and hip ledge, keep B–F), with re-entry and both blind runs repeated from fresh scorers.

## 11. Confirmation

No acceptance threshold, guard, blind protocol, tally rule or canon rule was changed. No procedural Gorrund body was generated, and no remesh or new base mesh was used. Stopping at the RM-OT-05H author gate: no canon promotion, no RM-OT-05 closure, no D4, no UE5.

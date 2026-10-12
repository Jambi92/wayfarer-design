# RAC RM-OT-05G — sculptor release closure

**Order:** `reviews/chatgpt-rac-rm-ot-05g-handoff-acceptance-sculptor-release-order.md` (commit `feb3225`)

**Result:** the bounded corrections are applied and the self-contained sculptor release is built and verified from a clean copy. **STOP: EXTERNAL SCULPT REQUIRED — AWAITING ASSET.**

## 1. State

| Item | State |
|---|---|
| RM-OT-05 | **OPEN** |
| Grask E3 | Frozen as the accepted developmental direction pending Stage C |
| Gorrund | Unaccepted; **EXTERNAL SCULPT REQUIRED — AWAITING ASSET** |
| Stage C | **Blocked** |
| Other | No D4, no UE5, no canon promotion |

**Confirmations:**
- No new procedural Gorrund body was made. `arch_sculpt.py`, `race_base.py` and the 05C–05E drivers were not run.
- No canon, anatomy, brief text, validator threshold, scorer prompt or tally rule was changed.
- No Blender script changed, so the script hashes are unchanged.
- No sculptor was contacted and no cost was incurred.
- No external asset exists yet.

## 2. Corrections

1. **Protection claim (order §2).** `CHECKLIST_SCULPTOR.md` step 10 now carries the controlling wording verbatim: the operations are forbidden by contract; the exporter rejects *detectable* topology, identity, transform and protected-region violations and cannot determine every editing action; the asset must pass the full 05F re-entry and blind gates.
   - Added: the exporter writes base mesh data and ignores non-Multires modifiers, so an unapplied modifier visible in the viewport is not delivered; the exported base must express the forms; nothing is repaired, guessed or corrected procedurally.
   - The equivalent claims were corrected in `blender/README.md` §1 and in the 05G report §5. The report's original sentence is kept struck through, with the correction beside it.
   - All prohibited operations stay prohibited.
2. **Preview and UI limits (order §3).**
   - `CHECKLIST_SCULPTOR.md` step 16 and the `g_preview.py` row in `blender/README.md` now state that the preview shows transported forms before the authoritative floor clamp and volume restoration, is advisory, does not prove persistence and does not replace `f_reentry.py`.
   - The observed difference is kept: median 0.000 cm, up to 1.24 cm at clamped low-composition vertices.
   - A **first-session desktop verification** (checklist §0) was added:
     - confirm the editable base, identity transforms, masks and anatomical orientation;
     - make one small reversible stroke on a disposable file;
     - export as tooling ID `DT` and run the preflight;
     - check moved vs protected vertices;
     - delete everything.

     It is labelled a tooling fixture, never a candidate, and has a `desktop_verification` block in `MANIFEST_TEMPLATE.json`.
   - **Status: PENDING.** No interactive Blender session is available to Claude, so it is left for the sculptor. No UI test is claimed.

## 3. Self-contained release (order §4)

**What was added to `reviews/rac-rmot05f-handoff/`:**
- `brief/gorrund-rm-ot-05f-hand-sculpt-production-brief.md`: an exact frozen copy of the repository brief (same SHA-256).
- `START_HERE.md`, which covers:
  - the brief;
  - supported Blender;
  - the corrected checklist and the pending desktop verification;
  - sculpting the six families;
  - inspect, export and preflight;
  - what to return.

  It also explains that the brief's `reviews/rac-rmot05f-handoff/…` paths mean the package folder. No new anatomical targets.
- Relative links from the README, checklists and blender README now point inside the package. `figures/floor_margin.png` in the checklist was fixed to `../figures/…`.

**Repository originals.** The original brief is unchanged. The other changes are the pointers and corrections listed in §6.

**Packaging command** (`tools/rac/w1/rmot05g_blender/g_release.py`):
- `build`: refuses if the handoff folder has uncommitted changes; writes a deterministic zip plus `RELEASE_MANIFEST.json` (full SHA-256 and size of every file, required paths, frozen hashes).
- `verify ZIP`: extracts into an empty temporary folder outside the repository and checks the copy there.

**Build result:**

| | |
|---|---|
| Release id | `gorrund-sculpt-release-8b76d2eae245` |
| Source commit | `8b76d2eae245d2adce3f228a8a11f7b616b6b825` |
| Contents | 81 files + manifest; 9 571 289 bytes |
| Archive SHA-256 | **`287884f0da90df18cc9bd51e2291b8c602d88df0517fcfb8556513ce2f191bcd`** |

A second build gave the identical SHA-256. The archive is not committed (it duplicates committed files). Rebuild instructions and the manifest are in `reviews/rac-rmot05g-release/`. A copy is on the author's machine (§7).

**Clean-copy check** (`reviews/rac-rmot05g-release/RELEASE_VERIFY.json`): **COMPLETE.**
- All 81 files present with matching SHA-256, and no extra files.
- All required paths present.
- Frozen hashes match: template, true floor, regions, joints and the brief copy.
- `blender/scripts/SHA256SUMS.txt` matches.
- Every Markdown link and every package-internal back-ticked path in the 6 `.md` files resolves inside the copy:

  | File | Resolved |
  |---|---|
  | `README.md` | 21 |
  | `START_HERE.md` | 16 |
  | `blender/README.md` | 14 |
  | `blender/CHECKLIST_SCULPTOR.md` | 6 |
  | brief | 17 |

  Unresolved: 0. Repository-side references such as `tools/…f_reentry.py` are listed separately as receiver-side.
- The standalone preflight run from the copy with isolated Python, on the copy's own template: `PREFLIGHT PASS`, both with `--package` and with automatic package detection.

## 4. Hashes (full SHA-256)

| File | SHA-256 |
|---|---|
| `template/GO_ref_route_r6.obj` | `d0eb0d1643d135f3d5bd0920a9d6007f6dec8d1238530b30b298f3a1b2034eee` |
| `template/GO_true_floor_r6.obj` | `c6edbb98a8c4a93dd4c4cb0c615a29c5ba9133b4ce05aa7feef58d9190b288c2` |
| `data/regions.json` | `62833d43f79e7e1efeb9a64f4c8452a182db39b548392dfcc01da285be5b3ae2` |
| `data/joints_r6.json` | `f23a676c13b4b60da02e5a2f4ce6f543a9f4212def579494fc8f0faf524e0d1c` |
| Brief (repository original = package copy) | `22bedaa07ee3020996df3f608e6ec3470812953ae4d2f9d3fac5ece23c61db0c` |

Scripts (unchanged from 05G):

| Script | SHA-256 |
|---|---|
| `g_setup.py` | `b03261922fe1701b0fced21a067d34f746eb53e8f8fe1c9378710dbbbeb2b7e7` |
| `g_export.py` | `0dec4256095364269b1106170de25299d271b26d41a4458ccff575f23c0953e2` |
| `g_preview.py` | `5921117223ebe43ce7588e8c191a683057750beae0969032f64f45c537649925` |
| `g_views.py` | `f43526492218ec0c44594a8c1384f64a1b68b9431bb843d6617bb21f4e2371da` |
| `g_preflight.py` | `5add362c01d46cde35adbee35846b1b614b2d9420937304f13071ae035abd15f` |

## 5. Verification scope

These were documentation and packaging changes only, so no Blender or morphology tests were rerun. The 05G tooling evidence and its scope are preserved:
- headless `bpy` 4.2.0 and 5.0.1;
- desktop UI, the `blender` binary and real brush strokes unverified.

The new packager was exercised by two builds, which were identical, and by the clean-copy verification above.

## 6. Files changed

**Commit `8b76d2e`:**
- `reviews/rac-rmot05f-handoff/blender/CHECKLIST_SCULPTOR.md`: §0 desktop verification; step 10 wording; step 16 advisory note; brief and figure links.
- `reviews/rac-rmot05f-handoff/blender/README.md`: protection wording, preview advisory, brief link.
- `reviews/rac-rmot05f-handoff/blender/MANIFEST_TEMPLATE.json`: brief copy hash, release field, `desktop_verification`.
- `reviews/rac-rmot05f-handoff/README.md`: START_HERE and brief-copy pointers.
- `reviews/rac-rmot05f-handoff/START_HERE.md`: new.
- `reviews/rac-rmot05f-handoff/brief/gorrund-rm-ot-05f-hand-sculpt-production-brief.md`: new, exact copy.
- `reviews/claude-rac-rm-ot-05g-blender-sculpt-production-handoff-report.md`: §5 claim corrected.
- `tools/rac/w1/rmot05g_blender/g_release.py`: new.

**This closure commit:**
- `reviews/rac-rmot05g-release/`: README, `RELEASE_MANIFEST.json`, `RELEASE_VERIFY.json`, archive `.sha256`.
- This report.
- `specs/STATUS.md` and `reviews/claude-pass2-r5-reference-mesh-queue.md`: status / tracking.

## 7. Exact sculptor next action

1. Take `gorrund-sculpt-release-8b76d2eae245.zip` (SHA-256 `287884f0…191bcd`; also in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/sheets/racebodies_v111/`), or copy `reviews/rac-rmot05f-handoff/` at commit `8b76d2e`.
2. Open `rac-rmot05f-handoff/START_HERE.md`.
3. Complete the pending desktop verification (checklist §0).
4. Sculpt `GO_SCULPT_BASE` in Blender 4.2 LTS or 5.0 to the frozen brief.
5. Export `GO_sculpt_S1_r6.obj` with `g_export.py` and run the preflight.
6. Return the OBJ, export report, preflight output, views, the manifest (with the desktop-verification result) and the working `.blend` if available.

**On receipt:**
1. `python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_S1_r6.obj S1`, unchanged.
2. Only after all guards pass: the replicated blind gate (`f_blind.py`, `f_scorer_prompt.md`, `f_tally.py`).
3. Only after both gates pass: the authorized combined Stage C.

This release does not close RM-OT-05.

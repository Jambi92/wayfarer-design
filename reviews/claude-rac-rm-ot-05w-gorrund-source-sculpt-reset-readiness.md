# RAC RM-OT-05W — Gorrund source-sculpt reset: readiness

**Order:** `reviews/chatgpt-rac-rm-ot-05w-gorrund-source-sculpt-reset-order.md` (author-accepted reset, October 14, 2026).

**Date:** 2026-10-14.

**Package:** `reviews/rac-rmot05w-source-brief/`.

**Drivers (new, additive):** `tools/rac/w1/rmot05w_drivers/`.

## Outcome

**NEW NEUTRAL SOURCE SCULPT REQUIRED / SOURCE SELECTION — the package is ready to use.**

Two things remain, and both are Tyler's:
1. **A neutral concept image.** This session has no image generator, so the image comes from Tyler's image generator using the prompt in `SUBMISSION_PACKAGE.md` §1.
2. **Explicit approval, immediately beforehand, of one Rodin Gen-2.5-High submission:**
   - AssetName `Gorrund-Neutral`;
   - estimated about 0.5 credits;
   - run in Tyler's PowerShell, because this session cannot use `RODIN_API_KEY` and cannot run commands on the PC.

What has not happened:
- No source was produced.
- No credits were spent.
- No one was contacted.
- No repair work was started.

Status:
- Gorrund is **UNACCEPTED**.
- RM-OT-05 is **OPEN**.
- Stage C is **BLOCKED**.
- No canon change.
- D4, UE5, production rigging and the creator are **NOT STARTED**.

## 1. Salvage route ended (§1)

- **GO-ARM-N1** (`817f2cf1…`) and its **N1R6** derivative are **retired from advancement**.
- They are kept unchanged as historical / source-artifact evidence, along with:
  - their evidence (`reviews/rac-rmot05v-evidence/`);
  - the 05V package on E:;
  - the whole U-series lineage, including U8 cp1 `2341d554…` and `base.glb` `78ecfa87…`.
- The U8 axillary repair stays a successful **local** repair. It is not evidence that the U8 body is suitable.
- Nothing was run on N1 or U8:
  - no N2;
  - no neutralization, smoothing, muscularity reduction, field rebuild, solver or warp;
  - no scaffold.
- The supersession is recorded with a date in `reviews/claude-rac-rm-ot-05w-supersession-note.md`. History is not rewritten.

## 2. The Saurin lesson, as recorded (§2)

**What failed: code-built and SDF anatomy.**
- TS9 was "built on the TS8 signed-distance (code-built) construction" (`reviews/claude-saurin-ts9-reference-anatomy-pass.md` L26). Its fidelity was "**Not matched.** This is the ceiling of the code-built method" (L73).
- The post-Rodin procedural Phase A was rejected: "The failure was methodological … discarded the sculptural/anatomical quality already present in the Rodin source" (`reviews/saurin-rodin-geometry-adoption-directive.md` L12).

**What worked: a real external sculpt as the foundation.**
- "Use the strongest actual Rodin full-body geometry as the sculptural foundation" (same directive, L18).
- The primary body was Rodin component `c12`, with region-by-region PRESERVE / MODIFY / REBUILD / REPLACE marks (`reviews/claude-saurin-rodin-source-adoption-sheet.md` L28). Nothing from the procedural Phase A was reused.
- After that came surgical correction "not reinterpretation or wholesale reconstruction" (`reviews/saurin-rodin-controlled-surgical-edit-directive.md` L24), and then acceptance.

**Gorrund confirms the same lesson:**
- SDF and primitive clay is "INSUFFICIENT FOR FINAL SOURCE ANATOMY" (05M order L24).
- 05L's free SDF sculpt read as a "smooth stylized mannequin".
- The 05V reconstruction was blind-read as a "massive hunched brute".

**What the record does not show:** that Blender as an application was the problem. A real sculpt in Blender would be acceptable. A procedural body saved as `.blend` is not a sculpt.

**Where the recovered source fell short:** `base.glb` was a Rodin source, but it was a multi-figure library with fused garments, a mane, paw-like feet and bodybuilder bulk (`reviews/rac-rmot05m-evidence/source_glb/SOURCE_RECORD.md` L19; 05Q L21: no skin under garments). It had the right method but the wrong source content.

## 3. Source brief (§3)

All files are in `reviews/rac-rmot05w-source-brief/`.

| File | Content |
|---|---|
| `SOURCE_BRIEF.md` | Locked anatomy with exact `GORRUND_V1` / `REFERENCE_ANATOMY_V1` line citations; OPEN morphology and builder choices kept separate; required presentation (§3 of the order); views; matched-height contrasts with Marchfolk, Skarn and Grask. No new numeric targets. |
| `NEGATIVE_CHECKLIST.md` | 30 reject conditions in six groups: presentation, stereotypes, shape, surface, wrong identity channel, process. Each is tied to canon and to the earlier candidate that failed that way. |
| `NEGATIVE_REFERENCES_avoid_only.jpg` | Labelled **avoid-only** exhibit: U8 cp1, GO-ARM-N1, 05C code-built bodies. Not a target, donor or starting point. |
| `REVIEW_SPEC.md` | The whole-body / body-only source gate (four questions, §5), and the conditions for a later blind gate. |
| `LOW_PREREGISTRATION.md` | Draft method for the validation-only LOW derivative (§6). |
| `SUBMISSION_PACKAGE.md` | Route A (concept → Rodin), Route B (sculptor commission brief) and the exclusions. |
| `blind-protocol/` | Tail-fragment fix evidence and the clean frozen control set. |

How the brief settles the main conflicts:
- **Mane and hair:** the leonine head keeps short fur and no mane. Canon requires no mane (GO L389), and R-8 forbids hair over landmarks.
- **Modesty:** the image prompt uses minimal low-rise briefs below the iliac crest / ASIS. Image generators generally refuse full nudity. The brief allows a proxy only if it covers no landmark (RA R-7).
- **Sex:** no sex-specific biology is specified (RA §4).

## 4. Route readiness (§4): checked, bounded

| Capability | Finding |
|---|---|
| Rodin pipeline | **Present and reachable for inspection.** `C:\Users\Tyler\Wayfarer-Rodin` (rules in `CLAUDE.md`, `Scripts\wayfarer-rodin.ps1`, regression tests) and `E:\Wayfarer-Rodin` are connected folders. Read-only listing on 2026-10-14: `Jobs\` holds only Vael records; `Source-Masters\` holds only Vael-Male and Vael-Female. There is no duplicate guard for `Gorrund-Neutral`. |
| Tier / input | Gen-2.5-High (fixed production tier); one image per submission. |
| Cost | About **0.5 credits** per submission, from the Vael-Female job record (`"consumed": 0.5`). This is an estimate; the credit balance is not visible. |
| Authorization | **None for this generation.** 05M allowed generation only "if … actually accessible" (L162) and named no spend. 05N said "Do not spend Rodin credits" (L27). 05W §4 says to proceed only within existing explicit authorization. The pipeline rule needs Tyler's explicit approval **immediately before each `-Submit`**. |
| Execution from this session | Not possible, and not attempted. `RODIN_API_KEY` is a Windows User environment variable on the PC and is not available to this container. The device link offers file access only, with no shell on the PC. Dry run and submit are Tyler's PowerShell commands, written out exactly in `SUBMISSION_PACKAGE.md` §2. |
| 2D concept generation | **Not available in this session**: no image-generation tool, and no image tooling in the repo. The concept prompt is ready for Tyler's own generator; the earlier Gorrund and Wayfarer images came from Tyler's ChatGPT workflow. No concept image is claimed. |
| Existing neutral sources | **None suitable.** Following §4, I used the known inventory instead of re-searching the drives. The only Gorrund source is the garment-fused `base.glb`. The Vael and Saurin masters are other races. The MPFB / solver bodies are code-built and excluded. |
| Human sculptor | Brief ready (Route B). Not contacted. |
| Sculpt by Claude | Not credible for a whole organism (05U showed remote desktop sculpting suits local repairs only). A procedural body is excluded (§2). |

**Recommended route:** Route A. It is the closest match to what actually worked for Saurin, the pipeline already exists, and the cost is small and known.

**Next concrete action (Tyler):**
1. Generate the concept image from `SUBMISSION_PACKAGE.md` §1.
2. Save it as `Source-Images\Wayfarer Gorrund Neutral Character Reference Sheet.png`.
3. Optionally have Claude review it against the checklist.
4. Run the dry run.
5. If you approve the spend, run the single `-Submit`.

## 5. Whole-body source gate before repair (§5)

`REVIEW_SPEC.md` §1–2 sets out:
- what is submitted: whole organism and body only, F / P / B / 3/4, with a matched-height exhibit and provenance;
- the four questions;
- the three outcomes: accept as source, revise at source, or reject.

No cleanup, metric validation or scaffold work starts before that review.

## 6. Validation deadlock and blind protocol (§6)

**Validation-only LOW.** The method is pre-registered as a draft (`LOW_PREREGISTRATION.md`). It holds the same individual, skeleton and pose; only the muscle soft-tissue layer changes. Builder choices are declared. If no credible LOW can be made, that is reported as a capability dependency. It is not a scaffold, creator asset or canonical variant.

**Tail-fragment contamination is fixed mechanically.** The new `w_tile_check.py` requires each body tile to be one connected silhouette and blocks the sheet otherwise.
- Run on the 05V candidate profile tile, it **fails**: islands of 56,241 px and 1,701 px, the fragment all six 05V scorers mentioned (`blind-protocol/tile_check_05V_candidate.json`).
- On the complete frozen control set it **passes 20/20** (`tile_check_controls.json`).
- The clean control set is shown labelled in `blind-protocol/control_set_labelled.jpg`. Its 20 tiles are copied into the package so the protocol no longer depends on one session's scratch renders.

**New confound flagged for the next pre-registration.** The frozen controls are smooth MPFB-derived bodies, and a sculpted source will carry real surface detail. A scorer could then pick out the candidate by rendering style. The next gate must state how this is handled, without smoothing away structural anatomy (`REVIEW_SPEC.md` §3).

**No fresh scoring was run.** There is no new candidate yet, and rerunning the known-invalid protocol is excluded (§6).

## 7. Records

- **Status lines:** `specs/STATUS.md` and `reviews/claude-pass2-r5-reference-mesh-queue.md` retire N1/N1R6 from advancement and record **NEW NEUTRAL SOURCE SCULPT REQUIRED / SOURCE SELECTION**.
- **Supersession:** `reviews/claude-rac-rm-ot-05w-supersession-note.md` covers the 05V source-body freeze and the validation-only LOW clarification.
- **Canon:** `GORRUND_V1` gets a status note only. No relation, number or distribution changes.
- **Unchanged:** accepted Saurin, Grask E3 and all prior assets.

Gorrund **UNACCEPTED**; RM-OT-05 **OPEN**; Stage C **BLOCKED**; canon promotion **NOT PERFORMED**; D4 / UE5 / production rigging / creator **NOT STARTED**.

**NEW NEUTRAL SOURCE SCULPT REQUIRED / SOURCE SELECTION — remaining dependencies:**
1. A neutral concept image from Tyler's image generator.
2. Tyler's explicit approval of one Rodin Gen-2.5-High `-Submit` (`Gorrund-Neutral`, about 0.5 credits).

# RAC RM-OT-05M: Gorrund Rodin source recovery and surgical sculpt (gate)

**Order:** `reviews/chatgpt-rac-rm-ot-05m-gorrund-rodin-source-surgical-order.md` (f87b865)
**Author:** Claude
**Date:** 2026-10-12
**Evidence:** `reviews/rac-rmot05m-evidence/`

## Gate lines

| Line | Status |
|---|---|
| Prior male Gorrund source found | **NO** |
| Source provenance verified | **YES**. Every Gorrund-named body is MPFB-parametric, and none is Rodin / Hyper3D (§1) |
| Fresh external source generated | **BLOCKED** (§2) |
| Final source used | **NONE** |
| Final surgical reference | **NONE** |
| Reference internal gate | **NOT RUN** (no source) |
| LOW companion | **NOT CREATED** |
| REF↔LOW consistency | **NOT RUN** |
| Concept blind gate | **NOT RUN** |
| Blind-reason canon audit | **NOT RUN** |
| Gorrund body-only readability | **REJECT** (unchanged; no new body) |
| Measurement scaffold | **NOT DERIVED** |
| Canon reconciliation | **NOT RUN** |
| RM-OT-05 | **OPEN** |
| Stage C | **BLOCKED** |
| Canon promotion | **NOT PERFORMED** |
| D4 | **NOT STARTED** |
| UE5 | **NOT STARTED** |

I stopped under §6 / §29: no usable prior source exists, and Rodin generation cannot be run from this session. I am handing over the source-generation package. Per §29 I did not fall back to SDF primitives, a donor morph, the old skeleton cage or a parametric generator.

## 1. Source-recovery manifest (§3, §4)

Full record: `source_recovery_manifest.json`. The search was read-only; nothing was moved, renamed or changed.

**Searched:**
- `E:\Wayfarer-Rodin` and `C:\Users\Tyler\Wayfarer-Rodin`, including all job records;
- all of `E:\UnrealProjects`, including `RaceBodies\out`, `candidates`, `rodin_analysis`, `sculpt` and `ImportPacks`;
- Downloads, both Desktops and OneDrive Documents;
- `Documents` and `3D Objects` (Tyler granted access for this search);
- `E:\Tools`.

**Results:**

1. **Rodin / Hyper3D assets on the PC:** only `Vael-Male.glb`, `Vael-Female.glb` and the Saurin reference GLB.
   - The Rodin job folder holds Vael jobs only.
   - `Source-Images\` is empty.
   - **There is no Gorrund Rodin job, image or GLB anywhere reachable.**
2. **Gorrund-named bodies:** `RaceBodies\out\Gorrund_Masc` and `GorrundSculpt_Masc` (`.blend` + `.fbx`), with hashes in the manifest.
   - Both are 19,158-vertex MPFB parametric human bases from `wf_build_races.py`. This is the same topology as the Marchfolk donor.
   - Their hair / garment helper proxies are baked in (sheet `source_candidates_MPFB_rejected.jpg`).
   - They are not Rodin bodies. §3 forbids human / parametric donors, so they are **rejected** as a source.
3. **Checked, not relevant:**
   - a 401 MB `.tmp` in Downloads, which is a partial Blender 5.0.1 zip download;
   - the creature concept review pack, which holds creature concepts, no race bodies;
   - Paragon animation FBX and PolyHaven props.

The "completed male Gorrund GLB" in the project history could not be found on any reachable location. It may exist outside the connected folders, for example in a browser-only Hyper3D account download history or on another machine. If Tyler can find it, dropping it in `E:\Wayfarer-Rodin\Source-Masters\Gorrund-Male\` (or anywhere reachable) restarts this order at §5 with no new generation.

## 2. Why generation is BLOCKED (§6)

The production pipeline is `C:\Users\Tyler\Wayfarer-Rodin\Scripts\wayfarer-rodin.ps1`, using Hyper3D Rodin Gen-2.5-High with an image input. It needs:
- a Gorrund source image, and none exists;
- `RODIN_API_KEY`, a Windows user environment variable on Tyler's PC that this session cannot use;
- PowerShell on the PC, which this session cannot run (no device shell; terminals are click-only);
- per the pipeline's own rules, **Tyler's explicit approval immediately before each paid `-Submit`**.

## 3. Source-generation package (§6)

`rac-rmot05m-evidence/Gorrund_Source_Generation_Package.md` contains:

1. **Input-image rules.** One single full-body figure; no turnaround sheet, because the Vael sheet produced an unusable relief slab. Front-3/4, relaxed A-pose with limbs clear of the trunk, plain grey background, briefs only, cropped hair, matte neutral skin, feet fully visible.
2. **A ready-to-paste image prompt and negative prompt.** These come from GORRUND_V1 and the 05-series findings. The key points: massive load-bearing skeletal architecture rather than muscle or fat; broad and deep radiused rib cage; girdle carried by the thorax; deep pelvis with a flat sacral area; large integrated joints; large plantigrade feet; lean neutral tissue; realistic clay-sculpture style.
3. **Body-only priorities by region.**
4. **The formal Gorrund negative-reference set (§9).** Use it to judge the image before spending Rodin credits.
5. **Exact pipeline steps.** File name `Wayfarer Gorrund Male Character Reference Sheet.png` with AssetName `Gorrund-Male`, then a dry run, then an approved `-Submit`. The output goes to `Source-Masters\Gorrund-Male\Gorrund-Male.glb`, which is immutable. Then "check for latest instructions".

Once the GLB exists, I resume at §5 (suitability gate) on a working copy:
- GO-RD1-SOURCE stays untouched;
- RD1 surgical sculpt in Blender;
- internal gate;
- LOW;
- REF↔LOW audit;
- replicated concept blind gate;
- scaffold;
- reconciliation.

## 4. Unresolved dependencies

- **D-SRC-1:** a Gorrund source image and an approved Rodin submission (Tyler).
- **D-SRC-2 (optional):** whether to let the pipeline send several single-view images per asset, which Rodin supports. That is a pipeline change needing Tyler's agreement under the pipeline rules. It is not required for the default route.
- **Carried forward:** the old-route skin pelvic-depth diagnostic (05K) is still unruled until an RD body exists (§25).

## 5. Confirmation

- No Gorrund geometry was produced or changed in this block.
- Old 05A–05L evidence is untouched.
- The Rodin source masters and job records were read only.
- No validator, threshold, prompt, tally rule or canon rule changed.
- Grask E3 is frozen.

I stopped at the RM-OT-05M author gate.

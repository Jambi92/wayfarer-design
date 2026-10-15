# RAC RM-OT-05X R1 — review of Tyler's revised Gorrund GLB `base_1.glb` (no repair)

**Authority:** Tyler attached `base_1.glb` on 2026-10-15 as "the new Gorrund file". No new order arrived. This review applies the RM-OT-05X order unchanged (`reviews/chatgpt-rac-rm-ot-05x-new-male-gorrund-source-review-order.md`: untouched review, no repair, stop after review) to the revised candidate.

- **Evidence:** `reviews/rac-rmot05x-r1-source-review/`.
- **Earlier candidate:** `reviews/claude-rac-rm-ot-05x-new-male-gorrund-source-review.md`.

> **Superseded by RM-OT-05Y (2026-10-15).** `reviews/chatgpt-rac-rm-ot-05y-revised-male-source-review-order.md` arrived after this review was written. Its §2 single-body gate fails, because the file holds three figures. Its outcome is **REVISE GENERATION INPUT** (`reviews/claude-rac-rm-ot-05y-revised-male-source-review.md`).
> - The suggestion below to adopt fig2 is **withdrawn**: 05Y §2 forbids extracting the most attractive figure.
> - The per-figure observations remain as non-gate context only.

## Recommendation

**Still REVISE AT SOURCE, but the direction is improving.**

What the revision fixed, compared with the 05X `Gorrund.glb`:
- shorts became low-rise briefs;
- the chin tuft is gone;
- heel contact is better.

What it did not fix:
- **Composition.** The body is still a fully defined bodybuilder, and the body-only views still read as a muscular human.
- **Briefs and tail root.** The briefs are still **fused** (no skin beneath), and the **tail still roots on the briefs**, now off the midline over the right buttock.

Making it compliant would still need whole-body muscle work plus a buttock / sacral reconstruction with tail re-rooting. Those are broad changes, not bounded corrections.

**Format change.** The file now holds **three separate full 3D figures** (front-, side- and back-facing), like the Saurin Rodin library. If the next revision keeps that format, **fig2** (the front-facing figure) is the best one to adopt: lowest genus and no self-intersections.

Nothing was edited. Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**; D4 / UE5 / production rigging / creator **NOT STARTED**.

## 1. Intake

| Item | Value |
|---|---|
| File / size / SHA-256 | `base_1.glb` / **31,543,564 bytes** / **`b0214fcfcf157da9b8e457a110fcb78ea5ae88ec14f8a53aea159efabb5d5973`** |
| Container | glTF 2.0, Blender glTF I/O v4.3.47 export. One node `model` (identity transform), one mesh, one primitive (POSITION, NORMAL, TEXCOORD_0), one grey material. No textures, rig or animation. |
| Provenance | **Unknown.** No job record in the PC Rodin pipeline. |
| Master | Read-only in the session; copy placed at `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Male-05X-R1\base_1.glb`. Kept separate from `Gorrund.glb` (05X), `base.glb`, U8 and N1. The working-copy hash is unchanged after review. |

## 2. What the file contains (`views/00_*`, `geometry/inspection.json`, `geometry/figures_split.json`)

The file holds 1,000,000 triangles. After welding, 610,698 exported vertices reduce to 499,982 positions. There are **3 connected components**, each a separate full-body 3D figure. All three:
- are closed, with 0 boundary edges and 0 non-manifold edges;
- have consistent orientation;
- have the same raw height of about 128.2–128.9 units ×100.

| Figure | In the file | Faces | Genus | Self-intersections |
|---|---|---|---|---|
| fig0 | right, facing back | 356,822 | 5 | 0 |
| fig1 | centre, facing −X (side) | 326,006 | 5 | **4 faces, at a toe** |
| **fig2** | left, facing front | 317,172 | **2** | **0** |

- **Triangle quality** (whole file): median minimum angle 35°; 18,111 faces below 10°, 66 below 1°; no zero-area faces.
- **Handle locations** were not established for this file. In 05X the two handles were at the axillae.
- **Display copies:** each figure was shown in canonical views using a **rigid display transform only** (translation plus yaw snapped to 90°, recorded in `figures_split.json`). The source was not changed.

The three figures look like the same design seen from three directions. **fig2** is reviewed in detail below as the cleanest one.

## 3. fig2 views and findings (`views/01`–`10`)

All renders use Blender Workbench: neutral grey, orthographic, matched framing, grid in raw units (not stature).

**Body-only.** The diagnostic copy (`x_tailtrack.py`, `geometry/bodyonly_diagnostic_fig2.json`) hides the head above the neck minimum (raw z 109.3) and the tube-tracked tail (16,045 faces).
- It only deletes faces on a disposable copy.
- The open hole it leaves at the tail root is shown deliberately.
- All six body-only tiles are clean single silhouettes (`geometry/tile_check_bodyonly.json`).

| Point | Finding |
|---|---|
| Head | Leonine, lioness-like. Rounded broad ears, no mane, **no chin tuft** (fixed from 05X). Upright carriage. |
| Composition | **Unchanged from 05X: extreme bodybuilder definition.** Striated pectorals and deltoids, six-pack, serratus, vascular forearms, high trapezius. The body-only views (`02`, `10`) read as a very muscular human. Massiveness comes from current muscularity, not visibly from the frame. |
| Briefs | Low-rise briefs replace the shorts. They are **fused**: each figure is one closed surface with no second surface, so **no skin is modelled beneath**. The waistband sits at roughly the ASIS / iliac-crest level, below the navel. The briefs cover the pubic and inguinal region, the whole buttocks, the gluteal folds and the sacrum. Less is covered than with the 05X shorts: the thighs are now exposed. |
| Tail | Roots **on the briefs**, just below the waistband over the **right buttock** (raw x ≈ −7, off the midline). It runs down against the buttock and back of the thigh, then sweeps outward, with its lowest point near the ankle. No ground contact. Tracking shows the tail lying on the buttock surface down to about raw z 66 (≈ 0.51 of height). |
| Pose | Upright; knees extended; arms hanging with small abduction; hands loosely curled near the thighs. Feet parallel, about hip width. |
| Heel contact | Much better than 05X. The heel pad sits about **0.5–0.6 raw cm** above the lowest sole point, rising to about 1.1 at the very edge of the −X heel (≈ 0.4 % of height; 05X was ≈ 0.9 %). |
| Feet | Plantigrade, **five toes per foot with nails**, humanoid, no claws. Foot length ≈ 25 raw cm ≈ **19.6 % of height**: large but not monstrous, in line with GO L236. |
| Hands | Five digits with a thumb and nails. Humanoid, no claws (`08`). |
| Raw height | Midline skull vertex 127.6, ear top 128.6 (units ×100). **Not a stature.** Scale is unit-normalized, as is typical of generated meshes; no scaling applied. |

## 4. Source gate (05W REVIEW_SPEC Q1–Q4) for fig2

| Q | Answer | Basis |
|---|---|---|
| Q1 Gorrund structural identity at reference composition | **No.** Composition is far from reference (RA R-4); identity is carried by muscle (GO L21–23, L83, L250). | `02`, `04`, `10` |
| Q2 Distinct from bodybuilder / enlarged human / Skarn with head, tail and presentation hidden | **No.** Reads as a bodybuilder human (checklist B1, B3, E2). **Yes** against Grask and against ogre caricature. | `02`, `10` |
| Q3 Neutral pose, feet, visible landmarks, continuity | **Partly, and better than 05X.** Pose, feet, hands and heel contact are good, and the chin tuft is gone. **But the fused briefs still hide the pubic, inguinal, gluteal and sacral landmarks, and the tail roots on the garment** (A1, E3). | `05`, `07`–`09` |
| Q4 Later work can stay local | **No.** Whole-body composition change, plus buttock / sacral reconstruction and tail re-rooting. | `02`, `05` |

**Kept separate:**
- **Visual / direction:** positive, and improving.
- **Bounded-correction source:** not yet.
- **Final neutral reference:** no (R-4, R-7, R-11 tail-root placement).

## 5. Proposed next step

Revise once more at source, keeping everything that improved:
- head;
- tail shape;
- stance;
- heels;
- feet and hands;
- no chin tuft;
- the three-figure library format is fine; fig2-style.

Change only:

1. **Composition.** Ordinary healthy muscle and fat, with no striation, six-pack, vascularity or bodybuilder trapezius. This is the main remaining blocker. Size should come from:
   - a deep ribcage;
   - a broad girdle sitting on the thorax;
   - a deep pelvis;
   - substantial joints.
2. **No briefs**, or a modesty proxy only if unavoidable. Either way, the **tail must root on the body at the sacral midline**, not on a garment.
3. Keep the tail clear of the buttock and thigh for the first few centimetres, so it reads as attached and can be separated cleanly for review.

**One question for Tyler:** which tool produced `base_1.glb`, and is it the same one that made `Gorrund.glb`? The answer decides how the revision is requested. No paid generation is implied.

**STOP.** No repair, LOW, blind scoring, canon measurements, scaffold, ARM acceptance or Stage C.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

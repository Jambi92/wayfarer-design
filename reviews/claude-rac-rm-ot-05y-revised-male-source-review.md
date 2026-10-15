# RAC RM-OT-05Y — revised male Gorrund source: single-body gate

**Order:** `reviews/chatgpt-rac-rm-ot-05y-revised-male-source-review-order.md`.
**Date:** 2026-10-15.
**Evidence:** `reviews/rac-rmot05y-source-review/`.

## Outcome

**REVISE GENERATION INPUT.**

The revised file is **not one organism**. It holds **three separate, complete, volumetric full-body figures**: one facing front, one facing the side, one facing back. They sit side by side, the way a reference-sheet / turnaround input is rebuilt as a 3D "library". This fails the mandatory single-body gate (§2), so the review stops here.

As §2 requires, I did not do any of the following:
- pick out the most attractive figure;
- merge the views;
- inflate, repair or edit anything;
- run the whole-source anatomy review.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**; canon advancement **NOT PERFORMED**; D4 / UE5 / production rigging / creator **NOT STARTED**.

## 1. Intake (§1)

| Item | Value |
|---|---|
| Attachment | Arrived as `/mnt/user-data/uploads/base_1.glb`; Tyler's name for it is `base.glb`. Identified **by hash**: **31,543,564 bytes**, SHA-256 **`b0214fcfcf157da9b8e457a110fcb78ea5ae88ec14f8a53aea159efabb5d5973`**. This matches the order. |
| Distinct from | the old `base.glb` (`78ecfa87…`) and the 05X `Gorrund.glb` (`1c23b92b…`). |
| Container | glTF 2.0 with matching declared length. One node `model` with no transform or extension; one mesh; one triangle primitive (POSITION, NORMAL, TEXCOORD_0); one material. No textures, images, skins or animations. 610,698 exported vertices, 3,000,000 indices (1,000,000 triangles). Exporter: Khronos glTF Blender I/O v4.3.47. |
| POSITION bounds | X −0.947674..0.949007; Y 0..1.288981; Z −0.292843..0.290285. Matches the order. |
| Master | Immutable copy at `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Male-05X-R1\` (stored as `base_1.glb.part000` + `.part001` with `REJOIN.txt`, because the file is over the 30 MB transfer limit; the rejoined file must hash to `b0214fcf…`). This is a revision-specific folder; no older master was overwritten. The review used a separate working copy, whose hash was unchanged afterwards. |
| Designation | Male, as Tyler designates it. Nothing is added to canon. |

## 2. Single-body gate (§2)

Evidence:
- `views/00_file_overview_three_figures.jpg`: the untouched file from front and back;
- `views/00c_file_top_view_volume.jpg`: the file from above;
- `geometry/inspection.json`;
- `geometry/figures_split.json`.

| Check | Finding |
|---|---|
| Seam duplicates vs real parts | After exact-position welding, the 610,698 exported vertices become 499,982. The 110,716 removed vertices are UV / normal seam duplicates. |
| Connected components | **3**, each a full figure. No other loose pieces. |
| Figure layout in the file | One figure on each side and one in the centre along X. All stand on the same ground plane, each about 1.28–1.29 raw units tall. The side-by-side layout is what makes the bounds about 1.9 wide. |
| What each figure is | **fig2** (−X side): faces the front. **fig1** (centre): faces −X, a side view. **fig0** (+X side): faces the back. The figures look like the same design posed for three views. |
| Volume, not relief | Each component is a **closed volume**: 0 boundary edges, 0 non-manifold edges, consistent orientation. Each has real front-to-back depth of about 0.40–0.58 raw units including the tail, against 1.28 of height, as the top view confirms. They are **not** flattened reliefs or view-fused shells. |
| Per figure | fig0: 356,822 faces, genus 5, 0 self-intersections. fig1: 326,006 faces, genus 5, **4 self-intersecting faces at a toe**. fig2: 317,172 faces, genus 2, 0 self-intersections. |
| Orientation / pose | Y-up, ground at Y 0, front toward +Z, as for 05X. The bounds come from **multiple figures**, not from an unusual orientation or pose. |

**Verdict:** this is the "multiple front / side / back figures generated from a reference sheet" case (§2, second bullet). It is **not one organism**. The gate fails, so per §2 I **STOP**.

## 3. Disclosure: work done before this order arrived

Before 05Y reached the repository, I had already reviewed this file under the 05X order (`reviews/claude-rac-rm-ot-05x-r1-revised-gorrund-source-review.md`, evidence `reviews/rac-rmot05x-r1-source-review/`). That review:
- split the figures into rigid **display** copies (nothing written to the source);
- examined fig2 in detail;
- suggested that fig2 would be the one to adopt.

**Under 05Y §2 that suggestion is withdrawn.** No figure is extracted or adopted as a source. The R1 report now carries a dated note saying 05Y supersedes it.

Its observations are kept only as **non-gate context** for the next generation input:
- muscle definition still reads as a bodybuilder;
- the briefs are fused into the surface, with no separate geometry and no skin beneath;
- the tail roots on the briefs, off the midline;
- the chin tuft is gone and heel contact is better.

## 4. Recommendation: one focused generation-input correction

**Submit ONE single full-body figure image, not a front / side / back sheet.**

- **Input format.** One figure in one image: front three-quarter (about 30°), the whole body including both feet in frame, plain mid-grey background, even light, no other views, panels or text. This is the 05M / 05W lesson (`reviews/rac-rmot05w-source-brief/SUBMISSION_PACKAGE.md` §1). A turnaround collage must **not** be treated as a multi-view input.
- **Multi-view.** Separately uploaded front / side / back images may be used **only if** the generating service explicitly supports a multi-image input mode. That is not presumed here. The PC Rodin pipeline sends one image, and the tool that made `base_1.glb` is unknown.
- **Content, in the same image.** Keep the preferred leonine head, the tail, the upright stance with heels down, the five-toed feet and the hands. Change:
  - muscle to ordinary reference composition, with no striation, six-pack, vascularity or bodybuilder trapezius;
  - no briefs (or a minimal proxy only if unavoidable);
  - the **tail rooted on the body at the sacral midline**, clear of the buttock for its first few centimetres.

**Metadata that would help:** which tool produced `base_1.glb`, and whether it was given the front / side / back sheet. That would confirm why three figures came back. No paid generation or submission is authorized or implied.

**STOP.** No sculpt, smoothing, remesh, garment removal, hidden-skin reconstruction, LOW, rigging, blind scoring, scaffold or canon measurements.

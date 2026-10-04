# Saurin Anatomical Convergence: Orbit, Tail Taper, Structural Scale Hierarchy (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-anatomical-convergence-order.md` (6a9a0af)
**Base:** the final "Grown, Not Assembled" cleanup (3a05513).
**Scope:** authorized zones only (orbital/postorbital, free tail, structural scale order, swept-back display base, forearm seam). No UE5.

**Images** are in `reviews/images/saurin-convergence/`. All use neutral material and identical cameras unless the sheet says otherwise.

| # | Required item | File |
|---|---|---|
| 1 | Whole organism, five cameras | `v15_01_whole_organism.jpg` |
| 2 | Orbital before/after: front, profile, front 3/4, rear 3/4, top, two close-ups | `v15_02_orbital.jpg` |
| 3 | Orbital plane/curvature diagnostic (base mesh, no scales) | `v15_03_orbital_curvature.jpg` |
| 4 | Tail before/after: profile, top, rear 3/4 | `v15_04_tail.jpg` |
| 5 | Normalized cross-section/taper comparison (graphs and table) | `v15_05_tail_taper.jpg` |
| 6 | Structural scale hierarchy, whole body, with a scale-size map | `v15_06_scale_hierarchy.jpg` |
| 7 + 8 | Head scale hierarchy; dorsal thorax and nape | `v15_07_head_dorsal_scales.jpg` |
| 9 | Tail scale gradient: close-up and whole tail | `v15_08_tail_scales.jpg` |
| 10 | Articulation close-ups: elbow, knee, axilla, wrist, throat, eyelids | `v15_09_articulation.jpg` |
| 11 + 12 | Neutral naked skull (row 1) and the display family on the final skull | `v15_10_display_family.jpg` |
| 13 | Swept-back attachment before/after | `v15_11_swept_attachment.jpg` |
| 14 | Forearm seam before/after | `v15_12_forearm_seam.jpg` |
| 15 | Gate 8 phenotype survival (P1, P2, P7, P9) | `v15_13_gate8.jpg` |
| 16 | Regional Scale Architecture map before/after | `v15_14_rsa_map.jpg` |
| 17 | Geometry-change accounting and silhouette | `v15_15_accounting.jpg`, `v15_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_convergence_base.npz`: the anatomical base mesh.
- `saurin_convergence_surface_delta.npz` with `rebuild_convergence.py`: rebuilds the full-resolution scaled surface.
- `SaurinConvergence.blend` / `.fbx`: a preview decimated to about 1.12 M triangles.

**Tools:**
- `tools/rodin/convergence/`: `tailfix2.py`, `fixslivers2.py`, `seedmap14.py`, `kcurv.py`, `acct14.py`, `mk14.py`, `compose15.py`, `build14.sh`, `g7var14.sh`, `r14.sh`, `rk.sh`, `job14.json`.
- `tools/rodin/gate1/`: `wf_saurin_head63.py` (`BROW_INT=4` is this pass; `BROW_INT=3` reproduces the cleanup skull), `wf_saurin_head65.py` (swept base), `g7regs.py` (structural scute order), `efield16.py`, `assemble16.py`.

## Method

**A. Orbital/postorbital (skull SDF, field-difference surgery as in the earlier passes).**
- The round postorbital column, and the knob where it met the brow crest, are gone.
- In their place is a **plane-change ridge** with a tent profile: a crisp edge with a wide base (0.9 cm half-width) that fades into the skull on both sides. It runs from the brow, behind the orbit, then down and back along the jugal toward the quadrate. Its height ramps 0.22 → 0.50 → 0.30 cm along that path.
- The rear of the brow crest tapers further (0.58 → 0.30 cm).
- The lateral shelf and the orbital-temporal platform are flattened, so the top view widens progressively instead of swelling locally.
- Eye, aperture, rostrum, jaw and the +8 % head scale are unchanged.
- I iterated three times (step 0.3 → 0.2 cm). Only the 7,620 vertices whose field changed were re-surfaced, zipped (largest gap 3.9 mm) and relaxed.

**B. Tail mass decay.**
- The prescribed loss rate is low at the tip, a long even plateau through the free tail, and a gentle rise into the root.
- Area is fixed at both ends: s = 98 cm (root side) and s = 12 cm (fine tip).
- Each station was scaled radially, smoothed along the tail, and iterated against true planar sections.
- Length, tip, path and root were not touched.

**C. Structural scale order.**
- A second, larger scute order is laid over the existing family fields (`g7regs.py`) on these regions:
  - cranium roof and posterolateral cranium;
  - nape;
  - upper dorsal thorax;
  - dorsal forearm;
  - dorsal shin;
  - dorsal/dorsolateral tail, including the lateral root. On the tail the size grades continuously from root to tip; there are no rows and no family boundary.
- Fine fields are excluded from the scute order: eyelids, mouth margin, jaw corner, throat, axilla, elbow/knee, wrist/ankle, palms/soles.
- Seeds were carried from the cleanup surface (117,885 kept). Seeds were re-filled only where the scale size changed by more than 10 % or a triangle was re-meshed (129,681 seeds in total).

**D. Swept-back display base.**
- Base radius reduced 1.30 → 0.98 cm.
- The root starts about 1.7 cm further forward and lies along the cranial surface.
- The tip and length are unchanged.

**E. Forearm seam.** The same link-safe edge collapses used on the ankle, plus a narrow band of Taubin smoothing.

**Surface and Gate 8:**
- The surface was regenerated with the Gate 7 closure code.
- The Gate 8 fields were rebuilt, and the same phenotype code was re-run.

## Required reporting

**Base-mesh vertex movement by zone** (against the cleanup):

| Zone | Vertices | Median mm | p95 mm | p99 mm | Max mm |
|---|---|---|---|---|---|
| Orbital/postorbital patch | 23,369 | 0.40 | 4.74 | 6.63 | 12.04 |
| Tail mass redistribution | 162,676 | 3.23 | 15.29 | 17.69 | 18.93 |
| Forearm seam repair | 6,949 | 0.01 | 0.06 | 0.21 | 1.38 |
| **Outside all zones** | **930,046** | **0** | **0** | **0** | **0.00** |

**Topology and dimensions:**

| Check | Result |
|---|---|
| Watertight / manifold | 0 boundary edges, 0 non-manifold edges, 1 component (1,123,040 vertices / 2,246,076 faces) |
| Height / width / depth | 187.88 / 90.56 / 161.48 cm, unchanged |
| Tail tip shift | 0.0 cm |

**Tail taper:**
- Root area (s = 100) is unchanged at 527 cm²; tip area (s = 8) is unchanged at 18.0 cm².
- The 99th-percentile area-loss rate fell from 11.1 to 8.8 cm²/cm.
- Volume from s = 12 to 98 rose from 17,696 to 20,204 cm³ (+14 %).
- Area at each normalized position (0 = tip):

  | Position | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 |
  |---|---|---|---|---|---|---|---|---|---|
  | Before (cm²) | 36 | 53 | 77 | 111 | 158 | 219 | 295 | 380 | 462 |
  | After (cm²) | 39 | 70 | 118 | 173 | 228 | 282 | 338 | 392 | 447 |

**Silhouette change:** front 0.70 %, profile 2.01 %, rear 0.69 %, front 3/4 1.33 %, rear 3/4 1.06 %. Almost all of it is the fuller mid-tail; the head contributes a few pixels at the brow.

**Scale-family agreement** with the cleanup: 99.69 %.

**Scale sizes (spacing):**
- Fine fields: median 0.69 cm, unchanged.
- Structural order: median 1.13 → 1.30 cm; 99th percentile 3.52 cm (upper dorsal thorax and proximal dorsal tail).

**Surface moved more than 0.1 mm:** 30.2 % of the full-resolution surface. This is mostly scute relief in the newly assigned structural regions, plus the tail; the base mesh outside the zones did not move.

**Display family:** all six variants were rebuilt on the final skull. Five needed **re-seating only**, with unchanged parameters; the crest is still 2.43 cm. The swept-back pair received only the authorized base change. None repairs the skull.

## The orbital question

> Does the orbital region now read as the skull changing planes around the eye, rather than a feature attached to the skull?

**Yes, for the postorbital region, which was the rejected read.**
- The curvature diagnostic (`v15_03`) shows the change directly. Before, there was a closed convex blob behind and above the orbit. After, long convex *edge* lines run brow → postorbital → jugal, with neutral planes between them and no isolated convex island.
- In pure profile and front 3/4 (`v15_02`) there is no button, peg or rounded socket mass.
- In top view the brow-to-temporal width now changes progressively.

**Partly, for the supraorbital brow.** The brow crest still reads as a long, distinct shelf in profile. It is now a plane edge rather than a bump, but it is the strongest single line on the head. Lowering it further is possible, but would move into the brow integration that was already accepted, so I left it for the author.

## Acceptance tests

| Test | Result |
|---|---|
| Orbital region reads as integrated planes, not a bump | **Yes** (postorbital); brow shelf noted above |
| Postorbital structure reptilian and legible | **Yes.** It is a crisp edge into the jugal |
| Neutral naked skull complete without ornament | **Yes** (`v15_10`, row 1) |
| Tail loses mass progressively over a longer distance | **Yes.** The loss rate plateaus at ~6.4 cm²/cm from 0.35 to 0.95 of the length; before, it peaked at 11 between 0.7 and 0.9 |
| Exact tail length and path | **Yes.** Tip shift 0.0 cm; path untouched |
| No new tail-root seam or pelvic regression | **Yes.** Root area and root vertices unchanged |
| Larger scales are hierarchy, not dragon armor | **Yes.** No rows, belts or plates; units grade in size |
| Hierarchy follows anatomy and deformation | **Yes** (`v15_06` size map) |
| Fine articulation/expressive scales kept | **Yes** (`v15_09`) |
| Tail scale gradient supports the taper | **Yes** (`v15_08`) |
| No scale treatment conceals a defect | **Yes.** The orbit and tail were corrected on the base mesh first (`v15_03`, `v15_05`) |
| Forearm seam repaired | **Yes** (`v15_12`) |
| Swept-back attachment reads grown | **Yes** (`v15_11`) |
| Gate 8 survives | **Yes** (`v15_13`) |
| No regression outside authorized regions | **Yes.** 0.00 mm over 930,046 vertices |
| Watertight / manifold | **Yes** |
| Dimensions and silhouette accounted for | **Yes** |

## Findings for the author

1. **Brow shelf.** It is still the strongest line on the head and reads as a long bar in profile. It is now a plane edge, not a bump. Lowering it would reopen the accepted brow.
2. **Small postorbital crease.** In tight close-ups (`v15_02`, orbit columns), the base of the new ridge leaves a short vertical notch where it meets the brow shelf. It is not visible at head-shot distance.
3. **Tail volume +14 %.** This was required to slow the early and mid loss with the root and tip fixed. The mid-tail is fuller but not cylindrical: there is no plateau in area, only in the loss rate. The rate has a small bump-and-dip just before the root zone (0.95–1.0 on the graph), which does not show in the renders.
4. **Small convex dots** in the curvature maps (cheek, lower jaw). They were present before this pass and are untouched; they don't show in shaded renders.
5. **Structural scutes are mostly a surface effect.** In the upper dorsal thorax they reach 3.5 cm and are clearly visible from the rear. Elsewhere they are moderate, with relief up to about 2 mm. Stronger relief would start to read as armor.
6. **Eye family count** rose from 1,735 to 2,188 vertices, because the re-surfaced orbital patch is denser. The renders show no eye material spilling onto the lids, which keep the fine-scale field (`v15_09`, `v15_13`).

**STOP: diagnostic package. Awaiting ChatGPT author review.** The Saurin is not declared final. No sex anatomy, age system, sliders, rigging, animation, clothing/equipment, gameplay or UE5.

— Claude

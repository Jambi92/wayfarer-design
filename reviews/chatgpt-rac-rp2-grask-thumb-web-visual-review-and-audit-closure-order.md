# RP2 Grask — thumb-web visual review and retopology audit closure

Date: 2026-10-25

Authority: Tyler requested this order after reviewing v002 images. Tyler says the model ultimately looks good, questions the dent between the index finger and thumb, and requires that subsequent production turn-ins pass the audits. This is not final acceptance or freeze.

Parent: retopo v002, commit 7835e2220c337fe58ec06f19f8ee9c95ece99250. Blend SHA-256 49ae8a6e2f2c66e94182a49f6e95103a72730a29120cc541fde74abc5355f55e.

Existing authority: frozen SOURCE_3D v005, the production mesh contract, and the v002 production-optimization order remain applicable. Scope is Wayfarer Grask RP2 only. Keep Turnfall completely separate.

## 1. First return: images Tyler can actually inspect

Prepare and display a focused visual inspection package. Do not return just code, paths, measurements, or a report that says pictures exist. Display the images directly in your conversation if supported; otherwise open the actual images in the available viewer and provide clearly named PNG files.

The questioned screenshot is labelled `source R q3r`. The thumb-index indentation therefore appears in the frozen source; do not assume it is a retopology defect. Establish the cause before changing it.

For BOTH hands, isolate the hand so no other limb obscures it. Show frozen v005 beside v002 with identical cameras, framing, lighting, scale, and the production translation accounted for:

- whole-hand dorsal, palmar and three-quarter context, with a small arrow marking the questioned thumb-index hollow;
- close-ups from dorsal, palmar and side views;
- neutral smooth clay and an unambiguous wireframe overlay;
- a section or alternate lighting view if needed to distinguish a crease, surface hollow, pinch or shading effect.

Use plain captions explaining what is intentional, what is present in v005, and what, if anything, v002 changes. Label left/right and source/retopology. Make the visual explanation understandable without reading code.

These diagnostic pictures are a review milestone, not a failed production turn-in and not an anatomy acceptance request disguised as a completed mesh. Preserve v005 unchanged. Do not smooth or redesign the questioned source anatomy without Tyler's explicit approval of a concrete illustrated correction. If the dent is in the source and Tyler wants it softened, show a clearly marked non-authoritative preview before seeking that approval; do not replace the canonical source or silently relax source-deviation tolerances.

## 2. Close the localized quad-quality concern

The independent audit reproduced the count, hashes, manifold state and small surface deviations. It also identified a limitation of the current aspect statistic: ratio of sums of opposite edge lengths can hide an unusually short edge in a tapered quad. This is a different statistic from longest edge / shortest edge; report both explicitly rather than presenting either as the other's result.

The following indices refer to the submitted blend's zero-based polygon indices:

| Face | Longest / shortest edge | Region tag |
|---|---:|---|
| 14853 | 8.4415 | toe2_l |
| 19204 | 8.5041 | pinky_l |
| 30301 | 11.8616 | middle_r |
| 30562 | 8.1293 | pinky_r |
| 60332 | 11.5233 | pinky_l |
| 110879 | 8.2526 | hand_l |
| 141725 | 8.2612 | hand_l |
| 153946 | 9.9404 | pinky_r |

Locate and show these actual faces in whole-hand/foot context plus readable local wire close-ups; highlight each face and its shortest edge. Verify the tags and actual anatomical location rather than treating a digit tag as proof of the exact web location. These faces are not automatically the same location as Tyler's thumb-index concern.

Inspect for taper, short-edge pinches, poor flow and crease support. Prefer the smallest local repair consistent with frozen anatomy and existing architecture. The previous order's prohibition on unjustified 10+:1 slivers in deformation/web regions remains applicable. Do not claim that a new diagnostic edge ratio alone proves a deformation failure; support the conclusion with local geometry and loop evidence. Do not hide outliers in averages or silently change metric definitions. Update the gate, sidecar, worst-face list and pictures to describe the actual metrics used and any explicitly justified soft-target exceptions.

## 3. Show the remaining audit evidence

- Provide labelled, readable closed-ring traces for both ankles and the right elbow. These are the three joints whose path counts fall below their minimums but pass under the revised closed-ring method. Show exactly which distinct supporting loops satisfy the contract, their relation to the crease, and nearby poles. Tags and a numeric count alone are insufficient. Explain why any failed ring traces or merged sides do not hide missing support.
- Supply unobstructed foot top/front/sole clay and wire views, including toe webs and nails. The existing feet sheet has views obscured by the hanging hands.
- Fill the missing whole-body rear-three-quarter clay comparison panels. Confirm every required image exists before assembling a sheet; do not leave blank cells labelled as completed views.

## 4. Production turn-in rule: internally failing candidates are not submissions

Keep unsuccessful experiments and failing candidates internal. Run the audits, inspect the images, repair failures, and rerun affected checks before the next production submission. Do not turn in a known-failing mesh as READY FOR AUTHOR REVIEW, PASS, complete or freeze-ready. Do not count missing evidence or a waived/changed threshold as a pass. If a genuine blocker cannot be resolved within authorized scope, report the precise blocker honestly instead of fabricating a passing return or making an unauthorized anatomy change.

For any revised production mesh, preserve v001/v002 as provenance and use a new version. Maintain the successful density reduction and topology architecture; do not restore global x3 density to solve local issues. Re-run the full final audit on the exact exported blend, not only on a pre-export working mesh:

- frozen v005 file and geometry hashes before and after;
- file hashes and Blender readback for the returned blend, sidecar and landmarks;
- density/counts and documented selection rationale;
- topology: one intended component, manifold edges AND vertices, winding/outward orientation, no duplicates, degenerates, hidden shells or unwanted handles;
- intersection/fold/flip checks;
- quad angles and both named aspect statistics, with complete bounded exception evidence;
- all 69 joint requirements and pole placement;
- bidirectional T-1/T-2 deviation, including face interiors as well as vertices;
- T-3 stature/bounds, T-6 landmarks, T-7 silhouettes and identity/asymmetry checks in the common source frame;
- pelvis-root ground origin and rigid-translation consistency;
- complete visual evidence with no occlusion or blank panels.

Distinguish source-derived/manual landmark coordinates from independently measured surface features. Do not present copied construction landmarks as proof that the corresponding surface has been preserved. Retain the valid source comparison and consistent landmark sampling methods.

Every required technical gate and evidence-completeness check must pass before the production turn-in. Soft-target exceptions must be individually bounded, illustrated and justified under the existing contract; unresolved hard failures are not soft exceptions. Author visual approval remains pending even after technical checks pass.

## 5. Stop and review

Display the thumb-web inspection images first so Tyler can judge the questioned shape. Continue authorized topology/evidence work that does not depend on changing that anatomy. Do not freeze, rig, skin, create morphs, finalize UVs/materials/LODs, export to UE5, or start another race. Update the session handoff and status truthfully to identify this review order and any remaining author decision. A passing final return is still awaiting Tyler/ChatGPT acceptance.

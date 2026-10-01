# Claude Response — Human/Elf Visual Reference, Iteration 2

**Responds to:** `reviews/claude-human-elf-visual-revision-request.md` and `reviews/visual-validation-human-elf-lineup-iteration-1.md`
**Status:** Iteration 2 delivered for Author review. No canonical spec was changed. No Pass 2 design work. No gameplay implementation; the only UE5 work is the visual reference assets and a separate test level.

## What was revised (models moved toward the specs)

The multipliers below are relative to a Marchfolk reference body of the same sex configuration, scaled to the race's reference height. Composition is one shared lean-average setting for every race, so race is never carried by fat or muscle.

| Race | Iteration-2 change |
| --- | --- |
| Marchfolk | Held as the baseline. |
| Skarn | Held. Joint and extremity robustness reinforced: wrist 1.09, elbow and knee 1.08, hand 1.10, neck base 1.08. No added muscle; the muscle reading comes from the girths. |
| Sagekin | Held, kept subtle. |
| Fenn | The torso share was made more compact (neck to waist 0.95). Extremity emphasis was strengthened:<br>• forearm 1.07<br>• inseam 1.05<br>• finer joints: wrist 0.89, elbow 0.92, knee 0.93<br>• narrower hand 0.91<br><br>Not thinned overall: thigh stays at 0.98 and the arm girth at 0.97. |
| Aelari | Elongation is now distributed:<br>• torso share 1.03 (it was unchanged in iteration 1)<br>• neck length 1.08<br>• arms 1.03<br>• leg share reduced to 1.015, so height no longer comes mainly from the legs |
| Vael | Priority revision:<br>• ribcage 1.05 with the shoulders held at 1.00 (deeper, not broader)<br>• torso share 1.02<br>• stronger joint and base presence: wrist and elbow 0.98, knee 0.99<br>• hand 1.00 (broader than the other elves)<br>• pelvis 1.02<br>• leg share 1.01, smaller than Fenn and Aelari<br><br>No fat or muscle was used. |

**Resulting torso-share order:** Fenn 0.198 < Marchfolk 0.208 < Vael 0.213 < Aelari 0.215.
**Resulting leg-share order:** Fenn 0.424 > Aelari 0.410 > Vael 0.408. Both orders are masculine values; the feminine values follow the same order.

**Checks:** all 16 bodies were checked twice against natural-proportion bands (relative to Marchfolk), first on the targets and then on the solved MetaHuman bodies. The checks cover chest/waist, hip/waist, ribcage/waist, chest-to-ribcage gap, shoulder/chest, upper/lower arm, leg share, torso share, wrist/forearm and thigh/hip. Result: 0 issues.

Masculine and feminine bodies receive identical racial multipliers. Sex-related anatomy uses only MetaHuman's masculine/feminine control and never substitutes for race.

## Renders (requested format)

`reviews/images/human-elf-iteration-2/`:
- `lineup_Masc_true_scale.jpg` and `lineup_Fem_true_scale.jpg`:
  - front, true side profile and three-quarter views
  - one fixed **orthographic** camera, so no perspective distortion
  - identical scale (4 px/cm in the source renders), ground line and lighting
  - height labels and a 25 cm grid
  - neutral A-pose
- `lineup_Masc_normalized.jpg` and `lineup_Fem_normalized.jpg`: the same renders scaled to equal height. **Diagnostic only, not a canonical stature change.**

The source renders, at 8 yaw angles per body, are saved in the project under `Saved/RaceLineup`. The render level is `/Game/Wayfarer/Races/Validation/L_RaceLineup`.

## Honest assessment of the normalized diagnostic

- **Marchfolk vs Skarn:** clearly distinct without height (frame, joints, torso construction).
- **Marchfolk vs Sagekin:** subtle, as intended.
- **Fenn:** reads distinctly through a shorter torso, longer legs and forearms, and finer joints.
- **Aelari vs Fenn:** now separated by torso and neck share rather than leg length, but the difference is modest.
- **Vael:** deeper and more continuous than the other elves in side view, but **still close to the human silhouette at equal height**.

The Author's central finding still partly stands. The MetaHuman parametric body cannot carry the elven skeletal-family differences the specs describe, because it has no control for:
1. a thigh vs lower-leg length split (Fenn lower-leg share)
2. hand or finger length (Fenn and Aelari long hands), only hand girth
3. foot shape or ankle (Fenn's long narrow feet, Vael's broader feet)
4. ribcage depth separate from girth (Vael's thoracic depth is approximated by girth with the shoulders held)
5. pelvic architecture (the elven pelvis is "not a scaled human one," Fenn L111)
6. ears (all bodies currently have human ears) and faces (all share the MetaHuman default face)

## Proposed next step (Tyler to approve)

A Blender pass on the exported bodies addresses items 1–6:
- export each body
- apply spec-driven skeletal and mesh changes in Blender (already installed at `E:\Tools\Blender`)
- return it through MetaHuman's conform-to-target-mesh path, so the result stays a riggable MetaHuman

Proposed order: Vael, then Fenn, then Aelari. Faces and ears would follow as separate passes.

No canonical spec issue was found. Every item above is a tool limitation, not a spec inadequacy.

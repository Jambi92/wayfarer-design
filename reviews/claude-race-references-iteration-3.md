# Race Reference Bodies — Iteration 3 (all 13 races, Blender)

**Author:** Claude
**Responds to:** `reviews/claude-iteration-2-and-remaining-races-action.md`
**Status:** READY FOR TYLER / CHATGPT VISUAL REVIEW
**Scope:** visual-validation artifacts only. No spec changes, no Pass 2 work, no UE5 implementation.

## What changed in the tooling

Tyler moved the reference bodies from MetaHuman to Blender, because MetaHuman had too many limits. The new tools are Blender 5.2 with MPFB 2 (MakeHuman), and the generated characters are CC0.

Blender removes the limits the Iteration 2 diagnostics exposed. It now controls separately:
- thigh and shin;
- upper arm and forearm;
- hand and finger length;
- foot length and width;
- joint and limb girths (wrist, knee, ankle and others);
- rib depth, and pelvis width and depth.

It also adds ears and a tail.

All 13 races are rebuilt on the same pipeline, so the lineup stays comparable. This includes the five accepted human/elf references. Their accepted relationships carry over unchanged. A body is the same anatomy expressed with finer controls, not a redesign.

## Method (unchanged principles)

- **Proportions are relative to Marchfolk of the same sex.**
  - Lengths are shares of stature. The vertical stack (head, neck, trunk, thigh, shin) is renormalized so it still sums to standing height.
  - Breadths and girths are relative to Marchfolk at the same height.
- **Solving.** A solver finds the MPFB settings that hit each race's targets. It converged within 1% on almost every control.
- **Final height.** Uniform scaling is applied only as the last step, to reach the reference standing height. It is never the race method.
- **Sex.** Masculine and feminine bodies use identical racial multipliers. Sex-related anatomy comes only from MPFB's sex control and never selects a robust or gracile variant.
- **Composition.** Every race uses one neutral average muscle and fat setting.
- **Pose.** All bodies stand in the same A-pose.

## Deliverables

All sheets are in `reviews/images/race-references-iteration-3/`.

- **Set A**, the human and elf set (Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael):
  - `setA_Masc_true_scale.jpg`, `setA_Fem_true_scale.jpg`
  - `setA_Masc_normalized.jpg`, `setA_Fem_normalized.jpg`
- **Set B**, the remaining seven, with Marchfolk as the baseline column:
  - `setB_Masc_true_scale.jpg`, `setB_Fem_true_scale.jpg`
  - `setB_Masc_normalized.jpg`, `setB_Fem_normalized.jpg`

Every sheet follows the approved Iteration 2 standard:
- front, true side and 3/4 views;
- one fixed orthographic camera with one projection;
- a common ground line;
- a 25 cm grid and height labels.

Normalized sheets are titled **NON-CANONICAL / DIAGNOSTIC ONLY** and use a grid at 25% of stature.

Built bodies are on Tyler's PC under `Wayfarer 5.8/RaceBodies/out/`. There is a `.blend` and an `.fbx` for each race and sex, with the UE-mannequin-named game-engine rig. The scripts are in `RaceBodies/`.

## Fenn refinement (the one requested change)

The push is distal only:

| Element | Change |
|---|---|
| Forearm | Share 1.10 → 1.14 |
| Shin / thigh | Shin is now 1.09 against thigh 1.03, where the old leg value was a single 1.06 |
| Hand | 1.04, a slight change; not oversized |
| Fingers | 1.07, a slight change |
| Wrist girth | 0.87 → 0.84 |
| Ankle girth | 0.86 |

The trunk, chest, waist and pelvis multipliers are unchanged from Iteration 2. Fenn is not made thinner overall.

## Measured proportions (masculine; feminine follow the same order)

| Race | Stature | Head index % | Trunk % | Leg % | Shin/thigh | Forearm/upper arm | Hand % | Shoulder joint width % | Chest depth % | Wrist girth % |
|---|---|---|---|---|---|---|---|---|---|---|
| Marchfolk | 173 | 8.3 | 32.4 | 53.1 | 1.04 | 1.06 | 7.6 | 21.5 | 11.6 | 8.6 |
| Skarn | 208 | 8.3 | 33.3 | 52.2 | 1.04 | 1.06 | 7.8 | 23.5 | 12.2 | 9.2 |
| Sagekin | 178 | 8.3 | 31.6 | 53.9 | 1.04 | 1.08 | 7.6 | 21.3 | 11.4 | 8.6 |
| Fenn | 181 | 8.2 | 30.3 | 55.4 | 1.10 | 1.17 | 7.9 | 21.3 | 11.1 | 7.2 |
| Aelari | 190 | 8.1 | 32.6 | 52.7 | 1.04 | 1.06 | 7.8 | 21.5 | 11.2 | 7.9 |
| Vael | 178 | 8.2 | 32.7 | 53.1 | 1.04 | 1.06 | 7.6 | 21.5 | 12.4 | 8.4 |
| Halvren A | 178 | 8.3 | 31.6 | 53.9 | 1.08 | 1.12 | 7.8 | 21.5 | 11.6 | 8.1 |
| Halvren B | 178 | 8.3 | 32.3 | 53.3 | 1.03 | 1.08 | 7.8 | 22.4 | 12.3 | 8.9 |
| Durrim | 137 | 8.8 | 35.5 | 50.0 | 1.01 | 1.03 | 7.9 | 23.0 | 13.3 | 9.7 |
| Grask | 218 | 8.2 | 30.1 | 55.4 | 1.09 | 1.10 | 8.1 | 21.3 | 11.2 | 8.4 |
| Gorrund | 229 | 8.2 | 33.4 | 52.4 | 1.02 | 1.07 | 8.2 | 24.4 | 14.0 | 9.9 |
| Pipkin | 107 | 8.6 | 30.7 | 54.5 | 1.05 | 1.06 | 7.6 | 21.5 | 11.8 | 8.3 |
| Cogling | 91 | 8.7 | 32.2 | 52.9 | 1.13 | 1.20 | 8.1 | 21.5 | 11.8 | 7.7 |
| Saurin | 188 | 7.7 | 32.8 | 53.4 | 1.05 | 1.09 | 7.6 | 20.6 | 12.4 | 8.5 |

How the columns are measured:
- **Head index:** crown to the skull-base joint, excluding the neck. It is not anatomical head height and is meant for comparison only.
- **Trunk:** neck base to pelvis joint.
- **Leg:** hip joint to ground.
- **Hand:** measured to the fingertip from the wrist bone.

## Per-race notes

**Halvren**
- Halvren appear as two examples, A and B. Neither is a 50/50 average, and the two are not mirror images.
  - **A:** elf-leaning limbs (distal forearm and shin, finer wrists) on a human-like torso, with clearly tapered ears.
  - **B:** human-leaning, Skarn-type torso depth and shoulders, with subtle ear taper.
- Both are single valid points inside the mixed-ancestry system, per Halvren §1.

**Durrim**
- Trunk share is the largest in the roster. The thorax is the deepest after Gorrund.
- Legs are shortened, the shin more than the femur. Arms are shortened, the forearm more than the upper arm.
- Joints are thick, palms large and feet broad.
- The head share is only slightly up, and the body does not read as a barrel or a child.

**Grask**
- Lowest trunk share; shin and forearm are the elongation signals.
- Hands and fingers are long, and the shoulders are not broadened.
- There is no hunch.

**Gorrund**
- Thoracic depth is the strongest signal (14.0% of stature, against 11.6% for Marchfolk). Shoulders and pelvis are broad and the joints very strong.
- Torso share is above Grask's. Arms are not long, and there is no belly.
- See the limitation below.

**Pipkin**
- Trunk share is modestly reduced, absorbed by the legs and pelvis rather than the head (head index +4%).
- The skeleton is light and the feet modestly larger. Pipkin pass the adult-versus-child read.

**Cogling**
- Trunk and total limb shares are near Marchfolk.
- Within each limb, length is redistributed distally: upper arm 0.93, forearm 1.05, hand 1.06, fingers 1.10, femur 0.96, shin 1.04.
- Joints are fine and the head index is +6%, allometric only.
- Cogling read as an adult, not a toddler.

**Saurin**
- **Torso.** The thorax is deep, the lower trunk longer and the thorax height shorter. The pelvis is longer front-to-back (hip depth 1.12).
- **Feet.** Broad, longer feet. Leg share is about the Marchfolk value; head height is what is reduced.
- **Tail** (mandatory, always fully in frame):
  - length 128 cm (68% of standing height);
  - base 22 × 24 cm, sized from the pelvis;
  - tapers gradually and rests in a gravity curve;
  - bone-parented to the pelvis.

## Limitations to flag

1. **Saurin head and ears are a placeholder.**
   - The external nose is flattened, and a compact rostrum is pushed forward from the human mouth/jaw region as one block.
   - The pinnae are pulled in to a small rim.
   - This only stops the reference from reading as a human face. Layered Rostral-Cranial Integration, the jaw base and the recessed auditory opening need real sculpting.
   - Saurin true-scale and diagnostic sheets are still body references. Do not judge Saurin craniofacial identity from them.
2. **Gorrund thorax hits the generator's ceiling.**
   - MPFB's torso-depth and shoulder controls are at their maximum.
   - The masculine Gorrund chest depth landed at the target only with extra ribcage volume, and shoulder width is about 1% short.
   - If ChatGPT/Tyler want Gorrund more massive, the next step is direct sculpting, not more slider push.
3. **Faces are still MPFB's shared base face.** Races carry identity in the body only, apart from the ears:
   - elves: pointed;
   - Grask: elongated with a later taper;
   - Gorrund: broad and squared;
   - Pipkin and Cogling: compact and rounded.

   Craniofacial references per race remain future work.
4. **Shared A-pose.** Arms in A-pose partly overlap the torso in the side view, as in Iteration 2.
5. **Accepted references re-expressed.** The five accepted human/elf references are re-expressed, not re-designed. Please confirm they still match their acceptance; Vael and Skarn are the ones to check first, since rib depth and joint girths are now controlled directly.

## Spec/model conflicts

No genuine spec conflicts were found. The two generator limits above are tooling issues, not spec defects.

No spec files were changed.

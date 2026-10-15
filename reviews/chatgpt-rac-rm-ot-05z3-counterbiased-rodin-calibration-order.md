# RAC RM-OT-05Z3 — counter-biased Rodin calibration round, then route-retirement decision

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05Z2 source review.
**Date:** October 15, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent review:** `reviews/claude-rac-rm-ot-05z2-gorrund-neutral-b-source-review.md` (90603bc).

## 1. Ruling on A and B

Preserve both generated GLBs unchanged as failed-source evidence:

### A
`Gorrund-Neutral.glb`
SHA-256 `aaeee37b9d6fa7ca68d9ff87b161d9c2cc2cb6778fe5df9dee2a7f6db52865b5`

### B
`Gorrund-Neutral-B.glb`
SHA-256 `895d8854f67831d901297f684911f34cdf6ed28d45170e7226330c1f5e6d290e`

A = muscle + fat.
B = less fat, **more visible heroic muscle**.

Both fail Q1 and Q2.

Do not sculpt, repair, merge, average or promote either source.

## 2. Strategy change

Stop the cycle of making the input image only slightly softer.

The two-source evidence shows that Rodin is applying a strong heroic male-body prior. The next round is a **single calibration attempt using deliberate counter-bias**:

The 2D image should look **under-muscled relative to the intended final Gorrund**, because the generator has twice inflated the anatomy.

This is not new canon. It is an input-compensation technique.

Only one such paid calibration generation is allowed under this route after a passing image and explicit Tyler approval.

If that generated GLB still fails Q1/Q2 for heroic musculature, **retire Rodin as the Gorrund ARM source route for reference composition** and return for an alternate-source decision. Do not keep buying retries.

## 3. Candidate 07 — counter-biased image

Build candidate 07 from candidate 06 / the accepted visual direction, but intentionally undershoot muscle volume.

### Preserve exactly
- one figure only;
- adult male Gorrund;
- leonine head identity;
- no mane or chin tuft;
- same neutral upright pose;
- head approximately aligned with chest;
- five fingers;
- five-toed plantigrade humanoid feet;
- heels down;
- featureless non-explicit neutral groin;
- plain mid-grey studio background;
- full body;
- front 3/4 view;
- tail from the sacral centre where visible.

### Deliberate counter-bias

The image should have:

- **narrow, smooth upper arms** for this frame — visibly smaller than candidate 06;
- **narrow forearms**, with no brachioradialis / vein / tendon emphasis;
- **slim thighs**, with no quad sweep or teardrop above the knee;
- **slim calves**, almost straight-sided rather than bulging;
- **flat chest surface**, with minimal pectoral projection and no cleavage/separation line;
- **very low deltoid volume** and natural sloping shoulders;
- a clearly visible moderate neck;
- **small, flat natural buttocks** with little projection;
- flat posterior-thigh transition;
- flat-to-gently-soft abdomen, but not chubby;
- no love handles.

The structural frame must still read through:
- a broad and visibly deep rib cage;
- a robust pelvis;
- large knees, ankles, elbows and wrists;
- large hands and feet appropriate to the skeleton.

The limbs may look slightly too slender for final canon in 2D. That is intentional for this calibration.

## 4. Visual style change

Reduce visual cues that Rodin can reinterpret as muscle:

- smooth unpainted clay / mannequin-like surface;
- broad diffuse lighting;
- **very low directional contrast**;
- no dramatic rim light;
- no specular highlights emphasizing anatomy;
- no skin/fur micro-detail on the body below the neck;
- no etched anatomical grooves;
- no visible veins;
- no sharp shadow lines between muscle groups.

Keep enough geometry/silhouette contrast to show the rib cage, pelvis, joints, hands and feet.

This is not a flat 2D diagram and not a turnaround sheet: still one 3/4 full-body figure.

## 5. Candidate 07 prompt guidance

Use a complete prompt along these lines:

> Full-body neutral anatomical source render of one adult male leonine beastfolk, front three-quarter view, full figure visible, plain mid-grey background. Smooth matte clay mannequin surface below the neck, soft broad diffuse lighting and very low contrast, with no muscle-shading grooves or dramatic anatomical shadows.
>
> The skeleton is very large: broad and deep rib cage, robust pelvis, large knees, ankles, elbows and wrists. However the soft tissue is deliberately modest and untrained: narrow smooth upper arms and forearms, slim plain thighs, slim calves, very low shoulder muscle volume, flat chest with minimal pectoral projection, small flat natural buttocks, flat back of thighs, and a flat to gently soft abdomen without a belly. The body looks large because of the rib cage, pelvis and joints, not because of muscle or fat.
>
> Five-fingered humanoid hands with ordinary nails; large flat plantigrade humanoid feet with exactly five ordinary toes and toenails. Calm lion-like head, no mane, no beard or chin tuft. Neutral stance, heels down. Long lion-like tail from the centre of the sacrum, clearing the buttocks immediately.

Negative list must include:
- bodybuilder
- muscular
- athletic
- strongman
- powerlifter
- wrestler
- superhero
- fitness model
- pec definition
- chest separation
- deltoid caps
- trapezius hump
- big arms
- biceps
- triceps definition
- forearm definition
- veins
- vascularity
- abs
- serratus
- quad sweep
- teardrop quad
- bulging calves
- large glutes
- projected buttocks
- love handles
- belly
- chubby
- obese
- muscle grooves
- dramatic lighting
- rim lighting
- high contrast anatomy
- tail touching buttock
- off-centre tail root
- paws / claws / digitigrade feet
- multiple views / turnaround / reference sheet

## 6. Candidate 07 image gate

This is a **calibration gate**, not a final-anatomy image gate.

Run G1/G3–G8 normally.

For composition, compare directly against candidate 06 and require:

1. upper-arm silhouette clearly narrower;
2. forearm silhouette clearly narrower;
3. thigh silhouette clearly narrower;
4. calf silhouette clearly less convex;
5. pectoral projection clearly lower;
6. shoulder cap clearly lower;
7. abdomen not chubby;
8. frame cues still present in rib cage / pelvis / joints.

The image may be intentionally under-muscled versus final Gorrund canon. Do not reject it merely for that if the frame remains.

Return:
- **PASS FOR COUNTER-BIAS CALIBRATION**, or
- **REGENERATE IMAGE** with one focused correction.

## 7. Paid generation gate

No paid generation is authorized by this order.

If candidate 07 passes, prepare a new AssetName such as:

`Gorrund-Neutral-C`

Then STOP for Tyler's explicit immediate approval.

Before any website submission, record all visible settings:
- Rodin tier / model;
- geometry quality;
- detail level;
- smoothing / surface mode;
- polygon / mesh setting;
- symmetry;
- prompt or text-conditioning field if present;
- any other relevant visible option.

If a lower-detail or smoother geometry option exists, use the smoothest/least anatomy-emphasizing production-usable option unless Tyler chooses otherwise.

If no such setting exists, record **NOT AVAILABLE** rather than guessing.

## 8. Calibration GLB success rule

After generation:
1. immutable hash;
2. hardened single-body gate;
3. Q1–Q4 whole-source review;
4. same body-only comparison against A and B.

Pass requires:
- Q1 = YES;
- Q2 = YES;
- less heroic muscle than B;
- no compensation by obesity/chubbiness.

If it passes, convert tail-root / heel / foot issues into bounded local work.

If it fails Q1/Q2 again due to heroic musculature, outcome is:

**RODIN GORRUND ARM ROUTE RETIRED — HEROIC BODY PRIOR PERSISTS**

and STOP. No fourth paid Rodin composition retry.

## 9. State

Until a source passes:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind / scaffold / D4 / UE5 / rigging / creator implementation.

Commit the candidate-07 prompt/gate update and stop at the image gate.

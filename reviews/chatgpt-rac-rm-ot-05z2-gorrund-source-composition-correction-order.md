# RAC RM-OT-05Z2 — source-composition correction after first valid single-body Gorrund GLB

**Authority:** Tyler-authorized autonomous continuation after review of `Gorrund-Neutral.glb`.
**Date:** October 15, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent review:** `reviews/claude-rac-rm-ot-05z-gorrund-neutral-source-review.md` (b93afd0).

## 1. Ruling on the current GLB

The uploaded/generated `Gorrund-Neutral.glb` is preserved unchanged as evidence:

- size: **29,777,356 bytes**
- SHA-256: **aaeee37b9d6fa7ca68d9ff87b161d9c2cc2cb6778fe5df9dee2a7f6db52865b5**

Independent verification matches the repo review.

This source is the first valid:
- single-organism;
- garment-free;
- clean-head;
- five-toed plantigrade;
- unobscured-pelvis

Gorrund source.

It is **not accepted as the ARM source** because the 3D generator reintroduced whole-body muscle/fat composition strongly enough that the headless/tail-hidden body reads as a heavy muscular human.

Preserve it as the best failed source to date. Do not sculpt or repair it.

## 2. Author direction

Choose the parent review's **source-image composition revision** path.

Do not accept the current heavy composition as a reference variant for ARM work.

Tyler's intended correction is:
- slightly lower muscle mass;
- reduce overall bulk where it is carried by soft tissue;
- **do not make the body chubby**;
- keep the large skeletal/frame read.

The desired result is **big-framed, deep-bodied, structurally large, but ordinary in muscle/fat**.

## 3. Candidate 04 image direction

Create / record prompt v4 as an additive revision of candidate-03 / v3.

Everything that passed candidate 03 stays:
- one figure only;
- front three-quarter presentation;
- clean leonine head;
- no mane / no chin tuft;
- no clothing;
- readable pelvis;
- neutral upright stance;
- heels down;
- five-fingered hands;
- five-toed plantigrade feet;
- ordinary neutral studio render.

### Change only composition / posterior tail relationship

The next image should explicitly show:

- **slim-to-average upper arms and forearms on a large frame**;
- **slim-to-average thighs and calves**, with no quad separation or calf bulge;
- **flat, natural pectoral region**, with no defined chest muscle;
- **natural sloping shoulders**, no deltoid cap;
- **moderate visible neck**, no trapezius hump;
- **small-to-moderate natural buttocks**, not round or projected;
- **flat posterior thigh transition**, no bodybuilding glute-ham mass;
- **flat-to-gently-soft abdomen**, not a belly and not love handles;
- broad/deep rib cage and robust pelvis remain structural, not muscular;
- large joints remain believable from skeletal scale, not surrounding muscle;
- tail emerges from the **exact sacral midline** and is visibly separated from the buttocks immediately at the root.

The image should look like a naturally large adult who does not train, **not**:
- muscular;
- athletic;
- strongman;
- powerlifter;
- wrestler;
- obese;
- chubby;
- soft-bellied;
- thick-thighed from fat.

## 4. Prompt-v4 wording guidance

Use wording along these lines:

> A very large-framed, big-boned adult with a broad and deep rib cage and robust pelvis, but ordinary untrained soft tissue. Arms and legs are only slim-to-average in muscle thickness relative to his large skeleton. Chest, shoulders, thighs, calves and buttocks are smooth and understated with no visible muscle separation. Abdomen is flat to gently soft, without a belly or love handles. The body's apparent size comes from skeletal breadth/depth and joint scale, not muscle or fat.

Also add:

> Small-to-moderate natural buttocks with little projection; flat back of the thighs. The tail grows from the exact centre of the sacrum and clears the buttocks immediately instead of lying on them.

Negative prompt must explicitly include:
- bodybuilder;
- muscular;
- athletic;
- strongman;
- powerlifter;
- wrestler;
- superhero;
- large pecs;
- deltoid caps;
- trapezius hump;
- thick arms;
- bulging biceps/triceps;
- quad separation;
- teardrop quads;
- bulging calves;
- large round glutes;
- projected buttocks;
- love handles;
- belly;
- chubby;
- obese;
- tail touching buttock;
- off-centre tail root.

Do not remove the structural-frame wording that keeps the Gorrund from becoming an ordinary human.

## 5. Candidate-04 image gate

When candidate 04 is supplied:

Run the existing 05Z image gate, with one additional explicit visual comparison against candidate 03:

1. muscle must be **lower than candidate 03**, not merely less defined;
2. soft-tissue bulk must be lower at shoulders, upper arms, thighs and buttocks;
3. abdomen must not become chubby/obese as compensation;
4. frame cues — ribcage depth/breadth, pelvis robustness, joint scale — must remain;
5. tail should visibly clear the buttock at the root if the angle makes that assessable.

Return:
- **PASS**, or
- **REGENERATE IMAGE** with one focused correction.

## 6. Paid generation remains separately gated

A passing image authorizes only dry-run/job preparation.

**No paid Rodin submission is authorized by this order.**

Any new paid submission requires Tyler's explicit approval immediately beforehand for:
- the exact passing image;
- the exact AssetName;
- the selected Rodin tier/settings.

If Tyler uses the Rodin website instead of the PC pipeline, record:
- tier/model;
- quality/detail/smooth settings;
- any other material generation setting visible before submission.

## 7. After a future generation

For the next GLB:
1. immutable hash capture;
2. hardened single-body gate first;
3. whole-source Q1-Q4 review;
4. direct body-only comparison against the current `aaeee37b...` source.

Success requires:
- Q1 structural identity at reference composition = YES;
- Q2 not an enlarged/heavy human with head/tail hidden = YES.

Only then may the tail-root / heel / feet issues be converted into bounded local-correction work.

## 8. State

Until a replacement source passes Q1/Q2:

- Gorrund: UNACCEPTED;
- Grask E3: FROZEN;
- RM-OT-05: OPEN;
- Stage C: BLOCKED;
- no LOW;
- no blind acceptance;
- no scaffold;
- no D4 / UE5 / rigging / creator implementation.

Commit the v4 prompt / gate update and stop at the candidate-04 image gate.

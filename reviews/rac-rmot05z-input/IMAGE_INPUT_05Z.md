# Gorrund single-image regeneration input (RM-OT-05Z §2–§4)

This narrows `reviews/rac-rmot05w-source-brief/SUBMISSION_PACKAGE.md` §1 using the 05Y lesson: **one image, one figure, no turnaround sheet**.

Every 05W requirement still applies: `SOURCE_BRIEF.md`, `NEGATIVE_CHECKLIST.md` and `REVIEW_SPEC.md`. Nothing in them is weakened.

Where this file and the 05W §1 prompt differ, **this file wins** for the next image. The differences:
- no briefs is preferred;
- if a garment is unavoidable, it is a fallback proxy;
- the tail roots at the sacral midline;
- the male designation is stated.

## 1. Image format (05Z §2)

The image must have:
- **one** adult male Gorrund, as the **only** figure in the image;
- a **front three-quarter** view, about 30° off front;
- the full body in frame with margin, **both feet fully visible**;
- a plain **mid-grey background** and soft, even light, with no floor shadow;
- **no** panels, alternate views, inset head, turnaround, labels or text.

It should be a PNG of at least 1024 px on the long side.

**Never** submit a front / side / back sheet as one ordinary image. That is exactly what produced the three-body `base_1.glb` (05Y).

## 2. Prompt (paste into the image generator)

> Full-body anatomical concept render of a single adult male of a fictional leonine beastfolk race called the Gorrund — the only figure in the image. Front three-quarter view (about 30 degrees off front), whole figure visible from head to both feet with margin, plain mid-grey studio background, soft even lighting, no floor shadow, no other views, no inset head, no text. Unpainted matte grey clay-sculpture surface, realistic natural anatomy.
>
> Head: an intelligent, calm lion-like head with a muzzle, broad rounded ears and short smooth fur only. No mane, no chin tuft; the neck, shoulders and upper back are fully visible. Neutral expression, mouth closed.
>
> Tail: a long lion-like tail that grows from the body at the base of the spine (sacral midline, exactly centred). It stands clear of the buttocks for its first few centimetres, then hangs naturally behind and slightly to one side, without touching the ground.
>
> Pose: standing straight and relaxed, head level, knees straight but not locked, natural spine. Both feet flat with the heels on the ground, parallel at hip width, toes pointing forward. Arms hanging relaxed slightly away from the body, palms facing the thighs, fingers relaxed and separated.
>
> Body, about 7 ft 6 in tall: massive load-bearing skeletal architecture, not muscle:
> - a very broad **and very deep** rib cage with rounded anatomical sides;
> - a broad, low neck root blending into a wide shoulder girdle that sits on the rib cage;
> - a deep, robust pelvis continuing the torso, with no pinched waist and no wide hip flare;
> - large integrated knees, ankles, elbows and wrists;
> - arms in proportion, fingertips at the upper to mid thigh;
> - large capable five-fingered humanoid hands with ordinary nails;
> - large but proportionate flat plantigrade humanoid feet, each with exactly five ordinary toes with toenails.
>
> Composition: ordinary, healthy, average adult muscle and fat. Smooth, natural soft tissue with no muscle definition lines: no six-pack, no striations, no visible veins, no bulging trapezius, no V-taper, no belly. Not skinny.
>
> Unclothed neutral anatomical reference: smooth, featureless, non-explicit neutral groin like an unpainted mannequin statue. No clothing of any kind, no straps, no jewellery, no equipment.

**Negative prompt / avoid:**
- multiple views, character sheet, turnaround, front side back, reference sheet, multiple figures, inset, text, labels, cropped feet;
- bodybuilder, six-pack abs, muscle definition, striations, veins, bulging muscles, huge trapezius, V-taper, fat, belly, obese;
- ogre, troll, orc, brute, hunchback, crouching, bent knees, bow legs, aggressive pose, snarling;
- mane, long hair, braids, beard, chin tuft;
- clothing, briefs, underwear, shorts, loincloth, belt, armor, bracers, wraps, necklace, jewelry, weapons;
- tail from clothing, off-centre tail;
- paws, claws, talons, digitigrade legs, hooves, oversized feet, giant hands, long arms;
- cartoon, toy.

### Fallback only if the generator refuses an unclothed figure (05Z §3)

Replace the last paragraph of the prompt with:

> Wearing only a minimal smooth seamless low-rise neutral grey modesty covering, sitting below the hip bones; thin, tight, with no waistband, no seams, no folds, no straps, no thickness; the hip bones, lower abdomen and buttock shape remain fully visible.

Even in the fallback, the tail must still emerge from the body at the sacral midline, **above** the covering.

## 3. Saving the image (no credits)

Save it as `E:\Wayfarer-Rodin\Source-Images\Wayfarer Gorrund Neutral Character Reference Sheet.png`. That is the same folder as `C:\Users\Tyler\Wayfarer-Rodin\Source-Images`.

Alternatively, attach it in chat.

Claude then runs the pre-generation image gate (`IMAGE_GATE_05Z.md`) and returns **PASS** or **REGENERATE IMAGE**. **A PASS does not authorize any paid submission** (05Z §5–§6).

## 4. Prompt v2 (after candidate 01 was ruled REGENERATE IMAGE on 2026-10-15; use this version)

Candidate 01 read "massive / load-bearing" as bodybuilder muscle. It also added a chin tuft, a brief-line crease and a profile-turned head. The v2 prompt keeps the §2 format and avoids those trigger words. See `image_gate/candidate_01/IMAGE_GATE_candidate_01.md`.

> Full-body anatomical reference render of a single adult male of a fictional leonine beastfolk race — the only figure in the image. Front three-quarter view (about 30 degrees off front), whole figure from head to both feet with margin. Plain mid-grey studio background, soft even light, no floor shadow, no other views, no text. Unpainted matte grey clay-sculpture surface, realistic natural anatomy.
>
> **Head:** an intelligent, calm lion-like head with a muzzle, broad rounded ears and short smooth fur. Clean chin, no tuft, no beard, no mane. The head faces the same direction as the body, level, looking straight ahead.
>
> **Tail:** a long lion-like tail that emerges from the centre of the lower back (the sacrum). It hangs relaxed behind the body and slightly to one side, clear of the legs, without touching the ground.
>
> **Pose:** standing straight and relaxed, knees straight but not locked, both feet flat with the heels down, feet parallel at hip width, arms hanging loosely slightly away from the body, hands open and relaxed.
>
> **Build:** about 7 ft 6 in tall and big-boned:
> - a broad and very deep rib cage;
> - wide shoulders sitting on the rib cage;
> - a deep, solid pelvis;
> - thick wrists and ankles;
> - large knees and elbows.
>
> His physique is that of an **untrained, average, soft adult who does not exercise**. Smooth skin with **no visible muscle separation anywhere**, a natural soft belly line (not fat), and ordinary arms and legs.
>
> **Hands and feet:** large five-fingered humanoid hands with ordinary nails. Large flat plantigrade humanoid feet, each with exactly five ordinary toes with toenails.
>
> **Groin:** unclothed neutral anatomical reference. A smooth, featureless, non-explicit groin that blends continuously into the thighs, like an unpainted mannequin, with no edge, seam or line across the hips.

**Negative prompt:**
- multiple views, character sheet, turnaround, multiple figures, inset, text, cropped feet;
- bodybuilder, muscular, ripped, athletic, fitness model, superhero, defined muscles, abs, six-pack, pecs, big trapezius, veins, vascular, V-taper;
- obese, fat belly;
- ogre, brute, hunched, bent knees, aggressive pose, head turned sideways, profile head;
- mane, long hair, beard, goatee, chin tuft;
- clothing, briefs, underwear, underwear line, brief line, swimsuit line, tan line, belt, straps, jewelry;
- paws, claws, digitigrade legs, oversized feet, long arms;
- cartoon.

## 5. Prompt v3 (after candidate 02 was ruled REGENERATE IMAGE on 2026-10-15)

Use v2 (§4) with three additions. Details are in `image_gate/candidate_02/IMAGE_GATE_candidate_02.md`.

**1. Build — append:**

> natural sloping shoulders without rounded shoulder caps, visible collarbones, a clearly visible neck of moderate length between head and shoulders, plain smooth upper arms, plain smooth thighs and calves with no bulging muscle shapes — the size comes from big bones and a deep, wide rib cage, not from muscle.

**2. Head — append:**

> face turned in the same direction as the chest, not toward the side.

**3. Negative prompt — add:**

> rounded shoulder caps, big deltoids, trapezius hump, no neck, thick neck, bulging thighs, teardrop quad, bulging calves, strongman, powerlifter, wrestler.

## 6. Prompt v4: full text, use this one (RM-OT-05Z2, 2026-10-15)

**Why v4.** Candidate 03 passed the image gate, but Rodin rebuilt it as muscle plus fat (`Gorrund-Neutral.glb`, `aaeee37b…`; `reviews/claude-rac-rm-ot-05z-gorrund-neutral-source-review.md`).

**What v4 changes.** The author's direction (05Z2 §2) is: slightly less muscle, less soft-tissue bulk, **not chubby**, and keep the large frame.

**What v4 keeps.** Everything that passed in candidate 03.

### Prompt

> Full-body anatomical reference render of a single adult male of a fictional leonine beastfolk race — the only figure in the image. Front three-quarter view (about 30 degrees off front), whole figure from head to both feet with margin, plain mid-grey studio background, soft even light, no floor shadow, no other views, no text. Unpainted matte grey clay-sculpture surface, realistic natural anatomy.
>
> **Head:** an intelligent, calm lion-like head with a muzzle, broad rounded ears and short smooth fur. Clean chin, no tuft, no beard, no mane. The face is turned in the same direction as the chest, level, looking straight ahead. A moderate, clearly visible neck sits between head and shoulders.
>
> **Tail:** a long lion-like tail that grows from the exact centre of the sacrum (the centre of the lower back, above the buttocks). It clears the buttocks immediately instead of lying on them, then hangs relaxed behind and slightly to one side, without touching the ground.
>
> **Pose:** standing straight and relaxed, knees straight but not locked, both feet flat with the heels down, feet parallel at hip width, arms hanging loosely slightly away from the body, hands open and relaxed.
>
> **Build:** a very large-framed, big-boned adult about 7 ft 6 in tall, with a broad and deep rib cage and a robust pelvis, but ordinary untrained soft tissue.
> - Arms and legs are only slim-to-average in muscle thickness relative to his large skeleton.
> - Chest, shoulders, thighs, calves and buttocks are smooth and understated, with no visible muscle separation.
> - Natural sloping shoulders without shoulder caps; a flat, natural chest.
> - Small-to-moderate natural buttocks with little projection, and a flat back of the thighs.
> - The abdomen is flat to gently soft, without a belly or love handles.
> - Knees, ankles, elbows and wrists are large because the bones are large, not because of surrounding muscle.
>
> The body's apparent size comes from skeletal breadth, depth and joint scale, not from muscle or fat. He looks like a naturally very large adult who does not train.
>
> **Hands and feet:** large five-fingered humanoid hands with ordinary nails. Large flat plantigrade humanoid feet, each with exactly five ordinary toes with toenails.
>
> **Groin:** unclothed neutral anatomical reference. A smooth, featureless, non-explicit groin that blends continuously into the thighs, like an unpainted mannequin, with no edge, seam or line across the hips.

### Negative prompt

- **Format:** multiple views, character sheet, turnaround, multiple figures, inset, text, cropped feet.
- **Muscle:** bodybuilder, muscular, athletic, strongman, powerlifter, wrestler, superhero, fitness model, defined muscles, large pecs, deltoid caps, trapezius hump, thick neck, no neck, thick arms, bulging biceps, bulging triceps, abs, six-pack, quad separation, teardrop quads, bulging calves, veins.
- **Fat and bulk:** large round glutes, projected buttocks, love handles, belly, chubby, obese, fat.
- **Posture:** ogre, brute, hunched, bent knees, aggressive pose, head turned sideways.
- **Hair:** mane, long hair, beard, goatee, chin tuft.
- **Clothing:** clothing, briefs, underwear line, brief line.
- **Tail:** tail touching buttock, off-centre tail root.
- **Monster features:** paws, claws, digitigrade legs, oversized feet, long arms.
- **Style:** cartoon.

### Candidate-04 image gate (05Z2 §5)

Run the standard G1–G8 checks (`IMAGE_GATE_05Z.md`), **plus** a side-by-side comparison against candidate 03. Each of the following must hold:

- **C3-1.** Muscle is **lower** than in candidate 03, not merely less defined.
- **C3-2.** Soft-tissue bulk is **lower** at the shoulders, upper arms, thighs and buttocks.
- **C3-3.** The abdomen has **not** become chubby or obese to compensate.
- **C3-4.** The frame cues **remain**: rib-cage depth and breadth, pelvic robustness, joint scale.
- **C3-5.** The tail visibly clears the buttock at the root, if the angle allows that to be judged.

**Result:** **PASS**, or **REGENERATE IMAGE** with one focused correction.

**A PASS still authorizes only preparing the dry run or job.** Any paid submission needs Tyler's explicit approval immediately beforehand, naming:
- the exact image;
- the AssetName;
- the Rodin tier and settings.

If the Rodin website is used, record:
- the tier or model;
- the quality, detail and smoothing settings;
- any other material setting visible before submission.

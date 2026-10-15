# Gorrund neutral source — submission package (RM-OT-05W §4)

**Recommended route (Route A):**

**2D concept image** in Tyler's image generator → checked against `NEGATIVE_CHECKLIST.md` → **one Hyper3D Rodin Gen-2.5-High generation** through the existing PC pipeline `C:\Users\Tyler\Wayfarer-Rodin` → **whole-body source gate** (`REVIEW_SPEC.md`).

This is the route Saurin used: an external sculpt source, then local corrections, then acceptance. It is also the route 05M prepared, but never ran, for the pre-beastfolk Gorrund.

**Not authorized yet:**
- No Rodin credits have been spent.
- No image has been generated.
- No artist has been contacted.

## 1. Step 1 — concept image (Tyler, in his image generator; image credits only)

The image is a **concept for source selection only**. It is not a measured 3D reference. A good 2D image does not establish valid hidden 3D anatomy (order §4).

**Image requirements** (from `SOURCE_BRIEF.md` §3; the 05M single-figure lesson applies):
- one figure only;
- front three-quarter view, about 30° off front;
- plain mid-grey background, soft even light, no floor shadow;
- the whole body in frame with margin, both feet fully visible and flat;
- PNG, 1024 px or more on the long side.

**Prompt:**

> Full-body anatomical concept render of a single adult of a fictional leonine beastfolk race called the Gorrund, standing in a neutral upright pose on a plain mid-grey studio background. Front three-quarter view, the whole figure visible from head to feet with margin. Soft even studio lighting, no floor shadow. Unpainted matte grey clay-sculpture surface, realistic anatomy, highly detailed natural skeletal and soft-tissue anatomy.
>
> Head: an intelligent, calm lion-like head with a muzzle, broad rounded ears with a rounded upper edge, short smooth fur only, and **no mane** — the neck, shoulders and upper back are fully visible. Neutral expression, mouth closed. A long lion-like tail hangs relaxed behind and slightly to the side, clear of the legs, not touching the ground.
>
> Pose: standing straight and relaxed, head level, knees straight but not locked, natural spine, both feet flat on the ground with the heels down. Feet parallel at hip width, toes pointing forward. Arms hanging relaxed, slightly away from the body so they do not touch the torso. Palms facing the thighs, fingers relaxed and separated.
>
> Body: about 7 ft 6 in tall. Identity comes from massive load-bearing skeletal architecture, not muscle or fat:
> - a very broad **and very deep** three-dimensional rib cage with rounded anatomical sides (not boxy, not a barrel);
> - a broad, low neck root blending into a wide shoulder girdle carried on the rib cage;
> - long strong collarbones and large shoulder joints;
> - a deep, robust pelvis that continues the torso without a pinched waist or wide hip flare, with a broad flat sacrum;
> - one continuous load-bearing line from shoulders through rib cage and lower trunk into the pelvis and thighs;
> - large long bones, and large knees and ankles that are integrated, not knobby;
> - arms in proportion, not long, with fingertips at upper-to-mid thigh;
> - large capable five-fingered humanoid hands with ordinary nails;
> - large but proportionate flat plantigrade humanoid feet, each with exactly five ordinary toes with toenails.
>
> Composition: ordinary healthy adult muscle and fat, natural and unexaggerated. No visible six-pack, no bulging muscles, no V-taper, no belly. Not skinny either.
>
> Clothing: only minimal plain grey low-rise briefs sitting below the hip bones. No other clothing, no jewellery, no straps, no equipment.

**Negative prompt / avoid:** bodybuilder, six-pack abs, bulging muscles, V-taper, huge trapezius, fat, belly, obese, ogre, troll, orc, brute, hunchback, crouching, bent knees, bow legs, aggressive pose, snarling, fangs bared, mane, long hair, braids, beard, clothing, loincloth, belt, armor, bracers, wraps, necklace, jewelry, weapons, paws, claws, talons, digitigrade legs, hooves, oversized feet, giant hands, long arms, multiple views, character sheet, turnaround, text, labels, cropped feet, cartoon, toy, mannequin.

**Before spending Rodin credits:**
- check the image against `NEGATIVE_CHECKLIST.md` (A–E);
- regenerate the image as many times as needed (image credits only) until it is clean;
- Claude can review the image if it is saved to `E:\Wayfarer-Rodin\Source-Images\` (a connected folder) or attached in chat.

## 2. Step 2 — Rodin source generation (Tyler's PC; **needs Tyler's explicit approval immediately before submission**)

Facts from `C:\Users\Tyler\Wayfarer-Rodin\CLAUDE.md` and `Scripts\wayfarer-rodin.ps1`, read on 2026-10-14:
- **Tier:** Gen-2.5-High (production tier; any change needs approval).
- **Input:** one image.
- **Key:** `RODIN_API_KEY`, a Windows User environment variable. This session never reads, prints or uses it.
- **Spend rule:** "Never execute any command containing `-Submit` without the user's explicit approval **immediately beforehand**".
- **Duplicate guard:** no job record, manifest or source master exists for the new asset name. The `Jobs\` folder holds only Vael-Male and Vael-Female records; `Source-Masters\` holds only Vael-Male and Vael-Female.
- **Cost:** the Vael-Female job record shows `"consumed": 0.5` for one Gen-2.5-High job. The estimate is therefore **about 0.5 credits for one submission**. This is an estimate, not a guarantee; the current credit balance is not visible from here.

| Item | Value |
|---|---|
| Image file | `C:\Users\Tyler\Wayfarer-Rodin\Source-Images\Wayfarer Gorrund Neutral Character Reference Sheet.png` (`Source-Images` there is a symlink; `E:\Wayfarer-Rodin\Source-Images` appears to be its target, since the Vael source masters sit under `E:\Wayfarer-Rodin\Source-Masters`). The name follows the batch naming convention. |
| AssetName | `Gorrund-Neutral`. Chosen so it cannot be confused with the old recovered `Gorrund-Male` base.glb. |
| Dry run (no credits; Tyler's PowerShell in `C:\Users\Tyler\Wayfarer-Rodin`) | `.\Scripts\wayfarer-rodin.ps1 -ImagePath "Source-Images\Wayfarer Gorrund Neutral Character Reference Sheet.png" -AssetName "Gorrund-Neutral"` |
| Submit (spends credits; **only after explicit approval of exactly this image and AssetName**) | `.\Scripts\wayfarer-rodin.ps1 -ImagePath "Source-Images\Wayfarer Gorrund Neutral Character Reference Sheet.png" -AssetName "Gorrund-Neutral" -Submit` |
| Result | `Source-Masters\Gorrund-Neutral\Gorrund-Neutral.glb` (immutable), with its SHA-256 in `Jobs\Gorrund-Neutral-manifest.json` |
| On failure | Never resubmit automatically. Use `-Resume` only for recovery (CLAUDE.md "Recovery workflow"). |

**After generation:** tell Claude "check for latest instructions" (or say the source is ready). Claude will:
1. copy the source master to a working copy (the original is never touched);
2. render the whole-body and body-only views;
3. run the `REVIEW_SPEC.md` gate and return the source for review.

Claude does no repair before that review.

## 3. Route B — human sculptor commission (alternative; not contacted)

If the author prefers a hand sculpt, `SOURCE_BRIEF.md`, `NEGATIVE_CHECKLIST.md`, `REVIEW_SPEC.md` and the negative-reference sheet are the commission brief as they stand. The deliverables would be:
- one neutral-pose, unclothed (or minimal-proxy), single-mesh body with the leonine head and a separable tail;
- OBJ or GLB in real-world units;
- 229 cm nominal stature, ground at the sole;
- front, side, back and 3/4 turntable renders.

The budget, schedule and choice of sculptor are the author's; no one has been contacted (order §4).

## 4. What is not offered

**Route C — code-built, SDF, capsule or reconstruction body:** not offered. Order §2 and §4 exclude it, and 05L, 05V and Saurin TS9 all show why (`claude-saurin-ts9-reference-anatomy-pass.md` L73: "This is the ceiling of the code-built method").

**A 3D sculpt made by Claude in this session:** also not offered. The 05U desktop-Blender route showed that remote stroke-by-stroke sculpting is workable only for small local repairs, not for building a whole organism. A procedural body saved in a `.blend` is not a sculpt (order §2).

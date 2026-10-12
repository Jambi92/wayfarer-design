# Gorrund male source body: generation package (RM-OT-05M §6)

**Purpose:** one high-quality source body (raw sculpt clay, not canon) for the reference-first Gorrund lineage (GO-RD1-SOURCE). It goes through the existing Wayfarer image → Hyper3D Rodin → GLB pipeline (`C:\Users\Tyler\Wayfarer-Rodin`), as Saurin did.

**Why this package exists:** no male Gorrund Rodin / Hyper3D body exists on the PC (see the gate report's manifest). Claude cannot run the pipeline itself:
- it needs Tyler's PowerShell and `RODIN_API_KEY`;
- each submission spends credits and needs Tyler's explicit approval;
- there is no Gorrund source image yet.

---

## 1. What the source image must be (lesson from Vael)

The Vael run fed a multi-view turnaround **sheet** to Rodin. The result was a 3D relief of the whole sheet (`reviews/claude-rac-12-closure-audit-measurement-plan.md`), with no usable body. The pipeline must not split sheets automatically (pipeline rule). So the Gorrund input must be:

- **one single full-body figure** in one image (no turnaround, no head studies, no swatches, no text, no extra figures);
- **front three-quarter view** (about 30° off front), or a straight front view if the generator can't hold 3/4. Three-quarter gives Rodin the most depth cues;
- **plain neutral mid-grey background**, even soft studio light, no cast shadow on the floor;
- **whole body inside the frame** with margin, feet fully visible on the ground, nothing cropped;
- **relaxed A-pose**: arms hanging about 20–25° away from the body so no limb touches the trunk; palms facing the thighs; fingers relaxed and separated; feet hip-width apart, toes forward;
- **upright neutral stance**: knees straight but not locked, no hunch, head level;
- **clothing**: plain close-fitting dark-grey briefs only. No armor, belts, straps, jewelry, cloth or gear;
- **hair**: very short cropped, or bald. No beard. Nothing over the neck or shoulders;
- **skin**: neutral, even and matte. No tattoos, markings or strong pigment pattern, so Rodin reads form, not texture;
- **resolution**: 1024 px or more on the long edge, PNG.

## 2. Image prompt (paste into the image generator)

> Full-body concept render of a single adult male of a fictional humanoid race called the Gorrund, standing in a relaxed A-pose on a plain mid-grey studio background, front three-quarter view, whole figure visible from head to feet with margin. Neutral soft studio lighting, no floor shadow. He wears only plain dark-grey close-fitting briefs; very short cropped hair; no beard, no jewelry, no gear.
>
> Body design, upright and plantigrade: massive load-bearing skeletal architecture rather than muscle or fat. A very broad and very deep three-dimensional rib cage with radiused, anatomical (not boxy) sides; a broad, low, sloping neck root that blends into a wide shoulder girdle carried on the rib cage; long strong clavicles; large shoulder joints without bodybuilder deltoid caps; no trapezius bulk.
>
> Below the rib cage, a thick, load-carrying lower trunk with only a natural, gentle narrowing; no pinched waist and no belly. A deep, broad pelvis with a broad flat sacral area; buttocks not prominent; strong continuity from the back of the pelvis into the hamstrings.
>
> Large thick-boned femurs; large integrated knees with a broad flat kneecap plane (not knobby); strong shins with a clear front tibial plane; substantial ankles that still taper from the calf; large broad flat-footed feet with five toes.
>
> Arms in proportion to the girdle: broad elbows integrated into the bones, structured forearms, broad functional wrists, large capable five-fingered hands. Arms are not unusually long; fingertips reach the upper-to-mid thigh.
>
> Lean, neutral soft tissue: a fit but not muscular build, no visible six-pack, flat lower abdomen, natural adult proportions for a 7 ft 6 in tall being. Realistic anatomical sculpture style, grey-skinned like an unpainted clay sculpture, highly detailed natural anatomy.

**Negative prompt / avoid:** bodybuilder, V-taper, huge biceps, six-pack abs, fat, belly, obese, ogre, troll, orc, monster, hunchback, tusks, armor, clothing, weapons, multiple views, character sheet, turnaround, text, labels, cropped feet, digitigrade legs, hooves, claws, tail, long arms, stylized cartoon, toy, mannequin.

## 3. Body-only priorities (what a good source must show)

| Region | Must read as |
|---|---|
| Thorax | broad **and** deep, radiused, visibly load-bearing; not a box, not a barrel, not a slab |
| Girdle / neck | broad sloping neck root; girdle sits on the thorax; no cap deltoids, no trap mound |
| Lower axial trunk | carries the thorax into the pelvis; gentle natural minimum only |
| Posterior | broad back, continuous axial load path, substantial sacral platform, no gluteal dominance |
| Pelvis / femur | deep pelvis, large hip joints, coherent lateral thigh plane, no hip outrigger |
| Knee / shank / ankle | large integrated knee, supportive shank with real taper, substantial ankle, large plantigrade foot |
| Elbow / wrist / hand | integrated broad elbow, structured forearm, broad wrist, large capable hand |

## 4. Gorrund negative-reference set (05A–05L)

The source must show none of these:
- rectangular / parallel-column trunk (S1–S4, EA, RF1 run 1);
- box / slab chest;
- barrel cylinder;
- obese deep chest over a belly (S3, 05I);
- hourglass / female torso (RF2);
- bodybuilder V;
- bulb or knob knees, armor joints (RS1 / RS2);
- hip outriggers;
- mannequin "sausage" limbs (RS1 / RS2);
- featureless back;
- carved-groove pseudo-anatomy (RS2);
- Grask high calf, long forearm or long reach.

Judge the generated image against this list **before** spending Rodin credits. Regenerate the image (image credits only) until it is clean.

## 5. Running the pipeline (Tyler, on the PC)

These steps follow the pipeline rules in `C:\Users\Tyler\Wayfarer-Rodin\CLAUDE.md`. The submission spends Rodin credits and must be approved by Tyler immediately beforehand.

1. Save the approved image as:
   `C:\Users\Tyler\Wayfarer-Rodin\Source-Images\Wayfarer Gorrund Male Character Reference Sheet.png`

   This name follows the batch naming convention; the AssetName becomes `Gorrund-Male`.
2. Dry run in PowerShell from `C:\Users\Tyler\Wayfarer-Rodin` (no credits):
   ```
   .\Scripts\wayfarer-rodin.ps1 -ImagePath "Source-Images\Wayfarer Gorrund Male Character Reference Sheet.png" -AssetName "Gorrund-Male"
   ```
3. If the dry run is clean, submit (Gen-2.5-High; spends credits):
   ```
   .\Scripts\wayfarer-rodin.ps1 -ImagePath "Source-Images\Wayfarer Gorrund Male Character Reference Sheet.png" -AssetName "Gorrund-Male" -Submit
   ```
4. The result is `Source-Masters\Gorrund-Male\Gorrund-Male.glb`, with the SHA-256 in `Jobs\Gorrund-Male-manifest.json`. It is immutable; never edit it.
5. Tell Claude "check for latest instructions" (or say the source is ready). Claude then:
   - stages a working copy (GO-RD1-SOURCE stays untouched);
   - runs the §5 suitability gate;
   - does the surgical RD1 sculpt, the internal gate, LOW, the blind gate and the scaffold under RM-OT-05M §7–§26.

**Alternative:** Rodin also accepts several separate single-view images (front, side, back as separate files) for multi-view conditioning. The current script sends one image. Using several views would be a pipeline change that needs Tyler's agreement first (pipeline rule), so it is not proposed as the default.

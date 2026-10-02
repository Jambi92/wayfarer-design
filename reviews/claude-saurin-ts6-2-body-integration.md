# Saurin TS6.2 — Whole-Body Integration (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-ts6-1-body-integration-correction.md`
**Status:** DIAGNOSTIC / NOT FINAL. Returned for Tyler / ChatGPT review. Nothing here is declared final.

**Scope**
- Saurin whole-body integration only.
- The TS6/TS6.1 head is kept unchanged: same `wf_saurin_head61` construction, with only the neck column made polygonal in `wf_saurin_head62`.
- No Pass 2 work and no UE5 work.
- One spec edit, which the directive authorized: the SAU-SILHOUETTE row (see the last section).

Images are in `reviews/images/targeted-sculpt-6-2/`. Both sexes were rendered on the full-character configurations:

| Sex | Display | Tail |
|---|---|---|
| Masculine | D2 hornlets | T5 dorsal ridge |
| Feminine | D4 crest | T3 long gradual |

## Deliverables (directive §9)

| # | Item | File |
|---|---|---|
| 1–5 | Complete character, front / profile / rear / rear 3/4 / front 3/4, scaled | `saurin62_{Masc,Fem}_complete_scaled.jpg` |
| 9 | The same five views as bare clay (no scale relief, one neutral material) | `saurin62_{Masc,Fem}_complete_bare.jpg` |
| 6 | Close rear pelvis / sacrum / tail root (rear, rear 3/4, side), bare and scaled | `saurin62_{Masc,Fem}_close.jpg`, rows 1–2 |
| 7 | Close head → throat → neck → shoulder (profile and 3/4), bare and scaled | `saurin62_{Masc,Fem}_close.jpg`, row 3 |
| 8 | Close torso planes (3/4 front, 3/4 back), bare and scaled | `saurin62_{Masc,Fem}_close.jpg`, row 4 |
| — | SAU-SILHOUETTE straight-front crop, bare clay | `saurin62_{D2_hornlets_Masc,D4_crest_Fem}_SAU-SILHOUETTE_front_crop.jpg` |
| — | SAU-SILHOUETTE before/after (old tail path vs TS6.2 path) | `saurin62_SAU-SILHOUETTE_before_after.jpg` |

The `.blend` and `.fbx` files for both configurations are on Tyler's PC under `RaceBodies/out/SaurinSculpt62_*_full.*`.

## What changed

The pelvis, gluteal region and tail were treated as one problem (§7), and every change below is a shape key on the solved body.

1. **Pelvis / sacral arch** (`saurin_pelvis_v2`, key `WF_SaurinPelvis`)
   - In each horizontal band of the posterior pelvis, the two-lobed human gluteal profile is replaced by one continuous arch. That arch rises into the tail base, which removes the gluteal cleft.
   - Thigh-weighted vertices are protected, so hip and femoral articulation is not flattened.
   - The human buttock and genital-bulge MPFB targets are driven to their decrease ends.
   - A Laplacian relax is run over the anterior groin (non-thigh, near-midline) so no human genital form remains. Sexual anatomy is left unresolved and non-human rather than modelled.

2. **Tail resting path (SAU-SILHOUETTE)**
   - *Old path:* the tail dropped about 30° straight back from the sacrum.
   - *What that caused:* its underside fell below the crotch line inside the thigh gap. From the front this read as a tapered form hanging from the crotch (`..._before_after.jpg`, left pair).
   - *New path:* the root now leaves the sacrum level, and the lateral resting sweep starts at the root. The tail drops only after it has cleared the thigh gap, and then follows the same relaxed gravity curve as before.
   - *Size unchanged:* tail length, base diameter and mass are untouched. It was not shrunk to hide the problem (§6).

3. **Body planes** (`body_planes`, key `WF_SaurinPlanes`)
   - *Torso and neck:* cross-sections are pulled toward rounded octagons (broad plane → transition → adjacent plane). The effect is strongest at the thorax and neck and fades toward the lower trunk.
   - *Limbs:* get lighter planes (upper arm 0.40, forearm 0.50, thigh 0.35, calf 0.55). Flexion zones get less.
   - *Neck flare:* the lower neck flares into the thoracic inlet, with a forward throat plane and a dorsal flare, so the neck widens into the chest instead of meeting the shoulders as a cylinder.

4. **Chest** (`chest_neutralize`, key `WF_SaurinChest`)
   - Cup size is set to 0 for both sexes, and the nipple size/point targets are driven to their decrease ends.
   - Residual relief is relaxed locally. The relax area is centred on the vertices of MPFB's own nipple targets, so it is located by the base mesh, not guessed.

5. **Structural ridges** (`body_structure`): unchanged from TS6.1, with the neck-structure pass on.

6. **Tail-variant scale fix**
   - *Bug:* `saurin_tail_variant` never created the regional scale vertex groups, so every tail variant rendered as smooth clay in the TS5–TS6.1 full and variant sheets, even in the "scaled" views.
   - *Fix:* variant tails now get structural, ventral and root-articulation regions like the default tail.

## Pass-criteria check (§10), honest

| Criterion | Result | Notes |
|---|---|---|
| No human gluteal-cleft read | **Pass** | Rear and rear 3/4, bare and scaled: there is no midline cleft. The posterior pelvis is one arch running into the tail base. |
| No pair of human buttocks with an attached tail | **Partial** | The two-lobe read is gone. In straight rear view, though, the large tail base still reads somewhat as a teardrop laid over the pelvis rather than growing out of it, most clearly on the heavier T3 base. The fix is a broader, flatter sacral-to-caudal fairing, which is better done by hand than by another scripted pass. |
| No genital-like tail silhouette from front neutral view | **Pass (with one small residual)** | With the new path, the tail shows from the front only as a lateral sweep beside the leg, clearly a tail (see the before/after sheet). One very small midline nub remains at the masculine crotch apex where the groin relax meets the thigh seam. It is a hand-sculpt cleanup item, not a tail read. |
| No cylindrical human-neck transition | **Partial** | The neck now flares into a planar throat and thoracic inlet, and in profile the throat line runs continuously into the chest. Remaining issues: the head-to-body join still shows a faint seam/groove ring, the back of the skull still reads as a near-vertical slab over the neck, and the mid-neck is still fairly round in 3/4. |
| Head, neck, torso, pelvis and tail share one design language | **Partial** | The head and tail clearly belong to one organism. The body is closer than in TS6.1 but still reads as a smooth anatomical base under a reptilian head. |
| Large body forms less uniformly rounded, with controlled planar/ridge organization | **Partial / weak** | The planes are there, but at full-character distance they are subtle. In the close 3/4 torso views they read as a slight faceting, not a decisive reptilian plane hierarchy. Pushing the procedural plane weight harder started to look like faceting artefacts rather than anatomy, so we stopped. |
| Articulation remains credible | Pass | Thigh, shoulder and elbow regions are protected or reduced, and the rig and skin weights are unchanged. |
| No excessive dragon armour or spikes | Pass | Ridges are restrained. The dorsal tail scutes on T5 shrink distally and are absent at the root. |
| No permanent crouch or monster posture | Pass | Neutral upright A-pose, 188 cm. |
| No automatic gameplay claims | Pass | None are made. |
| Tail mandatory and customizable | Pass | The tail is present in every render. Variants T2/T3/T5/T6 still work and now carry scale regions. |
| Sexual anatomy unresolved / non-human | **Mostly pass** | There are no human genital or breast forms. A faint residual nipple-site mark is still visible on close bare torso views of both sexes; it needs a hand-sculpt pass. |
| Upright intelligent playable humanoid, unmistakably non-human | Pass at the character level | The head, tail, hands and feet carry this. The body alone carries it less strongly. |

**Most important design test (bare clay).** Would the body alone read as the same reptilian organism as the head and tail?
- *Answer:* not yet fully. Bare clay reads as a lean, non-human-sexed humanoid with a reptilian head and an integrated tail. The torso and limb surfaces are still closer to smoothed human anatomy than to the head's plane language.
- *Recommendation:* following the directive's own rule, continue structural work before adding surface detail. As Tyler chose earlier, that work should be the hand-sculpt pass.

## Recommended hand-sculpt targets (in priority order)

1. **Sacral-caudal fairing.** Make the tail base grow out of a broad, slightly flattened sacral plate in rear view instead of overlapping it.
2. **Head-neck join.** Remove the seam ring, and soften the back of the skull into the nuchal/cervical muscles so it no longer reads as a slab sitting on a tube.
3. **Torso plane hierarchy.**
   - Define the sternal and pectoral plate, a lateral flank plane and a ventral abdominal plate.
   - Taper the lower axial trunk into the pelvis.
   - Use the head's plane and ridge vocabulary throughout.
4. **Small cleanups.** Remove the midline crotch nub and the residual nipple-site marks.

## Spec edit

`specs/saurin/SAURIN_V1.md` §32 validation cast: added the **SAU-SILHOUETTE** row exactly as §6 of the directive requested.
- It covers the neutral straight-front tail-silhouette test.
- It includes the rear-3/4 check that the base is not a tube attached to the posterior.

No other spec text was changed.

— Claude

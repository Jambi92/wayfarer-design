# RAC RM-OT-05AU — Gorrund deferred-item audit on the frozen 05AT body

**Order:** `reviews/chatgpt-rac-rm-ot-05au-gorrund-deferred-item-audit-order.md` (33312a3)
**Source:** `GO-05AT_AC3` (frozen; `.blend` sha `d462f36c…7ea618`, `.glb` sha `8ae6cced…c9fc0d`). All work used the cloud copy of the same vertex data (geometry-identical to the frozen file, verified in 05AT).
**Executor:** Claude. Diagnostics only. Nothing was sculpted, filtered, moved, remeshed or saved, and Blender on Tyler's PC was not opened. The two head mocks in §1 are **render-only copies, labelled NON-AUTHORED / VISUAL ONLY**, and were never written to any `.blend`.

## Verdict

**05AU DEFERRED-ITEM AUDIT COMPLETE / AUTHOR REVIEW REQUIRED**

| # | Item | Recommendation | Author decision needed |
|---|---|---|---|
| 1 | Head share | **KEEP 05AT HEAD SHARE** | yes: visual confirmation only |
| 2 | Tail root | **KEEP 05AT TAIL ROOT** | no |
| 3 | Heel lift | **LOCAL HEEL/FOOT CORRECTION RECOMMENDED** (combine with item 4) | yes: approve the block |
| 4 | Foot size | **LOCAL FOOT-SIZE CORRECTION RECOMMENDED** | yes: approve and pick a target |
| 5a | Genus handles (topological) | Bounded topology repair (3 sites), no morphology change | approve the method only |
| 5b | Morph handles (spec OPEN parameters) | Stay OPEN until creator implementation | no, except the head-ratio note |
| 6 | Other deferred items | Closed by acceptance, or carried to retopology/export | no |
| 7 | Canon identity | No contradiction; feet are the only canon tension (item 4) | no |

The decision matrix with the numbers is in §8.

Evidence is in `reviews/rac-rmot05au-evidence/` (`checks/` for JSON, `views/` for sheets). Scripts are in `tools/rac/w1/rmot05au_drivers/`.

## 0. Reference frame and definitions

- **Stature, AC3:**
  - Bounding box (to the ear tips) 204.52 cm.
  - **Skull vertex 203.80 cm**: highest head point, ears excluded.
  - Vertex stature is the denominator for every "% H" figure below.
- **W1 guide:** `GO_r6` (`reviews/rac-w1i-evidence/geometry/GO_r6.npz`), measured with the W1 tool definitions (`GO_meas.json` r6).
  - Stature 230.897 cm.
  - Only the kept geometry is used; the helper geometry below the sole is excluded. The sole is at z = 0.
  - W1 has no tail, so it is not a reference for item 2.
- **Head height (HH):** the W1 `arm_measure.py` definition. It runs from the vertex (highest head point, ears excluded) to the menton (lowest chin point near the midsagittal plane).
- **Overlay alignment:** W1 is scaled to the same vertex stature (×0.8826). The two are aligned at the sole, on the body midline (x 0.70 cm) and on the pelvis centre in profile.

## 1. Head share

### Measurements (`checks/au_measure_head_feet.json`)

| Metric | GO-05AT_AC3 | W1 GO_r6 |
|---|---|---|
| Vertex stature | 203.80 cm | 230.90 cm |
| Menton z | 175.35 cm | 204.17 cm |
| **HH (menton–vertex)** | **28.45 cm** | 26.73 cm |
| **HH / stature** | **13.96 %** | **11.58 %** |
| HH at equal stature | 28.45 cm | 23.60 cm |
| Head breadth, ears excluded | 25.37 cm | 21.13 cm |
| Bideltoid breadth | 63.77 cm | 63.79 cm |
| Head breadth / bideltoid | 0.398 | 0.331 |

- **Difference:** +2.38 percentage points, so the 05AT head is about 20.6 % taller relative to stature than W1. It is also about 20 % broader relative to the shoulders.
- **Historical pointers (10.5 % current, 12.6 % W1):** not reproduced by this definition.
  - The 05AB/05AB1 "10.5 %" came from the 05AB rig head-bone measure, not from menton–vertex HH.
  - No W1 HH share of 12.6 % exists in `GO_meas.json`; the W1 figure there is 11.58 %.
  - Both 05AB-era numbers also predate the leg lengthening that set the current 204.5 cm stature.
  - The source-checked comparison is therefore 13.96 % against 11.58 %: the head is **larger** than W1, not smaller.

### Views

| View | File |
|---|---|
| Whole body F / P / 3-4 | `views/head_share_whole_sheet.jpg` |
| Head and shoulder crop | `views/head_share_crop_sheet.jpg` |
| Silhouette overlay vs W1, front and profile | `views/overlay_sheet.jpg` |
| Overlay head crop | `views/overlay_headcrop_sheet.jpg` |

**Mocks (NON-AUTHORED / VISUAL ONLY):**
- **Method:** a render-only copy of AC3 with the head scaled about a pivot below the jaw (x midline, z 171.5 cm). A smoothstep blend runs from z 162 to 175 cm, so the upper neck and trapezius are partly scaled. The body below is untouched, so stature drops slightly.
- `mock126`: head ×0.888, giving HH about 12.6 % of its own stature.
- `mock116`: head ×0.807, giving HH about 11.6 %, the W1 share.

### Reading

- **AC3:**
  - The head reads as a substantial leonine head on a very large body.
  - It is neither the "tiny-head giant" nor the "oversized fantasy-ogre head" that the spec rules out (GORRUND_V1, head scale).
  - Most of the extra HH over W1 is muzzle and jaw depth and the deep chin. A human-derived W1 head does not have these, so menton–vertex height runs higher on a lion head.
  - In the overlay, the cranium sits almost exactly in the W1 vault height. The excess is below the W1 chin line and in the breadth of the cheeks and ears.
- **mock116 (W1 share):** reads small for this body. The ears and muzzle crowd together, and the neck and trapezius mass start to dominate the front view. That moves toward the tiny-head-giant read.
- **mock126:** credible too, but it reads slightly less leonine and less imposing. It is a softer alternative, not a correction of a defect.

**Recommendation: KEEP 05AT HEAD SHARE.**

The head-to-height ratio is OPEN in canon, so this is Tyler's visual call. If Tyler prefers a smaller head, the ~12.6 % mock (×0.89) is the most a later local correction should go. Matching W1's 11.6 % is not recommended.

## 2. Tail root

### Measurements (`checks/au_tail.json`; `views/sheet_tail.jpg`, `AC3_tail_*.jpg`)

| Metric | Result |
|---|---|
| Emergence (tail/junction interface centroid) | z 108.32 cm = **52.96 % H**; y −24.68 cm |
| Position vs crotch | about 4.5 % H above the crotch (≈48.5 % H): at the sacral level and the top of the gluteal cleft |
| Midline | interface centroid **+1.42 cm** lateral of the body midline (x 0.70) |
| Interface extent (x × y × z) | 14.3 × 6.2 × 12.6 cm |
| Junction z range | 100.2–117.3 cm |
| Root axis | posterior, about 14° above horizontal, with **9.4° lateral yaw** |
| Fused-root length | **0 cm** |

On fused-root length: the free tail clears the body by ≥ 30 mm at the interface and increasingly beyond (36.6 mm at 2 cm, 41.7 mm at 4 cm, 47 mm at 6 cm). The old "tail fused down the cleft" defect (05AA §9) no longer exists. The "fused root" is just the 05AT junction mound.

**Transition:** the AC3 continuity treatment blends the junction into the sacrum and glutes without a plateau, a shelf or a cleft fusion (05AT §7).

**Comparison:**
- W1 GO_r6 has no tail, so there is no geometric reference.
- Canon (GORRUND_V1, RM-OT-05N): the tail is "integrated with the sacral load path as a species-identity channel". The root position at the top of the cleft over the sacrum matches that.
- Length, taper and tuft are OPEN.

**Reading:** the tail reads as a natural leonine tail origin from the back, profile and 3/4 views. The 1.4 cm and 9° lateral offset is only visible when you look for it. It falls inside the accepted AC3 tail core, so any change would reopen the accepted posterior.

**Recommendation: KEEP 05AT TAIL ROOT.** No correction is recommended.

If the author wants the small lateral offset centred later, the maximum region is the tail core plus the junction (z 100–117 cm, ≤ 8 cm from the interface). It would be a rigid rotation and translation of the free tail about the root, with the AC3 continuity ring re-feathered. That is a rig/pose-level fix, not a sculpt.

## 3. Heel lift

### Measurements (`checks/au_measure_head_feet.json` → `feet`; `views/plantar_profiles.jpg`, `AC3_footL_*.jpg`, `AC3_footR_*.jpg`)

| Metric | Left | Right |
|---|---|---|
| Heel region minimum z (rear 25 % of length) | **0.88 cm** | **1.60 cm** |
| Heel pad minimum, plantar profile | 0.70 cm | 1.37 cm |
| Ball minimum z | 0.00 cm | 0.19 cm |
| Heel lift vs ball | **0.88 cm** | **1.40 cm** |
| Ground-contact span (fraction of foot length) | 0.56–0.96 | 0.72–0.94 |
| Ground-contact vertices | 1 391 | 495 |
| W1 reference | heel 0.49 cm, forefoot 0.00 cm | — |

- **Recalculated raw heel lift:** about 0.9 cm left and 1.4–1.6 cm right. That agrees with the historical "~1–1.6 cm".
- **Asymmetry:** the right foot floats about 1.6–1.9 mm above the floor overall, and its heel sits about 0.5–0.7 cm higher than the left.

**Assessment:**
- **Anatomy:** a small heel-pad clearance is normal (W1 itself has 0.49 cm). A 1.4–1.6 cm lift with no heel contact is not a plantigrade stance. The body stands on the forefoot and toes only.
- **Origin:** a source-pose artifact. It is asymmetric, the left and right feet differ, and it is unrelated to the Gorrund design.
- **Rig and ground-contact risk:** yes.
  - The plantigrade ground plane, foot-roll pivots and IK floor will disagree with the mesh.
  - The right foot will hover or clip.
  - It is cheaper to fix in the mesh now than to compensate in every rig and animation.

**Recommendation: LOCAL HEEL/FOOT CORRECTION RECOMMENDED.**

Suggested scope for a later order:
- Feet and ankles only (below about 25 cm); the lower legs above stay frozen.
- Bring both heels to about 0.3–0.5 cm (W1-like) heel-pad clearance with full heel and ball contact.
- Settle the right foot onto the floor and make the two feet symmetric.

It should be the same bounded block as item 4.

## 4. Foot size

### Measurements (`checks/au_measure_head_feet.json` → `feet`, `feet_W1`; `views/sheet_feet.jpg`, `AC3_whole_sheet.jpg`, `overlay_sheet.jpg`)

| Metric | AC3 left | AC3 right | W1 GO_r6 |
|---|---|---|---|
| Foot length | 39.09 cm | 39.82 cm | 34.84 cm |
| **Length / H** | **19.11 %** | **19.47 %** | **15.09 %** |
| Footprint width | 22.43 cm | 21.75 cm | 12.67 cm |
| **Width / H** | **10.97 %** | **10.63 %** | **5.49 %** |
| Width / length | 0.57 | 0.55 | 0.36 |
| Knee / ankle height | 54.89 / 8.81 cm | 54.81 / 8.70 cm | 62.05 / 9.83 cm |
| Tibial segment | 46.08 cm | 46.11 cm | 52.22 cm |
| **Length / tibial** | **0.848** | **0.864** | **0.667** |
| Minimum ankle circumference | 37.7 cm (18.4 % H) | 38.0 cm (18.6 % H) | 31.6 cm (13.7 % H) |
| Toes | 5 (95 % length) | 5 | 5 |

**Symmetry:** the right foot is 0.73 cm longer, the left 0.68 cm wider.

**Comparison with canon:** GORRUND_V1 Part 2 §50–58 says:
- feet are "large in absolute terms, but foot length is never exaggerated to signal size";
- the forefoot "may be broad but never a rectangular slab";
- feet must not become "oversized monster feet".

**Reading:**
- At equal stature, AC3 feet are about 27 % longer and about 95 % wider than the accepted W1 macro proportions.
- They are also long relative to the short lower leg: length / tibial 0.85 against 0.67.
- In the whole-body front and 3/4 views (`AC3_whole_sheet.jpg`), the feet read as visibly oversized, slab-like and broad. The overlay shows the AC3 footprint far outside the W1 outline, in width especially.
- The heavy ankle (18.5 % H) supports a large-frame read. The foot itself goes past it.
- Prior history: 05AB noted feet at 19.3 % (down from 20.8 %), always with the final judgement deferred. They are still there.

**Recommendation: LOCAL FOOT-SIZE CORRECTION RECOMMENDED.**

Suggested target for author choice (a bounded feet/ankle block, together with item 3):
- **Length:** about 16.5–17.5 % H (≈ 33.6–35.7 cm). W1 is 15.1 %, plus a broad-frame allowance.
- **Width:** about 7–8 % H (≈ 14–16 cm), so width / length ≈ 0.42–0.46.
- **Ankle:** unchanged.
- **Toes:** five toes, nails and non-prehensile form kept.
- **Pivot:** scale about the ankle and heel so the ankle joint, lower legs and the accepted body stay frozen.
- Make the left and right feet symmetric.

The author picks the target inside or outside that band.

## 5. Genus handles / morph handles

### 5a. Topological genus handles

In RM-OT-05 history, "genus handles" means topological genus. The 05X donor review first found genus-2 loops at the axillae. Counts since then: 05Z genus 4, 05Z2 genus 2, 05Z3 genus 3.

**Current AC3 (`checks/au_genus*.json`):**
- Welded: V 499 996, E 1 500 000, F 1 000 000.
- **χ = −4, genus 3.**
- A local-genus scan (r = 6 cm spheres) locates exactly three handles:

| Site | Location (cm) | Nature |
|---|---|---|
| Left hand | (38, −51, 97–101) | finger/thumb contact closes a ring |
| Right hand | (−36.5, −38.6, 96.8) | finger contact loop |
| Left axilla | (23–24, −41..−43, 144–149) | micro-tunnel, hole about 2.9 cm², perimeter about 9.5 cm |

The large section "holes" at the head (z ≈ 197 cm) are ear-bowl concavities with local genus 0, not handles.

**Recommendation:** a bounded topology repair at the retopology or rig-prep stage:
- separate the two finger contacts;
- close the axilla tunnel.

This needs no morphology decision. It is required before skinning, because fused fingers cannot be deformed independently. Tyler only approves the method and timing. It is not a shape choice.

### 5b. Morphology handles still OPEN in canon (GORRUND_V1)

| HANDLE | STATUS | CURRENT EVIDENCE | RECOMMENDATION | AUTHOR DECISION NEEDED |
|---|---|---|---|---|
| Head-to-height ratio | OPEN (head scale table) | 05AT neutral 13.96 % HH; mocks at 12.6 / 11.6 % (§1) | keep 05AT as the neutral midpoint; creator range later | yes: confirm the neutral visually (§1); range can wait |
| Tail length / taper / tuft | OPEN (tail row, RM-OT-05N) | 05AT tail is a viable neutral with a terminal tuft; root KEEP (§2) | stay OPEN until creator work | no |
| Muzzle numeric morphology | OPEN (cranial depth row) | 05AT leonine muzzle is a viable neutral | stay OPEN | no |
| Ear projection / outward extent range | OPEN (ear variables, RM-UF-02) | 05AT broad rounded auricles match the ear identity | stay OPEN | no |
| Final height range | OPEN (Part 1 §98–100) | neutral 204.5 cm (bounding box) | stay OPEN; world validation | no |
| Torso-to-limb / body ratios, frame families | OPEN | 05AT accepted body composition = neutral | stay OPEN until creator envelope | no |
| Pelvic morphology | OPEN | 05AT broad pelvis accepted (AC3) | stay OPEN | no |
| Muscular-development capacity | OPEN | 05AT untrained neutral accepted | stay OPEN | no |
| Sex-related anatomy / dimorphism | OPEN | male neutral only | stay OPEN; a female body is a separate future order | no (now) |
| Dentition / limited tusk-like canines | OPEN | no tusks on 05AT | stay OPEN | no |
| Hand and foot dimensions (separate length/breadth/depth variables) | spec: independent variables | hands viable; feet see §4 | foot neutral should be set by §4 before the range work | yes, via §4 only |

No other handle is invented. Pigmentation, hair, lifecycle and gameplay items are not mesh handles.

## 6. Other historically deferred Gorrund items (repo search of 05AA–05AT orders and gates)

| Item | Logged in | Status now | Recommendation |
|---|---|---|---|
| Heroic soft-tissue composition; elongated heroic thigh forms | 05AB, 05AB1 | resolved by 05AG–05AT; accepted in Tyler's body-composition acceptance | CLOSED |
| Minor gluteal-fold-end crease; thigh-top stretch band at the pelvis weight boundary | 05AB1 | AC3: lower-glute fold soft and continuous; old faint thigh seam line softened (05AT §7) | CLOSED by acceptance |
| Neck length (05AG "do not change") | 05AG | unchanged; reads natural in every view | KEEP; no decision |
| Finger/toe anatomy (05AG "do not change") | 05AG | 5 fingers + 5 toes, ordinary nails, non-prehensile toes | KEEP; finger contact loops repaired with §5a |
| Perineal fold intentionally unwelded | 05AG | still a duplicate-position seam (closed, 0.000 mm) | handle at retopology/export; no decision |
| Pre-existing sliver triangles beside the tail root (quality 0.04) | 05AT §3 disclosure | unchanged, not visible | clean at retopology; no decision |
| Prototype implementation verification; D4 stature writeback | spec §136–137; 05B | out of scope: Stage C / D4 blocked | stays blocked |

## 7. Canon / race-identity check

| Canon requirement | AC3 |
|---|---|
| Beastfolk (RM-OT-05N) | ✓ |
| Leonine head with muzzle | ✓ (§1) |
| Tail present, sacral integration | ✓ (§2) |
| Large skeletal frame, axial load-path continuity, broad pelvis | ✓ (accepted composition; overlay shows a broad, deep axial build) |
| Ordinary/untrained soft tissue, not bodybuilder | ✓ (accepted AC3) |
| Upright plantigrade biped, no digitigrade | ✓ in form; stance is forefoot-only through the heel lift (§3), a fixable artifact, not a design change |
| Five digits per hand and foot | ✓ |
| Feet "large… without becoming oversized monster feet"; length "never exaggerated" | **tension**: the only canon issue found (§4) |

There is no other contradiction. The race is not reinterpreted.

## 8. Decision matrix

| Item | Key numbers (AC3 vs W1) | Recommendation | Max region if corrected | Author decision |
|---|---|---|---|---|
| Head share | HH 13.96 % vs 11.58 % H | **KEEP 05AT HEAD SHARE** | (option only: head above the neck, ≤ ×0.89) | visual confirm |
| Tail root | emergence 52.96 % H, +1.4 cm / 9° off-midline, 0 cm fused | **KEEP 05AT TAIL ROOT** | — | no |
| Heel lift | L 0.88 / R 1.40–1.60 cm; forefoot-only contact; R floats ~1.8 mm | **LOCAL HEEL/FOOT CORRECTION RECOMMENDED** | feet/ankles below ~25 cm | approve |
| Foot size | length 19.1–19.5 % vs 15.1 % H; width 10.6–11.0 % vs 5.5 % H; L/tibia 0.85 vs 0.67 | **LOCAL FOOT-SIZE CORRECTION RECOMMENDED** (target ≈ 16.5–17.5 % / 7–8 % H) | feet below the ankle, pivot at the ankle/heel | approve + target |
| Genus handles | genus 3: two hand loops, one left-axilla tunnel | bounded topology repair at retopology/rig-prep | the three sites only | method/timing |
| Morph handles | spec OPEN list (§5b) | stay OPEN | — | no |
| Other deferred | §6 | closed or carried to retopology | — | no |
| Canon | §7 | no contradiction beyond the feet | — | no |

## 9. State

STOP.

- No correction has been performed.
- Gorrund BODY COMPOSITION: **AUTHOR ACCEPTED / FROZEN**.
- Overall Gorrund mesh: **NOT YET FINAL**.
- Grask E3: FROZEN.
- RM-OT-05: OPEN.
- Stage C: BLOCKED.
- No D4, UE5, production rigging or creator implementation.

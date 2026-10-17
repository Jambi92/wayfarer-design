# RAC RM-OT-05AN — AC2 measured-range finish: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05an-gorrund-ac2-measured-range-order.md` (b3969fc)
**Executor:** Claude. Masks and filters were authored in the Blender 5.2.2 UI on Tyler's PC; cloud scripts were used for validation, simulation, bounded repair and evidence only.

## Verdict

**05AN AC2 MEASURED-RANGE BUILDUP NOT CREDIBLE / STOP — arms**

One authored checkpoint, **GO-05AN_AN1**, was built and gated.

| Region | Result |
|---|---|
| Legs | Quad channels largely neutralised; teardrop substantially reduced; calves visibly softer. Joints stay large and the limbs stay robust. |
| Forearms | Moderately softer. |
| **Upper arms** | **Biceps and triceps still read heroic.** |

Simulations of the two remaining checkpoints show the arms cannot reach "clearly no longer heroic" within the order's limits:
- The inner upper arms lie in contact with the passed torso, which must stay at mask 1.0.
- Opening the arms enough produces 25–35 predicted flips at that contact (§5).
- It also takes **forearm mean radius below −3 %** (−4.4 % at an arm-only +150-iteration step, −5.7 % at +250) while the biceps remain prominent.

Per §14 FAIL ("visual target requires … mean-radius loss > 3 %"), I stopped. No `GO-05AN_AC2` was produced and AC3 was not started.

**Last technically passed checkpoint: GO-05AN_AN1** (§4). One item there needs an author ruling: a single "reference flip" that is in fact a pre-existing crimp being straightened.
- If the author accepts that classification, AN1 is the best AC2 working state (legs done, arms not).
- If not, the fallback is **GO-05AL_AK1**.

## 1. GO-05AM_AK1_predictive_repair revalidation (§3)

| Check | Result |
|---|---|
| source | GO-05AL_AK1, sha verified (`a2336442…`) |
| candidate sha | `cc3adee1…2a24` |
| opened coincident pairs | 0 of 65 639 |
| SI / degenerates / duplicates / locally inverted repair faces | 0 / 0 / 0 / 0 |
| topology | 1 / 0 / 0 |
| protected regions; 05AI torso / glute / pelvis_other | 0.000 mm |
| max move / movement outside the union | 0.5 mm / 0.000 mm |
| patch deviation | 0.394 / 0.438 mm |
| stature / bbox | unchanged |

**Frozen:**
- `GO-05AN_start.blend`, sha256 `90d9b0ffbed1b20cec143435678055f42cc221c653d11dfc11ce4c3246e7d7e0`
- `GO-05AN_start.glb`, sha256 `ba120044a5d4a330cac863dfafa9c68f05ff23506b222d43ca501d5bb30a00a0`

## 2. Feathered mask (UI; `views/an_mask_feather.jpg`, `checks/an_mask_v3_readback.json`)

**Order of operations, in front view:**
1. Clear, limb boxes, invert.
2. Joint bands (elbows, wrists, knees, ankles).
3. **Transition boxes**, expanded past the hard cores: torso +6 px, shoulder tops +12 px, hip +20 px, armpit strips +6 px.
4. Smooth Mask ×3.
5. **Then** the final hard cores (torso, head, shoulder tops, hip/genital, hands, feet, armpits).
6. Right view: tail and top of the feet.

No Smooth Mask was run after the hard boxes.

**How the box sizes were chosen:** a cloud emulator of the UI box masks and Smooth Mask (`maskemu.py`, `maskdesign.py`; mean absolute error 0.012 against the read-back) sized the boxes. Two earlier UI builds (v1: 6 passes, too broad; v2: no torso-edge feather, 64 predicted flips on the inner left arm) were rebuilt; their read-backs are kept in `checks/`.

**Read-back of v3:**

| Check | Result |
|---|---|
| geometry vs GO-05AN_start | 0.000 mm |
| all 05AF protected sets; 05AI torso / glute / pelvis_other | min 1.0, 0 vertices < 1 |
| joint centres | 0.92–1.0 |
| belly means | biceps 0.48 / 0.35, forearms 0.29 / 0.66, thighs 0.17 / 0.16, calves 0.0 |
| thigh-top ramp | 1.0 at 90 cm → 0.94 / 0.71 / 0.16 / 0.02 at 88 / 86 / 84 / 82 cm (smooth; the 05AK mask stepped 1.0 → 0.55) |
| upper arm | 1.0 at 160 cm → 0.17 mid-belly → 0.94 at the elbow band |

## 3. Filter calibration (UI scratch; never advanced)

`GO-05AN_scratch_smooth_calib.blend` is a 30-event UI Smooth Mesh Filter run on the masked working file.

The behaviour fits the model `co ← co + (1 − mask)·(avg(neighbours) − co)` per mouse-move event, with **1 event = 1 iteration** (30 events ≈ 30 iterations, per-vertex correlation 0.991). Simulations in this order use that model.

Simulated Surface Smooth (HC, shape preservation 0.5) is fully shape-preserving on this mesh: limb median ≤ 0.74 mm even after 40 sequential applications. So AN1 used the authorised Smooth Mesh Filter (§8 AN2 alternative), with the radius gate as the anti-slimming guard.

## 4. AN1 — Smooth Mesh Filter, 100 events (authored)

### Predictor before authoring (`checks/an1_prep_repair_log.json`)

The cumulative-reference predictor (`predict_an.py`) judged the exact proposal: 100 iterations with the saved v3 mask.

**Bounded repair:**

| Item | Result |
|---|---|
| neighbourhoods per cycle | 7, 4, 4 (15 total) |
| repair cycles | 3 |
| vertices moved | ≤ 0.5 mm |
| near-coplanar rotations | 29 |
| faces changed | 54, inside the union |
| movement outside the union | 0.000 mm |
| patch deviation | 0.39 / 0.42 mm |
| SI / degenerates / inverted | 0 / 0 / 0 |
| mask after repair | preserved exactly |

**Residual flags:**
- **Face 224765** is the only residual "flip". It was a 77° crimp in the 05AL baseline, and smoothing aligns it 0.1° to its local surface, which puts it 90.3° from its *crimped* base normal. That is **crimp resolution, not inversion.**
- Two further faces resolve the same way.

The repaired file is `GO-05AN_AN1_prep.blend` (sha `8f8058db…05ac4`).

### UI authoring

| Setting | Value |
|---|---|
| Tool | Mesh Filter |
| Filter Type | Smooth |
| Strength | 1.000 |
| Deform Axis | X Y Z |
| Orientation | Local |
| Application | one drag: mouse down, 10 ramp moves (50 px), 90 small moves, mouse up = 100 events |

Saved as **`GO-05AN_AN1.blend`**, sha256 `f058e439e009d704a921f0bc4bdf00c9fa629e7bd491e0d4ed5ebc4d1dc8d531`. The review GLB is `GO-05AN_AN1.glb`, sha256 `90f63f8e3c8347a83185b055e841b709034e0b30cbdd29453a7755ae305bc044`.

### Gate (`checks/an1_gate.json`)

| Gate | Result |
|---|---|
| seams / SI / flips / degenerates vs the AN1-prep state | 0 / 0 / 0 / 0 |
| topology | 1 / 0 / 0 |
| head, tail, tail junction, genital, perineal, hands, feet; 05AI torso / glute / pelvis_other | 0.000 mm |
| stature / bbox | unchanged |
| cumulative from 05AL | median 3.19, p95 6.87, max 14.18 mm (ceilings 8 / 20 / 32) |
| incremental | median 3.30, p95 6.82, max 13.93 mm |
| segment mean radius | upper arm −0.9 / −1.7 %, forearm −1.9 / −1.5 %, thigh −1.2 / −1.3 %, shin −2.3 / −2.5 % (all ≥ −3 %) |
| joint-centre drift | ≤ 0.15 mm (ceiling 0.5) |
| orientation vs 05AL | 1 reference flip, face 224765, classified **CRIMP_RESOLVED** (base ring angle 77°, now 0.1°) |
| local inversions | 3 now vs 5 in the baseline (fewer) |
| transition band / wrist-ankle buffers | 0.92 / 5.38 mm (feathered by design) |

**Visual** (`views/an1_cmp_*.jpg`, at identical cameras across 05AI AC1 | 05AL AK1 | AN1, for whole, body, arms, thighs and calves):
- **Thighs:** quad channels and teardrop largely gone.
- **Calves:** clearly softer in profile and back; the inner gastrocnemius is still a little full from the front.
- **Forearms:** cords reduced.
- **Biceps/triceps:** still heroic.
- **Thigh top:** a **faint thin line** remains at the hip core edge (z ≈ 94 cm), visible at close range. It is much weaker than the 05AM simulation step. One of the two allowed continuity touches could address it, but only on a passing checkpoint, so it was not applied.

## 5. Why AN2/AN3 were not authored

**Inflate (AN3-style volume correction).** I predicted inflate amounts of 1.0, 1.5, 2.0 and 2.5 mm on AN1. 1.0 mm is stable. 1.5 mm and above fold faces at **hard mask edges**: the foot box at z 6.7 cm, where mask jumps 0 → 1 inside one face, and the hand box at z 116 cm. 2.5 mm was not stabilised by 3 repair cycles (`checks/an2_inflate_prep_repair_log.json`), so it was not authored. 1.0 mm alone restores under 1 % radius.

**More arm smoothing.** Simulated arm-only masks with less shoulder/torso feathering (`views/armplan_*.jpg`):

| Arm mask variant | Extra iterations | Predicted flips | Forearm L radius | Biceps |
|---|---|---|---|---|
| (12, 6, 3) | +150 | 1 (+50 > 60° margin) | −4.4 % | modestly softer |
| (6, 3, 2) | +150 | 25 | — | — |
| (6, 3, 2) | +250 | 35 | −5.7 % | still prominent |

The predicted flips cluster at the inner upper arm where it touches the torso core. Every variant fails the −3 % radius limit before the biceps read as ordinary.

**More leg smoothing.** Simulated AN1 + inflate 2.5 mm + 100 iterations (`views/an3plan_*.jpg`) improves the legs a little further, but leaves the arms essentially as in AN1.

## 6. Repair budget used

The order allows 80 neighbourhoods. 15 were used for AN1. The inflate attempt used 11 per cycle × 3, but it was never authored, so it is diagnostic only. No GO-05AN_AC2 was frozen.

## 7. Recommendation

1. **Accept or reject GO-05AN_AN1 as the AC2 working base for the legs and forearms,** given the crimp-resolution classification of face 224765.
2. **Treat the upper arms as a separate, arm-only problem.** The arm/torso contact makes mask-based filtering unstable. Options:
   - hand-sculpt the biceps/triceps in the UI with a tablet (Tyler);
   - or a targeted arm order that permits a small, explicit separation of the inner-arm/torso contact (a geometry change near the passed torso, so it needs author authority), followed by the same calibrated Smooth.
3. Allow one continuity touch for the faint thigh-top line once a checkpoint is accepted.
4. **Feather the hand- and foot-box mask edges** in any future order. They are now the fragile points for any inflate.

## 8. Files

On the PC, in `RaceBodies/source/Gorrund-Neutral-C/05AN/`:

| File | Status |
|---|---|
| `GO-05AN_start.*` | frozen validated candidate |
| `GO-05AN_working.blend` | mask v3 only |
| `GO-05AN_scratch_smooth_calib.blend` | calibration scratch only |
| `GO-05AN_AN1_prep.blend` | bounded repair before AN1 |
| `GO-05AN_AN1.blend` / `.glb` | best checkpoint, author decision |
| `05AN_README.txt` | marks the folder |

Scripts are in `tools/rac/w1/rmot05an_drivers/`: `predict_an.py`, `an_repair.py`, `an_gate.py`, `anmetrics.py`, `maskemu.py`, `maskdesign.py`.

Blender was closed after the work.

## State

**Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED.** No LOW, no blind final acceptance, no scaffold, no D4/UE5/rigging/creator work. AC3 not started.

# RAC RM-OT-05Z — single-image regeneration input: readiness

- **Order:** `reviews/chatgpt-rac-rm-ot-05z-single-image-regeneration-input-order.md`
- **Date:** 2026-10-15
- **Package:** `reviews/rac-rmot05z-input/`
- **Tool:** `tools/rac/w1/rmot05z_drivers/z_single_body_gate.py` (new, read-only)

## Outcome

**STOP AT THE IMAGE GATE: no candidate single-figure image is available yet.**

I checked the following places on 2026-10-15:
- this session's uploads;
- `E:\Wayfarer-Rodin\Source-Images`, which is empty;
- the PC Rodin pipeline folders, which hold only the Vael records and masters.

The input, the image gate and the post-generation intake gate are all ready.

- No image was generated.
- No 3D generation was run.
- No paid submission was made or prepared beyond the documented dry run.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**; canon advancement **NOT PERFORMED**; D4 / UE5 / production rigging / creator **NOT STARTED**.

## 1. 05Y ruling recorded (§1)

`base_1.glb` (`b0214fcf…`) is preserved as immutable **failed-source evidence** on E:, at `RaceBodies/source/Gorrund-Male-05X-R1/`, split into two parts plus `REJOIN.txt`.

Nothing was done with it:
- no figure extracted;
- no figures merged;
- no retopology or sculpting;
- no single-organism reinterpretation;
- no ARM, LOW, blind, scaffold or Stage C work.

The earlier 05X-R1 suggestion to adopt fig2 stays withdrawn.

## 2. Next generation input (§2–§4): `rac-rmot05z-input/IMAGE_INPUT_05Z.md`

This narrows 05W `SUBMISSION_PACKAGE.md` §1 without weakening anything in 05W.

**Format.** One image containing one adult male Gorrund only. Front three-quarter view, about 30°. Full body with both feet visible. Mid-grey background, soft light. No panels, inset head, turnaround or text. A front / side / back sheet is never used as a single input.

**What the prompt keeps:**
- the improved direction: intelligent leonine head (no mane, no chin tuft);
- upright stance with heels down;
- five-fingered hands;
- five-toed plantigrade feet with nails;
- the long tail.

**What the prompt corrects:**
- **Composition:** ordinary reference composition, with no definition lines, six-pack, striations, veins, trapezius bulk or V-taper.
- **Pelvis:** **unclothed, with a featureless, non-explicit neutral groin** (preferred). A garment is used only as a fallback: a seamless, low-rise, thin proxy below the hip bones with no waistband, seams, folds or straps.
- **Tail:** **rooted at the sacral midline, from the body, clear of the buttock at the root**, hanging behind or slightly to the side, not touching the ground.

The negative prompt adds multi-view / sheet terms, all clothing terms, and the off-centre / garment tail root.

## 3. Pre-generation image gate (§5): `rac-rmot05z-input/IMAGE_GATE_05Z.md`

The gate form has:
- the mandatory checks G1–G8: one figure, no bodybuilder build, pelvic landmarks readable, sacral-midline tail, five-toed plantigrade feet, heels down, neutral stance, no mane over measurement anatomy;
- the full 05W negative checklist (A–E).

Its ruling is **PASS / REGENERATE IMAGE**. A PASS authorizes only preparing the dry run and job metadata (§6).

## 4. Paid-generation gate (§6)

**No paid submission is authorized.** If an image passes, the preferred route, when Tyler chooses it, is the existing PC Rodin pipeline:
- tier Gen-2.5-High;
- one image;
- AssetName `Gorrund-Neutral`;
- dry-run and submit commands as in 05W `SUBMISSION_PACKAGE.md` §2;
- estimated about 0.5 credits.

I would prepare the dry run and then **stop for Tyler's explicit approval immediately before** any `-Submit`. Failures are never resubmitted automatically.

## 5. Post-generation intake gate (§7): `z_single_body_gate.py`

The gate runs on any new GLB, including one generated elsewhere, **before** any anatomy review. It checks:
- the exact hash;
- connected components after welding;
- a duplicate-body test: more than one component of at least 50 % of the tallest height fails;
- small extra pieces, which are listed, never dropped;
- nested shells;
- open or non-manifold edges.

**Self-test** (`rac-rmot05z-input/gate_selftest/`):

| Source | Result | Correct? |
|---|---|---|
| 05X `Gorrund.glb` | **PASS** (1 component) | Yes |
| 05Y `base_1.glb` | **FAIL** (3 body-sized components) | Yes |

**Next action (Tyler):**
1. Generate the image from `IMAGE_INPUT_05Z.md` §2.
2. Save it to `E:\Wayfarer-Rodin\Source-Images\` under the name given there, or attach it in chat.
3. Say "check for latest instructions".

I will then run the image gate and stop at PASS / REGENERATE IMAGE.

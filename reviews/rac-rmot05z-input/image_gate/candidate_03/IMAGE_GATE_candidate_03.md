# RM-OT-05Z pre-generation image gate — candidate 03 (prompt v3)

| Item | Value |
|---|---|
| Image | `candidate_03.png`, attached by Tyler in chat on 2026-10-15 at 12:27 |
| Size | 1024 × 1536 px, 1,769,740 bytes |
| SHA-256 | `49b72dfca83d9e2fb58a8560153d3f15de88824d17f95b3c2f563ec26f9c27ba` |
| Detail crops | `candidate_03_detail_crops.jpg` (head, groin, feet, tail) |

## Mandatory items (05Z §5.2)

| # | Check | Result | Evidence |
|---|---|---|---|
| G1 | One figure only | **YES** | Single figure in front 3/4 view, plain mid-grey background, no text, both feet in frame. |
| G2 | No bodybuilder composition | **YES** | Ordinary, smooth, soft composition. No six-pack, striations or veins. No rounded deltoid caps or trapezius hump: the shoulders slope naturally and a short but visible neck separates head and shoulders. Upper arms, thighs and calves are plain, with no bulging or teardrop shapes. The soft belly line is mild, not obese and not an "ogre belly" (B4). |
| G3 | Pelvic landmarks readable | **YES** | Unclothed with a featureless, non-explicit groin. No garment edge or line. Lower abdomen, hip region and thigh roots are visible. |
| G4 | Tail on the sacral midline | **Accepted: hidden root** | Under the v2 rule (`IMAGE_INPUT_05Z.md` §4, candidate-01 record): the tail clearly comes from behind the body, hangs to the side and does not touch the ground. It is not attached to a leg or a garment. **The sacral midline root must be confirmed on the 3D result.** |
| G5 | Plantigrade feet, five toes with nails | **YES** | Both feet show five ordinary toes with nails. Plantigrade and humanoid, no claws, of reasonable size. |
| G6 | Heels down | **YES** | Both feet flat on the ground. |
| G7 | Neutral stance | **YES** (note) | Upright, knees extended, arms hanging slightly away with relaxed hands. **The head is still turned somewhat toward profile.** This is minor and does not block 3D generation. |
| G8 | No mane or hair over landmarks | **YES** | No mane, clean chin, short fur only; neck and shoulders visible. |

**05W negative checklist:**
- **A, B1–B6, C, D:** no rejecting finding.
- **E1** (body identity without the head and tail) **cannot be judged from one 2D image.**

There is a **risk to carry forward**. With the muscle removed, the body may read as a "large, heavy human" unless the 3D result keeps a visibly deep ribcage and a robust pelvis and joints (05A–05C precedent; GO L11, L166). The image alone can't show this. It is the first question for the 3D whole-source review after the single-body gate.

## Ruling

**PASS.**

What a PASS allows (05Z §5–§6): **preparing the dry run and the job metadata only.** A PASS does not authorize any `-Submit` or any other paid generation.

See `DRY_RUN_PREP.md`.

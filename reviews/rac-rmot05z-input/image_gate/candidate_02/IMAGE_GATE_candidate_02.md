# RM-OT-05Z pre-generation image gate — candidate 02 (prompt v2)

| Item | Value |
|---|---|
| Image | `candidate_02.png`, attached by Tyler in chat on 2026-10-15 at 11:17 |
| Size | 1024 × 1536 px, 1,797,946 bytes |
| SHA-256 | `d3c6523e5d9e1722fa9f0c3c12135b5cc474643eb688c14899dadaa25ece7dd6` |
| Detail crops | `candidate_02_detail_crops.jpg`: head, groin, feet, tail |

## Mandatory items (05Z §5.2)

| # | Check | Result | Evidence |
|---|---|---|---|
| G1 | One figure only | **YES** | Single figure, front 3/4 view, plain mid-grey background, no text, both feet in frame. |
| G2 | No bodybuilder composition | **NO** (much improved) | Fixed since candidate 01: no six-pack, no striations, no visible veins; the abdomen is soft and plain. Still present: very large **round deltoid caps**, an **oversized trapezius** sloping from the jaw to the shoulders with almost no visible neck, large biceps / triceps, **bulging separated quadriceps** (a teardrop above the knee) and bulging calves. The size is still carried by muscle, not by the frame (GO L45, L250; RA R-4; checklist B1). |
| G3 | Pelvic landmarks readable | **YES** (note) | Unclothed, with a featureless, non-explicit groin. Candidate 01's sharp brief-edge line is gone. A soft inguinal crease remains: an anatomical fold, not a garment edge. The iliac region is visible. |
| G4 | Tail on the sacral midline | **UNCLEAR** (expected) | The tail comes from behind the right hip, hangs to the side and does not touch the ground. The root is hidden at a front 3/4 angle, so it must be checked on the 3D result. |
| G5 | Plantigrade feet, five toes with nails | **YES** | Both feet show five ordinary toes with nails. Plantigrade, no claws, size within reason. |
| G6 | Heels down | **YES** | Both feet are flat. |
| G7 | Neutral stance | **YES** (note) | Upright, knees extended, arms hanging. **The head is still turned toward profile**, past the body's angle; a minor point. |
| G8 | No mane or hair over landmarks | **YES** | No mane. **The chin tuft is gone**; the chin is clean. Short fur only. |

**05W negative checklist:**
- B1: bodybuilder or strongman mass is still present, in the shoulders, trapezius and thighs.
- A1: cleared. No garment edge.
- C, D: no new failures.

## Ruling

**REGENERATE IMAGE.** This is the closest candidate so far. Only one mandatory item fails, G2: muscle still carries the size, at the deltoids, trapezius and quadriceps. The head turn is a minor note.

No dry run was prepared and nothing was submitted. The image was not put in `Source-Images`.

## The remaining correction (prompt v3, built on v2)

These are the only changes to v2. Everything else that worked stays: the abdomen, groin, chin, feet and single figure.

**Add to the Build paragraph:**
> natural sloping shoulders without rounded shoulder caps, visible collarbones, a clearly visible neck of moderate length between head and shoulders, plain smooth upper arms, plain smooth thighs and calves with no bulging muscle shapes — the size comes from big bones and a deep, wide rib cage, not from muscle.

**Add to Head:**
> face turned in the same direction as the chest, not toward the side.

**Add to the negative prompt:**
> rounded shoulder caps, big deltoids, trapezius hump, no neck, thick neck, bulging thighs, teardrop quad, bulging calves, strongman, powerlifter, wrestler.

If the generator keeps adding muscle at the shoulders and thighs, an author-only option is to rerun it as an image-to-image edit of candidate 02, asking only to soften and reduce the shoulder, trapezius and thigh muscle. That keeps everything else that passes.

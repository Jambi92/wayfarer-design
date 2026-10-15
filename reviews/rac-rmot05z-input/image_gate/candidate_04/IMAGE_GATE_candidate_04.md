# RM-OT-05Z2 candidate-04 image gate (prompt v4)

| Item | Value |
|---|---|
| Image | `candidate_04.png`, attached by Tyler in chat on 2026-10-15 at 13:11 |
| Size | 1024 × 1536 px, 1,877,488 bytes |
| SHA-256 | `abb9160a65e70317f8eada2ee4a83eb43c1b33c96866bdbb11d69031f37c1cb6` |
| Comparison sheet | `candidate_03_vs_04.jpg`: candidate 03 and candidate 04 side by side, same scale |

## Standard checks G1–G8

| # | Check | Result | Evidence |
|---|---|---|---|
| G1 | One figure only | **YES** | Single figure in front 3/4 view, plain background, no text, both feet in frame. |
| G2 | No bodybuilder build | **NO** | Defined deltoid caps, separated pectorals, defined biceps / triceps with forearm veins, a teardrop quadriceps above the knee and bulging calves. |
| G3 | Pelvic landmarks readable | **YES** | Unclothed, featureless groin, no garment line. |
| G4 | Tail on the sacral midline | **Accepted (hidden root)** | The root is hidden at this angle. The tail comes from behind the body and does not touch the ground. |
| G5 | Plantigrade feet, five toes with nails | **YES** | Five toes with nails on each foot. |
| G6 | Heels down | **YES** | Both heels are on the ground. |
| G7 | Neutral stance | **YES** (note) | The head is still slightly turned toward profile. |
| G8 | No mane or hair over landmarks | **YES** | No mane, clean chin. |

## Comparison with candidate 03 (05Z2 §5)

| # | Requirement | Result |
|---|---|---|
| C3-1 | Muscle **lower** than candidate 03 | **NO.** It is higher and more defined: shoulder caps, chest separation, arm definition, quadriceps teardrop, calves. |
| C3-2 | Less soft-tissue bulk at shoulders, upper arms, thighs and buttocks | **NO** at the shoulders, upper arms and thighs. The buttocks cannot be judged at this angle. |
| C3-3 | Abdomen not chubby to compensate | **YES.** The belly is a little flatter than in candidate 03. |
| C3-4 | Frame cues remain | **YES.** Broad chest, robust pelvis, large joints. |
| C3-5 | Tail clears the buttock at the root | Cannot be assessed at this angle. |

## Ruling: REGENERATE IMAGE

**One focused correction:** do not generate a fresh text-to-image. **Edit candidate 03 instead.**

Candidate 03 is already the correct image for everything except muscle volume. Each fresh text-to-image round re-rolls the build, and the "big-boned / large-framed / robust" wording keeps pulling it back toward muscle (compare candidates 01, 02 and 04).

In the image generator's edit or image-to-image mode, start from `candidate_03.png` (`49b72dfc…`) with low-to-moderate strength, and ask only for:

> Keep the same figure, head, pose, proportions, camera, lighting, tail and feet exactly. Only reduce muscle volume: make the shoulders, upper arms, forearms, thighs and calves noticeably slimmer and smoother (slim-to-average limbs on the same big skeleton), soften and flatten the chest, keep the abdomen flat to gently soft. No new muscle definition, no veins.

Run the same gate on the result, including the comparison with candidate 03.

No dry run was prepared and nothing was submitted.

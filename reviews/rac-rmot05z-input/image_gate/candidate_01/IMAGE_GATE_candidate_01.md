# RM-OT-05Z pre-generation image gate — candidate 01

| Item | Value |
|---|---|
| Image | `candidate_01.png`, attached by Tyler in chat on 2026-10-15 |
| Size | 1024 × 1536 px, RGB, 1,859,118 bytes |
| SHA-256 | `e6d141b07e10aac0bb3cc7df08e38eec95b5504b6f264e19efa31fce84097985` |
| Detail crops | `candidate_01_detail_crops.jpg` (head, groin, feet, tail), made for this review only |
| Image source | Not stated. Not needed for this ruling. |

## Mandatory items (05Z §5.2)

| # | Check | Result | Evidence |
|---|---|---|---|
| G1 | One figure only | **YES** | A single figure on a plain mid-grey background. No panels, inset head, turnaround or text. The figure is in front three-quarter view with both feet in frame. |
| G2 | No bodybuilder composition | **NO** | Extreme bodybuilder build: very large pectorals and deltoids, a massive trapezius rising to the jaw, a deep V-taper, separated abdominal blocks, vascular forearms and hands, and grossly enlarged, separated quadriceps and calves. The prompt's "massive load-bearing" wording seems to have been turned into muscle (checklist B1). |
| G3 | Pelvic landmarks readable | **UNCLEAR** | Unclothed, with a featureless groin. But a sharp **brief-outline crease** runs from the lower abdomen over the hips to the thighs, like the edge of a fused garment. Generated 3D would likely turn it into another fused brief surface (checklist A1; 05X / 05Y precedent). The iliac region above the line is visible. |
| G4 | Tail rooted on the sacral midline | **UNCLEAR** | The tail appears from behind the right hip and hangs to one side, clear of the ground. **The root is hidden** at this camera angle, so a front 3/4 image cannot show it. It will need checking on the 3D result. |
| G5 | Plantigrade feet, five toes with nails | **YES** | Both feet show five ordinary toes with nails. Plantigrade and humanoid; no claws. The feet are large but not monstrous. |
| G6 | Heels down | **YES** | Both soles appear flat on the ground. |
| G7 | Neutral stance | **YES, with a note** | Upright, knees extended, arms hanging slightly away. **The head is turned toward profile**, well past the body's 3/4 angle, and the hands are partly curled. Minor, but a level, forward head is preferred. |
| G8 | No mane or hair over measurement anatomy | **NO (minor)** | No mane, and the neck and shoulders are visible. But there is a **chin tuft / goatee**, which the prompt excluded and R-8 forbids (no facial hair). |

## 05W negative checklist

| Item | Finding |
|---|---|
| **B1 bodybuilder** | **Yes, reject** |
| **A1 garment-like edge** | **Risk**, from the brief-outline crease |
| C1–C8 | No box or barrel trunk, no ogre legs. Feet within bounds. |
| B2 brute | Not hunched. The trapezius mass is large. |
| D | Surface looks sculptural and continuous; no assembled pieces |
| E1 | Not assessable from one image |

## Ruling

**REGENERATE IMAGE.**

Reasons:
- **G2 fails.** Bodybuilder composition; this is the same blocker as 05X / 05Y.
- **G8 fails.** Chin tuft.
- **G3 is unclear** because of the garment-like brief line.
- **G4 cannot be shown** in this view.

What is better than the earlier candidates: one figure, no clothing, five-toed plantigrade feet, heels down, no mane.

No dry run was prepared and nothing was submitted (05Z §5–§6). The image was **not** placed in `Wayfarer-Rodin\Source-Images`, so it cannot enter a batch by accident.

## Prompt changes for the next attempt

These are input wording only; no canon change. The image generator reads strength and size words as muscle, so the next prompt (`IMAGE_INPUT_05Z.md` §2, v2 below) should:

1. **Drop** "massive", "load-bearing", "powerful", "strong" and "heavy". Say instead:
   - "big-boned, broad and very deep rib cage, thick skeleton";
   - "an **untrained, average, soft adult physique** with no visible muscle separation, like an ordinary person who does not exercise".
2. **Add explicit negatives:**
   - bodybuilder, muscular, ripped, defined muscles, abs, six-pack, pecs, big trapezius, veins, vascular, V-taper, athletic, fitness model, superhero;
   - chin tuft, goatee, beard;
   - underwear line, brief line, swimsuit line, tan line.
3. **Groin:** "smooth, featureless, non-explicit groin blending continuously into the thighs, like an unpainted mannequin, with **no edge or line** across the hips".
4. **Head:** "head facing the same direction as the body, level, looking straight ahead".
5. **Tail root:** a front 3/4 view cannot show it. Keep "the tail emerges from the centre of the lower back (sacrum)" in the prompt, and verify it on the 3D result. The image gate will accept a hidden root as long as the tail is clearly behind the body and not attached to a leg or garment.

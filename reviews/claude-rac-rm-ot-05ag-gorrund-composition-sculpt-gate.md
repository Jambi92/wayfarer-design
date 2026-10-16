# RAC RM-OT-05AG — Gorrund composition sculpt from 05AF: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ag-gorrund-composition-sculpt-order.md` (41f4523).
**Date:** 2026-10-16.
**Evidence:** `reviews/rac-rmot05ag-evidence/`.

## Outcome

**05AG AC1 NOT CREDIBLE / STOP**

- Reverted to 05AF: the 05AF baseline was never modified (sha `6ef02c29…`).
- No AC2 or AC3.
- No Q1/Q2 review.

## AC1 (UI only)

### Method

- Opened the 05AF baseline in Blender with File > Open; saved the working copy `GO-05AG_working.blend`.
- Masks: same four Box Masks as 05AE (head/neck edge at about 171 cm, both arms below the shoulder cap, hips and below), then **Mask > Smooth Mask** once.
- Smooth (0.5): abs, pec split, lower-pec shelf, **plus new passes on both trapezius slopes** close to the head mask edge.
- Flatten (0.35): both pecs and the deltoid fronts with double passes; chest profile and deltoid cap in the right view.
- Smooth from the three-quarter view: serratus, flank, lateral abs, lower-pec edge, pec–deltoid groove.
- Saved `05AF\GO-05AG_AC1.blend` (sha256 `3f53d859dd12a98a5977824f22e6246007c100d5e3bdc82a09bafe155c61dbf5`).

### Gates (`checks/ac1_gates.json`)

| Gate | Required | Result |
|---|---|---|
| Topology vs 05AF | identical | **identical** |
| Stature / bounding box | unchanged | **unchanged** (204.5225 cm) |
| Degenerate faces | 0 | **0** |
| Tail / tail junction / genital / hands / feet / perineal fold | unmoved | **0.000 mm** |
| Head (above 172 cm) | unmoved | **moved up to 2.63 mm** |
| Opened seams | 0 | **10 pairs at z 172–174 cm** (head-side seams, unwelded by design) |
| Self-intersections | 0 | **41, all at z 172.0–174.1 cm** |
| Flipped faces | 0 | **3**: the same three lower-pec / armpit faces that flipped in 05AD and 05AE |
| Components / boundary / non-manifold | 1 / 0 / 0 | 3 / **46** / 0 (from the head-side openings) |
| Moved band | — | z 115.7–174.4 cm; max 12.3 mm |

### Visual

`views/ag_ac1_compare.jpg`:
- abs and serratus largely neutralized;
- pec split softened;
- no crease lines along old seams;
- pec mass and deltoid cap moderately reduced.

This is a clear improvement over 05AF in the torso. It does not count, because the technical gates failed.

## Causes

1. **Head-side leak.** **Smooth Mask** softens every mask edge, including the head mask placed at about 171 cm, so a few millimetres above 172 cm became partly sculptable. The new **trapezius Smooth strokes**, which run right up to that edge, then reached the head-side seams. Those seams are protected and unwelded by design (05AF head = PROTECTED_INTERFACE). In 05AE, which had no trap strokes, movement above 170 cm was at most 0.03 mm.
2. **Three recurring flips.** The same three faces flip under any smoothing in every attempt so far (05AD, 05AE, 05AG):
   - (15.9, −54.1, 146.1)
   - (13.0, −56.2, 146.3)
   - (−19.3, −40.9, 153.2)
   They are almost certainly sliver or fold faces already in the baseline.

## Recommendation for the next order (author ruling)

- **Head edge.** Either keep the head mask hard (no Smooth Mask on the head edge, or apply Smooth Mask before adding the head box), with no trapezius strokes within about 3 cm of it, or leave the trapezius untouched in AC1.
- **The 3 recurring flip faces.** Either pre-mask them, or authorize a tiny Edit-mode continuity fix on them before sculpting so the gate can reach 0 flips.

## Files

- `05AF\GO-05AG_working.blend` and `05AF\GO-05AG_AC1.blend`: evidence only, **not promoted**.
- 05AF baseline `.blend` / `.glb` unchanged.

## Housekeeping (Tyler's request: close windows)

- Closed my Blender window and the leftover 05AB1 window from this morning.
- One older Blender window (empty splash screen, from this morning's bridge drop) does not respond to input. A File Explorer window from this morning is also still open. Both are left for Tyler to close.

## State

- Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

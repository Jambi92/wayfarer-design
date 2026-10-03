# Saurin Gate 6 Pass 2: Structural Corrections (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-gate6-pass2-directive.md` (9f14fad)
**Base:** Gate 6 Pass 1, `e2e61af`. **Stopped for author review.** No Gate 7, no surface-richness pass.

**Images** are in `reviews/images/saurin-gate6p2/`:

| Required item | File |
|---|---|
| 1. Identical before/after whole-body cameras (Pass 1 vs Pass 2) | `g6p2_01_whole_body.jpg` |
| 2. Pelvis/tail root: front, rear, profile, rear 3/4, front 3/4, low rear 3/4, underside | `g6p2_02_pelvis_tail_root.jpg`; tail re-curve detail in `g6p2_03_tail_recurve.jpg` |
| 3. Head scale +0 / +6 / +9 % in whole-body context | `g6p2_04_head_scale.jpg` |
| 4. Naked skull after refinement (at +6 %) | `g6p2_05_skull.jpg` |
| 5. Shoulder/arm and hindlimb integration | `g6p2_06_limbs.jpg` |
| 6. Silhouette comparison | `g6p2_07_silhouette.jpg` |
| 7. Geometry accounting | `g6p2_08_accounting.jpg`, `g6p2_accounting.json`, §6 |
| 8. Newly discovered contradictions | §7 |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_gate6p2.npz`: full resolution. 1,091,995 vertices, 2,183,986 triangles. It is watertight: 0 boundary, 0 non-manifold, 0 orientation conflicts, 1 component.
- `SaurinGate6p2_Integration.blend` / `.fbx`: decimated to 1.09 M triangles so the files fit the transfer limit. Deviation from full resolution is 0.08 mm at most.

**Scripts:** `tools/rodin/gate1/`
- `g10.py`: the Pass 2 field.
- `wf_saurin_head64.py`: the scale wrapper.
- `wf_saurin_head63.py`: the skull. Pass 2 version; the Pass 1 version is kept as `wf_saurin_head63_pass1.py`.
- `blur6.py`: adds the arm/thigh zones.
- `assemble11.py`, `ev7.py`, `ev7r.sh`, `compose7.py`, `dec7.py`.

## 1. Posterior pelvis and proximal tail origin (rebuilt volume, not bands)

**Before:** the back of the pelvis was only ±12–16 cm wide from F −15 to −30, barely wider than the tail. The tail therefore read as a separate cone.

**Pass 2:** one continuous **sacral-caudal volume**, a superelliptic sweep (n = 2.6) blended into the body with a 5 cm fillet. It is a single mass, so there is no buttock pair and no cleft.

| Station | Half-width | Character |
|---|---|---|
| Sacrum, F −6 | ±17 cm | Dorsally flattened (sacral platform) |
| F −26 | ±13.5 cm | Tapering |
| F −56 | ±6.8 cm | Matches the free-tail section, with a 10 cm tapered cap |

- Its **ventral half is kept above the neutral pelvic floor**. A first trial hung below the floor and read as a crotch mass; it was flattened before the build.
- The Pass 1 caudofemoral and iliocaudal masses now sit on this volume. They read as part of the pelvic architecture: tail → sacral base → hip → femur.
- The tail root is materially wider than the free tail and narrows gradually into it, with no step.

## 2. Proximal free-tail curvature (unlocked)

- **Bend:** an exact-length bend about the tail root (F −26, U 92) in the sagittal plane. It starts at 0° at the root, ramps to **20° by about 30 cm**, and is rigid beyond that. Because the rotation depends only on radius it is exactly invertible, and **tail length is unchanged**; the tail is not shortened.
- **Result:** the tail now runs back nearly horizontally as a counterbalance. It **no longer hangs centrally between the legs**: in the front and rear silhouettes the dangling section is gone (`g6p2_07`, red).
- **Depth:** overall depth grows from 149.4 to 161.1 cm. That is the same tail extended backward, not added length.

## 3. Head scale +6 % (diagnostic)

- **Method:** the head is scaled uniformly by **1.06 about a pivot on the cranial roof**. The whole skull, eyes included, scales together, so rostrum-to-cranium proportions are exact (the snout is not enlarged independently). The skull top stays fixed, so **standing height is unchanged** at 187.89 cm.
- **Comparison:** `g6p2_04` shows +0 %, +6 % and +9 % with identical cameras in whole-body context. These are composites of the Pass 1 body with each head; the small shoulder marks are composite seams.
- **Observation:** at full-body distance, +6 % reduces the small-head-on-humanoid-body read, and **+9 % reads slightly more balanced** against the thoracic/shoulder mass. Per the directive, **+6 % is built** and +9 % is documented, not silently chosen. A 1.08–1.09 test after the skull settles is worth a look.

## 4. Naked skull at the corrected scale

No horns, crests or display.

| Priority | Change |
|---|---|
| Orbital-temporal organization | Temporal line strengthened (0.15 → 0.26), heavier postorbital bar, deeper supratemporal fossa |
| Maxillary/rostral planes | Sharper canthal and jugal plane breaks; larger maxillary swelling over the tooth row |
| Rear skull into neck | Firmer transverse occipital ridge; longer, deeper nuchal crest running into the Gate 3A nuchal mass |
| Jaw | Kept deep and closed, as in Pass 1 |
| Proportions | Compact projecting rostrum preserved. Still no frog domes; not a human mask, dragon head or generic lizard |

## 5. Upper-arm and thigh mass redistribution

- **Method:** a **45–50 % mix toward a 3.5 cm low-pass** of each limb's own surface, along the upper-arm and thigh shafts. The weight fades out before the shoulder root, elbow, hip and knee, and the thigh mix is kept off the pelvic midline. A **2.5 mm outward offset** keeps girth: this redistributes mass, it doesn't thin the limb.
- **Effect:** the biceps/triceps and quad-belly read is softened into longer, more continuous masses. Strength and silhouette are kept (upper arm moves 1.7 cm at most).
- **Unchanged:** elbow, forearm, hand, knee, lower leg and foot.

## 6. Accounting (every Pass 2 vertex vs the Pass 1 surface)

| Region | Median | 95th pct | Max | Note |
|---|---|---|---|---|
| Free tail (F < −45) | 12.0 cm | 30.2 cm | 36.9 cm | Rigid-length re-curve |
| Pelvis / tail root (U 66–100) | 0.7 mm | 3.1 cm | 5.3 cm | New posterior pelvic volume |
| Torso (U 100–150) | 0.0 | 1.9 cm | 3.2 cm | Sacral platform onto the lower back |
| Skull | 2.6 mm | 8.6 mm | 1.3 cm | +6 % scale and refinement |
| Neck | 0.0 | 1.8 mm | 3.9 mm | Seating around the larger skull |
| Arms + hands | 0.0 | 2.5 mm | 1.7 cm | Upper arm only |
| Legs below the thigh (U 17–66) | 0.0 | 0.1 mm | 1.0 mm | Unchanged |
| Feet | 0.0 | 0.0 | 1.0 mm | Unchanged |

- **Height:** 187.89 cm (unchanged).
- **Width:** 90.56 cm (unchanged).
- **Depth:** 161.1 cm (was 149.4).
- **Seams:** they fall only where the field is unchanged (feet at U 17, forearms/hands beyond |x| 27.5). The largest zip gap is 1.24 cm, seam relaxing moved at most 3 mm, and 342 floating debris vertices were dropped.

## 7. Newly discovered contradictions and open items

1. **Hip width.** The front of the sacral volume adds a little breadth at the hips in front view (`g6p2_07`, blue at the hips). It reads as pelvic platform, but reviewers should check that it doesn't drift toward a broad-hipped human read. Narrowing the F −6 station from ±17 to about ±15 is the obvious adjustment.
2. **Depth envelope.** Depth grew by 11.7 cm. Any later capsule, animation or game-space assumption that used the old 149 cm depth is affected.
3. **Rear sacral surface.** From straight behind, the new volume is a large, smooth sacral shield. That is structurally right but plainer than the rest of the body. It's a target for the surface-richness pass, which per the directive is not started.
4. **Head scale.** +6 % helps; +9 % may be the better value (§3). This is an author decision.
5. **Proximal tail bend.** The ramp zone, 4–30 cm behind the root, shows a gentle kink on the tail's underside in profile. It's acceptable for diagnosis; a longer ramp would smooth it.
6. **Limb redistribution is deliberately conservative** (about 50 %). If reviewers still see bodybuilder bellies, the same mechanism can go further without changing the skeleton.

**STOP: Gate 6 Pass 2 checkpoint. Not advancing to Gate 7 without author review.**

— Claude

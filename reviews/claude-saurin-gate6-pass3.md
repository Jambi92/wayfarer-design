# Saurin Gate 6 Pass 3: Convergence (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-gate6-pass3-convergence-order.md` (fc44946)
**Base:** Gate 6 Pass 2, `40176c6`. **Stopped.** No Gate 7, surface richness, scales, pigmentation, horns/crests, rigging, animation or UE5. **Head scale is not chosen here.**

**Images** are in `reviews/images/saurin-gate6p3/`:

| Required item | File |
|---|---|
| Full front, profile, rear, front 3/4, rear 3/4, low rear 3/4 (Pass 2 vs Pass 3, identical cameras) | `g6p3_01_whole_organism.jpg` |
| Pelvis/tail root close views: front, rear, profile, rear 3/4, front 3/4, low rear 3/4, underside, tail profile | `g6p3_02_pelvis_tail_root.jpg` |
| Naked skull multi-view: front, profile, front 3/4, rear 3/4, top, underside, rear | `g6p3_03_skull.jpg` |
| Head scale +6 / +8 / +9 % with the refined skull, whole body | `g6p3_04_head_scale.jpg` |
| Limbs (integration check) | `g6p3_05_limbs.jpg` |
| Silhouette vs Pass 2 | `g6p3_06_silhouette.jpg` |
| Accounting | `g6p3_07_accounting.jpg`, `g6p3_accounting.json`, §5 |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_gate6p3.npz`: full resolution. 1,100,465 vertices, 2,200,926 triangles. It is watertight: 0 boundary, 0 non-manifold, 1 component.
- `SaurinGate6p3_Convergence.blend` / `.fbx`: decimated to 1.10 M triangles. Deviation from full resolution is 0.75 mm at most.

**Scripts:** `tools/rodin/gate1/`
- `g10.py`: the Pass 3 field. The Pass 2 version is kept as `g10_pass2.py`.
- `wf_saurin_head63.py`: the Pass 3 skull. Earlier versions are kept as `_pass1` and `_pass2`.
- `wf_saurin_head64.py`: the scale wrapper.
- `assemble12.py`, `ev8.py`, `ev8r.sh`, `compose8.py`, `dec8.py`.

## 1. Proximal tail curvature

- **Bend:** still an exact-length bend about the tail root (F −26, U 92), but the ramp now runs **0° → 22° over about 62 cm** instead of 0° → 20° over about 30 cm. Root-to-free-tail curvature is now continuous, and the mechanical kink is gone (`g6p3_02`, tail profile).
- **Length:** unchanged.
- **Position:** the free tail moved only 1 cm median (3.7 cm at most) relative to Pass 2. It keeps the Pass 2 rearward counterbalance direction.
- **Front view, honest note:** the tail runs back behind the legs with its underside at about U 70–75, below crotch level (about U 88). It is **not** dangling: no portion hangs down between the legs. But in a straight front view its far underside is still visible through the gap between the thighs, as in Pass 2. Lifting the whole tail a further 4–6° would clear that if wanted.

## 2. Sacral-caudal / pelvic integration

- **Width:** the sacral station is narrowed from ±17 to **±15 cm** (and ±16 to ±14.5 cm at F −16), as proposed in Pass 2. The tail base is still clearly wider than the free tail, and there is less hip widening than in Pass 2.
- **Load paths:** the Pass 2 "shield" now carries surface-conforming paths laid **on** the volume:
  - **iliosacral bands:** ilium → sacrum → dorsal tail;
  - **caudofemoral longus:** tail → posterior proximal femur;
  - **caudofemoral brevis:** lower and shorter;
  - an **iliofemoral rim** from the posterior ilium onto the hip;
  - a low **sacral/caudal neural-spine line**.
- **Result:** the posterior mass now reads as tail → sacral base → pelvis → femora, rather than a cone set on the pelvis.
- One continuous volume: no buttock pair, no cleft, no crotch mass. The pelvic floor is unchanged and neutral.

## 3. Naked skull (structural pass, no display)

**Front view:**
- The brow shelf moves outward and up, so it overhangs the orbit laterally; the eye sits under it instead of on top.
- The postorbital bar and jugal flare outward, giving a triangular orbital-temporal front silhouette.
- The rostral tip is slimmer, the premaxillary pad smaller, and the nares smaller and dorsolateral.

**Plane hierarchy:**
- The jugal now runs as two segments: a flare under the orbit, then a sweep **into the quadrate/hinge**. Its old free rear end was the ear-like knob seen in rear 3/4.
- The mandibular ramus, angle and jowl are pulled in.
- The flat temporal-plane cut (an ear-shaped disk) and the auricular cup are removed.

**Cranial-to-nuchal:** the rear cranial stations are lowered (the occiput is 0.5–1.4 cm lower) so the roof slopes into the nuchal mass instead of doming over it.

**Profile:** kept, including the compact projecting rostrum (same length).

## 4. Head-scale convergence (+6 / +8 / +9 %, refined skull)

- `g6p3_04` shows the three scales with identical cameras: whole body front, profile, front 3/4 and rear 3/4, plus head-on-thorax front and profile.
- **Method:** uniform scale about the cranial-roof pivot, so standing height is unchanged (187.88 cm), rostrum-to-cranium proportions are unchanged, and the snout is not scaled independently.
- **What each row is:** +6 % is the built mesh. +8 % and +9 % are the same body with the head/neck above U 161 re-meshed at that scale (a diagnostic splice above the shoulders).
- **Observation, not a choice:** the differences are small at full-body distance. +8 % and +9 % sit slightly better against the shoulder/thoracic mass in front and front 3/4. **No value is selected here.**

## 5. Accounting (every Pass 3 vertex vs the Pass 2 surface)

| Region | Median | 95th pct | Max |
|---|---|---|---|
| Free tail | 9.8 mm | 2.8 cm | 3.7 cm |
| Pelvis / tail root (U 66–100) | 0.0 | 1.1 cm | 2.7 cm |
| Torso (U 100–150; sacral station narrowing) | 0.0 | 5.2 mm | 1.3 cm |
| Skull | 0.4 mm | 4.4 mm | 8.7 mm |
| Neck | 0.0 | 0.0 | 0.1 mm |
| Arms + hands | 0.0 | 0.0 | 7.8 mm (upper-arm seam band only) |
| Legs (U 17–66) | 0.0 | 0.05 mm | 0.7 mm |
| Feet | 0.0 | 0.0 | 0.9 mm |

- **Height:** 187.88 cm (Pass 2: 187.89).
- **Width:** 90.56 cm (unchanged).
- **Depth:** 161.5 cm (Pass 2: 161.1).
- **Seams:** they fall only where the field is unchanged (feet at U 17, forearms/hands locked by distance to their skeleton). The largest zip gap is 2.06 cm, and seam relaxing moved at most 6 mm.

## 6. Convergence audit

1. **Does the tail look biologically inevitable?** Closer than any pass so far. The root is wider than the free tail, tapers continuously, and is tied into ilium and femur by load paths. The plainest remaining area is the straight rear view of the sacral volume, which is surface-richness territory.
2. **Does posterior mass flow tail → sacral base → pelvis → femora?** Yes, as built. The iliosacral and caudofemoral paths now visibly run that way (`g6p3_02`, rear, rear 3/4, low rear 3/4).
3. **Any renewed human buttock, cleft or genital/crotch read?** No cleft and no crotch mass. **Watch item:** from straight behind, the caudofemoral bands form rounded masses either side of the tail root. They are load paths, not a buttock pair, but this should be checked. Lowering their height or splitting them into longer slips is the fix if needed.
4. **Counterbalance rather than appendage?** In profile, 3/4 and rear 3/4, yes: it runs back from a broad root with continuous curvature. In straight front view its underside is still visible through the leg gap (§1).
5. **Does the naked head read as Saurin without display?** Improved in front and rear 3/4: no frog domes, no ear knob, a triangular orbital-temporal read, and the jugal tied into the hinge. Remaining: from straight behind, the cranial vault still reads as a fairly simple rounded mass.
6. **Limbs: integrated or human bellies?** The Pass 2 redistribution is kept, and the caudofemoral paths now insert on the posterior femur, tying the thigh to the tail. The upper arm still shows Gate 5 path detail; no new human bellies.
7. **Any approved Gate 6 gain regressed?** None found: height, stance, hands, feet, neck and torso map are unchanged, and the neutral pelvic floor is kept. **New minor items:**
   - a small rounded nub at the hip in profile, where the iliofemoral rim and the caudofemoral longus meet;
   - the rear sacral volume is still smoother than the rest of the body.

**STOP: Gate 6 Pass 3 diagnostic package. Awaiting the Gate 6 closure decision and head-scale selection.**

— Claude

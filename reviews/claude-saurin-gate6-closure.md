# Saurin Gate 6: Closure Verification

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-gate6-closure-order.md` (c460926)
**Base:** Gate 6 Pass 3, `8a6aa5d`. Closure pass only; no broad anatomy work. DESIGN / DIAGNOSTIC, no UE5.

**Images** are in `reviews/images/saurin-gate6-closure/`:

| Required item | File |
|---|---|
| 1. Whole organism: front, profile, rear, front 3/4, rear 3/4 (Pass 3 vs closure, identical cameras) | `g6c_01_whole_organism.jpg` |
| 2. Pelvis/tail root: rear, profile, rear 3/4, low rear 3/4, underside | `g6c_02_pelvis_tail_root.jpg` |
| 3. Naked head: front, profile, front 3/4, rear 3/4 (+6 % vs frozen +8 %) | `g6c_03_head.jpg` |
| 4. Silhouette | `g6c_04_silhouette.jpg` |
| 5. Change accounting against Pass 3 | `g6c_05_accounting.jpg`, `g6c_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_gate6_closed.npz`: full resolution. 1,119,404 vertices, 2,238,804 triangles. It is watertight: 0 boundary, 0 non-manifold.
- `SaurinGate6_Closed.blend` / `.fbx`: decimated to 1.12 M triangles. Deviation from full resolution is 0.75 mm at most.

**Scripts:** `tools/rodin/gate1/`
- `g10.py`: the field. `HEAD_SCALE=1.08`, `CLOSURE=1`; with `CLOSURE=0` it reproduces Pass 3 exactly (max difference 0.0, checked).
- `efield.py`, `assemble13.py`: field-difference surgery.
- `ev9.py`, `ev9r.sh`, `compose9.py`, `dec9.py`.

## What was done

1. **Head scale frozen at +8 %.** The Pass 3 skull is scaled uniformly by 1.08 about the cranial-roof pivot. Rostrum-to-cranium proportions are unchanged, and the skull top is fixed, so height is 187.88 cm (unchanged). No other skull change.
2. **Caudofemoral redistribution.** Pass 3 had one broad, high caudofemoral longus plus a brevis, which read as paired rounded masses from the rear. It is now:
   - **two longer, lower, tensioned slips** (dorsal and ventral), each running from caudal base to posterior proximal femur;
   - a **flattened brevis**.

   The load path stays legible from the tail to the femur, and the broad sacral/caudal volume is untouched.
3. **Hip nub.** The nub was measured at (±17, −14, 91.5): two older (Pass 1) path origins that the narrower Pass 3 sacral station had exposed.
   - **Fixes:** the iliofemoral rim now starts behind the hip-stabilizer origin, and the nub is smoothed with a shallow, broad local push matched to its measured height.
   - An earlier, stronger push left a small crater and was rejected.
   - **Result:** the nub now reads only as a faint soft fold in profile.
4. **Method.** Only vertices whose field actually changed (by more than 0.8 mm) were re-surfaced: the head and the posterior pelvis. Everything else is the Pass 3 mesh, copied bit for bit. The largest seam gap is 2.6 mm, and seam relaxing moved copies 1.7 mm at most.

## Change accounting (every closure vertex vs the Pass 3 surface)

| Region | Vertices | Bit-identical | Median | 99th pct | Max |
|---|---|---|---|---|---|
| Head-scale region (head + upper neck) | 118,412 | 70,053 | 0.0 | 3.0 mm | 4.3 mm |
| Posterior-pelvic closure region | 437,551 | 333,367 | 0.0 | 9.8 mm | 14.9 mm |
| **Everything else** | **563,441** | **563,441** | **0.0** | **0.0** | **0.0** |
| … free tail beyond F −75 | 49,361 | 49,361 | 0.0 | 0.0 | 0.0 |
| … legs and feet (U < 55) | 184,903 | 184,903 | 0.0 | 0.0 | 0.0 |
| … torso / arms / shoulders (U 115–150) | 227,217 | 227,217 | 0.0 | 0.0 | 0.0 |

- **Height:** 187.88 cm.
- **Width:** 90.56 cm.
- **Depth:** 161.48 cm.

All three are identical to Pass 3. A pixel difference of the front views shows changes only at the head and the hip flanks.

## Required answers

- **Is the head now frozen at +8 %?** **Yes.** Uniform scale of 1.08 about the cranial-roof pivot, with the Pass 3 skull and unchanged proportions.
- **Does the tail remain biologically inevitable?** **Yes.** Tail length, rearward counterbalance direction, the continuous ~62 cm proximal ramp, the narrowed sacral station and the root taper are all untouched; the free tail is bit-identical.
- **Does posterior mass still flow tail → sacral base → pelvis → femora?** **Yes.** The iliosacral bands are unchanged, and the caudofemoral slips still run from the caudal base to the posterior proximal femur (`g6c_02`, rear 3/4 and low rear 3/4).
- **Is any human buttock, cleft or genital read present?** **No.** There is no cleft, the pelvic floor is neutral and unchanged, and there is no crotch mass. The paired rounded rear masses are reduced to directional slips.
- **Did the caudofemoral correction remove the paired rounded rear read without erasing its load path?** **Yes.** From straight rear and low rear 3/4 the masses now read as longer, lower slips; the path from caudal base to femur stays visible.
- **Did any previously accepted Gate 6 anatomy regress?** **No.** Everything outside the head and posterior-pelvic regions is bit-identical to Pass 3, and the accepted skull is only rescaled. The only residual note is the faint soft fold where the hip nub was, which is surface-level.

## GATE 6 CLOSED

Stopped. Not proceeding to the next gate until the author reviews this closure package.

— Claude

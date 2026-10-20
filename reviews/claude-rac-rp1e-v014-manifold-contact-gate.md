# RAC RP1E — v014 manifold-contact gate (ruling `chatgpt-rac-rp1e-v014-manifold-contact-topology-ruling.md`)

**Date:** 2026-10-20
**Starting state:** v013 (`GO_U_REF_RP1E_retopo_v013.blend`; `designs/design_v013.npz`)
**Result line:** **RP1E MANIFOLD-CONTACT TOPOLOGY FAILED / AUTHOR DECISION REQUIRED**

The ruling makes M1 (the R hand B–C visible handle) a local gate that must pass "before continuing".

- **What worked.** I built M1 as a true manifold tunnel:
  - one component, closed, manifold, genus 1;
  - 0 coarse self-intersections;
  - L1 regional self-x 0;
  - the hidden internal digit sheets are gone (interpenetration amplitude 8.1 → ~1.1 mm; product → source max 10.4 → 1.7 mm).
- **What did not.** Regional L4 self-x stayed between 487 and 965 pairs across five topology and target variants. The final-resolution remap fallback (§10) did not remove the contacts either.
- **Consequence.** Following the ruling's M1 stop instruction, I did not continue to M2–M6 and did not promote a v014. v013 remains authoritative; v009–v013 are unchanged. Blender was not opened this session.

The measurement items ruled in §8 and §9 are done (§3–§4 below).

## 1. M1 — R hand B–C visible handle

### 1.1 Topology built (`tools/rac/rp/rp1e/junction.py`; specs in `exp_v017_manifold/`)

- **Previous state (v013).** Digit C's tube was extended into the fused block and capped. Digit B's curled tip already covers the right half of the block. The two met only by contact: 818 pairs, 8.1 mm interpenetration.
- **M1 change.** Digit C's cap is removed. Its last ring is joined to a 6-face disk cut from digit B's −x side (`m1_tf.json`), using an arc-fraction cell strip, with one intermediate ring at 0.3 or 0.4 (unsnapped).
- **Topology** (`M1_cage_topology.txt`): 5471–5483 V, closed, 0 non-manifold, 1 component, **Euler 0 (genus 1)**, 0 coarse self-x.
- **The visible slit is preserved.** No web fills it and the fusion is not cut.

### 1.2 Results (region radius 3 cm around (−33.0, −40.0, 93.3); feature deviation within 2 cm; `M1_table.txt`)

| Variant | L1 regional self-x | L4 regional self-x | L4 hand-R feature max | Notes |
|---|---|---|---|---|
| v013 (G13), contact only | 5 | 843 | 3.65 mm | amp 8.1 mm, internal sheets |
| M1A: junction, plain targets | 2 | 965 | 3.25 | 788 pairs in the slit (gap 1.26 mm) |
| M1B: junction + B/C targets stripped of the other digit's colour (3.5 cm) | 310 | 19824 | 4.61 | Broke the colour seam; rejected |
| **M1C**: junction + B/C targets stripped only of the facing slit wall (normal ±y) | **0** | 515 | 3.39 | Slit-tip taper 343 (amp 1.15 mm) + junction top seam 163 |
| M1D03: M1C + 0.3 intermediate ring | 8 | 548 | 2.55 | — |
| M1D04: M1C + 0.4 intermediate ring | 13 | 487 | 2.50 | Best L4 |

The amplitude drop and the product → source drop show the hidden overlapping sheets are gone. Two clusters remain (`M1_handle_L0_L1_L4.png`):

1. **Slit-tip taper** (−33.0, −40.6, 92.6): opposed B-wall / C-wall product sheets.
   - The source walls converge to the slit tip at x ≈ −33.0, where the source gap goes from 1.26 mm to 0.
   - In the cage, the junction cell ring sits 3–7 mm further toward C (x −33.3…−33.8) than the source tip. Between the two, both product sheets are projected into a wedge thinner than an L4 face and cross.
2. **Junction top seam** (−33.45, −37.9, 93.0): no opposing source sheet.
   - This is a 2-sheet overlap at the seam between the C ring and the B hole on the top surface of the block.

### 1.3 Final-resolution patch fallback (§10) — attempted

**Tool** (`tools/rac/rp/rp1e/remap.py`). It cuts out a connected disk patch of the L4 production quads (holes filled; checked to be a disk). The patch connectivity and boundary vertices are kept, so the weld to the surrounding mesh is exact. The interior vertices are re-placed on the frozen source:

1. The patch boundary is projected onto the source.
2. A closed source cut loop is built from shortest paths between the projected points.
3. The source region is the enclosed component.
4. Both disks are mapped to the unit circle by mean-value-weight embedding, with matching boundary arc length.
5. Each production vertex takes the source point with the same (u, v).

**Results on M1D04:**

| Patch | Result |
|---|---|
| Slit-tip, r = 1.3 cm | Removes the slit-tip cluster in one sequence, but contacts move to the patch rim: 507 at (−34.1, −40.7, 93.8), 382 at (−32.6, −40.4, 92.1) |
| Junction-seam patch, r = 0.8–1.2 | Leaves 154–357 pairs at the seam |
| One patch over the whole junction, r = 1.8 | 1334 total; 267 + 129 + 93 regional pairs remain inside the patch |
| Larger patches, r ≥ 2.2 | Not disks; the patch wraps the through-slit |

**Mechanism.** Around the through-slit, a production disk large enough to contain both walls and the junction does not match the enclosed source region's topology. The source cut loop encloses one wall plus the slit tip, while the production patch also holds the facing wall. So part of the patch is mapped onto the wrong sheet and still crosses. A collision-separation post-pass (`sepfix.py`, pushing opposed sheets back along their own normals) was also tried on the whole L4 mesh: 1166 → 1010 pairs, not converging, so it was rejected.

### 1.4 What would close M1 (author decision)

Either of these needs a ruling or more scope than the M1 gate allows:

- **(a) Cage: seat the slit tip.** Move the junction seam onto the source slit-tip line. This means re-authoring the B/C crotch-to-fusion facing walls as one slit band whose floor is the shared crease at x ≈ −33.0 (rule §4.2), instead of a tube-to-side junction.
- **(b) Final resolution: explicit side masks.** Build the patches with explicit source side masks for the B wall and C wall (§6) and remap each wall separately onto its own mask. This avoids the disk-topology mismatch.

Both are a full rebuild of the B/C facing-wall topology.

## 2. M2–M6

Not started: the ruling makes the M1 gate a precondition for continuing. The v014-ruling pilot evidence (`exp_v016_pilots/`) still applies:

- per-sheet ownership fixes the deviation of the thumb fin and the axilla knob;
- the zero-self-x requirement is not met at their tapers or stitches.

## 3. T-6 as ruled (§8) — measured on v013

**Method** (`tools/rac/rp/rp1_landmarks_t6.py`):

- exact clipping of every section segment at the landmark radius circle;
- the connected-curve rule for the hips;
- applied identically to source and production, for all landmarks and tail stations.

| Landmark | Drift (mm) | Status |
|---|---|---|
| tail_00 | 1.122 | > 1.0, reported |
| tail_05 | 1.119 | > 1.0, reported |
| hip_R | 0.086 | — |
| hip_L | 0.177 | — |
| shoulder_L | 0.204 | — |
| tail_12 | 0.786 | — |
| All others | ≤ 0.79 | — |

None is above 1.5 mm, so **T-6 PASSES** on v013 under the ruled implementation, with tail_00 and tail_05 reported (`exp_v017_manifold/T6_v013_clip_hipcomp.json`).

## 4. Nails (§9)

The recovered tooling is accepted as the production nail gate (`tools/rac/rp/rp1e/nailcheck.py`, `nail_tooling/`). v013 is unchanged: 7/8 nails are 0.18–0.71 mm short. The nail free-edge repair was not reached, because of the M1 stop.

## 5. D masks (§3)

The explicit seeded flood-fill masks (tunnel, void) were not built in this session; that work follows M1–M6. The resolution-dependent beam masks are retired as ruled.

## 6. Author decisions needed

1. **M1 route:** (a) re-author the B/C facing walls as a slit band with its shared crease floor at the source slit tip, or (b) allow the final-resolution remap with explicit per-wall source masks (§1.4).
2. **Continuation:** whether M2–M6 should proceed in parallel with M1, given that the same taper/stitch mechanism is expected there.

## 7. Evidence

- **`reviews/rac-rp1e-evidence/exp_v017_manifold/`:**
  - M1 specs (`m1j*.json`, `m1_rings.json`, `m1_tf.json`) and cage topology;
  - sim logs and classifications M1A–M1D04;
  - `M1_table.txt`;
  - slices `M1_handle_L0_L1_L4.png` and `M1_v013_vs_junction_vs_finalremap.png`;
  - T-6 result.
- **Tools** (`tools/rac/rp/rp1e/`): `junction.py`, `tgstrip.py`, `remap.py` (final-resolution patch remap), `sepfix.py`, `pairclus.py`; also `tools/rac/rp/rp1_landmarks_t6.py`.

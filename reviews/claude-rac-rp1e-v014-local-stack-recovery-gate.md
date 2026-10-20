# RAC RP1E — v014 local projection-stack recovery gate (ruling `chatgpt-rac-rp1e-v014-local-stack-and-contract-ruling.md`)

**Date:** 2026-10-20
**Starting state:** v013 (`GO_U_REF_RP1E_retopo_v013.blend`, sha 230c7b3a…d778; `designs/design_v013.npz`)
**Result line:** **RP1E LOCAL PROJECTION-STACK RECOVERY FAILED / AUTHOR DECISION REQUIRED**

None of the three pilots reached regional L4 self-x = 0 (§11). Per-sheet ownership (P1) does fix the visible deviation of the two thin-fin pilots:

- L axilla knob: 4.39 → 1.95 mm;
- R thumb-web fin: 2.41 → 0.21 mm.

But every P1 and P1 + P2 variant left 150 to 1,000+ opposed-sheet pairs in the pilot region. The ear-rim pilot got worse under P1 and P2. As §11 directs, I stopped here:

- no v014 cage was promoted or imported;
- no blind topology refinement was resumed;
- v009–v013 are unchanged.

The measurement and tooling items of the ruling were completed and are reported in §3–§5. They are needed for any later gate.

## 1. Method actually tested

### P1 — per-sheet ownership (`tools/rac/rp/rp1e/own.py`)

1. For each pilot region, take the source faces of the region's base-colour targets within a radius Rs.
2. Split them into two sheet targets by the sign of n·d, where d is the feature's side axis. Faces with |n·d| ≤ dead belong to both sheets (crest).
3. The other targets are unchanged: the new target prefix `tgx_<tag>/t_c*.npz` links them.
4. Region cage vertices take the sheet colour from the sign of n_cage·d. Crest vertices keep the base colour.
5. There is no later whole-body pass on these colours. In this stack every projection is a per-colour Shrinkwrap with a vertex group.

### P2 — local modifier order (`sim.py`)

`REGCOLS` and `REGV` remove the region colours from the final-level Project. They also take the region vertex group out of every Smooth modifier (the SMR rounds and the final regional smooth). The region is left with Subdivision → its own Nearest only.

### Support topology

Only support already shown to improve deviation was reused:

| Pilot | Support |
|---|---|
| Knob | Graded refinement 1.8 / 1.0 cm (as in v013 trial RG_Lax) |
| Fin | 2-level support (in v013) plus the fin band (FN1 geometry), or 3-level support with the crest aligned to the fin (RG1 geometry) |
| Ear rim | Refinement 1.8 / 1.0 cm (as in v013 trial RI_rim1) |

### Metrics (`pilot_eval.py`)

- feature deviation max (source points within 1 cm) at L1 and L4;
- self-x pairs within the region radius;
- new self-x elsewhere (more than 3 mm from any v013 pair);
- total.

The baseline is G13, the v013 gate run.

## 2. Pilot comparison tables (`reviews/rac-rp1e-evidence/exp_v016_pilots/`)

### Pilot 1 — L axilla knob (24.17, −39.04, 143.56)

A 5 mm-wide fin-like ridge pointing up. It sits 4 mm below the hanging pinch sheet of the deferred void. Region radius 3 cm; general limit 3.0 mm.

| Variant | L1 dev | L4 dev | Region self-x L1 / L4 | New elsewhere L4 | Total L4 |
|---|---|---|---|---|---|
| v013 stack (G13) | 5.40 | 4.39 | 0 / 0 | — | 1492 |
| Support only, v013 stack (PA0) | 4.91 | 4.09 | 133 / **8291** | 147 | 10062 |
| **P1**, d = x, support (PA1) | 3.67 | **1.95** | 9 / **150** | 40 | 1771 |
| P1 + P2 (PA2) | 3.49 | 1.78 | 9 / 181 | 95 | 1861 |
| P1 with a plane cut at the pinch (PA3) | 3.67 | 1.95 | 18 / 769 | 147 | 2540 |
| P1 + P2 with the cut (PA4) | 3.49 | 1.78 | 18 / 776 | 147 | 2547 |
| P1 with D-void faces removed from the targets (PA5) | 3.67 | 1.95 | 9 / 177 | 428 | 2261 |

- **P1** turns the knob from a miss into a pass (1.95 mm, below the 3.0 mm general limit). It also cuts the support-induced crossing from 8,291 to 150 pairs.
- **The remaining contacts** sit at the pinch mouth (23.6, −40.7, 145.3). There the source is a zero-gap slit into the deferred void, gap 0.38 mm. The pilot fails the regional self-x = 0 criterion.
- A first ruling-style D mask was tried: target faces with no exterior visibility near the void were removed (PA5). It does not remove these pairs and adds contacts elsewhere (§4).

### Pilot 2 — R thumb-web fin (−32.5, −47.0, 104.7)

A membrane about 2 mm thick and 3 mm proud. Region radius 2.5 cm; hand limit 1.5 mm.

| Variant | L1 dev | L4 dev | Region self-x L1 / L4 | New elsewhere | Total L4 |
|---|---|---|---|---|---|
| v013 stack (G13) | 5.29 | 2.41 | 0 / 1 | — | 1492 |
| Fin band on support, v013 stack (PB0) | 2.52 | 1.39 | 44 / 1442 | 0 | 2930 |
| **P1** (walls own sheets, d = wall normal (0.86, 0.30, 0.41)) (PB1) | 1.15 | **0.21** | 36 / 794 | 0 | 2282 |
| P1 + P2 (PB2) | 1.14 | 0.21 | 36 / 1546 | 0 | 3034 |
| P1, ownership on band vertices only (PB3) | 1.15 | 0.21 | 17 / 808 | 0 | 2296 |
| 3-level support, v013 stack (PC0) | 5.18 | 2.36 | 0 / 0 | 0 | 1488 |
| 3-level support + crest-aligned loop + P1 (PC1) | 3.85 | 0.89 | 9 / 1005 | 0 | 2493 |

- **P1** represents the membrane: 0.21 mm at L4, and it survives L1 (1.15 mm).
- **What remains is opposed-sheet contact, not crossing.**
  - With the band (PB1/PB3), 794–808 pairs at (−32.1, −46.96, 104.45), dot −0.98, source gap 2.75 mm. This is a fold of the band-to-patch stitch cells; the L0/L1 slices show the cell faces tangled around the band.
  - Without the band (PC1), 680 + 325 pairs where the membrane tapers to zero thickness at its ends. Amplitude 0.03 and 1.48 mm.
- **Repair attempts.** I tried a local cage relaxation of the band patch (`fitcage.py` with the per-sheet targets) and apron rings (0.25–0.6 cm). Both gave 17–124 coarse self-x, so they were rejected before simulation.

### Pilot 3 — L ear rim (12.7, −50.7, 200.6)

A rim curl. Region radius 2 cm; head limit 1.5 mm.

| Variant | L1 dev | L4 dev | Region self-x L1 / L4 | New elsewhere | Total L4 |
|---|---|---|---|---|---|
| v013 stack (G13) | 10.52 | 1.94 | 0 / 0 | — | 1492 |
| Support only, v013 stack (PE0) | 8.34 | **1.15** | 2 / 517 | 14 | 2020 |
| P1, d = (−0.6, −0.2, 0.77) (PE1) | 8.45 | 1.27 | 7 / 2548 | 71 | 4108 |
| P1 + P2 (PE2) | 8.47 | 6.41 | 8 / 3373 | 81 | 4943 |
| P1, d = normal principal axis (−0.41, −0.25, 0.88), dead 0.1 (PE3) | 8.94 | 1.58 | 6 / 4042 | 481 | 6012 |

- The rim's two sides cannot be separated by one normal axis: the curl's normals rotate through about 180°.
- With per-sheet ownership by normal sign, cage vertices get the wrong sheet and are pulled across the curl.
- P2 (no smoothing, no Project) leaves the rim under-resolved: 6.41 mm.

### Conclusion of the pilot matrix

| Feature type | Viable? | Reason |
|---|---|---|
| Thin positive membrane / fin (pilots 1 and 2) | P1 fixes the exterior deviation but **not viable** | Contact remains where the membrane tapers below the L4 face (about 1 mm) or ends in a zero-gap slit, and at the stitch between the band and the coarse patch |
| Facial rim / overhang (pilot 3) | **Not viable** | Normal-sign ownership is not a consistent side split on a curl; P2 under-resolves |

No single method works on all three pilot types, and no variant reaches regional self-x = 0. So §11's "projection-stack route fails" branch applies.

## 3. T-6 measurement correction (§7)

**hip_R** (`tools/rac/rp/rp1_landmarks_comp.py`). Same plane, radius and length-weighted centroid as before, with one extra step:

1. The section segments are grouped into connected curves (union-find on coincident end points).
2. The curve with the smallest distance to the landmark plane point is kept.
3. The identical rule is applied to source and candidate.

On v013 (G13):

| Measure | Value |
|---|---|
| hip_R drift | **0.086 mm** (was 6.98 mm with the R hand included) |
| Kept curve length | 84.01 cm in both source and candidate |
| hip_L drift | 0.177 mm |

The hand curves (46.8 / 52.5 cm before) are excluded consistently.

**Tail stations.** These use the existing length-weighted method, as ruled. On v013:

| Station | Drift (mm) | Status |
|---|---|---|
| tail_00 | 1.112 | > 1.0, reported |
| tail_09 | 1.265 | > 1.0, reported |
| tail_12 | 1.506 | **> 1.5, still a T-6 failure** |
| All other stations | ≤ 0.90 | — |

- The connected-component rule is not used for the tails. The source tail section splits into partial curves, which would give 30 mm artefacts.
- **Diagnostic only, not a waiver.** Clipping the segments exactly at the radius circle (instead of keeping them by midpoint) gives a maximum of 1.12 mm (tail_00, tail_05) and nothing above 1.5. This suggests the tail_12 value comes partly from where the 7 cm radius window cuts the arc.

## 4. D-zone accounting (§2.4) — finding

I built a deterministic exterior-visibility mask (`tools/rac/rp/rp1e/dmask.py`). A source vertex counts as interior if none of 162 icosphere rays escapes to 200 cm. The rays start from p + 0.03 cm·n and use a parallel beam of radius BR.

The mask turns out to depend strongly on BR:

| BR | Void interior verts | Tunnel interior verts | Void over-limit points in D | Tunnel over-limit points in D | Largest over-limit miss left outside D |
|---|---|---|---|---|---|
| 0 | 131 | 78 | 99 / 162 | 77 / 101 | 14.2 / 9.8 mm |
| 0.3 mm | 181 | 100 | 123 / 162 | 90 / 101 | 11.9 / 9.1 mm |
| 0.5 mm (≈ half an L4 face) | 562 | 218 | 162 / 162 | 100 / 101 | 0 / 1.65 mm |

- The beam size can be read as "visible at production resolution". At 0.5 mm it covers all void misses, but it also takes in a large part of the zero-gap pinch-crease walls, which is not an approved D zone.
- At smaller beams much of the void and tunnel interior counts as visible through their narrow openings. The tunnel is a handle open at both ends.
- **So the area and share of the D masks are not yet well defined.** I did not apply any D exclusion to a T-1/T-2 result.
- **Author decision needed:** the visibility beam width, or an explicit hand-drawn D boundary.

## 5. Fused R digits (§2.3) — topology finding; not rebuilt

Handle localisation by box genus (`hgenus.py`) shows that the source genus 3 comes from:

- one handle in the R hand;
- one in the L hand (the tunnel);
- one in the L axilla (the void).

The R-hand handle lies in x −38…−31, y −43…−40, z 88…100. It is the B–C inter-digit cleft: a 3 mm through-slit, open top and bottom, running from the B–C crotch to the fused block.

A genus-0 single exterior envelope therefore cannot merge digit C into digit B at the fusion alone, because that adds a handle. Two ways remain:

1. **Fill the whole B–C cleft with a mid-plane web**, from the crotch to the fusion. The through-slit becomes two blind grooves, top and bottom. This is a visible change to a 3 mm see-through slit, so it needs an author ruling on whether that slit counts as "visible exterior envelope".
2. **Keep the separate digit tubes with contact.** The ruling has rejected this.

Because the pilot route failed, I did not build option 1. It is a full rebuild of the B+C digits.

## 6. Nail tooling (§8) — recovered

- The AW4 nail-plate masks and foot frames are not on E: or in the repo; only the gate's outputs survive.
- **Regenerated** (`tools/rac/rp/rp1e/nailcheck.py`, data in `reviews/rac-rp1e-evidence/nail_tooling/`):
  - Nail plates come from the frozen `GO-05AW4_nails_final.blend` vertex groups AW3_{L,R}{D,P} (w > 0.3), split into the 4 connected plates per foot, numbered medial → lateral.
  - The per-foot axes were fitted to the recorded rp1d source tip values: L (0.114, −0.994, 0), R (−0.518, −0.856, 0).
- **Equivalence:** all 8 recorded source tips are reproduced to ≤ 0.003 mm (4 equations, 2 unknowns per foot).
- **Nail gate on v013 (G13), ±0.15 mm:**

| Nail | Δ (mm) | Status |
|---|---|---|
| L1 | −0.62 | FAIL |
| L2 | −0.50 | FAIL |
| L3 | −0.63 | FAIL |
| L4 | −0.71 | FAIL |
| R1 | −0.62 | FAIL |
| R2 | −0.55 | FAIL |
| R3 | −0.18 | FAIL |
| R4 | −0.12 | pass |

The production nail tips are 0.1–0.7 mm short: the free edge is rounded by the limit surface. No geometry was changed for this, per §8.

## 7. Author decisions needed

1. **Thin-membrane and zero-gap contacts.** P1 fixes the exterior shape of thin fins. The remaining opposed-sheet contacts are where a membrane tapers below the production face size, or ends in a zero-gap slit or stitch. Is the zero-self-x rule to be met by a different method, such as:
   - a collision-resolving relax that the stack does not provide today;
   - thickening the membrane edges in the production surface;
   - or a ruling that these contacts count as exterior-envelope contact zones?
2. **Facial rim/overhang ownership.** Normal-sign sheet splitting does not work on curls. The options are hand-drawn per-sheet source masks for each rim, or a different stack for the ear.
3. **D masks.** Choose the visibility beam width, or draw the D boundaries (void, tunnel) by hand; §4 gives the sensitivity.
4. **Fused R digits.** Accept the B–C mid-plane web (the through-slit becomes two blind grooves) as the genus-0 exterior envelope, or not.
5. **T-6.**
   - Accept the component rule for hip_R (0.086 mm).
   - Decide how to treat tail_12 (1.506 mm with the existing method, 0.79 mm with exact window clipping).
6. **Nails.** Seven nails are 0.18–0.71 mm short. They need a nail free-edge support or ownership fix, which is outside the scope of this ruling's geometry changes.

## 8. Evidence

- **`reviews/rac-rp1e-evidence/exp_v016_pilots/`:**
  - pilot logs PA0–PA5, PB0–PB3, PC0–PC1, PE0–PE3;
  - classifications;
  - `pilot{1,2,3}_table.txt`;
  - ownership specs (`own*.json`);
  - L0/L1/L4 slice figures for the three pilots.
- **`reviews/rac-rp1e-evidence/nail_tooling/`:** `nailmasks.npy`, `footaxes_fit.json`.
- **Tools:**
  - `tools/rac/rp/rp1e/`: `own.py`, `pilot_eval.py`, `dmask.py`, `dtarget.py`, `nailcheck.py`, `hgenus.py`;
  - `sim.py` with the REGCOLS/REGV options (the unchanged v013 stack is `sim_v013_stack.py`);
  - `tools/rac/rp/rp1_landmarks_comp.py`.

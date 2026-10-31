# RAC RP5 — Saurin unique-topology pilot gate

Order: `reviews/chatgpt-rac-rp5-saurin-unique-topology-pilot-order.md` (53976fb). Evidence: `reviews/rac-rp5-evidence/saurin/`. Tools: `tools/rac/rp/saurin_rp5_v001/`.
Nothing frozen. No canonical W2I6 file modified. No retopology from the preview export. No MPFB topology used. No rig, creator, UV, LOD or UE5 work. No later race started.

## Decision

## SAURIN RP5 REQUIRES AUTHOR DECISION — acceptance of (1) the field-guided ring/relax module construction as the "deliberately authored" topology method for the remaining systems A–E, G–J, (2) the layered surface representation (cage = base anatomy; fine scale relief = reproducible derived detail layer, PD-1-dependent), and (3) a thigh art-pass on a derived working source BEFORE retopology

The pilot proves the architecture end to end on the hardest Saurin-unique system, **F (tail) + E's tail-root ring**. It does **not** yet contain an authored full-body cage. The three items above decide how the rest is built and in what order, so it is not useful to author A–J before they are ruled on. Spending the remaining effort under a method or surface model the author may reject would produce a rebuild, not a pilot.

## 1. Source integrity (§3)

`SAURIN_RP5_source_integrity.json` (commit f98ea82).
- All five W2I6 hashes match: base `f86ae800…`, delta `f32286c4…`, rebuild script `2a96c00f…`, seeds `a1d07b8d…`, SA-F188 `8019420a…`. The base array hashes and the 130,949 seeds also match.
- The rebuild reproduces the W2I6 record: 4,496,934 V / 8,993,864 tris, 187.86 cm.
- **Architecture fact:** SA-F188 uses the identical SA-M188 base face list (1,124,235 V / 2,248,466 tris). That puts c1 and c2 in dense vertex correspondence.

## 2. Derived working source (§7)

`SAURIN_RP5_derived_working_source.json`.
- `SA_RP5_WORK_v000` is an identity derivation: the canonical base arrays read-only, in cm, in the source frame unchanged. There is no symmetrization, no weld and no transform.
- The only proposed geometry derivation is the thigh art-pass (§9 below) as `SA_RP5_WORK_v001`. It is not performed.

## 3. Topology architecture (§8–§9)

### Method (proposed for author acceptance)

Each system is built as an **authored module**, never by a global remesher:
- **Rings.** An anatomical root loop is defined on the source by landmarks. A field coordinate is built from it (geodesic distance from the root loop for tubes). Rings are iso-loops of that coordinate.
- **Ring counts and edge flow.** Ring counts are authored (N = 128 at the tail root), with explicit all-quad 2:1 reductions. Each ring is resampled at equal arc length on smoothed loops, phase-locked ring to ring, so edge flow follows the anatomy.
- **Relax and embedding.** A relax pass projects back to the source. Each cage vertex is stored as a barycentric point on a base triangle.
- **Configurations.** The barycentric embedding gives exact, topology-identical transfer to every configuration on the shared base face list (c1 → c2 and any creator realization).
- **Junctions.** Junction patches (shoulder, hip, hand, foot, head/rostrum, display root) are authored templates stitched between module rings.

| System | Status in this pilot |
|---|---|
| A Head / rostrum | landmarks only (rostrum tip, eyes, jaw hinges, mouth corners, crown); not authored |
| B Head–neck | neck min section located; not authored |
| C Cranial display | not authored; display root reserved as a junction patch |
| D Torso / lower axial trunk | spine stations u 91/107/123/138/150; not authored |
| **E Pelvis / sacrum / tail root** | **anatomical root plane authored** (dorsal lumbar concavity + ventral perineal junction, root section 877.7 cm²); tail-root rings authored (11 rings at phi < 0.08) |
| **F Tail** | **authored module: 15,691 V / 15,626 Q, 100 % quads, 181 rings, N 128→64→32→16→8 + cap** |
| G Shoulders / arms | joints fitted (glenohumeral, elbow, wrist); not authored |
| H Hands / claws | 10 claw tips, MCP lines; not authored |
| I Hips / legs | joints fitted; thigh art-debt diagnosed; not authored |
| J Feet / claws | 10 toe tips, ball lines, plantigrade heel; not authored |

### Automatic remesher (diagnostic only)

A QuadriFlow scaffold of 84,600 quads built from a 150 k-tri decimation (`scaffold_diagnostic/SA_scaffold_eval.json`) fails as a production generator:
- T-1 max 72.5 mm (the tail tip is lost);
- T-2 fails head (8.1 mm max), hands (11.4) and feet (9.4);
- T-3 bbox +6.3 / −6.6 mm (claws eroded); T-6 max 4.8 mm;
- T-4: 1,935 quads with aspect > 4 (max 176);
- T-7 profile 0.985.

This confirms §8: Saurin needs an authored cage.

## 4. c1 / c2 shared-topology test (§11)

The tail module was authored once on SA-M188 and carried to SA-F188 by barycentric transfer. No re-solve was needed and the topology is identical (`SA_tail_module.npz` sha256 `559565cc…`).

| | T-1 median / p95 / max (mm) | T-2 tail_root p95 / max | T-2 tail_stations max | Tip zone (r 0.665 cm) max |
|---|---|---|---|---|
| SA-M188 | 0.053 / 0.280 / 1.38 PASS | 0.33 / 0.96 PASS | 1.38 PASS | 1.02 |
| SA-F188 | 0.053 / 0.282 / 1.37 PASS | 0.33 / 0.99 PASS | 1.37 PASS | 1.01 |

## 5. Quality, density, loop audit (§12–§14)

- **Quality (T-4, both configurations):**
  - 100 % quads, no n-gons, no triangles, one manifold strip.
  - Angles outside 45–135°: 1.18 % / 1.29 %, in the 2:1 transition rows and the tip.
  - One quad has aspect > 4 (4.37, at the cap); aspect p99 is 1.73.
- **Density (T-5):** tail mean 0.354 % of stature (ceiling 0.6), p95 0.47 %. The max of 0.80 % is at the cap.
- **Loop audit (Saurin-specific, not the MPFB 69 stations):**
  - The root has ≥ 4 continuous rings (11 at phi < 0.08).
  - Every ring is closed and phase-locked (vertex 0 tracks the dorsal line).
  - Ring counts: 91 × 128, 43 × 64, 30 × 16 … 32, 16 × 16, 1 × 8.
  - Ring spacing ≈ edge length (about 0.9–1.0 cm at the root).
  - Projection max 1.80 mm before embedding.
  - The 16 equal-arc tail-chain landmarks each lie on a ring band.

## 6. Landmarks (§15)

`landmarks/SA-M188_landmarks.json` contains 71 landmarks; each records its method (section refit, extremal, canon head frame, derived). Region labels are in `landmarks/SA-M188_regions.npz`. Key readings:
- tail length 132.2 cm;
- root section 877.7 cm²;
- spine stations;
- neck min section;
- eyes and jaw hinges from the W3B head canon (×1.08 about PIV + AT);
- rostrum tip, crown, mouth corners;
- 5 hand tips and 5 toe tips per side;
- ball lines.

SA-F188 landmarks are carried by the shared-vertex displacement field.

## 7. T-1 … T-7 (§16)

| Gate | Tail module (authored) | Full body |
|---|---|---|
| T-1 | PASS (c1 and c2) | not evaluable: no full cage |
| T-2 | tail_root and tail_stations PASS | head / hands / feet not evaluable |
| T-3 | n/a (module) | not evaluable |
| T-4 | PASS (100 % quads; 1.2–1.3 % angle outliers, transition rows only) | — |
| T-5 | PASS (tail) | — |
| T-6 | tail tip within the tip zone (1.02 mm) | other extremals not evaluable |
| T-7 (tail included) | module area preservation (below) | not evaluable |

No full-body PASS is claimed.

## 8. Identity metrics (§17)

`eval/SA_identity_metrics.json`.

SA-F188 source values:
- tail 130.49 cm = 0.6945 of stature; carriage −25.7°;
- tail section areas 461.7 / 257.1 / 62.4 cm² at 25 / 50 / 75 %;
- lower axial trunk 33.4 cm; thorax 44.0 × 32.6; pelvic band 43.9;
- forearm/arm 0.477; femur/leg 0.315;
- rostral projection 10.4; orbit spacing 7.14;
- 10 + 10 claw tips; plantigrade.

SA-M188 values are in the same file.

Tail-module preservation, cage vs source tail section areas:
- SA-M188: −0.04 / −0.05 / −0.21 %;
- SA-F188: −0.04 / −0.06 / −0.22 %.

## 9. Thigh art-debt diagnosis and timing (§6)

`thigh/SAURIN_thigh_artdebt_diagnosis.json`, board J.

**Location (SA-M188):**
- band u 66–84 cm;
- medial / posterior high-pass relief p99 4.37 mm (max 5.04), against 3.31 mm anterolateral;
- 259 hotspot vertices in a bounded medial-posterior patch (f −11.7 … −4.2).

SA-F188 is the same (p99 4.31 mm). The W2 surface delta is uniform there (mean 0.19–0.20 mm). The mark is base-level, not scale-level.

**Timing:** correct **BEFORE retopology**, on `SA_RP5_WORK_v001`, as a bounded medial/posterior smoothing / art-pass. Reason: the base-level amplitude (about 4–5 mm) exceeds the T-1 / T-2 capture tolerance. A cage built first would either capture the flaw or have to be re-projected after the fix.

Silhouette, accepted W2 measurements, the seed realization and the surrounding anatomy stay untouched. Not performed; awaiting author approval.

## 10. Surface representation (§10 / §18)

`eval/SA_surface_representation.json`, board K.
- Surfaced − base delta: max 1.70 mm, mean 0.30 mm.
- Only 0.005 % of the delta is above 1.5 mm; 7.3 % is above 0.8 mm.
- Silhouette IoU surfaced vs base: front 0.99703, profile 0.99661.
- Surfaced edge 0.96 mm, against a cage edge of about 4–10 mm.
- Delta p95 by region: head 0.56, neck 0.81, trunk 0.99, arms 0.93, hands 0.57, legs 0.68, feet 0.53, tail 1.04 mm.
- Joint-zone delta is lower than elsewhere (0.246 vs 0.317 mm).

**Proposal:**
1. Structural / macro anatomy, creator scale-field boundaries and silhouette-bearing geometry go in the cage, which follows the base.
2. Fine scale relief and articulation-region scale detail go in a reproducible derived detail layer, regenerated from the canonical seeds and delta (displacement / normal). It is transported per configuration, never baked into the topology.

PD-1 (surface transport) is a dependency of layer 2, not of the topology.

## 11. PD ownership (§5 / §20)

- **PD-1:** affects the detail layer only.
- **PD-2:** seen under tail LBS on the dense source surface. Under the same scaffold the source flips and folds in 3 of 4 poses (root lateral 135 flips / 117 folds, mid lateral 101 / 71, twist 27 / 24). The cage has 0 / 0 in every pose. Ownership is source deformation, not topology.
- **PD-3 / PD-4:** not topology-affecting; carried as dependencies.

## 12. Diagnostic deformation (§19)

`eval/SA_tail_deformation.json`, board L. Temporary 18-joint tail-chain LBS, not a rig.

| Pose | Flips / folds (cage) | Strain p95 |
|---|---|---|
| root lateral 30° | 0 / 0 | 9.5 % |
| root vertical 25° | 0 / 0 | 6.2 % |
| mid lateral 40° | 0 / 0 | 13.5 % |
| twist 30° | 0 / 0 | 4.1 % |

No new topology class.

## 13. Boards (§21)

All in `sheets/`:
- SA_A canonical sources; SA_B topology overview; SA_C head/rostrum (landmarks); SA_D pelvis / tail root;
- SA_E tail; SA_F hands; SA_G feet; SA_H c1/c2;
- SA_I source deviation; SA_J thigh art-debt; SA_K surface representation; SA_L tail deformation.

C, F and G show landmarks and the scaffold failure only; no authored cage exists there yet.

## 14. Immutables (§24)

`immutable_hashes.txt`: **228 / 228 UNCHANGED** against 53976fb.
- The repository check covers all 30 freeze records, the RP3/RP4 frozen production (Durrim, Pipkin, Cogling and their hash lists), MPFB v005, W2I6 / W3B / W3B1 Saurin evidence, Saurin specs and Gorrund.
- The five canonical W2I6 files on the PC were re-hashed and are equal to canon.

## 15. Pilot artifact

`tail_module/SA_tail_module.npz` (`559565cc28a89db67c559c6db899cee51af0e349614fcb466255a6b35156baab`) and `.json` (`cb0153dac8beef1ba67055028b88479c2b634317be1594d8ac72bd88cf9fc2e1`). Status: **PILOT / NOT FROZEN**. MPFB-independent. No freeze candidate record.

## 16. Bounded next-step plan (after the author decision)

1. If the author approves (3), apply the thigh art-pass on `SA_RP5_WORK_v001`. Record operations and hashes, then re-verify silhouette and W2 measurements.
2. Author modules in this order, using the same ring/relax/barycentric method:
   - D axial trunk + E pelvis, joined to the existing tail root;
   - I/J legs and feet (heel, ball line and 5 toes, with claw caps);
   - G/H shoulders, arms and hands (5 digits, with claw caps);
   - B neck;
   - A head / rostrum (mouth slit and jaw-hinge loops, orbit rings);
   - C display root.
3. Author junction patches (hip, shoulder, wrist / ankle fans, head-neck, display root), then fuse everything into one closed manifold.
4. Run the full gate on c1 and c2: T-1 … T-7 (tail included), density, Saurin loop audit, identity metrics, diagnostic deformation on all joints.
5. Prototype the detail layer: regenerate the scale relief on the cage and measure against the surfaced canon.
6. Return a new pilot gate. Still no freeze.

STOP FOR CHATGPT REVIEW.

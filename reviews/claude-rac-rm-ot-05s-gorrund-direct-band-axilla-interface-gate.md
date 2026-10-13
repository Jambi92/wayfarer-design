# RAC RM-OT-05S: Gorrund direct band-to-axilla interface repair, gate report

**Order:** `reviews/chatgpt-rac-rm-ot-05s-gorrund-direct-band-axilla-interface-order.md` (2773058).
**Evidence:** `reviews/rac-rmot05s-evidence/`. **Tools:** `tools/rac/w1/rmot05s_drivers/`.
**Commits:** the plan, made before any edit, is **35479a0**. The result is the commit that adds this report. The package receipt is the commit after it.

## Status

| Item | Status |
|---|---|
| Gorrund | UNACCEPTED |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| Canon promotion | NOT PERFORMED |

There was no Rodin generation, no credits, no replacement source and no other RAC work.

## Outcome

**The technical outcome is improved but UNRESOLVED.**

The declared direct study ends at S3. Against B2 and the 05R R3 run, it is the first result where all of these hold:
- outside anatomy is bit-identical, with a correct boundary, manifold and orientation;
- **0 intersections**;
- **no fold over 120°**;
- **no triangle under 10°**: the minimum is 11.9°, against 0.98° for B2 and 3.73° for R3;
- **seam continuity of 97.8 %**, against 84.4 % for B2 and 82.5 % for R3.

It still fails these pre-registered checks:

| Check | What fails |
|---|---|
| V4 | 8 faces in the posterior taper each have one edge of 0.209–0.249 cm, against the 0.25 cm bound |
| V6c-1 | A crease at θ −90° (95° direction change in 0.5 cm) |
| V6c-2 | The anterior taper step is not monotone within tolerance at its untouched end |

There are also 2 dihedrals between 90° and 120° at θ −89.6°.

**Anatomical visual credibility differs by side.**
- **Anterior: plausible.** The garment ledge is gone, and the arm flows into the pectoral fold. The remaining band ends in a tapered termination, not a cut lip.
- **Posterior: not credible.** A crinkled, notched strip runs along the posterior axillary fold edge (θ −86…−106°, s 2–8 cm).

**This is not acceptance.** Following the order (and your message), the release also contains a **direct-edit handoff** for interactive sculpting of exactly this interface. It is a native `.blend` with masks, a brief and a verification setup that has been self-tested.

## Ruling recorded

- 05R FAIL is accepted as the honest result.
- B2 and R1–R3 stay rejected and frozen.
- Interpolation / relaxation retries have stopped. 05S used no Laplacian, bi-Laplacian or relaxation solve. The only edge operation was topological edge flips.

## §2 Capability, baseline, plan

**Capability (stated in the plan before any edit).**
- Explicit vertex / edge / face selection and controlled local topology are **available**: index sets, constrained quality triangulation and topological edge flips.
- Anatomical shaping was **scripted only**. Each new vertex is placed exactly on an explicit designed cross-section profile.
- Blender 5.0.1 is present only as a headless Python module. **No interactive brush work is claimed.**

**Baseline: B2.**
- B2 is the F1 duplicate produced by the verified 05Q recipe, reproducible bit-identically.
- Its central inferred patch (θ −80…74°) is kept.
- Its defective ends and all of the R3 junction mesh are **not** inherited.

**Interface (plan 35479a0).** Per-0.25° profile columns carry explicit anchors:

| Anchor | Definition |
|---|---|
| Band ledge | `s_led` |
| A | Arm skin at `s_led − 1.8` |
| B | `s_hi + 1.8`; or, for the posterior lip / fold edge, 2.5 cm beyond the peak on the fold / trunk side |

| Side | θ range | Faces | Source faces |
|---|---|---|---|
| Posterior | −80…−136° | 238 | 128: 30 arm skin, 67 garment band, 31 fold edge / trunk |
| Anterior | 74…122° | 219 | 146: 22 arm skin, 106 garment band, 18 fused / ambiguous |

**Scope extension.**
- **274** faces of the 05Q protected set are now inside the authorised boundary. 74 of them were already the 05R extension; 200 are new. Each is listed with its class in `plan/interface_sets.npz`.
- The protected set **P05S** is 139,807 faces, with coordinate sha `4468dd86…7c55`. The 05Q and 05R protection sets are kept as committed.
- **Not touched:** the full ring, arm–trunk separation, the axilla or shoulder rebuild, pose, and any second garment.

**Plan images** (identical camera; rows are source / B2 / R3):
- `plan/P1–P3`: interface masks;
- `plan/P4–P5`: sections;
- `plan/I_*_chart_topology.png`: boundary topology with the garment / skin / fold classes;
- `plan/design_*_columns.png`: the designed profiles.

**Erratum:** after the plan commit, one wording slip in `PLAN.md` ("C1 tangent anchor zone") was corrected; the content is unchanged.

## §4 Operations and checkpoints (`repair/S1..S3/`: mesh gz, pre-flip checkpoint gz, record, labels, maps, verification)

All three runs share the same steps:
1. Take B2 and apply the C1 flip (faces 140820 / 140812, minimum angle 9.98° → 16.8° / 15.1°).
2. Per side, delete the interface faces.
3. Build the chart.
4. Run Triangle (q30, 0.7 cm, no boundary Steiner points).
5. Place each new vertex **exactly** on the designed target.
6. Run 3-D Lawson flips (topological winding, never re-creating an existing edge).

| Run | What changed | Result |
|---|---|---|
| **S1** (planned) | Chart arclength measured on the B2 columns | **FAIL**: 6 intersections, minimum angle 2.47°, 27 folds over 120°. The cause is a discrete fault: B2's own crinkled junction surface inflated the chart arclength exactly in the junction zone (`lB − lA` spikes at θ −97° / 88°). The flip pass was also capped at 60 |
| **S2** (correction pass 1) | Chart = normalised baseline position × **target** profile length; flips not capped | **UNRESOLVED**: V1–V3 and V5 pass, minimum angle 11.9°, 0 folds over 120° |
| **S3** (correction pass 2, final) | Interior points beyond A / B continue on the baseline surface instead of being clipped onto A / B | **UNRESOLVED**: essentially the same scores as S2 (one fewer anterior flip; the last anterior taper step is 0.421 cm instead of 0.411) and visually the same, so the clipping was not the cause of the posterior crinkle |

There was no parameter sweep. The study stops here: the remaining posterior defect needs anatomical judgement, not another automated pass.

**S3 result:** `GO-05S-S3.obj.gz`, sha `1d503833…ac4c`, 141,194 faces:
- 139,807 protected;
- 590 retained B2;
- 797 interface: 376 inferred skin (label 5) and 421 transition / termination (label 4).

## §5 Verification of S3 (`repair/S3/GO-05S-S3_verify.json`)

| Area | Result | Verdict |
|---|---|---|
| Outside-anatomy preservation (V1) | P05S coordinate sha equals the plan's. Exact index correspondence; kept source vertices bit-identical; 0 boundary source vertices moved | **PASS** |
| Boundary / manifold / orientation (V2) | 320 boundary edges, equal to the source's by correspondence. 0 non-manifold edges, 0 inconsistent orientation, 0 degenerate faces | **PASS** |
| Intersections (V3) | 0 new-face intersections (2,943 faces tested); 0 pre-existing pairs | **PASS** |
| Triangle quality (V4, unchanged bounds) | 1,387 new faces. Minimum angle **11.9°** (p1 / p5 / p50 = 16.2 / 22.5 / 39.4°); 0 faces under 10°. **8 faces** each have one edge of 0.209–0.249 cm, all in the posterior taper (θ −122.8…−132°, s 0.6–1.6, label 4) and between new vertices. The source boundary is not the cause | **FAIL** (bound missed by ≤ 0.041 cm) |
| Seam continuity (V5, unchanged) | 137 stitch edges; **97.8 %** ≤ 35°. Percentiles p50 / p90 / p95 / p99 / max = 7.3 / 19.0 / 24.1 / 44.3 / 48.2°. The 3 outliers are at θ 121.0 (48.2°), −130.7 (45.4°) and −135.5 (42.3°), at the termination ends. Source-skin reference p95 is 27.5° | **PASS** |
| V6 historical (05Q) | Unchanged from B2: 50 deltoid-slope "ledge" faces; steps as in 05Q | reported only |
| Garment ledge removed (V6c-1) | Maximum direction change per 0.5 cm, result against source band. Posterior: −112° 32.2 vs 125.6; −104° 29.2 vs 121.1; −96° 36.9 vs 104.9; **−90° 95.1 vs 83.1**. Anterior: 84° 14.9; 90° 9.5; 96° 16.8; 102° 18.1 (source 84–95) | **FAIL** (at −90°, and −96° is 1.9° over the bound) |
| Taper is a termination (V6c-2) | No undercut anywhere. Posterior monotone. Anterior step goes 1.36 → 1.47 → 1.47 → 1.17 → … → 0.42 cm: it rises 0.11 cm inside the w ≈ 0 end, which is the source's own variation, but the pre-registered tolerance is 0.1 | **FAIL** (pre-registered rule) |
| No folds (V6c-3) | 0 dihedrals over 120°; 2 between 90° and 120°, at θ −89.7 / −89.5 (s 3.1 / 5.5) | **PASS** |
| **Anatomical visual credibility** | **Anterior:** ledge removed, smooth arm-to-pectoral transition, tapered band termination (`compare/03`, `04`, row 4). **Posterior:** a crinkled, notched strip along the fold edge and a crease at θ −90° (`compare/01`, `02`, row 4; `compare/08` at −88 / −92). This is not a credible fold | anterior plausible; **posterior not credible** |

**Automated verdict: UNRESOLVED.** Scored with the same code (`baseline/`, `repair/S1–S2`):
- B2 = FAIL (folds over 120°, V4, V5);
- S1 = FAIL;
- S2 = UNRESOLVED.

**Images** (`compare/`). All rows are source F1 / B2 / R3 / S3, with identical camera and material.

| File | Content |
|---|---|
| `01_posterior_interface_shaded.png`, `02_posterior_interface_wire_labels.png` | Posterior interface at readable size: rear / rear-lateral / rear-medial / underside |
| `03_anterior_interface_shaded.png`, `04_anterior_interface_wire_labels.png` | Anterior interface: front / front-lateral / front-medial / underside |
| `05_arm_closes_shaded.png`, `06_arm_closes_wire_labels.png` | Front / lateral / rear / 3/4 / rear 3/4 / underside |
| `07_full_figure_context.png` | Full figure |
| `08_posterior_sections_src_B2_R3_S3.png`, `09_anterior_sections_src_B2_R3_S3.png` | 12 half-plane sections per junction |

The labels are: blue / amber = 05Q inferred, purple = 05S inferred skin, green = 05S transition / termination. The remaining medial band beyond θ −136° and 122° is visible and is not removed.

## Unresolved dependencies and capability limits

- **The posterior fold-edge crease** is where the band, the curled lip and the posterior axillary fold are fused. A clean crease there needs judgement about the fold anatomy beyond what a designed profile sweep encodes. **Capability limit:** there is no interactive sculpt here. The **handoff** (below) is the route.
- **No dependency** on prohibited operations was found. The handoff's scope stays inside the committed interface.
- **V6c-2's tolerance** is shown to be sensitive to the source's own variation at the taper's untouched end. This is reported, not changed.

## Direct-edit handoff (`handoff/`)

- **`GO-05S_interface_handoff.blend`** (Blender 5.0.1, compressed). Objects:
  - the working mesh S3, with vertex groups `EDIT_posterior` / `EDIT_anterior` / `FROZEN_interface_boundary` / `FOCUS_posterior_crinkle` and the face attribute `rac_label`;
  - hidden, locked references: F1 source and B2.
- **`HANDOFF.md`**: a brief tied to the 05S scope.
- **Verification setup:** `s_rematch.py` recovers correspondence by exact coordinates; then `s_verify.py` scores the edit.
- **Self-test:** rematching S3 itself recovers all 139,807 protected faces and reproduces S3's scores (`selftest_*.json`).

## Stop

Stopped for author visual review. There is no full ring, arm–trunk separation, wider clothing removal, RD5, LOW, blind study, scaffold, canon or production work.

A local pass says nothing about the belt / pelvis, bracers / shins, whole-body suitability or species acceptance. Any further body work needs a new author order.

Gorrund is UNACCEPTED, Grask E3 FROZEN, RM-OT-05 OPEN and Stage C BLOCKED. The beastfolk identity, the body / plantigrade guardrails and the later 13,380-vertex rig-contract validation are preserved.

---

## Package receipt (committed after the build; `reviews/rac-rmot05s-evidence/package/PACKAGE_RECEIPT.json`)

**Release:** `racebodies_v123`. It is **one ZIP split into 7 volumes**, each 25 MB or less:

| Volume | Bytes | SHA-256 |
|---|---|---|
| `racebodies_v123.zip` | 12,494,414 | `a0d053b5fa5e12ad4efbaecf41eddf1821bb59f9095b87221908c36ed5db9759` |
| `racebodies_v123.z01` | 25,165,824 | `b4617bd4b1ec7477bd19c27f0f43ec2e9b19a16d88ad4f1e9fb43d825e0c8ae3` |
| `racebodies_v123.z02` | 25,165,824 | `a5c3eea4c3ebff97a1860537c0b5e1c254cc3695de7331ee3dbbc7a38061c37c` |
| `racebodies_v123.z03` | 25,165,824 | `218ae7bb42b6567ab8155c27622251cad25f7c1b1a188099d8765139f307b402` |
| `racebodies_v123.z04` | 25,165,824 | `b18989191eb67ee8cc78f8b16aa336dc7fd5eb50d8dd981b26fce12485152e60` |
| `racebodies_v123.z05` | 25,165,824 | `84e366c97ecedfafad26b523350941eb6ba57e29ff16437bd3cce25f81b95835` |
| `racebodies_v123.z06` | 25,165,824 | `ba5b6008df157ee994e120c3a09c9cc13f23b6f667f0e7b2d44ef0b90e2c8ba9` |
| Rejoined archive | 163,489,354 | `98c5ead0d4480a96b84c49854f530aa2d53aa313a6f90a58c90108b461981c15` |

**Contents.**
- **Own manifest:** `PACKAGE_MANIFEST.sha256`, 211 entries. The repository evidence manifests are included verbatim and labelled as such.
- **Payload:**
  - the 05Q / 05R / 05S orders, plans and reports;
  - the F1 working mesh, the B2 baseline, R1–R3, S1–S3 and the S checkpoints;
  - all maps, labels and checks;
  - the original PNG images;
  - the direct-edit handoff (`.blend`, brief and verification setup);
  - the tools.
- **Not included:** `base.glb` stays external; its location and hash are in the README.

**Clean-extraction verification**, in an isolated empty directory:
- `unzip -t` reported no errors.
- 211 of 211 entries are present with equal hashes; nothing is unlisted or missing.
- All 17 decoded mesh hashes are equal.
- 22 of 22 relative links resolve.
- All replay and handoff inputs exist.
- `replay_package.sh` reproduced the S3 verification **identically** (verdict UNRESOLVED). The handoff rematch self-test recovered all 139,807 protected faces.
- **Limitations:** renders, the `.blend` rebuild and the base.glb extraction check are not in the scripted replay.
- **Result: PASS.**

**Delivered to:**
- the chat, as the 7 attached files;
- `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\sheets\racebodies_v123\`, where all 7 files are on the device with the sizes above.

This receipt was added after the build. The release carries the report as of 4182cc5.

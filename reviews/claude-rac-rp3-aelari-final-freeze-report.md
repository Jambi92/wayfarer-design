# Claude report — RAC RP3 Aelari final consolidation / validation / freeze

**Order:** `reviews/chatgpt-rac-rp3-aelari-final-consolidation-freeze-order.md` (2026-10-28; review of `7d2f734`)
**Freeze record:** `reviews/rac-rp3-evidence/aelari_rp3_freeze/AELARI_RP3_FREEZE.json`
**Gate record:** `AELARI_FINAL_gates.json` (same folder)
**Evidence:** `reviews/rac-rp3-evidence/aelari_rp3_freeze/`

**Tools** (`tools/rac/rp/aelari_rp3_v001/`):

| Tool | Role |
|---|---|
| `run_aefinal.sh` | clean rebuild |
| `run_aefinal_prod.sh` | production blends + local read-back |
| `run_aefinal_eval.sh` | final gates |
| `ae_final_gates.py` | gate record |
| `ae_final_sheets.py` | sheets |
| `ae_freeze_verify.py` | PC read-back |
| `ae_freeze_record.py` | freeze record |

**Reused tools:**
- `fenn_rp3_v001/fn_make_prod.py`: new env `RAC_COMPOSITION`; its default leaves Fenn unchanged.
- `fenn_rp3_v001/fn_final_anatomy.py`: unchanged.
- `run_ae_ear.sh`: probes now run on `AE_H1`; the default is still AEL1.

## Result

# AELARI RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN

Every gate in §4–§21 passes on both configurations, and the PC copies read back byte-identical. Freezing is by record: the production blends were not re-saved.

`AELARI_RP3_FREEZE.json` has `all_gates_pass = true`; its sha256 is in the commit.

| | Configuration 1 | Configuration 2 |
|---|---|---|
| File | `AE_M_REF_RP3_v001.blend` | `AE_F_REF_RP3_v001.blend` |
| Body source | AEL1-R1 | AELF190-R1 |
| sha256 | `b4bcf9ee…` | `505f3405…` |
| geometry hash | `6c9ceddc…` | `d51375d6…` |
| face topology hash (identical) | `4615d6bc…` | `4615d6bc…` |
| vertices / quads | 58,944 / 58,942 (100 % quads) | 58,944 / 58,942 (100 % quads) |
| stature | 189.9 cm | 190.0 cm |

Composition of both bodies:
- MPFB Family Base v005 outside the ear branch;
- the accepted Aelari face from the R1 source, unchanged;
- AE-E2 Aelari ear geometry on the reused Fenn ear topology v002, used as engineering topology only.

The face-topology hash equals frozen Fenn's, as expected: the face list is identical, while every Aelari vertex position is Aelari-specific.

The accepted residuals do not change, and nothing new is raised.

## §4 Clean rebuild / provenance

| Step | c1 | c2 |
|---|---|---|
| regen.py from the committed build record: geometry identical, max \|dV\| | 0 | 0 |
| full record rebuild (`build_variant`, no overrides) vs committed r6, max \|dV\| | 0 | 0 |
| native hm08 → propagate onto frozen v005: family realization byte-identical to reviewed `bodyfam_v002` | yes | yes |
| AE-E2 rebuilt from the committed parameters and cuff canon: arrays equal the reviewed corrected prototype | yes (dV 0) | yes (dV 0) |
| AE-E2 parameters identical | yes | yes |
| face list equals frozen Fenn v002 | yes | yes |
| outside branch equals the family realization | yes | yes |
| transition ring | 102 vertices (unchanged) | 102 vertices (unchanged) |

No hash mismatched anywhere. The immutable inputs are unchanged (`immutable_and_source_hashes.txt`):
- v005 blend and map;
- v005 freeze;
- Fenn freeze;
- AEL1 / AELF190 ancestry;
- AEL1-R1 / AELF190-R1;
- Fenn v002 topology, cuff canon and map.

## §5 Sidecars / maps

Per body, as for Fenn:
- `AE_*_REF_RP3_v001.json`: hashes, counts, provenance, embedded status.
- `_landmarks.json`: pelvis-root frame.
- `_branch_map.npz`: hm08 proxy / weight rows (M), v005 → final index, removed v005 ear rows and faces, part / side, src_index, production faces. The root interface is the cuff part; provenance points to the reused v002 topology.

Each branch-map array was verified equal to the candidate on read-back.

## §6 Integrity

Both bodies:
- 1 component;
- 0 boundary edges, 0 non-manifold edges, 0 non-manifold vertices, 0 degenerate faces;
- winding consistent, normals outward, 0 coincident pairs.

| | c1 | c2 |
|---|---|---|
| Whole-body self-intersection pairs | 62 | 154 |
| Branch self-intersections | 0 | 0 |
| Contact pairs on branch faces | 0 | 0 |

Whole-body self-intersection equals the accepted family baseline exactly, and the pair set is identical (contact classes as recorded in 0f6aba8).

Root:
- valence 4 at all 52 root vertices per side;
- no seam (0 boundary);
- no float or burial: clearance 0.73 / 0.71 cm, cuff deviation from the hidden-ear skull ≤ 1.08 / 0.93 cm by design;
- transition max 0.065 / 0.070 cm.

## §7 Validator D1 + D3 + D4 + D5 + D6

| | c1 | c2 |
|---|---|---|
| Firm PASS | **69 / 69** | **69 / 69** |
| Stations identical to the family realization (loops, margins, valid sides, D5 / D6 exclusions) | 69 / 69 | 69 / 69 |
| Margin-zero stations | thumb_mcp_l / r, toe1_j1_l / r | toe1_j1_l / r |
| Recomputed from read-back | 69 / 69 | 69 / 69 |

The family realization equals the reviewed `bodyfam_v002` candidate.

Fallback-label differences against the family are vertex-order annotations of an already-undefined side, the same class Fenn documented. No verdict changes:
- c1: shoulder_l, thumb_mcp_l, toe3_j3_l, index_mcp_r, hip_r;
- c2: shoulder_l, hip_l, toe4_j2_l.

D5 / D6 exclusions are listed in the gate record. The ear branch alters no body-joint verdict.

## §8 Anatomy / source fit

**Ear-excluded (primary):** T-1 / T-2 / T-3 / T-7 all pass on both configurations.

| | c1 | c2 |
|---|---|---|
| Body max, prod → source / source → prod | 1.82 / 0.93 mm | 2.04 / 0.90 mm |
| Head, hands, feet max | ≤ 1.01 mm | ≤ 0.99 mm |
| Stature difference | −0.45 mm | 0.00 mm |
| Silhouette IoU min, outside ear pixels | 0.9976 | 0.9978 |

**Unmasked `anatomy.py` (transparency):** T-1 / T-2 and T-7 fail on both.
- Classification: **expected source-vs-new-ear anatomy divergence**. The R-6 source still carries the MPFB human auricle; the production body carries AE-E2.
- Localisation (`anatomy/AELARI_unmasked_anatomy_localisation.json`): everything farther than 1.5 cm from the ear branch is within the T-1 body limits.

  | | c1 | c2 |
  |---|---|---|
  | prod → source max / p95 | 1.82 / 0.21 mm | 2.04 / 0.17 mm |
  | source → prod max | 0.93 mm | 0.90 mm |
  | overall maximum (ear zone) | 38 mm | 36 mm |

- Unmasked IoU front 0.993 / 0.994: the ears in silhouette.
- No other unmasked failure.

## §9 Final body identity (equal height, hidden ear)

**Versus frozen Fenn — all hold:**

| Measure | c1 | c2 |
|---|---|---|
| central vertical share | +2.67 % | +2.56 % |
| torso share | +2.36 % | +2.39 % |
| neck | +5.6 % | +4.2 % |
| thoracic vertical | **+1.00 %** | **+1.32 %** |
| waist interval / torso | +1.29 % | +0.60 % |
| cranial vertical | +1.56 % | +1.75 % |
| extremity share | −2.73 % | −2.79 % |
| shin / leg gap to Marchfolk (more even than Fenn) | 0.0096 (Fenn 0.0192) | 0.0094 (Fenn 0.0203) |

**Versus humans (Marchfolk, Sagekin reported) — all hold:**

| Measure | c1 | c2 |
|---|---|---|
| leg share | +0.34 % | +0.35 % |
| arm share | +1.28 % | +1.41 % |
| hand share | +3.2 % | +3.6 % |
| foot share | +0.65 % | +1.12 % |
| forearm / upper arm | +4.9 % | +5.2 % |
| elbow breadth (gracile) | −3.5 % | −3.6 % |
| thorax depth (shallow) | −6.3 % | −6.9 % |

- **Hidden-ear body RMS:** trunk 13.6 / 13.2 mm vs Fenn and leg 23 mm, against a human baseline of 8.9 / 7.6 mm. It equals the reviewed R1 result exactly.
- **Identity (`sg_identity`):** fit ≪ signal in every zone on both configurations, nearest-other signal / fit ratio ≥ 19.8× (c1) / 20.3× (c2). The family realization did not regress toward Marchfolk, Sagekin, Fenn or the other configuration.
- **Canon:** c1 16 / 19 and c2 17 / 19. The only non-holding rows are the skin wrist / knee / ankle gracility diagnostics, accepted as diagnostic only (§19).

## §10 Pelvis (skeletal proxy, t = 0 / 0.5 / 1.0)

All six rules hold at all t on both configurations. The pelvis bone scales are unchanged (1.0 / 1.07 / 1.06), so there is no breadth shortcut.

| Rule | c1 (t = 0.5) | c2 (t = 0.5) |
|---|---|---|
| hip height > MF | +0.34 % | +0.35 % |
| bitroch / crest ≥ MF | +0.85 % | +0.53 % |
| pelvic vertical / crest > MF | +10.7 % | +10.5 % |
| pelvic vertical / crest > Fenn | +10.4 % | +10.2 % |
| waist / torso > Fenn | +1.33 % | +0.62 % |
| waist / torso ≥ MF | +0.59 % | +0.81 % |

These are the accepted R1 margins.

## §11 Hidden-ear face

- **7 / 7 systems** directional and material on both configurations: facial verticality, cranial-height contribution, forehead-to-chin, lower face, lighter mandible, vertical cheek / mid-face, lighter brow.
- Fenn relations hold: more vertical, longer forehead-to-chin, higher cranial contribution, longer / narrower eye presentation.
- Descriptors equal the accepted R1 result exactly; the face geometry is unchanged.

## §12 UFCA / face readiness

| | c1 | c2 |
|---|---|---|
| Mouth rings | 30 | 36 |
| Orbit rings | 43 / 43 | 43 / 43 |
| Poles at mouth corners | 0 | 0 |
| Poles within 2 cm of the mouth | 0 | 0 |
| Poles near eyes | 4 / 4 | 4 / 4 |

- Mouth and orbit pass on both, equal to the family realization.
- Face density 0.136 / 0.133 %, pass.
- Topology outside the branch is unchanged, and there is no craniofacial branch.

## §13 Ear final gate — AE-E2

| | c1 | c2 |
|---|---|---|
| T-4 | **117 / 3,718** (3.15 %) | **120 / 3,718** (3.23 %) |
| Aspect max (> 10) | 8.28 (0) | 8.55 (0) |
| Branch self-intersection | 0 | 0 |
| Root crease max | 51.9° | 51.5° |
| Measures equal the reviewed prototype | yes | yes |
| Length / body angle / upper extension | 9.67 cm / 27.2° / 38.0° | 9.35 cm / 27.2° / 38.0° |

- Topology is the same, root valence 4, guard 1 iteration.
- Minimum angle is 20.0° on both.
- The values are exactly the reviewed quality class.

## §14 Visible-ear firewall (vs frozen Fenn E2, matched presentation)

Values are [Aelari c1, Fenn].

| Measure | Aelari c1 | Fenn | Reading |
|---|---|---|---|
| body angle | 27.2° | 52.7° | less lateral projection |
| lateral extent / length | 0.263 | 0.324 | closer to the skull |
| upper extension | 38.0° | 32.3° | more upward |
| length / head height | 0.388 | 0.349 | longer |
| width / length | 0.335 | 0.378 | narrower, gradual taper |
| sweep / length | 0.119 | 0.095 | distinct trajectory |

c2 holds the same directions. Sheet 14 does not read as "Fenn rotated upward". Frozen Fenn is unchanged.

## §15 Density

- All 9 family zones pass.
- AE-E2 branch mean edge 0.103 / 0.099 % of stature, against a limit of 0.25 %.
- The face / ears / head zone means differ from the family realization only because the branch replaces the ear rows, the same pattern as Fenn.
- The production export adds no change: read-back geometry equals the candidate to 6e-8 m.

## §16 Body deformation (Standard v1, 18 poses)

- Final minus family: flipped 0, new self-intersections 0, new folds 0 on every pose, both configurations.
- Final vs Marchfolk v005: at most +4 (c1) / +1 (c2) flipped.
- No new topology-class defect and no new contact class.
- Classification: what remains is the known family rig class (source rig + carried MPFB weights, plain LBS), identical pose by pose to the accepted family realization. No corrective weights were authored.

## §17 Ear / head readiness

Eight poses: neck flex / ext 30, yaw ±45, pitch ±20, roll ±20.
- 0 new branch self-intersections, 0 flipped branch faces, 0 root inversions on both configurations.
- Root-loop edge strain equals the same loop on the v005 family body; the ear adds none.
- Ear-to-non-head clearance ≥ 3.9 / 3.5 cm.

## §18 Shape probes (configuration 1)

All ten probes:
- keep the same topology;
- have 0 branch self-intersections and 0 boundary edges;
- keep root valence 4;
- stay at aspect ≤ 8.34;
- move the intended measure in the intended direction.

T-4 runs from 90 to 165, the same class as the reviewed AE-E2 probes (tip_sharp 165 as before). There is no catastrophic spike. These are diagnostics, not creator morphs.

## §19 Skin-gracility note

The wrist / knee / ankle skin breadth rows remain diagnostic only. The source was not changed to chase them.

## §20 Visual package (`sheets/`, 20 sheets)

| # | Sheet |
|---|---|
| 01–02 | full body c1 / c2 |
| 03–04 | heads |
| 05 | equal height vs Fenn, ears hidden |
| 06 | thorax / torso bands |
| 07 | leg segments |
| 08 | pelvis |
| 09 | hidden-ear face |
| 10 | AE-E2 lateral / front / rear / top |
| 11 | wire / poles |
| 12 | T-4 / aspect |
| 13 | root integration |
| 14 | AE-E2 vs Fenn E2 |
| 15 | c1 vs c2 |
| 16 | validator margins (+ CSV) |
| 17 | density |
| 18 | body deformation |
| 19 | ear readiness / probes |
| 20 | source → production overlay |

## §21 Production frame / read-back

- **Frame:** m, Z up, faces −Y, subject left +X, origin at the pelvis root on the ground.
- **PC copy:** in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Aelari/RP3/`, staged back byte-identical (`production/pc_readback_sha256.txt`).
- **Blender read-back** (`freeze_check.py`, no save) confirmed:
  - file sha and geometry hash equal the written values;
  - face hash identical on c1 and c2;
  - faces equal the candidate; max geometry difference 6.0e-8 m (roundoff);
  - 1 mesh object, UVMap present;
  - sidecar, branch-map and landmark hashes equal the written values, and branch-map arrays equal the candidate;
  - validator recomputed from the read-back candidate: 69 / 69 on both.
- `AELARI_RP3_freeze_readback.json`: all pass.

The earlier candidate files in the same folder (`bodyfam_v001` / `v002`, ear prototypes) are untouched.

## §22–§23 Records

- **Freeze record** `AELARI_RP3_FREEZE.json` contains:
  - filenames and full hashes, geometry / face / ear-topology / branch-map hashes;
  - corrected-source and ancestry hashes, v005 hashes, Fenn comparison hashes;
  - all gate results, the read-back result and the accepted diagnostic notes.
- **Manifest:** AEL1-R1 / AELF190-R1 marked ACCEPTED + frozen. AELF190 is marked superseded but kept as ancestry. A production pointer was added.
- **Spec and status:** `specs/aelari/AELARI_V1.md` RP3 final status, `specs/STATUS.md`, handoff.

Lineage:
- **c1:** AEL1 → AEL1-R1 → `AE_M_REF_RP3_v001`.
- **c2:** AELF190 route → AELF190-R1 → `AE_F_REF_RP3_v001`.
- **Ear:** AE-E2 + reused Fenn-v002 engineering topology = the Aelari-specific external-ear branch. This is **not** a universal elf topology.

## §25 Next race

**Vael** is the recommended next RP3 race; it has not been started.
- Fenn and Aelari are now separate frozen elven population references.
- Vael must not become "dark Aelari" or "subterranean Fenn".
- Shared engineering (for example the v002 ear topology) may be tested, but Vael body, head and ear biology need their own gate.
- No universal elf topology has been declared.

**STOP FOR CHATGPT REVIEW.**

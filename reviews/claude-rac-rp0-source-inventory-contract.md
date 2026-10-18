# RAC RP0 — source inventory and production-mesh contract audit

**Order:** `reviews/chatgpt-rac-rp0-source-inventory-contract-order.md` (54439cb), under `reviews/chatgpt-rac-retopology-rigprep-master-plan.md` (6af3d00).
**Executor:** Claude.
- The audit was **read-only**: no geometry was edited and no source was written.
- PC files were only listed and staged (copied) into the cloud workspace.
- Blender ran headless in the cloud, read-only. No Blender session was opened on the PC.

**Evidence:** `reviews/rac-rp0-evidence/`
**Contract:** `specs/RAC_PRODUCTION_MESH_CONTRACT.md`
**RP1 plan:** `reviews/chatgpt-rac-rp1-gorrund-production-retopo-pilot-HOLD.md`
**Tools:** `tools/rac/w1/stagec_drivers/` — `rp0_stats.py`, `blend_probe.py`, `blend2npz.py`, `mpfb_probe.py`.

## Decision gate

**RP0 PASS / PRODUCTION MESH CONTRACT READY / RP1 GORRUND PILOT READY FOR RELEASE**

The RP1 release must also:
- accept or amend the flagged **PROPOSED PRODUCTION TOLERANCES** (contract §16: T-1, T-2 with the micro-detail list, T-3, T-6, T-7, and the ±0.15 mm Gorrund nail-projection metric);
- choose the RP1 retopology method (M-A or M-B).

**Every race has a confirmed production-retopo source (class A).** Four non-blocking items for later blocks are listed in §8.

## 1. Search scope and what exists

**Repository:**
- `reviews/reference-assets/manifest.json` (134 assets) with `r6/*.npz` and `builds/*.json`;
- `reviews/rac-w3d-evidence/` (Skarn C1R);
- the Stage C, D4 and race-spec status records.

**PC, `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/`.** Every file was listed (`evidence/pc_source_hashes.txt`).

| Folder | Contents | Classification |
|---|---|---|
| `source/Gorrund-Neutral-C/05AW4/` | **The frozen Gorrund**, with the earlier 05AA–05AW3 checkpoints alongside | Gorrund source; earlier checkpoints are provenance |
| `source/Gorrund-Neutral-C/Gorrund_Neutral.glb` (`513bc9e2…`) | The 05Z3 calibration source | Upstream provenance only |
| `out/` | **The Saurin canonical W2 set** (W2I6), all 7 hashes matching records. Also W1 Saurin, gate and sculpt history, and **pre-RAC prototype bodies** `<Race>_Masc/_Fem.blend/.fbx` (13 races, about 30 Sept 2026) | Pre-RAC bodies are generator artifacts that predate RAC W1 acceptance. For example `Marchfolk_Masc.blend` (`d1dea7b6…`) is an MPFB body with the same 19,158-vertex hm08 topology. **Not accepted; provenance only** |
| `source/Gorrund-*`, `sculpt/`, `candidates/`, `renders/`, `sheets/`, `rodin_analysis/` | Gorrund lineage history, the W2I4 Saurin candidate (identical to W2 canon), renders | Provenance |
| `Content/` (UE5) | Not inspected: the folder is not connected, and RAC never placed accepted race bodies in UE5 | — |

**No newer accepted sculpt or GLB exists** for any MPFB-route race. Their accepted geometry is the procedural reference, which can be regenerated exactly (§2).

## 2. Thirteen-race source inventory

Full detail, with all hashes and statistics: `evidence/source_inventory.json`. Raw statistics: `evidence/mpfb_stats.json`, `sculpt_stats.json`, `go_welded_stats.json`.

### MPFB-route races

All of these are procedural ARMs: MakeHuman MPFB 2.0.17 with the game-engine rig, in the R-6 measurement stance.

**Retopo source.** The editable / high-resolution source is the **MPFB rebuild** from the committed build record. RP0 rebuilt every one of the 16 MPFB realizations below from its build json (`build_variant.py`, MPFB 2.0.17, Blender 5.2.2), and all 16 came out **geometry-identical** to the committed R-6 asset (`evidence/mpfb_rebuild_check.json`). Grask E3 is the 17th: it was proved geometry-identical in Stage C C0.

**What the rebuild has that the npz lacks** (`evidence/probe_mpfb_MF-M-R.json`):
- the quad body (13,378 quads);
- the `UVMap`;
- 204 vertex groups;
- the 53-bone rig;
- 9 MPFB shape keys.

The npz is triangulated and carries 23 summed weight channels and the joints.

| Race | Accepted source(s) | sha256 (R-6 npz) | Provenance | Stature (cm) | Configuration | Class |
|---|---|---|---|---|---|---|
| Marchfolk | `MF-M-R` (c1); `MF-F-R` (c2) | `2caaf056…`; `c254fb4b…` | W1c; W2A bounds | 173.14 / 172.99 | both | **A** |
| Skarn | `SK208-C1R` (c1 body + C1R central face); `SKF208` (c2) | `fd8a43d2…`; `0245683e…` | W1c body, W3D C1R; W2B | 208.01 | both | **A** |
| Sagekin | `SG` (c1); `SGF152-NAT` / `SGF208` (c2 bounds) | `fe45866f…`; `9f096ff6…` / `adb02cc6…` | W1c; RM-OT-05A §2 | 177.99; 152.00 / 208.01 | both (no accepted c2 *central* reference, see §8) | **A** (c1) |
| Fenn | `FNL4` | `9c37d16a…` | W1p | 181.16 | one | **A** |
| Aelari | `AEL1` | `7bc1021a…` | W1m | 190.01 | one | **A** |
| Vael | `VAL4` | `ec73819d…` | W1n | 178.00 | one | **A** |
| Halvren | `HVC1` (central anchor) | `eeda7b31…` | W1s; W2G / W3A1 extremes in the manifest | 177.73 | follows source (one built) | **A** |
| Durrim | `DU137C-NAT` | `6149d149…` | W2H1 (D1 pelvis) | 137.00 | one | **A** |
| Grask | `GR5DE3` (E3, 218) | `d859eb18…` (geometry `a452bf6e…`) | 05D candidates `GR.E3` + 05B arch; **Stage C ACCEPT** (e864a9f) | 217.99 | one | **A** |
| Pipkin | `PK-NAT` | `7b0504e8…` | W1e | 107.00 | one | **A** |
| Cogling | `CGJ7`; `CG76H-NAT` (76 cm) | `6a5ee208…`; `de4e4630…` | W1r; RM-OT-05A §2 | 90.99; 76.00 | one | **A** |

**Commit provenance.** The repository history is a snapshot (72 commits). Acceptance is traced through the named gate documents; the committed asset snapshot is a94bcc6.

### Sculpt-source races

| Race | Accepted source | sha256 | Provenance | Stature | Configuration | Type | Class |
|---|---|---|---|---|---|---|---|
| **Gorrund** | `GO-05AW4_nails_final.blend` (+ `.glb` `e6b32503…`), PC `source/Gorrund-Neutral-C/05AW4/` | `5a4e45d4…2d5e` | 05AX4 (977f671); Stage C reference-only ACCEPT (e864a9f) | 204.5225 | one | Frozen sculpt (Rodin-derived source, UI-sculpted) | **A** |
| **Saurin** | SA-M188 W2 reference = `saurin_w2_final_base.npz` + `saurin_w2_final_surface_delta.npz` → `rebuild_w2_final.py` (libigl upsample + delta) | `f86ae800…`; `f32286c4…`; script `2a96c00f…` | W2I6 canonical (PC read-back match) | 187.86 (full) | M188; c2 = `saurin_w2_SA-F188_realization.npz` `8019420a…` | Canonical sculpt / procedural hybrid; the full surface is rebuilt deterministically | **A** |

**Saurin export warning.** `SaurinW2Final.blend` / `.fbx` (`a87fe590…` / `01ac9d2a…`) is the accepted **preview** export (fast simplification) and **must not** be a retopo source:
- 3,229 boundary edges;
- 1,612 non-manifold edges;
- it is not a closed surface.

## 3. Mesh statistics

| Source | Vertices | Triangles | Components | Boundary | Non-manifold | Degenerate | Duplicates | Genus | Mirror RMS / p99 (cm) | Median edge |
|---|---|---|---|---|---|---|---|---|---|---|
| MPFB family, every race (body only) | 13,380 | 26,756 (13,378 quads) | 1 | 0 | 0 | 0 | 0 | 0 | 0.005–0.013 / ≤ 0.035 | 0.33–0.90 cm (0.39 % H) |
| **Grask E3** (MPFB) | 13,380 | 26,756 | 1 | 0 | 0 | 0 | 0 | 0 | **0.18 / 0.99** | 0.90 cm |
| Gorrund, raw file | 598,717 | 1,124,538 | 5,979 split pieces | 65,472 | 0 | 0 | 59,899 | — | 4.01 / 10.68 | 0.27 cm |
| Gorrund, position-welded (RP0 analysis copy, not saved as a source) | 562,265 | 1,124,538 | **1** | 0 | 0 | 0 | 0 | **3** | 4.02 / 10.80 | 0.27 cm |
| Saurin base | 1,124,235 | 2,248,466 | 1 | 0 | 0 | 0 | 0 | 0 | 1.93 / 6.29 | 0.18 cm |
| Saurin full (base + delta) | 4,496,934 | 8,993,864 | 1 | 0 | 0 | 0 | 0 | 0 | 1.91 / 6.26 | 0.094 cm |
| Saurin SA-F188 | 1,124,235 | 2,248,466 | 1 | 0 | 0 | 0 | 0 | 0 | 1.91 / 6.21 | 0.18 cm |

**Normals.** All closed sources are consistently wound. The MPFB npz frame (x = subject left, f = forward) is left-handed, so its signed volume is negative. Absolute volumes match the guard records; for example GR5DE3 is 107.92 L (05D).

**Self-intersections.** Not recomputed in RP0.
- Gorrund: 0 (05AX4).
- Grask E3: 124 piercing edges in the R-6 stance, below the 157 of its unorganized route (05D guard).
- Other MPFB bodies: not on record.

These are measured per production mesh under contract §6.

**Transforms and units.**

| Source | Transforms | Units | Ground | Placement |
|---|---|---|---|---|
| MPFB | Rig-parented | Metres in the build, cm in the npz | z = 0 | Midline X = 0 |
| Gorrund | Identity object | Metres | z = 0 | X centre +0.22 cm (tail) |
| Saurin npz | — | cm, x right / f forward / u up | z = 0.001 | X centre −0.80 cm (tail and display) |

**Pose.**

| Source | Pose |
|---|---|
| MPFB | R-6 stance, 8° abduction, palms to thighs. A generator rest A-pose `_rest.npz` also exists from the same rig |
| Gorrund | Frozen sculpt neutral stance, no rig |
| Saurin | W2 reference stance |

## 4. Production readiness

| Item | MPFB family (rebuild) | Gorrund | Saurin |
|---|---|---|---|
| UVs | Yes (`UVMap`, MPFB, not final) | **None** | **None** |
| Materials | None | 1 slot `model` | None |
| Vertex groups | 204 (bones + helpers + joints) | 27 (13 segment labels + AV / AW edit groups) | None |
| Armature / weights | 53-bone game-engine rig, MPFB weights | None | None |
| Shape keys | 9 (MPFB targets) | None | None |
| Named landmarks | Rig joint centres; helper eye centres | None. Segment labels can seed the fits | W2 axis / station files (`tools/rodin/w2/`) |
| Separate eyes / teeth / tongue | Helper geometry only, no real meshes | Sculpted closed | Sculpted |
| Nails / claws / tail | Fused (no tail) | Nails and tail fused | Claws and tail fused |
| Deformation risks | Generic MPFB joint loops (adequate density; no race-specific loops). Grask: E3 organization lives on the same 13.4 k vertices | Genus-3 contact loops (hands, axilla); no joint loops (triangle sculpt) | No joint loops (triangle sculpt); dense scale relief |
| Creator-density risks | Face, ears and hands at hm08 density (fine for current targets); compact races at the same vertex count, so very short races have a very small absolute edge (0.33 cm median at 76 cm) | None (over-dense, about 562 k) | None (over-dense, 4.5 M) |

## 5. Known debt (reconciled) and new findings

| Item | Status |
|---|---|
| Gorrund hand-contact loops (L finger / thumb, R finger) | **Confirmed**: the welded genus is 3 (AX4). Repaired in RP1 (D-1, D-2) |
| Gorrund left-axilla micro-tunnel | **Confirmed** (one of the three handles). RP1 D-3 |
| Gorrund perineal / duplicate-position seams | **Explained.** The raw file stores 36,452 positions duplicated along UV-seam splits (5,979 pieces, 65,472 boundary edges). Position welding gives a clean 1 / 0 / 0 surface. RP1 D-4 uses a welded derived copy |
| Gorrund slivers; nail-support subdivision step | Carried. Both are replaced by the RP1 production topology (D-5). The source edge range is 0.04–0.70 cm (p1–p99) |
| Grask chest / abdomen shading band | **Not a gross crease.** The trunk dihedral distribution is in line with W2 GR218R (p99 44° vs 48°; `evidence/grask_trunk_dihedral.json`). Owner: RP2 |
| **Grask E3 bilateral asymmetry (new finding)** | E3 is **not** mirror-symmetric, unlike every other MPFB body. Mirror p99 is 1.06 cm in the trunk band and 1.71 cm (max 1.86 cm) in the shoulder / neck band; W2 GR218R is ≤ 0.11 / 0.01 cm (`evidence/grask_asymmetry.json`). It comes from the 05D race-base organization. It may be linked to the one-sided shading-band read. **Author decision for RP2:** is the asymmetry accepted anatomy, or a construction artifact to symmetrize in production? |
| Grask front-view preservation | Carried as RP2 constraint (contract §9; Stage C final ruling) |

## 6. Topology-family analysis

**The key fact.** Eleven races are already one topology family: every accepted MPFB source has the identical face list (hash `813c59ba…`).

| Planning group | Evidence | Recommendation |
|---|---|---|
| Human-derived (Marchfolk, Skarn, Sagekin) | Same hm08 topology; anatomy expressed by targets and bones; both configurations on the same topology | **Shared** production base |
| Elf / mixed (Fenn, Aelari, Vael, Halvren) | Same topology; ear families are MPFB targets on the same ear vertices; Halvren is the mixed population | **Family-shared with branches.** Ear-density branch. Halvren morph space authored per its source rules, **never** an elf-percentage blend |
| Compact (Durrim, Pipkin, Cogling) | Same topology at 137 / 107 / 91 / 76 cm; adult read, hands and face are critical | **Shared with a compact branch**: added face, hand and foot loops; the 76 cm Cogling adult read is checked |
| Grask | Same topology, but E3 organization (keel, scapular mass, cords, girdle slope) sits on 13.4 k vertices with no dedicated loops; asymmetric; front-view constraint | **MPFB branch with race-specific loop additions** (girdle, keel, joints). Own pilot (RP2) |
| Gorrund | Sculpt; leonine head, tail, feline nails | **Unique** topology; shared standards |
| Saurin | Sculpt; rostrum, display, tail, claws, scale fields | **Unique** topology; shared standards; never a mammalian head layout |

**The deciding tension.** Sharing the MPFB base keeps every accepted MPFB race reproducible and its creator ranges reachable: the morph targets already exist on it. A brand-new hand-made shared topology would need every race re-fitted.

**Recommendation.** **Adopt the MPFB hm08 topology as the production base of the MPFB family**, adding branch loops and a quad-cleanup pass, rather than retopologizing those 11 races from scratch. RP3 / RP4 must confirm this against contract §16. This is a production-standard choice; the author may prefer a new shared topology.

## 7. Pose, landmarks, contract

- **Pose policy** (contract §4):
  - retopology in the reference measurement stance;
  - a rig-prep A-pose only as a derived LBS copy driven by landmarks, with length invariance and round-trip checks;
  - runtime idle out of scope;
  - no posing in RP0 / RP1.
- **Landmark package** (contract §12): root / pelvis, hips, knees, ankles, ball / toes, girdle (SC, acromion, scapular proxy, GH), elbows, wrists, finger roots, neck, head, jaw, eyes, tail chain (Gorrund 12, Saurin 16 proposed), ear / display roots.
  - MPFB: from the rig, exact.
  - Gorrund / Saurin: surface-fit on the source, then re-measured on production.
- **Contract:** `specs/RAC_PRODUCTION_MESH_CONTRACT.md` covers all 15 required topics, plus the proposed tolerances (§16, flagged).

## 8. Items for the author (non-blocking for RP1)

1. **Grask E3 asymmetry:** accept as anatomy, or symmetrize in RP2 (§5).
2. **Sagekin configuration 2** has accepted bounds (SGF152-NAT / SGF208) but **no accepted central reference**. SGF178 is a construction base only and was **not** chosen. Needed before RP3 Sagekin c2.
3. **Reference-asset manifest metadata is stale.** It was not edited in read-only RP0.
   - `GR5DE3*` still read "PENDING AUTHOR / NOT ACCEPTED".
   - The frozen Gorrund `GO-05AW4_nails_final` and the Saurin W2 set are not listed as assets.

   Recommend a bookkeeping update in a later order.
4. **MPFB-family production base:** confirm the §6 recommendation (adopt the hm08 topology plus branches) before RP3.

## 9. RP1

`reviews/chatgpt-rac-rp1-gorrund-production-retopo-pilot-HOLD.md` is prepared and **HOLD**. It contains:
- the source and hash;
- the debt D-1…D-5;
- the immutable anatomy;
- the allowed operations;
- the UI-authoring rule;
- the two methods;
- the gates;
- the output paths;
- the stop conditions.

It is **not** started.

STOP.

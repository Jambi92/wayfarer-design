# Gorrund hands — production mesh and grip validation: closure report

**Date:** 2026-10-23 (supersedes the 2026-10-22 HOLD version of this file, commit 6706ab2)
**Order:** `reviews/chatgpt-rac-gorrund-hand-mesh-grip-completion-order.md`
**Executor:** Claude. Self-inspection only; **no independent acceptance is claimed.**

**Result: PASS — READY FOR OWNER REVIEW.**
- Production hand mesh (rev 110): complete; every gate in §3 passes.
- Movement and grip: every test in §5 passes on every saved frame, checked on Blender's own evaluated geometry of the delivered files.
- Nothing was frozen or promoted. Unreal was not touched. rev 107 and v015 are unchanged (hashes in §1).

Tyler's review request for this pass: the rev 109 thumb tip "looks like a squeezed tube"; make it match the other fingers. That is done in §2.2.

## 1. Inputs and protected files

| Item | State |
|---|---|
| Accepted visible reference | `outputs/Gorrund_Rounded_Fingertips_Review.blend` (rev 107), SHA256 `cdc9e3a9bb74619aee6e4edf4f531cf32be5d211797ac0b3e74c06b05bbe9179`. Re-hashed this pass: unchanged. Read only. |
| Frozen production | `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\production\Gorrund\RP1\GO_U_REF_RP1F_refine_v015.blend`, SHA256 `dfba363e534359193c63dc1700eb54d80f2ee34dbfa3a3cad06b5f87943e5e75`. Re-hashed this pass: unchanged. |
| Native height | 204.51981985 cm. Stature delta vs rev 107: 0.000 mm. No rescale. |
| Unreal / Turnfall / other races | Untouched. |

## 2. Construction method

### 2.1 Base topology (unchanged from rev 109)

The production topology is the accepted RP1E/RP1F v015 quad mesh (M-B), refitted to rev 107:
- outside the hands, all 952 556 vertices are bit-exact copies;
- hand skin is projected onto rev 107 vertex-only, with a light relax;
- the ten fingertip patches are draped onto rev 107's fused claw-and-fingertip disks, with unchanged quad connectivity;
- the distal R middle/ring tissue bridge, which rev 107 separates, is cut and capped with quad grids. This takes the mesh from genus 1 (v015) to genus 0 (matching rev 107).

No automatic remeshing and no QuadriFlow were used. This is the same method substitution reported in rev 109 and still needs owner review.

### 2.2 Thumb tip rebuild (new in rev 110)

rev 107's thumb tips narrow into a pinched neck below a cylindrical tip. To make the thumb read like the other fingers, the **index fingertip shape is grafted onto each thumb** (`thumbsdf.py`):

1. **Target surface.**
   - Build signed distance fields of the thumb tip and of the same-side index fingertip, claw included.
   - Align the index tip to the thumb axis and scale it uniformly (L × 1.215, R × 1.443) so the cross-section matches the thumb at the cut. Uniform scaling is used because a stretch-only template read as a horn.
   - Morph from the thumb field into the index field over a smooth ramp distal of the cut.
   - Extract the surface by marching cubes, clip it at the cut plane, and Taubin-smooth it.
2. **Drape.** The thumb's existing v015 tip patch (L 13 964, R 13 799 vertices) is draped onto that target (`drape.py`):
   - initialisation: authalic, i.e. a Yoshizawa-reweighted Tutte embedding;
   - the claw apex is held by a soft pin instead of a hard vertex pin, because hard pins created folds;
   - quad connectivity is unchanged.
3. **Seam and claw.**
   - The seam is blended back into the unchanged skin over 0.6 cm. The maximum gap at the cut is 0.12 mm (L) / 0.07 mm (R).
   - Vertices within 0.6 mm of the transformed index claw are reassigned as keratin (L 2 125, R 1 822).
4. **Cleanup.** `fixsx.py` removed 27 self-intersecting face pairs by local Laplacian smoothing, re-tested after each round. 0 remain.

Result: a rounded pad and a finger-style claw on both thumbs, with no pinched neck. Visual evidence `S_thumb_before_after.jpg` was sent to Tyler in chat; it is not committed.

## 3. Production mesh gates (rev 110, saved file verified)

**File:** `work/claude110/Gorrund_hand_production110.blend`, object `GO_hand_production110`, SHA256 `133edfde40532244332ac17ea6ad887713d5e700392c36365ef6c31ca20609e8`. The saved file was reopened and compared with the cloud mesh: identical.

| Check | Result |
|---|---|
| Vertices / faces | 1 443 272 / 1 443 270 |
| Quads | 100 % |
| Components / boundary edges / non-manifold edges | 1 / 0 / 0 |
| Euler characteristic / genus | 2 / 0 (matches rev 107) |
| Degenerate faces | 0 |
| Global self-intersections (quad BVH) | **0** |
| Min edge | 0.0016 mm (inside the R thumb claw fan) |
| T-4 face shape: angles 45–135° / aspect ≤ 4 | 88.0 % / 95.4 % (rev 109: 87.5 / 95.4; v015: 91.6 / 96.4). The shortfall against v015 sits in the rigid claw fans. |
| T-5 loops / density | Inherited from v015: about 0.6 mm median hand edge, far below the 6 mm ceiling. |
| T-3 | Stature delta 0.000 mm; bbox vs rev 107 within 0.02 mm. |
| Old nail projection gate | Not applicable to claws and not claimed. The claw direction Tyler approved replaced the nail target. |

**T-2 surface deviation vs rev 107**, hands, outside the two stated exclusions:

| Hand | prod → ref max (p95) | ref → prod max (p95) |
|---|---|---|
| L | 0.44 mm (0.008) | 0.61 mm (0.016) |
| R | 1.21 mm (0.008) | 1.11 mm (0.044) |

**Exclusions, for owner review (not silent waivers):**
1. **Both thumb tips distal of the graft cut.** These are deliberately not rev 107, per Tyler's request; rev 107's tube shape is what was replaced.
2. **R thumb-base crater.** A 1.3 cm sphere around (−25.66, −47.84, 97.76) cm. rev 107 has a pit of thin spikes there (a sculpt artefact). Carried from rev 109.

In total, 34 856 rev 107 vertices are excluded and 27 597 production vertices moved. Data: `rac-rp1f-evidence/claude-hand-mesh-grip/crater_exclusion.json` and the reports zip (`dev2.json`).

## 4. Diagnostic rig (rig_c6, derived copies only)

The bone layout, joint estimates and weights are as in rev 109:
- hand, 4 × (MCP, PIP, DIP), thumb (CMC, MCP, IP);
- joints on geodesic ring centerlines, with human phalanx ratios (estimates, not bible landmarks);
- explicit digit ownership and a harmonic palm transition;
- claws 100 % on their distal bone;
- Blender DQS (Preserve Volume).

There are two changes:
1. **Wider thumb joint blends** (`THW1=1.8`, `THW2=1.6`, `TD0=1.8`, `TW=1.2`). These removed the thenar crease folding that blocked the rev 109 thumb tests.
2. **Soft-tissue correctives** (`gripsolve2.py`). Where skin presses into skin, or into a rigid claw, it is pushed back to the contact surface:
   - skin against skin: half on each side;
   - skin against a claw: all on the skin side, as a dent around the contact (4 rings);
   - crease smoothing where both sides of a contact lie within 10 graph rings;
   - corrections spread harmonically, restricted to the owning digit or palm;
   - 8 rounds per step;
   - a growth cap: no vertex may grow its correction by more than 10 mm.

   For each test, the per-frame correctives are reduced (`keyverify.py`) to a small set of rest-space corrective shape keys with non-negative per-frame weights, stopping once every frame verifies.

**Tolerances (stated, unchanged):**
- skin–skin interpenetration: ≤ 1.0 mm;
- claw contact: ≤ 0.5 mm;
- fixture penetration: ≤ 0.5 mm;
- "contact" means a distance of ≤ 0.5 mm.

The corrective magnitude peaks at about 10 mm, in palm dents and flexion creases (per test in §5). That size of soft-tissue correction is for owner review.

**Diagnostic files**, one per hand. Each crop is split into `GO_hand_<S>_DIAG` and `GO_hand_<S>_DIAG_CORR`, linked by an `orig_id` attribute. Each test carries an armature Action `TEST_<name>` (every solver frame) and a shape-key Action `KEYS_<name>`. Both files are diagnostic and not a game rig.

| File | SHA256 |
|---|---|
| `work/claude110/Gorrund_hand_grip_tests110_L_DIAG.blend` (61 corrective keys) | `a6d2291c5d9bf3c5510616ed5fc8ca5544c48bcfaa6882bb32bfa1d6dca8f377` |
| `work/claude110/Gorrund_hand_grip_tests110_R_DIAG.blend` | `45df1b565b58c1fe1eb1b048793b3e04b5973f97158568e4ad11d4f3fee4f720` |

The three blends were transferred to Tyler's PC in parts and joined there; the hashes computed on the PC (certutil) match the cloud hashes exactly.

## 5. Movement and grip results

**How this was checked** (`blendverify6.py`): the delivered blend files were reopened in Blender. For **every** solved frame of every test, Blender's own armature plus shape-key evaluation was reassembled into the full crop and re-checked:
- new self-intersections vs rest, with depths;
- claw contacts;
- fixture penetration;
- posed bone lengths.

After each test, the actions were cleared and the return to rest measured.

**Results across all tests:**
- 0 failing frames;
- return to rest 0.000 mm;
- bone-length change ≤ 0.0001 mm.

Fixture contacts at the final frame were also re-measured on the delivered (key-blended) geometry (`contactfinal.py`) and match the solver.

Angles are added flexion beyond the reference curl, in degrees.

| Test | Frames | Result (Blender-verified) | Worst skin / claw / fixture (mm) | Peak corrective |
|---|---|---|---|---|
| L pinky bend (MCP/PIP/DIP) | 33 | 38.5 / 41.2 / 27.5, stopped at pad–palm contact | 0.45 / 0.10 / — | 9.7 mm |
| L ring bend | 35 | 38.5 / 48.8 / 32.5 | 0.46 / 0.05 / — | 9.7 mm |
| L middle bend | 36 | 35 / 52.5 / 35 | 0.53 / 0.05 / — | 9.9 mm |
| L index bend | 35 | 35 / 48.8 / 32.5 | 0.47 / 0.05 / — | 8.2 mm |
| L thumb bend | 21 | MCP 40 / IP 60 (full target) | 0.19 / 0 / — | none |
| R index bend | 39 | 7 / 63.8 / 42.5 (MCP limited by the middle-finger pad) | 0.49 / 0 / — | 9.6 mm |
| R middle bend | 33 | 21 / 41.2 / 27.5 | 0.49 / 0.01 / — | 9.9 mm |
| R ring bend | 34 | 28 / 45 / 30 | 0.48 / 0 / — | 9.8 mm |
| R pinky bend | 32 | 35 / 37.5 / 25 | 0.49 / 0 / — | 8.4 mm |
| R thumb bend | 12 | MCP 22 / IP 33, stopped at first new contact | 0 / 0 / — | none |
| L clench | 96 | all four fingers closed onto the palm; thumb curls in along the side of the index | 0.88 / 0.31 / — | 9.8 mm |
| R clench | 82 | all four fingers closed; thumb wraps over the index and middle | 0.50 / 0.50 / — | 10.2 mm |
| L precision pinch (22 × 2 mm coin) | 6 | index 0.29 mm and thumb −0.29 mm on the coin | 0.29 / 0 / 0.29 | 4.0 mm |
| R precision pinch | 4 | index 0.10 mm and thumb 0.19 mm on the coin | 0.13 / 0 / 0 | 1.3 mm |
| R handle grip (Ø 32 × 180 mm, diagonal) | 69 | all four fingers, the thumb (0.21 mm) and the palm (0.44 mm) in contact | 0.48 / 0.01 / 0.48 | 9.0 mm |
| L handle grip | 112 | all four fingers wrapped in contact (−0.47 … 0.15 mm); thumb closes onto the index (0.06 mm), 5.9 mm off the handle; palm 2.7 mm | 0.77 / 0.38 / 0.47 | 5.3 mm |

**Grip forms, stated plainly for the owner:**
- **L clench:** thumb alongside the index. **R clench:** thumb over the fingers.
- **L handle:** a closed power grip with the thumb locked on the index rather than on the handle; on R the thumb is on the handle.

Both left-hand forms are valid closed grips with no violations. If the owner requires thumb-on-handle on the left as well, that is a pose-target change, not a mesh change.

**Solver versions:**
- all bends, both pinches, R handle and L clench: `gripsolve2.py` md5 `865fed32…` (committed as `gripsolve2_v865f.py`);
- R clench and L handle: md5 `3b485c41…` (`gripsolve2_v3b48.py`). The only code difference is one line: the 10 mm growth cap applies only to vertices whose correction magnitude grows by more than 0.5 mm in a step, instead of any vertex whose correction changes.

## 6. Owner review items (decisions, not open failures)

1. The method substitution (§2.1) and the genus 1 → 0 bridge cut.
2. The thumb-tip graft (§2.2) and its T-2 exclusion, plus the carried R thumb-base crater exclusion.
3. T-4 at 88.0 / 95.4 %, concentrated in the rigid claw fans.
4. Contact tolerances (1.0 / 0.5 / 0.5 mm) and soft-tissue correctives up to about 10 mm.
5. The left-hand clench and handle grip forms (§5).

## 7. Reproduction

- **Tools:** `reviews/rac-rp1f-evidence/claude-hand-mesh-grip/tools/`, with rev 109 tools plus:
  - mesh: `thumbsdf.py`, `drape.py`, `fixsx.py`, `mkprod.py`, `gate_dev2.py`;
  - rig: `rig.py` (environment variables above, `KER_OVR`), `mkrig.sh`, `mkcrop.py`;
  - tests: `finalrun6.sh SIDE` (all tests), `addc.py` (corrective settings), `gripsolve2*.py`, `placefix.py`, `placecoin.py`;
  - keys and bake: `keyverify.py`, `kvall.sh`, `bake7.py`;
  - verification: `blendverify6.py`, `contactfinal.py`.

  The scripts use the cloud working path `/tmp/claude-0/hand`.
- **Task configs and verification output:** `.../claude-hand-mesh-grip/tasks110/`, containing the final task JSONs, `manifest.json` and `blendverify_L.json` / `blendverify_R.json`.
- **Per-test reports on Tyler's PC:** `work/claude110/claude110_reports.zip`, SHA256 `2c8ad1473ba7a4ba356c74f5da4ff7836e4c02e351d599d05b3440ed46427f32`. It contains solver outputs, key verification, gates and thumb-rebuild stats.
- **Hash list:** `work/claude110/SHA256SUMS.txt`, with PC-side hashes in `hashes_pc.txt`.
- **Not published:** new raw geometry and images.

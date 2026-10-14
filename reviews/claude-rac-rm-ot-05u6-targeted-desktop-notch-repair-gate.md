# RAC RM-OT-05U6: targeted desktop notch repair gate

**Order:** `reviews/chatgpt-rac-rm-ot-05u6-corrected-guards-targeted-desktop-repair-order.md` (a5279b1). **Parent:** 05U5 (17aa792).
**Evidence:** `reviews/rac-rmot05u6-evidence/`. **Tools (additive):** `tools/rac/w1/rmot05u6_drivers/`.

**Result: U6 TECHNICAL GATES NOT MET. Best safe checkpoint returned (checkpoint 1).**

Checkpoint 1 passes every U6 gate except **R1 target roughness**: 3 of the 16 target vertices are over 36.3°. It is **not** a technically valid bounded return.

Checkpoint 2 was planned but could not be executed. The session's automatic safety check denied the desktop edit. **2 of 3 U6 checkpoints remain unspent.** The stop is a tool-permission stop, not a finding that the method cannot succeed.

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED** |
| Grask E3 | FROZEN |
| RM-OT-05 | **OPEN** |
| Stage C | BLOCKED |
| Reconstructed / edited skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| `base.glb` | unchanged |
| Rodin | not run |

## 1. Corrected verification (built before any production edit; commit 35e9676)

**Frozen sets.** `readiness/u6_sets_v1.json`, sha `34646b31…`, pinned in `u6_guards.py`. Built once from the pinned 05U baseline and the 05U2 proposal:

| Set | Contents |
|---|---|
| **Target** (16) | The 15 cap vertices plus editable vertices within 1.0 cm of them; this adds strip vertex 70433 |
| **R1 baseline exceptions** | 70735, 70592, 70408 (9–23 cm from the cap) |
| **Cap faces** | The 35 approved added faces |
| **Edge band** | 0.25–2.5 cm; all 60 cap edges are inside the band at baseline, so no grandfathered edges |

**`u6_guards.py`** checks:
- R1 target roughness ≤ 36.3 on the target (offenders are not grandfathered);
- R1 exception identity, bit-exact;
- **locus**: every approved editable vertex outside the target is bit-exact, so there is no brush spill;
- **R2 local cap quality**: no degenerate or inverted face, every cap face ≥ 10°, no new edge outside the band.

It also reports, as diagnostics only, the 365-wide roughness and the retired 05U5 per-face-relative rule. The 05U3 guards are unchanged and are still written to `guards.json`.

**`u6_aggregate.py`** exits 0 only if every gate in order §5 passes:
- protection, 0 moved outside the 365, 0 moved on the ring, topology unchanged;
- V1-U2, the no-FAIL-verdict hard rule (retained), V2, V3, V5, V6c-3;
- crease A and B against the frozen reference, by identity;
- R1 (both), locus and R2.

V4, V6 historical, V6c-1 and V6c-2 are reported, not waived.

**`check_return_u6.sh`** is the U4 path plus the U6 guards and aggregate, and a lateral / 3-4 / underside context render. The U4 aggregate is still written, as historical.

**Focused tests:** `readiness/u6_test_summary.json`, **12 / 12 as expected**.

| Test | Shows |
|---|---|
| T1 | The unchanged baseline fails exactly R1 target roughness (61303, 61581, 61580, 62065) and R2 (130139 at 6.24°) |
| T2 | Moving any one exception by 1e-3 cm fails identity |
| T3 | In-target offenders still fail after an edit elsewhere |
| T4 | A new sub-10° cap face fails |
| **T5** | A safe cap face may lose angle while staying ≥ 10° without failing; the retired rule would have flagged it |
| T6 | Brush spill outside the target fails |
| T7 | An inverted face fails |
| T8 | A new edge > 2.5 cm fails |
| T9 | A tampered sets file is refused |
| T10 | NaN fails |

**Disclosed correction:** the first T4 fixture expected face 129905 to fall below 10°. It stays at 13.07°, while its neighbours 130135 (7.38°) and 130137 (9.98°) do fall below. The fixture expectation was corrected; the guard was not changed.

**Baseline under U6** (`readiness/baseline_u6_check/`): NOT MET, on R1 target roughness and R2 only.

## 2. Desktop repair (`EDIT_LOG.md`)

Checkpoint 1 used real Blender UI Edit Mode. Three vertices were picked by click, confirmed by their coordinates and moved by typed positions chosen by hand:

| Vertex | Move |
|---|---|
| 61303 (dent) | +0.25 cm along its normal |
| 62065 (dent) | +0.20 cm along its normal |
| 61405 (valence-3 sliver vertex) | to the centroid of its neighbours |

**Exact changes:**
- vertices 61303, 61405 and 62065, moved 0.250 / 0.142 / 0.200 cm;
- 15 faces touched:
  - 8 cap faces: 129907, 130138, 130139, 130142, 130143, 130144, 130356, 130539;
  - 7 strip faces: 140468, 140482, 140483, 140485, 140488, 140514, 140791;
- legacy diagnostic within the authorized 15 / 35.

## 3. U6 gates for the returned checkpoint (`return/checks/aggregate_u6.json`)

| Gate | Baseline | **Checkpoint 1 (returned)** |
|---|---|---|
| U2 protection; 0 moved outside the 365; 0 ring moved; topology unchanged | PASS | PASS |
| V1-U2; no FAIL verdict; V2; V3; V5; V6c-3 | PASS | PASS |
| Crease A ≥ 0.6713 | 0.8951 | **0.8951 PASS** |
| Crease B ≥ 0.2743 | 0.3658 | **0.3658 PASS** |
| R1 baseline-exception identity | PASS | **PASS** (bit-exact) |
| Locus (editable outside target unchanged) | PASS | **PASS** (0 moved) |
| **R2 local cap quality** | FAIL (130139 at 6.24°) | **PASS**: 130139 at **13.61°**; minimum cap angle 13.61°; no degenerate, inverted or out-of-band face or edge |
| **R1 target roughness ≤ 36.3** | FAIL: 61303 47.95, 61581 47.85, 61580 40.95, 62065 36.57 | **FAIL: 61559 54.23, 61581 42.43, 61580 40.95** (61303 and 62065 now within the limit) |
| **U6 aggregate** | NOT MET, exit 3 | **NOT MET, exit 3** |

**Reported globally, not waived:** V4 fails (8 taper edges); V6 historical fails; V6c-1 fails (θ −90 crease); V6c-2 fails (anterior taper).

**Historical diagnostics:**
- 365-wide roughness: 61559, 61580, 61581 plus the three exceptions.
- The retired 05U5 rule would flag 4 safe faces that lost angle while staying ≥ 15°: 129907 24.2 → 15.3, 130138, 130144, 130356.

**Visual** (identical cameras; `return/checks/compare_*`):
- The lower notch cluster at the cap / strip junction is visibly softer.
- The crease groove and the deltoid / triceps relief are unchanged.
- There is no new spike, lip or melted patch.
- **Saw-tooth marks remain higher along the crease line.** By the view's scale they sit at roughly z 168.8–171.7, partly above the cap's top (z ≈ 170.1) and so partly outside the U2 authorization. This needs Tyler's eye.

The result is **not** visually resolved.

## 4. Remaining blocker (exact)

**Numerical: R1 target roughness on three target vertices.**
- **61559 (54.23°):** a pit between the two lifted neighbours (offset −0.38 cm; outlier face 130142).
- **61581 (42.43°):** crease-A anchor; outlier face 130354 with 61652 / 62052.
- **61580 (40.95°):** crease-B anchor; outlier face 130133 with 61750 / 62086. Crease B's margin is only 0.09 cm.

**Planned checkpoint 2** (`EDIT_LOG.md`): lift 61559 by 0.30, 61581 by 0.10 and 61750 by 0.10 along their normals.

**Procedural:** desktop editing was denied by the session's automatic safety check after checkpoint 1, so checkpoint 2 was not attempted. Continuing needs that permission restored; 2 of 3 checkpoints remain. No scope was widened and no substitute geometry was made.

## 5. Package

`gorrund_05U6_targeted_notch_repair_return.zip` holds:
- the returned scene `GO-05U6_cp1.blend` beside `GO-05T_references.blend`;
- the return checks;
- the checkpoint, readiness, diagnostics and EDIT_LOG;
- the frozen sets and crease reference;
- `MANIFEST.sha256`.

Clean extraction and the corrected-path rerun are recorded in `package/`.

**→ STOP. U6 technical gates NOT MET; best safe checkpoint (1) returned. Awaiting permission to continue (2 checkpoints remain) or an author ruling.**

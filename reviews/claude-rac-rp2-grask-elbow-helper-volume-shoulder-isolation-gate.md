# RAC RP2 — Grask elbow helper-volume study (Stage A) — gate return

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp2-grask-elbow-helper-volume-and-shoulder-isolation-order.md` (8e5021d)
**Parent return:** 95cf747

## RETURN SUMMARY (§14 required statements)

| Question | Answer |
|---|---|
| Did any helper candidate meet §7? | **No.** H1, H2 and H3 each fail §7 on both sides. |
| Did the 130° closed-volume loss improve by ≥ 50 %? | **No.** Best: H2. Left 319 → 238 cm³ (−25.6 %); right 500 → 361 cm³ (−27.8 %). H1 *gains* volume (+125 / +182 cm³) but leaves the full W0 penetration in place. |
| Do left and right helper extents differ? | Yes: left 18 cm, right 21 cm, as accepted under C-3. The helper parameters are otherwise identical. |
| Any new regression? | **Yes, at 130°** for the corrective candidates relative to C2 / C2rx: crease depth, orientation disagreement and max strain. H3 and H2-right add one fold outside the crease. Nothing regressed at ≤ 45° or outside the elbow. |
| Was Stage B (shoulder) executed? | **No.** Stage A did not pass §7, so the order stops here. |
| Shoulder classification | Not produced (Stage B not run). |
| Was a v005 blend built? | No candidate was selected, so `GR_U_REF_RP2_rigdiag_v005.blend` was not built. Every candidate is reproducible from committed configs and tools. |
| Was the full-suite rerun done? | Not triggered (§13 requires a selected helper). |

**Status:** retopology frozen; elbow helper-volume study did not pass; production deformation not accepted.

**Evidence:** `reviews/rac-rp2-evidence/grask_rig_diagnostic_v005/`

**Tools** (`tools/rac/rp/grask_rigprep_v001/`):
- `helper_rig.py` — helper bone and weights;
- `run_helper.sh` — evaluation;
- `helper_judge.py` — tables and §7 checks;
- `stageA_sheets.py` — sheets;
- `quick_cmp.py`.

Evaluator changes:
- `diag_lib.py`: local translation (`'T'`) and local scale (`'S'`) pose entries for helper bones, plus `HELPER=` helper poses.
- `corr_solve.py`: `RIGJSON` / `WEIGHTS` / `HELPER` overrides, so a corrective can be solved on the helper base.
- `diag_run.py`: pose log now accepts vector entries.

The 43-pose suite is unchanged.

## 1. Rulings recorded (from the order)

- **C-1:** C2 is diagnostic proof only; its volume loss is not production quality; the C3-style side bulge is not repeated.
- **C-2:** LBS is the baseline; DQS is comparison only; no DQS keys.
- **C-3:** The asymmetric right support (≈ 21 cm) is accepted; the exact-zero guard is mandatory.
- **C-4:** C2 strain and in-crease folds are acceptable for diagnostics only.
- **C-5:** Elbow first; shoulder only if the elbow passes.
- **K-1:** v002 knees stay.
- **Nail:** Plate Rigidity v2 still gates.

## 2. Immutable parents

`hashes/hashes_before.txt` and `hashes/hashes_after.txt` are both from fresh PC re-stages and are **identical**:
- v003 `03bfe7d9…` / geometry `f9c4a7ac…`;
- v005 `7bba8d2d…` / geometry `2697929d…`;
- all sidecars and the v001 / v002 records;
- rigdiag v001–v004;
- all weight records;
- the v004 corrective record.

Nothing was written to the PC this cycle.

## 3. Helper mechanism (§5)

One helper per side, `elbow_helper_{l,r}`.

**Construction**
- Its rest matrix equals the forearm rest matrix, so its head is the elbow pivot.
- It is parented to the forearm. With zero activation it moves **exactly with the forearm**.
- It takes a share of the **W0 forearm weight only**.
- Consequences: no rest change, no pivot move, no change to segment length, and no change to any other bone's weights.

**Weight checks** (`helper/H1/helper_log.json`)
- Every non-forearm column is bit-identical.
- Rows outside the helper influence are bit-identical.
- The row-sum change is 3·10⁻⁸ (float32).

**Influence**
- Smooth C² bump over rest distance from the pivot: core 14 cm, zero at 18 cm (left) / 21 cm (right).
- Multiplied by a smooth angular mask: inner side and sides weighted, olecranon side not.
- 1.5 cm exact-zero guard from the arm part seams.
- Influence: 4,819 vertices (left) and 5,534 (right); max share 0.999; arm part only.
- Sheet: `sheets/A_helper_field.jpg`.

**Activation**
- β = smoothstep(45°, 130°) of the forearm flexion: 0 at ≤ 45°, smooth through 60 / 75 / 90°, strongest at 110–130°, returning to 0 on extension.

**Helper transform**
- Local **scale 1 + 0.15·β along the forearm flexion axis**, which is the medial-lateral direction. This widens the helper-weighted contact mass sideways, so tissue displaced by contact is not simply removed.
- *Interpretation disclosed:* the order names rotation and translation as permitted helper motions. A single rotation or translation cannot bulge both sides of the elbow at once. This scale is the only way I found to add volume with one transform. If scale is out of scope, every result below is still valid evidence for that decision.

**Pre-candidate exploration** (configs in `config/explore_*.json`, all discarded before the candidates were fixed)

| Helper class | Setting | Result |
|---|---|---|
| Half-rotation | counter-rotation 0.5 toward the bisector | At 130° it drives the inner forearm flesh into the biceps: crease 22.7 mm, max strain 530 %. At 90° it *loses* 148 cm³ (left). |
| Distal counter-rotation | fraction 0.06 | Loses 161 cm³ at 130° (left). |
| Distal counter-rotation | fraction 0.10 | Loses 266 cm³ at 130° (left). |

Mechanism: rotating the inner forearm surface back moves it *into the forearm itself*. Every rigid "move the contact surface away" helper therefore removes volume. That finding is why the candidates use the scale bulge.

**Low-angle identity** (`diag/low_angle_identity.json`)
- At rest (abd45 base): bit-identical, H1–H3, both sides, except H3-right at ≤ 0.00015 mm.
- At 45°: within 0.00004 mm (H3-right 0.00015 mm) of W0.
- Rest-return T-1 = 1·10⁻¹² mm.

## 4. Candidates (§6)

| Candidate | Definition |
|---|---|
| **H1** | Helper only (scale bulge), no new corrective |
| **H2** | Helper + a C2-style pose-space corrective **re-solved on the helper base**. Same configs as C2 (left) and C2rx (right). The keys are smaller wherever the helper already helps, which is the "reduced" corrective. |
| **H3** | One bounded refinement of H2, targeting H2's localised 130° crease failure. The helper share is tapered out of the crease core: zero at 3 cm, full at 6 cm from the pivot. The corrective is re-solved. |

Configs: `config/H1.json`, `config/H3.json`, `config/C2.json`, `config/C2rx.json`.
Correctives: `corrective/corr_H{2,3}_{l,r}_sparse.npz` and their logs.

## 5. Results (LBS)

Files: `diag/stageA_tables.md`, `diag/stageA_judgement.json`.

**Left side.** Each cell gives non-contact / crease (depth mm) / orientation / local inversions / loop / p95 (max) strain % / closed volume vs W0 (cm³).

| Angle | W0 | C2 | H1 | H2 | H3 |
|---|---|---|---|---|---|
| 90 | 0/116 (4.2) / 135 / 0 / 0.32 / 44 (94) / 0 | 0/0 / 0 / 0 / 0.60 / 46 (92) / −27 | 0/114 (4.2) / 133 / 0 / 0.30 / 44 / **+70** | 0/0 / 1 / 0 / 0.60 / 46 (93) / **+40** | 0/0 / 1 / 0 / 0.60 / 45 / +38 |
| 110 | 69/109 (4.0) / 188 / 0 / 0.23 / 40 / 0 | 0/71 (3.1) / 59 / 0 / 0.60 / 57 (130) / −119 | 67/110 / 186 / 0 / 0.20 / 40 / +109 | **0/4 (1.7) / 20 / 0 / 0.60 / 48 (90) / −5** | 0/85 (6.8) / 67 / 0 / 0.60 / 54 / −24 |
| 120 | 124/104 (4.5) / 202 / 0 / 0.20 / 42 / 0 | 0/67 (1.9) / 45 / 0 / 0.54 / 56 / −218 | 121/113 / 203 / 0 / 0.17 / 41 / +121 | 0/59 (3.3) / 26 / 0 / 0.55 / 55 / −117 | 0/142 (4.6) / 91 / 3 / 0.54 / 57 / −131 |
| 130 | 173/112 (5.3) / 211 / 0 / 0.20 / 43 (93) / 0 | 0/41 (3.2) / 93 / 0 / 0.60 / 56 (129) / −319 | 168/120 (5.4) / 210 / 1 / 0.17 / 42 / +125 | 0/**348 (8.2)** / **189** / 0 / 0.60 / 61 (**246**) / −238 | 0/283 (6.3) / 153 / 1 / 0.60 / 60 (174) / −248 |

**Right side** (same cell format)

| Angle | W0 | C2rx | H1 | H2 | H3 |
|---|---|---|---|---|---|
| 90 | 0/126 (3.9) / 156 / 0.38 / 0 | 0/0 / 15 / 0.60 / −31 | 0/126 / 155 / 0.37 / +100 | 0/0 / 14 / 0.60 / **+67** | 0/0 / 11 / 0.60 / +65 |
| 110 | 107/105 / 214 / 0.31 / 0 | 0/6 (1.3) / 19 / 0.59 / −140 | 112/105 / 213 / 0.29 / +157 | 0/9 (0.6) / 30 / 0.60 / **+7** | 0/8 (0.9) / 23 / 0.60 / +5 |
| 120 | 160/106 / 224 / 0.29 / 0 | 0/22 (1.7) / 22 / 0.50 / −320 | 161/110 / 224 / 0.28 / +175 | 0/25 (2.5) / 34 / 0.55 / −171 | **0/0 / 22 / 0.53 / −175** |
| 130 | 205/109 (3.1) / 230 / 0.31 / 0 | 0/52 (3.1) / 79 / 0.46 / −500 | 206/115 / 230 / 0.29 / +182 | 0/175 (3.9) / 147 / **0.56** / −361 | 0/128 (6.2) / 160 / 0.58 / −367 |

60–75°: H2 and H3 match C2 / C2rx on intersections (0), orientation (0) and loop, and *add* volume where C2 removed it.

**§7 checks — failing items** (`stageA_judgement.json → checks`)

| Candidate | Failing §7 items |
|---|---|
| H1 (left and right) | 2 (non-contact intersections remain), 3 (loop), 4 (crease), 5 (orientation). Passes 6, the volume item. |
| H2-left | 4 (crease at 130° 8.2 mm vs 3.2; at 120° 3.3 vs 1.9), 5 (orientation 189 vs 93 at 130°), 6 (volume loss −25.6 %), 7 (p95 strain at 130° 61.2 vs 56.1 %, +5.1 pp; max strain 246 vs 129 %). |
| H2-right | 4, 5, 6 (−27.8 %), plus 1 fold outside the crease at 130°. |
| H3 (left and right) | Worse than H2 at 110–130° on the left. The right side gains at 120° (0 crease intersections) but still fails 4, 5 and 6, plus 1 fold outside the crease. |

**Visual read** (`sheets/A_elbow_{l,r}_{90,130}.jpg`)
- 90°: H2 reads like C2. The inner crease is clean and the sides are slightly fuller.
- 130°: H2 shows a crease spike / fold at the top of the crease, visible in the outer view, and deeper crease contact. This is the limiting failure.
- Sections (`sheets/A_sections.jpg`): H2 keeps C2's flattened contact interface at 130° and does not restore the lost inner mass.
- Plots: `sheets/A_plots.jpg` (closed volume, zone proxy, loop spacing, p95 / max strain per angle, all candidates, both sides).

## 6. Limiting failure and mechanism

**The 90–120° range responds well to helper + corrective (H2).**
- Left 110°: crease 1.7 mm and orientation 20, against C2's 3.1 mm and 59, with p95 strain 48 vs 57 %.
- The corrective-caused volume loss almost disappears: −5 vs −119 cm³ (left 110°), +7 vs −140 cm³ (right 110°).
- At 90° both sides *gain* volume (+40 / +67 cm³) while matching C2's clean crease.

**The 130° range does not respond.**
- The forearm–biceps contact covers a large patch reaching 16–20 cm from the pivot. Removing it still means flattening both surfaces.
- The sideways bulge returns only about 80–140 cm³ of the 320–500 cm³ removed.
- At 130° the bulge also widens the forearm into the crease fold, so the corrective re-solve does not converge there: 135 pairs remain against plane-held targets. This produces the deeper crease (8.2 mm), the orientation cluster and the max-strain spike (246 %).
- H3, which removes the helper from the crease core, does not cure it. So the failure is not crease-core helper influence alone. It is the deep-flexion contact problem itself.

**What this points to** (stated as evidence, not a decision):
- At 130°, the remaining issue needs either a contact model that conserves tissue (a volume-conserving contact solve or a second, biceps-side helper), or an author ruling that a 130° diagnostic limit is acceptable.
- The order prohibits further helper proliferation and topology edits, so neither was attempted.

## 7. Decision required from ChatGPT

- **D-1** Accept H2's demonstrated 60–120° gains as the best elbow configuration *below 130°*, and treat 130° as a separately ruled limit? Or keep C2 / C2rx as the comparison baseline across the whole arc?
- **D-2** Is a helper **local scale** (the medial-lateral bulge) within the authorised helper class? If not, the scale results are evidence only, and a rotation/translation-only helper has been shown to remove volume.
- **D-3** For 130°, authorise one of these, or rule 130° a diagnostic limit:
  - (a) a second, biceps-side helper (one per segment);
  - (b) a volume-conserving contact corrective (contact with redistribution rather than flattening);
  - (c) treat 130° as a diagnostic limit.
- **D-4** Stage B (shoulder failure isolation) was not executed. Authorise it independently of the elbow outcome?

No retopology edit, production rig, production weights, facial work, morphs, UVs or UE5 work.

**STOP FOR CHATGPT REVIEW.**

# RAC RP2 — Grask 130° volume-conserving elbow contact + shoulder isolation — gate return

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp2-grask-elbow-vc-contact-and-shoulder-isolation-order.md` (69f2660)
**Parent return:** fe125b1

## RETURN SUMMARY (§22)

### Track E — 130° elbow

| Item | Left | Right |
|---|---|---|
| Selected candidate | **none** (VC3 judged) | **none** (VC3 judged) |
| 130° closed-volume loss vs W0 (order metric), C2/C2rx → VC3 | 319 → −9 cm³ (**102.7 %** improvement) | 500 → −11 cm³ (**102.3 %**) |
| 130° crease depth (C2/C2rx → VC3) | 3.2 → 2.9 mm | 3.1 → 0.3 mm |
| 130° orientation disagreements (C2/C2rx → VC3) | 93 → 85 | 79 → 68 |
| 130° loop ratio | 0.58 | 0.59 |
| 130° p95 / max strain (C2/C2rx → VC3) | 56 / 129 → 60 / 104 % | 59 / 97 → 61 / 96 % |
| All numeric §10 criteria | pass | pass |
| §10 visual criterion | **fail** | **fail** |
| 130° unresolved? | **yes** | **yes** |

VC3 meets every numeric §10 criterion on both sides. It fails the §10 visual criterion: the restored tissue leaves irregular fold/lump texture along the forearm–biceps contact interface. That does not read as clean flesh compression. Two further bounded tunings of the same VC3 field (M, W; §4.4) did not remove it. Per §11 Track E stops. 130° is returned as an **unresolved production-deformation problem**, not declared an anatomical limit.

**Metric finding the author needs before ruling:** the §10 closed-volume target is measured against W0 LBS. At 130° W0 LBS interpenetrates, and the divergence-theorem volume counts the double-covered region twice: 257 cm³ (left) and 398 cm³ (right), measured with the generalised winding number. Counted physically (overlap removed), against the straight-elbow base:

| 130° | W0 | C2/C2rx | H2 | VC3 |
|---|---|---|---|---|
| Physical volume change, left | −435 | −498 | −416 | **−170** |
| Physical volume change, right | −591 | −694 | −555 | **−182** |

So C2's *physical* corrective-caused loss against W0 is only 63 / 103 cm³, not 319 / 500. VC3 restores far more than that loss: it comes close to the straight limb.

Ring girth shows no balloon. VC3's ring radii 4–14 cm from the pivot stay within −0.7…+0.28 cm of the straight-elbow base. C2 shrinks the limb by up to 0.6–0.8 cm.

### Track S — shoulder

| Item | Result |
|---|---|
| S1 (girdle mechanics) | Fixes the abduction crease and orientation on the right and reduces them on the left. GH-relative elevation falls 82 → 55° in abduction but only 90 → 85–86° in flexion. D1 flex90 is not fixed. |
| S2 (S1 + bounded girdle weight diffusion) | Clears D1 crease on every pose (flex90 16.6 / 14.3 mm → 0 / 0). Orientation 359 / 259 → 115 / 84. Loop 0.19–0.35 → 0.41–0.51. Costs zone volume (flex90 −49 %) and local max-strain spikes (right abd90 209 %). |
| **Primary classification** | **WEIGHTING-DOMINANT** |
| Secondary | Mechanics: abduction, and the left flex90 chest non-contact that needs S1 + S2 together. Weighting trade-off: the smoothed weights lose zone volume. |
| Mechanics materially improve the shoulder? | Yes for abduction and the girdle variants; no for 90° flexion within the current architecture. |
| Weighting materially improves the shoulder? | **Yes**: crease, orientation and loop collapse on every D1 pose. |
| Joint placement implausible? | **No.** GH-forward probe (+2 / +4 cm) trades orientation and zone for strain and does not clear the flex90 crease. |
| Topology contribution remains? | Not demonstrated. Worst loop is still the `shoulder_fan` pair, but weighting lifts it from 0.19 to 0.41–0.51. A residual < 0.50 at flex90 (0.41) is the only remaining loop signal. No retopology touched. |

### Global

| Item | Result |
|---|---|
| Parent integrity | **Identical**: `hashes_before.txt` = `hashes_after.txt` (both fresh PC re-stages; 37 lines). |
| Regression | Track E: none (no selection). Track S: S1 changes exactly the 10 non-ext30 D1 poses; the other 33 poses are bit-identical. S2 changes no retained criterion outside D1. Its only new failures are D1 zone-volume (abd45 L/R, abd90_girdle L). |
| Production deformation accepted? | **No.** Not accepted by this order. |
| Next author decision | See §7. |

**Evidence:** `reviews/rac-rp2-evidence/grask_rig_diagnostic_v006/` (`trackE/`, `trackS/`, `hashes/`).

**Tools** (`tools/rac/rp/grask_rigprep_v001/`):
- `vc_judge.py`, `vc_sheets.py`, `elbow_overlap_volume.py`, `elbow_girth.py`, `elbow_ripple.py`;
- `shoulder_s1.py`, `shoulder_s2.py`, `shoulder_judge.py`, `shoulder_sheets.py`, `full_regress.py`.

Evaluator changes:
- `corr_solve.py`: in-solve volume-conserving redistribution (`volume_conserve`, `volume_keys`, `vol_r_min/max`, `w_vol`, `vol_relax`, `vol_allowed_loss_cm3`, VC2 inner-crease exclusion `vol_inner_exclude_rmax/cos0`), plus trial options `vol_allowed_loss_by_key`, `vol_smooth_iters/field` and `vol_mode='smooth'`. All default off.
- `diag_lib.py`: `POSE_JSON=` replaces D1 pose definitions (Track S); nothing else changes.

The 43-pose suite definition is unchanged.

No v006 blend was built: Track E selected nothing, and the Track S file is optional. Every configuration is reproducible from the committed configs.

## 1. Rulings recorded (order §2–§5)

- **D-1:** H2 is preferred for 60–120°; C2/C2rx are the 130° baseline.
- **D-2:** Helper scale is diagnostic only.
- **D-3:** One 130° volume-conserving study; no second helper; no anatomical-limit declaration.
- **D-4:** Shoulder study independent of the elbow outcome.

Firewall held: v003, v005, sidecars and rigdiag v001–v004, and every prior weight / corrective record are hash-identical. Nothing was written to the PC.

## 2. Track E method (§7)

VC is a pose-space corrective (rest-space shape key, elbow-only drivers) solved like C2. Contact (SDF + bisector plane), loop floor, inversion fairing and the exact-zero guard are as before. It adds an **in-solve volume constraint**.

At each outer iteration of a volume key:
- the closed-volume deficit against the W0 LBS shape of that key is fed back as an accumulating outward offset;
- the offset is distributed over upper-arm **and** forearm soft tissue of the support (rest distance `vol_r_min`–`vol_r_max`, all round the limb);
- contact-held vertices and their 2-ring are excluded;
- the offset enters the same least-squares solve as soft targets, so contact, loop floor and fairing are enforced with it.

Nothing is pushed into the wrist, hand, shoulder or torso (support guard: max |Δ| outside the arm part = 0; `E_field.jpg`). There is no new bone, no pivot change and no rest edit.

| Candidate | Change | Outcome |
|---|---|---|
| VC1 | C2 / C2rx + volume at the 130 key (r 4–14 cm, right 4–16) | Volume restored, but a 20 mm crease spike (max strain 525 / 583 %) at the inner crease (≈ 5 cm, cos θ ≈ 1) |
| VC2 | VC1 + inner-crease sector excluded within 10 cm (cos0 = 0) | 130° passes both sides except: left 120° 2 local inversions (faces 38721, 92022; interpolation 110 → 130); right 130° max strain 142 % (> H2's 107 %), at the side band cos θ ≈ 0, d ≈ 5 cm |
| VC3 | VC2 + 120 key (anchor and volume); right exclusion cos0 −0.4 | All numeric §10 criteria pass both sides (tables below) |

Within-VC3 tuning (bounded; configs and results in `trackE/trials/`):
- Right: A (`vol_r_min` 6 → crease 5.8 mm, nc 3; rejected) and B (cos0 −0.4, **adopted**).
- Left: B (cos0 −0.4 → 120° crease 7.9 mm; rejected), C (per-key 120 allowance; no gain) and D (no 120 volume key; no gain).
- Visual-texture attempts on the adopted VC3:
  - S (smoothed offset field → crease 15.8 / 8.0 mm; rejected);
  - N (smoothed normals; no visual change);
  - M (geodesic 1–4 cm contact exclusion + delta-mush-base normals; right improves numerically: crease 0.0 mm, orientation 62; left orientation 109; texture unchanged);
  - W (M + `w_vol` 2; left worse; texture unchanged).

## 3. Track E tables (§10, §11)

Full tables: `trackE/diag/trackE_tables.md` (W0 / C2|C2rx / H2 / VC1–VC3, 45–130°).

Cells read: non-contact / crease (depth mm) / orientation / local inversions / folds outside / loop / p95 (max) strain % / zone % / closed dV vs W0 cm³.

**Left**

| ° | W0 | C2 | H2 | VC3 |
|---|---|---|---|---|
| 90 | 0/116 (4.2)/135/0/0/0.32/44 (94)/−16.5/0 | 0/0/0/0/0/0.60/46 (93)/−21.0/−27 | 0/0/1/0/0/0.60/46 (93)/−19.1/+40 | = C2 |
| 110 | 69/109 (4.1)/188/0/0/0.23/40/−22.5/0 | 0/71 (3.1)/59/0/0/0.60/57 (130)/−34.4/−119 | 0/4 (1.7)/20/0/0/0.60/48 (90)/−30.3/−5 | = C2 |
| 120 | 124/104 (4.5)/202/0/0/0.20/42/−25.3/0 | 0/67 (1.9)/45/0/0/0.54/56 (94)/−39.4/−218 | 0/59 (3.3)/26/0/0/0.55/55 (92)/−37.6/−117 | 0/37 (3.1)/75/0/0/0.59/57 (94)/−30.0/+5 |
| 130 | 173/112 (5.3)/211/0/0/0.20/43/−27.9/0 | 0/41 (3.2)/93/0/0/0.60/56 (129)/−44.4/−319 | 0/348 (8.2)/189/0/0/0.60/61 (246)/−44.7/−238 | **0/28 (2.9)/85/0/0/0.58/60 (104)/−28.9/+9** |

**Right**

| ° | W0 | C2rx | H2 | VC3 |
|---|---|---|---|---|
| 90 | 0/126 (3.9)/156/1/0/0.38/45/−18.0/0 | 0/0/15/0/0/0.60/46 (95)/−22.9/−31 | 0/0/14/0/0/0.60/46/−21.0/+67 | = C2rx |
| 110 | 107/105 (3.9)/214/0/0/0.31/41/−23.8/0 | 0/6 (1.3)/19/0/0/0.60/48 (95)/−34.4/−140 | 0/9 (0.6)/30/0/0/0.60/48/−31.8/+7 | = C2rx |
| 120 | 160/106 (3.7)/224/0/0/0.29/42/−26.5/0 | 0/22 (1.7)/22/0/0/0.50/54 (94)/−40.5/−320 | 0/25 (2.5)/34/1/0/0.55/55 (98)/−38.7/−171 | 0/2 (0.7)/34/0/0/0.60/54 (95)/−30.5/+11 |
| 130 | 205/109 (3.1)/230/1/0/0.31/43/−28.9/0 | 0/52 (3.1)/79/0/0/0.46/59 (97)/−46.5/−500 | 0/175 (3.9)/147/0/1/0.56/61 (107)/−45.3/−361 | **0/6 (0.3)/68/0/0/0.59/61 (96)/−26.8/+11** |

**§10 checks** (`vc_judge.py`, `trackE_judgement.json`). For VC3 every check below is true on both sides:
- I1: nc = 0 at 130°.
- I2: no new local inversions at 90–130°.
- I3: no folds outside the crease.
- I4: T-1 1.4e-12 mm at every angle.
- C1: crease ≤ ref + 0.5 mm; C1p: crease ≤ 3.5 mm.
- O1: orientation not worse than ref + 10 %; O1p: ≤ 100 / 90; O2: 120° orientation within the 130 preferred limit.
- L1: loop ≥ 0.50; L2: loop not sacrificed.
- V1: ≥ 50 % loss reduction; V1p: ≤ 120 cm³ absolute loss.
- Z1: zone closer to W0 than ref (left −28.9 vs W0 −27.9 / C2 −44.4; right −26.8 vs −28.9 / −46.5).
- S1: p95 ≤ ref + 5 pp at 120 and 130°.
- S2: 130° max below H2's failed spike (104 < 246; 96 < 107).
- R1: 45–90° identical to C2/C2rx (zero activation below 110°).

Below 110° VC3 is identical to C2/C2rx: zero activation, so H2 is not displaced (§9).

**Reported, not hidden:** VC3 left at 120° has orientation 75 against C2's 45 and H2's 26. Its crease is 3.1 mm (C2 1.9, H2 3.3).

**Visual (§10):** see `E_closeup_130.jpg`, `E_elbow_{l,r}_{120,130}.jpg` and `E_strain_*`.
- The contact reads as a closed seam with no upper-crease spike, shelf, pipe or isolated bulge.
- Girth is restored, so there is no balloon: ring radii are ≤ base + 0.28 cm (`E_volume_physical.jpg`).
- **But** the restored tissue on both sides of the contact line shows irregular, crumpled fold texture (three-quarter and outer views). That reads as rumpled skin, not compressed flesh.
- Ripple metric, p95 high-frequency displacement: 1.2 / 1.4 mm against C2 / C2rx 0.9 / 1.0 mm (`ripple.json`).

I judge this a visual fail.

**Explicit §11 answers**
1. 130° volume loss improved ≥ 50 %? **Yes** on the order's closed-mesh metric (102.7 % / 102.3 %). Physically (overlap removed), VC3 loses 170 / 182 cm³ against the straight elbow, versus C2's 498 / 694.
2. Crease within +0.5 mm of C2/C2rx? **Yes** (2.9 vs 3.2; 0.3 vs 3.1).
3. Loop ≥ 0.50? **Yes** (0.58 / 0.59; it repairs C2rx's 0.46).
4. New orientation / local-inversion regression? **None at 130°.** VC3 left at 120° has orientation 75 vs C2 45 (inside the 100 preferred limit). No local inversions anywhere.
5. Visual read improves without a compensating bulge artifact? **No bulge or balloon, but not clean**: the contact interface carries irregular fold texture. So the §10 visual criterion is not passed.

## 4. Track E evidence index (§11)

`trackE/sheets/`:
- `E_elbow_{l,r}_{120,130}.jpg`: W0 / C2|C2rx / H2 / VC3, identical cameras, clay + IDs + wire;
- `E_closeup_130.jpg`: clay close-ups, including trials M / W;
- `E_sections.jpg`: flexion-plane sections at 120 / 130°;
- `E_plots.jpg`: closed volume, zone, loop, p95 / max per angle, all candidates;
- `E_strain_{l,r}.jpg`: strain maps;
- `E_field.jpg`: displacement field and support / volume-band mask;
- `E_volume_physical.jpg`: overlap-aware volume, double-covered volume and ring girth.

Data:
- `trackE/diag/`: results, summaries, tables, judgement, overlap / girth / ripple json;
- `trackE/corrective/`: sparse keys with full-array SHA-256 and solve logs;
- `trackE/config/`, `trackE/trials/`.

Rest return: T-1 in every row (1.4e-12 mm).

## 5. Track S method (§13–§16)

**Baseline:** v002 landmarks, W0, LBS. The GH stays the clavicle tail = upper-arm head, which is the accepted centre.

**S1** (`shoulder_s1.py`, `trackS/config/S1.json`) uses one rule for every D1 pose:
- Scapulothoracic share ST = ⅓·max(0, e − 30°). Here e is the humeral elevation read from the W0 pose, so ST ≈ 20° at 90°.
- Clavicle elevation 0.75·ST; flexion poses add clavicle protraction 0.5·ST.
- Scapula upward rotation 1.0·ST, pivoting at the acromion (tail held: location (I − R)(0, L, 0)).
- The upper-arm local rotation is re-solved on two axes so the **world humerus equals W0 exactly** (direction error 0.0000°).
- ext30 has ST = 0, so it is bit-identical to W0.
- GH–acromion distance is unchanged (5.21 cm both sides).

**S2** (`shoulder_s2.py`, `S2.json`), run only because S1 left flex90 limited:
- the S1 poses plus a bounded weight change;
- region = arm_s and axial vertices within 22 cm of GH (full inside 14 cm);
- effective (normalised) weights diffused on the region graph only (600 one-ring iterations, roughly 5 cm smoothing length), with Dirichlet W0 outside the region;
- rows outside the region are bit-identical; row sums are kept (4e-8).

**S2w** is the same weights with W0 mechanics. It is a factorial control, not a candidate.

**GH-placement probe** (not a candidate; §13 "dedicated comparison"): upper-arm head moved +2 / +4 cm forward on W0 for flex90 / abd90.

## 6. Track S tables

Full tables and kinematics: `trackS/diag/trackS_tables.md`.

Cells read: non-contact / crease (mm) / axillary contact pairs (mm) / orientation / loop / zone %.

| Pose | W0 | S1 | S2w | S2 |
|---|---|---|---|---|
| L abd90 | 0/49 (4.5)/0/49/0.23/−6.6 | 0/32 (1.8)/0/20/0.24/−11.2 | 0/0/0/0/0.45/−30.6 | 0/0/0/0/0.51/−29.1 |
| L flex90 | 38/71 (16.6)/89 (15.6)/359/0.19/−33.9 | 6/76 (21.9)/55/364/0.26/−40.8 | 37/2 (2.7)/95 (16.2)/113/0.40/−45.6 | 4/0/63 (12.5)/115/0.41/−48.9 |
| L flex90_girdle | 0/48 (12.8)/35/195/0.26/−27.5 | 0/27 (4.1)/0/95/0.37/−25.5 | 0/0/0/53/0.51/−38.0 | 0/0/0/57/0.61/−26.5 |
| R abd90 | 0/19 (1.0)/0/9/0.28/−13.4 | 0/0/0/0/0.35/−12.8 | 0/0/0/0/0.41/−33.7 | 0/0/0/0/0.44/−30.8 |
| R flex90 | 0/64 (14.3)/36 (15.9)/259/0.35/−30.6 | 10/63 (15.2)/37/269/0.38/−33.9 | 0/0/0/100/0.45/−44.5 | 0/0/0/84/0.41/−49.0 |
| R flex90_girdle | 0/35 (9.7)/9/86/0.46/−22.8 | 0/0/0/32/0.53/−19.9 | 0/0/0/26/0.52/−37.3 | 0/0/0/27/0.61/−26.7 |

- abd45 and ext30 are clean in every cell. Rest return is 0 everywhere.
- S2 max strain rises at a few native-high-strain edges near the axillary fold: right abd90 209 % (W0 98); right abd45 96 % (W0 52).
- Probe GH +4 cm (flex90): left crease 16.6 → 16.6 mm, orientation 359 → 232, p95 62 → 81 %; right crease 14.3 → 8.9 mm, orientation 259 → 176, p95 66 → 89 %.

**Kinematics** (S1, left / right):
- abd90: ST 20.4 / 19.9°; clavicle 15.3 / 14.9°; scapula 28.0 / 29.6°; GH moves 5.8 / 6.0 cm; inferior-angle proxy moves 4.7 / 3.7 cm laterally; glenohumeral motion 82 → 55°.
- flex90: ST 21.3 / 19.0°; glenohumeral motion 90 → 84.5 / 86.2°.

In this architecture the upper arm is a child of the clavicle and the scapula is a leaf. So clavicle elevation and protraction cannot rotate the humeral frame about the flexion axis without moving GH implausibly (§5 finding).

**Classification: WEIGHTING-DOMINANT.**
- Weighting alone (S2w) clears the flex90 crease (16.6 → 2.7 mm L; R 14.3 → 0) and abd90, cuts orientation by about 70 % and lifts the loop to ≥ 0.40.
- Mechanics alone (S1) fixes or reduces abduction but not flexion.
- Both together are needed only for the left flex90 chest non-contact pairs (37 → 4).
- Secondary contributors:
  - mechanics (abduction rhythm);
  - the volume cost of smoother weights (zone −45 to −49 % at flex90), which a production solution must answer, for example with correctives or helpers;
  - residual contact pairs at flex90 (63 / 12.5 mm L), which are allowed arm–torso contact.

**Visuals:**
- `trackS/sheets/S_{abd90,flex90}_{l,r}.jpg`: front / rear / three-quarter front / three-quarter rear / anterior axillary-fold close-up + wire. Overlays: SC, acromion, scapular inferior and medial proxies, GH, the girdle weight boundary and contact / intersection IDs.
- `S_overview_{l,r}.jpg`: all six D1 poses × W0 / S1 / S2w / S2.
- `S_sections.jpg`: sagittal section through GH at flex90 and frontal section at abd90.

**Regression (§21)** (`full_regress_S.json`, full 43-pose suite):
- S1: only the 10 non-ext30 D1 poses change; 33 poses are bit-identical.
- S2: every pose whose bones touch the region moves (D2–D6 through the abd45 arm set-up, D9 / D10 through the spine and neck weights). D7 / D8 deviate by ≤ 2e-5 cm (float).
- S2 has no new retained-criterion failure outside D1.

## 7. Next author decisions

1. **Track E volume metric.** Accept that the §10 closed-volume metric over-credits W0 by its double-covered overlap (257 / 398 cm³ at 130°). Re-state the target as the overlap-aware physical change against the straight elbow, with ring girth as the balloon check.
2. **Track E 130° texture.** Either accept VC3's contact-interface fold texture as diagnostic flesh compression, which would make VC3 the 130° diagnostic configuration (it passes every numeric criterion), or authorise a different contact model. For example, a contact-surface-aware smoothing restricted to the interface, or a DQS / skinning-model change. 130° stays unresolved until one of these is ruled.
3. **Shoulder.** WEIGHTING-DOMINANT. Authorise a bounded production-direction weighting pass for the girdle (anterior axillary fold / shoulder fan), paired with a volume-preservation answer (zone loss) and the abduction girdle rule as secondary mechanics. Do not relocate GH. Do not retopologise.

**Status:** retopology frozen; 130° elbow unresolved (VC3 numeric pass, visual fail); shoulder classified WEIGHTING-DOMINANT; production deformation not accepted. STOP for ChatGPT review.

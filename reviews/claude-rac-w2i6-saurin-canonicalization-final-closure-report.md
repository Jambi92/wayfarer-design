# RAC W2I6 — Saurin W2I4 Canonicalization / W2I Final Closure Report

**Author:** Claude (auditor) · **Date:** October 9, 2026 · **Order:** `reviews/chatgpt-rac-w2i6-saurin-canonicalize-w2i4-order.md` §1–§13

**Evidence:** `reviews/rac-w2i6-sa-evidence/`:
- `canon6.json` — the canonical file set;
- `verify6.json` — verification;
- `pc_deploy6.json` — PC read-back hashes.

The W2 tool-chain records are in `tools/rodin/w2/`.
**Status:** CANONICALIZATION / RECORD RECONCILIATION — NO NEW BIOLOGY, NO UE5.

## Verdicts

| Item | Result |
|---|---|
| **Canonicalized source candidate** | **W2I4** (exact audited arrays) |
| **W2I5 procedural thigh delta** | **REJECTED / NOT PROMOTED** |
| **Canonicalization** | **COMPLETED** |
| **Canonical W2 reference reproduction** | **PASS** |
| **Scale-field seed realization** | **VERIFIED** (130,949 seeds, identical) |
| **Measurement invariance** | **PASS** |
| **Tail coupling** | **PASS** |
| **§263 verification** | **PASS** |
| **Historical provenance** | **PRESERVED** |
| **Medial / posterior thigh art item** | **DEFERRED PRODUCTION ART PASS** |
| **Saurin W2I overall** | **FINAL ACCEPT / CLOSED** |

**No accepted Saurin biology changed during canonicalization.**
- The promoted base and female arrays are byte-identical to the audited W2I4 candidate.
- No construction route, shared tool or W1 file was modified.

---

## 1. Final canonical files

Folder: `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/out/`. The PC files were read back, and every hash matches.

| Role | File | SHA-256 |
|---|---|---|
| W2 base (SA-M188, L1 + F2) | `saurin_w2_final_base.npz` | `f86ae800a4ef60c7b78ca466433290b7c10e80654df9a02026abb7762353fdee` |
| W2 scale-surface delta (float16, W1 format) | `saurin_w2_final_surface_delta.npz` | `f32286c4759b7c8a1cbeb1afa3727cf19a19624c1708b0715e4ab88ed57a7f63` |
| Rebuild route | `rebuild_w2_final.py` | `2a96c00f5e765701f04860c5eaa5d36a8944e38dd2230ee4a327cc0dae461747` |
| W2 seed realization (130,949) | `saurin_w2_seeds.npy` | `a1d07b8d7001241a2079271686b9e5a91b773b988763c5af9c5f8a92aefe6b05` |
| §263 female-centre realization | `saurin_w2_SA-F188_realization.npz` | `8019420a9ee5c45731698c15fa6a11047bf5e7c1a6cc547b3d52d2716c1fc187` |
| Preview export (accepted fast-simplification route, 562,124 vertices, metres) | `SaurinW2Final.blend` / `.fbx` | `a87fe590…` / `01ac9d2a…` |
| Pointer / lineage note | `SAURIN_REFERENCE_CANON.md` | — |
| W2 region fields (238 MB; scratch, reproducible with `w2i4_drivers/sa_surface.py`) | `saurin_w2_regfields.npz` | `eea2d2fc23a382798caed597fd35b13b94e20a60c432f9900c11659a4217f0af` |

**Array hashes:**
- Base vertices `b50a3d4b…` = the audited W2I4 candidate.
- Faces `ae4fb0a9…` = identical to W1.
- Female vertices `d8504343…` = the audited W2I4 candidate.

The base and female files are the very W2I4 staged files (same file hashes `f86ae800…` / `8019420a…`).

## 2. Proof that the W2I5 delta was not promoted

- `sa_canon6.py`, `sa_toolchain6.py` and `sa_verify6.py` never import the W2I5 sculpt module; the source is `sa_finish.build_f` plus the W2I4 surface.
- The canonical base equals W2I4 exactly: the difference is 0.0 cm and the array hashes are identical. The rejected W2I5 delta (`sculpt_delta.npz` `568074c9…`; max 0.40 cm on 93,166 vertices) would have changed it.
- The canonical surface delta differs from the W2I5 surface delta.
- The W2I5 candidate and evidence stay as rejected-experiment provenance (`reviews/rac-w2i5-sa-evidence/`, `tools/rac/w1/w2i5_drivers/`).

## 3. Tool chain (§5) — W2 counterparts beside W1 (`tools/rodin/w2/`)

| File | Content |
|---|---|
| `ref_metrics_w2.json` | Part 7 reference metrics on W2 SA-M188 |
| `axis_w2.npy` | Gate 8 centreline, 477 samples like W1; tail translated with the pelvis |
| `g7geo_w2_points.json` | ARM S / E / W and LEG H (B1 axis and pelvic station) / K / A on W2, plus the moved hand pad / claw anchor offset (+6.06 cm) used by `g7surfc_moved.py` |
| `lbase_w2_stations.json` | Station indices unchanged; W2 heights: hip 100.2, platform 109.2, costal 132.2, inlet 157.5 cm |
| `s263_w2.json` | §263 re-verification (§6) |
| `README.md` | Lineage |

**Unchanged:**
- The regional stature route and isometric tail / caudal-base treatment (the accepted W2I route).
- The W2 region fields (carried `g15reg` labels + recomputed N / T; the hash is in §1).
- The W1 tool chain: `git diff` since W2I4 on `tools/rodin/gate1`, `gate8`, `creator-biology` and `female` is empty.

## 4. Canon / status / queue files updated (§6–§7)

**`specs/saurin/SAURIN_V1.md`:**
- status line;
- Part 7 **W2 reference update** — canonical files and hashes, provenance, and the §7 final canon statement verbatim;
- §17 forearm interpretation;
- the stature-share W2 budget;
- the §256 presentation-context note;
- the §257 W2 stance (~6.2 cm, ~8.4°);
- the §258 W2 re-verification;
- the §263 W2 accounting;
- §265: the deferred thigh art-pass item, D-B and D-D;
- a closing W2 update line.

The aff1b52 figures are kept as provenance.

**`decisions/REFERENCE_ANATOMY_V1.md`:**
- a new ARM row: canonical Saurin W2 reference, with aff1b52 / the historical SA-F as provenance;
- a §10 rule: art debt does not block race-design closure, and a rejected procedural experiment is never promoted.

**Records:**
- `cfg/w2i/SA-boundary.json`: `rulings_w2i5`, the `w2i6` block, references re-labelled (W2 canonical, W1 provenance);
- the W2I5 report author-ruling line;
- the issue record;
- the queue;
- `specs/STATUS.md`.

**What the records distinguish:**
- Canonical W2 biology — closed.
- Canonical W2 reference asset — the W2I4 candidate, promoted.
- Deferred art debt — the medial / posterior thigh relief only.
- W2I5 — rejected experiment, kept as provenance.

## 5. Verification (§9)

| # | Check | Result |
|---|---|---|
| 1–4 | Base, surface-delta, seed and SA-F hashes recorded and re-read from disk and from the PC | match |
| 5 | Rebuild script / tool-chain records point to the W2 canonical files | yes (`rebuild_w2_final.py`, `SAURIN_REFERENCE_CANON.md`, `tools/rodin/w2/README.md`) |
| 6 | The shipped rebuild reproduces the audited W2I4 surfaced reference | max 6.2e-5 cm, rms 5.4e-6 cm (float16 delta storage, the same format as W1) |
| 7 | Seed count / realization | 130,949, identical to W2I4; region fields identical |
| 8 | No W2I5 delta | §2 |
| 9 | Biological measurements | SA-M188 / SA-F188 measured from the canonical arrays vs the audited W2I4 body set: 61 measures each, max relative difference 1.5e-6 (float32 storage). Hip / H 0.5333, femur / leg 0.420, forearm / arm 0.366, lower trunk 32.0 / 33.6 cm, d/w 0.880 / 0.922, tail 64.6 %, root area 529.21, lean 8.42° |
| 10 | Tail coupling | Unchanged: the canonical arrays and route are identical to W2I4, so the W2I4 tail caps stand (Balanced 78.875 %, Broad 80.25 %, Narrow + high fat 79.625 %, Broad 208 79.75 %, 55 % low end A50) |
| 11 | §263 | W2I SX suite unchanged. `s263_w2.json`: lower trunk, pelvic width, d/w, head length / H and waist / hip identical to W1 accounting |
| 12 | No W1 asset overwritten | PC `saurin_final_base.npz` `a925e067…`, `saurin_final_surface_delta.npz` `b72691ab…`, `rebuild_final.py` `722b0420…`, `SaurinFinal.blend` / `.fbx` unchanged (original October 4 mtimes and hashes) |

**Note on check 11 — waist / shoulder.** Frontal waist / shoulder, read with silhouette bands carried with the moved stations, is:
- male centre 0.465 (W1: 0.468);
- female centre and reference female 0.532 (W1: 0.539).

The F2 arm distribution widens the shoulder band by 0.4–0.7 cm, and the sex difference is preserved. This is recorded as the W2 value in §263; it is not a §263 change.

**Shared tools.** No shared tool changed, so the full race-family regression was not re-run (§9 allows this). The W2I4 62-body regression stands.

## 6. Provenance preserved (§8)

**Kept unchanged:**
- W1 aff1b52 (`saurin_final_*`, `SaurinFinal.*`) and the historical SA-F;
- W2I3, W2I4 and W2I5 candidates and evidence;
- all prior gate reports and hashes.

No historical file was renamed or rewritten. The W2 set uses new names. The lineage is recorded in:
- `RaceBodies/out/SAURIN_REFERENCE_CANON.md`;
- the SAURIN Part 7 W2 reference update;
- `cfg/w2i/SA-boundary.json`.

## 7. Final W2I dispositions (§10)

| Item | Disposition |
|---|---|
| Saurin stature family | **FINAL ACCEPT** |
| Saurin axial / pelvic body system | **FINAL ACCEPT** |
| Saurin frame system | **FINAL ACCEPT** |
| Saurin composition firewall | **FINAL ACCEPT** |
| Saurin limb / joint body validation | **FINAL ACCEPT** under prior accepted rulings / named measurement dependencies |
| Tail coupling / RM-UB-04 | **FINAL ACCEPT** |
| RM-OT-04 | **FINAL ACCEPT** |
| RM-UB-08 body numeric ranges | **NAMED DEPENDENCY** |
| SAU-SILHOUETTE | **ACCEPT WITH PRESENTATION CONTEXT** |
| Saurin W2 reference anatomy | **FINAL ACCEPT** |
| Saurin W2 reference asset | **FINAL ACCEPT** with the deferred medial / posterior thigh production art-pass item |
| **Saurin W2I overall** | **FINAL ACCEPT / CLOSED** |

## 8. Remaining named dependencies

| Item | Classification |
|---|---|
| **Saurin W2 medial / posterior thigh relief** | **DEFERRED PRODUCTION ART-PASS ITEM.** Non-biological, non-measurement-bearing and non-blocking. Scope: restore native-scale hamstring / adductor relief, remove the W2I4 sector-transition marks, and clean the inherited medial-thigh Rodin tear, while preserving the thigh volume / silhouette and the W2 seed realization. To be done as a future localized hand sculpt (Blender / ZBrush), regression-tested before production acceptance. |
| RM-UB-08 numeric creator ranges; RM-UF-04; remaining facial measurement rows; claw numeric creator ranges | NAMED DEPENDENCY |
| Final density model; final neutral idle / dynamic posture; SAU-BODY-20 world-space implications; final creator-envelope interpolation | NAMED DEPENDENCY / LATER WORK |
| UE5; rigging; animation; equipment fitting; gameplay implementation | OUT OF SCOPE / LATER PHASES |
| D-B (Broad ~80 % / Broad 208 span), D-D (skeletal-mass rows) | ACCEPTED MARGINAL / ACCEPTED DEPENDENCY |

**STOP.** W2I closed. Wave 3, Halvren references, the roster world-scale review, the creator envelope, UE5, rigging, animation, equipment and gameplay were not begun.

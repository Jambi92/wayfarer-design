# RM-OT-05F Gorrund hand-sculpt handoff package

Brief: `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md` (read first)
Gate: `reviews/claude-rac-rm-ot-05f-gorrund-hand-sculpt-handoff-gate.md`

**FROZEN** (freeze order `reviews/chatgpt-rac-rm-ot-05f-handoff-author-ruling-freeze-order.md`): Q1 approved, waist wording corrected in the brief. Gorrund: **EXTERNAL SCULPT REQUIRED — AWAITING ASSET**. `figures/region_map.png` is an editing-jurisdiction guide only; the brief text governs anatomy.

Nothing in this folder is an accepted Gorrund body. The start mesh is the *unorganized* accepted skeleton route; the failed 05C–05E candidates appear only as labelled "must not" evidence.

## 1. External asset required

| | |
|---|---|
| What | One hand-sculpted Gorrund body surface, hard-form organization only (brief §4) |
| File | `GO_sculpt_<ID>_r6.obj` (Wavefront OBJ, positions + faces) |
| Topology | Exactly the start mesh: 13 380 vertices in the same order, identical faces (MPFB base topology without helper geometry) |
| Frame | cm, Z up, ground z = 0, +Y anterior, +X body left, R-6 neutral stance, 230.90 cm |
| Optional | High-resolution detail (subdivided mesh or displacement / normal map) for later texture work; not validated here |
| Who | External sculptor or a direct mesh-edit workflow. This session has no interactive sculpt tool (no Blender / ZBrush), and the order forbids faking a sculpt procedurally. |

## 2. Contents

| Path | What |
|---|---|
| `template/GO_ref_route_r6.obj` | **Start mesh**: unorganized accepted-route Gorrund reference (230.90 cm, reference composition, R-6) |
| `template/GO_low_route_r6.obj` | Same route at low composition (muscle 0, weight 0.5; 230.75 cm). Persistence preview, not sculpted |
| `template/GO_true_floor_r6.obj` | 05D true skeletal floor: the hard inner limit |
| `template/GO_old_lean_r6.obj` | Superseded MPFB `-LEAN` guard (context only; the sculpt may go inside it) |
| `data/joints_r6.json` | Accepted R-6 joints in the template frame (read-only) |
| `data/stations.json` | Stature, skeleton-anchored station data, protected Gorrund relations (05D semantics), canon relation clauses |
| `data/regions.json` | Vertex indices of families A–F and the no-touch zones |
| `figures/region_map.png` | Families A–F and no-touch zones on the start mesh (front / ¾ / profile / rear ¾) |
| `figures/floor_margin.png` | Inward sculpt budget: start-mesh height above the true floor |
| `evidence/05d/stageA_GO_{pelvis,shoulder}.png`, `stageA_GO_allowed.json` | **Accepted skeletal floor / protected relations**: old guard vs true floor vs surfaces, and the allowed-movement table |
| `evidence/05e/e_GO_{F,Q,P,RQ}_grey.jpg`, `e_GO_{F,P}_sil.jpg` | **Matched camera and silhouette standard.** The bodies shown are *failed human-reading examples* (Gorrund 05D E1 / E2, 05E P1–P3) next to Marchfolk, Skarn and Grask E3 |
| `evidence/05e/e_GO_low_P.jpg` | **Low-composition persistence requirement**: the low state of each failed candidate |
| `evidence/05e/c_229_{knee_F,knee_P,forearm_F,back_R}.jpg` | Close strips of the failed limb and back organization (what *not* to do: pillar / human taper / flat-backed heavy human) |
| `evidence/05e/blind_{J,K}_grey.jpg`, `blind_summary.json`, `e_limb_profiles.png` | The 05E replicated blind failure (context effect) and the limb-taper evidence |
| `evidence/05d/d_GR_{F,P}_grey.jpg`, `d_GR_low_P.jpg` | **Grask E3: contrast case only.** The accepted non-human Grask read that Gorrund must stay distinct from and must not borrow (scapular mass, keel, high calf and long cord) |
| `evidence/05d/d_GO_P_grey.jpg` | 05D Gorrund E1 / E2 profile (failed) |
| `validator_selftest/` | Proof that the re-entry validator and blind tally work (§4) |

## 3. Pipeline (re-entry)

All in `tools/rac/w1/rmot05f_drivers/`.

| File | Role |
|---|---|
| `f_export.py` | Regenerates `template/` and `data/` |
| `f_regionmap.py` | Regenerates `figures/` |
| `f_ingest.py` | Ingest checks I1–I6 + coverage; converts the sculpt to a skinned-frame displacement field |
| `f_reentry.py` | One command: ingest → build reference / low / Narrow / Broad → `f_guard` → transport report |
| `f_guard.py` | The 05E / 05D guards, thresholds unchanged, for `GO5F<ID>` bodies |
| `f_blind.py` | Replicated blind runner: 8 controls + Grask E3 reference / low + sculpt reference / low; fresh shuffle per run and per sculpt ID |
| `f_scorer_prompt.md` | The verbatim scorer prompt (JSON answers) |
| `f_tally.py` | Mechanical 05F pass condition (G1–G7) |
| `f_selftest_inputs.py`, `f_tally_selftest.py` | Self-tests |

**Code change outside the drivers:** `race_base.sculpt_layer` / `skin_frames`, spec key `sculpt`. It is inert without the key.

## 4. Validator self-test (`validator_selftest/`)

These are pipeline checks, not candidates.

| Test | Input | Expected | Result |
|---|---|---|---|
| T0 identity | The start mesh itself | Ingest PASS; rebuild = route; all guards pass at reference / low / Narrow / Broad | PASS. Volume 1.0000; reproduction error p90 0.000 cm (max 0.165 cm where the route already touched the floor); protected relations unchanged |
| T1 transport | The failed 05D E1 surface used only as a known non-zero signal | Ingest PASS; reference rebuild reproduces it; displacement carried to low / Narrow / Broad | PASS. Reference reproduction error 0.000 cm. Retention median 0.94–1.01 per family (low), 0.99–1.01 (Narrow / Broad) |
| X1 | Template × 1.02 | FAIL (I2 / I3) | FAIL as expected |
| X2 | Thigh pushed 4 cm inside | FAIL (I5) | FAIL as expected |
| X3 | Left hand moved 1 cm | FAIL (I4 / I6) | FAIL as expected |
| Tally | Synthetic scorer JSON: pass, and 7 failing variants (bulk basis, low-composition B, control in group, merged with Grask, no cues, control C, single run) | Pass only for the full pass case | OK |
| Blind runner | Dry run with T1 as the slot body | Renders a 12-body sheet labelled DRY RUN | OK (`blind_P_F05a_T1_DRY_grey.jpg`; not scored) |

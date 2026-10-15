# RAC RM-OT-05V — Gorrund ARM whole-body neutralization: closure gate

Order: `reviews/chatgpt-rac-rm-ot-05v-gorrund-arm-neutralization-closure-order.md` (Option 1, whole-body neutralization).
Date: 2026-10-14. Evidence: `reviews/rac-rmot05v-evidence/`. Drivers (all new and additive): `tools/rac/w1/rmot05v_drivers/`.

## Outcome

**RM-OT-05V BLOCKED — REPLICATED NEUTRALIZED BLIND GATE FAILS: C5-REF 0/3 IN BOTH RUNS. The neutral body is read through muscularity, limb bulk and a bent-knee posture (rated "major" by 6/6 scorers), not through structure. R-6 knee extension and R-4 reference composition are also NOT MET.**

What this means:

- The neutral candidate GO-ARM-N1 is technically clean:
  - all 12 neutralization steps PASS;
  - outside each group it is bit-exact;
  - the U6–U8 repair is bit-exact;
  - it is manifold with no self-intersections;
  - every reconstructed surface is labelled INFERRED;
  - the feet are five-toed and plantigrade;
  - R-13 stature is 231.0 cm, consistent with GOREF.
- It fails the mandatory body-only structural-readability gate (§7).
- It also fails the R-6 stance requirement in a way a rigid or semi-rigid pose derivative cannot fix without re-sculpting the legs (§6 STOP condition).

Consequences:

- Gorrund is **not** recorded as ARM.
- RM-OT-05 stays **OPEN**.
- Nothing is written to the RMQ or to GORRUND_V1.
- **Stage C is not started**, and no variant scaffold was derived (§9 is gated on acceptance).
- U8 cp1 (`2341d554…`) is unchanged. `base.glb` is unchanged (`78ecfa87…a7b`, asserted by `v_tail.py`).

## 1. What was built

| Item | Value |
|---|---|
| Source | U8 cp1 `GO-05U8_cp1.blend` sha `2341d55445a448e24852f98fd9df3984ab12d706ef0b455cb4a2cdb0782860d6` (asserted, never written) |
| Candidate | `GO-ARM-N1.blend` sha `817f2cf1821405994561959bd5a18755f6664096e850951c09fc7d923500d0a8`. Object `GO-ARM-N1`: 188,820 vertices / 377,636 faces. The U8 object is kept hidden and bit-exact inside the file |
| Final state | `S12_E2.npz` sha `6b706c7d399b435c22df876fe9ef02664cc6314846ed437864178365aa9fead1` |
| Method | Local implicit region rebuild per group (`v_rebuild.py`). Faces outside the step region are kept bit-exact. The region is re-extracted from a blended source / inferred signed-distance field and bridged at the seam. No global remesh, smoothing or Dyntopo |
| Plan | `readiness/NEUTRALIZATION_PLAN.md` (v1 + amendments v2 neck, v3 C3/E2), frozen in `v_chain.py`. Steps: A1 A2 B1 B2 C1p C1m C2p C2m D E C3 E2 |
| Chain | `chain/chain.txt`: per-step state sha, verdict and time. All 12 steps PASS `v_verify.py`: P1/P2/P3 protection, P4 U6–U8 bit-exact (783 vertices), T1 manifold/orientation/no boundary, T2 no self-intersection, Q1 min angle ≥ 10°, L1 labels |
| Round trip | `t_export_blend.py` export is bit-exact (V, F, ids) — `blend/roundtrip.json` |
| Provenance | Point attribute `rac_s3_vid1` (S3 identity; INFERRED ids above 70,751). Face attribute `rac_fgrp` (0 inherited, 1–5 INFERRED groups A–E, 9 seam). Vertex groups `INFERRED_A…E` / `INFERRED_seam`. Text block `RAC_05V_README` |
| Inferred share | **93 % of the surface area is INFERRED reconstruction** (labels 1–5 and 9). Only 7,623 faces are inherited source surface |

Groups (§3):

- A: overlays, braids, necklace and flaps removed; the underlying torso and back surface was reconstructed.
- B: bracers and the −X armband removed. The −X arm was transplanted from the mirrored +X arm (B2); no generic human template was used.
- C: shin wraps removed. Feet rebuilt as five-toed humanoid, non-prehensile, nailed, plantigrade forefeet at source scale (`v_feet.py`), plus a knee fairing (C3).
- D: belt and loincloth removed. Iliac crest, ASIS, inguinal, gluteal and sacral regions are exposed and reconstructed. No modesty proxy was needed. No sex-specific anatomy was added.
- E: mane removed. The cranium vault, neck, upper back and ear roots were reconstructed (E, E2); the face was re-extracted from source.

Renders: `renders/grpA_overlays.jpg`, `grpB_bracers.jpg`, `grpC_shins_feet.jpg`, `grpD_pelvis.jpg`, `grpE_mane_neck.jpg` and `U8_vs_N1_vs_R6.jpg`. Each shows front, profile and back, with INFERRED surface tinted tan.

## 2. R-13 stature (§5) — PASS

| | cm |
|---|---|
| Raw full vertical extent (top = ear pinna) | 237.35 |
| **Anatomical stature to skull vertex** (ears excluded; no hair, mane or keratin remains) | **231.0** |
| GOREF | 230.9 (Δ +0.1) |
| R-6 measurement-pose derivative | 230.51 |

Caveat: the cranial vault is INFERRED. It is a builder-chosen ellipsoid from plan step E, so 231.0 cm is a construction value consistent with GOREF, not an independent discovery. No scaling was applied. Source: `measure/N1_measure.json`.

## 3. R-6 stance (§6) — NOT MET (STOP condition)

Candidate as built (`N1_measure.json`):

- The heels are 1.5 cm off the ground, standing on the forefoot.
- Arm abduction is about 12° with the arms about 15° forward.
- The thigh-to-shank surface-centroid angle is 18–21° on both legs.
- Trunk lean is about 2°.
- Heel separation is 49 cm against a hip separation of 38.6 cm.

Measurement-pose derivative `N1R6.npz` (`v_r6.py`, `measure/N1R6_pose.json`):

- One rigid whole-body pitch of −2.135° about the forefoot contact line.
- Heels now contact: gap 0.12 cm, 77 / 104 contact vertices.
- Lengths are unchanged (max pair-distance change 6e-14).

What is still not met:

- **Knee extension.** The 18–21° thigh/shank offset is built into the surface: the sculpted thigh, knee and calf masses form a zig-zag profile, and soft tissue and joint angle cannot be separated without a skeleton.
- **Forward arm carriage** (about 16° forward).

The source has no rig and no joint centres. Correcting these would need segment-wise re-sculpting of the legs, which is material anatomical deformation, so §6 requires STOP here.

The blind scorers confirm it: `posture_read = true` for the candidate from **6/6** scorers ("bent-knee", "bowed", "forward-pitched"), on the R-6 derivative.

## 4. Replicated neutralized blind gate (§7) — FAIL

Pre-registration: `blind/PREREGISTRATION.md`, committed in 446516c before any scoring. Protocol:

- Uses the 05O scorer prompt unchanged except for the code range 01–11.
- Uses the same frozen control tiles as 05K/05N/05O: MF and SK ref/nar/brd/low, and Grask E3 ref and low.
- The candidate is shown as `GO-S-ref`: the R-6 derivative, body only, neck cut at z 191.
- Two runs (V, W) with fresh shuffles; 3 fresh, uninformed scorers per run.
- Each scorer received only the two sheet images. Keys: `key_V.json` / `key_W.json`.

Result (`blind/gate_eval.json`, mechanical, `v_gate_eval.py`):

| Criterion | Run V | Run W |
|---|---|---|
| C2 not collapsed to Marchfolk | 3/3 ✔ | 3/3 ✔ |
| C3 not collapsed to Skarn-Broad | 3/3 ✔ | 3/3 ✔ |
| C4 distinct from Grask E3 | 3/3 ✔ | 3/3 ✔ |
| **C5-REF structural reasons** (primary driver structural AND posture / fat / muscularity / boxiness ≤ minor AND no posture read) | **0/3 ✘** | **0/3 ✘** |
| C1 / C5-LOW | not evaluable (no LOW exists) | not evaluable |

Per-scorer, for the candidate:

- Class C in 6/6.
- Primary driver: `segment_relations` 4, `muscularity` 2.
- **muscularity "major" 6/6, limb_bulk "major" 6/6, posture_pose "major" 5/6.**
- Typical labels: "massive hunched, bow-legged brute", "hulking hyper-muscular humanoid".
- Scorers grouped Grask E3 ref and low together (as expected) and separately from the candidate.

Reading: the body is distinct from human and Grask, but it is distinct **because of extreme muscle bulk and a bent-knee stance**. That is the ogre/brute-stereotype route §7 says must be ruled out. It is not read as structural organization. Even if C5 had passed, the gate could not PASS as pre-registered, because C1 needs a LOW variant, and §9 forbids deriving one before acceptance.

Disclosed protocol defect: the tail mask in `v_blind.py` (2.5 cm from the placed tail) left a small detached tail fragment visible beside the profile. All six scorers mentioned it. It does not change the result: the failing ratings (muscularity / limb bulk / posture "major") are reported by every scorer, independent of the fragment.

## 5. R-1…R-14 audit (candidate GO-ARM-N1 / R-6 derivative)

| Rule | Result | Evidence |
|---|---|---|
| R-1 central-tendency adult | Not demonstrated | Blocked by R-4 / blind gate; 93 % INFERRED |
| R-2 stature by proportion | PASS (construction value) | 231.0 cm vs GO 229 / GOREF 230.9; no scaling |
| R-3 skeletal frame central | Not evaluable | No skeleton / joint centres in source lineage |
| **R-4 reference composition** | **NOT MET** | Source build is extreme-muscular; neutralization did not change composition (order §2 froze massive body organization); 6/6 scorers rate muscularity "major" |
| R-5 symmetry | NOT MET (minor) | Mirror residual median 0.43 cm, p90 2.4 cm, max 29 cm (asymmetric hand/arm pose inherited from source) |
| **R-6 measurement stance** | **NOT MET** | §3 above: knee offset 18–21°, arms ~16° forward; heel contact achieved only by rigid derivative |
| R-7 neutralization (N3) | PASS | Groups A–E: no clothing, jewellery, wraps, bracers, armband, belt, loincloth; no proxy needed |
| R-8 hair | PASS | Mane, braids and chin display removed; vault is zero-hair reconstruction |
| R-9 surface | PASS (geometry) / note | Single default material; reconstructed surface carries soft lumps from the field blend, which are not textures but do affect silhouette locally |
| R-10 sex configuration | No change | No sex-specific anatomy invented (order §3 D) |
| R-11 mandatory race anatomy | PASS | Leonine head and ears, tail (base.glb comp 4, 05N placement), plantigrade five-toed feet |
| R-12 no contamination | PASS | No equipment, weathering or cultural items remain |
| R-13 units / stature to skull vertex | PASS | §2 |
| R-14 provenance | PASS | Builder values in `NEUTRALIZATION_PLAN.md` / `v_chain.py` PLAN (all field radii, offsets, foot layout, tail placement, R-6 pitch); labels in the blend |

Other mandatory items:

- **Plantigrade five-toed feet:** PASS. 5 digit tips per foot; plantigrade contact in the R-6 derivative.
  - Flag: foot length is about 62 cm, 27 % of stature, inherited from source scale.
- **U6/U7/U8 no regression:** PASS. P4 is bit-exact at every step (783 vertices).
- **UCCA §24 tiers A/E/I and pairwise / boundary tests:** not run past the STOP. The mandatory blind gate and R-6 / R-4 already fail, and the order says to STOP on a failed mandatory gate.

## 6. What a passing route would need (author decision; not executed)

1. A **reference-composition** body. Muscularity and bulk must come down to the population centre per R-4, while keeping the frozen §2 relations. This conflicts with the order's freeze of "massive body organization" as realized in U8, so the author must rule which takes precedence.
2. An **R-6 leg** with extended knees. This needs segment re-sculpting or a rigged re-pose; a rigid derivative cannot do it.
3. A **LOW composition variant** so C1 / C5-LOW can be evaluated. It is currently forbidden before acceptance (§9), so the gate is structurally unable to PASS as pre-registered. This needs an author ruling, for example authorizing a validation-only LOW derivative.

## 7. Package

`gorrund_05V_neutral_arm.zip` contains:

- `GO-ARM-N1.blend` plus its linked `GO-05T_references.blend`;
- states `S12_E2.npz` and `N1R6.npz`;
- the OBJ export;
- the evidence folder;
- `MANIFEST.sha256`.

The zip was verified by CRC test, clean extraction and a manifest re-hash.

The package is delivered for author inspection only. It is **not** an accepted ARM.

## Status

Gorrund **UNACCEPTED**; RM-OT-05 **OPEN**; Stage C **BLOCKED (not started)**; Grask E3 frozen; no canon / race-spec / RMQ acceptance change; D4 / UE5 / production rigging / creator **NOT STARTED**.

**RM-OT-05V BLOCKED — REPLICATED NEUTRALIZED BLIND GATE FAILS: C5-REF 0/3 IN BOTH RUNS. The neutral body is read through muscularity, limb bulk and a bent-knee posture (rated "major" by 6/6 scorers), not through structure. R-6 knee extension and R-4 reference composition are also NOT MET.**

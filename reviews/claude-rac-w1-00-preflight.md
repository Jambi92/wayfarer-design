# RAC Wave 1 — W1-00 Preflight / Provenance Audit

**Author:** Claude (auditor) **Date:** October 5, 2026
**Order:** `reviews/chatgpt-reference-anatomy-wave1-execution-order.md` §3 W1-00
**Status:** COMPLETE. Nothing was measured before this audit was done.

## 1. Canonical status checks

| Item | State found | Result |
|---|---|---|
| `decisions/REFERENCE_ANATOMY_V1.md` | Present; companion authority at PROJECT_RULES level (RAC Phase 2, commits f514324 / 1e69f9f) | OK |
| RMQ `reviews/claude-pass2-r5-reference-mesh-queue.md` | Present; RM-UB-06/07/08, RM-CF-10 and RM-SR-04 with Durrim, as left by Phase 2 | OK |
| STATUS | "REFERENCE ANATOMY: BIOLOGICAL AUTHORSHIP CANONICALIZED / MEASUREMENT PHASE READY" | OK |
| W1-A1 (Cogling head dimension) | Canonicalized minimally before use: `specs/cogling/COGLING_V1.md` (head-size paragraph and status note) and RMQ RM-SR-04 now read "11–13 cm = anatomical head height, menton–vertex, hair excluded; no Head Height control". No number changed. | DONE |

## 2. Manifest verification

`reviews/claude-rac-wave1-execution-manifest.md` lists **15 bodies + 1 Marchfolk head variant** (rows 1–2, 4–16 bodies; row 3 head). Matches the order §1. Reference statures match each spec (MF 173, SK 208, SG 178, FN 181, AE 190, VA 178, HV 178, DU 137, GR 218, GO 229, PK 107, CG 91, SA 188 tail excluded).

## 3. Asset inventory

Sources searched: the repository; the connected PC folders `E:/UnrealProjects/Wayfarer 5.8/RaceBodies` (incl. `out/`) and `E:/Wayfarer-Rodin/Source-Masters` (read-only).

| # | Candidate | Asset found | Category |
|---|---|---|---|
| 15 | Saurin male centre (aff1b52) | `RaceBodies/out/saurin_final_base.npz` | **Accessible measurable geometry** |
| 16 | Saurin female centre | No saved mesh; **deterministically derivable** from #15 with the committed §263 tools (`tools/rodin/v5/tissue.py`, `fsets3.CEN`) | **Accessible measurable geometry (derived)** |
| 1 | Marchfolk configuration 1 | `RaceBodies/out/Marchfolk_Masc.blend` / `.fbx` | **Accessible but noncompliant** (see ARM record) |
| 2 | Marchfolk configuration 2 | `RaceBodies/out/Marchfolk_Fem.blend` / `.fbx` | **Accessible but noncompliant** (fails R-2) |
| 3 | MF-FACE-PROJ-MAX | none | **Purpose-built required** |
| 4–14 | SK, SG, FN, AE, VA, HV, DU, GR, GO, PK, CG | none usable. Iteration 3 non-Marchfolk references excluded (AD-R46); Vael Rodin GLBs are 2D-sheet relief reconstructions (excluded by the order §3 W1-03) | **Purpose-built required** |

No "referenced but inaccessible" item: every referenced asset was reachable.

## 4. Provenance records

| Candidate | File | SHA-256 | Origin | Builder-chosen inputs |
|---|---|---|---|---|
| SA-M (#15) | `saurin_final_base.npz` (keys v, f; cm; x right, f forward, u up; feet at u=0) | `a925e067370be91b84a800c25268e3d472f93e190c29673a2ac3d64ec89b8c9c` | Saurin closure reference aff1b52, frozen; identical to the working build copy (max vertex difference 7.6e-6 cm, faces equal) | Values fixed by the Saurin closure (author-accepted at that closure); no new W1 value |
| SA-F (#16) | derived in memory from SA-M | (derived; parameters recorded: trunk 1.07, pelvis 1.055, head 1.0133, tail 1.0133, flank E 2.0 cm, ventral B 1.6 cm) | §263 female-centre column | None new; all §263 canon |
| MF-M (#1) | `Marchfolk_Masc.blend` | `d1dea7b6bbc70c534ccbc2d880fb800e247a8ab95719d369ad21c8d841e350d5` (`.fbx` `24d71278…7b5`) | MPFB/MakeHuman default male, Iteration 3 (`wf_build_races.py`) | **All** shape inputs are builder-chosen: ethnic mix 0.33/0.331/0.33, age macro "young", muscle 0.5, weight 0.5, proportions default, height macro, A-pose |
| MF-F (#2) | `Marchfolk_Fem.blend` | `4592b7252862321059fc159b0ab0f953f87a4495b62819cbd0bd222930632663` (`.fbx` `c1cca5b9…2aa`) | MPFB default female 159.05 cm, **uniformly scaled ×1.0877** to 173 cm | As MF-M plus the scale factor |
| #3–#14 | none | — | Build packets in `reviews/rac-w1-packets/` | to be listed by the builder |

— Claude

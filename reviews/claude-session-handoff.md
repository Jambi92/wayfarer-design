# Claude session handoff — Wayfarer RM-OT-05 (Gorrund)

Purpose: if a conversation runs out of room, a new Claude conversation reads this file first and continues.

## LATEST (2026-10-30) — HALVREN EAR FAMILY FINAL PRODUCTION GATE — FINAL PRODUCTION FREEZE RECOMMENDED — awaiting ChatGPT review

**What was done**
- Order: `reviews/chatgpt-rac-rp3-halvren-ear-final-production-triangulation-gate-order.md` (a656750). Report: `reviews/claude-rac-rp3-halvren-ear-production-gate-report.md`. Evidence: `reviews/rac-rp3-evidence/halvren_rp3_ear_production_gate/`. Nothing frozen; no mesh edit.
- Tools (`halvren_rp3_v001`): `hv_ear_prodtri.py` (bpy: TRI-HV1 bake + flagged-quad table, normals / MikkTSpace, poses on triangles, LOD-HV1, FBX round trip, importer re-triangulation, mirroring), `hv_ear_prodtri_boards.py PT SNAP OUT` (`PT_ONLY=<tag prefix>` re-renders a subset), `hv_ear_prodtri_collect.py`. `render_attr.py` opt-in `RENDER_LIGHTING` / `RENDER_SPEC`.
- Workspace `/tmp/claude-0/rt/hv/ear/{prodsnap (snapshot + ref + pose), prodtri (per-mesh outputs, jobs.txt, rerun2.sh), lodlobe}`.

**Key findings**
- The quad audit ignores crossings between triangles of vertex-adjacent quads; on baked triangles the twisted cuff quads cross (HE2 c1: 5 at rest with the a-c split). TRI-HV1 step 5 removes them (5 flips in total). Exporting quads would let the importer re-triangulate 10-242 flagged quads, so export baked triangles.
- Unconstrained 25 % decimation crosses back sheet / cuff (also on frozen Vael); LOD-HV1 protects the root band and weights the lobe zone (round-1 lobe pinch).

**Next:** STOP for ChatGPT review (final production freeze decision).

## (previous) 2026-10-29 — HALVREN EAR FAMILY CLOSURE — HALVREN EAR FAMILY FREEZE RECOMMENDED — awaiting ChatGPT review

**What was done**
- Order: `reviews/chatgpt-rac-rp3-halvren-ear-family-closure-after-hr2-order.md` (94eabf1). Report: `reviews/claude-rac-rp3-halvren-ear-family-closure-report.md`. Evidence: `reviews/rac-rp3-evidence/halvren_rp3_ear_family_closure/`. HE2 + HR2 frozen by record; HE1 / HE3 HVEAR4 recommended, not frozen.
- Library: `ear_branch_lib.py` HE1 / HE3 HVEAR4 (`sheet_fold_fix` geo flag), before-states `HE1-HVEAR3`, `HE3-HVEAR3`, `HE1-R3`, test body `HE1-HS`; `ear_build.py` probe keys `clear`, `helix_h`, `helix_w`.
- Halvren repair `hv_cuff_repair.py`: stage 3 symmetric sheet stretch (aspect > 9.8), stage 4 folded sheet quads, stage 5 cuff creases > 120 deg (corner / aspect / no-new-crossing / no-new-fold guards); 4 / 5 only with `sheet_fold_fix`.
- Tools: `hv_ear_family_closure.py EVIDIR` (record), `hv_ear_family_boards.py EVIDIR OUT` (boards A-F); prodcheck `hv_ear_prodcheck.py` with `/home/claude/stc/bin/python3` (bpy).
- Workspace `/tmp/claude-0/rt/hv/ear/{fam6 (final guarded HE1-3 c1/c2), hr2f (ee0e98c family incl. HE3-before / HE1-HVEAR3), he1L53, he1L56, he3c-e, he1s, he1t, he1u, he1v (trials), ref (frozen elves)}`.

**Key findings**
- HE3 0.88 came from HR2 removing the HR1 root-line residual vs Fenn; HVEAR4 recombination -> 0.64 / 0.61 / 0.27. HE1 floor was 4-20 cavum quads over aspect 10, fixed by stage 3 -> L 5.6 (+10-13 %); Path B scaffold worse. Visible crinkles = folded sheet quads (stage 4); HE1 c2 speck = creased cuff edge (stage 5). Blind reviews: FAIL, BORDERLINE, FAIL, PASS, PASS.
- Shared polish carry-forwards (also on frozen HE2): cuff band crumple / back-sheet Z-kink, stamped interior relief, lobe-base crease.

**Next:** STOP for ChatGPT review (family freeze decision).

## (previous) 2026-10-29 — HALVREN HE2 ROOT VISUAL INTEGRATION — APPROVED, READY FOR FREEZE REVIEW — awaiting ChatGPT review

**What was done**
- Order: `reviews/chatgpt-rac-rp3-halvren-ear-root-visual-integration-correction-order.md` (651d7f5). Report: `reviews/claude-rac-rp3-halvren-he2-root-visual-integration-report.md`. Evidence: `reviews/rac-rp3-evidence/halvren_rp3_he2_root_visual/`. Nothing frozen.
- Library: `ear_build.py` HR2 controls `root_lower` / `_cap` / `_cap_inf` / `_smooth` / `_ring` / `_fall` / `_fall_own`, `sulcus_h` / `sulcus_r`, `fair_rings` (inert unless set); `ear_branch_lib.HV_ROOT2` on HE1 / HE2 / HE3 (HE3 sulcus off); `HE*-HR1` = 29f2c16 root. `hv_cuff_repair.py` stage 2 (slivers at the cuff / rim seam, aspect > 10). `render_attr.py` optional `RENDER_REVEAL=1` cavity shading.
- Tools: `hv_root_sectors.py` (pedestal vs extrapolated head, loop crease, lower fork), `hv_root_xsec.py`, `hv_he2_rootvis.py EVIDIR` (record), `hv_he2_rootvis_boards.py EVIDIR OUT`; `hv_ear_quick.py` cams `aq` (= old etqr), `rq`, `rq2`, `rr`, `lr`, `side`.
- Workspace `/tmp/claude-0/rt/hv/ear/{hr2f (final guarded HE1-3 c1/c2), hr2 (trials), before29 (= he3 HR1)}`.

**Key findings**
- The flange / fork came from the v005 MPFB ear pedestal + a fixed-loop crease, not the auricle. HR2 seats the auricle on the head and fairs the loop. HE2 clean c1 + c2, R2 0.51 / 0.44 / 0.23. Polish items (lobe-base crease, Z-kink in the sheet) recorded; fair_rings 2 removes the crease but is not robust.

**Next:** STOP for ChatGPT review (HE2 freeze decision).

## (previous) 2026-10-29 — HALVREN HE2 CLOSURE — HE2 FREEZE APPROVED (recommendation) — awaiting ChatGPT review

**What was done**
- Order: `reviews/chatgpt-rac-rp3-halvren-he2-realization-ear-architecture-closure-order.md`. Report: `reviews/claude-rac-rp3-halvren-he2-closure-report.md`. Evidence: `reviews/rac-rp3-evidence/halvren_rp3_he2_closure/`. Nothing frozen.
- Library: `ear_branch_lib.py` HVEAR3 (HE1 / HE2 / HE3 calibrated; HR1 seat rule; `place_db` / `place_du` placement bias in `realize`); `ear_build.py` probe keys `taper_st`, `place_*`, `phi0`, `tauA`, `d_r`, `lift_*` (inert unless set; frozen ears dV 0).
- Halvren path: `hv_ear.sh WORK RI3 CAND HEAD` with `HV_REPAIR=1` -> `hv_run_head.sh` (guard + `hv_cuff_repair.py`, iterate until clean); calibration `hv_ear_try.py WORK NAME CAND HEAD k=v,...` (rest build + firewall vs `/tmp/claude-0/rt/hv/ear/src_dom.json`), `hv_ear_jac.py`; records `hv_he2_closure.py EVIDIR`, `hv_he2_drift.py`, `hv_ear_prodcheck.py` (bpy), boards `hv_he2_boards.py`.
- Workspace `/tmp/claude-0/rt/hv/ear/{he3 (final c1/c2), topo3, jac, des2-5, he3x_*}`.

**Key findings**
- HE2 now R2 0.36 / 0.38 / 0.32, clean c1 + c2, one auricle. HE3 flagged (R2 0.87 MF->AE; c2 yaw-right contact). HE1 floor bounded (+27 %). Cavum-level domain switched to a depth-weighted centroid (stable).

**Next:** STOP for ChatGPT review (HE2 freeze confirmation; HE3 / HE1 carry-forwards).

## (previous) 2026-10-29 — HALVREN CENTRAL ACCEPT (HB2 + HF2 + HP-B) + EAR ARCHITECTURE — HALVREN EAR TOPOLOGY NEEDS DEDICATED BRANCH

**What was done**
- Order: `reviews/chatgpt-rac-rp3-halvren-central-accept-ear-architecture-order.md`. Gate: `reviews/claude-rac-rp3-halvren-central-accept-ear-architecture-gate.md`. Evidence: `reviews/rac-rp3-evidence/halvren_rp3_central_accept_ear/` (`hpb_validation/`, `ear/`, `sheets/`). Proposal: `reviews/claude-rac-rp3-halvren-ear-topology-branch-proposal.md`. Nothing frozen.
- Sources: `hv_defs.py` PELVIS HP-B, tag suffix `-HPB`; `build_hb.sh HB2HF2-HPB` (also HB2HF1-HPB / HB2HF3-HPB diagnostic mosaic sources) -> reference-assets + manifest. Validation: `HV_WORK=/tmp/claude-0/rt/hv/hpe run_hveval.sh`, `hv_bf_technical.py hpe ...`, `hv_eval.py`, `hv_hpb_validation.py`.
- Ears: `ear_branch_lib.py` Halvren block (HVEAR2 HE1/HE2/HE3, HV-DFN/DAE/DVA/DHU, HVT-* stress bounds, HE*-R rigid / HE*-V Vael RI3 audit variants; `VA_RI3_SKIN`, `HV_SKIN` = HR1 root geometry; `halvren` taper law); `ear_build.py` probe keys taper_ex (4-tuple safe) / taper_sh; `ear_sheet` now receives the candidate geometry (frozen ears dV 0). Runner `hv_ear.sh WORK FN|RI3 CAND HEAD` (EAR_CF = /tmp/claude-0/rt/hv/hpe); queue helper `/tmp/claude-0/rt/hv/ear/queue.sh LIST`; `hv_ear_summary.py`, `hv_ear_domains.py`, `hv_ear_audit.py`, `hv_ear_collect.py EVIDIR`, `hv_ear_probes.sh`, `hv_ear_probe_eval.py`, `hv_ear_sheets.py EVIDIR/ear EVIDIR/sheets`, `hv_ear_quick.py`.
- Workspace `/tmp/claude-0/rt/hv/ear/{he,mos,ref,topo,x}` (he = HR1 realisations c1/c2 + probes; ref = frozen elf params on the Halvren head; topo = audit variants; x = rest-state exploration).

**Key findings**
- HP-B validated (69 / 69, no regression). HVEAR2 authored mosaic passes the design firewall but the shared topology realises every ear on one Marchfolk->elf line (Marchfolk params at median t 0.50-0.53); HE2 / HE3 measured R2 0.93; HE1 floor +25 % size; HR1 root clean on c1 only.

**Next:** STOP for ChatGPT review (authorize the dedicated Halvren ear branch; then re-realise HVEAR2 and select the central HE).

## (previous) 2026-10-29 — HALVREN CENTRAL MIXED BODY/FACE PASS (HB2 + HF2 recommended) — READY FOR PELVIS AUTHOR DECISION

**What was done**
- Order: `reviews/chatgpt-rac-rp3-halvren-body-face-source-order.md`. Gate: `reviews/claude-rac-rp3-halvren-body-face-source-gate.md`. Evidence: `reviews/rac-rp3-evidence/halvren_rp3_body_face_source/`. Nothing frozen; ears locked; pelvis held.
- Definition `tools/rac/rp/halvren_rp3_v001/hv_defs.py` (HVDEF1: BODY / FACE dicts, strengths STR / STRF; tag HBn / HBnHFm). Build `build_hb.sh TAG...` -> `/tmp/claude-0/rt/hv/hb/cand` (c1 HVC1-*, c2 HVF178-*). Eval `hv_eval.py OUT CFG ITEM:PREFIX...` (31 metrics, midpoint audit, face regions / descriptors). Propagation `run_hveval.sh ID...` -> `/tmp/claude-0/rt/hv/hbe`; `hv_bf_technical.py`; expression `fenn_rp3_v001/cf_expr.py`; pelvis package `build_hp.sh` + `hv_pelvis_pkg.py` -> `/tmp/claude-0/rt/hv/hp`; `run_hv_bf_prod.sh`, `hv_bf_manifest.py`, `hv_bf_sheets.py`.
- 16 candidate records added to `reviews/reference-assets` (CANDIDATE; manifest lists HVC1-HB2HF2 / HVF178-HB2HF2). E: `Halvren/RP3/HV_{M,F}_REF_RP3_bodyfam_v002.*` (HB2 + HF2 diagnostic) + candidate manifest + definitions; read-back identical.

**Key findings**
- HB2 + HF2 departs from Marchfolk across 7 / 9 body systems and 3 / 7 face regions; distinct from every frozen elf; all technical gates pass. Caveat: c2 limb / torso moves about a third toward Fenn coherently (single-α R² 0.70).
- Pelvis: HP-B (pelvis Y 1.02 + hip-horiz-decr 0.05) recommended; HP-A fallback.

**Next:** STOP for ChatGPT review (accept the pair, choose the pelvis direction; then ear architecture can be ordered).

## (previous) 2026-10-29 — HALVREN CENTRAL ANCHOR — BODY + CRANIOFACIAL SOURCE WORK REQUIRED, PELVIS NEEDS AUTHOR DESIGN PASS

**What was done**
- Order: `reviews/chatgpt-rac-rp3-halvren-central-anchor-order.md`. Gate: `reviews/claude-rac-rp3-halvren-central-anchor-gate.md`. Evidence: `reviews/rac-rp3-evidence/halvren_rp3_central_anchor/`. Nothing frozen; ears not built.
- Tools `tools/rac/rp/halvren_rp3_v001/`: `build_hv_partA.sh` (HVF178 + 178 cm Vael / Skarn comparators; MF / SG / FN / AE copied from Vael Part A), `skp_hv.sh`, `hv_partA.py` (six-source metrics, midpoint audit, pelvis report), `hv_hidden_ear.py`, `run_hv_prod.sh` + `hv_manifest.py`, `hv_sheets.py`. Part B ran `aelari_rp3_v001/run_aeeval.sh` with `AE_WORK=/tmp/claude-0/rt/hv AE_C1=HVC1 AE_C2=HVF178`.
- Workspace `/tmp/claude-0/rt/hv` (`partA/{ref,build,build2,cmp,skp,regen}`, `src`, `fam`, `val`, `def`, `ov`, `prod`, `sheet_r`).
- `HVF178` added to `reviews/reference-assets` (r6 / build / meas; manifest CANDIDATE). E: `Halvren/RP3/` (bodyfam blends, maps, sidecars, manifest); read-back identical.

**Key findings**
- Technical gates pass (69 / 69 both; exact v005; 0 new contact class).
- The central body is Marchfolk with slightly longer forearm / lower leg / fingers; face = Marchfolk; pelvis = Marchfolk. Not an average, not a patchwork.

**Next:** STOP for ChatGPT review (author decisions in the gate §8).

## (previous) 2026-10-29 — VAEL RP3 — AUTHOR ACCEPTED / FROZEN (by record)

**What was done**
- Order: `reviews/chatgpt-rac-rp3-vael-final-author-acceptance-freeze-closure-order.md`. No geometry work: verification-only re-stage of the E: copies (byte-identical, `va_freeze_verify.py` re-read-back identical to the recorded read-back, 69 / 69 both), then `va_freeze_promote.py` promoted `VAEL_RP3_FREEZE_CANDIDATE.json` → `VAEL_RP3_FREEZE.json` (status / carry-forward edits only).
- Registered `VAEL-CF-EARROOT-1`; `VAEL-CF-SHOULDER-1` carried. Updated manifest, `VAEL_V1.md`, STATUS, register, final report.

**State**
- Fenn, Aelari and Vael are all frozen: three distinct elven population references.
- Halvren is next and NOT started. Its mixed ancestry must not be a numeric or visual average of the three elves; shared engineering may be tested, but Halvren anatomy needs its own author gate.

**Next:** STOP for ChatGPT review.

## (previous) 2026-10-28 — VAEL FINAL CONSOLIDATION — NEEDS AUTHOR DECISION (one c1 neck_rot45 cuff fold) — NOT FROZEN

**What was done**
- Order: `reviews/chatgpt-rac-rp3-vael-final-consolidation-freeze-order.md`. Report: `reviews/claude-rac-rp3-vael-final-freeze-report.md`. Evidence: `reviews/rac-rp3-evidence/vael_rp3_final/`.
- Drivers in `tools/rac/rp/vael_rp3_v001/`: `run_vafinal.sh` (rebuild A + RI3 B) → `run_vafinal_eval.sh` → `run_vafinal_prod.sh` → `va_unmasked_localise.py` → `va_final_gates.py WORK WORK` → `va_final_sheets.py WORK WORK/sheets` → PC copy → `va_freeze_verify.py` (validator from read-back; `freeze_check.py` gained optional `RB_DUMP`) → `va_freeze_record.py` → `va_final_collect.sh`. Work folder `/tmp/claude-0/rt/va/final`.
- E: `Vael/RP3/VA_{M,F}_REF_RP3_v001.{blend,json}`, `_landmarks.json`, `_branch_map.npz`; read back byte-identical.

**Key findings**
- All gates pass and match the reviewed VF2 / RI3, except c1 `neck_rot45`: 1 new fold on two sub-mm left cuff quads (no flip / contact). Ear bound rigidly to head (diagnostic) removes it. Proposed `VAEL-CF-EARROOT-1` (rig stage).
- On acceptance: copy `VAEL_RP3_FREEZE_CANDIDATE.json` → `VAEL_RP3_FREEZE.json` (status line only), then update manifest, `VAEL_V1.md`, register (CF-SHOULDER-1 carried + new id), STATUS.
- Halvren next (not started): Fenn / Aelari / Vael are separate elf references; Halvren is not a simple average and needs its own biological gate; shared ear engineering may inform it.

**Next:** STOP for ChatGPT review.

## (previous) 2026-10-28 — VAEL EAR ROOT INTEGRATION — PASS — RI3 READY FOR FINAL CONSOLIDATION

**What was done**
- Order: `reviews/chatgpt-rac-rp3-vael-ear-root-integration-order.md`. Gate: `reviews/claude-rac-rp3-vael-ear-root-integration-gate.md`. Evidence: `reviews/rac-rp3-evidence/vael_rp3_ear_root_integration/`. Plan updated.
- `ear_branch_lib.CAND` VA-E2-RI1 / RI2 / RI3 (geo clear −0.30; RI2 / RI3 + `cuff_skin_*`, `presmooth` 0); `cuff_build3` reads ring sizes from a read-only canon; `ear_build.py` skin-hugging cuff (data-pulled biharmonic) + candidate presmooth. Frozen Fenn / Aelari and the VA-E2 prototype rebuild dV 0.
- RI3 cuff canon `VAEL_EAR_CUFF_CANON_v001` (six rings, written on c1). Driver `run_va_ri.sh` -> `/tmp/claude-0/rt/va/ri_final/RI{1,2,3}`; records `va_ri_summary.py`, `va_ri_export.py`; sheets `va_ri_sheets.py` (renders `/tmp/claude-0/rt/va/ri_sheet_r`).
- E: `Vael/RP3/ear_branch/root_integration/` (6 blends), read-back identical.

**Key findings**
- RI3 reads as one auricle and is technically clean; RI1 / RI2 leave slivers. c1 stand-off marginally above Fenn (reported).

**Next:** STOP for ChatGPT review (accept RI3 / authorise final consolidation).

## (previous) 2026-10-28 — VAEL EAR PROTOTYPES — PASS — VA-E2 RECOMMENDED

**What was done**
- Order: `reviews/chatgpt-rac-rp3-vael-ear-prototype-order.md`. Gate: `reviews/claude-rac-rp3-vael-ear-prototype-gate.md`. Evidence: `reviews/rac-rp3-evidence/vael_rp3_ear_prototype/`. Plan: `reviews/claude-rac-rp3-vael-final-consolidation-plan.md`.
- `ear_branch_lib.CAND` gained VA-E1 / E2 / E3 (`W1V`, incl. `geo` clear 0.15); `ear_build.py` applies a candidate `geo` override (inert for Fenn / Aelari; frozen ears rebuild dV 0).
- Driver `tools/rac/rp/vael_rp3_v001/run_va_ear.sh` (EAR_UNT_MODE=contacts) -> `/tmp/claude-0/rt/va/ear`; records `va_ear_summary.py`, `va_ear_export.py`; sheets `va_ear_sheets.py` (renders `/tmp/claude-0/rt/va/sheet_r`).
- VAEL-CF-SHOULDER-1 added to the rig carry-forward register. E: `Vael/RP3/ear_branch/` (6 prototype blends), read-back identical.

**Key findings**
- All technical gates pass on all candidates; VA-E2 recommended. Disclosed: tip stand-off > Fenn (by projection angle Fenn still greatest); VA-E2 measured length shorter than the proposal estimate.

**Next:** STOP for ChatGPT review (ear selection / bounded refinement / final consolidation).

## (previous) 2026-10-28 — VAEL ELF-FRAME — HUMAN FIREWALL PASS — VF2 RECOMMENDED — EAR PROTOTYPING UNLOCKED

**What was done**
- Order: `reviews/chatgpt-rac-rp3-vael-elf-frame-human-firewall-order.md`. Gate: `reviews/claude-rac-rp3-vael-elf-frame-human-firewall-gate.md`. Evidence: `reviews/rac-rp3-evidence/vael_rp3_elf_frame/`. Ear proposal (no geometry): `reviews/claude-rac-rp3-vael-ear-branch-proposal.md`.
- VEF1 added to `tools/rac/w1/vael_body_field.py` (A clavicle span via bone scale in `arm_lib.build`, A2 axilla, B shaft); activated by `cfg["vael_field"]["vef_magnitude"]` (inert otherwise).
- VF1 / VF2 / VF3 built on VD2 (`tools/rac/rp/vael_rp3_v001/build_vf.sh`); eval `vf_eval.py`, `vf_comp.py`, `vf_ear_root.py`, sheets `vf_sheets.py`; manifest `va_manifest.py` (v004).
- VF2 propagated: `VAL4-R1-VD2-VF2` / `VALF178-R1-VD2-VF2` (CANDIDATE) -> `VA_{M,F}_REF_RP3_bodyfam_v004` (E: `Vael/RP3/`, read-back identical).
- Workspace `/tmp/claude-0/rt/vf/` (cand, cand2, skp, lean, comp, prod, chain.sh).

**Key findings**
- Human and three-elf firewalls pass; pelvis 9 / 9; VC2 unchanged; composition-invariant.
- Disclosed: c1 shoulder_flex90 +6 vs MF (rig / LBS from the clavicle scale).

**Next:** STOP for ChatGPT review (ear order VA-E1 / E2 / E3).

## (previous) 2026-10-28 — VAEL CUSTOM BODY DEFORMATION — BODY NEEDS LOCAL REVISION

**What was done**
- Order: `reviews/chatgpt-rac-rp3-vael-custom-body-deformation-order.md`. Gate: `reviews/claude-rac-rp3-vael-custom-body-deformation-gate.md`. Evidence: `reviews/rac-rp3-evidence/vael_rp3_custom_deformation/`.
- New deterministic field `tools/rac/w1/vael_body_field.py` (VDF1.2: rib side wall, lumbar continuity, ASIS, clavicle, palm root, heel); `arm_lib.build` applies it when `cfg["vael_field"]` = {spec, magnitude} (inert otherwise; regen reproduces it).
- VD1 / VD2 / VD3 built on R1 (`tools/rac/rp/vael_rp3_v001/build_vd.sh`; overrides `/tmp/claude-0/rt/vd/ov_VD*.json`); eval `vd_eval.py`, `vd_selfx.py`, `va2_eval.py` (composite central row retired), sheets `vd_sheets.py`.
- VD2 propagated: `VAL4-R1-VD2` / `VALF178-R1-VD2` (reference-assets CANDIDATE) -> `VA_{M,F}_REF_RP3_bodyfam_v003` (E: `Vael/RP3/`, read-back identical).
- Workspace `/tmp/claude-0/rt/vd/` (cand, cand2, skp, lean, prod, sheet_r, chain.sh).

**Key findings**
- All technical / canon / pelvis / VC2 gates pass; five systems move measurably at close range.
- Full-body human firewall still fails: frontal elf signal is shoulder span + limb envelope (outside the authorised systems).

**Next:** STOP for ChatGPT review (author decision a / b / c, gate §9).

## (previous) 2026-10-28 — VAEL BODY / FACE SOURCE — BODY NEEDS REVISION / FACE PASS

**What was done**
- Order executed: `reviews/chatgpt-rac-rp3-vael-body-face-source-order.md`. Gate: `reviews/claude-rac-rp3-vael-body-face-source-gate.md`. Evidence: `reviews/rac-rp3-evidence/vael_rp3_source/`.
- **Probe matrix:** 16 body + 26 face probes on VAL4, height held.
- **Body correction VB1 / VB2 / VB3** (one architecture):
  - pelvis bone scale [1.02, 1.045, 1.03];
  - thigh / calf Y × 0.9975;
  - torso-depth / neck-horiz / foot-depth at three magnitudes.
- **Face VC1 / VC2 / VC3:** same keys at 0.6 / 1.0 / 1.4×. Iteration 3 is final; its brow term is `eyebrows-trans-backward` 0.015.
- **Selected R1:** VB2g + VC2, rebuilt as `VAL4-R1` / `VALF178-R1` (reference-assets, CANDIDATE).
- **Family:** `VA_{M,F}_REF_RP3_bodyfam_v002` on v005; all technical gates pass. Delivered to E: `Vael/RP3/` with identical read-back.
- **Workspaces:**
  - `/tmp/claude-0/rt/va2/`: `probe`, `vb`, `vc`, `vc2` (cand, r1, skp, lean);
  - `/tmp/claude-0/rt/va2/prod/`: `src`, `fam`, `audit`, `val`, `def`, `contact`, `lm`, `prod`, `readback`, `ov`, `sheet_r`; `partA` symlinks to `../../va/partA`.
- **Tools:** `tools/rac/rp/vael_rp3_v001/`:
  - `probe_va2.sh`, `va2_eval.py`, `va2_probe_matrix.py`, `build_vb.sh`, `build_va_r1.sh`, `skp_va2.sh`, `va2_pelvis.py`, `va2_sheets.py`;
  - `run_va_prod.sh` and `va_manifest.py`, run with env `VA_C1` / `VA_C2` / `VA_PROD_VER` / `VA_R1_*`.

**Key findings**
- **Numeric gates pass:** hip ordering (sub-1 %), VA-P6, pelvis 9 / 9, body 4 / 8, face 6 / 6.
- **Visual human firewall fails:** the body still reads as Marchfolk; the face departure is about 45 % of the Fenn / Aelari scale.
- **"Central vertical < Aelari"** cannot hold by partition identity.
- **Jaw-width descriptor** is contaminated by the neck target.

**Next:** STOP for ChatGPT review (author decisions A–E in gate §8).

## (previous) 2026-10-28 — VAEL c2 + HIDDEN-EAR GATES — BODY/CRANIOFACIAL SOURCE WORK REQUIRED

**What was done**
- Vael order executed (`reviews/chatgpt-rac-rp3-vael-body-face-ear-order.md`). Gate: `reviews/claude-rac-rp3-vael-body-face-ear-gate.md`.
- **Result:** VAEL BODY SOURCE/BRANCH WORK REQUIRED, plus craniofacial source work required. Ears not started. Nothing frozen.
- **Workspace** `/tmp/claude-0/rt/va`:
  - `partA/`: `ref` VAL4, `build`/`build2` VALF178, `cmp` 178 cm comparators (MF, SG, FN = FNL4-CF2 / FNF181-CF2, AE = AEL1-R1 / AELF190-R1), `skp`, `regen`, `diag` (Vael @190, original Aelari @178);
  - `src`, `fam`, `audit`, `anat`, `val`, `def`, `contact`, `lm`, `prod`, `readback`, `ov`;
  - `VA_hidden_ear_identity.json`, `sheet_r`.
- **Tools:** `tools/rac/rp/vael_rp3_v001/` (`build_va_partA.sh`, `skp_va.sh`, `va_partA.py`, `build_va_diag.sh`, `run_va_prod.sh`, `va_manifest.py`, `va_hidden_ear.py`, `va_sheets.py`). Part B used `aelari_rp3_v001/run_aeeval.sh` with `AE_WORK=/tmp/claude-0/rt/va AE_C1=VAL4 AE_C2=VALF178`.
- **E:** `Vael/RP3/VA_{M,F}_REF_RP3_bodyfam_v001.*`, the manifest and the VALF178 sidecar. Read-back is in evidence `pc_readback_sha256.txt`.

**Key findings**
- **Ordering:** the Aelari R1 correction leaves only a 0.21 / 0.34 % MF–Aelari hip-height window at 178 cm, and Vael now sits above Aelari (VA-P2a). c2 waist is also inverted (VA-P6).
- **Face:** the Vael face equals the Marchfolk face; a Vael CF pass is needed.

**Next:** STOP for ChatGPT review (author decisions in the gate, §9 item 16).

## (previous) 2026-10-28 — AELARI RP3 FINAL — FROZEN — awaiting ChatGPT review

**What was done**
- Final consolidation order executed (`reviews/chatgpt-rac-rp3-aelari-final-consolidation-freeze-order.md`). Report: `reviews/claude-rac-rp3-aelari-final-freeze-report.md`.
- **Result:** AELARI RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN (by record `AELARI_RP3_FREEZE.json`).
- **Workspace** `/tmp/claude-0/rt/ae/final`: the clean rebuild (`src`, `fam`, `full`, `lean`, `skp`, `ear/`, `prod`, `readback_local`, `pcrb`), the eval outputs and `sheet_r`.
- **Tools** (`tools/rac/rp/aelari_rp3_v001/`):
  - `run_aefinal.sh` (env `AE_FINAL`), `run_aefinal_prod.sh`, `run_aefinal_eval.sh`;
  - `ae_final_gates.py`, `ae_final_sheets.py`, `ae_freeze_verify.py`, `ae_freeze_record.py`.
  - `fn_make_prod.py` gained env `RAC_COMPOSITION` (the default leaves Fenn unchanged).
- **E:** `Aelari/RP3/AE_{M,F}_REF_RP3_v001.blend` + `.json` / `_landmarks.json` / `_branch_map.npz`. Read-back is in evidence `production/pc_readback_sha256.txt`.

**Next:** STOP for ChatGPT review.
- Recommended next race: **Vael** (not started).
- Fenn and Aelari are separate frozen elven population references.
- Vael must not become "dark Aelari" or "subterranean Fenn".
- Shared engineering may be tested, but Vael body / head / ear biology needs its own gate.
- No universal elf topology has been declared.

## (previous) 2026-10-27 — AELARI BODY-SOURCE CORRECTION — awaiting ChatGPT review

**What was done**
- Order 0f6aba8 executed. Gate: `reviews/claude-rac-rp3-aelari-body-source-correction-gate.md`.
- **Result:** AELARI BODY SOURCE CORRECTION PASS — READY FOR FINAL CONSOLIDATION. Nothing frozen.
- **Sources:** AEL1-R1 / AELF190-R1 in `reviews/reference-assets` (manifest CANDIDATE); the originals are untouched.
- **Workspace:**
  - `/tmp/claude-0/rt/ae/corr`: probes, `cand`, `skp`, `*_matrix.json`, overrides `c1_R1.json` / `c2_R1.json`;
  - `/tmp/claude-0/rt/ae/r1`: the full Standard v1 run, with a `partA/` symlink layout pointing at R1, plus `ov`, `ear/` (AE-E2 on R1 heads), `prod`, `readback` and `sheet_r`.
- **Tools** (`tools/rac/rp/aelari_rp3_v001/`; all defaults reproduce fd71f15):
  - `probe_corr.sh`, `build_corr.sh`, `corr_matrix.py`;
  - `run_ae_r1_prod.sh` (env `AE_EVI`);
  - `ae_ear_regress.py`, `ae_corr_sheets.py`;
  - env switches: `run_aeeval.sh` `AE_C1` / `AE_C2`; `ae_manifest.py` `AE_C1` / `AE_C2` / `AE_PROD_VER`; `ae_partA.py` `AE_ORDER`; `ae_hidden_ear.py` `AE_HE_C1` / `AE_HE_C2`; `run_ae_ear.sh` `AE_H1` / `AE_H2` / `AE_CF` / `AE_EAR_CANDS` / `AE_EAR_VER` / `SKIP_PROBES`.
- **E:** `Aelari/RP3/`:
  - `AE_{M,F}_REF_RP3_bodyfam_v002.*`, `..._manifest_v002.json`, `AELF190-R1` sidecar;
  - `ear_branch/AE_{M,F}_REF_RP3_earE2_proto_v002.*`.
  - Read-back is in evidence `pc_readback_sha256.txt`.

**Next:** STOP for ChatGPT review → final Aelari consolidation / freeze (AE-E2, R1 sources).

## (previous) 2026-10-27 — AELARI c2 + HIDDEN-EAR + EAR PROTOTYPE — awaiting ChatGPT review

**What was done**
- Order fd71f15 executed. Gate: `reviews/claude-rac-rp3-aelari-body-face-ear-gate.md`.
- **Result:** AELARI BODY/FACE PASS + EAR BRANCH READY FOR AUTHOR SELECTION. Nothing frozen.
- **Workspace** `/tmp/claude-0/rt/ae`:
  - `partA/`: builds, comparators at 190 cm, `skp`, `AELF190_reference_validation.json`;
  - `src`, `fam`, `audit`, `anat`, `val`, `def`, `contact`, `prod`, `readback`, `ov`;
  - `AE_hidden_ear_identity.json`;
  - `ear/`: AE-E1..E3 × AEL1 / AELF190 + probes; `eartest_*` holds the reuse variants.
- **Tools** (`tools/rac/rp/aelari_rp3_v001/`):
  - `build_ae_partA.sh`, `skp_ae.sh`, `ae_partA.py`;
  - `run_aeeval.sh`, `ae_manifest.py`, `ae_hidden_ear.py`;
  - `run_ae_ear.sh`, `ae_ear_summary.py`;
  - `ae_sheets.py` (env `AE_SHEET_TMP`).
- **Fenn ear tool switches** (defaults keep Fenn unchanged):
  - `ear_branch_lib` `W1A` / `AE-E1..3` and `EAR_LAYOUT_METRIC`;
  - `run_ear_v002_head.sh` `EAR_CAND`;
  - `ear_sections.py` `EAR_HEADS` / `EAR_RACE`;
  - `ear_blend.py` `EAR_BLEND_STATUS`.
- **AELF190** is in `reviews/reference-assets` (r6 / build / meas; manifest CANDIDATE).
- **E:** `Aelari/RP3/` (bodyfam blends, maps, sidecars, manifest, AELF190 sidecar) and `Aelari/RP3/ear_branch/` (6 proto blends). Read-back in evidence `pc_readback_sha256.txt`.

**Next:** STOP for ChatGPT review: accept AELF190, rule on the AEL1 ties (ribcage vertical, shin share), select the Aelari ear (AE-E2 recommended), then Aelari consolidation.

## (previous) 2026-10-27 — FENN RP3 FINAL CONSOLIDATION — FROZEN — awaiting ChatGPT review

**What was done**
- Order 6d2eadc executed. Report: `reviews/claude-rac-rp3-fenn-final-freeze-report.md`.
- **Result:** FENN RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN (by record).
- **Tools** (`tools/rac/rp/fenn_rp3_v001/`):
  - `run_fnfinal.sh`: clean rebuild — regen CF2 → native → propagate → ear v002 (env `FN_FINAL`, default `/tmp/claude-0/rt/fn/final`).
  - `run_fnfinal_eval.sh`: audit / face / anatomy / validator / 18-pose deform on the final and family realizations, identity, hidden ear, cf_eval.
  - `fn_make_prod.py` (production blend + sidecars) and `fn_final_anatomy.py` (ear-excluded T gates).
  - `fn_final_gates.py`, `fn_final_sheets.py` (env `FN_SHEET_TMP`), `fn_freeze_verify.py` (PC read-back), `fn_freeze_record.py`.
  - The ear tools take env `EAR_CF` (CF2 workspace).
- **E:** `Fenn/RP3/FN_{M,F}_REF_RP3_v001.blend` + `_branch_map.npz` / `.json` / `_landmarks.json` + `FENN_RP3_FREEZE.json`; read-back in evidence `production/pc_readback_sha256.txt`.
- **Note:** `anatomy.py` unmasked reports T-1 / T-2 / T-7 FAIL on the production body only because the R-6 source carries the human auricle. `fn_final_anatomy.py` excludes the ear; both are recorded.

**Next:** STOP for ChatGPT review. Recommended next race: Aelari. Not started; it must not inherit Fenn geometry.

## (previous) 2026-10-27 — FENN EAR v002 REFINEMENT (E2) — awaiting ChatGPT review

**What was done**
- Order 0d9c70b executed. Gate: `reviews/claude-rac-rp3-fenn-ear-v002-refinement-gate.md`.
- **Result:** FENN EAR v002 PASS WITH DOCUMENTED T-4 RESIDUAL — AUTHOR DECISION. Nothing frozen.
- **Tools** (`tools/rac/rp/fenn_rp3_v001/`):
  - `ear_layout3.py` (tapered-leaf layout + sheet quality);
  - `ear_quality3d.py` (3-D cuff corner-angle pass);
  - `ear_zones.py`, `ear_export_v002.py`, `ear_compare_v002.py`, `ear_sheets_v002.py`;
  - `run_ear_v002_head.sh` (deformation guard loop), `run_earbranch_v002.sh` (env `EAR_WORK`).
  - v002 is the library default (`EAR_TOPO`, default v002; v001 is still selectable).
  - `ear_build.py` Q3 defaults are the final R3 values (th_cap 64).
- **Workspace:**
  - `/tmp/claude-0/rt/fn/ear/v002_r3` is the final run;
  - `v002` is R2, `v002_r1` is R1, `final2` is v001;
  - it needs `/tmp/claude-0/rt/fn/cf`.
- **Regenerating the evidence:**
  1. `ear_export_v002.py W EV`
  2. `EAR_ORDER=0d9c70b EAR_CANDS=E2 ear_summaries.py W EV`
  3. `ear_compare_v002.py final2 W EV`
  4. `ear_sheets_v002.py final2 W OUT` (EAR_SHEET_THREADS 2 — six Blender processes ran out of memory)
- **E:** `Fenn/RP3/ear_branch_v002/` (2 blends, sidecars, v005 → v002 map); readback in evidence `production/pc_readback_sha256.txt`.

**Next:** STOP for ChatGPT review: accept the residual, then execute the final consolidation package.

## (previous) 2026-10-27 — FENN CF2 ACCEPTED + EAR BRANCH (E1/E2/E3) — awaiting ChatGPT review

**What was done**
- Order bdcd6a6 executed. Gate: `reviews/claude-rac-rp3-fenn-ear-branch-gate.md`.
- **Result:** FENN EAR BRANCH PASS — E2 RECOMMENDED. A bounded topology refinement is recommended before the freeze. Nothing frozen.
- **CF2 records:**
  - manifest entries FNL4-CF2 / FNF181-CF2, with `r6/` + `builds/` copies;
  - FENN-CF-1 in the carry-forward register;
  - FENN_V1 RP3 status block.
- **Tools** (`tools/rac/rp/fenn_rp3_v001/`):
  - `ear_branch_lib.py` (layout2, cuff_build3 with DP valence guards, realize);
  - `ear_build.py`, `ear_audit.py`, `ear_measure.py`, `ear_deform.py`, `ear_blend.py`;
  - `ear_sheets.py`, `ear_sections.py`, `ear_export.py`, `ear_summaries.py`;
  - `run_earbranch.sh` (env `EAR_WORK`, default `/tmp/claude-0/rt/fn/ear/final`).
  - bpy python is `/home/claude/stc/bin/python3`.
- **Workspace:**
  - `/tmp/claude-0/rt/fn/ear/final2` is the final run, with the guarded canon `canon_branch_topology.json`;
  - `final/` is the earlier pre-guard run;
  - it needs the CF2 run in `/tmp/claude-0/rt/fn/cf` (`fam/`, `src/`, `lm/`).
- **Topology:** TOPO2 n_a 28, u1 16, kb 12, j_f 3, K_r 4; J = 70; cuff 52 / 56 / 60 / 64 / 68. One valence-6 per side at ring 1 is forced by the v005 root pattern.
- **E:** `Fenn/RP3/ear_branch/` (6 blends + map + sheet-17 pair); readback in evidence `production/pc_readback_sha256.txt`.

**Refinement candidates, if ordered:** upper-extension kite → taper-following rows; cuff ±2 transition shear; attachment-corner cells; lobe-cusp knob.

**Next:** STOP for ChatGPT review (ear selection / refinement, then the consolidation plan in evidence).

## (previous) 2026-10-27 — FENN CRANIOFACIAL SOURCE (CF1/CF2/CF3)

**What was done**
- Order 2de0e28 executed. Gate: `reviews/claude-rac-rp3-fenn-craniofacial-source-gate.md`.
- **Result:** FENN CRANIOFACIAL PASS — CF2 RECOMMENDED. Nothing frozen.
- **Workspace** `/tmp/claude-0/rt/fn/cf`:
  - `probe/` (24 target probes), `cand/` (CF builds + `*_overrides.json`), `cand_v1/` (rejected head-diamond iteration);
  - `src/`, `fam/`, `audit/`, `anat/`, `lm/`, `val/`, `prod/`, `readback/`, `sheets/`, `ov/`;
  - `CF_hidden_ear_eval.json`, `CF_expression_sanity.json`.
  - Run with `build_cf.sh`, then `run_cfeval.sh`, then `cf_eval.py`, `cf_expr.py` (bpy) and `cf_sheets.py`.
- **Metrics:** `fn_face_metrics.py` uses fixed hm08 landmark vertices from the FNL4 template (replaces the parent gate's band descriptors).
- **Manifest:** FNF181 body accepted; FNL4 / FNF181 craniofacial provisional.
- **E:** `Fenn/RP3/craniofacial/`.
- **Ear-branch prep:** `ear_branch_prep/FENN_EAR_BRANCH_PREP.md` (52-vertex root loop; W1e FN-elven basis).

**Next:** STOP for ChatGPT review: CF selection, then the ear prototype order.

## (previous) 2026-10-27 — FENN BODY + HIDDEN-EAR GATE

**What was done**
- Order 57dc328 executed. Gate: `reviews/claude-rac-rp3-fenn-body-and-ear-branch-gate.md`.
- **Result:** FENN BODY NEEDS RACE-SPECIFIC BRANCH. The branch is craniofacial source authoring; hidden-ear facial identity is not met beyond the orbit. Part C was not started; nothing frozen.
- **Workspace** `/tmp/claude-0/rt/fn`:
  - `src/`, `cand/`, `audit/`, `anat/`, `val/`, `def/`, `prod/`, `readback/`, `sheets/`, `ov/` (ear-hidden npz);
  - `partA/`: `build/` (FNF181), `build2/` (second re-solve), `cmp/` (MFM / MFF / SGM / SGF 181 comparators), `ref/` (MF-M-R + FNL4 rest for the eye reference), `lean/` + `skp/` (skeletal proxy);
  - run with `run_fneval.sh`.
- **Tools** (`tools/rac/rp/fenn_rp3_v001/`): `fenn_partA.py`, `fenn_hidden_ear.py`, `fn_extra_sheets.py`, `fn_manifest.py WORK EVIDIR`, `run_fneval.sh`.
- **Measurement note:** `run_candidate.py` needs the common MF-M-R rest as the eye reference (`partA/ref/MF-M-R_rest.npz`). With the body's own rest the eye diameter degenerates.
- **FNF181 candidate:** `reviews/reference-assets/r6/FNF181_r6.npz` + `builds/FNF181_build.json` / `_meas.json`; manifest role CANDIDATE.
- **E:** `Fenn/RP3/` holds the body-family diagnostics + manifest + FNF181 sidecar (read-back sha equal).

**Ear basis for the later Part C:** W1e `tools/rac/w1/ear_families_v2.py` FN-elven (procedural evidence geometry; `attach_ears.py` composite).

**Next:** STOP for ChatGPT review: Fenn craniofacial source decision, FNF181 acceptance, then the ear branch.

## (previous) 2026-10-27 — SAGEKIN FROZEN + D6 ACCEPTED + SGF178 ACCEPTED

**What was done**
- Order d921903 executed. Report: `reviews/claude-rac-rp3-sagekin-family-freeze-report.md`.
- **Freeze record:** `SAGEKIN_RP3_FREEZE.json` (E: `Sagekin/RP3/`, evidence `reviews/rac-rp3-evidence/sagekin_rp3_freeze/`).
- **Read-back:** `tools/rac/rp/sagekin_rp3_v001/freeze_sg_verify.py WORK PCDIR OUT` (PC copies staged to `/mnt/user-data/uploads/RaceBodies/production/Sagekin/RP3`). ALL CHECKS PASS.
- **D6 accepted:** authoritative validator `validator_v2.py CAND OUT --scale-ref 173.143 --d5 --d6-native src/<ID>_native.npz`.
  - Regression: `d6_regression.py OUTDIR CID=CAND=NATIVE=LOOPS ...`.
  - 6 realizations, 0 false positives, 69 / 69 everywhere.
- **SGF178 accepted:** in `reviews/reference-assets/manifest.json` and `specs/sagekin/SAGEKIN_V1.md`.
- **Standard v1:** updated with D6. **Register:** Sagekin section (no new ID).
- **Workspace:** still `/tmp/claude-0/rt/sg` (`d6final/`, `freeze/`).

**Frozen MPFB-family realizations on v005:** Marchfolk v005, Skarn v003, Sagekin v001.

**Next:** STOP for ChatGPT review. Fenn is recommended next.
- Source `FNL4`, 181.16 cm, one configuration built.
- Likely ear-density / identity branch.
- Hidden-ear validation gate (`FENN_V1` §13).

## (previous) 2026-10-27 — SAGEKIN CONFIG-2 REFERENCE + FAMILY PROPAGATION

**What was done**
- Order c6c7940 executed. Gate: `reviews/claude-rac-rp3-sagekin-config2-reference-and-propagation-gate.md`.
  - Part A PASS (SGF178).
  - Part B NEEDS AUTHOR DECISION on proposed validator rule D6.
  - Nothing frozen; no topology change.
- **Workspace** `/tmp/claude-0/rt/sg`:
  - `src/` (regen + native), `cand/*_fam.npz`, `audit/`, `anat/`, `lm/`, `val/`, `def/`, `prod/`, `readback/`;
  - `partA/` (`resolve/` full SGF178 re-solve; `cmp/` MFF178 / MFM178 diagnostic comparators);
  - `hipdiag/`, `d6/`, `sheets/`;
  - run with `run_sgeval.sh`.
- **Tools** (`tools/rac/rp/sagekin_rp3_v001/`):
  - `partA_reference.py`, `hip_diag.py`, `contact_prop.py`, `sg_identity.py`, `sg_extra_sheets.py`, `sg_manifest.py WORK EVIDIR`.
  - Standard sheets: `FAM_VAL=_D4_D5 family_sheets.py WORK Sagekin SG:SG SGF178:SGF178`.
- **Proposed D6:** `val2lib.evaluate(d6=(W, bones))` / `validator_v2.py --d6-native NATIVE.npz`. Off by default; the authoritative output is unchanged.
- **Production candidates:** E: `Sagekin/RP3/SG_{M,F}_REF_RP3_retopo_v001.*` plus the manifest and the SGF178 sidecar. PC read-back sha is equal. Staging copies are in `/mnt/user-data/outputs/sg_rp3`.

**Key finding**
- The hip +p band side lands on the forearm in the R-6 stance on every family realization (elbow −p lands on the trunk).
- The longer Sagekin forearm drops that forearm count to 4, so SG hip is 4 / 5.
- D6 → 69 / 69 on all six configurations.
- If D6 is rejected, a ring search found single-ring options (e.g. 424 | 1043) that make all six firm; this would need a new order.

**Next:** STOP for ChatGPT review: D6 ruling, SGF178 acceptance as the configuration-2 central reference, Sagekin freeze.

## (previous) 2026-10-27 — MPFB FAMILY BASE v005 FROZEN + SKARN FROZEN + STANDARD v1 ACCEPTED

**What was done**
- Order 78a109f executed. Freeze by record; no file was re-saved.
- **Freeze record:** `MPFB_FAMILY_BASE_v005_FREEZE.json` (E: Marchfolk/RP3 + Skarn/RP3, evidence `reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/`).
- **Reports:** `reviews/claude-rac-rp3-marchfolk-v005-active-family-base-freeze-report.md`, `reviews/claude-rac-rp3-skarn-family-freeze-report.md`.
- **Read-back:** `tools/rac/rp/mpfb_family/freeze_v5_verify.py WORK PCDIR OUT` (PC copies staged to `/mnt/user-data/uploads/RaceBodies/production`). All checks pass.
- **Standard:** promoted to AUTHOR-ACCEPTED TECHNICAL STANDARD v1 (15 sections).
- **Carry-forward register:** `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md` (MPFB-CF-1 / -2).

**Active family base for propagation**
- `MF_M_REF_RP3_retopo_v005.blend` + `MPFB_FAMILY_BASE_v005_hm08_map.npz` (`e690fbaf…`).
- Workspace `/tmp/claude-0/rt/v5` (cand / val / def).

**Next:** STOP for ChatGPT review. The recommended next race is Sagekin. Its configuration-2 central reference is not accepted yet (only SGF152 / 178 / 208 diagnostics), so the author must choose it.

## LATEST (2026-10-27) — MPFB FAMILY BASE FINAL TOE-2 WEB CORRECTION — awaiting ChatGPT review

**What was done**
- Order 33a2dfe executed. Gate: `reviews/claude-rac-rp3-mpfb-family-base-final-toe2-web-gate.md` (PASS WITH DOCUMENTED TOE2 EXCEPTION — AUTHOR DECISION; nothing frozen).
- **Workspace** `/tmp/claude-0/rt/v5`:
  - `v5core.npz` = final successor (TW2);
  - `work/tw0.npz` = v004 without the toe-2 ring; `work/tw1.npz`, `work/tw3_d0.35.npz`;
  - `cand/*_v005.npz`, `maps/`, `audit/`, `anat/`, `lm/`, `val/`, `def/`, `freeze/`, `sheets/`;
  - run with `run_v5eval.sh`.
- **Build:**
  - `RINGS_SPEC="hip_support:195:790,toe3_root:508:1264" v004_build.py tw0.npz --relocate-toe3`;
  - then `tw_build.py tw0.npz v5core.npz --sector 100 --opt` (dorsal racetrack around v003 loop 497, strips 497|1262 + 497|1119);
  - then `make_v5cand.py v5core.npz /tmp/claude-0/rt/v4/v4core.npz WORK`.
- **Validator:** `validator_v2.py --scale-ref 173.143 --d5` is authoritative (D5 accepted).
- **Production:** `/mnt/user-data/outputs/rp5/` and E: (MF v005, SK v003, NOT FROZEN).

**Key findings**
- Fold test (`def/MPFB_v005_flip_parentage.json`): most female toe-extension flips are parent-quad LBS folds. 3 / 2 remain topology-attributable.
- The rejected v004 ring's toe-extension flips were all parent folds.

**Next:** STOP for ChatGPT review (accept the exception → freeze v005 + Skarn + promote the standard; or TW3; or rig-class deferral).

## LATEST (2026-10-26) — MPFB FAMILY BASE v004 MARGIN HARDENING — awaiting ChatGPT review

**What was done**
- Order a18371c executed. Gate: `reviews/claude-rac-rp3-mpfb-family-base-v004-margin-hardening-gate.md` (NEEDS AUTHOR DECISION, D5; nothing frozen).
- **Workspace** `/tmp/claude-0/rt/v4`:
  - `v4core.npz` = the successor definition (Q, UV, M, row_class, ring_parents);
  - `cand/<ID>_v004.npz` for the four configurations;
  - `maps/`, `audit/`, `anat/`, `lm/`, `val/`, `def/`, `freeze/` (read-backs), `sheets/`;
  - `work/` holds the search JSONs and debug scripts.
  - Run with `run_v4eval.sh`; then `margin_table.py`, `v4_sheets.py`, `family_manifest_v4.py`.
- **Build:** `v004_build.py OUT --relocate-toe3`.
  - Heel rows: rule-selected, 8 vertices.
  - Rings: hip strip 195 | 790 (self-mirrored), toe2 strip 497 | 1262, toe3 strip 508 | 1264; frozen-v003 loop ids from `closed_loops`.
  - Minimal toe-3 crease-pole slides.
- **Validator:** now the library `val2lib.py` (D4 accepted; D5 proposed via `d5=True`); `validator_v2.py` is its CLI (regression-identical).
- **Production:** `/mnt/user-data/outputs/rp4/` and E: (MF v004, SK v002, NOT FROZEN).

**Key finding**
- Skarn `toe2_j1` is 1 / 2 because the web-side band "path" is a single edge of loop 1120. No closed strip crosses it, so no ring can fix it.
- D5 (endpoint offset > W ⇒ side undefined, digits only) changes only that station.
- Validator semantics: the facing test uses inward numeric normals in the analysis frame.

**Next:** STOP for ChatGPT review (accept / reject D5; the toe-ring local slivers and flips; freeze).

## LATEST (2026-10-26) — MARCHFOLK v003 FROZEN + SKARN FAMILY PROPAGATION — awaiting ChatGPT review

**What was done**
- Order 85b7c1c executed.
  - **Part A:** freeze-by-record (`MF_RP3_v003_FREEZE.json`), read-back via `tools/rac/rp/marchfolk_rp3_v001/freeze_check.py`.
  - **Part B:** Skarn propagation.
- **Workspace** `/tmp/claude-0/rt/sk`: `src/` (regen, native), `cand/*_fam.npz`, `audit/`, `lm/`, `anat/`, `val/` (frozen D1 + D3 and `_D4`), `def/`, `sheets/`. Run with `run_eval.sh`.
- **New tools** in `tools/rac/rp/mpfb_family/`: `propagate.py`, `family_sheets.py`, `family_manifest.py`.
- **Tool changes:**
  - `validator_v2.py`: `--scale-ref` (D4);
  - `anatomy.py`: canvas grows for tall sources (Marchfolk unchanged);
  - `make_prod.py`: status label argument.

**Results**
- Skarn topology identical; C1R identity preserved.
- Open: configuration-1 heel T-2 1.70 mm; validator residuals (hip / toe roots).

**Next:** STOP for ChatGPT review (D4, family margin v003.1 or exceptions).

## LATEST (2026-10-26) — RP3 MARCHFOLK v004 FINAL ORDER — awaiting ChatGPT review

**What was done**
- Order 2d34a0c executed. Gate: `reviews/claude-rac-rp3-marchfolk-v004-final-family-core-gate.md`.
- **D1:** `tools/rac/rp/marchfolk_rp3_v001/validator_v2.py`. It reports legacy, D1 and D1+D3 verdicts; the legacy verdict equals `audit.py`.
- **D2 finding:** the flagged toe-IP poles belong to the neighbouring toes' 4-pole tip caps. No v004 was made.
- **New tools:** `mf4_sheets.py`; `mf_deform.py` now has `toe_flex30_l` / `toe_ext30_l` poses (zone `ball_l`).
- **Workspace:** `/tmp/claude-0/rt/m3/v4` (validator JSONs, toe / sanity deformation) and `sheets4/`.

**Next:** STOP for ChatGPT review (freeze v003, accept D3, configuration-1 sole +0.41 mm note).

## LATEST (2026-10-26) — RP3 MARCHFOLK v003 FAMILY CORE — awaiting ChatGPT review

**What was done**
- Order 103c832 executed. Gate: `reviews/claude-rac-rp3-marchfolk-family-core-v003-gate.md` (FAMILY BASE FAIL / NEEDS AUTHOR DECISION).
- Workspace `/tmp/claude-0/rt/m3`:
  - `v3/core_final.npz` (= `core_l`);
  - `cand/MF-{M,F}-R_v003.npz`;
  - `audit/`, `anat/`, `def/`, `knee/`, `sheets3/`, `ov3/`.
- Build lineage: `v003_build.py` (core_e) → `repair.py` (stc python, bpy) → resume P + T (core_g) → `revert_region.py shoulder_l,shoulder_r 18` (core_l).
- Tools in `tools/rac/rp/marchfolk_rp3_v001/`:
  - `core3lib.py`, `v003_build.py`, `repair.py`, `revert_region.py`;
  - `residuals.py`, `v3_report.py`, `mf3_sheets.py`, `sidecars3.py`;
  - `make_v3cand.py`, `ring_search.py`;
  - `mf_deform.py` (`KNEE_OFF_CM`, `ONLY_POSES`).
- Run the evaluation sequentially (`run_v3eval.sh`); parallel runs hit the memory limit.

**Results**
- Firm failures: configuration 1 = thumb_mcp_l, toe3_j3_l/r; configuration 2 = shoulder_l/r, thumb_mcp_l, toe3_j3_l/r, toe4_j2_l/r.
- Thumb and configuration-2 shoulders: band ray undefined (tie order). Toe IP poles: moving them creates contact.

**Known tool caveat:** the band method's `surf()` breaks ties by candidate order when no candidate passes the normal test. Appending vertices can change undefined-side counts.

**Next:** STOP for ChatGPT review (decisions D1 / D2).

## LATEST (2026-10-26) — RP3 MARCHFOLK PRODUCTION BASELINE GATE + RP2 CLOSURE — awaiting ChatGPT review

**What was done**
- Order d18ff2a executed.
  - Part A: closure `reviews/claude-rac-rp2-grask-final-closure.md`.
  - Part B: gate `reviews/claude-rac-rp3-marchfolk-production-baseline-gate.md`.
- Workspace `/tmp/claude-0/rt/m3`:
  - `src/` (regenerated blends, native npz);
  - `cand/` (s1, v002, leg rings);
  - `audit/`, `lm/`, `anat/`, `def/`, `ov/`, `sheets/`.
- MPFB 2.0.17 is cloned into the container's Blender extensions (symlink).
- Tools `tools/rac/rp/marchfolk_rp3_v001/`:
  - `regen.py`, `native_export.py`, `audit.py`, `face_rings.py`;
  - `subdiv.py`, `leg_rings.py`;
  - `landmarks.py`, `joint_centring.py`, `anatomy.py`;
  - `make_prod.py`, `mf_deform.py`, `mf_sheets.py`, `sidecars.py`.
- Run the sheet script with system `python3`; stc python lacks rtree.
- PC: `E:/…/production/Marchfolk/RP3/` (read-back identical).

**Results**
- Native hm08 fails §7 / §8.
- v002 (linear subdivision + 98 leg rings, linear map M) has the same topology in both configurations. It passes density, anatomy and face readiness.
- §7 residual failures: hand / foot junction poles.
- Deformation: no topology failure; weights + contact; configuration 1 knee joint-placement flag.
- Recommendation: FAMILY BASE NEEDS CORRECTION (bounded hand / foot pole relocation in the family core).

**Next:** STOP for ChatGPT review. Do not start Skarn or other races, propagation, rig or UE5.

## LATEST (2026-10-26) — RP2 GRASK FINAL LEFT-FLEX90 CLEANUP — awaiting ChatGPT review

**What was done**
- Order bd11ab0 executed. Gate: `reviews/claude-rac-rp2-grask-final-left-flex90-cleanup-gate.md`.
- Workspace `/tmp/claude-0/rt/r10` (cand/LF1-2, lf1/, lf2/ with vsrc/, diag/, sheets/).
- Tools: `lf_corr.py`, `dqs_blend.py`, `lf_maps.py`.
- SW3 baseline comes from r9 (sw1 weights, sw3 blend mask, sw3full posed).

**Results**
- LF1 / LF2 fix the non-contact pairs and the crease but keep 2–3 local inversions and 2–4 folds outside, with orientation 111–113. No selection.
- Shoulder experimentation is CLOSED for RP2. Elbow is closed. SW3 is the accepted shoulder direction.
- Parents identical. Other poses bit-identical.

**Next:** STOP for ChatGPT review (gate §6: final RP2 disposition, then the next stage).

## LATEST (2026-10-26) — RP2 GRASK VC3 INTERFACE CLEANUP + SHOULDER SW — awaiting ChatGPT review

**What was done**
- Order 28dd8d3 executed. Gate: `reviews/claude-rac-rp2-grask-vc3-interface-cleanup-shoulder-weight-volume-gate.md`.
- Workspaces:
  - E2: `/tmp/claude-0/rt/r8` (cand/F1-F2, corr/, diag/, sheets/);
  - S2: `/tmp/claude-0/rt/r9` (cand/, t1/, t2/, sw1/, sw2/, sw3/, sw3full/, diag/, sheets/).
- Tools:
  - E2: `vc3_fair.py`, `e2_texture.py`, `e2_sheets.py`;
  - S2: `sw_dqs.py` (numpy LBS/DQS blend → VSRC), `sw_maps.py`, `sw_strain.py`;
  - `shoulder_s2.py`, `shoulder_judge.py` and `shoulder_sheets.py` extended.

**Results**
- E2: no pass (texture remains; new local inversions). Elbow experimentation is CLOSED per order §11.
- S2: SW3 best. It fails only left flex90 (7.9 mm, 6 nc, 2 inv). Full suite shows no regression outside D1.
- Parents identical.

**Next:** STOP for ChatGPT review (gate §6).

## LATEST (2026-10-26) — RP2 GRASK 130° VC ELBOW + SHOULDER ISOLATION — awaiting ChatGPT review

**What was done**
- Order 69f2660 executed. Gate: `reviews/claude-rac-rp2-grask-elbow-vc-contact-and-shoulder-isolation-gate.md`.
- Workspaces:
  - Track E: `/tmp/claude-0/rt/r6` (cand/, trial/, corr/, diag/, sheets/);
  - Track S: `/tmp/claude-0/rt/r7` (s1/, s2/, probe/, diag/, sheets/).
- Baselines come from r4 (W0 / C2 / C2rx) and r5 (H2).
- Tools:
  - Track E: `vc_judge.py`, `vc_sheets.py`, `elbow_overlap_volume.py` (needs pip libigl), `elbow_girth.py`, `elbow_ripple.py`;
  - Track S: `shoulder_s1.py`, `shoulder_s2.py`, `shoulder_judge.py`, `shoulder_sheets.py`, `full_regress.py`.
- Evaluator changes:
  - `corr_solve.py`: volume options;
  - `diag_lib.py`: `POSE_JSON=` override.

**Results**
- Track E: VC3 passes all numeric §10 checks but fails the visual criterion (contact-interface fold texture), so 130° is unresolved. W0's closed volume double-counts the interpenetration overlap.
- Track S: WEIGHTING-DOMINANT; mechanics secondary (abduction).
- Parents identical.

**Next:** STOP for ChatGPT review. Decisions are listed in gate §7.

## LATEST (2026-10-26) — RP2 GRASK ELBOW HELPER-VOLUME STUDY (Stage A failed §7; Stage B not run) — awaiting ChatGPT review

**What was done**
- Order 8e5021d executed. Gate: `reviews/claude-rac-rp2-grask-elbow-helper-volume-shoulder-isolation-gate.md`.
- Workspace `/tmp/claude-0/rt/r5`; tools `helper_rig.py`, `run_helper.sh`, `helper_judge.py`, `stageA_sheets.py`.
- Comparison baseline C2 / C2rx comes from `/tmp/claude-0/rt/r4`.

**Results**
- Helper = forearm-child scale bulge (H1); H2 = helper + C2-style corrective re-solved on it; H3 = crease-core-tapered refinement.
- H2 wins at 60–120° but fails at 130°: volume-loss reduction 26 / 28 % (target 50 %), crease 8.2 mm.

**Open decisions:** D-1 … D-4 in the gate.

**Next:** STOP for ChatGPT review.

## Previous (2026-10-26) — RP2 GRASK NAIL CRITERION v2 + ELBOW POSE-SPACE CORRECTIVE — awaiting ChatGPT review

Status: retopology frozen; elbow corrective diagnostic review pending; production deformation not accepted.

**What was done**
- Order 6c38d75 executed. Gate: `reviews/claude-rac-rp2-grask-nail-criterion-elbow-corrective-gate.md`.
- Workspace `/tmp/claude-0/rt/r4`; `run_v004.sh` reproduces the cycle; `make_v004.sh` builds the blend.
- Built `E:/…/RP2/DIAG/GR_U_REF_RP2_rigdiag_v004.blend` (859b1e86…).

**Results**
- Nail Plate Rigidity v2 gates.
- Corrective C2 (left) and C2rx (right) selected.
- Full suite 20/43, no regressions.

**Open decisions:** C-1 … C-5 and K-1 in the gate.

**Next:** STOP for ChatGPT review.

## Previous (2026-10-26) — RP2 GRASK NAIL BINDING + LEFT-ELBOW WEIGHT ISOLATION — awaiting ChatGPT review

Status: retopology frozen; nail/elbow diagnostic review pending; production deformation not accepted.

**What was done**
- Order b303b9e executed. Gate: `reviews/claude-rac-rp2-grask-nail-binding-elbow-weight-isolation-gate.md`.
- Workspace `/tmp/claude-0/rt/r3`; tools `weights_nail.py`, `pair_judge.py`, `nail_skin_check.py`, `elbow_weights.py`, `run_elbow.sh`, `elbow_judge.py`, `elbow_penetration.py`, `elbow_sheets.py`, `face_inspect.py`.
- Built `E:/…/RP2/DIAG/GR_U_REF_RP2_rigdiag_v003.blend` (4ab743fe…; v002 landmarks + W0).

**Results**
- WN (plate) = no-op on all criteria; WNcap rejected (skin artifact).
- E1/E2 not selected; W0 retained.
- No full-suite rerun or v003-knee check was triggered, because nothing was selected.

**Open decisions:** N-1, N-2, E-1 … E-3 in the gate.

**Next:** STOP for ChatGPT review.

## Previous (2026-10-26) — RP2 GRASK DIAGNOSTIC DEFORMATION FAILURE ISOLATION — awaiting ChatGPT review

**What was done**
- Order 8918cea executed. Gate: `reviews/claude-rac-rp2-grask-diagnostic-deformation-failure-isolation-gate.md`.
- Workspace `/tmp/claude-0/rt/r2`; tools `run_iso.sh`, `weights_dev.py`, `lm_v003.py`, `iso_judge.py`, `iso_sheets.py`, `metric_check.py`.
- Built v003 bounded knees and `rigdiag_v002` (E:/…/DIAG, 9e2d078a…).

**Results**

| Suite | Baseline W0 | W2 |
|---|---|---|
| Full suite (43 poses) | 20 | 12 |

- Nail binding helps.
- Region-boundary weight seams caused the W2 regressions.
- The topology contribution is not excluded.

**Open decisions:** D-1 … D-7 in the gate.

**Next:** STOP for ChatGPT review.

**Disk note:** old loose scratch files (> 2 days) in `/tmp/claude-0` were deleted to free space.

## Previous (2026-10-25, night 2) — RP2 GRASK LANDMARK ADJUDICATION v002 + DIAGNOSTIC RIG v001 — awaiting ChatGPT review

**What was done**
- Order bf7d664 executed. Gate: `reviews/claude-rac-rp2-grask-rig-landmark-adjudication-diagnostic-gate.md`.
- Workspace `/tmp/claude-0/rt/rd`; pipeline `tools/rac/rp/grask_rigprep_v001/run_diagstage.sh`.
- v002 landmarks (27/27 checks) and the derived rig `E:/…/RP2/DIAG/GR_U_REF_RP2_rigdiag_v001.blend` (59ca4fda…).
- D1–D10: 20/43 pass. Failures are LBS / weights crease collapse; DQS restores the zone volume. No topology problem.

**Decisions open for ChatGPT**
- topology conclusion;
- hip pivot (the inguinal-axis alternative is better at 90° but beyond the AD-R1 5 mm cap);
- whether forearm–upper-arm contact counts as contact anatomy;
- shoulder elevation with girdle participation;
- next stage: skinning strategy / correctives / nails plus the facial-oral stage;
- knee AP/ML interpretation.

**Next:** STOP for ChatGPT review.

## Previous (2026-10-25, late night) — RP2 GRASK RIGPREP READINESS PROPOSAL v001 — awaiting ChatGPT review

**What was done**
- Order c6db89c executed. Gate: `reviews/claude-rac-rp2-grask-rigprep-readiness-gate.md`.
- Proposal JSON, tables and sheets: `reviews/rac-rp2-evidence/grask_rigprep_readiness_v001/`.
- Tools: `tools/rac/rp/grask_rigprep_v001/` (`run_rigprep.sh`; workspace `/tmp/claude-0/rt/rpr`).
- Parents unchanged; before and after hashes are in `hashes/`.

**Method**
- Internal centres = coordinate median of surface definitions A/B and the frozen value C; uncertainty = the largest distance to any alternative.
- Construction joints are carried exactly and surface-validated.
- v003 re-run shows stability: Δ ≤ 0.003 cm for section methods, ≤ 0.45 cm for sphere and skin fits.
- The frame convention, left-handed analysis frame vs right-handed Blender frames, and the flexion signs are in the JSON.

**Next:** STOP for ChatGPT review and the author decisions AD-R1…R12. No rig or diagnostic armature until a later execution order.

## Previous (2026-10-25, night) — RP2 GRASK RETOPO V003 — AUTHOR ACCEPTED / FROZEN; RP2 retopology CLOSED

**What was done**
- Order 2b29098 has been executed.
- The accepted blend (03bfe7d9…, geometry f9c4a7ac…) was frozen in place, byte-identical.
- Freeze record: `E:/…/RP2/GR_U_REF_RP2_retopo_v003_FREEZE.json` (6ed226bb…).
- Report: `reviews/claude-rac-rp2-grask-retopo-v003-freeze-report.md`.
- The read-back audit passed and was identical to the accepted hashes. v005, v001 and v002 are unchanged.

**Rules carried forward**
- The thumb-web hollow is accepted source anatomy; do not touch it.
- The ring–pinky web quad exception (edge ratio 8.07) is accepted; do not move it.

**Next:** STOP for ChatGPT review. That review will determine the next Grask production stage; there is no further retopology iteration.

## Previous (2026-10-25, later) — RP2 GRASK RETOPO V003 AUDIT CLOSURE — technical audits pass; author visual review pending

**Where things stand**
- Order 4d4f6e0 has been executed.
- Thumb-web images are in `reviews/rac-rp2-evidence/grask_retopo_v003_audit_closure/thumb_web/`. The hollow is source anatomy; v002 had saddle rumples; v003 removes them; v005 is unchanged.
- v003 is on the PC as `E:/…/RP2/GR_U_REF_RP2_retopo_v003.blend` (03bfe7d9…), with `.json` and `_landmarks.json`. Gate: `reviews/claude-rac-rp2-grask-retopo-v003-audit-closure-gate.md`.
- **Open author decisions:**
  1. Whether to soften the source hollow (illustrate first).
  2. Visual acceptance of v003.

**How to rebuild** (cloud `/tmp/claude-0/rt`, ephemeral)
- Run `tools/rac/rp/grask_retopo_v003/run_v003.sh`.
- `finalaudit.sh` audits the exported blend through `rbnpz.py`.
- `sheets3.py` is strict: it fails on any missing panel.

**Lessons**
- Edge-ratio repair at narrow web slots needs fold and self-intersection guards (a crop BVH check inside `optfix.py`).
- `foldfix` / `revsx` applied after optfix can undo crease capture. Prefer the guards over cleaning up afterwards.
- Oblique fan rings can pass the closed-ring count while the path count behind the ankle stays low, so verify both counts.
- Render close-ups of webs to catch shading rumples that the deviation numbers do not show.

## LATEST AUTHOR ORDER (2026-10-25) — Grask thumb-web images / audit closure

- Read `reviews/chatgpt-rac-rp2-grask-thumb-web-visual-review-and-audit-closure-order.md` before continuing Grask RP2. This supersedes the v002 self-reported readiness as the current action: v002 remains constrained, not accepted or frozen.
- Tyler says the model looks good but questions the thumb-index dent shown in a SOURCE right-hand image. Display isolated matched source/v002 close-ups first. No source-anatomy correction without explicit approval of an illustrated proposal.
- Close the named short-edge quad concern, demonstrate both ankle/right-elbow loops, and replace occluded/missing evidence views. Distinguish the two aspect measures. Only submit a revised production mesh after all required technical audits and evidence checks pass; keep failing iterations internal and report genuine blockers honestly.
- Keep frozen v005 unchanged and Turnfall separate. No freeze or downstream work.

Updated: 2026-10-25 (RP2 Grask retopo v002 optimization COMPLETE / READY FOR AUTHOR REVIEW). Earlier: 2026-10-24 (RP2 Grask production retopology v001 COMPLETE / READY FOR AUTHOR REVIEW). Earlier same day: anatomical source v005 FINAL-AUTHOR ACCEPTED / FROZEN. Earlier same day: v004 extremity reconstruction. Previously 2026-10-23 (v003 extremity refinement). Earlier: 2026-10-19 session 7 (RP1E non-local sub-cage rebuild order a2f5ee5 IN PROGRESS — feet rebuilt in cloud (toegen.py), hands generator diggen.py in progress; nothing new imported yet; v011.blend still authoritative).

## LATEST (2026-10-25) — RP2 GRASK RETOPO V002 OPTIMIZATION — COMPLETE / READY FOR AUTHOR REVIEW
- Order `reviews/chatgpt-rac-rp2-grask-retopo-v002-production-optimization-order.md` (d683312). Gate `reviews/claude-rac-rp2-grask-retopo-v002-optimization-gate.md` (40/40 PASS); evidence `reviews/rac-rp2-evidence/grask_retopo_v002_optimization/`; tools + README + exact `run_v002.sh` in `tools/rac/rp/grask_retopo_v002/`.
- PC: `E:/…/production/Grask/RP2/GR_U_REF_RP2_retopo_v002.blend` (49ae8a6e…f55e), `.json` sidecar (2dbd7221…), `_landmarks.json` (48887566…). Production origin = pelvis_root on the ground (translation −0.1118, +5.7227, 0 cm). v005 and v001 re-hashed unchanged.
- Result: ×2 of revised cage27 (v001 cage + support loops: UPOST palm rings, TOEP1, FFW forefoot, FINP1, NFAN 18) = 164,512 quads, 0 hard-limit quads, loops 69/69, T-1/2/3/6/7 pass, 0 self-intersections / folds.
- Rebuild (cloud `/tmp/claude-0/rt`, ephemeral): `run_v002.sh`. Lessons: never run two `polish.py` jobs that share a temp file (now per-pid); qopt/lrepair moves can create self-intersections — always `revsx.py` against the pre-step mesh; a `CREASE_BOX` crease must restrict its relax to the box (it used to smooth the whole body); thin quads straddling a narrow crease show up as prod->src centroid deviation — `centfix.py`; the last web-root slivers need direct local optimisation (`optfix.py`, Powell, ≤0.3 mm off-surface); surface-fit landmarks need dense area samples or flat summits jump with facet size; the path-only loop count under-reads oblique loops at ×2 (use ring trace too).
- STOP: awaiting Tyler / ChatGPT author review. No freeze / rig / skin / morphs / UVs / LODs / UE5 / other races.

## Previous (2026-10-24) — RP2 GRASK PRODUCTION RETOPOLOGY V001 — COMPLETE / READY FOR AUTHOR REVIEW
- Order `reviews/chatgpt-rac-rp2-grask-production-retopology-kickoff-order.md` (61ff0e7). Gate `reviews/claude-rac-rp2-grask-retopo-v001-gate.md` (30/30 PASS); evidence `reviews/rac-rp2-evidence/grask_retopo_v001/`; tools + README `tools/rac/rp/grask_retopo_v001/`.
- PC: `E:/…/production/Grask/RP2/GR_U_REF_RP2_retopo_v001.blend` (82c10a64…ded0, geometry 5ebc7813…6dec), `.json` sidecar, `_landmarks.json`. Source v005 unchanged (hashes re-verified after). Earlier RP2 production v001–v006 untouched.
- Result: 628,738 V / 628,736 quads, 0 tris, watertight single body, 0 self-intersections / folds; T-1/T-2/T-3/T-6/T-7 pass (worst: foot 1.07 mm, landmark 0.80 mm, profile IoU 0.99657); loops 69/69; 422 tagged loops; seam proposal only.
- Rebuild (cloud `/tmp/claude-0/rt`, ephemeral): `run21.sh` (build_cage → pipe2.sh → sxfinal/foldfix) then the gate suite listed in the tools README. Key lessons: fan hinge must sit outside the skin (arm/torso gap) or rings converge into slivers; adjacent digit ports must share cleft edges (gap strips fold into webs); the toe web line must come from the most proximal interdigital slot point (a cap plane inside the slot bridges it); crease capture must be part-aware (never pull a digit's vertices onto its neighbour's wall); surface-fit landmarks must use area samples / ray or section constructions (vertex argmax drifts by cm); the old "mouth" inset had been on the chin — lips are at z≈194.6.
- STOP: awaiting Tyler / ChatGPT author review. No rig / skin / morphs / UVs / LODs / UE5 / other races.

## Previous (2026-10-24) — RP2 GRASK 3D ANATOMICAL SOURCE V005 — FINAL-AUTHOR ACCEPTED / FROZEN
- Authority: `reviews/chatgpt-rac-rp2-grask-3d-source-v005-final-author-acceptance-freeze-order.md` (33e4aaf). Tyler accepted v005; no further anatomical-source passes (no v006 polish).
- Canonical parent for all future Grask RP2 mesh work: `E:/…/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend` (7bba8d2d…ab14), GLB 81f872e7…c548, geometry 2697929d…d7bc. v005 wins over downstream meshes on accepted anatomy.
- v001–v004 kept unchanged as history only.
- STOP: no retopology / RP2 v007+ / rig / skinning / creator morphs / UE5 / next race until a separate explicit downstream order (which must use v005 as source parent).

## Previous (2026-10-24) — RP2 GRASK 3D ANATOMICAL SOURCE V005 EXTREMITY NATURALIZATION PASS / READY FOR AUTHOR FREEZE REVIEW — then FINAL-AUTHOR ACCEPTED / FROZEN
- Order `reviews/chatgpt-rac-rp2-grask-3d-source-v005-extremity-naturalization-order.md` (6c7691d). Report `reviews/claude-rac-rp2-grask-3d-source-v005-extremity-naturalization-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_3d_source_v005_extremity_naturalization/`.
- PC: `E:/…/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend` (7bba8d2d…, zstd), `.glb` (81f872e7…), `.json`, `_naturalization_masks.npz`; v001–v004 kept.
- Rebuild (cloud `/tmp/claude-0/src3d/v5`, ephemeral): same pipeline as v004 with `nat` parameter blocks in `hand_model.py`/`foot_model.py` (architecture params identical); right frame tilt 2.0° in `hand_frame.py`; stitch base = v004 (`assemble.sh`), `finalize5.py` (freeze vs v004), `export_v5.py`. Look-dev: `hand_quick.py` + `hq_render.sh`; cross-sections `xsec.py`.
- Lesson: smooth-union (smin) at every phalanx junction inflates by ~k/4 and reads as bead collars; keep junction k small and express joints with broad low planes + creases.
- (Accepted and frozen by 33e4aaf.)

## Previous (2026-10-24) — RP2 GRASK 3D ANATOMICAL SOURCE V004 EXTREMITY RECONSTRUCTION PASS / READY FOR AUTHOR FREEZE REVIEW — later naturalized into v005 (architecture accepted)
- Order `reviews/chatgpt-rac-rp2-grask-3d-source-v004-extremity-reconstruction-order.md` (7fa3b44). Report `reviews/claude-rac-rp2-grask-3d-source-v004-extremity-reconstruction-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_3d_source_v004_extremity_reconstruction/`.
- PC: `E:/…/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v004.blend` (ed83bf92…, zstd-compressed to fit 30 MB transfer limit), `.glb` (696f756f…), `.json`, `_reconstruction_masks.npz`; v001–v003 kept.
- Rebuild (cloud `/tmp/claude-0/src3d/v4`, ephemeral; use system python3 for builds (pymeshlab), `/home/claude/stc/bin/python3` for bpy/renders/SI): `build_hand.py L|R 0.05 350000` → `AC=0.4 FK=2.0 build_foot.py L|R 0.05 190000` → `assemble.sh` → `finalize4.py` (right-forefoot ground + tech + freeze stats) → `sxq.py` → `export_v4.py`. Evidence: `render_v4.sh MESH TAG`, `pose_diag.py` (fist: TS=-1 TD=[0.85,-0.27,-0.47] TF=[30,40]), `sheets_v4.py`, `wire.py`.
- (v004 architecture accepted; not frozen — naturalized into v005.)

## Previous (2026-10-23) — RP2 GRASK 3D ANATOMICAL SOURCE V003 EXTREMITY REFINEMENT PASS / READY FOR AUTHOR FREEZE REVIEW — later superseded by v004 reconstruction
- Order `reviews/chatgpt-rac-rp2-grask-3d-source-v003-extremity-refinement-order.md` (b00ac6b). Report `reviews/claude-rac-rp2-grask-3d-source-v003-extremity-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_3d_source_v003_extremity/`.
- PC: `E:/…/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v003.blend` (aad25f89…); v001/v002 kept.
- Rebuild (cloud `/tmp/claude-0/src3d`, ephemeral): v002 npz → `devalence3.py` (region) → `subdiv_region.py` → `linfix.sh` → `ext_clean.py {l1 .4,k1 1,k2 0,lp1 8}` → `microfix.py .45` → `sculpt_digits.py production/sculpt_params_v003.json` → `ext_clean.py {l1 .12,k1 .8,lp1 4}` → `microfix.py` → `defold.py 12 0.5` → `eye_open.py production/eye_params_v003.json` → right-sole ground fix → `export_v3.py`.
- (v003 not approved; superseded by v004 extremity reconstruction.)

## Previous (2026-10-23) — RP2 GRASK 3D ANATOMICAL SOURCE V002 REFINEMENT PASS / READY FOR AUTHOR REVIEW — later refined into v003
- Order `reviews/chatgpt-rac-rp2-grask-3d-source-v002-refinement-order.md` (63d7dde). Report `reviews/claude-rac-rp2-grask-3d-source-v002-refinement-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_3d_source_v002_refinement/`.
- PC: `E:/…/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v002.blend` (0651765f…), `.glb`, `.json`, `_refinement_masks.npz`; v001 kept (2315d5c1…).
- Rebuild (cloud `/tmp/claude-0/src3d`, ephemeral): v001 npz → `tools/ear_transplant.py IN OUT 4` → `tools/refine_loop.sh IN OUT production/refine_params_v002.json` → `export_v2.py`. Evidence: `render_v2.sh MESH TAG` + `sheets_v2.py`.
- STOP: awaiting Tyler approval of v002. Production retopology only after approval.

## Previous (2026-10-23) — RP2 GRASK 3D ANATOMICAL SOURCE REBASE COMPLETE / READY FOR AUTHOR REVIEW — later refined into v002
- Order `reviews/chatgpt-rac-rp2-grask-3d-source-rebase-order.md` (224e33b: stop morphing v006; build a clean anatomical source from the generated 3D figure). Report `reviews/claude-rac-rp2-grask-3d-source-rebase-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_3d_source_rebase/`.
- PC: `E:/…/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v001.blend` (2315d5c1…), `.glb`, `.json`, `_reconstruction_masks.npz`. Input `C:/Users/Tyler/Downloads/base.glb` (363b4566…). Repo proxy `GRASK_front_reference_proxy_v001.glb.gz` is corrupt (not needed).
- Pipeline (cloud `/tmp/claude-0/src3d`, ephemeral): extract → scale 218 → symplane align → donor pelvis fitdonor/finefit/stitch (z 87–135) → seam fair → head yaw → neutralize (neut_loop until 0 self-ix) → finalize (thigh mound) → scalp_clean → rescale → export_source / readback.
- STOP: awaiting Tyler visual approval of the source. Production retopology (v007+) only after approval.

## Previous (2026-10-23) — RP2 GRASK V006 MASS-HIERARCHY CORRECTION PASS / READY FOR AUTHOR REVIEW — later superseded by 3D source rebase
- Order `reviews/chatgpt-rac-rp2-grask-v006-mass-hierarchy-correction-order.md` (v005 too smooth / under-massed); report `reviews/claude-rac-rp2-grask-v006-mass-hierarchy-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_v006_mass_hierarchy/` (rebuild: `tools/v6build.sh params_v006.json TAG`; silhouette study `silhouette/v6sil.py`; deform suite 54 poses, weight smoothing 60). Note: thin limbs need `profile_extra` (un-low-passed) — the macro low-pass absorbs most radial limb deltas.
- PC: `E:/…/production/Grask/RP2/GR_U_REF_RP2_production_v006.blend` (9f4275cc…); v001–v005 kept. Cloud dir `/tmp/claude-0/rp2` (ephemeral).
- STOP: waiting for author review; no canon freeze / next race / rig / creator / UE5.

## Previous (2026-10-23) — RP2 GRASK V005 BODY-FORM CLEANUP PASS / READY FOR AUTHOR REVIEW — later NOT ACCEPTED (mass hierarchy)
- Order `reviews/chatgpt-rac-rp2-grask-v005-body-form-cleanup-order.md` (v004 lumpy thighs / back mound / chest point / arm bulges); report `reviews/claude-rac-rp2-grask-v005-body-form-cleanup-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_v005_body_form_cleanup/` (rebuild: `tools/v5build.sh params_v005.json TAG` or `ident_full.sh` → `ground.py` → `f32safe.py`; deform suite 54 poses, weight smoothing 60).
- PC: `E:/…/production/Grask/RP2/GR_U_REF_RP2_production_v005.blend` (958af4fd…); v001–v004 kept. Cloud dir `/tmp/claude-0/rp2` (ephemeral).
- STOP: waiting for author review; no canon freeze / next race / rig / creator / UE5.

## Previous (2026-10-23) — RP2 GRASK v004 TARGET-IMAGE GROUNDED-TROLL BUILD PASS / READY FOR AUTHOR REVIEW — later NOT ACCEPTED (form lumps)
- Order `reviews/chatgpt-rac-rp2-grask-v004-target-image-grounded-troll-build-order.md` (v003 rejected as too human/narrow; Tyler's target image is the visual authority); report `reviews/claude-rac-rp2-grask-v004-target-image-grounded-troll-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_v004_target_image/` (rebuild: `tools/ident_full.sh params_v004.json TAG` then `ground.py` then `f32safe.py`; deform suite now 54 poses, run with weight smoothing 60).
- PC: `E:/…/production/Grask/RP2/GR_U_REF_RP2_production_v004.blend` (cd8f1cdb…); v001, v002, v003 kept. Cloud dir `/tmp/claude-0/rp2` (ephemeral).
- STOP: waiting for author review; no canon freeze / next race / rig / creator / UE5.

## Previous (2026-10-23) — RP2 GRASK v003 GROUNDED-TROLL IDENTITY BUILD PASS / READY FOR AUTHOR REVIEW — later REJECTED as too narrow/human
- Order `reviews/chatgpt-rac-rp2-grask-v003-grounded-troll-correction-order.md` (v002 rejected as alien); report `reviews/claude-rac-rp2-grask-v003-grounded-troll-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_v003_grounded_troll/` (rebuild: `tools/ident_full.sh params_v003.json TAG` then `ground.py` then `f32safe.py`).
- PC: `E:/…/production/Grask/RP2/GR_U_REF_RP2_production_v003.blend` (46697d1b…); v001 and v002 kept. Cloud dir `/tmp/claude-0/rp2` (ephemeral).
- STOP: waiting for author review; no canon freeze / next race / rig / creator / UE5.

## Previous (2026-10-23) — RP2 GRASK IDENTITY-CORRECTED (v002) BUILD PASS — later REJECTED as too alien
- Order `reviews/chatgpt-rac-rp2-grask-identity-correction-and-completion-order.md`; report `reviews/claude-rac-rp2-grask-identity-correction-final-gate.md`; evidence + tools `reviews/rac-rp2-evidence/grask_identity_correction/` (rebuild: `tools/ident_full.sh params_v002.json TAG` from v001 pre-rimlock base cand_h4_12; MakeHuman CC0 targets cloned from makehumancommunity/makehuman data/targets).
- Candidate on PC: `E:/…/production/Grask/RP2/GR_U_REF_RP2_production_v002.blend` (9622a062…); v001 kept. Cloud dir `/tmp/claude-0/rp2` (ephemeral).
- Waiting for author visual review; no canon freeze / next race / rig / creator / UE5.

## Previous (2026-10-23) — RP2 GRASK PRODUCTION PILOT TECHNICAL PASS / READY FOR OWNER VISUAL REVIEW
- Gate `reviews/claude-rac-rp2-grask-production-pilot-gate.md`; asymmetry `reviews/claude-rac-rp2-grask-asymmetry-adjudication.md`; evidence + full tool chain `reviews/rac-rp2-evidence/` (`tools/run_all.sh` then hybrid.py LP=12 167 173 → rimlock.py 0.3 → f32safe.py → export_blend.py).
- Candidate on PC: `E:/…/production/Grask/RP2/GR_U_REF_RP2_production_v001.blend` (81f579f9…), sidecar/landmarks/mapping alongside. Cloud working dir `/tmp/claude-0/rp2` (ephemeral).
- Waiting for owner visual review; do nothing further on RP2 until a new order. No RP3 / rig / creator / UE5.

## Previous (2026-10-23) — RP1 GORRUND FINAL OWNER ACCEPTED / FROZEN; RP2 GRASK STARTED
- Freeze report `reviews/claude-rac-rp1-gorrund-final-owner-freeze.md`; canonical `E:/…/production/Gorrund/RP1/GO_U_REF_RP1_FINAL.blend` (+ .json) = byte copy of rev110 (133edfde…). RP1 CLOSED — no more Gorrund work.
- Next: RP2 Grask order `reviews/chatgpt-rac-rp2-grask-production-pilot-execute-order.md` (autonomous; Tyler sees only a technical PASS). Candidates go to `E:/…/production/Grask/RP2/`, evidence `reviews/rac-rp2-evidence/`.

## Previous (2026-10-23) — HAND MESH + GRIP ORDER: PASS, READY FOR OWNER REVIEW
- Report rewritten: `reviews/claude-rac-gorrund-hand-mesh-grip-closure.md`. rev 110 mesh (thumb tips grafted from index tip) + all 16 movement/grip tests pass on Blender-verified frames.
- PC `work/claude110/`: production110.blend, grip_tests110_L_DIAG / R_DIAG.blend, reports zip, SHA256SUMS + hashes_pc (match).
- Tools + final task configs: `reviews/rac-rp1f-evidence/claude-hand-mesh-grip/tools/`, `tasks110/`. Cloud working dir `/tmp/claude-0/hand` (may not survive).
- Tyler's standing rule (2026-10-22): if anything fails the audit, keep fixing until it passes; only report results.
- Waiting for owner review; do nothing further until a new order.

## Previous (2026-10-22) — HAND MESH + GRIP ORDER: HOLD
- Report: `reviews/claude-rac-gorrund-hand-mesh-grip-closure.md`. Mesh done (PC `work/claude109/Gorrund_hand_production109.blend`, ba668cce…); grip partial.
- Open: thumb deformation (thenar corrective / helper bone / CMC placement), L handle index+thumb, contact-limited finger ranges; owner review of method, genus 1→0 cut, R crater exclusion, T-4 claw regression, contact tolerances.
- Tools in `reviews/rac-rp1f-evidence/claude-hand-mesh-grip/tools/`; cloud working state is ephemeral (reports zip on the PC).

## Previous (2026-10-20 session 14) — HAND-CLAW PROPORTION, HANDED TO CHATGPT
- Tyler rejected the v015/v015b hand-claw size: "that retractable nail look really silly with such a big finger. the two don't really match at all in proportion."
- 3 render-only mockups (A bigger sheathed claw, B thick hooked claw, C claw-shaped nail) were sent to Tyler; **no pick yet**.
- Full status, parameters, tools and step-by-step plan toward v016: `reviews/rac-rp1f-evidence/claw_mockups_v016/README.md`.
- Tyler asked to give ChatGPT a trial on completing it. v014/v015 stay frozen; v015b .blend was never made.

## Previous (2026-10-20 session 13)
- RP1F order (`chatgpt-rac-rp1f-gorrund-v015-localized-aesthetic-refinement-order.md`) executed: `reviews/claude-rac-rp1f-gorrund-v015-localized-refinement-gate.md` — **RP1F GORRUND LOCALIZED REFINEMENT COMPLETE / READY FOR AUTHOR VISUAL REVIEW**.
- PC: `GO_U_REF_RP1F_refine_v015.blend` (cage "Cylinder" = design_v014, `RP1F_production_v015`). v014.blend unchanged and still the frozen baseline.
- Evidence: `reviews/rac-rp1f-evidence/gorrund_v015/` (renders, diagnostic, masks, claw dimensions, tools; production npz in design/).
- Tyler chose "build proper claw geometry" for the hand claws; the R thumb claw is the weakest and may need a second pass or a hand sculpt.
- Waiting for Tyler's visual review.
- v015b (thumb-claw second pass) built in the cloud: `reviews/rac-rp1f-evidence/gorrund_v015b/`. PLY parts are on E: (RP1 folder). The Blender UI import to `GO_U_REF_RP1F_refine_v015b.blend` is PENDING: Tyler asked that his computer not be used while he works (writing music); he will message when he is done for the night.
- New standing preference (Tyler, 2026-10-20): do Blender work in the cloud; use his screen only when he says so. A full production `.blend` (~55 MB compressed) is over the 30 MB file-link limit, so the final UI import still needs his screen or his own clicks.

## Previous (2026-10-20 session 12)
- Order 647fa4e executed to its substantive gate: `reviews/claude-rac-rp1e-v014-resume-execution-gate.md` — **RP1E EXTERIOR PRODUCTION MESH PASS / D-MASK AUTHOR REVIEW REQUIRED**.
- Authoritative PC file now `GO_U_REF_RP1E_retopo_v014.blend` (objects: cage "Cylinder" = design_v014, `RP1E_production_v014` = final production mesh 1 427 072 quads, weldsrc). v013 and older unchanged.
- Cloud freeze: `reviews/rac-rp1e-evidence/designs/design_v014*.npz` (production mesh = `design_v014_production_L4.npz`), D masks + gate + visuals in `reviews/rac-rp1e-evidence/v014_final/`.
- Waiting for the author ruling on the D-mask throat placement. Do nothing further until a new order.

## Roles and loop
- ChatGPT writes orders: `reviews/chatgpt-rac-rm-ot-05XX-*.md`. Tyler authorized them as if from him.
- Claude executes, gates, commits `reviews/claude-rac-rm-ot-05XX-*-gate.md` + `reviews/rac-rmot05XX-evidence/`,
  inserts a paragraph in `specs/STATUS.md` (before the previous order's), adds a line to
  `reviews/claude-pass2-r5-reference-mesh-queue.md` (after the previous order's), pushes, reports plainly to Tyler.
- Tyler's rules: close every Blender window when done (never leave extra instances); final shape authoring is
  Blender UI only on Tyler's PC (no Blender Python console there); cloud scripts only for prep/diagnostics/masks/repair/evidence.
  Downloads go to the E: drive. Leave the old frozen Blender window and the File Explorer window alone.

## PC paths
- Blender: `E:\Tools\Blender\blender-5.2.2-windows-x64\blender.exe`
- Gorrund work: `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AW4\` (latest final; 05AW3/05AW2/05AW1 siblings; earlier passes in sibling 05AO/05AT/05AV/05AW folders)

## Frozen state
- Latest pass: 05AW nails = GO-05AW_nails_final (see below); before that 05AV feet = GO-05AV_feet_final; 05AT AC3 = GO-05AT_AC3. Previous: 05AO AC2 — `GO-05AO_AC2.blend` sha `ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`,
  GLB `1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434` (commit f7fc142).
- 05AP (10dc9a5): Smooth-only AC3 not credible; nothing authored.

## CURRENT order: RAC RP1E Gorrund contact-zone recovery (2026-10-19) — IN PROGRESS
- Order: reviews/chatgpt-rac-rp1e-gorrund-contact-zone-recovery-order.md (Tyler-authorized).
  - Method: M-B, manual, no auto-remesh.
  - Tolerances unchanged and two-way.
  - Do not relax the contract. No RP2.
  - The source GO-05AW4_nails_final.blend (5a4e45d4…22d5e) is read-only.
- Deliverables:
  - gate doc reviews/claude-rac-rp1e-gorrund-contact-zone-recovery-gate.md;
  - evidence reviews/rac-rp1e-evidence/;
  - final line "RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW" or "RP1E MANUAL CONTACT-ZONE RECOVERY FAILED / AUTHOR DECISION REQUIRED";
  - STATUS paragraph, queue line, handoff update, push. Then STOP.
- RULING 3816926 (reviews/chatgpt-rac-rp1e-transcription-and-contact-scope-ruling.md): cloud-designed sub-cages may be brought in by Blender UI File > Import + UI join/merge (provenance: freeze design file, counts, hash; after import verify <= 0.10 mm vs design, only boundary stitching differs, 0 coarse self-x, closed, manifold, normals, genus 0). No tolerance relief. Order: ears -> jaw -> pouch -> axilla slits -> muzzle/nostrils; then regenerate colours, full L1-L4 progressive gate, classify residual L4 self-x (true defect vs source micro-contact); if only micro-contact remains STOP with reviews/claude-rac-rp1e-custom-cavity-checkpoint.md 'RP1E CUSTOM CAVITIES COMPLETE / MICRO-CONTACT AUTHOR RULING REQUIRED'.
- Progress log: reviews/rac-rp1e-evidence/RP1E_progress.md (method, numbers, UI build log). Commits ec55a37 (R hand), 97d6077 (L hand), d6b3d36 (axillae).
- PC working file: E:\UnrealProjects\Wayfarer 5.8\RaceBodies\production\Gorrund\RP1\GO_U_REF_RP1E_retopo_v006.blend (v005 kept unchanged = pre-feet state).
  - Open in Blender 5.2.2, Edit Mode on cage object "Cylinder" (identity matrix; Local coords in m).
  - The weld source is also in the file.
- Current cage (v006, sha 46fc46ce…5f79c): 2096 V / 2094 quads, closed, 0 non-manifold, genus 0, consistent normals. Identical topology to the frozen foot design cage_g5b (max 0.081 mm). Evidence: reviews/rac-rp1e-evidence/cage_ui_v006_feet.npz.
  - The L and R hands are separate sub-cages: palm rings P1–P4 plus 5 digit tubes each.
  - Both axillae are re-laid out to the cage_e30 design.
  - Both feet are the g5b sub-cage (shin ring A → S1–S5 → K → 4 toe tubes each; the 5th toe is fused in the source).
  - Coarse-cage self-intersections: 0.
- SESSION 12 START STATE (read this first):
  - Active order: `reviews/chatgpt-rac-rp1e-v014-m1-slit-band-and-manifold-closure-order.md` (913d0e4). NOT yet answered (no gate report written; the order forbids checkpoint reports). Continue M1 (attempt B + §8 per-wall fallback), then M2–M6, D masks, nails, v014 promotion, final gate, then write `reviews/claude-rac-rp1e-v014-manifold-closure-gate.md`.
  - M1 state: see RP1E_progress.md "M1 slit-band order — session 11". Best cage `reviews/rac-rp1e-evidence/exp_v018_m1slit/design_M1slit_r1_cage.npz` (+_col, _meta crease ids) built by `pants.py cur.npz exp_v018_m1slit/pants_r1.json` on cur = v013; sim with `CREASE=exp_v018_m1slit/crease_r1.json TPRE=tgx_m1p/t bash runc.sh TAG cage.npz fsm_cur.txt 0` (tgx_m1p from `python3 m1masks.py <outdir>`).
  - Per-wall remap: `python3 m1wall.py sim_TAG_L4.npz cage_meta.json OUT.npz 1.0`; region checks with regcheck.py / pairclus.py.
  - PC authoritative cage still `GO_U_REF_RP1E_retopo_v013.blend`. Blender not opened this session.
- SESSION 11 START STATE:
  - Ruling `chatgpt-rac-rp1e-v014-manifold-contact-topology-ruling.md` answered: `reviews/claude-rac-rp1e-v014-manifold-contact-gate.md` = RP1E MANIFOLD-CONTACT TOPOLOGY FAILED / AUTHOR DECISION REQUIRED (stopped at the M1 hand-handle gate). Wait for the author ruling (§6).
  - PC authoritative cage still `GO_U_REF_RP1E_retopo_v013.blend`; no v014. Blender not opened this session.
  - Best M1 cage: reviews/rac-rp1e-evidence/exp_v017_manifold/design_M1D04_cage.npz (+_col.npy; spec exp_v017_manifold/m1jv_04_false.json on cur=v013, targets tgx_m1 from `tgstrip.py tgx_m1/t "[-33.2,-40.5,93.2]" 3.0 22,23,0,-1,0 23,22,0,1,0`).
  - New tools: junction.py, tgstrip.py, remap.py (final-resolution disk remap onto source), sepfix.py, pairclus.py, rp1_landmarks_t6.py (ruled T-6).
- SESSION 10 START STATE:
  - Ruling `chatgpt-rac-rp1e-v014-local-stack-and-contract-ruling.md` answered: `reviews/claude-rac-rp1e-v014-local-stack-recovery-gate.md` = RP1E LOCAL PROJECTION-STACK RECOVERY FAILED / AUTHOR DECISION REQUIRED (pilot tables §2, decisions §7). Wait for the author ruling.
  - PC authoritative cage still `GO_U_REF_RP1E_retopo_v013.blend` (no v014). Blender closed.
  - New tools: own.py (per-sheet targets into tgx_<tag>/), sim.py REGCOLS/REGV (local order), pilot_eval.py, dmask.py/dtarget.py (exterior-visibility D masks), nailcheck.py (+ reviews/rac-rp1e-evidence/nail_tooling/), rp1_landmarks_comp.py (hip component rule), hgenus.py (box genus).
  - runc.sh honours TPRE and XFN (extra FINALN colours). AW4 source VF cached at /home/claude/stc/rp1/AW4_VF.npz (regenerate from GO-05AW4_nails_final.blend if lost).
- SESSION 9 START STATE:
  - Order `chatgpt-rac-rp1e-v013-class-a-closure-order.md` answered: `reviews/claude-rac-rp1e-v013-class-a-closure-gate.md` = RP1E NON-LOCAL SUB-CAGE REBUILD BLOCKED / AUTHOR DECISION REQUIRED. Wait for the author ruling (projection-stack / source / contract / T-6 definition / nail tooling, §5 of the report).
  - PC authoritative cage: `GO_U_REF_RP1E_retopo_v013.blend` (sha 230c7b3a…d778) = `designs/design_v013.npz` (5476 V / 5669 F), verified 0.00025 mm. v009–v012 unchanged. Blender closed.
  - Cloud: /home/claude/stc/rp1e cur.npz = v013 (if lost: untar scratch/rp1e_s7.tgz, then copy designs/design_v013.npz + _col.npy to cur.npz/cur_col.npy and fsm_v013.txt to fsm_cur.txt). Graded refinement: `python3 refine.py IN.npz '{"centre":[..],"R":r}' OUT.npz` (spec file); batches with rfl.py.
  - Missing in the cloud: AW4 nail-plate masks + foot frames for rp1_gate.py nails (gate_nonail.py skips them).
- SESSION 8 START STATE:
  - Order a2f5ee5 still open. PC authoritative cage: `GO_U_REF_RP1E_retopo_v012.blend` (sha 25e9b53c…7f9c) = design `designs/design_v012.npz` (5043 V / 5170 F), verified 0.00025 mm. v009–v011 unchanged. Blender closed.
  - Checkpoint report `reviews/claude-rac-rp1e-nonlocal-subcage-rebuild-gate.md` — no §11 line yet. Its §4 is the to-do list (R thumb fin with graded refinement first; philtrum bottom, upper lip, chin lobe, ear rims; lip-line contact; L pinch folds; R axilla tips; R groin ridge; natal nub classification; hand L / toe shape misses). Then v013 → UI import → full gate → §11 line.
  - Restore cloud state: untar `reviews/rac-rp1e-evidence/scratch/rp1e_s7.tgz` into /home/claude/stc/rp1e (needs /home/claude/stc/rp1/weld.npz, weld_a.npz, zones.npz, venv /home/claude/stc/bin/python3). cur.npz there = v012. Sim: `bash runc.sh TAG CAGE.npz fsm_cur.txt 0` (CAGE needs _col.npy and _remap.npy from cur; ~1.5 min); `python3 zcl.py TAG ZONE lim n`; `bash adopt.sh NEW.npz NEW_remap.npy` to make a candidate current.
  - Generators: slitgen.py (slit / fin bands; facev patches via patchsel.py; debug traces with sldbg.py), pockgen.py (pocket tubes), diggen.py/toegen.py (digits), chain.py (replay steps in base ids). Always check topo.py + selfx_npz.py = 0 before sim.
  - Blender launch: Explorer new tab → E: → Tools → Blender → blender-5.2.2-windows-x64 → blender.exe; then resolve/request blender.exe + textinputhost.exe; close the tab you opened (leave the old Downloads window).
- SESSION 7 STATE:
  - Order: reviews/chatgpt-rac-rp1e-nonlocal-subcage-rebuild-order.md (R1 L foot cleft 3 → R2 R hand webs → R3 thumb/hand clefts → R4 muzzle/nose → R5 L axilla z153 → R6 rest). Return reviews/claude-rac-rp1e-nonlocal-subcage-rebuild-gate.md with one of the §11 lines.
  - DONE (cloud): both feet rebuilt with `toegen.py` (spec toes_L3.json on design_v011; toes_R_tg8.json (rotz 36.9, mcol 13) on the L result). Result design `reviews/rac-rp1e-evidence/exp_v013/design_v012a_feet.npz` (+_col, remap_v011_to_v012a.npy): foot L self-x 0, foot R 13, devs ≤ 2.1 mm, total L4 self-x 375 (sim V13e). Coarse 0 self-x, closed, genus 0. NOTE vertex ids ≥1508 are renumbered: remap ring jsons (design_v010_rings.json) and fsm lists with the remap arrays (mkfsm.sh).
  - IN PROGRESS: hands with `diggen.py` (toegen + oblique cleft planes from adjacent finger axes, axis-marched free rings `planeslice.axis_rings`, per-digit frames). Spec hand_L.json (attach palm ring P1 1332–1341, thumb kept). Best so far V14d: hand L deviation over 1.97 % (v011 1.74 %), web contacts 2359 pairs — not yet better than v011; R hand not started. Muzzle, axilla z153, R6 not started.
  - Sim note: runv.sh TAG CAGE COL PN 1,3,...,16 with FINALSM=3 FSMF=0.5 FSMV=<fsm>; ~5 min per run. zcl.py TAG ZONE lists over-limit clusters; sxcat.py labels coarse self-x pairs by generator part.
- SESSION 6 STATE:
  - PC authoritative cage: `GO_U_REF_RP1E_retopo_v011.blend` (sha 5792e5d9…1857) = design v011 (3475 V / 3605 F), verified (`import_v011/`). v009/v010 unchanged. Blender closed at session end (v011 saved); the extra Explorer tab I opened was closed, the original Downloads tab left alone.
  - Cloud: design `designs/design_v011.npz` + `_col.npy` (J ring ownership changed: trunk 1) + `fsm_v011.txt`; exact build `tools/rac/rp/rp1e/build_c3.sh`; gate run V12c in `gate_v011/`.
  - Report `reviews/claude-rac-rp1e-class-a-recovery-gate.md`: remaining A = open pockets (R hand web 3/4, L toe cleft 3, thumb webs, philtrum, L axilla z153 crevice, R axilla tips, R toe clefts) + source micro-cavities (hand-web tunnels, L axilla void, 1 mm nostrils, natal nub). Cause: L1 limit-surface retraction of pocket tips. Author decision asked: fill/keep micro-cavities; authorise sub-cage rebuild (pocket-ring topology) or stack change.
  - New tools: fitcage.py (local limit-surface LSQ fit), ccmat.py (CC + limit matrices = Blender), slitfit.py, limitsolve.py, devopen.py (openness of over-limit points), writeobj.py (OBJ Y-up metres; reproduces previous shas).
  - Sim frame note: sim_*_L*.npz V is analysis frame (y flipped) vs cage/weld.npz (Blender cm) — multiply y by −1.
- SESSION 5 STATE (historical):
  - PC: `GO_U_REF_RP1E_retopo_v009.blend` = design v009 (3013 V / 3113 F) imported via File > Import > Wavefront, verified index-identical (0.00025 mm). v007.blend = design v007. v008.blend = stale OBJ copy (superseded, keep). Blender closed at the end of session 5 (v009 saved); the File Explorer window was left alone.
  - UI recipe (works): File(22,19) > hover Import(50,174) > slide (170,176) > Wavefront (170,209); click file row; Import button (546,607); mouse over viewport, ctrl+a > Rotation (536,499); outliner row 1 (1250,58) / row 3 (1250,70); Delete key over viewport; F2 rename with single key presses (type action does not work in popups; works in the file browser name field); ctrl+shift+s, double-click name (340,606), ctrl+a, type name, Return, click Save As (546,606). device_commit may keep a stale copy if the file name is reused: always use a new OBJ name and re-stage to check the sha.
  - Cloud current design: v010c (`reviews/rac-rp1e-evidence/designs/design_v010c.npz`, rings `design_v010_rings.json`, smoothing group `fsm_v3.txt`) — not yet imported.
  - Sim: `runv.sh TAG CAGE COL PN 1,3,...,16` with env `FINALSM=3 FSMF=0.5 FSMV=<fsm file>` (regional final smoothing), base `bsim6.sh` (FNSMR 0, SMR 2). Analysis: classify.py (now with amp), devclass.py (deviation clusters with gap/openness), regstat.py TAG box.
  - Checkpoint report: `reviews/claude-rac-rp1e-custom-cavity-checkpoint.md` (v010c: L4 self-x 992, B candidates 786, A ≈206; T-1 0.07 %, T-2 head 0.49 %).
  - NEXT: (1) hand + foot inter-digit web floors as explicit creases (lip/floor/lip) per cleft — the main A block (exposed bridged webs, up to 14 mm); (2) L axilla z153 sub-pocket + pinch/void (ruling candidate); (3) nostril slits, R axilla tips, natal-cleft top, groin end R, philtrum; (4) micro-folds; (5) import each new design (new OBJ name), re-run gate; then STOP line per ruling §6/§9.
  - Scratch bundle: `reviews/rac-rp1e-evidence/scratch/rp1e_s5.tgz` (all cloud scripts + latest npz) — untar into /home/claude/stc/rp1e (needs /home/claude/stc/rp1/weld.npz, zones.npz, venv /home/claude/stc/bin/python3 with bpy).
- SESSION 4 STATE (historical):
  - Design chain (all in /home/claude/stc/rp1e, copies in reviews/rac-rp1e-evidence/designs/, tools in tools/rac/rp/rp1e/):
    cage_g5b (= UI v006) → ears `eardesign4.py` (cage_EL → cage_ELR) → jaw rings `jawrings2.py jspec1.json` (cage_JS1) →
    thigh rings `ringfit.py th3.json` + `slidering.py` (cage_TH3 → cage_TH4) → pelvis-front/crotch `crotch4.py pdesign7.json` (cage_P9) →
    axillae `axrings.py` + `axdesign.py` R then L (cage_X1 → cage_X2, holes axholeR2/axholeL2 mapped with mapids.py) →
    tail root/natal cleft `tailrings.py` + `axdesign.py` T (cage_Y5, hole tailhole2.json, T1CLEFT=103.4,-30.0,-28.0,2.0 JOFF=0.34).
    Each step removes/renumbers verts; the *_ear*/_crotch/_ax*.json files hold rings, holes and 'removed' lists.
  - Ownership colours: source col_r2.npy (recolour.py + tailcol.py: trunk 1, head 2, L/R arm 4/5, L/R hand 3/12, flap 9, L/R leg 10/11, L/R foot 6-8/13-15, tail 16); cage colours from cagerecol.py / design scripts / tailrecol.py; targets tg_r2m5 (`targets.py col_r2.npy tg_r2m5 5.0 0.7`).
  - Sim: `bsim6.sh TAG CAGE COL tg_r2m5 4 PN <FINALN> 0 2` with FNSMR=0 and FINALN = all colours except 2 → final level Project only on the head. L4 now: self-x 1551 (axilla 842, feet R 289, head 168 (ear horn roots, ear canal mouth), hand R 105, perineum 132); general over 3 mm 0.38 %, head over 1.5 mm 1.24 %.
  - Next: fix the A-class residuals (ear horn folds, hands digit ownership — regenerate hand digit segmentation, feet webs), muzzle/nostrils, then classify L4 self-x A/B with gaps, write the checkpoint or continue; then UI import of the designs (provenance contract) into v007.
- Remaining (pre-session-4 list):
  1. (done) Feet and toes — see RP1E_progress.md "Feet authored in the UI".
  2. (re-scoped 2026-10-19 after the full-body sim, see RP1E_progress.md "Full-body diagnosis after the feet") — the cage misses four cavities/features; each needs explicit topology, designed in the cloud and authored in the UI:
     a. EARS (head identity zone, T-2 max 1.5 mm): the cage has no ear at all (just the head side). Each pinna (helix rim, concha cup ≈ 2.4 cm deep opening forward/laterally, inner ridges; x ±6…20, y −42…−58, z 190–205) needs a sub-cage "bag": base loop round the ear root → outer wall rings → helix rim → inner wall → concha floor cap.
     b. JAW / chin–chest contact (z 173–182, front): ≈ 7 mm deviation; jaw-line loop separating jaw underside from neck/chest.
     c. POUCH (x −9…12, y −22…−55, z 98–115): thin belly flap at z ≈ 99–100 over a pocket; median 12.6 mm deviation; needs a pocket invagination under the flap. (The perineum proper is clean: 0 self-intersections through L2.)
     d. AXILLA front slits (both sides): 1–2 mm pocket, top crease z 141 (back) → 154 (front); needs the arm/trunk junction loop on the crease + explicit slit walls; automatic relayouts failed (see log).
     e. Smaller: lower muzzle front (≈ 4 mm), nostrils (≈ 3 mm).
  3. (merged into 2.)
  4. Hand residual webs and thumb crotches. Also regenerate the hand digit segmentation (segH_R/L, col_full) — lost with the old scratch space; current sims use provisional hand colour 3.
  5. Colour vertex groups col1..col5 and the Shrinkwrap stack. The stack per level is Subsurf → Nearest per colour → 2 × [Smooth → Nearest]; the final level is Project ± 2 cm + Nearest. Feet need their own groups (6/7/8: rest 3, toes 1+3 → 5, toes 2+4 → 4 per col_foot2) whose final level is Nearest + Smooth only (no Project).
  6. Progressive gates at L1–L4 with sim.py, selfx and dev, on the cloud copy of the UI cage.
  7. Save production v002 (never overwrite).
  8. Full gate: T-1/T-2/T-3/T-6/T-7, nails, self-intersections 0, visual sheets.
  9. Gate doc and verdict line; STATUS, queue and handoff; push; close Blender.
- Cloud scratch: /home/claude/stc/rp1e/ (ephemeral; tools are copied to tools/rac/rp/rp1e/).
  - Design cage with the axilla layout: cage_e30.npz. The UI cage vertex indices equal e30 except in the L hand.
  - Check scripts:
    - `blendcage.py -- file.blend out.npz` reads the cage from the staged .blend (run with /home/claude/stc/bin/python3).
    - `selfx.py -- cage.npz out.json` counts self-intersecting face pairs (bpy BVH).
    - `chk.py cur.npz` diffs against the baseline.
- Toe-tube UI notes (feet): Front ortho calibration sx = 598.25 + 10.6·x, sy = 427.5 − 10.6·z (cm) after Top calib + View > Viewpoint > Front; Right view sx = 598.25 + 10.6·(y + 44). When extruding several loops that share K-ring corners, edges between selected corners get implicitly selected and extruded — deselect them in edge mode first (shift-click toggles). Grid Fill works on one closed loop at a time; check Span/Offset against the design.
- UI vertex-move method (proven: 136/136 axilla verts exact):
  1. alt+H.
  2. Front ortho. In N-panel View tab → 3D Cursor, type the region centre.
  3. View → Align View → Center View to Cursor: hover View(128,34) → Align View (160,201) → slide right (300,201) → (313,252).
  4. Scroll zoom about the centre (≈ ×1.2 per notch; 7 notches from Home ≈ 22.1 px/cm). Calibrate by moving the cursor 10 cm and reading its pixel.
  5. Box-drag the region (hidebox2.py picks a box with clear margins), then shift+H.
  6. Check the N-panel Median against the predicted visible-set median.
  7. Switch to the Right, Top or Front view; the centre is kept. View(128,34) → Viewpoint(152,176) → Top(290,193) / Front(288,218) / Right(288,244).
  8. `movegen.py hide.json moves.json cx,cy,ah,av,s hax,vax,hs OUT minsep base.npz` orders clicks by clearance. Then `mk.py OUT a b` prints the batch: per vertex, click, double-click X (1110,92), ctrl+a, keys, Tab, keys, Tab, keys, Return.
  9. Batches of about 16 vertices, ctrl+s, stage, chk.py.
  10. If clearance is under 14 px, click and read the N panel before typing.
- Other UI notes: type digits as key presses (the `type` action is ignored). The Item tab is (1188,70) and the View tab (1188,118). X-ray is on. Delete menu "Only Faces" is about 3 lines below "Faces". Select Non-Manifold remembers its last options (redo-panel checkboxes Boundaries (104,673) and Multiple Faces (104,685)).

## Previous: RAC RP1 Gorrund manual production retopo (2026-10-18) — GATED: FAIL
- RESULT: gate reviews/claude-rac-rp1-gorrund-production-retopo-pilot-gate.md, evidence reviews/rac-rp1-evidence/rp1d/. Candidate E:\...\production\Gorrund\RP1\GO_U_REF_RP1_production_v001.blend (ce35992a…; objects GO_U_REF_RP1_cage 1,810 v + 13-mod stack, GO_U_REF_RP1_prod applied 462,850 v, GO_U_REF_RP1_weldsrc). Cage+stack also in _retopo_v004.blend (212e7508…).
- Fails are all contact/concave zones (fingers/thumb webs, axillae, perineum/pouch, ear cups, under jaw, toe clefts): 193k self-intersecting pairs, hands 14–19 % over T-2 max. Fix path = separating cage loops per contact pair (or separate hand sub-cages), then re-run: rp1_prod_export.py → rp1_gate.py → rp1_selfx.py → rp1_landmarks_len.py (all in tools/rac/rp/; cloud scratch /home/claude/stc/rp1/).
- Do NOT start RP2 / rigging / creator / UE5 until Tyler/ChatGPT decide.

- Order reviews/chatgpt-rac-rp1-gorrund-manual-retopo-execute-order.md (f8aa243); authority reviews/tyler-chatgpt-rac-rp1-gorrund-release-decisions.md (c9d50b8); contract §16 ACCEPTED (5f93e98).
- Method M-B fully manual retopo in the Blender UI (no QuadriFlow/auto-remesh generator). Tolerances T-1 med/p95/max 0.5/1.5/3.0 mm; T-2 identity zones 0.3/0.8/1.5 mm; T-3 stature ±1.0 mm, bbox ±2.0 mm/axis; T-6 landmarks ≤1.0 (none >1.5); T-7 IoU ≥0.995; nails ±0.15 mm. Micro-detail exemption only skin creases + nail micro-edges (list + show). Visual veto absolute.
- Source (read-only, verify sha at entry/exit): ...\Gorrund-Neutral-C\05AW4\GO-05AW4_nails_final.blend 5a4e45d4...2d5e.
- Must repair: L/R hand contact handles (D-1/D-2), left-axilla micro-tunnel (D-3), split-position/perineal seam, tail-root slivers, nail-support density step. Target 1 comp / 0 boundary / 0 nonmanifold / genus 0.
- Checkpoints: RP1-A DONE (bcb2adc; evidence reviews/rac-rp1-evidence/rp1a/, plan RP1A_layout_plan.md). RP1-B trunk/girdle/pelvis/major limbs IN PROGRESS. RP1-C head/hands/feet/tail/identity zones. RP1-D close+cleanup+evidence+gate doc reviews/claude-rac-rp1-gorrund-production-retopo-pilot-gate.md, final line "RP1 Gorrund production-mesh pilot — PASS / CONSTRAIN / FAIL". Then STOP (no RP2/rig/creator/UE5).
- PC output dir E:\UnrealProjects\Wayfarer 5.8\RaceBodies\production\Gorrund\RP1\ : GO_U_REF_RP1_weldsrc_v001.blend (1d7adbe1..., welded 562,265 v, genus 3); _retopo_v002.blend (body cage, superseded); **_retopo_v003.blend = current working file**: weldsrc + cage object "Cylinder" CLOSED genus 0, 1774 v all quads (trunk re-shaped to source sections, head 11 rings + grid cap, tail 14 extrusions, L/R hands = palm+knuckle rings, 4-face knuckle cap, 4 finger tubes + thumb, L/R feet = foot block + sole grid fill), Shrinkwrap Nearest Surface Point -> weldsrc (edit-mode display off). Never overwrite accepted checkpoints; next save as _v004.
- Progress measurement (diagnostic): tools/rac/rp/rp1_ck_export.py (bpy; forces object mode, inserts Subsurf L3 before Shrinkwrap) + rp1_ck_measure.py; runner /home/claude/stc/rp1/ck/run.sh TAG FILESTEM. Evidence reviews/rac-rp1-evidence/rp1b/ (RP1B_progress_measure.md). v003c: general median 0.074 mm, 13.4% >3 mm; tail_root within; hands/feet ~45-55% over T-2 max; head 34.5% over. Gaps: spine groove, elbow backs, groin, toes/nails, heels, ears, nose/mouth/eyes, tail tuft, thenar. Data for finger tracks: /home/claude/stc/rp1/finger_cl2.json; source npz weld.npz (Blender frame cm), weld_a.npz (analysis frame), zones.npz.
- UI lessons: pivot must be Median Point (it once became 3D Cursor -> giant spikes; header pivot menu at (584,34)); select faces by clicking face dots and verify via N-panel Median (zoom region 1040,56-1180,160); View menu Viewpoint: Front (287,216), Bottom (287,203), Right (287,243), Left (287,255); Frame Selected = View(128,34) then (158,105); Undo History = Edit(42,19) -> hover (67,53); extrude chain = e, Escape, g dx Tab dy Tab dz Return (metres), then s/r with typed values; open_application("Blender") launches a NEW instance - don't; click into the Blender window instead.
- Cage placement (Blender m): L leg 14v r0.08 d0.86 loc(0.2148,-0.452,0.5172) rot X2.05 Y-4.65; R leg loc(-0.1856,-0.3891,0.5166) rot X5.68 Y5.19; trunk 24v r0.17 d0.76 loc(0.02,-0.465,1.32), bottom ring deleted; L arm 10v r0.06 d0.387 loc(0.3054,-0.4206,1.3431) rot X-14.39 Y-20.56; R arm d0.412 loc(-0.2925,-0.3715,1.321) rot X-9.85 Y16.21. Loop cuts legs 15, trunk 12, arms 12.
- Remaining: RP1-B joint/support loops (hip, knee, shoulder, elbow, girdle) + save v002; RP1-C neck 24->16 + head (muzzle, orbits, lips, ears rim loops), hands (palm 16, five 6v digits separated), feet (toes, nail inset loops), tail (8-edge hole at emergence 2.3,9.8,104.4 cm; 13 chain stations), axilla; RP1-D Subsurf L3 + Shrinkwrap, cleanup, export, cloud gates (rp1_landmarks.py measure, two-way deviation by zone, IoU, stature/bbox, nails), sheets, gate doc, STATUS/queue/handoff, push; re-verify source sha; close Blender.
- Blender UI notes (4K display, frame 1456x819): `type` is ignored in viewport/search — press keys one by one ("period","minus",digits); `type` works in file-browser fields. ctrl+number in object mode here triggered Select by Type (NOT subsurf) — add modifiers via Add Modifier button (1336,210). View pie = "grave" (Front -66,-42 / Back +64,-42 / Left -82,-2 / Right +82,-2 / Top 0,-64 / Bottom 0,+64 from cursor). X-ray button (1131,35). Outliner weldsrc eye (1438,71). Properties tabs Object (1208,298), Modifiers (1208,314). Add Cylinder redo fields: Vertices (142,580), Radius 592, Depth 604, Cap Fill 617, Loc X/Y/Z 653/664/675, Rot X/Y 686/698 (double-click, ctrl+a, keys, Return). Loop cut: ctrl+r hovering a VERTICAL edge, click, right-click, then Number of Cuts (142,611). Bridge: F3 + keys "bridge" + Return. alt+click loop select; shift+alt add; B box; X delete menu opens at cursor. Apply all transforms ctrl+A > All Transforms (848,431).
- Transfer: device_commit_files limit 30 MB/file and HTTP 400 on stagedPath — SendUserFile first, then commit by fileUuid.

## Previous: RAC RP0 source inventory + production-mesh contract (2026-10-18) — PASS
- Program reviews/chatgpt-rac-retopology-rigprep-master-plan.md; order 54439cb. Report reviews/claude-rac-rp0-source-inventory-contract.md; evidence reviews/rac-rp0-evidence/; contract specs/RAC_PRODUCTION_MESH_CONTRACT.md; RP1 plan reviews/chatgpt-rac-rp1-gorrund-production-retopo-pilot-HOLD.md (HOLD).
- Sources: MPFB family rebuilds via tools/rac/w1/build_variant.py <reviews/reference-assets/builds/X_build.json> {} outdir X (bpy env); Gorrund PC ...\Gorrund-Neutral-C\05AW4\GO-05AW4_nails_final.blend; Saurin PC RaceBodies\out saurin_w2_final_base.npz + _surface_delta.npz via rebuild_w2_final.py (needs libigl).
- RP1 release needs: tolerance acceptance (contract §16), method M-A/M-B. RP1 authoring = Blender UI on Tyler's PC; output RaceBodies\production\Gorrund\RP1\.
- Open for later: Grask E3 asymmetry ruling (RP2), Sagekin c2 central reference, manifest metadata refresh, MPFB-family base topology confirmation (RP3).

## Previous: RAC D4 race-spec stature writeback (2026-10-18) — COMPLETE
- Order b1b001d. Gate reviews/claude-rac-d4-race-spec-stature-writeback-gate.md; evidence reviews/rac-d4-evidence/; tool tools/rac/w1/stagec_drivers/d4_writeback.py.
- One "Accepted stature envelope (RAC D4 writeback)" paragraph per race spec (13), 6 headings relabelled, no other lines changed.
- NEXT: nothing has an executable contract (retopology/rig prep, creator, UE5, posture, equipment, environment, collision, camera). Wait for a new author decision/order.

## Previous: RAC Stage C final closure / writeback (2026-10-18) — STAGE C CLOSED
- Ruling 2619942, order 3e1a3cd. Closure reviews/claude-rac-stage-c-final-closure.md. Grask E3 ACCEPT, Gorrund ACCEPT (reference only), Combined ACCEPT.
- Canon edits: specs/grask/GRASK_V1.md (GR-G1 governing route clause; Durrim non-convergence in Torso depth + Thoracic depth rows; Stage C status block), specs/gorrund/GORRUND_V1.md (closure + Stage C status block).
- NEXT: D4 race-spec stature writeback — entry order reviews/chatgpt-rac-d4-race-spec-stature-writeback-entry-order.md READY, not run; wait for release. Text-only across 13 race specs; register = reviews/claude-rac-rm-ot-05-world-scale-author-gate.md §1; draft = reviews/claude-rac-rm-ot-05-visual-readability-closure-gate.md §6.
- Nothing after D4 has a contract (retopology/rig prep, creator, UE5).

## Previous: RAC Stage C C4.1 Grask resolution (2026-10-18) — AUTHOR RULING REQUIRED
- Order fd23b89. Report reviews/claude-rac-stage-c-c4-1-grask-resolution.md; evidence reviews/rac-stagec-c4-1-evidence/; tool tools/rac/w1/stagec_drivers/c41_gr_g1.py.
- GR-G1 canonical (W1/W2 skeletal_proxy over the skeletal_stations unorganized route, W1h skin-level CIB) PASS ref/N/B = 05B values; Stage C organized failure = S2 level shift (diagnostic).
- Durrim: ARCHITECTURALLY DISTINCT DESPITE DEPTH OVERLAP. Front-only blind read: Grask picked as differently built (medium confidence).
- Recommended: Grask E3 ACCEPT, Gorrund ACCEPT (reference only), Combined ACCEPT. NEXT: wait for the ruling; no D4/UE5/rigging/creator/sculpt.

## Previous: RAC Stage C C0–C4 (2026-10-18) — AUTHOR REVIEW REQUIRED
- Order 5aa5501 (rulings 95e7bc3: D1a Gorrund reference-only, D2c native 204.5 cm with in-memory scaled comparison copies, D3a Grask E3 from frozen GR.E3). Gate reviews/claude-rac-stage-c-gate.md; evidence reviews/rac-stagec-evidence/; protocol specs/RAC_STAGE_C_PROTOCOL.md; tools tools/rac/w1/stagec_drivers/.
- Status: Grask E3 Stage C CONSTRAIN; Gorrund Stage C ACCEPT (reference state only); Combined CONSTRAIN.
- Open author items: GR-G1 protected reading (ruling 2 scope); Durrim directional thoracic-depth row vs accepted E3 keel; E3 absolute-cm organisation across stature; Narrow not shown at elbow/knee; Grask front-view read; Gorrund 204.5 cm below canon min.
- Cloud setup: bpy venv /home/claude/bpyenv (wrapper /home/claude/stc/bin/python3), MPFB 2.0.17 at /home/claude/mpfb2_2017 symlinked into the Blender extensions dir, W1 scratch root symlinked to /home/claude/stc/S; PYTHONPATH=tools/rac/w1 for jbw/s7_station.
- NEXT: wait for the ChatGPT/Tyler ruling. Do not start D4/UE5/rigging/creator/Grask sculpt/Gorrund variants.

## Previous: RM-OT-05AW4 PASS + RM-OT-05AX4 CLOSURE PASS (2026-10-18) — GORRUND CLOSED
- Chain order 38dfda0 (AW4 -> AX4 -> Stage C release). AW4 gate reviews/claude-rac-rm-ot-05aw4-gorrund-final-microfinish-gate.md; AX4 review reviews/claude-rac-rm-ot-05ax4-gorrund-final-closure-review.md.
- FROZEN Gorrund neutral reference: GO-05AW4_nails_final.blend 5a4e45d40158e7dc92f6f8ba13d67ada2403e3e3dcda9048382323ee43a22d5e / .glb e6b325039993b48de1daf1b82da7054c9f466131daf41c2dcc14a0709adb6fc8 (PC ...\Gorrund-Neutral-C\05AW4\). RM-OT-05 CLOSED; Stage C Gorrund blocker CLEARED.
- AW4 technique: plate-edge bevel = Mesh Filter Smooth (one long drag ~33 it) on band 1.4 mm in / 0.8 mm out of outline (tools rmot05aw4_drivers/bevel.py); lesser projection via 2 Hooks AW4_LP/RP, empties 0.35 mm along foot axes (projB.py); freeze.py strips .sculpt_mask (geometry identical); glbexp.py for GLB.
- Stage C release done: STAGE C RELEASED / ENTRY PLAN READY (reviews/claude-rac-stage-c-entry-resolution.md; entry order reviews/chatgpt-rac-stage-c-entry-order.md HOLD; chain note reviews/claude-rac-autonomous-continuation-aw4-status.md).
- NEXT: wait for Tyler/ChatGPT answers to D1 (Gorrund variant method), D2 (204.5 cm sculpt vs 208.3-253 cm stature series / GOREF 230.9), D3 (Grask E3 body source: procedural GR.E3 spec in reviews/rac-rmot05d-evidence/candidates.json, no mesh hash). Then execute the entry order C0-C4.

## Previous: RM-OT-05AW3 — 05AW3 FINAL NAIL FINISH FAILED / AUTHOR REVIEW REQUIRED (2026-10-18)
- Run under autonomous continuation order fd3e67f (AW3 -> AX3 -> Stage C). Chain stopped at AW3 FAIL; status note reviews/claude-rac-autonomous-continuation-status.md.
- PC ...\05AW3\: A f89aa8f2 (side-wall Inflate 0.385 mm), B 5c3dcbe0 (4 Hooks, groups AW3_LP/LD/RP/RD, empties at origin, typed loc LP (0.00020445,-0.00178835,0), RP (-0.00093219,-0.00153981,0), LD/RD z -0.0012; No Falloff), C 1d68c9f5e496ce0076318a96220667040b5a4b467dc380d8c49a8e354823cc78 (candidate; still has mask + AW3 groups).
- Not met: side-wall groove read (plate step wall; skin raise doesn't help -> suggest plate-edge bevel), lesser-toe projection 1.25-1.42 mm (<1.5).
- NEXT: author ruling. If accepted: freeze C as GO-05AW3_nails_final (strip mask/groups, GLB via glbexp), then run 05AX3 HOLD (692ea50), then Stage C release (f659146) per continuation rules.
- Hook technique in UI: Add Modifier (menu opens at Deform; Hook in submenu), set Vertex Group (type filter) then Object, Falloff Type -> No Falloff; apply via header dropdown -> Apply. Empties: shift+A > Empty > Plain Axes, duplicate shift+D + Esc.
- Fit: Surface Smooth 5 short drags = ~10 HC it; Smooth big drag + 14 jiggles = ~37 Laplacian it (higher than the 05AW2 calibration; region-dependent).
- Tools: tools/rac/w1/rmot05aw3_drivers/ (fields, design, stageC, shelf). Cloud work dir /home/claude/aw1/aw3.

## Previous: RM-OT-05AW2 — 05AW2 HIGH-RES TOENAIL REBUILD FAILED / AUTHOR REVIEW REQUIRED (2026-10-18)
- Gate: reviews/claude-rac-rm-ot-05aw2-gorrund-local-subdivision-nail-gate.md. PC ...\Gorrund-Neutral-C\05AW2\: base 20153dae (T + group AW2_subd), subdiv_base 827d9c9c (2 cuts, ngons off, +62 712 verts, 598 717 V / 1 124 538 F), A 9e049052, B b3705d7f, C e07ac7c6, candidate nails_final.blend 75734a39b922f656ecc767b65c0263fa85cfde0e2e35600831b4f9830b1b9206 / .glb 2c7c560cf2f7d84f191309806cdbc17b5e8ea0431f9f3264a3cbc399172d1a09.
- Technical gate fully clean (local-surface fold metric 0; 'inverted vs source' 8 = crevice reference artefacts). Visual: pointed shield nails readable from front; NOT met: projection/curl past toe tip, side walls read as grooves in 3/4. All 4 checkpoints used.
- NEXT: author ruling. If Tyler accepts the candidate as is -> PASS, then run 05AX2 HOLD (d78a928) on GO-05AW2_nails_final, then Stage C HOLD (703dbb6). Otherwise expect an order for one projection/curl checkpoint (masked Grab/Inflate along toe axis, soften side-wall groove).
- Calibrations 05AW2: Smooth ~1.4 it per slow move (0.2 s wait) after big drag (150->500->900->1100 px, jiggle 1100/1105); Surface Smooth ~1.6 HC it per short drag (300->700->1000); Inflate 0.00792 mm/px at strength 0.002 (non-cumulative). Edit > Edge (252,34) > Subdivide (275,94); redo panel cuts (142,635), Create N-Gons (105,660).
- Large file commit via device_commit_files stagedPath can fail (HTTP 400) for ~28 MB: SendUserFile(display attach) then commit by fileUuid.
- Tools: tools/rac/w1/rmot05aw2_drivers/ (aw2gate with AW1_TOPO + AW1_ALLOWNEW=1 env; subsim; repairseeds; stageA4; stageB3; extrarender). Cloud bpy: /home/claude/bpyenv/bin/python.

## Previous: RM-OT-05AW1 — 05AW1 TOENAIL REWORK FAILED / AUTHOR REVIEW REQUIRED (2026-10-18)
- Context: Tyler rejected 05AW nails (f507bf0); 05AX closure SUPERSEDED; RM-OT-05 OPEN; Stage C BLOCKED. Active frozen source = GO-05AV_feet_final (45a04787...).
- Gate: reviews/claude-rac-rm-ot-05aw1-gorrund-toenail-rework-gate.md. PC folder ...\Gorrund-Neutral-C\05AW1\: prep (949d49ea), T (63aa8e74, topology repaired), A (0207bc72, cracks removed, 2 inverted faces), B (d877e426, bump-like sheaths, 3 inverted faces + 81 verts <=0.37 mm outside support).
- Finding: 1.3 mm toe-tip mesh spacing cannot hold a nail outline under the order's local-only ops. Options sent to author: local subdivision of nail supports (2 cuts, sim clean), defer nails to retopology/texture, or AW1-A interim.
- Superseded by 05AW2 (local subdivision authorised).
- Cloud work dir /home/claude/aw1 (ephemeral): aw1lib (AW1_TOPO env = topology npz), stageA4 (masked Smooth + HC), stageB2/B3, aw1gate (topology-aware gate), readvf. Tools copied to tools/rac/w1/rmot05aw1_drivers/.
- New calibrations: Mesh Filter events coalesce; Smooth ~1 iteration per slow (0.25 s) move at large drag distance; Surface Smooth ~1.6 HC iterations per SHORT separate drag (down, 2 moves, up); Inflate strength 0.005 + 152 px = 3.007 mm (non-cumulative, exact). Surface Smooth formula = HC (alpha = Shape Preservation on ORIGINAL, beta = Per Vertex Displacement), matches aw1lib.hc_smooth.
- Topology ops via vertex groups: select group in Data tab (Select button), Edit Mode M > By Distance (set 0.00001 with key presses), X > Dissolve Vertices. Read-back matched cloud bpy simulation exactly.

## Previous: RM-OT-05AX — RM-OT-05 GORRUND FINAL CLOSURE PASS (2026-10-17) [SUPERSEDED by f507bf0]
- Read-only closure review: reviews/claude-rac-rm-ot-05ax-gorrund-final-closure-review.md. Gorrund neutral reference sculpt = GO-05AW_nails_final (AUTHOR-APPROVED / FROZEN). RM-OT-05 CLOSED; Stage C Gorrund blocker CLEARED; Grask E3 may advance per Stage C plan.
- Only open courtesy item: Tyler's visual confirmation of the 05AW toenail look (inherited sunken/split plates; a full rebuild belongs to retopology).
- Downstream debt: 2 hand finger loops + L axilla tunnel (genus 3), perineal duplicate seam, tail-root slivers, optional nail rebuild -> retopology/rig prep.
- NEXT: wait for ChatGPT's next order (likely Stage C / Grask).

## Previous: RM-OT-05AW — TOENAIL REFINEMENT (2026-10-17)
- Active frozen source: `GO-05AW_nails_final.blend` sha bb815843b432042c31eef5424ec55379f8c4bfdf084b5074fed9ab647608784a; `.glb` 082de3c9b51576a89ac3a3a943e49b76637a7ddd8399f7b3bb15caf2ac55dae1 (PC ...\Gorrund-Neutral-C\05AW\) = 05AV + nails.
- Tyler accepted 05AV feet (d8d119f) with toenail exception; 05AW: 8 Hook nail transforms (taper .32, curl 14 deg, +4 mm distal, +3 mm outward). Caveat: inherited sunken/split nail plates; Tyler to confirm look.
- NEXT: RM-OT-05AX final closure review (reviews/chatgpt-rac-rm-ot-05ax-gorrund-final-closure-review-HOLD.md) is now unblocked: read-only review, no geometry authoring.
- Tips: Explorer at E:\Tools\Blender\blender-5.2.2-windows-x64 to launch Blender (blender.exe row). computer_open_application('Blender') spawns a SECOND empty instance - close it. Blender search dropdowns accept typed filters (vertex group 'AW_L1'). Tools: tools/rac/w1/rmot05aw_drivers/.

## Previous: RM-OT-05AV — FOOT/HEEL CORRECTION (2026-10-17)
- Active frozen source now: `GO-05AV_feet_final.blend` sha 45a04787c4760e95b9a9bef52837a516788670f1f1bade92c380ffcea74ab9a6; `.glb` b595f11e2cb4d6f69cdc38954fc9f422dadda9e8e46cee8aed57869face92b4b (PC ...\Gorrund-Neutral-C\05AV\). = AC3 + feet only.
- Feet 34.8 cm / 15.3 cm (17.0 / 7.5 % H), heel lift 0.35 cm L / 0.32 cm R. Head share + tail root approved/frozen (05AU ruling 5cc8df6). Connectivity handles (2 hand loops, L axilla) carried to retopology.
- UI technique that worked: Hook modifier + prepared vertex-group weights (falloff off = exact weighted local transform); add Empty, type loc/rot in Object tab, add Hook (vertex group first, then object; no reset needed), type empty scale/location, Apply in modifier menu. Type numbers with single key presses (ctrl+a, digits, 'period', 'minus').
- Next: ChatGPT/Tyler final Gorrund closure review. Tools: tools/rac/w1/rmot05av_drivers/.

## Previous: RM-OT-05AU — DEFERRED-ITEM AUDIT (2026-10-17)
- Tyler ACCEPTED the 05AT body composition (457c202): BODY COMPOSITION AUTHOR ACCEPTED / FROZEN; overall mesh NOT YET FINAL.
- Frozen active source: `GO-05AT_AC3.blend` sha d462f36c08a3b528aff5b4408539f7dfe704b513585da6f2923136c60b7ea618; `.glb` 8ae6ccedffa5098ceb1fad18583edb18d2243060faf942bec933e79899c9fc0d (PC ...\Gorrund-Neutral-C\05AT\).
- 05AU audit (reviews/claude-rac-rm-ot-05au-gorrund-deferred-item-audit.md): KEEP head share (HH 13.96 % vs W1 11.58 %), KEEP tail root;
  LOCAL heel/foot + foot-size correction recommended (feet 19.1-19.5 % length / 10.6-11.0 % width of H vs W1 15.1 / 5.5 %; heel lift L 0.88, R 1.4-1.6 cm;
  suggested target 16.5-17.5 % / 7-8 % H, pivot at ankle/heel, feet below ~25 cm only); genus 3 = two finger loops + left-axilla tunnel -> topology repair at retopology.
- Next: Tyler/ChatGPT review of 05AU recommendations; expect a bounded feet/heel order. Nothing authored in 05AU; Blender closed.
- W1 reference: GO_r6.npz uses `keep` mask (helper geometry below sole); sole z = 0, vertex stature 230.897 cm. Tools: tools/rac/w1/rmot05au_drivers/ (cloud bpy at /home/claude/bpyenv for renders).
- Key technique (05AT): log-map masks through the Smooth event count, M = 1 + ln(1 - 0.95 w)/N. Tools: tools/rac/w1/rmot05at_drivers/.

## Calibrations (Blender UI)
- Mesh Filter Smooth: each mouse-move event = 1 Laplacian iteration with mask.
- Surface Smooth one 200 px drag ≈ replica f=0.78.
- Mesh Filter Inflate: strength 0.020 with a −100 px drag = −7.92 mm x (1-mask), non-cumulative. Type numbers into Blender fields with single key presses (the type action doesn't land). Real Smooth runs ~1.16x the model.
- Duplicate-position seam vertices (tail root) behave as open boundaries under Smooth: keep a 30 mm mask ramp around them.
- Split duplicate-position seam vertices must carry IDENTICAL mask values (pin to 1.0), or Blender opens the seam.
- Blender is a portable install: it can only be resolved for computer use while running. Launch it from the Explorer window on E:\Tools\Blender (click tier) if closed; computer_open_application starts a NEW instance even when one is running, so avoid it.
- In Blender text fields the computer `type` action sometimes types directly and fails (and can leave the field empty); type file names with single key presses (shift+letter, minus, period) and zoom to verify before saving.
- Computer-use access expires after 30 min idle; re-grant blender.exe + textinputhost.exe.

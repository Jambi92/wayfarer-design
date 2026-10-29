# RAC RP3 — Vael final-consolidation preparation (plan only; NOT executed)

**Date:** 2026-10-28
**Order:** `reviews/chatgpt-rac-rp3-vael-ear-prototype-order.md` §20
**Gates:** `reviews/claude-rac-rp3-vael-ear-prototype-gate.md`; updated by `reviews/claude-rac-rp3-vael-ear-root-integration-gate.md` (root / concha integration, order `chatgpt-rac-rp3-vael-ear-root-integration-order.md` §18)
**Template:** the Aelari final consolidation (`reviews/claude-rac-rp3-aelari-final-freeze-report.md`), adapted to Vael.

This plan is prepared, not executed. Vael is **not frozen**. The next ChatGPT order selects / accepts the ear candidate, requests a bounded refinement, or authorises consolidation / freeze.

## 1. Inputs to consolidate

| Item | Accepted / proposed state | Record |
|---|---|---|
| Body | R1 + VD2 + VF2 (accepted). Sources `VAL4-R1-VD2-VF2` (c1) / `VALF178-R1-VD2-VF2` (c2), CANDIDATE until freeze | `reviews/reference-assets/builds/*-VF2_build.json`, `r6/*-VF2_r6.npz`; VEF1 definition sha b0bf94cf… |
| Face | VC2 (accepted; unchanged since the VC2 lock) | inside the VF2 source build records |
| Ear | **revised VA-E2, root integration RI3** (`ear_branch_lib.CAND['VA-E2-RI3']`: VA-E2 outer geometry unchanged; concha clearance −0.30 cm; skin-hugging cuff) — subject to author acceptance | `reviews/rac-rp3-evidence/vael_rp3_ear_root_integration/VAEL_EAR_root_integration_summary.json` |
| Ear topology | **VAEL_EAR_BRANCH_TOPOLOGY_v002**: local Vael cuff derivative of the Fenn v002 engineering topology (six cuff rings 52 / 56 / 60 / 64 / 66 / 68; sheet, junction ring, 52-vertex root interface and root band unchanged); 59,076 V / 59,074 Q; cuff canon `VAEL_EAR_CUFF_CANON_v001.json` read-only | `…/vael_rp3_ear_root_integration/topology/` |
| Ear engineering settings | `EAR_TOPO=v002`, `EAR_UNT_MODE=contacts`; geo `clear −0.30`, `cuff_skin_r 0.45`, `cuff_skin_w 0.2`, `cuff_skin_root 0.45`, `cuff_skin_slope 1.4` | `tools/rac/rp/vael_rp3_v001/run_va_ri.sh` |
| Family topology elsewhere | MPFB Family Base v005 (frozen, unchanged) | `MPFB_FAMILY_BASE_v005_FREEZE.json` |
| Rig carry-forward | **VAEL-CF-SHOULDER-1** (c1 shoulder flex 90° +6 flips; clavicle-length route / LBS) | `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md` |

## 2. Consolidation steps (mirrors Aelari §4–§23)

1. **Clean rebuild / provenance.**
   - `regen.py` from the committed VF2 build records: geometry identical (max |dV| 0).
   - Full record rebuild (`build_variant`) vs the committed r6: |dV| 0.
   - Native hm08 → propagation onto frozen v005: family realization byte-identical to the reviewed `VA_{M,F}_REF_RP3_bodyfam_v004`.
   - Selected ear (VA-E2-RI3) rebuilt from the committed parameters + the Vael cuff canon + recorded deformation-guard faces: arrays equal the reviewed revision (dV 0).
2. **Production blends** `VA_M_REF_RP3_v001` / `VA_F_REF_RP3_v001`: v005 outside the branch, VF2 + VC2 body / face, selected ear branch; sidecars, hm08 map, branch map, landmarks.
3. **Integrity:** all quads, 1 component, 0 boundary / non-manifold / degenerate, outward normals, 59,076 V / 59,074 Q (Vael local cuff derivative), face-topology hash identical c1 / c2.
4. **Validator D1 + D3 + D4 + D5 + D6:** 69 / 69 on both.
5. **Anatomy / source fit:** T-1 / T-2 / T-3 / T-7, density (9 zones + ear branch < 0.25 %), face rings.
6. **Final body identity (equal height, hidden ear):** human firewall PASS and three-elf firewall PASS re-read on the final bodies.
7. **Pelvis gate 9 / 9** (skeletal proxy, t = 0 / 0.5 / 1.0): MF < Vael < Aelari < Fenn hip ordering, VA-P6, VA-P2b, VA-P3 vertical, VA-P4.
8. **Hidden-ear face:** VC2 systems 6 / 6, elf rows 9 / 9, hidden-ear identity unchanged.
9. **UFCA / expression readiness:** expression sanity unchanged from VD2 / VF2.
10. **Ear final gate (selected candidate):** integrity, T-4 / aspect / min corner, root valence 4 (52 per side), root crease and transition ring, clearance, density.
11. **Visible-ear firewall + projection verification** vs frozen Fenn E2 and frozen Aelari AE-E2 (matched presentation): auricle-body angle, mean / median free-ear and tip stand-off ordering (Fenn > Vael > Aelari).
11b. **Root / concha integration re-read** on the final bodies: one continuous auricle (neutral clay, silhouette, sections), cuff mound / root deviation in the RI3 class.
12. **Body deformation (Standard v1, 18 poses):** 0 new contacts; flips ≤ Marchfolk v005 + 5 except **VAEL-CF-SHOULDER-1** (registered, rig stage).
13. **Ear / head readiness:** 8 poses, 0 / 0 / 0.
14. **Shape probes** (configuration 1): topology intact, intended directions.
15. **Visual package** (final sheets), **production frame / PC read-back** (E: `production/Vael/RP3/`, byte-identical), **freeze record** `VAEL_RP3_FREEZE.json` with `all_gates_pass`.

## 3. Freeze checklist (all must hold before a freeze record is written)

- [ ] Author acceptance of the revised VA-E2 root integration (RI3 recommended) and of the local Vael cuff topology derivative.
- [ ] VF2 body and VC2 face unchanged (immutable hashes equal this gate's list).
- [ ] Clean rebuild dV 0 for source, family realization and ear branch.
- [ ] 69 / 69 D1–D6 on both configurations.
- [ ] Pelvis 9 / 9; human and three-elf firewalls PASS on the final bodies.
- [ ] Ear integrity / quality / root / density / readiness pass on the final bodies.
- [ ] Deformation within family limits except the registered VAEL-CF-SHOULDER-1.
- [ ] Face-topology hash identical across c1 / c2 (VAEL_EAR_BRANCH_TOPOLOGY_v002).
- [ ] Projection ordering verified (auricle-body angle and average lateral stand-off).
- [ ] Production blends written to E: and read back byte-identical.
- [ ] Freeze record + STATUS + handoff committed; STOP for ChatGPT review.

## 4. Not in scope of consolidation

Halvren, creator morphs, production ear rigging, UV / materials, LODs, UE5 integration, low-light physiology. VAEL-CF-SHOULDER-1 stays with the production-rig stage.

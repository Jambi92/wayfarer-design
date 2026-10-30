# Claude Report — RAC RP4 Pipkin Final Author Acceptance / Freeze Closure

**Order:** `reviews/chatgpt-rac-rp4-pipkin-final-author-acceptance-freeze-closure-order.md` (695e2ba)
**Reviewed commit:** `e38a59d9257f8ee3b4ecba0f5805f430d1f85548`
**Date:** 2026-10-30
**Mode:** freeze by record only. No geometry, topology, branch or validator change, and no production file was rebuilt or resaved.

## Final state

**PIPKIN RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

## 1. Freeze record

`reviews/rac-rp4-evidence/pipkin/final/PIPKIN_RP4_FREEZE.json`, promoted from `PIPKIN_RP4_FREEZE_CANDIDATE.json` (the candidate is retained and its sha256 is recorded in `promoted_from`).
- The record is authoritative over the "CANDIDATE / NOT FROZEN" text embedded in both production files.
- **Frozen:**
  - `PK_M_REF_RP4_v001` and `PK_F_REF_RP4_v001`;
  - `MPFB_PIPKIN_COMPACT_BRANCH_v001`;
  - c1 source `PK-NAT` and c2 technical anchor `PKF107-NAT`;
  - accepted bounds `PK91-NAT` / `PK122-NAT`.

## 2. Hashes (all equal the reviewed values; re-verified)

| | PK_M_REF_RP4_v001 | PK_F_REF_RP4_v001 |
|---|---|---|
| file sha256 | `554f1a743b6b1c51c70392ce699ac91d31163699a23ee8034fbd646a31ba6826` | `e64406bb1ca4ac677a86e98ac34b08ec24c334d7fcfc2e7961878f161b5969d3` |
| geometry hash | `1af7d3a818abd8d301234caad03d43c72fa014c50927b977aeb087ef7bd16a5c` | `fd208db6f6bfe98c0226b8d623fe681c5e7ff3a05f603d964a9a500bc65897e5` |

Shared by both references:
- **Face topology:** `a11b8831506519db8ae17ba466540a0cd71faa5d82ca501f53c1fc1d5e3b76dc`. Both have 58,162 V / 58,160 Q (100 % quads), and the c1 / c2 topology is identical.
- **Branch definition:** `ff16400f0ea131bc6709a88427e75c9c5b554545c8d3abe29b48ab93a9572e70`.
- **Branch map:** `2e116576935275ce6ca41565b1cfb444899c63eb9cebdb429dd39c0686aaf7b0`.
- **Landmark files:** the hashes match the candidate record.

## 3. Read-back

I opened both committed `.blend` files fresh in Blender, without saving (`PIPKIN_RP4_freeze_closure_readback.json`):
- the file sha256 and geometry hash equal the reviewed values;
- faces equal the candidate; max |dV| 6e-8 m;
- 1 component;
- 0 boundary edges, 0 non-manifold edges / vertices, 0 degenerate faces;
- normals outward, UVMap present.

## 4. Validator — permanent dual record

| Body | Raw authoritative | Author-adjusted |
|---|---|---|
| PK91-NAT | 65 / 69 | **69 / 69** |
| PK-NAT (c1) | 65 / 69 | **69 / 69** |
| PKF107-NAT (c2) | 69 / 69 | **69 / 69** |
| PK122-NAT | 67 / 69 | **69 / 69** |

**Exception status:** `PASS_PIPKIN_TOE_PROBE_GEOMETRY_EXCEPTION`, preserved exactly.
- **Bodies:** PK91-NAT / PK-NAT / PK122-NAT only.
- **Stations:** `toe3_j1_l/r` and `toe4_j1_l/r` only.
- **Condition:** only the documented raw `FAIL_LOOPS` / closed-ring-fallback / no-crease-pole case, and only where the size-consistent diagnostic passes.

The raw validator outputs stay unchanged in `validator_raw/`. The exception does not change global D4, does not apply to Cogling, and adds no foot topology.

## 5. Immutable verification

`immutable_hashes_freeze_closure.txt`: **58 / 58 unchanged vs e38a59d9**. This covers:
- MPFB Family Base v005;
- the frozen Durrim RP4 branch and its production refs;
- all 11 `*_FREEZE.json` records: Marchfolk, Sagekin, Fenn, Aelari, Vael, Halvren ×3, Grask, v005 and Durrim. Skarn is covered by its family freeze report, because the repo has no separate Skarn freeze JSON;
- the accepted Pipkin sources and the PKF107-NAT anchor;
- the Cogling comparison references;
- the reviewed Pipkin final evidence: production blends, branch maps, landmarks, raw validators, the toe-exception summary and the candidate record.

No frozen race changed.

## 6. Accepted notes (recorded in the freeze JSON)

1. The c1 toe3 / toe4 j1 raw failures are a documented D4 probe-geometry artifact, covered by the Pipkin-specific exception.
2. Global D4 is unchanged.
3. The exception does not apply automatically to Cogling.
4. Pipkin / Durrim, Pipkin / Marchfolk and Pipkin / Cogling separation may stay subtle in neutral clay, because the distinction is anatomical, not caricature.
5. PKF107-NAT is a technical c2 anchor only; Pipkin sex-related anatomy stays OPEN.
6. The extra c2 thumb-opposition contact pairs are the same class: finer-face counts of an existing v005 contact, with 0 unmatched.

**Deformation and anatomy evidence (accepted):**
- c1: 18 / 18 poses identical to v005.
- c2: 17 / 18 identical; thumb opposition is the same-class difference above.
- PK91 / PK122 key poses: identical to v005.
- No new topology class and no new foot / toe defect.
- T-1 / T-2 / T-3 / T-6 / T-7 pass.
- Branch T-4 >4:1 = 0.
- 0 new contact pairs.

**Branch reuse:** `MPFB_PIPKIN_COMPACT_BRANCH_v001` is for Pipkin only and is not a universal compact-race branch. Cogling must be diagnosed independently, and none of these propagate without a Cogling gate:
- thumb placement;
- branch dimensions;
- the toe exception;
- Pipkin source assumptions.

## 7. Status / canon / handoff updates

- **`specs/STATUS.md`:** the top entry is now "PIPKIN RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN", and the READY FOR AUTHOR FREEZE entry is marked superseded.
- **`specs/pipkin/PIPKIN_V1.md`:** new RP4 FINAL STATUS block covering the refs, branch, lineage, hashes, dual validator record, scope, the accepted anatomy (not reopened) and the notes.
- **`specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`:** a Pipkin RP4 section with no carry-forward ID, because no later-stage item belongs there.
- **`reviews/reference-assets/manifest.json`:** a Pipkin RP4 production entry.
- **`reviews/claude-session-handoff.md`:** a LATEST entry.

The PC copy to `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Pipkin/RP4/` happens when the PC is linked.

## 8. STOP

- Pipkin is closed.
- **Cogling is next, but it is NOT started.**
- No geometry, feet, thumb branch or D4 change.
- No Saurin, rig finalization, creator or UE5 work.

**STOP FOR CHATGPT REVIEW.**

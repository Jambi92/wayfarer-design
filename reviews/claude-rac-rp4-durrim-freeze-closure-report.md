# Claude Closure — DURRIM RP4 Final Author Acceptance / Freeze (record only)

**Ruling:** final section of `reviews/chatgpt-rac-rp4-durrim-compact-branch-revision-closure-order.md` (a6b59b5), reviewing d92e677.
**Date:** 2026-10-30

## Result

**DURRIM RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

No geometry or topology was changed. This closure promotes the record and does the bookkeeping.

## 1. Freeze record

`reviews/rac-rp4-evidence/durrim/v002/DURRIM_RP4_FREEZE.json` is promoted from `DURRIM_RP4_FREEZE_CANDIDATE.json` (d92e677). Its contents:
- the reviewed hashes, the ruling, the frozen set, the final counts, the three accepted notes and the scope notes;
- it is authoritative over the "CANDIDATE … NOT frozen" status strings embedded in the production files.

| Item | Reviewed hash | Re-verified at closure |
|---|---|---|
| DU_M_REF_RP4_v001 file | `556793330ea0997a…` | sha256 of the committed blend: equal |
| DU_M geometry | `a6ff9218c9e6c53b…` | Blender read-back (open, no save): equal |
| DU_F_REF_RP4_v001 file | `797b06d7376ef9b4…` | equal |
| DU_F geometry | `7354b28d8836d9d4…` | Blender read-back: equal |
| MPFB_COMPACT_BRANCH_v002 definition | `aef4a30b60d736b7…` | equal |
| face topology, c1 = c2 | `fafdf4ccecbbc4bf…` | equal on both read-backs |

**Read-back (`DURRIM_RP4_freeze_closure_readback.json`), both files:**
- 58,138 V / 58,136 Q, 100 % quads;
- 1 component, 0 boundary / non-manifold / degenerate faces;
- UVMap present, normals outward;
- faces equal to the realization; max |dV| 6e-8 m.

**Immutables:** 26 / 26 unchanged vs a6b59b5. This covers all frozen-race records, v005, the Durrim sources and DUF137C.

## 2. Final counts

- 58,138 vertices / 58,136 quads, with identical c1 / c2 topology.
- Validator 69 / 69 on DU122C, DU137C, DU152C and DUF137C.

## 3. Accepted non-blocking notes (recorded as ruled)

1. Two local jaw–neck quads remain slightly outside the preferred T-4 angle range. They are deformation-clean and have no > 4:1 aspect failure.
2. The c2 thumb / hip diagnostic clearance is narrow but passing.
3. The 152 cm Durrim / Marchfolk visual distinction is intentionally subtle. The W2H / W2H1 source anatomy remains author accepted.

## 4. Scope recorded

- Durrim is the completed RP4 compact-branch pilot.
- `MPFB_COMPACT_BRANCH_v002` is accepted for Durrim and is **not** yet a universal compact-race topology.
- **Pipkin is next** and must be diagnosed independently before inheriting any branch element.

## 5. Bookkeeping updated

- `specs/durrim/DURRIM_V1.md`: RP4 FINAL STATUS block.
- `specs/STATUS.md`.
- `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`: Durrim section, no new carry-forward ID.
- `reviews/reference-assets/manifest.json`: `also` entry.
- `reviews/claude-session-handoff.md`.

**Production files:**
- They are committed in `reviews/rac-rp4-evidence/durrim/v002/production/`.
- The PC copy to `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Durrim/RP4/` is pending, because the PC was not reachable from this session.

## 6. Not done (STOP)

Pipkin, Cogling, Saurin, rig finalization, creator implementation and engine integration were not started.

**STOP FOR CHATGPT REVIEW.**

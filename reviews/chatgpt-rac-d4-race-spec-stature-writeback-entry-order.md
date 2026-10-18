# RAC D4 — race-spec stature writeback: entry order (READY, not run)

**Status:** PREPARED BY CLAUDE under `reviews/chatgpt-rac-stage-c-final-closure-writeback-order.md` §5. The contract is complete and needs no new author choice. Per that order's §6 it is **not run** in the Stage C closure block; it needs a release ("execute") from Tyler / ChatGPT.
**Date:** 2026-10-18.

## 1. Authority

**D4** is defined in `reviews/chatgpt-rac-rm-ot-05-visual-readability-correction-order.md` §9:

> After RM-OT-05 final closure, write the accepted current stature envelopes / statuses back into each race spec so stale "first-pass / provisional" labels do not contradict the accepted W2 / RM-OT-05 state. Preserve explicit qualifiers such as conditional Halvren reach and Gorrund's non-permanent world-validation upper end.

**Preconditions, all met:**

| Precondition | Where it is met |
|---|---|
| RM-OT-05 CLOSED | 05AX4, 977f671 |
| Stage C CLOSED | `reviews/claude-rac-stage-c-final-closure.md` |
| Sagekin configuration-2 bodies accepted | SAGEKIN_V1 L483; RM-OT-05A §2 |
| Cogling CG76H-NAT accepted as the 76 cm body | RM-OT-05A §2; reference-asset manifest |

**Drafted text:** `reviews/claude-rac-rm-ot-05-visual-readability-closure-gate.md` §6.

**Register:** `reviews/claude-rac-rm-ot-05-world-scale-author-gate.md` §1. This is the accepted W2 boundaries table.

## 2. Workstream

Reference anatomy, canon bookkeeping (LS world scale, RM-OT-05). The block is text-only.
- No geometry.
- No new bounds, centres or distributions.
- No UE5, rigging or creator work.

## 3. Scope: one status block per race spec

In every spec:
- the stale "first-pass / provisional" stature label becomes **"accepted W2 / RM-OT-05 envelope"**;
- the original first-pass text is kept as history, annotated rather than deleted.

Frequency stays **OPEN** in every row, and no interval midpoint is treated as an average.

| Race (spec) | Envelope to write | Reference realization | Qualifiers to preserve |
|---|---|---|---|
| Marchfolk `specs/marchfolk/MARCHFOLK_V1.md` | 147–203 cm, both configurations | 173 (MF-M-R / MF-F-R) | — |
| Skarn `specs/skarn/SKARN_V1.md` | 183–229 cm, both configurations | 208, C1R central face | configuration 2 at 229 = macro 1.0 + native extension |
| Sagekin `specs/sagekin/SAGEKIN_V1.md` | 152–208 cm, both configurations | 178 | configuration-2 bounds SGF152-NAT / SGF208 (accepted) |
| Fenn `specs/fenn/FENN_V1.md` | 157–211 cm | 181 (FNL4) | — |
| Aelari `specs/aelari/AELARI_V1.md` | 168–221 cm | 190 (AEL1) | 168 on the native route (R2) |
| Vael `specs/vael/VAEL_V1.md` | 157–203 cm | 178 (VAL4) | — |
| Halvren `specs/halvren/HALVREN_V1.md` | central envelope 152–213 cm | 178 (HVC1) | **Already written back (W2G / W3A1).** Verify only. Ancestry-conditional reach 147.2 / 228.8 / 221.0; tails are minority outcomes; frequency OPEN |
| Durrim `specs/durrim/DURRIM_V1.md` | 122–152 cm | 137 (DU137C, D1 pelvis) | — |
| Grask `specs/grask/GRASK_V1.md` | 198–239 cm | 218. Reference-anatomy direction = **Grask E3 (Stage C ACCEPT)**; W2 GR218R stays a constraint / provenance reference | The old "neutralized-readability FAIL open" note in the §6 draft is **superseded** by the Stage C ACCEPT |
| Gorrund `specs/gorrund/GORRUND_V1.md` | 208–251 cm | 229 nominal / 230.9 ARM (D1 bookkeeping, already in spec) | 251 = current world-validation upper end, **not permanent**. The frozen reference sculpt stands at native 204.5225 cm (Stage C D2(c)): **no envelope revision**, and uniform scaling is never stature construction. The old "neutralized-readability FAIL open" note is **superseded** by RM-OT-05 closure and the Stage C ACCEPT |
| Pipkin `specs/pipkin/PIPKIN_V1.md` | 91–122 cm | 107 (PK-NAT) | — |
| Cogling `specs/cogling/COGLING_V1.md` | 76–107 cm | 91 (CGJ7); 76 cm body = CG76H-NAT | the head ≥ 11.0 cm fix at 76 cm |
| Saurin `specs/saurin/SAURIN_V1.md` | 168–208 cm, tail excluded | 188 | **Already written back (W2I6).** Verify only |

## 4. Allowed and forbidden

**Allowed:**
- text edits to the 13 race specs listed above;
- status lines in `specs/STATUS.md`, the queue and the handoff;
- a gate report.

**Forbidden:**
- any geometry;
- new or changed bounds, references or frequencies;
- stature distributions;
- deleting historical first-pass text;
- changing any other canon;
- UE5, rigging and creator work.

## 5. Gates

1. Every changed number equals the §3 register (cross-check against the world-scale gate §1 and the reference-asset manifest).
2. No other line in a spec changes, other than the status block and the provisional-label annotations (diff audit).
3. The Halvren and Gorrund qualifiers are present verbatim in substance.
4. Halvren and Saurin are verified unchanged unless a stale label exists.

## 6. Return

- Report `reviews/claude-rac-d4-race-spec-stature-writeback-gate.md`, with a per-race diff table.
- Status line: `D4 race-spec stature writeback — COMPLETE / PARTIAL / BLOCKED`.

Then STOP.

## 7. After D4

The repository has **no executable contract** for anything after D4. The following are named only, with no defined block:
- retopology / rig prep, which carries the Gorrund topology debt and the Grask surface constraints;
- creator implementation, which carries the Gorrund deferred variant guarantees and the Grask relationship-aware organization;
- UE5;
- the later-systems items (posture, equipment, environmental scale, collision, camera).

They need an author decision and a new order.

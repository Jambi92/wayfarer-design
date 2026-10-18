# RAC D4 — race-spec stature writeback: gate

**Order:** `reviews/chatgpt-rac-d4-race-spec-stature-writeback-execute-order.md` (b1b001d), running the prepared contract `reviews/chatgpt-rac-d4-race-spec-stature-writeback-entry-order.md`.
**Register:** `reviews/claude-rac-rm-ot-05-world-scale-author-gate.md` §1. Reference assets: `reviews/reference-assets/manifest.json`. Stage C status: `reviews/claude-rac-stage-c-final-closure.md`.
**Executor:** Claude. The block is text-only: no geometry, morphology or relation changed.
**Evidence** (`reviews/rac-d4-evidence/`):
- `d4_specs.diff`: the full spec diff.
- `d4_crosscheck.json`: automated number, diff and qualifier checks.
- Tool: `tools/rac/w1/stagec_drivers/d4_writeback.py`.

## Status

**D4 race-spec stature writeback — COMPLETE**

## Method

Each of the 13 race specs receives **one "Accepted stature envelope (RAC D4 writeback)" paragraph**, inserted directly after its primary stature statement. Each paragraph:
- gives the accepted W2 / RM-OT-05 envelope and reference realization;
- says the first-pass / provisional / preliminary stature labels in that spec are historical and now read as the accepted envelope;
- restates that stature is DIR, never uniform scaling;
- says no midpoint is an average;
- keeps **frequency / distribution OPEN**;
- carries the race's qualifiers.

**Section headings** that carried a "(provisional)" or "(preliminary)" label are relabelled in place. This affects six headings: Skarn, Sagekin, Fenn, Aelari, Vael and the Marchfolk v1.5 "3. Height".

**Historical first-pass text** is kept verbatim (annotated, not deleted).

## Per-race summary and source cross-check

| Race | Envelope written | Reference | Register row match | Spec changes | Race-specific qualifiers carried |
|---|---|---|---|---|---|
| Marchfolk | 147–203 cm (W2A, both configurations) | 173 (MF-M-R / MF-F-R) | ✓ | +1 paragraph (§4–5), 1 heading relabel (v1.5 §3) | both configurations identical |
| Skarn | 183–229 (W2B / W2B1 / W2C1) | 208 (SK, C1R face) | ✓ | +1 paragraph, 1 heading | configuration 2 at 229 = macro 1.0 + native extension |
| Sagekin | 152–208 (W2E, both configurations) | 178 (SG) | ✓ | +1, 1 heading | configuration-2 bounds SGF152-NAT / SGF208 |
| Fenn | 157–211 (W2F) | 181 (FNL4) | ✓ | +1, 1 heading | — |
| Aelari | 168–221 (W2F) | 190 (AEL1) | ✓ | +1, 1 heading | 168 on the native route (R2) |
| Vael | 157–203 (W2F) | 178 (VAL4) | ✓ | +1, 1 heading | — |
| Halvren | central 152–213 (W2G; H-5 outer bound) | 178 (HVC1, diagnostic anchor) | ✓ | +1 (label cleanup only) | **conditional reach 147.2 / 228.8 / 221.0; tails minority (H-6); W3A1 block unchanged** |
| Durrim | 122–152 (W2H / W2H1) | 137 (DU137C, D1 pelvis) | ✓ | +1 | distribution stays OPEN |
| Grask | 198–239 (W2C) | 218. Direction = **Grask E3 (Stage C ACCEPT)**; GR218R = provenance | ✓ | +1 | "neutralized-readability FAIL open" superseded by Stage C |
| Gorrund | 208–251 (W1i / W1j / W2D) | **229 nominal / 230.9 ARM**, kept distinct | ✓ | +1 | **251 = current world-validation upper end, not a permanent maximum**; native 204.5225 cm sculpt is not an envelope revision; FAIL note superseded |
| Pipkin | 91–122 (W2H) | 107 (PK-NAT) | ✓ | +1 | — |
| Cogling | 76–107 (W2H) | 91 (CGJ7) | ✓ | +1 | **76 cm body CG76H-NAT, head 11.04 cm (≥ 11.0 fix)** |
| Saurin | 168–208, tail excluded (W2I D1 regional route; W2I6) | 188 (187.88) | ✓ | +1 (label cleanup only) | no sex shift or sex bound (§263); W2I6 blocks unchanged |

**Number cross-check** (`d4_crosscheck.json`). For every race:
- the envelope and reference parsed from the inserted paragraph equal the register row;
- the register row contains the same three numbers.

13 / 13.

## Qualifier preservation audit

| Qualifier | Present |
|---|---|
| Halvren 147.2 / 228.8 / 221.0, H-6 | ✓ (new paragraph plus the unchanged W3A1 block) |
| Gorrund "not a permanent project-wide maximum", 229 / 230.9 distinct | ✓ (new paragraph plus the unchanged RM-OT-05 bookkeeping block) |
| Gorrund frozen reference sculpt, native 204.5225 cm, D2(c) | ✓ |
| Cogling CG76H-NAT / head ≥ 11.0 cm | ✓ |
| Sagekin SGF152-NAT / SGF208 | ✓ |
| Grask E3 Stage C acceptance | ✓ |
| "frequency / distribution OPEN" and "no interval midpoint is an average" | ✓ 13 / 13 |

## Unrelated-line audit (`d4_specs.diff`)

**Additions.** Across the 13 specs there are 13 new paragraphs plus blank separators. Nothing else was added.

**Removals.** Exactly 6 lines were removed. Each is a section heading replaced by its relabelled form; each spec has at most one.

**Unchanged:**
- no table, bound, reference, relation, morphology, W1/W2 rule, Halvren reach, Saurin W2I6 block or Gorrund bookkeeping line;
- `decisions/`, geometry and tools for bodies.

## State

D4 COMPLETE. The race specs now consistently show the accepted W2 / RM-OT-05 stature envelopes.

**STOP.** The repository has no executable contract beyond D4. The following need a new author decision or order:
- retopology / rig prep;
- creator implementation;
- UE5;
- posture;
- equipment;
- environmental scale;
- collision;
- camera.

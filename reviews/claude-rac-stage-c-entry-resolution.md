# RAC Stage C — release and entry resolution (after 05AX4)

**Order:** `reviews/chatgpt-rac-stage-c-release-after-05ax4-HOLD.md` (3a48492)
**Sequencing:** `reviews/chatgpt-rac-autonomous-continuation-aw4-ax4-stagec-order.md` (38dfda0)
**Precondition met:** `reviews/claude-rac-rm-ot-05ax4-gorrund-final-closure-review.md` returned **RM-OT-05 GORRUND FINAL CLOSURE PASS — 05AX4** (977f671).
**Executor:** Claude. This was a read-only repo reconciliation: no geometry authored, Grask W2 not rerun.

## Return

**STAGE C RELEASED / ENTRY PLAN READY**

STOP. The existing Stage C contract is a scope definition, not an executable block. It also needs three author decisions (§4), so no Stage C validation has been run.

The entry order is committed as `reviews/chatgpt-rac-stage-c-entry-order.md`. It is HOLD until Tyler / ChatGPT answer D1–D3.

## 1. Reconciled state

| Item | State |
|---|---|
| Gorrund neutral reference sculpt | **AUTHOR-APPROVED / FROZEN**: `GO-05AW4_nails_final.blend` `5a4e45d4…2d5e`, `.glb` `e6b32503…6fc8` |
| RM-OT-05 | **CLOSED** (05AX4) |
| Stage C Gorrund blocker | **CLEARED** |
| Stage C | **RELEASED / ENTRY PLAN READY** (not executed) |
| Grask E3 | **FROZEN**; accepted developmental direction, pending Stage C execution |
| Definitive Gorrund lineage | AT AC3 → 05AV → AW1 → AW2 → AW3 → AW4 → AX4 |
| Earlier closure branches | historical / superseded: 05AX (on 05AW), AX1, AX2, AX3 |
| Gorrund downstream debt | retopology / rig prep: 2 hand contact loops, left-axilla micro-tunnel, perineal / duplicate-seam handling, slivers and the nail-support density step |
| D4, UE5, production rigging, creator, class / gameplay, language / story | NOT STARTED (not authorised here) |

## 2. What the existing Stage C contract says

**Definition.** 05D §Stage C (`reviews/chatgpt-rac-rm-ot-05d-true-skeletal-envelope-race-anatomy-order.md` L292-301) defines it, and 05E §9 (`reviews/chatgpt-rac-rm-ot-05e-gorrund-structural-readability-closure-order.md` L329-383) expands it. It is one **combined Grask E3 + Gorrund run**:

1. **§9.1** Freeze both directions for validation.
2. **§9.2** Run the full W2C / W2D validator suites:
   - stature endpoints and internal heights;
   - matched heights;
   - Frame extremes;
   - low / reference / higher composition;
   - protected skeletal relations;
   - clearance guards;
   - roster silhouettes;
   - UFCA / MPFB / ALPC guards.
3. **§9.3** A full-roster matched-scale lineup.
4. **§9.4** An author package with reference, low, Narrow and Broad sheets, and ACCEPT / CONSTRAIN / FAIL per race.

**Additions from later orders:**
- 05F §6 (`reviews/chatgpt-rac-rm-ot-05f-gorrund-hand-sculpt-handoff-stage-c-order.md` L207-213) adds distinctness checks across shared statures, Frame states and composition extremes, in front / 3-4 / profile / rear and body-only silhouettes.
- 05H / 05J add purpose checks (e.g. "do not accept a pair that separates only because one is thin and the other broad") and three status lines: Grask E3 / Gorrund / Combined Stage C.

**Stop rules:**
- Never promote at Stage C; stop for author review.
- No new thresholds. A protocol defect is stopped and reported.

## 3. Why it cannot be executed as-is

1. **Gorrund has no variants.** The contract validates Narrow / Broad, low / high composition and a stature series. The accepted Gorrund is one sculpted body. The scaffold was never derived (05N–05Q), and the LOW was not rebuilt after 05P. The 05 closure audit already flagged that "running Stage C will … need an author decision on how Gorrund variants are derived" (`reviews/claude-rac-rm-ot-05-final-gorrund-acceptance-closure.md` L76).
2. **Stature mismatch.**
   - The frozen sculpt stands **204.52 cm**.
   - The validated Gorrund stature series is 208.3 (true minimum) / 210.8 / 217.0 / 224.1 / **230.9 (GOREF)** / 253.0 cm (W1i, queue L119).
   - So the sculpt sits below the series minimum.
   - 05AU left "final height range" open (`reviews/claude-rac-rm-ot-05au-gorrund-deferred-item-audit.md` L228).
3. **No executable protocol file.** Orders cite "the existing frozen Stage C protocol" (05I L554, 05J L619), but none exists as a file. The W2C / W2D validators were built for procedural bodies (the 05D candidate specs). How they apply to a sculpted mesh is undefined.
4. **No Grask E3 mesh hash.** E3 exists as the procedural spec `GR.E3` (`reviews/rac-rmot05d-evidence/candidates.json`, built at 218 cm), not as a frozen mesh file with a hash.

## 4. Author decisions required (D1–D3)

| # | Decision | Options (no default assumed) |
|---|---|---|
| **D1** | How Gorrund **variants** for Stage C are obtained | (a) Validate the single sculpt as the **reference state only**, with Narrow / Broad / low / high composition **deferred to the creator stage** (Stage C becomes a reference-state validation plus roster read).<br>(b) **Derive** Narrow / Broad / low / high from the sculpt by bounded, author-reviewed deformations (a new derivation block before Stage C).<br>(c) Re-fit the W1i **procedural Gorrund** spec to the sculpt and validate variants on the procedural body, with the sculpt as the visual reference. |
| **D2** | How the **204.5 cm sculpt maps onto the Gorrund stature series** (208.3–253.0 cm; GOREF 230.9) | (a) Treat the sculpt as shape-only and uniformly scale it to GOREF 230.9 cm (scale 1.1290) for roster comparisons.<br>(b) Accept 204.5 cm as a new lower bound / reference, which revises the series (a canon-scale change).<br>(c) Validate the sculpt at its native height, scaled only for matched-height pairs. |
| **D3** | **Grask E3** source for the combined run | (a) Build E3 from the frozen `GR.E3` spec at the existing reference heights (procedural, as in 05D), and record a hash at entry.<br>(b) Supply / commission a sculpted Grask E3 first. |

## 5. Ready next order

`reviews/chatgpt-rac-stage-c-entry-order.md`, prepared and **HOLD**. It specifies:
- exact frozen sources;
- scope (blocks C0–C4);
- allowed and forbidden edits;
- evidence;
- technical gates and visual / canon gates;
- stop conditions;
- state transitions.

Its two variant-dependent blocks are written with branch points keyed to D1–D3, so ChatGPT / Tyler only need to fill in the choices to make it executable.

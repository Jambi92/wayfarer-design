# RAC W2B1 — Skarn Author Ruling and S7 Normalization Order

**Author:** ChatGPT  
**Date:** October 7, 2026  
**Basis:** Claude's RAC W2B1 Skarn 229 cm bounded-correction gate and evidence tables.

## Author ruling

1. **Configuration 1 · 229 cm knee: ACCEPT.**
   - Accept the W2B1 local knee correction at 229 cm.
   - The accepted change is `measure-knee-circ-incr: 1.0 -> removed` and `measure-knee-circ-decr: 0 -> 0.5`.
   - Preserve the 208 cm accepted reference body and all unrelated anatomy.

2. **Configuration 2 · 229 cm body: ACCEPT UNCHANGED.**
   - Do not make an anatomical correction for the reported S7 depth drop.
   - Accept Claude's finding that the discontinuity is produced by vertex-slab sampling rather than a demonstrated body defect.
   - Do not deform otherwise accepted anatomy to satisfy the old S7 sampling artifact.

3. **S7 measurement method: ADOPT EXACT PLANE SECTIONS.**
   - Replace the tessellation-sensitive S7 vertex-slab reading with the exact mesh-plane section method demonstrated in W2B1.
   - Treat this as measurement normalization, not anatomical redesign.

## Next block — bounded S7 normalization

Before final Skarn W2 closure, run one bounded bookkeeping/regression block across **W1, W2A, and W2B/W2B1** for every S7 row whose value depends on the old vertex-slab method.

Required work:
- Recompute applicable S7 breadth/depth readings with the exact-plane method.
- Re-run the affected S7 evaluation rows, including the existing evaluation states that depend on those readings.
- Preserve all accepted bodies during this measurement pass.
- Do not alter anatomy merely because a recorded S7 value changes.
- Record old value, normalized value, result, and whether any authored relationship changes status.
- Confirm the Skarn 229 cm configuration-2 continuity result under the normalized method.
- Confirm Skarn-vs-Marchfolk S7 relationships and relevant frame/comparator relationships remain valid.
- Identify any historical W1/W2A/W2B result that changes status.

If the normalized method exposes a genuine authored relationship failure, stop and report it for author ruling. Do not silently correct a body.

## Scope limits

- Measurement/bookkeeping block only.
- No new population work.
- No unrelated body retuning.
- No creator-envelope expansion.
- No UE5 implementation.

## Return gate

Return a concise **S7 Normalization / Skarn W2 Final Acceptance Gate** containing:
- normalization coverage;
- changed S7 values/results;
- regression summary;
- any genuine contradiction, if found;
- proposed final Skarn W2 disposition.

Then **STOP for author ruling** before starting the next W2 population.

# RAC RP1E — RESUME EXECUTION: finish M1, then M2–M6, D masks, nails, and v014 final gate

**Date:** 2026-10-20  
**Authority:** Tyler direct instruction via ChatGPT: resume work now.  
**Execution state:** latest Claude handoff `b7c2b8e1d781d48918fd04942a053c909a7e58ca`.  
**Governing order:** `reviews/chatgpt-rac-rp1e-v014-m1-slit-band-and-manifold-closure-order.md` (913d0e4).

## 1. Direct instruction

**RESUME EXECUTION NOW.**

Do not wait for another author message.

The prior order remains in force. This file is an explicit continuation signal and resolves any ambiguity created by the session handoff.

Continue from the exact session-12 state in `reviews/claude-session-handoff.md`.

Do not write another progress-only checkpoint unless a hard tool/safety interruption prevents execution.

## 2. Immediate M1 action

Use the current best slit-band work under:

`reviews/rac-rp1e-evidence/exp_v018_m1slit/`

Current best facts:
- continuous B/C slit-band topology exists;
- genus 1;
- 0 coarse self-x;
- L1 regional self-x = 0;
- best L4 regional self-x reduced from 843 to **10**;
- explicit B/C wall masks exist;
- per-wall final remap improved regional deviation to ~1.52 mm but still crossed at the sub-mm wedge.

### Execute Attempt B now

The next authorized production interpretation is:

> Once the source B/C slit narrows below production-resolvable thickness, terminate the two production walls onto one shared manifold crease **slightly mouthward of the mathematical zero-gap tip**, at the earliest traced section where the opposing source gap is approximately **0.5–0.7 mm**.

This is explicitly authorized if all of the following remain true:
- visible through-slit is preserved;
- exterior silhouette is unchanged to visual review;
- hand T-2 max <= 1.5 mm;
- no artificial thick block/web is created;
- the shared crease remains inside the frozen source's sub-mm convergence wedge;
- regional L1 self-x = 0;
- regional L4 self-x = 0.

This is a production representation of a sub-face-scale taper, not an anatomy redesign.

Try the current planned ~0.6 mm-gap crease first.

## 3. M1 remap fallback — execute without asking

If Attempt B is L1-clean but does not reach L4 regional self-x = 0:

Use the already-authorized explicit **per-wall final-resolution remap**.

Requirements:
- B wall remaps only to `Rhand_B_wall_source_faces`;
- C wall remaps only to `Rhand_C_wall_source_faces`;
- shared crease vertices remain one shared vertex chain;
- fusion continuation remaps only to fused exterior source faces;
- fix the 14–15 unlocated remap vertices using deterministic boundary-arc matching;
- no disk mapping may span both slit walls.

After remap:
- regional self-x = 0;
- hand T-2 <= 1.5 mm;
- visible slit preserved;
- genus 1;
- no boundary/non-manifold geometry.

If this succeeds, M1 is PASS.

## 4. M1 bounded stop

Only stop at M1 if both:
1. the ~0.6 mm shared-crease slit-band solution; and
2. the explicit per-wall final-resolution fallback

fail to achieve zero regional self-intersections while meeting T-2 and preserving the visible slit.

If both fail, return exactly:

**RP1E R-HAND VISIBLE HANDLE BLOCKED / AUTHOR DECISION REQUIRED**

with the required evidence.

Otherwise continue automatically.

## 5. After M1 passes — do not wait

Immediately execute M2–M6 from order 913d0e4:

### M2 — R thumb web
- rebuild whole local web patch;
- explicit palm/thumb source-side masks;
- finite-thickness portion remains two-sided;
- sub-face taper ends in shared manifold rim;
- direct final-resolution local patch fallback authorized;
- require regional self-x = 0 and T-2 pass.

### M3 — L axilla
- preserve visible knob, pinch mouth and z153 surface;
- do not enter hidden D void;
- finite gaps stay open;
- true zero-gap terminates as shared crease;
- regional self-x = 0.

### M4 — ear rims
- explicit source-side masks;
- shared manifold rim edge;
- no normal-sign ownership;
- regional self-x = 0;
- head T-2 pass.

### M5 — philtrum / upper lip / nose folds
- open finite slots remain open;
- zero-width crease becomes shared manifold edge;
- no overlapping production sheets;
- preserve muzzle identity.

### M6 — remaining exposed Class-A defects
- R axilla A tip;
- natal-cleft nub;
- L palm crease;
- R ulnar web;
- exposed toe/rim folds;
- any other visible/open Class-A residual found by the final classification.

Do not reopen passing regions without a measured reason.

## 6. Explicit D masks

After M1–M6 geometry is clean:

Build exactly two frozen D masks:
1. hidden L-hand tunnel interior;
2. hidden L-axilla void interior.

Use seeded source-face flood fill with explicit throat boundary loops.

Do not use beam-width visibility thresholds.

Do not include visible mouths, rims, slit walls or silhouette surfaces.

Freeze:
- source face ids;
- source vertex ids;
- boundary-loop ids;
- area/share;
- section screenshots/evidence.

No third D mask without a new author ruling.

## 7. Nails — execute the repair

Use the recovered nail tooling already proved equivalent to historical source measurements within <=0.003 mm.

Repair the seven failing nails by local free-edge support only.

Required:
- all 8 nails within ±0.15 mm;
- no global toe/foot/finger length change;
- preserve taper/curl/silhouette;
- no new self-x;
- relevant T-2 zones remain passing.

Do not stop merely because the current v013 nails fail; the repair is authorized.

## 8. T-6 is settled

Use the already-accepted implementation:
- hip connected-curve selection;
- exact radius-circle segment clipping;
- unchanged tolerance.

Do not reopen the T-6 method.

Re-run it on the final candidate.

## 9. Build and promote v014

Once M1–M6, D masks and nails are integrated:

Freeze:
- `reviews/rac-rp1e-evidence/designs/design_v014.npz`
- `design_v014_col.npy`
- `design_v014_info.json`
- explicit source-side masks
- D masks
- nail support metadata
- final-resolution patch provenance, if used.

Then import through the normal Blender UI as:

`GO_U_REF_RP1E_retopo_v014.blend`

Do not overwrite v013.

Verify import provenance <= 0.10 mm and exact intended topology.

## 10. Final v014 production gate

Required:

### Topology
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 1;
- 0 degenerates;
- quad-dominant;
- **0 production self-intersections**.

### Production-envelope T-1
- median <= 0.5 mm;
- p95 <= 1.5 mm;
- max <= 3.0 mm.

### Production-envelope T-2
- median <= 0.3 mm;
- p95 <= 0.8 mm;
- max <= 1.5 mm.

Also report raw full-source T-1/T-2.

### T-3
Unchanged.

### T-6
Target <=1.0 mm; none >1.5 mm; report >1.0.

### T-7
>=0.995.

### Nails
8/8 within ±0.15 mm.

### Visual veto
Unchanged.

## 11. Final return only

Do not stop for intermediate approval once M1 passes.

Return one substantive result:

### PASS
**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

### D-mask-only review
**RP1E EXTERIOR PRODUCTION MESH PASS / D-MASK AUTHOR REVIEW REQUIRED**

### Hard geometry block
**RP1E POST-M1 LOCAL FEATURE BLOCKED / AUTHOR DECISION REQUIRED**

or, if M1 itself fails both authorized routes:

**RP1E R-HAND VISIBLE HANDLE BLOCKED / AUTHOR DECISION REQUIRED**

Do not return a routine checkpoint/handoff as the answer to this execution order unless forced by a tool/safety interruption.

## 12. Scope

No RP2.
No rigging.
No creator implementation.
No UE5 production implementation.

## 13. Return file

`reviews/claude-rac-rp1e-v014-resume-execution-gate.md`

Update the normal RP1E evidence, handoff, and STATUS only with the substantive result.

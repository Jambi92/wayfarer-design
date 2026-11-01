# ChatGPT Order — Saurin RP5 Continue Option B / Validate Fold Census / Work Until PASS

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Latest internal WIP commit:** `25d8b9423550714cad06e89c55aa5066c7a1b13c`  
**Parent:** `reviews/chatgpt-rac-rp5-saurin-option-b-fold-census-closure-order.md`  
**Standing rule:** `reviews/chatgpt-claude-internal-audit-pass-before-submission-directive.md`

## Immediate instruction

Resume work now.

Do not wait for another ChatGPT order merely because the current fold census is ambiguous.

First determine whether the apparent web / palm / forefoot fold counts are:
1. true cage topology defects; or
2. false positives from the current fold-census measurement method.

Then continue Option B accordingly.

---

# 1. Validate the fold census before more topology changes

The current census uses:
- nearest source face to the quad centroid for inversion;
- one diagonal-derived quad normal for concavity / bow-tie classification.

This may be invalid in narrow two-sided web slots.

Rebuild the audit so every cage quad is evaluated against its own source correspondence.

Preferred source reference hierarchy:

1. barycentric host faces of the quad's four cage vertices;
2. host-face normals interpolated at the corresponding source points;
3. local source patch / tangent estimate derived only from those hosts;
4. nearest-face fallback only when host correspondence is unavailable.

Do not classify a quad against the opposite wall of a web slot.

---

# 2. New authoritative fold tests

For every quad outside allowed tip caps compute separately:

## Orientation / inversion
Compare the cage quad orientation against the orientation of its own mapped source patch.

Use:
- vertex host triangles;
- mapped corner order;
- robust average/source-patch normal.

A quad is inverted only if its mapped orientation is truly reversed relative to its own source patch.

## Self-cross / bow-tie
Use a true quad self-crossing test:
- project to a stable local tangent plane;
- test crossing of opposite edges;
- do not infer bow-tie solely from a non-planar diagonal normal.

## Concavity
Measure signed corner turns in the same local tangent plane.

Distinguish:
- valid non-planar convex quad;
- concave quad;
- bow-tie / self-crossing quad.

Record method and numerical tolerance.

---

# 3. Visual verification of the audit

Before accepting the new census:

Render closeups from both outside and inside the narrow slots for:

- all finger webs;
- all toe webs;
- palm reduction rows;
- forefoot reduction rows;
- thumb base;
- orbit fan;
- wrist transition;
- ankle transition.

Overlay:
- quad IDs;
- source host triangles;
- orientation flags;
- concave / bow-tie flags.

Manually inspect a deterministic sample from:
- every flagged structure;
- every structure that changed classification between old and new census.

If the old audit produced false positives, record them explicitly.

---

# 4. Fold-census ruling logic

After the corrected audit:

## If most flagged web quads were false positives
Keep Option B local density and proceed with only the genuinely defective quads.

Do not redesign clean topology to satisfy a bad validator.

## If genuine folds remain
Continue local structural refinement under the existing Option B authorization.

Allowed:
- local re-phasing;
- web-row placement;
- block parameterization;
- local source-patch mapping;
- controlled 2:1 transition redesign;
- local quad split / merge patterns within the Option B hand/foot regions;
- local edge rotation where manifold quad structure and semantic loops remain valid.

Do not propagate loops through the whole body.

---

# 5. Option B remains the author decision

Option B is still approved.

Do not revert to:
- Option A whole-body loops;
- Option C accepted residual folds.

The local hand/foot density architecture remains the intended production direction unless a genuinely new architecture impossibility is proven.

---

# 6. Continue automatically after audit validation

Once the corrected fold census is trustworthy, continue internally without waiting for another order.

Close:

- thumb residuals;
- finger webs;
- toe webs;
- palm reduction rows;
- forefoot reduction rows;
- wrist transition;
- ankle transition;
- orbit residuals;
- shoulder / vault residuals;
- any remaining genuine non-tip fold.

---

# 7. Final Saurin T-4 rule

Use the corrected host-aware census as the authoritative fold component of T-4.

Outside true finger / toe / tail tip caps require:

- 0 true inverted quads;
- 0 true bow-tie quads;
- 0 true concave quads in deformation-critical topology;
- aspect <= 4 outside explicit tip exemptions;
- no collapsed / zero-area edges;
- bounded angle residuals only where anatomically harmless and individually documented.

---

# 8. Rerun all remaining closure work

After topology passes:

1. full T-1 through T-7 on c1/c2;
2. deformation four-step ownership audit;
3. PD-2 creator-state ownership;
4. head creator states;
5. layered detail on c1/c2 + at least one creator state;
6. direct identity metrics;
7. updated semantic map;
8. final A–P boards;
9. immutable verification;
10. pilot .blend exports + read-back.

Final pilot names:
- `SA_M_REF_RP5_pilot_v001`
- `SA_F_REF_RP5_pilot_v001`

Status:
**PILOT / NOT FROZEN**

---

# 9. Internal submission rule

Do not stop and wait again for ordinary technical choices already covered by this order.

Keep iterating internally until one of:

## PASS
**SAURIN RP5 FULL AUTHORED CAGE PASS — READY FOR CHATGPT / AUTHOR REVIEW**

## Genuine author decision
Only if a new issue would require changing:
- canon;
- accepted production tolerance;
- Option B architecture scope;
- accepted tail-module architecture;
- shared c1/c2 topology policy.

## External blocker
Only if a required source/tool/permission is unavailable.

Do not submit another NEEDS REVISION gate for normal fixable topology/audit work.

---

# 10. Stop boundaries

Do not:
- freeze Saurin;
- alter canonical W2I6 source files;
- alter accepted Saurin biology;
- start final rigging;
- start final UV/material production;
- start LOD production;
- start creator implementation;
- start UE5 integration;
- start another race.

Resume work now and continue until internal PASS / genuine author decision / external blocker.

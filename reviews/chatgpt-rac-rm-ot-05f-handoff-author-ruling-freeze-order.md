# RAC RM-OT-05F — author ruling / handoff freeze / external sculpt wait order

**Authority:** author decision following review of `reviews/claude-rac-rm-ot-05f-gorrund-hand-sculpt-handoff-gate.md`  
**Status:** EXECUTE. This is a closure-and-freeze order for the handoff package, not authorization to invent another procedural Gorrund body.

## 1. Author decision

Accept RM-OT-05F as a successful **HANDOFF READY** stage exactly in the limited sense reported by Claude.

The following statuses are now authoritative:

- **RM-OT-05 remains OPEN.**
- **Grask E3 remains the accepted developmental race-anatomy direction pending Stage C.**
- **Gorrund remains unaccepted.**
- **Gorrund status: EXTERNAL SCULPT REQUIRED — AWAITING ASSET.**
- **Stage C remains blocked until a genuine direct/external Gorrund sculpt passes re-entry and the replicated blind gate.**
- **No D4.**
- **No UE5 implementation.**
- **No canon promotion.**
- **No reopening of the 05C–05E procedural search.**

Do not reinterpret HANDOFF READY as acceptance of any 05C, 05D or 05E Gorrund candidate. P1, P2, P3, E1, E2 and every other failed/provisional Gorrund body remain unpromoted.

## 2. Q1 author ruling — APPROVED

Approve the reconciliation already written in the 05F production brief for hard-form family A.

The intended Gorrund trunk may use:

- broad planar anatomical zones;
- strong but radiused plane breaks;
- a legible sternal/anterior plate;
- legible lateral thoracic planes;
- an anatomically organized hard-form section.

It may **not** become:

- rectangular;
- boxy;
- mechanically slab-sided;
- circular/cylindrical.

The controlling interpretation is:

> Planar anatomical zones and plane breaks are allowed and desired, but they must exist on an anatomically shaped, radiused thoracic cross-section. “Planar” describes surface organization, not a rectangular body section.

This is an interpretation of existing Gorrund canon, not new canon.

## 3. Required waist-language correction

Patch the 05F handoff package anywhere the wording could imply that “no waist hollow” is a permanent race-wide biological invariant.

The author ruling is:

> The **reference sculpt** must not rely on a human-style pinched waist or waist hollow as the Gorrund readability cue. Existing canon-valid waist variation remains available through the established Frame/composition system. Do not encode “no waist hollow” as an invariant Gorrund biological rule.

Therefore:

- preserve the reference-direction goal of avoiding a human pinched-waist read;
- preserve canon-valid waist variation through Frame/composition;
- do not create a race-wide prohibition on all waist hollowing;
- do not change the Frame/composition system to enforce an absolute waist shape.

Apply this correction to the production brief, sculptor checklist, silhouette/view targets, or other 05F text wherever needed.

## 4. Freeze the 05F handoff package

After the Q1 and waist-language corrections:

1. Freeze the RM-OT-05F production brief and handoff package for external/direct sculpt production.
2. Do not alter the six hard-form family intents unless a genuine conflict with locked canon is later demonstrated.
3. Do not relax any existing technical validator threshold.
4. Do not use `arch_sculpt.py`, `race_base.py`, or derivative procedural tuning to manufacture a substitute “hand sculpt.”
5. Do not create another procedural Gorrund candidate series.
6. Do not use bulk, obesity, muscle amount, posture, crouch, hunch, digitigrade illusion, oversized extremities, texture, pigmentation, clothing, hair or face as a workaround for body-only race readability.
7. Treat the region map only as an editing-jurisdiction guide. The production-brief text governs anatomy.

## 5. Grask freeze

Grask E3 remains the accepted **developmental race-anatomy direction pending Stage C**.

- Keep the demonstrated E3 organization frozen.
- Do not reopen the Grask search.
- Do not promote it beyond its current status.
- Do not borrow Grask-specific signature cues as the Gorrund solution.

In particular, do not collapse the two races by reusing Grask's distinctive scapular/hump, high-calf/long-cord, or other accepted Grask structural identity.

## 6. Gorrund external asset contract

The expected return asset remains the existing 05F contract:

- file: `GO_sculpt_<ID>_r6.obj`;
- base: `reviews/rac-rmot05f-handoff/template/GO_ref_route_r6.obj`;
- identical base topology and vertex order;
- R-6 neutral stance;
- protected/no-touch zones unchanged within the existing tolerance;
- no true-floor violation;
- six hard-form families expressed structurally;
- no topology, skeleton, stature-route, joint-centre, long-bone, plantigrade, digit-count, Frame/composition or rig-compatibility rewrite.

Do not create a placeholder “accepted” Gorrund body while this asset is absent.

## 7. Re-entry sequence remains unchanged

When a genuine sculpt is supplied, run the existing 05F pipeline exactly as already specified:

`python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_<ID>_r6.obj <ID>`

Only after re-entry passes:

1. run the replicated blind gate;
2. use the existing scorer prompt and mechanical tally;
3. require every existing blind-gate condition;
4. require Gorrund to read as a distinct humanoid race/species at reference and low composition;
5. require explanations to cite structural organization rather than body bulk;
6. require both axial and limb cues;
7. require stable distinction from both human-family controls and Grask E3.

Do not weaken the gate to obtain a pass.

## 8. Stage C remains blocked

Do not run combined Stage C until a genuine Gorrund sculpt has:

1. passed every technical re-entry guard; and
2. passed the replicated blind structural-readability gate.

If and only if that occurs, Stage C may use:

- Grask E3 as the frozen developmental Grask direction; and
- the newly accepted Gorrund sculpt.

Until then, record the dependency and stop.

## 9. Required repository updates for this order

Make only the changes necessary to capture the rulings above.

At minimum:

- patch `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md` for the approved Q1 interpretation and corrected waist language;
- update status/tracking text so Gorrund is explicitly **EXTERNAL SCULPT REQUIRED — AWAITING ASSET** and RM-OT-05 remains OPEN;
- preserve Grask E3's current developmental status;
- create a concise response report:
  `reviews/claude-rac-rm-ot-05f-handoff-author-ruling-closure.md`

The response report must list:
- exact files changed;
- confirmation that Q1 was applied;
- confirmation that the waist wording was corrected without changing canon;
- confirmation that the handoff package is frozen;
- confirmation that no new procedural Gorrund body was generated;
- confirmation that Stage C remains blocked;
- the exact external asset filename/base expected on re-entry.

Do not edit race canon files unless this order reveals an actual contradiction that cannot be resolved by wording correction. If that happens, stop and report it rather than silently changing canon.

## 10. Stop condition

After the repository updates in §9 are complete, **STOP**.

Do not continue into a new morphology stage while the required genuine Gorrund sculpt is absent.

The next action after this closure is external/direct sculpt production and delivery of `GO_sculpt_<ID>_r6.obj`.

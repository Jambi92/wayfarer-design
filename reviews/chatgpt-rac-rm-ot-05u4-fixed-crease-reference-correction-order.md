# RAC RM-OT-05U4 — fix the crease reference and readiness result; no production sculpt

**Authority:** Tyler requested these next instructions after the independent review of 05U3.
**Parent:** `12723d4` (05U3 verification readiness).

## 1. Audit finding

The independent review reproduced the existing baseline measurements exactly:

| Section | Baseline depth (cm) | Recorded 75% minimum (cm) |
|---|---|---|
| A, S3 vertex 61581 | 0.8951 | 0.6713 |
| B, S3 vertex 61580 | 0.3658 | 0.2743 |

The attached crease plot matches the committed image. The proposal scope and protection-preview hashes remain consistent. No production mutation is indicated by the 05U3 commit.

**Remaining defect:** `u3_crease.measure` derives `s0` and section selection from `V[v]` of the mesh being measured. `check_return_u2.sh` calls it on the returned mesh. Both named vertices are editable, so an allowed sculpt can move the measurement planes and change the reference chords. Comparing that depth to the frozen baseline is not a same-location comparison.

Independent disposable-array reproduction: moving vertex 61581 by 0.02 cm along the arm axis moves section A from s0 9.0357 to 9.0557 cm. The same probe on vertex 61580 moves B from 10.4628 to 10.4828 cm. This demonstrates reference drift; it does not claim that a particular flattened repair has passed.

## 2. Freeze a reproducible reference from the unchanged 05U baseline

Correct the additive U2 measurement path. Derive the references once from the pinned, unchanged 05U RETURN, then use those same references for every fixture and eventual return:

- the frame origin, axis, section plane positions and normal;
- baseline selection anchors, the intended section component and the region entry/exit boundary-edge identities;
- chord endpoints, direction, inward sign and depth definition;
- full-precision depths and 75% thresholds, with rounded values used for display only.

Persist a versioned, machine-readable reference artifact with the baseline mesh/return hashes, proposal hashes and index convention. Validate it on every measurement. The return must not supply or silently regenerate its own reference.

Intersect the returned geometry with the frozen planes. Use the frozen anchors and expected boundary-edge correspondence to identify each run; never choose it from a moved editable vertex. Confirm that its endpoints still agree with the frozen chord as required by exact boundary protection. Specify any numerical tolerance for intersection computations separately from the bit-exact vertex-protection rule.

If the reference is missing, mismatched, non-finite, ambiguous, or has unexpected entry/exit geometry, report an explicit failed measurement. Do not substitute another nearby section, use a moving chord, relax the threshold or change the proposal region.

The existing baseline values should reproduce under the fixed definition. If they differ materially, explain and resolve the cause before declaring readiness; do not silently replace them. Preserve the old outputs as historical evidence and identify their moving-plane limitation.

## 3. Add focused disposable regression tests

Test and commit evidence for:

1. Unchanged 05U baseline: same section locations, chords and depths, both limits pass.
2. Move each named editable vertex along the arm axis, separately, including the demonstrated +0.02 cm case. The measurement planes, reference anchors, chords and thresholds must remain invariant, though measured depth may change.
3. A synthetic allowed-region flattening that crosses a fixed 75% depth limit: explicit FAIL at the same fixed section, with no relocating the plane to recover a pass. This is a validator fixture, not a sculpt or candidate.
4. Ambiguous/missing section data, invalid reference hashes and non-finite measurements: explicit failed measurement/readiness, with no pass inferred from omitted results.
5. The two named sections cannot be swapped, omitted or truncated without failure; compare by identity, not an unchecked `zip` of lists.

Also retain the 13 existing protection probes and default-path regression checks. The original 05T/05U behavior and V2–V6c criteria must remain unchanged.

## 4. Make the result unambiguous

The current shell path prints a crease PASS/FAIL without making a failed depth check fail the command. Add a machine-readable aggregate result separating:

- protection/reintegration verdict;
- fixed-reference depth checks for A and B;
- roughness and sliver guards;
- geometry-gate results and their unresolved statuses;
- pending author visual review and desktop fixtures.

A failed, missing or ambiguous mandatory depth/roughness/sliver/protection check must prevent a numerical-stop-conditions PASS and return a nonzero status. Preserve diagnostic outputs, renders and hashes where feasible even on failure. Do not equate ACCEPTED_FOR_VERIFICATION_U2 with satisfaction of the stop conditions or author acceptance.

The unchanged 05U baseline is expected to pass protection/depth but fail the roughness target. That expected baseline failure must remain visible. Distinguish a successful verification-tool regression suite from a baseline or candidate meeting sculpt targets. Preserve the disclosed V4/V6c failures; do not waive them to manufacture an aggregate pass.

## 5. Deliver and stop

Commit `reviews/claude-rac-rm-ot-05u4-fixed-crease-reference-readiness.md`, the additive correction, immutable reference artifact, focused regression evidence and updated readiness/status pointers. Report the exact results and any remaining blocker.

This authorizes tool correction, read-only baseline measurement and disposable validator fixtures only. Keep the 35-face / 15-added-vertex boundary unchanged. Do not alter the production handoff, masks, face sets, source master, 05U RETURN or released ZIP; do not sculpt or build an anatomical candidate.

**STOP FOR READINESS REVIEW AND TYLER'S BOUNDARY/METHOD APPROVAL.** A corrected checker does not itself authorize the revision. Real desktop mask/brush/protection fixtures remain required after approval and before production strokes.

Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED; reconstructed skin INFERRED. No canon promotion, D4, UE5, production rigging or creator implementation.

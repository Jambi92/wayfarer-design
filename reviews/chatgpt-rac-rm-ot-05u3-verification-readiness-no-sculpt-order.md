# RAC RM-OT-05U3 — complete verification readiness; no production sculpt

**Authority:** Tyler requested the next instructions following the independent review of the 05U2 proposal.
**Parent:** `53fd98fd582dcbd2fd8996964d0a8ef996d48474`.
**Baseline:** verified 05U RETURN and its existing release; preserve both unchanged.

## 1. Review finding and authority boundary

The proposal's scope is independently verified: 35 source faces, 15 additional editable source vertices, 11.05 cm², 365 total editable vertices and a 106-vertex frozen boundary. Its lists and protection-preview hashes reproduce; the three supplied images match the committed images. The boundary appears appropriately localized and is recommended for Tyler's decision.

This order authorizes verification-tool development, disposable technical fixtures, read-only measurements and a readiness addendum. It does **not** approve the proposed boundary for production, authorize a production brush stroke, or accept Gorrund.

Keep the 05U RETURN, release, source master, production scene, production masks, face sets and active protection rules unchanged. Test-only copies and opt-in proposal sets must be clearly marked non-production. Do not build an anatomical candidate or perform a repair.

## 2. Implement a working opt-in verification path

The current `s_verify.py` does not recognize P05U2: an unknown `--prot_faces` value falls through to the older P set, and its source-coordinate check also requires an explicit approved-exception design. Do not present the proposed command as already executable.

Implement an additive, explicitly selected U2 test path or adapter that:

- loads the exact proposed lists and validates reference mesh, baseline, index convention and all relevant hashes;
- derives the 365 editable vertices, 106 frozen vertices and 832 editable faces, checking them against the approved-proposal preview rather than trusting arbitrary supplied counts;
- checks every vertex outside those 365 bit-exactly against the frozen 05U baseline, including all 106 frozen-boundary vertices;
- checks every face outside those 832 for preserved vertex identity and orientation;
- enforces the proposed no-topology-change production method; identity IDs alone must never authorize moved protected vertices;
- evaluates P05U2 source protection using its actual source-face index list, 139,772 faces and committed coordinate hash;
- retains full provenance for the 15 source vertices and 35 source faces; do not erase source correspondence merely to make V1 pass;
- reports the new inferred-source label separately from the original labels and accounts for it in every relevant consumer;
- retains the existing default 05T/05U behavior, verification code and thresholds. Run historical regression checks to demonstrate this.

Keep the V2–V6c mathematical criteria, thresholds and verdict rules unchanged. If an adapter must reorder faces, expose the mapping and show that the new region is included in geometry-quality checks; do not obtain a pass by excluding the 35 added faces or the changed source vertices.

Report the original V1 faithfully. If its face-prefix assumption is no longer applicable to the U2 layout, report that limitation explicitly and add a correspondence-aware legacy diagnostic. Do not label an incompatible invocation as meaningful evidence.

## 3. Correct the legacy-check expectation

Replace the proposal's requirement that original V1 must fail on exactly all 35 faces and all 15 vertices.

The lists define the **maximum authorized region**, not a quota of elements that must change. Some or all of them may remain untouched. Any source displacement or affected protected-source face detected by the legacy diagnostic must be confined to the authorized lists. Enumerate actual changed vertices and affected faces, with no changes outside the authorized region. Report the original verdict and the new U2 protection verdict separately.

## 4. Demonstrate the contract on disposable fixtures

Before any future production authorization, show:

- unchanged 05U baseline accepted with identical reconstructed coordinates, topology and correspondence; distinguish expected metadata/label changes from geometry equality;
- a synthetic test edit to an allowed added source vertex accepted;
- an edit just outside the proposed boundary rejected;
- a moved new frozen-boundary vertex rejected;
- a moved retained old frozen-boundary vertex rejected;
- a missing/reversed protected face and a spoofed identity claim rejected;
- mismatched or altered proposal lists/hashes rejected;
- historical 05T/05U protection behavior unchanged.

Synthetic fixture edits are validator probes only, never an anatomical repair or candidate. Store them separately from production and label results accordingly. Do not claim these probes substitute for the real desktop mask/brush fixtures required after production-boundary approval.

## 5. Define and measure crease depth now

The proposed 75% crease-depth limit needs reproducible baseline measurements before anyone can use it.

On the unchanged 05U baseline, record the two sections near S3 vertices 61581 and 61580. Define the exact section planes and coordinate frame, section-selection rule, frozen-ring endpoints/chord, deepest-point selection and units. Use mesh/plane intersections or another reproducible method; do not rely on a rendered pixel estimate or an undefined sample band.

Supply the actual baseline depths in centimetres, the resulting 75% lower limits, machine-readable measurements and annotated section plots. If the proposed boundary does not yield unambiguous endpoints, revise the measurement definition and explain it before seeking approval. Do not invent values or adjust the baseline after a future sculpt.

Explain how these depth checks, the source p95 roughness limit and visual judgement will be used together. Passing a roughness statistic alone does not establish natural anatomy.

## 6. Deliver the readiness addendum and stop

Commit:

- `reviews/claude-rac-rm-ot-05u3-verification-readiness.md`;
- additive tools and clearly labelled fixture evidence;
- the corrected verification-contract language in the 05U2 proposal, preserving the historical finding;
- exact crease-depth baselines and section evidence;
- status/queue pointers saying **VERIFICATION READINESS REVIEW / BOUNDARY AWAITING AUTHOR APPROVAL**, without claiming production approval.

Summarize what passes, what remains unresolved, and the exact boundary/method/verification contract Tyler would be approving. Keep the proposed lists and scope unchanged. If implementation exposes a required scope change, report it as a proposal rather than applying it.

**STOP before changing the production handoff or performing any sculpt.** Tyler must approve the concrete production boundary and method first. Real desktop protection fixtures are still required after that approval and before production strokes.

Gorrund remains UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED; reconstructed skin INFERRED. No canon promotion, D4, UE5, production rigging or creator implementation. The unresolved V6c-1 crease, V4 taper edges and anterior V6c-2 failure remain disclosed, unwaived and outside this repair scope.

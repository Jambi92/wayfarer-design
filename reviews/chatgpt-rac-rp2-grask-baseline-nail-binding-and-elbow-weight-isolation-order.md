# RAC RP2 — Grask baseline retention, nail binding and elbow weight isolation

**Date:** 2026-10-26  
**Authority:** Tyler requested these instructions through ChatGPT following review of return `9703fd2`.  
**Parent report:** `reviews/claude-rac-rp2-grask-diagnostic-deformation-failure-isolation-gate.md`.

## 1. Decisions on the return

- Retain **W0** as the diagnostic baseline. Reject W1 and W2 for adoption; preserve them as experiment history. W2's 12/43 passing poses do not improve W0's 20/43.
- Accept the qualified conclusion that weights, placement and skinning contribute, while topology remains unproven as either adequate or limiting under the failed poses. Do not reopen frozen retopology.
- Accept bounded landmark v003 knees **for diagnostic use only**, including the disclosed 2.75/0.83 mm residual from the section centres. The 5 mm total-displacement cap takes priority over exact section-centre coincidence for this diagnostic candidate.
- Retain v002 hip and GH centres as diagnostic baselines. Alternative centres remain comparison evidence only.
- AD-R2's ankle rule specified a section-centreline placement without a 5 mm cap. The disclosed 11.0/9.9 mm displacement is permitted for diagnostic use only; it does not establish biological accuracy or final placement.
- Keep shoulder/girdle policy unresolved. Preserve prior pure-GH and fixed-20-degree girdle tests as historical diagnostic settings. No new shoulder mechanics or elevation experiments in this order.
- Reject blanket acceptance of persistent crease compression as expected anatomy. The existing failures require evidence, not exemptions.

## 2. Immutable assets and scope

Grask RP2 retopology remains **AUTHOR ACCEPTED / FROZEN / CLOSED**.

Verify before and after all work:

- v003 blend SHA-256 `03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0`, geometry `f9c4a7ac98e86d98017376b9d67c85428503d2d6385258471d99bc766bfe702f`;
- v005 source SHA-256 `7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14`, geometry `2697929d90c9ed708997a594502a4d5edeaebb8f4ae39deefcc0802dc7c1d7bc`.

Stop on any mismatch. Preserve frozen parents, sidecars, landmarks, freeze record, provenance, loop tags, seam proposal, thumb-web anatomy, accepted quad exception, diagnostic v001/v002 and W0/W1/W2 records. New diagnostic copies only; never overwrite them. Read-back rest geometry must equal frozen v003.

No geometry, rest-shape or skeleton-architecture edits; no corrective shapes, helper bones, production weights, facial/oral work, morphs, UVs, materials, LODs, UE5 work or another race.

## 3. Nail-only candidate — WN

Create **WN = W0 plus nail binding only**. Reuse the documented distal-cap selection, inspect it visually, and record exact vertex IDs, distal-bone assignment and weight deltas. If the selection includes surrounding skin incorrectly, report and correct the selection with explicit evidence before binding; do not enlarge it to hide bending.

All weights outside the nail selection must remain bit-identical to W0. Normalize selected vertices only. No wrist, palm, thumb-base or region-transition edits in WN.

Run W0 and WN through the same original 43-pose suite using the same v002 diagnostic pivots, matrices, poses and metric implementation. This isolates nail binding and preserves comparability with 9703fd2; these comparison runs do not approve the former unrestricted knees.

Report nail residuals, surrounding-skin artifacts, every changed criterion and any regression. Adoption requires demonstrated nail rigidity improvement without new failures elsewhere; creating the file alone is not success. Preserve both arrays and their hashes.

## 4. One-region experiment — left elbow only

Use W0, or WN if its nail-only comparison supports adoption, as the parent. Keep the elbow pivot, skeleton, geometry and poses fixed. Author at most **two** new left-elbow diagnostic weight candidates, separately from WN.

Use a connected elbow/upper-arm/forearm support region with a continuous blend back into the unchanged baseline. The change must taper to zero across a documented boundary band. Do not repeat a hard region cutoff followed by smoothing only inside it. Preserve normalization and nonnegative weights, intended segment influences and all weights outside the support region.

Show the boundary band, individual bone maps, total weight-delta maps and the maximum per-edge change in weight delta across its boundary. Explain how continuity was enforced. A smooth-looking colour map alone does not establish acceptable posed deformation.

Test reference, 45/90/130-degree elbow flexion and extension back to rest, with the same disclosed shoulder-abduction setup. Compare LBS and DQS with identical weight arrays. Include a small shoulder/wrist/finger sentinel set to expose leakage or regressions. Select by geometric integrity and visual quality across poses, not volume proxy alone. Retain the baseline if neither candidate improves it.

If a candidate is selected for carry-forward, rerun the original 43-pose suite and report all regressions. Keep the landmark version fixed within every weight comparison. Separately verify the selected configuration with the accepted-for-diagnostics v003 knees and explicitly report that landmark difference; do not merge pivot effects into weight-effect claims.

Do not tune shoulder, hip, knee, wrist or thumb weights in this cycle. Do not iterate beyond two elbow candidates. Return even if neither succeeds.

## 5. Metric and evidence policy

Preserve historical pass/fail tables and thresholds. Continue reporting the skinned-reference-normal orientation disagreement, but label it accurately rather than calling it proven face inversion.

Report neighbour-normal opposition separately as a **local fold/inversion indicator**, not definitive proof of inversion: a sharply bent but valid surface can disagree with adjacent normals. For representative flagged faces show indexed wireframe, triangulation/area, adjacent faces, and intersections from multiple views. Identify what is demonstrated versus suspected.

Keep the open-patch cone-volume measurement as a historical proxy, with its sensitivity disclosed; do not call it tissue volume or adopt a weight set based on it alone. Retain rigid-transform sanity checks. Keep original contact masks and classifications; no enlarged masks, relaxed criteria or retroactive pass relabelling.

Provide identical-camera baseline/WN/elbow-candidate clay and wireframe sheets with failure IDs and boundary overlays. Show nail closeups in fist and pinch. Show elbow outer contour and inner crease at 90/130 degrees, including actual penetration and loop compression. Distinguish expected proximity from demonstrated penetration.

## 6. Return and stop

Commit `reviews/claude-rac-rp2-grask-nail-binding-elbow-weight-isolation-gate.md` with evidence under `reviews/rac-rp2-evidence/grask_rig_diagnostic_v003/`:

1. parent hashes before/after and new derived asset manifests/read-back hashes;
2. WN selection and bit-identity checks outside the nails;
3. versioned weight arrays, edit logs, boundary-continuity checks and reproducible runs;
4. nail-only full-suite comparison and elbow candidate comparisons, including rejected candidates;
5. full-suite regression check for any selected elbow candidate;
6. visual evidence, qualified conclusions and precise remaining decisions.

Any new blend should use a new version, e.g. `GR_U_REF_RP2_rigdiag_v003.blend`, and record exactly which landmark and weight versions it contains. It is a diagnostic artifact, never a frozen production rig.

Update STATUS/handoff narrowly: **retopology frozen; nail/elbow diagnostic review pending; production deformation not accepted**.

After this bounded cycle is committed, **STOP FOR CHATGPT REVIEW** and return the commit hash and key sheets. Do not advance to broader joint corrections, corrective-shape authoring, final rigging or a new race.

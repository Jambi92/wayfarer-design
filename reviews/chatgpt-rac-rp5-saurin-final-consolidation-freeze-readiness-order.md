# ChatGPT Order — Saurin RP5 Final Consolidation / Freeze-Readiness Pass

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Approved authored-cage submission:** `2ee75ae1845a223f3c8b8b9a5abfa10608f06b27`  
**Approved gate:** `reviews/claude-rac-rp5-saurin-full-authored-cage-gate.md`  
**Standing rule:** `reviews/chatgpt-claude-internal-audit-pass-before-submission-directive.md`

## Immediate instruction

Proceed with the **Saurin RP5 final consolidation / freeze-readiness pass**.

The authored Option B cage at commit `2ee75ae1845a223f3c8b8b9a5abfa10608f06b27` is **author approved for consolidation**.

This is **NOT** permission to freeze Saurin.

Work through this order internally. Do not submit ordinary intermediate checkpoints. Submit only when your own final consolidation audit reaches PASS, unless a genuine author decision or external blocker is encountered.

At the end, stop for ChatGPT / author review.

---

# 1. Lock the approved geometry as the consolidation source

The approved source is the cage and supporting state represented by the PASS gate at `2ee75ae...`.

Approved authored cage:

- `SA_RP5_full_cage_optionb_final.npz`
- 190,948 vertices
- 190,946 quads
- 100% quads
- one closed, consistently oriented manifold
- identical c1/c2 topology and vertex order
- accepted tail module unchanged
- canonical W2I6 source unchanged

Treat this geometry as **locked for the purposes of this pass**.

Do not perform opportunistic topology cleanup, smoothing, re-seating, re-parameterisation, angle chasing, density changes, semantic-loop changes, or identity edits.

The purpose of this pass is consolidation, reproducibility, package integrity, and freeze readiness — not another geometry-development cycle.

If a clean rebuild does not reproduce the approved state, diagnose the mismatch before changing anything. A discrepancy that cannot be reconciled without changing approved geometry is an author-review condition.

---

# 2. Preserve the accepted documented residuals

The following are accepted non-blocking residuals and are not instructions for additional repair.

## T-4 angle residual register

Preserve the complete existing `SA_T4_angle_residuals.csv` / `.json` register.

Current approved status includes:

- c1: 65 quads outside the 45–135° quality target, 0.034%
- c2: 166 quads outside the target, 0.087%
- all registered residuals remain correctly oriented
- all registered residuals remain convex
- all have acceptable aspect
- deformation testing is clean for the affected topology

The strong c1 examples already documented include:

- quad 2049 — trunk / sacral flank
- quad 54957 — xneg axilla
- quad 83708 — xneg thumb base
- quad 85405 — xneg palm 2:1 row

Do **not** force these angles back into the target band if doing so reintroduces concavity, folding, bow-ties, or worsens the topology.

## T-6

Preserve the approved reported T-6 result:

- c1 maximum landmark deviation: approximately 1.03 mm
- c2 maximum landmark deviation: approximately 1.02 mm
- PASS under the established tool rule
- below the previously established 1.5 mm hard ceiling

Do not alter approved identity merely to chase the nominal 1.0 mm quality target.

---

# 3. Create a clean consolidation workspace

Create a clean final-consolidation area under the Saurin RP5 evidence tree.

Recommended location:

`reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation/`

Keep the existing `optionb_final/` evidence immutable.

The consolidation directory should contain only the files needed to prove that the approved cage can be rebuilt, serialized, read back, and promoted as a production candidate without changing its approved content.

Do not delete or rewrite the original approved evidence.

---

# 4. Clean rebuild from the approved authored inputs

Perform a clean rebuild using the approved scripts, authored design data, accepted source assets, and accepted tail module.

The rebuild must not depend on undocumented manual edits.

Record:

- exact source commit
- exact tool/script paths
- Python / Blender versions where relevant
- deterministic seeds or parameters
- input hashes
- output hashes
- cage vertex count
- cage quad count
- topology hash
- semantic-map hash
- c1/c2 shared-topology result
- tail-module verification
- canonical-source immutable verification

Compare the clean rebuild against the approved `SA_RP5_full_cage_optionb_final.npz`.

Require:

- same vertex count
- same quad count
- same face list / topology hash
- same semantic ownership
- accepted tail module unchanged
- canonical W2I6 source unchanged

For geometry values, prefer exact reproduction. If serialization or tool-version behavior produces only insignificant floating-point differences, quantify them explicitly and prove they are numerically immaterial and do not alter any gate result.

Do not silently accept a mismatch.

---

# 5. Re-run the freeze-readiness validation gates

On the clean consolidation candidate, rerun the decisive validation set.

At minimum:

1. topology / manifold / orientation verification
2. c1/c2 shared face-list and vertex-order verification
3. T-1 through T-7
4. host-aware fold census
5. aspect / collapsed-edge checks
6. angle residual register comparison
7. deformation ownership audit
8. PD-2 creator-state ownership audit
9. direct identity metrics
10. semantic-map verification
11. accepted-tail verification
12. immutable canonical-source verification

Expected approved baseline includes:

- 0 inverted non-tip quads
- 0 bow-tie non-tip quads
- 0 concave non-tip quads
- 0 concave deformation-critical quads
- 0 aspect > 4 outside approved tip/tail exemptions
- 0 topology-classified deformation poses
- 0 topology-only flips
- 0 cage-owned creator-state flips

Any regression from the approved PASS state is a failure of consolidation and must be diagnosed internally before submission.

---

# 6. Pilot-to-freeze-candidate conversion

Create new candidate files from the approved cage.

Use explicit **FREEZE CANDIDATE / NOT FROZEN** status.

Recommended names:

- `SA_M_REF_RP5_freeze_candidate_v001.blend`
- `SA_F_REF_RP5_freeze_candidate_v001.blend`
- `SA_RP5_full_cage_freeze_candidate_v001.npz`
- `SA_RP5_freeze_candidate_v001_barycentric_map.npz`
- `SA_RP5_freeze_candidate_v001_sidecar.json`

The existing pilot files remain historical evidence and should not be overwritten.

Candidate files must preserve:

- identical approved cage geometry
- identical topology
- identical c1/c2 shared face list
- identical semantic data
- accepted tail module
- approved source correspondence / barycentric data
- documented residual register
- provenance back to `2ee75ae...`

Do not label any file `FROZEN`, `FINAL FROZEN`, or equivalent.

---

# 7. Blender read-back verification

Open / load each new freeze-candidate Blender file through a clean read-back verification path.

For both male and female candidates, record:

- object presence and expected names
- vertex count
- quad count
- face-list identity
- vertex-order identity
- semantic attribute identity
- topology hash
- source/cage provenance
- maximum vertex read-back error
- transform state
- unit / scale state
- modifier state
- hidden or accidental objects
- external dependency status

The file must not rely on missing external data to reconstruct the approved cage.

No accidental unapplied modifier, scale, transform, geometry node, shape key, or scene object may alter the approved cage on load.

If non-destructive metadata/support objects are present, document them.

---

# 8. Final evidence consolidation

Create a concise final freeze-readiness report that points to the already-approved detailed evidence rather than duplicating unnecessary material.

The report must clearly state:

- approved source commit: `2ee75ae...`
- clean rebuild result
- rebuild-vs-approved comparison
- final hashes
- candidate file names and hashes
- T-1 through T-7 status
- host-aware fold census status
- deformation ownership result
- PD-2 creator-state ownership result
- identity result
- semantic verification
- tail verification
- canonical immutable verification
- accepted angle residuals
- accepted T-6 residual
- Blender read-back result
- production-copy status
- final internal verdict

Include a compact manifest listing every file intended to become part of the frozen RP5 package.

---

# 9. Production-folder copy

If an established Saurin / Race Production production-candidate directory already exists and is clearly intended for freeze candidates, copy the candidate package there **without overwriting any previously frozen production asset**.

If no unambiguous production location exists, keep the candidate package in the review/evidence tree and report:

`PRODUCTION COPY DEFERRED — NO UNAMBIGUOUS APPROVED DESTINATION`

Do not invent a new production convention merely to satisfy this step.

Do not replace a frozen or canonical asset.

---

# 10. Freeze-candidate record

Create a freeze-candidate record that includes at minimum:

- race: Saurin
- stage: RP5
- architecture: Option B local hand/foot density
- source approval commit: `2ee75ae...`
- cage SHA-256
- topology SHA-256
- male candidate SHA-256
- female candidate SHA-256
- semantic-map SHA-256
- barycentric-map SHA-256
- accepted tail-module SHA-256
- canonical immutable verification result
- accepted residual references
- full gate result
- date / commit of candidate generation
- status: **FREEZE CANDIDATE / NOT FROZEN**

This record must make it possible to issue the later freeze authorization without ambiguity about exactly which artifacts are being frozen.

---

# 11. Internal audit before submission

Follow the standing internal-audit-before-submission directive.

Do not return merely because the files were copied or exported.

Before submission, independently verify the entire candidate package from the files on disk / repository state, not only from in-memory tool results.

Your final internal gate must confirm:

## Geometry identity
- approved cage geometry preserved
- topology hash preserved
- c1/c2 topology preserved

## Quality
- T-1 through T-7 still pass
- host-aware census still passes
- accepted residuals unchanged and explicitly carried forward

## Ownership
- deformation audit has no topology regression
- PD-2 has no cage-owned regression

## Package integrity
- candidate Blender files read back correctly
- manifests / sidecars match the actual files
- hashes are current
- no missing package dependency
- no accidental canonical modification

## Freeze safety
- nothing is marked frozen
- no frozen/canonical production asset was overwritten
- no prohibited downstream work was started

Continue fixing consolidation/package problems internally until this audit passes.

---

# 12. Submission state

When and only when the internal audit passes, submit:

## **SAURIN RP5 FINAL CONSOLIDATION PASS — READY FOR FINAL FREEZE REVIEW**

The submission should contain the final consolidation report, manifest, candidate hashes, and the exact commit containing the freeze candidates.

Then **STOP**.

Wait for ChatGPT / author review and an explicit freeze authorization.

---

# 13. Genuine author-decision conditions

Stop before PASS only if one of these occurs:

- the approved `2ee75ae...` cage cannot be cleanly reproduced without changing approved geometry;
- a mismatch indicates the approved evidence is internally inconsistent;
- an established production destination conflicts with an existing frozen/canonical asset;
- freezing would require changing canon, topology policy, accepted residual tolerance, or accepted Saurin identity;
- a required source/tool/permission is unavailable.

Do not request an author decision for ordinary packaging, scripting, hash, serialization, report, or read-back issues that can be resolved without changing the approved asset.

---

# 14. Stop boundaries

Do **not**:

- freeze Saurin;
- rename candidate files as frozen;
- create a final freeze authorization yourself;
- alter the approved authored cage geometry;
- alter canonical W2I6 source files;
- alter accepted Saurin biology;
- alter the accepted tail module;
- alter the approved Option B architecture;
- start final rigging;
- start final UV/material production;
- start LOD production;
- start creator implementation;
- start UE5 integration;
- start another race.

Proceed now with final consolidation and freeze-readiness work.

Work internally until your own audit reaches PASS, then submit **SAURIN RP5 FINAL CONSOLIDATION PASS — READY FOR FINAL FREEZE REVIEW** and stop.

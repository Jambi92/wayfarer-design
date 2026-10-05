# ChatGPT — Reference Anatomy Wave 1 Execution Order

**Author:** ChatGPT (design author)  
**For:** Claude (measurement auditor / reference-anatomy agent)  
**Status:** BEGIN WAVE 1 — ARM CANDIDATE ACCEPTANCE + CENTRAL MEASUREMENT  
**Authority:** `decisions/REFERENCE_ANATOMY_V1.md`, canonical race specs, PROJECT_RULES, UFCA, UCCA  
**Scope:** Reference anatomy only. NO UE5 IMPLEMENTATION.

## 1. Objective

Execute the RAC Wave 1 manifest. Establish the central quantitative reference layer for all 13 playable populations without allowing candidate assets, builders, solvers, generators, or measurements to silently author biology.

Wave 1 target remains **15 bodies + 1 Marchfolk diagnostic head variant**.

This order authorizes:
- inspection and validation of existing candidate reference geometry where available;
- preparation/specification of purpose-built ARM candidates where required;
- ARM acceptance records;
- measurement of accepted ARMs;
- diagnostic-envelope derivation;
- cross-race consistency auditing.

This order does **not** authorize UE5 implementation, runtime character systems, production rigging, skeleton architecture, animation, morph systems, equipment fitting, gameplay balancing, or automatic canonization of measured values.

## 2. Resolve the Cogling head-dimension ambiguity before measurement

Claude identified one new OPEN question: Cogling “roughly 11–13 cm” head size does not state whether the dimension is height or length.

**Author resolution W1-A1:** interpret the existing 11–13 cm statement as **anatomical head height**, measured from the inferior chin/mandibular landmark to skull vertex, excluding hair/presentation.

Rationale: the statement functions as a body-scale/head-share constraint; vertical head height is the appropriate dimension for that relationship. This does not authorize a separate player-facing Head Height slider. Cranial length/depth remain independently governed by Cogling anatomy and measurement.

Canonicalize this clarification minimally in the Cogling spec and measurement queue before using the value.

## 3. Mandatory execution sequence

### W1-00 — Preflight / provenance audit
Before measuring anything:
1. verify current canonical status of REFERENCE_ANATOMY_V1 and RMQ;
2. verify the 15-body + 1-head manifest;
3. inventory actual candidate files/assets available to the shared workflow;
4. distinguish:
   - accessible measurable geometry;
   - accessible but noncompliant candidate geometry;
   - referenced asset not actually accessible;
   - purpose-built candidate required;
5. create a provenance record for every candidate.

**Do not claim an asset was measured unless its actual geometry was accessible and inspected.**

If the necessary geometry is not accessible through the repository/current connected file sources, do not fabricate measurements. Produce the exact build/ingest requirement and continue with every other executable item.

### W1-01 — Saurin RM-CF-01
The manifest allows this first because it has no biological dependency.

Candidate:
- male-centre closure reference aff1b52;
- female-centre candidate only as specified in REFERENCE_ANATOMY_V1 and the manifest.

Tasks:
- establish whether actual aff1b52 geometry is accessible;
- run ARM §6 acceptance if accessible;
- if accepted, measure FPI and required coupling corners for RM-CF-01;
- compare against the provisional rostral floor;
- record diagnostic results only;
- do not alter the Saurin floor without later author acceptance.

If the geometry is unavailable, record **BLOCKED ON ASSET ACCESS**, not a numeric result.

### W1-02 — Marchfolk human baseline
This is the primary dependency for cross-race measurement.

Bodies:
1. Marchfolk 173 cm configuration 1;
2. Marchfolk 173 cm configuration 2;
3. MF-FACE-PROJ-MAX diagnostic head.

For each existing Iteration 3 Marchfolk candidate:
- confirm actual asset availability;
- re-pose/normalize to R-6 only if doing so does not alter anatomy;
- run R-1…R-14 and §6 acceptance;
- explicitly list every builder-chosen value;
- accept/reject each candidate on biological grounds.

If accepted, run:
- RM-UB-07 central portion;
- Marchfolk sides of RM-LR-01 / 05 / 07;
- Marchfolk side of RM-OT-01;
- RM-CF-02 central;
- RM-UF-01 Marchfolk.

For MF-FACE-PROJ-MAX:
- build/specify a purpose-built diagnostic head from canonical Marchfolk anatomy;
- validate “most-projecting valid adult human face” without muzzle-like/nonhuman maxilla;
- measure only after acceptance.

### W1-03 — Remaining central ARMs
Proceed in this order so dependencies become available early:

1. Skarn — 208 cm
2. Sagekin — 178 cm
3. Fenn — 181 cm
4. Aelari — 190 cm
5. Vael — 178 cm
6. Halvren — 178 cm no-lineage general envelope
7. Durrim — 137 cm
8. Grask — 218 cm
9. Gorrund — 229 cm
10. Pipkin — 107 cm
11. Cogling — 91 cm
12. Saurin female centre — 188 cm, tail excluded from stature

Use the exact configuration/reference state and validation requirements in `reviews/claude-rac-wave1-execution-manifest.md`.

For each:
- locate existing geometry if any;
- never use non-Marchfolk Iteration 3 references as measurement truth;
- never use Vael Rodin relief GLBs as measurable anatomy;
- use purpose-built candidate geometry where required;
- run ARM acceptance before measurement;
- reject and document candidates that fail rather than weakening canon;
- measure only the W1 items unlocked by that ARM.

## 4. Purpose-built ARM candidate rule

Where the manifest says **Purpose-built**, Claude may define and coordinate the reference candidate specification, but must not pretend a text specification is a mesh.

A purpose-built candidate must have:
- exact canonical reference stature;
- central skeletal values;
- reference composition;
- required sex-related configuration state;
- N3 neutralization;
- R-6 stance;
- no surface displacement affecting silhouette;
- all mandatory race anatomy;
- provenance identifying every numeric value not already canonical.

If a builder must choose a numeric value that canon has not supplied, that value is marked **BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED**. It may be used to create a candidate but cannot become canon by later measuring the candidate.

## 5. Measurement protocol

For every accepted ARM:
- measure in real-world units and normalized-to-stature ratios where the RMQ calls for them;
- preserve landmark definitions exactly;
- record raw measurements separately from derived ratios/indices;
- include uncertainty/measurement repeatability where geometry or landmark placement is ambiguous;
- keep left/right readings where asymmetry or landmark ambiguity matters even though the ARM state is symmetric;
- never round a borderline value into compliance;
- store enough precision for audit, but present practical summaries separately.

Every output must identify:
- ARM ID/version;
- source asset hash or immutable identifier if available;
- race/population;
- stature;
- configuration;
- measurement date/pass;
- landmark method;
- raw value;
- derived value;
- canonical constraint being tested;
- PASS / CONSTRAIN / FAIL where applicable.

## 6. Diagnostic-first rule

All W1 numeric results are **DIAGNOSTIC**.

Claude may conclude:
- candidate PASS;
- candidate CONSTRAIN/requires correction;
- candidate FAIL;
- measurement supports existing directional canon;
- measurement exposes an unresolved author choice.

Claude may **not**:
- convert a diagnostic envelope into canon;
- revise race anatomy to fit a mesh;
- move a creator bound;
- create a new creator control;
- decide RM-CF-05 FPI margin;
- infer population distributions from one central body.

Those require a later author-resolution order.

## 7. Cross-race checks during W1

As soon as relevant ARMs exist, test:
- Marchfolk as the normalized human comparator;
- Skarn vs Marchfolk human robustness/power architecture;
- Sagekin vs Marchfolk linearity and hand/ribcage tendencies;
- Fenn vs Aelari vs Vael central elf separation;
- Durrim vs Pipkin vs Cogling short-race identity;
- Skarn vs Grask vs Gorrund large-race identity;
- Grask central anterior projection ≈ Marchfolk while vertical midface remains Grask;
- Gorrund projection comparator;
- Halvren no-lineage body remains source-plausible and not 50/50;
- Saurin remains outside human/nonhuman rostral boundaries with mandatory tail architecture.

A cross-race failure means the candidate is corrected/rebuilt; canon is not weakened automatically.

## 8. Asset-access fallback

If Claude cannot directly access/build/measure the required geometry in the available environment:

Do **not** stop the whole Wave 1 at the first missing mesh.

Instead:
1. execute every item whose geometry is available;
2. create an **ARM Build Packet** for each missing candidate;
3. specify exact required views/state/stature/configuration/canon constraints;
4. identify which measurements that candidate unlocks;
5. state what file form/geometry access is needed for measurement;
6. place the item in a blocked queue.

This lets Tyler/ChatGPT supply or create assets without losing the measurement program.

## 9. Wave 1 deliverables

Create a structured W1 package:

1. `reviews/claude-rac-w1-00-preflight.md`
2. one ARM acceptance record per candidate actually inspected;
3. one build packet per candidate that must be created;
4. `reviews/claude-rac-w1-measurements.md` — raw + derived diagnostic measurements;
5. `reviews/claude-rac-w1-cross-race-audit.md`;
6. `reviews/claude-rac-w1-blocked-assets.md`;
7. `reviews/claude-rac-w1-author-decisions-needed.md`;
8. `reviews/claude-rac-w1-completion-report.md`.

Do not update canonical numeric envelopes yet.

## 10. Completion report

At the end, report:
- ARMs accepted / rejected / blocked;
- measurements completed;
- diagnostic findings;
- candidate corrections required;
- asset/build packets required;
- any genuine author decisions;
- exact readiness for W2.

Recommendation must be one of:
- **W1 COMPLETE — READY FOR AUTHOR ACCEPTANCE**
- **W1 PARTIAL — ASSET BUILD/ACCESS REQUIRED**
- **W1 BLOCKED — CANON CONTRADICTION** with exact contradiction.

Then STOP.

## 11. Explicit exclusions

No:
- UE5 implementation;
- skeleton-family decisions;
- production topology;
- rigging;
- morph-target design;
- animation/IK/retargeting;
- camera/first-person implementation;
- equipment fitting implementation;
- save/runtime architecture;
- gameplay racial-stat decisions.

Wave 1 quantifies approved anatomy. It does not implement the game.

— ChatGPT, Author

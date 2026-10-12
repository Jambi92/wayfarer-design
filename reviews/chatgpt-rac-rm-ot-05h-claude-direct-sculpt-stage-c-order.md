# WAYFARER RAC — RM-OT-05H CLAUDE-DIRECT GORRUND SCULPT / RE-ENTRY / STAGE-C GATE ORDER

**Status:** AUTHOR DESIGNATION — CLAUDE IS THE SCULPTOR  
**Parent block:** RM-OT-05G sculptor release closure  
**Release:** `gorrund-sculpt-release-8b76d2eae245`  
**Release SHA-256:** `287884f0da90df18cc9bd51e2291b8c602d88df0517fcfb8556513ce2f191bcd`  
**Scope:** DIRECT HAND SCULPT + VALIDATION ONLY — NO NEW ANATOMY, NO UE5, NO CANON PROMOTION BEFORE AUTHOR GATE  
**Stop condition:** Stop after the combined Stage C author gate, or earlier only on a genuine capability / validation blocker.

---

# 1. AUTHOR CLARIFICATION

The prior phrase **"external sculptor"** referred to the need for a genuine hand-sculpt route outside the failed procedural body-generation attempts.

For this project:

> **Claude is the designated sculptor.**

Do not wait for a third-party artist.

Do not ask the author to find another sculptor.

Do not treat the release as a package to hand off elsewhere.

Your next task is to use the frozen release yourself and produce the Gorrund sculpt asset.

---

# 2. NON-NEGOTIABLE METHOD BOUNDARY

The procedural Gorrund body-generation route is exhausted.

The required work is a **genuine direct sculpt / manual mesh-edit pass** on the supplied frozen base.

Do not substitute:

- a new procedural anatomy generator;
- parameter search;
- automated body synthesis;
- a fresh race-base algorithm;
- smoothing/deformation scripts intended to manufacture the six hard-form families automatically;
- a new base mesh;
- remeshing / topology replacement;
- any hidden geometry rewrite that bypasses the sculpt contract.

Allowed:

- direct sculpting / manual vertex movement in Blender using the frozen package;
- another genuinely direct/manual mesh-edit facility if and only if it preserves the exact topology, vertex order, transforms, pose, protected zones and export contract.

If your current execution environment truly provides **no interactive or direct manual mesh-edit capability**, stop with a concise capability report. Do **not** fake a hand sculpt procedurally and do **not** redirect the task to an unnamed external sculptor.

---

# 3. RELEASE INTEGRITY FIRST

Use the exact frozen release:

**`gorrund-sculpt-release-8b76d2eae245`**

Verify before sculpting:

- archive SHA-256 equals `287884f0da90df18cc9bd51e2291b8c602d88df0517fcfb8556513ce2f191bcd`;
- release manifest passes;
- required files are present;
- frozen hashes match;
- script hashes match.

Use the package's own:

- `START_HERE.md`;
- frozen sculpt brief;
- `blender/CHECKLIST_SCULPTOR.md`;
- `blender/CHECKLIST_DELIVERY.md`.

Do not modify the frozen package itself.

Work from a copy / working file outside the package.

---

# 4. FIRST-SESSION DESKTOP VERIFICATION — CLAUDE MUST COMPLETE IT

The RM-OT-05G closure correctly left the desktop verification PENDING.

Because Claude is now the sculptor, complete checklist §0 yourself before the real sculpt.

Required disposable test:

1. run `g_setup.py`;
2. save a disposable Blender file;
3. verify:
   - `GO_SCULPT_BASE` is the only selectable object;
   - Location = 0,0,0;
   - Rotation = 0,0,0;
   - Scale = 1,1,1;
   - transforms locked;
   - masks present on head/neck, hands/digits, toes/forefoot;
   - anatomical orientation correct;
4. make one small reversible allowed-region stroke;
5. export with `SCULPT_ID='DT'`;
6. require `RAC_EXPORT PASS`;
7. run preflight;
8. require `PREFLIGHT PASS`;
9. verify protected-zone change = 0;
10. delete the disposable outputs;
11. record Blender version, OS and verification PASS in the final sculpt manifest.

If any desktop verification step fails, stop and report the exact failure. Do not begin the real sculpt until the tooling path is proven.

---

# 5. SCULPT SOURCE / DELIVERY ID

Use:

**Start mesh:** `template/GO_ref_route_r6.obj`  
**Working object:** `GO_SCULPT_BASE`  
**Reference stature:** 230.90 cm  
**Delivery ID:** **S1**

Create:

**`GO_sculpt_S1_work.blend`**

Save incremental backups during the sculpt.

The delivered OBJ must remain:

- 13,380 vertices;
- exact original vertex order;
- identical faces;
- same coordinate system;
- same R-6 neutral pose;
- same transforms.

---

# 6. PROTECTED / FROZEN ANATOMY

Do not change the accepted skeleton or race proportions.

Hard holds include:

- joint centres;
- long-bone axes;
- stature;
- accepted pelvis/thorax relations;
- accepted pelvic depth relation;
- accepted S4/S2 breadth;
- accepted S3/S2 depth;
- plantigrade stance;
- five digits;
- human-compatible hands and feet;
- no hunch;
- no crouch;
- no forward lean;
- no exaggerated lumbar arch;
- no digitigrade illusion.

Protected surface zones:

- head / neck;
- hands / digits;
- toes / forefoot.

They must remain within the frozen package tolerance.

The true skeletal floor remains the hard inner limit.

---

# 7. SIX HARD-FORM FAMILIES — BUILD THEM BY HAND

The frozen brief is authoritative. Canon wins over any ambiguous sculpt wording.

The body must read as a **distinct upright plantigrade Gorrund through structural hard-form anatomy**, not as a heavy human.

Build all six families.

## A — Trunk S2–S5

Create:

- broad sternal / abdominal plate;
- legible lateral thoracic planes;
- strong but radiused plane breaks;
- crisp costal structural border;
- deep structural trunk continuity toward the pelvis.

The thorax must remain anatomically shaped and radiused.

Never make it:

- rectangular;
- boxy;
- mechanically slab-sided;
- cylindrical;
- barrel-like;
- dependent on a pinched human waist.

Do not use fat / muscle bulk as the read.

## B — Posterior axial load path

Create:

- paired broad low paraspinal columns;
- flat interscapular plane;
- defined sacral plate;
- hard transverse sacral border;
- structural sacrum → hamstring path.

Avoid:

- ordinary round buttock dominance;
- lumbar hollow;
- hump;
- spinal ridge;
- bodybuilder back.

## C — Pelvis → thigh

Create:

- structural hip plate;
- trochanteric shelf as a plane change;
- planar lateral thigh;
- clear pelvis → thigh step.

Never create:

- lateral pelvic outrigging;
- a thorax → pelvis step;
- inflated buttocks.

## D — Knee / shank / ankle

Create:

- broad flush patellar plane;
- integrated condyle blocks;
- squarish shank section;
- flat anteromedial tibial plane;
- posterior tendon column;
- broad malleolar anatomy.

The shank must taper.

Ankle must remain narrower than calf.

Never make:

- bulbous / armor knees;
- pillar legs;
- uniform limb diameter;
- Grask high-calf / long-cord anatomy.

## E — Elbow / forearm / wrist

Create:

- integrated olecranon / epicondyle block;
- flattened squarish forearm;
- clear tendon border;
- broad flattened wrist.

Hands remain unchanged.

Never make:

- isolated elbow knobs;
- columnar wrists;
- Grask tapering forearms.

## F — Shoulder girdle / neck root

Create:

- low broad girdle integrated into the trunk;
- trapezius plane as surface continuity, not bulk;
- planar shoulder block over the accepted joint;
- skeletal neck base readable at low composition.

Never create:

- girdle overhang;
- trapezius-produced neck-root breadth;
- deltoid-cap bodybuilder read;
- hump.

---

# 8. KEY READABILITY STANDARD

The sculpt must succeed when neutralized.

It must **not** depend on:

- height alone;
- width alone;
- obesity;
- muscularity;
- face;
- pigmentation;
- texture;
- clothing;
- hair;
- posture tricks.

At reference and especially **low composition**, the body-only read must remain structurally Gorrund.

The target is not "monster."

The target is:

> an unmistakably non-human-but-humanoid structural organization that still obeys the locked upright plantigrade Gorrund canon.

---

# 9. ITERATIVE SCULPT REVIEW

During the sculpt, repeatedly inspect:

- front;
- front 3/4;
- profile;
- rear 3/4;
- neutral grey;
- silhouette.

Run:

- `g_preview.py`;
- `g_views.py`.

Remember:

- preview is advisory only;
- authoritative persistence is decided by re-entry;
- low-composition readability is mandatory;
- no family may disappear at low composition.

Use the failed 05D/05E Gorrund examples only as "do not repeat" references.

Use Grask evidence only as contrast so Gorrund does not inherit Grask cues.

---

# 10. EXPORT / PREFLIGHT

When S1 is ready:

1. save the working `.blend`;
2. set:
   - `SCULPT_ID='S1'`;
   - `SCULPTOR='Claude'`;
3. export only through `g_export.py`;
4. require **RAC_EXPORT PASS**;
5. run:
   `g_preflight.py GO_sculpt_S1_r6.obj --package <pkg>`;
6. require **PREFLIGHT PASS**;
7. fill `GO_sculpt_S1_manifest.json`;
8. preserve the desktop-verification block;
9. produce the required views and preview evidence.

Never hand-edit the exported OBJ.

---

# 11. REQUIRED S1 ARTIFACT SET

Preserve together:

- `GO_sculpt_S1_r6.obj`;
- `GO_sculpt_S1_r6_export_report.json`;
- `GO_sculpt_S1_preflight.txt`;
- `GO_sculpt_S1_manifest.json`;
- `GO_sculpt_S1_work.blend`;
- required F/Q/P/RQ grey views;
- required F/Q/P/RQ silhouette views;
- low / Narrow / Broad preview views;
- preview console result.

Record SHA-256 for all principal returned artifacts.

Do not commit a huge `.blend` to Git if repository policy / size makes that inappropriate; record its hash and controlled location instead. Commit the compact validated outputs / reports / evidence needed for review.

---

# 12. CLAUDE IS ALSO AUTHORIZED TO RECEIVE HIS OWN SCULPT INTO THE VALIDATION PIPELINE

Because Claude is the designated sculptor and pipeline operator, do not stop merely to "return the OBJ to the receiver."

After S1 export/preflight passes, proceed directly to the unchanged receiver-side validation.

This does **not** waive any gate.

---

# 13. RE-ENTRY GATE — MANDATORY

Run unchanged:

`python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_S1_r6.obj S1`

It must execute:

- ingest I1–I6;
- reference build;
- low-composition build;
- Narrow build;
- Broad build;
- every 05D / 05E guard;
- transport report.

Thresholds are frozen.

Do not relax a threshold to rescue the sculpt.

If re-entry fails:

- stop Stage C;
- diagnose the smallest sculpt issue;
- return to the same S1 working sculpt;
- make a bounded direct/manual correction;
- export the next revision ID **S2**;
- preflight;
- re-enter again.

Repeat with S3, S4, etc. only as needed.

Do not switch back to procedural body generation.

---

# 14. BLIND GATE — ONLY AFTER RE-ENTRY PASS

After a sculpt revision passes full re-entry, run the replicated blind gate unchanged.

Required:

- `f_blind.py <ID> run1`;
- `f_blind.py <ID> run2`;
- run3 if the frozen protocol requires it;
- 3 fresh uninformed scorers per run;
- `f_scorer_prompt.md` verbatim;
- `f_tally.py`;
- all G1–G7 rules.

**Blindness must be preserved.**

Do not expose to scorer instances:

- sculpt intent;
- six-family target names;
- prior failures;
- which body is Gorrund;
- which revision Claude prefers;
- expected answer.

Claude's sculptor role must not contaminate the blind scorer context.

A pass in one blind run and fail in another is a FAIL.

Do not reinterpret ambiguity as a pass.

---

# 15. SCULPT ITERATION RULE

If the blind gate fails but re-entry passes:

- diagnose from the blind evidence;
- change only the weakest hard-form family/families;
- preserve all passing families;
- produce the next sculpt revision ID;
- rerun exporter + preflight + full re-entry;
- rerun the blind gate from fresh scorer instances.

Do not tune directly to a single scorer's wording.

Do not turn Gorrund into a caricature simply to force "non-human" votes.

The body still must obey every canon guardrail.

---

# 16. STAGE C — AUTHORIZED ONLY AFTER BOTH GATES PASS

Only when one sculpt revision passes:

1. full 05F re-entry;
2. replicated blind gate;

then proceed to the already-authorized **combined Stage C** using:

- frozen accepted-developmental-direction **Grask E3**;
- validated Gorrund sculpt revision.

Do not modify Grask E3 before Stage C.

Do not automatically promote either race solely because the individual sculpt passes.

Stage C must determine whether the paired large-race solution works together under the frozen comparative system.

---

# 17. STAGE C REQUIRED CHECKS

Run the existing authorized Stage C protocol exactly.

At minimum preserve the intent that Stage C verifies:

- Grask remains Grask;
- Gorrund remains Gorrund;
- the two are positively distinct;
- neither collapses into human-family anatomy;
- neither borrows the other's defining cues;
- low-composition identity survives;
- frame variants remain coherent;
- accepted skeleton/proportion constraints remain intact;
- cross-race collision/readability is solved without surface stereotypes.

Do not invent new Stage C acceptance thresholds unless the existing protocol has a genuine missing case.

If a protocol defect is discovered, stop and report it rather than improvising a new rule.

---

# 18. NO CANON PROMOTION BEFORE AUTHOR GATE

Even after Stage C passes:

- do not canonize the sculpt automatically;
- do not replace accepted Gorrund reference anatomy automatically;
- do not close RM-OT-05 automatically;
- do not begin D4;
- do not begin UE5.

Return an author gate first.

---

# 19. REQUIRED FINAL DELIVERABLE

Return:

**`reviews/claude-rac-rm-ot-05h-claude-sculpt-stage-c-gate.md`**

The gate must state:

- **Desktop Blender/direct-manual capability — PASS / BLOCKED**
- **Desktop verification — PASS / FAIL / NOT AVAILABLE**
- **Final sculpt revision ID — S1 / S2 / ...**
- **Exporter — PASS / FAIL**
- **Preflight — PASS / FAIL**
- **05F re-entry — PASS / FAIL**
- **Replicated blind gate — PASS / FAIL**
- **Gorrund structural readability — ACCEPT / CONSTRAIN / REJECT**
- **Grask E3 Stage C status — ACCEPT / CONSTRAIN / REJECT / NOT RUN**
- **Gorrund Stage C status — ACCEPT / CONSTRAIN / REJECT / NOT RUN**
- **Grask ↔ Gorrund combined Stage C — ACCEPT / CONSTRAIN / REJECT / NOT RUN**
- **RM-OT-05 — READY FOR AUTHOR CLOSURE / OPEN**
- **Canon promotion — NOT PERFORMED**
- **D4 — NOT STARTED**
- **UE5 — NOT STARTED**

Include:

1. exact release/hash verification;
2. desktop verification record;
3. sculpt revision history;
4. final artifact hashes;
5. required views;
6. preflight evidence;
7. complete re-entry evidence;
8. complete blind-gate evidence;
9. Stage C evidence if authorized gates passed;
10. every remaining fail / marginal / blocker;
11. explicit confirmation that no acceptance threshold or canon rule was changed.

---

# 20. STOP CONDITION

Stop at the RM-OT-05H author gate.

Do not begin:

- D4;
- UE5;
- rigging;
- animation;
- equipment fitting;
- gameplay implementation;
- unrelated RAC work.

If direct/manual sculpt capability is unavailable, stop earlier with the capability blocker rather than substituting another procedural Gorrund.

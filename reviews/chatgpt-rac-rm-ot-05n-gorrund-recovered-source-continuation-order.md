# WAYFARER RAC — RM-OT-05N GORRUND RECOVERED SOURCE + MINIMAL BEASTFOLK CANON ALIGNMENT + SURGICAL CONTINUATION ORDER

**Status:** AUTHOR DECISION ISSUED — RECOVERED SOURCE ACCEPTED FOR SUITABILITY REVIEW; CONTINUE EXISTING BODY PROGRAM WITHOUT MAJOR REDESIGN  
**Parent blocks:** RM-OT-05M source-recovery gate; recovered-source record commit e44781b  
**Recovered source:** original historical Gorrund Male GLB  
**Author intent:** Keep the established Gorrund body architecture. Formally preserve the recovered/original beastfolk identity — leonine head + tail — without using that discovery as an excuse to redesign the body from scratch.  
**Scope:** source suitability, minimal canon alignment, source extraction, surgical reference correction, LOW companion, revised neutralized body-structure gate, measurement scaffold.  
**Do not begin:** UE5, production rigging, animation, equipment fitting, creator implementation, unrelated RAC work.  
**Stop condition:** RM-OT-05N author gate.

---

## 1. SOURCE RECOVERY IS CLOSED

The original Gorrund Male GLB has now been recovered.

Authoritative recovered-source record:

- SHA-256: `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b`
- size: 43,012,652 bytes
- historical identity: the Gorrund Male GLB submitted in the Wayfarer 3D Models workflow
- recovered copy on author PC recorded in:
  `reviews/rac-rmot05m-evidence/source_glb/SOURCE_RECORD.md`

Do not generate a replacement Rodin source.

Do not spend Rodin credits.

Preserve the recovered source unchanged as provenance.

---

## 2. AUTHOR CANON RULING — NO MAJOR BODY REDESIGN

Tyler's ruling is explicit:

> The Gorrund remain the same massive, load-bearing race we have been developing. The recovered source confirms the intended beastfolk presentation. Preserve the established body work; add/retain the leonine head and tail identity. Continue the existing program rather than restarting the species.

Therefore:

### KEEP the established Gorrund body identity

- massive load-bearing skeletal architecture;
- high absolute structural scale;
- broad/deep axial organization;
- substantial integrated joints;
- strong axial-to-limb load path;
- upright humanoid stance;
- plantigrade locomotion;
- large functional hands;
- tool-capable civilization-compatible anatomy;
- body massiveness independent of current muscle/fat;
- no ogre/troll caricature;
- no bodybuilder dependency;
- no obesity dependency;
- no Grask reach architecture.

### FORMALLY ALIGN the species presentation

- Gorrund are **beastfolk**;
- the head is **leonine / lion-like**;
- Gorrund possess a **tail**.

These are targeted canon corrections, not permission to rewrite the whole body.

---

## 3. IMPORTANT LIMIT ON WHAT THE RECOVERED GLB MAKES CANON

The recovered GLB is the correct historical Gorrund source asset, but not every visual detail in it automatically becomes biological canon.

The author has specifically selected:

- beastfolk identity;
- leonine head;
- tail.

Do **not** silently promote every source-image feature.

In particular, the following remain governed by the existing Gorrund Bible unless separately authorized:

- **plantigrade** stance remains locked;
- do not convert Gorrund to digitigrade;
- do not import paw-foot anatomy merely because the source depicts it;
- do not import mandatory extreme muscularity;
- do not make claws/fangs/fur distribution or mane size into creator-wide biological constants unless existing canon supports them;
- loincloth/wraps/ornaments are presentation artifacts, not biology;
- do not import old concept-sheet culture text as canon;
- do not import class restrictions.

Treat the source as high-quality raw sculpt/reference clay, not an authority over the Bible.

---

## 4. MINIMAL GORRUND_V1 CANON ALIGNMENT

Update `specs/gorrund/GORRUND_V1.md` only where required to remove direct contradiction with the author's beastfolk ruling.

Required corrections:

1. Replace any statement that Gorrund are non-beastfolk or explicitly denies a leonine/muzzled head.
2. Remove/revise the existing “never a muzzle” restriction.
3. State that the canonical head is leonine/lion-like while remaining compatible with an intelligent upright humanoid race.
4. Add the presence of a tail.
5. Record that the tail and leonine head are species-identity channels and do not replace the existing structural body architecture.
6. Preserve all body architecture rules not directly contradicted by this ruling.
7. Do not invent numeric facial, muzzle, ear, mane or tail envelopes in this block unless an already accepted source exists.
8. Mark exact head/tail numeric morphology OPEN where necessary.

Do not perform a broad rewrite of GORRUND_V1.

Show the exact canon lines changed in the final gate.

---

## 5. REINTERPRET RM-OT-05 CORRECTLY

The prior RM-OT-05 body-only program was useful, but one part of the acceptance interpretation was too strong.

Because Gorrund species identity includes an unmistakably leonine head and tail:

> **The body alone does not need to make an uninformed observer identify “non-human species” with no head and no tail.**

What the neutralized body test must prove is:

- the body is not merely an ordinary Marchfolk/Skarn body scaled up;
- the Gorrund structural architecture remains coherent and distinctive;
- the body does not collapse into fatness, bodybuilding, boxiness or Grask cues;
- REF and LOW preserve the same structural organism;
- the body supports the complete leonine beastfolk design when head/tail are restored.

Therefore revise the interpretation from:

> BODY ALONE MUST SCREAM NON-HUMAN

to:

> BODY ALONE MUST SHOW DISTINCTIVE GORRUND LOAD-BEARING ARCHITECTURE WITHOUT CHEATING THROUGH COMPOSITION OR BAD SHAPE; SPECIES RECOGNITION IS COMPLETED BY THE LEONINE HEAD AND TAIL.

Do not discard old blind evidence. Reclassify it as negative evidence against box/fat/bodybuilder/mannequin solutions, not proof that the core Gorrund concept itself was invalid.

---

## 6. SOURCE SUITABILITY GATE — RUN NOW

Use the recovered original GLB.

First inspect the source without modifying it.

The source record says it contains:

- four separately modeled full-body figures;
- head/face studies;
- eye/ear/fur/nose details;
- separate hand/foot/lower-leg/tail parts.

Determine the connected components / major islands and identify the strongest complete full-body figure for anatomical source use.

Record for each full-body figure:

- vertex/face count;
- completeness;
- amount of clothing/wrap obstruction;
- front/back/side quality;
- whether body anatomy is true 3D rather than a flat relief;
- whether limbs are complete;
- whether the body can be isolated cleanly;
- whether the lion head and tail are attached or separate;
- obvious source artifacts;
- suitability for surgical sculpt.

Select **one primary body source**.

Do not average four views into a procedural body.

---

## 7. SOURCE EXTRACTION RULE

Create:

- `GO-RD0-SOURCE` — untouched extracted/isolated primary source body;
- `GO-RD1-REF` — surgical working candidate.

If the original GLB is a single mesh containing multiple disconnected figures/components:

- duplicate the file;
- isolate the chosen full-body component non-destructively;
- preserve original coordinates/provenance;
- do not alter the source master.

If clothing is a separable component, remove/hide it in the working copy.

If clothing is fused into anatomy:

- reconstruct only the obscured regions necessary for the body reference;
- document every reconstructed zone;
- do not infer unseen anatomy from the garment silhouette alone.

---

## 8. SCALE / ORIENTATION

The recovered source is in normalized units.

For the working reference only:

- orient consistently with the RAC coordinate convention;
- scale to the existing Gorrund nominal reference neighborhood (~229 cm) for comparable review;
- treat this as a **display/reference normalization**, not proof of a species constant;
- do not use uniform scale as the future creator stature mechanism.

Record the scale factor.

---

## 9. SURGICAL BODY CORRECTION — DO NOT REBUILD FROM ZERO

Claude remains the sculptor.

The purpose of RD1 is not to turn the source into a completely different creature.

Use the biological surface quality already present and surgically correct the body toward the established Gorrund architecture.

Priority order:

1. overall axial coherence;
2. girdle/thorax integration;
3. lower axial trunk;
4. pelvis/proximal femur;
5. posterior load path;
6. knee/shank/ankle;
7. elbow/forearm/wrist;
8. hands/feet;
9. source-artifact cleanup.

Do not impose the old failed S1–S4 cage.

Do not impose Marchfolk donor ratios.

---

## 10. BODY TARGET REMAINS THE SAME

RD1 must preserve the established Gorrund structural identity:

### Thorax

- broad and deep;
- three-dimensional;
- anatomically radiused;
- load-bearing;
- not rectangular;
- not slab-sided;
- not cylindrical/barrel.

### Lower axial trunk

- carries thorax into pelvis;
- may have a natural anatomical minimum;
- not a pinched human waist;
- not a parallel-sided column;
- not a belly transition.

### Girdle / neck root

- girdle carried by thorax;
- substantial neck root;
- no trap/bodybuilder solution;
- no shoulder overhang.

### Pelvis / femur

- substantial pelvis;
- large hip articulation;
- strong proximal-femur support;
- no hip outriggers.

### Legs

- load-bearing femoral scale;
- substantial integrated knees;
- shanks that retain taper;
- substantial ankles;
- plantigrade feet.

### Arms

- substantial integrated elbow;
- structured forearm;
- functional broad wrist;
- large capable hands;
- no Grask reach-dominant proportions.

### Posterior

- broad coherent load path;
- substantial sacral region;
- sacrum-to-hamstring continuity;
- no bodybuilder grooves;
- no ordinary soft-buttock dominance.

---

## 11. SOURCE-SPECIFIC ARTIFACTS TO REMOVE

The recovered source record notes:

- heavily muscled build;
- paw-like feet;
- loincloth;
- wrist/ankle wraps;
- beastfolk fur/mane presentation.

For body-reference purposes:

- reduce muscle if it obscures skeletal architecture;
- reconstruct/normalize the feet to the locked plantigrade Gorrund anatomy rather than canonizing a digitigrade/paw solution;
- remove/hide clothing and wraps from scored body views;
- keep the leonine head and tail available for full-organism review;
- fur/hair/mane must not hide body-surface evaluation.

Do not erase the head/tail from the source lineage; simply neutralize them when the body-only structural test requires it.

---

## 12. RD1 INTERNAL BODY GATE

Before LOW:

RD1 must pass an internal structural gate:

- coherent biological organism;
- source-surface anatomy retained/improved;
- no mannequin/sausage read;
- no rectangle/box/slab;
- no barrel cylinder;
- no obese-human read;
- no bodybuilder dependency;
- no hourglass solution;
- no Grask reach read;
- pelvis/femur integration clear;
- posterior load path clear;
- substantial joints integrated rather than knobbed;
- plantigrade lower limb preserved;
- Gorrund body reads as structurally massive rather than merely thick.

If one coherent surgical issue remains, allow **GO-RD2-REF**.

No RD3 without author order.

---

## 13. FULL-ORGANISM REVIEW — RESTORE HEAD AND TAIL

Once the structural reference passes internally, create a separate full-organism presentation using:

- the leonine/lion-like head from the source as a starting point;
- the source tail as a starting point.

This is a **review presentation**, not yet a final face/tail parameter freeze.

Confirm that:

- leonine head + structural Gorrund body + tail read as one coherent species;
- head scale does not make the body look undersized;
- neck root supports the head naturally;
- tail root integrates with the pelvis/sacral anatomy;
- tail does not create a quadrupedal/digitigrade implication;
- no ogre/orc/troll collapse.

If head/tail source anatomy needs surgical cleanup for a coherent presentation, perform bounded cleanup but do not invent numeric creator envelopes.

---

## 14. LOW COMPANION

Only after RD1/RD2 REF passes:

Create the LOW companion manually from the accepted reference body.

The LOW state should represent reduced muscle and reduced fat while preserving:

- skeletal thorax;
- pelvis;
- structural joints;
- neck/girdle architecture;
- limb lengths;
- load path;
- tail root relationship.

Do not use the old Marchfolk-derived composition deformation.

Do not shrink the body uniformly.

---

## 15. REVISED NEUTRALIZED STRUCTURAL GATE

Run a fresh neutralized body-structure evaluation on REF and LOW.

Use:

- head hidden/neutralized;
- tail hidden for the structural-only pass;
- neutral material;
- matched display stature;
- no fur/hair/culture/gear.

Controls:

- Marchfolk;
- Skarn;
- Skarn Broad;
- Grask E3;
- other relevant controls if already frozen.

### PASS no longer requires:

- uninformed scorers to call the headless/tailless body a clearly non-human species.

### PASS now requires:

1. REF and LOW group stably as the same structural body type;
2. they do not collapse into ordinary scaled-up Marchfolk;
3. they do not collapse into Skarn Broad;
4. they remain distinct from Grask architecture;
5. scorer reasons identify structural organization rather than fat, muscle, posture or boxiness;
6. the body remains compatible with the full leonine beastfolk presentation.

Record old RM-OT-05 criteria beside the revised interpretation so provenance is explicit.

Do not rewrite old scores.

---

## 16. FULL-ORGANISM CONFIRMATION GATE

After the structural-only pass, run a separate **full-organism confirmation** with the head and tail visible.

This is not a blind species-discovery test; it verifies coherence.

Confirm:

- leonine identity is unmistakable;
- tail is present and anatomically integrated;
- body still carries the established Gorrund load-bearing identity;
- the combination does not look like a generic lion-man pasted onto a human body;
- the combination does not look like Grask;
- the body does not require extreme muscle/fat to support the head/tail read.

This gate closes the gap that the old body-only test could never evaluate.

---

## 17. MEASUREMENT SCAFFOLD — ONLY AFTER ACCEPTED BODY

If REF/LOW pass the revised structural gate and full-organism review, derive measurement landmarks from the accepted body.

Derive:

- stature reference;
- shoulder centres;
- elbow centres;
- wrist centres;
- hip centres;
- knee centres;
- ankle centres;
- long-bone axes;
- axial stations;
- thoracic breadth/depth stations;
- pelvic breadth/depth stations;
- sacral/tail-root landmark;
- hand/foot attachment references.

For the tail:

- derive tail-root location and primary axis only if the source supports it;
- do not freeze final tail length/taper creator ranges in this block.

For the head:

- derive head/neck attachment and gross cranial scale only if defensible;
- do not freeze detailed muzzle/mane/ear ranges yet.

This remains measurement-only.

No production rig.

---

## 18. CANON RECONCILIATION

After scaffold derivation, classify each old Gorrund relationship:

- **PRESERVED**
- **PRESERVED IN DIRECTION**
- **NUMERIC REFERENCE UPDATED**
- **OLD ROUTE ARTIFACT**
- **TRUE CANON CONFLICT**
- **NOT YET MEASURABLE**

The recovered source must not automatically win against established body canon.

The author beastfolk ruling does win against the old “never a muzzle / no tail” contradiction.

---

## 19. STATUS OF OLD RM-OT-05 FAILURES

Do not delete them.

Record them as follows:

- S1–S4 / EA: failed attempts to force distinctiveness through a constrained body envelope;
- RF1/RF2: failed human-donor transformations;
- RS1/RS2: failed low-quality blank-clay source generation;
- these failures remain valuable negative evidence;
- they no longer imply that the Gorrund species concept itself is invalid;
- the new recovered-source route is the authoritative active path.

---

## 20. REQUIRED EVIDENCE

Create an RM-OT-05N evidence folder containing:

- source component/island manifest;
- selected source rationale;
- source screenshots;
- RD1/RD2 neutral body sheets;
- source-vs-sculpt comparisons;
- REF/LOW structural sheets;
- full-organism head+tail review;
- revised scorer outputs;
- measurement scaffold if derived;
- hashes;
- exact changed GORRUND_V1 lines.

Preserve the source master untouched.

---

## 21. REQUIRED AUTHOR GATE

Return:

`reviews/claude-rac-rm-ot-05n-gorrund-recovered-source-continuation-gate.md`

State:

- **Recovered source verified — PASS / FAIL**
- **Source hash — exact**
- **Primary full-body source selected — identifier**
- **Source suitability — PASS / FAIL**
- **Minimal beastfolk canon alignment — COMPLETE / BLOCKED**
- **Existing body canon preserved — YES / CONFLICT**
- **Final reference — RD1 / RD2 / NONE**
- **RD internal structural gate — PASS / FAIL**
- **Leonine head restored for organism review — YES / NO**
- **Tail restored/integrated for organism review — YES / NO**
- **LOW companion — CREATED / NOT CREATED**
- **REF↔LOW structural audit — PASS / FAIL / NOT RUN**
- **Revised neutralized structural gate — PASS / FAIL / NOT RUN**
- **Full-organism coherence gate — PASS / FAIL / NOT RUN**
- **Measurement scaffold — DERIVED / PARTIAL / NOT DERIVED**
- **Canon reconciliation — CLEAN / CONFLICTS / NOT RUN**
- **RM-OT-05 — READY FOR CLOSURE / OPEN**
- **Stage C — READY / BLOCKED**
- **Canon promotion — NOT PERFORMED**
- **D4 — NOT STARTED**
- **UE5 — NOT STARTED**

Include all unresolved conflicts rather than silently resolving them.

---

## 22. STOP CONDITION

Stop at the RM-OT-05N author gate.

Do not:

- regenerate the Gorrund source;
- perform another species redesign;
- convert to digitigrade;
- adopt all old concept-sheet traits wholesale;
- begin production rigging;
- begin UE5;
- start Stage C without the author reviewing this new recovered-source body;
- work on unrelated RAC blocks.

The goal is straightforward:

> **Use the recovered original high-quality Gorrund source to finish the body we were already designing, while restoring the intended leonine beastfolk head and tail — not to create a different race.**

# ChatGPT — Universal Facial Customization Architecture (UFCA) Phase 1 Order

**Author:** ChatGPT  
**For:** Claude (auditor / architecture analyst)  
**Phase:** DESIGN ONLY  
**Prerequisite:** Pass 2 FINAL-AUTHOR ACCEPTED / FROZEN  
**Status:** AUTHOR ORDER — BEGIN UFCA

## 1. Mission

Begin the **Universal Facial Customization Architecture Review** for all 13 playable populations.

The objective is not to make every race use one face, one topology, one skeleton, one morph set, or one identical slider range. The objective is to establish one coherent **creator-facing facial architecture and validation language** capable of expressing every approved race specification without weakening race-specific biology.

Existing race-specific facial-control organizations remain:

**APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION.**

They are evidence and requirements for UFCA, not obsolete material.

Use the accepted Pass 2 common craniofacial landmark/metric framework as the cross-population comparison and measurement language. It is **not automatically the creator-control hierarchy**.

Do not begin UE5 implementation.

## 2. Non-negotiable design principles

UFCA must preserve:

1. **Biology before UI convenience.** Controls adapt to approved anatomy; approved anatomy is never redesigned to fit a universal menu.
2. **Shared navigation does not require shared anatomy.** A category may exist across races while exposing different controls, ranges, dependencies, or no applicable control.
3. **Positive racial identity survives neutralization.** Remove hair, pigmentation, cosmetics, markings, cultural presentation and expression; valid faces must still preserve the approved biological space of their population.
4. **Individuality inside population identity.** The system must permit broad individual facial diversity without letting a race collapse into another population.
5. **No attractiveness architecture.** Beauty, youth, symmetry, delicacy, ruggedness, masculinity/femininity and conventional attractiveness are not universal biological goals.
6. **Sex-related anatomy follows R-SEX.** Do not invent facial dimorphism for races that do not canonically have it.
7. **Age systems remain distinct:** Chronological Age, Apparent Biological Age and Age Presentation.
8. **Natural asymmetry is supported.** Acquired damage remains distinct from biological asymmetry.
9. **Biological iris/ocular anatomy remains distinct from magical eye effects and observed lighting.**
10. **Culture/presentation remains separate from anatomy.**
11. **Relationship-aware validity is mandatory.** Valid individual parameters may form an invalid face when combined.
12. **Presets are legitimate outputs of the same system**, not handcrafted exceptions.

## 3. Roster coverage

Audit and architect for all 13:

- Marchfolk
- Skarn
- Sagekin
- Fenn
- Aelari
- Vael
- Halvren
- Durrim
- Grask
- Gorrund
- Pipkin
- Cogling
- Saurin

Halvren must be treated as a genuine mixed-ancestry developmental system, not a generic human/elf interpolation slider.

Saurin must be supported without forcing human nose, lips, chin, pinna or facial topology onto its Layered Rostral-Cranial Integration.

## 4. First task — Requirements Extraction Matrix

Before proposing the final hierarchy, extract the approved facial requirements from every canonical race spec.

For each population record, at minimum:

- cranial vault / cranial proportions;
- forehead;
- brow / supraorbital anatomy;
- orbital anatomy;
- external eye anatomy;
- ocular anatomy where relevant;
- cheek / zygomatic region;
- midface;
- nasal or rostral anatomy;
- mouth / lip or homologous oral anatomy;
- jaw / mandible;
- chin where anatomically applicable;
- external ear / auricular or homologous opening anatomy;
- teeth/dentition where creator-relevant;
- race-specific cranial displays/keratin structures;
- skin/surface structures that materially alter facial anatomy;
- natural asymmetry;
- age-related facial change;
- sex-related facial tendency only where canon exists;
- facial-hair biology where applicable;
- inherited/mixed-development requirements for Halvren;
- validation tests already locked;
- explicitly OPEN biology;
- provisional creator-control requirements from Pass 1.

Distinguish:
- **anatomical requirement**;
- **creator-facing control requirement**;
- **internal dependency/validator**;
- **presentation control**;
- **measurement/diagnostic only**;
- **OPEN / not yet authorized**.

Do not infer missing anatomy.

## 5. Second task — Universal navigation hierarchy

From the extraction matrix, propose the smallest universal creator-facing hierarchy that can contain all required facial systems.

Use a structure along these lines only as a starting hypothesis, not a mandated answer:

- Face Preset / Starting Face
- Global Craniofacial Relationships
- Cranium & Forehead
- Brow & Orbit
- Eyes / External Eye
- Cheeks & Midface
- Nose / Rostrum / Homologous Midface Projection
- Mouth / Oral Region
- Jaw & Chin / Mandibular Region
- Ears / Auricular Region
- Race-Specific Cranial Structures
- Asymmetry
- Age-related Anatomy
- Surface/Facial Biology
- Presentation

Determine which categories should actually be universal, conditional, nested, renamed or separated.

A universal category may have race-specific labels. Example: a shared navigation concept may route human/elven populations to nasal controls and Saurin to rostral/narial controls without pretending those structures are anatomically identical.

## 6. Control taxonomy

For every proposed control classify it as one of:

- **Direct anatomical control** — player intentionally edits a meaningful anatomical dimension.
- **Derived/coupled control** — value changes because connected anatomy requires it.
- **Soft-correlated control** — distribution tendency/correlation, but player may override within valid anatomy.
- **Validator-only variable** — not directly exposed; enforces biological coherence.
- **Preset latent variable** — may help generation/presets but should not appear as a literal slider.
- **Presentation control** — non-biological styling.
- **Diagnostic measurement** — comparison/QA only, not creator state.

Explicitly prevent diagnostic indices from becoming sliders merely because they are measurable.

## 7. Global vs regional controls

Resolve how broad facial controls interact with regional controls.

Requirements:

- No single “face width,” “face length,” “elfness,” “humanity,” “masculinity,” “femininity,” “beauty,” “age face,” or ancestry-percentage slider may silently drive the whole face.
- Broad controls may exist only when they represent a coherent anatomical relationship.
- Regional controls must preserve connected anatomy.
- Fine controls must not detach anatomy or defeat population validity.
- Halvren may expose phenotype expression without exposing genealogical ancestry as an appearance percentage.
- Randomization and presets may use latent correlated variables that are not exposed to the player.

Propose the dependency model, including when a child control should:
- follow a parent;
- retain relative offset;
- clamp;
- redistribute;
- trigger neighboring-region adjustment;
- become invalid and require correction.

## 8. Race-specific exceptions

Produce an exception map showing where a universal category cannot use identical controls.

At minimum inspect:

- human-family facial architecture;
- shared elven family versus Fenn/Aelari/Vael distinctions;
- Halvren mixed craniofacial inheritance;
- Durrim compact structural concentration;
- Grask non-human face and ear identity;
- Gorrund deep/integrated midface and jaw architecture plus non-human ears;
- Pipkin adult compact craniofacial identity;
- Cogling fine-scale facial articulation;
- Saurin Layered Rostral-Cranial Integration, recessed auricular openings, dentition and cranial keratin displays.

Do not solve exceptions by hiding them in presets.

## 9. Presets and randomization architecture

Define how facial presets work across the roster.

Requirements:

- presets are valid outputs of the same controls and validators;
- no preset-only anatomy;
- race-aware weighted generation;
- selective randomization (whole face or selected regions);
- lockable regions/attributes;
- reproducible seeded generation if technically useful later;
- rare valid phenotypes remain manually creatable even if rarely randomized;
- randomization respects correlated anatomy without producing clones;
- Halvren generation respects developmental inheritance and does not default to 50/50;
- Saurin generation respects mandatory rostral/skull identity and display biology.

Keep genealogical ancestry separate from visible phenotype.

## 10. Validation architecture

Design a universal validation framework with:

### A. Intra-population validity
Does the face remain biologically valid for its own population?

### B. Cross-population boundary validity
At normalized comparison conditions, does the face collapse into another population when neutralized?

### C. Relationship validity
Do connected structures remain coherent?

### D. Extreme-combination stress tests
Do individually valid extremes combine safely?

### E. Neutralization tests
Neutral expression, neutral lighting, hair/presentation removed, pigmentation neutralized where appropriate.

### F. Age and asymmetry tests
Do age/asymmetry preserve identity without becoming caricature or pathology by default?

### G. Preset/randomization tests
Can generated faces span the valid distribution without stereotype convergence?

Carry forward existing race-specific permanent validation tests rather than replacing them.

## 11. Measurement-deferred boundaries

Respect the Pass 2 Reference-Mesh Measurement Queue.

Do not invent numeric facial envelopes to make UFCA appear complete.

Where a control or validator ultimately needs a number:
- define the semantic variable now;
- define what structures/landmarks measure it;
- state whether it is player-facing or validator-only;
- connect it to the appropriate RM-CF / later measurement item;
- leave numeric bounds deferred until approved reference anatomy exists.

The provisional Saurin rostral floor remains protective canon.

## 12. Deliverables — Phase 1

Produce, in order:

1. **UFCA-01 — Roster Facial Requirements Extraction Matrix**
2. **UFCA-02 — Proposed Universal Navigation & Control Hierarchy**
3. **UFCA-03 — Control Taxonomy & Dependency Model**
4. **UFCA-04 — Race-Specific Exception Map**
5. **UFCA-05 — Preset & Randomization Architecture**
6. **UFCA-06 — Universal Facial Validation Framework**
7. **UFCA-07 — OPEN / Deferred / Author-Decision Register**
8. **UFCA-08 — Phase 1 Architecture Audit**

The audit must answer:
- Does every approved facial requirement from all 13 specs have a home?
- Did any universalization weaken a race's positive identity?
- Did any provisional Pass 1 requirement disappear without an explicit disposition?
- Did any OPEN item get silently resolved?
- Did any diagnostic measurement become a creator control without justification?
- Did any creator control become a hidden ancestry/culture/personality/gameplay control?
- Can Simple Mode and Advanced Mode both use this architecture?
- Can presets/randomization be represented as valid system outputs?
- Are Halvren and Saurin fully supported without forcing them into human topology?
- Are any author decisions required before architecture can be canonicalized?

## 13. Authority and editing rules

During Phase 1:
- **Do not rewrite the 13 canonical race specs.**
- **Do not rewrite PROJECT_RULES unless specifically ordered later.**
- Put UFCA analysis/proposals in new review files.
- Claude remains auditor/architecture analyst; ChatGPT remains author.
- Flag proposed canonical rules for author acceptance rather than silently canonizing them.
- Existing Pass 1 and Pass 2 canon remains authoritative.

## 14. Stop condition

Proceed autonomously through UFCA-01…UFCA-08.

Stop only if:
- two approved race requirements are genuinely incompatible with one architecture;
- a decision would materially change approved race biology;
- an OPEN biological question must be answered before architecture can proceed.

Otherwise complete Phase 1 and return the author-decision register.

After UFCA-08, **STOP** for ChatGPT author review.

Do not begin Phase 2 canonicalization.
Do not begin UE5 implementation.

— ChatGPT, Author

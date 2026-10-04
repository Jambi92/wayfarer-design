# Saurin — Next Phase Order: Character-Creation Biological Variation

**Author:** ChatGPT
**Status:** AUTHOR ORDER
**Prerequisite:** Anatomical / Surface Convergence CLOSED at `aff1b527ad6ef48b6490f7d4c4b2cff8b7fa9048`
**Phase:** DESIGN / VALIDATION ONLY — NO UE5

## Objective

Move from the frozen reference Saurin into a **population-capable character-creation biology specification**.

The question is no longer “what does a Saurin look like?” The frozen reference answers that. The question now is:

> How much individual biological variation can the Saurin support while every valid result remains recognizably Saurin, anatomically credible, compatible with equipment/world requirements, and generated from the same system used for presets and NPCs?

Do **not** reopen or beautify the reference anatomy.

## 1. Preserve the frozen target

Treat the closure artifact as immutable. Preserve:
- Counterbalanced Pelvic-Axial Architecture;
- accepted pelvis/sacrum/tail load path and tail geometry logic;
- +8% reference head scale;
- Layered Rostral-Cranial Integration and final brow/orbit solution;
- Regional Scale Architecture;
- hand/foot and claw identity;
- neutral naked skull;
- accepted display-family attachment logic;
- accepted phenotype/material/pattern definitions.

Reference values are centers/targets where appropriate, not automatic creator limits. Any proposed range must be validated at its extremes and in combinations.

## 2. Build the Saurin biological parameter register

Create a parameter register organized by the universal creator layers.

### A — Biological Anatomy
Define candidate controllable variation for at least:
- standing height;
- head-to-body proportion;
- cranial length/width/depth within Saurin identity;
- rostrum length, width and depth;
- jaw depth and posterior mandibular mass;
- orbital size/placement only where compatible with the frozen cranial architecture;
- neck length and structural depth;
- thoracic depth/width;
- axial trunk length;
- pelvic width/depth and sacral integration;
- shoulder breadth;
- arm and leg proportional length;
- hand/foot proportional size;
- tail length;
- tail base diameter/mass;
- tail taper profile;
- tail muscularity;
- tail resting curvature;
- digit/claw proportional variation;
- scale-field structural size/relief where biologically plausible;
- cranial display anatomy.

For every parameter classify:
1. independent,
2. correlated,
3. coupled/relationship constrained,
4. presentation-only,
5. locked racial biology.

Do not create sliders merely because a morph could technically exist.

### B — Skeletal Frame
Define Narrow / Balanced / Broad as editable starting distributions, not castes. Determine exactly which skeletal dimensions change and which Saurin relationships must remain protected.

### C — Physical Composition
Keep muscle amount/distribution and body-fat amount/distribution distinct from skeletal frame. Determine Saurin-specific plausible storage and muscular emphasis without importing human bodybuilding anatomy.

### D — Personal Presentation
Keep this outside biological inheritance except where it selects presentation of existing biological features. Do not make culture, profession or personality anatomical.

## 3. Solve tail coupling explicitly

The tail is the highest-risk creator subsystem.

Develop a relationship model for:
- standing height × tail length;
- pelvis/sacral dimensions × tail-base mass;
- tail length × base diameter × taper;
- composition × visible tail muscularity;
- tail mass × resting curvature;
- tail proportions × whole-body counterbalance.

The creator must reject or automatically constrain combinations that produce:
- attached appendage appearance;
- root too small for distal mass;
- oversized root with threadlike distal tail;
- tail mass inconsistent with pelvis/load path;
- implausible balance relationship;
- hidden reintroduction of the old Gate 6 failure modes.

Tail remains mandatory. No ordinary “tail off” control.

## 4. Cranial identity boundary study

Using the final naked skull, construct controlled diagnostic extremes for the major head parameters.

Test single-variable extremes first, then coupled extremes.

Every valid head must preserve:
- compact projecting rostrum;
- non-human nasal architecture;
- Layered Rostral-Cranial Integration;
- final brow → temporal/postorbital transition;
- embedded orbital read;
- deep articulated jaw base;
- no human chin/lips/nose/pinnae;
- complete naked-skull identity without display anatomy.

Display anatomy may never rescue a failed skull.

## 5. Display anatomy becomes a creator family, not a single default

Carry forward:
- neutral/naked;
- minimal ridges / near-naked;
- low hornlets;
- swept-back paired structures;
- mixed/asymmetric structures;
- restrained crest.

Treat these as biological phenotype/display anatomy analogous in creator role to a hair-selection category, **not hair itself**.

Determine which dimensions can vary safely: count, length, base size, orientation, sweep, modest asymmetry and crest height.

Do not assign automatic sex, culture, class, social status or gameplay meaning.

Use the accepted restrained crest reference as the current upper reference; do not silently expand into dragon/dinosaur horn architecture.

## 6. Surface phenotype variability

Translate the accepted Regional Scale Architecture into variation rules.

Allow variation *within* fields without destroying field identity:
- structural scale/scute size;
- local shape/orientation;
- relief;
- expressive-field fineness;
- ventral organization;
- articulation-field fineness;
- contact-surface treatment.

Field boundaries and biological function must remain coherent. Do not permit a global “scale size” slider that uniformly scales every field.

Preserve the already accepted pigmentation/pattern/material phenotype work. This pass should define how those systems coexist with anatomical variation, not redesign them.

## 7. Sex-related anatomy

Do not invent human sexual dimorphism.

For this phase, determine only:
- which visible skeletal/surface differences, if any, are justified by established Saurin biology;
- whether the current canon supports distinct dimorphic ranges;
- which questions remain genuinely unresolved.

If canon does not support a distinction, leave it open rather than manufacturing one.

Do not design external genital anatomy in this pass.

## 8. Combined-proportion stress testing

Single sliders passing is insufficient.

Build a matrix of deliberately difficult combinations, including:
- shortest + broadest frame;
- tallest + narrowest frame;
- long tail + minimum valid tail base;
- short tail + maximum valid base;
- longest rostrum + narrow cranial width;
- shortest rostrum + broad cranial width;
- maximum head proportion + narrow frame;
- minimum head proportion + broad frame;
- high muscle + low body fat;
- low muscle + high body fat;
- strongest allowed display + extreme cranial proportions;
- near-naked display + extreme cranial proportions.

Add additional combinations discovered during analysis.

For each, report PASS / CONSTRAIN / FAIL and why.

The goal is relationship-aware validity, not rectangular slider ranges.

## 9. Required deliverables

Produce:
1. `reviews/claude-saurin-creator-biology-variation.md`
2. a candidate parameter/coupling table suitable for later reconciliation into `specs/saurin/SAURIN_V1.md`;
3. identical-camera reference renders for neutral plus major single-variable extremes;
4. combined-extreme diagnostic sheets;
5. tail coupling diagnostics;
6. cranial identity diagnostics with displays disabled;
7. display-family range diagnostics;
8. a list of unresolved decisions that truly require author/canon resolution.

Include exact measurements wherever useful. Clearly distinguish:
- reference value,
- candidate soft distribution,
- hard validity boundary,
- unresolved value.

## 10. Stop conditions

This is still design validation.

Do **not** proceed to:
- UE5 implementation;
- production morph targets;
- skeleton/rig creation;
- animation;
- clothing/equipment fitting;
- final creator UI;
- gameplay modifiers;
- external sex anatomy;
- aging system implementation.

Do not modify the frozen reference model while developing variation. Derive diagnostics from it and report failures rather than silently repairing the reference.

## Author intent

We are transitioning from **one excellent Saurin** to **a system capable of producing thousands of distinct, credible Saurin**.

Variation is successful only when individuality increases without weakening racial anatomical identity.

Stop after the complete diagnostic package and await author review.

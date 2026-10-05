# Pass 2 — Roster-Wide Comparative & System Review Order

- **Author:** ChatGPT
- **Auditor:** Claude
- **Owner / final human authority:** Tyler
- **Phase:** DESIGN ONLY
- **Scope:** all 13 playable races
- **Prerequisite:** Pass 1 is complete; every playable race has an authoritative first-pass specification.
- **Implementation:** NO UE5 work is authorized by this order.

## 1. Purpose

Begin **Pass 2 — Roster-Wide Comparative & System Review**.

The objective is not to redesign thirteen races independently. Treat the complete roster as one biological and character-creation system and determine whether all accepted first-pass designs remain mutually coherent when compared directly.

The authoritative inputs are:

- `specs/<race>/<RACE>_V1.md` for every playable race;
- `decisions/PROJECT_RULES.md`;
- `specs/STATUS.md`;
- accepted comparative reviews and closure reports where needed to interpret the canonical specs.

Approved race specifications outrank old diagnostic artifacts. Do not reopen a closed race merely because an old review contains superseded wording.

## 2. Roster

Audit all thirteen together:

1. Marchfolk
2. Skarn
3. Sagekin
4. Fenn
5. Aelari
6. Vael
7. Halvren
8. Durrim
9. Grask
10. Gorrund
11. Pipkin
12. Cogling
13. Saurin

## 3. Audit principle

Pass 2 asks:

> **Does every race occupy a positive, internally coherent and mutually distinguishable biological design space while still supporting the project's shared character-creation system?**

Overlap is allowed and often desirable. A race does not need a unique value for every dimension. The failure condition is **identity collapse**, contradictory bounds, incompatible terminology, or a shared creator rule that cannot represent an approved race without distorting its biology.

Do not manufacture differences merely to make a comparison table cleaner.

## 4. Required audit tracks

### A. Stature and whole-body proportional space

Build a roster-wide comparison of:

- minimum/reference/maximum adult standing height;
- major body-proportion specialization;
- trunk contribution;
- limb contribution;
- skeletal mass/robusticity;
- frame behavior;
- center-of-mass implications where canonically established;
- any mandatory anatomical structures affecting silhouette or world space.

Identify legitimate overlaps and actual collisions.

Test equal-height comparisons wherever overlapping races could otherwise converge visually.

### B. Positive skeletal identity

For every race, state its strongest positive skeletal/anatomical identity carriers.

Then test whether those carriers survive removal or neutralization of:

- pigmentation;
- hair/presentation;
- clothing;
- cultural markers;
- class equipment;
- animation personality;
- non-biological effects.

Respect race-specific validation rules. In particular, do not remove mandatory biological structures merely to force a generic surface-neutral test.

Flag any race whose current identity depends primarily on stereotype, height alone, surface phenotype alone, or another race as the implicit baseline.

### C. Frame, composition and anatomy separation

Audit the four-layer creator model across the roster:

A. Biological Anatomy  
B. Skeletal Frame  
C. Physical Composition  
D. Personal Presentation

Check that:

- Narrow/Balanced/Broad are race-specific skeletal frames rather than uniform scaling;
- frame is not muscularity;
- muscularity is not fat;
- body-fat amount and distribution remain distinct;
- sex-related tendencies do not silently become frame or composition;
- biological traits do not leak into Presentation;
- valid combinations do not erase racial identity;
- no race is forced into one build.

### D. Sex-related anatomy consistency

Compare the thirteen race specs for:

- assumptions about human sexual dimorphism;
- sex-correlated distributions vs hard envelopes;
- overlap requirements;
- face/skull restrictions;
- stature/frame/muscle/fat restrictions;
- reproductive questions that remain intentionally OPEN.

Do **not** force one universal dimorphism model onto every race.

For Saurin, preserve the October 5 closure exactly: trunk-limited, low-to-moderate, overlapping, anti-hourglass sex-correlated tendencies; no craniofacial sex shift; reproductive biology remains OPEN.

### E. Craniofacial comparative architecture

Create a normalized roster-wide facial comparison using the accepted structural identities.

Audit:

- cranium/vault relationships;
- facial depth/projection;
- orbital organization;
- jaw architecture;
- nasal/rostral organization;
- ear/auricular architecture;
- neck-to-skull relationship;
- structural mass;
- race-defining non-overlap floors where explicitly canonical.

Pay special attention to populations that can approach one another at slider extremes.

Do not resolve the **Universal Facial Customization Architecture** yet. This track supplies its requirements.

### F. Surface phenotype

Compare:

- skin/integument architecture;
- pigmentation ranges;
- complexion behavior;
- scales or other non-human surfaces;
- hair/hair-equivalent biology;
- eye anatomy vs eye pigmentation/effects;
- markings;
- keratin/display systems.

Ensure surface phenotype strengthens anatomy without becoming a substitute for it.

Do not make Fenn the universal elven complexion baseline.

### G. Creator controls and randomization

Inventory race-specific creator requirements and identify:

1. genuinely universal controls;
2. controls shared by only some races;
3. race-specific controls;
4. biologically empty categories that must be hidden/replaced for particular races.

Audit:

- Simple Mode;
- Advanced Mode;
- presets as legitimate outputs of the same system;
- race-aware randomization;
- selective randomization;
- attribute locks;
- save/reuse appearance;
- NPC parity;
- combined-proportion validity.

Do not solve implementation architecture yet. Produce design requirements.

### H. Comparative terminology

Find terminology that is:

- used inconsistently between specs;
- comparative without naming a reference population;
- ambiguous between anatomy/frame/composition/presentation;
- inherited from obsolete prototype language;
- likely to produce implementation errors.

Recommend canonical terminology where needed without flattening meaningful race-specific anatomy.

### I. Cross-race collision matrix

Create a concise pairwise risk matrix or equivalent structured artifact covering all races.

Not every one of the 78 pairs requires equal prose. Prioritize meaningful collision risks, including:

- human populations against one another;
- Fenn/Aelari/Vael/Halvren;
- Durrim/Pipkin/Cogling;
- Grask/Gorrund;
- Saurin against humanoid populations at matched height;
- any additional collision discovered from the specs.

For each meaningful risk, identify the dimensions that preserve distinction.

### J. OPEN-item triage

Collect OPEN items from the canonical race specs and classify them:

- **Pass 2 blocking** — must be resolved for roster/system coherence;
- **later biological** — can remain open without blocking the shared creator design;
- **gameplay**;
- **equipment/world/camera**;
- **animation/rigging**;
- **technical/UE5**;
- **culture/presentation**.

Do not resolve an OPEN item merely because it exists.

## 5. Required outputs

Create a Pass 2 audit package in `reviews/`.

At minimum produce:

1. **Roster-wide comparative anatomy report**
2. **Cross-race collision matrix**
3. **Creator-system requirements report**
4. **Terminology/consistency report**
5. **OPEN-item triage**
6. **Final Pass 2 findings report**

You may split these into additional files if needed for clarity.

For every finding use severity:

- **BLOCKING CONTRADICTION**
- **MAJOR**
- **MINOR**
- **INFORMATIONAL**

Also identify the exact canonical spec section(s) involved.

## 6. Correction authority

Claude is the **auditor**, not the silent author of revised race canon.

You may:

- identify contradictions;
- trace superseded wording;
- demonstrate collisions;
- recommend corrections;
- correct obvious report-local transcription mistakes.

You must **not silently rewrite canonical race specifications** to resolve substantive design findings.

Return substantive findings to ChatGPT for author resolution.

If an apparent contradiction is already resolvable from authority hierarchy or newer canonical text, resolve it in the audit and explain why it is not a live contradiction.

## 7. Anti-regression rules

Pass 2 must preserve:

- all accepted positive racial identities;
- biological breadth within each race;
- no-uniform-scaling rule;
- culture/biology separation;
- anatomy/frame/composition/presentation separation;
- non-human anatomy where approved;
- overlapping phenotypes where canonically intended;
- combined-proportion validity;
- NPC/player parity;
- Simple and Advanced creator modes;
- race-aware randomization;
- saved/reusable appearances;
- current Saurin closures;
- the rule that every race may ultimately participate in the shared character system without being forced onto identical anatomy.

Do not homogenize the roster in the name of consistency.

## 8. Explicit exclusions

Do not begin:

- UE5 implementation;
- skeleton/rig production;
- animation;
- clothing or armor implementation;
- gameplay balance;
- class restrictions;
- racial stat balancing;
- crafting;
- world-building expansion;
- reproductive biology unless a genuine Pass 2 blocker is discovered.

Legacy gameplay traits may be catalogued where relevant but are not to be anatomically reverse-engineered during this review.

## 9. Final audit questions

Before returning the package, answer explicitly:

1. Are all thirteen races still positively distinguishable at their meaningful overlap points?
2. Does any race depend on height, attractiveness, culture, equipment, animation or surface phenotype as its primary identity?
3. Are any approved anatomical envelopes mutually contradictory?
4. Can the four-layer creator model represent all thirteen races without redefining their biology?
5. Are frame, composition, sex-related anatomy and presentation cleanly separated across the roster?
6. Which facial requirements must the future Universal Facial Customization Architecture support?
7. Which controls must be universal, conditional or race-specific?
8. Are there unresolved terminology collisions capable of causing later implementation mistakes?
9. Which OPEN items truly block the next design stage?
10. Did this audit discover any reason to reopen a race's first-pass completion?

## 10. Stop condition

Complete the audit package and self-audit it for cross-file consistency.

Then **STOP and return findings to ChatGPT**.

Do not edit canonical race specs, do not begin the Universal Facial Customization Architecture, and do not begin UE5 implementation until ChatGPT issues the next author order.

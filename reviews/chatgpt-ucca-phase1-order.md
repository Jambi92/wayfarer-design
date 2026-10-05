# ChatGPT — Universal Character Creation Architecture Phase 1 Order

**Author:** ChatGPT  
**For:** Claude (auditor / architecture analyst)  
**Phase:** DESIGN ONLY  
**Prerequisites:** All 13 race specs FIRST-PASS COMPLETE; Pass 2 FINAL-AUTHOR ACCEPTED / FROZEN; UFCA CLOSED / FINAL-AUTHOR ACCEPTED  
**Status:** BEGIN UCCA PHASE 1 — NON-FACIAL + WHOLE-CREATOR ARCHITECTURE

## 1. Mission

Begin the **Universal Character Creation Architecture (UCCA)** for the portions of character creation not already governed by the closed UFCA.

The goal is one coherent character-creation design for all 13 playable populations while preserving every approved population's biology.

UCCA must unify:
- creator flow;
- stature and body proportions;
- Skeletal Frame;
- Physical Composition;
- non-facial biological anatomy;
- skin / surface biology;
- hair and other population-specific homologous systems;
- age architecture;
- asymmetry and acquired history outside the face;
- Personal Presentation;
- presets, randomization and locks;
- saved/reusable appearances;
- validation;
- the interface boundary with UFCA.

This is **not** permission to make all populations share one skeleton, mesh, topology, morph set, body proportions, body-part vocabulary or range.

No UE5 implementation is authorized.

---

## 2. Authority

Use this order under the existing authority hierarchy:

1. canonical race specs;
2. PROJECT_RULES and closed UFCA where facial architecture is concerned;
3. accepted comparative reviews and explicit author resolutions;
4. decision register/history;
5. reviews/diagnostics;
6. prototype/implementation material.

Do not reopen Pass 1, Pass 2 or UFCA merely to make UCCA simpler.

Where UFCA already governs a facial concern, UCCA must integrate with it rather than duplicate or override it.

---

## 3. Non-negotiable principles

Preserve these project rules:

1. **Race defines biological foundation; customization creates the individual; Presentation creates personal/cultural expression.**
2. Biological Anatomy, Skeletal Frame, Physical Composition and Personal Presentation remain distinct layers.
3. Skeletal Frame is not body type and not composition.
4. Muscle and body fat are not skeletal scale.
5. Body-fat amount and distribution remain distinct.
6. No uniform whole-body scaling as a substitute for approved stature/proportional anatomy.
7. Culture, occupation, class, personality and reputation are not biology.
8. Chronological Age, Apparent Biological Age and Age Presentation remain distinct.
9. Sex is a distribution influence where canon authorizes it, never a body preset/package; R-SEX remains authoritative.
10. Individual cosmetic variation does not automatically grant gameplay advantages/penalties.
11. Presets are valid outputs of the same system as custom characters and NPCs.
12. Simple Mode and Advanced Mode use the same underlying appearance architecture.
13. Biological and Presentation randomization remain separate.
14. Selective randomization and locks are required.
15. Rare valid phenotypes remain manually creatable.
16. Combined-proportion validity is relationship-aware.
17. Surface phenotype overlap never makes populations anatomically interchangeable.
18. Population-level correlation does not automatically create a hard control dependency.
19. Anatomical Resting Alignment is distinct from Cultural/Personal Body Language.
20. Character-design requirements determine later technical architecture; implementation convenience cannot redefine approved anatomy.
21. Equipment dimensions do not automatically scale with the holder.
22. A universal creator category is navigation/organization, not authorization for anatomy.
23. UFCA remains closed and authoritative for facial creator organization.

---

## 4. Roster

Cover all 13 playable populations:

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

Pay special attention to:
- the three distinct elf populations;
- Halvren mixed developmental inheritance;
- Durrim compact structural concentration;
- Grask elongated leverage/reach;
- Gorrund massive load-bearing architecture;
- Pipkin light compact adult proportionality;
- Cogling fine-scale distal articulation;
- Saurin Counterbalanced Pelvic-Axial Architecture, mandatory tail, Regional Scale Architecture and non-human sex-related anatomy.

---

## 5. UCCA-01 — Whole-Roster Requirements Extraction Matrix

Extract the canonical creator requirements for every population.

At minimum inspect and classify:

### A. Stature and proportions
- standing-height range/reference;
- height distribution;
- torso length/depth/width relationships;
- limb length and segment proportions;
- shoulder/pelvic relationships;
- neck;
- hands/feet;
- reach-related anatomy;
- posture/resting alignment;
- population-specific axial structures;
- Saurin tail and tail-base integration.

### B. Skeletal Frame
- frame dimensions;
- robusticity;
- joint scale;
- bone breadth/depth;
- Narrow/Balanced/Broad preset implications;
- any correlations that are tendencies rather than dependencies.

### C. Physical Composition
- muscular-development capacity;
- current muscularity;
- body-fat amount;
- body-fat distribution;
- soft-tissue fullness;
- population-specific tissue systems;
- Saurin E/B anatomy and anti-hourglass rules.

### D. Biological surface
- skin/integument family;
- pigmentation;
- patterning;
- scales or homologous surface structures;
- regional variation;
- material/finish biology;
- natural vs environmental vs applied vs acquired layers.

### E. Hair / homologous structures
- scalp hair;
- body hair;
- facial hair where not already controlled by UFCA;
- eyebrows interface with UFCA;
- Saurin cranial keratin/display interface;
- other population-specific homologues.

### F. Age
- adult creator scope;
- Apparent Biological Age effects outside the face;
- systemic aging;
- age-related posture/composition/surface changes;
- explicit OPEN lifecycle questions.

### G. Sex-related anatomy
- only canonical tendencies;
- hard-bound equality under R-SEX unless explicit canon differs;
- population-specific non-human anatomy;
- reproductive biology kept separate unless already canon.

### H. Asymmetry and acquired history
- natural body asymmetry;
- scars/injuries;
- missing/damaged structures where authorized;
- acquired surface history;
- Saurin tail injury/loss remains OPEN unless canon says otherwise.

### I. Presentation
- hair styling;
- cosmetics/paint;
- markings;
- grooming;
- body-language/resting-pose presentation;
- clothing/gear preview only as creator presentation where appropriate;
- culture/background presentation separated from biology.

### J. Creator-system requirements
- presets;
- Simple/Advanced;
- randomization;
- locks;
- saved appearance;
- NPC parity;
- first-person geometry requirement if canonically relevant;
- validation;
- known OPEN/DEFERRED items.

Classify every extracted item as:
- anatomical requirement;
- creator-facing direct control;
- derived/coupled variable;
- SOFT tendency/correlation;
- validator-only;
- latent preset/randomization variable;
- Presentation;
- diagnostic/measurement only;
- OPEN / not authorized.

Do not infer missing biology.

---

## 6. UCCA-02 — Proposed Universal Creator Navigation

Propose the smallest coherent navigation hierarchy that can represent all 13 populations.

Evaluate, rather than blindly adopt, a structure such as:

0. Starting Character / Presets
1. Stature & Global Proportions
2. Skeletal Frame
3. Torso & Axial Structure
4. Shoulders / Upper Body
5. Pelvis / Lower Body
6. Arms & Hands
7. Legs & Feet
8. Physical Composition
9. Population-Specific Anatomy
10. Skin / Integument
11. Hair / Biological Display
12. Face — route into closed UFCA
13. Age
14. Asymmetry & Acquired History
15. Presentation

Claude must determine:
- which categories are truly universal;
- which are conditional;
- which require population-specific labels/bindings;
- which should be nested rather than top-level;
- which must be absent for some populations;
- whether Saurin tail requires its own top-level creator category;
- whether body hair belongs with Hair, Surface, or a conditional biological slot;
- how Halvren genealogy enters the creator without becoming a body slider.

Shared navigation must never imply shared anatomy.

---

## 7. UCCA-03 — Control Taxonomy & Dependency Model

Create the non-facial equivalent of UFCA's control discipline.

Every proposed body/creator variable must be classified as:
- DIR — direct anatomical control;
- DER — derived/coupled;
- SOFT — tendency/correlation;
- VAL — validator-only;
- LAT — preset/randomization latent variable;
- PRES — Presentation;
- DIAG — diagnostic/measurement.

Define relationship behaviors compatible with UFCA:
- FOLLOW;
- OFFSET;
- CLAMP;
- NEIGHBOR-ADJUST;
- ENVELOPE;
- REDISTRIBUTE only where explicitly authorized;
- INVALID.

Specifically prevent:
- one body-size slider scaling the whole character;
- height silently scaling head/hands/feet/width/depth;
- frame silently changing muscle/fat;
- muscle/fat silently changing skeleton;
- sex becoming a body package;
- age becoming a frailty package;
- ancestry becoming a Halvren body-percentage slider;
- race becoming a hidden global morph axis;
- “athletic,” “slim,” “heavy,” etc. becoming persistent hidden macro states after editing.

Determine how presets may write ordinary regional values without leaving hidden state.

---

## 8. UCCA-04 — Stature & Proportional Architecture

Develop the universal design architecture for stature without uniform scaling.

Must cover:
- absolute stature;
- population-specific valid ranges;
- stature distribution;
- segment contribution;
- torso vs limb contribution;
- arm/leg proportions;
- hand/foot scale;
- head-to-stature as deferred where not authored;
- shoulder/pelvis relationships;
- extreme-height validity;
- equal-height cross-population boundary testing.

Answer how a player changes height while preserving a biologically valid member of that population.

Do not invent numeric segment distributions.

Where reference-mesh measurements are required, define semantic variables and queue them rather than fabricating values.

---

## 9. UCCA-05 — Skeletal Frame Architecture

Resolve the universal design meaning of **Skeletal Frame**.

Requirements:
- continuous anatomy;
- Narrow / Balanced / Broad are editable starting presets, not castes;
- frame must not be synonymous with sex, body type, muscularity, fatness or stature;
- frame may influence several skeletal dimensions only where anatomically coherent;
- correlated dimensions remain independently editable where canon allows;
- no hidden permanent frame state after regional edits unless explicitly justified.

Audit the earlier Manny/Quinn placeholder problem and ensure UCCA supersedes it at the design level without making an implementation choice.

Define population-specific binding needs for frame, including Saurin.

---

## 10. UCCA-06 — Physical Composition Architecture

Create the architecture for:
- muscular-development capacity;
- current muscularity;
- body-fat amount;
- body-fat distribution;
- soft-tissue fullness;
- regional composition;
- population-specific composition systems.

Explicitly distinguish:
**capacity ≠ current muscularity ≠ fat amount ≠ fat distribution ≠ skeletal frame.**

Determine how an **Athletic** starting preset can exist without becoming a hidden anatomical layer or forbidden skeleton/composition bundle.

Carry Saurin sex-related E/B anatomy correctly and preserve anti-hourglass canon.

Do not infer gameplay strength from visual muscularity.

---

## 11. UCCA-07 — Surface / Hair / Age / Presentation Architecture

Propose the whole-body architecture for:

### Surface
Natural / Environmental / Applied / Acquired layers.

### Hair and homologues
Population-specific biological hair/display structures; styling separated from biology; interface with UFCA facial hair/brows and Saurin display.

### Age
Chronological Age / Apparent Biological Age / Age Presentation separation; body and face age driver interface; no automatic frailty.

### Presentation
Culture/background/personal styling, markings, grooming and body-language presentation without rewriting anatomy.

Define where controls live and which systems are shared vs population-bound.

---

## 12. UCCA-08 — Presets, Randomization, Locks & Saved Appearance

Integrate the full creator workflow.

### Simple Mode
Race → legitimate preset → Confirm, with only canonically necessary conditional steps.

### Advanced Mode
Race → Starting Character/Preset → Customize → Confirm.

Requirements:
- presets are ordinary valid appearance records;
- no preset-only anatomy;
- preset families may provide useful starting points but cannot remain hidden states;
- whole-character and selective randomization;
- locks by category/region/attribute;
- Biological vs Presentation randomization;
- Subtle / Diverse / Extreme behavior should remain compatible with UFCA;
- internal Very Common / Common / Uncommon / Rare weighting where applicable;
- rare valid phenotypes manually creatable;
- seeded reproducibility may be retained as design requirement;
- saved appearances include all resolved creator values necessary to reproduce the character;
- reusable appearances must not depend on a temporary preset identifier;
- NPCs use the same valid appearance system;
- randomization validates rather than rolling invalid anatomy and cosmetically repairing it.

Audit the current saved-appearance gap:
frame, height, composition, face, skin, hair, markings and other required systems must be representable in the eventual appearance record.

Do not decide implementation serialization format.

---

## 13. UCCA-09 — Whole-Character Validation Framework

Create validation tiers covering:

A. Intra-population validity  
B. Cross-population boundary validity  
C. Relationship validity  
D. Extreme-combination stress  
E. Neutralization / identity persistence  
F. Age / sex / asymmetry  
G. Preset/randomization diversity  
H. Stature/proportion validity  
I. Frame/composition independence  
J. Surface/presentation separation  
K. Whole-character integration with UFCA

Carry forward every existing permanent body/race test.

Required stress tests include:
- minimum/maximum stature;
- narrow/broad frame at stature extremes;
- low/high muscularity and fat combinations;
- segment extremes;
- equal-height neighboring populations;
- neutral presentation;
- randomized batches;
- saved appearance round trip;
- Simple → Advanced equivalence;
- Saurin tail/body coupling;
- Halvren mixed-development validity;
- no-race-identity collapse after removing hair, clothing and presentation.

No visual stereotype may substitute for anatomical validity.

---

## 14. UCCA-10 — OPEN / Deferred / Author-Decision Register

Collect every issue that UCCA cannot safely resolve from canon.

At minimum audit:
- head-to-stature measurements;
- population segment distributions;
- Grask/Gorrund ear ranges only insofar as whole-character measurement touches them;
- Saurin tail-base/length/mass coupling;
- Saurin partial garment coverage;
- acquired Saurin tail loss/injury;
- Saurin thermoregulation;
- reproductive biology;
- lifecycle questions;
- statistical calibration;
- saved-appearance schema implementation;
- body technical architecture;
- animation/locomotion implications;
- equipment fit implications;
- first-person body geometry implementation;
- any class/gameplay trait that should remain outside creator biology.

Separate:
- genuine author decision;
- biological OPEN;
- measurement-deferred;
- implementation-deferred;
- later gameplay review.

Do not resolve an OPEN item merely because UCCA would be cleaner if it were resolved.

---

## 15. UCCA-11 — Phase 1 Architecture Audit

Audit UCCA-01…10 against all 13 race specs, PROJECT_RULES and closed UFCA.

Answer:

1. Does every approved non-facial creator requirement have a home?
2. Did universalization weaken any population's positive body identity?
3. Did any Pass 1 requirement disappear without disposition?
4. Did any OPEN item get silently resolved?
5. Did any diagnostic measurement become a player control?
6. Did any control become hidden ancestry/culture/personality/gameplay?
7. Are Simple and Advanced both fully supported?
8. Are presets legitimate outputs?
9. Are saved/reusable appearances conceptually complete?
10. Is uniform scaling eliminated as the design model?
11. Are Frame and Composition genuinely independent?
12. Is height relationship-aware rather than whole-body scale?
13. Are R-SEX and age separation preserved?
14. Is Halvren supported without a percentage body slider?
15. Is Saurin supported without humanizing its body architecture?
16. Does the body architecture integrate cleanly with closed UFCA?
17. Are population-specific surface/hair systems preserved?
18. Are technical/UE5 decisions still deferred?
19. What author decisions are required before canonicalization?
20. Did any proposed universal rule conflict with frozen Pass 2 or closed UFCA?

If a conflict exists, identify it precisely. Do not silently rewrite canon.

---

## 16. Deliverables — exact order

Create Phase 1 review documents in this order:

1. **UCCA-01 — Whole-Roster Requirements Extraction Matrix**
2. **UCCA-02 — Proposed Universal Creator Navigation**
3. **UCCA-03 — Control Taxonomy & Dependency Model**
4. **UCCA-04 — Stature & Proportional Architecture**
5. **UCCA-05 — Skeletal Frame Architecture**
6. **UCCA-06 — Physical Composition Architecture**
7. **UCCA-07 — Surface / Hair / Age / Presentation Architecture**
8. **UCCA-08 — Presets, Randomization, Locks & Saved Appearance**
9. **UCCA-09 — Whole-Character Validation Framework**
10. **UCCA-10 — OPEN / Deferred / Author-Decision Register**
11. **UCCA-11 — Phase 1 Architecture Audit**

Use clear filenames under `reviews/`, e.g. `claude-ucca-01-...`.

Evidence appendices/subfiles are allowed where the roster matrix becomes too large.

---

## 17. Editing restrictions

During UCCA Phase 1:

- **Do not rewrite the 13 canonical race specs.**
- **Do not rewrite UFCA_V1.**
- **Do not rewrite PROJECT_RULES unless ordered later.**
- **Do not update STATUS to claim UCCA completion.**
- Put analysis/proposals in new review files.
- Flag proposed canonical rules for ChatGPT author acceptance.
- Preserve Pass 1, frozen Pass 2 and closed UFCA as authoritative.

---

## 18. Stop conditions

Proceed autonomously through UCCA-01…11.

Stop early only if:
- two approved population requirements genuinely cannot coexist in one creator architecture;
- proceeding requires changing approved biology;
- an OPEN biological question must be answered first;
- a frozen Pass 2 or closed UFCA rule would have to be violated.

Otherwise complete Phase 1.

After UCCA-11, **STOP for ChatGPT author review**.

Do not canonicalize UCCA in Phase 1.
Do not begin a Phase 2 order yourself.
Do not begin UE5 implementation, rigging, morph construction, animation, camera work, clothing/armor implementation, equipment fitting or gameplay balancing.

— ChatGPT, Author

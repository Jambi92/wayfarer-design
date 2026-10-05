# Project Rules and Decision Register

## Status
Canonical shared rules for Wayfarer first-pass character design.

## Character creation
- Race/population defines biological foundation; customization creates the individual; presentation creates identity.
- Simple Mode: Race -> Preset -> Confirm.
- Advanced Mode: Race -> Preset -> Customize -> Confirm.
- Presets are valid outputs of the same system as custom characters and NPCs.
- Race-aware and selective randomization are required.
- Biological Anatomy, Skeletal Frame, Physical Composition, and Personal Presentation remain conceptually separate.
- Narrow/Balanced/Broad frame presets are editable starts, not castes.
- Current Muscularity, Body-Fat Amount, and Body-Fat Distribution remain separate.
- Culture, occupation, personality, class, and presentation are not biological traits.
- Chronological Age, Apparent Biological Age, and Age Presentation are distinct.
- Combined-proportion validity is mandatory; individually valid controls may form invalid combinations.
- Population correlations normally use weighted distributions/conditional probabilities/validity envelopes rather than hard creator dependencies.
- Different populations may overlap in surface phenotype without becoming anatomically interchangeable.
- Biological appearance is distinct from observed lighting and environmental appearance.
- Anatomical Resting Alignment is distinct from Cultural/Personal Body Language.

## Technical authority
- Character design requirements determine later technical architecture.
- World compatibility is validated against approved target anatomy, not prototype-reachable anatomy.
- Canonical equipment dimensions do not automatically scale with the holder.
- Visual anatomy, equipment dimensions, collision, interaction reach, combat reach, and camera/targeting reach must not be assumed to be one system.
- Retargeting/IK/animation architecture must adapt to approved anatomy rather than redefine it.
- Current prototype race scales, uniform whole-body scaling, shared-human-animation assumptions, class restrictions, and racial stats remain non-authoritative unless explicitly approved.

## Facial architecture status
Race-specific facial control organizations are **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION**.
Do not delete them. A universal facial-customization architecture review occurs after all 13 playable races complete first-pass design.

## Reviews
- Short-Race Comparative Anatomy Review (Durrim, Pipkin, Cogling) — ACCEPTED / COMPLETE (`reviews/short-race-comparative-anatomy-v1.md`).
- Large-Race Comparative Anatomy Review (Skarn, Grask, Gorrund) — performed in the Pass 2 resolution sequence (`reviews/claude-pass2-r2-large-race-comparative-review.md`); narrowly scoped author decisions pending.
- Universal Facial Customization Architecture Review — required; begins only after the Pass 2 resolution sequence is closed.
- Implementation-level prototype conflict audits when project files are accessible.

## Authority hierarchy (adopted October 5, 2026 — Pass 2 resolution order)
1. Approved canonical race specifications (`specs/<race>/<RACE>_V1.md`).
2. `decisions/PROJECT_RULES.md`.
3. Accepted cross-race comparative reviews and explicit author resolutions.
4. `register/decision-register.md` — supporting decision history only; historical until reconciled.
5. Other reviews and diagnostics.
6. Prototype / implementation material (including `rules/character-creation-brief.md` where it conflicts with canon).

Later explicit author resolutions supersede older text at the same level. Terminology normalization never rewrites a race's positive anatomical identity.

## Terminology (adopted October 5, 2026)
- **Population** = biological population; **playable lineage / creation category** = playable classification; **culture** = cultural identity; **social identity** = social identity. Genealogy/ancestry stays distinct from playable classification.
- Unqualified **human** in an anatomical comparison means the **Marchfolk Human Reference Population at matched normalized height**.
- **Baseline** is retired where it means a comparator (use **Human Reference Population**), a population centre (use **central tendency**) or a design default (use **first-pass default**).
- **Simple Mode / Advanced Mode** are the creator modes; "Basic" is not a synonym for Simple Mode.
- **Narrow / Balanced / Broad** are reserved for Skeletal Frame. **Skeletal Frame** = the continuous domain; **Frame Preset** = an editable starting point.
- **Muscular Development Capacity** (Biological Anatomy) stays distinct from **Current Muscularity** (Physical Composition).
- **Skin Appearance Layers:** Natural / Environmental / Applied / Acquired.
- **Sex-related anatomy** = the biological category; **sex-related tendency** = a distribution shift. "Anatomy configuration" / "body configuration" are retired where they mean this category.
- Saurin: **structural ridge/plane** = skull anatomy, mandatory, never toggled; **keratin ridge** = optional cranial-display expression; "ridge-absent" means **keratin-ridge-absent / naked display**.
- Race-specific anatomical terms (e.g. Saurin rostrum, Gorrund Transverse Structural Continuity, Pipkin Low-Set Compact Trunk Architecture) are preserved.

## Sex-related anatomy rule — R-SEX (adopted October 5, 2026)
- Hard biological validity bounds remain available to either sex unless a race's canon explicitly establishes otherwise.
- Adult phenotype overlap is mandatory.
- Sex is never a body preset or package and never forces frame, stature, muscularity, body-fat amount or distribution, face, displays, coloration, personality, culture or presentation unless explicit race canon defines a tendency.
- Per-race sex-conditioned soft distributions are allowed; "no shift" is a valid complete state for a race.
- Reproductive biology is never inferred from creator architecture.
- Existing deliberate Saurin sex-related canon (SAURIN_V1 §263) remains intact and is not generalized to other races.

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
The **Universal Facial Customization Architecture (UFCA)** is canonical in `decisions/UFCA_V1.md` (UFCA Phase 2, October 5, 2026). It governs facial creator organization; race specs govern each population's anatomy.
Race-specific facial control organizations (formerly **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION**) are kept, not deleted: their requirements are preserved and routed to UFCA slots.
Universal UFCA rules (details in `decisions/UFCA_V1.md`):
- Navigation slots are not anatomy; each population binds a slot as Bound, Bound-locked or Absent. Absent anatomy is hidden, never a dead control. A shared slot never by itself authorizes a control.
- No master or whole-face sliders (face shape/width/length/depth, elfness, humanity, masculinity, femininity, beauty, ancestry percentage) and no broad relationship tools in v1.
- Diagnostic measurements and indices never become sliders because they are measurable; latent generation variables are never player-facing.
- Combined validity outcomes are PASS / CONSTRAIN / FAIL. CONSTRAIN is reported and biologically deterministic; locks are absolute; no silent reset.
- Eye "size" means bony orbit size + visible aperture; eyeball size is derived from the orbit.
- Randomization strengths Subtle / Diverse / Extreme are all biologically valid; Extreme samples valid tails only. Internal frequency vocabulary Very Common / Common / Uncommon / Rare describes weighting, never validity.
- Natural asymmetry is distinct from Acquired history; Naturalize Face remains provisional.

## Reviews
- Short-Race Comparative Anatomy Review (Durrim, Pipkin, Cogling) — ACCEPTED / COMPLETE (`reviews/short-race-comparative-anatomy-v1.md`).
- Large-Race Comparative Anatomy Review (Skarn, Grask, Gorrund) — ACCEPTED / COMPLETE (`reviews/claude-pass2-r2-large-race-comparative-review.md`; author decisions AD-1–AD-5, October 5, 2026, reconciled into the Skarn, Grask and Gorrund specs).
- Pass 2 Roster-Wide Comparative & System Review — **CLOSED / FINAL-AUTHOR ACCEPTED / FROZEN** (October 5, 2026; `reviews/claude-pass2-closure-canonicalization.md`, `reviews/chatgpt-pass2-final-author-acceptance-freeze-order.md`).
- Universal Facial Customization Architecture Review — Phase 1 **ACCEPTED** (`reviews/claude-ufca-01…08`); Phase 2 canonicalization completed in `decisions/UFCA_V1.md` (`reviews/claude-ufca-phase2-canonicalization-report.md`); **CLOSED / FINAL-AUTHOR ACCEPTED** October 5, 2026 (`reviews/claude-ufca-final-closure-report.md`). Uses `reviews/claude-pass2-r3-craniofacial-framework.md` as its cross-race comparison/measurement framework (not creator controls).
- Implementation-level prototype conflict audits when project files are accessible.

## Authority hierarchy (adopted October 5, 2026 — Pass 2 resolution order)
1. Approved canonical race specifications (`specs/<race>/<RACE>_V1.md`).
2. `decisions/PROJECT_RULES.md`, with `decisions/UFCA_V1.md` as its facial-creator companion (UFCA governs facial creator organization; race specs govern anatomy).
3. Accepted cross-race comparative reviews and explicit author resolutions.
4. `register/decision-register.md` — supporting decision history only; historical until reconciled.
5. Other reviews and diagnostics.
6. Prototype / implementation material (including `rules/character-creation-brief.md` where it conflicts with canon).

Later explicit author resolutions supersede older text at the same level. Terminology normalization never rewrites a race's positive anatomical identity.

## Terminology (adopted October 5, 2026)
- **Population** = biological population; **playable lineage / creation category** = playable classification; **culture** = cultural identity; **social identity** = social identity. Genealogy/ancestry stays distinct from playable classification.
- Unqualified **human** in an anatomical comparison means the **Marchfolk Human Reference Population at matched normalized height**.
- **Near-human** means within the Marchfolk adult anatomical envelope at normalized height, unless a specific spec explicitly defines a narrower comparison (Pass 2 AC-1).
- **Baseline** is retired where it means a comparator (use **Human Reference Population**), a population centre (use **central tendency**) or a design default (use **first-pass default**). Saurin's defined species-anatomy sense of "baseline" (SAURIN_V1 §157) is retained (Pass 2 AC-2).
- **Simple Mode / Advanced Mode** are the creator modes; "Basic" is not a synonym for Simple Mode.
- **Narrow / Balanced / Broad** are reserved for Skeletal Frame. **Skeletal Frame** = the continuous domain; **Frame Preset** = an editable starting point.
- **Muscular Development Capacity** (Biological Anatomy) stays distinct from **Current Muscularity** (Physical Composition).
- **Skin Appearance Layers:** Natural / Environmental / Applied / Acquired. Ordinary dirt and other transient accumulation are **Environmental**; Applied is deliberate paint/cosmetic application; Acquired is scars, damage and persistent acquired change (Pass 2 AC-3).
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

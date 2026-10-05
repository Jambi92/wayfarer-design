# ChatGPT — Pass 2 Resolution Sequence Order

**Author:** ChatGPT (author)
**For:** Claude (auditor)
**Phase:** Design only
**Basis:** Claude Pass 2 reports 01–06
**Status:** AUTHOR ORDER

## 1. Purpose

Pass 2 found no blocking contradiction and no completed race is to be reopened. This order resolves the cross-roster/system findings that must be closed before the Universal Facial Customization Architecture (UFCA) and universal creator-control review.

Do not begin UE5 implementation.

## 2. Authority decisions — adopt now

Use this authority hierarchy for this work:

1. Approved canonical race specifications
2. `decisions/PROJECT_RULES.md`
3. Accepted cross-race comparative reviews / explicit author resolutions
4. `register/decision-register.md` as supporting decision history
5. Other reviews and diagnostics
6. Prototype/implementation material

Later explicit author resolutions supersede older text at the same authority level. Do not silently rewrite a race's positive anatomical identity merely to normalize terminology.

Treat the stale decision register as historical/supporting until it is reconciled. Add a clear status/precedence notice rather than allowing it to compete with current canon.

## 3. Terminology decisions — adopt

Implement the following without flattening race-specific anatomical vocabulary:

- **population** = biological population.
- **playable lineage / creation category** = playable classification.
- **culture** = cultural identity.
- **social identity** = social identity.
- Genealogy/ancestry remains distinct from playable classification.
- Unqualified **human** in anatomical comparison means the **Marchfolk Human Reference Population at matched normalized height**.
- Retire ambiguous **baseline** where it means comparator or population centre:
  - use **Human Reference Population** for comparator;
  - **central tendency** for population centre;
  - **first-pass default** for a design default.
- Reserve **Simple Mode / Advanced Mode** for creator modes. Do not use Basic as a synonym for Simple Mode.
- Saurin:
  - **structural ridge/plane** = skull anatomy, mandatory/not toggled;
  - **keratin ridge** = optional cranial-display expression;
  - replace ambiguous “ridge-absent” with **keratin-ridge-absent / naked display**.
- Standardize Skin Appearance Layers as **Natural / Environmental / Applied / Acquired**.
- Add **Muscular Development Capacity** to Biological Anatomy; keep it distinct from **Current Muscularity** in Physical Composition.
- Use **sex-related anatomy** for the biological category and **sex-related tendency** for distribution shifts. Retire anatomy/body configuration where it means this category.
- Reserve Narrow / Balanced / Broad for Skeletal Frame.
- Use **Skeletal Frame** for the continuous domain and **Frame Preset** for an editable starting point.
- Preserve race-specific terms such as Saurin rostrum, Gorrund Transverse Structural Continuity, Pipkin Low-Set Compact Trunk Architecture, etc.

## 4. Universal sex-related anatomy rule — adopt R-SEX

Canonize the architecture rule, not universal numeric dimorphism:

- Hard biological validity bounds remain available to either sex unless a race's canon explicitly establishes otherwise.
- Adult phenotype overlap is mandatory.
- Sex is never a body preset/package and must not force frame, stature, muscularity, body-fat amount/distribution, face, displays, coloration, personality, culture, or presentation unless explicit race canon defines a tendency.
- Per-race sex-conditioned soft distributions are allowed.
- “No shift” is a valid complete state for a race.
- Reproductive biology is not inferred from creator architecture.
- Existing deliberate Saurin sex-related canon remains intact and is not generalized to other races.

Audit existing specs for wording conflicts with this rule, but do not invent per-race dimorphism magnitudes.

## 5. Large-Race Comparative Anatomy Review — perform next

Perform the missing comparative review for **Skarn / Grask / Gorrund**.

Required tests:

1. Compare all three at matched normalized height wherever their valid stature envelopes overlap.
2. Establish positive anatomical carriers for each population independent of absolute height:
   - Skarn: human-derived robust/powerful skeletal architecture;
   - Grask: elongated skeletal leverage and reach;
   - Gorrund: massive load-bearing non-human architecture / axial load-path continuity.
3. Specifically resolve the 208–229 cm Skarn–Gorrund overlap.
4. Verify a low-end Gorrund cannot collapse into a large Skarn and a short-limbed Grask cannot collapse into either.
5. Compare:
   - torso share;
   - thoracic breadth/depth;
   - shoulder architecture;
   - pelvic architecture;
   - arm/leg contribution;
   - forearm/lower-leg contribution;
   - joint scale;
   - hand/foot structure;
   - skeletal structural presence;
   - head/neck relationship;
   - posture-independent silhouette carriers.
6. Do not invent arbitrary numeric envelopes merely to finish the review. If canon supports only directional relationships, state them and identify which numeric validators must later come from approved reference meshes.
7. Return explicit PASS/FAIL collision tests and any narrowly scoped author decisions needed.

This review may clarify relationships but must not redesign the three races unless a genuine contradiction is discovered.

## 6. Common craniofacial comparison framework — design after Large-Race review

Create a **common normalized craniofacial landmark and metric framework** suitable for UFCA cross-race comparison.

It must:
- work for human, elf, Halvren, Durrim, Grask, Gorrund, Pipkin, Cogling and Saurin anatomy without forcing human facial topology onto non-human races;
- define landmarks/indices for projection, cranial proportions, orbit relationship, jaw depth/projection and other cross-race comparisons where anatomically meaningful;
- distinguish universal comparison landmarks from race-specific creator controls;
- support Saurin's provisional rostral-index floor and the future Marchfolk/Grask/Gorrund projection distributions;
- not fabricate missing projection distributions.

Then audit Saurin's requirement that its rostral floor remain outside Marchfolk/Grask/Gorrund approved ranges. If those source ranges still cannot be derived legitimately, leave the cross-race numeric closure OPEN and specify exactly what reference-mesh measurements are required. Do not weaken Saurin identity merely because comparison data are absent.

## 7. Conforming cleanup

After the above reviews, prepare author-reviewable conforming edits for:
- Skarn “natural muscle volume” -> **Muscular Development Capacity** where appropriate;
- comparator wording under the Marchfolk Human Reference Population rule;
- Saurin structural-ridge vs keratin-ridge terminology;
- four Skin Appearance Layers;
- stale process/status wording;
- stale character-creation brief: mark superseded; do not let it override approved specs;
- process tokens accidentally left in Saurin canon: replace with spec-defined language;
- stale OPEN items already resolved by later canon;
- Gorrund validation-prefix inconsistency and ambiguous Part.§ citations where useful.

Do not mass-rewrite race specs for style. Change only text needed to remove ambiguity, stale authority, or implementation risk.

## 8. Numeric identity envelopes

Do **not** invent numbers for Pipkin–Cogling, Skarn, Grask, Gorrund or other races merely because Pass 2 identified qualitative boundaries.

Create a **Reference-Mesh Measurement Queue** listing the numeric validators that must be derived once approved race reference meshes exist. Saurin's measured Part 7 approach is the model: derive diagnostic envelopes from accepted anatomy, then validate creator bounds.

Qualitative design can close now where the identities are structurally distinct; implementation validators remain deferred until measured.

## 9. Deliverables

Return this sequence:

1. **Pass 2 Authority & Terminology Resolution Report**
2. **Large-Race Comparative Anatomy Review — Skarn / Grask / Gorrund**
3. **Common Craniofacial Landmark & Metric Framework**
4. **Pass 2 Conforming-Edit Plan** with exact files/sections and proposed changes
5. **Reference-Mesh Measurement Queue**
6. **Pass 2 Closure Audit** mapping every Claude F-xx finding to:
   - RESOLVED;
   - RESOLVED BY AUTHORITY / conforming edit pending;
   - DEFERRED WITH NAMED INPUT;
   - genuinely OPEN.
7. Update `specs/STATUS.md` only after the closure audit establishes the actual state.

## 10. Stop conditions

Stop and return to ChatGPT if:
- a proposed resolution would materially redesign an approved race;
- the Large-Race review finds a genuine anatomical contradiction;
- a craniofacial metric cannot compare populations without imposing the wrong anatomy;
- a missing number would have to be invented.

Otherwise proceed autonomously through the entire sequence, self-audit, and correct non-substantive failures without asking for approval.

**Do not begin UFCA until this Pass 2 resolution sequence is closed.**
**Do not begin UE5 implementation, rigging, animation, clothing/armor implementation, or technical production.**

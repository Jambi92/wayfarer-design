# Audit: Pipkin v1.0 Part 2

**Auditor:** Claude
**Audited file:** `specs/pipkin/PIPKIN_V1.md` at commit `cb3510e`
**Compared against:**
- `races/11-pipkin.md`, the full approved Parts 1–2 text migrated from the Claude Docs plan
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- `rules/character-creation-brief.md`
- the completed Durrim, Marchfolk, Fenn, Aelari and Grask specs

These are findings, not changes. Neither spec file was edited. ChatGPT resolves any finding that Tyler accepts.

## 1. Result

**PASS WITH CLARIFICATIONS**

- **Design:** there is no blocking design contradiction. Low-Set Compact Trunk Architecture is a sound positive anchor.
- **Repository (needs a decision before Part 3):** `specs/pipkin/PIPKIN_V1.md` is a condensed copy of the approved Parts 1–2. It drops a number of approved requirements (see §2). It also exists alongside `races/11-pipkin.md`, so there are now two candidate authoritative Pipkin files.

## 2. Contradictions

### Design contradictions

None.

Every statement in `PIPKIN_V1.md` agrees with the full approved text and with project rules. Checks that passed:
- stature
- the adult-read requirement
- what "light" construction means
- the Durrim contrast
- head and feet being secondary
- pelvic breadth not standing in for sex, fat or muscle
- composition separation
- the legacy sneak trait
- equipment and world not scaling

### Fidelity gap

This is not a contradiction, but it would become one by omission. `PIPKIN_V1.md` presents itself as the Pipkin v1.0 spec. `WORKFLOW.md` makes `specs/` the place ChatGPT authors and revises. If it becomes canonical as it stands, these approved Part 1–2 requirements silently stop being part of the spec.

**Validation set**
- PIP-BODY-01 to PIP-BODY-14 are omitted entirely. That includes:
  - the reference body
  - the minimum-height anti-child test (PIP-BODY-02)
  - the Broad Pipkin vs Narrow Durrim body (PIP-BODY-14)
- PIP-STRESS-01 to PIP-STRESS-10 are collapsed into one line, so their configurations are lost. Two of them are the sex-coding and hip-width safeguards:
  - STRESS-06: greater pelvis with lower thorax.
  - STRESS-07: lower pelvis with greater thorax.
- Three tests are missing:
  - The Marchfolk-similar frame stress test.
  - The lower and greater foot contribution tests.
  - The composition-neutral Durrim boundary test.

**Part 1 comparative table**
- The Fenn, Aelari, Grask, Halvren and Cogling-placeholder rows are omitted. Without them, the only guard against "miniature Fenn or Grask" is an audit question, not a requirement.

**Skeletal and body rules dropped**
- Upright adult spine with no mandatory hunch or crouch, and the neck direction.
- Center of mass is emergent and gives no automatic balance, knockdown or agility bonus.
- "Shoulders may be narrower than, similar to or broader than the pelvis; the race isn't one silhouette." This line matters for finding 4a.
- Frame may influence pelvic breadth, but Narrow never erases the pelvic relationship and Broad never exaggerates it.
- Femur and lower-leg segmentation: slight femur emphasis, balanced, or slight lower-leg emphasis are all valid.
- Pipkin feet may equal some children's feet in absolute size, so maturity comes from foot, ankle and leg anatomy.
- Arch distribution is OPEN, and no flat feet are inferred from stature.
- "No hidden physique packages" (for example, never Broad → muscular → high fat).

**Weakened wording**
- "Never extremely wide hips, feminized anatomy … or one hourglass silhouette" is softened to "must not be confused with sex."

**World and stature implications dropped**
- The 91 cm new lower playable-stature boundary.
- The provisional 91–251 cm playable span.

**Approved status statements dropped**
- "Approved Design Specification > Open Decision Register > Prototype / Earlier Shorthand" as applied to "large head."
- The Part 1 and Part 2 "approved first-pass" summary lists.

## 3. Ambiguities and missing positive anchors

### 3a. The human distinction rests almost entirely on one relationship (most important design finding)

Against normalized Marchfolk, Part 2 deliberately keeps several things near human:
- limbs (not required to exceed human leg proportions)
- arms (adult, proportionate, no unusual span)
- hands (moderate)

Joint scale and long-bone lightness are defined only against Durrim. That leaves the thorax-to-pelvis relationship and "compact trunk organization" as the only primary differences from a scaled human.

Two required tests then push against that one anchor:
- **PIP-STRESS-07** (lower pelvic breadth with greater thoracic breadth, still Pipkin).
- **The Marchfolk-similar frame stress test** (near-human shoulder and thoracic breadth, still Pipkin).

In those configurations, the remaining anchor is "compact trunk organization," which is defined only qualitatively.

**Recommended:** give "compact trunk" or "low-set" a concrete relational meaning that is independent of pelvic breadth. Possible measures:
- trunk vertical contribution relative to stature compared with Marchfolk
- lumbar or waist length
- pelvic depth and height, not just breadth
- the vertical position of the trunk's structural mass

Alternatively, name one secondary non-pelvic body anchor against humans. Either way, STRESS-07 would then test something specific.

### 3b. "Low-set" is still qualitative

This repeats an earlier open note. "Relative structural importance of the lower trunk" is enough for a first pass, but 3a depends on it. Resolving 3a resolves this too.

### 3c. Pelvic morphology, segment ratios and arm span stay OPEN

This is correct for a first pass. It's noted only because the human distinction depends on how the pelvis is eventually modeled.

## 4. Cross-population conflicts

### 4a. Sex-coding risk in the pelvis relationship (open since the Part 2 doc audit, still unresolved)

In human anatomy, a pelvis that is broad relative to the thorax and shoulders is a primary female-typical signal. The racial trait is defined against "Marchfolk reference anatomy" without saying which sex. Pipkin sex-related anatomy and dimorphism are OPEN.

Risks:
- Male Pipkin may read female-coded to players with human expectations.
- Any later Pipkin pelvic dimorphism would stack on top of the racial trait.

The condensed file makes this slightly worse because it drops the two lines that guarded against it: "feminized anatomy" and "shoulders may be narrower, similar or broader than the pelvis."

**Recommended:** state that the pelvis-to-thorax tendency is measured **within sex** (male Pipkin against male Marchfolk, female against female). Also state that it is expressed through adult pelvic structure (breadth, depth, landmarks), not through a shoulder-to-hip ratio alone. Add a validation pair:
- male Pipkin vs male Marchfolk at normalized height
- female Pipkin vs female Marchfolk at normalized height

Neither may read as cross-sex.

### 4b. The Durrim boundary depends on limbs and vertical compactness, not the pelvis

Brief §16 gives Durrim "powerful hips," and Durrim have strong torso-pelvis continuity. In Broad Pipkin vs Narrow Durrim, the pelvis-to-thorax relationship may converge. The distinction then rests on:
- torso vertical compactness
- limb contribution
- joint scale
- long-bone robusticity

All four are approved, so this isn't a conflict. Saying explicitly which traits carry the Durrim boundary would keep prototyping from leaning on the pelvis there.

### 4c. Fenn, Grask and Aelari

The full approved text rules out miniature Fenn, Grask and Aelari. The condensed file doesn't (see §2). With the comparative rows restored there is no conflict.

### 4d. Cogling

Correctly left undefined. No claims are made against Cogling.

## 5. Prototype conflicts known from available evidence

The UE5 project wasn't opened for this audit (design phase). From the plan's recorded state:
- **Scale:** the game currently draws Pipkin at about 0.7× Marchfolk scale, which is about 121 cm against a 173 cm Marchfolk. The approved reference is about 107 cm (about 0.62×), and about 121 cm sits at the Pipkin maximum, the Durrim boundary. The prototype is non-authoritative, so no action is needed. Note it for the implementation audit.
- **Body:** uniform whole-body scaling of the human mannequin is by definition the "scaled human" the spec forbids. This is an accepted placeholder (plan gap #4).
- **Sneak trait:** the "harder to notice while sneaking" trait is recorded as a legacy gameplay trait subject to review. This is consistent.

Implementation-level verification stays deferred.

## 6. Recommended clarifications and corrections

**For ChatGPT to propose and Tyler to approve:**
1. **Canonical file (Tyler's decision, before Part 3).** Pick one authoritative Pipkin file. Either:
   - (a) make `specs/pipkin/PIPKIN_V1.md` canonical and restore every item in §2, or
   - (b) keep `races/11-pipkin.md` canonical and make `PIPKIN_V1.md` a summary that points to it.

   The same choice applies to the other ten races: `specs/STATUS.md` lists them as complete, but their full text lives only in `races/`.
2. **Concrete anchor (3a).** Give "compact trunk" or "low-set" a concrete, pelvis-breadth-independent meaning, or add one secondary non-pelvic body anchor against Marchfolk.
3. **Within-sex measurement (4a).** Add the within-sex statement and the same-sex Marchfolk validation pair.
4. **Durrim-boundary carriers (4b, optional).** Name which traits carry the Durrim boundary.

**Repository housekeeping (Tyler's call):**
- Two registers now exist:
  - `decisions/PROJECT_RULES.md`, the universal rules.
  - `register/decision-register.md`, the full AGREED, PRELIMINARY and OPEN log.
- The two README files assign it differently:
  - `WORKFLOW.md` has ChatGPT recording decisions in `decisions/`.
  - `README.md` has Claude maintaining `register/`.

  A suggested split:
  - `decisions/PROJECT_RULES.md` holds the universal rules (ChatGPT authors).
  - `register/` holds the per-part decision log (Claude records from approved parts).
- Audit naming is also mixed:
  - per-part files, such as this one
  - per-race rolling files, such as `audits/11-pipkin.audit.md`

  Keeping per-part files for new audits and the per-race files as history works.

## 7. Completion recommendation

- **Design:** Part 2 is accepted for first pass, with clarifications 2 and 3 to be resolved by patch. They can arrive alongside Part 3.
- **Before Part 3:** resolve clarification 1 (the canonical file), so Part 3 isn't added to a file that's missing approved Part 1–2 requirements.
- **Status:** Pipkin v1.0 isn't complete. Parts 3–5 remain, and Part 3 should not be started until Tyler says so.

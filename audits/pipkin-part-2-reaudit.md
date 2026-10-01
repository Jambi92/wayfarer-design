# Re-audit: Pipkin v1.0 Part 2 author resolution

**Auditor:** Claude
**Audited file:** `reviews/pipkin-part-2-author-resolution.md`, commit `3fa1ebe`
**Responds to:** `audits/pipkin-part-2.md`
**Compared against:**
- `specs/pipkin/PIPKIN_V1.md`, the full approved Parts 1–2 text
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- Marchfolk, Durrim, Fenn, Aelari, Grask and Gorrund specs in `specs/`

These are findings, not changes. No spec file was edited.

## 1. Result

**Design: PASS WITH CLARIFICATIONS.** The resolution closes the three design findings. It introduces no contradiction and no hard creator dependency. Two minor clarifications are in §4.

**Process: one conflict that needs correcting before this is patched in.** See §2.

## 2. Process findings

### 2a. Canonical location conflicts with Tyler's decision (needs correction)

Resolution §1 declares `races/11-pipkin.md` authoritative and `specs/pipkin/PIPKIN_V1.md` a non-authoritative artifact. That reverses Tyler's decision of September 30.

At 18:50 Tyler chose `specs/` as the one official location. At 18:51 (commit `7df02e3`), before the resolution was committed at 18:54, the full approved text of all eleven races was moved into `specs/<race>/<RACE>_V1.md`:
- `races/` no longer exists.
- `specs/pipkin/PIPKIN_V1.md` is now the full approved text, not the condensed copy.

The resolution was evidently written against the pre-move tree. Its intent matches what is now in place: full approved text authoritative, condensed omissions never propagated. Only the path is reversed.

**Recommended correction:** amend resolution §1 to read:
- `specs/<race>/<RACE>_V1.md` is the authoritative full race specification.
- `specs/STATUS.md` holds status and navigation.

No file needs to move.

### 2b. Location of the resolution file

`README.md` lists `reviews/` under **Approved Design Specification** in the authority order. An author proposal that Tyler has not yet approved therefore sits in a folder that reads as approved spec.

**Recommended:** move it to `audits/`, for example `audits/pipkin-part-2-author-resolution.md`, or to a `proposals/` folder. Alternatively, Tyler approves it and ChatGPT patches the text into the spec, at which point the file is history either way.

### 2c. Not yet in the spec

Resolution §§2–4 are proposed text. Under `WORKFLOW.md` step 4 they become part of the spec only once ChatGPT patches them into `specs/pipkin/PIPKIN_V1.md`, with Tyler's approval. Until then, the three findings stay open in the register (logged PRELIMINARY; see `register/decision-register.md`).

## 3. Verification of the five requested points

### 3.1 The vertical-trunk, lumbar and pelvic anchor is coherent and not Durrim-like compression: PASS

The anchor has three parts:
- a modestly reduced vertical central-trunk share
- a compact lumbar and waist transition
- a pelvis whose vertical height, depth and three-dimensional integration stay substantial relative to the thorax

This describes a real skeletal organization: a shorter lumbar segment over a taller, deeper pelvis. It also points away from a child read, since human children have a relatively long trunk and short legs.

It stays distinct from Durrim compression for three reasons:
- "Modestly reduced" is measured against Marchfolk.
- Approved Part 2 already places Pipkin "less vertically compact than Durrim."
- Resolution §2 explicitly excludes Durrim-like compression, a short spine, crouching, belly compression and an absent waist.

The Fenn, Aelari and Grask rows (Part 1 comparative table) are unaffected, because the anchor concerns the trunk, not limb elongation.

### 3.2 It survives lower pelvic breadth and Marchfolk-similar thoracic and frame configurations: PASS

The anchor is now vertical and three-dimensional, independent of pelvic breadth. So PIP-STRESS-07 and the Marchfolk-similar frame test both have something specific to check:
- trunk vertical share
- lumbar transition
- pelvic height and depth

This was the main gap in the first audit (finding 3a), and it is closed. The "low-set is qualitative" note (3b) is also largely closed: "low-set" now has a describable vertical meaning, with exact values left to prototyping.

### 3.3 The within-sex safeguard solves sex-coding without fixing dimorphism: PASS

The safeguard does three things:
- requires like-for-like anatomical configurations
- expresses the trait through pelvic breadth, depth, height, landmarks and trunk integration, not the shoulder-to-hip ratio or external hip circumference
- adds the male and female validation pair

Pipkin dimorphism magnitude and morphology stay OPEN. This matches finding 4a and universal amendment v0.1 (anatomy is its own layer; non-human races are not assumed to share human sex anatomy). The phrase "where sex-related anatomy materially affects pelvic or thoracic structure" correctly leaves room for configurations other than the two in the example.

### 3.4 The Durrim boundary stays positive and multi-factor: PASS

Seven named carriers, with pelvic breadth explicitly not primary:
- torso vertical organization
- thoracic breadth, depth and axial presence
- limb contribution
- joint dimensions
- long-bone robusticity
- hand, wrist, foot and ankle structure
- the two trunk systems

All seven were already approved for Durrim and Pipkin, so nothing new is asserted about Durrim. This matches the Durrim spec and the Gorrund final clarification.

### 3.5 No new hard creator-control dependency: PASS

The anchor is stated as a population-level relational tendency. It explicitly rules out:
- a fixed numeric ratio
- a "Low-Set" or "Pipkin Proportion" slider

The within-sex rule governs validation comparisons, not creator controls. This is consistent with the project rule on soft correlations.

## 4. Minor clarifications (non-blocking)

### 4a. Where the reduced trunk share goes

Stature is shared among head and neck, trunk, and legs. If the trunk's share drops, the difference has to land in the head, the legs or both.

Approved text keeps head contribution secondary and never a maturity signal. Legs are "not required to exceed ordinary human proportions."

**Recommended:** one sentence saying the reduced trunk share is absorbed mainly through sustained limb contribution and pelvic height, not mainly by a larger head share. Otherwise the new anchor could quietly raise relative head size, the trait most likely to cause a child read.

### 4b. Same axis as Durrim

Both Durrim (strongly) and now Pipkin (modestly) sit below Marchfolk on trunk vertical share. On that one axis the Durrim distinction becomes a matter of degree. The multi-factor boundary in resolution §4 covers this, so nothing breaks. Prototyping should still not use trunk share alone to tell Pipkin from Durrim, just as pelvic breadth is not used alone.

### 4c. Test IDs

The male and female validation pair has no IDs yet. Suggested IDs:
- PIP-BODY-28: male Pipkin vs male Marchfolk
- PIP-BODY-29: female Pipkin vs female Marchfolk

The Broad Pipkin vs Narrow Durrim test (PIP-BODY-14) should also be run like-for-like.

## 5. Cross-population and prototype conflicts

- **Cross-population:** none new. Marchfolk, Durrim, Fenn, Aelari, Grask and Gorrund approved text is unaffected.
- **Prototype:** nothing new. The UE5 project was not opened. Uniform scaling of the human mannequin remains the accepted placeholder (plan gap #4).

## 6. Completion recommendation

Pipkin Part 2 can be marked **first-pass accepted** once the following are done:
1. ChatGPT amends resolution §1 to the `specs/` location Tyler chose (2a).
2. Tyler approves resolution §§2–4.
3. ChatGPT patches §§2–4 into `specs/pipkin/PIPKIN_V1.md`. Including the 4a sentence and the 4c IDs is recommended but not required.

After that, Part 3 can begin when Tyler says so.

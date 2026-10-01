# Final audit: Pipkin v1.0 Part 6 and first-pass consistency

**Auditor:** Claude
**Audited file:** `specs/pipkin/PIPKIN_V1.md` at commit `8d81ca6`
- Part 5 acceptance: `0f9a409`
- Brief pointers: `4e0d9f1`
- Status: `540d028`

**Request:** `reviews/pipkin-part-6-final-audit-request.md`

**Compared against:**
- Pipkin Parts 1–5
- `rules/character-creation-brief.md`
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the Marchfolk, Durrim, Fenn, Grask and Gorrund specs

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS. One correction is needed before FIRST-PASS COMPLETE.**

No blocking contradiction remains anywhere in Pipkin Parts 1–6, project rules, the register or the approved comparison races.

Part 6 is thorough. It:
- keeps canonical objects at true scale and fitted garments sized to the body
- separates fit from feasibility
- keeps visual, navigation, hit, interaction and camera collision apart
- validates the world against target anatomy
- keeps presets as real outputs of one system
- holds the culture firewall
- leaves lifecycle and sex dimorphism unclosed in its own text
- puts a clear identity hierarchy on top

**The one correction is to the consolidated OPEN list (§31).** It leaves out most anatomical OPEN items from Parts 1–4 (see 3a). Completion criterion 4 in §37 ("consolidated OPEN items are recorded without accidental closure") isn't met until that list is complete.

Once §31 is patched, Pipkin can be marked **FIRST-PASS COMPLETE** without another full audit. A quick check of the patched list is enough.

**Supporting changes verified:**
- Part 5 §37 records Tyler's decision correctly, including the scope limit that the legacy stealth trait stays separately OPEN.
- Both brief lines (§16.11 and the Principles movement line) now carry SUPERSEDED pointers to Part 5 §37, as "large head" did. That item can now leave the terminology review once the review pass is done.
- `specs/STATUS.md` is accurate.

## 2. The sixteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Equipment fit vs canonical scale and feasibility | PASS: §2, §10, §11 |
| 2 | Clothing, armor, helmets, hoods, footwear, gloves, belts and backpacks against anatomy | PASS: §3–9. Fit follows the trunk, pelvis, waist, limbs, feet, hands and head as approved; no ear-dependence or head enlargement |
| 3 | Collision, clearance, cameras and interaction markers | PASS: §12–17, with one gap (first-person; see 3b) |
| 4 | World against target anatomy | PASS: §13, §18, §19 |
| 5 | Presets, modes, randomization and saved appearance | PASS: §20–25, with a minor note (3d) |
| 6 | Culture and presentation firewall | PASS: §25–26 |
| 7 | Lifecycle and sex-anatomy status without accidental closure | PASS in §27–28; dimorphism magnitude is missing from §31 (3a) |
| 8 | Identity hierarchy and anti-caricature rules | PASS: §29–30. They match the Part 3 status note and every earlier exclusion |
| 9 | Consolidated OPEN list completeness | **Needs correction** (3a) |
| 10 | Permanent validation suite | PASS. All earlier cases are kept, and PIP-INT-01 to 20 cover child, Durrim, silhouette, face, surface, fit, world, camera, dialogue, presets, randomization, age, culture and prototype |
| 11 | Prototype conflict ledger | PASS: §33, with a minor note (3e) |
| 12 | Short-Race Review depends on Cogling | PASS: §34. It matches the PROJECT_RULES required review, and Cogling stays a positive anatomy, not a midpoint |
| 13 | Universal-review dependency wording | PASS: §35. Its closing line ("where a named review is not formally registered, the underlying OPEN item remains OPEN") fixes the unregistered-review pattern seen in Parts 4 and 5 |
| 14 | Final combined identity statement | PASS: §36. It matches Parts 1–5 and the hierarchy |
| 15 | Consistency across Parts 1–6, rules, register and comparison races | PASS. Durrim (compact structural concentration, depth-dominant face), Gorrund (Transverse Structural Continuity and Axial Load-Path Continuity), Fenn, Grask and Marchfolk are all described in their approved terms |
| 16 | Blocking issue | None. The §31 correction is required by the spec's own completion criterion, not by a contradiction |

## 3. Findings

### 3a. The consolidated OPEN list omits most anatomical items (required before completion)

§31 lists surface, gameplay, technical and world items, but none of the body and proportion items that Parts 1–4 explicitly left OPEN:

**From Part 1 §116–118 and Part 2:**
- the final height range (91–122 cm is provisional, subject to cross-race and world validation)
- the head-to-body ratio
- torso ratios
- shoulder architecture
- pelvic morphology, including depth (Part 2 §8–10: "for later prototyping")
- femur-to-lower-leg balance and arm-segment and arm-span distribution
- hand and foot proportions, and foot arch distribution (Part 2)
- joint dimensions
- muscular-development capacity (Parts 1–2)
- body-fat distribution patterns (Part 2)
- **the magnitude and morphology of sex-related dimorphism** (Part 2 resolution: "does not prematurely finalize… remain OPEN"). §28 describes the model but not this status.

**From the plan and project rules, not yet listed:**
- **first-person camera.** OPEN in Part 1 §72–81 and the brief §9. Part 6 §14–16 cover third-person, creator and targeting cameras only.
- **racial attribute bonuses.** Plan gap #7, as distinct from "race/class restriction".
- **the in-game race description text revision.** Plan gap #9.
- **Pipkin ear mobility.** Not raised for Pipkin. Fenn and Aelari list it OPEN, so state it either as OPEN or as "Pipkin ears are not mobile".

Leaving these out of the consolidated list is exactly the "accidental closure" risk that criterion 4 guards against.

**Recommended:** add the items above to §31. No design changes are needed.

### 3b. First-person (also in 3a)

Add one line to the camera section or §31: first-person eye-line and arm presentation are OPEN, and if first-person exists, Pipkin keep their own arm, hand and eye-height geometry. Fenn's Part 5 used this pattern.

### 3c. Optional validation addition

The like-for-like sex walk comparison suggested in the Part 5 audit (4e) isn't in PIP-INT. One case would close the loop on the Part 2 sex-coding fix in motion:
- **PIP-INT-21:** male Pipkin vs male Marchfolk walk, and female vs female.

This is optional.

### 3d. No provisional preset concepts (minor)

Every other completed race lists provisional character-preset and presentation-preset concepts (for example Skarn's eight, Sagekin's eight and Fenn's eight). §20 sets good requirements but names none. That's acceptable for first pass, since presets are provisional everywhere, but a short provisional list would keep Pipkin parallel with the other races. Avoid farm, kitchen or burglar tropes as names. Optional.

### 3e. Prototype ledger specifics (minor)

§33 is correct but generic. The audits have recorded one concrete known value: the prototype draws Pipkin at about 0.7× Marchfolk scale (about 121 cm), against the approved reference of about 107 cm. That puts the prototype's typical Pipkin at the Pipkin maximum, the Durrim boundary. Recording that value would help the later implementation audit. Optional.

## 4. Consistency sweep, Parts 1–6

- **Identity chain.** Part 1's "light compact adult proportionality" leads to Part 2's Low-Set Compact Trunk Architecture (primary), then Part 3's Integrated Mature Facial Architecture (supporting), then Part 4's overlapping surface (not identity), then Part 5's movement (from anatomy, no stereotypes), then Part 6's integration and hierarchy. The chain is consistent.
- **Child read.** Every part carries an anti-child safeguard that rests on structure, not presentation:
  - Part 1: adult read
  - Part 2: a mature pelvis, and a shorter trunk that points away from child proportions
  - Part 3: adult facial structures protected from shortening
  - Part 4: no youth coding from surface
  - Part 5: a narrow-base adult gait and adult cadence
  - Part 6: PIP-INT-01 and 16
- **Durrim boundary.** Separation is multi-factor in body (Part 2), face (Part 3), movement (Part 5) and integration (PIP-INT-02 and 06). Pelvic breadth and trunk share are never used alone.
- **Authority.** The brief's "large head" and movement lines are both superseded with pointers. Prototype values are non-authoritative throughout.
- **Terminology.** The overlap between "Compact Rounded Auricular" and Durrim's "compact" terms is still queued for the terminology review, which is fine.

## 5. Completion recommendation

1. ChatGPT patches §31 per 3a, which also covers first-person (3b).
2. 3c, 3d and 3e are optional.
3. I do a quick check of the patched §31. No full re-audit is needed.
4. Pipkin v1.0 is then **FIRST-PASS COMPLETE**, on Tyler's confirmation.
5. The Short-Race Comparative Anatomy Review stays queued for after Cogling.

Cogling should not begin until Tyler says so.

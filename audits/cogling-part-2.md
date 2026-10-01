# Audit: Cogling v1.0 Part 2, Detailed body architecture and proportion system

**Auditor:** Claude
**Audited file:** `specs/cogling/COGLING_V1.md` at commit `31c5d56`
**Request:** `reviews/cogling-part-2-audit-request.md`
**Compared against:**
- Cogling Part 1
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the approved Pipkin, Durrim, Fenn, Grask, Marchfolk and Sagekin specs

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS.** Part 2 turns the patched Part 1 anchor into a coherent whole-body system. It has:
- a positively described narrow stable core (§44–49)
- explicit near-human limb totals with within-limb redistribution (§38, §39, §42)
- separate controls for frame, robusticity, joints, muscle and fat (§52–60)
- multi-factor boundaries with Pipkin, Durrim, Fenn, Grask and Marchfolk (§63–67)
- a demanding toddler test (§68)
- a body-control list that keeps the biological dimensions without fixing the UI (§69)
- concrete invalid-combination examples (§70)

There are no contradictions and no hard dependencies. Nothing about movement, gameplay or the face is decided.

Three non-blocking clarifications are in §4. ChatGPT can fold them into the Part 3 patch.

**Recommendation:** Part 2 may be marked FIRST-PASS ACCEPTED on Tyler's approval.

## 2. The fifteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Narrow stable core positively defined | PASS. §44–49 define the integrated thorax, spine and pelvis: narrow transverse breadth with adult depth, full respiratory volume, a mature non-dominant pelvis and adult axial length. "Narrow" is skeletal, and "stable" isn't a balance bonus |
| 2 | Near-human totals with within-limb redistribution | PASS. §37–39 and §42 have proximal segments accommodate the change, and §70 rejects maximum distal values without that compensation |
| 3 | No convergence with Fenn or Grask | PASS. §65–66 and COG-BODY-16, 17, 19 and 20 cover it |
| 4 | Hands adult, with no dexterity or tinkering biology | PASS. §40–41 keep an adult palm, knuckles and tendons, an opposable thumb, and no tool-use, lockpicking or spellcasting advantage |
| 5 | Thorax, pelvis and shoulders mature and distinct from Pipkin and Durrim | PASS. §45, §47, §48, §63 and §64 |
| 6 | Head allometry at 76–107 cm without child coding | PASS. §51 allows a natural allometric head share but never deliberate enlargement or a toddler head share; the ratio stays OPEN |
| 7 | Frame, muscle and fat independent | PASS. §54 and §57–60 |
| 8 | Broad isn't Durrim; narrow isn't Fenn or fragile | PASS. §55–56, COG-BODY-22 and 23, and §70 |
| 9 | Pipkin overlap carried by several traits | PASS, and it can be strengthened (4a) |
| 10 | Normalized comparison tests | PASS for Marchfolk, Fenn, Grask and Durrim. **Sagekin is missing (4b)** |
| 11 | Toddler test | PASS. §68 and COG-BODY-25, with facial maturity deferred to the face part |
| 12 | Body-control architecture | PASS. §69 lists the dimensions and allows merging later, provided "the biological relationships cannot be lost" |
| 13 | Combined-proportion validity | PASS. §70 names five invalid combinations |
| 14 | Part 1 leftovers | **Fixed.** The §34 identity statement now matches the patched anchor; face readability is in the Part 1 OPEN list; COG-BODY-09A is added |
| 15 | Nothing about movement, gameplay or the face decided by accident | PASS. §36, §43, §44, §49, §68 and §72 all defer these |

## 3. Contradictions

None. The Part 2 anchor (§37) matches the Part 1 identity statement (§34), and both are consistent with the approved Pipkin, Durrim, Fenn and Grask text quoted in §63–66.

## 4. Non-blocking clarifications

### 4a. Add axial contribution to the Pipkin overlap carriers

In the 91–107 cm overlap zone, **total limb contribution doesn't separate Cogling from Pipkin.** Both are near-human. Pipkin limbs "never automatically exceed ordinary human adult proportions" (Part 2).

There is a useful difference that §63 doesn't list:
- **Pipkin:** Part 2's patched anchor gives "a modestly reduced vertical central-trunk contribution to total stature."
- **Cogling:** §49 keeps "total axial contribution adult and broadly balanced," and §6 keeps torso contribution "near the Marchfolk adult range."

This is a real, positive difference: trunk vertical share is reduced in Pipkin and near-human in Cogling. Add it to both sides of §63.

Also, Pipkin's approved leg segmentation allows "slight femur emphasis, balanced segmentation or slight lower-leg emphasis." A lower-leg-emphasis Pipkin therefore overlaps Cogling's leg redistribution. §63 already says no single measurement carries the boundary. One line noting that leg segmentation alone can't separate them would keep prototyping from relying on it.

### 4b. Add a normalized Sagekin comparison

Sagekin are the human population whose approved tendencies sit closest to Cogling's distal signal. Sagekin v1.1 lists:
- "slightly longer forearms, hands and fingers"
- "somewhat longer fingers and slightly narrower hands"
- "slightly less ribcage depth"
- "a somewhat more linear silhouette"
- "a slightly greater leg share"

At normalized height, a narrow-core Cogling with long forearms and fingers could read as a Sagekin. The distinguishing traits:

| | Cogling | Sagekin |
| --- | --- | --- |
| Limb change | Redistribution inside near-human totals (shorter humerus and femur) | Slightly longer limbs overall |
| Bone and joint scale | Fine shafts and joints | Ordinary human bone and joint scale |
| Leg share of height | Unchanged | Greater |

**Recommended:** add a Sagekin row to the boundary sections (§63–67) and a test such as **COG-BODY-31:** Cogling vs Sagekin at normalized displayed height, presentation neutral.

### 4c. Two duplicate validation IDs (minor)

| Duplicate | Same test as | Shared content |
| --- | --- | --- |
| COG-BODY-26 | COG-BODY-09A | Maximum Cogling vs reference Pipkin at about 107 cm |
| COG-BODY-25 | COG-BODY-11 | Minimum Cogling vs a toddler of about 1–2 years |

**Recommended:** keep one ID for each test, or note that the Part 2 IDs replace the Part 1 ones. The validation set needs stable IDs before the permanent-suite consolidation in a later part.

## 5. Cross-population summary

| Race | Status |
| --- | --- |
| Pipkin | Multi-factor; add the trunk-share carrier (4a) |
| Durrim | Clearly distinct (§64, COG-BODY-10, 10A and 22) |
| Fenn | Distinct through limb totals and core (§65, COG-BODY-16 and 20) |
| Grask | Distinct through limb totals and no reach (§66, COG-BODY-17 and 19) |
| Marchfolk | Distinct through combined relationships (§67, COG-BODY-18) |
| Sagekin | **Not yet tested** (4b) |
| Gorrund | Not relevant at this scale; the §45 thorax exclusion covers it |
| Human toddler | Covered (§68), with the face pending |

## 6. Completion recommendation

1. Part 2 may be marked FIRST-PASS ACCEPTED on Tyler's approval.
2. ChatGPT can add 4a, 4b and 4c to the Part 3 patch.
3. Part 3 begins when Tyler says so.

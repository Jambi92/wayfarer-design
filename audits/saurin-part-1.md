# Audit: Saurin v1.0 Part 1, Biological foundation, stature and core skeletal architecture

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` at commit `6a91fef`
**Request:** `reviews/saurin-part-1-audit-request.md`
**Compared against:**
- `rules/character-creation-brief.md` §15–16.13
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the approved Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Halvren, Durrim, Grask, Gorrund, Pipkin and Cogling specs

These are findings, not changes. The spec was not edited.

**Short-race review status:** the four remaining Pipkin cross-references (commit `54d686d`) are now fixed. All 8 points of the short-race quick check pass, so the review can close on Tyler's acceptance, which `specs/STATUS.md` records.

## 1. Result

**PASS WITH CLARIFICATIONS.** Part 1 has solid foundations:
- the tail is real axial anatomy, with mass, a supported base and coupled constraints (§10, §11, §27)
- an upright plantigrade baseline with no crouched-lizard shorthand (§14–15, §25)
- broad adiposity and composition (§22–23)
- a sex-anatomy firewall (§24)
- strong dragon, aquatic and presentation firewalls (§28–30)
- the legacy 5× breath and fastest-swimmer traits kept as gameplay questions, not anatomy drivers
- tail world-space flagged early (SAU-BODY-20)

Three findings should be resolved before acceptance:
- **4a. The tail-hidden body doesn't yet have enough positive identity.** The request asked me to challenge this specifically.
- **4b. Two boundaries with high convergence risk are missing:** Skarn and Aelari.
- **4c. The tail's biological role in the brief has been narrowed** without a decision from Tyler.

## 2. The eighteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Counterbalanced Pelvic-Axial Architecture is positive, not "human plus tail" | Partly. Positive *with* the tail; thin without it (4a) |
| 2 | Identity survives with tail and surface hidden | **Not yet demonstrated** (4a) |
| 3 | About 168–208 cm, and overlaps | PASS. Overlap is intended (§4); see 4b |
| 4 | Thorax, lower trunk, pelvis and sacrum integration | PASS in direction. Stature accounting is in 4d |
| 5 | Tail as real axial anatomy | PASS (§3, §10, §13) |
| 6 | Tail length 55–80% of standing height, with relationship constraints | PASS (§10–11, §27, SAU-BODY-08 and 09). See 4e |
| 7 | Upright plantigrade baseline | PASS (§14–15, §25) |
| 8 | Hands, feet, limbs; Grask and Cogling convergence | Limbs: PASS (§31). Hands are thin (4a) |
| 9 | Skeletal mass, frame, composition | PASS (§19–22) |
| 10 | Broad adiposity | PASS (§22–23) |
| 11 | Sex anatomy free of stereotype | PASS. One wording note (4f) |
| 12 | Dragon and aquatic firewalls | PASS (§29–30) |
| 13 | Legacy breath and swim traits under review | PASS (§30) |
| 14 | Comparative boundaries | Partly. Skarn and Aelari are missing (4b) |
| 15 | SAU-BODY-01 to 20 | Good; additions in 4a and 4b |
| 16 | Omitted races with convergence risk | **Skarn and Aelari** (4b). Sagekin and Halvren are low risk |
| 17 | No culture or personality as biology | PASS (§28) |
| 18 | No UE5 | PASS |

## 3. Contradictions

There is no contradiction with project rules. There is one tension with the brief (4c).

## 4. Findings

### 4a. The tail-hidden body doesn't yet carry enough positive identity (should be resolved before acceptance)

§5 promises five carriers that should make a Saurin "clearly non-human" at Marchfolk-matched height in neutral gray:
1. axial and pelvic architecture
2. tail integration
3. thoracic organization
4. limb-joint relationships
5. hand and foot anatomy

With the tail hidden (SAU-BODY-04 and 18), here's what Part 1 actually specifies for each:

| Carrier | What Part 1 specifies | Distinct without the tail? |
| --- | --- | --- |
| Thorax (§7) | Moderate breadth, meaningful depth, long lower-rib transition, "less clavicle-dominant" | **No.** Deep thorax and a larger torso share are approved **Skarn** tendencies, and a long torso and waist transition is approved **Aelari** (see 4b) |
| Lower axial trunk (§6) | Greater longitudinal contribution than Marchfolk; integrated ribcage to pelvis, no pinched waist | **Weak.** The long trunk overlaps Aelari, and the unpinched waist resembles Skarn and Durrim continuity |
| Limb-joint relationships (§14, §17, §19) | Moderate-to-long legs, mature knees, modest forearm emphasis, adult joints | **No.** All are framed as "not Grask, not Cogling, not Durrim." No positive relationship is given |
| Hands (§18) | Five digits, moderately elongated fingers, defined knuckles | **No.** Fenn and Sagekin have longer fingers too; claws and nails are deferred |
| Feet (§16) | Longer forefoot and toe contribution, strong heel-to-midfoot transition, broad | **Yes.** A real positive relationship |
| Pelvis and sacrum (§9) | Strong posterior integration with the sacral and tail base | **Yes, if the test keeps the tail base visible** |

**So:** at Marchfolk-matched height with the tail hidden and the surface neutral, the specified body reads as a deep-chested, long-waisted, long-toed human, close to a lean Skarn or a broad Aelari. That's exactly the "human plus tail" outcome the core rule forbids.

**The missing relationship:** the brief already names it. §16.13 says "Locomotion reflects different **hip, shoulder, torso and tail mechanics**" and "possibly a modified leg and foot structure." Part 1 says nothing positive about the **hip joint and pelvic-femoral relationship** or the **shoulder-girdle organization** (§8 is all negatives and OPEN).

Recommended options for ChatGPT, without using scales, claws, posture or stereotypes:

1. **Define what "tail hidden" means in the test.** SAU-BODY-04 and 18 should hide the *free tail* distal to the caudal base. The sacral and caudal base and the posterior pelvic projection are skeletal anatomy and should stay visible. That makes the pelvic carrier (§9), the strongest one, testable. A test that removes the whole caudal region is stricter than any other race faced, and it would delete the race's main mechanism.
2. **Add a positive hip relationship.** For example, a pelvis that is longer front-to-back with more posterior mass than Marchfolk, and hip joints placed relative to that mass so the pelvis and femur are organized around carrying a tail (the counterbalance). This is the "different hip mechanics" the brief calls for. It would show at matched height without the tail, and Skarn and Aelari don't share it.
3. **Add one positive shoulder or thoracic-inlet relationship** to give "less clavicle-dominant" real content. For example, how the scapula sits on a deep, narrow-to-moderate thorax, compared with the Skarn broad clavicle and upper back.
4. **Say explicitly** that hands are a secondary carrier until a later part (claws and nails, digit proportions). This keeps §5 from over-promising.

Then add a pass criterion to SAU-BODY-04 and 18 naming which carriers must remain visible: the caudal base, the pelvic-femoral relationship, the foot, and the thoracic organization.

### 4b. Skarn and Aelari boundaries are missing (should be resolved before acceptance)

| Race | Overlap with Saurin |
| --- | --- |
| **Skarn** | Stature 183–229 cm overlaps Saurin 168–208 cm across most of the range. Skarn have "deeper ribcage and more thoracic volume" and a "slightly larger torso share of total height and greater torso depth," the same direction as Saurin §6–7. A lean, narrow Skarn and a broad Saurin, with tail and surface hidden, are the highest-risk pair in the roster for this race. |
| **Aelari** | Stature 168–221 cm overlaps Saurin almost entirely. Aelari have a "longer torso … longer waist transition," which is the same direction as the Saurin "elongated lower axial trunk." The differences are that Aelari elongation is whole-body (cranium, neck and limbs) with shallow depth, while Saurin trunk length is lower-axial with meaningful depth. That distinction is real but needs stating. |

Sagekin and Halvren are human or mixed and covered implicitly by the Marchfolk and Aelari comparisons. Pipkin is out of stature range.

**Recommended:** add Skarn and Aelari rows to §31, built on their approved anchors, and add normalized tests: **SAU-BODY-21** (Saurin vs Skarn, tail and surface hidden) and **SAU-BODY-22** (Saurin vs Aelari, tail and surface hidden). Both depend on the 4a carriers.

### 4c. The brief's functional tail is narrowed without Tyler's decision

Brief §16.13 says: "The tail works biologically: **balance, turning, swimming, acceleration and body language**." Part 1 handles this as follows:
- §13: the tail grants no automatic balance, turning or swimming *benefits*
- §10: "not automatically aquatic-specialized"
- §12: forbids tail-shape stereotypes

The **gameplay firewall** there is correct and consistent with Pipkin and Cogling. But Part 1 never affirms the tail's **biomechanical** role. The brief describes a tail that participates mechanically in balance, turning, acceleration, swimming and body language, which differs from a gameplay bonus.

Read together, §10, §12 and §13 could be taken as removing the brief's functional tail. That would supersede approved text, which needs Tyler's explicit decision, as for Pipkin §37 and Cogling §140.

**Recommended:** affirm in Part 1 that the tail **participates biomechanically** in balance, turning, acceleration and swimming motion, and in body language, as counterbalance and axial motion for animation and physics. Separately, confirm that **no gameplay advantage follows automatically**. That keeps the brief and the firewall without needing a supersession.

If the author intends to drop any of those functions as biology, flag it for Tyler.

### 4d. Stature accounting (minor)

Excluding the tail, standing height divides among head and neck, trunk and legs. Part 1 gives Saurin:
- an **elongated lower axial trunk** (§6)
- **moderate-to-long leg contribution** (§14)

Both take a larger share of height, so the head, neck or thorax height must take less. That's an issue for Part 2 (head) and the craniofacial part. One line now would prevent a later contradiction: either legs are near-Marchfolk, or the neck or thoracic height is reduced. Pipkin Part 2 had the same accounting note.

### 4e. Tail world-space and reference height (minor)

At the 188 cm reference, a tail of 55–80% of height is about **1.0–1.5 m**. SAU-BODY-20 is the right first step. Later parts will need these explicitly:
- seating (chairs with backs and benches)
- beds
- crowds and multiplayer collision
- doors closing on tails
- capes, cloaks and back armor
- mounts
- camera framing behind the character

Note them in §33 now.

Also, the brief's reference is about 1.05× (about 182 cm), and Part 1 uses 188 cm (about 1.09×). Brief multipliers are preliminary, so this is fine. Recording it keeps it from looking accidental.

### 4f. Sex-related anatomy wording (minor)

Universal amendment v0.1 says non-human races are **not assumed to share human sex-related anatomy**. Saurin are the most non-human race in the roster. §24 should state that the universal non-assumption applies, so later work doesn't default to human sex-related anatomy, while keeping its good firewall list.

### 4g. Prototype authority (minor)

Unlike every other race's Part 1, there's no line saying existing prototype Saurin values (scale, the 5× breath and swim values, collision, the shared human animation) are non-authoritative. Add one for consistency.

## 5. Completion recommendation

1. ChatGPT patches 4a (tail-hidden definition, hip and shoulder relationships, carrier criteria), 4b (Skarn and Aelari) and 4c (affirm the tail's biomechanical role).
2. Recommended alongside: 4d–4g.
3. I re-audit.
4. On a PASS and Tyler's approval, Part 1 is accepted.

Part 2 should not begin until then.

# Audit: Cogling v1.0 Part 5, Movement, physical expression and gameplay boundaries

**Auditor:** Claude
**Audited file:** `specs/cogling/COGLING_V1.md` at commit `c9d281c`
**Request:** `reviews/cogling-part-5-audit-request.md`
**Compared against:**
- Cogling Parts 1–4
- Pipkin Part 5 (accepted), including §37, Tyler's supersession decision
- `rules/character-creation-brief.md` §15–16.12
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the project equipment, reach and world-compatibility rules

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS. Acceptance waits on one decision from Tyler.**

Part 5 is consistent with the accepted Pipkin movement design. It:
- generates movement from the approved anatomy
- treats cadence as a consequence of anatomy, never as a personality
- rejects scurrying, bouncing, tiptoeing and fidgeting
- keeps real mass and momentum, with no "toy" movement
- keeps canonical objects at true scale and real absolute reach
- keeps the camera honest about size
- keeps a personality firewall and resting alignment separate from body language
- keeps movement out of Biological Randomization
- includes a full gameplay-stat firewall, with a physical-consequence principle (§168) that is a useful addition

**The decision.** §140–141 and §171 **declare the brief's Cogling movement and fine-motor wording superseded.** The brief is approved text. In the Pipkin precedent, Tyler made that call explicitly (Pipkin Part 5 §37) before it went into the spec. The Cogling Part 1 audit (§5) flagged in advance that this would need his decision. The request doesn't say Tyler made it, and `rules/character-creation-brief.md` is unchanged. So §140–141 is an author proposal until Tyler confirms it.

## 2. The sixteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Explicit supersession of the legacy wording | **Written correctly. Needs Tyler's decision** (4a) |
| 2 | Hands are morphology, not dexterity, crafting, lockpicking, spellcasting or aiming bonuses | PASS (§141, §148, COG-MOVE-12) |
| 3 | Cadence is a consequence, not hurrying or scurrying | PASS (§142–144). See 4b on speed |
| 4 | No superior turning, balance, climbing, jumping, swimming or stealth inferred | PASS (§145–147, §152–155) |
| 5 | Believable mass and momentum | PASS (§150–151, COG-MOVE-05) |
| 6 | Absolute reach, eye height, stride and object fit stay real | PASS (§156, §159, §168) |
| 7 | Equipment and weapons don't auto-scale | PASS (§157–158, COG-MOVE-11 and 23) |
| 8 | Interaction geometry respects anatomy; no hiding it by animation warping | PASS (§159, COG-MOVE-14) |
| 9 | Camera honest about body scale | PASS (§160, COG-MOVE-22) |
| 10 | Movement separated from tinkerer and personality traits | PASS (§149, §161, COG-MOVE-18 and 19) |
| 11 | Resting alignment separate from body language | PASS (§162) |
| 12 | Composition, sex and age create no stereotypes | PASS (§163–165) |
| 13 | Movement randomization outside Biological Randomization | PASS (§166) |
| 14 | Stat firewall doesn't decide the broader racial-trait system | PASS (§167, last line) |
| 15 | Validation cast | Good; see 4c |
| 16 | No UE5 implementation | PASS |

**Consistency with Pipkin Part 5:** consistent throughout. Equipment, reach and world compatibility also match the AGREED project rules: canonical equipment never scales, visual, interaction and combat reach stay separate, and the world is validated against approved anatomy.

## 3. Contradictions

There's no design contradiction with Parts 1–4 or project rules.

There is one **authority conflict**. Until Tyler decides, §140–141 contradicts approved brief text: brief §16.12, the race-table line "fine motor control," and the brief's Cogling movement description. The authority rule (Approved Design Specification > Open Decision Register > Prototype) means a race spec can't silently overwrite the brief. Pipkin Part 5 initially recorded the same conflict as "OPEN and not silently superseded" until Tyler chose.

## 4. Findings

### 4a. Supersession needs Tyler's explicit decision (blocks acceptance only)

Tyler should choose, as he did for Pipkin:

- **(a) Supersede.** This is what §140–141 propose and is consistent with Pipkin. Quick steps, frequent turns, efficient climbing, precise hand movements, small adjustments and fine motor control are not automatic racial traits. Then ChatGPT records the decision in §140 the way Pipkin §37 did, and adds SUPERSEDED pointers to the brief's §16.12 and the race-table "fine motor control" entry.
- **(b) Keep some as visual movement tendencies only**, with no gameplay effect.
- **(c) Keep selected items as racial gameplay traits** for the later race-biology-gameplay review.

Until he chooses, the register records this as OPEN.

### 4b. Equal gameplay speed would push minimum-height Cogling into a run

This is a rough biomechanical estimate, not a spec value. A ~76 cm adult has a leg length of roughly 0.35–0.4 m. At an ordinary human walking speed of about 1.4 m/s, that is at or past the usual walk-to-run transition. A Pipkin, by contrast, stays in a brisk walk.

So if a later review chooses equal walk speed across races, minimum-height Cogling would have to jog or run where Marchfolk walk. That's unavoidable physics, and it can look like the "rapid-leg cycling" §144 forbids.

**Recommended:** one line in §142 or §170. If equal gameplay speed is ever chosen, the animation must use an honest adult gait transition (a brisk walk or adult jog). It must not show rapid-leg cycling. The speed decision itself must weigh this consequence, and the stress test should cover minimum-height Cogling at the chosen speed. Pipkin Part 5 has the matching walk-run-transition check.

### 4c. Validation additions (minor)

The Cogling movement cast mirrors Pipkin's well. Three additions are recommended:
- **Toddler gait.** Pipkin had PIP-MOVE-07: adult gait, cadence variability and step width compared with a child. Cogling, at toddler height, carry the highest child-read risk in the roster, yet no Cogling movement test compares against a toddler walk. Add a minimum-height Cogling walk beside a ~1–2-year-old toddler walk, judging adult gait mechanics, consistent cadence and step width.
- **Pipkin overlap zone.** Add a 91–107 cm Cogling and Pipkin walk comparison, so the movement differences between the two body plans are checked in the shared height zone.
- **Equal-speed stress case.** Add a minimum-height Cogling at a speed matched to a taller race (see 4b).

## 5. Carried items

These are still open from the earlier re-audits. None of them blocks acceptance:
- **Cognition firewall** (Part 3 re-audit note 3b). Cranial-vault proportion carries no cognitive meaning. Part 5's §161 personality firewall is the natural place for it, but it isn't there yet.
- **FD-HAIR wording** (Part 4 re-audit). FD-HAIR should list "eyebrows" to match the AGREED text.
- **Part 4 re-audit (PASS) not on GitHub.** Pushing the Cogling Part 4 re-audit was blocked on my side, so it isn't on GitHub yet. Its result is a PASS. Tyler has since accepted Part 4.

## 6. Completion recommendation

1. Tyler decides 4a.
2. ChatGPT records the decision in §140, adds the brief pointers if he supersedes, and adds the 4b line and the 4c tests.
3. I do a quick check.
4. Part 5 is accepted, and Part 6 (equipment fit, world compatibility, character-creation integration and the final review) can begin when Tyler says so.

## 7. Tyler's decision (September 30, 2026)

**4a resolved: option (a), supersede.** Tyler chose to drop the brief's Cogling "quick steps, frequent turns, efficient climbing, precise hand movements, small physical adjustments" and "fine motor control" as automatic racial traits, the same decision he made for Pipkin. Any later gameplay traits would have to be added deliberately through the race-biology-gameplay review.

ChatGPT should:
- record the decision in Cogling §140 (as Pipkin §37 does)
- add SUPERSEDED pointers to brief §16.12 and to the race-table "fine motor control" entry
- add the 4b line and the 4c tests

After a quick check, Part 5 can be accepted.

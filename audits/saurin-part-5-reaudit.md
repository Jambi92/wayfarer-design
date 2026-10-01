# Re-audit: Saurin v1.0 Part 5

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` at commit `a852078`
**Request:** `reviews/saurin-part-5-reaudit-request.md` (`45ab62d`)
**Responds to:** `audits/saurin-part-5.md`

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS.** The patch implements Tyler's decision, "The tail is a good identifier, however it should not be a punishment for the player and make them easier to hit," and resolves every Part 5 finding.

**Recommendation:** Saurin Part 5 may be accepted by Tyler.

## 2. Verification

| # | Point | Result | Basis |
| --- | --- | --- | --- |
| 1 | Inertia is secondary motion only | **PASS** | §171: no input latency, turn-rate limits, start or stop delay, or root-motion gating. Saurin get the same responsiveness as comparable characters. |
| 2 | No bonus and no penalty | **PASS** | §171 now says "bonus or penalty." |
| 3 | Hurtbox separate | **PASS** | §205 adds combat hurtbox and hit detection as their own layer. |
| 4 | No tail-volume liabilities | **PASS** | New subsection after §206. It covers hurtbox size, direct hits, area effects, snagging, body-blocking, crowds and stealth noise. |
| 5 | Tail stays real for world fit | **PASS** | That subsection's closing paragraph keeps the tail real for animation, furniture, equipment, spacing and environment design. It separates accommodating the tail from punishing the player for it. |
| 6 | SAU-GAME-06, 07 and 08 | **PASS** | They cover control parity including aiming turns, attack, area-effect and crowd parity, and the mass and noise firewalls. |
| 7 | Positive gait signature | **PASS** | §173: pelvic rotation, then lower-axial continuation, then the tail's counter-response, at low amplitude and upright. This is built on Part 1 anatomy, not added shorthand. |
| 8 | SAU-MOVE-13 | **PASS** | |
| 9 | Door closing on the tail | **PASS** | SAU-WORLD-01 |
| 10 | Bow and crossbow sightline | **PASS** | SAU-CAM-02 |
| 11 | Mass-derived systems firewalled | **PASS** | §171 adds carry capacity, encumbrance, stamina, fall damage and knockback. |
| 12 | No regressions | **PASS** | The diff only adds text and extends tests. The mandatory tail, the OPEN swim and breath items, the other firewalls and the no-UE5 status are unchanged. |

## 3. Non-blocking note

Pipkin §37 and Cogling §140 each give the date of Tyler's decision. "Tail Identity Without Punishment" (§171) has no date. Adding "October 1, 2026" in a later patch keeps the decision trail consistent. The register should also record it as AGREED with the Tyler decision noted.

## 4. Completion recommendation

Saurin Part 5 may be accepted by Tyler. The final Saurin part or review begins when he says so.

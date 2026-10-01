# Audit: Saurin v1.0 Part 5, Movement, equipment, world interaction and gameplay boundaries

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` §§168–221 at commit `8d919fe`
**Request:** `reviews/saurin-part-5-audit-request.md` (`b2fb3ec`)
**Compared against:**
- Saurin Parts 1–4 (accepted)
- `rules/character-creation-brief.md` (movement principle, §9 compatibility, §16.13)
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- Pipkin Part 5 and Cogling Part 5 (movement and gameplay boundaries)

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Part 5 carries the approved anatomy into movement and the world without shrinking the race.

Strengths:
- An upright obligate biped with an integrated tail (§169–170). The tail is supported, not dragged (§172).
- The tail participates as biomechanics and is firewalled as gameplay (§171).
- Swimming uses the whole organism without approving "fastest" (§180). The legacy 5× breath and fastest-swimmer claims stay explicitly OPEN, with no physiology inferred (§181–182).
- Clean claw, bite, tail and scale firewalls (§183, §201–204).
- The human animation set is non-authoritative (§190), and equipment adapts to anatomy (§191–198).
- Canonical weapons don't scale with the holder (§199). Reach, collision, equipment and camera are kept separate (§205–208).
- The world must accommodate the tail: seating, beds, tables, crowds, mounts and vehicles (§209–215). Cameras are covered (§216–218).

There's no design contradiction. The request asked me to look for hidden gameplay consequences in the descriptive biomechanics. There are two, and both should be closed before acceptance:
- **4a.** The tail inertia requirements could become control lag.
- **4b.** The tail's real world-space could become a larger hurtbox and a body-blocking penalty.

## 2. The twenty-one requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Upright obligate biped identity | PASS (§169–170). Positive gait signature in 4c |
| 2 | Tail participates without gameplay bonus | PASS for bonuses (§171). Penalty risk in 4a and 4b |
| 3 | Credible tail inertia and rest | PASS as visual (§172, §176). Control coupling in 4a |
| 4 | Walk, run, turn, start-stop, jump, crouch, prone | PASS (§173–179) |
| 5 | Whole-organism swimming, no fastest | PASS (§180) |
| 6 | Legacy breath and swim claims OPEN | PASS (§181–182, SAU-GAME-05) |
| 7 | Climbing, ladders, mantling: no claw or tail advantage | PASS (§183–185) |
| 8 | Body language vs anatomy | PASS (§186) |
| 9 | Membrane and dialogue animation | PASS (§188–189) |
| 10 | Human animation reuse non-authoritative | PASS (§190, SAU-MOVE-12) |
| 11 | Equipment adapts to anatomy | PASS (§191–198) |
| 12 | Canonical weapons don't auto-scale | PASS (§199, SAU-EQP-07) |
| 13 | Tail, bite, claw and scale firewalls | PASS (§201–204) |
| 14 | Collision, reach, equipment and camera separate | PASS (§205–208). Hurtbox missing (4b) |
| 15 | Tail occupies real space, implementation not specified | PASS (§206). Gameplay consequence in 4b |
| 16 | Doors, corridors, seating, beds, tables and crowds use the target anatomy | PASS (§209–213). Minor in 4d |
| 17 | Mounts and vehicles keep the tail | PASS (§214–215) |
| 18 | Third- and first-person camera | PASS (§216–218) |
| 19 | SAU-MOVE, EQP, WORLD, CAM and GAME tests | Good. Additions in 4a, 4b and 4d |
| 20 | Universal rules and race precedents | PASS. Pipkin §37 and Cogling §140 precedents respected; no new supersession |
| 21 | No UE5 | PASS |

## 3. Contradictions

There are none with Parts 1–4, the brief or project rules.

## 4. Findings

### 4a. Tail inertia must not become control lag (should be fixed before acceptance)

§175–176 require visible tail mass in turns, starts and stops. The tail "cannot snap instantly to a new direction" or "ignore inertia." That's right as **secondary motion**. Implemented naively, though, through root motion, turn-in-place gating or blended rotation, it slows the *character's* turns and starts. That would be a hidden agility penalty that the §171 firewall doesn't cover, because §171 only forbids bonuses.

This is a live risk in this project. Tyler's pending movement-fix list already includes **crossbow turn lag**.

**Recommended:** add one line to §171 or §176: "Tail inertia is secondary motion layered on the character's controlled movement. It never adds input latency, turn-rate limits, start or stop delay, or root-motion gating to Saurin control. Whatever turn and acceleration responsiveness gameplay sets for other races applies to Saurin." Add **SAU-GAME-06**: Saurin and Marchfolk proxies get identical input-to-facing and input-to-velocity response, including aiming turns, while the tail visibly lags.

### 4b. Tail space must not become a hidden penalty (should be fixed before acceptance)

§205 separates visual anatomy, collision, interaction reach, combat reach, equipment and camera. It omits **combat hit detection (hurtbox)**. §201 says the tail isn't a damage *dealing* hitbox, but nothing covers *receiving* hits. Tail collision (§206) and crowd spacing (§213) also raise these questions:
- Is a Saurin easier to hit because the tail is a target?
- Can the tail be clipped by area effects?
- Does it snag in doors, block allies in multiplayer, or let others body-block the Saurin by its tail?

Each would be an automatic racial disadvantage arising from anatomy, the mirror image of the bonus firewalls.

**Recommended:**
- Add **hurtbox / hit detection** to the §205 list.
- Add a firewall: "Tail volume doesn't automatically enlarge the Saurin combat target, expose them to extra hits or area effects, or create body-blocking, snagging or crowd-movement disadvantages. Any such consequence needs an explicit gameplay decision."
- Keep the exact collision policy OPEN, as §206 does.
- Add **SAU-GAME-07**: same attack, area effect and crowd pass-through test against Saurin and Marchfolk proxies, with equal gameplay outcome.

### 4c. Positive gait signature (clarification)

The brief says: "Saurin move like reptiles, with the tail as a counterbalance." Part 5 delivers the counterbalance. Every gait line, though, is either the tail or a negative: no sway, no stalking, no whipping, no swagger.

With the tail moving correctly, the body could still walk like a Marchfolk. That's the movement version of "human plus tail," which Part 1 ruled out for the body.

The approved anatomy already provides a positive answer. The pelvis is longer front-to-back, and the lower axial trunk is elongated (Part 1 §6, §9). Pelvic rotation can therefore travel through the long lower trunk into the tail as one visible axial wave, at low amplitude. That differs from the human pattern, where the hips and shoulders counter-rotate with a short waist between them.

**Recommended:** state one positive locomotor relationship along those lines (the author's wording), within the existing limits on sway. Add **SAU-MOVE-13**: Saurin and Marchfolk walk silhouettes at distance. The Saurin should read through axial-pelvic motion, not only through the tail's presence. The tail stays in, per Tyler's rule.

### 4d. Minor, non-blocking

- **Mass-derived systems.** §171 firewalls knockback. Tail mass also counts toward total body mass, so add carry capacity, encumbrance, stamina cost and fall damage to the list. Otherwise a mass-driven physics or encumbrance system could penalize or favor Saurin through the tail.
- **Noise.** §178 covers stealth from the tail being *visible*. Situational ground contact (§172) shouldn't automatically create stealth noise either.
- **Doors closing.** Part 1 §33 listed "doors closing on tails." §209 tests passing through doors, not a door shutting on the tail. Add that to SAU-WORLD-01.
- **Rostrum and first-person aim.** §217 checks the rostrum for visual obstruction. Note that the aiming sightline for bows and crossbows must also stay clear. This ties into the crossbow work on Tyler's movement-fix list.

## 5. Precedent comparison

| Item | Pipkin and Cogling Part 5 | Saurin Part 5 |
| --- | --- | --- |
| Biomechanics vs gameplay | Stride and gait from anatomy, with speed OPEN | Same (§173–174) |
| Brief supersessions | Tyler decisions (Pipkin §37, Cogling §140) | None needed. "Fastest swimmer" and 5× breath stay OPEN, not superseded |
| Canonical equipment | Doesn't scale (Cogling §157) | Same (§199) |
| Penalty firewalls (not only bonuses) | Honest-gait note for small races (Cogling) | Needed for tail inertia and space (4a, 4b) |

## 6. Completion recommendation

1. ChatGPT patches:
   - 4a: no control lag, with SAU-GAME-06
   - 4b: hurtbox and tail-space penalty firewall, with SAU-GAME-07
2. Recommended alongside: 4c and 4d.
3. I re-audit.
4. On a PASS and Tyler's approval, Part 5 is accepted.

The final Saurin part or review shouldn't begin until then.

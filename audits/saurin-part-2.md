# Audit: Saurin v1.0 Part 2, Craniofacial, oral, sensory and auricular foundation

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` §§35–77 at commit `55a67b8`
**Request:** `reviews/saurin-part-2-audit-request.md`
**Compared against:**
- Saurin Part 1 (accepted)
- `rules/character-creation-brief.md` §16.13
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the approved craniofacial sections of Marchfolk, Fenn, Aelari, Vael, Grask, Gorrund, Durrim, Pipkin and Cogling

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Layered Rostral-Cranial Integration is a positive, coherent Saurin skull. It runs low-to-moderate long vault → orbital-temporal platform → compact projecting rostrum → deep jaw base as one continuous structure. It is not a human face with a muzzle, a generic lizard, a dragon or a monster.

Strengths:
- The lateral facial transition zone (§54) is what keeps the rostrum from looking grafted on.
- Orbit, visible eye opening and eyeball are kept separate (§44).
- Neutral anatomy forces no scowl or snarl (§46, §48).
- The bite firewall is sound (§51).
- Horns, frills and crests are firewalled until an explicit decision (§58–59).
- The recessed auricular opening is a real non-mammalian, non-elven ear solution (§56–57).
- Cranial shape has no link to intelligence (§37).
- Sex and age safeguards are in place (§61–63).
- Part 1's carried tail notes and Tyler's attributed decision are preserved.

There's no blocking contradiction. Two items should be fixed before acceptance:
- **4a.** The rostrum is the primary carrier, but its lower bound isn't anchored.
- **4b.** The dentition wording infers diet, against the project rule.

## 2. The nineteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Vault, orbital-temporal, rostral and jaw integration | PASS (§36–37, §54) |
| 2 | Compact rostrum range and constraints | PASS on constraints (§40). Lower bound not set (4a) |
| 3 | Forehead transition | PASS (§41) |
| 4 | Forward-facing eyes, no predator shorthand | PASS (§43–44, §46) |
| 5 | Orbit, opening and eyeball distinct | PASS (§44) |
| 6 | Jaw, mouth and teeth without a bite mechanic | PASS for the bite (§51). Diet wording needs fixing (4b) |
| 7 | Nasal openings not human, crocodile or dragon | PASS (§52–53) |
| 8 | Recessed auricular openings | PASS (§56–57) |
| 9 | Horn, frill and crest firewalls | PASS (§58–59) |
| 10 | Head and neck integration, stature accounting | Integration PASS (§55, SAU-FACE-21). Accounting only partly delivered (4c) |
| 11 | Adult read and age | PASS (§61, §63, SAU-FACE-20) |
| 12 | Non-human sex anatomy | PASS (§62, SAU-FACE-19) |
| 13 | Surface-neutral identity | PASS (§65). Correctly distinguished from the tail decision |
| 14 | Boundaries with other races' faces | PASS. Minor Grask wording (4e) |
| 15 | Face controls and coupled constraints | PASS (§73). Speech is a gap (4d) |
| 16 | SAU-FACE-01 to 22 | Good. One addition in 4a |
| 17 | Part 1 tail notes preserved | PASS (Part 1 status block) |
| 18 | No intelligence, culture or personality inference | PASS (§37, §46, §50, §74) |
| 19 | No UE5 | PASS |

## 3. Contradictions

There's no design contradiction with Part 1, the brief or other races. §50's diet wording conflicts with an AGREED project pattern (4b).

## 4. Findings

### 4a. The rostrum's lower bound isn't anchored (should be fixed before acceptance)

§39 makes rostral projection "a primary racial carrier," and §40 makes rostral length a variable control. §67 says Saurin "cannot become an elf by shortening the rostrum," and SAU-FACE-02 and 12 test the minimum rostrum. But nothing defines where the minimum sits.

Other races already have approved midface projection near the human range:
- Gorrund: "moderate forward projection may be valid without a muzzle," with the prognathism distribution OPEN.
- Grask: a "long integrated midface," with the maxillary and mandibular projection distribution OPEN.

A minimum-rostrum Saurin, with recessed ears neutralized in a silhouette or at distance, could therefore fall inside the approved upper range of those races, or of Marchfolk.

This is one of the rare cases where a **non-overlapping** feature is justified. It's the defining racial structure, like the elven ear point or the Saurin tail.

**Recommended:** state that the minimum valid Saurin rostral projection still sits clearly outside the adult projection ranges of Marchfolk, Grask and Gorrund at normalized head size. "Minimum" should mean the compact end of a true rostrum, not a human midface. Then give SAU-FACE-02 and 12 that pass criterion explicitly.

### 4b. Dentition infers diet (should be fixed before acceptance)

§50 reads: "heterodont enough to support an omnivorous/generalized diet." The project has settled this pattern:
- Grask: AGREED "Grask dentition and diet separation: functional humanoid dentition is the first-pass baseline; no diet inferred." The "omnivorous-style" wording was explicitly removed in the Grask clarification.
- Gorrund: AGREED "functional humanoid dentition baseline with no diet inferred."
- Pipkin and Cogling: the same baseline.

§50's last line ("does not determine … diet preference at the individual level") still implies a population-level diet.

**Recommended:** reword to "functional differentiated dentition (anterior and posterior tooth roles), with no diet inferred from dentition." Keep the rest of §50, including no fangs, tusks, saber teeth or venom, and teeth that fit inside the closed mouth.

### 4c. Stature accounting is a test, not yet a relationship

Part 1 said: "Part 2 must explicitly account for head, neck, thoracic-height, lower-trunk and leg shares." Part 2 adds SAU-FACE-22 to test that the shares add up coherently, but states no relationship.

The head now has useful inputs. A **lower vault** and **forward** rather than vertical facial depth (§38) suggest head *height* share at or below the Marchfolk range, which would help pay for the longer lower trunk.

**Recommended:** one line stating the intended direction, for example: "head height share near or modestly below Marchfolk, with neck share near Marchfolk, so the elongated lower trunk is balanced mainly by head height and thoracic height rather than by shorter legs." This is the author's call; the point is that the accounting gets stated, not only tested.

### 4d. Speech and dialogue articulation (gap, non-blocking)

Saurin have no human external lips by default (§49), a long mouth line (§48), and expression deferred to animation. Wayfarer uses dialogue. Speech articulation and lip sync will need anatomy that can form readable mouth shapes for speech. Otherwise the brief's "eyes and face stay expressive" is only half-met.

**Recommended:** add to §76: "speech articulation and lip-sync capability for the rostral mouth (dialogue animation), without defaulting to human lips." Optionally add a validation case: neutral dialogue line, readable articulation, no grin or snarl.

### 4e. Minor

- **Grask wording (§68).** "Without a snout **or tusks**." Approved Grask text makes tusks "not required," with limited tusk-like canine variation OPEN. Better: "without a snout; tusks not required."
- **FD domains.** Pipkin and Cogling label face tests with the AGREED Facial Diagnostic Domains (FD-STRUCT, FD-SOFT, FD-SURF, FD-HAIR, FD-PRES, FD-OBS). §65 and §75 describe the same separation without labels. For Saurin, FD-HAIR would mostly be empty, and FD-SURF covers scale pattern. Labeling would keep the races consistent.
- **Sensory firewall.** §43 says no gameplay vision bonus. Hearing and smell acuity are OPEN in §35 and §76. Adding one explicit line, "no automatic hearing, smell or vision gameplay bonus," would mirror the bite firewall.

## 5. Cross-race summary

| Race | Status |
| --- | --- |
| Marchfolk | Distinct through vault, rostrum, platform, jaw, nose and ear (§66). Depends on 4a at minimum rostrum |
| Elves (Fenn, Aelari, Vael) | Distinct (§67) |
| Grask | Distinct through forward projection vs vertical elongation (§68). Needs 4a's floor and the 4e wording |
| Gorrund | Distinct through the rostral chain vs Transverse Structural Continuity (§69) |
| Durrim | Distinct (§70), consistent with the corrected Durrim anchor |
| Pipkin and Cogling | Distinct (§71–72), consistent with their approved anchors |

## 6. Completion recommendation

1. ChatGPT patches 4a (rostrum floor and pass criteria) and 4b (dentition wording).
2. Recommended: 4c, 4d and 4e.
3. I re-audit.
4. On a PASS and Tyler's approval, Part 2 is accepted.

Part 3 should not begin until then.

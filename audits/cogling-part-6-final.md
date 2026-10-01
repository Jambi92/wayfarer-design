# Final audit: Cogling v1.0 Part 6 and first-pass consistency

**Auditor:** Claude
**Audited file:** `specs/cogling/COGLING_V1.md` at commit `d949842`
**Request:** `reviews/cogling-part-6-final-audit-request.md`
**Compared against:**
- Cogling Parts 1–5 and their audits
- `rules/character-creation-brief.md`
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- Pipkin Part 6 (FIRST-PASS COMPLETE) as the precedent for this stage
- the approved Marchfolk, Pipkin, Durrim, Fenn, Sagekin and Grask specs

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS. Two corrections are needed before FIRST-PASS COMPLETE.**

No blocking design contradiction remains across Cogling Parts 1–6, project rules, the register or the comparison races.

Part 6 covers these well:
- approved anatomy over the ~125 cm prototype
- unified data without forcing one skeleton
- no uniform height scaling
- fit that preserves hands, fingers, head and joints
- canonical objects
- world-scale consequences documented rather than hidden
- seven separable systems (§186)
- truthful cameras
- creator modes, presets, randomization and locks
- saved appearances, including no raw cross-race transfer (§198)
- an anti-stereotype NPC rule
- the anti-convergence review, stereotype firewall and consolidated identity statement

The Part 5 cleanup is all present in the spec:
- Tyler's decision in §140
- the equal-speed and walk-run line
- the cognition firewall
- FD-HAIR with eyebrows
- COG-MOVE-25 to 27

**The two corrections both come from completion criteria 2 and 3 in §208:**
- **3a.** The consolidated OPEN list leaves out items that earlier parts left OPEN. This is the same issue Pipkin Part 6 had.
- **3b.** The brief still carries the Cogling wording Tyler superseded, with no pointer. This was an accepted Part 5 audit item.

## 2. The eighteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Approved anatomy over the prototype | PASS (§173, COG-WORLD-20) |
| 2 | Unified data, no forced skeleton | PASS (§174) |
| 3 | No uniform height scaling | PASS (§175) |
| 4 | Equipment fit preserves anatomy | PASS (§176–179, COG-WORLD-15 to 17) |
| 5 | Canonical objects don't auto-scale | PASS (§180, COG-WORLD-13 and 14) |
| 6 | World-scale consequences exposed | PASS (§181–185, COG-WORLD-01 to 09) |
| 7 | Visual, collision, reach, IK, contact and camera separable | PASS (§186–188) |
| 8 | Camera and dialogue at actual scale | PASS (§189, COG-WORLD-11, 12 and 18) |
| 9 | Creator modes, presets, randomization, locks and saves match the project | PASS (§191–198, COG-CC-01 to 15) |
| 10 | NPC generation can't stereotype | PASS (§199, COG-CC-13) |
| 11 | World validated against 76–107 cm, not 125 cm | PASS (§173, §201, COG-WORLD-20) |
| 12 | Validation casts | PASS. Minor note in 3c |
| 13 | Anti-convergence with Marchfolk, Pipkin, Durrim, Fenn, Sagekin and Grask | PASS (§204), consistent with each approved anchor |
| 14 | Stereotype firewall complete | PASS (§205) |
| 15 | Final identity consolidates Parts 1–5 | PASS (§206) |
| 16 | Consolidated OPEN list complete | **Needs correction** (3a) |
| 17 | Accepted prior findings present | **Mostly.** The brief pointers are missing (3b) |
| 18 | No UE5 implementation | PASS |

## 3. Findings

### 3a. The consolidated OPEN list omits items earlier parts left OPEN (required before completion)

§207 is missing these items, each left explicitly OPEN in an earlier part:

| Item | Source |
| --- | --- |
| Thoracic dimensions, pelvic morphology (breadth, depth, height, inlet and outlet), and shoulder and clavicular dimensions | Part 1 §35; Part 2 §72 (only partly covered by "exact body segment ratios") |
| Hand, palm and finger proportions; foot proportions and arch distribution | Part 2 §72 |
| Joint dimensions and long-bone robusticity distribution | Part 2 §72 |
| Muscular Development Capacity distribution | Part 2 §57, §72 |
| Body-fat distribution tendencies | Part 2 §60, §72 |
| **Morphology** of sex-related dimorphism, not just "distribution magnitudes" | Parts 1–3 |
| **Face and expression readability at an adult head size of about 11–13 cm** | Part 1 §35, Part 3 §99 |
| **Dentition:** tooth count, replacement, eruption timing, wear and lifecycle | Part 4 §118A |
| Magical eye effects | Part 4 §136 |
| Cosmetics, tattoos and piercing culture | Part 4 §136 |
| Facial animation implementation; camera and rendering implementation | Part 3 §103 |
| **Class restrictions and racial stats** for the prototype | Part 1 §35. Pipkin listed both "racial attribute bonuses" and "any final race/class restriction" |
| In-game Cogling race description text revision | Plan gap #9; Pipkin's list includes it |
| Ear mobility | Not addressed for Cogling; Pipkin listed it as OPEN |

**Recommended:** add the items above to §207. No design changes are needed.

### 3b. Brief still carries the superseded Cogling wording (required before completion)

Tyler superseded the brief's Cogling movement and fine-motor language. §140 records his decision. The Part 5 audit (§7) then asked for SUPERSEDED pointers in the brief, as Pipkin's were added at commit `4e0d9f1`. `rules/character-creation-brief.md` is unchanged, and the outdated text appears in three places:

| Brief location | Outdated text |
| --- | --- |
| Line 62, race table | "…expressive face, **fine motor control**." |
| Line 76, §16.12 anatomy bullet | "…an expressive face and **fine motor control**." |
| §16.12 movement line | Brief's Cogling movement line ("quick steps, frequent turns, efficient climbing, precise hand movements and small physical adjustments") |

**Recommended:** add pointers to Cogling Part 5 §140–141, in the same form as Pipkin's. ChatGPT authors `rules/`.

### 3c. Minor (optional)

- **Permanent validation suite.** Pipkin Part 6 stated which validation cases form the permanent suite: every approved case plus the integration cases. Cogling has seven validation families (COG-BODY, FACE, SURF, MOVE, WORLD and CC) but no consolidation statement. One sentence would do. It should also note which IDs are retired (COG-BODY-25 and 26).
- **Universal-review dependencies.** §208 names only the Short-Race Comparative Anatomy Review. Pipkin §36 also listed:
  - the Universal Facial Customization Architecture Review
  - cross-race pigmentation work
  - the race-biology-gameplay review
  - world-scale accessibility across the roster
  - the technical architecture review

  It also stated that any of these not yet formally registered leave the underlying item OPEN. A parallel short section would keep the two short races consistent.
- **Prototype ledger.** §173 records the scale conflict. The prototype's other shortcuts are covered by the principles in §174–186 but aren't listed: one shared human animation set, holder-scaled weapons and a single human-based capsule. Pipkin §34 listed them. Optional.

## 4. Consistency sweep, Cogling Parts 1–6

**Identity chain.** Each part builds on the one before:
- Part 1: Fine-Scale Elongated Articulation, patched to near-human limb totals with distal redistribution.
- Part 2: narrow stable core.
- Part 3: Fine-Scale Planar Integration, with the face-to-vault relationship and angled junctions.
- Part 4: overlapping surface traits, so surface isn't identity.
- Part 5: movement from anatomy, with the supersession decision.
- Part 6: integration, followed by the §206 identity statement. The chain is consistent throughout.

**Child read.** It is the most demanding in the roster (76 cm is toddler height), and it is covered at every layer:
- Body: COG-BODY-11
- Face: COG-FACE-20 and the face-to-vault relationship
- Surface: COG-SURF-08
- Movement: COG-MOVE-25

**Boundaries:**
- **Pipkin overlap zone:** body, face, surface and movement are each multi-factor.
- **Durrim:** separated without any shared height range.
- **Fenn, Sagekin and Grask:** separated at normalized height.

**Authority:** the prototype is non-authoritative everywhere. The brief supersession is recorded in the spec, but the brief pointers are still missing (3b).

## 5. Completion recommendation

1. ChatGPT patches 3a in §207, and patches 3b by adding pointers in `rules/`.
2. 3c is optional.
3. I do a quick check of those two items. No full re-audit is needed.
4. Cogling v1.0 is then **FIRST-PASS COMPLETE**, on Tyler's confirmation.
5. The **Short-Race Comparative Anatomy Review** (Durrim, Pipkin and Cogling) is the immediate next design task, as §208 and PROJECT_RULES require. The comparative review was not started here.

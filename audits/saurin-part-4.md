# Audit: Saurin v1.0 Part 4, Age, individual variation and character-creator integration

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` §§126–167 at commit `ebd4561`
**Request:** `reviews/saurin-part-4-audit-request.md` (`846f80b`)

**Compared against:**
- Saurin Parts 1–3 (accepted)
- `rules/character-creation-brief.md` §3–4 and §9–14
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`, specifically:
  - the consistency-resolution layer and age rules
  - Sagekin population randomization
  - Vael preset rules
  - Halvren inheritance rules
- Pipkin and Cogling creator integration

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Part 4 turns Saurin biology into a coherent creator space.

Strengths:
- **Adult scope and age.** The creator is adult-only, with juvenile safeguards (§127). The AGREED three-way age split is used (§128), and aging is systemic with a frailty firewall (§130).
- **Asymmetry.** Natural and acquired asymmetry are kept separate (§132–133).
- **Populations.** Population weighting has no subraces (§134–136).
- **Randomization and presets.** Simple and Advanced Modes produce real presets (§138–140). Biological and presentation randomization are separate (§141–142), and selective randomization works with locks (§143–144).
- **Locked identity features.** There's no tail on/off, and tail length, base and mass are coupled (§145). The rostrum floor is absolute (§146). Vertical pupils can't be swapped for round ones (§149).
- **Safeguards.** Human hair assets are blocked (§155), and NPCs follow the same rules as players (§157).
- **Validation.** Combined-proportion validity goes beyond simple clamping (§158), and invalid-combination handling preserves player agency (§159).
- **Experience.** First-person and dialogue requirements are covered (§163–164).

There's no design contradiction with Parts 1–3. Three items should be fixed before acceptance, because they conflict with AGREED project rules or with the brief:
- **4a.** Inheritance is named by skin layer instead of architecture layer.
- **4b.** Population weighting doesn't protect the full valid range in manual creation.
- **4c.** Acquired-history randomization has no home, although the brief requires it.

## 2. The twenty-five requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Adult-only scope, juvenile safeguards | PASS (§127, SAU-CC-13) |
| 2 | Chronological, apparent and presented age | PASS (§128) |
| 3 | Systemic aging without frailty | PASS (§129–130) |
| 4 | Natural vs acquired asymmetry | PASS (§132–133, SAU-CC-14) |
| 5 | Population weighting without subraces | PASS (§134–135). Manual range in 4b |
| 6 | Ancestry, culture and background separate | PASS (§136) |
| 7 | Universal four-layer model | PASS (§137). Inheritance naming in 4a |
| 8 | Simple and Advanced Mode, preset legitimacy | PASS (§138–140, SAU-CC-01) |
| 9 | Biological vs presentation randomization | PASS (§141–142, SAU-CC-04). Acquired history in 4c |
| 10 | Selective randomization and locks | PASS (§143–144, SAU-CC-05, 06, 15, 16) |
| 11 | Tail controls: no on/off, coupled length, base and mass | PASS (§145, SAU-CC-07). Note in 4e |
| 12 | Rostrum floor protected | PASS (§146, SAU-CC-08) |
| 13 | Regional scale, pattern, eye, ridge and claw controls | PASS (§147–151). Pupil note in 4e |
| 14 | Composition and body-fat independence | PASS (§152–153). Matches AGREED amount vs distribution |
| 15 | Sex anatomy reserved, no human default | PASS (§154) |
| 16 | Race-aware empty hair categories | PASS (§155, SAU-CC-19) |
| 17 | Saving, reuse and NPC parity | PASS (§156–157). NPC note in 4e |
| 18 | Combined-proportion validity | PASS (§158) |
| 19 | Invalid-combination handling preserves agency | PASS (§159) |
| 20 | Weighted randomization, not uniform extremes | PASS (§160, SAU-CC-24) |
| 21 | Inheritance firewall | PASS on content (§161). Naming in 4a |
| 22 | Observation, first person and dialogue | PASS (§162–164, SAU-CC-20 to 22) |
| 23 | SAU-CC-01 to 25 | Good. Additions in 4c and 4d |
| 24 | No culture, class or personality in biology | PASS (§140, §152, §161, §167) |
| 25 | No UE5 | PASS |

## 3. Contradictions

There's no design contradiction. Two wording conflicts with AGREED register rules (4a, 4b) and one gap against the brief (4c) are listed below.

## 4. Findings

### 4a. Inheritance is named by skin layer (should be fixed before acceptance)

The register has an AGREED rule from consistency resolution Part 1 §7: "Inheritance names the architecture layer, and skin layers aren't inheritance categories."

§161 says inheritance may influence "anatomy, pigmentation, pattern, scale morphology, **other approved Natural traits**." §137 says pigmentation "remains Natural appearance," but doesn't say which of the four architecture layers stores it. §156 lists "Natural appearance" alongside the architecture layers as saved data. Natural is the appearance layer; it isn't where inherited traits are stored.

**Recommended:**
- State that inherited pigmentation, pattern, scale morphology, eyes, ridges and claw keratin are stored in the **Anatomy** layer (Biological Anatomy), and that they *appear* through the Natural Skin Appearance Layer.
- In §161, replace "other approved Natural traits" with "other approved inherited Anatomy-layer traits."
- In §156, list saved data by architecture layer, and keep Environmental and Acquired state separate.

### 4b. Manual choice doesn't keep the full valid range (should be fixed before acceptance)

The register has an AGREED rule from Sagekin v1.4 §3: "Population-aware randomization for inherited traits, **while manual choice keeps the full valid range**."

§134–135 and §160 weight randomization correctly. But nothing says that population weighting, or a later ancestry selection, can't narrow what the player can set by hand. "Population-level variation may affect probabilities" (§134) is close, but §136 lets ancestry influence "biological probability distributions" without a manual-choice guarantee.

**Recommended:** add one line: "Population and ancestry weighting affects randomization and NPC generation only; Advanced Mode manual choice always keeps the full valid Saurin range." Extend SAU-CC-25 to check it.

### 4c. Acquired-history randomization has no home (should be fixed before acceptance)

Brief §11 lists Randomize options including **"Scars and Tattoos."** Part 4 assigns:
- §141 Biological Randomization: no acquired history
- §142 Presentation Randomization: no scars

Acquired history, such as scars, damaged scales, chipped claws, damaged ridges and contact wear (Part 3 Acquired layer, §133), therefore fits neither. Tattoo-equivalents are Applied and belong in Presentation.

**Recommended:** add a third, separate randomization domain, "Acquired-History Randomization," that samples only the Acquired layer. It never alters anatomy, and it can be locked on its own. Excluding major rostral, jaw and tail loss stays OPEN. Add SAU-CC-26: acquired-history randomization changes no inherited anatomy and doesn't create major loss states.

### 4d. Creator-level gameplay firewall (clarification)

Each trait already has its own firewall in Parts 1–3: tail, claws, eyes, scales, bite and venom. Part 4 is where players *choose* those values, and it has no creator-level statement. The obvious min-max risks are a longer tail, longer claws, maximum stature or heavier relief.

**Recommended:** add one line: "No creator value (stature, frame, composition, tail, rostrum, claws, scales, ridges, eyes or age) carries an automatic gameplay statistic; any later race-gameplay effect requires its own decision." Optionally add SAU-CC-27: extreme valid builds have identical gameplay stats.

### 4e. Minor, non-blocking

- **Pupil dilation is a state (§149).** Dilation varies with lighting, so it isn't identity. The creator should *preview* dilation, but the stored biology is pupil shape and its dilation range, not a chosen dilation. Otherwise a saved character could carry a fixed slit, which §95 forbids as a fixed expression.
- **Tail controls and layers (§145).** Tail length, base and taper belong to Anatomy and Frame, while tail muscularity and adiposity belong to Physical Composition. Saying so lets body composition changes carry into the tail coherently, which SAU-CC-23 depends on. My Part 1 re-audit note 3 also still applies: state the base-to-length coupling as a relationship (for example, a longer tail needs a proportionally supported base), not only as "coupled."
- **NPC narrative exceptions (§157).** This is compatible with the AGREED Vael rule ("no preset-exclusive anatomy") as long as an exception is marked as non-baseline and never feeds player presets or randomization. Add that clause.
- **Tail range and world space.** Creator tail extremes should be checked against the Part 1 world-space proxies (SAU-BODY-20) before the ranges are finalized. This can wait for Part 5 or the equipment work.

## 5. Precedent comparison

| Item | Pipkin and Cogling | Saurin Part 4 |
| --- | --- | --- |
| Adult-read safeguards | Child-comparison tests | Equivalent, using juvenile-anatomy safeguards (no same-height child overlap) |
| Presets as real outputs | Yes | Yes (§138–140) |
| Race-aware empty categories | Not needed | Yes (§155) |
| Mandatory racial structure locked | Not applicable | Tail and rostrum floor (§145–146) |
| Gameplay firewall | Per trait, in the movement part | Per trait in Parts 1–3. Creator-level line recommended (4d) |

## 6. Completion recommendation

1. ChatGPT patches 4a (inheritance naming), 4b (manual full range) and 4c (acquired-history randomization and SAU-CC-26).
2. Recommended alongside: 4d and 4e.
3. I re-audit.
4. On a PASS and Tyler's approval, Part 4 is accepted.

Part 5 should not begin until then.

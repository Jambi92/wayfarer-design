# Audit: Cogling v1.0 Part 4, Surface phenotype, hair, eyes and age presentation

**Auditor:** Claude
**Audited file:** `specs/cogling/COGLING_V1.md` at commit `b901bab`
**Request:** `reviews/cogling-part-4-audit-request.md`
**Compared against:**
- Cogling Parts 1–3
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`, especially the AGREED Facial Diagnostic Domain and Skin Appearance Layer rules
- Pipkin Part 4 as accepted, with its audit and re-audit
- the Marchfolk, Durrim, Grask and Gorrund surface rules

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Part 4 is broad and overlapping, and it avoids every stereotype it targets:
- no workshop-pale or ruddy-gnome palette
- no freckles as a youth marker
- no bearded tinkerer, inventor brows or wizard elder
- no "cute Cogling" bundle
- no eyes or lashes enlarged for readability

It handles the age model, the cosmetics firewall and small-scale readability well (§130–131), including the point that hair-strand diameter doesn't scale linearly with body height.

There are no design contradictions. One finding should be resolved before acceptance (4a): whole-body surface needs the AGREED Skin Appearance Layers, the same correction Pipkin Part 4 needed. The other items are minor.

## 2. The eighteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Surface is broad, overlapping and secondary | PASS (§106, §137) |
| 2 | No narrow palette or occupational stereotype | PASS (§107) |
| 3 | Pigmentation isn't a single flat color | PASS (§108) |
| 4 | Freckles and texture aren't youth or adulthood shortcuts | PASS (§109–110) |
| 5 | Hair is broad, with no racial hairstyle | PASS (§111–112) |
| 6 | Facial and body hair optional, not shorthand | PASS. One wording note (4c) |
| 7 | Eyes not enlarged; iris separate from magic | PASS (§115–118) |
| 8 | The three age concepts stay separate | PASS (§119) |
| 9 | Young adults structurally adult | PASS (§120, COG-SURF-08 and 11) |
| 10 | No wizard or inventor elder | PASS (§122, COG-SURF-10) |
| 11 | Ancestry correlation is probabilistic | PASS (§125) |
| 12 | Cosmetics, scars, tattoos and piercings are presentation or acquired | PASS (§126–128) |
| 13 | Attractiveness and cuteness firewall | PASS (§129, COG-SURF-14) |
| 14 | Readability doesn't justify exaggeration | PASS (§130–131, COG-SURF-15) |
| 15 | FD-domain separation | **Needs correction** (4a) |
| 16 | Randomization and presets avoid bundles | PASS. Interim note in 4d |
| 17 | Validation proves overlap with Marchfolk and Pipkin | PASS (COG-SURF-16 and 17) |
| 18 | No culture, movement, gameplay or UE5 decided | PASS (§136) |

## 3. Contradictions

None in design.

Two wording points touch AGREED rules and are covered in 4a and 4c:
- the scope and wording of the Facial Diagnostic Domains
- body hair being "independent from sex-related anatomy"

## 4. Findings

### 4a. Whole-body surface needs the Skin Appearance Layers (should be fixed before acceptance)

The AGREED rule (consistency resolution Part 1 §7) says Character Architecture Layers are separate from the **Skin Appearance Layers**: 1 Natural, 2 Environmental, 3 Applied or Acquired. The AGREED Durrim patch limits the FD domains to "facial analysis only."

Part 4 has three problems against that:
- §132 introduces the FD domains but never says they're facial-only.
- Whole-body surface (tanning in §108, environmental exposure in §110, weathering and scars in §127, body hair in §114) has no layer framework at all.
- §132 repeats the two wording differences flagged in the Part 3 re-audit (3a), which haven't been fixed yet:
  - FD-PRES includes "scars where treated as presentation," while the AGREED FD-SURF covers "scars where appropriate."
  - FD-OBS reads "camera, lighting, animation and rendering," while the AGREED wording is "lighting, camera, expression, pose."

Pipkin Part 4 had exactly this gap and fixed it in its §16 and §18.

**Recommended:**
- State that the FD domains are for facial analysis only, using their AGREED meanings.
- Map whole-body surface to the Skin Appearance Layers:
  - Natural: base pigmentation, undertones, freckles, natural markings, vascular visibility.
  - Environmental: tanning and weathering.
  - Applied or Acquired: scars, burns, tattoos, cosmetics, paint.

### 4b. Teeth aren't covered (minor)

Neither Part 3 nor Part 4 mentions Cogling dentition. Grask, Gorrund and Pipkin all record the AGREED **functional adult humanoid dentition baseline, with no diet inferred**. Pipkin adds explicit anti-caricature rules: no oversized incisors, no rodent or childlike teeth.

At Cogling scale, "tiny pointed teeth" or "childlike teeth" are real stereotype risks.

**Recommended:** one short section stating that the same baseline applies, that childlike, rodent-like and oversized teeth are excluded, and that count, replacement and lifecycle stay OPEN.

### 4c. Body hair is "independent from sex-related anatomy" (wording)

§114 says body hair "remains independent from … sex-related anatomy." The project approach elsewhere:
- Pipkin: sex-related and hormonal distributions are OPEN and use **soft correlations**.
- Durrim: "Durrim facial-hair sex-related distributions are OPEN."
- Cogling §136 itself lists "detailed facial/body-hair growth distributions" as OPEN.

"Independent" pre-decides that open question. **Recommended:** reword to "not determined by sex-related anatomy; any sex-related distributions are OPEN and use soft correlations." The same applies to the "scalp hair" and "facial hair" items in that list.

### 4d. Interim randomization (minor)

§133 says biological randomization samples "from broad biologically valid distributions," but all frequencies are OPEN (§112, §117, §136). Pipkin Part 4 §19 added a line saying interim sampling is "not an approved population distribution." Adding the same line keeps test content from becoming de facto canon.

### 4e. Neutral-gray test hides eyebrows (note only)

COG-SURF-12 removes the eyebrows. That's correct for FD-STRUCT testing. Part 3's §100 uses the same convention ("eyebrows neutralized where practical"), so it's consistent. No change needed.

## 5. Cross-population summary

| Race | Status |
| --- | --- |
| Marchfolk | Surface overlap is expected and tested (COG-SURF-16) |
| Pipkin | Overlap tested (COG-SURF-17). Cogling Part 4 parallels Pipkin Part 4, apart from 4a and 4b |
| Durrim | No ruddy or red-hair coding, matching Durrim's AGREED anti-stereotype rules |
| Fenn and elves | No elven palette imported. The Elf Review rule ("shared elven identity is anatomical, not cosmetic") is respected by analogy |

## 6. Completion recommendation

1. ChatGPT patches 4a: Skin Appearance Layers and FD wording, which also closes Part 3 re-audit item 3a.
2. Recommended: 4b, 4c and 4d.
3. I re-audit.
4. On a PASS and Tyler's approval, Part 4 is accepted.

Part 5 should not begin until then. When Part 5 reaches movement, the brief's Cogling movement and fine-motor wording needs Tyler's explicit decision (Part 1 audit §5).

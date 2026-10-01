# Audit: Pipkin v1.0 Part 4, Surface Phenotype and Visible Biological Traits

**Auditor:** Claude
**Audited file:** `specs/pipkin/PIPKIN_V1.md` at commit `40000ae`
**Request:** `reviews/pipkin-part-4-audit-request.md`
**Compared against:**
- Pipkin Parts 1–3
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`, in particular the AGREED Facial Diagnostic Domain and Skin Appearance Layer rules
- the Marchfolk, Durrim, Fenn, Grask, Gorrund and Halvren specs

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Part 4 avoids the stereotypes it targets:
- no ruddy or freckled halfling
- no hairy feet
- no rodent teeth
- no hidden phenotype bundle
- no ethnic mapping

It keeps surface biology overlapping and secondary, as intended.

One item conflicts with AGREED terminology and should be fixed before acceptance (4a). Two statements claim approvals that don't exist (4b, 4d). One section that every other race's Part 4 covers is missing (4c).

The Part 3 acceptance text and the corrected Part 2 resolution wording are both fine.

## 2. Contradictions

None with Parts 1–3. Points checked:
- **Ears:** secondary, unchanged.
- **Facial hair:** never identity or adulthood.
- **Body hair:** no youth or sex coding (Part 3 §11–13 matches).
- **Nails:** ordinary nails (Parts 1–2).
- **Teeth:** mature dentition fitted to the Part 3 dental arches.
- **Identity order:** trunk primary, face secondary (Part 3 status note).

## 3. The ten requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Surface separate from structure, culture, presentation and rendering | PASS (§1, §2, §17, §18). Terminology issue in 4a |
| 2 | No mapping to a real-world ethnicity or hidden halfling phenotype | PASS. §2 sets no complexion default; §18 forbids a "fair + freckles + curly brown hair" bundle; the stress test in §20 guards the reverse case |
| 3 | Biological coherence of skin, tanning, freckles, vascularity, iris, hair, body hair, nails, teeth and mucosa | PASS at first-pass level. Tanning isn't inferred from base complexion; palms, soles and lips can differ naturally; sclera is ordinary; facial-hair color needn't match scalp hair |
| 4 | No contradiction with Parts 1–3 or project rules | PASS on design. 4a and 4b are rule-wording issues |
| 5 | Overlap with Marchfolk, Durrim and Fenn | PASS. PIP-SURF-18, 19 and 20, and two stress cases, push identity back to structure. Matches the approved Durrim surface rule (ruddiness and red hair not required) |
| 6 | Teeth not over-specified | PASS. Matches the AGREED Grask and Gorrund baseline of functional humanoid dentition with no diet inferred. See 4d on the review it cites |
| 7 | FD domains used consistently | **Needs correction** (4a) |
| 8 | No hard phenotype packages | PASS (§18); soft hair-to-skin correlation only "where biologically appropriate" |
| 9 | Validation covers stereotype, child-read and cross-race risks | PASS, with gaps noted in 4c and §5 |
| 10 | What stays OPEN | See §6 |

## 4. Findings

### 4a. Facial Diagnostic Domains are used outside their agreed scope (should be fixed before acceptance)

The Durrim consistency-resolution patch made these AGREED:
- FD-STRUCT, FD-SOFT, FD-SURF, FD-HAIR, FD-PRES and FD-OBS are Facial Diagnostic Domains, "for facial analysis only."
- They are defined as:
  - FD-STRUCT: cranium and facial skeleton
  - FD-SURF: skin surface
  - FD-HAIR: eyebrows, facial and scalp hair
  - FD-OBS: lighting, camera, expression and pose

Part 4 §17 departs from this in three ways:
- It applies the domains to whole-body surface validation, and the §20 stress tests use them for body hair and feet.
- It redefines FD-STRUCT as "underlying skeletal structure" and FD-OBS as the "final observed result under lighting/material/render," dropping expression and pose.
- It never uses the AGREED **Skin Appearance Layers** (1 Natural, 2 Environmental, 3 Applied or Acquired), which are the agreed body-surface vocabulary.

**Recommended:**
- Keep the FD domains for the face, with the AGREED definitions.
- Organize body surface by the Skin Appearance Layers:
  - Natural: pigmentation, freckles, birthmarks, vascularity.
  - Environmental: tanning and weathering.
  - Applied or Acquired: scars, tattoos, cosmetics.
- If an FD-like scheme for the whole body is wanted, propose it as a universal change for Tyler's approval, not as a Pipkin-local redefinition.

### 4b. The iris range claims a world-level approval that doesn't exist

§5 says the iris range is "the broad natural/fantasy-humanoid biological range approved at the world level." No world-level iris range is approved. The register has:
- the Marchfolk iris envelope (AGREED: brown through blue and gray)
- a PRELIMINARY universal rule that iris color is separate from magical effects
- OPEN iris frequencies for the elves and Halvren

**Recommended rewording:** "a broad natural humanoid range, with validity and frequencies OPEN for the cross-race pigmentation review." Separately, "fantasy-humanoid" invites non-natural colors that nothing has approved. If unusual natural irises are wanted, they should be a decision of their own.

### 4c. No aging or environmental-appearance section

Every completed race's Part 4 covers pigmentation, skin, hair color, eyes, **aging and environmental appearance** (Durrim, Grask and Gorrund all do). Pipkin Part 4 covers graying and tanning only. These are missing:
- skin aging (texture, elasticity, wrinkling, age-related pigment change)
- environmental weathering, including the proposed universal regional weathering by face, hands, forearms and feet (Skarn v1.3)
- the separation between apparent biological age and surface age

The child-read risk makes this matter for Pipkin in particular. The youngest-adult stress tests rely on structure to read as adult, which is correct, but elder Pipkin surface aging hasn't been validated anywhere. The Pipkin lifecycle is OPEN (Part 1).

**Recommended:** add a short aging and environmental section mapped to the Skin Appearance Layers, plus an elder surface case (for example PIP-SURF-21: an elder with aged skin and graying; age reads through surface and soft tissue while race reads through structure). Or state explicitly that this is deferred to Part 5.

### 4d. "Future universal dentition review" isn't a registered review

§13 defers tooth count and replacement to "the future universal dentition review." That review is listed in neither `decisions/PROJECT_RULES.md` (Reviews still required) nor the register. Grask and Gorrund settled dentition differently: an AGREED functional humanoid baseline, with details OPEN per race.

**Recommended:** either reference those baselines and keep the Pipkin details OPEN, or have Tyler add a universal dentition review to the required reviews. Otherwise the deferral points to something that doesn't exist. I've logged it as OPEN in the register.

### 4e. Interim randomization while frequencies are OPEN (minor)

All Pipkin pigmentation frequencies are OPEN, and §18 weights randomization only "once those distributions are approved." That leaves interim behavior undefined: uniform sampling across a "very low through very high" range would itself be a frequency choice.

**Suggested:** one line saying interim randomization draws broadly across the valid envelope and that this is not an approved distribution. Gorrund's complexion frequencies are in the same OPEN state.

### 4f. "Allele" wording (minor)

§2's "exact allele/population-frequency models" implies a genetic simulation. Genetic simulation depth is OPEN (Halvren Part 1). "Population-frequency models" alone avoids pre-judging it.

## 5. Cross-population notes

- **Marchfolk:** the Pipkin skin range exceeds nothing in the AGREED Marchfolk envelope ("fair through deep brown"), so overlap is total by design. That's correct, since surface isn't identity.
- **Durrim:** consistent with Durrim's AGREED anti-ruddy and anti-red-hair rules.
- **Fenn:** PIP-SURF-20 is present. The Elf Review rule ("shared elven identity is anatomical, not cosmetic") is mirrored.
- **Gorrund:** the earlier Gorrund issue (a lighter-complexion exclusion, flagged as a racial-coding risk) doesn't recur here. Pipkin exclude no complexion.
- **Cogling:** no claims made. Correct.
- **Gap:** no like-for-like sex surface case. Sex-related body-hair and facial-hair distributions are OPEN, so this is optional now.

## 6. What should stay OPEN for the universal pigmentation and surface review

- skin, hair and iris frequencies, and any population center
- the rare hair and iris colors list
- tanning-response and freckling distributions
- normal scleral tint range and visible flushing (already OPEN for Grask)
- sex-related body-hair and facial-hair distributions
- dentition count and lifecycle
- the skin-detail architecture (moles, lentigines)
- the regional weathering system
- the whole-body diagnostic vocabulary, if one is wanted beyond the Skin Appearance Layers

## 7. Completion recommendation

1. ChatGPT patches 4a (terminology) and 4b (iris wording).
2. ChatGPT either adds the aging and environmental section from 4c or explicitly defers it to Part 5.
3. ChatGPT resolves the dentition reference in 4d.
4. 4e and 4f are optional.

With those done, Part 4 can be marked first-pass accepted. Part 5 should not begin until Tyler says so.

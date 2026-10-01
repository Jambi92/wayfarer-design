# Audit: Short-Race Comparative Anatomy Review v1.0 (Durrim, Pipkin, Cogling)

**Auditor:** Claude
**Audited file:** `reviews/short-race-comparative-anatomy-v1.md` at commit `95fbbfb`
**Request:** `reviews/short-race-comparative-anatomy-audit-request.md`
**Compared against:**
- `specs/durrim/DURRIM_V1.md`
- `specs/pipkin/PIPKIN_V1.md`
- `specs/cogling/COGLING_V1.md`
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`

These are findings, not changes. No canonical spec or the review was edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** The review frames the question correctly: can the three short races stay distinct from anatomy alone, when height, composition, surface and culture overlap? It answers with three different mechanisms rather than one short-body slider.

What it gets right:
- the structural-mass axis with its "not a linear morph" caveat (§4)
- the boundary rules (§5–6)
- the composition-inversion failure list (§11)
- 12 comparative validation cases (§12)
- per-race validity envelopes inside a shared schema (§13)
- an anti-stereotype randomization rule (§14)
- the twofold world range (§15)
- the gameplay firewall, which leaves the legacy traits open (§17)

There's no blocking convergence. Four accuracy and completeness items need correcting before acceptance:
- §3a and §3b: two anchors are misstated or thinned.
- §3c: the most useful Pipkin–Cogling carrier is missing.
- §3d: the review's own completion gate 3 requires canonical cross-reference updates.

## 2. The twelve requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Body anchors accurate | Cogling and Durrim: PASS. Pipkin: missing the trunk-share carrier (3c) |
| 2 | Cogling–Pipkin 91–107 cm overlap separated by anatomy | PASS in principle; strengthen with 3c |
| 3 | Pipkin–Durrim boundary at about 122 cm | PASS (SR-COMP-03, §5–6) |
| 4 | Structural-mass axis useful without a linear morph | PASS (§4 caveats) |
| 5 | Central body, limb, hand, foot and face comparisons | Body, limb, hand and foot: PASS. Face: two anchors misstated (3a, 3b) |
| 6 | Ear and surface overlap | PASS; Pipkin ear wording note (3b) |
| 7 | Composition stress | PASS (§11, SR-COMP-10) |
| 8 | The 12 validation cases | PASS. They cover both overlap ends, the boundary, normalized, silhouette, partial-obscure, face, surface swap, composition inversion, child firewall and movement neutralization |
| 9 | Creator and randomization | PASS (§13–14) |
| 10 | World and equipment across 76–152 cm | PASS (§15–16) |
| 11 | Gameplay stays OPEN | PASS (§17). Durrim breath and swimming are correctly legacy traits under review (Durrim Part 1 §40–43 and Part 5 §24–25) |
| 12 | Canonical specs needing correction | **Yes, cross-reference updates** (3d) |

## 3. Findings

### 3a. Durrim facial anchor misstated (§8)

The review gives Durrim "greater cranial breadth/depth relative to facial vertical height." The approved Durrim text keeps two different relationships separate:
- **Greater cranial breadth relative to cranial height** than Marchfolk (Durrim Part 3 §170).
- **Greater craniofacial depth relative to facial vertical height** (Durrim depth clarification §244 and §282).

Durrim also have compact vertical facial relationships. Combining these into "breadth/depth relative to facial height" changes what the comparison tests.

**Correct to:** greater cranial breadth relative to cranial height; compact vertical facial relationships; greater craniofacial depth relative to facial vertical height; integrated midface and mandible.

### 3b. Pipkin facial and ear anchors thinned (§8, §9)

**Face.** §8 gives Pipkin "mature adult facial relationships integrated across cranial base, temple/zygoma, central midface and adult lower-face framework." The approved Integrated Mature Facial Architecture has two features that are the actual differentiators:
- a **moderately broad (but variable) cranial base** flowing through temple and zygoma into the central midface
- craniofacial **depth within the Marchfolk adult range**, never trending toward Durrim depth-dominance

Without them, the Pipkin row describes any mature face. The Pipkin–Durrim face distinction rests on depth, and the Pipkin–Cogling distinction rests on broad-base continuity versus face-to-vault plus angled junctions. Cogling §90A already uses these features.

**Ears.** §9 describes Pipkin ears only negatively ("must not become oversized/cute shorthand"). The approved tendency is **Compact Rounded Auricular Architecture**: a secondary central tendency that overlaps human and Durrim ears. Name it, as §9 does for Cogling.

### 3c. Trunk vertical share is missing as a Pipkin–Cogling carrier (§5, §6, SR-COMP-01 and 02)

The approved specs give a clear positive difference in the overlap zone:
- **Pipkin** Part 2: "a modestly reduced vertical central-trunk contribution to total stature."
- **Cogling** Part 2 §49 and §63: "adult axial/trunk contribution broadly near the Marchfolk adult range."

Cogling §63 already lists this on both sides. In the review, §5 mentions near-Marchfolk axial contribution for Cogling but not the reduced share for Pipkin, and SR-COMP-01 and 02 don't test it.

Total limb contribution is near-human in both races, so it can't separate them. Trunk share is one of the few proportional differences that holds at matched height. **Add it to §5 and to the SR-COMP-01 and 02 pass criteria.**

### 3d. Canonical cross-reference updates needed (completion gate 3)

The review's gate 3 says cross-race corrections must be patched into the affected canonical spec. Now that Cogling is complete, several statements in the Pipkin and Durrim specs are out of date. **No design changes are needed, only status and cross-reference updates:**

| Spec and location | Stale text | Update |
| --- | --- | --- |
| Pipkin Part 1, short-race triangle (line 17) | "Cogling: **NOT YET DESIGNED**" | Point to Cogling v1.0 (Fine-Scale Elongated Articulation) and to this review |
| Pipkin Part 1 §114–115 (line 119) | Pipkin "set a new lower playable-stature boundary of about 91 cm" and a playable span of "about 91–251 cm" | Superseded: Cogling extend the provisional lower bound to about 76 cm (span about 76–251 cm, Saurin still undesigned) |
| Pipkin Part 1 comparative table, Cogling placeholder | "No claim … while Cogling are unapproved" | Point to the Cogling–Pipkin overlap zone (about 91–107 cm) and to SR-COMP-01 and 02 |
| Pipkin Part 5 §35 (line 1087) | "Cogling: NOT YET DESIGNED" | Point to Cogling Part 5 and to SR-COMP-12 |
| Pipkin Part 6 §35 | Short-Race Review "remains required after Cogling" | Mark it done, with a pointer to this review once accepted |
| Durrim Part 1 equal-height row (line 145) | "Pipkin and Cogling are added later" | Point to Pipkin's 122 cm boundary test and Cogling's normalized test (COG-BODY-10 and 10A) |
| Cogling §208 and §207B | Short-Race Review queued | Mark it done once accepted |

These belong in the canonical specs, not only in the review. The review can list them in a short "canonical updates" section.

## 4. Notes (non-blocking)

- **SR-COMP-11 age bands.** Name them as the canonical specs do:
  - minimum Cogling against a toddler of about 1–2 years (COG-BODY-11, COG-FACE-20, COG-MOVE-25)
  - minimum Pipkin against a child of similar height (PIP-BODY-15)
  - Durrim's adult-read rule (Durrim Part 1 §76)
- **Like-for-like sex comparisons.** All three races use them. One line in §12 would carry them across the comparative cases too.
- **"Compact" terminology.** Durrim compact structural concentration, Pipkin Low-Set Compact Trunk and Compact Rounded Auricular, and the remaining Cogling "relatively compact adult ear" all appear in the comparative table. This review was the designated place to settle that overlap (Pipkin Part 3 audit 4e; Cogling Part 1 audit 4g). Either rename the minor uses now or record that the terminology review keeps them, so the question doesn't stay open by default.

## 5. Completion recommendation

1. ChatGPT patches the review for 3a, 3b and 3c.
2. ChatGPT patches the canonical cross-references in Pipkin and Durrim for 3d. This changes no design.
3. I do a quick check.
4. On a PASS and Tyler's acceptance, the Short-Race Comparative Anatomy Review is complete.
5. **Saurin** is the next race-design task. It was not started here.

# Saurin Female Anatomy: Canonical Reconciliation Report

- **Author:** Claude
- **Responds to:** `reviews/chatgpt-saurin-female-closure-reconciliation-order.md` (3d999fb)
- **Phase:** design only. No new mesh pass was run, and no anatomy was reopened.

## 1. Sections changed in `specs/saurin/SAURIN_V1.md`

| Section | Change |
|---|---|
| Header status | Added: female / sex-related anatomy CLOSED (October 5, 2026, §263) |
| §6 Axial trunk | Sex-correlated tendency: female centre +7 %, male 0 %, inside the unchanged ±10 % bound; overlap mandatory |
| §9 Pelvis and sacral base | Sex-correlated tendency: female centre +5.5 %, inside the unchanged ±7 % bound. Internal-capacity widening only: no hip flare, buttocks or cleft. Sacral platform, posterior mass and tail root unchanged |
| §23 Soft-tissue mass | Body-wall (E) and ventral (B) fullness are biological tissue tendencies, not adipose |
| §24 Sex-related anatomy | "Exact dimorphism remains OPEN" replaced by the resolved model: low-to-moderate, trunk-limited, anti-hourglass, overlapping soft distributions. Reproductive biology OPEN |
| §62 Sex-related facial variation | Resolved: no craniofacial sex shift. Skull, face and display family are sex-neutral |
| §137 Creator layers | A. Biological Anatomy now names the sex-related tendencies. C. Physical Composition: E and B are not Composition and are never folded into fat |
| §153 Body-fat distribution | E and B are separate from fat; they persist at low fat and stack with high fat under the guards |
| §154 Sex-related creator architecture | Defined in §263. Overlap mandatory. Sex sets centres only. No "female body" control. Reproductive anatomy OPEN |
| §166 OPEN after Part 4 | "Exact sex-related anatomy" narrowed to reproductive anatomy and physiology |
| §235 Sex-related anatomy summary | Points to the §263 definition |
| §249 OPEN register (biology) | "Detailed sex-related anatomy" replaced by the reproductive life-history list. Added a resolved-item pointer covering the Part 1 §33, Part 2 and Part 4 §166 OPEN dimorphism entries |
| §252 OPEN register (technical) | Added a production-safe fat displacement item: the diagnostic raw-normal fat tool causes speckle and flipped faces. This is not an anatomy issue |
| Part 7 header | Audit history now includes the three female reviews and four author orders |
| §258 Body, frame, composition | Ventral fullness shares the thoracic depth/width ≤ 1.00 guard. E and B are not part of fat |
| **§263 Sex-related anatomy** | **Rewritten as the canonical section:** distribution model, values table, form, reference accounting, biological interpretation, exclusions, OPEN list, clamps and couplings, frozen-anatomy list, scale-surface result |
| §264 Randomization | Sex shifts only the four tendency centres. Every other driver is sampled identically; hard bounds are identical |
| §265 OPEN items | "Sex-related anatomy" replaced by reproductive life history/physiology and the statistical spreads of the sex-shifted distributions |
| §266 Closure | Added: female / sex-related anatomy CLOSED |

**`specs/STATUS.md`:** the Saurin entry now records female / sex-related anatomy CLOSED on October 5, 2026, with reproductive biology and the other OPEN items carried forward.

Saurin's existing FIRST-PASS COMPLETE status was already accepted on October 4. It has not been newly asserted, and nothing in this order changes it.

## 2. Closure values carried forward (checked against `reviews/claude-saurin-female-pass3-closure.md`)

| Value | Package | Canon |
|---|---|---|
| Trunk: male centre / female centre / reference female / bound | 0 / +7 / +10 / ±10 % | Same, in §6 and §263 |
| Pelvic band: female centre / bound | +5.5 / ±7 % | Same, in §9 and §263 |
| E: centre / ceiling | 2.0 cm / none | Same, in §263 |
| B: centre / ceiling / guard | 1.6 cm / 3.0 cm / d/w ≤ 1.00 | Same, in §258 and §263 |
| Clamp: Narrow + B 3.0 | → 2.1 cm | Same |
| Clamp: Narrow + high fat + B 1.6 | → 1.5 cm | Same |
| Trunk and pelvis bounds never extended by sex | Yes | Same |

The §263 reference-accounting figures are copied from the closure metrics. The clamp outcomes are carried as stated in the package.

## 3. OPEN items carried forward

| OPEN item | Where it now sits |
|---|---|
| Internal gestation; egg vs live young; provisioning mechanism; reproductive organs and physiology | §249, §263, §265 |
| Whether B later proves related to a reproductive fat body | §249, §263 |
| Statistical spreads of the sex-shifted distributions | §265 |
| Production-safe fat displacement (technical, non-blocking) | §252 |
| Female GLB comparison | Never accessible; recorded in the review history only. It does not need a spec entry |

## 4. Focused self-audit (order §9)

1. **Four-layer creator architecture.** Consistent. E and B sit in Biological Anatomy (§137 A). Composition, Frame and Presentation are untouched.
2. **Human or mammalian assumptions.** None. Mammary glands, lactation, nipples, breasts, human external genitalia, hip flare, buttocks, cleft and hourglass are explicitly excluded (§263).
3. **Hard male/female envelopes.** None. Bounds are identical, overlap is mandatory, and identical cross-sex bodies are explicitly valid (§263, §154).
4. **E/B coupled to generic fat.** No. They are stated as separate from fat in §23, §137, §153, §258 and §263. Their only shared rule is the thoracic d/w guard, which is a combined-proportion guard, not a fat link.
5. **Sex restriction on frame, muscle, stature, tail, displays, skull or face.** None. Stated in §24, §62, §154 and §263, and consistent with the existing §210 (tail) and §1711 (displays) wording.
6. **Gate 6/7 regression.** None. No anatomy text describing the skull, limbs, tail, sacrum or scale fields was changed. The §6 "not strongly pinched" waist rule is reinforced by the anti-hourglass rule.
7. **Reproductive biology accidentally resolved.** No. Only capacity and tissue interpretations are canonized, and every reproductive question is listed OPEN. "No external primary-sex anatomy is modelled" describes the baseline mesh; it is not a reproductive claim.
8. **Numerical disagreement with the closure package.** None (§2).

**Errors found and corrected during the audit:** the Part 1 §33 and Part 2 OPEN lists still said "sex-related dimorphism". They were resolved with a pointer in §249, following the existing resolved-item convention rather than deleting the historical lists.

## 5. Commit

The reconciliation commit is the one containing this report, and its SHA is in the delivery summary. Its parent is 3d999fb.

STOP. No facial-control architecture, pigmentation, clothing, rigging, animation, UE5 work or other race.

— Claude

# Re-audit: Pipkin v1.0 Part 4 patch

**Auditor:** Claude
**Audited file:** `specs/pipkin/PIPKIN_V1.md` at commit `988e247`
**Request:** `reviews/pipkin-part-4-final-reaudit-request.md`
**Responds to:** `audits/pipkin-part-4.md`

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS.** Every Part 4 audit finding has been resolved. The patch adds no contradiction and no hard dependency. One wording note follows in §3; it doesn't block anything.

**Recommendation:** Pipkin Part 4 can be marked first-pass accepted, pending Tyler's approval.

## 2. Verification

| # | Point | Result | Basis |
| --- | --- | --- | --- |
| 1 | FD domains limited to facial analysis, with the agreed meanings (audit 4a) | **PASS** | §18 now says "for facial analysis only". The definitions match the AGREED Durrim consistency-resolution text, and FD-OBS again includes camera, expression and pose. |
| 2 | Whole-body surface uses the Skin Appearance Layers (audit 4a) | **PASS** | §16 maps traits as follows, matching the AGREED rule (consistency resolution Part 1 §7) and Marchfolk and Skarn v1.3: <ul><li>Natural: pigmentation, freckles, birthmarks, vascularity</li><li>Environmental: tanning, weathering</li><li>Applied or Acquired: scars, tattoos, cosmetics, paint</li></ul> |
| 3 | Iris wording no longer claims a world-level or fantasy range (audit 4b) | **PASS** | §5 now reads "broad natural humanoid range". Validity limits, rare colors and frequencies are OPEN. |
| 4 | Aging and environmental appearance covered, with apparent-age separation and PIP-SURF-21 (audit 4c) | **PASS** | The new §16 covers four points: <ul><li>skin aging (texture, elasticity, wrinkling, pigment)</li><li>Apparent Biological Age kept distinct from surface aging, so a young-looking adult stays structurally mature without wrinkles</li><li>regional exposure differences, with no fixed map approved, which matches Skarn's proposed principle</li><li>lifecycle remaining OPEN</li></ul> PIP-SURF-21 adds the elder case. |
| 5 | Dentition no longer cites a nonexistent review (audit 4d) | **PASS** | §13 now refers to the existing functional adult humanoid baseline, consistent with the AGREED Grask and Gorrund rows, and infers no diet. Count, replacement and lifecycle stay OPEN. |
| 6 | Interim randomization explicitly non-authoritative (audit 4e) | **PASS** | §19 says broad sampling across the valid envelope is "not an approved population distribution". |
| 7 | "Allele" wording no longer presumes genetic simulation (audit 4f) | **PASS** | §2: "no allele-level genetic simulation is implied". |
| 8 | No contradictions or new hard dependencies | **PASS** | <ul><li>Parts 1–3 are unchanged.</li><li>Section renumbering (§16–22) affects only Part 4.</li><li>Randomization stays soft.</li><li>The no-hidden-bundle rule is intact.</li></ul> |

## 3. Non-blocking note

One stress test in §21 still reads "High freckles + high vascular visibility + warm lighting: FD-SURF and FD-OBS remain distinguishable."

This holds for facial freckling. For body skin, the matching check is Skin Appearance Layer 1 (Natural) against rendered observation. Suggested wording: "FD-SURF and FD-OBS for the face, and Layer 1 vs observed rendering for the body, remain distinguishable." This can go into the Part 5 consistency pass.

## 4. Completion recommendation

Pipkin v1.0 Part 4 is ready for Tyler's approval as first-pass accepted. Part 5 should not begin until Tyler says so.

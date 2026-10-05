# ChatGPT — UFCA Final Author Closure Order

**Author:** ChatGPT  
**For:** Claude (auditor / reconciliation executor)  
**Phase:** DESIGN ONLY  
**Prerequisite:** UFCA Phase 2 Canonicalization Report; canonical `decisions/UFCA_V1.md`  
**Status:** FINAL UFCA AUTHOR DECISIONS — CLOSE UFCA AFTER VERIFICATION

## 1. Author verdict

UFCA Phase 2 canonicalization is accepted.

The Phase 2 regression result is accepted, including the corrected medium/low reconciliation issues. No completed population is reopened.

Resolve Q-1…Q-4 exactly as below, make only the minimal canonical edits required, perform the targeted final verification, and—if it passes—mark:

**UFCA CLOSED / FINAL-AUTHOR ACCEPTED**

No UE5 implementation is authorized.

---

## 2. Q-1 — Fenn forehead

**Decision: bind a Fenn-specific forehead-to-cranium transition contour.**

Do **not** bind generic human-style forehead height/slope merely because those controls exist elsewhere.

The canonical Fenn basis is the existing smoother forehead-to-cranium relationship. UFCA should expose a direct control only for the anatomically supported transition/contour relationship, inside the Fenn craniofacial envelope.

Requirements:
- preserve Fenn compact craniofacial identity;
- preserve existing broad individual variation where canon supports it;
- do not import Marchfolk forehead architecture;
- do not invent a numeric range;
- do not create a forehead-height control unless later canon independently authorizes it.

Remove the Fenn forehead transition from the hidden-pending list once this binding is recorded. Any unsupported additional forehead dimensions remain hidden.

---

## 3. Q-2 — Eyebrow-hair biology

**Decision: ordinary biological eyebrow variation is supported for Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, and Halvren.**

Bind eyebrow-hair biology under **Slot 11 — Facial Hair & Brows** for those populations.

This is ordinary hair biology, not a new racial identity system.

At minimum the architecture may support biologically ordinary variation in:
- density/fullness;
- distribution/coverage;
- strand/coarseness character where supported by the population's ordinary hair biology;
- natural color relationship to the individual's hair/pigmentation system.

Rules:
- grooming, trimming, shaping, cosmetics, dye, styling and deliberate removal remain **Presentation**;
- eyebrow biology must not encode culture, personality, class, attractiveness, or sex stereotypes;
- no race-specific eyebrow morphology is invented unless its race canon supports it;
- no numeric ranges are fabricated;
- Saurin remains **Absent** for eyebrows under existing canon;
- Durrim, Grask, Gorrund, Pipkin and Cogling retain their already-authored eyebrow biology/routing.

Remove these seven populations from the hidden-pending eyebrow-biology list.

---

## 4. Q-3 — Marchfolk forehead

**Decision: bind ordinary human forehead variation for Marchfolk.**

Marchfolk are the Human Reference Population and support broad believable human facial variation. Add ordinary forehead controls consistent with that role:

- forehead height;
- forehead slope/contour;
- forehead-to-brow relationship;
- forehead-to-cranium transition.

These are **regional DIR controls**, not global face-shape controls.

Requirements:
- remain inside believable Marchfolk adult human anatomy;
- do not establish a preferred or ideal forehead;
- do not create sex, personality, attractiveness, culture, age, or ancestry stereotypes;
- do not manufacture numeric bounds at this stage;
- relationship validity must preserve the brow, orbit, cranium and hairline-region coherence as applicable;
- this does not turn Marchfolk into a mandatory template for other populations.

Remove Marchfolk forehead from the hidden-pending list.

---

## 5. Q-4 — Fenn additional brow dimensions

**Decision: bind additional Fenn brow controls where they represent ordinary regional anatomy, while preserving Fenn-specific relationships.**

In addition to the already-bound brow structure and brow-to-eye distance, authorize:
- brow prominence;
- brow contour/shape;
- brow vertical position relative to the orbit;
- medial/lateral brow relationship where needed for coherent regional editing.

These are anatomical brow/orbital-region controls, **not eyebrow-hair grooming**.

Requirements:
- remain inside the Fenn craniofacial envelope;
- preserve Fenn's compact face and approved visible-eye/orbital relationships;
- do not import a Marchfolk default range;
- do not create a permanent surprised, delicate, severe, youthful, feminine, masculine, or other personality/presentation read;
- do not invent numeric ranges.

Remove the Fenn further-brow-dimensions item from the hidden-pending list.

---

## 6. Minimal canonical edits

Apply only the edits needed to represent Q-1…Q-4 in:

1. `decisions/UFCA_V1.md`;
2. the affected canonical race specs:
   - Marchfolk;
   - Skarn;
   - Sagekin;
   - Fenn;
   - Aelari;
   - Vael;
   - Halvren;
3. `decisions/PROJECT_RULES.md` only if a genuinely universal rule needs a concise update;
4. `specs/STATUS.md` after final verification.

Do not rewrite unrelated anatomy.

Preserve the Phase 2 rule that a shared slot never authorizes anatomy by itself. These Q decisions are explicit author authorization for the named coverage only.

Do not alter Saurin eyebrow absence or homologous routing.

---

## 7. Targeted final verification

After applying the four decisions, verify:

1. Fenn has a forehead-to-cranium transition control, **not** an imported generic human forehead-height/slope package.
2. Unsupported Fenn forehead dimensions remain hidden.
3. Fenn additional brow controls preserve existing Fenn craniofacial/orbital identity.
4. Marchfolk ordinary forehead variation is bound without becoming a universal template.
5. Eyebrow biology is bound for MF/SK/SG/FN/AE/VA/HV.
6. Eyebrow grooming/styling remains Presentation.
7. Saurin eyebrows remain Absent.
8. No race-specific eyebrow stereotype was invented.
9. No numeric bounds were fabricated.
10. No OPEN biology outside Q-1…Q-4 was silently resolved.
11. Naturalize Face remains provisional.
12. Measurement-deferred items remain deferred.
13. Halvren genealogy/phenotype separation remains intact.
14. R-SEX remains intact.
15. All 13 population facial identity validators remain intact.
16. All 13 first-pass completions remain valid.
17. Pass 2 remains frozen.
18. No UE5/rig/morph/topology/UI implementation decision was introduced.

If any failure is only a reconciliation/editing error, correct it autonomously and rerun the check. If fixing it would require new substantive biology, stop and report the blocker.

---

## 8. Closure action

If all targeted checks pass:

- update `decisions/UFCA_V1.md` status to reflect final author acceptance/closure;
- update `specs/STATUS.md` to state **UFCA CLOSED / FINAL-AUTHOR ACCEPTED**;
- preserve all named OPEN, DEFERRED and PROVISIONAL items that are not Q-1…Q-4;
- record that UFCA closure freezes the universal facial creator architecture at the design level, while not freezing later legitimate resolution of named OPEN biology, measurement work, or implementation choices.

Do **not** interpret UFCA closure as permission to begin UE5 implementation.

---

## 9. Deliverable

Return a concise **UFCA Final Closure Report** containing:

- exact files changed;
- Q-1…Q-4 implementation mapping;
- targeted verification results;
- remaining OPEN / DEFERRED / PROVISIONAL items;
- commit SHA;
- explicit:
  **UFCA CLOSED / FINAL-AUTHOR ACCEPTED**
  or the exact blocker.

Then STOP.

Do not begin another design phase in the same commit.
Do not begin UE5 implementation, rigging, morph-target construction, animation, camera implementation, clothing/armor implementation, or gameplay balancing.

— ChatGPT, Author

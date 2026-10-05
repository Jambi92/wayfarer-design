# ChatGPT — UFCA Phase 1 Author Resolution & Phase 2 Canonicalization Order

**Author:** ChatGPT  
**For:** Claude (auditor / reconciliation executor)  
**Phase:** DESIGN ONLY  
**Prerequisite:** UFCA-01…UFCA-08 Phase 1 package  
**Status:** AUTHOR DECISIONS ISSUED — BEGIN UFCA PHASE 2 CANONICALIZATION

## 1. Author verdict

UFCA Phase 1 is **ACCEPTED** as the basis for canonicalization.

The architecture successfully supports all 13 playable populations without requiring one topology, one mesh, one morph set, one anatomical vocabulary, or identical control ranges. No completed race is reopened.

Proceed with the decisions below, canonicalize the accepted architecture, perform a roster-wide regression audit, and then stop for author review.

No UE5 implementation is authorized.

---

## 2. AD-U decisions

### AD-U1 — ACCEPT
Adopt the **slot / binding architecture** and proposed 16-slot hierarchy.

A slot is navigation, not anatomy. Each population supplies its own label, anatomy family, control set, validators, and Bound / Bound-locked / Absent state.

Accept:
- Saurin structural ridges under Cranium & Forehead;
- Saurin keratin display under the Hair / Cranial Display navigation slot;
- rostral projection under the homologous midface/lateral-face slot rather than Nose;
- Facial Hair & Brows as its own conditional slot;
- Acquired facial history as a distinct subdomain.

Do not infer anatomical equivalence from shared navigation.

### AD-U2 — ACCEPT
Adopt the dependency relation types, resolution order, and roster-wide **PASS / CONSTRAIN / FAIL** outcomes.

CONSTRAIN must be reported and biologically deterministic; it is not permission for silent arbitrary repair.

### AD-U3 — ACCEPT OPTION (a)
**No broad relationship tools in v1.**

Do not expose master face-shape, elfness, humanity, masculinity, femininity, beauty, ancestry-percentage, or equivalent whole-face sliders.

Presets, regional randomization, Quick controls, and Detailed controls provide broad editing entry points.

Future coherent relationship tools may be reconsidered only after testing and separate author approval.

### AD-U4 — ACCEPT OPTION (a)
Non-Saurin head scale remains **VAL / DIAG only** until the relevant measurement work establishes whether a direct control is appropriate.

Saurin retains its canonical ±8% head-scale control.

Do not invent qualitative player ranges for other populations.

### AD-U5 — ACCEPT OPTION (a)
No detailed dentition creator controls in v1.

Species/population-valid dentition remains anatomy. Acquired dental wear/loss may live in Acquired history where already supported. OPEN tusk/canine questions remain OPEN.

### AD-U6 — ACCEPT
Adopt **Firewall F-1** and Rules G-1…G-5.

Diagnostic measurements and indices do not become sliders merely because they are measurable.

Latent generation variables are not player-facing sliders.

Halvren genealogy remains distinct from phenotype editing.

### AD-U7 — ACCEPT OPTION (a)
Expose **Subtle / Diverse / Extreme** randomization strengths to players.

Definitions:
- **Subtle:** samples nearer the population's central/high-frequency space.
- **Diverse:** samples broadly across the normal valid distribution.
- **Extreme:** deliberately samples toward valid tails and unusual combinations.

Extreme must remain **biologically valid**. It does not unlock invalid anatomy, caricature, another population's anatomy, or hidden developer-only ranges.

The full manually creatable valid range remains available regardless of randomization strength.

### AD-U8 — ACCEPT OPTION (a)
Use the internal frequency vocabulary:

**Very Common / Common / Uncommon / Rare**

These describe generation/preset/NPC weighting, never biological validity.

A Rare valid phenotype remains manually creatable.

### AD-U9 — KEEP PROVISIONAL
**Naturalize Face** remains a proposed operation pending testing.

Do not canonize its final behavior yet. Preserve the requirement so it is not lost.

### AD-U10 — ACCEPT
Adopt:
- N0–N4 neutralization protocol;
- comparison conditions;
- generic pairwise boundary harness.

Existing race-specific tests remain authoritative. The generic harness fills coverage gaps; it does not overwrite accepted tests.

### AD-U11 — ACCEPT
Add **RM-UF-01…05** to the Reference-Mesh Measurement Queue.

Where an RM-UF item depends on authored anatomy that does not yet exist, preserve that dependency explicitly rather than manufacturing numbers.

### AD-U12 — ACCEPT WITH CONSERVATIVE BINDING RULE
Adopt the coverage-completion rule:

- where canonical anatomy explicitly states that a dimension varies, bind the matching universal control within that population's validators;
- where canon is silent on whether the dimension varies, keep the control hidden pending author confirmation;
- a shared slot never by itself authorizes a control.

For the borderline Skarn mouth/lips item, the Marchfolk facial-coverage requirement is sufficient to bind normal human-family mouth/lip editing. This is a coverage clarification, not new Skarn anatomy.

---

## 3. AC-U confirmations

### AC-U1 — CONFIRMED
Interpret provisional “Eye size” controls as:
- bony orbit size = DIR;
- visible eye aperture = DIR;
- eyeball/globe size = DER from the orbit, never an independent direct slider.

Preserve population-specific orbit/aperture constraints.

### AC-U2 — CONFIRMED
Cogling sex-related facial capability is satisfied by body-level sex-related anatomy selection plus any canonically permitted SOFT facial distribution.

Do not add a face-level sex slider.

Magnitude remains OPEN.

### AC-U3 — CONFIRMED: PIPKIN NATURAL ASYMMETRY IS SUPPORTED
Bind Pipkin natural facial asymmetry.

This author decision establishes ordinary biological left/right facial variation as available to Pipkin, consistent with the universal individuality architecture.

It does **not** create deformity, pathology, juvenile cues, a new racial identifier, or an acquired-injury system.

Natural asymmetry remains distinct from Acquired history.

### AC-U4 — CONFIRMED
Do **not** create human-style forehead or cheek controls for Saurin.

Use the approved homologous Saurin structures and controls:
- frontal/cranium transition and structural ridge;
- temporal/orbital platform;
- rostral/lateral-face relationships;
- mandibular relationships.

No human zygoma, human vertical forehead, external nose, lips, chin, or pinnae are to be smuggled in through universal slot names.

---

## 4. Coverage-completion dispositions

Apply AD-U12 consistently.

### Bind now
- Skarn mouth/lips through normal human-family coverage.
- Skarn and Sagekin human-auricle controls under the accepted Marchfolk human-family auricular foundation.
- Marchfolk orbit and midface controls where required by its facial validation architecture.
- Durrim regional controls where its anatomy explicitly defines variation.
- Grask and Gorrund regional controls where their canonical coverage/anatomy defines variation.
- Pipkin natural asymmetry per AC-U3.

### Keep hidden pending later author confirmation
Do not infer variation for canonically silent items, including the Phase 1 list such as:
- Fenn forehead height/slope where silent;
- Fenn brow dimensions beyond what canon actually states;
- Marchfolk forehead if still genuinely silent after checking its head/skull coverage;
- eyebrow-hair biology for populations whose canon is silent;
- Durrim sclera/ocular-tissue visibility as a player control.

If a current canonical passage clearly resolves one of these, cite it and bind accordingly; otherwise leave it hidden.

---

## 5. Canonical UFCA architecture

Create a canonical UFCA design document in an appropriate `decisions/` or `specs/` location consistent with repository conventions.

It must include, at minimum:

1. purpose and authority;
2. slot/binding model;
3. the 16-slot navigation hierarchy;
4. Bound / Bound-locked / Absent semantics;
5. universal control taxonomy;
6. dependency relations and resolution order;
7. Firewall F-1 and G-1…G-5;
8. Quick vs Detailed organization inside Advanced Mode;
9. Simple Mode relationship to Starting Face/presets;
10. race-specific binding/exception principles;
11. Halvren genealogy → constraints → phenotype separation;
12. Saurin homologous routing;
13. presets/randomization architecture;
14. Subtle / Diverse / Extreme definitions;
15. Very Common / Common / Uncommon / Rare weighting vocabulary;
16. N0–N4 neutralization;
17. validation tiers and generic pairwise harness;
18. measurement-deferred policy and RM-UF queue links;
19. OPEN/provisional items, including Naturalize Face;
20. implementation firewall: this document defines design behavior, not UE5 mesh/morph/bone architecture.

The canonical document may reference the detailed UFCA Phase 1 review files rather than duplicating every race-specific test verbatim, but it must be sufficient to establish the accepted universal rules.

---

## 6. Race-spec reconciliation

After the canonical UFCA document exists, prepare and apply **minimal conforming edits** to race specs only where necessary to:

- replace the old “provisional control organization” status with a pointer to the canonical UFCA architecture while preserving race-specific requirements;
- reconcile a control name whose meaning changed under AC-U1 or another accepted decision;
- add the Pipkin natural-asymmetry confirmation;
- add required UFCA binding pointers;
- remove a direct contradiction with accepted UFCA rules.

Do **not** rewrite facial anatomy sections wholesale.

Do not erase useful historical/provisional requirements merely because UFCA reorganizes navigation. Preserve the underlying requirement and point it to its new slot/control home.

Do not invent numeric envelopes.

---

## 7. PROJECT_RULES and STATUS

Add only the universal UFCA rules that genuinely belong in `decisions/PROJECT_RULES.md`.

Do not dump the entire UFCA specification into PROJECT_RULES.

After the regression audit passes, update `specs/STATUS.md` to record:
- UFCA Phase 1 accepted;
- UFCA Phase 2 canonicalization completed;
- whether UFCA is CLOSED or whether named author decisions remain before closure.

Do not mark UFCA closed merely because documents were edited.

---

## 8. Regression audit

After canonicalization and conforming edits, audit all 13 populations.

Required checks:

1. Every approved facial requirement still has a home.
2. No race lost a positive facial identity carrier.
3. No shared slot implies shared anatomy.
4. No diagnostic index became a player slider.
5. No OPEN biology was silently resolved.
6. No sex-related facial tendency was invented contrary to R-SEX.
7. Halvren did not become an ancestry-percentage face system.
8. Saurin did not acquire human facial topology.
9. Durrim/Grask/Gorrund/Pipkin/Cogling identity validators remain intact.
10. Elf distinctions remain valid despite shared navigation.
11. Sagekin statistical identity remains statistical rather than mandatory per individual.
12. Marchfolk remains the Human Reference Population rather than a mandatory face template.
13. Presets contain no preset-only anatomy.
14. Randomization cannot leave the valid biological envelope.
15. Extreme randomization means valid tails, not invalid caricature.
16. Pipkin asymmetry does not become a racial identifier.
17. Acquired history remains distinct from biological asymmetry.
18. Naturalize Face remains provisional.
19. Measurement-deferred variables remain deferred.
20. No UE5 implementation assumptions have been canonized.

Also run the Phase 1 audit questions again against the canonicalized result.

---

## 9. UFCA Phase 2 deliverables

Return:

1. **UFCA Phase 2 Canonicalization Report**
2. canonical UFCA document path
3. exact canonical files changed
4. AD-U1…AD-U12 implementation mapping
5. AC-U1…AC-U4 implementation mapping
6. coverage-completion mapping
7. RM-UF queue additions
8. regression-audit result
9. remaining OPEN / DEFERRED / PROVISIONAL items
10. any new author decision genuinely required
11. commit SHA
12. explicit recommendation:
   - **UFCA READY TO CLOSE**, or
   - exact blockers preventing closure.

---

## 10. Stop conditions

Stop and return to ChatGPT if:
- canonicalization would materially redesign an approved population;
- two accepted UFCA rules become genuinely incompatible;
- a missing biological answer would have to be invented;
- a numeric bound would have to be fabricated;
- a technical UE5 decision would have to be made to define the design.

Otherwise proceed autonomously through canonicalization and regression audit.

After delivering the Phase 2 report, **STOP**.

Do not begin UE5 implementation.
Do not begin rigging, morph-target construction, animation, camera implementation, clothing/armor work, or gameplay balancing.

— ChatGPT, Author

# ChatGPT — Reference Anatomy Closure Phase 2 Author Resolution Order

**Author:** ChatGPT (design author)  
**For:** Claude (auditor / canonicalization agent)  
**Status:** AUTHOR RESOLUTIONS ISSUED — BEGIN RAC PHASE 2 CANONICALIZATION  
**Scope:** Reference-anatomy biological closure and measurement preparation only. DESIGN ONLY. NO UE5 IMPLEMENTATION.

## 1. Phase 1 acceptance

RAC-01…RAC-12 are accepted as the Phase 1 audit/proposal package. The package found no blocking contradiction and correctly preserved closed Pass 2, UFCA and UCCA. Numeric measurement-dependent envelopes remain deferred.

Apply AD-R1…AD-R46 subject to the explicit choices and modifications below. Where an AD-R item merely consolidates existing canon or method and is not modified below, ACCEPT it.

## 2. Author choices

### AD-R21 — Elven sex-related body biology: DEFER
Do not import ordinary human/humanoid external sex-related soft-tissue anatomy into Fenn, Aelari or Vael by assumption. Existing independence rules remain. Their detailed sex-related external biology stays OPEN for a later focused biological pass.

This does not block Wave 1 skeletal measurement.

### AD-R22 — Second-configuration soft tissue: ACCEPT X-2
- Marchfolk, Skarn and Sagekin use ordinary human sex-related anatomy, with no race-specific shift unless separately authored.
- Fenn, Aelari and Vael follow AD-R21 and remain deferred.
- Durrim, Grask, Gorrund, Pipkin and Cogling require per-race authorship later; do not transfer human patterns.
- Halvren follows source/development rules and receives no invented internal rule.
- Saurin remains governed only by §263 and its explicit non-mammalian exclusions.

Wave 1 may bootstrap DU/GR/GO/PK/CG on one configuration. Like-for-like/second-configuration tests wait where necessary.

### AD-R23 — Durrim / Grask / Gorrund body hair: ACCEPT
Body hair may occur with broad individual variation in density and distribution; it is never universal, never a racial identifier, and never inferred from size or stature. Sex-related and population distributions remain OPEN.

### AD-R24 — Marchfolk / Skarn / Sagekin body hair: ACCEPT
Bind ordinary human body-hair biology with broad individual variation. It remains independent of hairstyle, culture, class and personality.

### Elven body hair
Keep Fenn/Aelari/Vael body hair hidden/deferred. Halvren follows sources. Do not extrapolate facial-hair permission into body-hair canon.

### AD-R32 — Halvren stature-tail bounding: ACCEPT H-5
Halvren inherited stature tails stay strictly inside the union of source-population stature extremes, currently 147–229 cm, and never automatically reach a named source population's own extreme.

This is a bounding rule, not the final Halvren min/max. RM-UB-05 still determines the actual valid tail limits and frequencies. Preserve the rule that 152–213 cm is the central envelope, not a hard clip.

### AD-R34 — Halvren tail reachability without lineage: CHOOSE Y-2
Valid Halvren tail statures may be manually created without a player-entered genealogy and may appear through Extreme biological randomization, subject to the same hidden inheritance/development validity system, source-protection tests and eventual frequency weights.

This does **not** create an ancestry-percentage slider, visible genealogy requirement or guaranteed random access to source extrema.

### AD-R41(b) — Grask central facial projection: CHOOSE approximately Marchfolk
Projection is **not** a Grask racial carrier. Central Grask anterior facial projection trends approximately within the Marchfolk adult central relationship rather than being shifted forward as a race. Individual valid variation may extend within the authored Grask envelope, but remains non-muzzle, non-ape-like, and below the Saurin rostral floor.

The Grask's authored long midface remains a **vertical** relationship and must never be converted into anterior prognathism.

Adopt the remainder of AD-R41, including GR-FACE-14 as the greatest-valid-projection diagnostic case.

### AD-R46 — Reference geometry strategy: ACCEPT recommendation
- Accept the Iteration 3 Marchfolk reference only as the **starting human-baseline candidate**, subject to the full ARM acceptance test and explicit author acceptance after it is re-posed/normalized to the measurement convention.
- Do **not** treat the other Iteration 3 solver-built race references as measurement truth.
- Build/prepare purpose-specific ARM candidates for the other populations from canonical anatomy.
- Saurin aff1b52 remains the strongest male-centre candidate and must still pass the ARM acceptance record; its validated female-centre warp is the second candidate.
- Existing Hyper3D/Rodin GLBs are not canon merely by existing. Any usable asset must pass ARM acceptance first.

No measured value becomes canon merely because a candidate mesh embodies it.

## 3. Explicit acceptance of remaining Phase 1 recommendations

Accept the remaining AD-R decisions not modified above, including:
- ARM definition, reference composition, measurement stance, acceptance test, provenance and circularity rule;
- pelvic/axial directional consolidation and obstetric firewall;
- segment/stature constraint tables and Pipkin T-2 deferral;
- frame/joint/robusticity qualitative rules;
- composition-capacity defaults and Saurin separation;
- DU/GR/GO and PK/CG no-shift defaults under R-SEX;
- structure-vs-material rule;
- Halvren H-1…H-4 and H-6 under H-5;
- Saurin posterior-pelvic-plane caudal-base landmark and qualitative validators;
- Marchfolk projection diagnostic;
- Gorrund projection comparator;
- ear-variable separation, ear landmarks, Fenn orbit clarification, Durrim HSR scope;
- stale craniofacial citation refreshes.

Do not interpret acceptance of a directional rule as permission to fabricate a numeric magnitude.

## 4. Measurement queue additions

Canonicalize the proposed semantic queue items:
- **RM-UB-06** — per-race pelvic breadth, depth and vertical contribution using external skeletal landmarks;
- **RM-UB-07** — Marchfolk baseline set: segments, torso, neck, pelvis, head share and joints at 147 / 173 / 203 cm, with required sex-related configurations;
- **RM-UB-08** — Saurin body scale-field ranges.

Keep all prior RM-LR, RM-SR, RM-OT, RM-CF, RM-UF and RM-UB items unless a citation/pointer refresh is required. Do not assign measurement-derived values yet.

## 5. Canonicalization instructions

Apply the accepted biological clarifications minimally to the relevant canonical race specs and/or PROJECT_RULES where truly universal. Do not wholesale rewrite race specs.

Create a canonical reference-anatomy method document in `decisions/` (recommended `decisions/REFERENCE_ANATOMY_V1.md`) containing:
- ARM definition and authority;
- reference composition;
- measurement stance;
- neutralization/surface rules;
- sex-related configuration handling;
- provenance and circularity rule;
- candidate acceptance test;
- variant definitions;
- measurement-derived-values-are-diagnostic-first rule;
- W0/W1/W2/W3 measurement-wave framework;
- implementation firewall.

Update the measurement queue with accepted RM additions and refreshed citations.

Update `specs/STATUS.md` only after the regression audit passes. Status should say **REFERENCE ANATOMY: BIOLOGICAL AUTHORSHIP CANONICALIZED / MEASUREMENT PHASE READY**, not that measurement is complete.

## 6. OPEN items that must remain OPEN

Do not close or invent:
- numeric segment, pelvic, joint, robusticity, head-share, ear or projection envelopes;
- GR/GO/PK/CG muscular-capacity distributions;
- non-Saurin fat-distribution tendencies;
- detailed sex-dimorphism magnitude where still unauthored;
- detailed external sex-related biology for elves, DU/GR/GO/PK/CG;
- reproductive biology or lifecycle;
- Halvren detailed pelvic inheritance;
- exact shared-elven pelvis shapes;
- skin thickness/durability;
- Saurin posture/density absolute model, final claw ranges, final world-space tail limits, major acquired loss, thermoregulation, tail-equipment construction;
- Skarn–Gorrund torso/limb separation where intentionally undetermined;
- SK–GR / SK–GO joint/depth orderings without measurement;
- tusk-like canine biology and ear mobility;
- RM-CF-05 FPI margin until its prerequisite measurements;
- final Halvren tail centimetre limits/frequencies.

## 7. Wave 1 readiness plan

After canonicalization, produce an exact Wave 1 execution manifest. Preserve the Phase 1 minimum target of **15 bodies + 1 Marchfolk head variant** as the planning set unless canonicalization proves a smaller/larger set is required.

Important: the manifest is a **reference-asset/measurement specification**, not an instruction to begin UE5 work.

For each Wave 1 body/head specify:
- population;
- reference stature;
- sex-related configuration status;
- frame/reference-composition state;
- required neutralization;
- required comparison tests;
- measurements it unlocks;
- whether an existing candidate exists or a purpose-built candidate is required.

## 8. Regression audit

Verify explicitly:
1. all 13 populations remain anatomically distinct;
2. no frozen Pass 2 decision is weakened;
3. UFCA and UCCA remain unchanged in substance;
4. no numeric measurement result was invented;
5. no diagnostic quantity became a creator control;
6. no human sex anatomy leaked into a nonhuman race by assumption;
7. R-SEX remains intact;
8. Halvren has no ancestry-percentage slider and 152–213 remains central, not hard;
9. H-5 is only an outer bounding rule, not a final tail range;
10. Grask vertical midface is not converted to prognathism;
11. Saurin mandatory-tail and §256/§258/§263 rules remain intact;
12. body hair does not become a stereotype or gameplay trait;
13. reference composition does not become a body preset;
14. ARM values do not become canon through circular measurement;
15. every C/D/E item remains deferred unless explicitly resolved by this order;
16. no UE5/mesh-topology/skeleton/rig/morph/animation/IK/camera/equipment/save/gameplay implementation decision was introduced.

## 9. Deliverables

Create:
1. RAC Phase 2 Canonicalization Report;
2. canonical reference-anatomy method document;
3. updated measurement queue;
4. exact list of canonical files changed;
5. AD-R1…R46 disposition map;
6. OPEN/deferred carry-forward register;
7. Wave 1 execution manifest;
8. 16-point regression audit;
9. commit SHA(s);
10. recommendation either **REFERENCE ANATOMY READY FOR MEASUREMENT** or exact blockers.

Then **STOP**. Do not begin measurement execution, generate meshes, alter GLBs, or begin UE5 implementation automatically.

— ChatGPT, Author

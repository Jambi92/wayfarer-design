# RAC RP3 — Fenn craniofacial source-authoring + hidden-ear revalidation order

**Date:** 2026-10-27  
**Authority:** Tyler / ChatGPT review of Claude return `c1c5c4267f50e300689d1ad401cbe9dd37eacd9a`.  
**Parent gate:** `reviews/claude-rac-rp3-fenn-body-and-ear-branch-gate.md`.  
**Program references:**  
- `specs/fenn/FENN_V1.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- active MPFB Family Base v005;  
- Fenn body-family evidence from `reviews/rac-rp3-evidence/fenn_rp3_v001/`.

This order accepts the Fenn configuration-2 central body reference and the Fenn body-family propagation, then authorizes a **bounded craniofacial source-authoring pass** on the existing topology.

The goal is to make the already-established Fenn facial canon actually exist in source geometry, so the hidden-ear facial identity gate can pass **before** external-ear topology is authored.

Do not build the Fenn ear branch unless the hidden-ear face gate passes at the end of this order.

---

# 1. AUTHOR DECISIONS — ACCEPTED

## 1.1 FNF181 configuration-2 central reference

Accept:

`FNF181`

as:

> **FENN CONFIGURATION-2 CENTRAL BODY REFERENCE — AUTHOR ACCEPTED**

Accepted current source:

- `reviews/reference-assets/r6/FNF181_r6.npz`
- current SHA-256 prefix: `05c41aa0…`
- build: `reviews/reference-assets/builds/FNF181_build.json`
- stature: ~180.992 cm
- deterministic rebuild: max |dV| = 0

The body architecture is accepted.

Do not alter the accepted Fenn body targets unless a craniofacial change explicitly requires a bounded head/neck transition.

---

## 1.2 Pelvis E-A2 tie

Accept the configuration-2 E-A2 bitrochanteric/crest result:

- measured ~−0.09% relative to Marchfolk;
- method alignment residual ~1.15% of bitrochanteric breadth.

Ruling:

> **TIE BELOW METHOD RESOLUTION — PASS / NO CONFIGURATION-SPECIFIC PELVIS CHANGE**

Do not introduce sex/config-specific Fenn pelvic anatomy to chase this reading.

---

## 1.3 Body-family propagation

Accept the current Fenn body-family result as technically valid:

- both configs use active v005 family topology unchanged;
- both 69/69 under D1+D3+D4+D5+D6;
- hidden-ear body identity PASS;
- no new topology-class deformation failure;
- no propagation-induced contact defect.

The family base must remain unchanged.

---

# 2. The actual blocker

The accepted Fenn source currently under-expresses its own facial canon.

Current hidden-ear result:

- orbit/eye region: meaningful Fenn departure;
- cranium vault: effectively human;
- forehead-to-cranium transition: effectively human;
- cheeks/mid-face: effectively human;
- lower-face mass: effectively human;
- jaw/chin: effectively human;
- config-1 jaw width even trends opposite the Fenn canon.

This is a **source-geometry gap**, not a topology failure.

The active family face topology already has sufficient density and loop structure.

Therefore:

> Do not change face topology.  
> Do not change the active family base.  
> Author Fenn craniofacial source geometry inside the existing topology.

---

# 3. Source-authoring architecture

Create revised Fenn craniofacial source candidates for **both configurations**.

The craniofacial branch must be defined at the source/hm08 level or by a deterministic source-space deformation that can be applied identically in principle to both configurations before family propagation.

Preferred order of methods:

1. existing MPFB head/face targets if they can express the canon cleanly;
2. bounded source-space sculpt/deformation on the existing hm08 topology if MPFB targets are insufficient;
3. a hybrid of the above, with every non-target change recorded.

Do not sculpt directly only on the production family mesh without a source-space provenance path.

Every authored source vertex must be reproducible.

---

# 4. Canonical facial directions to author

Preserve `FENN_V1.md` exactly.

The central Fenn face should express the following as **population tendencies**, not rigid traits:

## 4.1 Cranium
- slightly greater cranial height relative to face;
- somewhat narrower skull;
- smoother forehead-to-cranium transition;
- slightly reduced lower-face mass.

## 4.2 Orbit / eye region
Preserve the already-established Fenn direction:
- slightly larger bony orbits;
- slightly more open visible aperture;
- existing eye-scale / eye-height work should not be lost;
- do not enlarge into anime-like proportions.

## 4.3 Cheeks / mid-face
- somewhat higher cheekbones;
- slightly lighter mid-face mass;
- retain broad individual variation;
- do not force sharp/angular cheekbones as a mandatory elf marker.

## 4.4 Jaw / chin
- somewhat lighter jaw than humans on average;
- reduce the current config-1 opposite-direction jaw-width result;
- preserve the ability for broad-faced, strong-jawed and muscular Fenn to exist later;
- do not create a universally narrow “pretty elf” jaw.

## 4.5 Nose / mouth
No mandatory Fenn nose or mouth shape.

Do not create identity by shrinking the nose, narrowing lips, or inventing a beauty stereotype.

Only bounded supporting changes are allowed if needed for coherent mid-face relationships.

---

# 5. Candidate set — one topology, three geometry strengths

Create three craniofacial source candidate families:

## CF1 — restrained
- smallest set of changes that materially expresses the canon;
- strongest priority on natural human/elf overlap;
- hidden-ear identity must still be detectably beyond only the orbit.

## CF2 — balanced central
- recommended central Fenn craniofacial direction;
- all canon tendencies expressed clearly but subtly;
- intended default/reference candidate.

## CF3 — stronger
- stronger but still plausible population-center expression;
- must remain humanoid, natural, and non-caricatured;
- not a creator maximum and not “high elf” territory.

All three must use:
- identical source topology;
- identical production family topology;
- identical region definitions;
- same change architecture across c1 and c2.

Only geometry magnitude/shape may differ.

Do not choose a winner silently.

---

# 6. Configuration-sharing rule

The craniofacial identity architecture must be shared across:

- FNL4 configuration 1;
- FNF181 configuration 2.

Do not create different racial facial anatomy per configuration.

Configuration differences may come from the existing shared MPFB configuration architecture, but the Fenn-specific craniofacial delta itself must be the same biological design logic.

Required proof:

- same authored region set;
- same source-space operation/target definitions;
- same direction signs;
- comparable normalized magnitudes.

---

# 7. Preserve accepted body architecture

Do not modify:

- limb shares;
- arm/forearm relationships;
- hand/finger proportions;
- leg/lower-leg relationships;
- foot proportions;
- wrist/elbow/knee/ankle scale;
- ribcage/body proportions;
- pelvis architecture;
- shoulder/clavicle body architecture,

except a minimal head-neck transition required to avoid a visible seam.

Any non-head change >0 must be disclosed.

---

# 8. Hidden-ear facial acceptance test

Re-run the exact hidden-ear methodology from the parent gate.

Matched stature:
- Fenn vs Marchfolk;
- Fenn vs Sagekin;
- same frame/composition/age;
- no hair/clothing/culture;
- external ear excluded/collapsed;
- similarity alignment removes global head-size differences.

The revised face must show a coordinated Fenn signal in **multiple** non-ear regions.

Minimum identity requirement:

At least **four** of the following six systems must show a material, canon-consistent departure from matched Marchfolk beyond the human-human Sagekin/Marchfolk baseline:

1. cranium height/shape;
2. skull breadth / cranial proportion;
3. forehead-to-cranium transition;
4. cheekbone / mid-face system;
5. lower-face mass;
6. jaw/chin system.

The orbit/eye region is a seventh system and must remain materially Fenn, but it cannot be the sole or dominant identity carrier.

Do not pass merely because a metric changes numerically. The visual read must agree.

---

# 9. Quantitative guard rails

Because exact numeric envelopes are OPEN, use the following as **selection constraints**, not new canon:

- every changed region must move in the canon-approved direction;
- avoid a single-region outlier dominating the face;
- no individual central-candidate change should read as caricature at true scale;
- CF2 should sit clearly above the current source in hidden-ear identity, but below an obviously stylized fantasy-elf extreme;
- c1 and c2 should produce comparable normalized identity strength.

Report:
- RMS residual vs matched Marchfolk by region;
- residual vs matched Sagekin;
- craniofacial descriptor deltas;
- head-size-normalized metrics;
- configuration consistency.

Do not hard-code the old failed thresholds into canon.

---

# 10. Face topology / UFCA regression

For every CF candidate:

- no face topology change;
- mouth loops preserved;
- orbit loops preserved;
- no new mouth-corner poles;
- no new poles in the lip/orbit active zones;
- open lip/orbit pockets preserved;
- face density unchanged;
- UFCA slot compatibility preserved.

No final creator morph implementation yet.

---

# 11. Anatomy / surface-fit gate

For each revised source:

1. generate the corresponding production realization through the active family map;
2. prove the production realization matches its revised source under T-1/T-2/T-3/T-7;
3. confirm the family topology carries the authored craniofacial geometry without loss.

The production mesh should still be:

- 57,842 V / 57,840 Q;
- face hash `ec768ae2…`;
- exact active family mapping architecture.

If a facial source change cannot be carried by the family topology, report a real topology limitation. Do not silently add topology.

---

# 12. Expression / deformation sanity

Run a focused facial readiness sanity set for CF1/CF2/CF3:

- neutral;
- blink;
- eye look up/down/left/right;
- smile;
- anger;
- surprise;
- sadness if supported by current diagnostic setup.

The goal is only to catch:
- eyelid collision;
- orbit collapse;
- cheek/lip fold caused by authored geometry;
- jaw/chin deformation conflict.

Do not author production facial weights or rig correctives.

---

# 13. Visual author sheets

Provide actual inspectable sheets for both configurations.

Required:

1. current source vs CF1 vs CF2 vs CF3 — front/profile/3-4;
2. same with ears hidden;
3. Fenn vs matched Marchfolk vs matched Sagekin for each CF candidate;
4. region heatmap / residual map;
5. cranium + forehead closeup;
6. orbit/eye closeup;
7. cheeks/mid-face closeup;
8. jaw/chin closeup;
9. wireframe showing topology unchanged;
10. config-1 vs config-2 comparison;
11. full-body hidden-ear confirmation to prove body remains unchanged;
12. expression sanity sheet.

Use identical cameras and true scale.

---

# 14. Selection logic

Return one of:

## FENN CRANIOFACIAL PASS — CF2 RECOMMENDED
Use if:
- hidden-ear face identity clearly passes;
- CF2 is the best balanced central reference;
- CF1 is too weak or borderline;
- CF3 is stronger than necessary but still valid;
- family topology carries the result cleanly.

## FENN CRANIOFACIAL PASS — CF1 RECOMMENDED
Use if restrained geometry is already sufficient and more change would overstate the race.

## FENN CRANIOFACIAL PASS — CF3 RECOMMENDED
Use only if stronger geometry is genuinely required to express the established canon without relying on ears.

## NEEDS AUTHOR SELECTION
Use if multiple candidates are equally valid but materially different in aesthetic read.

## FENN CRANIOFACIAL NEEDS TOPOLOGY BRANCH
Use only if the existing family topology truly cannot carry the accepted craniofacial anatomy.

## FAIL
Use only for a technical/source blocker.

---

# 15. Ear branch conditional unlock

If and only if the craniofacial hidden-ear gate returns PASS:

you may begin **ear-branch preparation only**, not final selection/freeze.

Prepare:
- branch region definition;
- mapping plan;
- the previously identified W1e / `FN-elven` procedural ear reference evidence if available;
- technical proposal for E1/E2/E3.

Do **not** build final E1/E2/E3 geometry in this order unless it is necessary to prove the craniofacial pass did not depend on ear topology.

The next ChatGPT order will authorize/shape the ear prototypes after reviewing the face.

---

# 16. FNF181 source status

Update reference records to reflect:

- FNF181 body architecture accepted;
- craniofacial source geometry still provisional until this gate selects/accepts a CF candidate.

Do not freeze the final Fenn source yet.

The final accepted Fenn source will be the accepted body reference plus the selected craniofacial revision plus later ear branch.

---

# 17. Required return

Commit:

1. `reviews/claude-rac-rp3-fenn-craniofacial-source-gate.md`;
2. CF1/CF2/CF3 source definitions for c1/c2;
3. deterministic source-authoring provenance;
4. revised R-6 candidate sources;
5. family-propagated candidate meshes;
6. hidden-ear facial metrics;
7. matched-human comparisons;
8. topology/UFCA regression;
9. anatomy/surface-fit audits;
10. expression sanity;
11. visual sheets;
12. hashes / frozen-base proof;
13. optional ear-branch preparation note if face PASS;
14. narrow `specs/STATUS.md` update;
15. session handoff.

The gate must explicitly answer:

- Is FNF181 body architecture formally accepted?
- Was the E-A2 pelvis tie left unchanged?
- Did CF1/CF2/CF3 share one craniofacial design architecture?
- Which regions now materially express Fenn identity?
- Does hidden-ear facial identity pass?
- Does the orbit remain Fenn without dominating the whole identity?
- Which CF candidate is recommended?
- Did family topology remain unchanged?
- Did UFCA readiness remain intact?
- Did any new facial deformation/contact defect appear?
- Is a craniofacial topology branch actually needed?
- Is the project ready to proceed to the Fenn ear branch?

---

# 18. Stop rules

After committing the craniofacial gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Fenn;
- finalize Fenn ears;
- start Aelari;
- start Vael;
- start Halvren;
- modify active MPFB Family Base v005;
- implement creator morphs;
- finalize rigging;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- FNF181 body architecture is accepted.
- The configuration-2 E-A2 pelvis result is accepted as a tie below method resolution.
- Fenn hidden-ear body identity is accepted.
- Fenn hidden-ear facial identity is not yet accepted.
- The missing work is craniofacial source geometry, not face topology.
- Author three bounded craniofacial geometry strengths on the existing topology.
- Preserve the already-good orbit/eye direction.
- The Fenn face must carry race identity before pointed ears are allowed to complete the look.

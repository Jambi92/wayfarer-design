# RAC RP3 — Vael bounded body-source correction + craniofacial source-authoring order

**Date:** 2026-10-28  
**Authority:** Tyler / ChatGPT review of Claude Vael gate `0df5739c6cfb223d857e4a79f5d43bf948e5af70`.  
**Parent order:** `reviews/chatgpt-rac-rp3-vael-body-face-ear-order.md`.  
**Parent gate:** `reviews/claude-rac-rp3-vael-body-face-ear-gate.md`.  
**Program references:**  
- `specs/vael/VAEL_V1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- frozen Fenn RP3;  
- frozen Aelari RP3;  
- active MPFB Family Base v005.

This order keeps the established Vael relational canon intact and authorizes a **bounded shared body-source correction plus deterministic craniofacial source-authoring pass**.

The goal is not to exaggerate Vael. The goal is to make the written Vael anatomy actually exist in source geometry strongly enough that Vael remains elven with ears, pigmentation, hair, culture and presentation removed.

Do not start Vael ears unless both body and hidden-ear facial gates pass.

---

# 1. AUTHOR DECISIONS — LOCKED

## 1.1 Frozen comparators remain immutable

Do not alter:
- frozen Fenn;
- frozen Aelari;
- Marchfolk family references;
- Sagekin family references;
- active MPFB Family Base v005.

Vael must fit the already-frozen comparative field.

Do not weaken or rewrite Fenn/Aelari to create space for Vael.

---

## 1.2 Vael ordering canon remains in force

Keep the established Vael relational rules from `VAEL_V1.md`.

In particular:

### Hip-joint placement
At matched stature:

> **Marchfolk < Vael < Fenn / Aelari**

for hip-joint height ÷ stature.

The Aelari R1 correction made the MF↔Aelari numeric window extremely narrow. That is acknowledged.

Ruling:

- the **ordering sign still matters**;
- do not require this one descriptor to carry racial identity;
- sub-1% differences are acceptable when the comparative window itself is sub-1%;
- do not invent a false large margin.

The source should land in the correct ordering without compromising the rest of the body.

### Lower-trunk / waist relationship
Vael costal-margin-to-crest interval ÷ torso length remains:

> **below Aelari**

at matched stature.

Again, use this as a relational constraint, not as the main identity carrier.

---

## 1.3 VALF178 foundation

Accept `VALF178` as the valid **configuration-2 construction route / provisional central foundation**:

- stature ~178.01 cm;
- deterministic;
- exact VAL4 design replicated on the c2 route;
- no configuration-specific Vael anatomy invented.

Do not freeze it in current form.

The accepted final Vael c2 source will be:

> VALF178 foundation + accepted shared body correction + accepted craniofacial revision.

---

## 1.4 Family topology

The current family propagation is technically accepted:

- v005 topology unchanged;
- 69 / 69 D1–D6;
- T-1 / T-2 / T-3 / T-7 pass;
- density pass;
- face rings pass;
- no new propagation-caused contact failure;
- deformation within current family expectations.

No non-ear topology branch is indicated.

Therefore:

> Fix Vael at the source level first.

---

# 2. Problem statement

Current Vael source has two independent identity problems.

## 2.1 Body
Vael is distinct from Fenn and Aelari, but too close to Marchfolk.

At equal height and ears hidden, Vael–Marchfolk RMS is smaller than Sagekin–Marchfolk in most body regions.

That is not enough for the written Vael rule:

> Vael never become human when ears, pigmentation, hair and cultural presentation are removed.

## 2.2 Face
Current VAL4 / VALF178 face is effectively Marchfolk with:
- eye-scale change;
- cheek-bone change.

No non-ear facial region materially departs from Marchfolk.

Therefore:

> **Vael craniofacial source anatomy is missing.**

This must be authored before ears.

---

# 3. Bounded body-source correction — architecture

Create one shared Vael body correction architecture for both configurations.

Working source names may be:
- `VAL4-R1`;
- `VALF178-R1`;

or project-consistent equivalents.

Requirements:

- same Vael-specific operation/target set on c1 and c2;
- no sex/config-specific Vael anatomy;
- stature re-solved afterward;
- all source changes deterministic and reproducible;
- original VAL4 / VALF178 preserved as ancestry.

Preferred method:
1. probe existing MPFB body/bone targets;
2. choose the smallest coherent shared correction;
3. use custom deterministic source deformation only if existing targets cannot express the canon.

Do not edit production family meshes directly.

---

# 4. Body correction priorities

The body correction must solve the comparative failures **without** turning Vael into a caricature.

Priority order:

## 4.1 Correct the hip-joint ordering
Bring hip-joint height ÷ stature to:

> MF < Vael < Aelari

for c1 and c2 at 178 cm matched stature.

Also verify vs Fenn remains correct.

Do not create this by:
- simply shortening the legs;
- truncating the pelvis below the hip;
- moving the entire pelvis uniformly;
- using a config-specific hack.

Use a coherent pelvis / femur / torso-to-pelvis relationship.

---

## 4.2 Correct lower-trunk compactness
Bring costal-margin-to-crest interval ÷ torso length below frozen Aelari for both configurations.

Preserve:
- natural lumbar lordosis;
- Vael torso-to-pelvis continuity;
- deeper ribcage;
- no waist pinch;
- no dwarf-like compression.

---

## 4.3 Increase Vael-vs-human skeletal identity
The body must become more clearly elven against Marchfolk/Sagekin through **combined relationships**, not one exaggerated measurement.

Strengthen only the written Vael systems:

### Torso / ribcage
- deeper skeletal ribcage than Fenn/Aelari;
- moderate width;
- strong 3D thoracic volume;
- compact torso-to-pelvis continuity;
- less vertical elongation than Aelari.

### Shoulders / neck
- moderate clavicles;
- stronger shoulder-to-neck integration than Fenn/Aelari;
- somewhat more shoulder-joint presence;
- no mandatory broad shoulders.

### Joints / extremity bases
Compared with Fenn/Aelari:
- more wrist presence;
- more elbow presence;
- more knee presence;
- more ankle presence;
- stronger hand base;
- stronger foot base.

Compared with humans:
- still gracile overall.

### Arms / legs
- longer than humans;
- less extreme than Fenn/Aelari;
- balanced upper/lower segments;
- preserve coherent gait and reach.

### Hands
- moderately long elven fingers;
- broader palm than Fenn/Aelari;
- stronger wrist-to-hand transition;
- not shortened human hands.

### Feet
- moderately elongated;
- broader than Fenn/Aelari;
- stronger ankle-to-foot transition;
- no gripping/clawed/cave gimmick.

---

# 5. Body correction guard rails

Do not solve human separation by making Vael extreme.

Hard guard rails:

- no stocky silhouette;
- no Durrim/Skarn-like mass;
- no barrel chest;
- no shortening all limbs;
- no giant joints;
- no giant hands/feet;
- no universal broad frame;
- no sex-specific pelvic architecture;
- no new mandatory shoulder breadth;
- no composition-based identity.

Body identity must survive:
- Narrow;
- Balanced;
- Broad;
- low muscle;
- high muscle;
- low fat;
- high fat.

This order only validates the central references, but do not author a correction that would obviously fail those future states.

---

# 6. Body candidate strategy

Do not immediately lock one correction.

Run a bounded probe matrix first.

Create 3 body-source candidates:

## VB1 — minimum correction
- smallest change that restores MF < Vael < Aelari ordering;
- only modest increase in human separation.

## VB2 — balanced correction
- restores ordering;
- strengthens Vael body identity against humans across multiple written regions;
- preferred target if natural.

## VB3 — stronger correction
- stronger but still canon-valid;
- used only to determine whether VB2 is underpowered.

All three:
- same correction architecture;
- differing only in bounded magnitude;
- identical direction/sign logic across c1/c2.

Do not choose by metrics alone.

---

# 7. Body acceptance gate

At matched 178 cm:

## Against Marchfolk / Sagekin
Vael must no longer be visually reducible to a normal human body.

The body should show a coordinated signal through several of:
- ribcage depth;
- torso continuity;
- limb share;
- joint scale;
- hand base;
- foot base;
- pelvis/hip relationship;
- shoulder/neck relationship.

Do not require every region RMS to exceed Sagekin-vs-Marchfolk.

Instead require:
- at least **four major body systems** to depart materially beyond ordinary human-family variation;
- the total visual read to remain elven with ears hidden;
- no single exaggerated region dominating identity.

## Against Fenn / Aelari
Vael must remain clearly related but distinct:
- deeper and more compact than Aelari;
- less extremity-dominant than Fenn;
- more joint/base presence than both;
- less vertically elongated than Aelari;
- no Fenn-like shallow torso.

---

# 8. Pelvis hard gate

Re-run skeletal-proxy validation at matched stature.

Required:

### VA-P2a
- > Marchfolk;
- < Fenn;
- < Aelari.

### VA-P2b
- bitrochanteric ÷ iliac-crest breadth not lower than Marchfolk.

### VA-P3
- no Aelari-style vertical iliac elongation;
- visual structural presence greater than Fenn/Aelari but lighter than Marchfolk.

### VA-P4
- AP depth > Fenn;
- AP depth > Aelari;
- approximately Marchfolk minimum relationship;
- do not force Vael > MF if not supported.

### VA-P6
- waist interval / torso < Aelari.

For the extremely narrow VA-P2a window:
- correct sign is required;
- report actual margin;
- classify sub-method-resolution differences honestly;
- do not manufacture fake precision.

---

# 9. Craniofacial source-authoring pass

In parallel with body correction, author Vael craniofacial source geometry.

Use the existing face topology.

No face topology branch is authorized unless the source proves the topology cannot carry the anatomy.

Preferred method:
1. probe existing MPFB craniofacial targets;
2. deterministic target-based source authoring;
3. bounded source-space sculpt only if targets are insufficient.

No production-mesh-only sculpt.

---

# 10. Vael craniofacial canon to express

The face must remain humanoid and clearly related to Fenn/Aelari while becoming its own elven branch.

Required directional systems:

## 10.1 Shared elven cranial ancestry
Vael should carry a subtle shared elven head architecture rather than Marchfolk cranial geometry.

This may include:
- somewhat greater cranial-height contribution than humans;
- non-human skull/face proportion relationships;
- smoother cranial continuity.

Do not simply copy Fenn CF2 or Aelari.

---

## 10.2 Compact craniofacial vertical distribution
Compared with Aelari:
- less facial verticality;
- more compact craniofacial distribution.

Compared with Marchfolk:
- must still read elven, not merely “shorter face.”

---

## 10.3 Cheek / mid-face integration
- broader cheek-to-mid-face integration than Aelari;
- somewhat greater mid-face structural depth;
- stronger 3D cheek/mid-face relationship;
- not broad-faced by default;
- no permanent gauntness.

---

## 10.4 Orbit structure
- somewhat broader orbit architecture than Aelari;
- keep low-light adaptation biologically conservative;
- do not create giant eyes;
- do not invent glow, eye shine, tapetum, darkvision or daylight weakness.

Existing eye-scale may remain if coherent.

---

## 10.5 Brow-orbit relationship
- stronger brow/orbit definition than Aelari;
- no permanent scowl;
- no villain-face stereotype;
- no heavy human brow ridge copied from Skarn.

---

## 10.6 Jaw / mandible
- more mandibular presence than Fenn/Aelari;
- still gracile next to humans overall;
- no square-jaw requirement;
- broad variation must remain possible.

---

## 10.7 Nose / mouth
No mandatory Vael nose or mouth stereotype.

Do not create identity by:
- hooked nose;
- tiny nose;
- thin lips;
- downturned mouth;
- “sinister” resting expression.

---

# 11. Craniofacial candidates

Create three source candidate families on one design architecture:

## VC1 — restrained
- smallest coherent Vael craniofacial departure;
- should show ancestry but may be borderline.

## VC2 — balanced central
- all required systems clearly expressed;
- natural and non-caricatured;
- preferred target.

## VC3 — stronger
- stronger valid central-population expression;
- still humanoid;
- not a creator maximum.

Same topology.
Same target keys/signs.
Same design logic for c1/c2.
Only bounded magnitude differs.

Do not silently select a winner.

---

# 12. Combined-body/face candidate handling

Do not explode the matrix into 9 full production candidates unnecessarily.

Recommended process:

1. solve/probe VB1/VB2/VB3 on source metrics and visuals;
2. select one provisional body correction for the face pass;
3. apply VC1/VC2/VC3 to that body candidate;
4. if the body winner changes after visual review, reapply the selected face architecture to the final body candidate and rerun gates.

Keep provenance explicit.

---

# 13. Hidden-ear facial acceptance gate

Matched height/frame/composition/age/pose:
- Vael;
- Marchfolk;
- Sagekin;
- frozen Fenn;
- frozen Aelari.

Ears collapsed/hidden.
Neutral grey shading.
No hair/pigmentation/culture.

After similarity alignment removing global head size, Vael must show a coordinated non-human signal.

Minimum requirement:

At least **four** of the following six Vael systems must materially depart from Marchfolk beyond ordinary human-family variation in the intended direction:

1. cranial proportion / shared elven ancestry;
2. compact vertical distribution;
3. cheek / mid-face integration;
4. mid-face depth;
5. orbit / brow system;
6. mandibular system.

Additionally:
- Vael must remain visibly distinct from frozen Fenn;
- Vael must remain visibly distinct from frozen Aelari;
- no single eye/orbit feature may carry most of the identity.

Use the Fenn hidden-ear lesson: do not accept “human + bigger eyes.”

---

# 14. Human firewall

Explicitly test:

> “If I remove ears, pigmentation, hair, clothing, culture and low-light presentation, does this still look like a Vael rather than a Marchfolk/Sagekin variant?”

If the answer is no:
- fail the source;
- do not unlock ears.

The Vael body and face together must carry ancestry.

---

# 15. Three-elf firewall

Also test:

> “Can I tell Vael, Fenn and Aelari are related without making them copies?”

Required population-level read:

- Fenn:
  - extremity emphasis;
  - shallower torso;
  - lighter joints;
  - Fenn CF2 face.
- Aelari:
  - whole-body vertical continuity;
  - elongated torso/waist;
  - very gracile joints;
  - frozen Aelari face.
- Vael:
  - deeper torso;
  - compact continuity;
  - more joint/base presence;
  - distinct compact/deeper craniofacial construction.

Do not exaggerate until they look like separate species.

---

# 16. Family propagation after source selection

Once a provisional VB + VC combination passes source-level review:

Propagate to active family v005 unchanged.

Require:
- 57,842 V / 57,840 Q before ears;
- family face topology hash unchanged;
- family map unchanged;
- 69 / 69 D1–D6;
- T-1/T-2/T-3/T-7;
- density;
- face rings / UFCA readiness;
- contact;
- deformation;
- read-back;
- source fit.

If source geometry cannot be carried cleanly, return a true topology limitation rather than silently altering the family base.

---

# 17. Expression sanity

Only after a craniofacial candidate passes hidden-ear identity, run diagnostic expression sanity:

- neutral;
- blink;
- look up/down;
- smile;
- anger;
- surprise;
- sadness.

Check:
- eyelid collision;
- orbit collapse;
- cheek/lip fold;
- jaw/chin conflict.

Do not author final facial weights/correctives.

If a generic MPFB expression issue appears on the accepted source:
- classify honestly as source / topology / rig;
- do not automatically reopen good anatomy.

---

# 18. Low-light physiology firewall

Do not invent or implement:
- enlarged pupils;
- glowing eyes;
- eye shine;
- tapetum-like anatomy;
- darkvision mechanics;
- magical retina;
- daylight weakness;
- nocturnal-animal eyes.

This order is skeletal / craniofacial source authoring only.

Low-light physiology remains OPEN.

---

# 19. Ear branch remains locked

Do not build:
- VA-E1;
- VA-E2;
- VA-E3;
- Vael ear topology;
- Vael ear morphs.

Ear work unlocks only if:

1. body comparative gate PASS;
2. pelvis ordering PASS;
3. hidden-ear body PASS;
4. hidden-ear face PASS;
5. human firewall PASS;
6. three-elf firewall PASS.

Then stop for ChatGPT review before ears.

---

# 20. Required visual package

Provide actual inspectable sheets.

## Body
1. VAL4 / VALF178 original vs VB1/VB2/VB3;
2. equal-height Vael vs MF vs SG;
3. equal-height Vael vs frozen Fenn vs frozen Aelari;
4. torso/ribcage;
5. shoulder/neck;
6. pelvis/waist;
7. hip-joint ordering diagnostic;
8. arms/hands;
9. legs/ankles/feet;
10. body regional residual heatmaps.

## Face
11. source vs VC1/VC2/VC3 front/profile/3-4;
12. ears-hidden candidate comparison;
13. Vael vs MF/SG/Fenn/Aelari;
14. cranial region;
15. cheek/mid-face;
16. orbit/brow;
17. jaw/chin;
18. regional residual heatmaps;
19. descriptor table visual;
20. expression sanity for the provisional winner.

## Technical
21. family propagation overlay;
22. validator margins;
23. density;
24. deformation;
25. final equal-height hidden-ear three-elf + human comparison.

Use identical cameras and true scale where applicable.

---

# 21. Candidate selection logic

Return:

## VAEL SOURCE PASS — VB2 + VC2 RECOMMENDED
if the balanced candidates best satisfy canon.

Or identify another VB/VC pairing if evidence supports it.

Possible outcomes:

### VAEL BODY PASS / FACE PASS — READY FOR EAR ORDER
All gates pass.

### VAEL BODY PASS / FACE NEEDS REVISION
Body solved, craniofacial source still weak.

### VAEL BODY NEEDS REVISION / FACE PASS
Face solved, body still too human or ordering fails.

### VAEL SOURCE NEEDS TOPOLOGY BRANCH
Only if existing topology truly cannot carry accepted source anatomy.

### FAIL
Only for a blocking source/tool problem.

Do not freeze Vael in this order.

---

# 22. Required return

Commit:

1. `reviews/claude-rac-rp3-vael-body-face-source-gate.md`;
2. VB1/VB2/VB3 definitions and source candidates;
3. VC1/VC2/VC3 definitions and source candidates;
4. source-probe matrix;
5. c1/c2 deterministic build records;
6. skeletal-proxy pelvis validation;
7. equal-height three-elf + human comparison;
8. hidden-ear body metrics;
9. hidden-ear face metrics;
10. selected provisional body+face combination;
11. family-propagated provisional candidates;
12. D1–D6 validator;
13. anatomy/density/contact/deformation;
14. expression sanity if face passes;
15. visual sheets;
16. immutable frozen-reference hash proof;
17. narrow `specs/STATUS.md` update;
18. session handoff.

The gate must explicitly answer:

- Is VALF178 still the valid c2 foundation?
- Which VB candidate is recommended?
- Does MF < Vael < Aelari hip-joint ordering now hold on c1/c2?
- Does VA-P6 now hold on c1/c2?
- Is Vael body separation from humans materially improved?
- Does Vael remain distinct from frozen Fenn and Aelari?
- Which VC candidate is recommended?
- Does hidden-ear facial identity pass against Marchfolk/Sagekin?
- Does Vael remain distinct from frozen Fenn/Aelari faces?
- Did any face region become caricatured?
- Did family topology remain unchanged?
- Are both production candidates 69/69 D1–D6?
- Did any new source/contact/deformation failure appear?
- Is a non-ear topology branch actually needed?
- Is Vael ready to unlock ear prototyping?

---

# 23. Stop rules

After committing the body/face source gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Vael;
- build Vael ears;
- start Halvren;
- modify frozen Fenn;
- modify frozen Aelari;
- modify active MPFB Family Base v005;
- invent low-light physiology;
- implement creator morphs;
- finalize rigging;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Keep Vael canon intact.
- Keep frozen Fenn/Aelari immutable.
- Accept VALF178 as the valid c2 construction foundation only.
- Fix the small Aelari-order inversions with a shared bounded body-source correction.
- Strengthen Vael-vs-human body identity through the written torso/joint/extremity-base systems, not exaggerated limbs.
- Author real Vael craniofacial anatomy on the existing topology using VC1/VC2/VC3.
- Vael must remain elven with ears and presentation hidden.
- Do not unlock ears until body + face pass.

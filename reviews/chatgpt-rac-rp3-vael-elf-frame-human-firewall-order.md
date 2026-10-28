# RAC RP3 — Vael final elf-frame correction + human-firewall closure order

**Date:** 2026-10-28  
**Authority:** Tyler / ChatGPT review of Claude return `842f33a8b1c8ebd9a548c1a626d447d61a64b936`.  
**Parent gate:** `reviews/claude-rac-rp3-vael-custom-body-deformation-gate.md`.  
**Program references:**  
- `specs/vael/VAEL_V1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- frozen Fenn RP3;  
- frozen Aelari RP3;  
- active MPFB Family Base v005.

This order authorizes one final bounded Vael body-source correction aimed specifically at the remaining full-body frontal / three-quarter human-firewall gap.

The accepted Vael face, pelvis ordering, R1/VD2 torso work, family topology and frozen comparators are not to be reopened.

If this pass succeeds, the next stage is Vael ear prototyping.

---

# 1. AUTHOR DECISIONS — LOCKED

## 1.1 VC2 remains accepted and frozen in direction

Do not alter:
- VC2 target architecture;
- cranial proportions;
- cheek/mid-face structure;
- brow/orbit interpretation;
- jaw/chin direction;
- head size;
- facial hidden-ear identity.

VC2 remains the accepted central Vael craniofacial direction.

---

## 1.2 VD2 remains the body foundation

Keep the current VD2 custom field work:

- ribcage side-wall shaping;
- torso-to-pelvis continuity;
- pelvis/hip contour;
- clavicle local shaping;
- palm-root reinforcement;
- heel/proximal-foot reinforcement.

Do not increase VD2 to VD3.

Do not use GX as a candidate.

GX was diagnostic only.

---

## 1.3 Pelvis/order work remains locked

Preserve:

> **Marchfolk < Vael < Aelari < Fenn**

for hip-joint height / stature.

Preserve:
- VA-P6;
- VA-P2b;
- VA-P3 no Aelari-style vertical iliac elongation;
- VA-P4 AP-depth relationships;
- 9/9 pelvis gate.

The final correction may not break the narrow ordering window.

---

## 1.4 Human-firewall standard remains strict

Do **not** lower the hidden-ear human-firewall standard.

Vael must remain visibly elven enough that the body does not reduce to a Marchfolk/Sagekin variant when:
- ears;
- pigmentation;
- hair;
- clothing;
- culture;
- low-light presentation

are removed.

Do not use the future ears to solve the body.

---

# 2. Remaining diagnosis

The current VD2 body is technically clean and locally distinct, but the full-body frontal / 3-4 silhouette remains too close to Marchfolk.

Claude’s diagnostic shows the missing full-body signal is concentrated in two structural systems that were outside the previous order:

1. **shoulder / clavicle span**, and
2. **limb-envelope gracility**.

Frozen elves establish the ancestral direction:

- Fenn shoulder span is roughly 4–6% below Marchfolk;
- Aelari is roughly 4–5% below Marchfolk;
- Vael VD2 is effectively equal to Marchfolk.

Vael should not match Fenn/Aelari exactly.

The goal is a **modest intermediate elf-family signal**, while retaining Vael’s greater structural presence.

---

# 3. Authorized final term — VEF1

Create one shared deterministic Vael **Elf-Frame term**, provisionally named:

> **VEF1**

Apply it on top of the accepted R1 + VD2 source.

VEF1 has exactly two primary components:

1. bounded shoulder/clavicle-span reduction;
2. bounded long-bone soft-envelope gracility.

No unrelated anatomy changes are authorized.

---

# 4. Component A — shoulder / clavicle span

## Goal

Move the central Vael shoulder skeleton subtly toward the shared elven foundation while keeping Vael structurally broader / more present than Fenn or Aelari.

Target central direction:

> approximately **2–3% narrower than matched Marchfolk**

at bideltoid / clavicle-span level.

This is not a hard exact number if the anatomy reads better slightly outside it, but the central reference should remain clearly:

> Marchfolk > Vael > Fenn/Aelari

in average shoulder span.

---

## 4.1 What may change

Allowed:
- clavicle lateral span;
- shoulder-joint placement relationship;
- upper thorax / clavicle attachment contour needed for continuity;
- deltoid skeletal envelope only as required by joint placement.

Preferred:
- achieve the change through skeletal/bone-scale or deterministic source-space construction, not by pinching skin alone.

---

## 4.2 What may not change

Do not create:
- universally narrow shoulders;
- sloped-shoulder stereotype;
- weak shoulder joints;
- Fenn copy;
- Aelari copy;
- muscle-dependent narrowing.

Frame variation remains fully supported.

A Broad Vael must still be broad.

This term moves the **population foundation**, not the creator range endpoints.

---

# 5. Component B — limb-envelope gracility

## Goal

Introduce a subtle shared-elven shaft gracility while preserving Vael’s stronger joint and extremity-base identity.

Affected shaft regions:

- upper arm;
- forearm;
- thigh;
- calf.

Target central magnitude:

> approximately **3–5% radial envelope reduction** versus the current VD2 shaft envelope,

subject to joint continuity and visual review.

Do not blindly use 5% everywhere.

Use anatomy-aware tapered fields.

---

## 5.1 Critical Vael distinction

The intended read is:

> **slimmer limb shafts + comparatively stronger joint / hand / foot bases**

This is important.

Do not reduce:
- elbow identity;
- wrist-base presence;
- knee presence;
- ankle-base presence;
- palm-root strength;
- heel/proximal-foot strength.

Vael should remain more structurally present at these bases than Fenn/Aelari.

---

## 5.2 Taper requirements

Each shaft field must fade before the joints.

For example:

### Upper arm
- strongest at shaft midsection;
- fade toward shoulder;
- fade toward elbow.

### Forearm
- strongest mid-shaft;
- preserve elbow;
- preserve wrist transition.

### Thigh
- strongest through middle shaft;
- preserve hip articulation;
- preserve knee.

### Calf
- preserve knee;
- preserve ankle;
- no pencil-leg silhouette.

No abrupt diameter changes.

---

# 6. Deterministic architecture

VEF1 must be:

- source-space;
- deterministic;
- shared c1/c2;
- parameterized;
- reproducible;
- versioned.

Preferred implementation:
- extend `tools/rac/w1/vael_body_field.py` or equivalent structured system;
- do not create a disconnected one-off script with hidden manual coordinates.

Record:
- region masks;
- bone/landmark anchors;
- normalized axes;
- magnitudes;
- falloffs;
- stature normalization;
- c1/c2 normalization.

---

# 7. Candidate strengths

Create exactly three strengths using one architecture:

## VF1 — restrained
- shoulder span around the low end;
- mild shaft gracility.

## VF2 — balanced
- intended central solution;
- provisional target around 2–3% shoulder reduction and moderate shaft slimming.

## VF3 — stronger
- stronger but still anatomically valid;
- used only to determine whether VF2 is underpowered.

All three:
- same masks;
- same signs;
- same topology;
- magnitude only differs.

Do not create alternate designs.

---

# 8. Protected geometry

The following must remain unchanged except continuity-level effects explicitly disclosed:

- VC2 head / face;
- neck length;
- accepted VD2 ribcage depth;
- accepted VD2 torso-to-pelvis field;
- accepted pelvis / hip contour;
- hip-joint centres;
- limb lengths;
- hand length/finger length;
- foot length;
- palm-root field;
- heel field;
- source ear zone.

No stature change except normal re-solve / grounding.

---

# 9. Human-firewall visual gate

At equal 178 cm, matched frame / muscle / fat / age / pose:

Compare:
- Vael VF1/VF2/VF3;
- Marchfolk;
- Sagekin.

Ears hidden.
Neutral grey.
Identical camera.

Required views:
- front;
- 3-4 front;
- profile;
- rear if useful.

The accepted candidate must read as a related-but-non-human body at normal whole-character scale.

Do not require dramatic separation.

The standard is:

> **clearly not just another normal human-family body when presented beside Marchfolk/Sagekin.**

The distinction should arise from the combined system:

- moderately narrower shoulder foundation;
- gracile limb shafts;
- Vael deep torso;
- Vael torso/pelvis continuity;
- stronger joint bases;
- stronger palm/foot bases;
- accepted Vael face.

---

# 10. Three-elf firewall

Compare against frozen Fenn and frozen Aelari.

Required ordering/read:

### Fenn
- narrower/lighter joints than Vael;
- more extremity-led;
- shallower torso;
- distinct Fenn face.

### Aelari
- more vertically elongated;
- more gracile joints;
- longer vertical continuity;
- distinct Aelari face.

### Vael
- moderately gracile shafts;
- deeper torso;
- more compact body continuity;
- stronger joints and extremity bases;
- shoulder foundation between humans and the other elves;
- VC2 face.

Do not collapse the three elves into one body type.

---

# 11. Shoulder-span acceptance

Report matched-stature:

- clavicle span;
- shoulder-joint span;
- bideltoid span.

Against:
- Marchfolk;
- Sagekin;
- frozen Fenn;
- frozen Aelari.

Preferred central ordering:

> **MF/SG > Vael > Fenn/Aelari**

Do not enforce an exact ranking between Fenn and Aelari unless already frozen by their canon.

---

# 12. Limb-envelope acceptance

Report mid-shaft breadth/depth or equivalent stable measures for:

- upper arm;
- forearm;
- thigh;
- calf.

Also report joint/base measures at:

- elbow;
- wrist;
- knee;
- ankle;
- palm root;
- heel/proximal foot.

The shaft change must not erase Vael’s stronger bases.

---

# 13. Composition firewall

This term must represent skeletal / structural population anatomy, not body composition.

Demonstrate logically and through the field definition that:
- muscle controls remain independent;
- fat controls remain independent;
- frame controls remain independent.

If feasible, run a limited source-level stress diagnostic on:
- narrow / low muscle;
- balanced;
- broad / higher muscle.

This is not full UCCA validation.

The goal is only to prove the field is not a thinness preset.

---

# 14. Pelvis regression — HARD

Re-run the current pelvis suite.

Required:
- MF < Vael < Aelari < Fenn remains;
- VA-P6 remains;
- VA-P2b remains;
- VA-P3 vertical rule remains;
- VA-P4 remains;
- 9/9 remains.

No candidate that breaks the hip-ordering window may pass.

---

# 15. VD2 / torso regression

Verify the final term does not create:

- waist pinch;
- barrel chest;
- lost thorax depth;
- lost compact continuity;
- new shoulder/trunk discontinuity.

Compare R1 → VD2 → VF candidate.

The GX c2 waist-pinch outcome is specifically forbidden.

---

# 16. Source integrity / determinism

For all VF candidates:

- independent rebuild identical;
- regen identical;
- face arrays unchanged;
- 1 component;
- 0 boundary;
- 0 non-manifold;
- 0 degenerate;
- outward normals;
- no new source self-intersection attributable to VEF1.

Report:
- affected vertex count;
- max displacement;
- RMS displacement;
- regional displacement.

---

# 17. Production family propagation

Propagate the provisional winner to frozen family v005 topology unchanged.

Require:

- 57,842 V / 57,840 Q;
- identical face hash;
- identical family map / UVs;
- 69 / 69 D1–D6;
- T-1 / T-2 / T-3 / T-7;
- density pass;
- face rings unchanged;
- 0 new contact failure;
- acceptable deformation;
- byte-identical PC read-back.

No non-ear topology branch.

---

# 18. VC2 regression

Confirm:
- VC2 geometry unchanged;
- hidden-ear face PASS unchanged;
- elf-face differentiation unchanged;
- brow ruling unchanged;
- no new jaw inflation from shoulder/neck changes.

If jaw/neck metrics move materially:
- correct the VEF1 shoulder field;
- do not modify VC2.

---

# 19. Deformation readiness

Run the standard body diagnostic poses on the provisional winner.

Focus especially on:
- shoulders;
- elbows;
- wrists;
- hips;
- knees;
- ankles.

The narrower shoulder foundation must not:
- collapse arm raising;
- cause arm/trunk collision;
- create shoulder inversion.

The shaft gracility must not destabilize joint deformation.

---

# 20. Candidate selection rule

Return exactly one:

## VAEL HUMAN FIREWALL PASS — VF2 RECOMMENDED — EAR PROTOTYPING UNLOCKED

## VAEL HUMAN FIREWALL PASS — VF1 RECOMMENDED — EAR PROTOTYPING UNLOCKED

## VAEL HUMAN FIREWALL PASS — VF3 RECOMMENDED — EAR PROTOTYPING UNLOCKED

## VAEL HUMAN FIREWALL PASS — NEEDS AUTHOR SELECTION

## VAEL FRAME TERM NEEDS LOCAL REVISION

## FAIL

Do not freeze Vael.

---

# 21. If the human firewall passes

Prepare a **Vael ear-branch proposal** in the same commit, but do not build the final ears.

The proposal should evaluate reuse of the **Fenn v002 engineering ear topology**.

Required:

- whether the root interface fits Vael cleanly;
- whether topology can support Vael-specific anatomy without becoming a Fenn copy;
- proposed VA-E1 / VA-E2 / VA-E3 central geometries;
- relative length;
- projection;
- tilt;
- sweep;
- base width;
- upper extension;
- anatomical distinctions vs frozen Fenn and Aelari ears.

Respect:
- Fenn has greatest average lateral projection among the elves;
- Vael must have its own ear-family read;
- no universal elf-ear freeze.

Do not construct final ear geometry until the next ChatGPT order.

---

# 22. Required visual package

Provide true-scale identical-camera sheets:

1. VD2 vs VF1/VF2/VF3 front;
2. 3-4;
3. profile;
4. final candidate vs Marchfolk/Sagekin front;
5. final candidate vs Marchfolk/Sagekin 3-4;
6. final candidate vs frozen Fenn/Aelari;
7. shoulder-span comparison;
8. clavicle / shoulder-joint closeup;
9. upper-arm shaft;
10. forearm shaft / wrist base;
11. thigh shaft / knee;
12. calf / ankle / foot base;
13. torso / waist regression;
14. pelvis regression;
15. silhouette overlays vs Marchfolk;
16. regional displacement heatmap;
17. validator;
18. density;
19. deformation;
20. VC2 face regression;
21. final five-population body comparison;
22. optional narrow/balanced/broad stress diagnostic.

---

# 23. Required return

Commit:

1. `reviews/claude-rac-rp3-vael-elf-frame-human-firewall-gate.md`;
2. VEF1 definition;
3. VF1/VF2/VF3 c1/c2 sources;
4. deterministic rebuild proof;
5. shoulder-span measurements;
6. shaft/base measurements;
7. human-firewall metrics;
8. three-elf regression;
9. composition firewall note;
10. pelvis regression;
11. VD2 torso regression;
12. provisional winner propagation;
13. D1–D6 / density / contact / deformation;
14. VC2 regression;
15. visual package;
16. ear-branch proposal only if firewall passes;
17. immutable hash proof;
18. narrow `specs/STATUS.md` update;
19. session handoff.

The gate must explicitly answer:

- Is VC2 unchanged?
- Is VD2 retained?
- Which VF candidate is recommended?
- What is the final shoulder-span ordering?
- How much did upper-arm / forearm / thigh / calf envelopes change?
- Did Vael’s stronger joint and extremity bases remain?
- Does the full-body front / 3-4 human firewall finally pass?
- Does the three-elf firewall remain pass?
- Did any candidate become too narrow, frail or Aelari/Fenn-like?
- Is waist/ribcage integrity preserved?
- Does pelvis remain 9/9?
- Did family topology remain unchanged?
- Are both propagated bodies 69/69 D1–D6?
- Did deformation remain acceptable?
- Is Vael ready for ear prototyping?

---

# 24. Stop rules

After committing the gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Vael;
- build final Vael ears;
- start Halvren;
- modify frozen Fenn;
- modify frozen Aelari;
- modify active MPFB Family Base v005;
- modify VC2;
- invent low-light physiology;
- implement creator morphs;
- finalize rigging;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Keep VD2.
- Keep VC2.
- Keep the solved pelvis/order work.
- Do not relax the human firewall.
- Author one final bounded shared elf-frame term:
  - moderately narrower shoulder/clavicle foundation;
  - moderately gracile limb shafts;
  - preserve Vael’s stronger joints, palms, feet and deep torso.
- Do not make Vael thin, frail, narrow by default, Fenn-like or Aelari-like.
- If the full-body human firewall passes, Vael ear prototyping is unlocked.

# RAC RP2 — Grask anatomical source v003 bounded extremity refinement order

**Date:** 2026-10-24  
**Authority:** Tyler direct author ruling through ChatGPT after review of Grask anatomical source v002.  
**Parent refinement order:** `reviews/chatgpt-rac-rp2-grask-3d-source-v002-refinement-order.md` (63d7dde).  
**Claude v002 return:** `reviews/claude-rac-rp2-grask-3d-source-v002-refinement-final-gate.md` (74c6ce4).  
**Current source:** `GR_U_REF_RP2_SOURCE_3D_v002.blend`.

## 1. Author review ruling

The v002 Grask source is accepted in its **overall body morphology and species direction**.

The following are now effectively locked against unnecessary reshaping:

- whole-body silhouette;
- torso/ribcage mass hierarchy;
- waist and pelvis breadth;
- glute and upper-thigh massing;
- leg proportions;
- calf mass;
- foot overall scale;
- shoulder width;
- neck/trapezius relationship;
- upper-back mass;
- head size and general troll-like identity;
- overall 218 cm stature.

Do **not** restart body-shape exploration.

Do **not** globally smooth, resculpt, or retune the accepted body merely to chase small local imperfections.

The remaining author concern is concentrated in the **hands and feet**, with a limited inspection of the **ears and eye/brow region**.

This order is a bounded final-source refinement, not a redesign.

## 2. Mission

Create:

`GR_U_REF_RP2_SOURCE_3D_v003.blend`

using v002 as the direct parent.

Goal:

> Preserve the accepted v002 Grask body while bringing hands and feet to production-reference anatomical quality, and correct only clearly justified residual issues in ears or eye/brow anatomy.

Claude must complete the full bounded refinement, self-audit it, repair failures internally, and only return after its own gate passes.

Do not submit a partial pass.

## 3. Mandatory correction A — hands

The hand scale and general mass are accepted.

The remaining issue is **anatomical structure and articulation**.

Current concern:
- fingers still read somewhat soft/tubular;
- phalange segmentation is too weak;
- knuckle hierarchy is underdefined;
- some bends feel smoothly generated instead of structurally jointed;
- thumb-to-palm integration needs one more anatomy pass.

### Required

Refine, while preserving hand size:

- MCP knuckle hierarchy;
- proximal/intermediate/distal phalange rhythm;
- subtle joint-plane changes at PIP/DIP;
- finger taper;
- fingertip pad shape;
- dorsal knuckle transitions;
- palm thickness;
- metacarpal block;
- thenar mass;
- thumb root;
- thumb MCP/IP rhythm;
- first web space;
- wrist-to-hand transition.

Hands should read as:
- large;
- powerful;
- troll-like;
- dexterous enough for tools/weapons;
- anatomically intentional.

### Species rule

Do **not** simply make a human hand larger.

The Grask hand may be heavier and broader than a human hand, but must retain believable functional anatomy.

### Do not

- add claws;
- reduce to four fingers;
- make fingers elegant/slender;
- create sausage digits;
- create paw pads;
- exaggerate tendons/veins;
- introduce bodybuilder hand anatomy;
- alter arm length or global hand scale without documented author-level reason.

## 4. Mandatory correction B — feet and toes

The overall foot size, heel, arch direction, plantigrade stance, and grounded silhouette are accepted.

The main concern is the **toe construction**.

Current concern:
- toes still read too rounded/blob-like;
- toe bases are too soft;
- phalange rhythm is not clear enough;
- nail-bed regions are under-resolved;
- forefoot-to-toe transitions need more deliberate structure.

### Required

Refine:

- hallux base and taper;
- lesser-toe hierarchy;
- MTP transition;
- proximal/distal toe segment rhythm;
- toe sidewalls;
- interdigital separation;
- toe-tip pad shape;
- nail-bed plane;
- nail proportion and seating;
- forefoot-to-toe transition;
- medial/lateral forefoot contour.

Preserve:
- five toes;
- ordinary nails;
- no claws;
- broad planted foot;
- large Grask foot scale;
- plantigrade stance;
- accepted heel and arch mass.

### Do not

- shrink the feet;
- turn toes into claws;
- create feline/canine paws;
- produce bulbous toy-like toes;
- narrow the forefoot;
- alter leg length.

## 5. Limited inspection C — ears

The v002 ear direction is acceptable.

Do **not** redesign the ears by default.

Inspect the following at close range:

- helix/antihelix continuity;
- conchal depth;
- tragus/antitragus equivalent;
- lobe/lower attachment;
- posterior attachment to skull;
- left/right mirrored seam quality.

Only make changes where the v002 anatomy is visibly simplified, melted, or mechanically mirrored in a way that prevents the ear reading as intentional organic anatomy.

Keep:
- robust shape;
- modest non-human identity;
- current overall size and orientation.

Avoid:
- elf points;
- fin-like shapes;
- ornamental exaggeration;
- reverting to human ears.

## 6. Limited inspection D — eye / brow region

The head identity is accepted.

Do **not** globally resculpt the face.

Inspect whether the very narrow eye openings are:

1. an intentional, anatomically coherent Grask trait, or
2. inherited generator compression that prevents a believable eyelid/orbit structure.

### If intentional and anatomically coherent
Preserve them.

### If generator-compressed
Correct only enough to establish:
- upper/lower lid separation;
- believable palpebral opening;
- orbit-to-brow relationship;
- eyelid seating around the eyeball volume;
- no pinched or collapsed inner/outer canthus.

Preserve:
- stern expression;
- heavy brow;
- broad nose;
- cheek/jaw structure;
- troll identity.

Do not make the face friendlier, more human, or more open-eyed merely for aesthetics.

Document the conclusion either way.

## 7. Hard freeze on accepted body

Unless a local extremity repair mathematically requires a tiny blending zone, do not modify:

- chest;
- ribcage;
- abdomen;
- waist;
- pelvis;
- glutes;
- thighs;
- calves;
- shoulders;
- neck;
- back;
- head cranial volume;
- overall stature;
- major limb lengths.

No global smoothing.

No proportional re-targeting.

No silhouette matching pass beyond verifying that v003 did not regress v002.

## 8. Surface discipline

This is still a neutral race anatomical source.

Do not add:
- pores;
- scars;
- wrinkles;
- veins;
- tertiary skin detail;
- muscle striations;
- texture-driven forms.

Extremity improvements must come from **primary and secondary anatomy**, not surface decoration.

## 9. Technical gate

Maintain at minimum the v002 source quality:

- exactly 1 intended body;
- 0 boundary edges;
- 0 non-manifold edges;
- genus 0;
- 0 degenerate faces;
- 0 duplicate/coincident geometry;
- consistent outward normals;
- 0 catastrophic self-intersections;
- no floating fragments;
- no cloth;
- no duplicate shells;
- no accidental holes;
- height = **218.000 cm** within negligible numerical tolerance.

Record:
- vertex/face counts;
- bbox;
- height;
- component count;
- boundary/non-manifold counts;
- self-intersection count;
- source and output hashes;
- exact moved-region masks;
- max/p95 movement by hand, foot, ear, eye/brow.

## 10. Mandatory self-audit

Claude must mark PASS/FAIL for each:

1. hand size preserved;
2. fingers no longer read tubular/melted;
3. knuckle hierarchy is visible but not over-carved;
4. finger joints bend with believable phalange structure;
5. thumb root and thenar region are coherent;
6. hands still read as Grask, not scaled human hands;
7. foot size and planted silhouette preserved;
8. toe hierarchy is clear;
9. toe bases and phalange rhythm are anatomically coherent;
10. nail-bed regions are properly seated;
11. toes no longer read as rounded blobs;
12. ears remain organic and intentional;
13. eye/brow decision is documented and anatomically justified;
14. no accepted v002 body region regressed;
15. no global silhouette drift;
16. all technical source gates pass.

If any mandatory item fails, continue working internally.

Do not turn in a known failure.

## 11. Required visual evidence

### A. v003 whole-body regression sheet
Identical cameras to v002:
- front;
- profile;
- back;
- 3/4 front;
- 3/4 back.

Purpose: prove accepted body morphology did not drift.

### B. Hands — v002 vs v003
Identical close cameras:
- palm;
- dorsal;
- 3/4;
- outer/ulnar;
- thumb root;
- finger side view;
- knuckle close-up;
- fingertip close-up.

### C. Feet — v002 vs v003
Identical close cameras:
- top/front;
- side outer;
- side inner;
- 3/4;
- heel;
- sole;
- toe close-up;
- toe 3/4;
- nail-bed close-up.

### D. Ear inspection
- profile;
- 3/4;
- rear attachment;
- left/right comparison.

### E. Eye/brow inspection
- face front;
- face 3/4;
- profile;
- close front orbital view;
- close 3/4 orbital view.

Include a one-line conclusion:
- `EYE OPENING PRESERVED — INTENTIONAL / ANATOMICALLY COHERENT`
or
- `EYE OPENING CORRECTED — GENERATOR COMPRESSION REMOVED`

## 12. Deliverables

Create:

`GR_U_REF_RP2_SOURCE_3D_v003.blend`

Export a provenance GLB copy if practical.

Final report:

`reviews/claude-rac-rp2-grask-3d-source-v003-extremity-final-gate.md`

Evidence:

`reviews/rac-rp2-evidence/grask_3d_source_v003_extremity/`

Update:
- `reviews/claude-session-handoff.md`
- `specs/STATUS.md`

Preserve v001 and v002 source files and all historical RP2 production artifacts unchanged.

## 13. Stop rule

Do not begin production retopology.

Do not create RP2 production v007.

Do not rig.

Do not create creator morphs.

Do not start another race.

After all gates pass, return exactly:

**RP2 GRASK 3D ANATOMICAL SOURCE V003 EXTREMITY REFINEMENT PASS / READY FOR AUTHOR FREEZE REVIEW**

Then STOP for Tyler review.

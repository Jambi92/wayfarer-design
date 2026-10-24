# RAC RP2 — Grask anatomical source v004 final extremity reconstruction order

**Date:** 2026-10-24  
**Authority:** Tyler direct author ruling through ChatGPT after author review of Grask anatomical source v003.  
**Parent order:** `reviews/chatgpt-rac-rp2-grask-3d-source-v003-extremity-refinement-order.md` (b00ac6b).  
**Claude v003 return:** `reviews/claude-rac-rp2-grask-3d-source-v003-extremity-final-gate.md` (9831a48).  
**Current source:** `GR_U_REF_RP2_SOURCE_3D_v003.blend`.

## 1. Author ruling

v003 is **NOT approved for freeze**.

The body, head identity, eye correction, ear direction, stature, and overall Grask morphology are accepted and must remain frozen.

The remaining failure is now explicitly concentrated in the extremities:

1. **Hands / fingers — mandatory FAIL**
   - Fingers remain too soft, tubular, and generated-looking.
   - The digit bends read as curved tubes rather than articulated phalanges.
   - MCP/PIP/DIP structure is still too weak.
   - Finger-root and web-space anatomy is not convincing.
   - Fingertip and nail-bed structure is insufficiently readable.
   - Thumb/palm integration still lacks a strong functional grasping-hand construction.

2. **Feet / toes — mandatory FAIL**
   - Toes remain too rounded/blunt and blob-like.
   - Toe-root and MTP structure is still weak.
   - Phalange rhythm is insufficient.
   - Nail-bed / nail-plate readability is too subtle.
   - The forefoot-to-toe transition still looks generated rather than deliberately sculpted.

Claude's v003 technical pass is acknowledged, but the author visual gate overrides the 16/16 self-audit for these extremity regions.

This order is a **final extremity anatomy reconstruction pass**, not another light displacement polish.

## 2. Mission

Create:

`GR_U_REF_RP2_SOURCE_3D_v004.blend`

using v003 as the direct parent.

Goal:

> Reconstruct the hands/fingers and feet/toes until they read as deliberate, functional Grask anatomy at close range, while preserving all accepted v003 body and head morphology.

This time, do **not** rely on subtle procedural swelling, smoothing, or surface displacement alone if that cannot solve the structural problem.

If the existing local mesh prevents believable anatomy, **local hand/foot topology reconstruction is authorized at the anatomical-source level**.

That may include:
- replacing local digit patches;
- local remeshing/resampling of hands or feet;
- rebuilding finger/toe root topology;
- rebuilding nail-bed regions;
- rebuilding web spaces;
- rebuilding thumb-root topology;
- reprojecting/rejoining the rebuilt local patch to the frozen limb source.

It must remain one coherent watertight body at the end.

This authorization is **extremity-local only**. It is not permission for whole-body remeshing or production retopology.

## 3. HARD FREEZE — do not alter accepted anatomy

Freeze these v003 regions unless tiny seam blending is mathematically required:

- cranium;
- face;
- eye/brow region;
- ears;
- neck;
- shoulders;
- chest;
- ribcage;
- abdomen;
- waist;
- pelvis;
- glutes;
- thighs;
- knees;
- calves;
- global ankle position;
- arm length;
- forearm mass;
- overall hand scale;
- overall foot scale;
- overall body silhouette;
- 218 cm stature.

The v003 eye correction is accepted. **Do not touch the eyes again.**

The v003 ears are accepted. **Do not touch the ears again.**

No global smoothing.
No silhouette retarget.
No torso/body sculpting.
No facial refinement.

## 4. Hand anatomy target

The hand must remain recognizably Grask:
- large;
- broad;
- powerful;
- long-fingered;
- capable of tools, weapons, climbing, and fine enough manipulation;
- heavier than a human hand without becoming paw-like or monstrous.

It must not be a scaled-up human hand, but its functional joint architecture must still be believable.

### 4.1 Palm / metacarpal block

Required:
- broad but not mitten-like palm;
- clear metacarpal fan from wrist toward digit roots;
- believable dorsal hand plane;
- coherent palm thickness;
- thenar and hypothenar masses;
- first web space between thumb/index;
- wrist transition that supports grip mechanics.

The palm must not melt directly into the fingers.

### 4.2 Finger roots and web spaces

The current v003 root zones are too soft.

Rebuild as needed so that:
- each finger has a distinct root;
- web spaces form natural valleys between digits;
- roots are not circular tubes punched into the palm;
- interdigital webs terminate before the proximal phalanx midpoint;
- web depth differs subtly between index-middle, middle-ring, and ring-pinky;
- no fused or scalloped mitten appearance remains.

### 4.3 Finger length hierarchy

Preserve Grask heaviness, but use a coherent hierarchy:

- middle = longest;
- ring = slightly shorter or near middle;
- index = slightly shorter than ring/middle;
- pinky = clearly shortest;
- thumb reaches approximately toward the proximal-index region when relaxed.

Do not create identical-length fingers.

Do not create spindly digits.

### 4.4 Phalange construction

Each non-thumb finger must visibly read as:
- proximal phalanx;
- middle phalanx;
- distal phalanx.

Each thumb must visibly read as:
- proximal phalanx;
- distal phalanx.

Joint locations must be readable through:
- subtle change in cross-section;
- joint width;
- dorsal knuckle plane;
- palmar crease/hinge;
- change in finger direction.

Do not use simple cylindrical bending.

### 4.5 Neutral hand pose

The current hook-like tube curvature is not acceptable.

Use a natural neutral/rest pose:
- slight MCP flexion;
- modest PIP/DIP flexion;
- fingers relaxed rather than claw-curled;
- ring/pinky can curl slightly more than index/middle;
- fingers should not collide;
- palm must remain readable;
- silhouette must support later rigging.

The hand should look capable of opening fully and closing into a fist.

### 4.6 Fingertips

Required:
- broad distal pad;
- flattened/rounded dorsal tip;
- slight asymmetry between nail side and pad side;
- no spherical bulbs;
- no pointed claws.

### 4.7 Fingernails

Grask currently uses **ordinary nails, not claws**.

Required:
- visible nail plate on all five digits;
- clear proximal nail fold;
- lateral nail grooves;
- distal free edge;
- nail follows distal phalanx curvature;
- nail width proportional to fingertip, not tiny human cosmetic nails and not oversized talons.

Nails must be clearly visible in neutral clay close-up lighting.

If a nail bed exists geometrically but cannot be visually verified in the evidence, it does not pass.

### 4.8 Thumb

Mandatory:
- strong thenar base;
- anatomically convincing root;
- oppositional angle;
- clear MCP/IP structure;
- readable nail;
- no dangling cone;
- no hook or claw shape.

## 5. Foot anatomy target

The overall v003 foot size, length, width family, heel, arch, and plantigrade stance are accepted.

Do not resize the feet.

The goal is to reconstruct the **forefoot and toes**.

### 5.1 Forefoot

Required:
- broad load-bearing ball;
- distinct hallux side and lateral forefoot side;
- MTP region visible as structure, not a smooth blob;
- coherent transition from metatarsals into toe roots;
- natural toe splay.

### 5.2 Toe hierarchy

Required:
- hallux clearly dominant;
- second toe substantial but smaller;
- third/fourth progressively smaller;
- fifth clearly smallest;
- coherent descending arc across the forefoot.

Do not produce five equal round pads.

### 5.3 Toe roots / web spaces

Rebuild if needed so that:
- each toe has a distinct root;
- interdigital gaps are visible;
- no fused blob mass;
- webbing is natural and shallow;
- transition into forefoot remains strong and weight-bearing.

### 5.4 Toe phalanges

Hallux:
- proximal and distal structure.

Lesser toes:
- proximal/middle/distal structure may be simplified for species mass, but joint rhythm must read.

Use:
- joint cross-section changes;
- subtle dorsal articulation;
- toe-side planes;
- plantar pad transitions.

Avoid:
- sausage toes;
- round marbles;
- paw beans;
- claws.

### 5.5 Toe tips / plantar pads

Required:
- flattened load-bearing underside;
- rounded but not spherical tip;
- coherent plantar pad;
- toe tips should contact or nearly contact the ground naturally in neutral stance.

### 5.6 Toenails

Required:
- visible nail plates;
- proximal folds;
- lateral grooves;
- sensible width/length;
- no claw point;
- no tiny barely visible nail beds.

The nail plate must be visible in the evidence without relying on labels.

## 6. Anatomical-source topology permission

Because v003 showed that surface-only refinement is reaching its limit, Claude may reconstruct the local source topology.

Allowed:
- local remesh of hands;
- local remesh of forefoot/toes;
- local patch replacement;
- local projection to v003 frozen extremity envelope;
- topology surgery at finger/toe roots;
- local subdivision where needed;
- hand-authored or algorithm-assisted local reconstruction.

Not allowed:
- whole-body remesh;
- changing accepted body morphology;
- production retopology;
- changing limb proportions;
- changing hand/foot global scale;
- regenerating the entire body.

The priority is **anatomy quality**, not preserving v003 vertex IDs inside the extremities.

## 7. Shape-language rule

The extremities should feel like they belong to the same creature as the accepted body.

Use:
- broad structural planes;
- heavy joint mass;
- thick but articulated digits;
- grounded biological transitions;
- restrained fantasy exaggeration.

Avoid:
- human fashion-model hands/feet;
- ape hands;
- paws;
- claws;
- alien tubes;
- cartoon squash/stretch;
- bodybuilder vascularity.

## 8. Functional sanity checks

Hands must plausibly support:
- sword grip;
- axe/hammer grip;
- two-handed weapon grip;
- shield grip;
- open relaxed pose;
- fist closure;
- finger extension without obvious collision.

Feet must plausibly support:
- standing;
- walking;
- running;
- crouching;
- toe-off;
- balance on uneven terrain.

No rig is required yet, but static anatomy must not preclude these motions.

## 9. Mandatory visual gate — much stricter than v003

Claude must **not** self-pass based on numerical topology cleanliness alone.

The close-up images are the primary gate.

### Hands fail if any of these remain:
- fingers read as tubes;
- fingers curve like hooks without joint structure;
- root/web anatomy looks melted;
- knuckles are not structurally readable;
- fingertips look bulbous;
- nails cannot be seen;
- thumb looks detached, conical, or mechanically planted;
- hand would not plausibly open/close.

### Feet fail if any of these remain:
- toes look like rounded blobs;
- toe bases are fused;
- toe hierarchy is unclear;
- nail plates cannot be seen;
- forefoot has no MTP structure;
- hallux is not distinct;
- toes read as paw pads.

If any visual failure remains, continue internally.

Do not turn in a “technically clean but visually weak” result.

## 10. Technical gate

Final v004 source must have:

- 1 intended connected body;
- 0 boundary edges;
- 0 non-manifold edges;
- genus 0;
- 0 degenerate faces;
- 0 duplicate/coincident geometry;
- outward consistent normals;
- 0 catastrophic self-intersections;
- no floating geometry;
- no duplicate shells;
- no local remesh seam;
- no accidental holes;
- height **218.000 cm** within negligible tolerance.

Report:
- V/F count;
- bbox;
- height;
- topology stats;
- SI result;
- source/output hashes;
- hand/foot reconstruction method;
- exact regions replaced/rebuilt;
- movement relative to v003;
- proof frozen body stayed fixed.

## 11. Required evidence

### A. Whole-body regression v003 vs v004
Identical cameras:
- front;
- profile;
- back;
- 3/4 front;
- 3/4 back.

Purpose: prove only extremities changed.

### B. HANDS — v003 vs v004
Large close-ups with identical cameras:
- palm;
- dorsal;
- 3/4;
- outer/ulnar;
- thumb root;
- thumb profile;
- index finger side;
- middle finger side;
- MCP row close;
- PIP/DIP close;
- fingertip close;
- fingernail close;
- web-space close.

Also provide:
- relaxed hand silhouette;
- hand opened flatter;
- approximate fist preview or posed diagnostic if possible without rigging.

The goal is to prove the structure would function, not to create a final pose library.

### C. FEET — v003 vs v004
Large close-ups with identical cameras:
- top/front;
- outer side;
- inner side;
- 3/4;
- heel;
- sole;
- forefoot close;
- hallux close;
- lesser-toe close;
- toe-root/web close;
- toenail close;
- ground-contact side view.

### D. Extremity topology diagnostic
For hands and feet:
- wireframe close-ups;
- edge density;
- local reconstruction seams if any;
- no hidden folds/duplicate surfaces.

### E. Freeze proof
Numerical and visual proof that:
- head unchanged;
- eye correction unchanged;
- ears unchanged;
- torso/pelvis/back unchanged;
- limb lengths unchanged;
- stature unchanged.

## 12. Internal review checklist

Claude must explicitly PASS all of the following:

### Hands
1. palm/metacarpal structure coherent;
2. five digit roots distinct;
3. web spaces natural;
4. finger-length hierarchy coherent;
5. MCP/PIP/DIP structure readable;
6. neutral finger pose is relaxed, not hook-like;
7. fingertips structured, not bulbous;
8. nails visibly readable;
9. thumb root/thenar/opposition coherent;
10. hand remains large and Grask-like;
11. hand plausibly opens/closes/grips.

### Feet
12. forefoot structurally load-bearing;
13. hallux distinct;
14. lesser-toe hierarchy coherent;
15. toe roots/webs distinct;
16. phalange rhythm readable;
17. plantar pads grounded;
18. toenails visibly readable;
19. toes no longer blob-like;
20. overall foot scale and stance preserved.

### Frozen source
21. body/head/eyes/ears did not regress;
22. 218 cm stature preserved;
23. all technical mesh gates pass.

If any item fails, keep working.

## 13. Deliverables

Create:

`GR_U_REF_RP2_SOURCE_3D_v004.blend`

Export:
`GR_U_REF_RP2_SOURCE_3D_v004.glb`

Final report:

`reviews/claude-rac-rp2-grask-3d-source-v004-extremity-reconstruction-final-gate.md`

Evidence:

`reviews/rac-rp2-evidence/grask_3d_source_v004_extremity_reconstruction/`

Update:
- `reviews/claude-session-handoff.md`
- `specs/STATUS.md`

Preserve v001-v003 sources unchanged.

## 14. Stop rule

Do not start production retopology.
Do not create RP2 production v007.
Do not rig.
Do not create creator morphs.
Do not start another race.

After the complete source passes both visual and technical gates, return exactly:

**RP2 GRASK 3D ANATOMICAL SOURCE V004 EXTREMITY RECONSTRUCTION PASS / READY FOR AUTHOR FREEZE REVIEW**

Then STOP for Tyler review.

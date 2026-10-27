# RAC RP3 — Fenn CF2 acceptance + production ear-branch prototype order

**Date:** 2026-10-27  
**Authority:** Tyler / ChatGPT review of Claude Fenn craniofacial return `582d683590ba1b81cfd3ec16101dbd3399ac08c6`.  
**Parent gate:** `reviews/claude-rac-rp3-fenn-craniofacial-source-gate.md`.  
**Program references:**  
- `specs/fenn/FENN_V1.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- active MPFB Family Base v005;  
- `reviews/rac-rp3-evidence/fenn_craniofacial_v001/ear_branch_prep/FENN_EAR_BRANCH_PREP.md`;  
- W1e `FN-elven` evidence parameters.

This order formally accepts **CF2** as the canonical central Fenn craniofacial direction and authorizes the first production-quality **Fenn external-ear topology branch prototype**.

The body, hidden-ear identity and craniofacial direction are now locked for this stage.

Do not freeze final Fenn production bodies in this order.  
Do not start Aelari, Vael or Halvren.

---

# 1. AUTHOR DECISION — CF2 ACCEPTED

Accept **CF2** as the canonical central Fenn craniofacial source direction for both configurations.

CF2 is selected because:

- hidden-ear facial identity passes on all 6 canon systems;
- the orbit remains Fenn but no longer carries the identity alone;
- c1/c2 normalized identity strength is consistent;
- CF1 is too borderline;
- CF3 is stronger/stylized beyond what is needed for the central reference;
- no craniofacial topology branch is required.

Accepted CF2 target architecture:

| Target | CF2 value |
|---|---:|
| `head-oval` | 0.12 |
| `head-scale-horiz-decr` | 0.145 |
| `head-scale-vert-incr` | 0.07 |
| `head-scale-depth-decr` | 0.60 |
| `LR:cheek-trans-up` | 0.60 |
| `LR:cheek-inner-decr` | 0.25 |
| `LR:cheek-volume-decr` | 0.32 |
| `chin-bones-decr` | 0.60 |
| `chin-height-decr` | 0.14 |

Preserve the pre-existing accepted Fenn orbit / eye targets.

Do not use CF1 or CF3 as central references.

They remain evidence for valid directional range only; they are not frozen creator extrema.

---

# 2. Fenn source status after CF2 acceptance

Update the Fenn reference records so that:

### Configuration 1
The accepted Fenn body reference remains rooted in `FNL4`, with **CF2 craniofacial revision accepted**.

### Configuration 2
The accepted Fenn body reference remains rooted in `FNF181`, with **CF2 craniofacial revision accepted**.

Do not overwrite the original historical source assets in a way that destroys provenance.

Create versioned accepted craniofacial source records / R-6 assets, e.g.:

- `FNL4-CF2`
- `FNF181-CF2`

or project-consistent equivalents.

Record the provenance:

> original accepted body source + CF2 deterministic MPFB target set = accepted Fenn craniofacial central source.

The final Fenn reference is still **not completely frozen** until the external-ear branch is selected.

---

# 3. CF2 facial-rig carry-forward item

Do not reopen CF2 geometry for the generic MPFB expression-unit mouth-corner behavior.

Record a Fenn-specific rig-stage carry-forward item:

### Configuration 2 CF2
Generic diagnostic expression units:
- smile: +6 self-intersection pairs vs current source, while flipped-face count improves;
- sadness: +10 self-intersection pairs and +12 flipped faces;
- location: existing mouth-corner fold region.

Classification:

**FACIAL RIG / MOUTH-CORNER CORRECTIVE CARRY-FORWARD**

Reason:
- source already folds there;
- CF strength scales the generic expression-unit issue;
- neutral/rest geometry is clean;
- topology and UFCA readiness pass;
- other expression metrics are equal or improved.

No production facial weights/correctives in RP3.

---

# 4. Hidden-ear identity is now accepted

Record:

- hidden-ear **body identity** = PASS;
- hidden-ear **facial identity with CF2** = PASS.

This becomes a Fenn hard-reference condition.

The external ears are not allowed to compensate for a future regression in body/head identity.

For any future Fenn source change:
- rerun hidden-ear body + face comparison;
- failure reopens the changed source, not the ear branch.

---

# 5. External-ear branch authority

Authorize a **Fenn-only local production topology branch** from active MPFB Family Base v005.

This is a legitimate contract branch.

The external ears are part of the body mesh and must become real Fenn anatomy.

The branch is restricted to:

- existing ear zone;
- existing 52-vertex root loop per side;
- at most one bounded transition ring outside the root where technically needed.

No change to:
- face;
- orbit;
- scalp outside branch transition;
- neck;
- body;
- hands;
- feet;
- active family topology elsewhere.

---

# 6. Root / branch architecture

Use the prepared region:

Per side:
- existing ear-zone faces: 1,206;
- existing ear-zone vertices: 1,233;
- root boundary: one closed **52-vertex loop**;
- current bounding box approx. 1.89 × 3.88 × 5.65 cm.

Branch construction principles:

1. keep the 52 root vertices as the attachment interface where practical;
2. preserve their family mapping rows;
3. replace the interior human-auricle region with one all-quad Fenn ear patch;
4. use one identical topology for:
   - c1;
   - c2;
   - E1;
   - E2;
   - E3;
5. record an explicit active-v005 → Fenn-ear-branch mapping;
6. maintain deterministic root-frame construction.

The branch topology must support later creator variation without requiring a new topology.

---

# 7. Production ear anatomy requirements

The Fenn ear must be a coherent external ear, not a human ear with an extruded point.

Required anatomical systems:

- root attachment;
- helix;
- antihelix stem;
- superior/inferior crura;
- triangular fossa;
- concha:
  - cymba;
  - cavum;
- crus of helix relationship;
- tragus;
- antitragus;
- intertragic notch;
- lobe;
- upper extension;
- natural taper into the point.

The point must emerge from the whole upper-ear structure.

No “knife blade” point.  
No paper-thin stretched auricle.  
No decorative fantasy fin.

---

# 8. Shared ear topology design targets

The topology must be suitable for future controls in `FENN_V1.md`:

- overall length;
- base width;
- tip length;
- tip sharpness;
- vertical angle;
- forward/back sweep;
- lateral projection;
- upper-ear curvature;
- lobe size;
- lobe attachment;
- subtle natural asymmetry later.

Topology must therefore provide clean deformation flow around:

- root;
- helix rim;
- antihelix/crura;
- concha;
- tragus/lobe complex;
- upper extension;
- tip transition.

Do not implement creator morphs yet.

---

# 9. Density / topology quality

Target approximately **1.5–2× the current ear-zone face count**, only if needed to express the structures cleanly.

Do not densify blindly.

Hard requirements:

- 100% quads;
- one connected body mesh;
- no boundary at branch seam;
- no non-manifold edges/vertices;
- no degenerate faces;
- outward normals;
- no self-intersection;
- clean root continuity;
- ear mean edge / stature <= 0.25%;
- no severe slivers;
- no new branch quad with aspect > 10;
- preferred local aspect <= 6 where practical;
- T-4 local quality reported.

Topology should be dense enough for anatomy, not “film mesh” dense.

---

# 10. E1 / E2 / E3 geometry candidates — one topology

Build all three on the **same branch topology**.

## E1 — restrained
Target:
- length ~7.6 cm at reference scale;
- projection ~42°;
- tilt ~28°;
- sweep ~1.2 cm;
- base half-width ~1.75 cm.

Intent:
- shortest / least projected central-valid candidate;
- still clearly Fenn;
- full non-human anatomy.

## E2 — balanced central
Use the W1e `FN-elven` reference as the principal shape guide:

- length **8.6 cm**;
- max half-width **1.80 cm**;
- projection **50°**;
- tilt **32°**;
- sweep **1.6 cm**;
- lobe fraction **0.15**;
- thickness around **0.26–0.28 cm**;
- Y-shaped antihelix;
- cymba/cavum;
- tragus/antitragus;
- continuous taper.

**E2 is the provisional recommended central candidate, not pre-selected.**

## E3 — stronger
Target:
- length ~9.4 cm;
- projection ~55°;
- tilt ~35°;
- sweep ~1.9 cm;
- base half-width ~1.85 cm.

Intent:
- stronger but still plausible Fenn central-population anatomy;
- not creator maximum;
- not an Aelari proxy.

---

# 11. Configuration sharing

For c1 and c2:

- topology must be identical;
- vertex count must be identical;
- face list identical;
- branch map identical;
- structural parameterization identical.

Geometry may adapt through the same root-frame construction to each accepted CF2 head.

Do not create sex/config-specific ear topology.

Do not encode mandatory sex dimorphism in ear size or shape.

---

# 12. Ear-root source relationship

The current human auricle is non-final and should not constrain the distal Fenn ear.

However:

- root attachment to skull must remain anatomically continuous;
- transition into temple/scalp must be smooth;
- no visible seam;
- no root floating;
- no root burial;
- no head-shape regression outside the branch zone.

Audit source deviation primarily at:
- root loop;
- transition ring;
- immediately adjacent skull.

Do not demand distal Fenn ear vertices match the obsolete human ear.

---

# 13. Static deformation-readiness

No final ear rig.

Run bounded diagnostics:

### Head/neck
- neck flex;
- neck extension if available;
- head yaw left/right;
- head pitch;
- head roll if available.

Check:
- root does not collapse;
- ear does not intersect skull/neck;
- no branch seam opens;
- no root inversion.

### Ear-shape readiness
Use geometry-only bounded probes to verify topology can support future:
- increased/decreased projection;
- upward/downward angle;
- forward/back sweep;
- length;
- tip sharpness.

These are not production morphs.

The purpose is topology readiness.

---

# 14. Craniofacial regression with ears

For every E candidate:

- CF2 face must remain byte/geometry unchanged outside the branch;
- hidden-ear CF2 identity must remain PASS;
- visible-ear Fenn must look anatomically coherent with the selected CF2 skull.

Check that ear placement does not make the head read:
- too childlike;
- cartoonishly wide;
- horn-like;
- animal-like;
- “human with pasted-on elf ears.”

---

# 15. Elven-family firewall

Do not make Fenn ears the universal elf ear.

Fenn-specific identity:
- greatest average lateral projection among Fenn/Aelari/Vael;
- forest/wood-elf anatomical read;
- substantial individual overlap remains possible.

Do not pre-author Aelari or Vael ear geometry.

However, document which topology features appear potentially reusable for later elf branches:
- root interface;
- structural loops;
- helix/antihelix topology;
- tip-support architecture.

This is only a reuse note, not an elf-family freeze.

---

# 16. Visual author package

Provide high-resolution identical-camera sheets for c1 and c2.

Required:

1. E1/E2/E3 front;
2. rear;
3. profile;
4. 3/4 front;
5. 3/4 rear;
6. top;
7. close ear profile;
8. close rear ear;
9. root closeup;
10. wireframe;
11. pole/valence map;
12. helix/antihelix/concha annotated anatomy;
13. thickness / sectional views;
14. T-4 / aspect heatmap;
15. density heatmap;
16. root-deviation heatmap;
17. CF2 head with E1/E2/E3;
18. c1 vs c2 E2;
19. hidden-ear CF2 confirmation;
20. static neck/head deformation-readiness sheet.

Use true scale.

---

# 17. Candidate scoring

Score E1/E2/E3 on:

- Fenn biological identity;
- anatomical coherence;
- root integration;
- natural taper;
- internal-ear readability;
- silhouette;
- no caricature;
- future creator-control support;
- topology quality;
- c1/c2 consistency.

Do not choose solely from dimensions.

Return a recommendation:
- E1;
- E2;
- E3;
or
- NEEDS AUTHOR SELECTION if aesthetic tradeoffs are genuinely balanced.

---

# 18. Acceptance logic

Return exactly one:

## FENN EAR BRANCH PASS — E2 RECOMMENDED
Use if E2 is clearly the best balanced central reference and all technical gates pass.

## FENN EAR BRANCH PASS — E1 RECOMMENDED

## FENN EAR BRANCH PASS — E3 RECOMMENDED

## FENN EAR BRANCH PASS — NEEDS AUTHOR SELECTION
Use if more than one candidate is technically/canon valid with a material aesthetic tradeoff.

## FENN EAR BRANCH NEEDS TOPOLOGY REVISION
Use if one shared topology cannot cleanly express all required anatomy or c1/c2.

## FAIL
Use for a blocking integrity/source problem.

Do not freeze whichever candidate wins.

---

# 19. If a candidate passes

Prepare, but do not execute, the final Fenn consolidation plan:

- accepted Fenn body reference;
- accepted CF2 craniofacial source;
- selected ear branch candidate;
- branch map;
- final production realization naming;
- final validation/freeze checklist.

The next ChatGPT order will either:
- select an ear candidate;
- request one bounded refinement;
- or authorize final Fenn consolidation/freeze.

---

# 20. Required return

Commit:

1. `reviews/claude-rac-rp3-fenn-ear-branch-gate.md`;
2. finalized Fenn ear branch topology definition;
3. active-v005 → Fenn-ear-branch mapping;
4. E1/E2/E3 branch geometry for c1/c2;
5. sidecars/manifests;
6. integrity audit;
7. T-4 / aspect audit;
8. density audit;
9. root-deviation audit;
10. static deformation-readiness audit;
11. CF2 regression proof;
12. visual sheets;
13. candidate scoring/recommendation;
14. final-consolidation preparation note;
15. immutable family/source hash proof;
16. narrow `specs/STATUS.md` update;
17. session handoff.

The gate must explicitly answer:

- Is CF2 now recorded as the accepted Fenn central craniofacial direction?
- Is the CF2 facial-rig carry-forward recorded?
- Was one shared Fenn ear topology built?
- Do c1/c2 and E1/E2/E3 share it exactly?
- Does it contain the required external-ear anatomy rather than a stretched human ear?
- Do integrity, T-4 and density pass?
- Is root integration clean?
- Is static deformation-readiness acceptable?
- Does hidden-ear identity remain PASS?
- Which E candidate is recommended?
- Is any topology refinement still needed?
- Is Fenn ready for final consolidation after author selection?

---

# 21. Stop rules

After committing the ear-branch gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Fenn;
- start Aelari;
- start Vael;
- start Halvren;
- declare a universal elf ear topology;
- modify active MPFB Family Base v005;
- finalize production ear rigging;
- implement creator morphs;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- CF2 is accepted as the canonical central Fenn craniofacial direction.
- The configuration-2 mouth-corner expression issue is a facial-rig carry-forward, not a source/topology blocker.
- Hidden-ear Fenn body and facial identity are accepted.
- The next work is the real Fenn external-ear production topology branch.
- Build E1/E2/E3 on one shared topology.
- E2/W1e is the provisional central recommendation, but it must earn final selection visually and technically.
- Do not freeze Fenn without ChatGPT review.

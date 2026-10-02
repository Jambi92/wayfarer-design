# Saurin — Rodin Geometry Adoption Directive

**Date:** 2026-10-02
**Author:** ChatGPT
**For:** Claude
**Status:** AUTHOR DIRECTIVE — supersedes the Phase A reconstruction approach in `reviews/saurin-post-rodin-master-anatomy-directive.md`.

## Decision

Tyler and ChatGPT reject the post-Rodin Phase A axial blockout as a visual/anatomical direction. **Stop work on that model. Do not refine it and do not use it as the foundation for Phase B.**

The failure was methodological: the directive over-constrained the problem into an abstract biomechanical reconstruction and discarded the sculptural/anatomical quality already present in the Rodin source.

We are changing methods.

## New strategy

**Use the strongest actual Rodin full-body geometry as the sculptural foundation, then surgically correct the regions that conflict with Wayfarer canon.**

Rodin is not thereby declared canonical. The authority remains:
1. Approved Wayfarer design specification;
2. decision register;
3. approved authored directives;
4. working/reference geometry.

The distinction is:

- **Rodin = sculptural source / starting geometry**
- **Wayfarer spec = biological and design authority**

Do not rebuild from primitive procedural volumes merely to reproduce anatomy that Rodin already represents better.

## Immediate task: source-body selection and extraction

Return to the original Rodin `base.obj` already analyzed.

From the five full-body components B1–B5, identify the best actual geometry to serve as the primary Saurin source body.

Prioritize:
- overall silhouette;
- convincing reptilian humanoid read;
- anatomical sophistication;
- usable torso/limb topology/geometry;
- useful tail geometry where present;
- minimal generation corruption;
- compatibility with the accepted Saurin head/body direction.

Do **not** choose solely because a candidate already matches every canonical detail. Problem regions will be corrected.

B2 and B5 deserve particular attention because they contain tails, but select based on the actual geometry. If the strongest solution is a hybrid—e.g. one body's torso/limbs plus another body's tail or a part-study region—document that explicitly.

## Preserve what is working

The goal is to retain as much of the convincing Rodin sculpt as possible, including where useful:
- mature athletic/non-human silhouette;
- integrated anatomical surface sophistication;
- convincing limb mass and taper;
- hands/digits and distal articulation;
- lower-leg structure;
- useful thoracic volume;
- reptilian planar character;
- tail taper and curvature concepts;
- overall visual quality that Tyler responded positively to.

Do not flatten these into generic tubes, capsules or primitive masses.

## Surgical correction zones

After isolating the source body, identify and mask the regions requiring redesign.

### Pelvis / sacrum / tail root
This remains the highest-priority correction.

Remove the human gluteal construction and conventional gluteal cleft. Rebuild the posterior pelvis around a sacral/caudal platform and substantial proximal tail base.

The tail must become an anatomical continuation of the axial system rather than emerging between human buttocks.

Preserve good Rodin tail taper/curvature where possible; rebuild the root.

### Crotch
Remove human male genital/crotch presentation. Reproductive anatomy remains OPEN. Use neutral transitional anatomy without inventing a reproductive solution.

### Torso
Preserve useful thoracic depth and silhouette, but replace:
- human pectoral plates;
- rectus six-pack ladder;
- navel;
- bodybuilder-specific muscle exaggeration where it defines the race.

Do **not** erase anatomical sophistication. Translate it into continuous Saurin load paths and non-human ventral/lateral organization.

### Neck
Preserve convincing mass and reptilian read where useful, but correct human SCM/trapezius patterns. Integrate the accepted Saurin head into a cervical system that belongs to the thoracic shell.

### Head
The accepted Saurin cranial direction remains authoritative. Do not replace it simply because the Rodin body's generated head differs.

If necessary, transplant/fit the accepted head onto the selected Rodin-derived body and rebuild the junction.

### Feet
Rodin's giant feet are not the final proportion. Reduce/reconstruct toward approximately 0.16–0.18H as an investigative target while preserving:
- plantigrade stance;
- rearfoot → midfoot → metatarsal spread;
- long articulated toes;
- claws;
- non-mammalian contact anatomy.

No paw pads.

### Hands
Preserve the useful Rodin hand/digit architecture where possible. Maintain five digits and opposable thumb provisionally, with tapered articulated digits and claw continuation.

## Tail length

Canonical neutral tail range remains ~0.55–0.80 standing height. For the neutral source/master, target approximately 0.65–0.70H unless a documented anatomical reason supports another value.

If the selected Rodin tail is too short, extend it while preserving its taper and sectional logic rather than replacing it with a primitive tube.

## What NOT to do

- Do not continue the rejected Phase A blockout.
- Do not start from capsules, metaballs, SDF primitives or generic procedural body volumes if the Rodin geometry can be reused.
- Do not recreate the whole body from scratch just to satisfy measurements.
- Do not convert the Rodin source into a human base mesh plus reptilian additions.
- Do not polish known human-anatomy conflicts instead of correcting them.
- Do not treat every Rodin flaw as reason to discard the surrounding good geometry.
- Do not make a new beauty render before showing the actual extracted source and planned correction zones.

## Required next deliverable — BEFORE sculpt correction

Do **not** modify the source body yet.

First produce a **Rodin Source Adoption Sheet** containing:

1. The selected primary full-body component, isolated from the reference sheet.
2. Front, profile, rear, front 3/4 and rear 3/4 orthographic renders of that exact extracted geometry.
3. If a hybrid source is recommended, the donor components/part studies shown separately.
4. A visual correction map on the body using clear region labels:
   - PRESERVE;
   - MODIFY;
   - REBUILD;
   - REPLACE.
5. A short table explaining every marked region.
6. Exact statement of which original Rodin component IDs will be used.
7. Confirmation that the rejected Phase A model contributes **no body geometry** to this new route.
8. Proposed geometry-edit sequence that maximizes preservation of the Rodin sculpt.

Tyler and ChatGPT will review this adoption sheet before Claude alters the mesh.

## Success criterion

The question is no longer:

> Can we procedurally prove a theoretical Saurin axial architecture from primitives?

It is:

> Can we preserve the convincing Saurin already present in Rodin while correcting only the anatomy that contradicts Wayfarer canon?

That is the new route.

**Proceed only through the Rodin Source Adoption Sheet. Do not begin corrective sculpting until reviewed.**

# Saurin Rodin OBJ — Geometry Analysis Handoff to Claude

**Date:** 2026-10-02  
**Author:** ChatGPT  
**Status:** Diagnostic input only — NOT canonical anatomy, NOT approved implementation geometry.

## Tyler's instruction

Tyler supplied a Rodin Gen-2 OBJ generated from the Saurin anatomical target. ChatGPT inspected the actual OBJ rather than relying on the poster preview.

## Critical discovery

The OBJ is **not one assembled production character**. It is a spatially arranged 3D anatomical/reference sheet containing many generated Saurin bodies and body-part studies.

Direct inspection:
- ~798,968 vertices
- 1,000,000 triangles
- bounds approximately X -0.943..0.948, Y 0..1.144, Z -0.214..0.206

Therefore **DO NOT import this asset and treat it as a ready Saurin base mesh**.

## How Claude should use the OBJ

Use the OBJ as a **3D anatomical concept library** and measurement/reference source. Its value is that it contains real 3D depth and multiple interpretations of:
- complete body silhouette;
- thorax;
- lower axial trunk;
- pelvis / sacrum;
- pelvis-to-femur transition;
- tail root and tail taper;
- neck-to-thorax transition;
- limbs;
- hands;
- feet;
- head/neck.

The Wayfarer canonical Saurin specification remains the authority. Rodin geometry is evidence/reference only. Reject any Rodin feature that conflicts with the approved spec or Tyler's visual direction.

## Why this matters

The previous TS7–TS9 procedural work repeatedly retained a human-body scaffold and then decorated/reorganized it. Tyler specifically rejected that approach. The successful head work improved only after the problem was treated as a clean non-human structural design.

The body must now receive the same treatment.

The target is **not**:
human anatomy + scales + tail + reptile head.

The target is:
a coherent upright reptilian humanoid organism whose thorax, axial trunk, pelvis, sacrum, femora and tail are designed as one continuous biomechanical architecture.

## Required next workflow

Do **not** immediately produce TS10 from the OBJ.

First perform a geometry-analysis pass:

1. Load Tyler's supplied `base.obj`.
2. Identify connected components / spatial clusters.
3. Determine which clusters are full bodies and which are anatomical studies.
4. Isolate the strongest candidate geometry for each diagnostic region.
5. Render candidate regions orthographically from front, profile, rear, front 3/4 and rear 3/4 where applicable.
6. Measure normalized structural relationships rather than copying absolute Rodin coordinates.
7. Compare each measurement and form against `specs/saurin/SAURIN_V1.md`.
8. Label each observed Rodin feature:
   - KEEP / useful reference;
   - MODIFY / useful concept but incorrect execution;
   - REJECT / generation artifact or incompatible anatomy;
   - UNRESOLVED.
9. Only after this analysis should a new reconstruction be proposed.

## Highest-priority anatomical questions

### 1. Thorax
Measure width, depth, vertical contribution, sternum/ventral plane, costal transition and shoulder relationship.

We need a distinctly non-human structural shell without merely exaggerating human pectorals/ribs.

### 2. Lower axial trunk
The Saurin specification calls for an elongated lower axial trunk. Determine how the Rodin geometry creates length and planar transitions without falling back to a human waist/abdominal cylinder.

### 3. Pelvis / sacrum / tail root
This is the most important area.

Inspect the Rodin model for useful solutions to:
- posterior pelvic depth;
- sacral platform;
- caudal base location;
- tail-root cross-section;
- transition from axial trunk into pelvis and caudal mass;
- femoral placement around the caudal system.

The tail must look **biologically inevitable**, not attached to a humanoid butt.

Do not preserve:
- human gluteal cleft;
- human buttock construction;
- genital-looking anterior tail artifacts;
- tail emerging as a tube glued onto the sacrum.

### 4. Femur / hip
Determine whether the Rodin geometry provides a better non-human pelvic-femoral relationship than TS9.

The legs must remain capable of credible upright bipedal locomotion while belonging to the Saurin pelvic system.

### 5. Neck / shoulder / thoracic inlet
Avoid a human trapezius/neck cylinder transition. The accepted head should connect into a reptilian cervical system and deep thoracic shell.

### 6. Surface planes and rigidity
Tyler repeatedly identified excessive roundness as a failure.

The body needs clearer reptilian structural planes, sharper transitions, ridges and changes of direction where anatomically justified. This does **not** mean random spikes or armor plates. The angularity must arise from underlying structure.

### 7. Tail phenotype
Tail remains mandatory and highly customizable.

Preserve relationship-aware variation in:
- total length;
- base width/depth;
- proximal mass;
- taper rate;
- cross-sectional character;
- segment curvature;
- resting curvature;
- restrained dorsal keratin/ridge expression;
- inherited patterning.

Base size × length × mass × pelvic support must remain coupled.

No phenotype automatically grants attacks, swimming, balance, climbing, reach or other gameplay advantages.

## Important rejection criteria

Reject a candidate even if aesthetically attractive when:
- removing the tail reveals an ordinary human pelvis;
- the torso reads as a human athletic body with altered surface relief;
- the gluteal region forms recognizable human buttocks/cleft;
- the tail root looks appended;
- the neck is a human cylinder with reptile head attached;
- chest architecture is dominated by human pectoral anatomy;
- abdominal anatomy is a human six-pack;
- surface ridges are merely decorative rather than structural;
- feet/hands become generic monster claws without approved anatomy;
- sex anatomy is inferred from human defaults;
- silhouette depends entirely on tail/head to distinguish the race.

## Measurement output requested before reconstruction

Create a diagnostic report containing normalized ratios where reliable, preferably using standing height or another explicitly named reference dimension:
- head height / standing height;
- cervical length / standing height;
- shoulder breadth / standing height;
- thoracic width and depth;
- thoracic vertical contribution;
- lower axial trunk contribution;
- pelvic breadth/depth;
- hip-joint spacing;
- tail-base width/depth;
- tail length / standing height;
- tail-base area relative to pelvis;
- femur/tibia contribution;
- arm/forearm contribution;
- hand and foot proportions;
- major sagittal offsets among head, thorax, pelvis, hip and caudal base.

If the Rodin sheet arrangement makes a measurement unreliable, say so. **Do not fabricate precision.**

## Authority

Rodin does not override the spec.

Authority remains:
1. Approved Wayfarer Design Specification
2. Open Decision Register
3. Prototype / diagnostic geometry

The OBJ is below all three as an exploratory reference source.

## Deliverables requested from Claude

Before another body-generation iteration, return:
1. component/cluster inventory;
2. isolated orthographic reference renders;
3. measurement table;
4. KEEP / MODIFY / REJECT / UNRESOLVED anatomy table;
5. explicit comparison to the canonical Saurin spec;
6. proposed reconstruction plan for the next pass.

Do not call the Rodin mesh canonical. Do not begin UE5 implementation.

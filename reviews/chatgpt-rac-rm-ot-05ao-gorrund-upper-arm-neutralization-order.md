# RAC RM-OT-05AO — accept AN1 as partial AC2 base; upper-arm-only neutralization

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AN.
**Date:** 2026-10-16.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05an-gorrund-ac2-measured-range-gate.md` (e2c796e).

## 1. Author ruling on GO-05AN_AN1

Accept `GO-05AN_AN1` as the **partial AC2 working base**.

This is not final AC2 acceptance.

The AN1 classification of face 224765 is accepted as:
**CRIMP_RESOLVED / NOT A NEW INVERSION**

Reason:
- the face was a pre-existing ~77° crimp in the 05AL reference;
- AN1 aligns it to ~0.1° to its local surface;
- the immediately preceding-state gate has 0 flips;
- local inversions decrease from 5 to 3.

Therefore AN1 is technically valid for continued work.

### Advancement source

`GO-05AN_AN1.blend`
SHA-256:
`f058e439e009d704a921f0bc4bdf00c9fa629e7bd491e0d4ed5ebc4d1dc8d531`

Review GLB:
`GO-05AN_AN1.glb`
SHA-256:
`90f63f8e3c8347a83185b055e841b709034e0b30cbdd29453a7755ae305bc044`

## 2. Freeze what AN1 already solved

Treat the following as protected passed work:

### Legs
- quad channels largely neutralized;
- knee teardrop substantially reduced;
- calves visibly softer;
- joints remain large;
- limbs remain robust.

### Forearms
- corded relief materially reduced;
- no further broad forearm smoothing is authorized unless needed only for a tiny upper-arm transition.

### Torso / prior AC1
- all passed 05AI torso work remains frozen.

### Hard protect in 05AO
- head / neck;
- passed torso core;
- pelvis / genital / perineal;
- glutes / posterior pelvis;
- thighs / knees / shins / ankles / feet;
- forearms below the elbow transition, except a narrow continuity band;
- hands;
- tail / tail junction.

The sole artistic target in 05AO is the **upper arms**.

## 3. Goal

Make the upper arms read as:

**large-boned Gorrund upper arms with ordinary untrained soft tissue**

Remove the heroic read from:
- biceps peak;
- triceps bulge/separation;
- hard biceps–triceps groove;
- rounded bodybuilder upper-arm silhouette.

Preserve:
- shoulder-joint identity;
- elbow size;
- upper-arm skeletal length;
- broad Gorrund frame;
- passed AC1 torso;
- passed forearm result.

Do not produce:
- skinny arms;
- atrophied arms;
- pinched axilla;
- melted cylinder;
- obvious dent where the arm meets the torso.

## 4. Why the previous -3% rule is superseded for upper arms

05AN demonstrated that the global segment-radius rule was too strict for the specific remaining problem.

The upper arms are still heroically over-muscled and therefore **some actual soft-tissue circumference reduction is desired**.

For 05AO only:

### Upper-arm mean-radius allowance
Per side, cumulative change from the frozen 05AL predictive-safe baseline may reach:

**>= -8.0%**

Hard stop below -8%.

### Forearms
Forearm mean-radius change must remain:

**>= -3.5%**

because AN1 already improved them and they are no longer the primary target.

### Joint centres
Shoulder/elbow joint-centre drift:
- target < 0.5 mm;
- hard ceiling **0.75 mm**.

Do not use joint movement to create the visual result.

## 5. Inner-arm / torso contact — bounded clearance authority

The inner upper arms currently contact or nearly contact the hard-protected torso, making mask-based filtering unstable.

Authorize one **small, explicit upper-arm-only clearance preparation**.

### Allowed
Using normal Blender UI only:
- masked Grab / Elastic Deform;
- very local Smooth;
- Edit Mode local vertex movement if needed.

Only upper-arm soft-tissue vertices on the inner-arm contact band may move.

### Torso
Torso vertices remain exactly:
**0.000 mm**

### Clearance target
Create only enough visible/metric separation that upper-arm smoothing no longer collides with or folds against the torso core.

Maximum upper-arm contact-band movement:
**8.0 mm**

Do not move the whole arm or shoulder skeleton.

Do not create a large daylight gap; natural near-contact is acceptable after filtering, but the surfaces must not be numerically coupled in the unstable contact configuration.

### Gate after clearance prep
Require:
- 0 opened seams;
- 0 SI;
- 0 flips;
- 0 degenerates;
- 1 / 0 / 0 topology;
- torso 0.000 mm;
- protected regions 0.000 mm;
- shoulder/elbow joint drift <= 0.75 mm;
- no visible armpit dent/ridge;
- no arm-length change.

Freeze if clean as:

`GO-05AO_arm_clearance_base.blend`
`GO-05AO_arm_clearance_base.glb`

## 6. Upper-arm mask

Build an upper-arm-only mask.

### Sculptable
- biceps belly;
- triceps belly;
- lateral upper-arm soft tissue;
- inner upper-arm soft tissue after clearance prep.

### Feathered transitions
- shoulder-cap to upper arm;
- elbow to forearm;
- inner-arm to axilla.

### Hard protect
- torso core;
- shoulder joint centre / clavicle region;
- forearm proper;
- elbow joint centre;
- hand;
- all non-arm anatomy.

No hard box edge may run through the middle of a muscle belly.

Any mask smoothing occurs before final hard protection.

Read back the mask.

## 7. Predictive gate

Use the cumulative-reference predictor before every authored arm step.

Reference:
- frozen 05AL baseline for inherited triangles;
- local repaired checkpoint reference for retriangulated faces.

Flag:
- flips;
- >60° cumulative normal rotation;
- new local inversions;
- adjacent >60° folds.

Repair only predicted discrete neighborhoods using the proven bounded method:
- <= 0.5 mm local vertex movement;
- near-coplanar edge rotations;
- <= 0.5 mm patch deviation;
- 0.000 mm outside repair union.

05AO additional repair budget:
- **40 neighborhoods total**
- max 3 analysis/repair cycles per proposed authoring step.

## 8. Authoring route

Maximum **2 deliberate upper-arm checkpoints**.

### AO1 — upper-arm Smooth buildup

Use a calibrated UI Smooth Mesh Filter on upper-arm soft-tissue masks only.

Choose event count from simulation so that the proposed result:
- materially reduces biceps/triceps relief;
- stays above -8% upper-arm mean radius;
- leaves forearm >= -3.5%;
- stays within joint-drift limits.

Do not reuse the whole-limb 100-event count automatically; calibrate for this arm-only mask.

Before real authoring:
- predictor must be clean or repaired to clean.

After real authoring:
- full gate + render.

If upper arms now read ordinary/untrained, STOP and PASS.

### AO2 — one final targeted refinement, only if needed

If AO1 is clean and substantially improved but still slightly heroic:

Use one of:
- a second restrained Smooth Mesh Filter;
- Surface Smooth if only relief remains;
- tiny UI-only Flatten/Smooth on biceps/triceps peak if a filter would over-shrink the whole arm.

Predict/gate first.

Do not perform a third arm checkpoint.

## 9. Optional volume recovery

If the upper-arm read becomes correct but mean radius approaches the -8% limit and looks too thin:

Allow one restrained upper-arm-only Inflate/volume correction.

Requirements:
- simulation/predictor first;
- joints hard protected;
- torso protected;
- no biceps peak recreation;
- final upper-arm mean radius must remain between:
  **-8.0% and -3.0%**

This volume correction counts as AO2 if used.

## 10. One AN1 leg continuity touch

AN1 has a faint thigh-top line at the hip-core edge.

Because AN1 is now accepted as the partial working base, Claude may use **one tiny UI-only continuity touch** on that line.

Allowed:
- light Smooth / Surface Smooth;
- local only.

Requirements:
- no meaningful thigh/pelvis reshaping;
- pelvis core 0.000 mm;
- no new flip/SI/degenerate;
- line materially reduced.

This touch may be done either before or after the arm work but must be separately disclosed.

## 11. Technical gates

After every saved checkpoint:

- 0 opened seams;
- 0 SI;
- 0 flipped faces;
- 0 degenerates;
- 1 component / 0 boundary / 0 non-manifold;
- torso core = 0.000 mm;
- legs outside optional continuity touch = 0.000 mm;
- forearm proper = 0.000 mm except feather band;
- protected anatomy = 0.000 mm;
- stature / bbox unchanged;
- shoulder/elbow drift <= 0.75 mm;
- upper-arm radius >= -8%;
- forearm radius >= -3.5%;
- no dents / ridges / melted patches;
- no armpit collapse;
- no visible unnatural torso/arm gap.

## 12. Visual gate

Compared with AN1:

Required:
- biceps peak clearly reduced;
- triceps bulge/separation clearly reduced;
- upper-arm silhouette no longer bodybuilder-like;
- shoulder still broad enough for Gorrund frame;
- elbow remains large;
- forearm remains robust;
- whole arm harmonizes with the now-neutralized legs and torso;
- no skinny/weak read.

## 13. AC2 completion decision

If the upper arms pass and the AN1 legs/forearms remain valid:

Freeze:

`GO-05AO_AC2.blend`
`GO-05AO_AC2.glb`

Return:

**05AO AC2 PASS / READY FOR AC3 DECISION**

Then STOP.

Do not start AC3.

If the arm route cannot achieve the visual target within:
- two authoring checkpoints;
- -8% upper-arm radius;
- 8 mm contact-band clearance;
- 0.75 mm joint drift;

return:

**05AO UPPER-ARM ROUTE NOT CREDIBLE / STOP**

Keep AN1 as the partial working base and STOP.

## 14. Evidence

Return:
- AN1 acceptance pointer;
- clearance-prep map and max movement;
- mask readback;
- predictor/repair results;
- exact filter settings/event counts;
- upper-arm and forearm radius changes;
- shoulder/elbow joint drift;
- geometry gates;
- identical-camera whole/body/arms views;
- close upper-arm front/3/4/profile;
- AN1 vs AO result;
- thigh-top continuity comparison if touched.

## 15. State

Until final composition/Q1/Q2 and Tyler visual acceptance:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 16. Return

Commit:

`reviews/claude-rac-rm-ot-05ao-gorrund-upper-arm-neutralization-gate.md`

Evidence:

`reviews/rac-rmot05ao-evidence/`

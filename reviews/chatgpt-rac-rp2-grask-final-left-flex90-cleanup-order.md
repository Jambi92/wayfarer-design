# RAC RP2 — Grask SW3 shoulder-direction acceptance + final left-flex90 residual cleanup order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT review of Claude return `da4e892601492dfdf3ca465805ff827f0708582a`.  
**Parent gate:** `reviews/claude-rac-rp2-grask-vc3-interface-cleanup-shoulder-weight-volume-gate.md`.  
**Status entering this order:** Grask RP2 retopology remains AUTHOR ACCEPTED / FROZEN / CLOSED. Elbow experimentation is closed for RP2. Production deformation is not yet final/accepted.

This order records the author ruling on the latest return and authorizes **one final bounded shoulder cleanup pass** focused only on the left 90° flexion anterior axillary-fold residual.

---

## 1. Immutable parents / firewall

Do not edit, resave over, reproject, smooth, retopologize, symmetrise, or otherwise change:

- `GR_U_REF_RP2_retopo_v003.blend`
- `GR_U_REF_RP2_SOURCE_3D_v005.blend`
- v003 sidecars / frozen landmark package / freeze record
- v001 / v002 retopo provenance
- prior diagnostic rigs and evidence packages
- accepted elbow diagnostic records
- SW1 / SW2 / SW3 provenance

The accepted Basis/rest geometry remains exactly frozen v003.

No v004 retopology is authorized.

No production rig finalization, final production skinning, facial/oral work, creator morphs, UVs, materials, LODs, UE5 integration, animation, or another race is authorized.

Capture immutable-parent hashes before and after all work. Stop on any mismatch.

---

# AUTHOR RULINGS

## 2. Elbow state — CLOSED FOR RP2

Record the following as final RP2 disposition:

- H2 remains the preferred diagnostic elbow configuration through 60–120°.
- VC3 remains the best 130° numeric reference.
- 130° elbow remains a named **production-rig/contact-corrective carry-forward item**.
- VC3F1/F2 are rejected.
- No further elbow corrective/helper/contact experiments are authorized in RP2.
- Primary 130° volume evaluation remains overlap-aware physical volume relative to the straight-elbow base plus ring girth.
- No elbow result demonstrates a retopology failure.

Do not perform any elbow work in this order.

---

## 3. Shoulder state — SW3 ACCEPTED AS PRODUCTION DIRECTION

SW3 is hereby accepted as the **Grask shoulder diagnostic / production direction**.

This means the following architecture is accepted for carry-forward:

- girdle-only bounded weight diffusion;
- 0.5 LBS / DQS preserve-volume blend as used by SW3;
- S1-style abduction girdle/scapular mechanics as secondary mechanics;
- current GH placement;
- current accepted v002 diagnostic landmark architecture.

This is **not** final production rig acceptance.

SW3 remains provisional implementation evidence for the later production rigging stage.

Do not:
- relocate GH;
- redesign the shoulder hierarchy;
- reopen general shoulder weight diffusion;
- rework the right shoulder;
- retopologize;
- alter accepted shoulder/girdle anatomy.

---

## 4. Remaining open shoulder item

The only shoulder item authorized for further RP2 work is:

> **Left flex90 anterior axillary-fold residual**

Current SW3 left flex90 residual:
- 6 non-contact arm–arm pairs;
- 38 crease pairs;
- crease depth 7.9 mm;
- orientation disagreement 122;
- 2 local inversions;
- 4 folds outside intended crease/contact;
- shoulder-fan loop ratio 0.53;
- p95 strain 49%;
- max strain 104%;
- zone proxy −32.1%.

The right flex90 result and the other 11 D1 poses are not to be reopened.

---

# FINAL BOUNDED LEFT-FLEX90 CLEANUP

## 5. Scope

Target only the localized left anterior axillary-fold overlap at flex90.

Use SW3 as the baseline.

Do not change:
- global SW3 weighting architecture;
- GH;
- clavicle/scapular mechanics;
- right-side weights;
- elbow;
- other shoulder poses except as regression checks.

The goal is a **local residual correction**, not another shoulder redesign.

---

## 6. Allowed mechanisms

You may test one small localized correction class confined to the left flex90 anterior fold.

Allowed:
- bounded local weight redistribution;
- one small pose-space corrective;
- one local preserve-volume/contact-aware corrective field;
- one localized helper influence if strictly necessary.

Prefer the least invasive mechanism.

If a pose-space corrective is used:
- it must activate only near left shoulder flexion;
- it must return to exact zero outside the defined flex90 activation range;
- it must not alter abd90 or right-side behavior.

If a local helper is used:
- no new global helper chain;
- no segment-length or pivot changes;
- support must taper exactly to zero.

---

## 7. Candidate limit

At most **two** cleanup candidates:

- **LF1:** first localized cleanup;
- **LF2:** one bounded refinement only if LF1 is close and one specific localized defect remains.

No third candidate.

No broad search tree.

No new global weighting pass.

---

## 8. Primary acceptance targets — left flex90

A candidate may be selected only if all of the following are met:

### Non-contact intersections
- target: **0**
- absolute maximum: 1 tiny residual pair only if demonstrated as numerical/contact-classification noise and visually clean.

### Crease
- target depth <= **2.0 mm**
- preferred: 0–1.5 mm.

### Orientation
- target <= **100**
- preferred <= 90.

### Local inversions
- **0**

### Folds outside intended contact/crease
- **0**

### Loop spacing
- >= **0.50**
- do not sacrifice the SW3 loop recovery.

### Volume
- zone proxy should remain no worse than **−35%**
- preferred approximately SW3 or better.
- do not recreate S2-style ~−49% collapse.

### Strain
- p95 <= SW3 + 3 percentage points;
- max <= **125%**
- no new concentrated hot spot.

### Visual
- anterior axillary fold must read as smooth soft-tissue compression;
- no shelf, spike, seam, tear, pinching ridge or inflated deltoid;
- preserve current accepted Grask girdle slope and long-limbed read.

---

## 9. Regression protection

The selected cleanup candidate must prove:

- right flex90 is unchanged or numerically negligible;
- left abd45 / abd90 / ext30 / girdle variants remain unchanged or numerically negligible;
- all other 11 D1 poses preserve SW3 gains;
- no new retained-criterion failure outside D1;
- unrelated body regions remain bit-identical or numerically negligible.

If the correction has any nonzero influence outside left flex90, run the full affected subset and disclose it.

If influence reaches outside D1, run the full 43-pose suite.

---

## 10. Weight / corrective boundary requirements

Every changed field must:
- be spatially bounded;
- taper continuously to zero;
- have an exact-zero guard at support boundaries;
- avoid visible support seams;
- preserve rest shape exactly;
- preserve accepted asymmetry.

Return:
- changed vertex count;
- support area;
- max delta / weight delta;
- boundary continuity check.

---

## 11. Required visuals

Provide identical-camera comparisons:

### Left flex90
- W0
- S2
- SW3
- LF1
- LF2 if used

Views:
- front;
- rear;
- 3/4 front;
- 3/4 rear;
- anterior axillary closeup;
- wire closeup.

Overlays:
- non-contact pairs;
- crease pairs;
- orientation disagreement;
- local inversions;
- folds;
- compressed loops;
- support boundary.

Also provide:
- strain map;
- weight/corrective field map;
- local section or contour plot through the anterior fold.

---

## 12. Acceptance logic

If LF1 or LF2 meets all §8 targets with no regression:

- select it as the final RP2 shoulder diagnostic configuration;
- record SW3 + selected left-flex90 correction as the accepted Grask shoulder production direction;
- do **not** call it final production rig/skin acceptance.

If neither candidate meets §8:

- stop shoulder experimentation in RP2;
- keep SW3 as the accepted production direction;
- carry left flex90 as a named production-rig corrective item;
- do not continue iterating.

Do not reopen topology.

---

## 13. Required return

Commit:

1. `reviews/claude-rac-rp2-grask-final-left-flex90-cleanup-gate.md`;
2. LF1/LF2 configs and tools;
3. diagnostic results and visual evidence;
4. selected candidate data if any;
5. before/after immutable-parent hashes;
6. narrow `specs/STATUS.md` update;
7. session handoff.

The gate must explicitly state:

- whether LF1 or LF2 was selected;
- left flex90 final values for:
  - non-contact pairs;
  - crease depth;
  - orientation;
  - local inversions;
  - folds outside;
  - loop ratio;
  - p95/max strain;
  - zone proxy;
- visual judgement;
- changed support size / vertex count;
- regression result;
- whether shoulder experimentation is now closed for RP2;
- whether any result demonstrates topology failure;
- exact next ChatGPT decision.

---

## 14. Stop rules

STOP FOR CHATGPT REVIEW after this pass.

Do not proceed to:
- production rig finalization;
- production skinning freeze;
- further shoulder experiments if LF1/LF2 fail;
- elbow work;
- topology edits;
- facial/oral/eye work;
- creator morphs;
- UV/materials;
- LODs;
- UE5;
- another race.

---

## FINAL AUTHOR RULING

- Grask RP2 retopology remains **ACCEPTED / FROZEN / CLOSED**.
- Elbow experimentation is **CLOSED FOR RP2**; 130° is carried forward as a production-rig contact-corrective item.
- SW3 is **ACCEPTED AS THE GRASK SHOULDER PRODUCTION DIRECTION**.
- GH remains fixed.
- Exactly one final bounded left-flex90 anterior axillary-fold cleanup cycle is authorized.
- If that cycle fails, shoulder experimentation closes and the residual is carried forward.
- No topology or source-anatomy reopening is authorized.

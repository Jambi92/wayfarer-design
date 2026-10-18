# RAC Stage C C4.1 — Grask constraint-resolution diagnostics before author ruling

**Authority:** ChatGPT canon-management continuation after Stage C C0–C4.
**Date:** 2026-10-18.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-stage-c-gate.md` (f9da37e).

## 1. Purpose

Resolve the evidence behind the remaining Grask Stage C constraints **without editing geometry and without changing canon yet**.

Stage C currently returned:
- Grask E3: CONSTRAIN
- Gorrund: ACCEPT (reference state only)
- Combined: CONSTRAIN

The two unresolved canon/measurement questions are:
1. GR-G1 on the organized surface;
2. the old "thoracic depth never approaching Durrim proportional depth" row.

A third visual risk is:
3. weak pure-front Grask identity.

This block is read-only diagnostics only.

## 2. Frozen sources

Use the exact Stage C sources and hashes from:
`reviews/rac-stagec-evidence/checks/source_manifest.json`

Do not rebuild with changed settings.
Do not edit any mesh.
Do not change Grask E3 construction.

## 3. GR-G1 canonical measurement resolution

The Grask specification states:

- GR-G1 is a **girdle / thorax skeletal-relationship rule**;
- girdle checks use skeletal acromial / glenohumeral landmarks;
- they do **not** use bideltoid breadth;
- exact numeric morphology remains open.

The Stage C failure came from an organized-surface reading:
- shoulder-joint / thoracic = 1.304 vs <= 1.249;
- biacromial / thoracic = 1.274 vs <= 1.185.

Perform the canonical GR-G1 read on the same protected skeletal landmark method used by the accepted W1/W2 Grask route.

Requirements:
- reuse existing landmark definitions and thresholds;
- no new threshold;
- no surface substitute;
- report reference E3 and, if already supported without inventing new states, Narrow / Broad.

Return:
- exact readings;
- exact comparator;
- PASS / MARGINAL / FAIL under the existing rule;
- whether the Stage C organized-surface GR-G1 should be classified DIAGNOSTIC rather than a gate.

If no canonical protected-station implementation exists, document that precisely rather than inventing one.

## 4. Durrim-depth rule resolution

The Grask v1 spec contains both:
- "thoracic depth ... never approaching Durrim proportional depth";
- and the later Durrim contrast rule that says no valid equal height exists, so compare **design principles, proportional organization and silhouette**:
  - Durrim = compact structural power;
  - Grask = rangy structural elongation / high limb contribution.

The Stage C scalar:
- Grask E3 thoracic-depth share = 0.1681;
- Durrim = 0.1602.

Do a read-only diagnostic to determine whether E3 actually **converges on Durrim-like architecture**, rather than deciding from one depth number.

Use existing measurements only where possible:
- thoracic depth / stature;
- thoracic breadth / stature;
- torso share;
- leg share;
- arm share;
- span/reach;
- pelvis / thorax relation;
- relevant joint / structural presence;
- stature-normalized front/profile silhouettes;
- native-scale context.

Produce a Grask E3 vs Durrim comparison sheet:
- front;
- 3/4;
- profile;
- rear;
- silhouettes.

Important:
- because no biological equal-height overlap exists, any uniform-height normalization is **diagnostic visualization only**;
- do not treat it as a valid biological body.

Return one evidence classification:
- **ARCHITECTURALLY DISTINCT DESPITE DEPTH OVERLAP**
- **AMBIGUOUS**
- **DURRIM-LIKE CONVERGENCE**

Do not modify either race.

## 5. Front-only Grask identity diagnostic

Stage C found:
- full multi-view Grask identity is distinct;
- pure front view is weaker.

Run a bounded front-only blind read using existing Stage C renders at matched comparison heights.

Include:
- Grask E3;
- Skarn;
- Marchfolk;
- Aelari if an existing matched or normalized comparison can be made without authoring a new body.

Do not tell the reader which is Grask.

Ask:
1. Can the bodies be distinguished structurally from front view alone?
2. What cues drive the distinction?
3. Is the distinction mainly size, thinness/breadth, or anatomical organization?
4. Does any body read as a stretched human / caricature?

No new acceptance threshold.

Return the raw answer and a compact interpretation.

## 6. Existing creator constraints

Do not re-test by authoring geometry.

Carry forward as implementation constraints unless evidence shows a contradiction:

- E3 organization currently uses absolute centimetres (scapular mass, keel, flank); creator implementation must scale these relationship-aware across stature.
- Narrow-frame joint breadth must be carried by the skeleton/frame system, not hidden by tendon-cord surface treatment.
- chest/abdomen shading band is a surface/normal/retopology issue, not a morphology change.

## 7. Gorrund

Do not reopen Gorrund.

Gorrund remains:
**Stage C ACCEPT — reference state only**

Its creator/frame/composition/stature-family guarantees remain deferred as already ruled.

## 8. Deliverable

Return:

`reviews/claude-rac-stage-c-c4-1-grask-resolution.md`

Evidence:

`reviews/rac-stagec-c4-1-evidence/`

Include:
- canonical GR-G1 measurement;
- Grask-vs-Durrim architecture table and sheet;
- front-only blind read;
- exact recommendation on each Stage C Grask constraint.

## 9. Stop

STOP for ChatGPT/Tyler author ruling.

Do not:
- edit Grask;
- sculpt Grask;
- change canon;
- promote Stage C;
- start D4;
- start UE5;
- start rigging;
- start creator implementation.

Return recommended statuses, but do not self-promote:
- Grask E3 Stage C — ACCEPT / CONSTRAIN / REJECT recommendation
- Gorrund Stage C — ACCEPT
- Combined Stage C — ACCEPT / CONSTRAIN recommendation

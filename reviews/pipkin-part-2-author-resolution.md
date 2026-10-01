# Author Resolution — Pipkin v1.0 Part 2 Audit

**Author:** ChatGPT  
**Responds to:** `audits/pipkin-part-2.md`  
**Audit result received:** PASS WITH CLARIFICATIONS

Claude: I have read the audit. The findings are accepted as follows.

## 1. Canonical race-file decision — ACCEPTED

`specs/pipkin/PIPKIN_V1.md` is the authoritative Pipkin race specification.

The earlier condensed version of `specs/pipkin/PIPKIN_V1.md` (initialization-era commit `cb3510e`) is superseded; its omissions must never be propagated into the current authoritative full specification.

Repository convention going forward:
- `specs/<race>/<RACE>_V1.md` = authoritative full race specifications.
- `specs/STATUS.md` = status/navigation only.
- `decisions/PROJECT_RULES.md` = universal authored project rules.
- `register/` = detailed decision/open-item register maintained as shared project record.
- `audits/` = Claude audit record.
- New audits may use per-part files; existing per-race audit files remain historical records.

Authority remains:
**Approved Design Specification > Open Decision Register > Prototype Implementation / Earlier Shorthand.**

## 2. Concrete human-differentiation anchor — ACCEPTED

The audit correctly identifies that Pipkin identity cannot depend primarily on pelvic breadth.

Add/interpret the Part 2 specialization as follows:

> **Low-Set Compact Trunk Architecture is defined not merely by pelvic breadth, but by the coordinated vertical organization of the trunk: compared with normalized Marchfolk adult anatomy, Pipkin trend toward a modestly reduced vertical central-trunk contribution to total stature, with a compact lumbar/waist transition and a mature pelvis whose vertical depth and three-dimensional structural participation remain substantial relative to the thorax. The resulting identity is a lower-trunk-centered adult structural organization that persists even when pelvic breadth approaches Marchfolk-like values.**

Clarifications:
- This is a population-level relational tendency, not one mandatory numeric ratio.
- "Reduced vertical central-trunk contribution" does **not** mean Durrim-like vertical compression.
- It does not require unusually long legs; the total stature relationship is coordinated across trunk and limbs.
- Compact lumbar/waist transition does not mean absent waist, short spine, crouching, belly compression, or a fixed external silhouette.
- Pelvic **vertical depth/height and 3D structural integration**, not hip width alone, contribute to the anchor.
- At lower-valid pelvic breadth, a Pipkin must still read Pipkin through trunk vertical organization, lower-trunk/pelvic integration, skeletal lightness, adult joint relationships, and coordinated limb contribution.
- At Marchfolk-similar shoulder/thoracic breadth, the same relationships must survive.
- No single "Low-Set" or "Pipkin Proportion" creator slider is implied.

This clarification is intended to strengthen PIP-STRESS-07 and the Marchfolk-similar-frame stress test without turning Pipkin into Durrim, Fenn, Grask, or a scaled human.

## 3. Sex-coding safeguard — ACCEPTED

The pelvis-to-thorax population comparison must be evaluated **within comparable sex-related anatomical configurations**, not by comparing a generic Pipkin pelvis against a sex-neutral or mismatched Marchfolk reference.

Add the following rule:

> **Where sex-related anatomy materially affects pelvic or thoracic structure, racial/population comparisons must use like-for-like anatomical configurations (for example, male Pipkin against male Marchfolk and female Pipkin against female Marchfolk). The Pipkin population tendency is expressed through coordinated adult pelvic breadth, depth, height, landmarks, and trunk integration; it is not defined by shoulder-to-hip ratio, external hip circumference, or a feminized silhouette.**

Required validation pair:
- Adult male Pipkin vs adult male Marchfolk at normalized displayed height/frame/composition.
- Adult female Pipkin vs adult female Marchfolk at normalized displayed height/frame/composition.

Neither comparison may require the Pipkin to read as the opposite human sex in order to express racial anatomy.

This does not prematurely finalize the magnitude or exact morphology of Pipkin sexual dimorphism; those remain OPEN.

## 4. Durrim-boundary carriers — ACCEPTED

At the ~122 cm equal-height boundary, pelvic breadth is not the primary discriminator.

The boundary must be carried jointly by:
- torso vertical organization,
- thoracic breadth/depth and axial structural presence,
- proportional limb contribution,
- joint dimensions,
- long-bone robusticity,
- hand/wrist and foot/ankle structural relationships,
- and the distinct Pipkin Low-Set Compact Trunk vs Durrim Compact Structural Concentration systems.

A Broad Pipkin and Narrow Durrim must remain distinguishable even where pelvic breadth converges.

## 5. Fidelity-gap finding — ACCEPTED

The omissions identified in the condensed `specs/pipkin/PIPKIN_V1.md` are not design deletions. All approved validation cases, comparative rows, skeletal/body safeguards, world/stature implications, status statements, and stronger anti-caricature wording retained in `races/11-pipkin.md` remain authoritative.

Do not propagate omissions from the condensed file.

## 6. Part 2 status

With these author clarifications, I consider Pipkin Part 2 **ready for re-audit**.

Claude: please audit this resolution against the full canonical `races/11-pipkin.md`, project rules, decision register, Marchfolk, Durrim, Fenn, Aelari, Grask, and Gorrund.

Please specifically verify:
1. the new vertical-trunk/lumbar/pelvic anchor is anatomically coherent and does not create Durrim-like compression;
2. it survives lower pelvic breadth and Marchfolk-similar thoracic/frame configurations;
3. the within-sex safeguard solves the sex-coding issue without prematurely fixing dimorphism;
4. the Durrim boundary remains positive and multi-factor;
5. no new hard creator-control dependency has been introduced.

Record the re-audit in `audits/pipkin-part-2-reaudit.md`.

**Do not begin Part 3 yet. Do not modify UE5.**

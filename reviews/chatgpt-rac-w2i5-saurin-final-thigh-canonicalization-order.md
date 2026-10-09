# WAYFARER RAC — W2I5 SAURIN FINAL THIGH FINISH / CONDITIONAL CANONICALIZATION ORDER

**Status:** AUTHOR DECISION ISSUED — OPTION (a) SELECTED  
**Parent block:** RAC W2I4 — Saurin final asset finish / canonicalization prep  
**Decision:** Authorize the localized medial / posterior thigh sculpt finish; accept the W2I4 regenerated scale-field realization; conditionally canonicalize and close W2I only if all guards pass  
**Scope:** REFERENCE-ASSET FINISH / CANONICALIZATION ONLY — NO UE5  
**Stop condition:** Stop after the final Saurin W2 canonicalization / closure report. Do not begin Wave 3.

---

# 1. AUTHOR RULINGS

The W2I4 gate has been reviewed.

Final author rulings:

- **L1 leg biology — ACCEPT**
- **F2 forearm biology — ACCEPT**
- **W2I4 regenerated scale-field realization — ACCEPT**
- **SAU-SILHOUETTE — ACCEPT WITH PRESENTATION CONTEXT**
- **Tail coupling — ACCEPT**
- **Saurin W2 biological design — ACCEPT**
- **W2I4 reference asset — CONSTRAIN only by medial / posterior thigh finish**
- **Canonicalization — HOLD only until the localized thigh finish is closed**

Select W2I4 author option:

> **(a) AUTHORIZE A LOCALIZED ARTIST SCULPT PASS ON THE MEDIAL / POSTERIOR THIGH.**

Do not choose option (b) or option (c).

The W2I4 anterior / lateral thigh improvement is retained.

The W2I4 regenerated scale-field layout is accepted as the new W2 realization despite the lost historical seed layout. The saved W2I4 seed set becomes the reproducible W2 seed realization going forward.

---

# 2. WHAT MAY CHANGE

The only body geometry authorized to change is the **fine / medium surface relief of the medial and posterior thigh**, including the narrow transition sector necessary to blend cleanly into the already accepted anterior / lateral thigh finish.

The purpose is to remove:

- vertically stretched hamstring / adductor relief inherited from W2I3;
- small procedural marks at the anterior/lateral ↔ medial/posterior sector boundary;
- any visible duplicated / smeared relief created by the +9.2 cm thigh extension.

Permitted operations:

- localized sculpt / smooth / re-form of muscular and tendinous surface relief;
- local redistribution of fine relief so it reads at native anatomical scale;
- narrow transition blending across the sector boundary;
- local surface cleanup necessary to remove procedural pits, tears, ridges or duplicated-looking forms.

This is an **asset-quality finish**, not a biology pass.

---

# 3. WHAT MAY NOT CHANGE

Do not change any accepted biological target or measurement-bearing relationship.

Hard holds:

- stature;
- hip station;
- knee station;
- femur / leg = accepted L1 target;
- total leg share;
- lower axial trunk;
- thoracic share;
- neck share;
- head;
- pelvis;
- caudal base;
- tail root area;
- tail length;
- tail taper / thickness system;
- tail carriage;
- total arm share;
- forearm / arm = accepted F2 target;
- hand / foot size;
- joint centres;
- foot plantigrade contact;
- §263 female-centre relationships;
- frame system;
- composition system;
- all accepted W2I3 / W2I4 race-comparison results.

Do not:

- bulk the thigh into human bodybuilder anatomy;
- introduce a new hamstring/adductor biological design;
- narrow the thigh to hide the stretch;
- alter the crotch / pouch / reproductive anatomy;
- modify the pelvis to make sculpt transfer easier;
- alter the caudal system;
- alter the accepted anterior / lateral thigh except for the minimum blend width required to erase the sector seam.

---

# 4. RELIEF QUALITY TARGET

Use the frozen SA-M188 / SA-F188 thigh only as the **native relief-scale reference**, not as a body-form target.

W2I4 measured:

- frozen medial / posterior native relief correlation length ≈ **3.94 cm**;
- W2I3 medial / posterior ≈ **6.67 cm**;
- W2I4 medial / posterior ≈ **6.75 cm**;
- W2I4 anterior / lateral corrected relief ≈ **2.92 cm** vs frozen ≈ **2.63 cm**.

The medial / posterior finish should move clearly back toward the **native-scale relief neighborhood**.

Do not overfit to exactly 3.94 cm.

Pass condition:

> The finished medial / posterior thigh must read materially closer to the frozen native relief scale than to the stretched W2I3/W2I4 value, while preserving the accepted longer femur and muscle-scale forms.

The sculpt should look like **longer muscles over a longer femur**, not a vertically stretched texture / relief pattern.

---

# 5. REQUIRED VISUAL REVIEW

Return close orthographic / shaded evidence for both SA-M188 and SA-F188:

- front thigh;
- lateral thigh;
- rear thigh;
- medial / adductor thigh;
- hip-to-thigh transition;
- knee-to-thigh transition;
- front 3/4;
- rear 3/4.

Also return:

- W2I3 stretched thigh;
- W2I4 partial-finish thigh;
- W2I5 final thigh;

side by side at matched camera / scale.

The final sheet must make it possible to inspect:

- adductor origin;
- hamstring flow;
- gluteal-to-proximal-femur transition;
- quadriceps continuity;
- sector boundary;
- hip crease;
- knee / tendon transition;
- medial crotch wall.

---

# 6. SURFACE / SCALE-FIELD HANDLING

The **W2I4 regenerated scale-field realization is author-accepted**.

Preserve its saved seed realization.

After the sculpt:

- keep topology unchanged if at all possible;
- keep region-family labels unchanged;
- recompute only geometry-dependent normals / flow / displacement placement as necessary;
- reuse the accepted W2I4 saved seed set rather than randomizing a new field;
- re-run the accepted surface generator without changing its family / size / elongation / imbrication logic;
- preserve palmar / plantar and moved-anchor handling.

Do not create a third unrelated scale layout.

If the sculpt makes exact reuse of the saved seed realization technically impossible, stop and report why before changing the seed realization.

---

# 7. TOPOLOGY / FOLD / STRAIN GUARDS

Re-run the W2I4 quality guards after the sculpt.

Required:

- 0 new flipped faces vs the accepted W2I4 candidate across all 62 bodies;
- 0 new flipped faces in SA-M188 / SA-F188 vs the accepted comparison baseline;
- closed manifold;
- no new degenerate faces;
- no new obvious sector-boundary crease;
- no visible pits / tears / lumps in the medial / posterior thigh;
- no new knee, hip, crotch, axilla, neck or shoulder artifact.

Track edge strain in the edited thigh.

A few isolated high-strain edges may be reported, but no band-wide stretch / compression artifact may remain.

If the sculpt creates a new topology or fold problem, fix only the sculpted region; do not compensate by changing accepted anatomy elsewhere.

---

# 8. MEASUREMENT-INVARIANCE AUDIT

Rebuild and remeasure the complete 62-body family after the finish.

The W2I5 sculpt must preserve the accepted W2I4 biological results.

At minimum re-check:

- stature;
- hip / H;
- femur / leg;
- total leg / H;
- lower trunk;
- thoracic share;
- neck share;
- head height / length;
- forearm / arm;
- total arm / H;
- thoracic d/w;
- tail length %;
- tail root area / RSI;
- lean;
- frame results;
- composition firewall;
- §263 sex cases;
- lower-trunk floor;
- matched-height race comparisons;
- Durrim leg separation;
- Cogling forearm separation;
- Grask reach;
- Gorrund never-collapse.

There must be **0 biological verdict changes** versus W2I4.

If a sculpt changes a measurement materially, restore the measurement and re-sculpt the relief locally.

---

# 9. TAIL / SAU-SILHOUETTE

Do not reopen the caudal design.

Preserve the W2I4 author ruling:

> **SAU-SILHOUETTE — ACCEPT WITH PRESENTATION CONTEXT.**

The strict front orthographic end-on tail projection remains provenance / diagnostic context only.

Do not modify:

- tail root;
- tail carriage;
- pelvis;
- leg spacing;
- RSI;
- tail length;
- caudal landmark.

No further silhouette experiment is authorized in W2I5.

---

# 10. TAIL-COUPLING REGRESSION

Re-run the accepted tail-cap confirmation after the final sculpt / surface regeneration.

Expected outcome: unchanged from W2I4.

Recheck at minimum:

- Balanced 188;
- Broad 188;
- Narrow + high fat 188;
- Broad 208;
- 55% substantial-base case;
- accepted anchor cases.

Use the same-state lean rule.

Do not reopen D-B / report-only beyond-anchor cases unless the sculpt itself changes them.

---

# 11. ACCEPTED NAMED DEPENDENCIES REMAIN OPEN

Do not attempt to solve these during W2I5:

- RM-UB-08 numeric creator ranges;
- RM-UF-04;
- remaining facial measurement rows;
- claw numeric creator ranges;
- final density model;
- final neutral idle / dynamic posture;
- SAU-BODY-20 world-space / furniture / mount / corridor implications;
- final creator-envelope interpolation;
- UE5;
- rigging;
- animation;
- equipment fitting;
- gameplay.

Carry them forward exactly as named dependencies / later work.

---

# 12. CONDITIONAL CANONICALIZATION AUTHORIZATION

If and only if all of the following are true:

1. medial / posterior thigh relief is visually reference-quality;
2. sector-boundary artifacts are removed;
3. the relief-scale diagnostic moves clearly toward native scale;
4. topology / fold / strain guards pass;
5. W2I4 biological measurements and verdicts remain unchanged;
6. scale-field reuse / regeneration with the accepted saved W2I4 seeds is clean;
7. tail coupling remains unchanged;
8. no new Saurin canon contradiction appears;

then **canonicalization is authorized in the same pass**.

Do not stop for another approval gate merely because the thigh passes.

If any condition fails, do not canonicalize; return the failure package and stop.

---

# 13. CANONICALIZATION ACTIONS IF PASS

On a clean pass, execute the canonicalization package prepared in W2I4.

## Asset / reference

Promote the final W2I5 candidate as the current W2 Saurin reference.

Preserve all historical W1 / W2I provenance files and hashes.

Do not delete or rewrite history.

Update the canonical equivalents of:

- Saurin final base;
- surface delta / relief;
- rebuild route;
- saved seed realization;
- SA-F §263 realization;
- carried / recomputed region fields.

If the final W2I5 sculpt changes a W2I4 candidate hash, record the **new W2I5 hashes** as canonical, not the obsolete W2I4 hashes.

## Tool chain

Update / reconcile the prepared items:

- Lbase.pkl / moved stations;
- Part 7 ref_metrics.json;
- Gate 8 axis.npy;
- g7geo.py ARM / LEG construction points and moved hand-pad / claw anchors;
- final region-field package;
- §263 fsets3 re-verification.

## Canon / records

Apply the prepared W2 Saurin canon / decision updates, adjusted to the final W2I5 hashes:

- specs/saurin/SAURIN_V1.md;
- decisions/REFERENCE_ANATOMY_V1.md;
- tools/rac/w1/cfg/w2i/SA-boundary.json;
- relevant Saurin evidence / reference records;
- specs/STATUS.md;
- race reference queue / closure record.

Preserve the presentation-context note already accepted.

---

# 14. FINAL CANON STATEMENT

If canonicalization succeeds, record explicitly:

> The W2 Saurin reference preserves the accepted W2I3 L1 + F2 biological target, W2I4 regenerated scale-field system, accepted tail/caudal biology, and §263 sex-related system. W2I5 changes only localized medial/posterior thigh reference-asset relief to restore native-scale anatomical surface detail. W1 aff1b52 / historical SA-F remain provenance references.

Do not describe the W2I5 sculpt as a new biological trait.

---

# 15. REQUIRED FINAL REPORT

Return:

**reviews/claude-rac-w2i5-saurin-canonicalization-closure-report.md**

The report must state:

- **Medial / posterior thigh relief — ACCEPT / CONSTRAIN / REJECT**
- **Scale-field continuity — ACCEPT / CONSTRAIN / REJECT**
- **Topology / fold / strain — ACCEPT / CONSTRAIN / REJECT**
- **Measurement invariance — ACCEPT / CONSTRAIN / REJECT**
- **Tail coupling — ACCEPT / CONSTRAIN / REJECT**
- **SAU-SILHOUETTE — ACCEPT WITH PRESENTATION CONTEXT**
- **Saurin W2 reference asset — ACCEPT / CONSTRAIN / REJECT**
- **Canonicalization — COMPLETED / NOT COMPLETED**
- **Saurin W2I overall — FINAL ACCEPT / CONSTRAIN / REJECT**

Include:

1. before / W2I4 / W2I5 thigh comparison;
2. relief-scale measurements;
3. topology / fold / strain results;
4. 62-body regression summary;
5. tail-cap regression;
6. final file hashes;
7. canonical files updated;
8. historical provenance preserved;
9. complete remaining named dependencies;
10. explicit confirmation that no accepted Saurin biology changed in W2I5.

---

# 16. STOP CONDITION

After a successful canonicalization:

**STOP with W2I formally closed.**

Do not begin:

- Wave 3;
- Halvren genealogy-conditioned references;
- final roster world-scale review;
- creator-envelope implementation;
- UE5;
- rigging;
- animation;
- equipment fitting;
- gameplay implementation.

Return the W2I5 canonicalization / closure report for ChatGPT review before the next RAC phase.

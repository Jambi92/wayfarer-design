# RAC RM-OT-05V — whole-body ARM neutralization, source-artifact cleanup, and final closure path

**Authority:** Tyler-authorized autonomous continuation after review of the RM-OT-05 final closure audit (323dfee).
**Date:** October 14, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent closure audit:** `reviews/claude-rac-rm-ot-05-final-gorrund-acceptance-closure.md`.

## 1. Author ruling

Choose closure-audit option **1: whole-body neutralization**.

Do **not** waive REFERENCE_ANATOMY_V1 R-7 / R-8 / R-12.

The selected U8 cp1 scene remains the accepted **visual/source-surface reference** for this lineage and must remain unchanged:

`GO-05U8_cp1.blend`
SHA-256 `2341d55445a448e24852f98fd9df3984ab12d706ef0b455cb4a2cdb0782860d6`.

Build a separate neutralized ARM candidate from it. Never overwrite the selected visual/source scene or `base.glb`.

All reconstructed skin is **INFERRED**, with explicit provenance. Nothing measured from reconstructed regions becomes biological canon merely because the candidate contains it.

## 2. Preserve the biological result already accepted

The following are frozen biological/visual decisions unless a neutralization seam requires a tiny local continuity correction:

- leonine beastfolk head identity and tail;
- massive load-bearing Gorrund body organization;
- accepted U6/U7/U8 posterior-axilla repair;
- U8 cp1 residual crease disposition: accepted anatomical crease/junction;
- accepted stature range and nominal reference bookkeeping;
- plantigrade bipedal body plan;
- all race relationships already locked in GORRUND_V1.

Do not restart the body architecture search. Do not reuse rejected 05A–05P procedural candidates as body-form targets.

## 3. Neutralization target and sequence

Create a new candidate, e.g. `GO-ARM-N1.blend`, from U8 cp1.

Work in bounded region groups, with a verification checkpoint after each group. Prefer direct desktop Blender work for reconstructed anatomy. Use existing correspondence/protection infrastructure additively.

### Group A — removable overlays / jewellery / hair

Remove where separable:
- loincloth flaps;
- necklace / pendant teeth;
- front braids;
- back braid;
- any other clearly separable non-body overlay in the 05Q inventory.

Removal must not alter underlying body geometry when underlying body exists.

### Group B — fused upper-limb garments

Neutralize:
- both forearm bracers;
- remaining -X upper-arm armband.

Where no skin exists beneath, reconstruct only the missing Gorrund surface using:
- adjacent accepted Gorrund anatomy;
- bilateral counterpart where valid;
- local limb axes / neighboring cross-sections;
- locked Gorrund arm / wrist / hand relationships.

Do not import a generic human arm or hand template.

### Group C — fused shin / ankle wraps and feet

Remove / reconstruct:
- shin and ankle wraps on both legs;
- the ankle-foot transition hidden by them.

At the same time, resolve the source foot artifact against **existing Gorrund canon**:

GORRUND_V1 requires:
- upright **plantigrade humanoid** feet;
- **five toes per foot**;
- toes humanoid and non-prehensile;
- ordinary protective toenails;
- never paws, claws, ape-like feet, digitigrade feet or monster feet.

The source-route “paw-like toes” are **not accepted canon**. If the selected source feet violate these rules, correct them in the neutral ARM candidate while preserving large absolute Gorrund foot scale and load-bearing integration.

This is a canon-enforcement correction, not a new design choice.

### Group D — waist / pelvis / loincloth top

This is the highest-risk reconstruction region.

Remove / neutralize the fused belt and loincloth top and reconstruct the body surface necessary to expose:
- iliac crest / ASIS region;
- pelvic breadth/depth silhouette;
- inguinal / upper-thigh transitions;
- gluteal / sacral / thigh-root landmarks needed by the ARM measurement method.

Use the accepted Gorrund pelvis / load-path relations and neighboring surface, not generic human pelvic anatomy.

A **minimal neutral modesty proxy** is allowed only over the external genital-only area if needed, provided:
- it is zero-thickness / measurement-excluded;
- it covers no pelvis, ASIS, thigh-root, gluteal, crotch-measurement or other required landmark;
- it is clearly labelled presentation-only and never used to validate anatomy.

Do not invent detailed sex-specific external biology that Gorrund canon has not authored.

### Group E — mane / neck / upper-back hair

For the ARM derivative, remove mane / body hair that obscures required neck, shoulder or upper-back landmarks under R-8.

Reconstruct only the underlying cranial/neck/back body surface necessary for measurement, using adjacent source anatomy and Gorrund neck/shoulder canon.

The original mane-bearing U8 visual reference remains preserved for character identity and later presentation work. Hair removal here is a measurement-state requirement, not a canon statement that Gorrund lack mane/hair.

## 4. Protection / topology rules

Before production edits, build a neutralization plan and frozen sets for each group.

For every group:
- preserve all geometry outside the active group bit-exact to the preceding accepted neutralization checkpoint;
- no global remesh or global smooth;
- no Dyntopo unless a later author order explicitly approves it;
- preserve vertex correspondence wherever possible;
- if local topology replacement is unavoidable because fused clothing has no skin beneath, confine it to the active region, document every replaced face, and maintain a deterministic map to the source boundary;
- no intersections, inverted faces, non-manifold seams or visible garment lips;
- local triangle quality >= the accepted local safety floor used in U6–U8 unless an inherited untouched source face is separately documented;
- reconstructed skin labelled INFERRED.

Use bilateral symmetry only where the source/reference state is supposed to be symmetric and where it does not copy a damaged/garmented counterpart.

## 5. Stature ruling and measurement

The closure audit's **241.06 cm raw vertical extent is not accepted as R-13 stature**, because it includes head display / hair / keratin and was not skull-vertex isolated.

After Group E:
1. identify the anatomical skull vertex with hair, mane, horn/keratin/display excluded exactly as R-13 requires;
2. measure sole-ground to skull vertex;
3. report raw full extent and R-13 anatomical stature separately.

The governing design remains:
- nominal reference about **229 cm**;
- accepted reference-realization bookkeeping **GOREF 230.9 cm**.

Do **not** uniformly scale the candidate.

If the true neutralized skull-vertex stature is consistent with the already accepted GOREF bookkeeping, record PASS.

If it is materially inconsistent with the accepted reference realization, STOP before changing proportions and report the exact anatomical stature and which body segments create the difference. Do not silently rescale or rewrite stature canon.

## 6. Measurement stance R-6

After neutralization, audit the candidate against R-6:
- upright head carriage;
- arms hanging with small fixed abduction;
- palms toward thighs;
- feet hip-width, parallel, full plantigrade contact;
- hips/knees extended without lock/crouch;
- neutral adult spine.

If the existing U8 pose already satisfies R-6, record that and do not change it.

If only presentation pose differs, a separate **measurement-pose derivative** may be made using rigid/semi-rigid segment repositioning that preserves lengths, joint centres and accepted anatomy. No posture trick may be used to improve race readability.

If R-6 cannot be achieved without materially deforming anatomy, STOP and report that blocker.

## 7. Final ARM acceptance gates after neutralization

Once Groups A–E and any necessary R-6 pose derivative are technically clean, rerun the governing REFERENCE_ANATOMY_V1 §6 acceptance path on the neutralized candidate.

Mandatory:
- R-1…R-14 audit;
- N3 neutralization;
- UCCA §24 applicable central-body tiers;
- pairwise / boundary tests required by §6;
- the replicated neutralized structural-readability / blind gate carried by 05E / 05F;
- Grask E3 remains in the comparison set where the established protocol requires it;
- verify the candidate does not collapse to “heavy human,” ogre/brute stereotype, or Grask;
- verify accepted Gorrund hard-form / load-bearing cues persist without clothing, mane or source presentation;
- confirm plantigrade five-toed humanoid feet;
- verify U6/U7/U8 accepted local repairs did not regress.

Do not use the leonine head, mane, clothing or tail as the only reason a body-only structural gate passes when the gate is specifically testing body architecture.

If a mandatory gate fails, STOP with exact evidence; do not weaken the canon or test.

## 8. Author acceptance and RM-OT-05 closure

If the neutralized candidate passes all mandatory ARM gates:

- record it as the **Gorrund Wave-1 ARM** under REFERENCE_ANATOMY_V1 §6;
- retain U8 cp1 separately as the clothed/mane-bearing source/visual reference and provenance ancestor;
- write the exact neutral ARM hash into the RMQ and GORRUND_V1 status line;
- preserve builder-chosen / inferred values as provenance, not discovered canon;
- mark **RM-OT-05 FINAL CLOSED**;
- release the Gorrund blocker on Stage C.

## 9. Stage C variant derivation author ruling

The closure audit also identified that Stage C needs Gorrund Narrow/Broad, low/high composition and stature variants but the recovered-source lineage has no accepted scaffold.

If and only if the neutralized ARM is accepted, this order authorizes creation of a **new validation scaffold derived from the accepted neutral ARM**.

Rules:
- the accepted neutral ARM is reproduced exactly at reference state;
- stature variants use established Gorrund allometry/proportion rules, never uniform scaling;
- Narrow/Broad alter frame relationships only as GORRUND_V1 defines;
- composition variants alter muscle/fat only, never skeletal identity;
- rejected 05A–05P meshes may be used only as provenance / constraint evidence, never as shape targets;
- all variants are validation candidates, not new canon individuals;
- if the scaffold cannot reproduce the accepted ARM exactly or violates protected relations, STOP before Stage C.

Once the scaffold is validated, execute the already-defined Stage C contract from 05E §7/§10 and 05F:
- Grask E3 + accepted Gorrund;
- stature endpoints and internal heights;
- matched-height cases;
- frame extremes;
- low/reference/high composition;
- protected skeletal/clearance guards;
- full-roster read;
- author package.

Do not begin D4, UE5, production rigging or creator implementation unless Stage C itself closes and the queue separately authorizes the next stage.

## 10. Evidence and return

Commit a gate report such as:

`reviews/claude-rac-rm-ot-05v-gorrund-arm-neutralization-closure-gate.md`

Evidence under:

`reviews/rac-rmot05v-evidence/`

Include:
- exact zone maps and editable/protected sets;
- before/after renders for each neutralization group;
- edit logs / desktop actions;
- source/return hashes;
- inferred-skin provenance;
- foot digit/plantigrade verification;
- R-13 stature evidence;
- R-6 stance evidence;
- final §6 acceptance / readability results;
- package/manifest/clean-extraction verification for the accepted neutral candidate.

Outcome must be one of:

**RM-OT-05V PASS / GORRUND NEUTRAL ARM AUTHOR ACCEPTANCE READY**

or

**RM-OT-05V BLOCKED — <EXACT MANDATORY FAILURE>**

If PASS, proceed to §8/§9 closure and Stage C preparation/execution autonomously as authorized above.

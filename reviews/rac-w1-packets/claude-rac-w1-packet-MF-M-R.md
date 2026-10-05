# ARM Build Packet — MF-M-R: Marchfolk configuration 1 (correction of the Iteration 3 candidate)

**Order:** `reviews/chatgpt-reference-anatomy-wave1-execution-order.md` §4, §8
**Status:** BUILD REQUIRED. This packet is a specification, **not a mesh**. No measurement exists for this candidate.

| Field | Content |
|---|---|
| Population / candidate | Marchfolk configuration 1 (correction of the Iteration 3 candidate) |
| Reference stature | 173 cm |
| Sex-related configuration | Configuration 1, ordinary human sex-related anatomy |
| Frame / composition | Central skeletal values; reference composition (R-3, R-4) |
| Neutralization | N3 body; N-Head only for body tests that require it |
| Canon constraints the candidate must embody | Human Reference Population; recognizably human skeleton (race spec; line citations to be confirmed by the builder); no race multipliers; Apparent Biological Age mid-adult (the Iteration 3 candidate uses MakeHuman's 'young' age macro). |
| Comparison tests to pass | MF permanent height character at the reference (MF L249); N3 identity; acceptance §6. |
| Measurements it unlocks | RM-UB-07 (central), MF sides of RM-LR-01/05/07 and RM-OT-01; RM-CF-02 central and RM-UF-01 only once eyeballs exist. |

- **Reference state** (`decisions/REFERENCE_ANATOMY_V1.md` §3): central-tendency adult (R-1); central skeletal values, not "Balanced" as a default (R-3); reference composition: population-centre muscularity and fat amount, neutral distribution, no regional offsets (R-4); zero natural asymmetry, bilaterally mirrored (R-5); measurement stance R-6 (upright; head neutral; arms hanging with a small fixed abduction, palms toward the thighs; feet hip-width, parallel, full plantigrade; hips and knees extended; neutral adult spinal curvature); N3 (R-7); no scalp, facial or body hair over landmarks (R-8); one neutral matte material, no displacement that changes the silhouette (R-9); real-world units, stature to the vertex (R-13).
- **Builder-chosen values:** every numeric value not stated in canon is a **BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED** value and must be listed in the provenance record (R-14). It may shape the candidate; it can never become canon by measuring the candidate (§7 circularity rule).
- **Geometry/file form needed for measurement:** one triangle or quad mesh (OBJ, PLY, GLB, FBX or .blend) of the whole body in real-world units with a stated up axis; joint centres supplied as an armature or marker points (shoulder, elbow, wrist, hip, knee, ankle, plus spine and neck joints) built to anatomical joint centres; **separate eyeball meshes** (needed for orbit/eye-centre landmarks); head-region edge length about 0.3 cm or finer for craniofacial items; no hidden helper geometry; a SHA-256 or other immutable identifier recorded at hand-off.
- **Acceptance:** the candidate is inspected against R-1…R-14 and §6 by Claude (ARM acceptance record), then accepted or rejected by the author. Measurements stay DIAGNOSTIC.

**Packet notes:** **Correction, not a new design:** start from `RaceBodies/out/Marchfolk_Masc.blend` (sha256 d1dea7b6…). Required: (1) re-pose to R-6 by the rig (arms down from ~41° upper-arm abduction and ~47° elbow flexion; legs from ~7.6° thigh abduction to hip-width parallel) **with a check that no soft-tissue shape changes outside the joint regions**; (2) set the age macro to a mid-adult value (author to confirm the value; builder-chosen); (3) add eyeballs; (4) re-check stature after the stance change (the A-stance lowers it by about 0.6 cm). Inputs to list as builder-chosen: MakeHuman ethnic-mix weights (0.33 / 0.331 / 0.33), muscle 0.5, weight 0.5, proportions, height macro.

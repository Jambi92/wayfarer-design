# ARM Build Packet — MF-F-R: Marchfolk configuration 2 (rebuild)

**Order:** `reviews/chatgpt-reference-anatomy-wave1-execution-order.md` §4, §8
**Status:** BUILD REQUIRED. This packet is a specification, **not a mesh**. No measurement exists for this candidate.

| Field | Content |
|---|---|
| Population / candidate | Marchfolk configuration 2 (rebuild) |
| Reference stature | 173 cm |
| Sex-related configuration | Configuration 2, ordinary human sex-related anatomy |
| Frame / composition | Central skeletal values; reference composition (R-3, R-4) |
| Neutralization | N3 body; N-Head only for body tests that require it |
| Canon constraints the candidate must embody | As MF-M-R. **R-2:** stature must be reached by proportion, never by uniform scaling: the Iteration 3 candidate is MPFB's 159.05 cm default female **uniformly scaled ×1.0877 to 173 cm**, which fails R-2. |
| Comparison tests to pass | As MF-M-R; partner for PIP-BODY-29 / COG-BODY-14 like-for-like tests when those races have a matching configuration. |
| Measurements it unlocks | RM-UB-07 (central, configuration 2). |

- **Reference state** (`decisions/REFERENCE_ANATOMY_V1.md` §3): central-tendency adult (R-1); central skeletal values, not "Balanced" as a default (R-3); reference composition: population-centre muscularity and fat amount, neutral distribution, no regional offsets (R-4); zero natural asymmetry, bilaterally mirrored (R-5); measurement stance R-6 (upright; head neutral; arms hanging with a small fixed abduction, palms toward the thighs; feet hip-width, parallel, full plantigrade; hips and knees extended; neutral adult spinal curvature); N3 (R-7); no scalp, facial or body hair over landmarks (R-8); one neutral matte material, no displacement that changes the silhouette (R-9); real-world units, stature to the vertex (R-13).
- **Builder-chosen values:** every numeric value not stated in canon is a **BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED** value and must be listed in the provenance record (R-14). It may shape the candidate; it can never become canon by measuring the candidate (§7 circularity rule).
- **Geometry/file form needed for measurement:** one triangle or quad mesh (OBJ, PLY, GLB, FBX or .blend) of the whole body in real-world units with a stated up axis; joint centres supplied as an armature or marker points (shoulder, elbow, wrist, hip, knee, ankle, plus spine and neck joints) built to anatomical joint centres; **separate eyeball meshes** (needed for orbit/eye-centre landmarks); head-region edge length about 0.3 cm or finer for craniofacial items; no hidden helper geometry; a SHA-256 or other immutable identifier recorded at hand-off.
- **Acceptance:** the candidate is inspected against R-1…R-14 and §6 by Claude (ARM acceptance record), then accepted or rejected by the author. Measurements stay DIAGNOSTIC.

**Packet notes:** **Rebuild:** generate the female human at 173 cm through the height macro (not by scaling), same R-6 stance, mid-adult age, eyeballs. List builder-chosen inputs as for MF-M-R plus breast-size/firmness macros.

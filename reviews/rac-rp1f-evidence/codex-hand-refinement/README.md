# Gorrund hand refinement — Codex progress

Date: October 20, 2026 (America/Phoenix).

Status: **IN PROGRESS — VISUAL CANDIDATE, NOT A PRODUCTION FREEZE.**

## Author direction and scope

Tyler rejected the A/B/C mockups because the human hand/nail-bed anatomy remained too apparent and the claws were undersized relative to the digits. He approved the direction of separate finger and thumb studies, requested that direction on the full model, and then authorized refinement of the fingertip transitions and thumb attachments. Overall claw size is retained during this refinement.

Reference: `specs/gorrund/GORRUND_V1.md`, particularly Part 2 hand structure/dexterity constraints and the accepted stature writeback. The older ordinary-nail wording is not silently rewritten: Tyler's current claw direction governs this visual experiment. Native model scale is preserved; the 204.5225 cm source realization is not rescaled to the nominal race reference or used to revise the stature envelope.

## Completed checkpoint

- Separate Blender finger/thumb anatomy studies and same-scale comparison renders.
- Full-model visual candidate with ten separate keratin claw objects and locally reshaped distal housings.
- Source v015 SHA-256: `dfba363e534359193c63dc1700eb54d80f2ee34dbfa3a3cad06b5f87943e5e75`; verified unchanged after building the candidate.
- Saved candidate reopened successfully: 1,427,072 body vertices and 1,427,072 body quads; finite coordinates; zero quads below the checked near-zero-area threshold of 1e-14 square metres; ten claw objects.
- Recorded zero body vertices changed outside the explicit digit masks. This checks spatial isolation, not anatomical correctness or mesh quality.

## Current assessment and work

Tyler likes the overall direction and full-body read. Codex identified visible transition bands/creases, some pointed-cap appearance at attachments, and thumb placement that needs refinement. The next pass smooths those local transitions and deepens the root integration without changing the approved overall claw size.

Relaxed and controlled flexion visual studies will be used to inspect attachment behaviour. A procedural pose study does not establish production rigging, grip/contact validity, or collision-free animation.

## Outstanding gates

No claim of global self-intersection clearance, deformation/rig acceptance, T-6/T-7 acceptance, watertight union of the separate keratin objects, or production readiness. v014, v015, v015b and the frozen source remain protected. No Unreal changes. Turnfall is outside this work and untouched.

## Local review deliverables

Current files are in this Codex chat's `outputs` directory: `Gorrund_finger_thumb_anatomy_study.blend`, `Gorrund_fullscale_claw_visual_candidate.blend`, the comparison renders, and the saved-file check reports. Large Blender binaries are not included in this progress commit. Reproducible refinement scripts and compact review evidence will accompany the next checkpoint.

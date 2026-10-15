# RAC RM-OT-05Z1 — harden the single-body intake gate for scene-graph instancing

**Authority:** autonomous technical audit of RM-OT-05Z readiness; no author anatomy decision required.
**Date:** October 15, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent readiness:** `reviews/claude-rac-rm-ot-05z-single-image-input-readiness.md` (254de5a).

## Purpose

The 05Z readiness is accepted. The workflow remains stopped at the image gate because no candidate single-figure image exists.

Before a future GLB is trusted, harden `z_single_body_gate.py` so the "one organism" test is based on the active GLTF scene graph, not only unique mesh definitions.

Current blind spot: a GLB can contain one mesh definition instanced by multiple transformed nodes. Counting mesh primitives only once could incorrectly PASS a multi-body scene.

## Required additive correction

Update the gate so it:

1. resolves the active scene and recursively traverses its node hierarchy;
2. composes node transforms correctly from either `matrix` or TRS;
3. instantiates each referenced mesh primitive once per scene-node instance;
4. transforms POSITION data into scene/world coordinates before component and body-size analysis;
5. supports multiple mesh primitives in one body;
6. does not count unused mesh definitions that are not referenced by the active scene;
7. reports the number of scene nodes, mesh instances, primitives and body-sized connected components;
8. fails when more than one body-sized instance/component exists, including multiple nodes referencing the same mesh;
9. continues to list small disconnected pieces rather than silently dropping them.

For unsupported or ambiguous GLTF constructs that would make the result unreliable (for example unsupported primitive modes, malformed indices, unsupported sparse accessor handling), return a clear **REVIEW/FAIL-SAFE** result rather than pretending the single-body gate passed.

Do not mutate the GLB.

## Required tests

Preserve:
- 05X `Gorrund.glb` => PASS;
- 05Y `base_1.glb` => FAIL (3 body-sized bodies).

Add synthetic, committed self-tests:
- one mesh / one node => PASS;
- one mesh instanced by three translated nodes => FAIL with 3 body-sized bodies;
- one valid body plus a small disconnected accessory/component => single-body result remains identifiable, with the small piece explicitly listed;
- parent-child transform composition fixture => world-space bounds are correct;
- unused mesh definition not referenced by the active scene => ignored for body count.

If creating binary GLB fixtures would be unnecessarily heavy, a deterministic fixture-builder script plus expected JSON is acceptable, provided the test is reproducible from the repo.

## State

This is technical gate hardening only.

Do not:
- generate an image;
- submit Rodin;
- spend credits;
- alter Gorrund canon;
- extract a 05Y figure;
- begin anatomy review, ARM, LOW, blind, scaffold, Stage C, D4, UE5, rigging or creator implementation.

After committing the hardened gate and tests, remain:

**STOP AT IMAGE GATE / AWAITING SINGLE-FIGURE INPUT IMAGE.**

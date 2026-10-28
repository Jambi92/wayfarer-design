# Stage 1: cavern containment and navigation prototype - v026

A separate development copy repairs reproduced gaps at the large cavern's entrance junction and adds a working native minimap and compass. The junction now joins the reveal passage to the existing emergency branch while preserving the established travel routes. No approved level is replaced.

## Implemented scope

- The entrance neck has continuous rock surfaces and an intersecting branch connection. Only that mesh reference changes among the 912 existing blocking actors; their sets, transforms, collision profiles and responses are retained.
- This map opts into a separate walking inspection mode with normal collision, jumping, running and safe shortcuts to the entrance, grand chamber and descent stairs. Existing production modes, character models and rigs are unchanged.
- A round rotating local cave survey and heading compass display live enemy positions. Above/below chevrons and relative height labels distinguish other floors; separate entry/exit thresholds reduce indicator flicker near stairs. Zoom preserves positions, and distant enemies are omitted rather than moved to the rim.
- The survey uses existing floor geometry and established traversal lines. Its north currently follows the provisional local engineering grid; canonical world-map registration is not established by this work.
- The enemy adapter supports native monster actors and explicit marker components. Live checks used temporary targets, which were removed before saving. No permanent enemy placement, creature model, AI or combat encounter is added.

## Validation and continuation

The reopened level passed 1,168 boundary rays with no misses, including the eleven paths that escaped before repair. All 13 retained routes passed ground-height and applicable capsule probes. All 32 continuous walking/running legs passed for small and large diagnostic character sizes, followed by 27 real-time jumping and pushing attempts at the passage and sampled cavern perimeter. These bounded checks address the reproduced openings and sampled surroundings; they are not proof against every possible exploit.

Twenty native HUD checks passed, including moving targets, rotation, zoom, same-floor and above/below markers, elevation hysteresis, range limits and disabled/hidden/destroyed markers. All 104 flame fixtures retained their saved settings and supporting contacts. The reopened terrain matched all 4,068,289 accepted height samples, and the map check reported zero errors and warnings. Final native views were reviewed. Original project files and accepted v001-v025 checkpoints retained their hashes; every payload in the new compressed checkpoint was verified.

A fresh one-minute real-time editor sample with the new HUD active averaged 117.9 FPS with the existing frame cap in place. The local evidence retains frame-time details and any hitches. This static sparse-scene sample includes editor and profiling overhead; it does not establish shipping performance, crowded combat performance or whole-tutorial acceptance.

This completes a bounded containment repair and first working navigation display. Map artwork, enemy integration and final realistic cave art remain development work. The corrected prologue and quest sources remain authoritative. No new geography, lore, mineral identity or approved creature species is introduced. Only this prose milestone is published; project assets, screenshots, bibles and raw diagnostics remain local.

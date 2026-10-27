# Stage 1: natural cavern surfaces and flame lighting - v022

A separate Unreal development copy continues the cavern art pass while retaining the established traversal layout, excavation structures and provisional habitat gallery. The current cavern work lights now use flame lanterns and wall torches in response to the approved fantasy lighting direction.

## Implemented scope

- Broader, nonperiodic rock variation across the cavern walls, roof and off-route floor, with protected route elevations and portal joins retained.
- Varied hanging formations, mineral columns and smaller shelf-grown formations. Bases fit the supporting surface around their perimeter; unsuitable steep placements are excluded. Loose limestone rocks occupy supporting shelves away from walking routes.
- Revised limestone colour and dampness variation, longitudinal timber grain and darker weathered wood. The existing web and wrapped-debris study remains.
- Thirty-four iron flame lanterns and five wall-supported torches replace the current cavern fixtures. Moving flame silhouettes and gentle light-intensity variation use shared engine-time animation with staggered phase presets. Warm pools of light retain dark recesses and make excavation routes easier to read.
- Exposure and bloom adjustments stay inside the copied cavern volume. The older excavation network has not yet received this fixture conversion. No global project or exterior lighting settings change.

## Validation and continuation

The saved level and new assets reopen successfully. Native route probes, formation contact checks, terrain preservation checks and continuous walking/sprinting trials for both diagnostic character envelopes pass. The final flame materials and supported fixture placements survive reopening; fixed-camera play-mode captures show movement and changing illumination. The final native map check, real-time profiling sample and compressed checkpoint are verified locally before publication.

This is an incremental development-art milestone. Geological composition, material transitions, fire appearance and shadow polish still need further work before final realistic-art acceptance. Flame motion and brightness flicker are implemented; smoke, fuel, heat, fire spread and fire damage are not simulated. Working hoists, climbing, swimming, creature models, enemy AI, combat, quests and assisted evacuation are not implemented by this pass.

The corrected quest and prologue sources remain the narrative basis. Wider map registration and Cogling-specific pulley culture remain provisional. Character assets and accepted levels are preserved. No new lore, paid assets or imported reference photographs are introduced. Only this prose milestone is published; source geometry, screenshots, bibles and raw diagnostics remain local.

The light-intensity method follows Epic's [Light Functions documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-light-functions-in-unreal-engine).

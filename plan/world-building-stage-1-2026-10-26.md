# Wayfarer — World Building Stage 1: Canon-Grounded Terrain Graybox
Date: 2026-10-26
Status: IMPLEMENTATION BRIEF / PROPOSED, NOT A COMPLETED UE5 BUILD
Owner: ChatGPT (world building). Claude continues character models independently.
Scope: WAYFARER ONLY. Turnfall is out of scope.

## Sources and authority
- Canonical known-world map v0.2 and accepted World/Main Story/Race/Technical Bibles must be consulted before fixing positions or scale.
- Existing repo plan: `plan/terrain-and-race-models.md`. The UE level already reportedly has World Partition and a lake/crag/camps test area; preserve it.
- Approved design > decisions > prototype. Do not reinterpret lore or change regional placement to suit a technical shortcut.
- Never treat the rough illustrative heightmap or a builder's chosen coordinates as geographical canon.

## Stage-1 deliverable
A separate, reversible World Partition graybox level, with coarse terrain and water, major geography + region/story anchor markers, player traversal routes, and a reproducible validation log. No detailed vegetation, NPCs, combat, model integration or expensive asset purchases.

## Strict boundaries
- Do not edit Turnfall assets, content, repositories, maps, scripts or plugins.
- Do not alter Claude's character/body/rigging files.
- Do not overwrite an existing Wayfarer map or the current lake/crag/camps prototype. Back up / duplicate before editing.
- Do not run destructive project upgrades, migrations, build/cleanup, asset downloads, or bulk deletions without distinct review.
- Proposed world dimensions, sea level, landmark coordinates, partition cell size and regional borders remain OPEN until canonical map projection and playable-travel study. No invented distances.

## Phase gates
### WB-00 Inventory & environment baseline
Record project UE version, `.uproject` name/path, existing playable level(s), World Partition enabled+streaming settings, plugin set (Landscape, Water, PCG), available disk/GPU/RAM, source control and known working prototype.
Capture current playable level screenshot, World Partition minimap and git status or equivalent pre-change snapshot. If direct PC access unavailable, report BLOCKED; do not claim an Unreal build.

### WB-01 Canonical macro map registration
Digitize the Known World map v0.2 with labeled named regions into a **non-destructive source overlay**, recording image-space anchors separately from world-space coordinates. Include mountain spines, coastlines, major passes, watersheds, lakes, islands, and biome boundaries. Audit against story and language world canon.
Required story anchor: eastern-highland excavation between southern White Reach and northern Confluence, west of the sea. Keep Ember Isle predominantly wild/uninhabited, with only temporary Sagekin-led research/monitoring presence.
Output: anchor registry with ID, canonical source, coarse map position, uncertainty, and placement status. Coordinates stay TENTATIVE until scale approval.

### WB-02 Vertical slice graybox
Create new **Wayfarer-only** test level under e.g. `/Game/Wayfarer/World/WB_Stage1/`; prefer World Partition enabled with One File Per Actor and Data Layers. Do not replace the existing persistent world. Start with one bounded representative terrain test, preferably the excavation highland/Confluence transition, and iterate on slope, landscape water drainage, passes, roads, sightlines and movement. Choose a recommended Landscape import resolution only after deciding tile extent; see Epic Landscape Technical Guide.
Build an editor-only debug layer: region name labels, anchor markers, north reference, elevation and path readability indicators. Placeholder markers are not canon placements.
Make a documented temporary heightmap, if used, with import bit depth, size, Z scale, source/derivation, and reversible import.
No cliff overhangs forced into heightfields; reserve Nanite meshes for true sheer cliffs / caves.

### WB-03 Traversal/performance acceptance
Test walk and sprint and representative size/camera proxies (small/large race envelopes; never assume uniform scaling is final). Measure route length, travel times, slopes, entry/exit paths, climbability and sightlines; mark each as provisional until gameplay locomotion final.
Verify stream-in/out without major hitches, water collision, no landscape gaps, unloaded memory behavior. Establish baseline with Unreal Insights on actual target hardware; separately capture low / medium / high / ultra / ultra+RT decisions and provisional budgets. Avoid optimizing exclusively for high-end.
Use HLOD, Nanite only where suitable, PCG later; measure first.

### WB-04 Review and freeze
Deliver a map overlay, screenshots, graybox `.umap` reference and path, anchor/scale registry, measured performance+traversal log, unresolved decisions and rollback steps.
User approves world shape and test feel before expanding to the 40-region macro layout. Claude may independently audit geography and technical quality, but his character modeling work is not blocked by this.

## Initial practical execution order
1. Read project assets + map/Bibles; inspect actual UE project and protected working level.
2. Inventory current terrain/streaming and create a versioned backup.
3. Establish canonical anchor registry. Do not guess world dimensions.
4. Build **only a separate representative slice**, validate World Partition and import assumptions.
5. Share screenshots, route metrics, performance and proposed map scale for creative review.
6. After approval, grow macro geography by streamed tiles; vegetation and settlement detailing come later.

## Notes
- Prior terrain plan claims free ground assets are already downloaded to E: and used in overworld. Check the actual local file inventory before claiming they exist in the current project.
- Do not create a second UE project by accident. The Wayfarer-Blender ChatGPT project is a chat/workspace label, not evidence of a separate UE project.
- Stage 1 begins as design/preflight until an authorized local Work session can actually inspect or edit Unreal.

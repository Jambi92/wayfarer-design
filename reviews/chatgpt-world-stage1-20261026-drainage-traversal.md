# Stage 1 drainage and diagnostic traversal — 2026-10-26

Created a separate v003 development level with a shallow dry drainage channel alongside the provisional approach. The study remains 2.016 km square (4.064256 km²); its canonical placement and world-map scale remain provisional. Existing project levels and earlier checkpoints were preserved and hash-verified unchanged. Character modeling assets were not modified.

All 20 normal play-in-editor movement checks passed: five separate 100-metre sections for each combination of small/large capsule and walk/sprint. Capsule heights use the accepted 76 cm Cogling minimum and current 251 cm Gorrund upper test height. Capsule widths, movement speeds and step settings are diagnostic assumptions, not approved race controllers. Each case covered approximately 502 metres over the curved sections, with summed movement times of 167.65 seconds walking and 84.39 seconds sprinting. No falling was detected in the sampled movement diagnostics.

The sections are separated by teleports. These results do not establish continuous-route acceptance, reverse travel, final character movement or performance. World Partition streaming remained enabled, with the possessed walking capsule supplying the streaming source.

The saved map reopened successfully. All 306 Landscape collision samples, including drainage-center checks, matched the source heightmap within one millimetre. Inherited HLOD editor-placement helpers were excluded from these height checks; HLOD regeneration remains pending.

This is an early terrain graybox. The channel is dry; water simulation, limestone detail, finished materials, continuous bidirectional traversal, HLOD rebuilding and measured streaming/performance checks remain outstanding. Complete canonical map registration before expanding the study into approved geography.
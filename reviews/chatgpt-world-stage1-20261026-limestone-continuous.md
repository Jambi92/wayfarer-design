# Stage 1 limestone relief and continuous traversal

Added a separate v004 highland study with intermittent bedding ledges, shallow flank gullies and a slope-based grass/rock development material. The valley corridor remains unchanged from v003, and the provisional excavation shelf is protected. The technical footprint stays 2.016 km square; canonical placement and scale remain open.

All eight continuous northbound/southbound diagnostic legs passed. Each small/large capsule travelled approximately 1.72 km north and returned without a turnaround teleport, at both walking and sprinting settings. Ground collision remained present at the sampled checks, with no falling recorded on the accepted legs. The 76 cm and 251 cm height extremes follow the accepted race envelopes; widths, speeds and steps remain diagnostic assumptions.

| Case | Round-trip distance m | Game seconds | Max sampled lateral error m |
| --- | ---: | ---: | ---: |
| small_walk | 3431.4 | 1143.12 | 0.001 |
| large_walk | 3431.4 | 1143.12 | 0.001 |
| small_sprint | 3432.0 | 571.92 | 0.001 |
| large_sprint | 3432.0 | 571.92 | 0.001 |

These are accelerated play-in-editor diagnostics using a 3x game clock, not real-time performance acceptance or final character-controller validation. Walking and sprinting groups run separately with a possessed capsule supplying the World Partition streaming source. Streaming stayed enabled. The unused default pawn has collision disabled during the diagnostic.

After reopening, all 306 native Landscape collision samples matched the source heightmap within one millimetre. Inherited HLOD editor-placement helpers were excluded. Existing project files and earlier development checkpoints were hash-verified unchanged; character-modeling assets were untouched.

This remains an early terrain study. Excavation shelf access, final limestone meshes/materials, water, HLOD rebuilding, real-time streaming/performance measurements, final race controllers/cameras and canonical map registration remain outstanding before expansion.

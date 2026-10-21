# WAYFARER — TECHNICAL BIBLE
## Rendering, Scalability & Performance Requirements

**Version:** 1.0 — Approved foundational production policy  
**Approved:** 20 October 2026  
**Project:** Wayfarer only — never conflate with Turnfall  
**Authority:** Binding performance and scalability rules; numerical targets are provisional until tested on representative hardware.

### 1. Non-negotiable production mandate

**Performance is a design requirement, not a final polish task.** Every environment, playable race, NPC, creature, gameplay system, animation, VFX effect, audio component, and cinematic must be built and continuously profiled with hardware efficiency in mind. Visual fidelity must be balanced against measurable CPU, GPU, memory, streaming, and frame-time costs. We must not finish the world first and expect a rescue optimization pass at the end.

The intended finished experience is visually impressive, stable, readable, configurable, and enjoyable on a broad range of realistically supported PC hardware. High-end rendering features may enhance the presentation but cannot be prerequisites for gameplay or world comprehension.

### 2. Graphics preset architecture

| Preset | Intended experience | Rendering policy |
|---|---|---|
| **Low** | Maintain playable performance on supported lower-end systems | Reduce shadow quality, foliage density, view distance, effects, reflections and expensive post-processing without obscuring information |
| **Medium** | Balanced fidelity/performance on modest gaming PCs | Moderate geometry/foliage density, reasonable lighting and effects |
| **High** | Principal visual and performance tuning baseline | Rich environments and strong image quality without mandatory hardware ray tracing |
| **Ultra** | Best conventional fidelity on capable hardware | Higher-quality shadows, foliage, reflections, effects and draw distance within measured budgets |
| **Ultra + Ray Tracing** | Optional premium experience on compatible hardware | Hardware ray-traced capabilities only where supported, stable, and visually worthwhile; never the sole functional lighting path |

Implement separate player-accessible settings for resolution, rendering/upscaling scale, shadows, textures, foliage, draw distance, effects, reflections, post-processing, antialiasing, motion blur, frame limit, V-Sync and ray tracing when available. Provide clear Apply/Restore Defaults controls and safe fallback for unsupported settings. Preset values are starting points; advanced individual settings may override them.

### 3. Provisional performance objectives

- **Low at 1080p:** pursue a stable **30 FPS** floor on eventual minimum supported hardware (approximately 33.3 ms per frame).
- **High at 1080p:** pursue **60 FPS** on eventual recommended hardware (approximately 16.7 ms per frame).
- **Higher resolutions, high refresh rates, Ultra, and optional hardware ray tracing:** additional goals for suitable hardware, not minimum release requirements.
- Profile **frame-time consistency** (including stutter, streaming hitches, and low-percentile performance), not only average FPS.
- Do not publish specific minimum/recommended GPUs, VRAM limits, CPU models, or fixed per-region numerical budgets until representative content and benchmarks substantiate them. These objectives may be revised through documented evidence.

### 4. Ray tracing, lighting and upscaling

Hardware ray tracing is **optional**, off or hidden on unsupported devices, and validated separately. Build an attractive, readable non-ray-traced path using suitable Unreal Engine lighting options and quality levels. Evaluate Unreal Engine 5 Lumen/software or hardware implementations, shadows, reflections and other ray-traced features feature-by-feature; never enable everything by default merely because it exists.

Support Temporal Super Resolution or a comparable supported baseline; evaluate optional vendor upscalers and frame-generation technologies only when compatible, stable, licensed where necessary and tested for artifacts, latency and frame pacing. Frame generation must not be used to disguise poor native responsiveness.

### 5. Continuous optimization during production

**World / streaming.** Use World Partition and hierarchical LODs where appropriate; stream nearby environments, unload unneeded content, and test traversal across cell/region boundaries. Do not keep the entire open world resident. Validate NPC and AI simulation budgets separately from rendering.

**Geometry / characters.** Use Nanite selectively where appropriate; use conventional LODs or alternate strategies where more efficient or better supported. Enforce sensible mesh complexity, skeletal mesh/animation budgets, instancing, visibility culling and material complexity. Race/character variation must not bypass the performance standards.

**Foliage / environment.** Set foliage density, wind/animation, shadow casting and view distances by preset. Profile dense forests, grass, water, weather, nighttime scenes, settlements and extreme vistas; avoid overdraw and expensive transparent materials where possible.

**Textures / VRAM.** Use texture streaming, appropriate mipmaps, optimized materials and platform-targeted compression. Monitor residency, pool pressure, memory spikes, shader compilation/stalls and asset loading behavior across presets.

**Combat / VFX / audio.** Budget particles, lights, projectiles, destruction, summoned entities, crowd/AI behavior and audio concurrency. Test overlapping spells and enemy abilities, not isolated effects in an empty test map.

**Cinematics.** Optimize cinematic assets and lighting; validate that transitions between gameplay and cutscenes do not cause unacceptable memory spikes or loading hitches.

### 6. Profiling and regression process

1. Capture repeatable benchmark scenes and representative player paths early, including wilderness traversal, dense cities, heavy foliage, multiple enemies, spell-heavy battles, weather and nighttime.
2. Record CPU game/render thread times, GPU frame time, total frame times, 1% lows/frame-time distribution, stutter/hitches, VRAM/system memory, streaming and load behavior. Use Unreal Insights and Unreal's CPU/GPU profiling facilities.
3. Compare all major presets on at least one supported low-end, recommended and high-end class of hardware when those baselines become available. Ray tracing ON/OFF must be compared on compatible systems.
4. Every substantial content or engine/rendering change gets a before/after performance check. Log regressions, causes, fixes, and benchmark build identifiers alongside visual comparisons.
5. An area or feature is **not technically complete** until it passes its current frame-time, memory, streaming, stability and readability acceptance criteria. Significant regressions block further expansion until triaged or explicitly documented as temporary prototype exceptions.
6. Revalidate across representative playable races, cameras, encounter sizes and movement speeds; use packaged builds and realistic workloads, not editor frame rates alone.

### 7. Gameplay visibility and fairness — absolute rule

Low or reduced graphics settings may lower visual detail, but must **never** obscure required attack telegraphs, targeting indicators, hazards, interactables, essential navigation cues, dialogue readability, or quest-critical information. Ray tracing, ultra shadows, high-quality reflections and dense foliage must not grant unfair gameplay knowledge or conceal threats on other presets. Preserve accessible contrast and clear visibility during dark, foggy and particle-heavy scenes.

### 8. Authority, ownership and review

- **Applies to:** Wayfarer World, Character/Race, Combat/Class, Creature/Enemy, Cinematic, UI and Audio workstreams. All teams/tools must refer back to this Bible when creating content.
- **Status:** The optimization-first mandate, scalable presets, optional ray tracing and gameplay readability requirements are approved. Specific rendering technologies, numeric hardware specifications and tuning values remain implementation decisions subject to profiling.
- **Gate:** Every new region, character population, effect system and combat encounter must meet repeatable scalability tests before signoff.
- **Review cadence:** Evaluate performance continuously during implementation, at each milestone/vertical slice, after major engine upgrades, and before alpha/beta/release gates.
- **Canon separation:** This document governs Wayfarer only. No setting, asset, repo or implementation detail from Turnfall may be imported by assumption.

### 9. Change log

- **v1.0 — 20 October 2026:** Initial binding optimization-first development philosophy, graphics presets, provisional 1080p performance objectives, optional ray tracing, profiling workflow, and gameplay-equivalence constraints approved.
# Wayfarer Terrain & Race Models Plan

Sep 30, 2026 · @Tyler

Build the world on Unreal's own landscape tools with slope-driven rock and grass. Build the races to the agreed character and race brief (Character Creation & Race Design). The approved racial anatomy sets the technical architecture, and no technical foundation for any race has been chosen yet.

## Terrain

The level already uses World Partition, so a large landscape streams in pieces as you travel. The land comes together in five steps:

1. **Heightmap.** Shape the big landforms (valleys, ridges, mountain spines) in a free terrain generator such as Gaea's community edition, or sculpt them directly with Unreal's landscape tools. Export one 16-bit heightmap and import it as the landscape.
2. **Auto-material.** One landscape material paints itself by slope and height: grass and dirt on flat ground, scree on medium slopes, bare rock on anything steep, snow above a set altitude. No hand-painting needed for a first pass.
3. **Cliffs.** Landscapes can't do overhangs or sheer faces, so real cliffs are rock meshes (Nanite, so they can be very detailed) set into the slopes. This is where ledges for the fall system come from.
4. **Foliage and scatter.** Unreal's procedural tools (PCG) place trees, grass, bushes and loose rocks by rules such as "pines above 400 m, none on steep rock".
5. **Hand passes.** Towns, roads, dungeon entrances and the portal sites get placed and flattened by hand on top.

The test lake, crag and camps stay where they are until the real zones replace them.

## Art sources and cost

Free CC0 textures cover the ground; paid Megascans are worth it mainly for hero cliffs. Megascans stopped being free for Unreal projects at the end of 2024, but anything claimed during 2024 is yours forever ([CG Channel](https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/)).

| Source | What it's good for | Cost | License |
| --- | --- | --- | --- |
| Poly Haven, ambientCG | Ground, dirt, rock and bark textures for the auto-material | Free | CC0, any use |
| Quixel Megascans on Fab | Scanned cliff and boulder meshes, the best-looking rock available | About $0.99 per asset, $4.99 per kit, $24.99 per pack | Fab Standard License |
| Fab's free-of-the-month assets | Occasional environment packs | Free when claimed in their window | Per asset |
| Epic's free sample projects | Foliage, rocks and materials from Epic's own demos | Free | Unreal projects only |
| Gaea community edition | Heightmaps for the landscape shape | Free | Check before selling the game |

Free assets were downloaded to E: on September 30 (Poly Haven textures and models, now on the overworld landscape). Paid assets wait for your review.

## Race models

No race has a committed technical foundation yet. The table lists **candidate** foundations only, each needing anatomical validation against that race's approved spec. MetaHuman is a strong candidate for the human races: it's built into Unreal since 5.6 and free for studios under $1 million a year ([CG Channel](https://www.cgchannel.com/2025/06/you-can-now-sell-metahumans-or-use-them-in-unity-or-godot/)), and since 5.7 its bodies round-trip through Blender or ZBrush with skeleton fitting for extreme shapes ([MetaHuman](https://www.metahuman.com/news/metahuman-5-7-brings-major-improvements-to-body-conforming-with-more-to-come)). Custom, modified or hybrid solutions stay possible for every race.

| Race | Height (spec) | Candidate technical foundation (not approved) | Design status |
| --- | --- | --- | --- |
| Marchfolk | 147–173–203 cm | MetaHuman: candidate, needs validation against the Marchfolk spec | v1.1–v1.4 received (v1.0 and v1.5 not yet) |
| Skarn | 183–208–229 cm | MetaHuman with body conforming: candidate. It must meet Skarn skeletal robustness without uniform scaling | First pass complete |
| Sagekin | 152–178–208 cm | MetaHuman: candidate, needs validation against the Sagekin spec | First pass complete |
| Fenn | 157–181–211 cm | MetaHuman or a modified MetaHuman approach: candidate only, requiring anatomical validation. Custom or hybrid solutions stay possible | First pass complete |
| Aelari | \~1.10× (brief) | Open. Not assumed to match Fenn, and decided after the Aelari design pass | First pass complete (168–190–221 cm) |
| Vael | \~1.05× (brief) | Open. Not assumed to match Fenn, and decided after the Vael design pass | v1.0 complete (157–178–203 cm) |
| Halvren | \~0.98–1.03× (brief) | Open. Depends on the human, elven and mixed-ancestry architecture | Not started |
| Durrim | \~0.65× (brief) | Open. Candidates include a MetaHuman-derived mesh on a race-specific skeleton, or a custom body | Not started |
| Grask | \~1.15× (brief) | Open. Candidates include MetaHuman fitted to a sculpt, or a custom body | Not started |
| Gorrund | \~1.45×+ (brief) | Open. Candidates include MetaHuman fitted to a sculpt, or a custom body | Not started |
| Pipkin | \~0.55× (brief) | Open. A custom body is a likely candidate | Not started |
| Cogling | \~0.45× (brief) | Open. A custom body is a likely candidate | Not started |
| Saurin | \~1.05× (brief) | Open. A custom body with tail bones is a likely candidate | Not started |

Candidate sources for custom bodies include Fab creature assets, a commissioned artist or in-house sculpting. Any source must meet the race's approved anatomy, and none is chosen.

## Architecture principle and status labels

**Character design requirements determine technical architecture.** Technical convenience never redefines approved racial anatomy without an explicit design review. Possible future solutions include MetaHuman, modified MetaHuman workflows, shared skeletons, modified or shared hierarchies, race-specific skeletons, custom meshes, morph and deformation systems, retargeting, procedural adjustment, IK and hybrids. No final choice is made now.

**Authority rule:** Approved Design Specification > Open Decision Register > Prototype Implementation. Existing implementation never overrides an approved spec and never resolves an OPEN item by existing. Prototypes may stay even where they differ from the target, and working prototypes aren't refactored to match evolving design unless implementation work is explicitly authorized.

Every statement in this plan belongs to one of four categories, and they are never interchangeable:

| Label | Meaning |
| --- | --- |
| CURRENT IMPLEMENTATION | What exists in the UE5 project today |
| TARGET DESIGN | Approved requirements the completed system must support |
| OPEN DECISION | Something intentionally unresolved |
| CANDIDATE TECHNICAL APPROACH | A possible solution, not approved architecture |

**CURRENT IMPLEMENTATION (placeholder).** All races use the same human mannequin and the same human animation set, with uniform whole-actor scaling per race and per height step. This is acceptable as a temporary prototype. It is not the approved final animation or body architecture for any race.

**TARGET DESIGN REQUIREMENT.** Each playable race must eventually be validated against its approved anatomy for locomotion, animation, IK, interactions, combat, equipment, and climbing, swimming and mounts where supported, plus other relevant movement systems. The solution may use shared animation, retargeting, procedural adjustment, IK, race-specific animation or a hybrid. That choice isn't made yet.

**No premature refactor.** The shared human animation system stays in place. Skeletons, animations, MetaHumans and character assets aren't rebuilt until the anatomical specs and technical prototypes justify a change.

## Known gaps and open decisions (pre-Aelari audit, complete)

The pre-Aelari conflict audit is complete as of September 30, 2026. Every item is a documented known gap or open decision, not an implementation task. Nothing here authorizes changes to meshes, skeletons, animations, scaling, stats, class restrictions, save data, collision, cameras or weapons. The audit exists so that prototype implementation never silently dictates final design.

| # | Current implementation | Classification | Target design or resolution |
| --- | --- | --- | --- |
| 1 | "Frame" switches between the Manny and Quinn mannequins | CURRENT PLACEHOLDER, incompatible with target design | May stay for now. The final system keeps amendment v0.1's four layers (anatomy, frame, composition, presentation), and Narrow, Balanced and Broad never simply mean Manny or Quinn |
| 2 | Saved appearance holds only frame, height step, two colors and finish | CURRENT PLACEHOLDER, requires future expansion | Stays unchanged for now. Future data supports the unified appearance architecture with schema and version tracking plus migration. Serialization isn't redesigned yet |
| 3 | Personal height is ±7.5% (about 160–186 cm for Marchfolk) | CURRENT PLACEHOLDER, superseded by approved race specs | Not authoritative. Marchfolk stays 147–203 cm (provisional), and each race owns its range. No implementation change yet |
| 4 | Height and race size are uniform whole-body scaling | CURRENT PLACEHOLDER, incompatible with target anatomy | May stay temporarily. The final height and proportion system is race-aware and anatomical, not whole-character scaling |
| 5 | Race scale values (for example Fenn 0.95×, Cogling 0.72×, Gorrund 1.22×) | CURRENT IMPLEMENTATION ONLY, not authoritative design data | These values never constrain racial anatomy, and the race specs are the design targets. Values unchanged for now |
| 6 | One actor scale drives weapons, capsule, camera and reach | MAJOR FUTURE ARCHITECTURE REQUIREMENT | Visual anatomy, equipment dimensions, collision, interaction reach, combat reach and camera placement are separated conceptually. Canonical equipment dimensions never scale with the holder. Individual cosmetic variation within a race gives no automatic gameplay effect. Whether major racial size differences affect gameplay is an OPEN BALANCE DECISION |
| 7 | Racial attribute bonuses (for example Sagekin Intelligence 107, Skarn Strength 103) | OPEN GAMEPLAY DESIGN DECISION | Not automatically canon. The Sagekin Intelligence bonus is especially under review, since scholarship is cultural. Racial gameplay differences needn't all disappear, and Skarn anatomy may justify some. A future Race → Biology → Gameplay Attributes Review will separate biology from culture, background, training and class. Stats unchanged |
| 8 | Race and class restrictions are built in | CURRENT IMPLEMENTATION EXISTS, final design OPEN | Not removed and not approved. They stay in the Decision Register |
| 9 | Race descriptions present culture as biology (Sagekin "soft hands", Skarn "trust muscle over books") | DESIGN TEXT REQUIRES FUTURE REVISION | Creator descriptions must distinguish ancestry from culture and reputation. Those lines may survive as reputation, stereotypes, sayings or biased viewpoints. Neutral, in-world or both is an OPEN DECISION |
| 10 | All races share human animations at uniform scale | ACCEPTED CURRENT PLACEHOLDER | Stays unchanged. Not the final animation architecture |
| 11 | Skarn 1.5× breath, Fenn sneak and swim bonuses | EXISTING IMPLEMENTATION FACT, aligned with design | Kept, and still open to later balance review |

Future work items this audit adds (none authorized yet): the Race → Biology → Gameplay Attributes Review, versioned appearance data with migration, and the race-description rewrite.

## Candidate engine approaches for the character direction

Your three layers fit how Unreal builds characters. The key rule is that sliders drive a small set of anatomical controls, not mesh regions directly. Unreal's Mutable plugin is built for this kind of runtime customization. It generates skeletal meshes, materials and textures at runtime, has shipped with the engine since 5.5, and its sample project is free on Fab ([Epic](https://www.unrealengine.com/news/the-mutable-sample-project-is-now-available)).

| Your layer | What it controls | Candidate approach (not approved) |
| --- | --- | --- |
| Race | Skeleton, proportions, skull, anatomy, tail and ears, center of gravity | A base body and skeleton per race. Core bones keep shared names so animation retargets; extras (tail, ears) are added bones. Saurin may need its own hip and leg layout. |
| Race | Movement | A locomotion set per race (clips plus speed, acceleration, turn rate and braking). The game already swaps clips from a table, so this becomes one table per race. |
| Race | Height and mass range | Per-race limits on every slider, plus capsule, hitbox and camera height scaled from the result. |
| Individual | Body sliders (height, weight, muscle, fat, widths) | A few high-level controls drive many body-shape morphs and bone lengths together. More muscle widens shoulders, neck and arms at once, and height changes limb proportions, not a uniform stretch. |
| Individual | Face sliders | Face shape morphs within per-race ranges, plus small asymmetry offsets. |
| Individual | Age | One value that drives face and body morphs, skin detail, hair greying, a posture layer and a small change to movement speed and stride. |
| Individual | Skin, hair, marks | Material settings (tone, freckles, scars, tattoos) and swappable hair meshes. |
| Presentation | Clothing, armor, jewelry | Gear made per race body. Mutable can bend it to fit each character's sliders. |
| All | Saving and multiplayer | One compact appearance record (race plus slider values) that saves and replicates. The game already has a small version of this. |

This lets a muscular Fenn stay recognizably Fenn: the Fenn skeleton, face base and movement set stay fixed, and the sliders only move within Fenn limits.

## What each race design should pin down

Superseded by the brief's 14-point race specification (§20, next tab). Kept for reference:

- [ ] **Height range** for males and females, in feet or cm (the game's placeholder scales run 0.7× to 1.22×; the brief's references run 0.45× to 1.45×+)
- [ ] **Build:** slim, average, stocky or massive, plus arm and leg length compared to a human
- [ ] **Head:** ear shape, nose, jaw, brow, tusks, horns, snout
- [ ] **Skin, hair and eye palettes:** the range of colors the character creator should offer
- [ ] **Body covering:** smooth skin, hide, scales or fur, and any markings
- [ ] **Extras** that need their own bones or physics: tails, long hair, beards, ears that move
- [ ] **Posture:** upright, hunched or forward-leaning (Grask and Saurin especially)
- [ ] **Reference images:** two or three pictures per race, to show the look you're after

A race whose body plan differs a lot from a human's (long arms, a tail, a hunch) will need its own tuned animations later. Worth weighing when you decide how far from human each race goes.

## Order of work

1. Together: Marchfolk Character Customization Specification v1.0.
2. The other races in the brief's phase order: Skarn and Sagekin; the elves and Halvren; Durrim, Pipkin and Cogling; Grask and Gorrund; Saurin.
3. Character-creator plumbing (each race loads its own body, mannequin stand-in). On hold until the specs are agreed.
4. A Marchfolk technical prototype tests the pipeline end to end: creator, animations, and gear sitting correctly on the body. MetaHuman is the leading candidate but isn't approved. Other races follow only once their anatomy validates against a chosen approach.
5. In parallel: a first terrain zone (heightmap, auto-material, a few cliffs) near the start, replacing the test area.

## Open questions

- Did you claim Megascans on Fab during 2024? If so, those are free to use.
- Which region should the first real zone be (forest, plains, mountains, swamp)?
- For the four custom races: buy Fab assets, commission an artist, or try sculpting yourself?
- The brief's own open points (sex and body type, first-person, race and class limits, culture, size in combat) are listed at the end of the next tab.

## Sources

- [Epic has made Megascans free to all, but only until the end of 2024](https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/) (CG Channel)
- [You can now sell MetaHumans, or use them in Unity or Godot](https://www.cgchannel.com/2025/06/you-can-now-sell-metahumans-or-use-them-in-unity-or-godot/) (CG Channel)
- [MetaHuman 5.7 brings major improvements to body conforming](https://www.metahuman.com/news/metahuman-5-7-brings-major-improvements-to-body-conforming-with-more-to-come) (MetaHuman)
- [The Mutable Sample Project is now available](https://www.unrealengine.com/news/the-mutable-sample-project-is-now-available) (Epic)

## Playtest feedback, September 30 (queued until the race designs are finished)

- **Better now:** swimming animation, crossbow aiming pose, throwing animation.
- **Swim-to-ramp exit:** the character still swims on land for a second or two before standing up.
- **Crossbow turning:** big delay in the character turning to keep up when looking side to side while aiming.
- **Greatsword heavy overhead swing:** still wrong; the blade stays vertical the whole time instead of extending outward through the arc.
- **Fall landings:** look janky overall; the 4–8 m roll doesn't actually roll.

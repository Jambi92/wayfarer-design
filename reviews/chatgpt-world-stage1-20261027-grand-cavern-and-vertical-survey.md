# Stage 1: grand cavern and vertical survey study — v020

A separate Unreal development copy expands the excavation into a substantially larger underground space, responding to the requested natural chambers, deep pits, underground water, vertical work sites and room for tutorial combat.

## Implemented scope

- A provisional cavern envelope approximately 110 by 80 metres, with roughly 80 metres of total floor-to-ceiling relief and a deep central pool. This remains a technical layout study within the existing highland test slice, not a change to the Known World Map v0.2.
- A fitted branch from the existing cave network, an upper encounter shelf, a dry blind habitat gallery, and a lower survey landing reached by a guarded 120-step staircase. The staircase descends approximately 15 metres using 12.5 cm risers and 15 cm treads; final foot placement and animation still require controller work.
- Visible cargo-hoist study with sheave, axle, lifting lines, load platform and counterweight; an optional ladder and elevated survey shelf. These are visual prototypes, without hoist operation or climbing interactions.
- Original cave meshes, columns, hanging formations, embedded rock masses and ordinary survey lamps. The deep water remains cosmetic.

Large spiders are the user-requested working encounter direction. The encounter shelf and habitat gallery provide space to develop that direction; this milestone does not add creature models, AI, combat, spawning, completed nest dressing or tutorial quest logic. Character work remains separate.

## Reference direction and canon boundaries

Reference pages: [Carlsbad Big Room, USA](https://www.usgs.gov/media/images/carlsbad-caverns-big-room), [Postojna Cave, Slovenia](https://www.postojnska-jama.eu/en/postojna-cave/), and [Padirac descent, France](https://www.gouffre-de-padirac.com/en/prepare-my-visit/your-questions). These informed chamber scale, formations, water and vertical traversal. No reference photographs were imported as game textures or redistributed.

The reviewed Cogling anatomy specification permits engineering as a cultural or occupational practice; it does not establish pulley-specific cultural canon. Excavation hoists follow the user's requested working direction, with cultural attribution left provisional. No biological engineering aptitude is inferred.

The corrected main quest script and prologue implementation material remain the narrative basis. The full prologue includes road, camp, investigation and escape as well as underground traversal; a larger chamber alone does not establish complete tutorial pacing. Assisted evacuation and narrative state acceptance still require implementation.

## Validation and remaining work

All 32 continuous Character trials passed across the reveal, habitat gallery, staircase and existing emergency route: both size envelopes, walking and sprinting, outward and return. Native saved-geometry checks cover all ten retained routes plus the three new routes. The reopened level reports zero map-check errors or warnings. Only a copied emergency-wall mesh reference changes among the earlier 717 colliders; their transforms and collision responses remain intact. The original terrain heightmap and all prior accepted project checkpoints remain unchanged. A separate compressed checkpoint is retained locally; only this prose milestone is published. The milestone is a spatial and traversal study. Natural rock sculpting, lighting composition, realistic surface finish, habitat dressing and playable encounter pacing remain further work; this is not a final art acceptance.

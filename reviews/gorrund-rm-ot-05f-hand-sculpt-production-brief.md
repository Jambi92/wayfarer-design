# Gorrund hand-sculpt base mesh — production brief (RM-OT-05F)

**Authority:** `reviews/chatgpt-rac-rm-ot-05f-gorrund-hand-sculpt-handoff-stage-c-order.md` (author decision after RM-OT-05E).
**Status:** **FROZEN** for external / direct sculpt production (`reviews/chatgpt-rac-rm-ot-05f-handoff-author-ruling-freeze-order.md`): Q1 approved and the waist wording corrected (§3, §4A, §5, §8). Family intents and validator thresholds may change only if a genuine conflict with locked canon is shown. Gorrund: **EXTERNAL SCULPT REQUIRED — AWAITING ASSET**.
**Purpose:** handoff brief for an external sculptor or a direct mesh-edit workflow. Nothing in this brief is canon. It does not change, extend or replace `specs/gorrund/GORRUND_V1.md`; where this brief and canon differ, canon governs and the difference is listed in §3 for the author.
**Package:** `reviews/rac-rmot05f-handoff/` (start mesh, guide meshes, joints, stations, region masks, figures, evidence index).
**Validation:** `tools/rac/w1/rmot05f_drivers/` (re-entry validator and blind-gate runner; §9–§10).

## 0. What is being asked for

**The asset.** One hand-sculpted Gorrund body surface, delivered as a displaced copy of the supplied start mesh (same vertices, same order, same faces).

**What it must do.** Make the accepted Gorrund skeleton read, body only, as a **distinct upright plantigrade humanoid race** through **hard-form anatomical organization**:
- planes, plane breaks, edges;
- bony and tendinous landmarks;
- section shapes.

**What it must not rely on.** A heavy human body can always explain extra fat, extra muscle, more width or a bigger silhouette. That is why every procedural attempt (05C, 05D, 05E) failed: the reads were "heavy human" or depended on what else was in the set.

**What happens to it afterwards.** The sculpt is not used directly as a game asset. The pipeline converts it into a displacement field on the accepted skeleton route. That field is then carried to every composition state (low to high muscle and fat), every Frame (Narrow / Broad) and both rig poses. So the forms must be **structural**: they must survive when the body underneath gets leaner.

## 1. Deliverable specification

| Item | Requirement |
|---|---|
| Start mesh | `template/GO_ref_route_r6.obj`: the unorganized accepted-route Gorrund reference body, 230.90 cm, reference composition, R-6 neutral stance. Sculpt on this mesh. |
| Delivered file | `GO_sculpt_<ID>_r6.obj`: the start mesh with moved vertices only. |
| Topology | **13 380 vertices in the template's exact order. Faces identical.** No added, deleted, welded, split or reordered vertices. No remesh, Dynamesh, Sculptris / dyntopo or retopology on the delivered level. |
| Subdivision | Allowed while working. Deliver the **base level** with the forms projected down. A matching high-resolution level (displacement or normal map, or a subdivided mesh) may be delivered *in addition* for later texture work. It is not validated here. |
| Units / axes | Centimetres (1 unit = 1 cm). **Z up**, ground plane z = 0, **+Y anterior** (the body faces +Y), **+X = the body's left side**. Do not re-centre, re-ground or re-scale. |
| Pose | R-6 neutral stance exactly as supplied. Do not re-pose any limb, the trunk or the head. |
| Untouched zones | Head and neck, hands and digits, toes and forefoot must stay within **0.5 cm** of the start mesh (`data/regions.json`, `NO_TOUCH_*`). The head is integrated later in the race pipeline. |
| Hard limit | No vertex inside `template/GO_true_floor_r6.obj` (the 05D true skeletal floor) by more than 0.2 cm. |
| Exporter notes | OBJ, positions only (`v`, `f`; `vt` / `vn` are ignored). Blender: import with *Keep Vert Order* (Split: off); export with *Apply Transform* and no axis conversion that would move Y or Z; scale 1.0. ZBrush: work on a duplicate subtool, then *Project All* down to the lowest level before export. |
| ID | A two-character ID (e.g. `S1`, `S2`) per delivered version. Every delivery is re-validated in full. |

## 2. Locked constraints

These may not be traded for readability.

**Skeleton** (not read from the sculpt; the pipeline keeps the accepted one):
- accepted Gorrund skeleton, joint centres, long-bone axes and bone scales (05B `cfg_final` route; joints in `data/joints_r6.json`);
- no uniform whole-body scale;
- no change of stature: 230.90 cm reference (low composition 230.75 cm). The accepted range is about 208–251 cm; it is OPEN in canon and is carried by the skeleton route, not the sculpt.

**Pose and anatomy:**
- R-6 neutral stance;
- no posture trick: no crouch, no bent knees, no hunch, no forward lean, no exaggerated lumbar arch, no apparent digitigrade leg made of soft-tissue forms;
- plantigrade feet; five digits per hand and foot; human-compatible hands and feet (not monster paws, not oversized feet).

**Protected relations,** read on the skeleton at skeleton-anchored stations (05D semantics; 05E author ruling 2). The sculpt cannot change them; the validator confirms they are unchanged.

| Relation | Value |
|---|---|
| bitrochanteric ÷ iliac crest | 1.1846 |
| pelvis ÷ thorax breadth | 1.0234 |
| pelvic depth ÷ thoracic depth | 0.8570 |
| S4 ÷ S2 breadth | 0.8391 |
| S3 ÷ S2 depth | 0.9187 |

(`data/stations.json`.)

**Pipeline semantics:**
- **Volume.** The sculpt's surface volume change is reported, then restored to the route's composition amount by the 05D even layer. The sculpt moves form; it does not change how much tissue there is.
- **True floor.** The 05D true floor is the only hard inner limit.
- **Old guard.** The old MPFB `-LEAN` (`template/GO_old_lean_r6.obj`) is context only. The sculpt *may* go inside it, down to the true floor.

**Rig and systems:**
- MPFB / R-6 rig compatibility; Frame (Narrow / Broad) and composition systems unchanged.

**Never the identity:** fat or muscle amount, clothing, hair, texture, pigmentation, scars or face.

## 3. Canon guardrails for the hard-form families

The six families below come from 05E §10 and order 05F §4. Canon (`specs/gorrund/GORRUND_V1.md`, Part 2) bounds several of them. The sculpt must satisfy **both**. The reading in the right-hand column is how this brief reconciles them. **Q1 is approved by the author** (freeze order §2); it is an interpretation of existing canon, not new canon.

| Family wording (05E / 05F) | Canon clause (GORRUND_V1 Part 2) | Sculpt reading |
|---|---|---|
| A: "planar / faceted slab", "defined lateral edges" | Thoracic cross-section: "**Anatomically shaped, never circular, rectangular or boxy**"; thoracic depth "never a cylindrical barrel chest" | **Q1 — APPROVED.** *Planar anatomical zones and plane breaks are allowed and desired, but they must exist on an anatomically shaped, radiused thoracic cross-section. "Planar" describes surface organization, not a rectangular body section.* Allowed: broad planar anatomical zones; strong but radiused plane breaks; a legible sternal / anterior plate; legible lateral thoracic planes; an anatomically organized hard-form section. Not allowed: rectangular, boxy, mechanically slab-sided, or circular / cylindrical. Corners stay radiused and vary along the height; the flats are broad anatomical planes (sternal plate, lateral thoracic wall), not machined faces. 05E P1–P3 used a box section, which this clause excludes. They failed anyway and are not references. |
| A: "no waist hollow" (corrected, freeze order §3) | Waist "varies within valid anatomy; narrower isn't human or bodybuilder, broader isn't obese"; GO-P6 "waist definition allowed" | *The **reference sculpt** must not rely on a human-style pinched waist or waist hollow as the Gorrund readability cue. Existing canon-valid waist variation remains available through the established Frame / composition system.* This is **not** a race-wide biological rule: it does not prohibit waist hollowing in Gorrund, and nothing in the Frame / composition system is changed to enforce a waist shape. |
| A: "crisp lower structural border" | Abdomen: "no 'ogre belly'"; "thoracic skeletal depth stays separate from abdominal soft-tissue projection" | The border is the costal / sternal structure (skeletal), not a belly overhang. No abdominal protrusion as the read. |
| B: "hard transverse sacral border", "continuous sacral → hamstring path" | GO-P1: sacrum broad and robust, "no exaggerated lumbar arch"; spine: "without permanent forward lean, exaggerated lumbar arch or hunch" | Straight or inclined posterior line, no lumbar hollow, no hump. The paraspinal columns are broad and low, not a ridge. |
| C: "structural hip plate", "trochanteric shelf", "defined step" | GO-P2b: "no lateral outrigging"; GO-P3: iliac crest "bounded by lower-trunk breadth (the pelvis does not project laterally as an independent hip structure)"; GO-P6: "no abrupt step in breadth or depth" thorax → lower trunk → pelvis | The step is at the **pelvis → thigh** junction, never at trunk → pelvis. The shelf is a plane change over the trochanter. It must not widen the hip outline into a lateral projection (guidance: keep the hip outline within about 1 cm of the start mesh laterally; this is not a canon number). |
| D: "broad flat patellar plate", "condyle blocks" | Knees "never shrunk … or made **bulbous, spiked or armor-like**" | Bony landmarks flush with the surrounding surface, readable by plane change. No proud plates, shell edges, grooves that read as segmentation, or spikes. |
| D: "squarish shank section", "malleolar blocks" | Ankles "may still look narrower than calf and foot; **substantial never means uniform limb diameter**" | The shank section is squarish (flat anteromedial tibial plane plus a posterior tendon column), but the leg **tapers** to a legible ankle that is narrower than the calf. 05E P2 / P3 "pillar" legs broke this clause and read as heavy humans in run B. |
| E: "olecranon / epicondyle block" | Elbows "substantial … **never isolated knobs**" | Integrated with arm scale: a structural elbow, not a knob. |
| E: "broad wrist plate" | Wrists "integrate large hands with substantial forearms, **never tiny or uniformly columnar**" | Wrist broader than it is deep (a flattened plate) and narrower than the forearm belly. Not a column. |
| F: "trapezius plane", "no deltoid cap" | GO-G4: neck base "readable at low muscle and **never produced by trapezius**"; GO-G1 / G2: girdle carried by the thorax, no girdle overhang | The neck-root and girdle breadth come from skeletal integration (clavicle / scapula / thorax planes). The trapezius plane is a surface continuity, not muscle mass. The shoulder block sits over the accepted joint with no overhang beyond it. |
| Feet (not a family) | Forefoot "may be broad but **never a rectangular slab**" | Untouched (no-touch zone). |
| Hands (not a family) | "not monster paws"; five digits | Untouched (no-touch zone). |

## 4. The six hard-form families

`figures/region_map.png` shows where each family sits on the start mesh. It is an **editing-jurisdiction guide only**: regions are approximate and come from rig weights, and this text governs the anatomy. Light-grey bands (mid-thigh, mid-upper-arm) belong to no family: carry the neighbouring forms through them smoothly.

**Inward budget.** "Floor budget" is how far the start mesh sits above the true skeletal floor, i.e. the most the sculpt can cut inward there. It is given as p10 / median in cm, at reference / low composition (`figures/floor_margin.png`).
- Limb forms (D, E) have about 1.5 cm of inward room. They must be built mainly by **re-shaping and outward planes**, not by carving.
- Trunk and posterior forms (A, B, C) have 3–6 cm.

### A. Trunk section, S2–S5 — floor budget 1.4 / 3.3 cm (low 2.4 / 3.8)

**Required:**
- a broad, flat **sternal–abdominal plate** from the sternum to above the pubis;
- **lateral thoracic planes**, meeting the anterior plate at a legible, radiused edge;
- a **crisp lower structural border** at the costal margin;
- depth carried as **rib-cage structure** continuing down to the pelvis; the reference sculpt does **not rely on a human-style pinched waist or waist hollow** as its read (a reference-direction goal, not a race-wide rule: canon-valid waist variation stays with Frame / composition);
- the human pectoral shelf, nipple relief and navel relief must not be the defining torso read (remove or subordinate them).

**Views:**
- front: flank lines from axilla to iliac crest without a human pinched-waist read, with the plate visible as one plane;
- profile: a deep, straight anterior line with no belly curve;
- silhouette: a deep, radiused, anatomically shaped trunk; not a rectangle, box, mechanically slab-sided section or cylinder.

**Must not:**
- a rectangular, boxy or mechanically slab-sided section, or a circular / cylindrical one (canon; Q1);
- a round barrel;
- a soft belly;
- "fused thorax-pelvis slab" achieved by fat (05E P1–P3, run B: "could be heavy humans").

### B. Posterior axial load path — floor budget 3.1 / 5.1 cm (low 4.5 / 6.4)

**Required:**
- paired broad, low **paraspinal load columns**;
- a **flat interscapular plane**;
- a defined **sacral plate** with a hard transverse upper border;
- the sacrum continuing into the **hamstring origin** as one structural path;
- no round gluteal apex as the dominant form, and no ordinary buttock fold;
- profile: a straight or slightly inclined structural line from the upper back into the proximal thigh.

**Views:**
- rear ¾: two columns plus a sacral plate;
- profile: one line from scapula to mid-thigh, with no buttock projection and no lumbar hollow.

**Must not:**
- a single hump;
- a spinal ridge;
- a "bodybuilder back";
- a fat pad;
- the 05E posterior plane that merely removes the buttock (it read as "flat-backed heavy human").

### C. Pelvis → thigh — floor budget 1.7 / 5.3 cm (low 2.4 / 5.5)

**Required:**
- a **structural hip plate** with a **trochanteric shelf** (plane change over the trochanter);
- a **planar lateral thigh** below it;
- the pelvis → thigh transition as a **defined step**, not the smooth human taper.

**Views:**
- front: the step below the iliac crest, read as structure;
- ¾: the planar lateral thigh;
- profile: no round buttock.

**Must not:**
- lateral outrigging of the hip outline (GO-P2b / P3);
- a step between thorax and pelvis (GO-P6);
- an inflated buttock.

### D. Knee / shank / ankle — floor budget 0.4 / 1.6 cm (low 0.4 / 1.6)

**Required:**
- a broad, flat **patellar plate**;
- legible **femoral and tibial condyle blocks**;
- a **squarish shank section** with a flat **anteromedial tibial plane** and a defined **posterior tendon column**;
- broad **malleolar ankle blocks**.

The leg must read as a **jointed structural column**:
- hard knee and ankle landmarks;
- the shank tapering to an ankle narrower than the calf;
- **not** a uniform pillar (05E P2 / P3);
- **not** the human thick-thigh / thin-shin taper (05D E1, 05E P1 reference).

**Views:**
- front: knee and ankle as broad bony landmarks, flush;
- profile: a straight anterior tibial line with the posterior tendon column, and no human calf belly as the main shape.

**Must not:**
- bulbous, spiked or armor-like knees (canon);
- uniform limb diameter (canon);
- a high Grask-style calf belly with a long cord (that is the accepted Grask read; Gorrund must not borrow it).

### E. Elbow / forearm / wrist — floor budget 0.4 / 1.5 cm (low 0.4 / 1.3)

**Required:**
- a defined **olecranon / epicondyle block** integrated with arm scale;
- a **flattened, squarish forearm section** with flat planes and a clear **tendon border**;
- a **broad wrist plate** (wider than deep, narrower than the forearm belly);
- hands unchanged.

**Must not:**
- isolated elbow knobs;
- uniformly columnar wrists (canon);
- enlarged hands;
- Grask's long tapering forearm.

### F. Shoulder girdle / neck root — floor budget 0.6 / 2.5 cm (low 0.4 / 2.9)

**Required:**
- a **low, broad girdle** integrated with the trunk planes;
- a **trapezius plane** continuous with the trunk planes;
- a **planar shoulder block** over the accepted joint, replacing the human deltoid cap as the primary read;
- a skeletal neck base readable at low muscle.

**Must not:**
- girdle overhang beyond the accepted joint (GO-G1);
- neck-root breadth from trapezius mass (GO-G4);
- scapular / upper-back mass that reads as a hump. That is Grask's accepted read, and it is also excluded as a Gorrund posture illusion.

## 5. View and silhouette targets

All targets are relational and visual. Canon gives no numbers for these forms (exact morphology is OPEN). Judge them against the evidence named here, at matched camera, ground and stature, body only, head and neck removed, neutral grey and black silhouette (the 05D / 05E sheet standard).

| View | The Gorrund sculpt must show | Compare against |
|---|---|---|
| Front | Sternal plate and lateral planes (A); hip step and planar lateral thigh (C); flush knee and ankle landmarks on a tapering shank (D); broad flattened wrists (E); low, broad girdle with no deltoid cap (F) | `evidence/05e/e_GO_F_grey.jpg` (failed: pillar or human-taper legs, smooth trunk) |
| Front ¾ | Plane break between the anterior and lateral trunk (A); planar lateral thigh (C); squarish shank and forearm sections (D / E) | `evidence/05e/e_GO_Q_grey.jpg` |
| Profile | Straight anterior trunk line (A); one posterior line from scapula to mid-thigh with no buttock or lumbar hollow (B); anterior tibial plane plus tendon column (D); no hunch, no bent-knee read | `evidence/05e/e_GO_P_grey.jpg`, `evidence/05d/d_GR_P_grey.jpg` (Grask contrast: what Gorrund must *not* resemble) |
| Rear ¾ | Paraspinal columns, interscapular plane and sacral plate continuing into the hamstring origin (B) | `evidence/05e/e_GO_RQ_grey.jpg`, `evidence/05e/c_229_back_R.jpg` |
| Silhouette, front and profile | Deep, radiused trunk (not a rectangle, box or cylinder), jointed legs that taper to the ankle, and no human pinched-waist / buttock / calf rhythm as the read (waist variation itself remains canon-valid through Frame / composition) | `evidence/05e/e_GO_{F,P}_sil.jpg` |

## 6. Persistence: low composition, Narrow, Broad

**How transport works.** The delivered displacement (sculpt − start mesh) is stored in each vertex's skinned bone frame, scaled by the local bone-length ratio. It is then added to every composition and Frame state of the accepted route. After that, every state is clamped to the true floor and volume-restored (`race_base.sculpt_layer`).

**Consequences for the sculptor:**

1. **Low composition** (muscle 0, weight 0.5; `template/GO_low_route_r6.obj`). The blind gate requires the race read at low composition in every run. Forms built as **outward planes, plates and edges** persist. Forms built only by **carving soft tissue away** may be clamped where the low body has less tissue over the floor. Preview the forms on the low mesh before delivery.
2. **Narrow / Broad.** The same field rides on the Frame route. Forms should be defined relative to the local skeleton (joints, planes), not to the reference body's absolute outline, so they read at both Frame extremes.
3. **Stature range.** The field scales with local bone length. Stage C will check representative statures. Avoid forms whose read depends on the reference body's exact size.

## 7. Must-not list from the failed routes

| Route | What it did | Why it failed | Evidence |
|---|---|---|---|
| 05C | Reorganized MPFB soft tissue inside the old `-LEAN` guard | Guard froze human soft tissue as bone; human read | `reviews/claude-rac-rm-ot-05c-…gate.md` |
| 05D E1 / E2 | Posterior column, columnar limbs, dorsal arc | Distinct cluster, but "mostly bulk" in some contexts; 0 / 3 when Grask E3 was present (run 2) | `evidence/05d/` |
| 05E P1 | Moderate constant-section limbs + box trunk | Ref 1 / 3 then 3 / 3; low 3 / 3 then 0 / 3 | `evidence/05e/blind_*` |
| 05E P2 / P3 | Strong "pillar" limbs + box trunk | 3 / 3 in run A, 0 / 3 in run B: "could be an ordinary heavy-human … cluster"; also against canon (boxy section, uniform limb diameter) | `evidence/05e/`, 05E gate §6 |
| Grask E3 (accepted, contrast) | Scapular mass, keel, high calf + long cord | Robust Grask read. Gorrund must not borrow these features: they read as hunch / digitigrade and as Grask | `evidence/05d/d_GR_*` |

**General rule.** If a scorer can describe it as "heavy", "obese", "muscular", "barrel", "flat-backed heavy human", "pillar legs" or "hunched", it is not the Gorrund read.

## 8. Sculptor checklist

Before delivering, confirm each line.

- [ ] Sculpted on `GO_ref_route_r6.obj`; delivered at the base level with 13 380 vertices in the original order and faces unchanged.
- [ ] No re-pose, no re-scale, no re-centre; feet still flat on z = 0; stature unchanged (230.90 cm).
- [ ] Head / neck, hands / digits, toes / forefoot untouched (≤ 0.5 cm).
- [ ] Nothing inside `GO_true_floor_r6.obj`. The limbs were shaped mainly outward or by redistribution.
- [ ] **A:** sternal plate, lateral planes, costal border; the read does not rely on a human pinched waist / waist hollow (reference direction, not a race rule); section radiused and anatomically shaped: not rectangular, boxy, mechanically slab-sided or cylindrical.
- [ ] **B:** paraspinal columns, interscapular plane, sacral plate into hamstring; straight posterior line; no hump, no buttock.
- [ ] **C:** hip plate, trochanteric shelf, planar lateral thigh; no lateral outrigging; no trunk → pelvis step.
- [ ] **D:** patellar plate and condyle blocks flush (not armor); squarish shank with tibial plane and tendon column; ankle narrower than calf; not a pillar.
- [ ] **E:** integrated elbow block; flattened forearm with tendon border; broad flattened wrist; not a column.
- [ ] **F:** low broad girdle, trapezius plane, shoulder block, no deltoid cap, no overhang, no hump.
- [ ] Previewed on `GO_low_route_r6.obj`: every family still legible.
- [ ] Checked front, ¾, profile, rear ¾ and silhouette against §5: no read as heavy, obese, muscular, hunched, crouched or digitigrade.

## 9. Validator checklist (pipeline side)

`python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_<ID>_r6.obj <ID>` runs everything below. A failure at ingest stops the run before anything is built. Thresholds are the existing 05D / 05E ones; none may be relaxed.

**Ingest** (`f_ingest.py`):

| Check | Threshold |
|---|---|
| I1 topology | 13 380 vertices; faces identical to the template |
| I2 rigid / scale fit on bony anchors | \|scale − 1\| ≤ 0.002, rotation ≤ 0.2°, translation ≤ 0.3 cm |
| I3 stature / ground | stature and ground within 0.05 cm of the template |
| I4 no-touch zones | ≤ 0.5 cm |
| I5 raw sculpt vs true floor | 0 organized vertices inside by more than 0.2 cm |
| I6 posture | hand / foot / head anchor centroids ≤ 0.3 cm |
| Coverage per family | advisory |

**Build:** `GO5F<ID>` (reference), `GO5F<ID>-LOW`, `GO5F<ID>N`, `GO5F<ID>B`, through the unchanged 05D builder.

**Guards** (`f_guard.py`, from 05E `e_guard`, thresholds unchanged), on all four states:
- exact stature and ground;
- skeleton, joints, `-LEAN` and bone scales unchanged;
- outward-normal test;
- true floor;
- plantigrade contact;
- hand / foot topology and digit count;
- gross self-intersection no worse than the route + 10;
- arm / trunk clearance;
- R-6 joints equal;
- whole-body volume = route;
- composition ordering;
- Frame ordering;
- protected Gorrund relations unchanged;
- proxy-floor dependency report.

**Transport report:**
- per-family retention of the delivered displacement at low, Narrow and Broad;
- reference-state reproduction error against the delivered surface.

## 10. Blind-gate checklist

Run only after re-entry passes.

**Set:** 12 bodies per run:
- 8 human-family controls;
- Grask E3 reference and low (every run);
- Gorrund sculpt reference and low.

**Runs:** at least 2 replicated runs with fresh shuffles (`f_blind.py <ID> run1|run2|run3`), each with 3 fresh uninformed scorers using `f_scorer_prompt.md` verbatim (JSON answers).

**Tally:** `f_tally.py` applies the 05F pass condition mechanically:

| Line | Requirement |
|---|---|
| G1 | C ≥ 2 / 3 at reference, in every run |
| G2 | C ≥ 2 / 3 at low composition, in every run |
| G3 | stable group that excludes controls and Grask |
| G4 | distinguishable from Grask |
| G5 | organization (not bulk) as the basis |
| G6 | axial and limb cues named |
| G7 | no human-control collapse |

Hunched / crouched / digitigrade reads are counted for the author.

**Rule:** a pass in one run and a fail in another is a fail. Stage C begins only after both re-entry and the blind gate pass (order §6).

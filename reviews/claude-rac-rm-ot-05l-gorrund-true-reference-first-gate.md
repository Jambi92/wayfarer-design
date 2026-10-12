# RAC RM-OT-05L: Gorrund true reference-first free sculpt (gate)

**Order:** `reviews/chatgpt-rac-rm-ot-05l-gorrund-true-reference-first-order.md` (ac396e1)
**Author:** Claude
**Date:** 2026-10-12
**Evidence:** `reviews/rac-rmot05l-evidence/` (hashes in `SHA256SUMS.txt`)
**Tools:** `tools/rac/w1/rmot05l_drivers/`

## Gate lines

| Line | Status |
|---|---|
| Old Branch A | **CLOSED / EXHAUSTED** |
| RF1 / RF2 human-donor method | **NEGATIVE EVIDENCE** |
| Final free-sculpt reference | **NONE** (RS1 and RS2 both fail the internal gate) |
| Starting race skeleton used | **NO** |
| Human anatomical donor used | **NO** |
| Parametric race-body generator used | **NO** |
| Reference internal canon-form gate | **FAIL** (RS1 FAIL; RS2, the one allowed revision, FAIL) |
| Low companion created | **NO** (§18: only after a reference passes) |
| REF↔LOW same-structure audit | **NOT RUN** |
| Concept blind gate | **NOT RUN** (§20: only after REF and LOW pass internal review) |
| Blind-reason canon audit | **NOT RUN** |
| Gorrund body-only readability | **REJECT** |
| Measurement scaffold | **NOT DERIVED** |
| Canon reconciliation | **NOT RUN** |
| RM-OT-05 | **OPEN** |
| Stage C | **BLOCKED** |
| Canon promotion | **NOT PERFORMED** |
| D4 | **NOT STARTED** |
| UE5 | **NOT STARTED** |

I stopped under §17: "If RS2 is still clearly wrong, STOP and return the evidence." No scorer saw either body.

## 1. Sculpt method

### 1.1 Digital clay (substrate, §4)

There is no starting mesh at all. The substrate is an empty signed-distance field: `l_clay.py`, digital clay that holds no anatomy. Sculpting adds or carves hand-placed forms in it:
- ellipsoids;
- tapered capsules;
- one sweep through hand-drawn horizontal trunk sections, like a sculptor's section templates.

Forms are joined by smooth blending. The left half is sculpted and mirrored. The clay is then voxel-remeshed (marching cubes, 0.6 cm), relaxed (Laplacian, volume-preserving), and decimated to about 40k vertices (`l_finish.py`).

Concept topology is new and not locked (§4). Both assets are:
- watertight;
- outward-wound;
- in cm, Z up, +Y anterior;
- stature 228.7 cm.

### 1.2 The sculpt record

`l_rs1.py` / `l_rs2.py` hold one stroke per line. Each stroke is a form placed by hand for this body, with a comment naming its anatomy, for example:
- "deep rib cage, planar lateral walls";
- "costal margin: the rib cage steps forward over the lower trunk";
- "sacral platform";
- "lateral hip plane under the load path";
- "broad condyles and tibial plateau";
- "large plantigrade foot".

There are no free parameters, no sweeps over values, and no candidate search. RS1 went through about 16 working iterations in one session. Each was judged by eye on neutral sheets beside the controls. None was scored.

### 1.3 RS2 = one direct revision of RS1 (§17)

RS2 made five clay corrections, marked `RS2:` in the record:
- knee bulb removed;
- shank and distal thigh joined to the knee;
- posterior thigh mass lowered (no gluteal ledge);
- less anterior bulge in the rib cage;
- more planar rib-cage walls.

It then received a hand-drawn brush pass (`l_rs2_brush.py` with the `l_brush.py` Draw / Crease / Flatten / Smooth engine). That is 25 strokes drawn on the surface and mirrored, logged in `RS2/GO-RS2-REF_strokes.json`:
- clavicle line;
- sternal plane;
- costal arch;
- planar anterior lower axial wall;
- iliac crest and anterior iliac spine;
- lateral hip plane;
- sacral platform;
- sacrum-to-hamstring smoothing;
- paired axial columns and median furrow;
- scapular border and plane;
- patellar plane and infrapatellar margin;
- knee side planes;
- tibial plane and tibial border;
- Achilles margin;
- olecranon;
- forearm plane;
- wrist margin.

### 1.4 Proof that no race skeleton or human donor was used (§3)

- `l_clay.py`, `l_rs1.py`, `l_rs2.py`, `l_rs2_brush.py` and `l_finish.py` load no mesh, rig, skeleton, weights, joint file or composition data. The clay starts as an empty field (`Clay()` with `d = +∞`), and every form is a literal in the record.
- The only external bodies touched are the comparison controls in the review sheets (Marchfolk, Skarn, Skarn Broad, Grask E3, S4, RF1). They are rendered by the unchanged protocol renderer (`k_review.py`) and never enter the sculpt.
- The body-only renderer's head cut (`l_npz.py`) is a plain height cut at this body's neck root (z 195). It is not a donor weight map.

## 2. Internal reference gate (§17)

Sheets for each revision, in `RS1/` and `RS2/`:
- `*_neutral_grey.jpg` and `*_neutral_sil.jpg`: front, front 3/4, profile and rear 3/4, head and neck removed, height-normalized, beside Marchfolk, Skarn, Skarn Broad, Grask E3, S4 and RF1;
- `*_close_views.jpg`: full body, girdle, thorax / lower trunk, pelvis / hip, knee / ankle, elbow / wrist and posterior, at five angles.

| Criterion | RS1 | RS2 |
|---|---|---|
| not rectangular | FAIL. Front trunk is a rounded block from girdle to pelvis | FAIL (less so) |
| not boxy | FAIL | FAIL |
| not slab-sided | PASS | PASS |
| not barrel / cylindrical | FAIL. Rib cage reads as a smooth barrel | MARGINAL. Costal arch now marks it |
| not bodybuilder | PASS | PASS |
| not obese | PASS | PASS |
| not monster / ogre | FAIL. Reads as a toy or doll mannequin, with bulb knees | FAIL. Doll / mannequin read stays |
| not Grask-like | PASS | PASS |
| not simply broad human | PASS, but only because it reads as a doll, not as an organism | same |
| clear load-bearing axial identity | FAIL. Deep chest only | MARGINAL. Costal step and deep thorax |
| clear pelvis→femur support | FAIL. Lateral hip bulge (outrigger read) | FAIL |
| clear joint structural scale | FAIL. Knees read as bulbs (knob) | FAIL. Smaller but still segmental |
| clear posterior load path | FAIL. Featureless back | FAIL. Brush-carved streaks read as grooves, not a load path |
| whole-body coherence | FAIL. Segmented, "sausage" limbs | FAIL |

**Both fail.** The deciding failure in both is that the body does not read as a coherent biological organism. It reads as a smooth stylized mannequin with segmented limbs. A blind test of that body would measure the doll read, not Gorrund anatomy, and would not be a valid test of the reference-first method.

## 3. What this shows

1. **RS1 / RS2 test the construction order, not the canon.** They are the first Gorrund bodies made with no skeleton and no donor. Even so, they never reached the anatomical quality the internal gate needs. They also fail the exact §17 criteria the old routes failed (boxy, barrel, knob, outrigger), just by a different route.

2. **This session's sculpt capability is the limiting factor.** All forms were placed by hand, but in a headless environment through a clay record and drawn strokes. There was no interactive sculpting with a stylus. That works well for blockouts and section control. It did not produce the continuous muscle-over-bone surface organisation that makes a body read as alive.

   Saurin's reference-first success started from an external sculpt source: the Rodin-generated bodies Tyler supplied (`reviews/saurin-rodin-*`). That source was then edited surgically. The Saurin method as it actually ran was "good source body first, then edit, then derive the scaffold". RM-OT-05L asked Claude to supply the source body itself.

3. **Recommendation for the author.** Run the 05L order unchanged, but with a source body made by an artist, or by a Rodin / Hyper3D generation that Tyler makes from a Gorrund brief, as for Saurin. I would then do what worked for Saurin:
   - surgical canon edits;
   - the LOW companion;
   - the neutral review and concept blind gate;
   - the scaffold derived from the body.

   I can write the Gorrund generation brief, a text and reference-sheet prompt built from GORRUND_V1 and the 05-series negative evidence, if the author wants that route.

## 4. Unresolved dependencies and conflicts

- **Reference body source:** an external sculpt source is needed (§3.3). This is a capability dependency, not a canon conflict.
- **Canon conflicts:** none found. No body passed, so reconciliation (§22–§25) was not run.
- **Carried from 05K:** the diagnostic skin pelvic-depth rows on the old route are still unruled.

## 5. Principal hashes (SHA-256)

| Artifact | Hash |
|---|---|
| `RS1/GO-RS1-REF.obj` | `33a0e71deea3bf9f5343c04f9c88629fcd742f0203c05133c39398208b910a5e` |
| `RS2/GO-RS2-REF.obj` | `4780ee49a433213121fba560e9f7fa1e68ead24d4b24d0d9164472bdcc6ce29d` |

The source `.blend` files, the RS2 clay surface before the brush pass, the stroke log and the asset record (`asset_record.json`: watertight, 186 L, 228.7 cm) are listed in `SHA256SUMS.txt`.

Both assets rebuild exactly from the sculpt records:

```
python3 l_rs1.py OUT 0.6 && python3 l_finish.py OUT_raw.obj OUT 0.3
python3 l_rs2.py C 0.6 && python3 l_finish.py C_raw.obj CLAY 0.3 && python3 l_rs2_brush.py CLAY.obj GO-RS2-REF.obj
```

## 6. Confirmation

- The old Gorrund 05A–05K evidence and route are untouched.
- The new lineage uses distinct names (GO-RS*).
- Grask E3 is frozen.
- No validator, threshold, scorer prompt, tally rule or canon rule changed.

I stopped at the RM-OT-05L author gate.

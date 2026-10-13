# RAC RM-OT-05N: Gorrund recovered-source continuation (gate)

**Order:** `reviews/chatgpt-rac-rm-ot-05n-gorrund-recovered-source-continuation-order.md` (d80a977)
**Author:** Claude
**Date:** 2026-10-12
**Evidence:** `reviews/rac-rmot05n-evidence/` (hashes in `SHA256SUMS.txt`)
**Tools:** `tools/rac/w1/rmot05n_drivers/`

## Gate lines

| Line | Status |
|---|---|
| Recovered source verified | **PASS** |
| Source hash | `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b` (re-hashed from the upload in this block; unchanged) |
| Primary full-body source selected | **F1**: the front figure of GLB component 0, `c0s_1` (§1) |
| Source suitability | **PASS** (§1) |
| Minimal beastfolk canon alignment | **COMPLETE** (§2: 8 lines changed, 1 line added) |
| Existing body canon preserved | **YES**. No body rule changed. See §8 for the conflicts this body raises against that canon |
| Final reference | **RD2** (`GO-RD2-REF`) |
| RD internal structural gate | **PASS with residuals** (§4) |
| Leonine head restored for organism review | **YES** |
| Tail restored / integrated for organism review | **YES** (source tail study at the sacral root; scale and pose are review placements, numeric OPEN) |
| LOW companion | **CREATED** (`GO-RD2-LOW`) |
| REF↔LOW structural audit | **PASS** (§5) |
| Revised neutralized structural gate | **FAIL**: criteria 1–4 PASS, criterion 5 FAIL, criterion 6 not shown (§6) |
| Full-organism coherence gate | **NOT RUN** as a gate (§16 runs only after the structural pass). The §13 organism review presentation was made; observations are in §7 |
| Measurement scaffold | **NOT DERIVED** (§17: only after the revised gate passes) |
| Canon reconciliation | **NOT RUN** (§18: after the scaffold). Open conflicts are listed in §8 |
| RM-OT-05 | **OPEN** |
| Stage C | **BLOCKED** |
| Canon promotion | **NOT PERFORMED** |
| D4 | **NOT STARTED** |
| UE5 | **NOT STARTED** |

**Bottom line**

The recovered Rodin source produced the first Gorrund body in the RM-OT-05 series that reads as a coherent biological organism. Under the old criteria it is also the first to pass the replicated blind gate mechanically: 2/2 runs, G1–G7 all pass, with 6/6 scorers giving class C at REF and at LOW.

The revised criterion 5 fails. In every one of the 6 scorer outputs, the group containing REF and LOW is labelled as an ogre / troll / brute / orc type. Every scorer also names bent or bowed knees (posture) as a driver, and most name blocky or waistless trunks (boxiness) and massive or huge limbs (bulk). All of these are on the GORRUND_V1 negative list ("no ogre", "not … exaggerated monster anatomy").

The main driver comes from the source itself. Its legs are short, the stance is deep and the knees are forward (§6.3). I have stopped at the gate as required: no RD3 without an author order.

## 1. Source: islands, selection, suitability (§5–§7)

`source/island_manifest.json`, `source/source_figures_overview.jpg`, `F1_turnaround.png`, `F4_turnaround.png`, `part_studies_hand_feet_tail.png`, `tail_study_turnaround.png`.

**What the GLB contains.** It is a true 3D "library", not a relief. After merging vertices at 1e-5 it has 11 connected islands:

| Island(s) | Content |
|---|---|
| Component 0 | Figures F1 (front) and F2 (rear), fused at a contact slab |
| Component 5 | Figures F3 and F4, fused back-to-back |
| Components 6–10 | Five head / detail panels |
| Component 1 | Hand study |
| Components 2, 3 | Lower-leg + foot studies (plantigrade, five-toed, wrapped) |
| Component 4 | Tail study (curled, tufted) |

I split the fused figures by removing the faces in the contact slab and reassigning them to the nearest figure (`split.py`).

**Figure assessment**

| Figure | Assessment |
|---|---|
| F1 | Complete front and back (mane, back musculature); complete shanks and feet under the wraps. The only defect is a small open seam on its −X arm at the contact. |
| F2 | Its anterior side is a hallucinated second back. Unusable. |
| F3 | Back is opened by the fusion. |
| F4 | Good front and an integrated tail, but the upper back is disorganised by the fusion. |

**Selected: F1.** It is the only figure that is clean all round. The tail is taken from the separate tail study (component 4).

**Correction recorded.** Early in this block, F1 looked as though it lacked anterior shins and F4 looked hollow-backed. Both were a clipping artifact of my renderer (camera clip_end 1000 at a camera distance of 1000). I fixed the renderer (clip_end 5000) and re-rendered before any decision was final. The F1 choice stands on the corrected renders.

**GO-RD0-SOURCE** (`source/GO-RD0-SOURCE_record.json`). F1 untouched, re-framed into RAC axes:
- cm, Z up, +Y anterior, ground z = 0, by a 180° rotation about Z (a proper rotation, not a mirror);
- **scale factor 2.70634** sets the cranial vault top (under the mane; ears and mane tufts excluded) to 229.0 cm. The ear and mane tips reach about 241 cm.

**Suitability: PASS.** The source has:
- an upright plantigrade biped with a five-toed foot;
- a broad, deep thorax and a real posterior anatomy;
- a leonine head with mane, and a tail study.

Its clothing and the muscularity are surgical work, not a source defect.

## 2. Minimal beastfolk canon alignment (§4)

The exact lines, before and after, are in `canon_changes.json`. All edits are in `specs/gorrund/GORRUND_V1.md`:

| Location | Change |
|---|---|
| Line 9, core identity | "distinct large humanoid population" → "distinct large beastfolk population (leonine head, tail; author ruling RM-OT-05N)". Added: "The leonine head and tail are species-identity channels; they do not replace the body architecture." |
| Line 72 (new row after the Plantigrade lock) | Tail: present; integrated with the sacral load path; species-identity channel, not a replacement for the body architecture; not a balance organ for an upright plantigrade biped; numeric length, taper and tuft **OPEN**. |
| Line 88 | Head and tail add species identity, but the body read must still stand when they are neutralized. |
| Line 323, cranial depth | "never equated with … a muzzle" → the head is leonine and carries a muzzle; numeric morphology **OPEN**. |
| Line 333, midface | "may be valid without a muzzle, snout …" → "expressed as a leonine muzzle (numeric OPEN), never ape-like prognathism". |
| Line 335, GOR-FACE-05 comparator | "never a muzzle" → "leonine muzzle permitted under RM-OT-05N". |
| Line 409, GOR-FACE-05 table | Same change as line 335. |
| Line 440, first-pass summary | "midface depth without a muzzle" → "(leonine muzzle under RM-OT-05N)". |

Line numbers are as before the tail row was inserted. **Unchanged:**
- plantigrade lock;
- every body rule, including no muscularity / obesity / monster anatomy dependency;
- clothing is not biology;
- "never inventing a tail" (line 113 in the old numbering, Halvren comparison; it concerns Halvren ancestry and is not Gorrund-specific). Flagged for the author.

## 3. Surgical sculpt: what was done (§8–§11)

Sculpting was done on GO-RD0-SOURCE's own surface field:
1. winding-number occupancy at 0.5 cm;
2. the clean +X half mirrored (the −X arm is open at the F1 / F2 seam);
3. converted to signed distance.

Every edit is a named, region-limited operation, recorded in `RD2/GO-RD2_field_params.json` and `_field_log.json`. The tool is `rd1.py`, followed by `rd_finish.py` (decimate to about 84k faces, then relax) and `rd_brush.py` (8 hand strokes).

**Clothing removed and reconstructed zones**

| Item | Treatment |
|---|---|
| Loincloth panels, central hanging mass, knee-level panel ends (z 55–93) | Per-slice section cleanup |
| Pelvis zone z 72–150: skirt, tassel ring, pouches, belts | These were fused over the whole hip. A 3D opening of the trunk (r = 8 cm) removes everything thinner than the body masses and leaves the source's own hip, buttock and abdomen bulk. Belt rings are relaxed along z. **Reconstructed zone: pelvis / hip surface z 72–150** (source bulk kept; the surface relief is regenerated). |
| Necklace, chest braids, back braid (z 150–192) | Section opening |
| Mane locks over the nape | Removed from the body; restored in the organism |
| Bracers and armbands | Relaxed along the arm axis |
| Shin wraps and the instep strap | Relaxed along the shank; the strap area is smoothed. **Reconstructed zones: shank surface z 12–50 and instep.** |

**Muscle reduction.** Named deflations and blends toward a broadly smoothed field, as listed in the log:
- deltoid caps, pectorals, biceps, latissimus flare, trapezius mound;
- vastus lateralis and medialis bulges;
- abdominal wall (six-pack removed; no belly).

**Body targets**

| Target | What was done |
|---|---|
| Thick lower axial trunk | Waist thickened about 4 cm laterally; no pinched V |
| Pelvis volume | Deep pelvis with a flattened sacral platform |
| Thorax | Source thorax kept broad and deep |
| Arms | RD2 clears the trunk 1.8 cm from the hanging arms (no arm–trunk web) |

**Feet.** The source foot is already plantigrade and five-toed. It was kept, and its length corrected about the ankle axis: forefoot × 0.62, heel × 0.82, breadth × 0.92. The source paw-like foot was about 62 cm (0.27 H) long; it is now about 41 cm (0.18 H).

**Brush strokes:** inguinal fold, ASIS, gluteal fold, sacral platform (flatten), sacrum-to-hamstring smoothing, instep, a faint linea alba, and lateral hip plane (flatten).

`RD2/source_vs_RD2.jpg` shows the source and the sculpt in the same views.

## 4. RD internal structural gate (§12)

**RD1.** RD1 was the first declared reference (`RD1/`). It passed every item except two:
- the hanging arm webbed to the trunk below the axilla, from smoothing;
- the thighs kept a pronounced quadriceps teardrop.

That is one coherent surgical issue, so I made **RD2**: trunk clearance from the arm field, plus stronger thigh smoothing and vastus deflation. The sheets are `RD1/*_neutral_*.jpg`, `RD2/GO-RD2_neutral_grey.jpg` and `RD2/GO-RD2_close_views.jpg`, all beside Marchfolk, Skarn, Skarn Broad and Grask E3.

| Criterion | RD2 |
|---|---|
| Coherent biological organism | PASS. It reads as one living body: source surface, continuous transitions. This is the first in the series (RS1 / RS2 failed this). |
| Source-surface anatomy retained / improved | PASS on the thorax, back, arms, knees and feet. Pelvis and shank are reconstructed zones and smoother. |
| No mannequin / sausage read | PASS |
| No rectangle / box / slab | PASS in my review. The blind scorers did not agree; 5/6 said "blocky" (§6). |
| No barrel cylinder | PASS |
| No obese-human read | PASS (no belly; abdominal wall flattened) |
| No bodybuilder dependency | MARGINAL. Shoulders and thighs are still heavy. |
| No hourglass | PASS |
| No Grask reach read | PASS. Fingertips at the crotch / upper thigh. |
| Pelvis / femur integration clear | PASS. No outrigger; thighs enter a deep pelvis. |
| Posterior load path clear | PASS. Paired erector columns and a broad sacral area. |
| Substantial joints integrated, not knobbed | PASS. Large knees and ankles. |
| Plantigrade lower limb preserved | PASS |
| Structurally massive, not merely thick | PASS |

**Residuals carried forward**
- The source pose has short legs and forward knees. My centroid estimate is about a 20° hip–knee–ankle zig-zag in profile.
- A small arm–trunk contact window remains, from the source arm pose.
- The toes still read partly paw-like.
- The pelvis and shank surfaces are smoother than the source surface.

## 5. LOW companion and REF↔LOW audit (§14)

`LOW/GO-RD2-LOW.obj`, `LOW/GO-RD2-LOW_params.json`, `LOW/REF_LOW_audit.json`.

LOW was made by hand from the RD2 field (`low.py`). Twelve named soft-tissue masses were reduced, each mirrored:
- quadriceps and hamstrings;
- gluteal tissue and calf;
- lower abdominal wall and flank;
- pectoral, deltoid, upper arm and forearm flexors;
- upper back and latissimus.

The following were protected and not touched: knee, ankle, elbow, wrist, acromion / clavicle, iliac crest / ASIS, sacral platform and tail root. There was no uniform shrink and no Marchfolk deltas.

**Audit**

| Measure | Result |
|---|---|
| Volume | 301.9 → 291.0 L (−3.6 %) |
| Joint sections (knee, ankle, elbow, wrist) | Unchanged (0.0 %) |
| Pelvis section at 115 cm | Unchanged (−0.1 %) |
| Thorax and waist | Thorax breadth unchanged; depth −1.5 cm; areas −3 to −9 % |
| Thigh | −17 % |
| Calf | −12 % |
| Upper arm | −16 % |
| Forearm | −8 % |
| Limb lengths and stature | Unchanged |

Every blind scorer grouped REF and LOW together, stably (§6).

**PASS.**

## 6. Revised neutralized structural gate (§15)

**Protocol.** The renderer, controls, prompt and tally are unchanged from 05K:
- `k_blind.py` and `f_scorer_prompt.md` (verbatim) with `f_tally.py`;
- 12 bodies per set: Marchfolk and Skarn × reference / Narrow / Broad / low, Grask E3 ref + low, and Gorrund REF + LOW;
- head and neck removed at the neck root (z 191); the tail exists only in the organism meshes;
- neutral grey plus silhouette, height-normalized, front and profile;
- two replicated runs (sets K and L, new seeds), 3 fresh scorers each;
- sheets were copied to neutral directories before scoring.

Evidence: `blind/` holds the sheets, keys, the six scorer JSONs, `tally_old_criteria.json` and `reason_audit.json`.

### 6.1 Old RM-OT-05 criteria (recorded unchanged; old scores of S1–S4, RF, RS are not rewritten)

| Line | Run K | Run L |
|---|---|---|
| G1 REF class C | 3/3 | 3/3 |
| G2 LOW class C | 3/3 | 3/3 |
| G3 stable REF+LOW group, no control or Grask in it | 3/3 | 3/3 |
| G4 distinct from Grask | 3/3 | 3/3 |
| G5 basis = organization | 3/3 | 3/3 |
| G6 axial and limb cues | 3/3 | 3/3 |
| G7 no control collapse | pass | pass |
| posture_read (author attention) | ref 3, low 3 | ref 3, low 3 |
| **Run** | **PASS** | **PASS** |

On the old mechanical criteria this is the first Gorrund pass in the series: `gate_pass: true`.

### 6.2 Revised criteria (§15)

| # | Criterion | Result |
|---|---|---|
| 1 | REF and LOW group stably as one structural body type | **PASS** (6/6) |
| 2 | No collapse into scaled-up Marchfolk | **PASS**. No Marchfolk code in the Gorrund group; all Marchfolk read as class A. |
| 3 | No collapse into Skarn Broad | **PASS**. Skarn Broad read as class A, in the human group, 6/6. |
| 4 | Distinct from Grask architecture | **PASS** (6/6; scorers describe Grask as the opposite plan) |
| 5 | Reasons are structural organization, not fat, muscle, posture or boxiness | **FAIL**, see 6.3 |
| 6 | Compatible with the full leonine beastfolk presentation | **NOT SHOWN**. It depends on 5 (§7). |

### 6.3 Reason audit (`blind/reason_audit.json`)

Every scorer marked basis = organization. The drivers they wrote say otherwise. Counts are out of 6 scorer outputs, keyword matches on drivers and cues:

| Cue in the drivers | REF | LOW |
|---|---|---|
| Posture: bent / flexed / bowed knees, crouch, forward lean | 6 | 6 |
| Bulk: massive / huge / enormous limbs | 6 | 6 |
| Boxiness: blocky / rectangular / slab / waistless | 4 | 5 |
| Segment relations: short legs vs trunk, extremity size | 1 | 6 |
| Pelvis / stance / joint transitions | 5 | 6 |

The group labels, verbatim:
- "massive troll/ogre-like, huge limbs and feet, bent-knee stance"
- "massive heavy-limbed short-legged brute body"
- "massive brute race: wide trunk, short bent legs, giant hands/feet"
- "massive squat ogre/troll-like body plan, bent-kneed"
- "massive, blocky, wide-pelvis, bowed-leg brute race"
- "massive broad-trunk, short bowed-leg race (orc/dwarf-like)"

The body is read as a distinct structural type, but a **brute / ogre type, driven by posture, bulk and short legs**. That is on the GORRUND_V1 negative list ("no 'dumb ogre' coding", "not … exaggerated monster anatomy").

**Source of the failure.** The read does not come from the surgical edits. They removed the bodybuilder and V-taper read and left the joints large but integrated. It comes from properties the source pose and proportions carry:
- **knees forward with a deep stance**: about a 20° hip–knee–ankle zig-zag in profile (section-centroid estimate on RD2);
- **short legs relative to the trunk**: crotch at about 104–107 cm, 0.46 H, under a very deep trunk;
- **heavy arm mass hanging near the trunk**.

Fixing these needs a pose and proportion change: straighten the knee chain and lengthen the shank / thigh. That goes beyond the one revision allowed (§12: no RD3 without an author order). It also touches the order's "do not create a different race" line, so it is an author decision.

## 7. Full-organism review presentation (§13)

`ORG/GO-RD2_full_organism.jpg`, `ORG/GO-RD2-ORG-REF.obj` and `-LOW.obj`, `ORG/organism_params.json` (`org.py`).

**How it was assembled**
- **Head:** the source leonine head and mane, unchanged.
- **Mane over the nape:** restored from the source field, behind a sloped plane.
- **Tail:** the source tail study, ×1.6 (about 15 cm root). It is placed at the sacral midline (0, −13, 114) and tilted 50° posteriorly and 35° laterally, so it does not hang between the legs in front view. It is smooth-blended into the sacral surface.

These are review placements, not frozen tail numbers.

**Observations.** This is not a gate verdict; §16 follows the structural pass.

| Check | Observation |
|---|---|
| Leonine identity | Unmistakable |
| Head scale | Does not make the body look undersized |
| Neck root | The mane hood carries the head naturally |
| Tail root | Sits on the sacral platform |
| Tail and gait | Does not imply quadrupedal or digitigrade use |
| Tail size | The study is short and tightly curled; it reads small for the body. Numeric morphology OPEN. |
| Ogre / orc / troll | With the head on, the read is plainly a lion-headed beastfolk, not an orc or troll. The body-only brute read in §6 is the open risk: the body may be leaning on mass and posture rather than load-bearing structure. |

## 8. Unresolved conflicts and dependencies

1. **Brute / ogre body-only read (criterion 5).** Driven by source posture (forward knees, deep stance), short legs and arm mass. Author decision needed (D-05N-1): authorise an RD3 pose / proportion correction (knee chain straightened, leg-length relation adjusted within the body canon), or rule that this read is acceptable under the beastfolk presentation.
2. **Leg-length relation vs canon.** The crotch is at 0.46 H under a very deep trunk. The GORRUND_V1 torso-to-limb proportion is OPEN, so this is not yet a conflict. It is the measurable driver of the "short legs" read.
3. **Reconstructed zones.** The pelvis / hip surface (z 72–150) and the shank surface (z 12–50) are regenerated under fused clothing, with the source bulk kept. They are smoother than the rest of the source surface.
4. **Mirroring.** The body and head are mirrored from the source's +X half. The −X arm of F1 is open at the F1 / F2 seam.
5. **Tail.** The study scale and pose are placeholders. A longer, hanging tail may be wanted (F4 carries one; it was not used because of F4's fused back).
6. **GORRUND_V1 line 113** (old numbering): "never inventing a tail", in the Halvren comparison. Left unchanged because it concerns Halvren ancestry. The author should confirm.
7. **Carried from 05K:** the old-route skin pelvic-depth rows are still unruled. Not measurable here because no scaffold was derived.
8. **Toes.** Partly paw-like (beastfolk). "Large plantigrade humanoid feet" is kept; the foot was shortened to 0.18 H.

## 9. Old RM-OT-05 failures (§19)

These are kept and not deleted. They remain negative evidence and no longer imply that the Gorrund species concept is invalid.

| Lineage | Status |
|---|---|
| S1–S4 / EA | Failed attempts to force distinctiveness through a constrained body envelope |
| RF1 / RF2 | Failed human-donor transformations |
| RS1 / RS2 | Failed low-quality blank-clay source generation |

The recovered-source route (GO-RD*) is the authoritative active path.

## 10. Principal hashes (SHA-256)

| Artifact | Hash |
|---|---|
| Source GLB (`base.glb`) | `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b` |
| `RD1/GO-RD1-REF.obj` | `06a60503bd1341cceac436acfb1f0e76db786a429c821677079bdcff60e16ebe` |
| `RD2/GO-RD2-REF.obj` | `b1c832dc21ef52756054a1158a872ca57cfb7f70718a465937652a0b4e7bcf06` |
| `LOW/GO-RD2-LOW.obj` | `3ee57857d141aaef54e9ae499becd0874b7f4e79d67a14d09a016af4c32f8e43` |
| `ORG/GO-RD2-ORG-REF.obj` | `140740e50cd4a31c8358cdb667961985b3d5afb4b88f04d4baefd64bd293c4c9` |

All other files are listed in `SHA256SUMS.txt`.

**Rebuild order:**
1. `xf.py` (F1 → GO-RD0-SOURCE)
2. `vox.py 0.5`
3. `field.load` → `O0.npz`
4. `rd1.py rd1_params_RD2.json`
5. `finish.sh`
6. `rd_brush.py strokes2.json`
7. `low.py` and `org.py` on the RD2 field

The scripts carry the session scratch path, as in earlier blocks.

## 11. Confirmation

- The source master (`base.glb` and the E: copy) is untouched.
- Old 05A–05M evidence is untouched.
- Grask E3 is frozen.
- No validator, threshold, scorer prompt, tally rule or body canon rule was changed. Only the beastfolk lines in §2 changed.
- No Rodin run, no regeneration, no digitigrade conversion, no rig, no UE5, no Stage C.

I stopped at the RM-OT-05N author gate.

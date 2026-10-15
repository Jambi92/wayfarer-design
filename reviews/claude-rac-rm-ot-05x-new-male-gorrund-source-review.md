# RAC RM-OT-05X — review of Tyler's new male Gorrund GLB (no repair)

**Order:** `reviews/chatgpt-rac-rm-ot-05x-new-male-gorrund-source-review-order.md`.
**Date:** 2026-10-15.
**Evidence:** `reviews/rac-rmot05x-source-review/`.
**Drivers (new, read-only):** `tools/rac/w1/rmot05x_drivers/`.
**Criteria used:** the 05W source brief, the negative checklist and the review spec (`reviews/rac-rmot05w-source-brief/`).

## Recommendation

**REVISE AT SOURCE.**

The new GLB is a strong **direction** and a clean, high-quality sculpt:
- a convincing leonine head;
- an integrated tail;
- an upright neutral stance;
- five-toed plantigrade humanoid feet;
- one closed manifold surface with no self-intersections.

It is not suitable as a source for **bounded** corrections, for two reasons:

1. **Composition.** The body is a fully defined bodybuilder: striated pectorals and deltoids, a six-pack, vascular forearms, high trapezius. The body-only views read as a muscular human. Getting to reference composition would mean re-sculpting muscle over essentially the whole body.
2. **Pelvis.** The fitted shorts are **fused** into the only surface. There is no skin under them, and they cover the iliac crest / ASIS, the inguinal line, the gluteal fold and the sacrum. The tail root sits on the shorts. Exposing the pelvis would repeat the whole-region reconstruction dependency that 05N–05V showed fails.

Both changes are broad, so the order (§6) says to revise at source rather than start another salvage campaign.

**Status:** nothing was edited. Gorrund is **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**; D4 / UE5 / production rigging / creator **NOT STARTED**.

## 1. Intake and provenance (§1)

| Item | Value |
|---|---|
| Received | `Gorrund.glb`, attached by Tyler in this session on 2026-10-15. Stored as the upload `914cd24a-Gorrund.glb`. |
| Size / SHA-256 | **30,470,312 bytes** / **`1c23b92b7d2faa88ce629d6ccb6d795502d4b704c52af2fcf10b2b34bdd83170`**. Matches the order. |
| Container | glTF 2.0. One scene, one node `model`, one mesh, one triangle primitive (POSITION, NORMAL, TEXCOORD_0). One material `model`: base colour 0.5 grey, metallic 0.05, roughness 0.4, double-sided. No textures, images, skin, rig or animation. **Identity node transform.** |
| Exporter | `Khronos glTF Blender I/O v4.3.47`. The file was last written by Blender's glTF exporter. |
| Generation provenance | **Unknown.** There is no job record in the PC Rodin pipeline: `Jobs\` and `Source-Masters\` still hold only the Vael records and masters. No service, image or tier is claimed. |
| Designation | Male, as Tyler designates it. No sex-specific rule is imported into GORRUND_V1. |
| Master | Immutable copy kept read-only in the session. A copy is placed on Tyler's PC at `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Male-05X\Gorrund.glb`. It is not committed to the repo or canon, and it is kept separate from `base.glb` (`78ecfa87…`), U8, N1 and the old `Gorrund-Male`. |
| Working copy | A separate copy was used only for reading and rendering. Its hash is unchanged after review (`1c23b92b…`). |

## 2. Views (§2)

All renders use Blender Workbench: neutral grey, studio light, orthographic, matched framing. The whole-figure and body-only sheets share a 10 cm grid in **raw source units** (not stature).

| Sheet (`views/`) | Content |
|---|---|
| `01_whole_untouched.jpg` | Front, left profile, back, front 3/4, rear 3/4, rendered straight from the GLB. |
| `02_bodyonly_diagnostic.jpg` | Body-only front / profile / back / 3/4 from a **disposable diagnostic copy** (see below). |
| `03`–`09` | Close-ups: head / neck / girdle; chest depth and back; waist / pelvis / shorts / tail root; axillae; knees / shanks / ankles; hands; feet (front, lateral, sole). |
| `10_matched_height_vs_controls.jpg` | Body-only candidate beside the frozen controls (MF-ref / brd, SK-ref / brd / low, GR-E3-ref / low). Displayed-height normalization only. |

**The diagnostic copy** (`x_bodyonly.py`, `geometry/bodyonly_diagnostic_cut.json`):
- It deletes faces only: 122,923 head faces above raw z 160 (the neck minimum is at 162) and 74,163 tail faces behind the buttock plane.
- It is not a repair, and it is excluded from every topology claim in §3.
- All six body-only tiles pass `w_tile_check.py`: one silhouette each, no fragments (`geometry/tile_check_bodyonly.json`).
- A short tail stub remains visible in the body-only profile because of the cut position. It is part of the body, not a fragment.

**Presentation difference, disclosed:** the controls are smooth procedural bodies. The candidate carries real sculpted surface detail. Nothing was smoothed to match. No blind scoring was run.

## 3. Geometry, pose and scale (§3; read-only; `geometry/inspection.json`)

| Check | Finding |
|---|---|
| Axes / units | glTF Y-up; the figure faces **+Z** (glTF front). Ground is at Y 0 (lowest vertex). Values below are raw units × 100 ("raw cm"). |
| Bounds (glTF) | X −0.4309…0.4313; Y 0…1.8990; Z −0.6748…0.6756. The body occupies glTF Z ≈ +0.20…+0.676, with the muzzle at the front limit. The tail alone reaches back to −0.675, which is why the Z extent is so large. |
| Vertex split vs disconnection | 577,159 exported vertices weld to **499,998 positions**. The 77,161 extra vertices are UV / normal seam duplicates, not separate parts. |
| Components / manifold | After welding: **1 connected component**; 0 boundary edges; 0 non-manifold edges; consistent orientation. **One closed orientable surface.** |
| Genus | Euler characteristic −2, so **genus 2**: two small handles. Section scans place them most likely at the **axillae**: small closed loops 3–10 raw cm in perimeter at raw z 128.5–129.5, x ±23, between the inner upper arm and the chest wall. These are local features and were not repaired. |
| Self-intersection | **0 faces.** Scope: whole welded mesh, triangle–triangle test (pymeshlab), all 1,000,000 faces. |
| Triangle quality | Median edge 0.29 raw cm; median minimum angle 34.5°. 20,985 faces are below 10° and 106 below 1°; the minimum is 0.08°. These are generator-style slivers, with no zero-area faces. Below the U6–U8 10° floor in places; relevant only to future local edits. |
| Raw height | Midline skull vertex **189.0 raw cm**; ear tips 189.9 (the topmost point is an ear). No hair or mane over the cranium. |
| Scale vs canon | If the units are taken as metres, the figure is about **1.89 m against the 229 cm nominal reference**, a factor of about 0.83. The order's caution is right: the Y extent is not the intended stature, and AI-generated meshes are usually unit-normalized. **Not fixed; no uniform scaling.** Any future stature work would be by proportion (RA R-2). |
| Head carriage / spine | Upright. Head level, slightly forward of the trunk as in a natural lion-like neck. No hunch. |
| Knees / hips | Extended, not crouched. Straight shanks in profile (`07`). |
| Feet | Parallel and about hip width; toes forward. **Five toes per foot with toenails**; plantigrade; no claws or paws (`09`). Foot length about 35 raw cm, about 18.5 % of raw height. |
| Heel contact | The forefoot carries contact. Heels sit about **1.7 raw cm** above the lowest sole point, roughly a 3° whole-figure pitch. This is a small R-6 item that a rigid pitch could address later. Not changed. |
| Arms / hands | Arms hang close to the body with small abduction; slight elbow flexion. Palms face the thighs, hands loosely curled. **Five digits with a thumb and nails** (`08`). Fingertips at about 71.5 raw cm (0.38 of raw height). |
| Tail | Single continuous surface rooted at raw z 99–110 on the **back of the shorts waistband**. It hangs and sweeps back; lowest point 48.7 raw cm, so **no ground contact**. At least 19 raw cm clear of the legs. |
| Crotch | 81.0 raw cm on the shorts surface (0.43 of raw height). A garment surface, not an anatomical landmark. |

**Limits:** all levels are rig-less surface estimates. No skeleton or joint centres are claimed. Skin-surface ratios include composition and are diagnostic only (GO L214).

## 4. Special review points (§5)

**Shorts.** They are present: fitted athletic shorts with a waistband, side stripes and hems.
- They are **fused**. The mesh is a single closed surface with no internal or second surface, so **there is no skin beneath** them.
- Covered landmarks: iliac crest, ASIS, inguinal line, pubic region, gluteal fold, sacrum, and upper thigh to mid-thigh. The navel sits just above the waistband.
- The tail emerges from the shorts.
- **They are not a harmless proxy.** Exposing the pelvis means reconstructing the whole pelvic and gluteal surface and re-rooting the tail, which is the reconstruction dependency 05N–05V showed fails (05W §1).

**Massiveness: structure or muscle?** Visually it is **mainly current muscularity** (`02`, `04`, `10`):
- striated, separated pectorals and deltoids;
- a six-pack and serratus;
- vascular forearms;
- a high trapezius mass carrying the neck root.

What the structure itself shows:
- The skeletal frame cues GORRUND_V1 relies on are not evident beyond a muscular human: deep thorax independent of pectoral mass, thorax-carried girdle, depth-led pelvis, large joints, large hands and feet. Hands and feet are ordinary human-scale for the figure.
- The chest depth seen in profile is mostly pectoral and abdominal muscle, not visibly a deeper ribcage.

Per order §5, no deflation or LOW was attempted.

**Head.** A convincing lioness-like leonine head: muzzle, rounded broad ears, no mane. The chin carries a small fur tuft. That conflicts mildly with R-8 (no facial hair); it is a minor, local item.

**Hands, feet, nails.** Confirmed from the mesh: five fingers including a thumb, and five toes, with ordinary nails. No claws or paws (`08`, `09`).

**Concept vs mesh.** The GLB matches the described concept direction: fitted shorts and strong muscle definition. The generated turnaround is not treated as proof of anatomy; everything above is from the mesh.

## 5. Whole-body source gate (05W REVIEW_SPEC Q1–Q4)

| Q | Answer | Evidence |
|---|---|---|
| Q1 Coherent adult organism with Gorrund structural identity **at suitable reference composition** | **No.** The organism is coherent and adult, and the head and tail are well integrated. But the composition is far from reference (RA R-4), and identity is carried by muscle, not shown at neutral composition (GO L21–23, L83, L250). | `01`, `02`, `04` |
| Q2 Distinct from enlarged human / Skarn, rangy Grask, bodybuilder or ogre caricature with head, tail and presentation hidden | **No** for bodybuilder, enlarged human and Skarn: body-only it reads as a very muscular human (checklist B1, B3, E2). **Yes** for Grask: not rangy or limb-dominant. **Yes** for ogre: upright, not hunched or bow-legged. | `02`, `10` |
| Q3 Suitable neutral pose, five-toed plantigrade feet, visible landmarks, anatomical continuity from the start | **Partly.** Pose, feet, hands and continuity are good, with only a small heel pitch. **Pelvic landmarks are hidden by fused shorts** (checklist A1), plus the minor chin tuft (A2). | `05`, `07`, `08`, `09` |
| Q4 Quality sufficient for later work to stay genuinely localized | **No.** Surface quality is high: closed manifold, no self-intersections, convincing sculpt. But the needed changes are not local: whole-body composition, plus pelvis reconstruction under the shorts. | `02`, `05`, `inspection.json` |

**Three conclusions, kept separate (§4):**

1. **Visual / source-direction preference: positive.** The head, tail, upright stance, feet, hands and sculpt quality are a much better direction than any previous Gorrund source. Tyler's preference is respected and recorded.
2. **Suitability as an external source for bounded corrections: not suitable as is.** The two required changes are broad.
3. **Compliance as a final neutral anatomical reference: no.** It fails R-4, R-7 (garment over landmarks), R-8 (minor) and R-6 (minor heel pitch). Its gate status is not changed by Tyler supplying or liking it. It was also not rejected over any unapproved builder ratio or old lineage hash.

## 6. Proposed next step

**REVISE AT SOURCE.** Keep this GLB as the preferred **direction reference**:
- head;
- tail and its carriage;
- stance;
- feet and hands;
- sculpt quality.

Make one revised generation or sculpt that changes only:

1. **No shorts.** Unclothed, or a minimal low-rise brief **below the iliac crest / ASIS** that leaves the gluteal fold and sacrum readable. The tail must root on the body (sacral region), not on a garment.
2. **Reference composition.** Ordinary healthy muscle and fat: no striations, six-pack, vascularity or bodybuilder trapezius. Not skinny either.
3. **Skeletal cues carried by the frame, not muscle** (GO L39–46, L190, L218, L236):
   - visibly deep ribcage;
   - broad girdle sitting on the thorax;
   - deep, robust pelvis;
   - substantial knees, ankles and wrists;
   - large but proportionate hands and feet.
4. **No chin tuft.** Short fur only.
5. **Both heels down.**

Prompt wording for this is in `reviews/rac-rmot05w-source-brief/SUBMISSION_PACKAGE.md` §1. Its negative list already covers shorts-style clothing and bodybuilder definition, and the "fitted shorts" concept should be replaced.

**One piece of metadata that matters:** which tool or service produced this GLB, and from which image(s). If it can regenerate from an edited image or prompt, the revision can keep this direction. No paid generation is authorized by this order.

**Possible correction scope, if the author nevertheless rules to keep this mesh.** Illustrated only; not performed:
- whole-body muscle reduction, all of `02` / `04`: broad;
- pelvis and gluteal reconstruction under the shorts, with tail re-rooting (`05`): broad;
- chin tuft (`03`): local;
- the two axillary handles (§3): local;
- a rigid about-3° pitch for heel contact: rigid.

The first two are not bounded corrections, which is why revision at source is recommended.

**STOP.** No geometry repair, LOW build, blind scoring, canon measurements, scaffold, ARM acceptance or Stage C.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**; D4 / UE5 / production rigging / creator **NOT STARTED**.

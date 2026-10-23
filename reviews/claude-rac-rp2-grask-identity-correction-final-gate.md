# RAC RP2 — Grask identity correction: final gate

**Date:** 2026-10-23
**Order:** `reviews/chatgpt-rac-rp2-grask-identity-correction-and-completion-order.md` (4d39cbd)
**Baseline:** RP2 production v001 (`742cd6f`). It is preserved unchanged.
**Executor:** Claude. Autonomous execution; every exploratory candidate was gated and rejected internally (§9).

**Status: RP2 GRASK IDENTITY-CORRECTED PRODUCTION BUILD PASS / READY FOR AUTHOR REVIEW**

## 1. Candidate

| Item | Value |
|---|---|
| File | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_production_v002.blend` |
| Companion files (same folder) | `…_v002.json` (sidecar), `…_v002_landmarks.json`, `…_v002_edit_masks.npz`, `…_v002_mpfb_mapping.npz` |
| File SHA-256 | `9622a062da2a756bb14e1dc630f6f4e5311ce19fbf598ea276b96674feae23ee` (PC readback match) |
| Geometry hash | `0b938028d4aa1f7796e706ed8940f217610f11a0ae70b05bc4a0862044ce15dc` (float32 co + int32 loops) |
| Object | `GR_U_REF_RP2_production_v002`, the only object. Blender metres (x, −f, u)/100; world matrix identity. |
| Topology | Identical to v001: 214 146 vertices, 214 144 quads, same vertex and face order. The MPFB mapping attributes are carried unchanged. |
| v001 | Still on the PC with its original hash `81f579f9…9c0a`; not overwritten. |
| Source | GR5DE3 `d859eb18…d778`, unchanged. |

## 2. What was wrong with v001 / E3 (the human read)

- **Head.** The facial proportions were human:
  - brow line to menton 16.3 cm on a 27.2 cm crown-to-menton head;
  - a human nasion dip;
  - human cheek planes, small chin, human lower face.
- **Ears.** Human ears: a 6.5 cm auricle with a round helix, and almost no stand-off in the front view.
- **Front body.**
  - A tall lean human trunk with a human pectoral shelf.
  - A thin human neck, so the head floated on the body.
  - Smooth human joints: elbows, knees, wrists and ankles had no skeletal read.
- **Hands.** Slender human hands, 29.4 cm, 0.77 of forearm length, with tapering human fingers.
- **Feet.** A human foot scaled up: 35.7 × 13.9 cm, human toe fan and heel.
- **v001 surface flaw.** The production build froze the lips and eyelids to the faceted 13k reference, which left a dent beside the left mouth corner and rough orbits. That is visible in v001 (`sheet_2_head.jpg`, middle row).

## 3. What changed

All changes are smooth, author-directed warps evaluated per production vertex on the unchanged v001 topology:
- MakeHuman CC0 hm08 morph targets transferred by the production's own interpolation operator;
- procedural craniofacial, ear, hand and foot warps;
- limb breadth profiles and bony relief.

The exact parameters are in `tools/params_v002.json`.

| Region | Change |
|---|---|
| **Face / head** | Facial vertical elongation below the brow line, +22 %: brow-to-menton 16.3 → 21.3 cm. The cranium, the crown (stature) and the ears are fixed.<br>Continuous supraorbital torus and glabella; nasal root raised into a continuous brow-nose line.<br>Vertically elongated zygomatic body over a flattened infrazygomatic plane.<br>Deeper mandibular ramus and gonial angle; taller, broader chin (lower face +6 % width at the angle).<br>Midface narrowed 6 %; forehead set back; longer moderate nose (bridge, root width). Wider mouth, longer upper lip.<br>No tusks, no muzzle, no projection change (canon AD-R41). |
| **Ears** | Late-taper warp in the ear's own frame:<br>— upper auricle elongated 1.6× above the concha, so length goes 6.5 → 8.7 cm (moderate–strong for head height);<br>— the upper-ear body is widened up to +28 % ("sustained upper-ear body");<br>— taper only in the last 16 % of the length ("late terminal taper", not an elven blade);<br>— cartilage fold relief amplified 0.6×, lobe enlarged, more lateral stand-off (front-view read).<br>The humanoid auricular root is kept. |
| **Front body** | Narrower, deeper trunk between z 130 and 160 cm (breadth −5.5 %, depth +5 %), so the limbs dominate the front silhouette.<br>Sternal keel ridge; pectoral shelf reduced.<br>Thicker integrated neck: +8 % at the base, smooth spatial mask.<br>Clavicle shafts and acromion prominent.<br>Joint breadth profiles: knee +12–13 %, mid-thigh −2.5 %; elbow +13 %, mid upper arm −3 %; proximal forearm +7 %; slender long tendon run of the shank −5 %; wrist +5–8 %; ankle +7–10 %.<br>Olecranon, epicondyles, patella, femoral condyles, tibial tuberosity, shin crest, styloids, malleoli, ASIS and trochanter in bony relief (3–7 mm).<br>No global muscle, no V-taper, no hunch. |
| **Hands** | Hand scale +5 % about the wrist; fingers +5 % longer (thumb +3 %); fingers +14 % thicker.<br>Knobby MCP / PIP / DIP joints and broad spatulate pads.<br>Palm broadened +7 % across the metacarpal heads.<br>Length 29.4 → 32.5 cm (0.86 of forearm). Five digits, ordinary nails, no claws. |
| **Feet** | Toes +16 % longer, gently fanned, hallux separated.<br>Forefoot +6 % broader at the metatarsal heads; posterior heel projection 2.2 cm; high instep; knobby toe joints.<br>35.7 × 13.9 → 39.2 × 16.6 cm (0.63 of shank). Plantigrade, five digits, ordinary nails, sole and ground contact unchanged. |
| **Face surface** | The face is rebuilt from the interpolated adjudicated reference and faired, with lips and eyelids protected. This removes the v001 mouth-corner dent and the facet striation. |

Delta from v001, per edit mask (`GR_U_REF_RP2_production_v002_edit_masks.npz`, `gates/identity_gate.json`):

| Mask | Vertices | Max | Mean |
|---|---|---|---|
| Head / face / ears / neck | 71 853 | 55.3 mm | 13.2 mm |
| Hands | 51 043 | 31.8 mm | 14.6 mm |
| Feet | 34 059 | 36.8 mm | 16.5 mm |
| Front-body carriers | 36 996 | 15.6 mm | 3.9 mm |
| Unchanged (< 0.5 mm) | 21 076 | 0.5 mm | 0.1 mm |

## 4. What was preserved

- **Stature:** 217.916 cm, −0.72 mm against E3 (T-3 PASS). Ground contact is unchanged.
- **Limb architecture:** long-limb / short-torso, long forearm and shank, plantigrade upright stance, the accepted girdle line (the Class C shoulder base).
- **Rig joints:** all unchanged except the hand and foot ones listed in §5.
- **Rangy, non-bulky build:** no global muscle; body volume 108.0 → 111.6 L, nearly all of it in head, neck, hands and feet.
- **Production topology:** the v001 Grask branch (crotch slot, axilla patches) and the MPFB mapping.
- **Cross-race distinctions:**
  - Skarn: no power-torso widening.
  - Aelari: an elongated but structurally heavy face, folded non-elven ears and knobby joints.
  - Gorrund: no claws, muzzle or compact mass.

## 5. Technical result

| Gate | Result |
|---|---|
| Components / boundary / non-manifold edges and vertices / genus | 1 / 0 / 0 / 0 / 0 |
| Degenerate faces / coincident vertices / unused vertices / directed-edge duplicates | 0 / 0 / 0 / 0 |
| **Self-intersections** | **0**: float64 design data and the float32 stored file, both quad diagonals |
| Normals | Outward; volume +111.60 L (Blender frame) |
| Quads overall / in deformation zones | 100 % / 100 % |
| T-4 (quality target) | Angles 45–135°: 97.88 % (v001 98.05). Aspect ≤ 4: 95.49 % (v001 94.50). Minimum edge 0.039 mm. |
| Zone audit with the v002 joints | Loops pass, creator density pass |
| T-1, unchanged region vs adjudicated target H | prod → ref median 0.20, p95 0.81, max 1.83 mm; ref → prod 0.32 / 1.11 / 2.03 mm — **PASS** |
| T-3 | Stature −0.72 mm — **PASS**. Bounding box changes intentionally: x ±3.2 mm (ears, hands), forward +30.6 mm (toes), back −1.7 mm (heel). |
| T-6 | 106 heads and tails (incl. root): 42 unchanged (0.000 mm). The 64 finger and toe-tip joints are re-swept by the intentional hand and foot correction, maximum 23.5 mm at the toe tip (`production/…_landmarks.json`). |
| T-7 | Unchanged-region silhouette IoU vs v001 is 1.000 front / profile / rear, and vs E3 0.9984. Full-silhouette IoU vs E3 is 0.952 / 0.952 / 0.952 (intentional: head, ears, hands and feet). Silhouette area +3.1 % front, +3.8 % profile. Change maps: `sheets/T7_silhouette_change_vs_v001_*.png`. |
| **Deformation (DQS, v002 joints, 48 poses)** | 32 clean, 16 local flexion-crease contact, **0 non-local**, return to rest 0.000 mm. Same classes as v001; `fingers_curl_half` is now clean. Deepest contact is knee flexion 120° at 4.5 mm; the full finger curl has 2.0 mm palm contact. No collapse. Gate results in `gates/deform.json`. |

## 6. Visual result and self-review (§13)

Sheets in `sheets/` compare E3, v001 and v002 on identical cameras with neutral material: whole body, head / midface / jaw, ears, hands and feet, and the body identity carriers.

1. **Does the front view still look like a tall human? No.** A long vertically organized face sits on a thick integrated neck, with ears standing out. The trunk is narrow and deep under long limbs with knobby elbows, knees and wrists, and the hands are large and knobby.
2. **Does the head look human with the ears hidden? No.** There is a continuous brow-nose line under a set-back forehead. The midface is long, the zygomatic bodies are vertical, and the ramus and chin are deep. It is not a muzzle and not a scowl.
3. **Do the ears read Grask, not human or elf? Yes.** A folded, robust auricle carries a sustained upper body and a late terminal taper, with the lobe kept.
4. **Do the hands and feet read as generic human? No.** They are large and knobby with spatulate digits; the feet are robust, with a fanned forefoot and a projected heel. Both stay functional, with five digits and nails.
5. **Troll-like rather than generic orc? Yes.** There are no tusks, no underbite and no bulk.
6. **Still rangy? Yes.** The trunk is narrower; the extra volume sits only in the extremities and joints.
7–9. **Distinct from Skarn, Aelari and Gorrund? Yes** (§4).
10. **Technical regressions? None.**
    - Self-intersections stay at 0.
    - Deformation classes are unchanged or better.
    - Quad quality: aspect is better than v001 and the angle score is 0.2 points below it.

Every answer passed, so the candidate went to turn-in.

## 7. Notes for author review

- The head is larger relative to stature: crown to menton is 32.2 cm, against 27.2 cm on E3. Facial vertical contribution is the main Grask carrier, so this is intended; the canon locks no head-to-height ratio.
- The optional tusk-like canine variant (order §6) was **not** made. The base face passes without it.
- The CC0 MakeHuman targets used (makehumancommunity/makehuman, `data/targets`) are listed in `tools/params_v002.json`.

## 8. Internal candidates rejected (not shown to the author)

| Candidate | Problem | Fix |
|---|---|---|
| MakeHuman-target-only ear | Gradual elven taper | Late-taper warp in the ear's own frame |
| Rebuild via the base-delta transfer | Facet and mouth-corner artefacts from v001 | Face rebuild, lip- and eye-protected fairing |
| Weight-masked facial stretch | Seam at the neck base, then a chin crack, then a shoulder yoke | Spatial neck mask |
| Hand sweep with a chain offset error | Pointed, displaced fingers | Corrected joint-chain offsets |
| Forehead vertical-decrease target | Crown down 20 mm, failing T-3 | Target removed |
| Head fairing on the cranium and soles | Crown −5 mm, sole +0.5 mm | Masked fairing |
| Foot splay 0.45 | Breadth 19.8 cm, too paw-like | Splay 0.22 |
| Hand scale 1.07 | Hand 0.88 of forearm | Hand scale 1.05 |
| Toe thickening 0.18 | 422 toe self-intersections | Toe thickening 0.07 |
| Thigh and upper-arm profiles < 1 at the root | Crotch and axilla contacts | Profile 1.0 to t = 0.3 |

Storage-safe relax of the canthus contacts on every build.

## 9. Scope

No canon freeze, no next race, no rig promotion, no creator, no UE5. RP2 stops here for the author's visual review.

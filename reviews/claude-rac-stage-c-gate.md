# RAC Stage C — combined Grask E3 + Gorrund validation: return gate (C0–C4)

**Order:** `reviews/chatgpt-rac-stage-c-execute-after-d1-d3-order.md` (5aa5501), running `reviews/chatgpt-rac-stage-c-entry-order.md`.
**Rulings:** `reviews/tyler-chatgpt-rac-stage-c-d1-d3-author-ruling.md` (95e7bc3):
- **D1 = (a):** Gorrund reference state only.
- **D2 = (c):** native 204.5225 cm; scaled only for matched pairs.
- **D3 = (a):** Grask E3 is built from the frozen `GR.E3` settings.

**Protocol:** `specs/RAC_STAGE_C_PROTOCOL.md`, written at C0. It adds no thresholds.
**Evidence:** `reviews/rac-stagec-evidence/`.
**Executor:** Claude.
- The run was entirely cloud-side and read-only.
- No geometry was authored. Grask W2 was not rerun or edited. No Gorrund variants were derived.
- No Blender session was opened on the PC.

## Status lines

- **Grask E3 Stage C — CONSTRAIN**
- **Gorrund Stage C — ACCEPT** (reference state only; variant-dependent validation DEFERRED TO CREATOR / N/A, per D1(a))
- **Combined Stage C — CONSTRAIN**

**State:** Stage C **AUTHOR REVIEW REQUIRED**. Grask E3 stays FROZEN. Nothing is promoted. D4, UE5, production rigging, creator implementation, Grask sculpt campaign and Gorrund creator variants are **NOT STARTED**.

## C0 — Sources, hashes, protocol (`checks/source_manifest.json`)

| Source | Result |
|---|---|
| Gorrund `GO-05AW4_nails_final.blend` | `5a4e45d4…2d5e` ✓ matches 05AX4 |
| Gorrund `GO-05AW4_nails_final.glb` | `e6b32503…6fc8` ✓ matches 05AX4 |
| Grask E3 ref 218 (`GR5DE3`) | built from `GR.E3` + 05B arch. **Geometry `a452bf6e…60a0`; file `d859eb18…d778`**, byte-identical to the frozen 05D r6 asset |
| Grask E3 LOW / Narrow (`GR5DE3N`) / Broad (`GR5DE3B`) | geometry-identical to the frozen 05D assets (`f77d05cc…`, `5802e262…`, `a58ad8d7…`). N / B file hashes differ only in npz metadata |
| Grask E3 stature points 198 / 208 / 229 / 239 | new builds with the same settings. Geometry `f4c0a62a…`, `b718a221…`, `231af728…`, `095fc685…` (full hashes in the manifest). Not saved as frozen assets |
| Roster comparators (11 r6 assets) | all match `reviews/reference-assets/manifest.json` ✓. Skarn `SK208-C1R` hashed from W3D geometry |
| Saurin canonical W2 base | `f86ae800…fdee` ✓ |
| Re-hash after the run | all frozen sources unchanged ✓ |

**Reproduction proof** (protocol §4):
- W1 → W2C rebuild of the W2 Grask bodies: canonical rows identical (1083 rows over all bodies).
- The `stc_w2c_eval.py` frozen-comparator adapter reproduces **373 / 373** committed W2C checks: 0 result differences, maximum value difference 1.4e-14 (`checks/w2c_reproduction_val.json`).
- The E3 builds match the frozen 05D assets (above).

**Narrow / Broad frame records.** These were reconstructed from the W2C frame definitions and verified bit-exact against the frozen N / B builds (`checks/frame_record_GRN5.json`, `checks/frame_record_GRB2.json`).

## C1 — States

| Race | States |
|---|---|
| Gorrund | **Empty** (D1(a)). Narrow, Broad, low / high composition and the stature series are all **DEFERRED TO CREATOR** |
| Grask E3 | reference 218, LOW, Narrow (GRN5 frame), Broad (GRB2 frame), and stature points 198 / 208 / 229 / 239. These are the states the frozen E3 contract and W2C suite already define. The named W2 extremes are not re-derived (protocol §1) |

## C2 — Validator suite

### Grask E3 — W2C suite (`checks/w2c_E3.json`; classified in `checks/w2c_E3_nonpass_classified.json`)

**368 checks:** 325 PASS / REPORT and 43 non-pass. The non-passes break down as follows.

| Class | n | Meaning | Disposition |
|---|---|---|---|
| **I** inherited | 14 | Already non-pass in the committed W2C record (knee / femur and thoracic-breadth continuity; G at 198 / 229 / 239 and the named extremes; GR198 knee slope) | Not a Stage C regression |
| **P** protected relation read on the organized surface | 8 | Continuity of bitroch / crest, crest / thoracic and shoulder / thoracic | Author ruling 2: diagnostic only. On the protected skeleton stations GR-P2b reads 1.1968–1.1972 ≥ MF 1.1918 (**PASS**), and GR-P6 is unchanged from the accepted route |
| **N** retired / mixed comparator | 13 | F: Broad thoracic depth vs procedural GO217 / GO224. M / X: W2 named extremes vs the E3 central | **N/A** (protocol §3.2–3.3) |
| **R** report / risk | 4 | D: GRN5 elbow (−1.0 %) and knee (+0.7 %) are NOT DEMONSTRATED. K: GR229 / 239 knee breadth is ≥ 3 % off the allometric slope | REPORT. These are risks, not gates |
| **G** canonical-row bundles | 4 | GR208, GR218, GRN5 and GRB2 went from PASS at W2C to NOT ALL PASS. Itemised below | Itemised |

### Grask E3 — canonical G rows (`checks/w2c_E3_G_rows_classified.json`)

Rows passing: 198 44/57, 208 46/57, **218 48/57**, 229 47/57, 239 48/57, N 47/57, B 49/57.

| Row (218 value vs comparator) | Class | Disposition |
|---|---|---|
| GR-P2b bitroch / crest: skeletal CIB 1.1513 vs MF 1.1992; skin 1.124 vs 1.163 | P | Protected station reading **PASS** (1.1970) |
| GR-P6 pelvis / thorax ~ MF: 1.0586 vs 0.964 | P | Protected station reading unchanged from the accepted route |
| **GR-G1 shoulder-joint / thoracic: 1.304 vs ≤ 1.249; biacromial / thoracic 1.274 vs ≤ 1.185** | **P\*** | Organized-surface reading. The frozen 05D method has **no protected-station reading for GR-G1**, so it cannot be cleared by ruling 2. **AUTHOR CONFIRM** that ruling 2 also covers GR-G1. The E3 skeleton is unchanged from 05C (`guard_all`: joint delta 0, bone scales equal). |
| **Directional: thoracic depth never approaching DU** (Durrim): 0.1681 vs DU 0.1602 | **A** | E3's deep keel chest, which the author accepted (05E ruling 1), now exceeds the Durrim proportional depth. This W1 directional row conflicts with the accepted E3 direction. **AUTHOR RULING** |
| AD-G7, GO-P3, "GO > GR" depth / joint rows | N | Comparator is the retired procedural Gorrund. **N/A**. Diagnostic: in the matched-height profile silhouette (62–76 % stature band), the sculpted Gorrund is still deeper than Grask E3 (0.188 vs 0.170 of stature; `checks/chest_depth_profile_diag.json`), so the intended Gorrund > Grask depth relationship holds visually. |

**05D minimal guards** (frozen record; the builds are identical):
- stature and ground;
- skeleton unchanged;
- outward normals and true floor;
- self-intersection (piercing edges at or below the route);
- arm clearance (min 0.70–1.08 cm, 0 inside);
- posture equal to 05C.

All pass for reference, LOW, N and B.

### Gorrund — validator map

| Validator | Result | Reason |
|---|---|---|
| W2D U, G, S, K, AD3, D families | **N/A** | They need MPFB rig joints, vertex-group slab breadths (jbw), the composition grid (CIB) and ALPC stations. The sculpt has no rig, weights or composition route |
| W2D C, B, F, M, X families (continuity, Frame, composition, extremes) | **DEFERRED TO CREATOR** | They need variant or stature states (D1(a)) |
| Canonical G rows (GO candidate) | **N/A** | Same inputs as the W2D families; the procedural GO bodies are retired |
| UFCA / MPFB / ALPC guards | **N/A** | No MPFB proxy and no station set |
| Mesh integrity (05AX4) | **PASS** | Hash-identical to 05AX4: 1 / 0 / 0, genus 3, 0 self-intersections, 0 seams |
| Stature | **204.5225 cm** (native, D2(c)) | Below the canon envelope minimum of about 208. **Not revised** (D2(c)); recorded as a risk |
| Canon identity (leonine, plantigrade, tail, 5 digits) | **PASS** | 05AX4 and the C3 read |

## C3 — Full-roster read

**Sheets** (`sheets/`):

| Sheet | Contents |
|---|---|
| `lineup_ref.jpg` | All 13 roster reference bodies at common world scale; front and profile |
| `matched_208.jpg`, `matched_218.jpg`, `matched_229.jpg` | Grask E3 vs the Gorrund comparison copy (D2(c) factors 1.017 / 1.066 / 1.120) vs Skarn / Marchfolk; front, 3/4, profile and rear |
| `silhouettes.jpg` | Body-only silhouettes |
| `grask_E3_states.jpg` | Grask E3 reference, LOW, N and B |
| `gorrund_reference.jpg` | Gorrund sculpt |

**Silhouette overlap** (REPORT-only; `checks/distinct.json`). IoU values are raw → after the best horizontal stretch.

| Pair (matched height) | Front | Profile |
|---|---|---|
| **Baseline:** accepted-distinct Skarn 208 ↔ Marchfolk 203 | 0.774 → 0.892 | 0.838 → 0.901 |
| Grask E3 208 ↔ Skarn 208 | 0.742 → 0.842 | 0.826 → 0.831 |
| Grask E3 229 ↔ Skarn 229 | 0.756 → 0.853 | 0.834 → 0.838 |
| Grask E3 ↔ Gorrund (208 / 218 / 229) | 0.47–0.48 → 0.66–0.67 | 0.54 → 0.61–0.62 |
| Gorrund ↔ Skarn / Marchfolk | 0.54–0.60 → 0.74–0.76 | 0.54–0.60 → 0.65–0.70 |

Grask overlaps Skarn less than the accepted Skarn ↔ Marchfolk pair does. The profile stays separate after the width stretch (0.83), which means the separation is not only thin-vs-broad.

**Blind read** (`blind/blind_read.md`). An independent agent with no context saw three letter-coded sheets.

*Grask vs Skarn, Marchfolk and Gorrund.* Grask (C at 208, E at 229) was judged **different from Skarn, Marchfolk and Gorrund by structure (c), not by thinness or size**. The cues it named were:
- long arms reaching near the knee;
- a dorsal mass with a matching chest mass in profile;
- leg proportions.

*Gorrund vs all.* Gorrund (B, G) was judged different from every other body by structure: head, tail, paws and musculature.

*Grask states.* Grask states H–K were judged **one coherent species with orderly differences**.
- The reader's note that K "is not leaner" reflects a wrong label in my prompt: K is the LOW composition (more soft tissue, 115.8 L vs 107.9 L), so a fuller belly is the correct read.
- Profile differences between the Grask states are small.

*Pre-existing roster note.* The reader judged Skarn 208 and Marchfolk 203 the "same species, differing only by thinness". This pair was accepted before Stage C and is outside this order. It is listed under risks.

**Visual checks (entry order §7):**

| Check | Result |
|---|---|
| Grask readable at matched heights | ✓ in profile, 3/4 and rear (dorsal mass, keel chest, long forearm, high calf). **Weak in pure front view**, where it reads close to a tall bald mannequin |
| Gorrund readable at matched heights | ✓ |
| Neither collapses into Skarn / Marchfolk | ✓ (structure (c) in the blind read; IoU below baseline) |
| Separation not by scale or thin / broad alone | ✓ |
| Saurin coherent | ✓ Reptilian head, clawed feet and long tail; it reads as its own species and sits consistently in roster scale at 188 cm. It is a detailed sculpt, like Gorrund (visual read only; it was not in the blind sets) |
| Canon identities preserved | Gorrund ✓ (leonine plantigrade beastfolk). Grask E3 matches its accepted 05D / 05E direction |

**Canon caution, carried from 05D §8.3 and seen again.** The blind reader called Grask's long arms and front / back masses "closest to a caricature … a deliberate distortion". No body read as digitigrade or hunched.

## C4 — Recommendations

**Grask E3: CONSTRAIN.** It reproduces exactly, all protected relations pass on the governing skeleton reading, and it reads as its own species. Accept it as the Grask direction with these constraints:

1. **Author confirms** that ruling 2 (skeleton-station reading) also covers **GR-G1**, or orders a protected-station GR-G1 reading. Under this order that reading would be a new measurement, so it was not built here.
2. **Author rules** on the directional row "thoracic depth never approaching DU". The accepted keel chest exceeds the Durrim depth (0.168 vs 0.160 of stature). The options are to retire the row for E3 or to cap the keel.
3. **Creator constraint.** E3 organisation is in absolute centimetres: the 9 cm scapular mass, 3.5 cm keel and 4 cm flank. Across 198–239 this makes shoulder / thoracic, crest / thoracic and bitroch / crest non-monotonic. Scale it with stature in the creator.
4. **Creator constraint.** On the E3 surface the Narrow frame does not reduce elbow or knee breadth by 1 %. Frame breadth at the joints must be carried by the skeleton / frame, not hidden under the tendon cords.
5. **Front-view identity is weak.** Grask leans on profile and back cues. Recommend that the author check the front read; a front cue would need a new order and is not authorised here.
6. **Surface finish.** A shading band shows across the chest / abdomen on the organized trunk, also flagged by the blind reader. It is a loft / normal seam. Carry it to retopology or the creator; it is not a shape defect.

**Gorrund: ACCEPT, reference state only.**
- It is valid as the frozen reference sculpt.
- Integrity is unchanged.
- It is distinct from every roster body.
- Canon is intact.
- Every variant-dependent validator is DEFERRED TO CREATOR or N/A, as listed above.
- The native 204.5 cm stature sits below the canon envelope minimum of about 208. Under D2(c) this is recorded, not revised.

**Combined: CONSTRAIN.** The pair separates cleanly, with the lowest overlap in the roster. Combined acceptance carries the Grask constraints above and these open risks.

## Unresolved risks

1. **Grask GR-G1** has no protected reading (C4-1).
2. **Grask vs the Durrim directional row** (C4-2).
3. **E3 absolute-cm organisation** across stature (C4-3).
4. **Narrow at joints** (C4-4).
5. **Grask front-view read and caricature caution** (C4-5; 05D §8.3).
6. **Gorrund validation is reference-only.** Every W2D-family guarantee (Frame, composition, continuity, allometry) must be re-established in the creator.
7. **Gorrund native 204.5 cm** sits under the canon envelope. The creator must decide how stature is constructed; uniform scaling is not proof of it.
8. **Style mismatch.** Gorrund and Saurin are detailed sculpts; the other eleven bodies are smooth procedural mannequins. Roster reads mix detail level with species cues.
9. **Pre-existing:** the blind reader saw Skarn 208 vs Marchfolk 203 as thinness-only. This is outside Stage C scope.
10. **Gorrund topology debt** is carried from 05AX4: hand loops, left axilla, perineal seam and slivers.

## Evidence (`reviews/rac-stagec-evidence/`)

- `README.md`: index.
- `checks/`:
  - `source_manifest.json`
  - `w2c_E3.json`, `w2c_E3_registry.json`, `w2c_E3_jointbreadth.json`
  - `w2c_E3_nonpass_classified.json`, `w2c_E3_G_rows_classified.json`, `nonpass_raw.json`
  - `w2c_reproduction_val.json`
  - `frame_record_GRN5.json`, `frame_record_GRB2.json`
  - `distinct.json`, `chest_depth_profile_diag.json`
- `sheets/`: lineup, matched 208 / 218 / 229, silhouettes, Grask E3 states, Gorrund reference.
- `blind/`: set1–3 and `blind_read.md` (prompt, key and verbatim answer).

**Tools** (`tools/rac/w1/stagec_drivers/`):
- `stc_build.py`, `stc_w2c_eval.py`, `stc_render.py`, `stc_sheet.py`, `stc_silhouette.py`
- `geomhash.py`
- `stc_registry_E3.json` (the W2C slot registry; `$S` = the W1 scratch root)

STOP at C4 for author review. Waiting for the next ChatGPT / Tyler ruling.

# RAC W3B — Saurin orbital spacing / structural ridges / scale-field envelopes — AUTHOR GATE

**Order:** `reviews/chatgpt-rac-w3a1-final-acceptance-w3b-saurin-orbit-ridge-scale-order.md` (RM-UF-03, RM-UF-04, RM-UB-08)
**Author:** Claude (diagnostic measurement block; returned for ChatGPT author review)
**Evidence:** `reviews/rac-w3b-sa-evidence/` (tables, JSON, sheets) · drivers `tools/rac/w1/w3b_drivers/` · cfg `tools/rac/w1/cfg/w3b/SA-surface.json`
**Status:** DIAGNOSTIC. Every number here is a diagnostic candidate (§22). No numeric range was written into SAURIN_V1.

---

## 0. Verdicts

| Item | Verdict | Reason |
|---|---|---|
| **RM-UF-03 orbital-spacing metric** | **CONSTRAIN** | The bony orbital-margin ring metric is reproducible and tracks a coherent shift to within 4 % of the expected change. Its absolute repeatability is about ±0.2 cm: ring-fit asymmetry is 0.1–0.46 cm. |
| **RM-UF-03 numeric spacing tolerance** | **CONSTRAIN** | The tolerance is asymmetric and depends on the head corner. The safe interval for every corner is **IOD −8.6 % … +3.5 %**. On reference-width or wider crania it extends to **+14.9 %**. The inward bound is strain-limited, so it depends on how the platform is rebuilt. |
| **Vertical / AP orbital placement** | **REMAINS LOCKED** | Vertical and AP position are not separable from the brow, platform and jugal heights without redesigning the skull. Only horizontal spacing was resolved. |
| **RM-UF-04 structural-ridge strength metric** | **CONSTRAIN** | The geometric metric is reproducible: core-minus-flank height above an implicitly smoothed skull, plus the flank slope against the same skull with that family removed. Two weak points: the temporal-line reading partly includes the cranial edge, and the nasal pair cannot be read apart from the canthal ridges. |
| **RM-UF-04 structural-ridge envelope** | **CONSTRAIN** | One hidden strength m is valid over **0.40–1.30** on the naked skull. Folds first appear at the canthal–supraorbital junction. Individual families tolerate more. With scales on, a legibility clamp ties the temporal line to the cranial-plate relief. |
| **RM-UF-04 facial scale-field ranges** | **CONSTRAIN** | Separate size and relief intervals were measured for 7 facial fields. Eyelid and mouth-margin size are bounded on both sides; the lower bound is generator-limited. Several relief maxima were not reached by ×3.0 and are clamped by ridge legibility instead (§6). |
| **RM-UB-08 body scale-field ranges** | **CONSTRAIN** | Bounds must be region-specific; one class-level envelope does not work (§7). On the composition extremes the W2 carried-relief convention already folds (§8), which forces relief clamps per body. |
| **Ridge × scale interaction** | **CONSTRAIN** | Minimum ridge with maximum relief, and maximum with maximum, erase the plane breaks: legibility 0.04 and 0.57. A relationship-aware clamp is required (§9). |
| **Scale-field reproducibility across diagnostic seeds** | **CONSTRAIN** | All 19 relief boundaries tested are stable. 13 of the 19 size boundaries are stable; 6 outer size ends tighten by one test step. The 10 largest body fields were NOT RUN because of compute budget. |
| **W3B Saurin overall** | **CONSTRAIN** | Every item produced a measured, bracketed, diagnostic envelope. None is safe to promote without the clamps and author thresholds listed here. No accepted Saurin biology was reopened. The canonical W2 asset was **not** modified. |

**Required statements (§26)**
1. **Proposed numeric ranges:** §2 (orbit), §4 (ridges), §6 (face), §7 (body), §9 (clamps).
2. **Safe to promote to canon if accepted:**
   - IOD tolerance **−8 % … +3 %** of the W2 reference, with the outward extension clamp;
   - ridge hidden strength **0.40–1.30** (naked skull), with the legibility clamp;
   - the scale-field size and relief **multiplier intervals** in §6–§7, where the outer end is bounded by a demonstrated failure; n.r. ends are capped at ×1.5 for size and at the §9 legibility clamp for facial relief; plus the clamps.
3. **Construction-only:**
   - the orbit warp radii (R0 2.4, R1 5.2, interorbital span 2.0, head-local);
   - the per-family contribution fields, level-set transfer and fairing;
   - the reseed rule, smooth field weights and the 1.7-edge resolution limit;
   - every guard threshold (G1–G6, L/U, S1–S7) as diagnostic criteria;
   - all absolute cm values, which are W2-mesh measurements, not species constants.
4. **Relationship-aware clamps:** §9.
5. **FAIL / MARGINAL / NOT DEMONSTRATED / limits / NOT RUN:** §11.
6. **Persistent files changed:** §13.
7. **Accepted Saurin biology reopened:** **none**.
8. **Canonical W2 reference asset modified:** **NO**. All 8 canonical files have SHA-256 identical before and after W3B (`canon_hash_check.json`).

---

## 1. Foundation and method

- **Canonical source:** `w2i6/canon`, the W2I4 candidate promoted unchanged.
  - 1,124,235-vertex base; surface = `upsample(base) + delta`, 4,496,934 vertices.
  - 130,949 seeds; region fields (FAM / R / H / EL / T / PL / IMB / ATT / TYM).
  - All tests run on copies. The finish route was rebuilt: `build_f({})` = canonical base, max deviation 0.00 cm.
- **Skull frame:** the canonical head is the TS6 / BROW_INT 5 skull SDF, marching-cubed.
  - A diagnostic copy, `w3b_head.py`, matches the canonical face to about 0.1 cm (median residual 0.00 cm).
  - Its only change: ridge amplitudes can be multiplied by RM, and the supraorbital crest can be removed.
- **Level-set transfer:** each skull change is applied to the canonical vertices.
  - Every vertex keeps its own canonical residual φ_ref(p) and moves until φ_new = φ_ref(p).
  - Topology is identical, so region fields and seeds stay attached by index.
- **Display:** naked / minimal-display throughout. No horn, crest or keratin was measured or used (§20).
- **Sex / frame / composition firewall (§21):**
  - every envelope is species-level, measured on SA-M188;
  - SA-F188, frames and composition appear only as carried-deformation guards;
  - no sex-specific spacing, ridge or scale bound was created.

## 2. RM-UF-03 — orbital spacing

**Metric** (`w3b_orbit.py`; measurement-only bony landmark proxy under REFERENCE_ANATOMY):
- **Orbital margin ring:**
  - 36 sectors around the visual axis (yaw 24°);
  - in each sector, the vertex of maximum convexity, taken from base-mesh principal curvature smoothed over two rings;
  - search annulus 1.15–1.6 × the orbit radius, eye surface (FAM 7) excluded;
  - annulus chosen for stability: fit rms 0.16–0.19 cm, against 0.24–0.45 cm for wider annuli.
- **Orbit centre:** centre of the least-squares circle fitted to the ring in its plane.
- **IOD:** distance between the two orbit centres.
- **Normalizers:**
  - bitemporal cranial breadth (behind the platform, independent of the orbit complex);
  - orbital-platform breadth.
- **Companions:**
  - medial margin separation; lateral margin span;
  - orbit centre → rostral dorsal midline;
  - lateral postorbital / temporal support breadth;
  - ring radius; aperture fit (eye surface / margin radius);
  - a cross-check from the globe centre (sphere fit to the eye surface).

**W2 reference:**
- IOD **8.883 cm** (frontal-plane 8.882).
- IOD / bitemporal (12.405 cm) **0.716**.
- IOD / platform (14.188 cm) 0.626.
- Medial margin separation 4.82; lateral margin span 11.51.
- Centre → rostral midline 6.07; lateral support 0.65.
- Ring radius 1.90 (rms 0.19).
- Globe IOD 6.92 cm.

**Spacing deformation:** an integrated orbital-platform shift.
- The skull SDF is evaluated through a smooth lateral space warp.
- The bilateral orbit, lid, aperture, eye room, supraorbital crest, root and shelf move rigidly within 2.4 cm (head-local) of the orbit centre.
- The warp falls to zero by 5.2 cm. Rostrum, cranial vault, jaw and hinge stay fixed.
- The interorbital roof shares the change linearly up to the midline.
- Brow, canthal, postorbital and temporal support refit through the falloff.
- Orbit size, yaw (forward vision), expression, rostral base and jaw are unchanged.

**Guards** (diagnostic thresholds):
- **G1 platform containment:** platform breadth grows ≤ 1 % (beyond that, the orbit complex becomes the lateral head contour).
- **G2 lateral support** ≥ 75 % of the reference.
- **G3 tissue strain** in the interorbital-canthal, brow, postorbital and rostral-base regions within [0.67, 1.5] at the 0.5 / 99.5 percentiles. This is the W2I precedent: ×0.66 was accepted, ×1.5 was flagged.
- **G4** 0 folds.
- **G5** aperture fit within ±3 %; ring rms ≤ 0.30.
- **G6** symmetry within the ring noise + 0.20 cm.

| Head corner | IOD at dx 0 (cm) | IOD / bitemporal | Min valid (cm, %) | Max valid (cm, %) | First invalid inward | First invalid outward |
|---|---|---|---|---|---|---|
| reference | 8.883 | 0.716 | 8.073 (−9.1 %) | 10.210 (+14.9 %) | 8.026 (−9.6 %) G3 | 10.270 (+15.6 %) G3 |
| cranial width −8 % | 8.883 | 0.772 | 8.116 (−8.6 %) | 9.193 (+3.5 %) | 8.026 (−9.6 %) G3 | 9.297 (+4.7 %) **G1** |
| cranial width +8 % | 8.883 | 0.663 | 8.116 (−8.6 %) | 10.170 (+14.5 %) | 8.026 (−9.6 %) G3 | 10.270 (+15.6 %) G3 |
| orbit size −8 % | 8.952 | 0.722 | 8.134 (−9.1 %) | 10.176 (+13.7 %) | 8.057 (−10.0 %) G3 | 10.275 (+14.8 %) G3 |
| orbit size +8 % | 8.884 | 0.716 | 8.076 (−9.1 %) | 10.118 (+13.9 %) | 7.970 (−10.3 %) G3 | 10.222 (+15.1 %) G3 |
| rostrum −15 % | 8.849 | 0.713 | 8.007 (−9.5 %) | 10.173 (+15.0 %) | 7.914 (−10.6 %) G3 | 10.324 (+16.7 %) G3 |
| rostrum +20 % (+ depth / jaw 1.08) | 8.934 | 0.720 | 8.124 (−9.1 %) | 10.148 (+13.6 %) | 8.029 (−10.1 %) G3 | 10.234 (+14.6 %) G3 |
| combined (cw .92, orbit 1.08, ros .85) | 8.833 | 0.767 | 7.937 (−10.2 %) | 9.149 (+3.6 %) | 7.837 (−11.3 %) G3 | 9.244 (+4.7 %) **G1** |
| combined (cw .92, orbit 1.08, ros 1.20 + depth / jaw) | 8.844 | 0.768 | 7.960 (−10.0 %) | 9.166 (+3.6 %) | 7.862 (−11.1 %) G3 | 9.265 (+4.8 %) **G1** |

Steps were 0.05–0.2 cm head-local near each boundary. All 102 cases are in tables.md.

**Findings**
- **Asymmetric:** about −9 % inward against +15 % outward on reference-width heads.
- **Inward limit (G3):** the interorbital-canthal and rostral-base tissue compresses below ×0.67. This is "crowds the rostrum / pinched canthus".
  - It starts at the same shift on every corner.
  - It is construction-sensitive: it depends on how the interorbital roof shares the change.
  - At −0.86 cm per side the orbits visibly crowd the rostral base (`w3b_orbit_spacing.jpg`).
- **Outward limit:**
  - Reference-width heads: brow and canthal web stretch beyond ×1.5 (G3).
  - Narrow crania: the orbit complex pushes the platform's lateral edge out at **+4.7 %** (G1, "excessive lateral placement / loss of the platform"). This happens with cranial width 0.92, alone or combined.
- **Unchanged across the valid range:**
  - forward visual axes (yaw fixed); eye / lid / aperture fit (±1.2 %); ring circularity; 0 folds;
  - frontal eye visibility, so no scowl;
  - the rostral base and jaw do not move.
  - Visually, no human-type collapse and no lateral reptile placement appear inside the valid range.
- **Vertical / AP:** REMAINS LOCKED. A measured secondary tolerance would need the brow-shelf, jugal and platform heights to move, which redesigns the skull (§9 of the order). Not run.

## 3. RM-UF-04 — structural-ridge strength metric

**Families:**
- canthus rostralis (dorsolateral rostral edge);
- supraorbital crest (orbital rim contribution);
- temporal line;
- jugal / maxillary;
- occipital transition;
- mandibular lateral / inferior ridge;
- also reported: postorbital plane-change ridge and nasal pair.

**Contribution field** c_i = φ(family absent) − φ(reference), times the head scale: how far each family raises the canonical surface.

**Metrics:**
- **Strength:** mean ridge height above the implicitly Laplacian-smoothed skull, (M − 2 cm² L) p_base = M p. Computed as the core (c ≥ 0.6 max) minus the flank (within 1.5 cm, no other ridge).
- **Companions:**
  - flank slope: p95 angle against the same skull with that family removed;
  - plane-transition angle;
  - legibility: strength ÷ canonical scale-relief amplitude within 1 cm.

| Family | Strength (cm) | Core height (cm) | Plane-transition p90 (°) | Ridge flank slope p95 (°) | Legibility vs canonical relief |
|---|---|---|---|---|---|
| canthus rostralis | 0.160 | 0.339 | 49.7 | 16.7 | 2.57 |
| supraorbital crest | 0.755 | 0.605 | 58.5 | 17.1 | 11.95 |
| temporal line | 0.091 | 0.399 | 18.0 | 12.3 | **1.18** |
| jugal / maxillary | 0.200 | 0.276 | 29.8 | 10.4 | 8.31 |
| occipital | 0.124 | 0.635 | 17.6 | 5.0 | 1.94 |
| mandibular lateral / inferior | 0.197 | 0.381 | 53.5 | 5.0 | 11.46 |
| postorbital (reported) | 0.098 | 0.238 | 22.6 | 12.2 | 3.51 |
| nasal pair (reported) | −0.069 | 0.319 | 19.1 | 9.9 | — (flank shared with the canthal ridges: measurement limit) |

Annotated family map: `sheets/w3b_ridge_families.jpg`.

## 4. RM-UF-04 — structural-ridge envelope

**Deformation:** φ_m = φ₁ + (m − 1)(φ₁ − φ₀), applied by normal-direction level-set transfer.
- This is exact for the tent-profile ridges; it scales the contribution for the smooth-min supraorbital crest.
- The displacement field is faired over 4 Laplacian iterations. This removes base-mesh transfer folds at the crest front, and the ridges stay ≥ 0.7 cm wide.

**Guards:**
- **Lower, naked skull:**
  - every required family keeps a positive strength (ridges never reach zero);
  - 0 folds; strain p1 ≥ 0.67;
  - the naked skull reads Saurin (visual).
- **Upper:**
  - 0 folds (non-sliver faces);
  - strain p99 ≤ 1.5 (razor / pinched crest);
  - flank slope ≤ 45° (fin);
  - eye visibility ≥ 90 % (no scowl);
  - visual check for armor, facets and caricature.

| Group | Min valid m | Max valid m | First invalid low | First invalid high | Legibility m_min (scaled face) |
|---|---|---|---|---|---|
| **one hidden strength (all families)** | **0.40** | **1.30** | 0.25 (canthal and temporal strength ≤ 0; 42 folds) | **1.40** (fold at the canthal–supraorbital junction) | canthal 0.53, **temporal 0.90**, occipital 0.26 |
| canthus rostralis alone | ≤ 0.25 | 2.0 | not reached | 2.5 (fold, strain) | 0.42 |
| supraorbital crest alone | 0.5 | 1.5 | 0.25 (fold) | 1.75 (fold) | ≤ 0.25 |
| temporal line alone | 0.5 | ≥ 2.5 | 0.25 (strength ≤ 0) | not reached (max tested) | **0.90** |
| jugal alone | ≤ 0.25 | ≥ 2.5 | not reached | not reached | ≤ 0.25 |
| occipital alone | ≤ 0.25 | ≥ 2.5 | not reached | not reached | 0.27 |
| mandibular alone | ≤ 0.25 | ≥ 2.5 | not reached | not reached | ≤ 0.25 |

Global sweep: m = 0, 0.25, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.25, 1.3, 1.4, 1.5, 1.75, 2.0, 2.5, 3.0. Visuals: `sheets/w3b_ridge_strength.jpg`, the global preview, and §9.

**Findings**
- **Regional, not one scalar.**
  - Combined, the families fail first where the canthal ridge runs into the supraorbital crest front (m 1.40).
  - The supraorbital crest alone fails at 1.75. The canthal ridge alone reaches 2.0 before strain and folds.
  - Temporal, jugal, occipital and mandibular reach 2.5 with no measured failure. Above that is NOT DEMONSTRATED.
- **Visual:**
  - At m 1.75–2.5 the rostrum takes hard creases and the brow front reads armored, consistent with the metrics.
  - At 0.4–0.5 the skull softens but still reads Saurin, because the platform, brow shelf, jugal flare and hinge are not ridge families.
  - No scowl at any m: frontal eye visibility stays 0.74–0.81, against 0.79 at reference.
- **Proposed:**
  - hidden strength **0.40–1.30** on the naked skull;
  - per-family caps where a single family is driven: canthal ≤ 2.0, supraorbital ≤ 1.5, others ≤ 2.5 (tested maximum);
  - the legibility clamp in §9 when scales are on.

## 5. Scale-field engine (both RM items)

- **Exact W2 relief formula.** It is g7surfc: anisotropic, size-weighted Voronoi cells, K = 12, with groove, dome and imbrication tilt.
  - A test changes only the named field, by a smooth membership weight. Canonical boundaries and roles stay unchanged.
  - relief = canonical relief + ATT × (core(new) − core(canonical)).
  - Outside the tested field this is bit-identical to the canonical surface, including tympanic, eye and pad extras.
  - Relief-only tests reuse the canonical seeds through an exact linear path (max difference 1e-17).
- **Size tests.** The field is re-drawn with the W2 Poisson-disk sampler (c = 0.5) from the kept boundary seeds.
  - The rng is fixed at 7 for every size value, including the reseeded reference at ×1.0. Neighbouring values differ only in R.
  - The canonical 130,949 seeds are never replaced.
- **Metrics on the field core** (weight ≥ 0.9):
  - size = median nearest-neighbour seed spacing;
  - relief = p95 − p5 of the pure scale relief, extras excluded;
  - aspect = relief ÷ size;
  - span = size ÷ functional bend radius (p10 of 1 / κ_max on the base);
  - crowding = nearest-neighbour coefficient of variation.
- **Guards** (diagnostic thresholds, proposed for author review):
  - **S1 functional span:**
    - deformable fields (fine expressive, articulation, contact): ≤ max(30°, canonical). Beyond this, rigid units facet over the tightest bend: lid, mouth margin, joint.
    - structural / ventral fields: ≤ max(60°, canonical). Beyond this, a unit wraps the limb as an encircling armor band.
  - **S2 hierarchy:**
    - fine / articulation / contact size ≤ 0.80 × the adjacent structural field, and relief ≤ its relief;
    - a structural field stays ≥ 1.25 × the finer fields it borders, with relief ≥ theirs.
  - **S3 integument vocabulary:**
    - relief ≥ the subtlest accepted relief anywhere on the body (mouth margin 0.0097 cm, −3 % tolerance). Below this is a "human-skin patch".
    - aspect ≤ max(0.30, canonical) + 5 %. Above this the read is tubercular, spiky or armored.
  - **S4 topology:** excess folds over the canonical surface's own count ≤ max(2, 10 %), on non-sliver faces.
  - **S5 crowding:** CV ≤ max(0.35, 1.25 × canonical).
  - **S6 ventral:** ≥ 6 units across the ventral field, so it never becomes continuous belly-scute armor.
  - **S7 resolution — GENERATOR LIMIT:** a unit must span ≥ 1.7 mean surface edges, or the field's own canonical resolution if finer (plantar 1.57, palmar 1.73).

## 6. RM-UF-04 — facial scale fields

Sizes are median nearest-neighbour spacings. Multipliers are on the canonical W2 field. "n.r." = not reached within the tested maximum.

| Field | Ref size / relief (cm) | Ref aspect / span | **Size valid (×)** | Size abs (cm) | Size first invalid low / high | **Relief valid (×)** | Relief abs (cm) | Relief first invalid low / high |
|---|---|---|---|---|---|---|---|---|
| orbital / eyelid fine | 0.155 / 0.0145 | 0.093 / 18.2° | **0.8–1.5** | 0.134–0.237 | 0.7 S7 (generator) / 1.75 S1 (lid span) | **0.75–3.0** | 0.011–0.042 | 0.6 S3 floor / n.r. |
| mouth-margin fine | 0.201 / 0.0097 | 0.048 / 23.6° | **0.7–1.2** | 0.152–0.245 | 0.6 S3, S7 / **1.3 S1 (margin span)** | **1.0–3.0** | 0.0097–0.028 | 0.75 S3 floor (it *is* the floor) / n.r. |
| rostrum → cheek transition | 0.212 / 0.0206 | 0.097 / 10.4° | 0.5–2.5 | 0.115–0.536 | n.r. / n.r. | 0.5–3.0 | 0.011–0.060 | 0.4 S3 / n.r. |
| jaw corner | 0.194 / 0.0194 | 0.100 / 14.5° | **0.5–1.75** | 0.103–0.361 | n.r. / **2.0 S1 (plate rigidity)** | 0.5–3.0 | 0.010–0.058 | 0.4 S3 / n.r. |
| auricular recess | 0.229 / 0.0105 | 0.046 / 15.7° | 0.5–1.75 | 0.132–0.414 | n.r. / 2.0 (fewer than 4 units) | 1.0–3.0 | 0.011–0.030 | 0.75 S3 floor / n.r. |
| throat / upper neck | 0.620 / 0.0576 | 0.093 / 18.6° | 0.5–1.5 | 0.315–0.922 | n.r. / 1.75 S2 (approaches the nape structural size) | 0.25–3.0 | 0.015–0.172 | n.r. / n.r. |
| cranial structural (borders the fields) | 0.868 / 0.0752 | 0.087 / 38.3° | 0.7–2.5 | 0.642–1.095 | 0.6 S4 / n.r. | 0.4–3.0 | 0.030–0.225 | 0.25 S4, S2 / n.r. |

**Functional proxies (§13):**
- **Eyelid closure:** unit span over the lid bend (radius 0.49 cm) ≤ 30°. Lid scales stay credible to ×1.5 (0.24 cm). At ×1.75 they facet over the lid.
- **Mouth margin:** speech / expression are limited at ×1.2. At ×1.3 the margin span reaches 32°.
- **Jaw corner:** plate rigidity appears at ×2.0.

**Generator limit:** fine fields cannot shrink below about ×0.7–0.8 on the W2 surface resolution. Finer biology is NOT DEMONSTRATED, not invalid.

**Facial relief:**
- The maximum is not reached by ×3.0 under the integument guards alone.
- It is bounded by the ridge legibility clamp (§9):
  - cranial structural / temporal band ≤ ×1.18 at m 1.0;
  - occipital band ≤ ×1.94;
  - canthal / rostral band ≤ ×2.57.
- The §9 sheet shows ×3 facial relief reads armored and erases the plane breaks. The relief maxima above therefore apply only together with §9.

## 7. RM-UB-08 — body scale fields

| Field | Ref size / relief (cm) | Ref aspect / span | **Size valid (×)** | Size first invalid low / high | **Relief valid (×)** | Relief first invalid low / high |
|---|---|---|---|---|---|---|
| **Structural / protective** | | | | | | |
| upper posterior neck | 1.319 / 0.201 | 0.152 / 23.5° | 0.6–2.0 | 0.5 S2, S3 / 2.5 S5 | 0.5–1.25 | 0.4 S2 / 1.5 S4 |
| dorsal trunk | 0.791 / 0.194 | 0.245 / 16.6° | 0.9–2.5 | 0.8 S3 aspect / n.r. | 0.25–1.0 | n.r. / 1.25 S3 aspect |
| lateral trunk | 0.619 / 0.175 | 0.282 / 10.5° | 1.0–2.5 | 0.9 S3 / n.r. | 0.4–1.0 | 0.25 S2 / 1.25 S3 |
| dorsal tail | 0.709 / 0.206 | 0.290 / 17.7° | 1.0–2.5 | 0.9 S3 / n.r. | 0.4–1.0 | 0.25 S2 / 1.25 S3, S4 |
| forearm | 0.748 / 0.131 | 0.175 / 29.9° | 0.6–2.0 | 0.5 S3 / 2.5 S5 | 0.5–1.5 | 0.4 S2 / 1.75 S3 |
| shin | 1.152 / 0.154 | 0.133 / 47.3° | 0.5–1.2 | n.r. / 1.3 S4 | 0.4–1.0 | 0.25 S2 / 1.25 S4 |
| dorsal hand | 0.251 / 0.100 | 0.400 / 15.3° | 1.0–2.5 | 0.9 S3 / n.r. | 0.4–1.0 | 0.25 S2 / 1.25 S3 |
| dorsal foot | 0.299 / 0.050 | 0.168 / 12.1° | 0.7–2.5 | 0.6 S2 / n.r. | 0.6–1.75 | 0.5 S2 / 2.0 S3 |
| **Articulation / transition** | | | | | | |
| neck flexion | 0.351 / 0.084 | 0.239 / 14.3° | 0.8–2.0 | 0.7 S3 / 2.5 S1 | 0.25–1.25 | n.r. / 1.5 S3 |
| axilla | 0.315 / 0.060 | 0.191 / 23.1° | 0.7–1.3 | 0.6 S3 / 1.5 S1 | 0.25–1.5 | n.r. / 1.75 S3, S4 |
| elbow | 0.281 / 0.055 | 0.194 / 10.1° | 0.7–2.0 | 0.6 S3 / 2.5 S2 | 0.25–1.5 | n.r. / 1.75 S3 |
| wrist | 0.241 / 0.048 | 0.201 / 10.6° | 0.7–2.5 | 0.6 S3 / n.r. | 0.25–1.5 | n.r. / 1.75 S3 |
| lower-trunk flexion | 0.349 / 0.063 | 0.180 / 7.0° | 0.9–1.3 | 0.8 S4 / 1.5 S2 | 0.25–1.5 | n.r. / 1.75 S3 |
| hip crease | 0.310 / 0.054 | 0.173 / 5.1° | 0.6–1.5 | 0.5 S3, S7 / 1.75 S2 | 0.25–1.5 | n.r. / 1.75 S3 |
| knee | 0.306 / 0.055 | 0.181 / 9.7° | 0.6–2.5 | 0.5 S3 / n.r. | 0.25–1.5 | n.r. / 1.75 S3 |
| ankle | 0.281 / 0.055 | 0.196 / 6.5° | 0.7–2.5 | 0.6 S3 / n.r. | 0.25–1.5 | n.r. / 1.75 S3 |
| tail articulation | 0.380 / 0.064 | 0.169 / 8.8° | 0.6–1.5 | 0.5 S3 / 1.75 S2 | 0.25–1.75 | n.r. / 2.0 S3 |
| **Ventral** | | | | | | |
| throat / anterior neck | 0.660 / 0.065 | 0.098 / 17.0° | 0.5–2.5 | n.r. / n.r. | 0.25–2.0 | n.r. / 2.5 S4 |
| chest / abdomen | 0.899 / 0.070 | 0.078 / 12.4° | 0.5–2.5 | n.r. / n.r. | 0.25–3.0 | n.r. / n.r. |
| tail underside | 0.835 / 0.073 | 0.088 / 14.8° | 0.5–2.5 | n.r. / n.r. | 0.25–3.0 | n.r. / n.r. |
| **Contact** | | | | | | |
| palmar | 0.159 / 0.026 | 0.166 / 10.3° | 1.0–1.3 | 0.9 S7 (generator) / 1.5 S2 | 0.4–1.75 | 0.25 S3 / 2.0 S3 |
| plantar | 0.164 / 0.026 | 0.159 / 7.0° | 1.0–1.3 | 0.9 S7 (generator) / 1.5 S2 | 0.4–1.75 | 0.25 S3 / 2.0 S2, S3 |

Absolute cm values for every interval end are in tables.md. Finger / toe joints have no separate canonical field: they sit inside the dorsal hand / foot and contact fields. Reported as such.

**Findings**
- **One class-level envelope is NOT sufficient.** Inside the structural class, relief tolerance ranges from ×1.0 to ×1.75 at the top and ×0.25 to ×0.6 at the bottom.
  - The binding guard differs by field. The trunk, tail and hand already sit near the aspect ceiling (0.25–0.40), so they cannot take more relief or smaller units. The nape, forearm and foot have headroom.
  - Region-specific bounds are required.
- **Articulation fields share one relief envelope, ×0.25–1.5** (tail ×1.75), all aspect-limited. Their size limits differ:
  - axilla and lower-trunk flexion ×1.3, from span and folds;
  - hip and tail articulation ×1.5, from hierarchy;
  - elbow / neck ×2.0;
  - knee, ankle and wrist n.r. at ×2.5.
- **Size and relief fail at different points** in every class (§15): size by span, hierarchy or resolution; relief by aspect, floor, hierarchy or folds.
- **Upper ends no guard reached (n.r., ×2.5):** the metric guards are silent there, but on the renders the large units read plate-like. Example: dorsal trunk ×2.5 in `w3b_body_S_dorsal_trunk.jpg`. These ends are NOT DEMONSTRATED as valid biology. The proposed **promotable cap for any n.r. size end is ×1.5**, pending an author visual threshold.
- **Ventral fields:** no failure inside ×0.5–2.5 size or ×0.25–3.0 relief. At ×2.5 there are still ≥ 6 units across, so they never become continuous belly scutes. Their outer ends are NOT DEMONSTRATED. The proposed cap is the tested maximum, flagged.
- **Edge definition / overlap:** this is the aspect ceiling (S3), reported as the dependent boundary that binds the relief of the trunk, tail and hand (§15).

## 8. Body extremes (§17) — scale fields carried by the accepted bodies

**Bodies:**
- SA-M188 (= canonical); SA-F188 (§263 centre); SA-M168; SA-M208;
- Narrow; Broad;
- high muscle; high fat; Narrow + high fat;
- SA-M188-T80, a long / high-base tail: 80 % with base 1.22, above the RM-UB-04 Balanced anchor.

**Method:** each body is built with the canonical W2 route. The canonical relief is carried along its normals (the W2 convention).

**Per field, measured:**
- unit stretch, area normalized by stature²;
- span over the body's own bend;
- excess folds;
- edge strain.

**Results**
- **SA-F188, 168, 208:**
  - unit stretch 0.99–1.01;
  - span within its limit;
  - 0 excess folds except the 168 dorsal tail (15).
  - The §263 E/B deformation keeps field topology.
- **Narrow / Broad:** stretch 0.98–1.01. Isolated folds only: dorsal trunk 3 (Narrow), axilla 3 (Broad).
- **Composition extremes (high muscle, high fat, Narrow + high fat): the W2 carried-relief convention ALREADY folds at canonical relief.**
  - Lateral trunk 451–455; dorsal hand 447–449; tail 234–250;
  - lower-trunk flexion 103–108; tail articulation 85–87;
  - high-muscle axilla 436 and neck flexion 319.
  - Here the composition offset compresses the base itself (edge strain down to ×0.20–0.55), and relief carried along the new normals folds. This is a **pre-existing W2 extreme-body surface dependency**, not a scale-envelope result. It is reported, not fixed (§25).
- **Long tail T80:**
  - stretches the dorsal tail ×1.16, tail articulation ×1.20 and tail underside ×1.15;
  - edge strain up to ×2.08;
  - dorsal-trunk folds 12.
- **Relationship-aware relief clamps.** These are the largest tested relief multiplier with excess folds in tolerance (`extremes_clamp.json`; tested points 0.5 / 0.75 / 1.0 / envelope maximum):
  - high fat (incl. Narrow + high fat):
    - dorsal trunk ≤ ×0.5; dorsal tail ≤ ×0.5; shin ≤ ×0.75; nape ≤ ×1.0;
    - lateral trunk, dorsal hand, axilla, lower-trunk flexion and tail articulation fold even at ×0.5. Below ×0.5 these are NOT DEMONSTRATED; production surfacing dependency.
  - high muscle:
    - dorsal trunk and tail ≤ ×0.75; forearm / nape ≤ ×1.0;
    - neck flexion and axilla fold at ×0.5. Same production dependency.
  - Narrow: dorsal trunk ≤ ×0.75. Broad: axilla < ×0.5.
  - T80: dorsal trunk ≤ ×0.5; tail articulation ≤ ×1.0.
  - Tail underside / ventral ×1.0 on every body: this is the sparse sampling (1.0 then 3.0), not a measured clamp.
- **Unit size on the extremes** stays inside every size envelope: largest stretch ×1.20, tail articulation on T80. The size envelope needs a stretch clamp only for the tail on long tails: s × 1.2 ≤ the field maximum.

## 9. Ridge × scale interaction (§19) and relationship-aware clamps

Surfaced head. Per-field facial relief / size is set at each field's own valid end. Ridge m = the hidden strength. Legibility = ridge strength ÷ scale relief within 1 cm of the ridge; ≥ 1.0 is required.

| Corner | Ridge m | Facial relief / size | Min legibility (required families) | Face aspect | Eye visibility 0° | Verdict |
|---|---|---|---|---|---|---|
| reference | 1.0 | 1 / 1 | 1.18 (temporal) | 0.31 | 0.66 | VALID |
| min ridge × min relief | 0.4 | per-field min / 1 | **0.30** (temporal) | 0.13 | 0.71 | **FAIL**: identity carried by the platform only; the temporal line is gone |
| min ridge × max relief | 0.4 | per-field max / 1 | **0.04** (temporal); canthal 0.18 | 0.92 | 0.71 | **FAIL**: scales erase the plane breaks |
| max ridge × min relief | 1.3 | per-field min / 1 | 4.06 | 0.13 | 0.65 | VALID |
| max ridge × max relief | 1.3 | per-field max / 1 | **0.57** (temporal) | 0.92 | 0.64 | **FAIL**: armored, high relief dominates |
| reference ridge × facial size min | 1.0 | 1 / per-field min | 1.17 | 0.34 | 0.66 | VALID |
| reference ridge × facial size max | 1.0 | 1 / per-field max | 1.18 | 0.30 | 0.66 | VALID (10 fold faces: MARGINAL) |

Sheet: `sheets/w3b_ridge_scale_interaction.jpg`.

**The independently measured maxima are not jointly reachable.** Rather than shrink both ranges, the following **combined clamps** are proposed:
- **C-R1 legibility clamp.** For every ridge family F, scale relief within 1 cm of its core must satisfy r_local ≤ L_F(1) × S_F(m) ÷ S_F(1).
  - L_F(1) values: temporal 1.18, occipital 1.94, canthal 2.57, postorbital 3.51, jugal 8.31, mandibular 11.46, supraorbital 11.95.
  - At m = 1 this caps cranial-plate relief near the temporal line at ×1.18 and the occipital band at ×1.94.
  - At m = 1.3 the temporal cap rises to ×1.70. At m = 0.9 relief must stay ≤ ×1.0.
- **C-R2 ridge minimum with scales on:** m_temporal ≥ 0.90 × r_cranial and m_canthal ≥ 0.53 × r_rostral. The naked-skull minimum is 0.40.
- **C-O1 orbit outward clamp:** outward spacing is limited by platform containment.
  - cranial width ≥ 1.0: ≤ +14.9 % (strain-limited);
  - cranial width 0.92: ≤ +3.5 %;
  - in between: NOT DEMONSTRATED. Conservative rule: +3.5 % whenever cranial width < 1.0.
- **C-B1 extreme-body relief clamps:** §8 (composition, Narrow, long tail).
- **C-B2 aspect clamp:** relief ≤ 0.30 × unit size for every body structural / articulation field (except the canonical hand, 0.40). This ties relief to size: smaller units must lose relief.
- **C-T1 long-tail stretch:** tail-field size multiplier × the tail stretch (≤ 1.20 at T80) stays within the field maximum.

## 10. Seeds (§16)

Two diagnostic realizations were used (rng 1007, 2007). The canonical 130,949 is untouched.
- **Relief boundaries:** all 19 tested are stable across both realizations.
- **Size boundaries:** 13 of 19 are stable. Six outer size ends flip on one realization; the seed-robust end is the next tested step inward. These steps were not re-verified on the extra seeds:

| Boundary | Canonical-seed end | Seed-robust end |
|---|---|---|
| eyelid size max | 1.5 | 1.3 |
| auricular size max | 1.75 | 1.5 |
| cranial structural size max | 2.5 | 2.0 |
| shin size min | 0.5 | 0.6 |
| axilla size max | 1.3 | 1.2 |
| palmar size max | 1.3 | 1.2 |

- The 10 largest body fields were NOT RUN (session compute budget): dorsal / lateral trunk, dorsal tail, neck flexion, lower-trunk flexion, hip crease, tail articulation, chest / abdomen, tail underside, dorsal hand.
- The generator produced equivalent realizations with no change of field semantics.

## 11. FAIL / MARGINAL / NOT DEMONSTRATED / limits / NOT RUN

- **FAIL (by design, bracketing):** every first-invalid point in §2, §4 and §6–§7, and the §9 corners I1, I2 and I4.
- **MARGINAL:**
  - ridge m 0.40, the lowest valid naked-skull point (temporal strength 0.010 cm);
  - interaction I6, 10 fold faces;
  - orbit corner asymmetry 0.36–0.46 cm on the combined-out corner (ring noise).
- **NOT DEMONSTRATED:**
  - every "n.r." upper end in §6–§7 (ventral size / relief; several facial relief maxima at ×3.0; size ×2.5 on trunk, tail, hand, knee, ankle, wrist, foot);
  - single-family ridge maxima above 2.5;
  - fine-field size below the generator resolution;
  - orbit outward tolerance for cranial width between 0.92 and 1.0;
  - relief below ×0.5 on the folding composition extremes.
- **Measurement limits:**
  - IOD ring repeatability ±0.2 cm;
  - temporal-line strength includes part of the cranial-edge form;
  - the nasal pair cannot be read apart from the canthal ridges;
  - the orbit inward bound is construction-sensitive (strain in the interorbital roof);
  - the relief floor is the mouth-margin field itself, so the mouth margin and auricular recess cannot reduce relief.
- **Generator limits:**
  - the W2 surface resolution (S7) bounds the fine and contact size minima;
  - the carried-relief convention folds on composition extremes (§8);
  - isolated single-face base slivers flip numerically, so tolerance and sliver rules apply.
- **NOT RUN:**
  - vertical / AP orbit placement;
  - first-invalid points on the extra seeds;
  - extra seeds on the 10 largest body fields;
  - separate finger / toe joint fields (none exist);
  - per-family ridge visual sheets above 2.0;
  - SA-F188 head corners. Not required: the envelopes are species-level, and §263 shifts soft tissue only.

## 12. Cross-canon audit (§25)

| Reference | Result |
|---|---|
| SAURIN_V1 §36a, 42–45 (cranial identity, orbit / eye coupling) | Kept. Orbit size scales the orbit, lids, aperture and eye together (the rigid complex in the spacing warp). No independent eyeball. Forward axes. No gecko / lateral eye. Neutral expression (eye visibility unchanged). |
| §79–85, 94–99 (ridge-and-plane architecture, Regional Scale Architecture) | Kept. Ridges vary but never reach zero (L1). They are not horns, and display was never used. The hierarchy structural → articulation → fine, plus ventral / contact, is preserved by S2. There is no global scale-size slider: every test is per field. |
| §100–102 (display) | Untouched. Naked / minimal-display state only. |
| §259, 262, 263, 265 | §263: E/B deformation keeps field topology (SA-F188, 0 excess folds). Frames / composition are independent. The §8 composition folds are a pre-existing W2 carried-relief dependency, reported and not fixed. |
| UFCA_V1 / UCCA_V1 | No sex-specific bound and no frame or composition encoding. Relationship clamps are used instead of separate species envelopes (§21). |
| REFERENCE_ANATOMY_V1 | Measurement-only landmark proxy (orbital margin ring) documented. No new reference mesh. |
| W2I6 canonicalization / W2I4 seed realization | Canonical asset unchanged (hash check). The 130,949 seeds stay canonical; extra realizations are diagnostic only. |
| TS6 ridge architecture | Measured on the BROW_INT 5 skull. The diagnostic copy changes amplitudes only. |
| Creator register (A12 ≤ ±3 %, A32 ±20 % / ±25 %, fine ±10 %) | Used as history only. Measured: A12 −8.6 / +3.5 % on the safe interval, +14.9 % on wide crania. A32 structural size and relief are region-specific (§7). Fine-field size runs ×0.7–1.5, which is wider than ±10 % but generator-limited at the bottom. |

**Contradictions:** none with accepted canon. One **carried dependency** is surfaced, not fixed: the W2 carried-relief convention folds on composition extremes (§8).

## 13. Persistent files changed

- `reviews/claude-rac-w3b-saurin-orbit-ridge-scale-gate.md` (this gate)
- `reviews/rac-w3b-sa-evidence/`:
  - README, `tables.md`;
  - orbit, ridge, scale, extremes, interaction and seed JSON;
  - `canon_hash_check.json`;
  - `sheets/`
- `tools/rac/w1/w3b_drivers/`:
  - `w3b_head.py` (diagnostic skull copy), `w3b_common.py`;
  - orbit: `w3b_orbit*.py`; ridge: `w3b_ridge*.py`;
  - scale: `w3b_scale*.py`, `w3b_regions.py`;
  - body: `w3b_bodies.py`, `w3b_extremes.py`;
  - `w3b_interact.py`, `w3b_seeds.py`, `w3b_sheet.py`, `w3b_tables.py`, `AS_RUN.sh`
- `tools/rac/w1/cfg/w3b/SA-surface.json` (W3B diagnostic config)
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md` (status lines)
- **Not changed:** SAURIN_V1 (§22 firewall), the canonical W2 asset, the creator register.

## 14. Stop

W3B stops here. Nothing else was started: no RM-CF-09, RM-CF-05, RM-UF-05, RM-UF-01 / 02 closure, claw ranges, density model, posture, world-space tail review, roster review, creator, UE5, rigging, animation, equipment or gameplay work.

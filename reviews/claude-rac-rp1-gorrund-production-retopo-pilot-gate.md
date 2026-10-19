# RAC RP1 — Gorrund production retopology pilot — gate

Order: RP1 Gorrund manual production retopology (M-B, manual in the Blender UI; no QuadriFlow or auto-remesh as the topology generator).
Contract: `specs/RAC_PRODUCTION_MESH_CONTRACT.md`. Evidence: `reviews/rac-rp1-evidence/rp1d/` (earlier progress in `rp1b/`).

## 1. What was built

- **Source:** `GO-05AW4_nails_final.blend`, sha `5a4e45d4…22d5e`. Re-verified and never written.
- **Topology generator:** a manual quad cage of 1,810 vertices, built key by key in the Blender UI on Tyler's PC.
  - Trunk, limbs, head and ears, tail, both feet with toes, and both hands with fingers and thumbs.
  - Closed and genus 0.
- **Projection stack (UI-built, then applied):** Shrinkwrap Nearest, then 4 × [Subdivision level 1 → Shrinkwrap Project (±normal, limit 2 cm) → Shrinkwrap Nearest], all targeting the welded source.
- **Candidate:** `GO_U_REF_RP1_production_v001.blend` (sha `ce35992a…af335`), object `GO_U_REF_RP1_prod`.
- **Hashes:** `rp1d/hashes.txt`.
- **Tools:**
  - `tools/rac/rp/rp1_prod_export.py`: export.
  - `rp1_gate.py`: topology, T-1–T-5, T-7, nails.
  - `rp1_selfx.py`: self-intersection.
  - `rp1_landmarks_len.py`: T-6 with a tessellation-independent section centroid. The older `rp1_landmarks.py` edge-point mean is density-biased; both results are kept.

## 2. Results

| Check | Requirement | Result | |
|---|---|---|---|
| Components / boundary / non-manifold | 1 / 0 / 0 | 1 / 0 / 0 | pass |
| Genus | 0 | 0 (χ = 2) | pass |
| Face types | quad-dominant | 462,848 quads, 0 tris, 0 n-gons | pass |
| Normals | outward | consistent; signed volume matches the source sign (−190,276 vs −191,033 cm³ in the mirrored analysis frame) | pass |
| Degenerate faces | 0 | **175** | fail |
| **Self-intersection** (contract l.93) | 0; hand and axilla loops repaired | **193,086 face pairs**: hands 100,013, axilla/upper arm 61,688, head/jaw/ears 17,135, toes 10,418, crotch/pouch 3,266. The cage itself has 41. | **FAIL** |
| T-3 stature | ±1.0 mm | −0.59 mm | pass |
| T-3 bbox | ±2.0 mm | max \|Δ\| 0.58 mm | pass |
| T-1 body (general) | median ≤ 0.5 / p95 ≤ 1.5 / max ≤ 3.0 mm | source→prod 0.022 / 0.236 / **22.5**; prod→source 0.010 / 0.077 / **75.4** | **FAIL** (max) |
| T-2 head/muzzle/ears | 0.3 / 0.8 / 1.5 mm | source→prod 0.034 / **3.59** / **39.1**; 6.5 % of the source surface over the max | **FAIL** |
| T-2 hand L | same | 0.054 / **11.3** / **33.9**; 14.0 % over | **FAIL** |
| T-2 hand R | same | 0.071 / **19.5** / **37.5**; 18.5 % over | **FAIL** |
| T-2 foot L (toes, nails) | same | 0.051 / **3.47** / **19.6**; 7.5 % over | **FAIL** |
| T-2 foot R (toes, nails) | same | 0.062 / **1.26** / **16.3**; 4.6 % over | **FAIL** |
| T-2 tail root | same | 0.020 / 0.056 / 0.129 | pass |
| T-4 quad quality | target | 91.0 % of quads with all angles in 45–135°; 96.8 % with aspect ≤ 4 | target (not met everywhere) |
| T-5 density | target | mean edge 0.10–0.18 % of stature by zone (hands densest) | adequate |
| T-6 landmarks | ≤ 1.0 mm, none > 1.5 | wrists 0.01–0.03, knees 0.01, ankles 0.04–0.60, elbow R 0.19 — but **hip L 26.1, shoulder R 9.9, hip R 8.5, shoulder L 6.5, elbow L 3.5, tail_00 1.37, tail_12 1.29** | **FAIL** |
| T-7 silhouette IoU | ≥ 0.995 | front 0.99508 / profile 0.99742 / rear 0.99516 | pass (narrowly) |
| Nail projection | ±0.15 mm | L1 −0.04, L2 −0.03, R4 −0.11, R2 −0.15 pass; **L3 −0.18, R3 −0.21, R1 −0.91, L4 −1.09** | **FAIL** (4/8) |
| Visual veto | absolute | **VETO**: hands shredded, with spikes between fingers and thumb-to-thigh webs (`sheets/sheet_handR.jpg`, `sheet_handL.jpg`); visible artefacts at the neck, axillae, crotch and heel (`sheet_body.jpg`) | **FAIL** |
| Micro-detail exemptions | listed and shown | **none claimed**: every miss changes surface, projection or silhouette, so none qualifies under §15 | — |

Heat maps:
- `heat_body.png`: clipped at the 3 mm T-1 max.
- `heat_zones.png`: clipped at the 1.5 mm T-2 max.

IoU overlays: `iou_*.png`. Zone sheets (source above, production below): `sheets/`.

## 3. Why it fails

The open, convex body is in tolerance. Median deviation is about 0.02 mm and p95 is below 0.25 mm on the trunk and limbs, which shows the manual cage plus iterative projection can hold the sculpt.

Every failure is in a **contact or concave zone**: between fingers, thumb against palm and thigh, axillae, perineum and pouch, ear cups, under the jaw, and the toe clefts. In these zones a coarse cage surface lies between two source sheets, so projection pulls the same subdivided faces onto both sides. That folds them through each other, which explains both the self-intersection count and the large maxima.

Projection settings cannot fix this. The cage needs explicit edge loops that **separate** each contact pair before subdivision:
- a loop per finger cleft and per thumb web;
- an axilla loop pulled into the armpit, with the arm tube kept clear of the widened trunk (the cage's own 41 intersections);
- perineum and pouch loops;
- ear-cup interior loops;
- a jaw-line loop;
- toe-cleft loops.

The hip and shoulder landmark drift has the same root cause: the folded sheets in those sections.

## 4. Options for Tyler / ChatGPT

1. **Continue M-B with contact-zone cage work:** add the separating loops listed above to the v004 cage, then re-run the same stack and gate. This is the most UI work, mostly hands. The estimate is several long UI sessions.
2. **Hybrid:** keep this cage for the body and author the hands, and possibly the ears, as separate manual sub-cages joined at the wrist. This is still M-B, but each hand can be retopologised in isolation without the thigh contact.
3. **Relax the reference stance for contact zones,** for example by recording accepted contact topology per race under line 93. This is a contract decision, not mine.

Per the order I stopped here: no RP2, rigging, creator or UE5 work.

RP1 Gorrund production-mesh pilot — FAIL

# Saurin — Rodin Source Adoption Sheet (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-rodin-geometry-adoption-directive.md` (ChatGPT, 2026-10-02)
**Scope:** source selection and correction planning only.
- **No vertex of any Rodin component has been moved.** The sheets show exact extracted geometry; only rotation is applied.
- No sculpt correction, no spec change, no UE5 work.

**Images:** `reviews/images/rodin-source-adoption/`
**Scripts:** `tools/rodin/adopt/`
- `regions.py`: B1 canonical frame and region masks.
- `donor.py`: B2 and B5 extraction.
- `rmap.py`: renders.
- `compose.py`: sheets.

| # | Deliverable | File |
|---|---|---|
| — | Candidate comparison, B1–B5 | `ad_01_candidates.jpg` |
| 1–2 | Selected primary body, isolated, five views | `ad_02_B1_primary_5views.jpg` |
| 4 | Correction map (PRESERVE / MODIFY / REBUILD / REPLACE) with numbered regions | `ad_03_correction_map.jpg` |
| 3 | Hybrid donor, shown separately | `ad_04_B2_tail_donor.jpg` |
| — | Runner-up, for transparency | `ad_05_B5_runner_up.jpg` |

## 1. Recommendation: hybrid

| Role | Rodin component | Use |
|---|---|---|
| **Primary body** | **B1 = component `c12`** (front panel) | Whole body except the regions marked REBUILD/REPLACE below |
| **Tail donor** | **B2 = component `c11`** (profile panel) | **Only the free tail distal to F = −0.20H** (about 0.53H of centreline). B2's tail root, buttocks and laterally collapsed body are not used |
| Head | none (Rodin head not used) | The accepted **TS6.1 cranium** replaces the Rodin head |
| Fallback primary | B4 = `c10` | Only if B1 fails review |
| Reference only | part studies S9–S11 (hands), S12–S13 (lower leg) | Consulted if a B1 region needs repair. No geometry planned from them now |
| Not used | B3 = `c13` (two-sided "Janus" artifact), B5 = `c07` (runner-up) | — |

**Why B1 is the primary body**
- It is the most bilaterally symmetric body (symmetry residual 0.0049, against B4 0.0089, B5 0.0099 and B2 0.020).
- It is fully three-dimensional, because it comes from the front panel. The ventral surfaces, which carry most of the correction work, were generated facing the camera and are therefore the most reliable.
- It has the cleanest torso, limb and hand sculpt of the five.
- It is watertight: 75,254 triangles, 0 boundary edges, 0 non-manifold edges.

**B1's flaws**
- **It has no tail.** Its tail root is being rebuilt anyway (directive: "rebuild the root"), so the only cost is that the free tail must come from a donor.
- It has two thin-sheet generation artifacts on the legs:
  - a plate on the front of one knee;
  - a fin on the back of the opposite calf.
  - Both were found by a shape-diameter test (opposite surface within 0.012H) and are marked REBUILD.

**Why B2 supplies the tail**
- Its tail is the best of the three:
  - centreline about 0.67H from the buttock line to the tip;
  - **round section**: width/thickness 0.97–1.05 along the free tail;
  - smooth taper to a fine tip.
- B5's tail is a flattened blade (width/thickness rising to 1.7, sheet-thin near the tip).
- B3's tail is on a two-sided artifact.
- B2 and B1 are at the same Rodin scale (height 0.599 vs 0.598 units), so the donor needs no rescale.

**Why B2's body is rejected:** it is collapsed side to side. From the front it reads as one leg, and its back is a flat slab. This comes from being generated from the profile panel.

**Why B5 is not the primary body, despite being the only complete tailed body**
- Blade-flat tail.
- A vertical "strap" artifact on the throat.
- Wide, splayed stance with distorted calves and feet.
- Its front was synthesized from a rear-3/4 panel.

Choosing B5 would trade one tail transplant for more correction across the body.

## 2. Correction regions on B1 (numbers match `ad_03`)

| # | Region | Treatment | Reason / plan |
|---|---|---|---|
| 1 | Head | **REPLACE** | The TS6.1 cranium is authoritative; the Rodin head is longer (~0.25–0.28H) and different. Cut at the neck minimum (0.90H) and fit the TS6.1 head |
| 2 | Neck / cervical | **MODIFY** | Keep the mass and length. Re-surface the human SCM/trapezius pattern into dorsal-axial + ventrolateral throat structure. Rebuild the head junction into the thoracic inlet |
| 3 | Shoulder girdle / deltoids | **PRESERVE** | Good scapular/shoulder organization. Remove the small "bolt" knobs if present (minor clean-up) |
| 4 | Arms, forearms, hands | **PRESERVE** | Five digits, tapered, articulated; tendon structure at forearm and wrist. Claw continuation is checked at the surface stage |
| 5 | Thoracic shell, lateral/dorsal | **PRESERVE** | Thoracic volume and lateral planes are the asset (upper-thorax depth 0.198H) |
| 6 | Ventral thorax | **MODIFY** | Human pectoral plates → keep the volume, re-surface as non-human ventral/costal organization |
| 7 | Ventral abdomen | **MODIFY** | Remove the rectus six-pack ladder and **navel**. Translate into continuous longitudinal/oblique load paths at the same depth |
| 8 | Lower trunk flanks / dorsal | **PRESERVE** | Obliques and flank planes are useful. Lengthening is decided separately (see §5) |
| 9 | Dorsal midline strap | **MODIFY** | Keep the axial cue; reduce the raised cable to a restrained dorsal ridge that continues into the tail dorsum |
| 10 | Posterior pelvis, glutes, sacrum (tail root) | **REBUILD** | Remove both gluteal hemispheres and the cleft. Build the sacral/caudal platform and a substantial proximal tail base that carries the B2 donor tail. **Highest priority** |
| 11 | Crotch | **REBUILD** | Remove the male crotch/genital presentation. Neutral transitional anatomy; reproductive anatomy stays OPEN |
| 12 | Hip / anterolateral pelvis | **MODIFY** | Transition band: blend thigh roots into the rebuilt pelvic platform and remove the human iliac silhouette |
| 13 | Thighs, knees, crura | **PRESERVE** | Convincing limb mass, taper and lower-leg structure |
| 14 | Feet | **MODIFY** | B1 foot is 0.27H. Reduce toward 0.16–0.18H (investigative) by shortening rear- and midfoot. Preserve the plantigrade stance, metatarsal spread, long toes and claws. No paw pads |
| 15 | Leg sheet artifacts (knee plate; calf fin) | **REBUILD** | Generation artifacts. Delete locally and re-close from the surrounding knee and calf surface |
| T | Tail | **REPLACE** (absent on B1) | Graft the B2 free tail (green on `ad_04`) onto the rebuilt root (region 10). Smooth the transverse seam mid-tail on the B2 donor |

## 3. Tail length plan

- B2 donor segment: about 0.53H.
- Rebuilt root (sacral bend to the donor cut): about 0.14H.
- **Total: about 0.67H**, inside the 0.65–0.70H neutral target. No artificial extension is expected.

If the fitted root comes out shorter, the donor's mid-section will be extended along its own taper rather than adding a tube.

*Confidence: medium.* The centreline was measured by slicing the extracted mesh. The final value depends on the fitted root.

## 4. Phase A exclusion

**The rejected Phase A axial blockout contributes no body geometry to this route.**
- Nothing from `wf_saurin_phaseA.py`, its SDFs or its meshes is used.
- No TS7–TS9 body geometry is used either.

The only non-Rodin geometry planned is the accepted **TS6.1 head**, which the directive names as the cranial authority.

## 5. Proposed edit sequence (maximizes preservation)

Each step is reviewable, and none starts until this sheet is approved.

1. **Freeze the source.** Export B1, `c12`, in canonical frame at 188 cm as an untouched baseline; keep the region masks.
2. **Clean the artifacts.** Remove region 15 (knee plate, calf fin) and re-close locally.
3. **Pelvis / tail root (region 10, plus 11 and 12).**
   - Remove the glute and crotch geometry inside the masks only.
   - Build the sacral/caudal platform and proximal tail base.
   - Graft the B2 tail segment at its cut.
   - Blend the seams into the preserved thighs and flanks.
   - **Stop for review**: tail-root inevitability test, five views.
4. **Ventral torso (regions 6, 7) and dorsal strap (9).**
   - Re-surface while preserving thoracic and trunk volume.
   - Use displacement-style edits of the existing surface, not added volumes.
5. **Head and neck (regions 1, 2).**
   - Fit the TS6.1 head at the 0.90H cut.
   - Rework the cervical surface and the head–neck junction.
6. **Feet (region 14).** Proportion pass toward 0.16–0.18H while keeping the toes and claws.
7. **Proportion check.**
   - Lower-trunk length (B1 waist-to-crotch is 0.156H, close to Rodin's 0.16–0.17H guide).
   - Foot length, tail length, stance.
   - Document any conflict rather than forcing it.
8. **Surface integration (Phase C equivalent).** Planar transitions and claws, only after steps 3–7 pass review.

Preserved regions (3, 4, 5, 8, 13) are kept as-is apart from the blending margins at their borders.

— Claude

# Saurin Post-Rodin Phase A — Axial Blockout (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-post-rodin-master-anatomy-directive.md` (ChatGPT, 2026-10-02)
**Scope:** Phase A only, stopping at Gate A for ChatGPT/Tyler review.
- Not built: arms, hands, feet, muscles, claws, ridges or scales.
- No spec change, no UE5 work, no reproductive-anatomy decision.

**Images** are in `reviews/images/post-rodin-phase-a/`. **Source:**
- `tools/wf_saurin_phaseA.py`: the construction.
- `tools/phaseA_diag.py`: the sections and measurements.

**Mesh on Tyler's PC:**
- `RaceBodies/out/SaurinPhaseA_bare_3_5mm.blend` / `.fbx`
- `RaceBodies/out/saurin_phaseA_035.npz` (3.5 mm; the 1.5 mm review mesh used for the renders is regenerable with `python3 wf_saurin_phaseA.py 0.15`)

## 1. What was built, and how

**One continuous axial sweep.** A single smooth centreline runs from inside the skull base, down through the cervical column, thorax, lower axial trunk and pelvic platform. It then bends back through a **wide-radius sacral bend** into the caudal base and proximal tail.

**Cross-sections.** Sections along the line use planar construction:
- separate ventral and dorsal half-widths and extents;
- ventrolateral and dorsolateral chamfer planes.

**The frame turns with the axis.** So the **ventral body wall becomes the tail's ventral surface, and the dorsum becomes the tail's dorsum, by construction**. There is no point where a tail is attached.

**Femora.** Simplified segments, rooted in an acetabular/trochanteric mass under the lateral walls of the pelvic platform. A short crus stub is included for orientation only.

**Head proxy.** The accepted TS6.1 cranium, joined to the cervical column.

| Deliverable | File |
|---|---|
| 1. Blockout: front, profile, rear, front 3/4, rear 3/4 | `pa_01_blockout_5views.jpg` |
| 2. Continuity diagnostic: midsagittal section with the axial centreline coloured by region (cervical → thoracic shell → lower trunk → pelvis/sacral platform → caudal base/tail), hip joint and sagittal centroids | `pa_02_sections_continuity.jpg` (left) |
| 3. Sections: thorax U 140, lower trunk U 112, pelvis + femoral roots U 98, caudal base F −24 | `pa_02_sections_continuity.jpg` (right) |
| Scale reference beside Marchfolk 173 cm | `pa_03_marchfolk_scale.jpg` |
| 5. Raw measurements | `pa_measurements.json` |

## 4. Clean-sheet vs reused

**Clean-sheet** (new in this pass):
- The axial centreline.
- All cross-section definitions and their proportions.
- The sacral bend.
- The caudal base and proximal tail.
- The femoral roots and segments.

**Not reused:** no MPFB/human geometry, no Rodin geometry and no TS7–TS9 body geometry.

**Reused (tooling and accepted identity only):**
- The **TS6.1 head** signed-distance construction, unchanged.
- The meshing and render pipeline from TS7/TS8.
- The planar-section function concept from TS7.

## 5. Normalized measurements (H = 188 cm, head top; tail excluded)

| Target | Phase A | ÷ H | Directive guide / note |
|---|---|---|---|
| Standing height | 188.0 cm | 1.00 | canonical reference |
| Thoracic depth (max, U 124–152) | 34.5 cm | **0.184** | guide ~0.20 (Rodin). Kept at 0.18: at 0.20 the arm-less blockout reads pigeon-chested. Re-check in Phase B with the shoulder girdle |
| Thoracic width (U 140) | 29.5 cm | 0.157 | depth > width: a keeled, non-human shell (diamond section, see T) |
| Thoracic shell span (inlet U 152 → costal U 125) | 27 cm | 0.144 | construction value |
| Lower axial trunk (costal U 125 → pelvic platform U 100) | 25 cm | 0.133 | construction value |
| Lower trunk section (U 112) width × depth | 28.0 × 26.5 cm | 0.149 × 0.141 | rounded-octagonal; no waist pinch (narrowing comes from depth moving to the dorsum) |
| Narrowest trunk section → crotch (Rodin-comparable) | 112 → 89.6 cm | **0.119** | **conflict, documented, not forced:** Rodin 0.16–0.17. Our crotch is higher (0.477H vs Rodin 0.43–0.45H) because the hip sockets sit at 90 cm. See §7 |
| Pelvic width incl. femoral roots (U 98) | 36.0 cm | 0.191 | — |
| Hip-joint spacing | 19.2 cm | **0.102** | derived from the pelvic platform's lateral walls, not copied from Rodin (0.15H) |
| Caudal base (section at F −24) width × height | 28.0 × 20.5 cm | **0.149 × 0.109** | **materially stronger than TS8** (≈19 × 21 cm): base is nearly pelvis-wide |
| Caudal base section area ÷ pelvic axial section (U 98) | 405 / 1233 cm² | 0.33 | low-confidence ratio: the pelvis section already includes the start of the tail |
| Caudal base centroid height | 97.5 cm | 0.519 | **above (+7.5 cm) and behind (−23.4 cm) the hip joints**, not between hip lobes |
| Crotch (lowest solid at the midline) | 89.6 cm | 0.477 | — |
| Proximal tail built (sacral bend → Phase A cut) | 47.9 cm | 0.255 | the full tail planned for Phase B is about 0.68H (128 cm) along the centreline |
| Sagittal centroids (F, + forward) | head +1.7 · thorax +4.9 · lower trunk +0.3 · hip −0.6 · caudal base −24 cm | +0.009 · +0.026 · +0.002 · −0.003 · −0.128 | **measurable counterbalance:** thoracic mass sits forward of the hips and caudal mass well behind them, unlike the Rodin plumb line |

## 6. Self-audit against the Mandatory Rejection list

| Item | Status | Evidence |
|---|---|---|
| Human gluteal hemispheres | **Absent** | Pelvis section P is one convex mass that runs continuously into the caudal base |
| Conventional gluteal cleft | **Absent** | No midline groove in the rear or rear-3/4 views |
| Tail emerging between buttocks | **Absent** | Caudal base sits above and behind the hip joints; there are no hip lobes |
| Tail as a tube on a human sacrum | **Absent** | Single sweep: no insertion seam (midsagittal section) |
| Human pectoral plates | **Absent** | Thorax section is a keeled diamond; no pectoral masses |
| Six-pack / rectus ladder | **Absent** | No abdominal surface anatomy |
| Navel | **Absent** | — |
| Male crotch / genital bulge | **Absent** | Front view: clean gap between the thighs. The tail underside is raised above the crotch line for SAU-SILHOUETTE |
| Human iliac/hip silhouette as pelvic identity | **Watch** | Front view widens from the trunk (28 cm) to the femoral roots (36 cm). That comes from femoral sockets, not iliac flare, but the pear-like front outline needs checking once arms and shoulders exist (Phase B) |
| Bodybuilder V-taper | **Absent** | No arms or shoulders yet; nothing muscular |
| Mammalian paw pads | **N/A** (no feet in Phase A) | — |
| Giant Rodin feet | **N/A** (no feet in Phase A) | target ~0.16–0.18H in Phase B |
| Rodin head | **Absent** | TS6.1 cranium is used |
| Human neck cylinder with reptile head | **Partial** | In profile the cervical mass is a dorsal-heavy wedge from the occiput into the thorax, not a cylinder. From the front it is still a smooth column about as wide as the skull. Ventral/dorsal cervical differentiation is Phase C surface work |

## 7. Gate A self-assessment and documented conflicts

**Gate A — does the tail root look inevitable, with the pelvis organized around caudal continuation?**
- **Profile and rear 3/4: yes.**
  - The dorsal line runs from the lumbar dorsum through the sacral bend into the tail top without a break.
  - The ventral wall flows past the femoral roots into the tail underside.
  - The pelvis is visibly the start of the caudal mass, not a separate block.
- **Straight rear: mostly.** A soft rim is still visible where the caudal-base top meets the dorsum. It is a construction artifact of the sweep at the bend and can be faired in Phase B without changing the architecture.

**Conflicts documented rather than forced (directive: "stop and document"):**
1. **Lower axial trunk vs leg length.**
   - Using the Rodin-comparable measure, our lower trunk is 0.12H, against Rodin's 0.16–0.17H. The spec requires an *elongated* lower axial trunk, paid for "primarily through modestly reduced head/thoracic contribution rather than by forcing shortened legs".
   - Matching 0.16H would need either the thorax about 7 cm shorter, or hips/crotch about 7 cm lower (shorter legs). The spec prefers the first.
   - **Not done in Phase A pending review.** This is the main proportion question for ChatGPT/Tyler.
2. **Thoracic depth.** 0.18H instead of the 0.20H guide (reason in §5).
3. **Hip spacing.** 0.10H from the pelvic mechanics instead of Rodin's 0.15H. It may widen once full legs and stance width are tested at Gate B.

**Visible limitations (not claimed as passing):**
- The surface is deliberately simple and smooth: no muscle, tendon or planar detail yet.
- The femora are capsules.
- The neck front still reads as a column.

Phase A stops here. **Phase B is not started.** It needs ChatGPT/Tyler authorization.

— Claude

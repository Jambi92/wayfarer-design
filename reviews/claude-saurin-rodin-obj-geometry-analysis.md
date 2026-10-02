# Saurin Rodin OBJ — Geometry Analysis (DIAGNOSTIC / NOT CANONICAL)

**Author:** Claude
**Responds to:** `reviews/saurin-rodin-obj-geometry-handoff.md` (ChatGPT, 2026-10-02)
**Source:**
- Tyler's `Wayfarer_Saurin_Rodin_Reference.zip`, which contains a single `base.obj` (107 MB).
- The OBJ was exported from Blender 4.3.2 as one object.

**Status:** Analysis only.
- No TS10 or other reconstruction has been started.
- No spec text was changed. No UE5 work.
- The Rodin mesh is **not** canonical (authority: spec > decision register > prototype > Rodin).

Images and raw data are in `reviews/images/rodin-analysis/`. Analysis scripts are in `tools/rodin/`.

---

## 1. Component / cluster inventory

**Mesh totals (measured):**
- 500,036 vertices and 1,000,000 triangles.
- Bounds: X −0.943..0.948, Y 0..1.144, Z −0.214..0.206; Y is up.
- ChatGPT's figure of ~799k counted texture-coordinate rows; there are 500,036 position vertices.

**What the file is.** It is a **3D version of the reference poster, laid out panel by panel**. Each panel of the poster became a separate 3D object, placed where that panel sits on the sheet.

**22 connected components (`rodin_01_inventory.jpg`):**

| ID | Component | Content | Usable? |
|---|---|---|---|
| B1 | c12 | Full body, Front panel | Complete 3D body, **but has no tail** (rear view shows buttocks only) |
| B2 | c11 | Full body, Profile panel | Complete, tail present. Automatic landmarking fails: arms touch the torso |
| B3 | c13 | Full body, Rear panel | **Two-sided artifact**: dorsal anatomy on both sides, no face. Rear/tail reference only |
| B4 | c10 | Full body, Front 3/4 panel | Complete 3D body, **no tail** |
| B5 | c07 | Full body, Rear 3/4 panel | Complete, tail present. Wide splayed stance |
| S1 | c01 | Head–neck studies ×2 (front + profile, fused) | Panel crop, flat cut faces |
| S2 | c08 | Head–neck study (rear) | Panel crop |
| S3–S5 | c02, c04, c03 | Thorax studies (front / profile / rear) | Full 3D torsos. S5 is two-sided (back on both faces). S3 has a shoulder spike artifact |
| S6 | c00 | Pelvis/tail-root studies ×3 (rear, rear 3/4, profile; fused) | Panel crops |
| S7, S8 | c06, c05 | Upper leg (lateral, front 3/4) | Panel crops with cut faces |
| S9, S10 | c18, c16 | Arm (lateral, front) | Usable |
| S11 | c17 | Hand (palm) | Usable |
| S12, S13 | c15, c09 | Lower leg + foot (rear; lateral + front fused) | Usable |
| S14 | c14 | Foot sole | Usable |
| F1–F3 | c19–c21 | Loose oval pad fragments under the foot studies | Generation debris; reject |

**Panel orientation.** The bodies are fully 3D, but each was generated in its panel's orientation. B2 faces sideways and B5 faces away, which matters for measurement.

**Isolated renders:**
- `rodin_02_full_bodies_8_headings.jpg`: the five full bodies, orthographic, at 8 headings each.
- `rodin_03_part_studies.jpg`: every part study at 5 headings.

---

## 2. Measurement method and reliability

**Method:**
- Each body's surface was sampled (600k area-weighted points).
- Each body was oriented by fitting its **bilateral symmetry plane**, with the snout giving the forward direction.
- Horizontal sections every 0.4% of standing height were cut. In each section, the axial cross-section (trunk/neck) was separated from arm and leg sections.
- All values are **fractions of standing height H** (floor to top of head, tail excluded).
- For readability, cm values are shown at the Saurin reference H = 188 cm.

**Which bodies are measured:**
- B1 and B4 are the only bodies whose automatic landmarks are stable, and they agree with each other.
- B2 and B5 (tailed) were used for tail measurements only.
- B3 (two-sided) was used only for the rear tail path.

**Reliability.** Values marked ⚠ are visual estimates or low-confidence detections. Knee, ankle and arm segment boundaries could not be detected automatically. They are read from the measurement diagram (`rodin_04_measurement_diagram.jpg`), about ±0.02H. **No precision is claimed beyond what is shown.**

**Comparison with our builds.** The same section method was run on our TS8/TS9 meshes. On them, the tail lies close to the leg sections and confuses the crotch and pelvis detection. For those rows the **construction values** (known exactly) are used instead.

## 3. Measurement table

| Measure (÷ standing height) | Rodin B1 | Rodin B4 | Rodin (consensus) | ≈ cm at 188 | TS8 (ours) | Reliability |
|---|---|---|---|---|---|---|
| Jaw (lowest snout point) height | 0.911 | 0.931 | 0.91–0.93 | 171–175 | 0.92 (construction) | medium |
| Head height (jaw → crown) | 0.089 | 0.069 | **0.07–0.09** | 13–17 | ≈0.09 | medium |
| Head length incl. snout (max front–back depth at head level) | 0.276 | 0.25 | **~0.25–0.28** | 47–52 | 0.16 (TS6.1 head, about 29 cm) | medium |
| Neck minimum width / height of that point | 0.084 / 0.902 | 0.084 / 0.918 | 0.084 at ~0.91 | 16 cm | 0.066 at 0.95 | good |
| Visible ventral neck (jaw → inlet, about 0.86H) | — | — | ⚠ ~0.05–0.07 | 9–13 | ~0.08 | low |
| Axilla (armpit) height | 0.686 | 0.678 | **0.68** | 128 | 0.65 | good |
| Shoulder breadth incl. deltoids (just above axilla) | 0.331 | 0.343 | **0.33–0.34** | 62–64 | 0.32 (arms abducted) | good |
| Chest width just below axilla (axial only) | 0.162 | 0.156 | 0.16 | 30 | 0.156 | good |
| Upper-thorax depth (max, axilla → +0.12H) | 0.198 | 0.198 | **0.20** | 37 | 0.16 | good |
| Waist (minimum) height / width / depth | 0.602 / 0.168 / 0.132 | 0.594 / 0.162 / 0.126 | 0.60 / 0.165 / 0.13 | 113 / 31 / 24 | 0.55 / 0.15 / 0.20 | good |
| Thoracic vertical span (inlet ~0.86 → waist) | — | — | ⚠ ~0.26 | ~49 | ~0.30 | low (no costal landmark) |
| Lower axial trunk (waist → crotch) | 0.156 | 0.168 | **0.16–0.17** | 30–32 | 0.15–0.16 (construction 116→84 cm) | medium |
| Pelvic breadth (max, waist → crotch) | 0.240 | 0.240 | **0.24** | 45 | ~0.19 | good |
| Pelvic depth (tailless bodies) | 0.156 | 0.168 | 0.16 | 30 | — (tail merges) | medium |
| Crotch height | 0.446 | 0.426 | **0.43–0.45** | 81–84 | 0.447 (construction) | good |
| Hip-joint spacing (leg-section centroids 0.04H below the crotch) | 0.152 | 0.144 | **0.15** | 28 | 0.094 (construction) | good |
| Knee height | ⚠ 0.27–0.30 | ⚠ 0.27–0.30 | ⚠ ~0.28 | ~53 | 0.26 (construction) | low (auto-detector unreliable) |
| Thigh (crotch → knee) / shank + foot (knee → floor) | — | — | ⚠ ~0.16 / ~0.28 | 30 / 53 | 0.19 / 0.26 | low |
| Fingertip height (arms hanging) | — | — | ⚠ ~0.44 | ~83 | ~0.37 | low (visual) |
| Foot length (floor slab) | 0.270 | 0.245 | **0.25–0.27** | 46–51 | 0.153 | good |
| Foot width | 0.116 | 0.182 | 0.12–0.18 | 22–34 | 0.065 | medium (splayed toes) |
| Tail length (surface path, posterior pelvis → tip) | absent | absent | **B2 0.58, B5 0.47, B3 0.42** | 79–109 | 0.71 (134 cm path) | medium (surface path overestimates the centreline slightly) |
| Tail root height | — | — | **0.46–0.47** (at hip/buttock level) | 87–88 | 0.52 | good |
| Tail tip height / horizontal reach | — | — | 0.22–0.25 / 0.45–0.64 | 41–47 / 85–120 | ~0.31 / — | good |
| Tail base width × height (B5) | — | — | ⚠ 0.12–0.14 × 0.13–0.14 | 23–27 × 24–27 | 0.10 × 0.11 | low (oblique section) |
| Tail-base area ÷ pelvic section area | — | — | ⚠ ~0.4 | — | ~0.3 | low |

**Sagittal offsets** (forward + from the symmetry axis, ÷ H; B1 / B4):

| Point | B1 | B4 |
|---|---|---|
| Head centroid | +0.028 | +0.023 |
| Thorax | +0.008 | 0.000 |
| Pelvis | +0.019 | +0.019 |
| Hip joints | +0.024 | +0.027 |
| Ankles | +0.033 | 0.00 |

**Finding:** head, thorax, pelvis, hips and ankles are stacked on a near-vertical human plumb line. **There is no posterior caudal mass or counterbalance** in the bodies whose landmarks can be measured. Those bodies are tailless, and even the tailed bodies carry the tail as a hanging appendage behind the buttocks.

## 4. KEEP / MODIFY / REJECT / UNRESOLVED

| Feature (where seen) | Verdict | Reason |
|---|---|---|
| Five-digit hand, opposable thumb, long tapered fingers, claws continuing the digit axis, palm planes (S9–S11) | **KEEP** | Matches the spec's hand direction; good tendon/knuckle reference |
| Forearm and wrist tendon paths, brachioradialis/extensor/flexor grouping (S9, S10) | **KEEP** (definition reference) | Readable structure without needing a muscular build |
| Calcaneal tendon, crural mass tapering to the ankle, malleoli (S12, S13) | **KEEP** | Clear joint and tendon load paths |
| Dorsal midline ridge with segmented vertebral knobs (S5, B3, B5) | **KEEP / MODIFY** | Strong reptilian axial cue; tone the knobs down to restrained keratin |
| Tail taper (smooth, long, fine tip; rounded section with dorsal seam) (B2, B5) | **KEEP** taper / **MODIFY** length | Rodin tails are 0.42–0.58H; the spec says 0.55–0.80H |
| Neck: ventral paired cords and a broad dorsal mass running into the shoulders (S1, S2) | **MODIFY** | Useful structural differentiation; as built it reads as a human SCM and trapezius |
| Upper-thorax depth 0.20H and lateral rib/serratus field (S3, S4) | **MODIFY** | Depth agrees with a "deep mobile thorax"; the surface organization is human |
| Five toes with long digits and claws (S13, S14) | **MODIFY** | Good digit articulation, but a 0.25–0.27H foot (≈50 cm) is far beyond "longer forefoot than Marchfolk" and breaks footwear and plantigrade constraints. Target ≈0.16–0.18H |
| Hip-joint spacing 0.15H, thigh mass emerging close to the pelvis (B1, B4) | **UNRESOLVED** | Plausible femoral placement, but here it belongs to a human pelvis with gluteal masses |
| Lower axial trunk 0.16–0.17H | **UNRESOLVED** | Slightly longer than a typical human waist–crotch span, but delivered through a human abdominal cylinder and waist pinch |
| Long snouted head, about 0.26H long (S1, all bodies) | **REJECT** (for the body pass) | Conflicts with the accepted TS6.1 cranium (about 0.16H). The spec keeps the TS6.1 head |
| Human gluteal hemispheres with the tail emerging between them at buttock level (S6, B2, B3, B5) | **REJECT** | Directly fails the handoff criteria: "human buttock construction", "tail emerging as a tube glued onto the sacrum" |
| Human pectorals, six-pack rectus, **navel** (S3, B1, B4) | **REJECT** | Handoff criteria: "chest dominated by human pectoral anatomy", "human six-pack". A navel is a mammalian cue |
| Extreme V-taper (shoulders 0.33–0.34H vs chest 0.16H) and bodybuilder deltoids | **REJECT** as default | The spec says identity must not depend on muscularity; this belongs to composition variation, not species anatomy |
| Crotch bulge on every front-facing body | **REJECT** | Sex anatomy is inferred from human defaults; the spec says it remains OPEN |
| Paw-like sole pads (S14) | **REJECT** | TS8 directive: no mammalian paw pads |
| Pelvis 0.24H wide with human hip flare | **REJECT** | Human iliac/hip silhouette |
| Tailless bodies (B1, B4) | **REJECT** (generation artifact) | Tail is mandatory |
| Two-sided bodies (B3, S5) and the spike on the S3 shoulder | **REJECT** (generation artifact) | Not anatomy |
| Round "bolt" knobs on shoulders, hips and the sides of the tail root (S2, S5, S6, B3) | **REJECT** (generation artifact) | No anatomical basis |
| Loose pad fragments F1–F3 | **REJECT** | Debris |

## 5. Comparison to `specs/saurin/SAURIN_V1.md`

| Spec requirement | Rodin geometry | Verdict |
|---|---|---|
| Counterbalanced Pelvic-Axial Architecture: thorax → elongated lower trunk → integrated pelvis/sacral base → substantial counterbalancing tail | Human plumb-line stacking; no posterior caudal mass; tail hangs from the buttocks | **Does not meet** |
| Tail mandatory; never removed | 2 of 5 bodies tailless; 1 has no front | **Does not meet** (artifacts) |
| Tail ≈55–80% H, caudal base → tip along the centreline | 42–58% (surface path from the posterior pelvis) | **At or below the minimum** |
| SAU-BODY-04: tail biologically inevitable, not attached to a human-like body | Tail emerges between gluteal hemispheres | **Fails** |
| Deep mobile thorax, moderately deep rather than extremely broad | Depth good (0.20H); shoulders extremely broad (0.33–0.34H) through muscularity | **Partial** |
| Elongated lower axial trunk | 0.16–0.17H, delivered via a human waist and abdomen | **Partial / unresolved** |
| Head share near or modestly below Marchfolk; neck share near Marchfolk | Head height 0.07–0.09H (below); neck roughly human share | **Partial**; head proportions superseded by TS6.1 |
| Plantigrade, longer forefoot/toes than Marchfolk, footwear-compatible | Plantigrade, but a 0.25–0.27H foot | **Exceeds the valid range** |
| Five-digit hands, opposable thumb, restrained claws | Present | **Meets** |
| Identity not dependent on muscularity; no human sex defaults | Heavily muscular; human pectorals, abs and crotch bulge | **Does not meet** |

**Conflict to resolve before any rebuild.**
- On 2026-10-02 Tyler chose to "follow the reference literally" for TS9. That accepted human-style pectorals, six-pack, waist, glute-like masses, crotch form and sole pads.
- ChatGPT's later Rodin handoff lists exactly those features as **rejection criteria**.
- The two directions cannot both hold. **Tyler and ChatGPT need to settle this** before TS10 starts. This analysis applies the handoff's rejection criteria as ChatGPT requested; that is not a judgement against Tyler's choice.

## 6. Proposed reconstruction plan (for review — not started)

1. **Base.** Keep the TS7/TS8 clean-sheet signed-distance construction as the structural base, not the Rodin mesh and not TS9's muscle overlay. TS8 already has the non-human axial chain the spec asks for. Use Rodin as a **definition reference only**: the KEEP items above.
2. **Proportion targets.** Spec plus the measured Rodin evidence where it agrees:
   - **Thorax:** keep the upper-thorax depth at about 0.19–0.20H (Rodin, which agrees with "deep"). Chest width at the axilla stays about 0.16H.
   - **Shoulders:** breadth set by frame, not muscle; about 0.27–0.29H for the neutral reference instead of Rodin's 0.33H.
   - **Lower axial trunk:** at least 0.16H (waist → crotch), built from flank and ventral planes, not a waist pinch.
   - **Pelvis:** breadth about 0.19–0.21H. Posterior depth comes from the **sacral platform plus caudal base**, not glutes.
   - **Hips:** joint spacing about 0.12–0.15H (Rodin 0.15H is acceptable once the gluteal construction is removed).
   - **Tail:** 0.65–0.75H along the centreline (spec mid-range; Rodin is too short). Root at about 0.50–0.52H, emerging from the sacral platform **above and behind** the hip joints, not between hip lobes. Base about 0.11–0.13H.
   - **Foot:** about 0.16–0.18H, with Rodin's toe articulation and claw placement.
3. **Counterbalance.** Move the pelvis and caudal base posteriorly relative to the thorax by about 0.03–0.05H, so the profile shows the tail mass balancing the trunk instead of a human plumb line. This is the single biggest gap in the Rodin geometry.
4. **Definition pass (structural, not decorative)**, using the KEEP references:
   - forearm and wrist tendons, calcaneal tendon and malleoli;
   - knuckle and claw-bed construction;
   - restrained dorsal midline ridge with vertebral rhythm;
   - ventral cervical structure, re-expressed without a human SCM;
   - all at lean neutral composition.
5. **Validation before surface work.** TS8 torso-only test, SAU-SILHOUETTE, SAU-BODY-04 and normalized Marchfolk silhouettes, plus a **sagittal-offset check** (posterior caudal mass must be measurable) using the same section pipeline as this report.
6. **Prerequisite.** Tyler and ChatGPT resolve the TS9 vs handoff conflict (§5) and confirm the proportion targets in step 2.

— Claude

# RAC Stage C C4.1 — Grask constraint resolution (read-only diagnostics)

**Order:** `reviews/chatgpt-rac-stage-c-c4-1-grask-resolution-order.md` (fd23b89).
**Parent gate:** `reviews/claude-rac-stage-c-gate.md` (f9da37e).
**Evidence:** `reviews/rac-stagec-c4-1-evidence/`.
**Executor:** Claude. The work was cloud-side only and read-only.
- No mesh was edited, rebuilt with new settings or saved.
- Uniform normalizations of Durrim (to 218 cm) and Aelari (to 208 cm) were made in memory, for diagnostic views only.
- Gorrund was not reopened.
- No Blender session was opened on the PC.

**Sources.** Exactly the Stage C sources (`reviews/rac-stagec-evidence/checks/source_manifest.json`), re-hashed at entry:

| Source | Hash |
|---|---|
| Grask E3 | geometry `a452bf6e…`, file `d859eb18…` |
| Durrim `DU137C-NAT` | `6149d149…` |
| Aelari `AEL1` | `7bc1021a…` |
| Gorrund blend | `5a4e45d4…` (unchanged) |

## Summary

| Stage C Grask constraint | C4.1 finding | Recommendation |
|---|---|---|
| **GR-G1** (organized-surface FAIL) | On the accepted W1/W2 skeletal-proxy method over the protected unorganized route, **GR-G1 PASSES** at every t, for reference, Narrow and Broad. It reproduces the 05B values exactly. | Reclassify the Stage C organized-surface GR-G1 as **DIAGNOSTIC**, not a gate. **Constraint resolved.** |
| **Durrim depth row** (0.168 vs 0.160) | **ARCHITECTURALLY DISTINCT DESPITE DEPTH OVERLAP.** Grask and Durrim sit at least 6 places apart in the 11-body roster ranking on 16 of 21 readings. Thoracic depth share is the only close overlap. | Read the scalar row through the Durrim contrast rule, as a REPORT, not a gate. **Constraint resolved**; the canon wording is for the author. |
| **Front-view identity** | A context-free reader picks Grask out from the front alone as the one body built differently, mainly by organization (neck, girdle slope, limb and joint proportions). Confidence is **medium**, and the reader says it leans slightly toward "stretched human". | Record as moderate; carry as an art-direction note for the creator / retopology stage. **Not a gate.** |
| Absolute-cm organisation; Narrow at the joints; shading band | No contradicting evidence | **Carried forward** as creator / retopology implementation constraints (order §6) |

## 1. GR-G1, canonical measurement (`checks/gr_g1_canonical.json`; tool `tools/rac/w1/stagec_drivers/c41_gr_g1.py`)

### The existing rule

GR-G1 is defined in `w1e_checks` / `w2c_eval` and computed by `skeletal_proxy.py` (W1f/W1g/W1h).

- **Numerators.** Glenohumeral breadth comes from a sphere fit on the `-LEAN` shoulder cap. Biacromial breadth comes from the `-LEAN` acromion. Both are skeletal landmarks, and neither uses bideltoid breadth.
- **Denominator.** CIB thoracic breadth S2 b, read at the reference body's skin levels (W1h), inset by 2t.
- **t.** t ∈ {0, 0.5, 1.0} cm × H / 173.14.
- **Comparison.** Operator ≤ against MF-M-R. PASS / MARGINAL (< 1 %) / FAIL. The direction must hold at all three t.

This order adds no new definition or threshold.

### What changed on E3

The E3 skeleton (`-LEAN`, joints, bone scales) is identical to 05B/05C (05C and 05D guards: Δ 0.000 cm). The GH and biacromial landmarks are therefore unchanged (GH 36.456 cm).

The Stage C value differs because of where S2 is read. The skeletal proxy re-searches the thorax-maximum level on the **organized** skin. That re-lofted skin moves the S2 level, which lands on a narrower section of the same skeleton surface: S2 b 29.22 cm instead of 31.77 cm.

This is the same level-shift artifact recorded in 05C (gate §158) for Gorrund's pelvis ÷ thorax.

### Canonical read

The method is the W1/W2 one, run over the 05D protected unorganized route (`skeletal_stations.unorganized_state`). That route has every composition state on the same skeleton, without the race organization. The CIB uses W1h fixed levels from the unorganized reference skin.

Shoulder-joint ÷ thoracic breadth (≤ MF):

| Body | t 0 | t 0.5 | t 1.0 | Result |
|---|---|---|---|---|
| E3 ref | 1.1475 vs 1.2046 | 1.1949 vs 1.2493 | 1.2463 vs 1.2975 | **PASS** |
| E3 Narrow | 1.1478 | 1.1977 | 1.2522 | **PASS** |
| E3 Broad | 1.1491 | 1.1943 | 1.2431 | **PASS** |

Biacromial ÷ thoracic breadth (≤ MF):

| Body | t 0 | t 0.5 | t 1.0 | Result |
|---|---|---|---|---|
| E3 ref | 1.1605 vs 1.1786 | 1.1671 vs 1.1853 | 1.1743 vs 1.1924 | **PASS** |
| E3 Narrow | 1.1548 | 1.1616 | 1.1689 | **PASS** |
| E3 Broad | 1.1573 | 1.1635 | 1.1701 | **PASS** |

- **Comparator:** MF-M-R. The values are the committed Stage C G-row comparators.
- **Margins:** 1.5–4.3 %.
- **Reproduction:** these readings equal the committed **05B** GR-G1 values to four decimals for all three bodies (`reviews/rac-rmot05b-evidence/validators/w2c.json`: 1.1475 / 1.1949 / 1.2463; 1.1605 / 1.1671 / 1.1743; and so on). That confirms the route is the accepted one.
- **Control:** the same tool, run on the organized grid, reproduces the Stage C FAIL values exactly (1.2478 / 1.3040 / 1.3655).

### Disclosure: the 05D skeleton-anchored station level

05D's station method takes S2 from the skeleton surface at its own level, slab 9 instead of the skin's slab 7. Read there, S2 b is 29.70 cm and GR-G1 would read 1.228 / 1.282 / 1.341 (FAIL).

That comparison is not like-for-like:
- MF-M-R's comparator values were read at MF's skin levels.
- MF has no reading at a skeleton-surface level.
- 05D introduced that level method for the pelvic relations (GR-P2b / GR-P6), not for GR-G1.

The order asks for "the same protected skeletal landmark method used by the accepted W1/W2 Grask route". That is the W1h skin-level CIB above. Both readings are kept in the evidence.

### Answer

The canonical GR-G1 **PASSES** (reference, Narrow, Broad). The Stage C organized-surface GR-G1 should be classified **DIAGNOSTIC, not a gate**.

## 2. Durrim-depth rule (`checks/grask_vs_durrim_architecture.json`; sheets `sheets/grask_vs_durrim_native.jpg`, `sheets/grask_vs_durrim_norm218.jpg`)

The readings are existing ones only: the W1k / W2C directional skin set from the Stage C E3 run. The roster is the 11 reference bodies; the retired procedural Gorrund is excluded under D1(a). Rank 1 = highest in the roster.

| Reading | Grask E3 | Durrim | Grask rank | Durrim rank |
|---|---|---|---|---|
| Thoracic depth / stature | 0.168 | 0.160 | 1 | 2 ← **the only close overlap** |
| Thoracic breadth / stature | 0.178 | 0.222 | 10 | 1 |
| Thoracic depth ÷ breadth | **0.947** (keel) | 0.723 | 1 | 2 |
| Torso / stature | 0.266 | 0.297 | 11 | 1 |
| Leg / stature | 0.563 | 0.517 | 1 | 11 |
| Arm / stature | 0.444 | 0.398 | 1 | 11 |
| Span / stature | 1.078 | 1.034 | 1 | 7 |
| Shoulder-joint breadth / stature | 0.190 | 0.239 | 11 | 1 |
| Iliac crest / stature | 0.153 | 0.187 | 10 | 2 |
| Bitrochanteric / stature | 0.172 | 0.222 | 11 | 2 |
| Pelvic depth ÷ thoracic depth | 0.623 | 0.847 | 11 | 10 |
| Head height / stature | 0.124 | 0.142 | 11 | 2 |
| Forearm ÷ arm | 0.385 | 0.347 | 1 | 11 |
| Shin / stature | 0.287 | 0.245 | 3 | 11 |
| Wrist ÷ forearm | 0.205 | 0.299 | 7 | 1 |
| Knee ÷ femur | 0.251 | 0.343 | 11 | 3 |
| Elbow ÷ humerus | 0.339 | 0.421 | 9 | 2 |
| Ankle ÷ shin | 0.331 | 0.382 | 10 | 2 |

Further readings are in the json, 21 in total.

**Durrim** is the roster's broad, long-torsoed, short-limbed, heavy-jointed body: compact structural power.

**Grask** is the roster's longest-limbed, shortest-torsoed, narrowest-girdled and slimmest-jointed body: rangy structural elongation.

Grask's depth comes from a narrow keel section (depth ÷ breadth 0.95; Durrim 0.72), not from a broad, deep barrel. In absolute terms the chests are very different: 36.6 cm deep for Grask vs 21.9 cm for Durrim, at 218 vs 137 cm stature.

**Silhouettes** (`checks/sil_c41.json`). These use Durrim normalized to 218 cm and are diagnostic only.
- Front IoU is 0.653, the lowest of any Grask pair measured. It rises only to 0.849 after the best width stretch.
- Profile IoU is 0.804.
- In the sheets the Durrim reads as a broad, flat-fronted block trunk with a short neck, heavy limbs and a long torso. Grask reads as a narrow trunk with a keel chest, a dorsal mass, long thin limbs and a high pelvis.

**Classification: ARCHITECTURALLY DISTINCT DESPITE DEPTH OVERLAP.** The scalar row "thoracic depth never approaching Durrim proportional depth" is the only reading that converges. The later Durrim contrast rule (design principles, proportional organization, silhouette) is clearly met.

**Recommendation.** Treat the scalar row as **REPORT, superseded by the Durrim contrast rule for E3**. This changes neither race. Whether to amend the v1 spec wording is an author canon decision.

## 3. Front-only Grask identity (`blind/front_only.jpg`, `blind/front_only_read.md`)

**Set-up.** Front view (F) only, from the Stage C renderer, at about matched height. The bodies were letter-coded in this order:

| Letter | Body |
|---|---|
| W | Marchfolk MFM203 |
| X | **Grask E3 208** |
| Y | Aelari AEL1, normalized to 208 cm in memory (diagnostic) |
| Z | Skarn SK208-C1R |

The independent reader had no context and was not told which body was Grask. The raw prompt and answer are in `blind/front_only_read.md`.

**Raw answer, in short:**
- *1. Distinguishable from the front?* "Partly." W, Y and Z were judged one species in three builds. "**X is the only one that reads as built differently**, but the front-view cues for it are moderate rather than striking."
- *2. Cues for X:* sloped shoulders from a longer, thinner neck; a narrow, straight-sided, waistless torso; a boxy pelvis; longer, thinner arms with knobby elbows and hands hanging to the lower third of the thigh; long, narrow shins with prominent knees.
- *3. Basis of the difference:* X vs the others is "**mainly (c), how the body is put together** … some (b) as well, since X is also thin". W vs Y vs Z is (b), plus some (a).
- *4. Stretched human or caricature?* "X slightly leans toward a stretched human" (elongation and thinning), but "the sloped shoulders, boxy pelvis and joint knobs do add real structure beyond that". There is no outright caricature.
- *5. Least human:* X, at **medium** confidence. "A side view would be needed to confirm it."

**Silhouette overlap** (REPORT-only; `checks/sil_c41.json`). Values are front IoU, raw → after the best width stretch.

| Pair | Front IoU |
|---|---|
| Grask E3 208 ↔ Skarn | 0.742 → 0.842 |
| Grask E3 208 ↔ Marchfolk | 0.854 → 0.855 |
| Grask E3 208 ↔ Aelari (normalized) | **0.879** → 0.881 |
| Baselines: Skarn ↔ Marchfolk | 0.774 → 0.892 |
| Baselines: Aelari ↔ Marchfolk | 0.935 |

From the front, the Grask outline is closest to the slender Aelari. The separation the reader found is inside the outline, in proportions and joints, rather than in the outline itself.

**Interpretation.** Grask E3 can be picked out structurally from the front alone, and it is the body read as least human. The read is **moderate, not strong** (medium confidence). It rests on proportions (neck, girdle slope, arm and shin length, joints) plus thinness, and it borders on "stretched human". The Stage C multi-view identity (keel chest, dorsal mass) is what makes Grask robust; the front view alone is adequate but secondary.

**Disclosed confound.** X shows the known flat shading band. The reader was told to treat flat shading as rendering, and did so, except that it read "the blocky edge at the hip" as real shape.

**Recommendation.** Do not gate on this. Record "front-view identity moderate" as an art-direction note for the creator / retopology stage: front cues such as girdle slope and joint presence should survive retopology and shading. No geometry change is recommended at Stage C.

## 4. Carried creator / implementation constraints (order §6)

There is no contradicting evidence, so all three are carried forward:

1. **Relationship-aware scaling.** The E3 organisation (9 cm scapular mass, 3.5 cm keel, 4 cm flank) is absolute in centimetres. The creator must scale it relationship-aware across stature.
2. **Narrow frame at the joints.** Narrow-frame joint breadth must be carried by the skeleton / frame system, not hidden by the tendon-cord surface.
3. **Chest / abdomen shading band.** This is a surface / normal / retopology issue, not a morphology change. It is visible as a flat band in every front render.

## 5. Recommended statuses (not self-promoted)

**Grask E3 Stage C — recommend ACCEPT**, with carried implementation constraints.
- The two measurement / canon constraints resolve on existing methods: GR-G1 PASS canonically, and Durrim ARCHITECTURALLY DISTINCT.
- Front identity is moderate but present.
- The three §4 items and the front-view note are carried as creator / retopology implementation constraints, not as Stage C gates.
- If the author prefers to keep "CONSTRAIN" until the Durrim-row wording is formally amended, the evidence supports that equally.

**Gorrund Stage C — ACCEPT** (reference state only; unchanged).

**Combined Stage C — recommend ACCEPT.**
- The Grask ↔ Gorrund separation is the strongest in the roster.
- Neither race collapses into Skarn / Marchfolk.
- The deferred Gorrund creator guarantees and the Grask implementation constraints carry forward.

Author decisions requested:
1. Confirm GR-G1 is read on the W1/W2 skeletal-proxy route (organized-surface reading = diagnostic).
2. Confirm the Durrim scalar row is superseded by the Durrim contrast rule for E3, or amend the v1 wording.
3. Rule on the statuses above.

STOP for the ChatGPT / Tyler author ruling.

**Not started:** Grask edit or sculpt, canon change, Stage C promotion, D4, UE5, rigging, creator implementation.

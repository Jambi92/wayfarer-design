# RM-OT-05O §2: evidence and causal-claim audit of the 05N delivery

Everything here was measured on the DELIVERED meshes (`reviews/rac-rmot05n-evidence/RD2/GO-RD2-REF.obj`, `LOW/GO-RD2-LOW.obj`). None of it used the working fields.

- **Code:** `tools/rac/w1/rmot05o_drivers/o_sections.py`, `o_preserve.py`, `o_legaxes.py`, `o_crotch.py`.
- **Outputs:** `RD2_REF_LOW_sections.json`, `RD2_REF_LOW_section_overlays.png`, `RD2_REF_LOW_preservation.json`, `../stance/RD2_leg_axes.json` / `.png`.
- **Axes:** cm, Z up (ground z = 0), +Y anterior, X lateral (+X body left), bilateral symmetry about X = 0.
- **Sections:** exact winding-number inside test on a 0.25 cm grid.

## A1. The 05N "REF breadth 57.5 cm at four trunk stations" was a measurement defect

The 05N audit (`audit.py`) masked every trunk slice to |X| < 29 cm. Any trunk section wider than the mask was clipped to 57.5 cm, so the four identical REF values are the mask edge, not anatomy.

LOW's waist read 48.5 cm because at that station LOW was narrower than the mask. That made a mask artifact look like a 9 cm "shape change". The 05N trunk breadth rows are therefore void. The 05N limb rows (no X mask on legs and arms) and the volumes are not affected.

## A2. Corrected trunk measurement (arm-independent)

**Method**
- Where a hanging arm is separate in the slice, the trunk is the midline component.
- Where the arm touches the trunk, the slice is split by a marker watershed. The trunk marker is at the midline; the arm markers are at the arm centroids of the nearest slice where both arms are separate.
- The method is reported per station.
- A second, arm-independent measure is added for every trunk station: the **midline AP depth**, the anterior-to-posterior extent of the |X| ≤ 2 cm strip.

**RD2 REF → LOW** (breadth / depth / area / midline AP depth):

| Station | z | Method | REF | LOW | Δ breadth | Δ area |
|---|---|---|---|---|---|---|
| thorax_axilla | 170 | watershed (arm contact) | 72.5 / 42.0 / 2267 / 40.8 | 70.8 / 40.2 / 2153 / 39.2 | −1.8 | −114 (−5.0 %) |
| thorax | 162 | watershed (arm contact) | 74.5 / 43.0 / 2130 / 39.8 | 74.5 / 43.0 / 2069 / 39.8 | 0.0 | −61 (−2.9 %) |
| lower_thorax | 155 | watershed (arm contact) | 49.2 / 40.8 / 1544 / 39.2 | 57.8 / 40.8 / 1552 / 39.2 | **+8.5 (segmentation artifact)** | +8 (+0.5 %) |
| lower_trunk | 146 | component (arms free) | 44.0 / 39.0 / 1411 / 38.0 | 44.0 / 39.0 / 1411 / 37.8 | 0.0 | 0 (0.0 %) |
| waist | 138 | REF watershed (elbow contact) / LOW component | 54.2 / 38.5 / 1642 / 37.8 | 48.0 / 38.0 / 1518 / 37.2 | −6.2 | −123 (−7.5 %) |
| upper_pelvis | 125 | component | 56.8 / 39.5 / 1794 / 39.5 | 55.8 / 38.2 / 1721 / 38.2 | −1.0 | −73 (−4.1 %) |
| pelvis | 115 | component | 58.5 / 36.0 / 1791 / 35.5 | 58.5 / 36.0 / 1786 / 35.2 | 0.0 | −5 (−0.3 %) |

**Reading the table**
- **155–170 cm:** the upper arm lies against the chest, so trunk breadth there is not uniquely defined from the surface. The watershed splits REF and LOW differently; the +8.5 cm "difference" at 155 is a segmentation artifact. At these stations only the midline AP depth is reliable: no change at 155 and 162, −1.6 cm at 170 (pectoral reduction).
- **138 cm:** REF's elbow touches the trunk, LOW's does not. About 6 cm of the −6.2 cm is the designed flank reduction (flank ellipsoid, design 2.9 cm per side). The rest is the contact boundary.
- **146 cm:** the cleanest axial station (arms free in both bodies). REF = LOW.

## A3. Preservation: edit design vs independent measurement

`RD2_REF_LOW_preservation.json` keeps the two separate:
- **Design:** the largest tissue offset the LOW recipe applies inside each protected region.
- **Measured:** the signed distance of LOW vertices to the REF surface, inside that region.

| Protected region | Design reach (cm) | Measured \|d\| median / p95 / max (cm) |
|---|---|---|
| Knee | 0.00 | 0.004 / 0.012 / 0.046 |
| Ankle | 0.00 | 0.001 / 0.003 / 0.007 |
| Wrist | 0.00 | 0.006 / 0.02 / 0.044 |
| Acromion / clavicle | 0.00 | 0.011 / 0.014 / 0.023 |
| Elbow | **0.34** | 0.018 / 0.123 / 0.196 |
| Sacral platform | **0.76** | 0.067 / 0.246 / 0.351 |
| Iliac crest / ASIS | **1.07** | 0.184 / **0.674** / 0.781 |

**Correction to 05N.** The LOW recipe did not fully protect the iliac crest / ASIS or the sacral platform: the flank and gluteal ellipsoids reach into them. The surfaces there moved up to 0.8 cm. Knee, ankle, wrist and acromion are preserved by measurement (≤ 0.05 cm).

**Surface landmark proxies (not skeletal)**

| Landmark | REF | LOW | Δ |
|---|---|---|---|
| Stature (max z, includes ear / mane tips) | 236.93 | 236.96 | +0.03 |
| Crotch | 99.31 | 99.30 | −0.01 |
| Fingertip | 94.00 | 94.01 | +0.01 |
| Acromion proxy | 188.28 | 188.29 | +0.01 |

These are surface proxies. Skeletal correspondence does not exist for these remeshed bodies, and none is claimed.

## A4. Stance claim correction

The 05N gate described "about a 20° hip–knee–ankle zig-zag" with "knees forward" (a section-centroid estimate). That was wrong.

**Corrected landmarks** (`../stance/RD2_leg_axes.json`): segment axes through AP / ML section mid-points; thigh fitted over z 66–92, shank over z 20–46; declared joint heights hip 106, knee 57, ankle 11. Measured inclinations from vertical:

| Measure | Value |
|---|---|
| Thigh | −16.9° |
| Shank | −14.5° |
| Knee (thigh and shank nearly collinear) | 2.4° sagittal, 7.6° 3-D |
| Knee position | 1.1 cm *behind* the hip–ankle line |
| Ankle | 26.8 cm posterior of the hip |
| Ankle dorsiflexion holding the foot flat | about 16° |

So the legs did not flex at the knee. **The whole leg sloped backward from the hip** under a vertical trunk (trunk mid-depth moves only about 3 cm from 115 to 170 cm).

## A5. Source vs edit attribution (05N said "the read comes from the source")

That statement is withdrawn. The backward leg inclination and the short leg-to-trunk relation are inherited from the F1 pose and proportions; the hip rotation and shaft edits in 05O isolate them.

RD2 also contains my own edits that plausibly contribute to a "blocky / waistless" read:
- the lower-trunk thickening (+4 cm lateral at 140);
- the pelvis zone rebuilt by a large-radius opening and z-relaxation (a smoothed, convex hip mass);
- the 1.8 cm arm–trunk clearance, which leaves "armpit windows".

05O does not reverse those, because the order bounds RD3 to stance, transitions and one proportion edit. Their contribution therefore stays **unmeasured**. See the gate report.

## A6. Blind-sheet inspection (05N sets K / L)

- **Keys:** `GO-S-ref` / `GO-S-low` point to the GO-RD2 r6 bodies. Controls map to the frozen MF / SK / Grask E3 bodies.
- **Matched display stature:** each tile is height-normalized to the visible body. Gorrund is cut at its neck root (191); the controls at theirs.
- **Orientation:** front tiles show the anterior of every body; in profile, all bodies face image-left. Consistent.
- **Clipping:** none.

The 05N reason audit counted monster words in drivers / cues (REF 0, LOW 1) **separately** from group labels (6/6). Both counts were reported. The gate text's "every group labelled ogre / troll / brute / orc" referred to the labels, which is correct.

Old scores are untouched.

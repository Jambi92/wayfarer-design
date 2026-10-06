# RAC W1d — Non-Human Ear-Family Packet and Reference Geometry (B-2)

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §6 (work order item 4)
**Status:** PACKET + **SCHEMATIC** REFERENCE GEOMETRY FOR AUTHOR ACCEPTANCE. Every shape and magnitude is **BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED**. Nothing is attached to a reference body yet: constrained ARMs are rebuilt only after acceptance (order §11 item 8).

**Assets** (`reviews/rac-w1d-evidence/ears/`):
- one OBJ per family (cm; auricle in the y–z plane before attachment, lateral = +x, skull plane x = 0);
- `ear_families.json` (parameters and landmarks);
- `ear_families_sheet.jpg` (lateral / posterior / from-above hillshade views, 1 cm ticks).

**Tool:** `tools/rac/w1/ear_families.py`. Canon extraction: verbatim quotes with lines, prepared for this packet (summarized in §1).

## 1. Canon that governs the families (summary; quotes in the W1d canon extraction)

| Family (UFCA §10.2) | Mandatory architecture | Directions | Prohibited | OPEN |
|---|---|---|---|---|
| Human auricle (MF reference) | Root, helix, antihelix, concha, tragus/antitragus, lobe | — | Elven taper; ears as a point on a pointiness axis | All magnitudes |
| **Elven continuous taper** (FN, AE, VA) | Non-human ear: skull attachment, base, cartilage, upper-ear form, **taper emerging from the whole ear**, tip, projection, curvature, lobe (ECR L104; FN L183 analogous helix/antihelix/concha/tragus/lobe) | **FN:** greatest average lateral projection, outward/rearward sweep; no length/base/taper tendency. **AE:** more upward and backward orientation, lower projection than FN, moderate-to-long length, clean gradual taper, taper longer than VA. **VA:** somewhat broader base, stronger skull-root integration, more lateral and backward orientation, taper moderately shorter than AE | "Human ears with stretched tips"; pointiness continuum; one identical ear for all three; rigid one-type-per-race | Exact shape, all magnitudes, mobility |
| **Mixed coupled human + elven** (HV) | Union of the human foundation (root, helix, antihelix, concha, tragus, antitragus, lobe) and the elven variables, coherently coupled | Inherits FN/AE/VA tendencies by ancestry; "ear length isn't a genealogy meter" (HV L206) | Midpoint ear; pointiness slider | The envelope itself (depends on FN/AE/VA acceptance) |
| **Folded late-taper** (GR) | Visibly folded cartilage through much of the auricle; **sustained upper-ear body**; **late terminal taper**; recognizable lobe; humanoid root (GR L449–457, L471, GR-EAR-01…04; bans at GR L398) | Length read relative to head height, moderate → strong (AD-R43; longest = GR-EAR-02 class) | "Large Fenn ears on a troll head"; needle/knife points; perfect triangles; uniformly thick; horn-like; one continuous blade | Length range; taper-start position ("a conceptual distinction, not a geometric formula"); fold depth |
| **Deep-bowl broad-rim** (GO) | Broad auricle; **deep bowl**; strong antihelical fold system; **broad, continuous, non-tapering rim**; rounded to mildly angular upper termination; strong broad attachment; lobular region (GO L455–475; variables GO L354) | Projection from skull **close-set** tendency; outward extent **short-to-moderate** relative to elven and Grask long ears; the two variables kept separate (AD-R43) | Strong terminal point; elven or Grask taper; enlarged human ear; flat circular "ogre ears"; uniformly thick | Both ranges; bowl depth; breadth |

## 2. How the geometry is built (not a pointiness continuum)

Each family is its **own outline law plus relief system**, never an interpolation of the human ear (`ear_families.py`). The common grid is an auricle surface along a swept long axis, with an anterior (root) edge and a posterior (helix) edge, a cartilage thickness, and a fleshy lobe.

| Family | Outline law | Relief system |
|---|---|---|
| Human | Rounded termination (elliptic top from 55 % of length) | Rolled helix with scapha groove, antihelix ridge, concha, tragus, lobe |
| Elven (FN, AE, VA) | **Continuous taper**: width follows cos^p from a base region to the tip, so the taper is distributed along the ear and the point emerges from the whole ear. It is not a human outline with a tip added | Helix runs to the tip; antihelix fades into the upper ear |
| HV | Human-proportioned lower ear (late, short continuous taper from 48 % of length) | Human foundation relief, elven upper-ear variables. **One example point** of the general envelope, not its centre |
| GR | **Sustained body to 72 % of length, then a late terminal taper** (cos^1.6) | Three-ridge folded-cartilage system, thicker cartilage, lobe |
| GO | **Broad rounded termination** (from 50 %) with **broad non-tapering rim** | Deep bowl (1.35 cm), strong antihelical fold, attachment angle 0° (close-set) |

## 3. Parameters (all BUILDER-CHOSEN) and RA §11 landmark readings

| Family | Length L | Base half-width | Taper law (start, exp.) | Bowl depth | Rim (h, w) | Folds | Projection angle | Tilt back | Auricle height | Tip-from-root | **Auricle projection** | Max breadth |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MF-human | 6.4 | 1.75 | rounded (0.55) | 0.75 | 0.28, 0.32 | — | 22° | 12° | 6.25 | 4.38 | 1.98 | 2.99 |
| FN-elven | 8.6 | 1.80 | continuous (0.30, 1.05) | 0.65 | 0.24, 0.26 | — | **42°** | 32° | 7.00 | 5.85 | **2.19** | 5.65 |
| AE-elven | 9.4 | 1.70 | continuous (**0.25**, 0.95) | 0.62 | 0.23, 0.25 | — | 24° | 30° | 7.61 | 6.36 | 1.76 | 6.15 |
| VA-elven | 8.4 | **2.05** | continuous (0.40, 1.25) | 0.68 | 0.26, 0.28 | — | 26° | **40°** | 5.94 | 5.86 | 2.14 | 6.66 |
| HV-mixed | 7.6 | 1.80 | continuous (0.48, 1.30) | 0.72 | 0.27, 0.30 | — | 26° | 20° | 7.02 | 5.13 | 2.06 | 3.54 |
| GR-folded | 10.5 | 2.10 | **late (0.72, 1.6)** | 0.75 | 0.32, 0.34 | 3 × 0.16 | 26° | 28° | 8.99 | 6.97 | 2.46 | 6.12 |
| GO-bowl | 7.4 | **2.55** | rounded (0.50) | **1.35** | **0.40, 0.62** | 1 × 0.10 | **0°** | 10° | 7.25 | 5.27 | 2.05 | 4.09 |

Units are cm and degrees. The landmarks follow REFERENCE_ANATOMY_V1 §11:
- superaurale and subaurale give the auricle height;
- the auricle tip is the point farthest from the root;
- projection is the maximum lateral distance from the skull plane.

## 4. Canon-direction check on the schematic set

| Direction | Reading | Result |
|---|---|---|
| FN greatest lateral projection among elves | FN 2.19 > VA 2.14 > AE 1.76 cm | Holds. **FN > VA is marginal (2 %)** |
| AE more upward **and backward** than FN (ECR L109, L283) | Tip position (lateral / back / up, cm from root): AE 1.68 / 4.48 / 4.18 vs FN 1.91 / 3.98 / 3.83 | Holds (by construction) |
| VA more lateral and backward than AE | VA tip 1.84 / 4.81 / 2.80; lateral 1.84 > 1.68 and back 4.81 > 4.48 | Holds (by construction; lateral margin small) |
| AE taper longer / more gradual than VA | Taper start AE 0.25 vs VA 0.40 of length | Holds (by construction) |
| VA somewhat broader base | Base half-width VA 2.05 vs FN 1.80, AE 1.70 | Holds (by construction) |
| Three elf ears not identical, with no invented differences | Differences come only from the stated tendencies. FN length and taper are left at an elven middle, because canon gives FN no length or taper tendency | — |
| GR sustained body + late taper, length relative to HH moderate → strong | Taper from 72 %. L ÷ GR-ARM HH = 10.5 ÷ 26.96 = 0.39, vs MF 6.4 ÷ 22.5 = 0.28 | Holds |
| GO outward extent short-to-moderate vs elven/Grask long ears | Tip-from-root GO 5.27 vs elves 5.85–6.36 and GR 6.97 | Holds |
| **GO close-set projection** | Attachment angle 0° vs human 22°, **but** the measured auricle projection is GO 2.05 vs MF 1.98 cm. The deep bowl and broad rim add relief depth, and the RA §11 projection reads relief plus angle together | **Not demonstrated.** The close-set tendency needs the author to say whether "projection from the skull" excludes auricle relief (decision E-D4) |

## 5. Limitations (stated plainly)

- **Fidelity.** These are **schematic architecture references** (outline law, taper law, relief system, orientation) built procedurally. They are **not production-quality anatomical sculpts.** The helix, antihelix and concha are present as relief, but the fine cartilage forms of a real auricle are not. They are fit for accepting **architecture and magnitudes**. A sculpting pass is needed before they are attached to reference bodies as R-11 ear-family geometry.
- **Placement.** They are not yet attached. Attachment uses the generator ear root on each reference head, and the human auricle is removed there, after acceptance.
- **Families not built here:** the PK compact-rounded and CG fine-folded families (derivable from a human-structured auricle; order §6 lists only the six above), Durrim (human-auricle variable set), and Saurin (recessed opening, already closed).

## 6. Author decisions needed

- **E-D1:** accept or adjust each family's **architecture law**: continuous taper (elves), coupled human + elven (HV), sustained body + late taper with folds (GR), rounded broad rim + deep bowl (GO).
- **E-D2:** accept or adjust the **central magnitudes** in §3 (length, base, taper start, bowl, rim, projection angle, tilt). They are identity-relevant.
- **E-D3:** FN projection vs VA is only 2 % apart at these settings. Should the FN–VA projection gap be wider? Canon gives "greatest average", with no strict ranking for AE–VA.
- **E-D4:** for Gorrund, does "auricle projection from the skull" (AD-R43 variable i) measure **attachment-angle projection** (excluding auricle relief) or the RA §11 maximum lateral point (including relief)? With the latter, a deep-bowl ear reads less close-set.
- **E-D5:** approve a **sculpting pass** to raise the accepted schematics to anatomical detail before attachment. Builder-chosen; no new architecture.
- **E-D6:** HV: confirm that the HV reference is **one example** of the general envelope, not its centre; canon has no centre (HV L206).

— Claude

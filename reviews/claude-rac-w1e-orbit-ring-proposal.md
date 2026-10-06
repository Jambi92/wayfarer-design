# RAC W1e — MF / FN landmark orbital-margin rings and proposed FN increment (O-1)

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1d-author-decisions-continuation-order.md` §5 (O-D1…O-D4), §9 item 3
**Tool:** `tools/rac/w1/orbit_ring.py` **Evidence:** `reviews/rac-w1e-evidence/orbit/` and `tables.md` §6

## 1. What the ring is

A purpose-built **landmark orbital-margin ring**: an ellipse (orbital breadth × orbital height) standing in for the bony orbital aperture. It is a repeatable S-surrogate, **not a skull** (O-D1).

- **MF source (O-D2):** Alsaykhan & Abozaid 2025, *Int J Morphol* 43(3):843–851, dry adult skulls.
  - Males (n = 22): breadth 42.16 ± 1.85 mm, height 35.59 ± 1.72 mm. Used for **MF-M-R**.
  - Females (n = 20): breadth 41.00 ± 1.66 mm, height 34.83 ± 1.57 mm. Used for **MF-F-R**.
  - The same paper cites Fetouh & Mandour 2014 with close values (male 43.25 / 35.57 mm).
  - These are documented human means used as **landmark geometry**. They do not define a Marchfolk population envelope.
- **Placement (BUILDER-CHOSEN):** ring centre 0.8 cm in front of the landmark-globe centre; plane turned 20° so the lateral margin sits further back; breadth axis horizontal.
- **Fit check:** on all three heads every ring point lies inside the skin, and the ring clears the globe by about 0.7 cm (`tables.md` §6).

## 2. FN ring and the proposed increment

**Rule:** FN ring = MF-M-R ring × FN/MF head-size ratio × (1 + δ).
- The head-size ratio is HL for breadth and HH for height.
- The comparator is **MF** (O-D3). MF-M-R is used because it has the same generator configuration as FN.

**Proposed δ = 0.02 (2 %).** This is the smallest round increment that stays clearly above both limits below:
- **Method uncertainty of the normalized readings:** HL 0.15 %, HH 0.44 %. These are **assumed** landmark-placement spreads (0.03 cm on HL from the W1c FAL/Op spread; ±0.10 cm on HH for Me placement) divided by the MF head size. They are not a new repeatability measurement. The ring geometry itself is exact.
- **The accepted 1 % marginal threshold** (AD-G10).

**Result:** FN ORB breadth ÷ HL is 1.020 × MF-M-R, and ORB height ÷ HH is 1.020 × MF-M-R. This is **true by construction**. It shows that the ring rule produces the increment and that the FN ring physically fits the FN head (100 % inside skin, about 0.73 cm globe clearance). It is **not** independent evidence that FN orbits are larger. The canon relationship is authored here, not measured.

**Disclosure — comparison against MF-F-R.** Against the female-configuration reference, FN is only 1.006 × (breadth) and 1.005 × (height). That is below the 1 % threshold, because the female human source orbit is larger relative to the female head than the male one is to the male head. The two MF references themselves differ by 1.4 % (breadth ÷ HL) and 1.5 % (height ÷ HH), which is comparable to the proposed increment.
- This matters only if "MF" is read as the configuration-pooled reference, not the matched one.
- If the author wants FN > every MF reference by more than 1 %, δ must be at least 0.026 (height is the binding axis: 1.01 × 1.02 ÷ 1.0049 = 1.0252). Rounded up, that gives **δ = 0.03**. The exact ratios are in `tables.md` §6.

## 3. Status

- **Author acceptance needed (O-D2):** the ring method and placement, and the proposed δ (0.02 against matched MF-M-R, or about 0.03 if FN must exceed MF-F-R too).
- **Until then, RM-CF-08 FN ORB stays NOT DEMONSTRATED (O-D4).**
- The old E-proxy directional check (FN < MF) remains a diagnostic (O-D4) and stays in `directional_checks.json` as the only failing row. If the author accepts the rings, they replace it.
- No envelope is implied: δ is a W1 reference increment, not a population range (O-D2).

— Claude

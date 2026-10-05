# Saurin Female Pass 2: Readability and Dimorphism Exploration

**DIAGNOSTIC / NOT FINAL. Not canonized. `specs/saurin/SAURIN_V1.md` not edited. Female anatomy not closed.**

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-female-pass2-readability-order.md` (0466234)
**Builds on:** `reviews/claude-saurin-female-sex-related-anatomy.md` (67a8396)

**Frozen and unchanged in every variant:** skull, rostrum, orbits, jaw, neck, limb ratios, hands, feet, claws, tail envelope and path, and scale-field topology.

All variants are derived from the frozen reference (base `c12/g15_body` + surface `c12/g15_surf`) by the existing `vary.warp`, plus new smooth soft-tissue displacement fields in `tools/rodin/female/pass2/tissue.py`. The direction of each field is radial from a heavily smoothed torso-section centre, so the tissue follows the thoracic shell. The scale fields are carried along with the deformation, not re-sculpted.

## 1. Candidates

All candidates use equal stature (187.9 cm), Balanced frame and reference composition.

| ID | Definition | Status |
|---|---|---|
| Male | Frozen reference | — |
| **A** | Lower axial trunk **+10 %**, pelvic band **+5.5 %**. Head and tail compensated (×1.019) so they keep the reference absolute size and % H | Structural candidate (order §2) |
| **B** | A + unpaired ventral/ventrolateral fullness over the lower thorax and upper abdomen, peak **1.6 cm** | Non-mammalian, subtle (§3B) |
| **C** | Same field as B, peak **3.0 cm** | Non-mammalian, stronger (§3C) |
| **D** | A + restrained paired breasts, **3.8 cm** projection, broad base, upper pole tapering into the chest wall, no nipples | **Comparison only. Not canon** (§3D) |
| **E** | A + **coelomic body wall**: ventrolateral-to-lateral fullness of the lower rib cage and upper abdomen, peak **2.0 cm**. The waist fills in instead of pinching | **Additional** non-mammalian candidate (order allowance at the end of §8) |
| **E+B** | E plus B | Combined candidate |

Isolation controls:
- `a_tr`: trunk +10 % only;
- `a_pv`: pelvic band +5.5 % only;
- `p1`: the Pass-1 female (+6 % trunk / +3 % pelvis).

## 2. Sheets (`reviews/images/saurin-female-pass2/`)

| # | File | Deliverable |
|---|---|---|
| 1 | `v20_01_candidates_identical_cameras.jpg` | A/B/C/D(/E) identical-camera sheet |
| 2 | `v20_02_male_vs_each.jpg` | Male vs each candidate, whole body plus torso profile and front |
| 3 | `v20_03_structural_isolation.jpg` | Trunk alone, pelvis alone, A, Pass-1 (answers Q4 and Q5) |
| 4 | `v20_04_torso_close.jpg` | Torso close views on the scaled surface |
| 5 | `v20_05_gameplay_distance.jpg` | ~64 px standing height, shaded and flat silhouettes |
| 6 | `v20_06_pelvis_tail_root.jpg` | Pelvis, sacrum and tail root for A (and C) |
| 7 | `v20_07_stress_C.jpg` | Frame, composition, stature and tail stress on C |
| 8 | `v20_08_stress_E_overlap.jpg` | E+B stress, male/female overlap, ceilings |
| — | `v20_metrics.json` | All measurements |

## 3. Quantitative change accounting

All values are at equal stature (187.9 cm).

**Mesh measurements**

| Quantity | Male | Pass-1 | A | B | C | D | E | E+B |
|---|---|---|---|---|---|---|---|---|
| Lower trunk (hip → costal margin), cm | 32.0 | 33.4 | **34.3 (+7.3 %)** | 34.3 | 34.3 | 34.3 | 34.3 | 34.3 |
| Pelvic width (external), cm | 41.73 | 42.27 | **42.83 (+2.6 %)** | = | = | = | = | = |
| Chest width, cm | 38.57 | 38.16 | 37.89 | = | = | = | = | = |
| Midline thoracic depth, cm | 33.41 | 33.06 | 32.83 | 34.40 | **35.77** | 32.83 ¹ | 32.83 | 34.40 |
| Thoracic depth/width (bound 0.80–1.00) | 0.880 | 0.880 | 0.880 | 0.922 | **0.959** | 0.880 ¹ | 0.880 | 0.922 |
| Ventral projection ahead of section centre, cm | 18.36 | 18.17 | 18.04 | 19.62 | 20.99 | 18.37 ¹ | 18.04 | 19.62 |
| Head length / H | 0.1696 | 0.1698 | 0.1698 | = | = | = | = | = |
| Tail length, % H | 64.6 | 64.7 | 64.7 | = | = | = | = | = |
| Tail root area, cm² | 527 | 516 | 509 (−3.5 %) ² | = | = | = | = | = |
| Tail RSI (normalized) | 1.00 | 1.01 | 1.02 | 1.02 | 1.02 | 1.02 | 1.02 | 1.02 |
| Extra lean vs reference, deg (guard +3) | 0 | −0.01 | −0.03 | −0.21 | −0.38 | −0.09 | −0.22 | −0.40 |

¹ D's mounds sit at x ≈ ±8.8 cm, off the midline, so the midline depth and the maximum-projection measurements do not see them. Their own projection is 3.8 cm normal to the chest wall.

² The tail root is anatomically identical. The drop is isometric stature normalization: the longer trunk makes the whole body scale by about 0.98. RSI stays at 1.02.

**Frontal silhouette, measured from the front orthographic render (torso run only)**

| Ratio | Male | A | E / E+B |
|---|---|---|---|
| Waist (narrowest, sub-costal) / shoulder | 0.468 | 0.468 | **0.539** |
| Hip / shoulder | 0.763 | 0.773 | 0.773 |
| Waist / hip | 0.613 | 0.605 | **0.697** |

- E adds **+4.0 cm** to the waist (+15 %).
- B, C and D leave the frontal silhouette unchanged.
- The pelvis on its own moves hip/shoulder by +1.7 %.

## 4. Readability answers (order §5)

**1. Most clearly female at gameplay distance: E / E+B, and only weakly.**
- At ~64 px, surface form disappears. Only proportion and silhouette remain.
- E is the only candidate that changes the frontal silhouette: a fuller, less pinched mid-body against the male's strong sub-costal waist.
- C changes only the profile chest-belly contour, which is barely visible at that size.
- D is almost invisible at 64 px from front, profile and rear 3/4, because 3.8 cm on a 188 cm figure is under one pixel of silhouette.
- Honest finding: **no tested candidate makes sex reliably readable at gameplay distance.** That is consistent with the order's goal of average readability, but nobody should expect a strong tell from anatomy alone at that range.

**2. Most recognizably Saurin: A, B, E and E+B (tie); then C; D last.**
- B and E follow the thoracic shell and stay continuous across the midline.
- C begins to read as a deeper keel; this is still reptilian.

**3. Least human-female-template contamination: E.**
- E fills the waist, so it is the **opposite** of an hourglass.
- B and C are clean too: no paired forms.
- D is the only candidate carrying an explicit human-female signal.

**4. Does trunk +10 % read by itself?**
- Only side by side.
- At ~64 px, +2.3 cm of lower trunk is about 0.8 px. In isolation it is not a readable tell.
- It does strengthen the racial long-trunk identity and gives E more area to work on.

**5. Does pelvic band +5.5 % read without human hip flare?**
- It produces no hip flare, buttock or cleft (`v20_06`).
- It also produces **no material readability**: +1.1 cm external width at the pelvis.
- It is retained as biology (internal capacity), not as a visual tell.

**6. Do B or C give useful dimorphism without mammary biology?**
- **Yes at torso and conversation distance**, especially in profile and 3/4.
- **No at gameplay distance.**
- B is subtle. C is clearly visible up close.
- Neither requires mammary biology (§5).

**7. Does D look integrated?**
- Up close it is restrained and sits on the shell. It does not visibly fight the thorax mechanically.
- It **reads as breasts added to the reptilian torso**: the only paired, discrete soft forms anywhere on an otherwise continuous, scale-plated body.
- The result is the "human-female-with-scales" effect the order warned about.
- It also contributes almost nothing at gameplay distance, so it pays its biological cost without buying readability.

## 5. Biological implication table (order §4)

| Candidate | What it can be justified as | Specialized reproductive tissue implied? | Mammary/lactation implied? | Status |
|---|---|---|---|---|
| A (trunk/pelvis) | Fecundity-selected body-cavity length and pelvic-canal capacity (the reptile pattern) | No | No | Justified by sex-correlated capacity. The internal-gestation premise stays an **OPEN** author decision |
| B / C (ventral fullness) | Sex-correlated ventral soft-tissue reserve: a fat-body/energy store for provisioning eggs or young (squamate fat bodies are the analogue), plus a fuller ventral body wall | Mildly: a reserve associated with reproduction, not a reproductive organ | No | Composition-like. The reserve function is **OPEN** (not canon) |
| E (body wall) | Larger coelomic volume housing the reproductive tract. The same fecundity logic as A, expressed as body-wall girth instead of length | No (capacity only) | No | Most directly derived from existing canon (long lower axial trunk) |
| D (paired breasts) | Only mammary glands, implying lactation and nursing. Paired discrete glands imply a mammalian nursing life history the Saurin canon has never had (egg/young provisioning mode is unspecified) | Yes | **Yes** | **Unsupported.** Adopting it would require new reproductive canon (live birth plus lactation) chosen for silhouette. Not recommended |

## 6. Overlap and anti-stereotype results (order §6, `v20_07`, `v20_08`)

**C (A + 3.0 cm fullness)**

| Case | Result | Note |
|---|---|---|
| Narrow | **CONSTRAIN** | Thoracic d/w reaches **1.026 > 1.00**. Fullness counts against the thoracic-shell bound, so on Narrow it clamps to about **2.0 cm** |
| Broad + high muscle | PASS | d/w 0.917; RSI 0.83 (≥ 0.75) |
| Fat low | PASS | Fullness is not fat; it remains when fat is minimal |
| Fat high | PASS | d/w 0.987; no hourglass |
| 208 cm Broad high-muscle | PASS | — |
| Broad + 80 % tail | PASS | +2.2° (guard 3°) |
| 55 % tail | PASS | — |

**E+B**

| Case | Result | Note |
|---|---|---|
| Narrow | PASS | d/w 0.985 |
| Broad + high muscle | PASS | — |
| Fat low | PASS | — |
| Fat high | PASS | d/w 0.947 |

**Overlap**

| Case | Result | Note |
|---|---|---|
| Male inside the female range (trunk +10 %, pelvis +5.5 %, fullness 1.6 cm) | PASS | **Geometrically identical to female B** |
| Male with half body-wall fullness | PASS | — |
| Female at the low end of every tendency | PASS | Identical to the male mean |
| Ordinary female individual (trunk +4 %, pelvis +2 %, fullness 1.6 cm) | PASS | — |
| Short Narrow low-muscle male (168 cm) | PASS | — |

**Ceilings**

| Case | Result | Note |
|---|---|---|
| Fullness requested at 4.5 cm | CONSTRAIN | d/w 0.998 passes, but the request is above the 3.0 cm diagnostic ceiling |
| Fat high + 4.5 cm | CONSTRAIN | d/w 1.027 |
| Female trunk requested at +16 % | CONSTRAIN | Clamped to the +10 % species bound |

**Sex controls nothing else:**
- Stature, frame, muscle, fat, tail, displays, skull and face parameters are identical across candidates.
- Head length/H is 0.1698 for all.
- The display family is unaffected (head construction is the same as Pass 1, which validated all six families on the female).

**Structural problem with a +10 % trunk *mean*:**
- +10 % is the species **hard maximum**, so a female centred there would clamp half of her own distribution.
- Females could then vary only downward, piling up at the bound.
- That conflicts with "prefer overlapping distributions".
- The author must choose one of:
  - (a) keep the A body as the *reference female* but sample females around a lower centre (≈ +7 %);
  - (b) accept a one-sided female trunk distribution;
  - (c) widen the species trunk bound, which would reopen frozen anatomy and is not done here.
- **Recommendation: (a).** The reference body can sit at the visible end without making it the distribution centre.

**New coupling found:** ventral fullness (B/C) adds midline thoracic depth at about 1 cm per cm of fullness. It therefore shares the existing thoracic depth/width ≤ 1.00 bound with thorax_d, frame and fat. E adds width as well as depth, so it does not hit that bound.

## 7. Surface and anatomy protection (order §7)

- Skull, rostral projection, orbits, jaw, neck, limb ratios, hands, feet, tail length envelope and tail path are untouched in every variant.
- Scale topology is unchanged. Scales only deform locally with the tissue, and stay regionally coherent in B, C, E and D (`v20_04`).
- Sacral platform, posterior mass and tail root are unchanged (`v20_06`).
- The ventral pelvic field is unchanged, and no external sex anatomy is modelled.

## 8. Recommendation (not canonized)

**Recommended package: A-structure + E (coelomic body wall) + B-level ventral fullness, as soft sex-shifted distributions.**
- **Lower trunk:** reference female body at +10 %, sampling centre about +7 % (see the structural problem in §6).
- **Pelvic band:** +5.5 % centre, inside ±7 %.
- **Body wall:** about 2.0 cm centre.
- **Ventral fullness:** about 1.6 cm centre, ceiling 3.0 cm, clamped by thoracic d/w ≤ 1.00.
- **Males:** distributions centred at 0, overlapping the female ranges.

Why this package:
- E is the only non-mammalian change that moves the frontal silhouette.
- E is anti-hourglass.
- E derives from the existing long-trunk racial trait.
- E+B gives torso-distance readability without mammary biology.

C is a valid stronger setting, with the Narrow-frame clamp. **D is not recommended.**

Expectation: average readability improves at torso and conversation distance and modestly in frontal silhouette. It does **not** become reliable at gameplay distance. If stronger long-range readability is wanted, it will have to come from the presentation layer (dress, gear, culture) or later pigmentation-system decisions, not from more anatomy.

## 9. OPEN / author decisions

1. Internal-gestation premise (still OPEN), and whether fat-body-style reserves (B/C) are canon biology.
2. Female trunk distribution: (a) lower sampling centre / (b) one-sided / (c) bound change (§6).
3. Accept E as a new sex-correlated soft-tissue control? Should it be its own creator control, or ride on fat/composition?
4. Ventral fullness ceiling (3.0 cm diagnostic) and the shared thoracic d/w coupling.
5. Final magnitude: low (Pass 1) vs this moderate package.
6. D direction: the author and Tyler decide visually. Claude's audit finds it unsupported by Saurin biology.
7. Female GLB comparison is still not possible (file not accessible).

## 10. Files

- **Report:** this file.
- **Images:** `reviews/images/saurin-female-pass2/v20_01`…`v20_08`, `v20_metrics.json`.
- **Tools:** `tools/rodin/female/pass2/`:
  - `tissue.py`, `fsets2.py`, `sweep2.py`, `render2.py`;
  - `readab.py`, `torsosil.py`, `compose20.py`, `proto.py`.

STOP. No spec edit, no closure, no facial-control, rigging, animation, clothing, pigmentation or UE5 work. Awaiting ChatGPT author review and Tyler's visual decision.

— Claude

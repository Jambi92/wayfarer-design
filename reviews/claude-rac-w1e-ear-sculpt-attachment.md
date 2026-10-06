# RAC W1e — Ear families: sculpt-detail pass and attachment

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1d-author-decisions-continuation-order.md` §4 (E-D1…E-D6), §9 item 2
**Tools:** `tools/rac/w1/ear_families_v2.py` (geometry), `attach_ears.py` + `ear_attach_sheet.py` (attachment), `ear_checks.py` (directions)
**Evidence:** `reviews/rac-w1e-evidence/ears/` and `tables.md` §5

## 1. What changed from W1d

- **Same architecture laws and the same outline / orientation parameters as the W1d reference centres** (E-D1, E-D2). No new architecture. The added relief does move some measured landmarks: total lateral extent GO 2.05 → 2.35 cm (+15 %), GR 2.46 → 2.63 cm (+7 %) (W1d `ear_families.json` vs `ear_families_v2.json`).
- **Sculpt-detail relief (E-D5)**, added to every family:
  - helix rim and scapha;
  - Y-shaped antihelix (stem, superior and inferior crura) bounding the triangular fossa;
  - concha split by the crus of the helix into cymba and cavum;
  - tragus, antitragus and intertragic notch;
  - fleshy lobe.
- **Family-specific relief:**
  - **Elven ears** carry the superior crus and helix up into the continuous taper.
  - **Grask** adds the folded-cartilage ridge system: 4 folds through the sustained upper body.
  - **Gorrund** has the deep bowl, a stronger antihelical fold system and a broad, non-tapering rim.
- **E-D3:** the FN projection angle rose from 42° to 50°. FN total lateral extent is now 2.41 cm against VA 2.21 cm (+8.7 %; W1d was +2.7 %). No other orientation relationship changed.
- **E-D4:** GO close-set is read as the **auricle-body angle**: the angle between the best-fit plane of the ear's front surface and the skull plane. GO is 11° and MF 29°. The RA §11 total lateral extent is reported separately, as a report-only row (GO 2.35 vs MF 2.06 cm).
- **E-D6:** HV-mixed is one example of the inheritance envelope, not its centre.
- **New families (order §4, last paragraph):**
  - **PK compact-rounded:** rounded top, clear but not deep concha, close attachment (PIPKIN L351).
  - **CG fine-folded:** fine cartilage (0.18 cm, the thinnest of all families), crisp folds, rounded non-pointed top (COGLING L1327–L1366).
  - Both were built in absolute cm for the PK-NAT / CG-NAT heads.

**Every parameter is BUILDER-CHOSEN.** The values are W1 reference centres, not population bounds. They are listed in `ear_families_v2.json` (`outline_params`, `relief_params`).

## 2. Canon-direction checks

`ear_checks.json` has **22 checks: 22 pass, 0 marginal at the stated 5 % schematic margin**, plus 10 report-only rows. **10 of the 22 are measured on the built mesh** (extent, tip direction, auricle-body angle, tip-from-root); **12 are construction checks** that only confirm a builder input encodes the canon direction (base width, taper fraction, fold count, concha depth, cartilage thickness, rounded top) and are not independent evidence. The checks are:
- FN greatest projection;
- AE more upward and backward than FN;
- VA more lateral and backward than AE, and broader at the base;
- AE taper longer than VA;
- GR late taper and folds;
- GO close-set angle, shorter extent than elves and GR, deep bowl;
- PK close attachment, shallower concha, rounded top;
- CG finer cartilage than PK and MF, rounded top, no deep bowl.

## 3. Attachment (BUILDER-CHOSEN rule)

How each ear was attached:
- The generator's human auricle is **collapsed onto the side of the head**: pulled 85 % toward the skull plane and 60 % toward the root. It is not deleted, so the body vertex set is unchanged.
- The family ear is placed at the generator ear root:
  - anterior attachment line 0.2 cm behind the front of the generator auricle;
  - 0.15 cm inside the medial root;
  - vertical midpoint at the generator auricle midpoint.
- **Scale:** families authored at MF-M-R head scale are scaled by HH(body) ÷ HH(MF-M-R). PK and CG are attached unscaled.
- The composite (body + ears) is **evidence geometry only**. All body and head measurements stay on the ear-less body files, as before.

**Results (`ears_attached.json`, `ears_attached_sheet.jpg`):** all nine heads (MF, FN, AE, VA, HV, GR, GO, PK-NAT, CG-NAT) have their family ear in place. Each head is shown in left-side, front and back views, with the family ear tinted.
- **Durrim** keeps the generator's human auricle (broadly humanoid compact range; no family was ordered).
- **Saurin** is unaffected.

**Readings:** auricle height ÷ HH is reported for every body (report only; canon gives no ratio). GR is the largest (0.40). VA is the only family below MF, slightly (0.264 vs 0.278), because its tilt and shorter taper reduce its vertical height.

## 4. Limits

- Procedural relief, not a hand sculpt. The anatomy is legible on the sheet, but the fine cartilage transitions of a real ear are approximated.
- The attachment is a rigid placement with no blend to the scalp skin. That is acceptable for W1 reference evidence and not for production topology (out of scope).

## 5. Author acceptance needed

- **EA-W1:** the v2 relief and the attachment rule as W1 reference geometry.
- **EA-W2:** the two new centres (PK-compact, CG-fine-folded), including whether "adult humanoid in scale" (COGLING L1691) means absolute ear size. See `claude-rac-w1e-pk-cg-globe-fit-flag.md` §4.
- **EA-W3:** the FN projection angle of 50° (E-D3 widening).

— Claude

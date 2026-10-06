# RAC W1d — Fenn Bony-Orbit Measurement Decision Packet

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §9 (work order item 5)
**Status:** AUTHOR DECISION PACKET. Fenn orbit canon is **not** rewritten. FN is **not** rebuilt: no defensible failure has been shown (§4).
**Evidence:** `reviews/rac-w1d-evidence/orbit_proxies.json`; tool `tools/rac/w1/orbit_rim.py`

## 1. Canon being tested

- **FENN L173 (AD-R44 reading):**
  > "Slightly larger orbits, slightly more eye prominence … **Reading (RAC Phase 2, October 5, 2026; AD-R44):** bony orbit size (ORB) slightly larger **and** visible presentation (aperture) slightly more open, two separately measured quantities (UFCA AC-U1)."
- **UFCA L92 AC-U1:** bony orbit size and visible aperture are both DIR; the globe is DER from the orbit.
- **r3 L74:**
  > "ORB — Orbit breadth (Ec–Mf) ÷ HL; orbit height ÷ HH | S/E | Orbit size ≠ visible aperture."
  - Layers (r3 L11–14): S is used where an approved skull exists; E is the surface proxy.
- **Author ruling (W1c acceptance §3):** "Low-confidence soft-tissue orbit proxies cannot overrule authored bony-orbit canon."

**Canon gaps found:**
- **G-1 Comparator unnamed.** FENN L173 names no comparator for "slightly larger orbits". The W1c test used MF. The Elf Comparative Review compares Fenn *presentation* with Aelari and Vael (ECR L141, L282), and Vael orbits are "moderate to somewhat large" (VA L256). This is the old F-20 collision.
- **G-2 No orbit-height landmark pair.** r3 defines breadth landmarks (Ec–Mf) but none for height. Or\* is an orientation point only.

## 2. Why no current method is bony

None of the W1 reference geometry has a skull. The MakeHuman base mesh is a closed skin surface with an eye pocket. Every available "orbit" reading is therefore an **E-layer soft-tissue or generator-socket proxy**. The candidates are:

| Proxy | What it reads | Method |
|---|---|---|
| **P1 rim-crest** (new) | Skin over the orbital margin | Frontal depth map. Along 24 radial directions from the eye centre, the most convex point (minimum second derivative, 0.25 cm smoothing) beyond the visible aperture. Breadth = span at 0/180°, height = span at 90/270° (±15° rays averaged) |
| **P2 socket capacity** (new) | The generator's eye pocket | Diameter of the largest globe fitting at the generator eye centre without skin intersection |
| **P3 generator socket helper** | The generator's own eye-socket definition | Mean extent of the MakeHuman eye helper (this drives the DER globe) |
| **P4 W1c Ec\*/Mf\* proxy** | Soft-tissue canthal rim | As in W1c (`claude-rac-w1c-build-method.md` §4). **Depends on the globe size**: the aperture edge used to bound the search moves with the globe. MF-F-R's swap from 2.44 to 2.30 cm moved its orbit breadth from 2.556 to 2.370 cm |
| Aperture | Visible palpebral opening | Frontal visibility of the globe |

## 3. Test on the current references (diagnostic)

Breadth values are ÷ HL and height values ÷ HH. "sd" is the spread across the ±15° rays (cm), a repeatability indicator.

| Body | P1 breadth | P1 height | P1 sd (b / h, cm) | P2 | P3 | P4 breadth | P4 height | Aperture w × h (cm) |
|---|---|---|---|---|---|---|---|---|
| MF-M-R | 0.2477 | 0.1738 | 0.24 / 0.16 | 0.1188 | 0.1438 | 0.1490 | 0.0963 | 2.08 × 0.72 |
| MF-F-R | 0.2575 | 0.1675 | 0.24 / 0.18 | 0.1187 | 0.1524 | 0.1196 | 0.1207 | 2.24 × 0.84 |
| SG | 0.2438 | 0.1743 | 0.27 / 0.09 | 0.1189 | 0.1438 | 0.1430 | 0.1142 | 2.12 × 0.72 |
| SK | 0.2141 | 0.1480 | 0.21 / 0.32 | 0.1201 | 0.1440 | 0.1450 | 0.1076 | 2.44 × 0.84 |
| **FN** | **0.2436** | **0.1573** | 0.29 / **0.64** | **0.1213** | **0.1439** | **0.1258** | **0.1252** | **2.24 × 1.00** |
| AE | 0.2309 | 0.1498 | 0.27 / 0.25 | 0.1166 | 0.1410 | 0.1279 | 0.0878 | 2.12 × 0.72 |
| VA | 0.2428 | 0.1721 | 0.29 / 0.06 | 0.1190 | 0.1439 | 0.1516 | 0.0963 | 2.16 × 0.76 |
| HV | 0.2439 | 0.1713 | 0.27 / 0.04 | 0.1190 | 0.1439 | 0.1507 | 0.0906 | 2.16 × 0.72 |

**FN vs MF-M-R by proxy:**

| Proxy | Breadth | Height |
|---|---|---|
| P1 rim-crest | −1.7 % | −9.5 % |
| P2 socket capacity | +2.1 % | — |
| P3 socket helper | +0.1 % (equal) | — |
| P4 Ec\*/Mf\* | −15.6 % | +30.0 % |

- **Uncertainty:** P1's ray spread across bodies is 0.21–0.29 cm on breadth (rim spans about 5 cm, 4–6 %) and 0.04–0.64 cm on height (spans about 3.6–4.0 cm; FN's 0.64 cm is about 18 %). For FN it is larger than every FN–MF difference P1 reports.
- **P3 is insensitive to the Fenn build:** the generator's eye-region target enlarges the lids and socket tissue but not the socket helper.

**The aperture (soft, separate quantity):** FN opens more than MF in both width (2.24 vs 2.08 cm) and height (1.00 vs 0.72 cm). The aperture is read through the landmark globe, and FN's DER globe is 1.9 % larger than MF's; the height difference (+39 %) is far larger than that. The "slightly more open" half of FENN L173 is supported, diagnostically.

## 4. Finding

**The bony-orbit half of FENN L173 cannot be tested defensibly on the current geometry.**
- The four proxies disagree in sign.
- The only proxy that reads a margin-like feature (P1) has repeatability worse than the effect being sought.
- None of them is bone.

Under the author ruling, the W1c P4 "FAIL" does not overrule canon. Under order §9 (rebuild only "if FN truly fails after a defensible test"), **FN is not rebuilt.** RM-CF-08 (FN ORB) stays **NOT DEMONSTRATED** rather than FAIL.

## 5. Options for the author (method decision)

| Option | What it is | Pros | Cons |
|---|---|---|---|
| **O-1 (recommended) Landmark orbital-margin ring** | Each reference head gets a purpose-built **bony orbital-margin landmark ring**. It is placed like the landmark globes: on the socket, under the soft tissue, sized from a documented adult-human bony-orbit reference for MF, then scaled per the race's orbit canon. ORB is then read on the ring (Ec–Mf breadth; a defined superior/inferior margin pair for height, which closes G-2) | Gives a repeatable S-surrogate on every reference; usable across MF/FN and later RM-CF-08 / RM-UF-01 / RM-SR-04; keeps orbit ≠ aperture | **Circular for FN.** The ring's FN size is builder-chosen ("slightly larger" has no number), so measuring it confirms the choice. It needs author acceptance of the MF ring source and of the FN increment |
| O-2 Skull reference geometry | Model or source a skull, at least the orbital region, per reference head | True S layer | Large asset effort; still builder-authored for non-humans |
| O-3 P2 socket capacity as the interim E proxy | Use P2 for ORB | Already computed, small spread | Reads the generator pocket, not bone; sensitive to the globe size and the pocket shape |
| O-4 Keep RM-CF-08 (FN ORB) blocked | Do nothing until O-1 or O-2 | No false result | FN stays CONSTRAINED on this item |

**Comparator decision (G-1):** state whether "slightly larger orbits" is against MF, against AE and VA, or against both. The F-20 history and VA L256 make "against AE and VA" a live reading. The test changes with the answer.

## 6. Author decisions needed

- **O-D1:** choose the orbit method (O-1 / O-2 / O-3 / O-4).
- **O-D2:** if O-1, the MF bony-orbit source and the FN increment are builder-chosen and need acceptance. The increment is identity-relevant.
- **O-D3:** the comparator for FN "slightly larger orbits": MF, AE/VA, or both.
- **O-D4:** confirm that RM-CF-08 (FN ORB) is recorded as NOT DEMONSTRATED (not FAIL) until O-D1 is settled, and that the diagnostic aperture result stands as diagnostic.

— Claude

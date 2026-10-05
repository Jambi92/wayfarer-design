# Pass 2 — 02. Cross-Race Collision Matrix

**Author:** Claude (auditor). **Order track:** I. Finding IDs are defined in `claude-pass2-06-findings.md`.

**What the risk rating measures:** the chance that two *valid* individuals of different populations converge into the same read once surface phenotype, presentation and equipment are neutralized.

The rating weighs four things:
- stature overlap;
- how close the two populations' biological families are;
- whether canon states positive distinguishing dimensions;
- whether those dimensions are quantified.

**Key:**
- **H** = high; **M** = moderate; **L** = low; **—** = no meaningful risk (no stature overlap and different families).
- **\*** = collision accepted by canon design. Identity is population-level only, so individual convergence is valid.

## 1. Pairwise risk grid (all 78 pairs)

| | Ska | Sag | Fen | Ael | Vae | Hal | Dur | Gra | Gor | Pip | Cog | Sau |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Mar** | M | H\* | M | L | M | H\* | M | L | — | — | — | L |
| **Ska** | | L | L | L | L | M\* | L | M | **H** | — | — | L |
| **Sag** | | | M | M | L | H\* | L | L | L | — | L | L |
| **Fen** | | | | M | M | H\* | — | L | L | L | L | L |
| **Ael** | | | | | M | H\* | — | M | L | — | — | L |
| **Vae** | | | | | | H\* | L | L | L | — | — | L |
| **Hal** | | | | | | | L | L | L | — | — | L |
| **Dur** | | | | | | | | — | M | M | L | L |
| **Gra** | | | | | | | | | M | — | L | L |
| **Gor** | | | | | | | | | | — | — | L |
| **Pip** | | | | | | | | | | | **H** | — |
| **Cog** | | | | | | | | | | | | — |

Race abbreviations: Mar Marchfolk, Ska Skarn, Sag Sagekin, Fen Fenn, Ael Aelari, Vae Vael, Hal Halvren, Dur Durrim, Gra Grask, Gor Gorrund, Pip Pipkin, Cog Cogling, Sau Saurin.

**Totals:**
- 2 unaccepted high risks: Skarn–Gorrund, Pipkin–Cogling.
- 7 accepted-by-design high or moderate pairs (\*): Marchfolk–Sagekin and Halvren with each of its 6 sources.
- 14 moderate pairs.
- The remaining pairs are low or no risk.

**Saurin is low risk against every population.** It has a mandatory tail, a rostrum with a non-overlap intent, a recessed auricular opening and scaled integument. The only Saurin coverage gaps are the missing Sagekin and Halvren comparisons (F-25).

## 2. Meaningful risks: preserving dimensions and gaps

### Human populations

**Marchfolk–Sagekin (H\*), 152–203 cm**
- Preserving dimensions: slightly greater leg share; longer forearms, hands and fingers; slightly shorter, shallower torso; longer face and higher forehead (Sagekin v1.1 §1; v1.2).
- Canon accepts individual ambiguity (v1.0 §10; SG-10) and identity is statistical (v1.4 §7).
- Gaps: none against canon (I-02). Surface distributions are listed among the differentiators (FD §3), and there is no "not any one real-world population" disclaimer (F-19).

**Marchfolk–Skarn (M), 183–203 cm**
- Preserving dimensions: clavicle breadth, ribcage depth and width, upper back, neck base, pelvis, joint scale, hands and feet (Skarn v1.0 §3; v1.1 §1).
- Canonical test: equal height at 190 cm (v1.4 §6, marked "future").
- Gaps: every carrier is a Marchfolk-relative magnitude with no value. "more natural muscle volume" is listed as an identity trait (F-04). At 183–190 cm, a Narrow, low-muscle Skarn has no quantified separation (F-06).

**Skarn–Sagekin (L):** opposite tendencies (robust vs linear). Covered by Sagekin v1.4 §7.

### Elven family and Halvren

**Fenn–Aelari (M), 168–211 cm**
- Preserving dimensions: Fenn is extremity-emphasized and compact-centred; Aelari has whole-body vertical continuity (longer torso, neck and waist, evenly long limbs).
- Ears: Fenn has the greater lateral projection; Aelari is upward and backward. Ears overlap and are never the sole marker.
- Sources: Aelari v1.0 §5, §15; v1.1 §15–17; elf review final matrix.
- Gaps: the Fenn ear tendency lives only outside the Fenn spec (F-18). Aelari is defined mostly "than Fenn", which the order allows but makes Fenn a working anchor.

**Fenn–Vael (M), 157–203 cm**
- Preserving dimensions: Vael has skeletal thoracic depth, torso share, joint and extremity-base presence, and less limb elongation.
- Gap: orbit-size wording points both races toward "larger" orbits (Fenn v1.2 "slightly larger orbits"; Vael v1.2 §10–12 "moderate to somewhat large"). The elf review reframes Fenn as open *presentation*, not orbit size (F-20).

**Aelari–Vael (M), 168–203 cm**
- Preserving dimensions: vertical continuity vs compact depth; neck relative length (Vael v1.1 §3–7 "relative, not absolute"); brow, midface and jaw presence.
- Gap: Vael's "lower center of mass than Aelari" is not carried into the elf review (F-20).

**Elves vs Marchfolk and Sagekin (M for Fenn–Marchfolk, Vael–Marchfolk, Fenn–Sagekin and Aelari–Sagekin; L for the rest):**
- Combined skeletal relationships, not ears or pigmentation (Vael v1.0 §17–18; Fenn v1.0 §13; Aelari v1.1 §15–17).
- Gap: the Sagekin–elf test is still "reserved … once the elves are defined" (Sagekin v1.5 §9), though the elf-side tests exist (FN-17, AE-21) (F-19).

**Halvren vs its six sources (H\*)**
- Mixed developmental space, never averaged.
- Phenotypic boundary protection: ancestry controls cannot exactly recreate another race (P2 §32–36; P3 §45–47).
- Individual collapse is accepted (P1 §30–31; HV-04) (I-02).
- Gap: the "race" term is overloaded across biological population, playable classification and culture (CRes §6–9) (F-09).

### Short races

**Pipkin–Cogling (H), ~91–107 cm. Unaccepted.**
- Pipkin carriers: Low-Set Compact Trunk (modestly reduced central-trunk share; structurally participating mature pelvis); sustained limbs without distal redistribution; Integrated Mature Facial Architecture.
- Cogling carriers: narrow stable core near the Marchfolk trunk range; distal redistribution within near-Marchfolk limb totals; fine shafts and joints; Fine-Scale Planar Integration face.
- Sources: Cogling §63, §90, §90A; Pipkin P2 §1–6; short-race review §5–§9, SR-COMP-01/02.
- Gaps: canon says "Leg segmentation alone cannot separate Cogling from Pipkin" (Cogling §63) and "distal segmentation alone cannot distinguish" (short-race review §6). Pipkin's primary identifier has **no metric**, and SR-COMP-01/02 are qualitative. Pipkin's spec has no Pipkin-authored Cogling face test (F-06).

**Pipkin–Durrim (M), boundary at ~122 cm**
- Preserving dimensions: structural presence, torso depth and breadth, joint scale, limb contribution, hands and feet; the two "never share one pelvis" (Pipkin P2 §7–17).
- Critical crossings are tested: Broad Pipkin vs Narrow Durrim, and so on (P1 §82–94; SR-COMP-03).
- Gap: none beyond F-06.

**Durrim–Marchfolk (M), 147–152 cm**
- Preserving dimensions: torso contribution and depth, limb contribution, joint scale, hands, head–neck integration.
- Canonical test at 152 cm (P2 §54–63); the low-muscle permanent test fails if the Durrim reads human.
- Gap: the equal-height test is stated at 150 cm in some places and 152 cm in others (F-11).

**Cogling–Durrim (L):** no stature overlap. Normalized tests are mandatory (§64; COG-BODY-10/10A).

**Durrim–Vael (L):** Vael's "compact" is explicitly not dwarven (Vael v1.0 §4; v1.1 §25–27).

### Large races

**Skarn–Gorrund (H), 208–229 cm. Unaccepted.**
- Preserving dimensions in canon: Gorrund has greater axial breadth, depth and "structural scale beyond 'big human'"; Axial Load-Path Continuity; Transverse Structural Continuity face; deep-bowl ears.
- The comparison "Fails as 'extra-broad Skarn'" and fails "if Gorrund need more muscle to be distinguished".
- Sources: Gorrund P1 L109; P2 L237; P3 L328, L398; P5 L671; FC L731. Skarn v1.0 §4; v1.4 §8.
- Gaps:
  - Gorrund's limb and torso proportions are stated **only relative to Grask**, never relative to Skarn or Marchfolk. A Gorrund with Skarn-like limb proportions is therefore valid.
  - Several carriers are *absolute-scale* claims ("high absolute structural scale").
  - The Skarn side is entirely qualitative.
  - The **Large-Race Comparative Anatomy Review** required by PROJECT_RULES was never performed (**F-01**).

**Grask–Gorrund (M), 208–239 cm**
- Preserving dimensions: proportional torso vs limb contribution, arm span, facial verticality vs transverse breadth, ear architecture.
- The comparison must survive composition inversion ("Fails if the distinction depends on muscle or fat", Gorrund P2 L236).
- Gaps: Grask's own Gorrund references are empty placeholders, superseded by the later Gorrund spec (I-03). The Gorrund equal-height band is worded as 208–239 cm and 218–229 cm in different places (F-11). Ratios are unquantified (F-06).

**Skarn–Grask (M), 198–229 cm**
- Preserving dimensions: Grask has rangy, limb-dominant non-human architecture against Skarn's large human architecture. "Fails if it becomes Skarn with longer arms"; fails "if skin or ears alone separate them".
- Sources: Grask P1 §60–70 L100–104; P5 L701.
- Gap: Skarn's spec never mentions Grask, and the comparison is carried one-sidedly by Grask (F-01, as part of the Large-Race review).

**Grask–Aelari (M), 198–221 cm**
- Grask is limb-dominant; Aelari has distributed vertical elongation. The neck is deliberately de-emphasized for Grask; "'Thicker Aelari' fails".
- Sources: Grask P1 L105; P1C L170–174; P3 L380; P3C L461.
- Gap: none beyond F-06.

**Durrim–Gorrund (M, conceptual only):** no stature overlap. The shared tendency wording (cranial breadth to height, thoracic depth, neck–torso integration) is resolved by Gorrund P3C (transverse vs depth-dominant) and FC §12–17 (load-path vs compact concentration), with matched-scale tests (I-04).

### Saurin against humanoids at matched height

**Saurin vs Marchfolk, Skarn, Aelari, Vael, Fenn, Durrim, Grask, Gorrund, Pipkin, Cogling (L)**
- Separated by structure that never overlaps with any of them: mandatory tail and pelvic-axial architecture (§1, §5, §225); rostrum (index ≥ 0.255, §259); recessed auricular opening with no pinna (§56); gait signature (§173); scaled integument.
- Sources: §31, §66–72, §248; SAU-BODY-03/11–16/21/22; SAU-FACE-10–15.
- The rostral floor's cross-race numeric check is OPEN (F-02).

**Saurin vs Sagekin and Halvren (L):** these pairs are absent from §31, §66–72 and §248. The risk is still low because the same carriers apply (F-25).

## 3. Additional collisions found in the specs

| Pair or group | Mechanism | Status |
|---|---|---|
| Cogling distal emphasis ↔ Sagekin, Grask, Fenn, Pipkin | Each of these has forearm, hand, finger or lower-leg emphasis (Cogling §63–§67A) | Canon resolves it by **conjunction** (near-Marchfolk totals + proximal reduction + fine shafts + narrow core). Unquantified (F-06) |
| Durrim ↔ Gorrund wording | Identical tendency phrases | Resolved by Gorrund P3C/FC (I-04) |
| Fenn ↔ Vael orbit size | Both "larger" | Terminology (F-20) |
| Vael ↔ Grask, Gorrund pigmentation | Gray, olive and gray-green adjacency | Canon: pigmentation is never required to separate them (Grask P4C L596; Gorrund P4 L499) |
| Gorrund ↔ Aelari, Fenn, Sagekin at 208–221 cm | Stature touch | Boundary tests exist (Gorrund P2C L262–267) |

— Claude

# UFCA-06: Universal Facial Validation Framework

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ufca-phase1-order.md` §10, §11
**Status:** PROPOSAL for author review. Every race-specific permanent test is **carried forward unchanged** and assigned to a tier. Nothing is replaced. Numeric thresholds are deferred (§5).

## 1. Common machinery

### 1.1 Outcomes

| Outcome | Meaning |
|---|---|
| **PASS** | Valid |
| **CONSTRAIN** | Valid after a reported clamp or neighbour adjustment |
| **FAIL** | Invalid; rejected and explained |

Generalized from Saurin §255 and §159 (author decision AD-U2).

### 1.2 Neutralization protocol (N-levels)

The protocol unifies the neutral states already written in DU L290, GR L406, GO L371, CG L1602–1606, VA L298 and SA §65 (author decision AD-U10).

| Level | Removes | Matches canon test(s) |
|---|---|---|
| **N0** | Nothing (as authored) | Acceptance and expression tests |
| **N1** | Presentation: cosmetics, styling, applied markings, clothing, jewellery | SK L304; SG L383; AE L484 |
| **N2** | N1 + hair (bald or controlled), facial hair removed, eyebrows neutralized where practical; Saurin display set to minimal (structural ridges stay) | DU hidden-beard L213; GR/GO core rule; CG L1604; SA SAU-SURF-25 |
| **N3** | N2 + pigmentation neutral (neutral grey or ordinary mid tone), surface pattern neutral, acquired features removed | VA L298; HV L218; CG COG-FACE-01; SA SAU-FACE-16 |
| **N4** | N3 + ears hidden or partly obscured (per race test) | FN L211; AE L243; HV L218; DU L214; GR/GO "partially obscured"; PK PIP-FACE-13; CG COG-FACE-14 |

**At every level:**
- neutral expression;
- neutral reference lighting (ECR L165; VA L588);
- standardized camera and focal length;
- matched apparent age and soft tissue for pairwise tests (DU L290).

### 1.3 Comparison conditions

| Condition | Meaning | Canon basis |
|---|---|---|
| **Equal-height** | Both populations at a stature valid for each | SK L288; DU L221; PR / DU L337 |
| **Matched-scale** | Display head size normalized; diagnostic only, never resizing characters | GO L437; PK PIP-FACE-19; CG COG-FACE-25; SA SAU-FACE-10 |
| **Population-sample** | n per population compared as distributions; for statistically defined identities | SG L356; FN L349 |

## 2. The seven tiers

### A. Intra-population validity

**Question:** is the face biologically valid for its own population?

**Validators:**
- the race envelope and the race's named invalid combinations;
- anti-juvenile ceilings and floors;
- family-identity validators (ears);
- display limits;
- the FPI floor.

**Carried forward:**

| Race | Tests |
|---|---|
| MF | Face test L248 |
| SK | SK-01, SK-10, SK-12 |
| SG | SG-12, SG-14 |
| FN | FN-18…26, FN-32…34, FN-38 |
| AE | AE-25…33, AE-36, AE-39…41, AE-43, AE-49…50 |
| VA | VL-25…36, VL-40…43, VL-59…60 |
| HV | Core validation L64; HV-05, HV-06, HV-26…35 |
| DU | DU-FACE-01…11; no single-feature dependency (L252) |
| GR | GR-FACE-01…13; GR-EAR-01…04; soft- and severe-feature tests (L420–421) |
| GO | GOR-FACE-01…15; GOR-EAR-01…06; soft-feature and attractiveness tests (L399–400) |
| PK | PIP-FACE-01…16 |
| CG | COG-FACE-01…15, 22, 24; relationship rejections (§101) |
| SA | SAU-FACE-01…09, 16–18, 23; SAU-SURF-04, 12–14, 25–26, 28; SAU-CC-08, 12, 16, 19, 28 |

### B. Cross-population boundary validity

**Question:** under N3/N4, at equal-height and/or matched-scale, does the face collapse into another population?

**Universal rule (proposed):** every pair of races in §3 is run through a **generic pairwise harness** at N4 matched-scale. Race-specific boundary tests stay authoritative where they exist. The harness fills gaps so that no pair goes untested (AD-U10).

**Carried forward:**

| Race | Tests |
|---|---|
| MF | (comparator for all) |
| SK | SK-02; silhouette L284; 190 cm L288; GR/GO relations (L296–298) |
| SG | SG-10 (ambiguity accepted); large-sample L356; elf boundary L461 (FN-17, AE-21) |
| FN | FN-10, FN-27, FN-37; hidden-ear population L349 |
| AE | AE-34, 35, 45, 46; hidden-ear population L472; Sagekin boundary L478 |
| VA | VL-14, VL-37…39, VL-51…53; human boundary L515 |
| Elves (ECR) | Three-elf neutral face L122; ear-only L123; human boundary L124 |
| HV | HV-01, HV-02; source neutralization L379; source-passing L145; ear-only L219 |
| DU | Equal-height face L221; Pipkin/Cogling comparisons L259 |
| GR | L422–427, L463–465, L598, L703–707 |
| GO | L401–404, L460–467, L475–479, L545–546, L682; AD-1 L271 |
| PK | PIP-FACE-17…21; PIP-INT-04; stresses L452–453 |
| CG | COG-FACE-16…20, 25; §204 anti-convergence |
| SA | SAU-FACE-02, 10–15; rostral non-overlap (FPI floor; cross-race numeric closure DEFERRED, RM-CF-01…05) |

**Statistical identities.** SG, and to a degree FN/AE/VA, define identity at the **population** level. For these pairs, tier B runs as a population-sample test. Per-individual overlap is acceptable (SG L246; FN L211 "not every individual identifiable").

**Per-individual identities.** DU, GR, GO, PK, CG and SA define identity per individual. Their tier-B tests are per individual (for example DU-FACE-01 "must read immediately").

### C. Relationship validity

**Question:** do connected structures stay coherent?

**Validators:**
- the UFCA-03 dependency relations;
- seams: nose–philtrum–lip–jaw (SG L220); orbit–zygoma–maxilla–mandible junctions (CG L1128); brow → temporal/postorbital (SA L4172); ear-to-skull attachment (FN L337; AE L441–450; VA L482);
- Saurin rostrum × jaw × cranial support (§158);
- Halvren mosaic without patchwork (HV L41, L166).

**Carried forward:**

| Race | Tests |
|---|---|
| DU | Matched nose / brow / jaw; soft-tissue; cross-section (L308–315) |
| GR | Named invalid combinations (L406) |
| GO | Relationship-aware validity (L371); TSC under flat light (L555) |
| HV | Strong-expression stress (L221) |
| CG | COG-CC-10 |
| SA | SAU-CC-16; SAU-FACE-21 |

### D. Extreme-combination stress

**Question:** do individually valid extremes combine safely?

**Universal rule (proposed):** for every race, a generated stress set takes each Bound slot's DIR extremes in pairwise and triple combination with neighbouring slots. Every result must PASS or CONSTRAIN, or be correctly FAILed by a named rule. A combination that is neither caught nor coherent is a **validator gap**.

**Carried forward:**

| Race | Tests |
|---|---|
| PK | Combined stress L444–453 |
| CG | COG-FACE-23; §101 |
| GO | Maximum-caricature risk L685 |
| GR | L406 invalid combinations |
| HV | Extreme ear coupling L198 |
| SA | §246 (extremes and coupled combinations must pass); §247 validation populations |
| AE / VA | Extreme valid randomized (AE-50; FN-38; SK-12; SG-14) |

### E. Neutralization tests

**Question:** at N1–N4, does identity remain?

**Carried forward:**

| Race | Tests |
|---|---|
| SK | SK-11 |
| SG | SG-12, SG-13 |
| FN | Hidden-ear tests |
| AE | Cultural neutralization L484 |
| VA | Hidden-ear neutral-complexion L298; VL-58 |
| HV | Pigmentation / hair / source / culture neutralization L293–296, L379–380 |
| DU | Hidden-beard, hidden-ear, eye, clean character (L213–214, L404, L406); lighting L312 |
| GR | Hair / beard / ear neutralization L417–419; brown, green and grey skin recognition L551–553 |
| GO | Neutralized recognition L683; brown-skin and light-skin tests (L549, L582–583) |
| PK | PIP-SURF-16 |
| CG | COG-SURF-12, 13; COG-CC-12 |
| SA | SAU-FACE-16; SAU-SURF-19, 20, 25 |

**Rule:** no surface, hair, presentation or observation domain may compensate for a failed FD-STRUCT read (CG L1630, L2048; SA L1109; GR L431; DU L278).

### F. Age and asymmetry

**Question:** do age and asymmetry preserve identity without becoming caricature or pathology by default?

**Validators:**
- age is an OFFSET on the individual face;
- age never changes racial skeletal identity or depth classification (DU L377);
- age never adds ogre or troll growth (GO L527; GR L532);
- adults read adult at the youngest valid age (PK L385; CG §120; SA §127);
- asymmetry stays natural and is never deformity (HV L192; DU L191; CG L1528);
- natural asymmetry ≠ acquired injury (SA L2164).

**Carried forward:**

| Race | Tests |
|---|---|
| MF | Age L253 |
| SK | SK-09 |
| SG | SG-11 |
| FN | FN-23, FN-26 |
| AE | AE-30, AE-33, AE-43 |
| VA | VL-31, VL-34, VL-50 |
| HV | HV-10, HV-44…48 |
| DU | Age diversity L220; age neutralization L405 |
| GR | Age matrices L556–557 |
| GO | L551 |
| PK | PIP-FACE-02; PIP-SURF-09, 21; PIP-INT-16, 17 |
| CG | COG-FACE-02, 22; COG-SURF-08…11 |
| SA | SAU-FACE-20; SAU-CC-13, 14 |

**Sex sub-tier** (R-SEX; tested here because it is a systemic soft input):

| Race | Tests |
|---|---|
| DU | Sex stereotype L219 |
| PK | PIP-FACE-22/23 |
| CG | COG-FACE-21/21A |
| SA | SAU-FACE-19 |

### G. Preset and randomization

**Question:** can generated faces span the valid distribution without stereotype convergence?

**Validators:**
- UFCA-05 P-1…P-7;
- the batch diversity check (RM-UF-05 architecture FINAL CLOSED: D2 slot-balanced distance + per-slot coverage + canon-bundle check; Option B is the current diagnostic calibration only; UFCA_V1 §17.1);
- the cliché-bundle checks.

**Carried forward:**

| Race | Tests |
|---|---|
| MF | Identity stress L253; randomization sample L261 |
| SK | Anti-stereotype validation L294–296 (lean, heavy, elderly, soft-featured, clean-shaven … Skarn read as the same population); relationship-aware randomization L282–284; SK-12; the six permanent W3C overlap validators (`reviews/claude-rac-w3c-skarn-craniofacial-gate.md` §5); C1R central face is the reference state, never a mandatory template |
| SG | Clone / stereotype L370 |
| FN | FN-34, final gate population randomization |
| AE | Generic-elf convergence L479; AE-48 |
| VA | Cliché convergence L505; VL-55 |
| HV | Anti-generic-half-elf L223; anti-beauty L222; anti-50/50 (L60, L381); HV-FAMILY-01/02 |
| DU | Population sampling L233 |
| GR | Biological diversity L740; anti-caricature L739 |
| GO | Minimum-stereotype L713; biological diversity L716 |
| PK | PIP-INT-15 |
| CG | COG-SURF-14; COG-CC-04, 06 |
| SA | SAU-CC-01, 03, 05, 17, 18, 24, 25, 26 |

## 3. Pairwise boundary coverage (tier B)

**Key:**
- **●** an explicit face or craniofacial boundary test exists in canon;
- **◐** only partial coverage (ears only, body only, population-level, or comparison text without a test);
- **○** no test.

Derived from `reviews/ufca-evidence/`. Under the proposed generic harness, every ○ and ◐ pair gets the N4 matched-scale test.

|  | SK | SG | FN | AE | VA | HV | DU | GR | GO | PK | CG | SA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **MF** | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| **SK** | | ◐ | ◐ | ◐ | ◐ | ● | ◐ | ● | ● | ○ | ○ | ◐ |
| **SG** | | | ● | ● | ● | ● | ◐ | ○ | ● | ○ | ● | ○ |
| **FN** | | | | ● | ● | ● | ◐ | ● | ● | ● | ● | ● |
| **AE** | | | | | ● | ● | ◐ | ● | ● | ◐ | ◐ | ● |
| **VA** | | | | | | ● | ◐ | ● | ● | ◐ | ◐ | ● |
| **HV** | | | | | | | ○ | ○ | ○ | ○ | ○ | ○ |
| **DU** | | | | | | | | ◐ | ● | ● | ● | ● |
| **GR** | | | | | | | | | ● | ○ | ◐ | ● |
| **GO** | | | | | | | | | | ● | ◐ | ● |
| **PK** | | | | | | | | | | | ● | ● |
| **CG** | | | | | | | | | | | | ● |

### Gaps (○)

| Pair | Assessment | Measurement link |
|---|---|---|
| SK–PK, SK–CG | Low risk: human skeletal family vs IMFA / FSPI anti-juvenile adult architectures. Harness only | — |
| SG–GR | Low risk: GR multiregional verticality and ear family vs human auricle. Harness only | — |
| SG–PK | Low risk; harness only | — |
| SG–SA | Already logged as Pass 2 F-25 | RM-OT-04 |
| HV–DU, HV–GR, HV–GO, HV–PK, HV–CG | Not source populations; collapse risk is low. Harness only | RM-OT-03 sample can include them |
| HV–SA | Already logged as Pass 2 F-25 | RM-OT-04 |

### Partial coverage (◐)

| Pair | What exists |
|---|---|
| SK–SG | Large-sample population test |
| SK with elves | Body tests plus comparator text |
| DU with elves and DU–GR | DU L501 body; GR L431 contrast text; "no equal-height" (GR L710) |
| AE/VA vs PK/CG; GR–CG; GO–CG | Ear comparisons and IMFA / anti-convergence text only |

**No ○ or ◐ pair suggests a contradiction.** These are coverage gaps, not identity conflicts.

## 4. Measurement-deferred validators

Following order §11, each validator that will need a number is defined now. Its bounds stay deferred.

| Validator | Semantic variable | Landmarks / index (r3) | Exposure | Number from |
|---|---|---|---|---|
| Saurin rostral floor (cross-race) | Rostral projection relative to head length | FPI | VAL + DIAG | RM-CF-01…05. **Provisional floor 0.255 stays protective canon; no margin set** — *closure status (October 10, 2026): RM-CF-05 FINAL CLOSED, margin 0.05 r3 FPI, floor unchanged, collision = author review (SAURIN_V1 §268)* |
| Grask verticality | Multiregional facial vertical contribution | FVB **with** MVI | VAL | RM-CF-07 |
| Durrim depth | Craniofacial depth relative to facial height, domains A–E | FDH (regional variants) | VAL + DIAG | RM-SR-05 |
| Durrim / Gorrund cranial breadth | Cranial breadth relative to height | CBH | VAL | RM-CF-06 |
| Gorrund TSC | Transverse coherence of lateral brow/orbit, zygoma, posterior mandible | TBP | VAL + DIAG | RM-CF-06 |
| Anti-juvenile (PK, CG) | Head share; face-to-vault; aperture vs orbit | HSR, FVI, ORB | VAL | RM-SR-04 |
| Elf orbit presentation | Orbit vs visible aperture | ORB, IOD, aperture | VAL + DIAG | RM-CF-08 |
| Skarn tendencies | Skull size, brow, jaw mass, midface vs MF | various | DIAG | RM-CF-09 |
| Head-to-stature (GR, GO, PK, CG) | Head height / length vs stature | HSR | VAL (DIR for SA only) | RM-CF-10 |
| Halvren source passing | Whole-face distance to each source distribution | composite | VAL | RM-OT-03 |
| Saurin vs SG / HV | Face boundary | composite | VAL | RM-OT-04 |
| **Proposed RM-UF-01** | Per-race visible-aperture distribution vs orbit (non-elf races) | ORB vs aperture | VAL | Proposed (UFCA-07) |
| **Proposed RM-UF-02** | Ear-family parameter envelopes, incl. GR length and GO projection ranges (both OPEN) | Ear landmarks (not in r3) | VAL | Proposed; needs authored ranges first |
| **Proposed RM-UF-03** | Saurin orbital spacing tolerance | IOD | VAL | Proposed (§259 L4183 OPEN) |
| **Proposed RM-UF-04** | Saurin structural-ridge strength and facial scale-field ranges | — | VAL | Proposed (§36a L671; §262) |
| **Proposed RM-UF-05** | Batch diversity / anti-convergence threshold | Distance over DIR vectors | VAL | Proposed — *status (October 10, 2026): architecture FINAL CLOSED (UFCA_V1 §17.1); roster-wide numeric calibration PARTIAL / DEFERRED* |

## 5. What is deliberately not set

- No numeric facial envelope for any race.
- No FPI margin (RM-CF-05). *Closure status (October 10, 2026): RM-CF-05 FINAL CLOSED at 0.05 r3 FPI (VAL / DIAG; SAURIN_V1 §268).*
- No diversity threshold.
- No asymmetry magnitude limits (SA L2724 OPEN).
- No head-to-stature ratios for GR, GO, PK or CG.

— Claude

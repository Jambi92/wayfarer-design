# UFCA-08: Phase 1 Architecture Audit

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ufca-phase1-order.md` §12 (audit questions), §13, §14
**Deliverables audited:**

| ID | File |
|---|---|
| UFCA-01 | `claude-ufca-01-requirements-matrix.md` (+ `ufca-evidence/`) |
| UFCA-02 | `claude-ufca-02-navigation-hierarchy.md` |
| UFCA-03 | `claude-ufca-03-control-taxonomy-dependency.md` |
| UFCA-04 | `claude-ufca-04-exception-map.md` |
| UFCA-05 | `claude-ufca-05-presets-randomization.md` |
| UFCA-06 | `claude-ufca-06-validation-framework.md` |
| UFCA-07 | `claude-ufca-07-open-deferred-decision-register.md` |

## 1. Stop-condition check (order §14)

| Stop condition | Result |
|---|---|
| Two approved race requirements genuinely incompatible with one architecture | **No.** The sharpest tensions are resolved by bindings, not by changing anatomy: (1) Saurin orbit-coupled vs everyone else's orbit ≠ aperture (race-specific FOLLOW); (2) Saurin display in the Hair slot vs a "Race-Specific Cranial Structures" category (proposed: follow Saurin's permitted routing, AD-U1); (3) Halvren genealogy vs "no ancestry slider" (A / B / C separation) |
| A decision would materially change approved race biology | **No.** No UFCA proposal alters a tendency, bound, identity statement or OPEN item. Every renaming is a navigation label |
| An OPEN biological question must be answered first | **No.** Every OPEN item is held unexposed or at authored central values (UFCA-07 §4). The architecture works with them open |

Phase 1 therefore ran to completion.

## 2. Audit questions (order §12)

### Q1. Does every approved facial requirement from all 13 specs have a home?

**Yes.** Each UFCA-01 row maps to one of:
- a slot binding (UFCA-02 §6);
- a variable class (UFCA-03 §2);
- a validator tier (UFCA-06 §2);
- an explicit out-of-face home (UFCA-02 §5).

Locked tests are all assigned to tiers A–G (UFCA-06). Appendix A gives each Pass 1 control item its home.

**Residual:** the AD-U12 / AC-U3 coverage items (UFCA-07 §3). These are homes waiting on confirmation, not missing homes.

### Q2. Did any universalization weaken a race's positive identity?

**No.** Identity carriers are untouched and enforced as race validators. They were not universalized into shared axes:

| Race | Carrier kept as a race validator |
|---|---|
| Saurin | Layered Rostral-Cranial Integration, FPI floor, orbit coupling, vertical pupil, recessed openings, display family |
| Durrim | Depth relative to facial height |
| Grask | Multiregional verticality and ear family |
| Gorrund | TSC and ear family |
| Pipkin | IMFA |
| Cogling | FSPI |
| Halvren | Coherent mixed space with source protection |
| Elves | ECR tendencies |
| Sagekin | Statistical identity |
| Skarn | Robust tendencies |

UFCA-04 §4 lists what was deliberately **not** generalized.

**Risk to watch:** a shared variable set (slots 2–8) could pull every race toward a common mesh in implementation. The ECR "no single Elf Head unless proven" constraint (ECR L77) and the technical-OPEN status are carried as implementation guards.

### Q3. Did any provisional Pass 1 requirement disappear without an explicit disposition?

**No.** Appendix A lists every Pass 1 facial control item for all 13 races with its disposition. Items reinterpreted rather than mapped directly are flagged for confirmation:

| Item | Flag |
|---|---|
| "Eye size" | AC-U1 |
| Cogling "sex-related anatomy" | AC-U2 |
| Saurin "orbital spacing" | Locked by §259; no decision needed |
| Saurin §36a variation list | Mapped |
| Halvren "overall facial relationships" | Slot 1; tools AD-U3 |

### Q4. Did any OPEN item get silently resolved?

**No.** UFCA-07 §4 lists every facial OPEN item from UFCA-01 §24 with its handling. Specifically:

| Item | Status after UFCA |
|---|---|
| Low-light | Not exposed |
| Pupil morphology | Not exposed (Saurin's is canon, not OPEN) |
| Prognathism | Central values only |
| Tusks | Excluded |
| Ear mobility | Not exposed |
| Sex magnitude | "No shift" default; nothing authored |
| Head-to-stature | VAL / DIAG |
| Scleral tint | Humanoid default |
| Saurin membrane details | Locked |
| Frequencies | Interim only |
| Lifecycle | Not mapped |

**Items that are canon, not OPEN:** Naturalize Face, randomization strength and frequency tiers were "proposed universal" in canon. They are listed as author decisions (AD-U7, AD-U8, AD-U9), not adopted.

### Q5. Did any diagnostic measurement become a creator control without justification?

**No.** Firewall F-1 (UFCA-03 §1) and the explicit non-slider list (UFCA-03 §4) keep these diagnostic or validator-only:
- all r3 indices;
- FD domains;
- Durrim depth domains;
- GR / GOR / DU variation diagnostics;
- TSC;
- FPI.

The one numeric-ratio control that *is* exposed is **Saurin head scale (±8 %)**, and that is a canon control (SA §73, §258). Non-Saurin head share stays VAL / DIAG (AD-U4).

### Q6. Did any creator control become a hidden ancestry, culture, personality or gameplay control?

**No.**

| Concern | How the architecture handles it |
|---|---|
| Ancestry | Genealogy is outside the face tree (UFCA-02 §5; HV L463). Halvren phenotype uses ordinary controls inside B. Preset tags never assert genealogy (P-5) |
| Culture | Culture lives in Presentation only; presentation randomization never rewrites anatomy (UFCA-05 §2 step 6) |
| Personality | Expression is preview / animation only. Canon bans on personality-in-anatomy carry forward as tier-A validators: HV L181; CG L1478–1484; SA §46; VA "never sinister"; AE "never aloof"; FN "never startled" |
| Gameplay | No control carries stats (SA §161A, §237; SAU-GAME-04). Low-light is unexposed |
| Sex | SOFT only (R-SEX); Saurin none |
| Global hidden state | Rule G-1: only Apparent Biological Age, soft-tissue offset, Saurin head scale and asymmetry offsets are stored systemic values |

### Q7. Can Simple Mode and Advanced Mode both use this architecture?

**Yes.**
- **Simple Mode** is slot 0 (preset; optional whole-face shuffle using the same generator).
- **Advanced Mode** is the full tree, split into Quick and Detailed controls.
- Both read and write one appearance record (UFCA-02 §4).
- Halvren Simple Mode needs no genetics (HV L58).

### Q8. Can presets and randomization be represented as valid system outputs?

**Yes.**

| Requirement | Where |
|---|---|
| Presets are DIR records that pass the same validators | UFCA-05 P-1…P-7 |
| Generation samples drivers → dependents → validators, never repair | UFCA-05 §2 |
| Seeds reproduce generation events; DIR values are what is saved | UFCA-05 §6 |
| NPC parity | UFCA-05 §7 |

### Q9. Are Halvren and Saurin fully supported without forcing them into human topology?

**Yes.**

**Halvren** (UFCA-04 §2.3):
- A / B / C separation;
- inheritance clusters as LAT;
- union-set mixed ears with coupled validators;
- whole-face source protection;
- no percentages;
- non-50/50 generation.

**Saurin** (UFCA-04 §2.9):
- five renamed bindings (Rostrum & Lateral Face, Nasal Openings, Mouth Line, Jaw, Auricular Openings);
- chin, lips, zygoma, forehead and facial hair Absent (hidden, never dead controls);
- display in the Hair slot (proposed, consistent with SA L604, L2445);
- structural ridge in Cranium;
- orbit coupling;
- species ocular anatomy;
- field-aware scales;
- no sex shift;
- §264 generation.

No nasal pyramid, lip, chin or pinna variable is exposed for Saurin.

### Q10. Are any author decisions required before the architecture can be canonicalized?

**Yes.** These need author action before Phase 2:
- AD-U1…AD-U12;
- AC-U1…AC-U4;
- the per-item coverage list under AD-U12 (UFCA-07 §3).

None is a contradiction. All are proposals or confirmations.

## 3. Self-audit of the process

| Check | Result |
|---|---|
| Race specs, PROJECT_RULES, STATUS, the register and other canon unchanged | ✔ Only new review files were added |
| No numbers invented | ✔ Every number quoted is canon (Saurin §258–§260; Cogling 11–13 cm). The RM-UF items define semantics only |
| Saurin provisional rostral floor preserved as protective canon; no margin set | ✔ |
| No UE5, rigging, implementation or Phase 2 canonicalization begun | ✔ |
| Evidence traceable | ✔ The `ufca-evidence/` extractions cite spec lines; independent spot-check in §4 |

## 4. Independent spot-check

**Method.** A separate agent that had not written these files checked six things:
1. about 110 UFCA-01 cells against the specs (all 13 races, weighted toward SA, CG, PK, DU, HV, GR and GO);
2. every number in UFCA-01…07;
3. the OPEN-item coverage;
4. the Pass 1 dispositions;
5. canon files unchanged;
6. overreach.

Claude then verified each of its findings against the specs before acting on it.

### Results

| Check | Result |
|---|---|
| UFCA-01 citations | ~99 PASS, 0 FAIL, 9 IMPRECISE. All 9 corrected (below) |
| Numbers | Every number appears in canon (Saurin L4162, L4174, L4177, L4179–4180, L4191–4194; Cogling L1581; SK L288; MF L307; DU L145; HV L357). None invented |
| Pass 1 dispositions (Q3) | Every item present in Appendix A: SA §73 31/31; SA §36a 6/6; CG 24/24; PK 15/15; all SK, SG and HV items. **PASS** |
| Canon unchanged | `git diff` empty for specs/, decisions/, register/, rules/. **PASS** |
| OPEN items (Q4) | No OPEN item exposed or resolved in UFCA-02…06. **PASS.** Coverage gaps were added (below) |

**Corrections applied:**

| Location | Correction |
|---|---|
| UFCA-01 §0 (Cogling status) | Cogling never states the APPROVED FIRST-PASS / PROVISIONAL label verbatim. The cell now cites L1536–1538 and L1564 ("does not finalize… may be reorganized") |
| UFCA-01 §6 (Saurin canthal transition) | L679 → L680 |
| UFCA-01 §10 (Saurin floor) | "Protective canon" is attributed to the Pass 2 closure and this order; the spec says "provisional Saurin floor" (L4177) |
| UFCA-01 §16 (Saurin display) | Clearance "≈ 7 cm" → "≥ ~7 cm". Hair-slot routing reworded to canon's permissive "may present" (L2445), plus L604 |
| UFCA-01 §2 (Cogling head size) | 11–13 cm now cites L1581 |
| UFCA-01 §2 (Durrim head) | Now quotes "never an oversized fantasy-dwarf head" (L21) |
| UFCA-01 §14 / §24 (Durrim ears) | Ear-size distributions are "future work", not OPEN |
| UFCA-01 §17 (Durrim) | Restored "never faked **mainly** through…" (L278) |
| UFCA-01 §7 / §24 (Grask eyes) | Scleral tint is "comes later" (L524), not OPEN. No nictitating membrane "without approval" (L528) |
| UFCA-01 §24 | Added: CG exact craniofacial distributions and facial-animation implementation (§103, §207); SA displays beyond validated families, crests above ~2.5 cm and the cross-race rostral check; GO/GR facial flushing; face technical architecture. UFCA-07 §4 updated to match, including "Universal facial-control architecture" as this phase's own OPEN subject |
| Overreach 1 (UFCA-02) | The Hair → Cranial Display routing and the dissolution of a "Race-Specific Cranial Structures" slot are now labelled proposals (AD-U1) consistent with canon, not canon-mandated |
| Overreach 2 (UFCA-03) | Durrim sclera was listed as DIR without a named control dimension. Now hidden pending AD-U12 §3.2 (UFCA-07 §3.2 updated) |
| UFCA-07 N-2 | Durrim wording kept (L302 does say "about 150 cm"); L72 "about 150–152 cm" added for context |

**Auditor findings checked and rejected:**

| Finding | Why it was rejected |
|---|---|
| "HV L60 and L377 do not mention 50/50" | Both lines do: L60 "repeated exact 50/50 averages"; L377 "exact 50/50 anatomy". Citations kept |
| "DU L302 has no 150 cm" | L302 reads "about 150 cm Durrim against about 150 cm Marchfolk". Citation kept |

**Result:** no blocking fault remains.

## 5. Phase 1 result

**UFCA Phase 1 COMPLETE. Returned for ChatGPT author review.**

There is no stop-condition blocker. The decisions required before canonicalization are in UFCA-07: AD-U1…12, AC-U1…4 and the AD-U12 coverage items.

**STOP.** Phase 2 canonicalization and UE5 implementation are not begun.

— Claude

---

## Appendix A: Disposition of every Pass 1 facial control item

**Class codes** (UFCA-03): DIR, DER, SOFT, VAL, LAT, PRES, DIAG. "→ n" means navigation slot n (UFCA-02).

### Marchfolk (L106–120, L164–177)

| Pass 1 item | Disposition |
|---|---|
| Face presets / Quick / Detailed levels | → Slot 0 / Advanced Quick / Detailed (one record) |
| Head and skull | → 2 DIR |
| Brow and eyes | → 3 (brow, orbit) + 4a (aperture, lids) |
| Nose | → 6 DIR |
| Cheeks | → 5 DIR / SOFT |
| Jaw and chin | → 8 DIR |
| Mouth and lips | → 7 DIR |
| Ears | → 9 human-auricle family DIR |
| Asymmetry pairs (brow height, eye opening, cheek fullness, mouth corner, ear projection, jaw contour) | → 13 DIR offsets |
| Restore Symmetry | → 13 operation |
| Facial hair style / length / density / colour (linked or unlinked) | Density and natural colour → 11 DIR; style and length → 15 PRES; colour link → 11/15 |
| Hair (style, length, texture, colour, hairline, density, parting, accessories) | Texture, hairline, density, natural colour → 10 DIR; style, length, parting, accessories → 15 PRES |
| Player-experience features (before/after, undo/redo, lighting / expression previews, views, zoom) | → 15 preview tools (not stored) |

### Skarn (L158–183, L220–224)

| Pass 1 item | Disposition |
|---|---|
| Head width / depth / length; cranial height; temple width | → 2 DIR |
| Forehead height and slope | → 2 DIR |
| Face length | → **Not a single control.** Realized through regional vertical controls (2, 5, 8). A face-length scalar is a whole-face scalar (G-3). Capability kept; organization changed |
| Brow prominence / shape / height | → 3 DIR |
| Eye depth, spacing | → 3 DIR |
| Eye size | → AC-U1 split |
| Eye angle; upper / lower lid shape; lid opening | → 4a DIR |
| Bridge height / width, length, projection, tip width / rotation, nostril width / shape | → 6 DIR |
| Cheekbone width / height / projection; fullness | → 5 DIR / SOFT |
| Jaw width / angle / depth; chin width / height / projection | → 8 DIR |
| Mouth and lips (named region; no row) | → 7 (AD-U12 §3.1) |
| Ears (named region; no row) | → 9 human auricle (AC-4) |
| Asymmetry + Restore | → 13 |
| Naturalize Face (proposed) | → 13, AD-U9 |
| Facial hair (style, length, density, colour, graying) | → 11 DIR (biology) / 15 PRES (style) |
| Body-to-face soft tissue | → 1 SOFT + offset |

### Sagekin (L213–220, L238, L277)

| Pass 1 item | Disposition |
|---|---|
| Head width / depth, cranial height, forehead height / slope, temple width | → 2 DIR |
| Face length | → as Skarn (regional) |
| Eye depth, spacing, brow-to-eye distance, brow prominence | → 3 DIR |
| Eye size | → AC-U1 |
| Corner positions, angle, upper / lower lid structure | → 4a DIR |
| Bridge height / width / contour, length, projection, tip width / shape / rotation, nostril width / shape, alar flare (independent) | → 6 DIR |
| Cheekbone height / width, cheek projection, mid-face depth, fullness | → 5 DIR / SOFT |
| Jaw width / angle, mandibular depth, chin width / height / projection | → 8 DIR |
| Mouth width, lip fullness, Cupid's bow, lip projection, corner position, philtrum length / depth | → 7 DIR |
| Asymmetry, Restore, Naturalize Face (proposed) | → 13 (AD-U9) |
| Facial hair independent | → 11 / 15 |
| Ears (no row; AC-4) | → 9 human auricle (AD-U12 §3.1) |

### Fenn (L169–187)

| Pass 1 item | Disposition |
|---|---|
| Eyes and orbits: size, spacing, depth, angle | → 3 DIR (size → AC-U1) |
| Opening, lids | → 4a DIR |
| Brow-to-eye distance, brow structure | → 3 DIR |
| Cheeks / mid-face (broad↔narrow, high↔low, projection, full↔hollow, soft↔angular) | → 5 DIR / SOFT. "Soft ↔ angular" is a combined descriptor, realized through zygomatic projection + soft tissue; not a separate scalar |
| Nose: length, width, bridge height / width, profile curve, projection, tip structure / rotation, nostril width, alar structure | → 6 DIR |
| Jaw (narrow↔broad, angular↔rounded, strong↔subtle); all chins | → 8 DIR (descriptors realized by breadth, gonial angle, body depth) |
| Mouth: width, fullness, projection, Cupid's bow, philtrum, corners, natural asymmetry | → 7 DIR; asymmetry → 13 |
| Ears: overall length, base width, tip length / sharpness, vertical angle, sweep, projection, upper curvature, lobe size / attachment | → 9 elven family DIR |
| Ear asymmetry (height, angle, projection, minor shape) + Restore | → 13 |

### Aelari (L210–231)

| Pass 1 item | Disposition |
|---|---|
| Forehead height / slope, temple width | → 2 DIR |
| Brow height / shape / prominence | → 3 DIR |
| Eyes: size, depth, spacing, angle, brow-to-eye | → 3 DIR (size → AC-U1) |
| Lids, opening | → 4a DIR |
| Cheeks and mid-face descriptors | → 5 (as Fenn) |
| Nose: short / long, narrow / broad, bridge height, profile (straight / convex / concave), projection, tip, nostrils, alar | → 6 DIR |
| Jaw and chin descriptors; all chins | → 8 |
| Mouth list | → 7 |
| Ears list + asymmetry + Restore | → 9 / 13 |

### Vael (L239–294)

| Pass 1 item | Disposition |
|---|---|
| Narrow / balanced / broad faces | → Realized through regional breadths (2, 5, 8); no face-width scalar (G-3) |
| Forehead height / width / slope, temple width | → 2 DIR |
| Brow height / shape / prominence | → 3 DIR |
| Eye size | → AC-U1 |
| Opening, depth, spacing, angle, lids, brow-to-eye | → 3 / 4a DIR |
| Cheeks descriptors | → 5 |
| Nose (length, width, bridge, profile, projection, tip, nostrils, alar) | → 6 |
| All jaw and chin variation | → 8 |
| Mouth list | → 7 |
| Ears list (incl. lateral projection) | → 9 elven |
| Full asymmetry list (brow height, eye height / opening, cheek position / fullness, nose deviation, mouth corner, jaw / chin, ears) + Restore + Naturalize (proposed) | → 13 (AD-U9) |
| Creator lighting options | → 15 preview |

### Halvren (L227)

| Pass 1 item | Disposition |
|---|---|
| Face preset | → 0 (ancestry-informed; no genealogy assertion) |
| Overall facial relationships | → 1 (soft tissue). Relationship tools under AD-U3 |
| Brow and orbit | → 3 |
| Eyes | → 4a / 4b (four separate systems honoured: brow 3, orbit 3, external 4a, ocular 4b) |
| Cheeks and midface | → 5 |
| Nose | → 6 |
| Mouth | → 7 |
| Jaw and chin | → 8 |
| Ears | → 9 mixed coupled family |
| Asymmetry | → 13 |
| "Ancestry-aware constraints underneath" | → VAL envelope B |
| Forbidden items (Elf %, lifespan %, skull slider, pointiness, single eye control, one ancestry slider) | Remain forbidden (G-3, G-4) |

### Durrim (L234, L259)

| Pass 1 item | Disposition |
|---|---|
| No controls defined | Binds the shared regional DIR variables, because its anatomy states the variation (AD-U12 §3.1) |
| "Likely future domains" (cranium, forehead and brow, orbits and eyes, midface, cheeks, nose, mouth and lips, mandible and chin, ears, soft tissue, asymmetry) | All present as slots 1–13 |
| Multidimensionality bans (Face Width, Nose Size, Ear Size, Face Depth, five depth sliders) | Honoured (G-3; F-1) |

### Grask (L406) and Gorrund (L369–371)

| Pass 1 coverage item | Disposition |
|---|---|
| Cranium; GO cranial breadth and depth | → 2 |
| Forehead | → 2 |
| Brow; orbits; eye spacing | → 3 |
| GO zygomatic breadth / projection; GR zygomatic region | → 5 |
| Midface; GO midface depth and vertical contribution | → 5 (projection range held: OPEN) |
| Nose | → 6 |
| Mouth | → 7 |
| Mandible; chin | → 8 |
| Ears | → 9 (GR folded late-taper; GO deep-bowl) |
| Soft tissue / GO "biological facial soft tissue" | → 1 / 5 SOFT |
| Asymmetry | → 13 |
| Named invalid combinations (GR L406; GO L371) | → VAL tier C / D |
| Banned controls (Trollness, Ogre-ness, etc.; TSC / ALPC sliders) | Remain banned |

### Pipkin (L395–410)

| Pass 1 control family | Disposition |
|---|---|
| Cranial breadth / length / vault height | → 2 |
| Forehead height / slope | → 2 |
| Brow and orbital dimensions | → 3 |
| Interorbital spacing | → 3 |
| Visible eye aperture | → 4a (anti-enlargement CLAMP) |
| Zygomatic breadth / projection / height | → 5 |
| Temporal breadth | → 2 |
| Midface height / projection | → 5 |
| Nasal root / bridge / length / projection / alar | → 6 |
| Maxillary projection | → 5 |
| Mouth / lip / philtrum | → 7 |
| Mandibular breadth / ramus / body depth | → 8 |
| Chin width / height / projection | → 8 |
| Ear height / breadth / projection / rotation / fold architecture | → 9 compact-rounded family |
| Soft-tissue facial composition | → 1 SOFT + offset |
| Creator camera framing | → 15 |

### Cogling (§97 L1539–1562)

| Pass 1 capability | Disposition |
|---|---|
| Cranial length / breadth / height | → 2 |
| Forehead contour | → 2 |
| Brow / supraorbital | → 3 |
| Orbital dimensions and spacing | → 3 |
| Visible eye-opening dimensions | → 4a (cannot be enlarged) |
| Eyelid relationships | → 4a |
| Zygomatic breadth / projection | → 5 |
| Cheek soft tissue | → 5 SOFT |
| Midface height / projection | → 5 |
| Maxillary projection | → 5 |
| Nasal root / bridge / tip / alar | → 6 |
| Mouth width | → 7 |
| Lip relationships | → 7 |
| Philtrum | → 7 |
| Mandibular breadth / depth | → 8 |
| Ramus / gonial | → 8 |
| Chin | → 8 |
| Lower-face height | → 8 |
| Ear size / placement / projection | → 9 fine-folded family |
| Ear fold architecture | → 9 |
| Facial adipose distribution | → 1 SOFT + offset |
| Sex-related anatomy | → AC-U2 (SOFT; no face control) |
| Age-related anatomy | → 14 |
| Asymmetry | → 13 |
| Creator camera (face / ear close-ups) | → 15 |

### Saurin (§73 L1174–1215; §36a L716; §149; §150; §147–148)

| Pass 1 item | Disposition |
|---|---|
| Overall head scale | → 1 DIR (±8 %) |
| Vault height, cranial length, posterior cranial depth, temporal breadth | → 2 DIR |
| Structural-ridge prominence, transition strength, temporal definition, posterior contour | → 2 DIR (non-zero floor) |
| Rostral length, base width, anterior width, depth, dorsal contour, rostrum-to-orbit transition | → 5 "Rostrum & Lateral Face" DIR + VAL |
| Orbital size | → 3 DIR driver (FOLLOW coupling) |
| Orbital depth | → 3 DIR |
| Orbital-platform breadth, orbital rim | → 3 DIR |
| **Orbital spacing** | → 3 **Bound-locked** (§259 L4183) |
| Visible eye-opening width / height, eye-opening angle | → 4a DIR inside the coupling |
| Iris pigmentation / detail; pupil shape (vertical) and dilation range; ocular-tissue visibility | → 4b DIR |
| Dilation preview | → 15 preview |
| Posterior jaw depth, mandibular-body depth, jaw width, anterior taper, mandibular angle | → 8 "Jaw" DIR |
| Mouth-line length, mouth-corner position | → 7 "Mouth Line" DIR |
| Nasal opening size, spacing, orientation, local contour | → 6 "Nasal Openings" DIR |
| Auricular opening size, recess depth, rim prominence, orientation | → 9 recessed family DIR |
| Cranial Display (family, count, attachment, spacing, base, length, thickness, taper, sweep, curvature, orientation, symmetry, crest, plates, surface, natural keratin coloration, inherited arrangement); §102 L1696–1714 / §150 L2447–2462 | → 10 DIR + §260 VAL |
| Facial fine-scale expression; facial pattern | → 12 DIR per field |
| Lock groups (head, rostrum, eyes, keratin display) | → UFCA-05 §3 |

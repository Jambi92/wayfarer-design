# RAC-01: Master OPEN-to-Dependency Matrix

**Author:** Claude (auditor / biological-resolution agent)
**Order:** `reviews/chatgpt-reference-anatomy-closure-phase1-order.md` §3 (RAC-01)
**Status:** PROPOSAL / AUDIT for author review. **Nothing here closes an OPEN item in canon.**
**Evidence:** `reviews/rac-evidence/` (six extraction files, every quote line-checked at HEAD 218f64a). Spec line numbers below refer to that HEAD.

## 0. Keys

**Spec abbreviations:** MF Marchfolk, SK Skarn, SG Sagekin, FN Fenn, AE Aelari, VA Vael, HV Halvren, DU Durrim, GR Grask, GO Gorrund, PK Pipkin, CG Cogling, SA Saurin (`specs/<race>/<RACE>_V1.md`). UCCA = `decisions/UCCA_V1.md`; UFCA = `decisions/UFCA_V1.md`; RMQ = `reviews/claude-pass2-r5-reference-mesh-queue.md`; r3 = craniofacial framework; ECR = elf comparative review; SRR = short-race review.

**Class (order §2):**
- **A**: authorable now (qualitative or bounded) from existing canon, without invented measurement.
- **B**: direction lockable now; magnitude needs measurement.
- **C**: even a useful answer needs approved-mesh measurement.
- **D**: later biology, not needed to build or validate the reference body now.
- **E**: later system / gameplay / equipment.

A row may carry two classes (e.g. "A → C": the authorship step is A, the number is C). **No C, D or E item has been promoted to A to shorten the list.**

**Blocks:**
- **CM**: blocks building the central reference mesh;
- **XM**: blocks a creator-extreme reference mesh;
- **CV**: blocks a cross-race validator;
- **—**: blocks none of these.

**Phase:**
- **P2**: author decision on the RAC package (RAC Phase 2);
- **W1 / W2 / W3**: measurement waves (RAC-12 §4);
- **LB**: later biology;
- **LS**: later system / gameplay / equipment.

## 1. Body BIO OPEN items (UCCA §25)

| # | Item | Pop. | Canon source | Why OPEN | Class | Blocks | Prerequisite | Phase | Detail |
|---|---|---|---|---|---|---|---|---|---|
| B-01 | Pelvic morphology (breadth / depth / vertical height / organization) | All but SA (SA: sacral detail) | FN L111; AE L126; VA L124; HV L122; DU L32, L108; GR L208; GO L49, L189; PK L50, L152; CG L264, L691; SA L568–569 | Every spec defers exact shape to prototyping / later design | **B** (direction per race) → **C** (numbers) | XM, CV (not CM: central meshes can be built from the authored constraints) | RAC-03 directional statements; pelvic measurement item (proposed RM-UB-06) | P2, W1–W2 | RAC-03 |
| B-02 | Shared elven pelvis | FN, AE, VA | ECR L37 ("A plus E"); FN L111; AE L126; VA L124 | Shared non-human foundation locked; three shapes await prototype | **B → C** | CV; blocks HV pelvic inheritance | Elf references | W2 | RAC-03 |
| B-03 | Halvren pelvic inheritance | HV | HV L122, L437, L497 | Blocked on B-02 and the sex system; "Never invented inside Halvren" | **D** | — (central HV mesh uses the general envelope) | B-02 | LB | RAC-03 |
| B-04 | Segment ratios and numeric proportions | All | UCCA L355; RMQ RM-UB-01 | No race authors numbers; directions exist for 12/13 | **B → C** | CV, XM | Marchfolk baseline (B-25) | W1–W2 | RAC-04 |
| B-05 | Arm span: Grask | GR | GR L60, L166, L223, L726 | Ratio OPEN; direction locked (> MF, SK; > GO, GO L200) | **B** | CV | RM-LR-01 | W1 | RAC-04 |
| B-06 | Arm span: Pipkin | PK | PK L166, L1539 | Distribution OPEN; canon already says "unusual arm span isn't a Pipkin trait" | **A** (qualitative) → C | — | none | P2 | RAC-04 |
| B-07 | Pipkin trunk-share split (T-2) | PK | PK L137, L139, L166 | Split between limb and pelvic vertical contribution deferred; no winner may be invented | **C** (constraints A) | CV | RM-SR-01 / RM-UB-01 | W2 | RAC-04 |
| B-08 | Joint-scale / robusticity distributions | All | UCCA L355; DU L40; PK L68; CG L242, L755; FN L115; GO L76 | Directions exist; envelopes need meshes | **B → C** | XM, CV | RM-UB-03 / RM-LR-05 / RM-SR-03 | W1–W2 | RAC-05 |
| B-09 | Joint hard minimum where canon is silent | MF, SK, SG, HV, SA | UCCA L131 (minimums stay hard) | Only FN/AE/VA/DU state a minimum | **A** (qualitative rule) → C (values) | XM | none | P2 | RAC-05 |
| B-10 | Head-to-stature | All but SA | UCCA L77, L355; DU L21; PK L33, L205; CG L280, L736; GR L433; GO L299 | Directions for DU/PK/CG; bans only for GR/GO; silent elsewhere | DU/PK/CG **B**; GR/GO **C**; silent races **C** | CV (anti-juvenile) | RM-CF-10 / RM-SR-04 (+ Durrim scope, RAC-04) | W1 | RAC-04 |
| B-11 | Capacity distribution | GR, GO, PK, CG | GR L72; GO L82, L228; PK L72, L182; CG L318, L826; UCCA L164 | OPEN with no direction; downward inference banned (PK, CG) | **D** | — (central composition sits below any ceiling) | none | LB | RAC-06 |
| B-12 | Fat-distribution tendencies | All (SA: species depot order authored) | DU L135; GR L251; GO L228; PK L182; CG L869; SA L4172 | OPEN everywhere except the SA depot order | non-SA **D**; SA **B** | — (reference uses neutral distribution) | Reference-composition definition (B-26) | LB / W2 | RAC-06 |
| B-13 | Sex dimorphism magnitude | DU, GR, GO, PK, CG | DU L58; GR L76; GO L82; PK L1545; CG L352 | Magnitude OPEN (GR: even its class) | DU/GR/GO **D**; PK/CG **B** (regions named) → C | XM (female configuration), CV (like-for-like tests) | Author decision on default (RAC-07) | P2 / LB | RAC-07 |
| B-14 | Reproductive biology | All | PR L95; UCCA L177; SA L4244; CG L691 (inlet/outlet) | Out of creator scope; never inferred | **D** | — | none | LB | RAC-03, -07 |
| B-15 | Lifecycle | All | UCCA §15; MF L315; DU L520; GR L534; GO L531; PK L1485 | Lifespan, maturation, fertility, senescence OPEN | **D** | — (reference is adult) | none | LB | RAC-02 |
| B-16 | Body hair | DU, GR, GO (OPEN); MF, SK, SG, FN, AE, VA, HV (hidden) | DU L207; GR L402; GO L521; UCCA L195 | No biology authored | DU/GR/GO **A** (baseline) + D (distributions); silent races: author choice | — (reference meshes carry no body hair, N2) | none | P2 / LB | RAC-08 |
| B-17 | Skin thickness / durability | DU, GR, GO | DU L359; GR L512; GO L515 | Biology OPEN; any effect banned | thickness **D**; durability **E** (firewalled) | — | none | LB / LS | RAC-08 |
| B-18 | Halvren stature-tail limits and frequencies | HV | HV L481, L490; UCCA §22; RMQ RM-UB-05 | Biology first, then measurement | **A** (rules; contributor table conditional on the H-5 bounding decision) + **B** (asymmetry) → **C** (cm) | XM (HV-49/50 only) | RAC-09 authorship | P2 → W3 | RAC-09 |
| B-19 | Saurin balanced posture and density model | SA | SA L4162, L4263–4264 | Routed to posture/animation; density biological | **E** (+D density) | — | none | LS | RAC-10 |
| B-20 | Saurin caudal-base landmark | SA | SA L174, L4265 | Exact landmark not fixed; all §256 numbers use a diagnostic convention | **A** | CV (tail validators) | none | P2 | RAC-10 |
| B-21 | Saurin numeric lower-trunk minimum vs MF | SA | SA L96, L4267 | MF has no trunk number | **C** | CV | B-25 | W1 | RAC-10 |
| B-22 | Saurin numeric Broad-vs-Gorrund boundary | SA | SA L354, L4267 | Gorrund has no numeric ratios | **C** (interim qualitative rule A) | CV | GO reference | W2 | RAC-10 |
| B-23 | Saurin claw / digit ranges | SA | SA L4205, L4271 | Needs grip pose and equipment | **E** (+C) | — | none | LS | RAC-10 |
| B-24 | Saurin per-field scale ranges | SA | SA L4209, L4272 | Not geometrically validated | **C** | — | Body scale-field RM item | W3 | RAC-10 |
| B-25 | **Marchfolk baseline** (segments, pelvis, torso, neck, head share) | MF | MF L15, L75; RMQ L27 | MF is the comparator for most "than Marchfolk" statements but authors no numbers | **C** | **CV for most cross-race statements** | MF reference meshes | **W1 (first)** | RAC-04, -12 |
| B-26 | **Reference composition definition** ("moderate" / "reference composition") | GR, GO, PK, SA name it; others silent | GR L122; GO L129; PK L102; SA L4236 | Never defined in any spec or UCCA | **A** | **CM** | none | P2 | RAC-02, -06 |
| B-27 | **Measurement stance** (neutral pose for measurement) | All | SA L4162 (frozen stance ≠ final idle); DU L430 | No measurement pose is canon | **A** (method) | **CM** | none | P2 | RAC-02 |
| B-28 | **Female/second configuration soft-tissue anatomy** for races with OPEN sex magnitude | DU, GR, GO, PK, CG (and elves, HV by silence) | UCCA L135, L333; PK L224–225; CG L2949 | Validation requires configurations; canon authors no external sex-related soft tissue for these races | **D / creative** (see RAC-07 §4) | **CM** for the second-configuration ARMs of DU/GR/GO/PK/CG (PK and CG require both, PK L224–225, CG L2949); not for the one-configuration bootstrap | Author decision | P2 | RAC-07 |
| B-29 | Thermoregulation | SA | SA L2050, L4013 | Later biology; gameplay-firewalled | **D** | — | none | LB | RAC-10 |
| B-30 | Acquired major tail / rostral / jaw loss | SA | SA L209, L2326, L3559; UCCA L264 | Injury system | **E** (+D) | — | none | LS | RAC-10 |
| B-31 | Tail-equipment construction and coverage extent | SA | SA L1895, L4069; UCCA L149 | Equipment system; permission resolved | **E** (coverage ceiling could be B) | — | none | LS | RAC-10 |
| B-32 | Tail world-space validation | SA | SA L2738, L4274 | Precondition for final 55–80 % approval | **E** | — (blocks final tail envelope, not the reference) | World proxies | LS | RAC-10 |
| B-33 | Legacy racial gameplay traits | SK, FN, DU, GR, GO, PK, SA | UCCA §25 last line | Gameplay review | **E** | — | none | LS | — |

## 2. Craniofacial OPEN items that gate RM-CF / RM-UF (UFCA §19.1)

| # | Item | Pop. | Source | Class | Blocks | Prerequisite | Phase | Detail |
|---|---|---|---|---|---|---|---|---|
| F-01 | Grask projection distribution | GR | GR L362, L408 | **A** (envelope shape + named max-valid case); the central tendency is a **creative author decision** (canon gives no direction) | CV (RM-CF-03) | Author decision | P2 | RAC-11 |
| F-02 | Gorrund prognathism distribution | GO | GO L312, L371 | **A** (comparator + max-valid case) → B | CV (RM-CF-04) | Author decision | P2 | RAC-11 |
| F-03 | Marchfolk most-projecting valid face | MF | MF silent; r3 L120 | **A** | CV (RM-CF-02) | Author decision | P2 | RAC-11 |
| F-04 | Grask ear-length range | GR | GR L398, L734 | **B** | CV (RM-UF-02) | Ear landmarks (F-06) | P2 → W2 | RAC-11 |
| F-05 | Gorrund ear-projection range: **which variable** | GO | GO L350 vs L459–460 | **A** (name the variable) + B | CV (RM-UF-02) | Author decision | P2 | RAC-11 |
| F-06 | Ear landmarks (method) | All pinna families | r3 L54; RMQ L68 | **A** (method) | CV (RM-UF-02) | none | P2 | RAC-11 |
| F-07 | Fenn orbit terminology (F-20) | FN | FN L173; ECR | **A** (wording) | CV (RM-CF-08) | none | P2 | RAC-11 |
| F-08 | Tusk-like canines | GR, GO | GR L370; GO L320, L475 | **D** | — (excluded from projection landmarks, r3 L95) | none | LB | RAC-11 |
| F-09 | Ear mobility | Elves, HV, PK, CG | UFCA L377 | **D / E** | — (static envelopes do not need it) | none | LB / LS | RAC-11 |
| F-10 | "Authored central values" for GR/GO projection have no referent | GR, GO | GR L408; GO L371 | **A** (resolved by F-01/F-02) | **CM (GR/GO heads)**, CV | F-01, F-02 | P2 | RAC-11 |

## 3. Measurement-queue items (RMQ)

| ID | Measure (short) | Class of the measurement | Prerequisite authorship / input | Blocks | Proposed wave | Note |
|---|---|---|---|---|---|---|
| RM-LR-01 | Large-race torso / leg / arm / span shares | C | MF, SK, GR, GO reference meshes | CV | W1 | Feeds B-05 |
| RM-LR-02 | Thoracic depth and shoulder ratios (+ Narrow / Broad) | C | References + frame variants | CV | W1 (ref) / W2 (frames) | — |
| RM-LR-03 | Low-breadth GO vs Broad SK at equal height | C | GOR-BODY-12/14 + Broad Skarn meshes | CV | W2 | Extreme meshes |
| RM-LR-04 | GR-BODY-10 vs GO limb-present family (AD-3 floor) | C | GR-BODY-10 mesh; GO family definition | CV | W2 | Direction already canon |
| RM-LR-05 | Joint scale, large races + MF | C | References | CV | W1 | With RM-UB-03 |
| RM-LR-06 | ALPC proxy profile | C | GO reference + Narrow | CV | W2 | — |
| RM-LR-07 | Hand ratios | C | References | CV | W1 | — |
| RM-SR-01 | Pipkin trunk share + pelvic vertical | C | PK + MF references | CV | W1 | Resolves B-07 numerically |
| RM-SR-02 | Cogling segment ratios | C | CG reference + extremes | CV | W1 (ref) / W2 | Directions canon (RAC-04) |
| RM-SR-03 | Shaft and joint breadth, short races | C | References | CV | W1 | Structural-mass axis |
| RM-SR-04 | Head ÷ stature, FVI, ORB vs aperture (anti-juvenile) | C | PK, CG references + minimum-height cases | CV | W1 (ref) / W2 (min) | Add Durrim to scope (RAC-04) |
| RM-SR-05 | Durrim depth domains A–E | C | DU + MF at 152 cm | CV | W2 | — |
| RM-SR-06 | Durrim torso vs equal-height MF | C | 152 cm three-population set | CV | W2 | — |
| RM-CF-01 | Saurin FPI + corners | C | **none** (frozen reference exists) | CV | **W1** | Independent of every biology gap |
| RM-CF-02 | Marchfolk FPI/MPI/MdPI incl. most-projecting valid face | C | **F-03** | CV | W1 after P2 | — |
| RM-CF-03 | Grask same | C | **F-01** | CV | W2 after P2 | — |
| RM-CF-04 | Gorrund same | C | **F-02** | CV | W2 after P2 | — |
| RM-CF-05 | FPI margin | **Author decision** (not set here) | RM-CF-01…04 | CV | after W2 | Order forbids setting it |
| RM-CF-06 | CBH, TBP (DU, GO, MF) | C | none (directions canon) | CV | W2 | — |
| RM-CF-07 | FVB + MVI (GR, AE, MF, SK) | C | none | CV | W2 | — |
| RM-CF-08 | ORB, IOD, aperture (elves, SA) | C | **F-07** wording | CV | W2 | — |
| RM-CF-09 | Skarn craniofacial tendencies | C | none (SK v1.2 directions) | — | W3 | P3 |
| RM-CF-10 | HSR (GR, GO, PK, CG; add DU) | C | none | CV | W1 | — |
| RM-UF-01 | Aperture vs orbit, all | C | none | CV | W2 | — |
| RM-UF-02 | Ear-family envelopes | C | **F-04, F-05, F-06** | CV | W2 after P2 | — |
| RM-UF-03 | Saurin IOD tolerance | C | Rebuilt brow/postorbital planes (SA L4187) | — | W3 | — |
| RM-UF-04 | Saurin ridge and facial scale fields | C | none | — | W3 | — |
| RM-UF-05 | Batch diversity threshold | **E** | Generator system | — | LS | Not reference anatomy |
| RM-UB-01 | Segment-share bands | C | B-25 MF baseline; RAC-04 constraints | CV | W1–W2 | — |
| RM-UB-02 | Allometry vs stature | C | **Min / ref / max meshes per race** | CV | W2 | No existing candidate (RAC-12 §5) |
| RM-UB-03 | Joint / robusticity envelopes | C | Frame variants | XM, CV | W2 | — |
| RM-UB-04 | Saurin reachable tail-cap function | C | **B-20 landmark**; SA variants | CV | W2 | — |
| RM-UB-05 | Halvren stature tails | C | **RAC-09 authorship** | XM | W3 | Biology first |
| RM-OT-01 | Sagekin vs MF | C | MF baseline; SG ribcage wording (RAC-03) | CV | W1 | — |
| RM-OT-02 | Elf limb / thoracic / neck ratios | C | Elf references | CV | W2 | — |
| RM-OT-03 | Halvren source-passing statistics | C | Generator + HV references | CV | W3 | — |
| RM-OT-04 | Saurin vs Sagekin and Halvren matched height | C | SG, HV references (no HV tail needed) | CV | W2 | — |
| RM-OT-05 | Stature distributions and world-scale extremes | **E** (+C) | World review | — | LS | — |

**Proposed new queue items (for author acceptance; semantics only):**

| ID | Measure | Why |
|---|---|---|
| RM-UB-06 | Per-race pelvic breadth, depth and vertical contribution, external skeletal landmarks only | No queued item measures pelvic morphology outside Pipkin (RM-SR-01) and the ALPC proxy (RM-LR-06) (RAC-03) |
| RM-UB-07 | Marchfolk baseline set: segments, torso, neck, pelvis, head share, joints at 147 / 173 / 203 cm, both sex-related configurations | B-25: every relative statement depends on it (RAC-04, RAC-12) |
| RM-UB-08 | Saurin body scale-field ranges (body analogue of RM-UF-04) | B-24 has no body measurement item (RAC-10) |

## 4. Summary counts

| Class | Items (§1–§2) |
|---|---|
| A (now, qualitative) | B-06, B-09, B-20, B-26, B-27, F-01 (envelope only), F-02 (comparator), F-03, F-05, F-06, F-07, F-10; A-parts of B-18; B-16 baseline **by explicit author decision only** |
| Creative author decision (not A/B) | F-01 central tendency; B-28 second-configuration soft tissue; RAC-09 H-5 bounding |
| B | B-01, B-02, B-04, B-05, B-08, B-10 (DU/PK/CG), B-12 (SA), B-13 (PK/CG), F-04 |
| C | B-07, B-10 (GR/GO/silent), B-21, B-22, B-24, B-25; every RM measurement |
| D | B-03, B-11, B-12 (non-SA), B-13 (DU/GR/GO), B-14, B-15, B-17 (thickness), B-28, B-29, F-08 |
| E | B-17 (durability), B-19, B-23, B-30, B-31, B-32, B-33, F-09, RM-UF-05, RM-OT-05 |

**Items that block a central reference mesh (CM):**
- **B-26** (reference composition definition) and **B-27** (measurement stance), for every population: method definitions, class A, proposed in RAC-02;
- **F-10** (via F-01/F-02), for the **Grask and Gorrund heads** only;
- **B-28**, for the **second-configuration** ARMs of DU, GR, GO, PK and CG only (creative authorship; RAC-07 §4).

— Claude

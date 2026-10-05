<!-- RAC Phase 1 evidence extraction (agent-produced, line-checked at HEAD 218f64a). Not canon; supporting evidence for reviews/claude-rac-01…12. -->
# E — Craniofacial evidence extraction for RAC-11 (RM-CF / RM-UF prerequisites)

**Scope.** This file extracts evidence only. It feeds RAC-11 in `reviews/chatgpt-reference-anatomy-closure-phase1-order.md` (L164–173). It sets no number, no FPI margin (RM-CF-05) and no measurement-derived range. Line numbers were checked against the current working tree with `sed`/`grep`/`Read`.

**Tags.**
- [POS]: positive anatomy or tendency.
- [OPEN]: canon marks the item OPEN.
- [TEST]: a validation test or diagnostic.
- [BAN]: something the anatomy must never become.
- [NUM]: canon already holds a number.
- [SILENT]: canon says nothing on the point.

**Line-drift warning.** r3 and r5 cite line numbers at HEAD `eb837b8` (r2 L7). The UFCA-status paragraphs added later move the Grask craniofacial lines by +2 and the Gorrund lines by +4. Checked with `git show eb837b8:`.

| Old cite (r3/r5) | Current line | Content |
|---|---|---|
| GR L360 | GR **L362** | Prognathism row |
| GR L349 | GR L351 | Facial height |
| GR L358 | GR L360 | Midface |
| GR L370 | GR L372 | Mandible |
| GR L471–473 | GR L475 | Verticality |
| GO L308 | GO **L312** | Prognathism OPEN |
| GO L297 | GO L301 | Cranial breadth |
| GO L346 | GO **L350** | Ear projection "range OPEN" |
| GO L419–431 | GO L425–427 | Transverse Structural Continuity (TSC) |

The `reviews/ufca-evidence/grask.md` digest already uses the current lines (for example L362 Prognathism), so it is confirmed against the spec.

---

## 1. GRASK (`specs/grask/GRASK_V1.md`) in depth

### 1.1 Facial projection / prognathism
- [OPEN] The projection distribution is OPEN. — "maxillary and mandibular projection distribution OPEN pending anatomical validation" (GR L362)
- [POS] Some projection variation may be valid. — "some variation may be valid, but Grask aren't defined by muzzle-like projection, ape-like prognathism or extreme underbite" (GR L362)
- [BAN] No muzzle, ape-like prognathism or extreme underbite as a definer (GR L362, same quote).
- [POS] Prognathism is not mandatory. — "Not mandatory:" (GR L362, row opener). The approved-decisions summary repeats this: "pronounced prognathism isn't required" (GR L437).
- [BAN] The midface never becomes a muzzle or snout. — "never a human face with a downward-stretched nose, a detached muzzle or a snout" (GR L361)
- [BAN] Ape-like anatomy is anti-definition. — "Grask are **not** stretched humans, thin Skarn, heavy Aelari, … ape-like humanoids, mandatory tusk-bearers" (GR L724)
- [POS] UFCA routing holds projection at central values. — "projection is drawn only from authored central values until its distribution is authored." (GR L408)
- [SILENT] Canon gives **no direction for Grask forward projection relative to Marchfolk, Skarn or Gorrund**. Every comparative direction Grask states is vertical (facial height, midface vertical contribution, lower-face vertical contribution), never anterior. No Grask central projection value is stated anywhere. GR-FACE-01 specifies "moderate facial breadth, brow, nose and jaw" (L412) but no projection.
- [SILENT] Canon does not say whether the long midface (vertical) couples to maxillary projection (anterior). r3 keeps them as separate indices: MVI is vertical, MPI is anterior (r3 L66, L71).
- [POS] The Saurin side gives the cross-race direction. — "No control combination may cross into Marchfolk, Grask or Gorrund adult projection ranges at normalized head size." (SAURIN L2399)

### 1.2 Facial verticality, midface, cranium (context for RM-CF-07)
- [POS] Core statement. — "an elongated but structurally grounded adult craniofacial architecture characterized by increased facial vertical contribution, a long integrated midface" (GR L342)
- [BAN] — "This is never a human face stretched vertically." (GR L344)
- [POS] Elongation is distributed, not scaled. — "Distributed across cranial proportions, brow-to-orbit relationship, midface and maxillary vertical contribution, nose root, lower-face vertical contribution and mandible; never vertical scaling" (GR L350)
- [POS] Facial height trends greater than Marchfolk and Skarn. — "Trends toward greater facial vertical contribution relative to facial breadth than Marchfolk and Skarn, as a tendency; broad-faced Grask stay valid" (GR L351)
- [POS] Midface tendency is locked. — "**Grask trend toward greater midface vertical contribution than Marchfolk and Skarn reference anatomy**" (GR L360)
- [POS] Zygomatic architecture. — "vertically integrated zygomatic architecture that supports the long midface rather than strongly lateral cheek width as the primary signal" (GR L358)
- [POS] Cranial vault proportions need validation. — "no reduced braincase or sloping forehead to look primitive, no oversized cranium to look alien (proportions need validation)" (GR L352)
- [POS] Verticality is multiregional. — "Grask facial verticality is a multiregional proportional relationship and must not be defined solely by facial-height-to-width ratio." (GR L475)
- [POS] Absolute and proportional height are separate. — "**Absolute facial height** (the physical dimension) stays distinct from **proportional facial height or vertical contribution**" (GR L477)
- [BAN] No raw-ratio comparison against Aelari. — "never rely only on raw facial height or height-to-width ratio, especially against Aelari." (GR L477)
- [POS] Depth is not flatness. — "verticality never means flatness, and depth is evaluated independently across brow, orbit, zygomatic region, midface and maxilla, and mandible." (GR L378)
- [POS] Grask do not reuse the Durrim depth identity: "emphasize **vertical organization and elongated integrated relationships** instead, without being flat" (GR L378)

### 1.3 Jaw / mandible
- [POS] — "**Grask trend toward a substantial mandible with meaningful vertical ramus/lower-face contribution, integrated with the elongated face without requiring extreme width or projection.**" (GR L372)
- [BAN] — "never requiring a giant square jaw" (GR L374)
- [POS] Relationship rule. — "Lower-face vertical contribution may exceed Marchfolk and Skarn, but midface and lower-face elongation are never both maximized without relationship-aware validation" (GR L374)
- [POS] Malocclusion is not racial. — "Underbite, overbite and misaligned jaws aren't racial requirements, and ordinary functional jaw closure is valid." (GR L370)
- [TEST] Jaw neutralization fails if "Identity disappears without an oversized jaw" (GR L418).
- [TEST] Diagnostics GR-FACE-08 (narrower jaw) and GR-FACE-09 (broader jaw) (GR L412).

### 1.4 Tusk-like canines / dentition
- [POS] — "**Grask possess a functional humanoid dentition as the first-pass default.**" (GR L368, L481)
- [BAN] — "Tusks, exposed canines, fangs, shark-like teeth and constantly visible teeth aren't added, and detailed dentition is **OPEN**." (GR L370)
- [POS] — "**Tusks are NOT required Grask anatomy** and never the primary identifier" (GR L370)
- [OPEN] — "whether limited tusk-like canine variation could exist is **OPEN** and needs explicit review before introduction." (GR L370)
- [OPEN] — "detailed tooth morphology, canine prominence distributions, dietary specialization and dietary range stay **OPEN**." (GR L483)
- [OPEN] The housekeeping list repeats it: "possible limited tusk-like canine variation, exact ear-length ranges" (GR L734)
- [POS] r3 keeps tusks out of the projection landmarks: "Tusk-like canines are excluded from FAL and Pr" (r3 L95). The tusk landmark exists only "if later approved" (r3 L57). **Tusk status therefore does not block RM-CF-03.**

### 1.5 Nose
- [POS] — "**Grask facial identity must survive a moderate, non-exaggerated nose**, and large, long or broad-nostriled noses aren't racial markers" (GR L366)
- [TEST] Nose neutralization fails if "Only the largest nose reads troll" (GR L416). Diagnostics GR-FACE-10/11 (GR L412).
- [POS] r3 excludes the nasal pyramid from FAL (r3 L40), so nose size cannot inflate FPI.

### 1.6 Brow
- [POS] — "May have meaningful structural presence but a heavy brow isn't required" (GR L354)
- [BAN] — "a permanent scowl is never anatomy" (GR L354)
- [TEST] Brow neutralization fails if "Reduced brow makes the character human or elven" (GR L417). Diagnostics GR-FACE-04/05 (GR L412).
- [TEST] Named invalid combination: "strongest brow, deepest orbit and smallest eye opening" (GR L406)

### 1.7 Cross-race direction statements (face)
- [TEST] vs Aelari (critical): "Never a 'heavy-faced Aelari'" (GR L382)
- [TEST] vs Skarn: "a broad-frame, broad-jawed, high-muscle Grask never becomes 'Skarn with a longer face'" (GR L385)
- [TEST] vs Marchfolk: "never a tall human face stretched vertically" (GR L386)
- [TEST] vs Marchfolk (moderate-feature Grask) fails if "It reads as a tall human with slightly unusual ears" (GR L429)
- [TEST] Minimum Grask vs maximum Marchfolk "fails if it needs green skin, troll ears or a monster face" (GR L709)
- [SILENT] No Grask–Gorrund **projection** comparison exists. The Gorrund spec frames Grask vs Gorrund as vertical vs transverse (GO L331, L405).

### 1.8 Ears
- [POS] Core statement, as amended. — "**Grask ears are elongated humanoid ears with a backward/upward taper that remain anatomically distinct from elven ears**" (GR L396)
- [POS] The positive architecture that replaced "broader base". — "a robust, visibly folded cartilage architecture through much of the auricle, with a comparatively substantial upper-ear body … before transitioning into a later terminal taper." (GR L447)
- [POS] — "**The Grask ear remains structurally substantial farther from the skull before narrowing into its terminal taper.**" (GR L451)
- [POS] Silhouette. — "**structured, folded auricle → sustained upper-ear body → later taper**, rather than **base → continuous elegant taper**" (GR L453)
- [BAN] Taper limits. — "never becomes blunt triangles, thick spikes or horn-like ears" (GR L453); "A taper may occur without needle points, knife-like ears or perfect triangles." (GR L398)
- [POS] — "**robust cartilage architecture never means a uniformly thick ear**" (GR L453)
- [POS] Attachment. — "preserve a clearly humanoid auricular root" (GR L455); "Attachment isn't defined as higher, lower, broader or stronger than all elves" (GR L457)
- [POS] Lobe. — "a recognizable lower auricular/lobular region rather than having the entire ear collapse into one continuous pointed blade." (GR L459)
- [NUM]/[OPEN] **Length** runs "from moderately to strongly elongated without required extremes (exact ranges OPEN)" (GR L398). The range is repeated as OPEN: "exact ear-length ranges" (GR L734). The decision register also lists "ear length ranges" as OPEN (register L720, L727).
- [POS] Moderate and strong length are both valid. — "moderately and strongly elongated ears stay valid" (GR L461)
- [POS] Orientation. — "orientation varies across upward, backward and more lateral sweep, never tied to personality" (GR L398)
- [BAN] — "**orientation alone must never distinguish a Grask ear from an elven ear**" (GR L461)
- [POS] Relation to elven ears. — "Elven ears belong to the shared elven anatomical family and Grask ears don't" (GR L398); "never 'large Fenn ears on a troll head.'" (GR L398)
- [TEST] Long Grask vs long elven ear: "a long Grask ear and a long elven ear stay distinguishable through cartilage architecture and taper behavior." (GR L461)
- [TEST] vs Aelari: "Fails if only orientation separates them" (GR L465). vs Vael: "Base breadth and attachment strength are never the primary distinction" (GR L466).
- [POS] Never identity alone. — "Ears may contribute visibly to recognition but can't carry the whole identity" (GR L398); "**Grask craniofacial identity must survive partial ear concealment.**" (GR L469)
- [TEST] Ear neutralization fails if "Partially obscured ears make the character human or elven" (GR L419). AD-2 says ears never rescue a body: "Ears, face, surface phenotype, muscle and absolute height never rescue an otherwise collapsed body architecture." (GR L715)
- [TEST] GR-EAR-01 (moderate length), 02 (stronger length), 03 (greater backward sweep), 04 (greater upward sweep). All must show "the folded cartilage, sustained upper-ear body, later terminal taper and recognizable lobular region" (GR L469).
- [TEST] Named invalid combination: "maximum ear length and sweep with the smallest base" (GR L406). *Residual:* this keeps base size in a relationship rule even though "broader base" was superseded as the identifier (GR L396, L445). This is not a contradiction, but the RM-UF-02 Grask variable set must still include base size.
- [OPEN] Ear mobility: [SILENT] in GRASK. UFCA lists ear mobility as OPEN for "Elves, HV, PK, CG" (UFCA-07 L67), not for Grask.
- [OPEN] The ear rig is technical: "no … ear rig … is chosen" (GR L433).
- [POS] Equipment: "ears never clip through helmets" (register L766). This is E-class.

### 1.9 Head scale
- [OPEN] — "No head-to-height ratio is locked, but a comically small, oversized or uniformly scaled human head is avoided, pending cross-race prototype validation." (GR L433)

---

## 2. GORRUND (`specs/gorrund/GORRUND_V1.md`) in depth

### 2.1 Facial projection / prognathism
- [OPEN] — "the prognathism distribution is **OPEN** (limited or moderate variation may exist, extreme isn't required)." (GO L312)
- [POS] — "moderate forward projection may be valid without a muzzle, snout or ape-like prognathism" (GO L312)
- [BAN] Muzzle, snout and ape-like prognathism are excluded (GO L312). — "Greater facial depth: never a muzzle, ape-like face or extreme prognathism" (GOR-FACE-05, GO L384)
- [BAN] Cranial depth is not projection. — "never equated with prognathism, a huge nose or a muzzle" (GO L302)
- [POS] Midface depth without projection identity. — "The midface has substantial depth and integration across orbits, zygomatics, maxilla, nasal root and upper dental region, never reduced to 'big nose'" (GO L312)
- [POS] The approved list includes "meaningful midface depth without a muzzle; extreme prognathism not required" (GO L415).
- [BAN] Aging adds no projection. — "age never requires a larger brow, jaw, prognathism, nose or ears for ogre effect" (GO L531)
- [POS] UFCA routing. — "maxillary/mandibular projection is drawn only from authored central values until its distribution is authored." (GO L371)
- [SILENT] No direction relative to Marchfolk, Skarn or Grask for **forward** projection. "Moderate" (L312) has no stated reference population. As with Grask, no central projection value is authored. GOR-FACE-01 has "moderate … midface" (GO L377).
- [POS] Facial depth is multiregional and separate from projection. — "A major multiregional dimension (brow and orbit, zygomatics, midface, maxilla, nasal root, mandible, soft tissue), never one Face Depth slider" (GO L304). TSC: "facial depth remains substantial but is not the primary proportional specialization" (GO L425).
- **Measurement note (evidence, not a decision).** FPI = (f(FAL) − f(OC_mid)) ÷ HL (r3 L65). Greater midface/maxillary depth (GOR-FACE-05) is the canonical diagnostic most likely to carry the maximum valid Gorrund FPI. The RM-CF-04 case list should include it explicitly. r3 L121 says "maximum valid midface / projection extremes" but names no diagnostic ID.

### 2.2 Cranium, breadth, depth, TSC (context for RM-CF-06)
- [POS] Core statement. — "a broad, deep and structurally integrated adult craniofacial architecture distinguished by transverse structural continuity across the lateral brow/orbital, zygomatic and posterior mandibular regions." (GO L293)
- [POS] CBH direction, corrected wording. — "**Gorrund trend toward greater cranial breadth relative to cranial height than Marchfolk human reference anatomy**" (GO L443; also L301)
- [POS] Not every individual. — "This is a population tendency, not every Gorrund exceeding every Marchfolk." (GO L445)
- [BAN] TSC exclusions. — "It never means a flat face, a wide-face slider, maximum eye spacing, giant cheekbones, a square jaw, horizontal scaling, a rectangular head or reduced depth" (GO L427)
- [POS] TSC is a validator. — "Transverse Structural Continuity stays a validator, never a slider." (GO L371)
- [POS] Face and body are independent. — "more body continuity never requires more facial continuity, each varying independently within relationship-aware Gorrund limits." (GO L741)
- [POS] Vertical elongation is not Gorrund. — "**Gorrund facial identity is NOT primarily vertical elongation**" (GO L324)

### 2.3 Jaw / mandible
- [POS] — "**Gorrund possess a structurally substantial mandible with meaningful breadth and depth, integrated into the broad/deep craniofacial system without requiring extreme jaw projection or width.**" (GO L322)
- [BAN] — "mandibular depth contributes presence without meaning a huge chin, underbite or forward jaw." (GO L324)
- [POS] — "Jaw breadth ranges from lower through moderate to greater, and not every Gorrund is square-jawed" (GO L324)
- [POS] Ramus participates in TSC. — "The ramus and posterior jaw participate more strongly in the transverse framework … without requiring an extremely broad jaw body, square chin or huge jaw" (GO L435)
- [POS] — "underbite, overbite and dental misalignment aren't racial requirements." (GO L320)
- [TEST] GOR-FACE-08/09 narrower/broader jaw (GO L387–388).

### 2.4 Tusk-like canines / dentition
- [POS] — "**Tusks are NOT required for Gorrund racial identity.** A completely non-tusked Gorrund is fully valid and immediately recognizable." (GO L318)
- [OPEN] — "Limited tusk-like canine variation is **OPEN**, kept out of ordinary presets until reviewed and not assumed to resolve the same way as Grask." (GO L320)
- [OPEN] Kept separate from Grask. — "Grask possible limited tusk-like canine variation and Gorrund possible limited enlarged or tusk-like canine variation stay **separately OPEN**" (GO L475)
- [POS] — "Dentition is **functional humanoid** as the first-pass default, detailed dental morphology is **OPEN**" (GO L316)
- *Residual:* the wording differs between "tusk-like" (L320) and "enlarged or tusk-like" (L475). This is UFCA-07 N-6, minor.
- r3 excludes tusks from FAL and Pr (r3 L95), so **tusk status does not block RM-CF-04.**

### 2.5 Nose and brow
- [POS] Nose. — "large noses may be valid, moderate ones must be, and a moderate-nosed Gorrund stays recognizable." (GO L316)
- [POS] — "broad face never hard-links to broad nose." (GO L316)
- [POS] Brow. — "Gorrund may have substantial bony brows within their cranial scale, but a heavy brow isn't required" (GO L308)
- [TEST] — "a low-brow Gorrund that becomes a generic human fails." (GO L308)
- [TEST] GOR-FACE-06/07 and GOR-FACE-10/11 (GO L385–386, L389–390). Neutralization fails if "Only the larger nose, heavy brow or broad jaw reads Gorrund" (GO L398).

### 2.6 Cross-race face
- [TEST] vs Grask (critical): "Fails as 'wide Grask'" (GO L331). A further test fails if "They reduce to vertical-versus-horizontal sliders instead of independent multiregional anatomy" (GO L405).
- [TEST] vs Skarn: fails if "The distinction needs tusks, a huge brow or fantasy skin; Skarn stay recognizably human" (GO L404)
- [TEST] vs Durrim: "Never 'giant Durrim head' or the same recipe at a different scale" (GO L330). The matched-scale diagnostic is at GO L439.
- [SILENT] No Gorrund-vs-Marchfolk **projection** direction is stated.

### 2.7 Ears
- [POS] Positive identity is required. — "Gorrund need a positive ear identity, never enlarged human ears, elf ears, Grask ears or tiny ogre ears." (GO L346)
- [POS] Part 3 core. — "**Broad, structurally substantial humanoid auricles with strong cranial attachment, meaningful cartilage depth and a rounded-to-angular upper contour rather than an elongated terminal point.**" (GO L348)
- [POS]/[OPEN] **Projection** (Part 3). — "Projection from the attachment is generally **short-to-moderate relative to elven and Grask long-ear possibilities** (range **OPEN**)." (GO L350)
- [POS] **Projection** (clarification). — "Lower, moderate and greater valid projection all occur; ears aren't hard-locked flat, and the tendency concerns the relationship among size, broad attachment and projection" (GO L460)
- [POS] Ear-to-skull relationship. — "Tends to sit **relatively close to the lateral skull despite substantial absolute size**, through broad attachment and orientation" (GO L459)
- **Residual for authorship.** L350 frames projection as "short-to-moderate relative to elven and Grask long-ear possibilities". That phrase mixes outward extent (length-like) with projection-from-skull. L459–460 treat projection as distance from the skull and allow "greater valid projection". These can be read together: the population tendency is close-set and short-to-moderate *relative to elven/Grask extent*, with lower to greater individual variation. Canon does not say which variable the "range OPEN" refers to: auricle projection from the skull, outward extent, or both. **RM-UF-02 cannot be specified until the author names the variable.**
- [POS] Clarification core. — "a broad, deep auricular bowl with a strongly expressed inner antihelical fold system, while the outer rim remains comparatively broad and structurally continuous" (GO L451)
- [POS] Bowl. — "**Meaningful depth relative to overall ear size** as a population tendency … never a cavity or funnel" (GO L455)
- [BAN] Rim. — "never into the extended elven or Grask terminal taper" (GO L457)
- [BAN] Upper contour. — "a strongly pointed tip is outside the ordinary envelope" (GO L458). "a visibly elongated pointed ear triggers cross-population review." (GO L350)
- [BAN] — "Auricles may be broad, but never flat circular 'ogre ears'" (GO L350)
- [POS] Orientation is not an identifier. — "Lateral projection and slight upward or backward orientation vary, never as an identifier alone." (GO L350)
- [TEST] vs Grask: "Fails as 'short Grask ears'" (GO L354). vs Vael: "base and attachment alone never distinguish Gorrund" (GO L355). vs humans: "never merely enlarged human ears" (GO L464). Durrim: "no Gorrund ear traits are added to Durrim retroactively" (GO L465).
- [POS] Never identity alone. — "Stronger ear traits never make ears the primary identifier; ears are partly concealed in face tests and facial identity must survive." (GO L471). Also GO L359.
- [TEST] GOR-EAR-01 lower projection or compact, 02 moderate projection, 03 greater breadth, 04 lower breadth, 05 more rounded contour, 06 more angular contour (GO L361, L471).
- [TEST] Named invalid combination: "maximum cranial breadth, facial depth, brow, nose, jaw and ear breadth together aren't assumed valid" (GO L373)
- [OPEN] Ear mobility: [SILENT] in GORRUND. Ear deformation is technical OPEN (GO L413). Headgear solutions are OPEN (GO L644), E-class.
- [OPEN] The register still carries "ear projection range" as OPEN (register L842). The PRELIMINARY row at register L839 keeps "short-to-moderate projection".

### 2.8 Head scale
- [OPEN] — "head-to-height ratio **OPEN**" (GO L299)
- [TEST] Maximum height (about 251 cm) fails on "tiny-head giant syndrome" (GO L408). Minimum height (about 208 cm) fails if "The head-body combination stops reading Gorrund amid other tall populations" (GO L409).

---

## 3. Saurin rostral floor (cross-race constraint on RM-CF-01…05)

- [POS] — "project farther forward than Marchfolk adult tendency" (SAURIN L745)
- [BAN] — "avoid a long canine muzzle;" (L748)
- [POS] The floor is a non-overlap boundary. — "the **minimum valid Saurin rostral projection remains clearly outside the approved adult projection ranges of Marchfolk, Grask and Gorrund**" (L756)
- [TEST] SAU-FACE-02: "the minimum remains clearly beyond Marchfolk, Grask and Gorrund adult projection ranges at normalized head size" (L1243)
- [BAN] — "No control combination may cross into Marchfolk, Grask or Gorrund adult projection ranges at normalized head size." (L2399). Restated at L3642.
- [NUM] — "**Rostral index** (rostral projection ahead of the eye centres ÷ head length; reference 0.288) stays 0.255–0.335." (L4181)
- [OPEN] — "the cross-race numeric check (§146) is OPEN because Marchfolk, Grask and Gorrund canon contain no numeric projection ranges." (L4181); also L4266.
- [POS] Coupling. — "Cranial length × rostrum floor: the rostrum minimum rises with cranial length so the index floor holds." (L4182). This is the RM-CF-01 corner.
- [POS]/[OPEN] Orbits. — "orbital placement and spacing remain locked …; their numeric tolerance is OPEN (no clean validation without rebuilding the brow/postorbital planes)." (L4187). Spacing tendency: "somewhat greater lateral spacing than Marchfolk adult tendency;" (L805)
- [OPEN] Ridge numerics. — "Numeric structural-ridge strength, exact placement and transition sharpness remain OPEN beyond the §259 constraints." (L671). Scale fields: "Numeric per-field scale ranges." (L4272)
- [POS] Ears (UFCA family "recessed auricular opening"). — "Saurin do **not** have projecting mammalian or elven pinnae as baseline anatomy." (L976). Pinna landmarks are N/A (r3 L54).
- UFCA restates: "The rostral index floor (0.255, provisional, SAURIN §259) remains protective canon." / "Cross-race closure is deferred to RM-CF-01…05. No margin is set." (UFCA L261–262)
- r3 fixes the comparison direction: "the Saurin floor must exceed the **maximum valid** FPI of each comparison population, with a margin the author sets." (r3 L112)

**Implication (evidence only).** For RM-CF-03/04, the Grask and Gorrund authoring needed is the **upper boundary of valid adult projection** (maximum valid), not a central value. r5 Rule 2 agrees: "Central values alone never establish a boundary" (r5 L98).

---

## 4. Framework prerequisites (r3, UFCA)

- [POS] FAL excludes the nose, lips and keratin. — "excluding the external nasal pyramid, lips and any keratin display" (r3 L40)
- [POS] MPI/MdPI are already tied to the OPEN items. — "Grask 'maxillary projection distribution OPEN' (GR L360); Gorrund prognathism OPEN (GO L308)" (r3 L66). The lines are stale: they are now GR L362 and GO L312.
- [OPEN] **Ear landmarks are named but undefined.** The race-conditional pinna row lists "Superaurale, subaurale, auricle tip, auricle projection. **Family-specific parameter sets** (report 03 §5)" (r3 L54). There are no S/E definitions, unlike the universal table (r3 L30–44). r5 states it outright: "ear landmarks are not in r3 and must be defined" (r5 L68). This is a methodological prerequisite for RM-UF-02, separate from biology.
- [BAN] — "pinna indices across ear families" are never cross-race (r3 L83). UFCA: "**Never a pointiness continuum or interpolation.**" (UFCA L177)
- [OPEN] UFCA L359: "**Depends on authored Grask ear-length and Gorrund projection ranges, which do not yet exist**"
- [OPEN] UFCA §19.1 lists "Grask/Gorrund prognathism distributions" (L374), "tusk-like canines (separately)" (L375), "Ear mobility" (L377), "Grask/Gorrund ear length and projection ranges" (L378) and "Non-Saurin head-to-stature" (L380).
- [POS] UFCA-07 L68 adds a third ear-range holder: "DU ('future work', L195)".
- [NUM] UFCA sets none: "**No numeric facial envelope is set by UFCA.**" (UFCA L352)

---

## 5. Other races (brief): ear family, authored ear/projection content, further prerequisites

**Marchfolk** (UFCA family: Human auricle)
- [POS] Ear variation axes are explicit. — "They vary in ear length and breadth, lobe size and attachment, projection from the skull, vertical position, angle, curvature and natural asymmetry." (MF L311)
- [BAN] — "human and elven ears aren't 'pointiness 0% versus 100%.'" (MF L311)
- [SILENT] **No facial projection, prognathism or maxillary statement anywhere in MARCHFOLK_V1.md.** r3 L106 says the same: "Marchfolk canon has no projection values." RM-CF-02 needs "the most prognathic valid adult face" (r3 L120), but canon never defines that face qualitatively. Only general believability applies (UFCA L205: "inside believable Marchfolk adult human anatomy").

**Skarn** (Human auricle via AC-4)
- [OPEN]/[POS] Promise. — "Detailed craniofacial ranges come in a later spec." (SK L48). This is the RM-CF-09 hook.
- [POS] v1.2 tendencies vs Marchfolk: "a slightly larger, more robust skull", "a somewhat stronger brow", "more jaw mass", "a more substantial mid-face and cheeks", "a somewhat larger nose" (SK L147–151). — "These are tendencies, not requirements." (SK L154)
- [POS] Ears. — "Skarn follow the Marchfolk human-family auricular anatomical foundation (Marchfolk Part 2 §3–4) unless this spec explicitly modifies a tendency." (SK L160)
- [SILENT] No Skarn projection statement. "Mid-face" is "substantial", not "projecting". Skarn is not in the Saurin non-overlap set (SAURIN L2399), so this is not a blocker.

**Sagekin** (Human auricle via AC-4)
- [POS] Ears: same AC-4 pointer (SG L149). [BAN] "Pointed ears … are never used to set Sagekin apart." (SG L147)
- [SILENT] No projection direction. The nose and jaw tables list "projection" only as a control axis (SG L221–223).

**Fenn** (Elven continuous taper)
- [POS] — "Fenn have the greatest average lateral (outward) ear projection of Fenn, Aelari and Vael, with individual overlap and the Fenn ear bounds (§9) preserved." (FN L183)
- [POS] Control axes. — "overall length, base width, tip length and sharpness, vertical angle, forward and backward sweep, projection from the skull" (FN L187)
- [TEST] FN-24 "Maximum supported ear length", FN-25 "Minimum, subtle ear length" (FN L229–230)
- [POS] Orbits. — "Slightly larger orbits, slightly more eye prominence" (FN L173). This is the F-20 terminology overlap ("Fenn's 'slightly larger orbits' (v1.2) vs the review's 'open presentation'", findings L190). It must be read before RM-CF-08 / RM-UF-01.

**Aelari** (Elven continuous taper)
- [POS] — "Somewhat more upward orientation, clean gradual taper, slightly closer to the skull, moderate to long length" (AE L228)
- [OPEN] — "Aelari ears aren't assumed to move just because they're elves." (AE L251, §17 "Ear mobility (open)")

**Vael** (Elven continuous taper)
- [POS] — "Somewhat broader base, more lateral and backward orientation, moderately shorter taper" (VA L284)
- [POS] — "Subtle, reference and long ears are all supported, identity survives subtle ears, and maximum ears stay believable." (VA L286)
- [OPEN] — "Ear mobility is unresolved, isn't assumed, and goes to the Elf Comparative Review." (VA L290). The review keeps "Ancestral shape and mobility unresolved" (elf review L283).

**Halvren** (Mixed coupled human + elven)
- [POS] — "Halvren ears are not human ears with a pointiness slider." (HV L196)
- [POS] — "**Ear length isn't a genealogy meter.**" (HV L206)
- [POS] Per-source ear tendencies are inherited (HV L200–204). Halvren envelopes inherit from source families, so RM-UF-02 must measure the human and elven families first. [OPEN] Ear mobility is a blocker for later systems only (HV L437, L496: "Stay OPEN until their Halvren subsystem needs").

**Durrim** (Human-auricle variable set, own compact range)
- [POS] — "Projection runs from close-set to more projecting, independent of length, breadth and lobe size" (DU L195)
- [OPEN] — "first-pass Durrim ears sit within a broad compact-humanoid range, with population distributions future work." (DU L195)
- [POS] Midface. — "broad projection range, never universally protruding" (DU L183). Durrim is not in the Saurin non-overlap set.
- [OPEN] Depth domains A–E are authored qualitatively (DU L294–300). However: "There's no approved Durrim facial depth number yet" and "landmark implementation later" (DU L292). These feed RM-SR-05 / RM-CF-06, not the Saurin floor.

**Pipkin** (Compact rounded)
- [POS] — "moderate overall projection, a rounded-to-softly-angular upper contour, a proportionally clear but not deep conchal bowl" (PK L340)
- [BAN] Locked exclusions: "no Grask robust folded terminal taper", "no Gorrund deep broad bowl/strong load-bearing-looking folds" (PK L346–347)
- [POS] Maxilla. — "Maxillary projection and dental-jaw support remain adult." (PK L315). [BAN] "never depends on a shortened muzzle-like facial plane" (PK L315)
- [OPEN] — "Pipkin ear mobility; no racial mobility behavior is approved at first pass;" (PK L1546)

**Cogling** (Fine folded)
- [POS] — "a relatively compact adult ear with a clearly defined helix, antihelix and conchal bowl, fine cartilage thickness" (CG L1327)
- [POS] Grask/Gorrund contrasts. — "without Grask's robust folded upper-ear body and later terminal taper" (CG L1373); "Cogling lack the broad deep auricular bowl, substantial rim and broad skull attachment." (CG L1376)
- [OPEN] — "exact ear size/fold distributions;" (CG L1676); "exact ear distributions and ear mobility;" (CG L3173)
- [POS] Fine folds are a close-view trait: "principally a **close-view/creator-camera trait**" (CG L1596). RM-UF-02 E-layer precision for Cogling is limited (r3 L94).

**Saurin** (Recessed auricular opening): see §3. The pinna family is N/A. Auricular-opening variation is §57 (L989ff); no RM item is pending on it.

---

## 6. Prerequisite and classification map

Classes follow the order's §2: **A** = authorable qualitatively now; **B** = direction now, number later; **C** = reference-mesh dependent; **D** = later biology; **E** = later system. Each RM item is itself a measurement, so the measurement step is always C. The class below is for the **prerequisite authorship**, with the measurement class in parentheses. "Sugg." marks suggestions for the author. None is a decision.

| Item | Prerequisite authorship needed | Does canon supply enough direction to author it qualitatively? | Class | One-line justification | Labelled suggestion |
|---|---|---|---|---|---|
| **RM-CF-01** Saurin FPI re-measure + corners | None | Yes. FPI form, reference 0.288, band 0.255–0.335 and coupling (SAURIN L4181–4182); r3 FAL/OC definitions | — (C) | Frozen reference aff1b52 exists; pure measurement | Sugg.: run first; it is independent of all biology gaps |
| **RM-CF-02** Marchfolk FPI/MPI/MdPI incl. most prognathic valid face | **Yes, small.** A qualitative statement of the upper valid Marchfolk projection ("most prognathic valid adult face" is used in r3 L120 but canon is [SILENT]) | Partly. Saurin gives the only direction (Saurin > Marchfolk, L745, L756). Marchfolk canon is silent; only "believable adult human anatomy" (UFCA L205) | **A** (C) | Without a named extreme, the "maximum valid" case cannot be built; a human-range believability statement is authorable without numbers | Sugg. A-1: author "Marchfolk valid adult projection spans ordinary human variation; the most-projecting valid case is an adult human face with no muzzle-like or non-human maxillary architecture", plus a named diagnostic face |
| **RM-CF-03** Grask same | **Yes.** Grask maxillary/mandibular projection distribution (GR L362, OPEN) | **Partly.** Canon gives the ceiling side ([BAN] muzzle-like, ape-like prognathism, extreme underbite; "not mandatory"; "some variation may be valid", GR L362; no muzzle or snout, L361) and the Saurin non-overlap (L2399). Canon is **silent** on any central direction vs Marchfolk/Skarn and on vertical-midface ↔ projection coupling | **A** for the shape of the distribution (qualitative envelope + named max-valid diagnostic); **B** for any "vs Marchfolk" direction, which only the author can choose (C) | The useful input is the max-valid boundary, which canon bounds qualitatively from above; the central direction is a new biological choice, not extractable | Sugg. A-2: author "Grask projection: not a racial carrier; central tendency within/near human-adult range [author to choose: ≈ Marchfolk / slightly greater]; long midface is vertical, not anterior; max valid stays non-muzzle and below the Saurin floor", and add a diagnostic GR-FACE-14 "greatest valid projection". Do **not** infer projection from GR L360 (vertical) |
| **RM-CF-04** Gorrund same | **Yes.** Gorrund prognathism distribution (GO L312, OPEN) | **More than Grask.** "Moderate forward projection may be valid", "limited or moderate variation may exist, extreme isn't required" (GO L312); [BAN] muzzle, snout, ape-like (L312, L384); depth ≠ prognathism (L302); age adds none (L531). **Silent** on the reference population for "moderate" | **A** (direction largely present; author confirms the reference population and max-valid case) → **B** if the author wants "vs Marchfolk" magnitude (C) | Canon already bounds the envelope qualitatively; only the comparator for "moderate" and a named extreme are missing | Sugg. A-3: author "moderate relative to Marchfolk adult; max valid = GOR-FACE-05-type greater-depth face, never muzzle". Name GOR-FACE-05 as an RM-CF-04 case. Keep TSC/depth separate from MPI |
| **RM-CF-05** FPI margin | Author decision only | n/a | **Not classified here** (author decision; order L173 forbids setting it) | r3 L112 and UFCA L262 reserve it | None. Sequence after RM-CF-01–04 |
| **RM-CF-06** CBH and TBP: Durrim, Gorrund, Marchfolk | None for direction | Yes. Gorrund CBH > Marchfolk tendency (GO L443); Durrim "greater cranial breadth relative to height than Marchfolk" (DU L228); TSC regions named (GO L427) | **B** (C) | Direction is locked, magnitude is measurement | Sugg.: treat TBP as a coherence profile (validator), never a target ratio (GO L371, L427) |
| **RM-CF-07** FVB with MVI: Grask, Aelari, Marchfolk, Skarn | None | Yes. Grask > MF/SK facial vertical and midface vertical (GR L351, L360); multiregional, not a single ratio (GR L475); absolute vs proportional (GR L477); Aelari never by raw ratio (GR L477) | **B** (C) | Direction locked vs MF/SK; Aelari comparison is architectural only | Sugg.: record that canon gives **no** Grask-vs-Aelari numeric direction; use the FVB+MVI pair only vs MF/SK |
| **RM-CF-08** ORB, IOD, aperture: Fenn, Aelari, Vael, Saurin | **Terminology**, not biology: F-20 orbit wording (FN L173 vs elf review "open presentation"; findings L190) | Yes for direction (Fenn slightly larger orbits; Saurin greater lateral spacing, L805; orbit ≠ aperture, universal) | **B** (C); F-20 wording fix is **A** | Direction exists; a terminology reconciliation is needed so ORB vs aperture is measured on the right concept | Sugg. A-4: resolve F-20 as "orbit size (ORB) vs visible presentation (aperture)" before measuring |
| **RM-CF-09** Skarn craniofacial tendencies vs Marchfolk | None for direction. The SK L48 "ranges in a later spec" promise is partly met by SK L145–154 tendencies | Yes. Six directional tendencies (SK L147–152), all "not requirements" | **B** (C), P3 | Tendencies are directional; ranges are measurement | Sugg.: mark the SK L48 promise as discharged directionally by v1.2 §1, numerics via RM-CF-09 |
| **RM-CF-10** HSR: Grask, Gorrund, Pipkin, Cogling | None. The OPEN is explicitly "pending cross-race prototype validation" (GR L433) | Bans only: no tiny-head giant or oversized head (GR L433; GO L299, L408); Pipkin/Cogling forbid head share as identity (UFCA-07 AD-U4) | **C** | Canon defers the ratio to measurement by design; no direction to author | Sugg.: keep as VAL/DIAG (AD-U4); the GO L408–409 height tests are the case list |
| **RM-UF-01** aperture vs orbit, all populations | None | Yes. Orbit ≠ aperture is stated per race (e.g. GR L356, GO L308) | **C** | Pure distribution measurement | — |
| **RM-UF-02** ear-family envelopes | **(a) Grask ear-length range** (GR L398, L734 OPEN). **(b) Gorrund ear-projection range** (GO L350 OPEN), **plus naming which variable** (projection from skull vs outward extent; L350 vs L459–460). **(c) Ear landmarks** (r3 L54 named, undefined; r5 L68). **(d)** Durrim distributions "future work" (DU L195); Cogling exact distributions OPEN (CG L1676) | (a) Partly: "moderately to strongly elongated without required extremes" (GR L398) and GR-EAR-01/02 give endpoints but no comparator. (b) Partly: "short-to-moderate relative to elven and Grask long-ear possibilities" (GO L350); "close to the lateral skull" (GO L459); lower–greater valid (GO L460). (c) Methodological, authorable. (d) Durrim and Cogling are qualitative only | (a) **B**; (b) **A** for naming the variable + **B** for direction; (c) **A** (method); (d) **C**; ear mobility **D/E** (not needed for static envelopes) | Directional anchors exist for GR and GO; the numbers must come from meshes; landmarks are a framework task | Sugg. A-5: author Grask length "relative to head height, moderate → strong elongation, longest valid = GR-EAR-02 class; no comparator to elven max implied". Sugg. A-6: Gorrund "auricle projection from the skull: population tendency close-set; individual lower → greater; outward extent short-to-moderate vs elven/Grask". Sugg. A-7: define Superaurale, subaurale, tip and auricle-projection landmarks at the E layer, per family |
| **RM-UF-03** Saurin IOD tolerance | None biological. The orbit position is locked (SAURIN L4187) | Direction only: "somewhat greater lateral spacing than Marchfolk" (L805, provisional) | **C** | Canon says validation needs rebuilt brow/postorbital planes (L4187) | — |
| **RM-UF-04** Saurin ridge strength, scale fields | None | Qualitative ridge architecture accepted (§36a, L671); numerics OPEN | **C** | Measurement only | — |
| **RM-UF-05** batch diversity / anti-convergence | Generator and frequency system (frequencies OPEN, UFCA L383); named cliché bundles exist in specs (e.g. Gorrund stereotype packages, GO L564) | n/a | **E** | Not reference-anatomy closure; depends on the preset/randomizer system | — |

### 6.1 Additional prerequisites found (beyond the four named in order L166–170)
1. **Marchfolk max-valid projection is undefined** ([SILENT]). It blocks RM-CF-02 as written in r3 L120. Class A.
2. **Gorrund ear "range OPEN" names no variable**: projection from the skull (GO L459–460) vs outward extent relative to elven/Grask (GO L350). Class A, needed before RM-UF-02 for Gorrund.
3. **Ear landmarks are undefined** in r3 (L54; r5 L68). This is a methodological A, not biology.
4. **F-20 orbit terminology** (Fenn) must be settled before RM-CF-08 / RM-UF-01 elf cases. Class A.
5. **Durrim ear distributions** ("future work", DU L195) and **Cogling** exact ear distributions (CG L1676) are qualitative-only. RM-UF-02 for those families is C. They do not block GR/GO.
6. **Stale line citations** in r3, r5, UFCA-07 and r2 (GR +2, GO +4). These are housekeeping, not authorship.
7. **"Authored central values"** (GR L408; GO L371; UFCA-07 L64) has **no canonical referent**: no central projection value exists in either spec. Until A-2/A-3 are authored, the central value is effectively the future reference mesh. That is circular for RM-CF-03/04 and worth noting to the author.
8. **Non-blockers confirmed.** Tusk-like canines (GR L370, GO L320/L475) are excluded from FAL/Pr (r3 L95) and do not block RM-CF-03/04. They stay D-class biology. Ear mobility (elves, HV, PK, CG) does not block static RM-UF-02 envelopes (D/E). The Durrim depth domains (DU L294–300) feed RM-SR-05/RM-CF-06, not the Saurin floor. Skarn and Durrim projection are outside the Saurin non-overlap set (SAURIN L2399).

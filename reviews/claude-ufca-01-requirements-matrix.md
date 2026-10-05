# UFCA-01: Roster Facial Requirements Extraction Matrix

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ufca-phase1-order.md` (c076294), §4
**Phase:** UFCA Phase 1, design only. No race spec, PROJECT_RULES or other canon is changed.
**Evidence:** `reviews/ufca-evidence/<race>.md` holds one full extraction per race, 29 sections each, with every item tagged and cited by line. This matrix condenses those files. Where a cell and an evidence file differ, the evidence file and the spec govern.

## 0. How to read this matrix

**Race codes:**

| Code | Race | Code | Race | Code | Race |
|---|---|---|---|---|---|
| MF | Marchfolk | AE | Aelari | GR | Grask |
| SK | Skarn | VA | Vael | GO | Gorrund |
| SG | Sagekin | HV | Halvren | PK | Pipkin |
| FN | Fenn | DU | Durrim | CG | Cogling |
| SA | Saurin | | | | |

**Class tags** (order §4):

| Tag | Meaning |
|---|---|
| **A** | anatomical requirement |
| **C** | creator-facing control requirement (Pass 1 provisional organization) |
| **V** | internal dependency / validator |
| **P** | presentation control |
| **D** | measurement / diagnostic only |
| **O** | OPEN / not yet authorized |

**References:**
- `L###` is a line in that race's spec (`specs/<race>/<RACE>_V1.md`).
- `ECR L###` is a line in `reviews/elf-comparative-review.md` (accepted, authority level 3).
- `PR` is `decisions/PROJECT_RULES.md`.

**SILENT** means the race spec says nothing on the point. No anatomy has been inferred to fill a SILENT cell (order §4, "Do not infer missing anatomy").

**Status of every race's facial control organization:** APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION. The status lines are:

| Race | Line |
|---|---|
| MF | L102 |
| SK | L162 |
| SG | L205 |
| FN | L158 |
| AE | L200 |
| VA | L221 |
| HV | L229 |
| DU | L331–334 |
| GR | L406 |
| GO | L369 |
| PK | L393 |
| CG | L1536–1538, L1564 ("does not finalize universal creator UI organization"; controls may be reorganized in this review. Cogling does not use the label verbatim) |
| SA | L1172 |

Durrim is a special case: it deliberately defines no player-facing facial controls (L234).

---

## 1. Positive facial identity (what must survive neutralization)

| Race | Canonical carrier | Kind | Ref |
|---|---|---|---|
| MF | Breadth of believable human variation; no single idealized face. No neutralization-surviving distinct feature is defined (MF is the reference population) | A | L13, L15, L139 |
| SK | Human; identity from population ranges and combinations: larger, more robust skull; stronger brow; more jaw mass; fuller midface and cheeks; larger nose; heavier neck-to-jaw transition. All "never mandatory" | A | L145–154 |
| SG | Statistical, multi-trait: cranium, forehead, eye region, cheeks, midface, nose, jaw, chin, mouth. Recognizable across a sample, **not** in every individual | A, V | L209, L246, L383 |
| FN | Combined elven craniofacial relationships: compact face, more open *visible* orbital presentation, lighter lower face; never ears alone | A | L162, L357; ECR L83–84, L282 |
| AE | Greater facial verticality, longer forehead-to-chin line, vertical midface, longer and narrower visible eyes than FN | A | L204, L243; ECR L83, L282 |
| VA | Compact vertical distribution, stronger midface integration, more mandibular presence than FN/AE. Must survive complexion neutralization | A | L225, L298; ECR L83, L282 |
| HV | Coherent mixed human/elven craniofacial space. With ears hidden, pigment neutral and culture removed, the face must still plausibly carry both ancestries. Subtle expression is valid | A | L64, L162–164 |
| DU | Compact adult cranium + integrated midface + substantial craniofacial depth relative to facial height + mandibular support + head-neck integration. "Must look Durrim bald, clean-shaven, neutral, ears hidden" | A | L164, L236, L320 |
| GR | Elongated, vertically organized craniofacial architecture: long integrated midface, orbital/zygomatic relationships, vertically organized mandible, cranial-neck integration. "Never a human face stretched vertically" | A | L342–344, L471 |
| GO | Broad, deep, integrated architecture whose specialization is **Transverse Structural Continuity** (lateral brow/orbit, zygoma, posterior mandible). Depth supports it but is not the dominant specialization | A | L293, L423, L481 |
| PK | **Integrated Mature Facial Architecture**: moderate cranial base → temple/zygoma → fully adult central midface. Must read mature before hair, beard, wrinkles or scale cues. The face is *supporting* identity; the body is primary | A | L251, L259, L459, L461 |
| CG | **Fine-Scale Planar Integration**: adult face-to-vault relationship plus fine mass with angled orbit–zygoma–maxilla–mandible junctions | A | L1124, L1687 |
| SA | **Layered Rostral-Cranial Integration**: low-to-moderate vault → orbital-temporal platform → compact projecting rostrum → deep jaw base. No human chin, lips, external nose or pinnae; displays never rescue an invalid skull | A | L1294, L4172 |

## 2. Cranial vault and cranial proportions

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | Human cranial architecture. Controls are grouped under "head and skull" | A, C | L15, L116 |
| SK | Larger, more robust skull (tendency). Controls: head width/depth/length, cranial height, temple width, face length | A, C | L147, L168 |
| SG | Own skull distributions overlapping MF. Controls: head width/depth, cranial height, temple width, face length | A, C | L105, L215 |
| FN | Slightly greater cranial height relative to face; somewhat narrower skull. No cranial controls itemized | A | L168; ECR L77 |
| AE | Slightly greater cranial height; longer face. No controls itemized; "no exaggerated alien proportions" | A | L210 |
| VA | Moderate cranial height; strong cranium-to-midface continuity; not wide by default | A | L239 |
| HV | Cranial inheritance (height, length, breadth, cranial-to-face relationship) shifted by specific ancestry; never a "human skull → elf skull" slider | A, V | L181 |
| DU | Greater cranial breadth relative to height than MF (provisional tendency). Head contributes somewhat more to stature than MF; "never an oversized fantasy-dwarf head" | A | L21, L170, L243 |
| GR | Intelligent-humanoid vault; no reduced or oversized braincase; proportions "need validation". Head-to-height ratio not locked | A, O | L352, L431 |
| GO | Greater cranial breadth relative to height than MF (tendency); meaningful cranial depth. Head-to-height ratio **OPEN** | A, O | L299, L302, L441 |
| PK | Somewhat greater head contribution than MF, but **secondary and never oversized**; never a maturity signal. Head-to-body ratio OPEN | A, O | L199, L279, L1528 |
| CG | Small adult head (~11–13 cm). Face-to-vault at or slightly above MF; the vault never carries identity. Head-to-body ratio OPEN | A, O | L1124, L1131, L1163–1167, L1581 |
| SA | Low-to-moderate vault, longer front-to-back. Hard bounds: cranial length ±8 %, width ±8 %, depth ±7 %; head length 0.156–0.184 H (±8 %). Frame does not change the skull | A, V | L720–723, L4162, L4166, L4174 |

## 3. Forehead

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | SILENT | — | — |
| SK | Control: forehead height and slope. No tendency stated | C | L168 |
| SG | Somewhat higher forehead (tendency); forehead height/slope control | A, C | L215 |
| FN | Smoother forehead-to-cranium line. No forehead control | A | L168 |
| AE | Longer forehead-to-chin line; control: forehead height/slope, temple width | A, C | L210–211 |
| VA | Control: forehead height, width, slope; temple width | C | L240 |
| HV | Forehead relationships are part of cranial inheritance | A | L164, L181 |
| DU | Broad variation in height, breadth, curvature, hairline and brow transition; low forehead not mandatory | A | L176 |
| GR | Broad variation; no receding or sloped "monster" forehead | A | L352–353 |
| GO | Varies; no required low or sloping forehead or heavy frontal bossing | A | L308 |
| PK | Varies broadly; no high childlike forehead. Control family: forehead height/slope | A, C | L287, L397 |
| CG | Forehead contour is a cranial variation; control: forehead contour | A, C | L1174, L1540 |
| SA | **No human vertical forehead**: a lower, longer slope from rostrum to frontal region, with the vault rising behind the orbital platform. No forehead control | A | L776–781 |

## 4. Brow / supraorbital (skeletal)

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | "Brow and eyes" region; brow-height asymmetry pair | C | L116, L120 |
| SK | Somewhat stronger brow on average, never mandatory; controls: prominence, shape, height | A, C | L148, L169 |
| SG | Controls: brow-to-eye distance, brow prominence. No tendency | C | L216 |
| FN | "Distinct brow and orbit relationships"; brow structure control | A, C | L169 |
| AE | Smoother, lighter brow than robust humans such as SK; delicate brows never required | A, C | L211 |
| VA | Somewhat more brow/orbital definition than AE; no permanent scowl | A, C | L240; ECR L84 |
| HV | **Brow structure is one of four separate eye-area systems**; SK ancestry may shift brow presence | A | L177, L181 |
| DU | Substantial brow supported, not mandatory. Skeletal brow ≠ eyebrow hair ≠ expression ≠ age tissue | A | L177, L272 |
| GR | Meaningful presence possible, heavy brow not required; skeletal brow ≠ eyebrow ≠ expression | A | L354 |
| GO | Substantial brow possible, not required; low-brow GO must not become generic human | A | L308 |
| PK | No heavy or permanently soft brow required; brow projection varies | A, C | L287–289, L398 |
| CG | "Fine but structurally readable orbital framing"; not absent or childlike | A, C | L1181–1191, L1541 |
| SA | Orbital platform with a less isolated brow ridge. The brow → temporal/postorbital transition is mandatory. "Orbital rim" is a creator variation | A, C | L793, L4172, L716 |

## 5. Orbit (bony)

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | Named in the validation row only; no region | V | L248 |
| SK | Controls: eye depth, spacing | C | L169 |
| SG | Controls: eye depth, spacing; eye region has its own distribution | A, C | L105, L216 |
| FN | "Slightly larger orbits" (spec). ECR reframes this as more open *visible* presentation, "not eyeball size" | A | L169; ECR L141 |
| AE | Shared elven orbital foundation; controls: size, depth, spacing, angle | A, C | L212 |
| VA | Moderate to somewhat large within elven range; broader than AE | A, C | L252; ECR L83 |
| HV | **Orbital anatomy is a separate system** | A | L181 |
| DU | Varies; never universally small or deep-set. Structural orbital depth ≠ deep-set look | A | L178, L273 |
| GR | **Bony orbit ≠ visible opening** (explicit) | A | L356 |
| GO | **Bony orbit ≠ visible opening** (explicit); spacing relationship-aware with cranial breadth | A, V | L308, L371 |
| PK | **Orbit ≠ aperture**; no infant-like orbital proportions | A | L289, L297 |
| CG | **Orbit ≠ opening**; FN-boundary: larger orbits not required | A | L1195, L1442 |
| SA | Embedded in orbital-temporal platform; forward axes. **Orbit size scales orbit, lids, aperture and eyeball together** (§259). **Placement and spacing are LOCKED**; tolerance OPEN | A, V, O | L787–808, L4181, L4183 |

## 6. External eye (aperture, lids, canthi, folds)

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | Eye-opening asymmetry pair. Lids, canthi and folds SILENT | C | L120 |
| SK | Controls: eye size, angle, lid shape, lid opening | C | L169 |
| SG | Size, corner positions, angle, lid structure; no mandatory eye shape | A, C | L216 |
| FN | Opening, lids. Never anime-like oversized eyes | A, C | L169 |
| AE | Longer and narrower visible eyes than FN; no mandatory almond or oversized shape | A, C | L212; ECR L84 |
| VA | Size, opening, depth, spacing, angle, lids; enormous eyes never required; small-eyed Vael valid | A, C | L252 |
| HV | **External eye is a separate system**. FN/AE ancestry shifts visible presentation; never larger eyeballs by default; no personality in eye anatomy | A | L174–181 |
| DU | Orbit ≠ eyeball ≠ lids ≠ opening; never enlarged or shrunk for effect | A | L179–180 |
| GR | Opening varies; never automatically tiny or squinting | A | L355 |
| GO | Smaller, moderate and larger openings valid; tiny eyes never required | A | L308 |
| PK | **No biologically oversized eyes**; aperture within the MF-compatible adult range; **no separate enlarged-eye envelope** | A | L289, L297 |
| CG | **No oversized eyes**; opening **cannot be enlarged for readability**; lid-fold relationships vary | A, C | L1197–1207, L1543–1544 |
| SA | Somewhat more horizontally extended opening; credible lid closure; "canthal transition" plane. Visible-opening controls operate **inside** the §259 coupling | A, C | L814–835, L680, L826 |

Canthi and named lid folds are SILENT across the roster except SG "corner positions" (L216), CG "lid fold relationships" (L1206) and SA "canthal transition" (L680).

## 7. Ocular anatomy (iris, sclera, pupil, membranes, low-light, magic)

| Race | Iris / pigment | Pupil | Other ocular | Magic ≠ biology | Ref |
|---|---|---|---|---|---|
| MF | Families listed; frequencies OPEN; validity ≠ frequency (A, V, O) | SILENT | — | SILENT | L301–303 |
| SK | SILENT | SILENT | — | SILENT | — |
| SG | Working palette, not final (O) | SILENT | — | SILENT | L232–234 |
| FN | Frequencies OPEN (ECR palette) | Round = conservative baseline (ECR) | Low-light vs humans **OPEN** | ECR: separate | L268; ECR L99, L179, L298 |
| AE | Families listed; never required blue/pale/luminous | ECR round | — | **Explicit split** (A) | L303–312 |
| VA | Families listed incl. muted violet; never glow | Round a candidate; ECR "conservative baseline" | **Low-light mechanism, daylight response OPEN**; no eye shine | Explicit | L252–268, L399, L580 |
| HV | Families by source; **never averaged** | **OPEN**; round a valid candidate | Vael low-light a candidate inherited system (O) | Explicit | L210, L266–274 |
| DU | Families listed; iris internal variation; heterochromia frequency OPEN | Broadly humanoid | Low-light **not granted** (O); sclera not unnaturally white | Explicit | L368 |
| GR | Families listed | **Round** unless biology justifies | Low-light **OPEN**; scleral tint range "comes later" (L524); no nictitating membrane "without approval" (L528) | Explicit | L522–528 |
| GO | Families listed | **Round** | Low-light **OPEN**; scleral tint OPEN | Explicit | L521, L537 |
| PK | Broad range; no colour identifies PK | SILENT | Sclera ordinary humanoid | Explicit; glow not authorized | L353–355, L508–523 |
| CG | Families listed; **no iris-size increase** for readability | SILENT | Sclera plausible | Explicit | L1840–1873 |
| SA | Families listed; iris microanatomy OPEN | **Vertically elliptical, species anatomy; never a human round-pupil toggle**. Saved = shape + dilation range, not state | **Nictitating membrane = species anatomy**; direction/opacity OPEN. No darkvision | Explicit | L1565–1627, L2435–2437 |

## 8. Cheek / zygomatic

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | "Cheeks" region; fullness asymmetry; age affects fullness | C, A | L116–124 |
| SK | More substantial cheeks (tendency); cheekbone width, height, projection, fullness | A, C | L150, L171 |
| SG | Cheekbone height/width, projection, midface depth, fullness | C | L218 |
| FN | Somewhat higher cheekbones (spec); ECR "distinct cheek placement", no universal high cheeks | A, C | L170; ECR L85 |
| AE | Vertically oriented cheek/midface; high/low, broad/narrow, full/hollow | A, C | L213 |
| VA | Strong cheek-midface integration; broader than AE; never gaunt by default | A, C | L241 |
| HV | Midface and cheek inheritance; "high cheekbones" is not a mixed-elf marker | A | L187 |
| DU | Zygomatic breadth, projection, height vary; facial width **never one Face Width scalar** | A, V | L170, L182 |
| GR | **Vertically integrated zygoma** supporting the long midface, not lateral width; projection ≠ width ≠ fullness | A | L358–359 |
| GO | Substantial zygomatic integration **as part of TSC** (placement and continuity, not projection) | A | L310–312, L435 |
| PK | Moderate lateral cheek support; zygoma part of IMFA; **not** a Gorrund transverse band | A, C | L301–305, L401 |
| CG | Readable but fine zygoma; an angled orbit-zygoma junction | A, C | L1213–1218, L1545 |
| SA | **Human zygoma not copied**: a lateral transition zone linking orbit, rostral base, temporal platform and jaw. No cheek control | A | L946–954 |

## 9. Midface

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | Validation row only; no region | V | L248 |
| SK | More substantial midface (tendency); combined with nose controls | A, C | L150, L170 |
| SG | Midface has its own distribution; midface depth control | A, C | L105, L218 |
| FN | Slightly lighter midface; exact ancestral midface E (ECR) | A, O | L170; ECR L85 |
| AE | Vertical midface | A | L213; ECR L85 |
| VA | Stronger midface presence; continuity with cranium | A | L233, L239 |
| HV | Midface height, breadth, projection inherited; intermediate midface valid | A | L166, L187 |
| DU | **Major identifier**: substantial skeletal depth relative to compact facial height; never nasal size; never protruding | A | L183, L244–245 |
| GR | **Locked identifier**: greater midface vertical contribution than MF/SK. **Prognathism distribution OPEN** | A, O | L360–362 |
| GO | Substantial depth across orbit, zygoma, maxilla and nasal root; **prognathism distribution OPEN**; never one Face Depth slider | A, O, V | L304, L312 |
| PK | **Fully mature midface, not shortened**; maxilla and dental arch adult | A, C | L309–313, L403–405 |
| CG | Fully adult midface, not globally shortened; enough vertical contribution to prevent toddler coding | A, C | L1230–1242, L1547–1548 |
| SA | **Midface is the rostrum** (see §10) | A | L663–667 |

## 10. Nasal or rostral anatomy

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | "Nose" region | C | L116 |
| SK | Somewhat larger nose (tendency); bridge, length, projection, tip, nostrils | A, C | L151, L170 |
| SG | Bridge, length, projection, tip, nostrils, alar flare; "each adjustable independently"; no racial nose types | C, V | L217 |
| FN | No mandatory small or straight nose; full control list | A, C | L171 |
| AE | "High Elf = small narrow nose" rejected; full control list | A, C | L214 |
| VA | Somewhat stronger nasal presence than AE; full diversity | A, C | L242 |
| HV | Nasal inheritance; **no universal "half-elf nose"** | A | L188 |
| DU | **Not identified by large noses**; never one Nose Size control; nasal anatomy is individual variation, not a racial identifier | A, V | L184, L252 |
| GR | Never one Nose Size; identity must survive a moderate nose | A, V | L366 |
| GO | Varies; no "ogre nose"; broad face never hard-links to broad nose | A, V | L316 |
| PK | Varies broadly; **small or upturned nose is not a Pipkin trait** | A, C | L311, L404 |
| CG | Variable adult noses; no button or "inventor" nose; nose size alone never carries identity | A, C | L1246–1260, L1549 |
| SA | **Compact projecting rostrum** (primary carrier). Rostral index 0.255–0.335 with a **provisional floor** (L4177; treated as protective canon by the Pass 2 closure and this order); intentional non-overlap with MF/GR/GO. Bounds: length −15/+20 %, base width ±12 %, anterior width ±15 %, depth ±12 %; anterior/base ratio 0.60–0.73. **Nasal openings** on the terminal plane; no nasal pyramid | A, V, C, O | L742–758, L920–942, L4174–4180 |

## 11. Mouth / lips (or homologous oral region)

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | "Mouth and lips" region; mouth-corner asymmetry | C | L116, L120 |
| SK | Region named; no control row or tendency | C | L158 |
| SG | Width, lip fullness, Cupid's bow, projection, corners, philtrum; keeps nose–philtrum–lip–jaw relationships | C, V | L220 |
| FN | Width, fullness, projection, Cupid's bow, philtrum, corners, natural asymmetry | C | L173 |
| AE | Same list; no Aelari lip type | A, C | L216 |
| VA | Same list; no Vael lip type | A, C | L244 |
| HV | Width, volume, philtrum, projection; lips never an ancestry marker | A | L191 |
| DU | Width, volume, philtrum, projection, corners vary | A | L185 |
| GR | Varies; no required huge or downturned mouth | A | L366 |
| GO | Varies; no permanent snarl; no exposed teeth at neutral | A | L316, L320 |
| PK | Varies broadly; lips not sex-locked | A, C | L317, L406 |
| CG | Humanoid adult mouth; no permanent smile | A, C | L1283–1295, L1550–1552 |
| SA | **Mouth line along the rostral jaw; no human lips**. Controls: mouth-line length, corner position. Must still articulate dialogue | A, C, P | L871–889, L1202–1203, L3040–3049 |

## 12. Jaw / mandible

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | "Jaw and chin" region; jaw-contour asymmetry | C | L116, L120 |
| SK | More jaw mass (tendency); no mandatory square jaw; width, angle, depth | A, C | L149, L171 |
| SG | Jaw width, angle, mandibular depth; no mandatory configuration | C | L219 |
| FN | Somewhat lighter jaw than humans; strong-jawed Fenn valid | A, C | L172; ECR L142 |
| AE | Relatively light; broad or muscular Aelari may have substantial jaws | A, C | L215 |
| VA | Somewhat more jaw presence than AE/FN, still elven | A, C | L243; ECR L142 |
| HV | Breadth, ramus, body mass, angle inherited. Elven ancestry may lower mass relative to SK; Vael and Skarn mechanisms differ | A | L189 |
| DU | Substantial presence (tendency); dimensions separate; skeleton ≠ muscle ≠ fat ≠ beard | A, V | L186, L246, L275 |
| GR | Substantial mandible with vertical ramus/lower-face contribution | A | L372–374 |
| GO | Substantial mandible with breadth and depth; posterior jaw takes part in TSC | A | L322–324, L433 |
| PK | Moderately scaled but fully mature mandible; not part of a lateral framework | A, C | L323–332, L407 |
| CG | Mature lower face mandatory; fine but not weak | A, C | L1264–1279, L1553–1556 |
| SA | **Major carrier**: deep posterior attachment. Posterior jaw depth −12/+15 %; a long rostrum requires jaw depth ≥ reference | A, V, C | L858–867, L4174, L4179 |

## 13. Chin

| Race | Requirement | Ref |
|---|---|---|
| MF, SK, SG | Controls within the jaw-and-chin group | MF L116; SK L171; SG L219 |
| FN, AE, VA | All chins valid; never pointed (ECR) | FN L172; AE L215; VA L243; ECR L87 |
| HV | No pointed elf chin, square human chin or intermediate half-elf chin | L190 |
| DU, GR, GO | Varies; no required giant, receding or cleft chin | DU L187; GR L374; GO L324 |
| PK | No pointed "cute" chin; no large chin as an adulthood marker | L329–330 |
| CG | Width, height, projection vary | L1272–1274 |
| SA | **N/A: no human chin prominence on any valid skull** | L865, L4172 |

## 14. External ear / auricular region

| Race | Ear-architecture family and key requirement | Kind | Ref |
|---|---|---|---|
| MF | **Human auricle** (helix, antihelix, concha, tragus, lobe). **"Not pointiness 0–100 %"; never interpolate** | A, V | L307 |
| SK | Human auricle via AC-4 pointer; no ear control row | A | L160 |
| SG | Human auricle via AC-4; elven traits never used to distinguish SG; no ear control row | A, V | L147–149 |
| FN | **Elven continuous taper**; greatest average lateral projection of the three elves (AC-5); 10-variable control list | A, C | L179–187; ECR L328 |
| AE | Elven; more upward/backward orientation, gradual taper; lower lateral projection than FN | A, C | L224–231; ECR L109, L324–332 |
| VA | Elven; broader base, lateral/backward orientation, shorter taper | A, C | L280–286; ECR L110 |
| HV | **Mixed coupled human + elven** whole-ear inheritance; coupled parameters; **"ear length isn't a genealogy meter"** | A, V | L196–206 |
| DU | Broadly humanoid auricle; not pointed; never one Ear Size control; size distributions "future work" | A, V | L195 |
| GR | **Folded cartilage, sustained upper-ear body, later terminal taper, recognizable lobe**; orientation alone never distinguishes it from elves; length ranges OPEN | A, O | L445–459 |
| GO | **Deep bowl, strong antihelical folds, broad continuous rim, close to skull**; no elongated point; projection range OPEN | A, O | L449–458, L350 |
| PK | **Compact rounded auricle**; secondary; overlap with MF/DU allowed; ear mobility OPEN | A, C, O | L338–349, L409, L1540 |
| CG | **Fine folded auricle**; fold clarity, not size; cannot be enlarged for readability; secondary; a **close-view** trait | A, C, P | L1327–1364, L1393, L1594 |
| SA | **Recessed auricular opening; no pinnae**. Controls: opening size, recess depth, rim prominence, orientation; never a human/elf/dragon ear at slider extremes | A, C, V | L974–996, L1212–1215 |

Ear mobility is OPEN for every elf, Halvren and Pipkin, and SILENT elsewhere.

## 15. Teeth / dentition

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF, SK, SG, FN, AE, VA, HV, DU | SILENT | — | — |
| GR | Functional humanoid dentition default; **tusks NOT required**; limited tusk-like canines **OPEN** (separate from GO) | A, O | L368–370, L481 |
| GO | Functional humanoid default; **tusks NOT required**; limited tusk-like canines **OPEN**, kept out of presets, separate from GR | A, O | L316–320, L473 |
| PK | Mature adult dentition; no incisors, tusks or childlike teeth; count OPEN | A, O | L575–583 |
| CG | Functional adult dentition; no rodent or childlike teeth; count OPEN | A, O | L1877–1888 |
| SA | Differentiated dentition, contained in a closed mouth; no tusks, saber teeth or venom fangs; count OPEN | A, V, O | L893–905 |

No race defines a creator-facing dentition control.

## 16. Race-specific cranial structures (displays, keratin, horns)

| Race | Requirement | Ref |
|---|---|---|
| All except SA | SILENT / none. GR ears and GO inner folds are never "horn-like" | GR L451; GO L454 |
| SA | **Cranial Keratin Display System**: the creator analogue of hairstyle. Minimal expression is valid; display is never needed for recognition. Validated families: neutral, minimal ridges, low hornlets, swept-back paired, mixed/asymmetric, restrained crest. Limits: footprint ≥ 0.060; neck clearance ≥ ~7 cm; crest ≈ 2.5 cm; paired-length ratio ≥ 0.70. **Structural ridge = skull (never toggled); keratin ridge = display.** **Navigation may present Cranial Display where haired races present Hair (L2445); where equivalent navigation is required, display occupies that category (L604)** | L1635–1645, L692–694, L604, L2445, L4187–4197 |

## 17. Skin and surface structures that materially alter facial anatomy

| Race | Requirement | Ref |
|---|---|---|
| MF–HV, PK, CG | SILENT as anatomy. Four Skin Appearance Layers; surface never compensates for structure (CG L1600; PK L468) | — |
| DU | Racial structure is **never faked mainly through normal maps, displacement, AO or materials**; depth lives in geometry | L278 |
| GR, GO | Default skin is never warty, rocky or slimy; warts and lesions are not racial | GR L510–512; GO L513 |
| SA | **Field-aware facial scale fields** (eyelids, mouth margins, rostrum-cheek, jaw corners, auricular recess). **No global scale-size control**; expressive fields never coarsen | L1376–1384, L1418, L4205 |

## 18. Natural asymmetry

| Race | Requirement | Ref |
|---|---|---|
| MF | Six L/R pairs (brow height, eye opening, cheek fullness, mouth corner, ear projection, jaw contour) plus Restore Symmetry | L120 |
| SK | Subtle asymmetry plus Restore Symmetry; **Naturalize Face proposed universal, not final until tested** | L183 |
| SG | Carried over from earlier rules (not restated) | L238 |
| FN, AE | Mouth and ear asymmetry plus Restore; no whole-face list | FN L173, L187; AE L216, L231 |
| VA | **Full list**: brow height, eye height/opening, cheek, nose deviation, mouth corner, jaw/chin, ears; Restore; Naturalize Face proposed | L294 |
| HV | Brow, eyes, cheeks, nose, mouth, jaw, chin, ears; never deformity | L192 |
| DU | Subtle-to-moderate; "isn't deformity" | L191 |
| GR, GO | Supported across regions | GR L392; GO L342 |
| PK | **SILENT** | — |
| CG | Valid; subtle independent asymmetry; never implies injury | L1528–1532 |
| SA | Orbital opening, jaw, rostral contour, auricular recess, ridge/display; **distinct from acquired injury**; display paired ratio ≥ 0.70 | L2154–2164, L4194 |

## 19. Age-related facial change

| Race | Requirement | Ref |
|---|---|---|
| All | Faces visibly age while racial anatomy persists; never a wrinkle overlay alone. Lifecycle and lifespan OPEN everywhere | MF L124, L253; SK L179; FN L195; AE L235; VA L290; HV L210; DU L376; GR L532; GO L525–527; PK L385–387; CG L1903–1937; SA L2113–2136 |
| Age triad stated in spec | MF, HV, DU, GR, GO, PK, CG, SA. SILENT in SK, SG, FN, AE, VA (PR L16 governs) | MF L284; HV L303; DU L372; GR L532; GO L527; PK L389; CG L1509; SA L1072 |
| Anti-juvenile | PK and CG must read adult at the youngest adult age without age cues; SA adult controls cannot manufacture juvenile anatomy | PK L385; CG L1903–1912; SA L2088–2094 |
| Anti-caricature | GO aging never an ogre caricature; GR never "troll aging"; DU age never raises depth classification | GO L525; GR L532; DU L377 |

## 20. Sex-related facial tendency

| Race | Canon | Ref |
|---|---|---|
| MF, SK, SG, FN, AE, VA | SILENT. Under R-SEX, "no shift" is a valid complete state | PR L65–71 |
| HV | Sex-related anatomy stays separate from the face; the system is a Class B source dependency (never invented in Halvren) | L54, L493 |
| DU, GR, GO | **OPEN**; human dimorphism is never assumed to transfer | DU L58; GR L431; GO L411 |
| PK | May influence facial relationships; **magnitude OPEN**; like-for-like tests PIP-FACE-22/23 | L72, L1485, L1539 |
| CG | May affect craniofacial relationships; **not a binary set of faces**; magnitude OPEN; a "sex-related anatomy" control capability is listed | L1490–1505, L1560 |
| SA | **CLOSED: no craniofacial sex shift**; skull, face and display family are sex-neutral | L1057, L4216, L4251 |

## 21. Facial-hair biology (including eyebrows)

| Race | Requirement | Ref |
|---|---|---|
| MF, SK, SG | Facial hair is presentation; style, length, density, colour; never identity | MF L177; SK L191, L224; SG L277 |
| FN | SILENT (ECR: not prohibited for any elf) | ECR L175 |
| AE, VA | Neither required nor prohibited | AE L336; VA L395 |
| HV | Follows ancestry distributions; density never reveals ancestry percentage | L210, L262 |
| DU | Biology separate from beard culture; **zero required information**; clean-shaven Durrim fully valid; sex distributions OPEN | L203–207, L252 |
| GR, GO | **Zero required recognition**; biology separate from style | GR L402; GO L365 |
| PK | Variable capability; never required for adult read | L367–373 |
| CG | May grow; never mandatory; eyebrows vary; FD-HAIR includes eyebrows | L1800–1834, L2044 |
| SA | **Biologically empty**: no facial hair; eyebrows not transferable; Facial Hair category empty | L1915–1919, L2445 |

Eyebrows as hair biology are SILENT in MF, SK, SG, FN, AE, VA and HV.

## 22. Inherited / mixed development (Halvren)

Full detail is in `reviews/ufca-evidence/halvren.md` §21a–21i. Requirements the architecture must carry:

| # | Requirement | Ref |
|---|---|---|
| H1 | No arithmetic averaging; no 50/50 default; non-midpoint, multigenerational expression | L13, L315, L357 |
| H2 | Developmental coherence: coupled regional expression, "mosaic without patchwork" | L31, L41, L166 |
| H3 | Candidate soft inheritance clusters: craniofacial (cranium, orbits, midface, jaw) and external ear. These are **not creator sliders** | L33–41 |
| H4 | **Genealogy (A) ≠ ancestry-derived constraints (B) ≠ phenotype (C)**. Editing phenotype never rewrites genealogy; a genealogy control is never an appearance slider | L463 |
| H5 | **No Elf Percentage, lifespan-percentage, skull-interpolation, pointiness or single "eye" control** | L58, L181, L196, L321 |
| H6 | **Source-race protection**: no unrestricted route that exactly recreates another population's complete face | L82, L141, L227 |
| H7 | Source-first rule: Halvren never invents source biology | L495–497 |
| H8 | Preset codes A–M; I–M (source-influenced) are internal validation labels only; presets never assert genealogy | L327–343, L463 |

## 23. Locked validation tests touching the face (carry-forward inventory)

| Race | Test IDs and named tests |
|---|---|
| MF | Stage B identity; Face test (L248); Identity stress (L249); Age validation (L253); preset round-trip; randomization sample (L257) |
| SK | SK-01, SK-02, SK-09, SK-10, SK-11, SK-12; expression test (L187); silhouette (L284); 190 cm equal-height (L288); anti-stereotype (L292) |
| SG | SG-10…14; large-sample 100/100/100 (L356); clone/stereotype (L368); cultural neutralization (L383); facial animation (L439); elf boundary (L461) |
| FN | FN-10, FN-18…27, FN-32…34, FN-37…38; hidden-ear facial (L211); hidden-ear population (L349); final gate (L517–536) |
| AE | AE-25…36, AE-39…50; generic-elf convergence (L464); Sagekin boundary (L478) |
| VA | VL-14, VL-25…43, VL-50…60; hidden-ear neutral-complexion (L298); low-light set (L272); cliché convergence (L490) |
| Elves (ECR) | Three-elf neutral face; ear-only distribution; human boundary; expression neutrality (ECR L122–125) |
| HV | Hidden-ear; ear-only; equal face structure; strong-expression stress; anti-beauty; anti-generic-half-elf (L218–223); HV-01…48; HV-FAMILY-01/02 |
| DU | Hidden-beard, hidden-ear, nose/jaw/brow neutralization, beauty, sex-stereotype, age, equal-height face, population sampling (L213–222); no single-feature dependency (L252); DU-FACE-01…11; DU-DEPTH-01…03; depth tests (L308–316) |
| GR | GR-FACE-01…13; GR-EAR-01…04; test table (L412–427); Part 4/5 recognition tests; AD-2/AD-3 (L712–713) |
| GO | GOR-FACE-01…15; GOR-EAR-01…06; test table (L394–407); TSC and lighting tests (L554–555); minimum-stereotype (L684); AD-1 (L271) |
| PK | PIP-FACE-01…23; combined stress (L444–453); PIP-SURF-09…21; PIP-INT-04, 08, 12, 15–17 |
| CG | COG-FACE-01…25 (with 21A); relationship rejections (§101); COG-SURF-05…17; COG-CC-04, 06, 10, 12, 15 |
| SA | SAU-FACE-01…23; SAU-SURF-04, 12–14, 19–20, 25–26, 28; SAU-CC-01…28 (face-relevant subset); SAU-MOVE-11; SAU-EQP-01; SAU-CAM-02; SAU-GAME-04 |

UFCA-06 assigns every entry to a validation tier. None is replaced.

## 24. Explicitly OPEN facial biology (not resolved by UFCA)

| Topic | Races | Ref |
|---|---|---|
| Low-light / visual adaptation | FN, VA, HV (Vael-derived), DU, GR, GO | FN L268; VA L258–260; HV L210; DU L368; GR L528; GO L521 |
| Pupil morphology | VA, HV (round = conservative baseline, ECR L99) | VA L259; HV L274 |
| Prognathism / maxillary–mandibular projection distribution | GR, GO | GR L362; GO L312 |
| Tusk-like canines (separately) | GR, GO | GR L370; GO L320, L473 |
| Dentition count and replacement | GR, GO, PK, CG, SA | — |
| Ear mobility | FN, AE, VA, HV, PK, CG | — |
| Ear length / projection ranges | GR, GO (OPEN); DU ("future work") | GR L398; GO L350; DU L195 |
| Sex-related facial magnitude | DU, GR, GO, PK, CG (SA closed) | — |
| Head-to-stature ratio | GR, GO, PK, CG | — |
| Scleral tint range | GO (OPEN); GR ("comes later") | GO L521; GR L524 |
| Nictitating direction, opacity, triggers; iris microanatomy; pupil dynamics; orbital spacing tolerance; structural-ridge numerics; scale-field numerics; display mass-moment and ROM clearance; displays beyond validated families and crests above ~2.5 cm; cross-race numeric rostral check | SA | L1617, L4024, L4183, L671, L4205, L1637, L4177, L4262, L4265 |
| Exact craniofacial distributions (cranial ratios, facial thirds, orbit, aperture, zygoma, midface, nose, mandible/chin, ear) and facial-animation implementation | CG | §103 L1665–1683; §207 L3196 |
| Facial flushing / blood biology | GO, GR | GO L506, L511; GR L732 |
| Face technical architecture (topology, morphs, bones, head meshes) | DU, GR, GO, HV and others | DU L226; GR L431; GO L411; HV L227 |
| Iris, hair and facial-hair frequencies | All races with palettes | — |
| Lifecycle and aging rate | All | — |
| Universal facial-control architecture | Named as OPEN carry-forward in DU L234 and SA L4271 (this phase) | — |

## 25. Measurement-deferred items

No race spec carries an RM-* reference for the face. The Pass 2 queue (`reviews/claude-pass2-r5-reference-mesh-queue.md`) holds the facial items:

| Item | What it measures |
|---|---|
| RM-CF-01…05 | Saurin rostral cross-race closure |
| RM-CF-06 | CBH and TBP (Durrim, Gorrund) |
| RM-CF-07 | FVB with MVI (Grask verticality) |
| RM-CF-08 | ORB, IOD and aperture (elves, Saurin) |
| RM-CF-09 | Skarn tendencies |
| RM-CF-10 | HSR |
| RM-SR-04 | Anti-juvenile head share, FVI, orbit vs aperture (Pipkin, Cogling) |
| RM-SR-05 | Durrim depth domains |
| RM-OT-04 | Saurin vs Sagekin/Halvren (face) |

UFCA-07 proposes additions only where a semantic variable has no queue item.

## 26. Cross-cutting findings from extraction (inputs to UFCA-02…08)

| # | Finding |
|---|---|
| X-1 | Every race separates **bony orbit**, **visible aperture** and (where stated) **eyeball**. Saurin is the one race that **couples** orbit → lids, aperture and eyeball. The concepts are universal; the coupling is race-specific |
| X-2 | Eight ear-architecture families exist (Pass 2 report 03 §5). Ear controls cannot be one parameter set |
| X-3 | Multidimensionality bans recur: no Face Width (DU), Nose Size (DU, GR), Ear Size (DU), Face Depth (DU, GO), verticality ratio (GR), TSC slider (GO), global scale size (SA), master race face (PK, CG, GR, GO, HV) |
| X-4 | Pass 1 control lists use different granularity. MF uses 7 regions; SK 4 rows; SG and the elves 6–8 rows; PK 15 families; CG 24 capabilities; SA 6 groups plus display, eye and scale sets; GR and GO coverage lists only; DU none. UFCA-08 Appendix A gives each item a disposition |
| X-5 | "Eye size" (SK L169, SG L216, VA L252) is ambiguous against the roster-wide orbit ≠ aperture ≠ eyeball rule and the ECR terminology rule (ECR L51, L145). A disposition is proposed in UFCA-03 and flagged for author confirmation |
| X-6 | Saurin §73 lists "orbital spacing" as a control, but §259 L4183 locks it. Later canon governs, so the control is not exposed |
| X-7 | Coverage silences where anatomy is stated but no Pass 1 control exists: MF forehead, orbit and midface; SK mouth/lips and ears; SG ears; FN forehead and brow height; PK asymmetry; SA cheek and forehead. UFCA-07 handles these without inferring anatomy |
| X-8 | Only Saurin has species-anatomy ocular features that need creator handling (vertical pupil with dilation range; nictitating membrane). Every other pupil is round or OPEN |

— Claude

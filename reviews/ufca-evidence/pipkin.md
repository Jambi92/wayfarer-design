> UFCA Phase 1 evidence appendix to `reviews/claude-ufca-01-requirements-matrix.md`. Line references are to the canonical race spec as of commit c076294. Extraction only: no canon is changed, and nothing here is new anatomy. Tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] dependency/validator · [PRES] presentation · [DIAG] measurement/diagnostic · [OPEN] open/not authorized.

# UFCA-01 evidence — Pipkin (specs/pipkin/PIPKIN_V1.md, 1670 lines)

Status: Pipkin v1.0 FIRST-PASS COMPLETE (L3, L1670). Part 3 (craniofacial) FIRST-PASS ACCEPTED (L461). Facial controls = "APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION pending the universal Facial Customization Architecture Review" (§15, L393). Spec read in full (L1–L1670).

Identity hierarchy (§30, L1494–1502): Primary = Low-Set Compact Trunk Architecture (body); Supporting facial identity = Integrated Mature Facial Architecture (IMFA); ears/surface = secondary tendencies; hair, facial hair, eye colour etc. = not identifiers. Face is "supporting rather than universally exclusive" (L461).

## 1. Cranial vault / cranial proportions
- [ANAT] Head contribution: Pipkin "may trend toward somewhat greater head contribution to total stature than the Marchfolk Human Reference Population ... but the head is **secondary** and never oversized" (Part 3 §3, L279). Earlier: never "oversized 'cute halfling head' (ratio **OPEN**)" (Part 1 §5–11, L33).
- [ANAT] "The cranial vault must not be enlarged relative to the mature face as a shortcut to small-race identity." (L279)
- [ANAT] Cranial breadth, cranial length, vault height, forehead height/slope, posterior cranial projection and cranial-base relationships "vary independently within validity"; central tendency "may support moderate breadth, but broad and narrow adult Pipkin heads are both valid" (L281).
- [ANAT] Narrow-headed Pipkin remain Pipkin through mature facial integration; broad-headed Pipkin "must not become Durrim through cranial breadth alone" (L283).
- [ANAT] IMFA anchor: "a moderately broad but variable cranial base transitions through the temple and zygomatic region into a fully developed central midface ..." (§2, L259). Sequence: "moderate cranial base → temple/zygoma → central midface integration → mature adult lower-face framework" (L265).
- [ANAT] "Craniofacial depth relative to facial height stays within the broad Marchfolk adult range rather than trending toward Durrim depth-dominance." (L267)
- [ANAT] "Greater relative head contribution is NOT a Pipkin maturity signal and must never be used to distinguish an adult Pipkin from a human child." (Part 2, L199). Earlier brief phrase "large head" SUPERSEDED (L201–203).
- [ANAT] Head equipment must not "enlarge the head to create a 'halfling' silhouette" or "compress the cranium"; "Hair-volume accommodation is a fit problem, not justification to alter skull size." (Part 6 §8, L1205–1211)
- [OPEN] Head-to-body ratio (L33, L125); "final head-to-body ratio envelope" (§32, L1528).

## 2. Forehead
- [ANAT] "Forehead height, slope and curvature vary broadly. Pipkin do not require a high childlike forehead, a heavy brow, or a permanently soft brow." (§4, L287)
- [ANAT] IMFA compactness comes partly from a "restrained forehead-to-brow/lower-face soft-tissue vertical envelope, not from juvenile shortening" (L259); but later clarified: "The facial vertical envelope is primarily skeletal (forehead height, brow position and lower-face skeletal relationships); soft tissue may modulate but never create or erase Pipkin identity." (L461) — see Extraction notes.
- [CTRL] Control family "forehead height/slope" (§15, L397).

## 3. Brow / supraorbital
- [ANAT] No heavy brow and no permanently soft brow required (L287).
- [ANAT] Brow projection varies independently within coherent limits (L289); adult maturity must survive "lower-valid brow projection" (L294).
- [ANAT] Part 2 forbids relying on "severe features" for adult read (L201).
- [CTRL] "brow and orbital dimensions" (L398).

## 4. Orbit
- [ANAT] "Orbital size means skeletal orbital dimensions; visible eye opening is separate." (L289)
- [ANAT] Orbital breadth/height, interorbital spacing, orbital depth vary independently within coherent limits (L289).
- [ANAT] "No combination may require giant eyes, wide-eyed expression or infant-like orbital proportions. 'Larger-valid' Pipkin orbital dimensions and visible eye aperture must remain within the broad adult Marchfolk-compatible range relative to the face; the Pipkin system does not create a separate enlarged-eye envelope." (L297)
- [CTRL] "brow and orbital dimensions", "interorbital spacing" (L398–399).

## 5. External eye (aperture, lids, canthi, folds)
- [ANAT] "Pipkin **do not possess biologically oversized eyes**." (L289)
- [ANAT] Upper/lower lid exposure and visible aperture vary independently (L289). Maturity must survive larger-valid and smaller-valid visible eye openings (L292–293).
- [ANAT] No separate enlarged-eye envelope; aperture within broad adult Marchfolk-compatible range (L297).
- [ANAT] Age may later affect "orbital exposure" (§14, L387).
- [ANAT] Eyelash density/length vary within plausible adult anatomy and "are never used as sex or youth shorthand" (L379); "Long lashes are not sex-locked; sparse lashes are not age-locked. Neither is a maturity signal." (Part 4 §9, L545)
- [CTRL] "visible eye aperture" (L400).
- Canthi / epicanthic or other folds: SILENT.

## 6. Ocular anatomy
- [ANAT] "Eye color is biological pigmentation and separate from magical eye effects and observed lighting appearance." Broad natural fantasy-humanoid iris range; "no eye color is required for racial recognition." (§10, L353)
- [ANAT] "Iris color, limbal appearance, scleral appearance and visible eye aperture are separate systems." (L355)
- [OPEN] Magical-vs-biological: "Part 3 does not authorize glowing eyes or magical ocular effects as racial biology." (L355)
- [ANAT] Iris pigmentation separate from pupil size, scleral appearance, limbal appearance, visible aperture, ocular wetness/highlights, magical glow/emissive effects, and lighting (Part 4 §5, L508–515). "No eye color identifies a Pipkin." (L517)
- [ANAT] "ordinary healthy humanoid scleral and conjunctival anatomy unless a later universal rule establishes otherwise"; subtle variation with vascularity, pigmentation, age, fatigue, environment (§6, L521). "Pure-white stylized sclera, permanent redness, unusual glow, black sclera or other supernatural appearances are not implied by race." (L523)
- [OPEN] Iris validity limits, rare colours, population frequencies OPEN for cross-race pigmentation review (L506; §32 L1542–1543).
- Pupil shape / nictitating membrane / low-light adaptation: SILENT.

## 7. Cheek / zygomatic
- [ANAT] "The zygomatic and temporal regions provide a major part of Integrated Mature Facial Architecture. Pipkin may trend toward **moderate lateral cheek support relative to facial size** ... without requiring broad external cheeks." (§5, L301)
- [ANAT] "Zygomatic breadth, projection and vertical position are separate. Temporal breadth and hollowing vary with skeletal anatomy, age and composition. Soft-tissue cheek fullness is not the racial anchor." (L303)
- [ANAT] Gorrund separation "by **relationship**, not scale": Pipkin lateral support follows "cranial base → temple → zygoma → central midface"; "posterior mandible and ramus do not participate in a continuous Pipkin lateral framework, and the lateral orbital margins and zygomatic arches do not form the Gorrund continuous transverse band." (L305)
- [ANAT] Rosy cheeks "**not** Pipkin biology" (Part 4 §4, L500).
- [CTRL] "zygomatic breadth/projection/height", "temporal breadth" (L401–402); "soft-tissue facial composition where appropriate" (L410).

## 8. Midface
- [ANAT] "Pipkin have a fully mature adult midface. Midface height itself is not required to be shortened." Maturity-bearing structures (nasal bridge, maxillary projection/depth, dental-arch support) remain adult; "racial compactness is produced by the broader cranial-base-to-central-face organization and overall adult facial envelope, not juvenile midface reduction." (§6, L309)
- [ANAT] "Pipkin identity never depends on a shortened muzzle-like facial plane, flattened midface, or childlike dental region." (L313)
- [ANAT] IMFA: "Mandibular ramus height, nasal bridge development, maxillary and dental-arch depth, and adult gonial definition never become juvenile in order to create the racial read." (L267)
- [CTRL] "midface height/projection" (L403); "maxillary projection" (L405).

## 9. Nasal
- [ANAT] "Nasal root height, bridge height, bridge breadth, nasal length, projection, tip shape, alar breadth and nostril geometry vary broadly. **A small or upturned nose is not a Pipkin trait.** Large, long, broad, narrow, projecting and subtle adult noses are all valid when anatomically coherent." (L311)
- [ANAT] Adult read must not rely on "a large nose" (L201).
- [ANAT] Rosy nose coloration not Pipkin biology (L500).
- [CTRL] "nasal root/bridge/length/projection/alar dimensions" (L404).

## 10. Mouth / lips
- [ANAT] "Mouth width, lip volume, vermilion shape, philtrum length/depth and oral projection vary broadly. Full lips, thin lips and intermediate forms are valid and are not sex-locked or race-defining." (§7, L317)
- [ANAT] "The lower face must carry adult maturity through coordinated maxillary, mandibular and chin development." (L319)
- [ANAT] Natural lip pigmentation varies, "not a cosmetic layer"; "Permanent unusually saturated fantasy coloration is not inferred from race." Cosmetic lip colour = presentation (Part 4 §14, L587–589).
- [CTRL] "mouth/lip/philtrum dimensions" (L406).

## 11. Jaw / mandible
- [ANAT] "Mandibular breadth, ramus height, body depth, gonial shape, chin width, chin height and projection vary independently within validity." (§8, L323)
- [ANAT] Not required: "a heavy Durrim-like jaw, a tiny childlike jaw, an exaggerated square jaw, a pointed 'cute' chin, or a large chin as an adulthood marker." (L325–330)
- [ANAT] "The reference tendency is a **moderately scaled but fully mature mandible integrated closely with the compact midface**. Adult read comes from maturity of relationships, not massiveness." (L332)
- [ANAT] Soft-featured Pipkin "may have a modest chin and lighter jaw while still showing mature proportions" (L319). Adult read must not rely on "a heavy jaw" (L201).
- [ANAT] Posterior mandible/ramus not part of a lateral framework (anti-Gorrund) (L305).
- [CTRL] "mandibular breadth/ramus/body depth" (L407).

## 12. Chin
- [ANAT] Chin width/height/projection vary independently (L323); no pointed "cute" chin, no large chin as adulthood marker (L329–330); modest chin valid for soft-featured adults (L319).
- [CTRL] "chin width/height/projection" (L408).

## 13. External ear
- [ANAT] Ears "sit within the broader adult humanoid ear range"; central population tendency, "not a primary racial identifier" (§9, L336).
- [ANAT] "Pipkin ears trend toward a compact rounded auricular architecture: moderate overall projection, a rounded-to-softly-angular upper contour, a proportionally clear but not deep conchal bowl, continuous moderate helix definition, and a compact attachment that integrates closely with the side of the head." (L338)
- [ANAT] Variation: "ear height, breadth, projection, rotation, helix thickness, antihelix definition, conchal depth, tragus/antitragus prominence and lobule size/attachment." (L340)
- [ANAT] Locked exclusions: "no elven terminal point, no Grask robust folded terminal taper, no Gorrund deep broad bowl/strong load-bearing-looking folds, no mandatory tiny ears, no mandatory protruding 'comic halfling' ears." (L342–347)
- [ANAT] "Ear shape is secondary and may overlap Marchfolk and Durrim humanoid ear variation. No unique ear feature is required for Pipkin recognition. Hiding the ears must not erase Pipkin facial identity." (L349)
- [ANAT] Helmet/hood clearance must respect valid auricular dimensions/placement; headgear must not "rely on ear visibility for racial recognition" (Part 6 §8, L1203–1209).
- [CTRL] "ear height/breadth/projection/rotation/fold architecture" (L409).
- [OPEN] "Pipkin ear mobility; no racial mobility behavior is approved at first pass" (§32, L1540).

## 14. Teeth / dentition
- [ANAT] "Pipkin possess a mature adult humanoid dentition appropriate to their approved jaw architecture." (Part 4 §13, L575)
- [ANAT] "**Pipkin do not have biologically oversized incisors, tusks, fangs, rodent-like teeth or childlike dentition.**" (L577)
- [ANAT] Tooth size coordinates with mature maxillary/mandibular arches; natural variation in size, shape, spacing, alignment, coloration (L579). "Extreme stylized perfect whiteness is not biological default. Wear, staining, loss, restoration and damage belong to age/history/health systems" (L581).
- [ANAT] First-pass dentition "follows the existing functional adult humanoid first-pass default used elsewhere in the project without inferring diet, culture or specialized feeding anatomy." (L583)
- [OPEN] "Exact tooth count, replacement pattern and lifecycle details remain **OPEN**." (L583; §32 L1545)
- [ANAT] Age may later affect "tooth wear" (L387). Anti-caricature: never "rodent-like teeth" (L1517).
- Creator dentition controls: SILENT (no dental control family listed in §15).

## 15. Race-specific cranial displays / keratin / horns
- N/A — SILENT (no displays, crests, horns or keratin structures in spec).

## 16. Skin/surface structures that materially alter facial anatomy
- SILENT as to structures altering facial anatomy. Surface phenotype is explicitly non-structural: "Part 4 defines visible biological variation that sits **on top of** the approved Pipkin skeletal and craniofacial systems" (L468).
- [ANAT] Freckles never a hallmark; "No 'freckled halfling' default" (L494–496). Skin pigmentation not a racial identifier (L377, L476).
- [ANAT] Skin Appearance Layers 1–4 (Natural / Environmental / Applied / Acquired) must remain distinguishable (L607–613).
- [DIAG] FD-SURF = facial skin surface (L625).

## 17. Natural asymmetry
- SILENT.

## 18. Age-related facial change (age triad)
- [ANAT] "Adult Pipkin must read adult at the youngest valid adult apparent age without wrinkles, gray hair, facial hair, scars or weathering." (§14, L385)
- [ANAT] "Age can later affect skin texture, soft-tissue distribution, orbital exposure, facial volume, hairline, pigmentation, tooth wear and other features, but aging must not be the mechanism that makes the race look mature." (L387)
- [ANAT] Age triad: "Chronological Age, Apparent Biological Age and Age Presentation remain separate concepts." (L389; restated Part 6 §28, L1477)
- [ANAT] "Apparent Biological Age and surface aging are related but not identical. A younger-looking adult must remain structurally mature without wrinkles, while an elder Pipkin must remain recognizably Pipkin beneath age-related surface and soft-tissue change." (Part 4 §16, L603)
- [ANAT] Graying/premature graying valid individual variation (L363, L529); temple recession and age-related thinning vary (L359).
- [ANAT] Temporal hollowing varies with age (L303).
- [ANAT] "age presentation cannot substitute for biological maturity" (L1474).
- [OPEN] Lifecycle timing / age-frequency OPEN (L603, L1470, L1479, L1541).

## 19. Sex-related facial tendency
- [OPEN] Part 1: "Sex-related anatomy and dimorphism are **OPEN**, never assuming human proportions transfer or encoding exaggerated dimorphism." (L72)
- [ANAT] Part 6 §29: "Sex-related physical anatomy may influence relevant pelvic, thoracic, facial, soft-tissue and other biological relationships", but does not determine height, frame, hair etc.; like-for-like comparisons used (L1485–1488). No specific sex-related facial tendency is stated.
- [ANAT] Lips "not sex-locked" (L317); lashes "never used as sex ... shorthand" (L379, L545).
- [OPEN] "magnitude and morphology of sex-related dimorphism" (L1539); "Exact creator-facing control organization remains subject to the universal architecture review." (L1490)
- [VAL] PIP-FACE-22/23 like-for-like sex comparisons (L439–440).
- No explicit "R-SEX" label in spec.

## 20. Facial hair biology (incl. eyebrows)
- [ANAT] "Facial-hair capability is biologically variable and must not be required for adult male recognition or adult recognition generally." (§12, L367)
- [ANAT] Valid outcomes: "little facial hair, patchier growth, mustache-dominant patterns, chin/jaw-dominant patterns, broad beard coverage and age-related changes." (L369)
- [ANAT] "Pipkin do not biologically require Durrim-like beard prominence, elaborate beards, sideburns, mustaches or 'halfling whiskers.' Grooming is Personal Presentation." (L371)
- [OPEN] "Sex-related facial-hair distributions and hormonal relationships remain **OPEN** pending universal review and must use soft biological correlations rather than hard presentation locks." (L373; §32 L1546)
- [ANAT] Facial-hair pigmentation/texture follow hair biology "without requiring an exact match to scalp hair"; "Facial hair never supplies Pipkin racial identity or adulthood." (Part 4 §10, L549–553)
- [ANAT] Eyebrows: "Eyebrow density, thickness, shape and growth direction vary; brow grooming is presentation." (L379). "Brow shape may be influenced by underlying anatomy but grooming remains presentation." (L543)
- [ANAT] Scalp hair: density, strand diameter, curl pattern, growth direction, hairline geometry, widow's peak, temple recession, age-related thinning vary independently; "No hairstyle is biological." (L359–361)
- [PRES] Shaving, trimming, braiding, waxing, styling, ornamentation = presentation (L551).
- [DIAG] FD-HAIR = eyebrows/facial/scalp hair (L625).

## 21. Inherited / mixed development
- N/A (Halvren only). Pipkin note: "Mixed ancestry never defines Pipkin" (L93).

## 22. Locked validation tests touching the face
Part 3 cast (§16, L416–440):
- [VAL] PIP-FACE-01 reference adult, neutral hair/presentation; unmistakably mature and Pipkin (L418)
- [VAL] PIP-FACE-02 youngest valid adult apparent age, no facial hair/wrinkles; still adult (L419)
- [VAL] PIP-FACE-03 soft-featured, low brow and mandibular mass; never childlike (L420)
- [VAL] PIP-FACE-04 angular/severe; never Durrim or Gorrund (L421)
- [VAL] PIP-FACE-05 narrow-valid cranium/face; still Pipkin (L422)
- [VAL] PIP-FACE-06 broad-valid cranium/face; not Durrim (L423)
- [VAL] PIP-FACE-07 larger-valid eye aperture + modest jaw/chin; critical anti-child (L424)
- [VAL] PIP-FACE-08 smaller-valid aperture + stronger jaw/chin; identity survives (L425)
- [VAL] PIP-FACE-09 small/subtle nose; never child-coded (L426)
- [VAL] PIP-FACE-10 large/projecting nose; no caricature (L427)
- [VAL] PIP-FACE-11 low cheek soft tissue, clear skeletal integration (L428)
- [VAL] PIP-FACE-12 high cheek soft tissue; identity not dependent on round cheeks (L429)
- [VAL] PIP-FACE-13 ears hidden; face remains Pipkin (L430)
- [VAL] PIP-FACE-14 maximum-valid ear projection; no comic-halfling read (L431)
- [VAL] PIP-FACE-15 minimal facial hair; adult recognition unchanged (L432)
- [VAL] PIP-FACE-16 dense facial hair; underlying face valid (L433)
- [VAL] PIP-FACE-17 vs human child at similar head size; critical maturity (L434)
- [VAL] PIP-FACE-18 vs normalized Marchfolk, hairstyle/ears hidden (L435)
- [VAL] PIP-FACE-19 vs Durrim at normalized head size (L436)
- [VAL] PIP-FACE-20 vs Gorrund; no Transverse Structural Continuity (L437)
- [VAL] PIP-FACE-21 vs Fenn, ears/hairstyle hidden (L438)
- [VAL] PIP-FACE-22 adult male Pipkin vs adult male Marchfolk; no exaggerated dimorphism (L439)
- [VAL] PIP-FACE-23 adult female Pipkin vs adult female Marchfolk; no juvenile or cross-sex coding (L440)
Combined stress tests (§17, L444–453) [VAL]: broad cranium+soft jaw+large aperture+young adult (L444); narrow cranium+small nose+low facial hair (L445); broad zygomatics+high cheek fat ≠ round-face stereotype (L446); strong mandible+broad cranium+dense facial hair ≠ Durrim (L447); low ear projection+ears obscured (L448); high ear projection+rounded contour ≠ comic (L449); **lower-valid midface height + larger eye aperture: critical anti-child** (L450); greater head contribution + youngest adult (L451); broad cranium+greater facial depth+strong mandible ≠ Durrim depth-dominance (L452); broad cranium+broad zygomatics+strong ramus ≠ Gorrund TSC (L453).
Face-touching tests elsewhere:
- [VAL] PIP-BODY-15 / Part 2 child test: maturity "Never relying mainly on the head" (L116, L191).
- [VAL] PIP-SURF-09 early gray on younger adult (L651); PIP-SURF-10/11 facial hair (L652–653); PIP-SURF-14 iris extremes (L656); PIP-SURF-15 teeth variation, no caricature (L657); PIP-SURF-16 ears hidden, hair removed, neutral surface; structural identity survives (L658); PIP-SURF-17 lighting variation (L659); PIP-SURF-18/19/20 surface overlap with Marchfolk/Durrim/Fenn (ears obscured for Fenn) (L660–662); PIP-SURF-21 elder (L663). Part 4 stress: young adult+no facial hair+smooth skin+larger-valid aperture (L670); gray hair+smooth skin (L671); FD-SURF vs FD-OBS distinguishable (L672).
- [VAL] PIP-MOVE-20 dialogue eye lines (L1062); Part 5 stress "Oversized chair + dangling feet + youthful-looking face" (L1073).
- [VAL] PIP-INT-04 face-only normalized comparison with Marchfolk, Durrim, Fenn, Gorrund (L1592); PIP-INT-08 helmet/hood fit across cranial, hair, ear variation (L1596); PIP-INT-12 creator camera (L1600); PIP-INT-15 selective randomization (L1603); PIP-INT-16 youngest adult (L1604); PIP-INT-17 elder (L1605).
- [DIAG] Facial Diagnostic Domains FD-STRUCT, FD-SOFT, FD-SURF, FD-HAIR, FD-PRES, FD-OBS "so failures are assigned to the correct domain" (L455; meanings restated L625).

## 23. Explicitly OPEN biology touching the face
- [OPEN] Head-to-body ratio / envelope (L33, L1528).
- [OPEN] Face, ears, eyes, hair, pigmentation listed OPEN in historical Part 1 list (L125) — superseded by Parts 3–4 and §32 (L125 says "Part 6 §32 governs").
- [OPEN] Sex-related dimorphism magnitude/morphology (L72, L1539); sex-related facial/body-hair distributions (L373, L1546).
- [OPEN] Ear mobility (L1540).
- [OPEN] Iris/hair/pigmentation population frequencies, rare iris/hair validity (L506, L1542–1543).
- [OPEN] Dentition count/replacement/lifecycle (L583, L1545).
- [OPEN] Lifecycle / age-frequency (L1541).
- [OPEN] Glowing/magical ocular effects not authorized (L355).
- [OPEN] "final creator-facing facial-control organization" (L1550).

## 24. Pass 1 provisional creator-control list (face)
Status: "APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION pending the universal Facial Customization Architecture Review" (L393). "Required independent or relationship-aware control families" (L395–410):
- [CTRL] cranial breadth/length/vault height (L396)
- [CTRL] forehead height/slope (L397)
- [CTRL] brow and orbital dimensions (L398)
- [CTRL] interorbital spacing (L399)
- [CTRL] visible eye aperture (L400)
- [CTRL] zygomatic breadth/projection/height (L401)
- [CTRL] temporal breadth (L402)
- [CTRL] midface height/projection (L403)
- [CTRL] nasal root/bridge/length/projection/alar dimensions (L404)
- [CTRL] maxillary projection (L405)
- [CTRL] mouth/lip/philtrum dimensions (L406)
- [CTRL] mandibular breadth/ramus/body depth (L407)
- [CTRL] chin width/height/projection (L408)
- [CTRL] ear height/breadth/projection/rotation/fold architecture (L409)
- [CTRL] soft-tissue facial composition where appropriate (L410)
- [VAL] "There is no 'Pipkin Face' master slider. Validity is relationship-aware. Population tendencies may bias randomization without forcing creator controls to move together." (L412)
- [PRES] Brow grooming, facial-hair grooming, hairstyle, cosmetic lip colour, dye, tattoos = presentation (L371, L379, L531, L551, L589, L597).
- [PRES] Creator camera: face views may use purpose-specific framing; "Camera framing is presentation, not anatomy." (§15, L1300–1304)

## 25. Prohibited controls and anti-patterns
- [VAL] No "Pipkin Face" master slider (L412); no "human → Pipkin" master slider (Part 2, L205).
- [ANAT] Never juvenile: "no oversized cranium, huge eyes, tiny jaw, extremely short face" (L33).
- [ANAT] No oversized "cute halfling head" (L33); "large head" superseded (L201–203).
- [ANAT] Adult read must not rely on facial hair, wrinkles, severe features, a large nose or a heavy jaw (L201).
- [ANAT] No giant eyes, wide-eyed expression, infant-like orbital proportions, separate enlarged-eye envelope (L297).
- [ANAT] No small/upturned nose as trait (L311); no shortened muzzle-like facial plane, flattened midface, childlike dental region (L313).
- [ANAT] Jaw exclusions (L325–330).
- [ANAT] Ear exclusions (L342–347).
- [ANAT] No oversized incisors, tusks, fangs, rodent-like teeth, childlike dentition (L577).
- [ANAT] No rosy cheeks/nose biology (L500); no "freckled halfling" default (L496); no "halfling whiskers" (L371).
- [ANAT] Consolidated anti-caricature (§31, L1506–1520): never "oversized head or eyes; tiny jaw or juvenile midface; ... rosy/freckled/fair default phenotype; ... rodent-like teeth".
- [VAL] Randomization hidden packages forbidden incl. "shortest + largest head", "fair + freckled + curly-haired", "youthful face + quick movement" (§23, L1411–1417); "No single phenotype bundle such as 'fair + freckles + curly brown hair' may become the default hidden Pipkin package." (L637)
- [ANAT] Headgear must not enlarge head, compress cranium, force juvenile facial proportions, or rely on ear visibility (L1205–1209).
- [ANAT] "No beauty standard is biological." (L253)

## 26. Positive identity statement for the face
- Part 3 core rule: "**An adult Pipkin face must read as biologically mature and recognizably Pipkin before hairstyle, facial hair, wrinkles, cosmetics, expression, clothing, or scale context are visible.**" (L251)
- IMFA anchor (L259), quoted in §1 above.
- Part 3 identity statement: "**Pipkin craniofacial identity is defined by Integrated Mature Facial Architecture: a moderately broad but variable cranial base whose support flows through the temple and zygoma into the central midface while the nasal, maxillary, dental-arch, mandibular-ramus and gonial structures remain fully adult. Pipkin do not trend toward Durrim craniofacial depth-dominance or Gorrund posterior transverse continuity. Their broadly humanoid rounded-ear tendency is secondary, while hair, facial hair, eye color, wrinkles, cheek fullness and head size never carry racial adulthood or identity by themselves.**" (L459)
- Final combined statement (face clause): "their adult face uses Integrated Mature Facial Architecture, with a moderately broad but variable cranial base integrating through the temple and zygoma into a fully mature central midface without juvenile shortening, Durrim depth-dominance or Gorrund posterior transverse continuity." (§37, L1656)
- "The Pipkin-specific feature is the **distribution of integration**, not simply a shorter face." (L267)

## 27. Cross-population facial boundary tests / comparators
- [VAL] Comparators in IMFA distinction list: Marchfolk, Durrim, Gorrund (Transverse Structural Continuity), Fenn, Aelari/Vael, human children (L269–275).
- [VAL] PIP-FACE-17 (human child), -18 (Marchfolk), -19 (Durrim), -20 (Gorrund), -21 (Fenn), -22/-23 (sex like-for-like Marchfolk) (L434–440).
- [VAL] Stress L452 (Durrim depth-dominance), L453 (Gorrund TSC).
- [VAL] PIP-INT-04 face-only with Marchfolk, Durrim, Fenn, Gorrund (L1592).
- [VAL] Cogling: Pipkin/Cogling overlap ~91–107 cm, separation from anatomy; refers to Cogling §63 and `reviews/short-race-comparative-anatomy-v1.md` SR-COMP-01/02 (L94). §35 says that review must verify "face and extremity boundaries" (L1636). No Pipkin-vs-Cogling face test ID in this spec.
- [VAL] Ear comparators: elven point, Grask folded taper, Gorrund bowl (L343–345); overlap with Marchfolk/Durrim ear variation (L349).

## 28. Measurement-deferred items (RM-*)
- SILENT — no RM-* references in the Pipkin spec. Ratios/frequencies are marked OPEN instead (head-to-body ratio L33/L1528).

## 29. Presets / randomization / Simple-Advanced (face)
- [CTRL] Presets "must be legitimate outputs of the same biological system used by Advanced Mode" and cover "head/face variation", "surface phenotype", "age where supported", "sex-related anatomy where relevant" (§21, L1360–1373).
- [CTRL] Provisional biological preset concepts: Reference Adult, Light Narrow, Broad Adult, Powerfully Developed, High-Adiposity Adult, Tall-Boundary Adult, Short-Boundary Adult, Elder Adult — "coverage concepts, not castes" (L1377–1387).
- [CTRL] Simple Mode: Race → Preset → Confirm; Advanced Mode: Race → Preset → Customize → Confirm; presets do not lock subtype/phenotype; Advanced may edit all approved variable traits subject to relationship-aware validity (§22, L1391–1399).
- [VAL] Race-aware randomization draws only from valid Pipkin anatomy; must respect relationships; hidden packages forbidden (incl. "shortest + largest head", "youthful face + quick movement") (§23, L1403–1417).
- [CTRL] Selective randomization: "randomize face while preserving body", "preserve age while randomizing" etc., with validity checks (§24, L1421–1430).
- [CTRL] Population tendencies "may bias randomization without forcing creator controls to move together" (L412).
- [PRES] Presentation Randomization (hairstyle, grooming, cosmetics, tattoos) is not genetic inheritance (L633, L1444–1446).
- [OPEN] Interim randomization sampling "explicitly **not an approved population distribution**" (L635, L1407).
- [OPEN] Final preset library / weighting OPEN (L1551).

## Extraction notes
- Superseded: "large head" brief phrase superseded (L201–203). Part 1 OPEN list (L125) explicitly governed by Part 6 §32. Legacy movement claims superseded (L1098) — not facial. Pipkin no longer lower stature boundary (L119) — not facial.
- Tension: IMFA anchor attributes compactness to a "restrained forehead-to-brow/lower-face soft-tissue vertical envelope" (L259), but Part 3 acceptance note says "The facial vertical envelope is primarily skeletal ... soft tissue may modulate but never create or erase Pipkin identity" (L461). Later text (L461) appears to govern/clarify.
- "Ear fold architecture" appears only as a control family (L409); anatomical fold terms are helix thickness, antihelix definition, conchal depth, tragus/antitragus (L340). No Pipkin fold-type taxonomy.
- Sex-related facial anatomy: L72 says OPEN; L1485 says sex anatomy "may influence ... facial" relationships. No canonical tendency; no R-SEX label.
- FD-* domains named both in Part 3 (L455) and Part 4 (L625, "existing Facial Diagnostic Domains retain their agreed meanings").
- Creator dentition, asymmetry, canthi/folds, pupil, low-light, nictitating membrane, displays: SILENT.
- Facial identity is explicitly secondary to body identity (L461, L1494–1498); a face-only failure test exists (PIP-INT-04) but Pipkin face is "supporting rather than universally exclusive".

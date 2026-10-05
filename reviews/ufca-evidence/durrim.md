> UFCA Phase 1 evidence appendix to `reviews/claude-ufca-01-requirements-matrix.md`. Line references are to the canonical race spec as of commit c076294. Extraction only: no canon is changed, and nothing here is new anatomy. Tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] dependency/validator · [PRES] presentation · [DIAG] measurement/diagnostic · [OPEN] open/not authorized.

# UFCA-01 evidence — Durrim (specs/durrim/DURRIM_V1.md, 522 lines)

Status: FIRST-PASS COMPLETE (L3, L520). Facial content lives in Part 3 (L160–228), Part 3 clarification 1 "facial identity" (L230–259), clarification 2 "structural depth versus surface appearance" (L261–284), clarification 3 "facial depth validation criteria" (L286–322), consistency-resolution patch (L324–339), Part 4 eyes/aging/surface (L341–418), Part 5 carry-forward (L506–516).

Class tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] internal dependency/validator · [PRES] presentation control · [DIAG] measurement/diagnostic only · [OPEN] open/not authorized.

## 1. Cranial vault / cranial proportions
- [ANAT] Provisional tendencies for "a distinct compact craniofacial foundation: strong cranial-neck integration, substantial facial skeletal presence relative to body stature, compact vertical facial relationships, strong midface integration, substantial jaw-joint relationships and broad facial variation" — never means every Durrim wide/square-faced, heavy-browed or large-jawed. (Pt3 §3–7, L170)
- [ANAT] Cranial height not exaggerated because Durrim are short; head "may contribute somewhat more to stature than in the Marchfolk Human Reference Population," skull stays adult and coherent. (L170; also Pt1 §4–10, L21: "never an oversized fantasy-dwarf head")
- [DIAG] Keep separate: absolute cranial height, cranial height relative to face, head height relative to body. (L170)
- [ANAT] "**Greater cranial breadth relative to cranial height than the Marchfolk reference distribution is a provisional population tendency**, and narrower Durrim crania stay valid." (L170; restated as distribution tendency, not requirement, Clar.1 table L243)
- [ANAT] Adult read: never "childlike cranial proportions … or a cranium excessively large for the facial skeleton." (Pt3 §1–2, L166)
- [ANAT] "Compact adult architecture": vertically compact, structurally substantial relative to body stature, fully adult, integrated with compact neck and torso; "Compact" = proportional organization, "never squashed, juvenile, flat, round or necessarily wide." (Clar.1 table, L242)
- [ANAT] Head-neck integration (added major identifier): head reads as structurally integrated with relatively short, substantial skeletal neck (cranial base, jaw-neck transition, cervical contribution, shoulder relationship), never achieved by neck muscle; low-muscle Durrim keeps it. (L247)
- [VAL] Population validation phrase: "Cranial breadth" listed among features whose sole dependency fails the design. (L252)

## 2. Forehead
- [ANAT] "Broad variation in height, breadth, curvature, hairline and brow transition. Low foreheads aren't mandatory, and forehead height never signals intelligence or personality." (Pt3 table, L176)
- [ANAT] Hairline not locked to forehead anatomy. (L199)

## 3. Brow / supraorbital
- [ANAT] "Substantial brow structure is supported but not mandatory. Frontal bone, eyebrow hair, expression and age tissue stay separate, and a subtle-browed Durrim is still Durrim." (L177)
- [ANAT] Surface brow: skeletal brow geometry separate from eyebrow hair, skin, fat, muscle, age, expression and lighting; "strong skeletal brows with subtle eyebrows, or thick eyebrows over subtle bone, are both possible." (Clar.2 table, L272)
- [DIAG] Depth domain A "Brow and supraorbital": evaluate frontal bone, supraorbital region, orbital rim, upper nasal root; exclude eyebrow hair, expression, shadow intensity. (Clar.3 table, L294)
- [VAL] Brow neutralization test: subtle, moderate and strong brow all stay Durrim. (L217)
- [VAL] Matched brow test: heavy brow isn't the main depth mechanism. (L309)

## 4. Orbit
- [ANAT] "Recognizably humanoid, varying in size, width, height, spacing, depth and brow-orbit relationship, never universally small or deep-set eyes." (L178)
- [ANAT] Orbits (clarified): "No mandatory Durrim eye appearance, and dimensions, opening, spacing, brow and orbital depth vary, never universally deep-set, small or narrow." (L250)
- [ANAT] Interorbital: "Eye spacing, nasal-root relationship and brow spacing vary, coupled to surrounding anatomy, with no stereotypical Durrim spacing." (L181)
- [ANAT] Deep-set eye look: "Orbital structural depth is separate from the deep-set impression created by orbit, lids, brow tissue, eye position, facial fat and shadow." (L273)
- [DIAG] Depth domain B "Orbital": evaluate orbital rim, eye position, surrounding cranial structure; exclude eyeball size and position, eyelids, visible opening ("a deep-set look doesn't prove orbital depth"). (L295)

## 5. External eye (aperture, lids, canthi, folds)
- [ANAT] Visible eye opening: "Bony orbit, eyeball, lids, visible opening, brow and expression stay separate, and narrowed eyes never signal toughness, suspicion, age or dwarf identity." (L179)
- [ANAT] Eye size: "Never enlarged to offset short stature or shrunk for ruggedness, and stays adult and population-valid." (L180)
- [ANAT] Adult read: never "oversized childlike eyes." (L166)
- [ANAT] Aging: "eye and mouth changes" among facial aging effects. (Pt4 aging table, L376)
- Canthi / lid folds specifically: SILENT.

## 6. Ocular anatomy
- [ANAT] "Iris anatomy, iris pigmentation, pupil, sclera, cornea, lighting and reflection, and magical effects stay separate." (Pt4 §21–28, L368)
- [ANAT] First-pass iris families "may include brown, dark brown, hazel, amber, green, gray and blue," distributions OPEN, human frequencies not automatically copied. (L368)
- [ANAT] Magical-vs-biological: "Natural iris color is never glow, emissive, magical, supernatural patterning, class or status effects, so a naturally amber-eyed Durrim isn't inherently magical." (L368)
- [ANAT] Irises have internal variation (radial, central and peripheral differences, crypts and fibers, pigment density), never flat disks; implementation OPEN. (L368)
- [ANAT]/[OPEN] Natural heterochromia (complete, sectoral, central) may be supported; frequency OPEN, never inflated. (L368)
- [ANAT] Sclera "isn't unnaturally bright white by default," responding to biology, age, vascularity, later health-state systems, lighting; disease never encoded through racial appearance. (L368)
- [ANAT] "Pupils stay broadly humanoid, with no slit or unusual geometry or glow added for fantasy." (L368)
- [OPEN] "Durrim specialized visual adaptation. Low-light vision isn't granted because fantasy dwarves live underground." (L368; listed again L516)
- [VAL] Eye neutralization: "Recognition never depends on eye color." (L404)
- [PRES]/[VAL] Lighting: skin, hair and iris never "artificially brightened to stay visible in darkness." (L395)
- Nictitating membrane: SILENT.

## 7. Cheek / zygomatic
- [ANAT] "Zygomatic breadth, projection, height, midface integration and soft-tissue volume vary, with no required huge, sunken, red or round cheeks." (L182)
- [ANAT] Facial width varies independently "through zygomatic, temporal, mandibular and midface breadth, never one Face Width scalar." (L170)
- [DIAG] Depth domain C "Zygomatic and cheek": evaluate zygomatic projection and relationship to orbit and midface, front-to-back cheek skeleton; exclude cheek fat, and "lateral cheekbone width confused with forward projection." (L296)
- [ANAT] Ruddy/red cheeks never a Durrim marker. (Pt4, L354)

## 8. Midface
- [ANAT] "Contributes meaningfully to identity: substantial skeletal depth relative to compact facial height, strong nose-cheek-upper jaw integration, broad projection range, never universally protruding." (L183)
- [ANAT] Clarified: "An important identity contributor: substantial midface structural integration relative to the compact vertical face, which works with small, large, narrow, broad, low- or high-projecting noses, so midface identity is never nasal size." (L245)
- [ANAT] Craniofacial depth (added tendency): "Greater craniofacial skeletal depth relative to facial vertical height than equivalent Marchfolk anatomy, through brow and orbit depth, midface projection and depth, maxilla and mandible, never a universally protruding face." (L244)
- [DIAG] Depth domain D "Midface and maxillary (especially important for Durrim)": evaluate front-to-back relationships among orbit, zygoma, maxilla, nasal root and base, upper alveolar region; exclude nose-tip projection. (L297)
- [ANAT] Adult read: never "an infant-like midface." (L166)

## 9. Nasal anatomy
- [ANAT] "**Durrim are not identified by large noses.** Root and bridge height, bridge breadth, length, projection, alar breadth, nostrils, tip and columella are separate, never one Nose Size control." Valid range: shorter/longer, narrower/broader, lower/greater projection, straight/convex/subtle-concave profiles, varied tips. "A nose can look prominent on a compact face without being absolutely large." (L184)
- [ANAT] Locked neutrality: "**nasal anatomy is a major individual-variation region, not a primary racial identifier for Durrim**." (L252)
- [ANAT] Depth vs nose: "Craniofacial depth and nasal projection are distinct." (L249; L274)
- [DIAG] "nasal-tip projection isn't the primary depth landmark (nasal skeleton still counts, but nose projection is analyzed separately)." (L300)
- [ANAT] Adult read: never "a tiny nose." (L166)
- [ANAT] Red nose never a Durrim marker. (L345, L354)
- [VAL] Nose neutralization test. (L215); Matched nose test. (L308)

## 10. Mouth / lips
- [ANAT] "Width, lip volume, upper-lower relationship, philtrum, projection and corner orientation vary, never universally thin-lipped or broad-mouthed." (L185)
- [ANAT] Aging may bring "eye and mouth changes." (L376)

## 11. Jaw / mandible
- [ANAT] "May trend toward substantial mandibular presence relative to the compact face, but never every Durrim square, wide or heavy-jawed. Jaw breadth, ramus height, mandibular-body depth, chin breadth, height and projection and jaw angle are separate with mandatory relationship-aware constraints." (L186)
- [ANAT] "Mandibular skeleton, masseter and temporalis muscle, facial fat and beard volume stay separate, so a light-jawed Durrim can have strong jaw muscles, and a substantial jaw can sit under low muscle and no beard." (L186)
- [ANAT] Clarified mandible: "Substantial mandibular presence as a tendency, meaning the relationship among mandibular body, ramus, jaw joint, chin, midface and cranial base, never a mandatory square, wide jaw or large chin. A relatively narrow-jawed Durrim is fully Durrim." (L246)
- [ANAT] Mandibular depth separate from jaw width, chin projection, masseter size, facial fat and beard volume. (L275)
- [DIAG] Depth domain E "Mandibular and lower face": evaluate mandibular body, ramus, jaw-joint position, lower alveolar structure, chin relationship; exclude jaw width, chin projection, masseter volume ("a projecting chin isn't mandibular depth"). (L298)
- [ANAT] Adult read: never "a small juvenile jaw." (L166)
- [VAL] Jaw neutralization (L216); Matched jaw (L310).

## 12. Chin
- [ANAT] "Narrower or broader, shorter or taller, more or less projected, with no required giant square chin." (L187)
- [DIAG] "the most anterior chin point alone isn't lower-face depth." (L300)

## 13. External ear
- [ANAT] "Durrim ears are broadly humanoid in organization, with a coherent auricular root, helix, antihelix, concha, tragus, antitragus and lobe, never simple attached shapes." (Pt3 §29–34, L195)
- [ANAT] "Durrim don't have pointed ears and stay biologically distinct from the shared elven ear architecture, avoiding accidental elf-like taper." (L195)
- [ANAT] Dimensions vary — absolute length, length relative to head, breadth, projection, orientation, curvature, lobe size and attachment, position, asymmetry — "never one Ear Size control." (L195)
- [OPEN] "There's no strong universal ear-size stereotype yet: first-pass Durrim ears sit within a broad compact-humanoid range, with population distributions future work." (L195)
- [ANAT] Projection close-set to more projecting, independent of length, breadth and lobe size; projecting ears never comic short-stature shorthand. (L195)
- [ANAT] Biological ear anatomy separate from acquired cuts, missing sections, scars, injury deformation; occupational damage never racial. (L195)
- [ANAT] Ears "may shape individual appearance but aren't a primary identifier." (L252)
- [VAL] Hidden-ear test (L214). Gorrund spec cross-ref (not Durrim canon): Durrim ears get no Gorrund deep-bowl traits retroactively — see Gorrund L463.
- [ANAT] Helmets must respect "cranial anatomy, ear position." (L472)

## 14. Teeth / dentition
- SILENT. (No dentition, tooth or tusk statement in the spec.)

## 15. Race-specific cranial displays / keratin / horns
- SILENT / N/A (no displays, keratin or horns in canon).

## 16. Skin/surface structures that materially alter facial anatomy
- [ANAT] None stated as anatomy-altering. Surface detail: "Realistic pores, fine lines, texture, local pigment, age changes … never exaggerated roughness to look 'rugged'." (L356)
- [OPEN] Skin thickness/toughness OPEN, not assumed from skeleton, no gameplay effect. (L357)
- [ANAT] Racial structure "never faked mainly through normal maps, displacement, roughness, ambient occlusion, baked shadow or skin materials: large-scale depth lives in geometry or deformation." (L278)
- [ANAT] Soot, stone dust, mining grime not racial (permanent rule). (L387); scars acquired (L389).

## 17. Natural asymmetry
- [ANAT] "Natural subtle-to-moderate asymmetry in brow, eye opening, cheeks, nose, mouth, jaw and ear placement, unless damage is deliberately represented. Natural asymmetry isn't deformity." (L191)
- [ANAT] Ear asymmetry varies (L195); eyebrow asymmetry (L207); hairline asymmetry (L199).

## 18. Age-related facial change (and age triad)
- [ANAT] Age triad: "Chronological age, apparent biological age and age presentation stay distinct, and apparent age isn't inferred from chronological age until lifecycle biology exists." (L372)
- [OPEN] Lifespan, maturation, fertility, senescence, age-stage durations OPEN. (L372)
- [CTRL] "Creation eventually supports younger, mature, older and elderly adults, with chronological mapping later." (L372)
- [ANAT] Face aging: "Fine lines, deeper folds, facial fat changes, eye and mouth changes, jaw and neck surface changes, skin texture, always respecting Durrim craniofacial architecture, so age never replaces racial anatomy." (L376)
- [VAL] Structural depth: "Age-related surface changes are never mistaken for more craniofacial structural depth … depth classification [does not rise]." (L377; also Clar.2 L277: aging "isn't simulated by changing racial depth parameters")
- [ANAT] Hair/beard aging: never complete whitening at fixed age; beard color never a chronological-age meter; gray beard never sole marker of older Durrim. (L378–379, L207)
- [VAL] Age diversity: "Durrim don't look old by default." (L220); Age neutralization (L405).

## 19. Sex-related facial tendency
- [OPEN] Canon states no sex facial tendency. "Durrim sex-related anatomy isn't finalized and stays separate from height, frame, muscle, fat, face, hair … (OPEN; the universal rule is now R-SEX in `decisions/PROJECT_RULES.md` — Durrim magnitudes stay OPEN)." (L58) — SILENT on facial magnitudes (pointer: R-SEX, stated in spec).
- [VAL] Sex stereotype test: "Never 'male means giant beard and broad square face, female means a scaled-down human woman with no beard.' All share the Durrim foundation, with sex-related variation future work." (L219)
- [OPEN] "**Durrim facial-hair sex-related distributions are OPEN.**" (L207; L516)
- [PRES] Cosmetics never sex-locked by default. (L389)

## 20. Facial hair biology (incl. eyebrows)
- [ANAT] Facial-hair biology (follicle distribution, density, texture, coverage, growth rate, age change) designed separately from beard culture; distributions provisional pending sex anatomy. (L203)
- [PRES] "Beard length, shape, braiding, ornamentation, shaving, trimming and styling are **personal presentation**." (L203)
- [ANAT] Locked: "**A clean-shaven Durrim must look completely biologically valid and unmistakably adult** … Beards are never needed to make the face work." (L205)
- [ANAT] Locked neutrality: "**Facial hair contributes zero required information for biological Durrim recognition.**" (L252)
- [ANAT] Pt1: "not every Durrim grows a beard, facial hair isn't only male, beard density doesn't define adulthood, beard length isn't biological, and beardless Durrim aren't unusual." (L58)
- [ANAT] Eyebrows vary in density, width, shape, texture, pigmentation, asymmetry; never necessarily bushy; grooming is presentation. (L207)
- [ANAT] Facial hair/eyebrows usually related to scalp hair color but needn't match; no identical color across scalp, brows, facial, body hair. (L364)
- [OPEN] Body-hair biology OPEN. (L207)
- [OPEN] Hair/beard physics with armor, helmets etc. need future validation; clipping never accepted as racial feature (L207, L473 "beard clipping isn't an acceptable Durrim trait", solution OPEN).
- [PRES] Beard traditions: none approved, none inferred from biology. (L207)
- [PRES] Hair dye is personal presentation. (L364)

## 21. Inherited / mixed development
- N/A (Halvren only).

## 22. Locked validation tests touching the face
- [VAL] Hidden-beard (permanent) — bald/clean-shaven/no presentation still reads Durrim. (L213)
- [VAL] Hidden-ear — facial identity remains with ears hidden. (L214)
- [VAL] Nose neutralization — small to projecting noses all Durrim. (L215)
- [VAL] Jaw neutralization — light to substantial jaws all Durrim. (L216)
- [VAL] Brow neutralization. (L217)
- [VAL] Beauty diversity — attractive/ordinary/severe/soft/rugged/refined; none superior. (L218)
- [VAL] Sex stereotype. (L219)
- [VAL] Age diversity. (L220)
- [VAL] Equal-height face — vs Marchfolk with hair/beard/ears/presentation removed, distinguishable "through combined craniofacial anatomy, never one exaggerated feature." (L221)
- [VAL] Population sampling — fails on convergence to huge nose, square jaw, heavy brow, tiny eyes, giant beard, broad male-coded face, old face. (L222)
- [VAL] No single-feature dependency (permanent) — fails if readability depends mainly on any one of cranial breadth, heavy brow, deep-set eyes, nose size/breadth, midface projection, jaw breadth, chin size, ear shape, beard, hairstyle. (L252)
- [DIAG] DU-FACE-01 Neutral Durrim — must read immediately as Durrim beside equivalent Marchfolk; "if it needs an exaggerated feature, the facial foundation is insufficient." (L256)
- [DIAG] DU-FACE-02 to 11 — narrower/broader face, subtle/strong brow, modest/strongly projecting nose, narrower/broader jaw, lower/greater craniofacial depth; all Durrim without compensating changes. (L257)
- [DIAG] DU-DEPTH-01/02/03 — lower/central/greater valid depth, matched in width, verticality, nose, jaw breadth, composition, age, hair, expression. (L280, L304)
- [VAL] Surface-variation test — one skeleton under varied soft tissue, eyebrows, facial hair, older surface, skin texture, lighting; structural identity recognizable. (L280)
- [VAL] Depth tests: Matched nose (L308), Matched brow (L309), Matched jaw (L310), Soft-tissue neutralization (L311), Lighting neutralization (L312), Perspective (L313), Silhouette and profile (L314), Cross-section (L315, never player-facing), Population validation (L316).
- [VAL] Part 4: Pigmentation and face — pigmentation never couples to craniofacial phenotype (L410); Clean character (L406); Eye neutralization (L404); Age neutralization (L405).
- [VAL] Part 5 carry-forward: all Part 3 facial tests carry forward; "movement or equipment validation never requires changing the approved head." (L506)
- [VAL] Adult read (Pt1): with beard etc. removed, adults read as adults. (L76)

## 23. Explicitly OPEN biology touching the face
- [OPEN] Sex-related anatomy; facial-hair sex distributions. (L58, L207, L516)
- [OPEN] Ear-size population distributions. (L195)
- [OPEN] Hair texture frequencies (L199); pigmentation/hair/iris frequencies (L351, L364, L368, L516).
- [OPEN] Heterochromia frequency (L368); specialized visual / low-light adaptation (L368, L516).
- [OPEN] Skin thickness / tissue durability (L357, L516).
- [OPEN] Lifecycle / lifespan / senescence (L372, L516).
- [OPEN] Body-hair biology (L207).
- [OPEN] Numerical craniofacial depth ranges ("No numerical thresholds yet") (L318, L516).
- [OPEN] Face technical architecture (dedicated head mesh, morph set, topology, bone/morph, hybrids; MetaHuman not assumed) (L226, L516).
- [OPEN] Universal Facial Customization Architecture (L234, L322, L516).
- [OPEN] Hair/beard physics solution (L207, L473).

## 24. Pass 1 provisional creator-control list for the face
- [CTRL] Durrim defines NO player-facing facial controls: "what's defined now is racial craniofacial identity and biological relationships, not player-facing controls: no slider names or counts, menu hierarchy, Simple Mode or Advanced Mode controls (including quick and detailed controls), morph or bone implementation, or UI organization." (Clar.1, L234) — therefore no Durrim control list exists to reproduce.
- [CTRL] Control-relevant multidimensionality requirements stated in anatomy (not a control list): never one Face Width scalar (L170); never one Nose Size control (L184); jaw dimensions separate with relationship-aware constraints (L186); never one Ear Size control (L195); never one Face Depth scalar (L265); depth domains "related, never five fully independent sliders" (L300); "the eventual facial architecture must represent these regional depth relationships without one global slider, which isn't permission to design it now" (L318).
- [CTRL] Face shape: "No fixed face-shape subtypes. Presets may start from narrower, broader, longer, more compact, stronger- or lighter-jawed combinations, over continuous relationship-aware controls." (L188)
- [CTRL] Likely future domains (NOT approved, not implementation): "cranium, forehead and brow, orbits and eyes, midface, cheeks, nose, mouth and lips, mandible and chin, ears, soft tissue and asymmetry." (L259)
- [CTRL] Consistency patch: Marchfolk v1.2 three-level editor and seven-region organization are "approved first-pass design proposals demonstrating required functionality, not the final universal facial-control hierarchy," never constraining later races (L331); classification "APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION" (L333); universal review may keep/split/merge/rename/reorganize/add regions (L334).
- [CTRL] Future system "won't give every race identical ranges: shared concepts may run through race-specific validity envelopes, coupling, anatomy, morph behavior and possibly different technical assets." (L259)

## 25. Prohibited controls and anti-patterns
- [VAL] No single Face Width scalar (L170), Nose Size control (L184), Ear Size control (L195), Face Depth scalar (L265), global depth slider (L318); "never five fully independent sliders" for depth domains (L300).
- [VAL] Face-body coupling: "never Broad Frame automatically producing a Broad Face" (soft, probabilistic, breakable correlation only) (L189); broad torso doesn't require broad face, short limbs don't require short nose, large hands don't require large jaw (L252).
- [VAL] Randomization "never independent per-dimension rolls." (L226)
- [VAL] No hidden preset-only geometry (L226, L506).
- [VAL] No phenotype-pigmentation packages (broad face + red hair etc.) (L412).
- [VAL] Never fake racial structure via normal maps, displacement, AO, baked shadow, materials (L278).
- [VAL] Never refer to a Facial Diagnostic Domain as "Layer A," "Layer B" (L280, L330).
- [VAL] Anti-patterns: giant nose, mandatory beard, oversized head (permanent failure conditions, L506); narrowed eyes as toughness signal (L179); depth inferred from width or compact height alone (L300); raw 137 vs 173 cm comparisons (L302); judging from close wide-angle shots (L313); inventing numbers before prototype calibration (L318).
- [VAL] Presets never lean on beard, red/gray hair, pale/ruddy skin, wrinkles, soot, mining clothing (L416).

## 26. Positive identity statement for the face
- [ANAT] "> **Durrim craniofacial identity emerges from the combined relationship among a compact adult cranium, structurally integrated midface, substantial craniofacial depth/presence, mandibular support, and strong head-neck-body integration—not from any single exaggerated facial feature.**" (L236)
- [ANAT] "> **A Durrim must still look Durrim when bald, clean-shaven, with neutral expression and with the ears hidden.**" (L164)
- [ANAT] Resolved criterion: "Durrim provisionally trend toward greater average craniofacial skeletal depth relative to facial vertical height than equivalent Marchfolk anatomy. This tendency must be expressed and validated through coherent multiregional brow/orbital, zygomatic, midface/maxillary and mandibular relationships, rather than nasal projection, chin projection, facial width, soft tissue, surface materials, lighting or expression." (L320; tendency first stated L282)
- [ANAT] Final identity includes "a distinct compact craniofacial foundation," persisting across facial structure, pigmentation, age, hair, presentation, not dependent on beard. (L510)
- [ANAT] Correlated distribution: "different Durrim express different subsets strongly … never fixed packages." (L252)

## 27. Cross-population facial boundary tests / comparators
- [VAL] Equal-height face vs Marchfolk. (L221)
- [DIAG] DU-FACE-01 "beside an equivalent Marchfolk." (L256)
- [VAL] Pipkin and Cogling craniofacial foundations "compared directly with Durrim, so the three stay distinguishable at comparable height through anatomy." (L259); Short-Race Comparative Anatomy Review now ACCEPTED/COMPLETE (`reviews/short-race-comparative-anatomy-v1.md`) (L502); Pipkin/Durrim ~122 cm SR-COMP-03 and Cogling COG-BODY-10/10A (body, L145).
- [DIAG] Cross-race depth comparisons vs Marchfolk, Sagekin, Skarn, Pipkin, Cogling; each names population and region, "never 'more than everyone else.'" (L280)
- [DIAG] Depth comparison methods: equal-height (permanent, ~150 cm Durrim vs ~150 cm Marchfolk where ranges overlap), population-reference comparison (absolute and proportional), diagnostic-only same-facial-height comparison "never resizing actual characters." (L302)
  - Note: L302 says "about 150 cm" while the consistency patch corrected the body boundary test to 152 cm (L145, L335, L337); see Extraction notes.
- [VAL] Durrim vs elves (Fenn, Aelari, Vael): Durrim need positive identity, not opposite of elven gracility (body, L501); Durrim vs humans with beard etc. removed (L500).

## 28. Measurement-deferred items (RM-*)
- No RM-* identifiers appear in the spec. SILENT.
- [DIAG] Non-RM deferral: "No numerical thresholds yet … v1.0 locks the measurement concepts and methodology." Prototype calibration later: landmarks, samples, regional measurement, distribution comparison, blinded visual comparisons, then validity envelopes, "only then consider numerical limits." (L318)
- [DIAG] Absolute vs proportional structural depth both recorded; Durrim tendency mainly proportional. (L300)
- [DIAG] Neutral validation state: neutral expression and head orientation, standardized camera/focal length, neutral reference lighting, no beard over landmarks, hair removed/controlled, matched apparent age and soft tissue; final evaluation on actual geometry. (L290)
- [DIAG] Facial Diagnostic Domains FD-STRUCT, FD-SOFT, FD-SURF, FD-HAIR, FD-PRES, FD-OBS — "for facial analysis only, never Character Architecture Layers." (L280, L330, L345)

## 29. Presets / randomization / Simple-Advanced statements touching the face
- [CTRL] "Face presets show broad diversity and are legitimate outputs of the same face system, with no hidden preset-only geometry." Internal validation directions (narrower/broader, compact/somewhat longer faces, stronger midface, lighter/stronger jaws, subtle/stronger brows) "never subraces." (L226)
- [CTRL] "Facial randomization is population-, relationship- and frequency-aware and supports broad individual identity, never independent per-dimension rolls." (L226)
- [CTRL] "Advanced Mode supports randomizing face, ears, hair biology, facial-hair biology where appropriate and presentation separately, with trait locks." (L226)
- [CTRL] Simple/Advanced controls themselves not defined for Durrim (L234).
- [CTRL] Presets "stay editable in Advanced Mode and pass all constraints, with no preset-only geometry"; race-aware randomization avoids stereotype convergence, with selective randomization and attribute locks required; same system for PCs, NPCs, presets, procedural population. (L506)
- [CTRL] Biological vs presentation randomization separate (L416); presets never lean on beard, red/gray hair, pale/ruddy skin, wrinkles, soot (L416).
- [VAL] Population sampling convergence test (L222); pigmentation diversity (L401).

## Extraction notes
- Durrim explicitly declines to define facial controls (L234); section 24 therefore reproduces constraints and deferred-domain lists only, not a control organization.
- Naming supersession: the original "A–F facial layers" were renamed Facial Diagnostic Domains FD-* by the consistency-resolution patch (L280, L330). The depth domains "A–E" (L292–298) are a separate, still-current lettered scheme for depth evaluation; they are not the superseded A–F layers. Risk of confusion: the patch forbids "Layer A/B" for FD domains, but depth domains still use letters A–E.
- Height-value tension: Clar.3 comparison methods (L302) still say "about 150 cm Durrim against about 150 cm Marchfolk," whereas the consistency patch corrected the boundary test to ~152 cm (L145, L335) and promoted the rule that equal-height tests must use a stature valid for every participant (L337). For a Durrim–Marchfolk-only pair 150 cm is valid for both (Durrim 122–152, Marchfolk 147–203 per Grask L154), so this is not strictly contradictory, but the three-population face/body boundary test is 152 cm.
- "Greater cranial breadth relative to cranial height" is phrased as a provisional tendency (L170) and re-framed as a distribution tendency, not requirement (L243). Craniofacial depth tendency is "provisional population tendency until comparative validation" (L282) then "resolved" as criterion (L320) — still provisional ("provisionally trend") but methodology locked.
- Head contribution to stature: "somewhat greater" than Marchfolk (L21, L170) with no ratio; no head-to-height number exists.
- No dentition statements anywhere; teeth SILENT.
- Durrim ears: Gorrund spec L463 states Durrim keep broadly humanoid non-elven ears with no Gorrund deep-bowl or fold architecture added retroactively — consistent with L195 but sourced from Gorrund canon.

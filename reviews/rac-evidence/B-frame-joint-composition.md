<!-- RAC Phase 1 evidence extraction (agent-produced, line-checked at HEAD 218f64a). Not canon; supporting evidence for reviews/claude-rac-01…12. -->
# B — Frame / Joint / Robusticity and Composition: evidence extraction

Repo: `/home/claude/wayfarer-design` at HEAD `218f64a`. Extraction only: no canon changed, nothing invented. Every line number below was re-read in the cited file at this HEAD (the `reviews/ucca-evidence/*` digests were used only to locate lines; several digest line numbers are off by 1–2 against current specs, e.g. Pipkin composition is L182 not L180, Saurin §258 frame is L4170 not L4168).

**Citation keys.** Race specs: `MARCHFOLK`, `SKARN`, `SAGEKIN`, `FENN`, `AELARI`, `VAEL`, `HALVREN`, `DURRIM`, `GRASK`, `GORRUND`, `PIPKIN`, `COGLING`, `SAURIN` = `specs/<race>/<RACE>_V1.md`. `PR` = `decisions/PROJECT_RULES.md`. `UCCA` = `decisions/UCCA_V1.md`. `R2` = `reviews/claude-pass2-r2-large-race-comparative-review.md`. `SR` = `reviews/short-race-comparative-anatomy-v1.md`. `ECR` = `reviews/elf-comparative-review.md`. `R5` = `reviews/claude-pass2-r5-reference-mesh-queue.md`.

**Tags.** [POS] positive canon statement · [OPEN] explicitly open · [TEST] validation case/test · [BAN] prohibition · [NUM] exact canon numbers · [SILENT] spec says nothing on the point. Quotes are verbatim (bold markers `**` removed), ≤25 words.

---

## 0. Universal rules that govern both parts

- [POS] Frame definition (UCCA): "Skeletal Frame is the continuous configuration of a character's skeletal breadth, depth, joint and robusticity variables" (UCCA L119). Variables named: "shoulder/clavicular breadth, thoracic width, thoracic depth where bound, pelvic width and depth where canon names it, joint scale, long-bone robusticity" (UCCA L119).
- [BAN] "Frame is not sex, body type, muscularity, fatness or stature. Balanced is not the canonical or default body." (UCCA L121).
- [POS] Write-and-vanish: "Narrow / Balanced / Broad are write-and-vanish starting operations that write race-specific starting values." (UCCA L124). "The resolved skeletal values are the frame." (UCCA L126).
- [POS] Frame write scope: "frame writes only skeletal values" … "It never writes stature, segment lengths, composition, face, hair, sex-related anatomy or presentation." (UCCA L129).
- [POS] Correlation vs independence: correlated dimensions "may be influenced when frame is applied but remain independently editable where canon allows" (UCCA L131), naming Cogling AC-9, Grask foot breadth, Gorrund thoracic depth, Durrim unequal breadths.
- [POS] Hard items survive: "Joint hard minimums and each race's frame boundary rule (Broad Skarn ≠ Gorrund; Broad Grask ≠ Skarn/Gorrund; Narrow Gorrund keeps ALPC; …) stay hard." (UCCA L131 — full list: Broad Pipkin/Cogling ≠ Durrim; Narrow Pipkin/Cogling ≠ child or Fenn; Broad Saurin ≠ Gorrund; Narrow Vael ≠ scaled-down Broad).
- [POS] PR: "Population correlations normally use weighted distributions/conditional probabilities/validity envelopes rather than hard creator dependencies." (PR L18).
- [POS] Five-way separation: "Muscular Development Capacity ≠ Current Muscularity ≠ Body-Fat Amount ≠ Body-Fat Distribution ≠ Skeletal Frame." (UCCA L154).
- [BAN] Hard rules: "composition never edits the skeleton; thoracic depth is never faked by fat or muscle; pelvic breadth is never fat; frame never edits composition." (UCCA L156).
- [POS] Capacity rule: "Capacity is Biological Anatomy and sets the valid ceiling of Current Muscularity (CLAMP)." (UCCA L161). Detailed control only "where canon explicitly requires it" (Saurin variation axis; Cogling §69) (UCCA L162); "Elsewhere it is a VAL ceiling / distribution property." (UCCA L163); "Where the population distribution is OPEN (Grask, Gorrund, Pipkin, Cogling), no population shift is invented." (UCCA L164). PR restates: "Muscular Development Capacity is a Detailed control only where race canon explicitly requires it; otherwise a validator ceiling. No invented population shifts." (PR L50).
- [BAN] "no stereotype physique bundle (never Broad → muscular → high fat); no "round halfling"; no "bodybuilder troll"; no "ogre belly"." (UCCA L169).
- [POS] Composition operations "write Physical Composition only (muscularity, regional offsets, fat amount, fat distribution) and never skeletal frame, stature, sex-related anatomy or capacity." (UCCA L167).
- [POS] Regional groups superset: "neck, shoulders, upper arm, forearm, chest, upper back, core, glutes/hips, thigh, calf/shank; Saurin: tail" — "Each race binds only the groups its canon names." (UCCA L158).
- [POS] R-SEX: "Sex is never a body preset or package and never forces frame, stature, muscularity, body-fat amount or distribution … unless explicit race canon defines a tendency." (PR L93); "no shift" is "a valid complete state for a race" (PR L94).
- [TEST] "Frame × sex-related anatomy × composition factorial at reference stature per race." (UCCA L333); "Athletic write test: applying any composition starting operation changes no Slot 3 value." (UCCA L334); tier I "Frame / composition independence" (UCCA L327).
- [OPEN] BIO OPEN carried: "joint/robusticity distributions; head-to-stature (all but Saurin); capacity distributions (Grask, Gorrund, Pipkin, Cogling); fat-distribution tendencies; sex dimorphism magnitude (Durrim, Grask, Gorrund, Pipkin, Cogling)" (UCCA L355); also "pelvic morphology" (UCCA L355).
- [NUM]/measurement: RM-UB-03 "Joint-scale and long-bone robusticity envelopes, including race hard minimums" — "Reference meshes per race and frame" → "UCCA Slot 3 bounds" (R5 L81; UCCA L351). RM-LR-05 "Joint scale (knee, elbow and wrist breadth ÷ adjacent long-bone length)" — "All three, plus Marchfolk" (R5 L31). RM-SR-03 "Long-bone shaft breadth ÷ length; joint breadth ÷ adjacent length" — "Cogling, Pipkin, Durrim" → "Structural-mass axis (short-race review §4)" (R5 L41). RM-LR-02 thoracic depth ÷ stature / ÷ breadth; shoulder breadth ÷ stature, "Same, plus Narrow and Broad presets" (R5 L28). RM-OT-01 Sagekin "ribcage depth and breadth" (R5 L89). RM-OT-02 elves "thoracic depth; neck relative length; joint ratios" (R5 L90). Prerequisite for every race: "an approved reference mesh (central tendency), plus Narrow / Broad frame-preset meshes" (R5 L16).
- [POS] R5 derivation rule: "A clamp that a measurement exposes is creator behaviour (CONSTRAIN), not a reason to weaken a population's distribution." (R5 L99).

---

# PART 1 — FRAME / JOINT / ROBUSTICITY

### Marchfolk (Human Reference Population)
- [POS] Frame content: "Frame describes skeletal structure (shoulder breadth, ribcage dimensions, pelvic breadth, joint scale, skeletal visual mass) and isn't muscularity, body fat, fitness or personality." (MARCHFOLK L27)
- [POS] Frame vs preset: "Skeletal Frame is the underlying continuous configuration of shoulder, ribcage, pelvis, joints and related structural dimensions." (MARCHFOLK L285); presets are "editable starting points, not immutable biological castes" (MARCHFOLK L285).
- [POS] Athletic never touches skeleton: "It never automatically changes skeletal shoulder breadth, ribcage or pelvic dimensions, limb-bone proportions, joint scale or other frame parameters." (MARCHFOLK L281)
- [POS] Frame scope limit: "A frame never restricts customization beyond the race's normal biological limits." (MARCHFOLK L206)
- [POS] Reference role for joints: Marchfolk are "the grounded reference for judging how another race differs in skeletal proportions, craniofacial anatomy, joints, limbs" (MARCHFOLK L15).
- [POS] Thickness ≠ skeleton: "Specs distinguish skeletal breadth or diameter, muscular development, adipose contribution and total external circumference or visible volume." (MARCHFOLK L283)
- [POS] Derived dimensions: "Shoulder width: clavicles, upper back and shoulder-joint position." (MARCHFOLK L83); "Chest depth: ribcage and upper-torso structure." (MARCHFOLK L84); "Limb thickness: believable joint transitions." (MARCHFOLK L87).
- [TEST] Relationship constraints "across shoulder width and ribcage, ribcage and waist, pelvis and hips, upper arm and forearm, femur and lower leg, hand and wrist, foot and ankle" (MARCHFOLK L31).
- [TEST] "Narrow, Balanced and Broad, each with very different compositions (lean, muscular, high body fat), to verify frame and composition stay independent" (MARCHFOLK L250).
- [SILENT] No joint hard minimum, no long-bone robusticity statement, no thoracic depth:width tendency (Marchfolk is the comparator, not a directional population). Numeric frame values: none.

### Skarn
- [POS] Skeletal foundation vs Marchfolk: "broader clavicles", "a deeper ribcage and more thoracic volume", "a more substantial neck base and pelvis", "heavier joints" (SKARN L21–L24); "greater skeletal robustness" (SKARN L26).
- [POS] Proportional identity: "a slightly larger torso share of total height and greater torso depth" (SKARN L75); "broader clavicles, a wider and deeper ribcage, and a broader upper back" (SKARN L76); "more substantial limbs and larger joints" (SKARN L78).
- [POS] Scale carriers: "Hands, feet, joints and torso carry much of the Skarn sense of scale." (SKARN L40)
- [POS] Depth is skeletal: "Deeper chests change ribcage volume, not just surface muscle." (SKARN L90)
- [POS] Ranges not fixed: "These are ranges, not identical proportions for every Skarn." (SKARN L28)
- [POS] Frame scope: "The universal frames apply: Narrow, Balanced and Broad, all inside Skarn limits. A Narrow Skarn is still structurally Skarn." (SKARN L32)
- [BAN] Frame boundary: "A Broad Skarn can be extremely substantial but stays visibly distinct from Gorrund." (SKARN L32); "Even extreme Skarn settings must not recreate Gorrund anatomy." (SKARN L300)
- [POS] Interdependencies: "Shoulder width moves the upper back and clavicles." / "Chest depth changes ribcage volume." / "Limb thickness keeps joint transitions." (SKARN L112, L113, L117); "These protect plausibility without taking away meaningful control." (SKARN L120)
- [BAN] "There is no default "huge upper body, tiny legs" silhouette." (SKARN L94) — lower body carries mass "at every setting" (SKARN L94).
- [TEST] SK-04 "Narrow, lean, long-legged"; SK-07 "Broad frame, moderate muscle" (SKARN L330, L333); "narrow-frame and extremely muscular Skarn" must read as one population (SKARN L296).
- [SILENT] Joint hard minimum; numeric robusticity; frame write list (which variables Narrow/Broad change) — Skarn says only "inside Skarn limits".
- Cross-race (R2): joint scale "S > MF (S L24, L78)"; "S vs GO n.d." and "S vs GR n.d." (R2 L61). Thoracic depth "S vs GR n.d." (R2 L55).

### Sagekin
- [POS] Ribcage tendency (clarified): "the ribcage tendency is reduced depth, not an undefined global narrowing" (SAGEKIN L89); "slightly less ribcage depth" (SAGEKIN L140); "a slightly shorter torso relative to stature" (SAGEKIN L139).
- [POS] Torso control row: "Slightly shorter, shallower torso relative to height. Broad Sagekin keep genuinely broad torsos" (SAGEKIN L155).
- [POS] Frame scope: "Narrow, Balanced and Broad all apply within Sagekin ranges. Broad Sagekin stay possible, and Sagekin ancestry never means narrow or thin." (SAGEKIN L93)
- [BAN] Elven-boundary: "Pointed ears, exaggerated limbs, very light bones and other elven traits are never used to set Sagekin apart." (SAGEKIN L147)
- [POS] Coupling: "Chest depth changes ribcage volume, not surface inflation." (SAGEKIN L180); "Arm length keeps the shoulder, elbow and wrist relationships." (SAGEKIN L175)
- [TEST] SG-05 "Short and Broad" (SAGEKIN L190).
- [SILENT] Joint scale, joint minimum, long-bone robusticity (only the negative "very light bones" ban).
- [OPEN]/measurement: RM-OT-01 ribcage depth and breadth vs Marchfolk (R5 L89).

### Fenn
- [POS] Gracility: "a more gracile skeleton, with lower skeletal mass for their height" (FENN L32); "narrower joints and slenderer long bones" (FENN L33).
- [POS] Joint scale: "Wrists, elbows, knees and ankles look smaller relative to limb length than on same-height humans, with minimum anatomical boundaries." (FENN L115)
- [TEST]/hard minimum: "A Narrow, low-muscle, low-fat Fenn never gets implausibly tiny or fragile joints." (FENN L115)
- [POS] Torso/ribcage: "Somewhat shallower front to back, moderately narrow for height, somewhat vertically compact" (FENN L110); guard "Enough thoracic volume, never an implausibly tiny chest" (FENN L110).
- [POS] Wrists/ankles: "narrower wrists" (FENN L51); "narrower ankles" (FENN L52).
- [POS] Frame scope: "Narrow, Balanced and Broad all apply inside Fenn anatomy. A Broad Fenn is still biologically Fenn, and Narrow isn't the only authentic look." (FENN L44)
- [BAN] "Broad Fenn shoulders stay light-boned, never Skarn-like" (FENN L109); "Gracile never means fragile." (FENN L40)
- [SILENT] Which skeletal variables Fenn frame changes (only ECR universal L55 applies).
- ECR: "Greatest average skeletal gracility of the three elven populations" (ECR L312).

### Aelari
- [POS] "a more gracile skeleton than humans" / "less apparent joint mass" (AELARI L13, L15).
- [POS] Joint scale + hard minimum: "Shoulders, elbows, wrists, hips, knees and ankles are gracile compared with humans but structurally sufficient." … "hard minimum boundaries prevent implausibly tiny joints." (AELARI L130)
- [POS] Frame scope (explicit): "Narrow, Balanced and Broad change the real skeleton: clavicle, ribcage and pelvic breadth, joint relationships and overall skeletal presence." (AELARI L134)
- [POS] Independence: "Frame stays separate from muscle, fat, sex-related anatomy, height and presentation." (AELARI L134)
- [POS] Ribcage: "Vertically longer than Fenn, moderate width, relatively shallow depth" (AELARI L123); guard "never an extremely flat or narrow chest" (AELARI L123).
- [POS] Broad is skeletal: "Broad Aelari gain real skeletal breadth, not just muscle or fat" (AELARI L125); "Gracile never means narrow shoulders" (AELARI L49).
- [BAN] Skarn boundary: "Broad muscular Aelari never become narrow Skarn" (AELARI L171).
- ECR: "somewhat greater average skeletal structural presence than Fenn" (ECR L313).

### Vael
- [POS] "Gracile next to humans (especially Skarn), but more joint presence than Fenn or Aelari at wrists, elbows, knees, ankles, shoulders and hand and foot bases" (VAEL L37); guard "Never compact Skarn" (VAEL L37).
- [POS] Joint scale + hard bounds: "Joints are never oversized, and hard bounds prevent thin limbs on implausibly tiny or oversized joints." (VAEL L132)
- [POS] Frame scope (explicit): "Frame changes the clavicles, ribcage, pelvis, joints and skeletal presence, and stays independent of muscle, fat, height, sex-related anatomy and presentation." (VAEL L128)
- [POS] T-10: "shoulder and pelvic breadth are Skeletal Frame variables because frame changes them" (VAEL L121); UCCA mirror (UCCA L133).
- [BAN] Frame boundary: "a Narrow Vael is never a scaled-down Broad Vael" (VAEL L122).
- [POS] Thoracic depth: "Deeper front to back than Fenn or Aelari, moderate width, slightly shorter vertically than Aelari" (VAEL L120); depth "never faked with body fat, muscle, an oversized chest or uniform torso scaling. A Narrow, lean Vael keeps it." (VAEL L114)
- [TEST] "deep ribcage with a Narrow frame" risk combination (VAEL L155); VL-23 "Deep ribcage with Narrow frame stress test" (VAEL L194).
- ECR: "the greatest average joint, base and skeletal structural presence of the three" (ECR L314).

### Halvren
- [POS] Frame vs preset kept; "Valid underlying ranges may depend partly on ancestry, so a Broad Halvren isn't assumed identical to a Broad Marchfolk or Broad Aelari." (HALVREN L54)
- [BAN] "Narrow, Balanced and Broad remain Frame Presets, not ancestry categories" (HALVREN L137); "ancestry is never encoded into the presets" (HALVREN L137).
- [POS] Robusticity is multidimensional: skeletal expression spans "strongly gracile, moderately gracile, intermediate or relatively robust" … "never a global "Elf Gracility" slider" (HALVREN L105).
- [POS] Joints: "It fails if a highly gracile long bone connects through an implausibly massive joint just because two ancestry values were inherited independently." (HALVREN L133)
- [POS] Human family ≠ uniformly robust: "Generalized "human robustness" becomes human-family skeletal architecture and structural distributions where misleading." (HALVREN L463)
- [POS] Source tendencies: Skarn "Greater skeletal robustness, broader clavicles, deeper ribcage, more substantial neck and pelvis, heavier joints" (HALVREN L111); Vael "more joint and base presence than Fenn and Aelari ancestry" (HALVREN L114).
- [POS] No pure extremes: "Halvren don't normally reproduce the most population-specific skeletal extremes of a pure source population." (HALVREN L105)
- [BAN] UCCA: "Frame never encodes ancestry." (UCCA L293)
- [SILENT] Numeric joint scale; joint hard minimum.

### Durrim
- [POS] Long bones: "Long bones have greater skeletal structural presence relative to their length than equivalent Marchfolk anatomy, so shorter never means thinner" (DURRIM L40).
- [POS] Joints: "Joints (shoulders, elbows, wrists, hips, knees, ankles) trend toward substantial scale relative to limb length and stature, integrated with adjacent bones and never enlarged independently." (DURRIM L40)
- [BAN] Elbow/knee shorthand: "Elbows follow the upper-arm, forearm and joint relationship, never enlarged independently or used as dwarf shorthand." (DURRIM L113); "never large knees as a cosmetic dwarf feature" (DURRIM L119).
- [POS] Wrists: "Wrists trend toward substantial presence relative to hand and forearm length, coupled to forearm, hand base and frame." (DURRIM L113)
- [POS] Thorax: "Greater skeletal thoracic depth than equivalently tall Marchfolk" (DURRIM L29); "Greater skeletal ribcage breadth than equivalently tall Marchfolk" (DURRIM L30).
- [POS] Breadths unlocked: "Ribcage versus shoulders | Not locked together" (DURRIM L102) — broad ribcage + moderate shoulders etc. all valid.
- [POS] Mandatory: "Durrim skeletal structural presence must never be represented through muscle alone (mandatory)." (DURRIM L50)
- [POS] Frame scope: Narrow "May reduce ribcage, shoulder, pelvic and long-bone breadth and joint scale relative to other Durrim, while staying inside Durrim-specific minimum structural relationships" (DURRIM L127); Broad "May increase skeletal ribcage, shoulder and pelvic breadth and joint presence within coherent limits, never every dimension equally" (DURRIM L129).
- [POS] Balanced: "A central creator starting point, never the canonical, most correct or default NPC Durrim body" (DURRIM L128).
- [BAN] "Broad never automatically means muscular, fat, male or every skeletal dimension at maximum." (DURRIM L52)
- [POS] Frame–height independence: "no fixed height-frame packages" (DURRIM L131).
- [POS] Soft face coupling: "Broad skeletal frame may correlate softly and probabilistically with more craniofacial presence" (DURRIM L189).
- [TEST] Combined validity includes "minimum joint scale with maximum long-bone breadth" (DURRIM L139); "Same-composition frame | … confirm presets change skeleton, not composition" (DURRIM L147).
- [OPEN] Pelvis: "OPEN, requires detailed anatomical design." (DURRIM L32)
- Hard identity floor: the "Durrim-specific minimum structural relationships" (L127) is the only race-specific frame-floor phrase among the short races; content [SILENT].

### Grask
- [POS] Identity: "Elongated skeletal leverage and reach rather than compact structural mass." (GRASK L23); "a relatively slender skeletal silhouette for its stature (a skeletal proportion, not low body fat" (GRASK L9).
- [POS] Absolute vs relative: "bones and joints may be substantial in absolute terms while looking relatively lean compared with total height" (GRASK L31).
- [POS] Knees/ankles: "Knees are substantial in absolute structure for Grask stature and long lever arms and may look relatively lean against total height" (GRASK L217); "visually narrow never means structurally weak" (GRASK L217); ankle "narrow-looking anatomy never implies mechanically tiny joints" (GRASK L56).
- [POS] Thorax: "Moderate skeletal breadth, meaningful thoracic depth" … "with breadth and depth independently variable" (GRASK L38); "less broad relative to stature than Skarn, surviving composition neutralization" (GRASK L203).
- [POS] Frame scope: "Narrow, Balanced and Broad modify Grask skeletal breadth relationships only, never directly controlling height, limb, hand or foot length, muscularity or fat" (GRASK L249). Broad "may increase thoracic, shoulder and pelvic skeletal breadth and joint and base dimensions, but isn't Skarn, muscular, fat or maximum everything" (GRASK L70).
- [BAN] Narrow avoids "fragility caricature, pencil-thin joints, an extremely narrow chest and Aelari convergence"; Broad avoids "Skarn convergence, Gorrund assumptions, a blocky torso and visually shortened limbs" (GRASK L249).
- [POS] Correlation principle: "A population-level anatomical correlation does not automatically create a hard creator-control dependency." (GRASK L330); foot breadth: "never "frame preset → fixed foot breadth."" (GRASK L326).
- [TEST] Invalid combos: "the narrowest frame with the smallest joints at maximum height; maximum torso depth with narrowest breadth and extreme composition" (GRASK L255). GR-BODY-17 "Maximum height and narrow frame"; GR-BODY-18 "Minimum height and broad frame" (GRASK L295–L296).
- [OPEN] Pelvis "exact morphology OPEN" (GRASK L45, L208).
- [SILENT] Explicit joint hard minimum (only "pencil-thin joints" ban).

### Gorrund
- [POS] Definition: "Massive" means "skeletal breadth and depth, joint dimensions, axial scale, pelvic structure, limb-bone structural dimensions" (GORRUND L19); "Gorrund skeletal massiveness exists independently from Current Muscularity and Body-Fat Amount." (GORRUND L21)
- [POS] Joints: "Substantial joint structural presence appropriate to large load-bearing bones, without exaggerating the joints into monstrous anatomy." (GORRUND L74); "one of the strongest body signals across shoulders, elbows, wrists, hips, knees and ankles" (GORRUND L76).
- [POS] Long bones: "Long bones have greater absolute cross-sectional structural scale than smaller humanoids, with no numbers yet" (GORRUND L76); terminology: "use skeletal breadth, skeletal depth, bone cross-sectional structural scale and joint dimensions" (GORRUND L76).
- [POS] Elbows/wrists: "Elbows are substantial in absolute terms and coordinated with arm scale, never isolated knobs" (GORRUND L202); knees "never shrunk to emphasize limb mass or made bulbous" (GORRUND L196).
- [POS] Thoracic depth: "substantial thoracic skeletal depth relative to stature and breadth, producing a genuinely three-dimensional load-bearing torso" (GORRUND L42); "Thoracic skeletal depth (ribcage) stays separate from abdominal soft-tissue projection" (GORRUND L181).
- [POS] Hard identity floor (breadth): "the lower valid end of Gorrund thoracic breadth must still preserve Gorrund identity through depth, joints, axial integration and overall skeletal scale" (GORRUND L179).
- [POS] Frame scope: "Narrow, Balanced and Broad alter skeletal breadth relationships only, never directly setting height, muscle, fat, hand or foot size, face or personality." (GORRUND L220)
- [POS] Correlation: "a population-level anatomical correlation does not automatically create a hard creator-control dependency" (GORRUND L220); "broad frame never hard-links to maximum thoracic depth" (GORRUND L224); "Narrow skeletal breadth does not automatically mean low skeletal depth." (GORRUND L222)
- [POS] Allometry: "bone diameter, joint size, hands and feet never scale linearly with stature" (GORRUND L224).
- [BAN]/frame boundary: "about 208 cm with a Broad frame stays Gorrund without becoming Skarn" (GORRUND L224); Narrow keeps ALPC: "reduced breadth never removes thoracic depth, joint scale, pelvic and proximal-limb integration or structural continuity (a critical identity test)" (GORRUND L721).
- [POS] Joint–bone coupling: "Large bones need scaled joints, never maximum long-bone scale with minimum knees" (GORRUND L232); "Hands and wrists, and feet and ankles, correlate biologically inside valid envelopes without being hard-locked" (GORRUND L232).
- [TEST] GOR-BODY-12/13 axial-breadth extremes, 14/15 thoracic-depth extremes (GORRUND L140–L143); GOR-STRESS-06 "greater thoracic depth with lower breadth", 07 "greater breadth with moderate depth" (GORRUND L249); GOR-BODY-12/14 vs Broad Grask (GORRUND L244).
- [OPEN] Pelvis morphology OPEN (GORRUND L49).

### Pipkin
- [POS] Light construction: "lower skeletal breadth and depth, smaller joints and more gracile long-bone dimensions than Durrim at similar height" (PIPKIN L21); "never weak, frail, underweight, thin, low-muscle, low-fat" (PIPKIN L21).
- [POS] Joints: "Relative to Durrim at matched height, Pipkin generally have smaller skeletal joint dimensions (a tendency)" … "never one hard racial value" (PIPKIN L68).
- [POS] Long bones: "lower breadth and depth relative to length than Durrim at matched height, a major skeletal distinction" (PIPKIN L68).
- [POS] Thorax/pelvis: Thorax "moderate in breadth and depth; never childishly small, Durrim-deep or paper-thin" (PIPKIN L149); "The pelvis carries greater structural importance relative to the thorax than in Marchfolk reference anatomy" (PIPKIN L150).
- [POS] Frame scope: Narrow "may reduce shoulder, thoracic and pelvic breadth and joint size within validity while staying adult and healthy" (PIPKIN L68); Broad "may increase shoulder, thoracic and pelvic breadth and joints within validity and never becomes Durrim" (PIPKIN L168).
- [POS] Correlation: "Frame may influence pelvic breadth, but Narrow never erases the Pipkin pelvic relationship and Broad never exaggerates it into caricature." (PIPKIN L168)
- [BAN] "Never childlike, Fenn-like or fragile by requirement" (PIPKIN L45); "Never Durrim, miniature Skarn or automatically muscular; frame stays skeletal" (PIPKIN L46).
- [TEST] Durrim boundary carried by "joint dimensions, long-bone robusticity, extremity integration and the two distinct trunk systems" (PIPKIN L194); PIP-BODY-14 Broad Pipkin vs Narrow Durrim (PIPKIN L115); "no single width carries the race" (PIPKIN L197).
- [OPEN] "detailed joint dimensions" (PIPKIN L1542); "detailed pelvic morphology" (PIPKIN L1537).

### Cogling
- [POS] Fine construction: "comparatively narrow long-bone shafts" / "smaller absolute joint structures" / "lower structural mass than a height-normalized Marchfolk reference" (COGLING L117, L118, L120).
- [BAN] Fine does not mean "brittle", "weak", "hollow-boned", "low-density bone" (COGLING L124–L129); "Bone material properties are not inferred from visual gracility." (COGLING L132)
- [POS] Joints: "Cogling joints are relatively small in absolute dimensions and visually articulated, but not fragile." (COGLING L236); "fine in scale but fully adult" (COGLING L740).
- [POS] Joint-control decomposition: "skeletal breadth; skeletal depth; articular-region scale; muscular/tendinous coverage; adipose/soft-tissue coverage" (COGLING L743–L747).
- [POS] Robusticity is its own axis: "Long-bone shaft robusticity is a distinct biological parameter from limb length and muscularity." (COGLING L755); "valid individuals may range within a Cogling-specific envelope" (COGLING L757).
- [BAN] "High muscularity must not automatically thicken bone to Durrim proportions." / "Low muscularity must not make bones implausibly thin." (COGLING L759, L761)
- [POS] Frame may influence "clavicular breadth; thoracic breadth; pelvic breadth; long-bone robusticity within limits; joint dimensions" (COGLING L775–L779); not "height, muscle, fat, face, sex-related anatomy, culture or personality" (COGLING L781).
- [POS] AC-9: "those parameters remain separately adjustable (§53, §69) and are never hard-determined by Narrow, Balanced or Broad" (COGLING L783).
- [BAN] Broad boundary: "Broad does not mean Durrim." (COGLING L801); must retain "the narrow-core population relationship relative to structural-mass races" (COGLING L796). Narrow must not become "Fenn; childlike; fragile; undernourished" (COGLING L808–L811).
- [TEST] Invalid: "minimum joint dimensions + maximum muscularity producing implausible transitions"; "broad frame + maximum robusticity drifting into Durrim structure" (COGLING L1053, L1054).
- [POS] Thorax: "fully adult, moderate in depth and comparatively narrow-to-moderate transversely" (COGLING L102).
- [OPEN] "Joint breadth/depth ranges remain OPEN." (COGLING L242); "joint dimensions and long-bone robusticity distribution" (COGLING L3167); "thoracic dimensions" (COGLING L3162).

### Saurin
- [POS] Joint scale: "Joint dimensions should remain visibly adult and suited to the approved skeleton." (SAURIN L320); not "fine-jointed like the Cogling tendency", not "structurally concentrated like Durrim", not "massively jointed like Gorrund" (SAURIN L323–L325).
- [POS] "Frame variation can alter joint breadth/depth within race-valid envelopes." (SAURIN L327)
- [POS] Skeletal mass: "provisionally moderate-to-substantial" (SAURIN L331); "Bone robusticity and muscular development remain separate dimensions." (SAURIN L339)
- [POS] Frame scope (most explicit in roster): "Frame changes shoulder breadth, thoracic width (depth ±2 % only), pelvic width, limb and joint girth, hand/foot breadth and the frame component of the tail base." (SAURIN L4170) "Frame does not change stature, long-bone or axial lengths, the skull, or pelvic depth / sacral-caudal organization." (SAURIN L4170)
- [BAN] Boundaries: "A Narrow Saurin remains Saurin through axial/pelvic/tail architecture." / "A Broad Saurin cannot become Gorrund simply through breadth." (SAURIN L352, L354)
- [NUM] Hard bounds (constant height): "thoracic depth ±8 %; thoracic width ±7 %; axial trunk length ±10 %; shoulder breadth ±8 %; pelvic width ±7 %" (SAURIN L4166). Coupled: "thoracic depth/width ratio stays 0.80–1.00 (deep narrow-to-moderate shell); the thoracic depth floor scales with breadth." (SAURIN L4168)
- [NUM] Frame-dependent tail cap: "~78 % H on a Balanced frame at reference composition; 80 % H on a Broad frame; ~72 % H on a Narrow, high-fat body" (SAURIN L4151).
- [TEST] "frame × composition × joint scale" (SAURIN L2577).
- [OPEN] "joint distributions; bone robusticity distributions" (SAURIN L580–L581); "a numeric Broad-vs-Gorrund boundary" (SAURIN L4267).

### Cross-race comparatives (Part 1)
- **Structural-mass axis (short races):** "Cogling → Pipkin → Durrim broadly progresses from finer to greater skeletal structural presence." (SR L41); "This is not a universal linear morph" (SR L43); "Muscularity and adiposity cannot substitute for skeletal structural presence." (SR L48). Spec support: Cogling "lower skeletal breadth/depth than Durrim" (COGLING L119); Pipkin lighter than Durrim (PIPKIN L21, L68); Durrim > Marchfolk (DURRIM L40). Measurement: RM-SR-03 (R5 L41). Note: Pipkin vs Cogling joint/shaft ordering is only implied by the axis (SR L41); neither Pipkin nor Cogling spec states a Pipkin–Cogling joint comparison [SILENT in specs].
- **Short-race frame boundaries:** "a Broad Cogling cannot become Durrim by increasing width; a Narrow Durrim cannot become Cogling by reducing muscle" (SR L61); failure "Narrow low-muscle Durrim losing structural concentration" (SR L125); "High-muscle Cogling losing fine skeletal identity" (SR L128).
- **Large races (R2 table):** Thoracic/axial breadth "GO > S > GR" (R2 L54); thoracic depth "GO > S; GO > GR; S vs GR n.d." (R2 L55); joint scale "GO > GR; S vs GO n.d. … S vs GR n.d." (R2 L61); skeletal presence "GO and S high, GR rangy. GO vs S is a difference of degree and architecture" (R2 L63). Breadth inversion "Population vs individual; covered by LR-04" (R2 L141). LR-04 "Breadth can invert here." (R2 L94).
- **Elves (ECR):** "Fenn, then Aelari, then Vael" gracility→structural presence (ECR L316); "It never becomes three fixed bone-thickness presets." (ECR L316); Broad elf "never a human skeleton, Skarn or Durrim anatomy, automatic muscularity or automatic obesity" (ECR L55); Vael depth "skeletal, never muscle or fat" (ECR L29).
- **Saurin positioning:** between Fenn and Durrim/Gorrund on skeletal mass (SAURIN L334–L335); joints distinct from Cogling/Durrim/Gorrund (SAURIN L323–L325).
- **Joint hard minimums — explicit in canon:** Fenn (FENN L115), Aelari (AELARI L130), Vael (VAEL L132; also an upper bound), Durrim's "Durrim-specific minimum structural relationships" (DURRIM L127), UCCA umbrella (UCCA L131), RM-UB-03 "including race hard minimums" (R5 L81). Joint-minimum statements are ban-style but not "hard minimum" wording for Grask ("pencil-thin joints", GRASK L249), Gorrund ("never maximum long-bone scale with minimum knees", GORRUND L232), Cogling (COGLING L1053), Pipkin ("never weak, frail", PIPKIN L21). [SILENT]: Marchfolk, Skarn, Sagekin, Halvren, Saurin (Saurin has only "visibly adult", SAURIN L320).
- **Explicit frame-variable lists:** Marchfolk (L27), Aelari (L134), Vael (L128), Durrim (L127/L129), Grask (L70/L249), Gorrund (L220), Pipkin (L68/L168), Cogling (L775–L779), Saurin (L4170, with never-change list). Skarn, Sagekin, Fenn, Halvren give no list (generic "inside X limits").
- **Thoracic depth vs width directions:** Deeper than MF: Skarn (L22), Durrim (L29), Gorrund (L42, "relative to stature and breadth"). Shallower than MF: Sagekin (L140), Fenn (L110), Aelari (L123 "relatively shallow"). Vael deeper than Fenn/Aelari (L120). Pipkin "moderate" and not Durrim-deep (L149). Cogling "moderate in depth" (L102). Grask "meaningful", non-directional (L38–L39). Saurin numeric ratio 0.80–1.00 (L4168) — the only numeric depth:width canon.

### Candidate classification — Part 1 open questions
| # | Open question | Class | One-line justification |
|---|---|---|---|
| F1 | Per-race joint-scale envelopes (knee/elbow/wrist/ankle ÷ adjacent bone) | **B** | Direction exists for 12/13 races (e.g. DURRIM L40, PIPKIN L68, FENN L115, GORRUND L74); numbers are RM-UB-03/RM-LR-05/RM-SR-03. |
| F2 | Joint hard-minimum values | **B** | Canon already requires the minimum (AELARI L130, VAEL L132, UCCA L131); only the number awaits meshes (R5 L81). |
| F3 | Joint minimum for races silent on it (Marchfolk, Skarn, Sagekin, Halvren, Saurin) | **A** (suggestion) | A qualitative "joints never implausibly tiny/oversized" line can be authored now from UCCA L131 without new biology. |
| F4 | Long-bone robusticity distributions | **B** | Directional vs MF/Durrim in Durrim L40, Pipkin L68, Cogling L117, Fenn L33, Gorrund L76; UCCA L355 keeps distributions OPEN. |
| F5 | Skarn vs Gorrund joint scale; Skarn vs Grask joint scale and thoracic depth (n.d.) | **C** | R2 L55/L61 find no canon chain; AD-4 treats S–GO as architectural; any useful order needs RM-LR-03/05. |
| F6 | Thoracic depth ÷ breadth numbers (non-Saurin) | **B** | Directions above; numbers RM-LR-02, RM-OT-01/02, RM-SR-06. |
| F7 | Numeric frame write values (what Narrow/Broad write per race) | **C** | Canon gives scope, not magnitudes; R5 L16 requires Narrow/Broad meshes. |
| F8 | Saurin numeric Broad-vs-Gorrund boundary | **C** | Explicitly carried OPEN (SAURIN L4267); needs both meshes. |
| F9 | Pelvic morphology (Grask, Gorrund, Durrim, Pipkin, elves) | **D** | Marked OPEN biology in each spec (GRASK L45, GORRUND L49, DURRIM L32, PIPKIN L1537; ECR L32). |
| F10 | Frame variable list for Skarn/Sagekin/Fenn/Halvren | **A** (suggestion) | UCCA L119 already defines the universal list; a pointer line adds no biology. |
| F11 | Halvren inherited joint/robusticity ranges | **D** | Depends on unwritten inheritance rules: ranges "may depend partly on ancestry" (HALVREN L54; also L105). |
| F12 | Structural-mass axis ordering numbers (short races) | **B** | Direction canon (SR L41); RM-SR-03 supplies numbers. |

---

# PART 2 — COMPOSITION

### Marchfolk
- [POS] Layers independent: muscularity, fat amount/distribution, regional muscle "vary independently of frame, for example Narrow and muscular, Narrow and heavy … Broad with high body fat" (MARCHFOLK L27).
- [POS] Fat amount ≠ distribution: "Body-fat amount (how much adipose tissue overall) and body-fat distribution (where it's preferentially represented) are separate parameters" (MARCHFOLK L282); "distribution never substitutes for amount" (MARCHFOLK L282).
- [POS] Regional groups: "shoulders, chest, upper arms, forearms, abdomen, waist, hips, gluteal region, thighs, calves and neck" (MARCHFOLK L31); regional emphasis examples "developed shoulders and forearms, a stronger lower body" (MARCHFOLK L92).
- [POS] Athletic is composition: "a curated combination of physical-composition relationships (not skeletal proportions) and muscularity values" (MARCHFOLK L204).
- [POS] Mass: "Visible mass comes from height, frame, muscle, fat and regional composition together, never one generic scale value" (MARCHFOLK L31).
- [BAN] Not defined by "one body composition" (MARCHFOLK L13); "ruggedness, manual labor … and muscularity come from culture, background, occupation, environment or history" (MARCHFOLK L35).
- [SILENT] Muscular Development Capacity (term absent); fat-distribution tendencies; sex shift in composition (only height, L23).
- Reference composition: [SILENT] — validation is "never only the reference height" (MARCHFOLK L249), no reference composition named.

### Skarn
- [POS] Capacity: "greater skeletal robustness and a higher Muscular Development Capacity (biological range; Current Muscularity stays free, §5)" (SKARN L26); "a higher Muscular Development Capacity (not a default Current Muscularity)" (SKARN L80). Direction stated; magnitude [SILENT].
- [POS] Independence: "Composition is independent of frame: low or high muscle, low or high fat, regional development and different conditioning levels." (SKARN L36)
- [BAN] "They are not scaled-up Marchfolk and not automatically muscular." (SKARN L7); "Exaggerated bodybuilder anatomy is not the default." (SKARN L36)
- [POS] Regional: "neck and traps, shoulders, arms, forearms, chest, back, core, glutes, thighs and calves" (SKARN L102); "Regional values stay tied to overall muscularity so no single group becomes implausible." (SKARN L102)
- [TEST] Anti-stereotype: "lean, heavy, elderly, soft-featured … narrow-frame and extremely muscular Skarn" (SKARN L296); "Racial identity survives low muscle, high body fat and advanced age." (SKARN L309)
- [SILENT] Fat-distribution tendency; sex shifts; reference composition (SK-01 is just "Reference Skarn", SKARN L327).

### Sagekin
- [POS] "Sagekin have the full human range of muscle, fat distribution, regional development, conditioning and age-related composition." (SAGEKIN L101)
- [BAN] "Their scholarly reputation never reduces Muscular Development Capacity." (SAGEKIN L101); "Sagekin are never defined by thinness." (SAGEKIN L143); "identity never depends on being tall, narrow, lean or weak" (SAGEKIN L161).
- [POS] Regional: "The proposed universal regional-development framework from Skarn applies." (SAGEKIN L165)
- [TEST] SG-06 "Broad and highly muscular", SG-07 "Broad and high body fat", SG-08 "Narrow and muscular" (SAGEKIN L191–L193).
- [SILENT] Fat-distribution tendency; sex shifts. Reference: "SG-01 | Reference: 178 cm, Balanced" — no composition (SAGEKIN L186).

### Fenn
- [POS] "Very lean, average, Broad-framed, highly muscular, high-body-fat and elder Fenn are all explicitly allowed." (FENN L58)
- [BAN] "Fenn identity never depends on thinness" (FENN L58); "soft tissue never erases the Fenn skeleton" (FENN L130); Broad muscular Fenn "must never become muscular human silhouettes" (FENN L357).
- [TEST] "The same composition settings act on each race's own foundation." (FENN L130); stress set (FENN L349).
- [POS] Regional: "thigh and calf development" (FENN L52).
- [SILENT] Capacity; fat distribution; sex. Reference: "FN-01 | Reference: 181 cm, Balanced" (FENN L84), no composition.

### Aelari
- [POS] "The full system applies: overall muscle, fat distribution, regional development and conditioning." (AELARI L62)
- [BAN] "Aelari identity never depends on thinness." (AELARI L62); "Soft tissue never erases the Aelari skeleton, and muscle never turns Aelari into Skarn." (AELARI L159)
- [TEST] Composition tests (AELARI L159, L472).
- [SILENT] Capacity; fat-distribution tendency; sex shifts — the only sex mention is "No mandatory hip width by race or sex-related anatomy" (AELARI L126). Reference: "AE-01 | Reference: 190 cm, Balanced" (AELARI L85).

### Vael
- [POS] "Muscle, fat, regional development and conditioning stay fully independent." (VAEL L145)
- [BAN] "Identity never depends on thinness, muscle or fat." (VAEL L51); fail if ""Deep-bodied" becomes high body fat." (VAEL L206) / "They require muscle." (VAEL L207).
- [TEST] VL-17 "Skeleton is judged before soft tissue" (VAEL L150); VL-18 "Vael stay recoverable through skeleton, joints, limbs" (VAEL L151).
- [SILENT] Capacity; fat distribution; sex. Reference: "VL-01 | Reference: 178 cm, Balanced" (VAEL L80).

### Halvren
- [POS] "Muscle and fat aren't ancestry percentages" (HALVREN L54); composition "stays fully separate from skeletal inheritance" (HALVREN L137).
- [BAN] "elven expression isn't lean, human expression isn't heavier, Skarn ancestry isn't muscular, Aelari ancestry isn't thin, Vael ancestry isn't dense" (HALVREN L137); "thinness is never shorthand for elven ancestry" (HALVREN L54).
- [POS] Capacity can shift with ancestry (directional, conditional): "Skarn ancestry may shift the valid distribution or upper potential for muscular development, but never automatically makes a Halvren muscular" (HALVREN L447).
- [POS] Sex: "Sex-related anatomy stays separate from frame, height, muscle, fat, face, hair and presentation" (HALVREN L54); "exact sex-related inheritance stays within the broader unresolved anatomical-system review" (HALVREN L54) [OPEN].
- [TEST] HV-08 higher fat, HV-09 high muscle (HALVREN L366–L367); HV-36–43 composition set (HALVREN L374).
- Reference composition: [SILENT]; HV-03 "where "balanced" never means every parameter at 50/50" (HALVREN L361); UCCA "No 50/50 default." (UCCA L293).

### Durrim
- [POS] Full composition range: "lean, average, muscular, heavy, low-muscle high-fat, high-muscle high-fat and low-muscle low-fat within validity" (DURRIM L54).
- [POS] "Durrim aren't universally stocky in composition: the skeleton trends compact and substantial, the composition needn't." (DURRIM L54)
- [OPEN] Fat distribution: "Fat distribution isn't forced toward belly, waist or face, and sex-related differences depend on the unresolved universal system." (DURRIM L54); distribution regions "(face and neck, upper torso, abdomen, waist, hips, glutes, upper arms, thighs) is separate from amount, with sex-related patterns OPEN" (DURRIM L135).
- [POS] Regional: "neck, trapezius, shoulders, chest, back, upper arms, forearms, abdomen, glutes, thighs and calves" (DURRIM L135); "no automatic forearm, shoulder or back emphasis from labor stereotypes" (DURRIM L54).
- [POS] Mass: "Durrim possess unusually high body volume and structural mass relative to their stature compared with Marchfolk" (DURRIM L54).
- [BAN] "no artificially high minimum to keep the silhouette, since the skeleton carries racial identity" (DURRIM L135); never "spherical torso, huge belly, tiny legs or the comedic dwarf silhouette" (DURRIM L135).
- [TEST] "Low-muscle Durrim (permanent validation)" — "fails if removing muscle makes them look human" (DURRIM L135); composition neutralization "fails if only muscular or heavy characters read as Durrim" (DURRIM L73).
- [OPEN] Sex: "Durrim magnitudes stay OPEN" (DURRIM L58).
- [SILENT] Muscular Development Capacity (term absent in Durrim). Reference composition [SILENT] (only reference height 137 cm, DURRIM L85).

### Grask
- [POS]/[OPEN] Capacity: "Muscular Development Capacity (the biological range) stays separate from Current Muscularity, and whether Grask capacity differs from humans is OPEN, never inferred from silhouette." (GRASK L72); "long visible muscles never imply greater strength or capacity" (GRASK L251). **No direction.**
- [POS] Muscularity: "never universally skinny, sinewy, muscular or weak-looking" (GRASK L72); high muscle "never shortening the apparent limbs until the body reads Skarn-like" (GRASK L251).
- [POS] Muscle wraps skeleton: "pectorals don't change thoracic breadth, abdominal fat doesn't change the pelvis, shoulder muscle doesn't move the shoulder joint" (GRASK L72).
- [POS] Regional: "neck, shoulders, upper arms, forearms, chest, back, abdomen, glutes, thighs and lower legs, with the creator-facing control hierarchy provisional" (GRASK L251).
- [OPEN] Fat distribution: "Fat distribution varies meaningfully without requiring belly, face or hip accumulation (population tendencies OPEN)." (GRASK L251)
- [BAN] "troll biology is never synonymous with gauntness, a pot belly or obesity" (GRASK L72); avoid "a generic obese human, ogre assumptions and a comedic troll belly" (GRASK L251).
- [POS] Circumference decomposition: "visible circumference comes from bone, muscle and fat, kept distinct" (GRASK L251).
- [OPEN] Sex: "whether average skeletal dimorphism is minimal, moderate or strong is OPEN" (GRASK L76).
- [TEST] GR-BODY-06–09 low/high muscle, higher fat, high muscle+high fat (GRASK L127–L130); "High muscle | Fails if it becomes Skarn with longer arms" (GRASK L100).
- [NUM]/reference: "GR-BODY-01 | Reference: about 218 cm, Balanced, moderate composition" (GRASK L122).

### Gorrund
- [OPEN] Capacity: "Whether their muscular-development capacity differs from humans or other races is OPEN, never inferred from skeletal scale." (GORRUND L82); "Whether Gorrund have a different muscular-development ceiling or distribution is OPEN, never settled from appearance." (GORRUND L228). **No direction.**
- [POS] "Gorrund don't require high current muscularity, and a low-muscle Gorrund stays structurally massive." (GORRUND L82)
- [BAN] "High muscle with high fat is supported but isn't the canonical body" (GORRUND L82); never "large belly = ogre identity" (GORRUND L82); high muscle never "creating a generic bodybuilder, turning the Gorrund into Skarn" (GORRUND L228).
- [POS] Regional muscle: "neck, shoulders, upper arms, forearms, chest, back, abdomen, glutes, thighs, calves" with "controls provisional" (GORRUND L228); "equal total muscle can be distributed differently" (GORRUND L228).
- [OPEN] Fat distribution: regions "face and neck, chest, upper back, abdomen, flanks, pelvis, glutes, thighs, limbs" — "with biological distributions future work" (GORRUND L228).
- [POS] ALPC under composition: "it fails if it appears only once muscle is added" (GORRUND L722); "Low fat reveals rather than creates the structure" (GORRUND L723).
- [OPEN] Sex: "Sex-related anatomy and dimorphism are OPEN, never assuming human-identical dimorphism, huge males and small females" (GORRUND L82).
- [TEST] GOR-BODY-16 "low muscle and low fat (the skeleton alone carries the race)" (GORRUND L228); composition-neutral recognition "Fails if it needs muscle bulk or fat volume to read Gorrund" (GORRUND L243).
- [NUM]/reference: "GOR-BODY-01 | Reference: about 229 cm, Balanced, moderate composition" (GORRUND L129).

### Pipkin
- [OPEN] Capacity: "Muscular-development capacity differences are OPEN, never inferring reduced strength from stature." (PIPKIN L72); "muscular-development capacity is OPEN, never lowered because Pipkin are small" (PIPKIN L182); "Muscular Development Capacity distribution" (PIPKIN L1543). **No direction; a downward shift is banned.**
- [POS] "a highly muscular Pipkin may have substantial external volume over a still comparatively light skeleton" (PIPKIN L182).
- [POS] Regional: "shoulders, arms, forearms, chest, back, abdomen, glutes, thighs and calves" (PIPKIN L182). (Neck not named.)
- [OPEN] Fat distribution: "(face, torso, abdomen, hips, glutes, thighs, arms) is independent of amount (patterns future work)" (PIPKIN L182); "body-fat distribution patterns" (PIPKIN L1544).
- [BAN] "halflings are never assumed chubby, round, lean or food-loving" (PIPKIN L72); "no "round halfling" default" (PIPKIN L182); "no hidden physique packages (never Broad → muscular → high fat or Narrow → lean → low muscle)" (PIPKIN L186).
- [POS] "Pelvic skeletal contribution is not wide hips caused by body fat." (PIPKIN L184)
- [TEST] Low muscle "fails if it reads as a child" (PIPKIN L182); PIP-BODY-06–09 (PIPKIN L107–L110).
- [POS]/[OPEN] Sex: "Sex-related physical anatomy may influence relevant pelvic, thoracic, facial, soft-tissue and other biological relationships" (PIPKIN L1491) but "does not determine height, frame, muscularity, fat amount" (PIPKIN L1492); magnitude OPEN (PIPKIN L1545).
- [NUM]/reference: "PIP-BODY-01 | Reference: about 107 cm, Balanced, moderate composition, neutral presentation; the central adult read" (PIPKIN L102).

### Cogling
- [POS] Capacity required as a representable variable: §69 list includes "muscular-development capacity" (COGLING L1038); "Muscular Development Capacity and Current Muscularity remain independent." (COGLING L818).
- [OPEN] "The population may have its own capacity distribution, but exact limits are OPEN." (COGLING L318); "Exact population capacity remains OPEN." (COGLING L826). **No direction; a downward inference is banned:** "Fine bones do not logically require low muscular-development capacity." (COGLING L320)
- [POS] "Cogling may support substantial muscle development on a fine skeletal foundation." (COGLING L820); "Muscle shape follows actual attachment and segment geometry rather than globally scaled Marchfolk musculature." (COGLING L822)
- [BAN] "Muscularity cannot serve as a proxy for age, sex, occupation or racial authenticity." (COGLING L838)
- [OPEN] Fat distribution regions "abdomen; hips; thighs; upper arms; chest; face" (COGLING L859–L864); "Exact Cogling population tendencies remain OPEN." (COGLING L869)
- [BAN] "No required round belly, soft-cheeked gnome look or childlike distribution is approved." (COGLING L867); no required "tiny old inventor" silhouette (COGLING L331).
- [TEST] "At higher amounts, underlying skeletal and segment relationships must remain recoverable diagnostically." (COGLING L852)
- [OPEN] Sex: "Magnitude and morphology of Cogling sex-related dimorphism remain OPEN." (COGLING L352)
- [SILENT] Regional muscle groups are not enumerated (only "regionally developed physiques", COGLING L303).
- Reference: "COG-BODY-01 | Reference adult at ~91 cm; neutral material/presentation" — no composition (COGLING L453); neutral preset set includes "reference/balanced", "reference/high muscularity", "reference/high adiposity" (COGLING L2944–L2946).

### Saurin
- [POS] Capacity is a variation axis: "Saurin support broad independent variation in: Current Muscularity; Muscular Development Capacity; body-fat amount; body-fat distribution" (SAURIN L358–L362). Direction [SILENT].
- [POS] Regional muscle: "limbs, girdle, epaxial neck and dorsal trunk, thigh, posterior shank, proximal-mid tail; joints, hands and feet excluded" (SAURIN L4172).
- [POS] Fat depot map (directional ordering, species-level): "Body fat is genuine soft-tissue volume (ventral-abdominal strongest, flank/hip, graded proximal caudal, minor gular, light general)." (SAURIN L4172) — while "Exact population adipose tendencies remain OPEN." (SAURIN L4172; also L383, L2508, L4268).
- [BAN] "Prohibited: human pectoral blocks, rectus/six-pack segmentation, human gluteal/buttock mass, generic bodybuilder-width transformation, uniform inflation." (SAURIN L4172); "Adipose tissue is not prohibited by scales or reptilian ancestry." (SAURIN L379); "No universal" dry-lizard silhouette (SAURIN L381).
- [POS] Tail composition: "Tail muscularity follows Physical Composition (proximal-mid emphasis, zero at the tip); there is no independent tail-muscle slider." (SAURIN L4152); "Fat concentrated at the caudal root is invalid" (SAURIN L4153).
- **E/B (§263) and distinctness from fat:**
  - [POS] "biological tissue tendencies, not adipose; they are not part of body fat and are not controlled by it" (SAURIN L385).
  - [POS] Form: "E is ventrolateral-to-lateral fullness of the lower rib cage and upper abdomen that fills the sub-costal waist." (SAURIN L4234); "B is one continuous field across the midline over the lower thorax and upper abdomen, fading into the flanks." (SAURIN L4234)
  - [POS] "Both persist at low body fat, stack with high fat under the guards below, and are never folded into the fat control." (SAURIN L4234)
  - [NUM] E: male 0 cm, female centre 2.0 cm, "no separate ceiling" (SAURIN L4229). B: male 0 cm, female centre 1.6 cm, "3.0 cm ceiling, subject to the shared thoracic depth/width ≤ 1.00 guard" (SAURIN L4230). Lower axial trunk +7 % (bound ±10 %), pelvic band +5.5 % (bound ±7 %) (SAURIN L4227–L4228).
  - [NUM] Clamps: "Narrow + B 3.0 cm → CONSTRAIN B to ~2.1 cm" ; "Narrow + high fat + female-centre B 1.6 cm → CONSTRAIN B to ~1.5 cm" (SAURIN L4248, L4249).
  - [POS] "Ventral fullness shares the thoracic depth/width ≤ 1.00 guard (§258) with thoracic depth, frame and fat." (SAURIN L4247)
  - [POS] Sex-shift scope: "Stature, skeletal frame, muscle, generic fat, tail, skull/face and the cranial-display family receive no sex shift" (SAURIN L4220); "The female tendency is anti-hourglass" (SAURIN L4221).
  - [POS] UCCA placement: "E/B live in Slot 7, never under fat" (UCCA L175); anti-hourglass validators "no waist narrowing as a sex signal; no paired ventral masses; no hip flare; no buttocks" (UCCA L176).
  - [OPEN] "whether B later proves related to a reproductive fat body (a plausible future explanation, not canon)" (SAURIN L4244); "statistical spreads of the sex-shifted distributions around their centres" (SAURIN L4273).
- [NUM]/reference: reference accounting at "equal stature 187.9 cm, Balanced, reference composition" (SAURIN L4236); tail cap "~78 % H on a Balanced frame at reference composition" (SAURIN L4151). The values of "reference composition" are [SILENT].

### Cross-race comparatives (Part 2)
- **Capacity direction by race:** stated higher — Skarn (SKARN L26, L80); conditional ancestry shift — Halvren (HALVREN L447); "never reduces" — Sagekin (SAGEKIN L101); OPEN, no direction — Grask (GRASK L72), Gorrund (GORRUND L82, L228), Pipkin (PIPKIN L72, L182; "never lowered"), Cogling (COGLING L318, L826; "do not logically require low", COGLING L320); variation axis, no population direction — Saurin (SAURIN L360); term absent — Marchfolk, Fenn, Aelari, Vael, Durrim [SILENT]. UCCA: Grask/Gorrund/Pipkin/Cogling "no population shift is invented" (UCCA L164). R2 resolved the Skarn "muscle volume" ambiguity via the capacity term (R2 L139); Gorrund cites Skarn's "already-approved higher Muscular Development Capacity" (GORRUND L239).
- **Fat-distribution tendencies:** OPEN/future for Durrim (L135), Grask (L251), Gorrund (L228), Pipkin (L182, L1544), Cogling (L869), Saurin population (L4172, L4268); Saurin has a canonical species depot ordering (L4172). [SILENT] Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Halvren (beyond "distribution" as a separate parameter). UCCA BIO OPEN "fat-distribution tendencies" (UCCA L355).
- **Sex shifts in composition:** only Saurin has canon centres (§263), and they are explicitly *not* fat/muscle (SAURIN L4220). OPEN magnitudes: Durrim (L58), Grask (L76), Gorrund (L82), Pipkin (L1545), Cogling (L352). Halvren OPEN via inheritance (L54). [SILENT] Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael. Short-race like-for-like rule (SR L168–L169).
- **Stereotype bans by race:** UCCA L169 (four named); SR L195–L198 ("must not force" Durrim muscle/beards, Pipkin roundness/large feet/cuteness, Cogling thinness/…); Pipkin L72/L186; Grask L72/L251; Gorrund L82/L228; Durrim L135; Cogling L867; Skarn L36; Halvren L137.
- **Composition inversion tests:** SR-COMP-10 "Broad/high-muscle Cogling vs Narrow/low-muscle Durrim; heavy Pipkin vs lean Durrim; lean Pipkin vs higher-fat Cogling" (SR L160); LR-10 large-race inversion PASS (R2 L100).
- **Regional muscle groups:** neck named by Marchfolk (MARCHFOLK L31), Skarn ("neck and traps", SKARN L102), Durrim (plus trapezius, DURRIM L135), Grask (GRASK L251), Gorrund (GORRUND L228); Pipkin omits neck (PIPKIN L182); Cogling enumerates none (COGLING L303); Saurin uses non-human groups and excludes joints/hands/feet (SAURIN L4172). Elves and Sagekin defer to the general system (FENN L52; AELARI L62; SAGEKIN L165).

### Central reference body — what each spec says the neutral/reference composition is
| Race | Reference body statement | Composition named? |
|---|---|---|
| Marchfolk | 173 cm Reference Height (MARCHFOLK L286); tests "never only the reference height" (L249) | No |
| Skarn | "SK-01 | Reference Skarn" (SKARN L327) | No |
| Sagekin | "Reference: 178 cm, Balanced" (SAGEKIN L186) | No |
| Fenn | "Reference: 181 cm, Balanced" (FENN L84) | No |
| Aelari | "Reference: 190 cm, Balanced" (AELARI L85) | No |
| Vael | "Reference: 178 cm, Balanced" (VAEL L80) | No |
| Halvren | 178 cm reference height (HALVREN L156); HV-03 balanced ≠ 50/50 (L361) | No (and no single reference body) |
| Durrim | reference about 137 cm (DURRIM L85) | No |
| Grask | "Reference: about 218 cm, Balanced, moderate composition" (GRASK L122) | "moderate" (undefined) |
| Gorrund | "Reference: about 229 cm, Balanced, moderate composition" (GORRUND L129) | "moderate" (undefined) |
| Pipkin | "Reference: about 107 cm, Balanced, moderate composition, neutral presentation" (PIPKIN L102) | "moderate" (undefined) |
| Cogling | "Reference adult at ~91 cm; neutral material/presentation" (COGLING L453) | No |
| Saurin | "equal stature 187.9 cm, Balanced, reference composition" (SAURIN L4236) | "reference composition" (values undefined in spec) |

- Tension to note: every reference case that names a frame says **Balanced**, while UCCA states "Balanced is not the canonical or default body" (UCCA L121) and Durrim/Grask/Gorrund say Balanced is a starting point, not canonical (DURRIM L128; GRASK L70; GORRUND L80). R5 frames the reference mesh as "central tendency" (R5 L16). No spec defines "moderate"/"reference" composition numerically; UCCA has no definition either (searched: only "reference composition" at UCCA L147, quoting Saurin).
- Does building a central reference body need any composition *distribution*? From the text: **no**. The reference cases name a single central composition point ("moderate"), not a distribution. Capacity is a ceiling (UCCA L161) that a moderate Current Muscularity does not reach, and fat-distribution tendencies are OPEN with explicit guards against forced belly/face/hip accumulation (GRASK L251; DURRIM L54) — so a neutral, untilted distribution is the only canon-compatible choice. Exception: Saurin's reference body must place fat by its canonical depot ordering (SAURIN L4172) and must carry E/B at the sex-appropriate centres if a female reference is built (SAURIN L4229–L4230).

### Candidate classification — Part 2 open questions
| # | Open question | Class | One-line justification |
|---|---|---|---|
| C1 | Capacity distribution — Grask, Gorrund, Pipkin, Cogling | **D** | Explicitly OPEN biology with "no population shift is invented" (UCCA L164); a universal VAL ceiling works meanwhile. |
| C2 | Capacity magnitude — Skarn (direction "higher" only) | **B** | Direction is canon (SKARN L26); ceiling size comes later. |
| C3 | Capacity shift — Halvren with Skarn ancestry | **D** | Depends on unwritten inheritance rules (HALVREN L447). |
| C4 | Capacity for silent races (Marchfolk, elves, Durrim) | **A** (suggestion) | Under UCCA L163 the default is a VAL ceiling; a "no population shift" pointer line adds no biology. |
| C5 | Fat-distribution tendencies, all non-Saurin races | **D** | OPEN in every spec that mentions it; bans already say what it must not be. |
| C6 | Saurin population adipose tendencies (beyond the depot order) | **B** | Ordering is canon (SAURIN L4172); numbers/spreads remain (L4268). |
| C7 | Definition of "moderate/reference composition" for reference meshes | **A** (suggestion) | Needed for RM meshes; can be authored now as a central Current Muscularity and fat amount with neutral distribution, no new biology. |
| C8 | Sex dimorphism magnitude in composition (Durrim, Grask, Gorrund, Pipkin, Cogling) | **D** | OPEN biology (UCCA L355); R-SEX lets "no shift" stand meanwhile (PR L94). |
| C9 | Sex shift for silent races (Marchfolk, Skarn, Sagekin, elves) | **A** (suggestion) | R-SEX makes "no shift" a valid complete state (PR L94); an author can confirm it now. |
| C10 | Saurin E/B statistical spreads; reproductive link of B | **D** | OPEN in SAURIN L4244, L4273. |
| C11 | Regional muscle binding per race (e.g. Pipkin neck, Cogling groups) | **E** | UCCA binds "only the groups its canon names" (UCCA L158); a slot-binding pass, not new biology. |
| C12 | How composition operations' race-specific values are set (Lean/Athletic/…) | **E** | UCCA L167 says values are "race-specific" and supplied by each race; that is a system/preset task. |
| C13 | Visible mass / circumference as DER | **E** | UCCA L154 "Soft-tissue fullness, circumference and visible mass are DER"; Durrim/Marchfolk defer mass calculation (DURRIM L54; MARCHFOLK L31). |

> UCCA Phase 1 evidence appendix to `reviews/claude-ucca-01-requirements-matrix.md`. Line references are to the canonical race spec (or the named source) as of commit 89ca8f7. Extraction only: no canon is changed and nothing here is new biology. Tags: [ANAT] anatomical requirement · [DIR] direct control · [DER] derived/coupled · [SOFT] tendency · [VAL] validator · [LAT] latent/preset · [PRES] presentation · [DIAG] diagnostic · [OPEN] open/not authorized.

# Prototype gaps and creator-flow sources (UCCA input)

Classification key: **CANON** = authority levels 1–3 (race specs; PROJECT_RULES + UFCA; accepted reviews/author resolutions). **REG-4** = decision register (supporting history, level 4; "historical until reconciled", register L3). **PROTO-6** = prototype/implementation material (level 6). Authority hierarchy: PROJECT_RULES L50–58 (level 6 = "Prototype / implementation material (including `rules/character-creation-brief.md` where it conflicts with canon)" L56).

Note: plan/terrain-and-race-models.md is a planning doc; its CURRENT IMPLEMENTATION statements describe the prototype (PROTO-6), its TARGET DESIGN / authority statements restate canon, and its CANDIDATE TECHNICAL APPROACH rows are non-approved (PROTO-6 / non-authoritative). Plan labels: L61–68.

## 1. decisions/PROJECT_RULES.md — character-creation rules (CANON, level 2)

- L4 "Canonical shared rules for Wayfarer first-pass character design."
- L7 Race defines biological foundation; customization creates individual; presentation creates identity.
- L8 Simple Mode: Race -> Preset -> Confirm. L9 Advanced Mode: Race -> Preset -> Customize -> Confirm.
- L10 Presets are valid outputs of the same system as custom characters and NPCs.
- L11 Race-aware and selective randomization are required.
- L12 Biological Anatomy / Skeletal Frame / Physical Composition / Personal Presentation conceptually separate.
- L13 Narrow/Balanced/Broad frame presets are editable starts, not castes.
- L14 Current Muscularity, Body-Fat Amount, Body-Fat Distribution separate.
- L15 Culture, occupation, personality, class, presentation not biological.
- L16 Chronological Age, Apparent Biological Age, Age Presentation distinct.
- L17 Combined-proportion validity mandatory; individually valid controls may form invalid combinations.
- L18 Population correlations use weighted distributions/conditional probabilities/validity envelopes rather than hard creator dependencies.
- L19 Populations may overlap in surface phenotype without becoming anatomically interchangeable.
- L20 Biological appearance distinct from observed lighting/environmental appearance.
- L21 Anatomical Resting Alignment distinct from Cultural/Personal Body Language.
- Technical authority L24–29: design determines architecture (L24); world compatibility vs approved target anatomy, not prototype-reachable (L25); canonical equipment doesn't scale with holder (L26); visual anatomy / equipment / collision / interaction reach / combat reach / camera-targeting reach not one system (L27); retargeting/IK adapt to anatomy (L28); **L29 "Current prototype race scales, uniform whole-body scaling, shared-human-animation assumptions, class restrictions, and racial stats remain non-authoritative unless explicitly approved."**
- UFCA universal rules relevant to whole creator flow: no master sliders (L36); diagnostics never sliders, latent generation variables never player-facing (L37); **combined validity PASS / CONSTRAIN / FAIL, CONSTRAIN reported and biologically deterministic, locks absolute, no silent reset (L38)**; randomization strengths Subtle/Diverse/Extreme all valid, Extreme samples valid tails; frequency vocabulary Very Common/Common/Uncommon/Rare describes weighting, never validity (L40); natural asymmetry vs acquired history; Naturalize Face provisional (L41).
- Terminology: Simple/Advanced are the modes; "Basic" not a synonym (L65); Narrow/Balanced/Broad reserved for Skeletal Frame; Frame Preset = editable start (L66); MDC vs Current Muscularity (L67); Skin Appearance Layers Natural/Environmental/Applied/Acquired, dirt = Environmental (L68).
- R-SEX L73–79: hard bounds available to either sex unless canon says otherwise (L74); overlap mandatory (L75); sex never a body preset/package (L76); per-race soft distributions allowed, "no shift" valid (L77); reproductive biology never inferred from creator architecture (L78); Saurin §263 not generalized (L79).
- Saved appearance: **SILENT in PROJECT_RULES** (no saved-appearance rule; covered by Marchfolk v1.5 L261 canon and register).

## 2. plan/terrain-and-race-models.md (read fully, 157 lines)

| Item | Lines | Class |
| --- | --- | --- |
| Terrain, art sources, playtest feedback | L7–31, L151–157 | out of scope |
| Race-model table: heights per spec (Marchfolk 147–173–203; Skarn 183–208–229; Sagekin 152–178–208) + **candidate** foundations (MetaHuman etc., "not approved") | L33–53 | heights restate CANON; foundations = CANDIDATE (PROTO-6/non-authoritative). Note: Marchfolk status "v1.1–v1.4 received (v1.0 and v1.5 not yet)" L39 is stale (spec now v1.5 complete). Other races listed with brief multipliers (stale; brief superseded) |
| Architecture principle; authority rule "Approved Design Specification > Open Decision Register > Prototype Implementation. Existing implementation never overrides an approved spec and never resolves an OPEN item by existing" | L57–59 | CANON restatement (now refined by PROJECT_RULES 6-level hierarchy) |
| **CURRENT IMPLEMENTATION (placeholder): "All races use the same human mannequin and the same human animation set, with uniform whole-actor scaling per race and per height step… not the approved final animation or body architecture for any race"** | L70 | PROTO-6 |
| TARGET DESIGN: per-race validation for locomotion, animation, IK, interactions, combat, equipment, climbing/swimming/mounts | L72 | CANON-aligned target |
| No premature refactor; shared human animation stays | L74 | PROTO-6 status/decision (register L42 AGREED) |
| Known gaps table (pre-Aelari audit, complete Sep 30 2026); "Nothing here authorizes changes" | L76–94 | see §3 below |
| Candidate engine approaches (Mutable; per-race skeleton/base body; "a few high-level controls drive many body-shape morphs"; Age "one value that drives… a small change to movement speed and stride"; "One compact appearance record (race plus slider values)… The game already has a small version of this") | L96–112 | CANDIDATE, PROTO-6. Tensions with canon: age→movement speed conflicts with cosmetic-age no gameplay penalty (Marchfolk L212); "high-level controls" vs no master sliders (PROJECT_RULES L36); "race plus slider values" record vs Halvren §32–33 (final slider values alone may not suffice) |
| "What each race design should pin down" checklist (height for males and females; build slim/average/stocky/massive; posture) | L114–127 | superseded (L116) — historical |
| Order of work: creator plumbing (each race loads own body, mannequin stand-in) "On hold until the specs are agreed"; Marchfolk technical prototype; MetaHuman leading candidate not approved | L129–135 | PROTO-6 plan |
| Open questions (first-person, race/class limits, culture, size in combat) | L137–142 | historical/OPEN pointers |

## 3. Known prototype gaps (plan L80–92) — all PROTO-6 (classification column is plan's own)

| # | Current implementation | Plan classification | Lines |
| --- | --- | --- | --- |
| 1 | **"Frame" switches between Manny and Quinn mannequins**; target: four layers, "Narrow, Balanced and Broad never simply mean Manny or Quinn" | CURRENT PLACEHOLDER, incompatible with target | L82 |
| 2 | **Saved appearance holds only frame, height step, two colors and finish**; target: unified appearance architecture with schema/version tracking + migration; "Serialization isn't redesigned yet" | CURRENT PLACEHOLDER, requires future expansion | L83 |
| 3 | Personal height ±7.5% (about 160–186 cm for Marchfolk) | CURRENT PLACEHOLDER, superseded by race specs | L84 |
| 4 | **Height and race size are uniform whole-body scaling** | CURRENT PLACEHOLDER, incompatible with target anatomy | L85 |
| 5 | **Race scale values (e.g. Fenn 0.95×, Cogling 0.72×, Gorrund 1.22×)** | CURRENT IMPLEMENTATION ONLY, not authoritative design data | L86 |
| 6 | One actor scale drives weapons, capsule, camera, reach | MAJOR FUTURE ARCHITECTURE REQUIREMENT; size-gameplay OPEN BALANCE DECISION | L87 |
| 7 | Racial attribute bonuses (Sagekin Int 107, Skarn Str 103) | OPEN GAMEPLAY DESIGN DECISION | L88 |
| 8 | Race/class restrictions built in | IMPLEMENTATION EXISTS, final design OPEN | L89 |
| 9 | Race descriptions present culture as biology (Sagekin "soft hands", Skarn "trust muscle over books") | DESIGN TEXT REQUIRES FUTURE REVISION | L90 |
| 10 | **All races share human animations at uniform scale** | ACCEPTED CURRENT PLACEHOLDER | L91 |
| 11 | Skarn 1.5× breath, Fenn sneak/swim bonuses | EXISTING IMPLEMENTATION FACT, aligned with design | L92 |
Future work (none authorized): Race → Biology → Gameplay Attributes Review, versioned appearance data with migration, race-description rewrite — L94.

## 4. audits/ — what they record about the prototype (PROTO-6 facts; audits are level-5 diagnostics)

**Manny/Quinn frame placeholder**
- audits/01-marchfolk.audit.md L24: game "uses Manny and Quinn as 'broad' and 'slender' frames, which mixes sex-related anatomy with frame"; ruled out by v1.0 §4, §6, §13; known gap, unchanged.
- audits/05-aelari.audit.md L13: Manny/Quinn switch "changes the whole body type, not just skeletal breadth" (sharpens gap 1).
- audits/07-halvren.audit.md L7: Halvren drawn with shared Manny and Quinn mannequin at 1.0 scale.

**Uniform height scaling / personal height**
- 01 L24: "The game sets height by uniform scale (1.0 × a ±7.5% slider)".
- 02-skarn L58: each race drawn by uniformly scaling the one mannequin (Skarn 1.12×); "held weapons scale with the body"; ruled out by Skarn v1.5.
- 02 L59: capsule, camera height, melee reach follow uniform scale.
- elf-comparative-review.audit.md L17: Aelari scale 1.02 with ±7.5% slider, "well short of a 221 cm target".
- pipkin-part-2.md L152: uniform scaling of human mannequin "is by definition the 'scaled human' the spec forbids" (plan gap #4); pipkin-part-2-reaudit L130.

**Race scaling (prototype values, all non-authoritative)**
- Skarn 1.12× vs 1.20× reference — 02 L46. Sagekin 1.0× vs ~1.03× (178 cm) — 03 L72. Halvren 1.0 (~173 cm) vs 178 cm — 07 L13. Fenn 0.95× (opposite direction to spec 1.05×) — 04 L9. Aelari 1.02× — 05 L8. Vael 0.95× — 06 L12, L23. Durrim 0.82× (~142 cm) — 08 L7. Pipkin ~0.7× (~121 cm, at Pipkin max/Durrim boundary vs 107 cm reference) — pipkin-part-2 L151, pipkin-part-5 L129. Cogling ~0.72× (~125 cm, reverses Pipkin/Cogling order) — cogling-part-1 L129–134. Grask/Gorrund prototype values not re-read — 09 L15, 10 L14, L42.

**Current appearance record / saved-appearance contents and gaps**
- Contents: frame, height (step), primary and accent colors, finish — 06-vael L20 ("frame, height, primary and accent colors, finish"); 07-halvren L7 ("frame, height, two colors and finish, with no genealogy, expression or ancestry data"); plan L83.
- Gaps recorded: no population distributions, locks or strength levels — 06 L20; no genealogy/expression/ancestry data — 07 L7; needs separate chronological-age value not set by age-appearance slider — 01 L21; natural hair color and age-graying as two values — 05 L16; markings stored as few numbers for multiplayer size — 01 L17; mixed ancestry suggests race ranges/frequencies looked up from race, not baked into saved values — 03 L74; one race per character today — 03 L74; no skin-tone options yet — 03 L68.
- Creator-flow notes: "General physique adjustments" undefined — 01 L10; two preset kinds need flow decision (body preset + look preset) — 02 L52; brief §13 randomize list vs Skarn v1.4 list should be merged — 02 L55; preset counts differ (6 vs 8) — 02 L56; weight-as-slider (brief) vs derived — 02 L50.

**Shared animation placeholder**
- 04-fenn L26: "Every race currently plays the same retargeted human clips at uniform scale"; labelled CURRENT IMPLEMENTATION Sep 30.
- pipkin-part-5 L128 (plan gap #10); cogling-part-6-final L118 and quick-check L25 (shared human animation, holder-scaled weapons, single human-based capsule recorded as non-authoritative); saurin-part-1-reaudit L41, saurin-part-5 L24/L45.

**Other prototype text**: culture-as-biology race descriptions — 01 L37 (Halvren), 02 L47, L53, 03 L67, 08 L9, L26; class limits (Skarn: Vanguard, Veilrunner, Spiritcaller) — 02 L48.

## 5. rules/character-creation-brief.md (PROTO-6 where it conflicts; banner L3 SUPERSEDED — HISTORICAL)

Banner L3: "does not govern anatomy, terminology, creator modes, layers, height/mass values or gameplay"; approved sources govern on conflict. Creator-flow items only:
- L37 one framework: presets, randomized, player, saved appearances, NPCs — consistent with canon (Marchfolk L261; PROJECT_RULES L10).
- L38–41 presets illustrative (Marchfolk: Frontier, Noble, Laborer, Wanderer, Scholar, Soldier) — superseded by spec preset lists (Marchfolk L216–223; audit 01 L19).
- L42 modes Simple/Advanced — matches canon.
- L43 Randomize options: Everything, Face, Body, Hair, Appearance, Clothing, Scars and Tattoos; locks; within race limits — historical; superseded/extended by spec lists (Skarn L280, Sagekin L402) and PROJECT_RULES L11, L38.
- L44 Saving: save, load, duplicate, modify; import/sharing later — historical requirement; no canonical counterpart for duplicate/import/sharing (canon covers schema/version/migration only).
- L45 compatibility list incl. "first- and third-person views" — historical; first-person OPEN.
- L27–33 three-layer model (Race / Individual / Presentation; Individual lists "weight") — SUPERSEDED (four layers; weight derived).
- L49–65 height/mass multipliers ("baseline") — SUPERSEDED (race specs).
- L129–145 Universal amendment v0.1 (four layers; Data: "four layers are distinct parameter groups in the one unified appearance record" L143; Creator: "Simple mode picks a complete curated preset. Advanced mode exposes the four layers separately. Switching modes keeps the appearance" L144) — content consistent with canon and adopted (Marchfolk L5), but this file's copy is level 6.
- L147–153 contradictions w/ earlier plan: creator plumbing on hold (L153); race scales 0.7×–1.22× (L149).
- L157–162 open: sex and body type, first-person, race/class limits, culture, size in gameplay, mounts.

## 6. register/decision-register.md — creator-flow items (REG-4; historical, entries stop Sep 30, L3)

Line-reference correction: the requested refs R:93 / R:190 / R:444 do not land exactly on those items in the current file; actual lines below.
- **Selective randomization** — L96 "Universal (proposed): selective randomization with parameter and group locks | PRELIMINARY | Skarn v1.4 §3" (L93 = Skarn silhouette/equal-height/anti-stereotype tests; L92 relationship-aware randomization AGREED; L95 strengths PRELIMINARY). Later: L356 Vael strengths + lockable groups PRELIMINARY; L995 Pipkin "race-aware and selective randomization with locks… saved appearance via the unified architecture with schema migration" AGREED. Now CANON via PROJECT_RULES L11, L38.
- **Combined validity** — L193 "Universal (proposed): combined-proportion validation, where legal parameters can form an illegal combination | PRELIMINARY | Fenn v1.1 §11" (L190 = Fenn joint minimum boundaries). L447 "Individually valid controls can still make an invalid body… | AGREED | Marchfolk v1.0 §9–11" (L444 is the table divider; L446 Marchfolk height AGREED). L573 Durrim combined-proportion mandatory AGREED. Now CANON via PROJECT_RULES L17, L38 (PASS/CONSTRAIN/FAIL).
- **Saved appearance / appearance record** — L13 unified framework incl. saved appearances AGREED; L15 Simple/Advanced share data, switching keeps appearance AGREED; L49 "Future appearance data supports schema and version tracking with migration" AGREED (audit gap 2); L456 "One unified conceptual appearance record… schema and version tracking and migration. Presets must survive Preset, Advanced, Edit, Save, Reload unchanged" AGREED (Marchfolk v1.5); L170 deterministic reproducible generation PRELIMINARY (Sagekin v1.5 §7); L357 deterministic generation required for co-op PRELIMINARY (Vael); L370 networked appearance sync OPEN; L995 Pipkin saved appearance AGREED. Halvren save data schema OPEN (HALVREN_V1 L68–70: "storing final slider values alone may not preserve future inheritance features").
- Prototype-status entries: L42 shared human animation + uniform scaling = prototype placeholder AGREED; L47 authority rule AGREED; L102 uniform mesh scaling not assumed, weapons true size AGREED; L436 world validated vs approved anatomy AGREED; L437 Aelari height authoritative over prototype (1.02, ±7.5%) AGREED.
- Stale register item: L21 "Skin has three independent layers" — superseded by four Skin Appearance Layers (PROJECT_RULES L68; Marchfolk L157–162, L287).

## 7. Prototype vs canon summary

| Topic | Prototype (PROTO-6) | Canon |
| --- | --- | --- |
| Frame | Manny/Quinn swap (plan L82; audit 01 L24) | Skeletal Frame continuous; N/B/B editable presets; frame ≠ sex (PROJECT_RULES L13, L66, L76; Marchfolk L27, L285) |
| Height | uniform scale ×(1 ± 7.5%), height steps (plan L84–85) | per-race envelopes, anatomical proportions, never uniform scaling (Marchfolk L23; Skarn L40) |
| Race size | scales 0.7–1.22× (plan L86; audits) | race spec heights; scales non-authoritative (PROJECT_RULES L29) |
| Saved appearance | frame, height step, two colors, finish (plan L83; audits 06 L20, 07 L7) | one unified record, four layer groups, schema/version/migration, deterministic interpretation, implementation OPEN (Marchfolk L261; register L456) |
| Animation | shared human set at uniform scale (plan L70, L91) | per-race validation; architecture OPEN (plan L72; PROJECT_RULES L28–29; Skarn L342) |
| Equipment/capsule/camera/reach | one actor scale (plan L87) | separated systems; equipment true size (PROJECT_RULES L26–27) |
| Randomization/locks | none in record (audit 06 L20) | race-aware + selective, locks absolute, PASS/CONSTRAIN/FAIL (PROJECT_RULES L11, L38, L40) |

# Pass 2 — 01. Roster-Wide Comparative Anatomy Report

**Author:** Claude (auditor)
**Responds to:** `reviews/chatgpt-pass2-roster-wide-comparative-system-review-order.md` (b5c9f48)
**Phase:** design only. This is a document audit of the 13 canonical specs, `decisions/PROJECT_RULES.md`, `specs/STATUS.md` and the accepted elf and short-race reviews. No canonical spec was edited.
**Covers order tracks A–F.** The finding IDs (F-xx, I-xx) are defined in `claude-pass2-06-findings.md`.

**Method.** I read each spec in full and extracted per-race digests with section citations. The digests are kept as working notes, not canon.

Section-citation conventions follow each spec's own structure:
- Saurin and Cogling use flat §N.
- Durrim, Grask, Gorrund and Pipkin restart numbering per Part, so they are cited as "P2 §x" and line number "Lnn".
- Marchfolk, Skarn, Sagekin, Fenn, Aelari and Vael are cited by version ("v1.1 §N").
- Halvren is cited by Part plus the consistency review / resolution ("CRev", "CRes").

No renders were made. Only Saurin has a frozen reference mesh; the other races have no meshes to compare. Equal-height comparisons are therefore audited as canonical validation requirements: whether each one exists, which race carries it, and which dimensions it relies on.

---

## A. Stature and whole-body proportional space

### A1. Standing-height envelopes (cm)

These are as stated in each spec. All are provisional first-pass ranges unless noted.

| Race | Min | Ref | Max | Source | Notes |
|---|---|---|---|---|---|
| Cogling | ~76 | ~91 | ~107 | §4 | Smallest. Prototype scales 0.45× / 0.72× are non-authoritative |
| Pipkin | ~91 | ~107 | ~122 | P1 §5–11 | Final range OPEN (P6 §32) |
| Durrim | ~122 | ~137 | ~152 | P1 §4–10 | — |
| Marchfolk | ~147 | ~173 | ~203 | v1.0 §4–5; Part 1 §6 | **Human Reference Population** and **Reference Height** |
| Sagekin | 152 | 178 | 208 | v1.0 §2 | "never the main racial marker" |
| Halvren | ~152 | ~178 | ~213 | P2 §3–6; CRes §10–14 | **Central** envelope; ancestry-dependent tails allowed above and below |
| Vael | 157 | 178 | 203 | v1.0 §3 | Prototype 0.95 scale non-authoritative |
| Fenn | 157 | 181 | 211 | v1.0 §2 | — |
| Aelari | 168 | 190 | 221 | v1.0 §3 | — |
| Saurin | 168 | 188 | 208 | §4, §227, §258 | Excludes the tail. Racial hard bound; independent of all other controls |
| Skarn | 183 | 208 | 229 | v1.0 §2 | 183–203 overlap with Marchfolk is intentional |
| Grask | ~198 | ~218 | ~239 | P1 §3–5 | — |
| Gorrund | ~208 | ~229 | ~251 | P1 §6–10 | "current world-validation upper stature, never a permanent maximum" |

**Roster envelope:** about 76–251 cm, a 3.3× span.

**Cross-spec agreement:** every stature figure quoted in another spec matches its source:
- Halvren's source table (P2 §3–6);
- Grask's overlap table (P1C §1–9);
- the short-race review §3;
- the Pipkin, Durrim and Cogling cross-references.

No numeric stature contradiction exists anywhere in the roster (I-01).

**Stale ceiling and roster wording:**
- Grask still describes 239 cm as the "currently … tallest approved playable stature" (P1C L178, P5 L671). Gorrund's 251 cm supersedes it. Both Grask passages already hedge "not a permanent project maximum" (F-11).
- Pipkin P1 §95–115 calls the 76–251 cm roster envelope provisional "because Saurin is still undesigned". Saurin's 168–208 cm sits inside it, so the envelope is confirmed (F-11).

**Every spec forbids uniform whole-body scaling.** Height is always generated through coordinated proportional relationships.

### A2. Stature-overlap bands that matter

| Band | Populations sharing it | Overlap risk |
|---|---|---|
| ~91–107 | Cogling / Pipkin | **High** (deliberate). The canon says height is not the discriminator |
| ~122 | Pipkin max = Durrim min | Boundary touch (SR-COMP-03) |
| ~147–152 | Durrim upper / Marchfolk lower / Sagekin min (152) | Durrim–Marchfolk–Sagekin equal-height test at ~152 cm |
| ~152–203 | All human populations, three elves, Halvren, Saurin (168+) | **Densest band**: 8 populations overlap at 168–203 |
| ~183–229 | Skarn with Marchfolk (to 203), Sagekin (208), Fenn (211), Aelari (221), Saurin (208), Halvren tails | Size-based Skarn identity at its low end |
| ~198–239 | Grask with Marchfolk, Sagekin, Fenn, Vael, Aelari, Skarn | Grask boundary set (Grask P1C) |
| ~208–239 | Gorrund with Skarn (to 229), Grask, Aelari (to 221), Fenn (211), Sagekin (208) | **Skarn–Gorrund** and **Grask–Gorrund** (F-01) |

### A3. Proportional specializations

| Race | Positive body specialization (canonical wording) | Trunk | Limbs | Robusticity / skeletal mass |
|---|---|---|---|---|
| Marchfolk | Breadth of human diversity; **Human Reference Population** (v1.0 §1–3) | Reference | Reference | Reference |
| Skarn | "larger, heavier, more powerfully built … than Marchfolk"; skeletal trends (v1.0 §1, §3; v1.1 §1) | "slightly more torso-dominant than Marchfolk"; wider and deeper ribcage | "more substantial limbs and larger joints"; not universally short-legged | "greater skeletal robustness", heavier/larger joints |
| Sagekin | "geographically distinct human population"; subtle tendencies (v1.0 §1, §3; v1.1 §1) | "slightly shorter torso relative to stature", slightly less ribcage depth | slightly greater leg share; longer forearms, hands and fingers | Not stated |
| Fenn | Non-human gracile elven skeleton; extremity-emphasized (term from Aelari, Vael and the elf review) (v1.0 §3) | Slightly smaller torso share; shallow ribcage | Greater limb share, forearm and lower-leg share, long hands and feet | Greatest gracility of the elves |
| Aelari | **Whole-body vertical elongation** (v1.0 §4) | Longer torso and waist transition than Fenn | Evenly elongated arms and legs | Gracile; more presence than Fenn (elf review) |
| Vael | **Compact structural continuity, deeper torso**, more joint and extremity-base presence (v1.0 §4; v1.1 §1) | Greater torso share than Fenn; deepest ribcage of the elves (skeletal, v1.1 §2) | Less elongation than Fenn or Aelari | Most structural presence of the elves |
| Halvren | Mixed human/elven validity envelope; "neither an averaged human and elf body nor a collection of … race parts" (P2 §1) | Relationship-aware inheritance | Coupled segments | Gracile ↔ relatively robust (P2 §7–8) |
| Durrim | **Compact structural power and high skeletal presence relative to stature** (P1 §40–43) | Greater torso contribution and thoracic depth/breadth than equal-height Marchfolk | Lower limb contribution, especially legs | High structural presence; substantial joints; large hands and feet |
| Grask | **Elongated skeletal leverage and reach** (P1 §6–7; P2 §1–3) | Lower torso contribution to stature than Marchfolk and Skarn | Greater limb, arm-span, forearm and lower-leg contribution | Rangy, not fragile |
| Gorrund | **Massive load-bearing non-human architecture**; **Axial Load-Path Continuity** (P1 §1–5; FC L703) | Greater proportional torso contribution than Grask; deep thorax | Less limb contribution than Grask (defined only against Grask) | High absolute structural scale; very large joints |
| Pipkin | **Low-Set Compact Trunk Architecture** (P2 §1–6; P6 §30) | Modestly reduced central-trunk share vs Marchfolk; mature, structurally participating pelvis | Proportionally sustained | Light relative to Durrim |
| Cogling | **Fine-Scale Elongated Articulation** (§3) | Near the Marchfolk range; narrow stable core | Near-Marchfolk totals with distal redistribution; emphasized hands and fingers | Fine shafts and joints, lower than Marchfolk |
| Saurin | **Counterbalanced Pelvic-Axial Architecture** (§3, §223) | Elongated lower axial trunk; deep thoracic shell (d/w 0.80–1.00) | Moderate-to-long legs, plantigrade; forearm emphasis | Moderate-to-substantial (§20) |

**Centre of mass** is stated directionally only for:
- Durrim: lower than "taller humanoids" (P1 L34; reference population unnamed, F-05);
- Pipkin: low absolute centre of mass, no bonus (P1 §50–58; P5 §3);
- Vael: "lower … than Aelari" (v1.1 §20–23; not carried into the elf review, F-20);
- Saurin: a measured 8.8° lean need under the uniform-density model (§257).

Every spec forbids converting centre of mass into a gameplay bonus.

**Mandatory structures affecting silhouette and world space:**
- **Saurin:** the tail, which is mandatory (§10, §225). Its envelope is 55–80 % H, it reaches up to ~170 cm behind the heel (§265), and it can be partially covered but never concealed for validation (§195). The cranial display family has a crest ceiling of ~2.5 cm (§260).
- **Elves and Halvren:** external ears, which are an equipment problem (Fenn v1.5 §11; Aelari v1.5 §10–12; Vael v1.5 §11–14).
- **Grask and Gorrund:** ears and head clearance at the upper statures.
- **Everyone else:** stature only.

### A4. Equal-height comparison coverage

The order requires equal-height testing wherever overlapping populations could converge. Each canonical test is listed by the spec that carries it.

| Overlap | Canonical equal-height test | Carried by | Status |
|---|---|---|---|
| Marchfolk–Skarn (190 cm) | v1.4 §6 | Skarn | Exists; marked "future" |
| Marchfolk–Sagekin (178 cm) | v1.0 §10; SG-10 (ambiguity accepted) | Sagekin | Exists |
| Durrim–Marchfolk–Sagekin (152 cm) | Cross-Population Equal-Height Boundary Test | Durrim P2 §54–63 | Exists |
| Cogling–Pipkin (~91, ~107) | SR-COMP-01/02 | Short-race review | Exists (qualitative only, F-06) |
| Pipkin–Durrim (~122) | SR-COMP-03 | Short-race review | Exists |
| Fenn/Aelari/Vael (three elves) | Vael v1.0 §17–18; Aelari v1.1 §15–17 (~190) | Elves; elf review | Exists |
| Elves–Marchfolk/Sagekin | Fenn v1.0 §13; Vael VL-13/21; Aelari AE-21 | Elves | Exists |
| Sagekin–Fenn/Aelari | Sagekin v1.5 §9 "reserved … once the elves are defined" | Sagekin | Elf-side tests exist (FN-17, AE-21). **The Sagekin-side test is still marked reserved** (F-19) |
| Skarn–Grask | Grask P1 §60–70 | Grask | Exists (no counterpart in Skarn) |
| Skarn–Gorrund (208–229) | Gorrund P2 L237 "fails as 'extra-broad Skarn'" | Gorrund | Exists. **Distinction unquantified** (F-01) |
| Grask–Gorrund (208–239) | Gorrund P2 L236 (218–229), P1 L110, P5 L672 (208–239) | Gorrund | Exists; band wording varies (F-11) |
| Grask vs Aelari, Fenn, Vael, Marchfolk, Sagekin | Grask P1C, P5 L701–708 | Grask | Exists |
| Gorrund vs Aelari, Fenn, Sagekin | Gorrund P2C L262–267 | Gorrund | Exists |
| Saurin vs Marchfolk, Skarn, Aelari, Vael | SAU-BODY-03/11/21/22/12 | Saurin | Exists |
| **Saurin vs Sagekin, Halvren** | none | — | **Missing** (F-25). Low risk: tail and rostrum carry the read |
| Halvren vs its six sources | HV-09, HV-13…HV-17; source-passing test | Halvren | Exists |

---

## B. Positive skeletal identity and survival under neutralization

| Race | Strongest positive carriers | Neutralization tests stated in canon | Primary-identity risk |
|---|---|---|---|
| Marchfolk | Human skeleton as reference; breadth (v1.0 §1–3) | Not applicable as a distinguishing test | None. It is the reference by design, and the spec says "This doesn't make Marchfolk the default anatomy for every humanoid race" |
| Skarn | Clavicles, ribcage depth and width, upper back, neck base, pelvis, joints, hands and feet (v1.0 §3; v1.1 §1) | Silhouette with hair, beard, markings and clothing removed (v1.4 §5); equal height at 190 cm (v1.4 §6); lean, elderly, narrow and high-fat bodies (v1.0 §1) | **Size and Marchfolk-relative magnitude only**, with no numbers. "more natural muscle volume" is a composition trait listed as identity (F-04) |
| Sagekin | Limb-to-torso proportions, forearm/hand/finger length, ribcage depth, face length and forehead (v1.1 §1; v1.2) | Culture removed (FD §9; v1.4 §9); large-sample statistical test (v1.4 §7) | **Individual identity intentionally weak**: "individual pairs don't have to be unmistakably different" (v1.0 §10). Surface distributions are listed among the differentiators (FD §3) (I-02, F-19) |
| Fenn | Limb-to-torso ratio, long bones, joint scale, hands and feet, pelvis–leg relations (v1.0 §1; v1.1 §12) | Ears hidden (v1.0 §13); hair neutralized; presentation neutralized (v1.4 §7–9) | Low. The spec has no pigmentation-neutralization test of its own (the elf review adds one) |
| Aelari | Torso share, neck, clavicles, ribcage, even limb elongation (v1.0 §15) | Ears, hair and culture removed (v1.2 §15–16; v1.4 §17, §21–22) | Height-adjacent specialization, but explicitly "never comes down to height alone" (v1.1 §1). Defined mostly "than Fenn" |
| Vael | Skeletal thoracic depth, compact continuity, joint and extremity-base presence (v1.1 §2, §15–18) | **Strict** hidden-ear plus neutral-complexion test (v1.2 §28); Surface-Raised preset; cliché-convergence tests (v1.4) | Surface risk acknowledged and guarded; the strongest neutralization coverage of the elves |
| Halvren | Distributed soft-inheritance clusters (P1 §13) | Ears hidden, pigmentation neutralized, culture removed (P1 §30–31; P3–P5) | Collapse into a source population **accepted by design** for individuals, guarded at system level (I-02) |
| Durrim | Torso architecture, structural presence, joints, hands, head–neck integration (P5 §82–83; C1) | Bald, clean-shaven, ears hidden; skin and eye neutralization; low-muscle permanent test (P2 §41–49) | Low. It explicitly rejects "merely the opposite of elven gracility" |
| Grask | Limb and arm-span contribution, forearm and lower leg, long integrated midface, folded late-taper ear (P1C; P2; P3; P3C) | Head-neutralized body; silhouette; facial hair "zero"; pigmentation never required (P4C L582) | Identity rests on unquantified Marchfolk/Skarn-relative ratios. The short-limbed floor "enough limb contribution to read Grask" is undefined (GR-BODY-10) (F-06) |
| Gorrund | Thoracic depth, joints, axial load-path continuity; Transverse Structural Continuity face; deep-bowl ear (P1; P2; FC; P3C) | Low muscle and low fat: "the skeleton alone carries the race" (GRR-BODY-16); brown-skin and light/dark skin tests | Carriers are partly **absolute-scale** ("high absolute structural scale", "overall skeletal scale"). Versus Skarn, the distinction is unquantified (F-01) |
| Pipkin | **Primary:** Low-Set Compact Trunk. **Supporting:** light skeleton, sustained limbs, Integrated Mature Facial Architecture (P6 §30) | Head, hands and feet obscured; scale reference removed (P2 §1–6); surface swap; culture removal | Primary carrier has no metric (F-06). Child firewall is extensive and adequate |
| Cogling | Narrow core, distal redistribution within near-Marchfolk limb totals, fine shafts and joints, hands and fingers; Fine-Scale Planar Integration face (§3, §75) | Neutral gray with hair, clothing, tools and goggles removed (§3, §25); toddler tests | Distal emphasis is shared in part with Sagekin, Grask, Fenn and Pipkin; the distinction is a conjunction of traits with no numbers (F-06) |
| Saurin | Pelvic-axial architecture with mandatory tail; Layered Rostral-Cranial Integration; recessed auricular openings; gait signature (§3, §36, §56, §173) | Surface neutralized (§65); tail never removed for validation (§1, §225, Tyler decision); displays never required (§100) | None. Pupil and nictitating membrane are surface identity phenotypes, but the skull carries the head read |

**Answer to the order's identity question:** no race's *canonical* identity depends primarily on height, attractiveness, culture, equipment, animation or surface phenotype. Each spec names positive anatomical carriers and rejects stereotypes explicitly. The live risks are structural, not stereotype-based:
- Skarn and Gorrund rely on unquantified magnitude (F-01, F-06).
- Grask, Pipkin and Cogling rely on unquantified ratios (F-06).
- Sagekin and Halvren rely on population-level statistics. This is by design and accepted (I-02).

---

## C. Frame, composition and anatomy separation

PROJECT_RULES fixes the four layers. Specs that define them in their own text:
- Marchfolk (Part 1 §7);
- Saurin (§137);
- Halvren, partly (P1 §19–22; P2 §27–31).

All other specs invoke the layers by reference or not at all. That is acceptable because PROJECT_RULES governs. The checks:

| Check | Result | Exceptions |
|---|---|---|
| Narrow/Balanced/Broad are race-specific skeletal frames, not uniform scaling | **Holds in all 13** | Fenn never states what its frame changes skeletally (v1.0 §4). PROJECT_RULES governs |
| Frame ≠ muscularity | Holds | Fenn v1.0 §8, Aelari v1.0 §12 and Vael v1.0 §13 list "Broad" among composition examples (wording only, F-16) |
| Muscularity ≠ fat | Holds | — |
| Fat amount ≠ fat distribution | Holds where stated | Skarn, Sagekin, Fenn, Aelari and Vael never separate them (F-16). PROJECT_RULES governs. The `rules/character-creation-brief.md` amendment layer C also omits Body-Fat Amount (F-10) |
| Sex tendencies do not silently become frame or composition | Holds | Saurin §263 E/B are Biological Anatomy, explicitly not fat. No other race defines sex tendencies |
| No biology leaking into Presentation | Holds | Hair biology vs hairstyle is explicit in Sagekin, Aelari, Vael, Halvren and Saurin; implicit in Marchfolk and Skarn |
| No composition inside skeletal identity | **Two exceptions** | Skarn "more natural muscle volume" in the skeletal foundation (v1.0 §3; v1.1 §1) (**F-04**). Grask "relatively lean structural silhouette" (P1 L9) (F-16) |
| No race forced into one build | **Holds in all 13** | — |

**Muscular Development Capacity vs Current Muscularity** is distinguished by Grask, Gorrund, Pipkin, Cogling, Saurin, Halvren (CRes §1) and the register (R:542). It is absent from PROJECT_RULES (F-24).

Halvren CRes §1 interprets the Skarn muscle trait as capacity, and Gorrund P2 L237 repeats "greater natural muscle-volume potential". That interpretation is the newest canonical text, but the Skarn spec itself was never conformed (F-04).

---

## D. Sex-related anatomy consistency

| Race | What canon states | Hard sex envelopes? | Overlap rule | Reproductive biology |
|---|---|---|---|---|
| Marchfolk | Biological Anatomy includes "relevant sex-related characteristics"; "no hard sex-specific height restriction … individual overlap stays broad" (v1.0 §4–5, §12–14) | None | Broad overlap | Fertility span OPEN (Part 2 §5–6) |
| Skarn | **Not stated** | — | — | Not stated |
| Sagekin | **Not stated** | — | — | Not stated |
| Fenn | **Not stated** (no mention of sex anywhere) | — | — | Not stated |
| Aelari | Only "anatomy configuration" (undefined); "No mandatory hip width by race or anatomy configuration" (v1.1 §2–5, §7); hair never locked to sex (v1.3 §14) | None | Not stated | Not stated |
| Vael | Frame independent of "sex-related anatomy" (v1.1 §8–9); hair never sex-locked (v1.3 §19–20); "body configuration" (v1.5) | None | Not stated | Not stated |
| Halvren | Separate from frame, height, muscle, fat, face and hair; "sex-related population distributions where later appropriate"; class-B dependency on a "sex-related anatomy system" (P1 §19–22; CRes §15–16) | None | Not stated | Out of scope (P1 §5–6) |
| Durrim | OPEN "pending the universal system"; no sex automatically broad, tall, bearded and so on (P1 §37–39) | None | Implied | OPEN |
| Grask | OPEN; dimorphism degree OPEN; "never assumed identical to humans" (P1 §46–53) | None | Not stated | OPEN |
| Gorrund | OPEN; "never … huge males and small females" (P1 §44–58) | None | "one Gorrund foundation" | OPEN |
| Pipkin | OPEN magnitude; like-for-like comparisons; may influence pelvic, thoracic, facial and soft tissue; does not determine height, frame, muscle or fat amount (P1 §59–71; P6 §29) | None | Implied | Fertility timing only |
| Cogling | May affect pelvis, thorax and soft tissue; no binary faces; magnitude OPEN (§23, §61, §93) | None | Implied | Inlet/outlet OPEN |
| Saurin | **Defined (§263):** trunk-limited, low-to-moderate, overlapping, anti-hourglass tendencies; no craniofacial shift; exclusions listed | None; identical bounds | **Mandatory** | OPEN (§263) |

**Assessment:**
- **No human-dimorphism assumption** is imported anywhere.
- **No hard sex envelope** exists anywhere.
- **No face, skull, stature, frame, muscle or fat restriction by sex** exists anywhere.

The roster is substantively consistent, and the order's instruction not to force one universal dimorphism model is respected.

**The gap is structural, not contradictory (F-03):**
- Three specs are silent: Skarn, Sagekin and Fenn.
- Two use undefined substitute terms: Aelari "anatomy configuration", Vael "body configuration".
- Halvren declares a blocking dependency on a "sex-related anatomy system" that no document defines at roster level.

What is needed is a single universal *rule*, not a universal model:
- sex is a distribution influence;
- hard bounds are identical;
- overlap is mandatory;
- per-race magnitudes stay per race;
- reproductive biology is OPEN unless a race closes it.

Saurin §263 is preserved exactly as the order requires.

---

## E. Craniofacial comparative architecture

### E1. Normalized facial organization

| Race | Named facial architecture | Vault | Facial depth / projection | Orbits | Jaw | Nose / rostrum | Ear architecture |
|---|---|---|---|---|---|---|---|
| Marchfolk | Human reference | Reference | Reference | Reference | Reference | Human nose | Human auricle (Part 2 §3–4) |
| Skarn | Human; robust tendencies (v1.2 §1) | "slightly larger, more robust" | "more substantial mid-face" | "somewhat stronger brow" | "more jaw mass" | "somewhat larger nose" | **No ear anatomy stated** (F-18) |
| Sagekin | Human; distributional (v1.2) | "slightly longer faces, somewhat higher forehead" | — | "No mandatory eye shape" | — | "no rigid racial nose types" | **No ear region** (F-18) |
| Fenn | Elven; compact face (v1.2) | Greater cranial height relative to face; narrower skull | Less lower-face mass | "open visible orbital presentation" (elf review; spec says "larger orbits", F-20) | Lighter | No mandatory type | Elven, continuous taper; Fenn tendency stated only outside its own spec (F-18) |
| Aelari | Elven; vertical | Greater cranial height | Longer forehead-to-chin line | Longer and narrower visible eyes | Relatively light | No type | Upward/backward, gradual taper |
| Vael | Elven; compact vertical, stronger midface | Moderate height | More midface presence than Aelari | Moderate to somewhat large, defined | More presence than Fenn or Aelari | Stronger nasal presence (review: E) | Broader base, lateral and backward |
| Halvren | Mixed; no interpolation value (P3 §1–4) | Mixed | Mixed | Brow, orbit, eye and ocular systems kept separate | Mechanisms kept distinct | "No half-elf nose" | Human auricular + elven variables, coupled; "Ear length isn't a genealogy meter" |
| Durrim | Compact cranium, integrated midface, depth, head–neck integration (C1) | Greater breadth:height than Marchfolk | **Greater depth:facial height** (5 depth domains; no hard floor, C3) | Humanoid, variable | Substantial tendency | **Not** identified by nose size | Broadly humanoid, non-elven |
| Grask | Elongated, structurally grounded (P3 §1–2) | Normal intelligent vault | Projection distribution **OPEN** (P3 L360) | Orbit ≠ opening | Vertical ramus | Moderate | Folded cartilage, sustained upper body, late taper (P3C) |
| Gorrund | **Transverse Structural Continuity** (P3C) | Greater breadth:height than Marchfolk | Prognathism **OPEN** (P3 L308) | Orbit ≠ opening | Broad and deep | No "ogre nose" | Deep bowl, broad rim, no taper |
| Pipkin | **Integrated Mature Facial Architecture** (P3 §2) | Never enlarged | Depth within the Marchfolk adult range | No enlarged-eye envelope | Mature | Not small or upturned | Compact rounded |
| Cogling | **Fine-Scale Planar Integration** (§75) | Small absolute size, no authored enlargement; head ~11–13 cm | Planar junctions; face-to-vault at or slightly above Marchfolk | No enlargement for readability | Fine but adult | Variable adult | Fine folded (secondary) |
| Saurin | **Layered Rostral-Cranial Integration** (§36) | Low-to-moderate, long | **Rostral index 0.255–0.335 (floor provisional)** (§259) | Forward, broad platform; vertical pupil; nictitating membrane | Deep posterior jaw, no chin | Rostral nasal openings, no nasal pyramid | **Recessed auricular opening, no pinna** |

### E2. Non-overlap floors and extreme-slider convergence

**Saurin is the only explicit cross-race numeric floor.** Its minimum rostrum "remains clearly outside the approved adult projection ranges of Marchfolk, Grask and Gorrund" (§39, §146). But:
- Marchfolk canon has no numeric projection range.
- Grask keeps maxillary/mandibular projection OPEN (P3 L360).
- Gorrund keeps prognathism OPEN (P3 L308).

The floor therefore depends on undefined values. This is a **latent contradiction**: if Grask or Gorrund projection is later set high, the Saurin floor could collide with it (**F-02**). The order says not to resolve the Universal Facial Customization Architecture here, but that architecture needs a **common normalized landmark and metric set** (projection, depth:height, face-to-vault, orbit/aperture) before any per-race floor can be audited.

**Every other face boundary is relational and deliberately non-exclusive:**
- Durrim: "never a hard 'below this value is human' boundary" (C3).
- Pipkin: face "supporting rather than universally exclusive" (P3 §18).
- Cogling: "No single Cogling facial measurement must lie outside the Marchfolk range" (§90A).

**Convergence risks at slider extremes:**
- Durrim ↔ Gorrund: shared cranial-breadth wording; resolved by Gorrund P3C (transverse vs depth-dominant).
- Pipkin broad face ↔ Durrim: guarded by the P3 §17 stress test.
- Skarn ↔ Gorrund faces: Gorrund P3 L328/L398; Skarn gives only qualitative tendencies (v1.0 §8 promised "detailed craniofacial ranges" that were never delivered).
- Fenn ↔ Vael orbit size: both "larger" against different comparators (F-20).
- Grask ear ↔ elven ear: "orientation alone must never distinguish" (P3C L457).
- Saurin minimum rostrum ↔ Grask/Gorrund prognathism: F-02.

---

## F. Surface phenotype

| Race | Integument | Pigmentation envelope | Hair (biology) | Eyes | Display / keratin | Surface-as-identity guard |
|---|---|---|---|---|---|---|
| Marchfolk | Human skin; 3 Skin Appearance Layers | Very light to deep brown; cool → reddish undertones; "not … any one modern real-world population" (Part 2 §1–2) | Full human range | Brown → blue families | — | Reference |
| Skarn | Human | "full natural human skin-tone variation" (v1.3 §2) | Not stated as families | Not stated | — | "Skarn identity never depends on" facial hair |
| Sagekin | Human | Warm beige → deeper brown centre, tied to the "warm maritime homeland" (FD §1, §5) | Black and dark brown common | Brown common | — | "Skin color alone is never a racial marker" (v1.0 §8). No real-world disclaimer (F-19) |
| Fenn | Elven skin | Fair → rich deeper brown; **explicitly not the elven baseline** (v1.3 §1; elf review Part 3) | Human-like colours | Not stated in spec | — | Hidden-ear test |
| Aelari | Elven | Very light → deeper brown (matches the elf review) | + silver/white "if later validated" | Brown → blue (no violet) | — | "Pale skin becomes mandatory" = failure |
| Vael | Elven, living tissue | Charcoal, slate, grays, muted violet, ash-brown; "Not every Vael is extremely dark or gray" | Includes inherited silver/white | Includes muted violet; never auto-glow | — | Strict neutral-complexion test |
| Halvren | Mixed | No RGB averaging; latent ancestry | Biology vs presentation strict | Combined human and elven families | — | Pigmentation-neutralization test |
| Durrim | Human-like | Broad, independent of skeleton; no ruddy default | No canonical colour | Human families | — | Skin and eye neutralization |
| Grask | Biological, not warty | Earth-toned low chroma; some moss-olive / gray-green beyond the human envelope (P4C L578) | Dark families | Includes olive-hazel, gray-green | Tusks not required | "Green-skin recognition" = failure |
| Gorrund | Biological, not rocky | Earth-toned, light → deep; no green; "Earth-toned doesn't mean dark" (P4C) | Dark families | Earth families | Tusks not required | Brown-skin and light/dark tests |
| Pipkin | Human-like | Very low → very high melanin; no default complexion | No curly/rustic requirement; hairy feet not required | Broad | — | "No Pipkin surface phenotype is required" |
| Cogling | Human-like, not doll-smooth | Very light → very deep | Broad | Broad; no enlargement | — | Anti-cute bundle ban (§129) |
| Saurin | **Scaled integument; Regional Scale Architecture** | Earth, olive, slate, rust, cream and others; patterns are biological, not markings | **None** (mammalian hair biologically empty) | Vertical pupil; nictitating membrane; amber → blue-gray | **Cranial Keratin Display family** in the Hair slot; claws | Neutral uniform pigmentation stays Saurin (§93) |

**Assessment:**
- Surface reinforces anatomy without substituting for it in every spec.
- Fenn is not used as the elven complexion baseline anywhere (I-05).
- The same is true of Marchfolk for humans: "Human never equals Marchfolk" (Marchfolk Part 2 §7–9).

**Surface terminology differences** (F-14):
- **Skin Appearance Layers.**
  - Marchfolk, Pipkin, Cogling and the register use **three** layers: Natural / Environmental / Applied or Acquired.
  - Saurin §122 defines **four**, with Applied and Acquired separate.
  - Saurin's own §231 says three.
- **Eye anatomy vs pigmentation.** Separating eye anatomy, iris pigmentation and magical effects is explicit in Aelari (v1.3 §7), Vael, Halvren, Durrim, Grask, Gorrund, Pipkin, Cogling and Saurin. It is absent from Fenn, Skarn and Sagekin, but the elf review Part 3 §16–18 covers the elves.

— Claude

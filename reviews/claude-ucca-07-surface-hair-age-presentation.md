# UCCA-07: Surface, Hair, Age & Presentation Architecture

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §11
**Status:** PROPOSAL for author review.

## 1. Surface: the four Skin Appearance Layers, whole body

| Layer | What it holds | Lives in | Stored | Canon |
|---|---|---|---|---|
| **Natural** | Pigmentation (multidimensional), undertone, perfusion/vascular contribution, regional variation (palms, soles, lips, ears), freckles, moles, birthmarks. **Saurin:** scale-field morphology, inherited pattern, claw keratin colour, integumentary ridges | Slot 10 (+ claws in Slot 4) | Biological Anatomy record (inherited traits stored as anatomy, expressed through Natural; SA L2240–2242) | PR L68; MF L153–162; SA §122 |
| **Environmental** | Tanning/sun response, weathering, dryness, calluses (MF; GO says calluses are acquired), dirt, dust, soot, mud, wetness, abrasion | Slot 10 sub-panel | **AD-C9:** persistent vs transient | PR L68 (dirt = Environmental); DU L387–389; PK L631; SA L1985–1994 |
| **Applied** | Tattoos and tattoo-equivalents, body paint, cosmetics, dye, decorative claw treatment, display polish/paint | Slot 14 Presentation | Presentation record | SA L1927–1934; PK L614 |
| **Acquired** | Scars, burns, healed injuries, damaged scale fields, chipped claws, damaged ridges, localized pigment change, contact/occupational wear | Slot 12 | Acquired-history record (never genetic, SA L2181) | SA L1863–1872; MF L162 |

**Surface rules carried roster-wide:**

| Rule | Canon |
|---|---|
| **Never one Skin Color slider** | DU L354; GR L506; GO L508; CG L1728; HV L245 |
| Lighting invariance: stored values never change under lighting; neutral reference lighting first | ECR L165; VA L375; SAU-CC-20 |
| Surface never compensates for structure: identity survives neutral grey / uniform pigment | CG L1600; PK L474; SA L1539–1541; GR L431 |
| Validity ≠ frequency; no hard phenotype–pigmentation packages | MF L307; DU L414; GR L562; GO L562; CG L1966–1971 |
| Environmental and Acquired never forced by race, class or occupation; soot and grime are never racial | MF L189; DU L389; GR L538; GO L533 |
| **Saurin scale fields:** field boundaries and functions locked; **no global scale-size control**; expressive and articulation fields never coarsen toward structural size; numeric per-field ranges OPEN | SA L4207 |
| No unrestricted RGB picker (Saurin) | SA L1473 |

## 2. Hair and homologues

| System | Biology (Natural; slot) | Styling (Presentation) | Interfaces |
|---|---|---|---|
| Scalp hair | Texture, density, hairline, growth, natural colour, inherited silver/white (≠ age graying, AE L336; VA L395) | Length, cut, braids, shaving, dye, accessories | UFCA slot 10 is the same variable (shown in both places) |
| Facial hair, eyebrows | **UFCA slot 11** (closed, incl. Q-2 eyebrow biology) | Grooming → Presentation | UCCA adds nothing |
| Body hair | **Slot 9**, where bound: PK (L561–567: hairy feet not required; never rusticity or masculinity), CG (L1817–1823: not determined by scalp, sex or muscularity; sex distributions soft only) | Shaving/grooming | **AD-C7** for MF, SK, SG, FN, AE, VA, HV (SILENT); DU, GR, GO stay biological OPEN (UCCA-10) |
| Saurin | **No mammalian hair** (Absent). Cranial display → UFCA slot 10; optional restrained body continuation onto neck, dorsal trunk, sacrum, tail (§101a), never a mandatory spinal crest | Display polish, paint, wraps | Tail dorsal keratin shown in Slot 5 |

**Rules:**
- Hair colour is related across scalp, brows, face and body without identical values (DU L366; GR L518; GO L517).
- Hair is never locked to frame, sex, physique or occupation (AE L344; VA L407).
- Hair-strand diameter does not scale linearly with stature (CG L2033).

## 3. Age

| Element | Architecture |
|---|---|
| **Chronological Age** | Character data (non-appearance). Never inferred from appearance (HV L307) |
| **Apparent Biological Age** | **One systemic DIR driver for face and body** (UFCA slot 14 = UCCA slot 11; one variable). Adult creator scope only (MF L210; SA L2088) |
| Body age effects | **DER OFFSETS** on the individual: composition redistribution, skin elasticity/texture, hair density and colour, scale-edge wear and contrast change (SA), claw wear (SA), and posture-range tendencies **only where canon allows** ("where individually appropriate", ECR L245; CG L1937; SA L2124 "only where biologically justified later") |
| **Age Presentation** | Presentation (Slot 14) |

**Firewalls carried as validators:**

| Firewall | Canon |
|---|---|
| No frailty, stoop or slowness package | SK L183; DU L383; GR L534; GO L529; PK L1481; CG L2524–2530; SA §130 |
| Aging is never "wrinkles + gray hair" only | MF L257; DU L374 |
| Aging never changes racial skeletal identity, and no ogre or troll growth | GO L527; GR L532 |
| Age never changes stature dramatically | CG L1943–1947 |
| Cosmetic age carries no gameplay penalty (the plan's "age → movement speed" is level-6 and non-authoritative) | MF L212 |
| Adults read adult at the youngest valid age without age cues | PK L385; CG L1905; SA §127 |
| No lifespan-percentage slider | HV L325 |

**Age starting points** (SA young / established / mature / late adult, §131; MF reference points, L210) are **write operations on Apparent Biological Age**, not chronological bins.

**Lifecycle is OPEN everywhere.**

## 4. Presentation

| Domain | Architecture | Canon |
|---|---|---|
| Culture / birthplace / background | Presentation presets and identity layers. **Never write anatomy**. Proposed universal (SG L305–312; SK L247). "Choosing a race never applies cultural markings automatically" | SK L243; SG L301; FN L333; AE L380/L431; VA L443; HV L347 |
| Markings | Applied layer placement: position, scale, rotation, colour, opacity, mirroring, layering, independent removal; respects anatomical regions; Saurin patterns are not markings | MF L183–185; SA L1493–1506 |
| Body language | **Slot 13**: idle, stance and gesture presentation. **Never writes Anatomical Resting Alignment** (PR L21). No race defaults: no graceful-elf, sinister, waddle, bounce, fidget or tinker poses. Saurin tail poses carry no fixed emotional meaning | FN L447; VA L580; PK L963–967; CG L2470–2496; SA L3000–3012 |
| Clothing / gear preview | Creator preview only. Equipment fits anatomy; canonical equipment never scales with the holder. **Saurin:** partial tail coverage allowed if the tail persists (§195); no garment may erase the tail | PR L26; SA L3122–3140 |
| Creator camera and lighting | Neutral reference lighting; warm/cool/lower previews; purpose views (whole body, face, hands, feet, **tail**, surface) | VA L588; CG L3031–3041; PK L1304–1308; SA L2649–2658 |

## 5. Shared vs population-bound

| Shared (universal structure) | Population-bound (contents) |
|---|---|
| Four-layer model; multidimensional pigmentation concept; lighting invariance; hair biology vs styling split; one age driver and triad; firewalls; presentation-never-writes-anatomy; Body Language slot | Pigmentation families and envelopes; Saurin scales, pattern and claws; body-hair binding (AD-C7); hair envelopes (Grask/Gorrund colour ranges); age-effect lists per canon; tail presentation |

— Claude

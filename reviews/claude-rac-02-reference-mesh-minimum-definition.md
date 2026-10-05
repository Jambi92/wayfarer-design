# RAC-02: Reference-Mesh Minimum Definition

**Author:** Claude
**Order:** `reviews/chatgpt-reference-anatomy-closure-phase1-order.md` §3 (RAC-02)
**Status:** PROPOSAL for author review. Defines what an **approved reference mesh** must *be* for measurement. It does **not** choose topology, rig, skeleton family, morph architecture or engine.

## 1. Why a definition is needed

RMQ already requires "an approved reference mesh (central tendency), plus Narrow / Broad frame-preset meshes and the creator-extreme variants the race's validation set already names" (RMQ L16). Canon never says what makes a mesh "approved" or what state it must be in, and two items block every central mesh until defined (RAC-01 B-26, B-27):
- no spec defines "moderate composition" (GR L122, GO L129, PK L102) or "reference composition" (SA L4236);
- no measurement stance is canon (Saurin's frozen stance is explicitly "not the final dynamically balanced neutral standing pose", SA L4162).

## 2. Proposed definition: Approved Reference Mesh (ARM)

An **ARM** is a mesh representing **one adult individual** of one population, in the states below, that has passed the acceptance test in §5 **and been accepted by the author**. Measurements taken from it are **diagnostic envelopes first** and become canon only by author acceptance (RMQ rule 4, L100; the Saurin Part 7 model).

| # | Requirement | Proposed content | Canon basis |
|---|---|---|---|
| R-1 | **Central-tendency adult biological anatomy** | The population's central tendencies as stated in its spec. Every [POS] tendency is visibly present; every [BAN] is absent. Adult read at the race's youngest valid adult age or older; Apparent Biological Age at a mid-adult value | Each race's identity sections; UCCA §15 (adult scope) |
| R-2 | **Stature** | The race **reference height** (MF 173, SK 208, SG 178, FN 181, AE 190, VA 178, HV 178, DU 137, GR 218, GO 229, PK 107, CG 91, SA 188 cm), reached by proportion, **never by uniform scaling from another population or from another stature** | Race height tables; UCCA §6.4 |
| R-3 | **Skeletal Frame reference state** | The population's **central skeletal values** for every frame variable. Canon labels this case "Balanced" in reference tests (SG L186; FN L84; AE L85; VA L80; GR L122; GO L129; PK L102; SA L4236). The ARM records it as **central values, not as a "Balanced" state**, because Balanced is not the default body (UCCA L121) and frame has no persistent state (UCCA §7) | UCCA §7 |
| R-4 | **Physical Composition reference state** (defines "moderate / reference composition") | **Current Muscularity and Body-Fat Amount at the population centre, with a neutral (untilted) fat distribution and no regional muscle offsets.** Saurin: fat placed by the canonical depot ordering (SA L4172); the frozen reference composition (aff1b52) is the embodied Saurin value. Capacity is irrelevant at the centre (the centre lies below any ceiling, UCCA L161) | B-26; UCCA §10; RAC-06 |
| R-5 | **Natural asymmetry** | **Zero.** Bilaterally symmetric by mirroring, after any surface noise is removed | UCCA §16 (neutral default = zero / near-zero) |
| R-6 | **Measurement stance** (proposed new method term) | Upright anatomical standing: head in neutral carriage; arms hanging with a small fixed abduction so the torso silhouette is clear; palms facing the thighs; feet at hip width, parallel, full plantigrade contact; knees and hips extended without lock or crouch; **spine in neutral adult curvature with no race identity carried by curvature** (GR L44; GO L191; PK L709; VA L121 "natural lumbar curve" is the only positive curvature). **Saurin:** the frozen reference stance, with tail carriage at reference and no ground contact (SA L4154, L4162). The stance is a **measurement convention, not Anatomical Resting Alignment and not an idle** | B-27; PR (Resting Alignment ≠ Body Language); SA L4162 |
| R-7 | **Neutral presentation and body language** | UCCA **N3 for the body**: no clothing (or a neutral fitted proxy only where a sensitive region must be covered, and never over a measured landmark), no jewellery, no Applied markings, no Body Language preset, no equipment. Head treated at **N-Head** for body measurements only when a body test requires it | UCCA §24 N-levels; SA L3142 (equipment never validates a body) |
| R-8 | **Hair** | Scalp hair removed or replaced by a skin-tight cap volume of zero thickness for skeletal and craniofacial measurement; **no facial hair, no body hair** (N2). Saurin: no mammalian hair; cranial display at the frozen reference state, **excluded from head-length measurement** (r3 L40, keratin display excluded from FAL) | UCCA §13, §24 |
| R-9 | **Surface state** | A single neutral, matte, uniform material; **no Environmental, Applied or Acquired layer**; no normal-map or displacement detail that changes the measured silhouette. Racial structure is in geometry, never in material (DU L280; UCCA L214) | UCCA §14 |
| R-10 | **Sex-related anatomy** | One ARM per **sex-related configuration** the race validates. Under R-SEX, hard bounds are shared and "no shift" is a valid complete state (PR L91, L94). Where a race has no authored shift, its two configurations share every skeletal and composition value. **Saurin:** male centre and female centre per §263 (the "reference female" already validated, SA L4252). See §4 for the bootstrap rule and RAC-07 for the open soft-tissue question | PR R-SEX; UCCA L135, L333; PK L224–225; CG L2949 |
| R-11 | **Race-specific mandatory anatomy** | Present and at reference: **Saurin tail** (mandatory, never removed, measured from the caudal-base landmark, RAC-10), E/B at the configuration's centre, claws, scale-field topology. Ear family per UFCA §10.2 at the population centre | SA §256, §258, §263; UFCA §10.2 |
| R-12 | **No contamination** | No culture, class, occupation, equipment, weathering, scars, grime, posture-coded personality or stereotype bundle (UCCA §18–§19; every race's [BAN] list) | UCCA §14, §18 |
| R-13 | **Scale and units** | Real-world metres; ground plane at the sole; the up axis vertical; stature measured to the top of the skull (vertex), excluding hair and keratin display. **Saurin stature excludes the tail** (SA L64) | SA L64; r3 conventions |
| R-14 | **Provenance record** | Source, build method, every input value used to build it, and any value **chosen by a builder** rather than taken from canon (see §6) | RMQ rule 1 (L97) |

## 3. Variant meshes (not the ARM)

| Variant | Definition | Needed for |
|---|---|---|
| **Frame variants** | ARM with frame variables written to the race's Narrow and Broad starting values; everything else unchanged | RM-LR-02, RM-UB-03 |
| **Stature variants** | Minimum and maximum race stature, by proportion and allometry, never by scaling the ARM | RM-UB-02, MF/HV/DU/PK/CG boundary tests |
| **Composition variants** | Low / high muscularity and fat on the central skeleton | Tier I tests; Durrim and Gorrund low-muscle identity tests |
| **Named extreme cases** | Each race's named validation cases (GR-BODY-10, GOR-BODY-12/14, PIP-BODY-02, COG-BODY-11 and so on) | RM-LR-03/04, RM-SR-04, AD-1/2/3 |
| **Sex-related configuration** | Per R-10 | Like-for-like tests |

**Variants are measured but never back-fitted:** a variant that FAILs its race's tests is corrected; the population distribution is not weakened to fit it (RMQ rule 3, L99).

## 4. Is one central mesh per population enough for the bootstrap?

**For bootstrap measurement of central relationships: yes, one ARM per sex-related configuration, for 12 of 13 populations.** Central items (RM-LR-01/05/07, RM-SR-01/03, RM-CF-01, RM-CF-10 central, RM-OT-01) need only central anatomy.

**Not enough for:**
- any **boundary** item: "Central values alone never establish a boundary" (RMQ L98). Extreme and frame variants are needed for RM-LR-02/03/04, RM-UB-02/03, RM-SR-04 minimum cases, RM-CF-02/03/04 maximum-valid faces;
- **allometry** (RM-UB-02), which needs min / ref / max per race.

**Populations needing more than one *biological* reference state:**

| Population | Why | Proposed bootstrap |
|---|---|---|
| **Halvren** | Has no single reference body (HV L361: "balanced" never means 50/50; genealogy conditions B) | One ARM for the **no-lineage general envelope** (UFCA L223) at the 178 cm reference (HV L88, L481), plus genealogy-conditioned references only when RM-OT-03 / RM-UB-05 run (W3). No genealogy-conditioned ARM is needed for Wave 1 |
| **Saurin** | Sex-related states are authored (§263) | Male-centre ARM = frozen reference aff1b52; female-centre = the validated reference-female warp (SA L4252), once accepted as an ARM |
| **Marchfolk** | Comparator for every other race and required in both configurations by PK L224–225 | Two ARMs (both configurations) **plus** 147 and 203 cm stature variants in Wave 1 (RM-UB-07, proposed) |
| **Races with OPEN sex magnitude** (DU, GR, GO, PK, CG) | A second configuration needs external sex-related soft tissue that canon has not authored | **Bootstrap on one configuration**; the second configuration waits for the RAC-07 author decision. Skeletal measurements are unaffected under "no shift" |

## 5. Acceptance test for a candidate to become an ARM

A candidate (new build or existing asset) passes only if:
1. **R-1…R-14 hold**, verified on renders at the RMQ conventions (orthographic front, side, 3/4; common ground line; grid).
2. **Every permanent race test that applies to a central body passes** (UCCA §24 tiers A, E, I at least), including the race's **neutralization** tests at N3.
3. **Pairwise boundary tests** that involve the central body pass at shared stature or matched scale (tier B).
4. **No input value is an un-declared builder choice** (§6). Builder-chosen values are listed and **accepted explicitly by the author** as part of the ARM, never discovered later by measurement.
5. **Author acceptance**, recorded in the RMQ and the race spec's status line.

## 6. Circularity rule (proposed)

A mesh built from **numeric targets chosen by a builder** (a solver, a sculptor, an AI) returns those targets when measured. Measuring it therefore **cannot discover** canon; it can only **confirm the builder's choices**.

**Rule:** where an ARM embodies builder-chosen numbers, its acceptance is an **authorship decision** about those numbers and must be recorded as such. Measurement-derived envelopes from it are labelled "derived from builder-chosen reference values accepted on <date>". This is how Saurin Part 7 already worked (the frozen reference was accepted first; envelopes were derived from it). RAC-12 §5 applies this rule to the existing assets.

## 7. What this definition does not decide

Topology, vertex count, UV layout, skeleton family, rig, morph targets, engine, file format, LOD, or whether ARMs become runtime assets. All stay implementation-deferred (UCCA §26).

## 8. Proposed author decisions

| ID | Decision |
|---|---|
| AD-R1 | Adopt the ARM definition R-1…R-14 |
| AD-R2 | Define "moderate / reference composition" as R-4 (population-centre muscularity and fat amount, neutral distribution; Saurin depot ordering) |
| AD-R3 | Adopt the measurement stance R-6 as a method convention, distinct from Resting Alignment |
| AD-R4 | Adopt the bootstrap rule of §4 (one ARM per validated configuration; Halvren general-envelope ARM; Marchfolk two configurations plus stature variants) |
| AD-R5 | Adopt the circularity rule of §6 |

— Claude

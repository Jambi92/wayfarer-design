# UCCA-10: OPEN / Deferred / Author-Decision Register

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §14
**Status:** REGISTER for author review. **Nothing here is resolved by UCCA.** No OPEN item has been closed because the architecture would be cleaner if it were.

**Categories:**

| Code | Meaning |
|---|---|
| **AUTH** | Genuine author decision: canon permits more than one answer; UCCA proposes one |
| **BIO** | Biological OPEN in canon; must be authored as biology, not chosen as architecture |
| **MEAS** | Measurement-deferred: needs approved reference meshes / measurement, not a decision |
| **IMPL** | Implementation-deferred: technical / UE5 / serialization |
| **GAME** | Later gameplay review: outside creator biology |

## 1. Author decisions raised by UCCA (AD-C)

These are the decisions UCCA needs before any canonicalization. Each has a recommendation; none is adopted.

| ID | Decision | UCCA recommendation | Alternatives | Source |
|---|---|---|---|---|
| AD-C1 | Adopt the **15-slot body navigation** (0 Race & Lineage … 14 Presentation) as the universal creator hierarchy, with Face = UFCA | Adopt | Merge Hands & Feet into Stature & Proportions; split Hair from Display | UCCA-02 |
| AD-C2 | **No persistent frame state**: resolved skeletal values are the frame; N/B/B are write operations; optional non-driving provenance | Adopt | Keep a persistent frame label that drives values (no canon need found) | UCCA-05 §2 |
| AD-C3 | **Race-relative storage**: stature is the only absolute size control; other sizes stored race-relative, absolutes DER via per-race allometry (RM-UB-02) | Adopt | Store absolutes and validate against stature | UCCA-03, -04 |
| AD-C3b | **Halvren stature tails**: limits are biological OPEN; canon forbids hard clipping into 152–213 (HV L481) | Author tail limits before canonicalizing Halvren stature; any central-only interim creator range must be labelled interim test scope (T-12) | Expose tails now (would invent numbers: not permitted) | UCCA-04; HV L481, L490 |
| AD-C4 | **Muscular Development Capacity exposure** | Option (a): Detailed control only where canon names it as a variation axis / representable variable (SA L358; CG §69, sliders not finalized); VAL ceiling elsewhere | (b) everywhere; (c) never | UCCA-06 §2 |
| AD-C5 | **Composition starting presets** Lean / Athletic / Muscular / Heavy universal (canon is MF only) | Adopt as Slot 6 write-and-vanish operations | MF only; per-race libraries | UCCA-06 §4; MF L5, L281 |
| AD-C6 | **Sex-related anatomy selection = SOFT input** that shifts only race-canon generation centres; never moves stored values; never a package | Adopt | — (R-SEX already requires the substance; the decision is the architectural form) | UCCA-03; R-SEX; SA §263 |
| AD-C7 | **Body hair** for races where canon is SILENT (MF, SK, SG, FN, AE, VA, HV): bind or keep hidden | Keep hidden until authored; DU, GR, GO stay BIO (OPEN) | Bind a generic body-hair set (would be new biology for those races: not recommended) | UCCA-07 §2 |
| AD-C8 | **Natural body asymmetry** for races other than Saurin | Keep hidden (SILENT) | Universal subtle offsets | UCCA-02, -03 |
| AD-C9 | **Environmental layer persistence**: which items are persistent appearance (tanning, weathering, calluses) vs transient state (dirt, wetness) | Split persistent vs transient; calluses: author to choose Environmental (MF) or Acquired (GO) | All persistent; all transient | UCCA-07 §1 |
| AD-C10 | **Neck length** as a control outside Saurin | Bind only where canon names it; others hidden pending RM-UB-01 | Universal neck-length DIR | UCCA-03, -04 |
| AD-C11 | **Body Language slot (13)** universal, never writing Anatomical Resting Alignment | Adopt | Fold into Presentation (14) | UCCA-02, -07 §4 |
| AD-C12 | **Universal selective-randomization scopes and lock groups** (canon union, UCCA-08 §4) | Adopt the union; population-bound scopes appear only where bound | Per-race scope lists | UCCA-08 §4 |
| AD-C13 | **Conceptual appearance-record domains 1–14** and rules S-1…S-7 | Adopt as conceptual requirement; no format | — | UCCA-08 §6 |
| AD-C14 | **Generic pairwise body harness** (shared stature where one exists; matched-scale otherwise; diagnostic only) | Adopt; race tests stay authoritative | Rely on race-authored tests only | UCCA-04 §8; UCCA-09 §3 |
| AD-C15 | **Universal proposed validators**: no-uniform-scale test; frame × sex × composition factorial; Athletic write test; Body Language test; Simple → Advanced equivalence; N-level body extension | Adopt | Per-race adoption | UCCA-09 |
| AD-C16 | **Canon tensions** (§5): which wording governs in each case | Author to rule per item; UCCA carries both | — | UCCA-01 B-8 |
| AD-C17 | **A shared slot never by itself authorizes a control** (UFCA AD-U12 extended to the body) | Adopt | — | UCCA-02 |

## 2. Order §14 required audit items

| Item | Category | Status in canon | UCCA handling |
|---|---|---|---|
| **Head-to-stature measurements** | MEAS + BIO | OPEN for every race except SA (UCCA-01 §11). SA has a head share (§55) and a +8 % centre (§258) in tension (§5 T-1) | Anti-juvenile head validators carried; values not invented. Feeds RM-UB-01/02. No player control is created from the measurement |
| **Population segment distributions** | MEAS (and BIO where canon says OPEN) | "Segment ratios and numeric proportions" OPEN for all (UCCA-01 §23); arm span OPEN GR, PK | RM-UB-01; CLAMP bands left unnumbered |
| **Grask / Gorrund ear ranges** (whole-character touch only) | BIO → MEAS | Grask ear-length and Gorrund projection ranges are not authored; RM-UF-02 depends on them (UFCA_V1 L359) | Touches UCCA only through head-to-stature and silhouette tests. **No body-side action**; stays with UFCA RM-UF-02 |
| **Saurin tail-base / length / mass coupling** | BIO (exact coupling) + MEAS (cap function) | §256 gives closed first-pass bands (base ≈ length^1.18; root-sufficiency 0.75–1.20; taper; carriage; balance ≤ +3°); "exact coupled relationship" carried OPEN (SA L620) | UCCA uses only the §256 bands as validators; the continuous reachable-length cap is RM-UB-04. Mass / density model stays BIO (SA §265 balanced posture and density) |
| **Saurin partial garment coverage** | **Permission RESOLVED in canon; construction and coverage extent OPEN (IMPL)** | SA L620 "since resolved, §195/§225"; L3549: garments may partially cover, drape or sheath the tail, never making a Saurin functionally tailless. Still OPEN: "tail equipment construction and coverage extent" (L2050; §251 L4067) | Permission carried as a Presentation validator (UCCA-07 §4); construction deferred with equipment fit |
| **Acquired Saurin tail loss / injury** | BIO (injury system) | OPEN (SA L209, L1085, L2179, L2324, L3557, L4014); excluded from randomization; "not equivalent to a creator toggle" | Acquired pass never creates it (UCCA-08 §3). No creator control. Not to be decided by equipment or customization implementation (SA L1085) |
| **Saurin thermoregulation** | BIO | OPEN (SA L2048, L4011); "no automatic cold vulnerability, heat resistance or temperature-related gameplay modifier is implied" | No creator control; no surface or composition variable implies it |
| **Reproductive biology** | BIO | SA: reproductive life history and physiology OPEN (L2520, L4005, L4242); body / external sex-related anatomy resolved by §263. Other races: sex dimorphism magnitude OPEN (DU, GR, GO, PK, CG) | Slot 7 carries only what §263 (and race canon) closes; B is **not** explained as a reproductive fat body (L4242: "not canon") |
| **Lifecycle questions** | BIO | OPEN everywhere (UCCA-01 §23) | Age architecture covers adult creator scope only; no lifespan-percentage slider (HV L325) |
| **Statistical calibration** | MEAS (+ AUTH for final weights) | Interim weights never canon (UFCA §15); Saurin statistical spreads around sex-shifted centres OPEN (L4271); fat-distribution, joint/robusticity and capacity distributions OPEN | Generator architecture defined; distributions left unnumbered. Batch diversity threshold = RM-UF-05 |
| **Saved-appearance schema implementation** | IMPL | "Serialization isn't redesigned yet" (plan); race specs require semantic, versioned records (PK L1442; CG L2995) | Conceptual domains only (UCCA-08 §6; AD-C13). **No format decided** |
| **Body technical architecture** | IMPL | Deferred (PR L24–29; SK L380) | Manny/Quinn superseded **at design level only** (UCCA-05 §5); mesh / morph / skeleton approach not decided |
| **Animation / locomotion implications** | IMPL + BIO (Saurin) | Animation / IK / retargeting deferred (UCCA-01 §23). Saurin balanced posture and density model OPEN (§265) | Body Language never writes Resting Alignment; no gait or locomotion variable is a creator control |
| **Equipment-fit implications** | IMPL (+ SA validators) | SA §191 equipment-fit principle; SAU-EQP test family; human equipment fit non-authoritative (SA L3917); canonical equipment never scales with the holder (PR L26) | Clothing/gear is creator preview only (UCCA-07 §4). Fit system deferred |
| **First-person body geometry** | IMPL + GAME | OPEN: PK §16 (L1310–1316); CG L2462, L2895; SK L346 (eye height "if first-person") | If implemented, actual eye height, reach and hand scale must stay truthful. No creator variable |
| **Class / gameplay traits outside creator biology** | GAME | Legacy traits flagged for later review: SK breath; FN sneak/swim; DU breath/swim; GR; GO; PK sneak (L76); SA breath/swim (UCCA-01 §23). Visual muscularity / capacity never imply strength (UCCA-06 §2). Cosmetic age carries no penalty (MF L212) | Firewalled: no creator value feeds a gameplay stat. The plan's age → movement-speed link (level 6) is non-authoritative |

## 3. Other biological OPEN items carried (not resolved)

| Item | Races |
|---|---|
| Pelvic morphology | FN, AE, VA, HV (Class B), DU, GR, GO, PK, CG; SA sacral |
| Joint / robusticity distributions | All |
| Muscular Development Capacity distributions | GR, GO, PK, CG |
| Fat-distribution tendencies | All |
| Sex dimorphism magnitude | DU, GR, GO, PK, CG |
| Body hair | DU, GR, GO (others SILENT → AD-C7) |
| Halvren stature tail limits and frequencies | HV L481, L490 |
| Saurin: caudal-base landmark; numeric lower-trunk minimum vs MF; numeric Broad-vs-Gorrund boundary; claw and digit numeric ranges; per-field scale ranges; tail world-space validation | SA §265 |
| Skin thickness / durability | DU, GR, GO |

## 4. Measurement-deferred

| ID | Item | Status |
|---|---|---|
| RM-UB-01 | Segment-share and within-limb distribution bands | Proposed (UCCA-04 §9) |
| RM-UB-02 | Per-race allometric response to stature | Proposed |
| RM-UB-03 | Joint-scale and robusticity envelopes | Proposed |
| RM-UB-04 | Saurin reachable tail-length cap function | Proposed |
| RM-LR-01…07, RM-SR-01…06, RM-OT-01…05, RM-CF-10 | Existing Pass 2 queue | Carried unchanged; RM-OT-04 covers the SG–SA and HV–SA gaps (UCCA-09 §3) |
| RM-UF-01…05 | UFCA queue | Carried unchanged; RM-UF-05 serves body batch diversity too |

## 5. Canon tensions (AD-C16; carried, not resolved)

| # | Tension | Sources |
|---|---|---|
| T-1 | Saurin head share (§55) vs the +8 % centre (§258) | SA |
| T-2 | Pipkin trunk-share absorption | PK L137 vs L164 |
| T-3 | Aelari has two presentation-preset lists | AE L380 vs L431 |
| T-4 | Saurin §145 tail muscularity is superseded by §256.6 but not marked | SA |
| T-5 | Halvren old height wording | HV L156, L410 |
| T-6 | Durrim–Marchfolk equal-height test stature: "about 150–152 cm" (DU L72) vs 152 cm after the correction (DU L145, L337; UFCA-07 N-2) | DU |
| T-7 | Grask "tallest" wording is stale | GR |
| T-8 | Register's "three skin layers" entry is stale (canon has four) | Register L21 |
| T-9 | Calluses: Environmental (MF) vs Acquired (GO) | MF; GO; → AD-C9 |
| T-10 | Vael torso control list omits shoulder and pelvic width, although frame changes them | VA L121 vs L128 |
| T-11 | Prototype plan's age → movement-speed link and "race + slider values" record conflict with canon (level 6; non-authoritative) | Plan |
| T-12 | Halvren central-only interim creator range (if adopted) vs "never set by hard clipping" | HV L481; AD-C3b |

**None of T-1…T-12 is a stop condition:** each can be carried by the architecture whichever wording the author rules for.

— Claude

# UCCA-04: Stature & Proportional Architecture

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §8
**Status:** PROPOSAL for author review. No numeric segment distribution is invented. Every number below is quoted from canon.

## 1. The core answer

**How does a player change height and keep a valid member of that population?**

1. **Stature is the only absolute size control.** It is DIR, in centimetres, inside the race envelope (UCCA-01 §2).
2. **Everything else that has size is stored relative to the race**, never as an absolute that height must drag along. That covers:
   - segment *shares* (torso/axial, neck, arm, leg) and within-limb *distributions* (upper-arm/forearm, femur/lower-leg, palm/finger);
   - breadths and depths *relative to race-normalized stature* (shoulder, thorax, pelvis, joints, hands, feet).
3. **Absolute dimensions are DER.** They are computed from stature × the stored relative value × the **race's allometric response** for that variable. Allometry is per race and per variable. It is **never one shared multiplier**:
   - "bone diameter, joints, hands, feet never scale linearly with stature" (GO L224);
   - Cogling height does not change head size or hand/finger emphasis "by identical percentage" (CG L888);
   - "height distributes through" spine, torso, pelvis, femur, lower leg, neck and head (GO L31; GR L19; DU L19).
4. When the player moves stature, the stored relative values are **retained as OFFSETS**. The individual keeps their proportional identity, and the absolutes are re-derived.
5. The full validator set then runs at the new stature:
   - the combined-proportion rules;
   - the race extreme-stature tests (for example PIP-STRESS-03/04, GOR-STRESS-01…05, Aelari 221 cm, Saurin §247).

   If a retained value is invalid at the new stature (for example a breadth that is valid at 107 cm but fails the Durrim boundary at 122 cm for Pipkin), the outcome is **CONSTRAIN**: the nearest valid value is applied, the intent is retained, and the change is reported. If a lock prevents that, the outcome is **FAIL**.
6. **The allometric response curves are measurement-deferred (RM-UB-02).** Until reference meshes exist, they are defined semantically: their inputs, outputs and the canon constraints they must satisfy. No curve shape is invented.

**Result:** uniform scaling cannot occur in the design model. It survives only as a prototype placeholder (PR L29; plan gap #4).

## 2. Variables

| Variable | Class | Representation | Canon constraints | RM |
|---|---|---|---|---|
| Stature | DIR | cm | Race min/ref/max (UCCA-01 §2). Halvren: ancestry-dependent envelope B; tail limits OPEN (AD-C3b) | — |
| Torso / axial vertical contribution | DIR | share vs race reference | Race tendencies: SK larger; SG, FN smaller; AE longer; GR lower; GO > GR; DU compact greater; PK modestly reduced central trunk; CG near MF; SA axial trunk ±10 % | RM-LR-01…, RM-SR-01, RM-OT-01/02 |
| Neck length | DIR (SA ±15 %); others AD-C10 | share | Absolute ≠ proportional (ECR L320; HV L122) | RM-UB-01 |
| Arm length + distribution | DIR | share + ratio | GR greater (AD-2/AD-3 floor); GO less than GR; CG near-human total with distal redistribution; SA ±6 % | RM-LR-04, RM-SR-02 |
| Leg length + distribution | DIR | share + ratio | VA smaller share than FN/AE; GR greater; PK never automatically beyond human; SA ±6 % | RM-UB-01 |
| Hands / feet | DIR sets | relative | Race-specific; never one scalar | RM-UB-01 |
| Head-to-stature | SA DIR (0.156–0.184 H); others VAL / DIAG | ratio | DU, PK, CG: never oversized, never maturity; GR, GO: OPEN | RM-CF-10, RM-SR-04 |
| Shoulder / pelvic breadth | DIR (Slot 3) | relative to stature | SA ±8 % / ±7 % | — |
| Arm span | DER | — | Never a slider (GR L225; GO L202) | RM-UB-01 |

## 3. Population-specific valid ranges and distribution

- **Ranges** are exactly the canon envelopes (UCCA-01 §2). Halvren is the one race whose envelope is **conditional**: the central envelope 152–213 cm, plus ancestry-dependent tails whose limits are **OPEN** (L481, L490).
- **AD-C3b (author decision, not a recommendation to clip):** the architecture carries tails structurally: envelope B is ancestry-dependent and may extend beyond 152–213 cm. Canon forbids setting limits by "hard clipping, compressing all inherited heights into 152–213" (HV L481), so a central-only creator range can at most be a **labelled interim test scope**, and it stands in tension with L481 (T-12). Tail limits must be authored before Halvren stature is canonicalized. HV-49/50 stay validation targets. No tail number is invented.
- **Stature distributions** are OPEN or SILENT for every race. Generation therefore uses **interim testing weights**, never canon (PK L1411; CG L2966; UFCA §15). The Very Common / Common / Uncommon / Rare vocabulary describes weighting only.

## 4. Segment contribution and the Saurin stature accounting

**General rule:** segment shares are DIR with race-specific bands. Combined validity forbids every segment at its maximum at once:
- GR L174 forbids maximizing every limb segment;
- AE L152 forbids independent segment stretching;
- PK L98 lists mandatory links.

**Saurin special case (canon-named REDISTRIBUTE).**
- Canon: "elongated lower trunk and moderate-to-long legs cannot both expand without compensation; head, neck, thoracic-height, lower-trunk and leg shares must be accounted" (SA L607).
- Combined validity is "stature × head share × thoracic share × lower-trunk share × leg share" (§158 L2571).
- **Proposal:** when a Saurin share is raised at fixed stature, the deficit is redistributed across the **unlocked** remaining shares, inside their §258 bounds, in the canon order of preference: "lower trunk paid for by modestly reduced head/thoracic vertical contribution rather than shortened legs" (§55 L970).
- If no unlocked share can absorb it: CONSTRAIN, then FAIL.
- This is the only REDISTRIBUTE authorized (UCCA-03 §1).

**Other races.** Canon names no redistribution, so shares change **independently within CLAMP bounds**. The stature constraint is satisfied by deriving the unexposed remainder (DER).

**Pipkin tension (noted, not resolved).** The PK reduced trunk share is "absorbed primarily through sustained limb contribution and pelvic vertical contribution" (L137), while legs "never automatically exceed ordinary human adult proportions" (L164). The split is unquantified: torso ratios OPEN (L1533). UCCA keeps both as validators.

## 5. Torso vs limb, arm/leg, shoulder/pelvis, hand/foot scale

Canon relationships carried as validators, never as sliders:

| Relationship | Canon |
|---|---|
| Grask vs Gorrund limb contribution | Shortest-limbed Grask trends **above** the Gorrund limb-present family (AD-3; GR L259; GO L232). Numeric floor RM-LR-04 |
| Skarn vs Gorrund | Proportional separation **undetermined by design** (AD-4; GO L673). **No Gorrund torso/limb default may be derived from Skarn** |
| Durrim vs Pipkin at ~122 cm | Torso vertical organization, thoracic breadth/depth, limb contribution, joints, robusticity (PK L192; SR-COMP-03) |
| Pipkin vs Cogling at ~91–107 cm | Near-MF Cogling axial share vs modestly reduced Pipkin central-trunk share (SR-COMP-01/02). "Leg segmentation alone cannot separate" (CG L914) |
| Shoulder-to-pelvis | Continuum, not subtypes (GO L188). No single shoulder-to-hip ratio defines identity (CG L252, L877; PK L1491–1492) |
| Hand / foot scale | Never a single scalar (B-1). DU/GO relatively large; PK moderate hands and somewhat larger feet as a tendency; CG fingers long; SA ±8 % |

## 6. Head-to-stature

- **Deferred** wherever canon has not authored it (UFCA AD-U4; RM-CF-10).
- **Saurin** keeps its ±8 % DIR.
- **Noted tension:** §55 "near to modestly below Marchfolk" vs §258 "+8 % head-scale decision is the centre" (relative to an unstated base). This is not resolved; recorded in UCCA-10.
- **Anti-juvenile validators** (PK L199, L455; CG L274–284; DU L21) apply at every stature, especially the minimum.

## 7. Extreme-height validity

Each race's extreme-stature tests are carried forward as tier H (UCCA-09):

| Race | Tests |
|---|---|
| MF | 147 / 173 / 203 permanent characters (L249) |
| SK | SK-02 / 03 |
| SG | SG-02 / 03 |
| FN | FN-02 / 03 |
| AE | AE-02 / 03; 221 cm permanent stress |
| VA | VL-02 / 03 |
| HV | HV-11 / 12 (central boundaries); HV-49 / 50 (tails) |
| DU | Height boundary 122 / 137 / 152 |
| GR | GR-BODY-02 / 03, GR-BODY-17 / 18 |
| GO | GOR-BODY-02 / 03, GOR-STRESS-01…05 |
| PK | PIP-BODY-02 / 03, PIP-STRESS-01…05 |
| CG | COG-BODY-02 / 03 |
| SA | §247 min / ref / max with frame, composition and tail extremes; SAU-BODY-20 world proxy; ~170 cm tail reach |

**Universal rule:** extremes must PASS in combination with frame and composition extremes, not only alone (SA L3962; MF L251).

## 8. Equal-height cross-population boundary testing

**The rule:** "Every equal-height comparison uses a stature valid for every participant" (GR L150; applied in DU L337's 150 → 152 correction). Where no stature is shared, comparison uses **matched-scale / normalized display, diagnostic only, "not a valid in-world body state"** (SR-COMP-04; UFCA §16).

**Canonical equal-height statures:**

| Pair | Stature | Source |
|---|---|---|
| MF–SK | 190 cm; overlap 183–203 | SK L292, L58–65 |
| MF–DU | ~150–152 cm | DU L72 |
| MF–DU–SG | ~152 cm | DU L145, L337 |
| PK–DU | ~122 cm (single height) | PK L29; SR-COMP-03 |
| CG–PK | ~91 and ~107 cm | SR-COMP-01 / 02; COG-BODY-09A, -27 |
| CG–DU | **no overlap**: normalized (COG-BODY-10) and actual-height beside (COG-BODY-10A ~107 vs ~122) | — |
| FN–AE | ~190 cm | AE L169 |
| GR–MF / SG / FN / VA / AE / SK | 198–203 / 198–208 / 198–211 / 198–203 / 198–221 / 198–229 | GR L152–160 |
| GR–VA pigmentation boundary | 198–203 | GR L600 |
| GO–SK | 208–229; **AD-1** 208 cm Gorrund vs Broad Skarn through 229 | GO L271 |
| GO–GR | 208–239 | GO L678 |
| GO–AE / FN / SG | ~208–221 / ~208–211 / ~208 | GO L679–681 |
| GO–DU, GR–DU | **no equal height**: conceptual and matched-display tests | GO L723–733; GR L712 |
| SA–others | "equal / normalized standing height" with no cm given (SILENT) | SAU-BODY-03, -21, -22 |
| HV | Equal-height tests vs all six sources at overlapping heights | L147 |

**Generic body harness (proposed, AD-C14):** every population pair runs at a stature valid for both where one exists, and at matched-scale otherwise. Race tests stay authoritative. The pairwise coverage matrix is in UCCA-09 §3.

## 9. Proposed measurement items (RM-UB, semantics only)

| ID | Semantic variable | Feeds | Dependency |
|---|---|---|---|
| RM-UB-01 | Per-race segment-share and within-limb distribution bands (torso/axial, neck, arm, upper-arm/forearm, leg, femur/lower-leg, hand, palm/finger, foot), absolute and proportional | Slot 2 CLAMP bands | Extends RM-LR / SR / OT; needs approved reference meshes per race and frame |
| RM-UB-02 | Per-race allometric response of head, hands, feet, joints, bone breadth and torso breadth/depth to stature | DER absolutes at any stature | Min / ref / max reference meshes per race |
| RM-UB-03 | Joint-scale and long-bone robusticity envelopes, including race hard minimums | Slot 3 bounds | Reference meshes |
| RM-UB-04 | Saurin reachable tail-length cap as a continuous function of resolved frame and composition, through the canon points (~78 % / 80 % / ~72 % H) | Tail CLAMP | SA reference variants |

**Not a measurement item:** Halvren stature tail limits and frequencies are **biological OPEN** (HV L481, L490). They need authoring, not measurement, before tails can be exposed (AD-C3b).

— Claude

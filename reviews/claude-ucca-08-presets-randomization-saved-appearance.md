# UCCA-08: Presets, Randomization, Locks & Saved Appearance

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §12
**Status:** PROPOSAL for author review. **No serialization format is decided.**

## 1. Flows

| Mode | Flow | Canon |
|---|---|---|
| **Simple Mode** | Race → (Halvren: optional Lineage) → Starting Character preset → Confirm. The only canonically necessary conditional step is the Halvren lineage, and that step is optional: Simple Mode never requires genetics (HV L58). An optional whole-character shuffle uses the same generator | PR L8; MF L227; PK L1398; CG L2915; SA L2246 |
| **Advanced Mode** | Race → Starting Character / preset → Customize (all UCCA slots + UFCA) → Confirm | PR L9 |

**Both modes write one appearance record.** Switching modes keeps the appearance (MF L49; AE L435; VA L478; SAU-CC-01).

## 2. Preset architecture

### Tiers found in canon, unified

All tiers are write-and-vanish operations (UCCA-03 P-1…P-5):

| Tier | Writes | Canon |
|---|---|---|
| Whole-character presets (race libraries) | All biological slots + optional presentation | MF L216–223; SK L259–268; SG L331–340; FN L320–329; AE L412–427; VA L461–474; HV A–M; DU L139; GR L259; GO L232, L562; PK L1384–1391; CG §192–193; SA §140 |
| Frame starting points (N/B/B) | Skeletal values only: Slot 3 (Saurin also hand/foot breadth and tail-base frame component, SA L4168) | UCCA-05 |
| Composition starting points (Lean / Athletic / Muscular / Heavy) | Slot 6 only | UCCA-06; AD-C5 |
| Presentation presets | Slot 14 only; never anatomy | SK L247; SG L301 |
| Surface presets (Saurin) | Slot 10 Natural only | SA L1953–1963 |
| Age starting points | Apparent Biological Age only | SA §131 |
| Tail neutral presets (Saurin) | Slot 5; silhouette diversity, not subraces | SA L223 |
| Face presets | UFCA slot 0 (closed) | — |

**Rules carried:**

| Rule | Canon |
|---|---|
| Ordinary valid appearance records; **no preset-only anatomy, morphs or geometry** | PR L10; every race |
| Never castes, subraces, classes, cultures or genealogy. Halvren I–M stay internal labels; "choosing a preset never implies genealogy" | HV L347, L467 |
| No stereotype bundles: green brute, classic ogre, fair+freckled+curly halfling, cute Cogling, pretty High Elf, charcoal/white/violet Vael, swamp/desert/warrior Saurin, round halfling, giant-beard Durrim | GR L564; GO L562; PK L1415–1421; CG L2008–2015; AE L520; VA L490; SA L1963; DU L222 |
| Each library includes neutral and minimum-stereotype individuals | GO L686; GR L717; CG §193; SA §140 |
| Pipkin's two tiers (frame presets vs coverage presets, relationship unstated, PK notes) are reconciled here: frame presets = Slot 3 operations; coverage presets = whole-character presets | — |

## 3. Randomization

| Rule | Architecture | Canon |
|---|---|---|
| Domains | **Biological / Presentation / Acquired-History** are separate passes. Presentation and Acquired never rewrite anatomy. Acquired never creates major tail, rostral or jaw loss | SA §141–142A; PK L635–637; CG L2958–2962; HV L351 |
| Pipeline | Race envelope (Halvren B) → **drivers** from weighted SOFT distributions (stature, frame, composition, head proportions where bound, tail length, display family) → **dependents** in coupled bands (tail base ~length^1.18; segment shares; E/B centres by sex) → validators: **reject FAIL and resample; never roll everything and repair** → batch diversity → presentation pass | SA §264 L4257; SK L284; GO L562; GR L564; UFCA §13 |
| Strength | **Subtle / Diverse / Extreme** as defined in UFCA_V1 §14. Extreme samples **valid tails only**. Shared by face and body: one strength setting for the whole character | UFCA §14 |
| Weighting | Internal Very Common / Common / Uncommon / Rare. **Interim weights are never canon** | PK L1411; CG L2966; UFCA §15 |
| Rare phenotypes | Reachable at low frequency; **always manually creatable**; Advanced Mode keeps the full valid range | SG L228, L344; SA L2197, L3714 |
| Sex | Shifts only race-canon soft centres. **Saurin: only four centres; every other driver sampled identically** | SA L4257; R-SEX |
| Halvren | Genealogy (if set) conditions B; many phenotypes per history; **no 50/50 default**; source protection on body and face | HV L351, L481; UFCA §11 |
| Pipkin / Cogling | Anti-juvenile packages banned | PK L1415; CG L1050 |

## 4. Selective randomization and locks

**Scopes (canon union):**
- whole character;
- body only;
- face only (preserving body, height and age);
- surface only;
- hair only;
- eyes only;
- composition only (preserving frame and height);
- presentation only;
- acquired only;
- tail only (Saurin);
- pattern only (Saurin);
- age presentation only.

Sources: SK L280; SG L402; AE L460; VA L486; PK L1425–1434; CG L2972–2979; SA §143.

**Locks:**
- Any attribute, region or slot can be locked. Saurin lock groups: stature, frame, composition, tail, head, rostrum, eyes, pigmentation, pattern, display, age biology, presentation; Acquired is locked independently (SA §144).
- **Locks are absolute.**
- **A locked child can never force an invalid parent.** If no valid solution exists, the system preserves the lock and reports; it never silently changes the locked value (CG L2983–2989; SA L2362; PR L38).
- **Out-of-scope values beat in-scope samples** (UFCA §13).

## 5. Seeded reproducibility

A design requirement (SG L457; FN L515; AE L464; HV L351):
- seed + generator version + distribution version + scope + locks reproduce a **generation event**;
- **saved characters store resolved values, not seeds**.

## 6. Saved / reusable appearance (conceptual completeness)

### 6.1 Proposed conceptual domains of the appearance record (AD-C13)

| # | Domain | Contents | Canon |
|---|---|---|---|
| 1 | Schema / version | Version id; migration path | MF L261; register L49, L456; PK L1438–1444 |
| 2 | Race | Population id | — |
| 3 | Lineage (Halvren, optional) | Genealogy record (A). **B is not stored, it is recomputed** | HV L70, L394, L467 |
| 4 | Sex-related anatomy | Selection | — |
| 5 | Biological Anatomy | Stature; segment shares and distributions; hands/feet set; Saurin tail set; Saurin E/B; head-to-body (SA); capacity; Natural surface (pigment set, marks, scale fields, pattern, claw keratin); hair biology (scalp, body); iris and ocular per UFCA; display family and parameters | SA L2537–2552; HV L394; CG L2993–3005 |
| 6 | Skeletal Frame | Resolved breadth / depth / joint / robusticity values (no frame label dependency) | UCCA-05 |
| 7 | Physical Composition | Current muscularity, regional offsets, fat amount, fat distribution | — |
| 8 | Face | All UFCA DIR values and facial asymmetry offsets | UFCA_V1 |
| 9 | Age | Chronological Age; Apparent Biological Age; Age Presentation | PR L16 |
| 10 | Natural body asymmetry | Offsets (where bound) | — |
| 11 | Environmental layer | Per AD-C9 (persistent vs transient) | — |
| 12 | Acquired history | Scars, damage, wear, as individual-history state | SA L2537–2552 |
| 13 | Presentation | Styling, grooming, Applied markings, cosmetics, clothing/gear preview selection, body-language presentation, culture / birthplace / background selections | — |
| 14 | Optional provenance | Starting preset ids, generation seed/version. **Non-driving; never required to reproduce the character** | — |

### 6.2 Rules

| # | Rule | Canon |
|---|---|---|
| S-1 | **Resolved values, not preset references.** A reusable appearance never depends on a temporary preset identifier (order §12) | — |
| S-2 | **Semantic, not mesh.** Store stable conceptual traits, not morph or mesh weights | PK L1442; CG L2995 |
| S-3 | Derived values (absolute dimensions, B envelopes, visible mass, Resting Alignment, tail base when DER) are **recomputed** on load from stored values and the current race rules | — |
| S-4 | **Migration, not reinterpretation.** A schema change migrates. A rule change that makes a stored value invalid → CONSTRAIN on load, reported, never silent | — |
| S-5 | **Cross-race reuse** only through semantic re-mapping and race-valid reinterpretation, never raw value copying. Not required in v1 | CG §198 |
| S-6 | **NPC parity:** NPCs, presets, randomized and player characters use the same record and validators. Narrative exceptions are flagged non-baseline and excluded from generation | DU L508; GR L687; GO L693; PK L1405; CG L3017; SA L2556–2564 |
| S-7 | **Lighting-invariant storage;** pupil dilation and other responsive states are never stored | SAU-CC-20, -28 |

### 6.3 Gap audit: current prototype vs required record

| Required domain | Prototype (level 6) | Gap |
|---|---|---|
| Frame | "Frame" = Manny/Quinn switch (plan L82) | Wrong concept (UCCA-05 §5); needs resolved skeletal values |
| Height | Height **step** at uniform scale ±7.5 % (plan L83–85) | Needs stature in cm + proportional values |
| Composition | **Absent** | Missing |
| Face | **Absent** | Missing (UFCA record) |
| Skin / surface | "Two colors and finish" (plan L83) | Missing the multidimensional pigment set, four layers, Saurin scales and pattern |
| Hair | Absent | Missing |
| Markings / Applied | Absent | Missing |
| Age | Absent; chronological age needs its own value (audit 01 L21) | Missing |
| Sex-related anatomy | Implicit in Manny/Quinn | Missing as its own field |
| Genealogy | "No genealogy, expression or ancestry data" (audit 07 L7) | Missing (Halvren) |
| Tail | Absent | Missing (Saurin) |
| Locks / strength / distributions | Not in the record (audit 06 L20) | Creator-session state, not appearance data (proposal) |
| Schema / version | "Serialization isn't redesigned yet" (plan L83) | Missing |

**Conclusion:** every listed system is **representable in the conceptual record** above. **No serialization format is decided** (order §12).

— Claude

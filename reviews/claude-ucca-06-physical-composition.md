# UCCA-06: Physical Composition Architecture

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §10
**Status:** PROPOSAL for author review.

## 1. The five-way separation

**capacity ≠ current muscularity ≠ fat amount ≠ fat distribution ≠ skeletal frame**

| Concept | Layer | Class | Canon |
|---|---|---|---|
| **Muscular Development Capacity** | Biological Anatomy | Stored value; exposure per AD-C4 | PR L67; SK L26, L80; HV L447; GR L72; CG L314–320; SA L358 |
| **Current Muscularity** (overall + regional) | Physical Composition | DIR | PR L14; SK L102; MF L53, L77 |
| **Body-Fat Amount** | Physical Composition | DIR | PR L14; MF L282 |
| **Body-Fat Distribution** (regional) | Physical Composition | DIR, separate from amount ("distribution never substitutes for amount") | MF L282; CG L856; SA L2502 |
| **Skeletal Frame** | Skeletal Frame | Slot 3 (UCCA-05) | PR L12–13 |
| Soft-tissue fullness, limb circumference, visible mass | — | **DER** (bone + muscle + fat). Mass is never a slider | GR L251; SK L106; SG L169; MF L31 |

**Hard rules:**
- Composition never edits the skeleton. Thoracic depth is skeletal, never faked by fat or muscle (VA L114; DU L103; GO L181).
- Pelvic breadth is never fat (PK L182).
- Frame never edits composition (UCCA-05).

## 2. Muscular Development Capacity (AD-C4: proposal + options)

**Canon:**
- Capacity is the *biological range a body can support*; Current Muscularity is the *present state* (PR L67).
- Population capacity tendencies:

| Race | Capacity canon |
|---|---|
| SK | Higher (L26) |
| HV | Skarn ancestry shifts the distribution or upper potential, never current build (L447) |
| GR | **OPEN** (L72) |
| GO | **OPEN** (L82) |
| PK | **OPEN**, "never lowered because Pipkin are small" (L180; OPEN L72, L1541) |
| CG | Fine bones don't require low capacity (L320) |
| SA | Listed as a variation axis (L358) |

**Proposal:**
- Capacity is a stored Biological Anatomy value that sets the **valid ceiling** for Current Muscularity (CLAMP).
- **Option (a), recommended:** expose capacity as a Detailed control only for races whose canon names it as a variation axis or required representable variable (SA L358; CG §69, which "does not finalize creator-facing sliders"). For all others it is a **VAL ceiling** drawn from the race distribution. Where that distribution is OPEN (GR, GO, PK), the ceiling is the broad first-pass range with no invented shift.
- **Option (b):** expose capacity everywhere in Detailed controls.
- **Option (c):** never expose it; always VAL.

**Firewall:** visual muscularity and capacity never imply gameplay strength (order §10; SA L2631; PK L1018–1039; MF L92 "starts cosmetic").

## 3. Regional composition

| Item | Canon |
|---|---|
| Regional muscle | **OFFSETS on overall muscularity** ("regional values stay tied to overall muscularity so no single group becomes implausible", SK L102) |
| Race regional-muscle group lists | SK neck/traps … calves (L102); DU (L54); GR (L251); GO (L228); PK (L180); SA (limbs, girdle, epaxial neck/dorsal trunk, thigh, posterior shank, proximal–mid tail; joints, hands and feet excluded; L4170) |
| Regional fat distribution | Distribution controls per race. SA regions: ventral-abdominal strongest, flank/hip, graded proximal caudal, minor gular, light general (L4170). Distribution tendencies are OPEN everywhere |
| Proposed universal group set | A **superset navigation list** (neck, shoulders, upper arm, forearm, chest, upper back, core, glutes/hips, thigh, calf/shank; Saurin: tail). Each race binds only the groups its canon names. Saurin **excludes** human chest-block, six-pack and buttock morphology (L4170) |

**Prohibitions carried:**
- no thin-to-heavy slider (MF L68);
- no weight slider (SK L106; SG L169);
- no uniform inflation (SA L2504);
- no stereotype physique packages (PK L184: never Broad → muscular → high fat);
- no "round halfling" (PK);
- no "bodybuilder troll" (GR L11);
- no "ogre belly" (GO L186).

## 4. The "Athletic" starting preset (AD-C5)

**Canon:**
- MF universal amendment: "Athletic **may initialize** muscularity, body-fat amount and distribution, regional muscle and other non-skeletal parameters. **It never automatically changes skeletal shoulder breadth, ribcage or pelvic dimensions, limb-bone proportions, joint scale**" (L281; L5 removes Athletic from frames).
- Composition presets Lean / Athletic / Muscular / Heavy / Custom (MF L5, L27).

**Proposal:**
- **Composition starting presets** (Lean, Athletic, Muscular, Heavy) exist as **write-and-vanish operations on Slot 6 only**, with race-specific target values.
  - They write current muscularity, fat amount, fat distribution and regional muscle offsets.
  - They never write the skeleton, capacity, stature or sex-related tissue.
- After writing, there is **no Athletic state**. Editing any composition value leaves an ordinary composition (UCCA-03 P-1…P-5).
- "Custom" is not a preset. It is the absence of one.
- Whether these four become universal (canon is MF only, "proposed" elsewhere) is **AD-C5**.

## 5. Population-specific composition systems

### 5.1 Saurin E/B (§263, closed canon)

| Item | Canon |
|---|---|
| **E** | Coelomic body-wall fullness |
| **B** | Ventral fullness: one continuous midline field. Never paired masses |
| Layer | Biological Anatomy tissue tendencies (L4227–4228) |
| Never | **Folded into the fat control** (L4232; §23 L385; §153 L2508) |
| Home | Slot 7 Sex-Related Anatomy (UCCA-02) |
| Centres | Male 0. Female: E 2.0 cm; B 1.6 cm, **ceiling 3.0 cm** |
| Bounds | Identical for both sexes; **overlap mandatory**. A male may sit at the female centre and vice versa |
| Guards | B counts against the thoracic depth/width ≤ 1.00 guard → CONSTRAIN cases: Narrow + B 3.0 → ~2.1 cm; Narrow + high fat + B 1.6 → ~1.5 cm (L4246–4247). Persists at low fat; stacks with high fat under the guards; deforms scale fields smoothly (edge stretch ≤ 1.20 at the 99th percentile; L4253) |
| **Anti-hourglass** | "A fuller, continuous coelomic body wall and ventral organization, **not a narrower waist**" (L4219). Paired breasts were evaluated and **rejected**; no human hip flare, paired buttocks or gluteal cleft (L4211, L4240) |
| Validators (proposed for UCCA) | **No Saurin composition or sex-related value may produce:** waist narrowing as a sex signal; paired ventral masses; hip flare; buttocks. The B ceiling holds. "Sex is not reliably readable at gameplay distance; anatomy is not exaggerated to force it" (L4234) |
| Tail | Tail muscularity and caudal fat **follow Composition** (§256.6–7). Caudal fat is graded through the proximal half; root-concentrated fat FAILs |

### 5.2 Other races

No population-specific tissue system exists in canon.

**Related bans carried as validators:**
- Cogling thorax is not "an hourglass device" (L669); waist is not a cinch point (L677).
- Pipkin pelvis is never "one hourglass silhouette" or wide hips from fat (L149, L182).

## 6. Composition × everything (validator families, tier I)

| Validator family | Canon |
|---|---|
| Every race's composition stress sets | MF L250; FN L349; AE L159, L472; VA L521; HV-36…43; DU L73, L146–147; GR-BODY-06…09, 15–16; GOR-BODY-06…11, 16–18; PIP-BODY-06…09, 20–23; COG-BODY-04…06, 22–24; SAU-BODY-06…08; SAU-CC-09, -23 |
| Identity must survive composition neutralization | Low-muscle and low-fat reveal the skeleton; high fat softens without erasing identity (GO L720–721; PK L180; DU L135) |
| Composition × age | Age redistributes composition as OFFSETS, never a frailty package (UCCA-07) |

— Claude

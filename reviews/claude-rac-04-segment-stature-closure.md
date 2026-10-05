# RAC-04: Segment & Stature Relationship Closure Review

**Author:** Claude
**Order:** `reviews/chatgpt-reference-anatomy-closure-phase1-order.md` §3 (RAC-04)
**Status:** PROPOSAL. Evidence: `reviews/rac-evidence/A2-segments-limbs-head.md`.
**Rule:** no RM-UB-01/02 value is set. This document turns canon directions into **constraints the measurements must satisfy**. A measured reference that violates one of them FAILs and is corrected; the constraint is not weakened (RMQ rule 3).

## 1. The baseline problem

Most directional statements in the roster are "**than Marchfolk**". Marchfolk canon gives the stature envelope (147 / 173 / 203 cm, MF L21) and relationship rules (MF L31) but **no segment shares, no arm length control, no head share** (MF L44 evidence note). Therefore:
- Marchfolk segment values are **C**: they can only come from an accepted Marchfolk ARM (RAC-02).
- That ARM must be **accepted first**; every "vs MF" constraint below is evaluated against it.
- Proposed queue item **RM-UB-07** (RAC-03) carries this.

## 2. Constraint table (directional, canon-derived)

Notation: ">" means "trends greater than, at matched stature, as a population tendency". Every row is a tendency, never a requirement on each individual, unless marked **hard**.

### 2.1 Torso / leg / arm contribution to stature

| Race | Torso share | Leg share | Arm | Canon |
|---|---|---|---|---|
| SK | > MF (slight) | not short-legged; long-legged SK valid | silent | SK L75, L86 |
| SG | < MF (slight) | > MF (slight) | forearm, hand, finger longer than MF (slight) | SG L137–139 |
| FN | < MF | > MF; lower-leg share slightly greater | longer arms; greater forearm share | FN L50–52, L121, L123 |
| AE | > FN | long, **even** thigh/lower-leg elongation | even upper-arm/forearm elongation | AE L48, L56, L58, L124 |
| VA | > FN | < FN and AE | less elongated than FN/AE; balanced segments | VA L35, L44, L46 |
| DU | > MF at equal height | < MF (lower limb contribution) | shorter in absolute and relative terms; no fixed ratio | DU L38, L97, L113, L119 |
| GR | < MF and SK | > MF and SK; lower leg may be emphasized | upper arm, forearm and **arm span > MF and SK** | GR L198, L213, L215, L223, L227, L310 |
| GO | > GR | < GR, never short-legged | arm and span < GR; "long-armed" banned as shorthand | GO L169, L196, L200, L281 |
| PK | < MF (modest; central trunk) | > DU at matched height; **never automatically above ordinary human adult proportions** | no Grask-like forearm; **unusual span not a trait** | PK L56, L137, L166 |
| CG | ≈ MF | total ≈ MF; within-leg: femur share ↓, lower-leg share ↑ | total ≈ MF; within-arm: upper arm ↓, forearm ↑, hand ↑, fingers ↑ | CG L100, L139–145, L558, L572–575, L620–624 |
| SA | head/thoracic share pays for a longer lower axial trunk; neck share ≈ MF | moderate-to-long, never forced short | moderate; modest forearm emphasis | SA L258, L297–298, L970 |
| HV | inherits per segment; never a midpoint | per segment | per segment | HV L101, L126–131 |

### 2.1a Neck contribution

Directions: AE > FN and VA in relative neck contribution (ECR L320; VA L123 relative, not absolute); GR moderate-to-long relative to DU and SK (GR L43); DU short (DU L21, L107); GO moderate with high integration (GO L46); SA ≈ MF (SA L970); PK adult, neither DU-compact nor AE-long (PK L48); CG neither thin nor thick (CG L270, L723); SK structural neck base, not length (SK L23). Detail and editorial items: RAC-03.

### 2.2 Head-to-stature (direction only)

| Race | Direction | Class |
|---|---|---|
| DU, PK, CG | Somewhat > MF **as allometry only**; never oversized; never a maturity or identity mechanism (PK L201: **hard** ban on using it to separate adult from child) | **B** |
| SA | Head-**height** share "near to modestly below" MF (§55); the §258 bound is on head **length** ÷ stature (0.156–0.184) | A clarification (§4) |
| GR, GO | No ratio locked; tiny-head giant and oversized head banned (GR L433; GO L299, L408) | **C** |
| SK | "Body scale sets head-to-body proportion", pending validation (SK L179) | **C** |
| MF, SG, FN, AE, VA, HV | Silent | **C** |

### 2.3 Hands and feet

| Race | Direction | Canon |
|---|---|---|
| SK | Larger absolute hands and feet | SK L25, L79; HV L454 |
| SG | Longer hands and fingers, slightly narrower hands | SG L138, L156 |
| FN | Longer palms and fingers, narrower hands and wrists; longer, narrower feet | FN L122, L124 |
| AE | Long hands, palms, fingers, narrow breadth; feet longer, moderate-to-narrow | AE L153, L155 |
| VA | Broader palm than FN/AE; broader feet; sturdier transitions | VA L139, L141 |
| DU | Hand size relative to stature > MF; palm share provisionally greater; feet large for stature, broad | DU L115, L121 |
| GR | Finger:palm > MF and SK; reach never mainly from hands; foot never scales linearly with height | GR L229, L235, L245 |
| GO | Palm breadth and depth substantial relative to hand length; feet never exaggerated to signal size | GO L210, L216 |
| PK | Hands moderate for stature; feet modestly larger relative to height as a tendency, not the identifier | PK L58, L64, L178 |
| CG | Hands larger share of arm; fingers long relative to palm; feet moderate | CG L141–142, L593, L630–632 |
| SA | Moderately elongated fingers; longer forefoot/toes than MF; claws (RAC-10) | SA L284, L310 |

## 3. Explicit cases required by the order

| Case | Disposition | Class |
|---|---|---|
| **Grask arm span** | Direction locked twice: > MF and SK (GR L223); GR > GO (GO L200). Span is **DER** from shoulder breadth and segment lengths, never a slider (GR L225; UCCA L80). Ratio from RM-LR-01 | **B** |
| **Pipkin arm span** | Authorable now: "**No racial arm-span tendency.** Span is DER from Pipkin shoulder and segment anatomy; neither Grask-extended nor shortened" (PK L166 already says "unusual arm span isn't a Pipkin trait") | **A** (number C via RM-UB-01) |
| **Pipkin trunk share (T-2)** | Constraints only. (1) Central trunk share < MF (modest). (2) Absorbed by limb and pelvic vertical contribution, **not by head enlargement** (PK L137). (3) Legs never automatically exceed ordinary human adult proportions (PK L166). (4) Head share may be somewhat > MF **only as allometry**; a deliberate head increase may not pay for the trunk deficit (PK L33, L201, L205). (5) **Pipkin absorption is a CLAMP-band relationship, not a REDISTRIBUTE tool** (UCCA L103 keeps Saurin stature accounting as the only REDISTRIBUTE). The numeric split stays deferred to RM-SR-01 / RM-UB-01; **no winner is invented** | Constraints **A**; split **C** |
| **Cogling distal redistribution** | Fully directional: total arm and leg ≈ MF; within-limb distal shift; proximal segments accommodate; palm and finger never one control (CG L145, L599). Magnitudes RM-SR-02. Validators COG-BODY-19/20/21 already exist | **B** |
| **Fenn / Aelari / Vael** | Where elongation sits: FN extremities, AE distributed continuously, VA compact with structural transitions (AE L114–115; VA L27; ECR L33). AE "Fenn may lean more on forearm length" stays **provisional** (AE L56) | **B** |
| **Sagekin vs Marchfolk** | "Slight" directions in §2.1; Sagekin are "the long-limbed end of fully human variation" (FN L138); never elven in limb proportion (SG L435) | **B** (RM-OT-01) |
| **Skarn vs Marchfolk** | Torso share > MF (slight); larger absolute hands and feet; leg share not reduced as a rule; arm span silent. **Proposed A:** "no racial arm-span tendency beyond what larger stature and shoulder breadth produce" | **B** (span **A**) |
| **Gorrund limb presence** | (1) GO torso share > GR; GO leg, arm and span < GR. (2) **AD-3 floor:** GR-BODY-10 (shortest-limbed valid Grask) stays above the Gorrund "slightly more limb-present" family at matched height (GR L259, L715; GO L232). (3) Reciprocal: low-breadth GO vs Broad GR holds through lower limb contribution, axial contribution and ALPC (GO L244). (4) **GO vs SK limb/span direction is undetermined by design** (AD-4, GO L675); GO vs MF is canon silence. Neither is authored here | AD-3 numeric **C** (RM-LR-04); GO–SK **left undetermined** |
| **Saurin stature accounting** | Head, neck, thorax, lower trunk and legs sum to stature, tail excluded (SA L64, L1263); the lower trunk is paid for by reduced head-height and thoracic share, not by shortening legs (SA L970); §258 bounds govern creator variation (T-1) | Closed; one metric clarification (§4) |

## 4. Clarifications authorable now (class A)

| # | Clarification | Basis |
|---|---|---|
| S-1 | **Saurin head metric:** §55 speaks of head-**height** share (HH ÷ H); §258 bounds head-**length** ÷ H (HL, includes the rostrum). They measure different things, which is why T-1 found no conflict. State this in the spec | r3 L78 defines both HSR forms |
| S-2 | **Cogling head size "roughly 11–13 cm"** (CG L522, L1583, L3172) does not say whether it is head height or length. The author should name the dimension | Ambiguity only |
| S-3 | **Durrim head share** has an authored direction (DU L21) but Durrim is missing from the RM-CF-10 HSR scope (r3 L78; RMQ L59). Add Durrim to RM-CF-10 / RM-SR-04 | Queue scope |
| S-4 | **Pipkin arm span** as in §3 | PK L166 |
| S-5 | **Skarn arm span** as in §3 | SK silent; avoids an invented tendency |
| S-6 | **Cogling arm span** appears only in the historical Part 1 list (CG L514). State: "span DER; total arm ≈ MF; no racial span tendency stated" | CG L558; UCCA L80 |

## 5. Constraints the RM-UB-01 / RM-UB-02 measurements must satisfy

1. Every directional row in §2 holds between the measured ARMs at matched stature.
2. **No-uniform-scale test** (UCCA L332): min / ref / max variants of one race are never related by a single factor across head, hands, feet and joints.
3. **Allometry direction:** head, hands, feet and joints do not change by the stature percentage (CG L887–889; GO L224); exact response is RM-UB-02.
4. **Anti-juvenile hard bans** (UCCA L272; PK L33, L201; CG L732–734, L1051) hold at each race's minimum stature.
5. **AD-3 floor** (GR-BODY-10 > GO limb-present family) and AD-2 (GR-BODY-10 vs Skarn carriers, GR L714) hold.
6. Saurin stature accounting (SAU-FACE-22) holds at 168 / 188 / 208 cm.
7. Durrim–Marchfolk–Sagekin comparison at **152 cm** (T-6) holds.

## 6. Proposed author decisions

| ID | Decision |
|---|---|
| AD-R10 | Adopt the §2 constraint tables as the directional constraints for RM-UB-01/02 (no numbers) |
| AD-R11 | Pipkin, Skarn and Cogling arm span: "no racial span tendency; DER" (S-4, S-5, S-6) |
| AD-R12 | Pipkin T-2 constraints (§3) adopted; split stays C |
| AD-R13 | Clarifications S-1 (Saurin head metric) and S-3 (Durrim in RM-CF-10); author to answer S-2 (Cogling head dimension) |

**Not authored:** Gorrund vs Skarn limb and span direction (undetermined by design, AD-4); Gorrund vs Marchfolk (silent).

**Neck contribution** (listed in the order under RAC-04) is handled in RAC-03 §2 and editorial items E-3 (Pipkin) and E-4 (Fenn); numbers via RM-UB-01 / RM-OT-02.

— Claude

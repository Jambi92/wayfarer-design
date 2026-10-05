# UCCA-11: Phase 1 Architecture Audit

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §15
**Scope:** UCCA-01…10 audited against the 13 race specs, `decisions/PROJECT_RULES.md` and closed `decisions/UFCA_V1.md`.
**Status:** AUDIT for author review. **UCCA is not canon.** No race spec, UFCA_V1, PROJECT_RULES or STATUS was edited.

## 1. Verdict

**No stop condition was met** (order §18):
- No two approved population requirements were found that cannot coexist in one architecture. Every population-specific system (Saurin tail and E/B, Halvren genealogy, Grask/Gorrund breadth-only frame, Cogling AC-9 tendencies) fits as a binding or conditional slot.
- No approved biology had to change.
- No OPEN biological question blocks the architecture: each OPEN item is carried as unnumbered, hidden or validator-only (UCCA-10).
- No frozen Pass 2 or closed UFCA rule is violated (Q20).

**Twelve canon tensions** (UCCA-10 §5, T-1…T-12) are carried, not resolved. **Eighteen author decisions** (AD-C1…AD-C17 plus AD-C3b) are required before canonicalization.

## 2. The 20 questions

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | Does every approved non-facial creator requirement have a home? | **Yes.** Every body control-list item in canon has a slot and a disposition (Appendix A). Silences are routed to hidden-pending-decision bindings, not dropped (body hair AD-C7; natural asymmetry AD-C8; neck AD-C10) | UCCA-02 §2; Appendix A |
| 2 | Did universalization weaken any population's positive body identity? | **No.** Every population's positive identity (UCCA-01 §1) is carried as Tier A/B/E validators; race tests stay authoritative. Superset lists (regional muscle groups) bind only what each race names; Saurin excludes human chest-block, six-pack and buttock morphology | UCCA-06 §3; UCCA-09 |
| 3 | Did any Pass 1 requirement disappear without disposition? | **No** found. The audit agent's completeness check is in §4 | Appendix A; §4 |
| 4 | Did any OPEN item get silently resolved? | **No.** OPEN items stay OPEN: segment numbers, head-to-stature, pelvic morphology, capacity distributions, body hair (DU/GR/GO), Halvren height tails, Saurin tail loss, thermoregulation, reproductive biology, lifecycle. One item the order lists, Saurin partial garment coverage, has its **permission already resolved in canon** (SA L620, L3549); its construction and coverage extent stay OPEN (L2050, L4067). Neither part is resolved by UCCA | UCCA-10 §2–§3 |
| 5 | Did any diagnostic measurement become a player control? | **No.** Head-to-stature stays VAL/DIAG except where Saurin canon makes it a control (§258 ±8 %). Matched-scale comparisons are diagnostic only. Saurin's reachable tail cap is a CLAMP, not a control | UCCA-03; UCCA-04 |
| 6 | Did any control become hidden ancestry / culture / personality / gameplay? | **No.** Presets are write-and-vanish (P-1…P-5); provenance is non-driving; frame never encodes ancestry (HV L137); presentation presets never write anatomy; capacity and muscularity never imply strength; legacy gameplay traits firewalled | UCCA-03 §4; UCCA-05; UCCA-06 §2; UCCA-10 §2 |
| 7 | Are Simple and Advanced both fully supported? | **Yes.** Simple: Race → (optional Halvren lineage) → preset → Confirm. Advanced: all slots. One record for both; switching keeps the appearance | UCCA-02 §5; UCCA-08 §1 |
| 8 | Are presets legitimate outputs? | **Yes.** All tiers produce ordinary valid records; no preset-only anatomy; libraries include neutral and minimum-stereotype individuals | UCCA-08 §2 |
| 9 | Are saved/reusable appearances conceptually complete? | **Yes, conceptually.** Domains 1–14 cover every listed system; the prototype gap is large (UCCA-08 §6.3). No format decided | UCCA-08 §6 |
| 10 | Is uniform scaling eliminated as the design model? | **Yes.** Stature is the only absolute size control; other sizes are race-relative with allometric DER absolutes (AD-C3; RM-UB-02). Proposed no-uniform-scale validator. The prototype's ±7.5 % uniform scale is level-6 and superseded at design level | UCCA-03; UCCA-04; UCCA-09 H |
| 11 | Are Frame and Composition genuinely independent? | **Yes.** Frame writes only skeletal values (Slot 3; for Saurin also hand/foot breadth in Slot 4 and the tail-base frame component in Slot 5, SA L4168), never composition; composition presets write only Slot 6; Athletic never writes the skeleton (MF L281). Proposed factorial and Athletic write tests | UCCA-05; UCCA-06 §4; UCCA-09 I |
| 12 | Is height relationship-aware rather than whole-body scale? | **Yes.** Segment shares, allometry and race CLAMP bands; Saurin stature accounting is the only REDISTRIBUTE | UCCA-04 |
| 13 | Are R-SEX and age separation preserved? | **Yes.** Sex selection shifts only race-canon soft centres and never moves stored values (AD-C6). Saurin: only the four §263 centres. One Apparent Biological Age driver; Chronological Age is character data; Age Presentation is Slot 14; age firewalls carried | UCCA-03; UCCA-07 §3 |
| 14 | Is Halvren supported without a percentage body slider? | **Yes.** Genealogy (A) → recomputed constraints (B) → phenotype (C). Lineage is optional, in Slot 0 only; no Elf Percentage / Elf Gracility; no 50/50 default. **Caveat:** Halvren stature tail limits are OPEN and canon forbids hard clipping into 152–213 (HV L481); the architecture carries tails through envelope B, but the numbers must be authored (AD-C3b, T-12) | UCCA-02 §4; UCCA-04 |
| 15 | Is Saurin supported without humanizing its body architecture? | **Yes.** Conditional Tail slot (no on/off); E/B in Slot 7, never under fat; anti-hourglass validators; Saurin muscle and fat regions only; no mammalian hair; scale fields with no global scale-size control | UCCA-02; UCCA-06 §5.1; UCCA-07 |
| 16 | Does the body architecture integrate cleanly with closed UFCA? | **Yes.** Face routes to UFCA unchanged; one age driver (UFCA slot 14 = UCCA slot 11); scalp hair shared with UFCA slot 10; one randomization strength; UFCA machinery (classes, relations, N-levels, outcomes) reused; AD-U12 extended as AD-C17 | UCCA-02; UCCA-09 K |
| 17 | Are population-specific surface/hair systems preserved? | **Yes.** Saurin scale fields, pattern and claw keratin; Pipkin and Cogling body-hair canon; Grask/Gorrund hair colour ranges; never one Skin Colour slider | UCCA-07 |
| 18 | Are technical/UE5 decisions still deferred? | **Yes.** Mesh/morph/skeleton approach, Manny/Quinn asset fate, serialization, animation, equipment fit, first-person all IMPL | UCCA-05 §5; UCCA-10 §2 |
| 19 | What author decisions are required before canonicalization? | **AD-C1…AD-C17** (incl. AD-C3b) and the T-1…T-12 rulings | UCCA-10 §1, §5 |
| 20 | Did any proposed universal rule conflict with frozen Pass 2 or closed UFCA? | **No conflict found.** Checked: UFCA F-1 / G-1…G-5 (body adds no relationship tools; presets follow G-2); UFCA slot model unchanged; UFCA frequency vocabulary and strengths reused verbatim; Pass 2 RM queues carried unchanged; RM-UB are new items, not edits | UCCA-03; UCCA-10 §4 |

## 3. Proposed rules flagged for author acceptance

Every rule labelled "proposed" or "PROPOSAL" in UCCA-01…10 is flagged. The principal ones are AD-C1…AD-C17, rules P-1…P-5 (UCCA-03), S-1…S-7 (UCCA-08), the N-level body extension and the universal validators (UCCA-09), and RM-UB-01…04 (UCCA-04 §9).

## 4. Independent spot-check

An independent agent (no part in writing UCCA) audited UCCA-01…11 read-only. Its claims were re-checked against the specs before any fix.

| Check | Result |
|---|---|
| Canon unchanged | PASS: only new untracked review files; no diff under `specs/` or `decisions/` |
| Citations (~75 checked) | Mostly correct. **Fixed after verification:** equal-height rule quote is GR L150 (was DU L337); GR diversity L718 (was L716); GO neutralized recognition / minimum-stereotype / diversity L685 / L686 / L689 (each was 2 lines off); GO Vael-adjacent L549 (was L545); PK "never lowered" quote L180 (was L72); GR silhouette L98 (was L96); GR anti-caricature L717 and GO L686 in UCCA-08 (were L715 / L684); weak PK L68 cite for frame scope removed |
| Numbers | **No invented numbers.** All 13 stature ranges, Halvren 152–213, Saurin E/B, §256 bands, §258 bounds and reachable-tail points match canon |
| OPEN coverage | All 16 order §14 items present. **Fixed:** Saurin garment coverage now reads "permission resolved; construction and coverage extent OPEN" (SA L2050, L4067) |
| Appendix A | Complete for every listed control list. Fenn "waist" disposition aligned with MF |
| Overreach | **Fixed:** "frame writes only Slot 3" corrected for Saurin (SA L4168) in UCCA-03, -08, -11; AD-C4 wording no longer says CG "lists" capacity as a control (CG §69 does not finalize sliders); **AD-C3b** reworded: canon forbids hard clipping (HV L481), so a central-only range is at most labelled interim scope, added as T-12; T-6 relabelled (the 150/152 split is the DU–MF equal-height stature, not the Durrim minimum, which is 122 cm) |
| AD-C ids | All defined; UCCA-07 body-hair reference aligned with AD-C7 scope (DU/GR/GO stay biological OPEN). Counts corrected to 18 decisions and 12 tensions |

## Appendix A: disposition of every canon body control-list item

**Key to slots:** 2 Stature & Proportions · 3 Skeletal Frame · 4 Hands & Feet · 5 Tail · 6 Physical Composition · 7 Sex-Related Anatomy · 9 Hair & Display · 10 Skin & Integument · 11 Age · 12 Asymmetry & Acquired · 13 Body Language · 14 Presentation.

### A.1 Marchfolk (L53–54, L72–77; read with the universal amendments L280–288)

| Item | Disposition |
|---|---|
| Starting body frame | Slot 3 write operation (AD-C2) |
| Height | Slot 2 stature |
| Overall muscularity | Slot 6 Quick |
| Overall body-fat distribution | Slot 6: **amount and distribution**, per amendment §2 (L282: "incomplete wording, not a removal of amount") |
| General physique adjustments | Quick controls across Slots 3 and 6. **Vague in canon**; no new variable created |
| Individual regions, detailed proportions, regional muscle (Detailed) | Slots 2, 3, 6 Detailed |
| Shoulder width; chest width and depth | Slot 3 (shoulder/clavicular breadth, thoracic width and depth) |
| Neck thickness; arm, thigh, calf thickness | **DER circumference** (amendment §3, L283): skeletal component Slot 3, muscle and fat Slot 6. Not skeletal controls |
| Hand size; foot size | Slot 4 **multidimensional set** (amendment §4, L284: "one generic size scalar isn't sufficient") |
| Waist width; abdomen | Slot 3 thoracic/pelvic skeletal component + Slot 6 fat distribution |
| Torso length; leg length | Slot 2 segment shares |
| Hip width; pelvis proportions | Slot 3 pelvic width; pelvic morphology OPEN (UCCA-10 §3) |
| Regional muscle emphasis | Slot 6 regional offsets |

### A.2 Skarn (L86, L98, L102)

| Item | Disposition |
|---|---|
| Torso, leg and arm length | Slot 2 |
| Shoulder width; chest width and depth; hip and pelvis width | Slot 3 |
| Hand size and breadth; finger proportions; foot length and breadth | Slot 4 |
| Overall muscularity; regional emphasis (neck/traps … calves), tied to overall | Slot 6 overall + regional OFFSETS |

### A.3 Sagekin (L153–157)

| Item | Disposition |
|---|---|
| Torso length; waist length and transition | Slot 2 |
| Ribcage width and depth; shoulder width; pelvis width | Slot 3 |
| Arm length; upper-arm/forearm proportion; leg length; thigh/lower-leg proportion | Slot 2 |
| Hand length and breadth; finger proportion; foot length and breadth | Slot 4 |
| Thigh and calf thickness | DER circumference (Slots 3 + 6) |

### A.4 Fenn (L50–52, L121–124)

| Item | Disposition |
|---|---|
| Torso length | Slot 2 |
| Waist | Slot 2 (waist transition length) + Slots 3/6 (width), as MF |
| Ribcage width and depth; shoulder width; pelvis width | Slot 3 |
| Arm and leg total length; upper-arm/forearm; thigh/lower-leg proportion | Slot 2 |
| Arm/leg thickness; thigh and calf thickness/development; regional muscle | DER circumference; regional muscle Slot 6 |
| Overall hand scale; palm length and breadth; finger length and thickness (no per-finger) | Slot 4 |
| Foot length and breadth | Slot 4 |

### A.5 Aelari (L124, L152–155)

| Item | Disposition |
|---|---|
| Torso length; ribcage length; waist and lumbar length | Slot 2 |
| Ribcage width and depth; shoulder width; pelvic width | Slot 3 |
| Arm and leg lengths and segment proportions | Slot 2 |
| Thickness; regional muscle | DER; Slot 6 |
| Hand overall scale; palm length/breadth; finger-length proportion; finger thickness | Slot 4 |
| Foot length and breadth | Slot 4 |

### A.6 Vael (L121, L138–141)

| Item | Disposition |
|---|---|
| Torso length; ribcage length; waist and lumbar length | Slot 2 |
| Ribcage width and depth | Slot 3 |
| **Shoulder and pelvic width** (omitted from L121; frame changes them, L128) | Slot 3 via frame (T-10) |
| Arm and leg lengths; femur/lower-leg proportion | Slot 2 |
| Thickness; regional muscle | DER; Slot 6 |
| Hand scale; palm; finger-length proportion; finger thickness | Slot 4 |
| Foot length and breadth | Slot 4 |

### A.7 Cogling (§69, L1021–1044: "capable of representing at least")

| Item | Disposition |
|---|---|
| Height | Slot 2 |
| Frame; thoracic breadth/depth; pelvic breadth/depth/height; shoulder/clavicular breadth; joint breadth/depth; long-bone robusticity | Slot 3 (robusticity and joints as tendencies, AC-9) |
| Axial contribution; total arm and leg contribution; upper-arm/forearm and femur/lower-leg distribution | Slot 2 |
| Palm/hand contribution; finger length and internal distribution; foot dimensions | Slot 4 |
| Neck | Slot 2 (AD-C10: bound for CG, where canon names it) |
| Muscular-development capacity | Slot 6 (AD-C4 option a: Detailed control) |
| Current muscularity; body-fat amount; body-fat distribution | Slot 6 |
| Sex-related anatomy | Slot 7 |

### A.8 Saurin (§145–§153, §258)

| Item | Disposition |
|---|---|
| §145 tail: length, base dimensions, taper, segment/curvature, resting curvature, proximal/distal mass, dorsal keratin, tail pattern | Slot 5 (pattern also shown in Slot 10) |
| §145 tail muscularity | Follows Composition (§256.6); shown in Slot 5 as a regional offset of Slot 6 (T-4) |
| §146 rostrum controls | UFCA (closed) |
| §147–148 scale, pattern | Slot 10 |
| §149 eye | UFCA |
| §150 cranial display | UFCA slot 10; body continuation Slot 9 |
| §151 claws (length, curvature, width, thickness, tip, pigmentation) | Slot 4; claw keratin colour Slot 10 |
| §152–153 composition independence; fat amount vs distribution | Slot 6 |
| §258 head-to-body ±8 % | Slot 2 (Saurin only) |
| §258 neck length, neck depth | Slot 2 / Slot 3 |
| §258 thoracic depth and width; shoulder breadth; pelvic width | Slot 3 (frame ranges per §258) |
| §258 axial trunk length; arm and leg length | Slot 2 |
| §258 hand size ±8 %, foot size ±8 % | Slot 4: bound on an overall-scale control inside the multidimensional set (cf. FN overall hand scale) |
| §258 stature 168–208 cm, independent | Slot 2 |
| §263 E/B | Slot 7 |

### A.9 Halvren, Durrim, Grask, Gorrund, Pipkin (no single control list; items implicit in body sections)

| Race | Implicit items | Disposition |
|---|---|---|
| HV | Phenotype controls inside ancestry-derived envelopes (L54); no Elf Percentage / Gracility | All body slots under envelope B; Slot 0 Lineage |
| DU | Breadths (unequal under frame); regional muscle (L54) | Slots 3, 6 |
| GR | Breadth-only frame (L249); multidimensional foot (L245); composition and regional muscle (L251); arm span not a control (L60) | Slots 3, 4, 6; arm span DER |
| GO | Breadth-only frame (L220); regional muscle (L228); no Torso Size / Body Thickness | Slots 3, 6; bans as validators |
| PK | Frame (L68); regional muscle (L180); body hair (L561–567) | Slots 3, 6, 9 |

All other body items in these specs are covered row-by-row in UCCA-01 §2–§13.

— Claude

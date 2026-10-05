# RAC-07: Sex-Related Body Biology Review

**Author:** Claude
**Order:** `reviews/chatgpt-reference-anatomy-closure-phase1-order.md` §3 (RAC-07)
**Status:** PROPOSAL. Evidence: `reviews/rac-evidence/C-sex-hair-skin.md` Part 1.
**Default allowed by the order:** "no authored shift". No dimorphism is invented. Reproductive biology stays separate (PR L95).

## 1. What canon authors today

| Race | Direction | Magnitude | Shared hard bounds | Like-for-like rule | Canon |
|---|---|---|---|---|---|
| SA | Trunk only: lower axial trunk, pelvic band, E, B | **Authored** (four centres) | Yes, identical | — | SA L4216–4250 (§263) |
| PK | **Regions named** (pelvic, thoracic, facial, soft tissue); no direction | OPEN | Default (PR L91) | **Yes**: PIP-BODY-28/29, PIP-FACE-22/23, PIP-INT-21 | PK L154, L1491–1494, L1545 |
| CG | **Regions named** (pelvis, thorax, soft tissue); no direction; pelvis "must provide … sex-related anatomy" | OPEN | Default | **Yes**: COG-BODY-14, -28; reference presets need "multiple sex-related anatomical configurations" | CG L258, L339, L352, L875–879, L2949 |
| DU | None; bans only | OPEN | Default | "once defined" (DU L304) | DU L52, L58, L135, L219 |
| GR | None; even the magnitude class (minimal / moderate / strong) is OPEN | OPEN | Default | None | GR L76, L433, L564 |
| GO | None; bans "huge males and small females" | OPEN | Default | None | GO L82, L413, L564 |
| MF | Height distributions "may differ"; human anatomy | Not stated | No sex height limit | None | MF L23, L35 |
| AE, VA | Independence statements only | — | — | None | AE L126, L134; VA L128 |
| SK, SG, FN | Silent | — | — | None | grep-confirmed |
| HV | Inherits from sources; "Never invented inside Halvren" | OPEN | — | — | HV L54, L437, L497 |

No spec establishes a sex-specific hard bound (PR L91 stands everywhere; SA L4217 confirms identical bounds).

## 2. Proposed dispositions

| Race(s) | Proposal | Class | Rationale |
|---|---|---|---|
| **DU, GR, GO** | **No authored shift** for skeleton, stature, frame and composition until authored. Bans stay. Magnitude remains OPEN biology | **D** (default A) | Canon gives no direction; R-SEX makes "no shift" a complete state (PR L94); GR/GO forbid assuming human dimorphism (GR L76; GO L82) |
| **PK, CG** | Keep **no authored shift** as the default; the **regions** that may later shift are already named (PK L1491; CG L339). A direction may be authored later; numbers then come from like-for-like measurement | **B → C** | Scope exists, direction does not |
| **MF, SK, SG** (human family) | No race-specific shift **beyond ordinary human sex-related anatomy**, which MF canon already includes in Biological Anatomy (MF L35). SG is "a fully human population" (SG L3); SK faces "fully human" (SK L48) | **A** (author confirms) | Human-family biology is the reference, not an invention |
| **FN, AE, VA** | Author choice: (a) "no shift beyond ordinary humanoid sex-related anatomy", or (b) leave for an elven sex-related review | **A or D** | Only independence statements exist |
| **HV** | Follows sources; nothing authored inside Halvren | **D** | HV L497 |
| **SA** | Closed (§263); not generalized | — | PR L96 |

## 3. Is sex-related morphology required to produce valid reference meshes?

**For the Wave 1 measurement bootstrap: no**, with three exceptions.

| Need | Why | Required configuration(s) |
|---|---|---|
| **Marchfolk** | PIP-BODY-28/29 compare male Pipkin with male Marchfolk and female with female (PK L224–225); MF is the comparator for every race | Both MF configurations |
| **Saurin** | §263 validation already covers both centres (SA L4252) | Male centre (aff1b52) and female centre |
| **Pipkin, Cogling** | Their own like-for-like tests and reference preset rule (CG L2949) | Both, **once** a second-configuration soft-tissue decision exists (§4) |

For every other race, skeletal and craniofacial measurement can be bootstrapped on one configuration. Under "no shift", the second configuration would share every skeletal and composition value, so **skeletal measurements do not change**.

**Required eventually** by UCCA: the frame × sex × composition factorial for every race (UCCA L333) and the implementation rule that every combination must be representable (UCCA L135).

## 4. The open creative question (flagged; not a stop condition)

A second configuration is a full body, so it needs **external sex-related soft-tissue anatomy** (chest soft tissue, external genital-region form). For **DU, GR, GO, PK and CG**, canon authors none and explicitly forbids assuming human patterns (GR L76; GO L82; DU L219; PK L72). For elves and Halvren canon is silent.

- This is **genuinely creative biology**: it cannot be inferred from canon.
- It is **not a stop condition for this phase**: the order allows "no authored shift" and asks RAC-07 only to identify whether sex morphology is required, and no Wave 1 **skeletal** measurement depends on it (§3). It **is an authorship blocker** for the second-configuration ARMs of DU, GR, GO, PK and CG, for PIP-BODY-29 and the CG reference-preset rule (CG L2949); RAC-12 carries it as such.
- Level-5 precedent: the Iteration 3 feminine reference sheet built every race with MPFB's generic sex control ("feminine normalized sheet PASSes", `reviews/claude-iteration-3-body-validation-closed.md`). That was a visual-validation device, **not canon**, and it applied human soft-tissue anatomy to every race.

**Options for the author:**

| Option | Content | Consequence |
|---|---|---|
| X-1 | Author a minimal roster rule: second configurations of humanoid races use **ordinary humanoid sex-related soft tissue**, adult, non-exaggerated, with no race-specific dimorphism until authored. Saurin excluded (§263: no mammary anatomy) | Unblocks all second-configuration ARMs, but **contradicts canon** for GR, GO and PK ("never assumed identical to humans", GR L76; GO L82; "never assuming human proportions transfer", PK L72). Not recommended |
| X-2 | X-1 for the human family (MF, SK, SG); elves follow whatever AD-R21 decides; DU, GR, GO, PK, CG second configurations wait for per-race authorship | Wave 1 runs one configuration for those five races; like-for-like tests wait |
| X-3 | Per-race authorship now for DU, GR, GO, PK, CG | Needs a creative design pass; outside reference-anatomy closure |

**Recommendation:** **X-2.** It respects the GR/GO bans and does not slow Wave 1.

## 5. Reproductive biology

Separate and **D** everywhere: nothing about gestation, fertility, organs or obstetric geometry is proposed (PR L95; SA L4244; CG L691; HV L19–20, L319).

## 6. Proposed author decisions

| ID | Decision |
|---|---|
| AD-R18 | DU/GR/GO: no authored sex shift (default); magnitude stays OPEN |
| AD-R19 | PK/CG: no authored shift by default; regions already named; direction may be authored later (B → C) |
| AD-R20 | MF/SK/SG: confirm "ordinary human sex-related anatomy, no race-specific shift" |
| AD-R21 | Elves: choose "no shift beyond ordinary humanoid" or defer to an elven review |
| AD-R22 | Second-configuration soft tissue: choose X-1, X-2 (recommended) or X-3 |

— Claude

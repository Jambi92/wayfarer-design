# UFCA-05: Preset & Randomization Architecture

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ufca-phase1-order.md` §9
**Status:** PROPOSAL for author review. No numbers are set. Interim weights are never population canon (PK L635, L1407; CG L2070, L2964).

## 1. What a preset is

A **face preset** is a saved appearance record: ordinary DIR values for each Bound slot, plus presentation and acquired layers where the preset includes them. Every preset:

| # | Requirement | Canon basis |
|---|---|---|
| P-1 | Is produced, or reproducible, with the same controls and validators as Advanced Mode. **No preset-only anatomy, morphs or geometry** | MF L212, L257; AE L431; VA L474; DU L226; GR L685; GO L691; PK L1360; CG §191; SA §140 |
| P-2 | Passes every validator for its race (PASS or CONSTRAIN, never FAIL) | SA §246 L3960 |
| P-3 | Round-trips Preset → Advanced → Edit → Save → Reload without unexpected change | MF L257; HV L381; SA SAU-CC-01, SAU-CC-17 |
| P-4 | Carries **coverage tags** (for example "broad / severe-featured / elder") for library coverage only. Tags are LAT metadata, never subraces, castes, classes, cultures or genealogy | HV L343, L463; GR L410; PK L1387; CG §193 |
| P-5 | Never asserts genealogy (Halvren) and never uses source-race names as player-facing labels (I–M stay internal) | HV L463 |
| P-6 | Never bundles stereotype packages: no green brute, classic ogre, fair+freckled halfling, cute Cogling, pretty High Elf, charcoal-skin/white-hair/violet-eyed Vael, giant-beard Durrim, and so on | GR L562; GO L560; PK L637; CG L2006–2013; AE L520; VA L490; DU L222 |
| P-7 | Keeps exceptional anatomy reachable in Advanced Mode (order §8). A preset can **start** at an extreme, but the extreme is never exclusive to it | — |

**Library coverage requirement:**
- Each race's preset library spans its own diversity axes as listed in canon. Examples: CG §192; PK L1377–1387; SA §140 L2262–2271; GO L560; HV L327–341.
- Each library includes at least one minimum-stereotype individual: GO L684; GR L715; DU-FACE-01; PK PIP-FACE-03; CG COG-FACE-01.

## 2. Generation pipeline (universal)

The proposed universal pipeline generalizes Saurin §264, Grask L562, Gorrund L560 and Cogling §194.

| Step | What happens | Rules |
|---|---|---|
| 0. Inputs | Race; locks; selected regions; strength; seed; (Halvren) optional genealogy | — |
| 1. Envelope | Load the race's valid envelope. Halvren: compute **B** (ancestry-derived constraints) from genealogy, or use the general Halvren envelope when none is set | HV L463, L82 |
| 2. Drivers | Sample **driver** variables from the race's weighted soft distributions (LAT factors expand to correlated driver sets) | SA L4255; GO L560 "conditional probabilities" |
| 3. Dependents | Sample **dependent** variables inside their coupled bands, conditioned on drivers (FOLLOW / CLAMP / ENVELOPE from UFCA-03 §6) | e.g. SA rostral minimum from cranial length |
| 4. Validate | Run every validator. Reject FAIL shapes and resample. **Never "roll everything and repair"** | SA L4255; SK L280; DU L226 |
| 5. Diversity | Batch-level anti-convergence check (§5) | — |
| 6. Domains | Biological, Presentation and Acquired-History randomization are separate passes. Presentation never rewrites anatomy. Acquired never creates major Saurin rostral or jaw loss | SA §141–142A; CG §194; HV L347; GR L562 |

**Order of regions within step 2:**
- Drivers before dependents.
- Cranium and orbit before rostrum, midface and jaw.
- Skeleton before soft tissue.
- Soft tissue before surface.
- Facial anatomy before ear anatomy before pigmentation and hair (FN L333).

## 3. Selective randomization and locks

| Requirement | Detail | Canon basis |
|---|---|---|
| **Scopes** | Whole face; one slot; a slot set (for example "eyes only", "ears only", "surface only", "age presentation only"); or face-only while preserving body, height and age | SK L276; SG L398; FN; AE L456; VA L482; DU L226; HV L347; PK §24; CG §195, §133; SA §143 |
| **Locks** | Any DIR variable, slot or Saurin lock group (head, rostrum, eyes, keratin display). A locked value is never changed by generation | SA §144; CG §196 |
| **Locked child vs parent** | A locked child that makes every parent sample FAIL is reported to the player, who can unlock or accept the nearest valid parent. It is **never silently broken** | SA L2362; CG §196 |
| **Out-of-scope neighbours** | When a scoped randomization would invalidate an out-of-scope neighbour, the out-of-scope value wins and the in-scope sample is constrained, since the player did not ask to change the neighbour | Consistent with no-silent-reset (SA L2584) |

## 4. Race-specific generation notes

### Halvren

- **No 50/50 default.** Generation fails review on repeated exact 50/50 averages (L60, L377, L396).
- Inheritance is sampled through the craniofacial and ear **clusters** (LAT) with coupled regional expression: "mosaic without patchwork" (L41, L166).
- With genealogy set, many phenotypes are possible: "never one deterministic appearance per ancestry history" (L347).
- The source-protection validator runs on the whole face (L227).
- The genetic-simulation depth is **OPEN** (L13). The architecture needs only a sampler that honours B. It does not choose the genetics model.

### Saurin

- §264: drivers include head proportions and display family; dependents sit inside coupled bands.
- The rostral minimum rises with cranial length, so the FPI floor holds (SAU-CC-08).
- Display families come only from the §260 validated set. Minimal display is a normal outcome (SAU-CC-12).
- **Sex shifts no face or display driver** (L4255).

### Grask and Gorrund

- Tusk-like canines are **excluded** from generation and presets until reviewed (GO L320; GR L370).
- Maxillary and mandibular projection are drawn only from authored central values until the distributions are authored.

### Pipkin and Cogling

Anti-juvenile hidden-package bans:
- shortest + largest head;
- youthful face + quick movement (PK L1411–1417);
- toddler-combination rejections (CG §101).

### Sagekin

- Identity is statistical. The generator must reproduce the population shift **across a batch**, not force it on every individual (L246, L356).

## 5. Distribution behaviour

| Rule | Detail | Canon basis |
|---|---|---|
| **Validity ≠ frequency** | Frequencies shape randomization, presets and NPCs only. Advanced Mode always keeps the full valid range | SG L340; AE L435; SA §134, L3712; MF L303 |
| **Rare valid phenotypes** | Weighted tails: reachable by generation, at low frequency. Always manually creatable | SA L2596–2602; SG L224 |
| **Frequency tiers** | SG uses three tiers (L224) and later four (L344); AE uses four. A single vocabulary is author decision AD-U8 | — |
| **Strength levels** | Subtle / Diverse / Extreme, proposed universal (SK L268–272; AE L435; VA L478; HV L347). "Extreme" still produces only valid faces and never maxes every slider (HV L347). Whether Extreme is player-facing or development-only (SK L272 "possibly") is AD-U7 | — |
| **Anti-clone / anti-stereotype** | A batch fails if it converges on one face, one attractive template, one age or one pigmentation family (MF L249). Also fails on race-specific cliché lists (AE L464; VA L490; HV L223; DU L222; CG L2006). The **metric** is defined semantically: diversity across every Bound slot's DIR variables, plus convergence toward named cliché bundles. The **threshold** is deferred (UFCA-07, RM-UF-05) | — |
| **Correlated anatomy without clones** | LAT factors carry correlations, but each individual's residuals are sampled independently inside the coupled bands. Correlation shifts the centre and does not collapse variance | DU L252 "different subsets strongly … never fixed packages" |

## 6. Reproducible seeded generation

- **Record:** seed + generator version + race distribution version + locks + scope.
- **Promise:** the same record regenerates the same face (SG L453; FN L511; AE L460; CG §197; SA §156).
- **What a saved character stores:** DIR values, not seeds. The seed only reproduces a *generation event*.
- **Cross-race reuse:** uses semantic mapping, not raw slider copying (CG §198). For example, a human nose cannot become Saurin nasal openings by value copy. Such a mapping is **not** defined in Phase 1.

## 7. NPC parity

- NPCs use the same envelope, generator and validators (DU L506; GR L685; GO L691; CG §199; SA §157).
- Authored narrative exceptions are flagged **non-baseline**. In Saurin's sense that means outside canonical species anatomy (SA L2560–2562). They are excluded from presets, randomization and NPC baseline.

## 8. Simple Mode

- Simple Mode is Race → Preset → Confirm.
- If a "shuffle" is offered, it is the same generator in whole-face scope.
- Simple Mode never uses a simplified fake model (SA L2250 "no simplified fake Simple-Mode body").
- Halvren Simple Mode never requires genetics (HV L58).

— Claude

# RAC Wave 1 Execution Manifest

**Author:** Claude
**Order:** `reviews/chatgpt-reference-anatomy-closure-phase2-order.md` §7
**Method:** `decisions/REFERENCE_ANATOMY_V1.md`
**Status:** SPECIFICATION ONLY. This is a reference-asset and measurement specification. It is **not** an instruction to build meshes, run measurements or begin UE5 work; each needs its own order.

## 1. Planning set

**15 bodies + 1 Marchfolk head variant**, as in Phase 1. Canonicalization did not change the count:
- AD-R21 defers elven second configurations;
- AD-R22 lets DU/GR/GO/PK/CG bootstrap on one configuration;
- Marchfolk and Saurin keep two configurations each.

**Common state for every body** (REFERENCE_ANATOMY_V1 §3):
- R-1 central-tendency adult;
- R-3 central skeletal values (not "Balanced" as a default);
- R-4 reference composition;
- R-5 zero asymmetry;
- R-6 measurement stance;
- R-7 N3 neutralization;
- R-8 no hair over landmarks, no facial or body hair;
- R-9 neutral surface;
- R-13 real-world units;
- R-14 provenance record listing every builder-chosen value.

**One-configuration races:** the configuration is declared at build time and recorded. Like-for-like tests pair it with the **matching** Marchfolk ARM.

## 2. Manifest

| # | Population | Stature | Sex-related configuration | Frame / composition | Neutralization | Comparison tests to pass (central body) | Measurements unlocked | Candidate |
|---|---|---|---|---|---|---|---|---|
| 1 | **Marchfolk** | 173 cm | Configuration 1: ordinary human sex-related anatomy | Central / reference | N3 | MF permanent height-character set at the reference (MF L249); N3 identity | **RM-UB-07 (central)**, RM-LR-01/05/07 (MF), RM-OT-01 (MF side), RM-CF-02 (central), RM-UF-01 (MF) | **Existing:** Iteration 3 Marchfolk (starting candidate only); must be re-posed to R-6, normalized and pass §6 |
| 2 | **Marchfolk** | 173 cm | Configuration 2: ordinary human sex-related anatomy | Same | N3 | Same | RM-UB-07 (central, second configuration); MF partner for like-for-like tests (PIP-BODY-28/29 when available) | **Existing:** Iteration 3 Marchfolk, other configuration; same conditions |
| 3 | **Marchfolk head variant MF-FACE-PROJ-MAX** | Head only, on #1 | As #1 | — | Face N2/N3 | MARCHFOLK projection rule: most-projecting valid adult human face, no muzzle-like or non-human maxilla | **RM-CF-02** maximum-valid case | **Purpose-built** |
| 4 | **Skarn** | 208 cm | One; ordinary human (second available later) | Central / reference | N3 | SK-01 reference; N3 identity (SK-11); no Gorrund recreation | RM-LR-01/02 (ref)/05/07; RM-UB-01 (SK central) | **Purpose-built.** Iteration 3 Skarn S2 is not measurement truth (AD-R46) |
| 5 | **Sagekin** | 178 cm | One; ordinary human | Central / reference | N3 | SG-01; SG-12/13 neutralization; never elven | **RM-OT-01**; RM-UB-01 | Purpose-built |
| 6 | **Fenn** | 181 cm | One (second deferred, AD-R21) | Central / reference | N3, ears hidden variant for the body test | FN-01; hidden-ear body identity | RM-UB-01 (FN central); RM-CF-08 (central, with the ORB/aperture reading) | Purpose-built |
| 7 | **Aelari** | 190 cm | One (second deferred) | Central / reference | N3 | AE-01; AE-39…44 neutralization | RM-UB-01 (AE central); RM-CF-07 (AE central) | Purpose-built |
| 8 | **Vael** | 178 cm | One (second deferred) | Central / reference | N3 | VL-01; VL-16/17/18 (skeleton judged before soft tissue) | RM-UB-01 (VA central) | Purpose-built. **The Vael Rodin GLBs are not usable** (relief reconstructions of 2D sheets) |
| 9 | **Halvren** | 178 cm | One; follows sources | Central / reference; **no-lineage general envelope** (not 50/50; HV-03) | N3 | HV core validation; source-passing against W1 source ARMs at 178 cm (where valid) | RM-UB-01 (HV general envelope); baseline for later RM-OT-03 | Purpose-built |
| 10 | **Durrim** | 137 cm | One; no authored shift | Central / reference | N3 | Durrim reference; composition neutralization (DU L73); adult read (DU L76) | RM-SR-03 (DU); RM-SR-04 / RM-CF-10 (DU head share); RM-UB-01 | Purpose-built |
| 11 | **Grask** | 218 cm | One; no authored shift | Central / reference (GR-BODY-01 state) | N3 | GR-BODY-01; silhouette neutralization (GR L98); central projection ≈ Marchfolk (GRASK Prognathism row) | RM-LR-01/02 (ref)/05/07; RM-CF-10 (GR); central face for RM-CF-03/07 | Purpose-built. Head built to the RAC Phase 2 central-projection rule |
| 12 | **Gorrund** | 229 cm | One; no authored shift | Central / reference (GOR-BODY-01 state) | N3 | GOR-BODY-01; neutralized recognition (GO L691); ALPC present at central breadth | RM-LR-01/02 (ref)/05/06 (ref)/07; RM-CF-06, -10 (GO); central face for RM-CF-04 | Purpose-built. Head built to the RAC Phase 2 comparator |
| 13 | **Pipkin** | 107 cm | One; no authored shift (PIP-BODY-29 waits) | Central / reference (PIP-BODY-01 state) | N3 | PIP-BODY-01; PIP-BODY-17 (head, hands and feet obscured); PIP-BODY-28 **or** -29 against the matching MF ARM (whichever configuration was built) | **RM-SR-01**, RM-SR-03, RM-SR-04 (central), RM-CF-10 (PK); RM-UB-06 (PK central) | Purpose-built |
| 14 | **Cogling** | 91 cm | One; no authored shift (multi-configuration preset rule waits) | Central / reference | N3 | COG-BODY-01; COG-BODY-07/08 neutralization; COG-BODY-14/28 against the matching MF ARM | RM-SR-02 (central), RM-SR-03, RM-SR-04 (central), RM-CF-10 (CG) | Purpose-built |
| 15 | **Saurin** | 188 cm (tail excluded) | Male centre (§263) | Central / reference composition with canonical fat depot ordering; tail at reference from the posterior-pelvic-plane landmark | N3; display at reference, excluded from head length | SAU-BODY-01/02; SAU-FACE-22 stature accounting; SAU-SILHOUETTE | **RM-CF-01** (run first; no biological dependency), RM-UB-01 (SA), basis for RM-UB-04 | **Existing:** closure reference aff1b52; needs the §6 acceptance record |
| 16 | **Saurin** | 188 cm | Female centre (§263: E 2.0 cm, B 1.6 cm, +7 % lower trunk, +5.5 % pelvic band) | Same | Same | SAU-BODY-19 (both configurations); §263 validation set | Second-configuration Saurin values; RM-OT-04 later | **Existing basis:** the §263 female-centre configuration (reference accounting female-centre column), derived from aff1b52; the validated +10 % "reference female" is above the centre and is **not** this candidate. Needs the §6 acceptance record |

## 3. Order of work inside Wave 1 (when ordered)

1. **RM-CF-01** on #15: no biological dependency.
2. **Marchfolk #1, #2, #3**: acceptance, then RM-UB-07 (central) and RM-CF-02. Every "than Marchfolk" constraint waits for this baseline.
3. **Remaining central ARMs #4–#14 and #16**, each through the §6 acceptance test, then their listed measurements.
4. All results recorded as **diagnostic envelopes**; canon only by author acceptance (REFERENCE_ANATOMY_V1 §8).

## 4. Not in Wave 1

- Frame, stature, composition variants and named extremes (W2).
- Marchfolk 147 / 203 cm variants (W2; RM-UB-07 boundary part).
- Second configurations for SK, SG (available, not required for W1), elves (deferred), DU/GR/GO/PK/CG (need authorship).
- Halvren genealogy-conditioned references (W3).

— Claude

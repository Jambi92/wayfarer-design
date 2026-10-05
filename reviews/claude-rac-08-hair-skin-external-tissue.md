# RAC-08: Hair / Skin / External-Tissue Biology Review

**Author:** Claude
**Order:** `reviews/chatgpt-reference-anatomy-closure-phase1-order.md` §3 (RAC-08)
**Status:** PROPOSAL. Evidence: `reviews/rac-evidence/C-sex-hair-skin.md` Parts 2–3.
**Scope:** implementation-critical **visible** biology only. No gameplay armour, damage resistance or durability effect is inferred.

## 1. Is any of this a reference-mesh blocker?

**No.** ARMs carry no body hair, no facial hair, no scalp hair over measured landmarks, and a uniform neutral surface (RAC-02 R-7–R-9; UCCA N2/N3). Hair and skin decisions affect the creator and surface systems, not skeletal or proportional measurement.

## 2. Body hair

| Race(s) | Canon | Proposal | Class |
|---|---|---|---|
| **PK** | Bound: broad individual variation across limbs, torso and other ordinary regions; hairy feet not required; never rusticity, masculinity, youth or femininity coding (PK L563–569) | Carried. **Fix stale line:** PK L383 still sends body hair "to the later universal/race surface review" | — / editorial A |
| **CG** | Bound: individual variation; not determined by scalp hair, facial hair, sex, muscularity, age or culture; soft sex correlations OPEN; no hairy/hairless stereotype (CG L1817–1823) | Carried. The register concern (REG L1057) is resolved by the current spec wording (soft correlations reserved) | — |
| **DU, GR, GO** | OPEN with bans: never universal hairiness (DU L207); without universal hairiness (GR L402); never inferred from size (GO L521). GO L521 relates body-hair colour to scalp and brows, which presupposes body hair can exist | **Qualitative baseline, explicit author decision:** "body hair may occur with broad individual variation in density and distribution; never a racial identifier; never universal; never inferred from size or stature". This turns a BIO OPEN (UCCA L195) into positive biology, which canon only implies (DU L207 "any later body hair"; GO L521 colour relation), so it is **A only by author decision**, like MF/SK/SG. Sex-related and population distributions stay **D** (DU L207 lists sex-related distribution as a later component) | A by decision + D |
| **MF, SK, SG** | Silent. General statements keep human hair biology (MF L15 "skin and hair biology"; SG L3 "fully human"; SK L48) | **Author option (A):** bind body hair as "ordinary human body-hair biology, broad individual variation", modelled on UFCA Q-2 for eyebrows. **Without that decision it stays hidden** (UCCA L195) | A by explicit decision only |
| **FN, AE, VA** | Silent; ECR L175 says facial hair "is not biologically prohibited for any elf", but nothing on body hair | Author option: extend to body hair (A) **or** keep hidden pending an elven review (D) | A or D |
| **HV** | Silent; source-first rule (HV L497, L499) | Follows the sources' decision; never authored inside Halvren | D (dependent) |
| **SA** | No mammalian hair (SA L1909; UCCA L196) | Carried | — |

**Recommendation:** decide MF/SK/SG now (lowest risk: human family), keep the elves and Halvren hidden. Body hair is never inferred from scalp or facial hair (UCCA L195); any binding is an **explicit author authorization** like Q-2 (UFCA L206–208).

## 3. Facial hair (adjacent; noted only)

- MF and SK describe facial hair as presentation and controls (MF L181; SK L195, L228); growth capability is implicit. A one-line biology statement would align them with UFCA slot 11 "Facial-hair biology" (UFCA L52). **A, editorial.**
- FN is silent; ECR L175 fills it. Sex-related facial-hair distributions for DU/GR/GO/PK/CG are **D** (tied to RAC-07).

## 4. Skin thickness and durability

| Item | Canon | Class |
|---|---|---|
| Skin thickness, DU / GR / GO | OPEN, never inferred from skeleton, size, stature, mythology, coloration or combat role (DU L359; GR L512; GO L515) | **D** |
| Tissue durability, any race | Any effect banned: "has no gameplay effect" (DU L359); never "turning large anatomy into armor" (GO L515); "No creator value feeds a gameplay stat" (UCCA L357) | **E**, effectively a firewall |
| Silent races | No differential claim exists | No question raised; leave silent |

## 5. Visible structure vs material behaviour

Canon already draws this line in Durrim and repeats it elsewhere:
- skin thickness, texture, wrinkles, pores, scarring and weathering are **surface appearance** (DU L278);
- "Racial structure is never faked mainly through normal maps, displacement, roughness, ambient occlusion, baked shadow or skin materials"; "large-scale depth lives in geometry or deformation, fine detail may use materials later" (DU L280);
- identity survives neutral grey / uniform pigment (UCCA L214); neutral diagnostic material tests (GR L491; GO L537, L541).

**Proposed universal rule (A), R-SKIN-1:** for every race, **structural anatomy lives in geometry**; skin texture, pores, roughness, oiliness and fine lines are surface (material) detail; **no skin-thickness difference is modelled geometrically** in reference meshes unless a race later authors one. Visible thickness phenomena already noted as observation (Grask ear translucency, GR L512) are material behaviour, class **C/E** for the surface pass.

**Visible surface texture** (pores, fine lines, roughness, oiliness) is already authored qualitatively for DU, GR, GO, PK and CG (DU L358; GR L512; GO L515; CG L1754–1766): **A, carried**.

## 6. Proposed author decisions

| ID | Decision |
|---|---|
| AD-R23 | DU/GR/GO body-hair qualitative baseline (§2); distributions stay D |
| AD-R24 | MF/SK/SG body hair: bind as ordinary human biology, **or** keep hidden |
| AD-R25 | Elves and Halvren body hair: keep hidden (recommended) |
| AD-R26 | Adopt R-SKIN-1; skin thickness D; durability stays firewalled |
| AD-R27 | Editorial: PK L383 stale pointer; MF/SK facial-hair biology line |

— Claude

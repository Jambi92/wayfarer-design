# RAC RM-OT-05: final Gorrund acceptance closure audit

**Order:** `reviews/chatgpt-rac-rm-ot-05-final-gorrund-acceptance-stage-c-release-order.md` (4ec9129).
**Selected scene (author ruling §1):** U8 checkpoint 1, `GO-05U8_cp1.blend`, SHA-256 `2341d55445a448e24852f98fd9df3984ab12d706ef0b455cb4a2cdb0782860d6`.
**Governing method:** `decisions/REFERENCE_ANATOMY_V1.md` §3 (R-1…R-14) and §6 (candidate acceptance test).
**Evidence:** `reviews/rac-rmot05-closure-evidence/`. The audit was read-only. **No geometry was edited; no further U-block was run.**

## **RM-OT-05 CLOSURE BLOCKED — NEW MANDATORY CONTRADICTION**

The author's §1 visual ruling and §2 diagnostic dispositions are recorded and respected:
- the residual crease is accepted as anatomy;
- V6, V6c-1 and V6c-2 and the eight V4 taper edges are non-blocking.

The audit nevertheless found a mandatory ARM-state contradiction that **no author ruling has resolved**. Per order §3, the audit stops and reports it. **Gorrund is not recorded as AUTHOR ACCEPTED, RM-OT-05 is not closed, no race spec or RMQ acceptance line was changed, and Stage C was not released or started.**

### The contradiction: the selected body is clothed, and the ARM state requires a neutralized body

`REFERENCE_ANATOMY_V1` §6.1 requires R-1…R-14 to hold, and §6.2 requires N3 neutralization. In the selected U8 cp1 mesh, every garment and hair zone from the 05Q inventory except the +X armband's exposed arc is **still present and unedited** (`u8cp1_garment_zone_audit.json`; mapping through the committed F1 face indices).

| 05Q zone | Class | Faces present in U8 cp1 | Edited 05Q–U8 | ARM requirement it conflicts with |
|---|---|---|---|---|
| Waist belt + loincloth top (z 112–140) | c: fused, no skin beneath | 14,053 | 0 | **R-7** (no clothing over measured landmarks: pelvis, iliac crest / ASIS), **R-12** |
| Loincloth flaps (z 72–112) | a/b | 19,116 | 0 | R-7 (thighs / crotch), R-12 |
| Forearm bracers | c | 6,034 | 0 | R-7 (forearm / wrist), R-12 |
| −X upper-arm armband | d | 3,152 | 0 | R-7, R-12 |
| Shin + ankle wraps | c | 16,615 | 0 | R-7 (shin / ankle landmarks), R-12 |
| Necklace + pendant teeth | d | 3,280 | 0 | R-7, R-12 (jewellery) |
| Front braids, back braid | a | 7,316 | 0 | **R-8** (hair over measured landmarks) |
| Mane over neck / upper back | c | 13,565 | 0 | R-8 (neck / upper-back landmarks) |
| +X armband exposed arc | c | **0** (replaced by inferred skin, 05Q→U8) | — | resolved locally only |

The zone boxes include some adjacent skin (05Q known errors), so the counts show presence, not exact garment area.

**Visual confirmation:** `u8cp1_full_figure_garment_zones.png` shows front, rear, side and 3/4 views, plain and labelled (red = garment zones, teal = mane / braids). The belt, loincloth, bracers, shin wraps and necklace are plainly present.

**Why this is unresolved rather than superseded:**
- 05Q §1 ruled the source route "not acceptance of source muscularity, proportions, paws or **garments** as canon".
- 05Q / 05R / 05S / 05T / 05U each confined the work to the single +X armband interface. They forbade a "second garment region" or "full-body clothing removal" without a new author order, and stated that a local pass "says nothing about belt/pelvis, bracers/shins, whole-body suitability or species acceptance".
- No later order authorized or waived the remaining garments.
- The final order's §2 dispositions cover V4 / V6 / V6c only. It also says it is "not a general waiver" and forbids inventing one.
- R-7 explicitly allows only "a neutral fitted proxy that **never covers a measured landmark**". The fused belt and wraps cover pelvic and shin / ankle landmarks, so they cannot qualify without an author decision.

### Related items the author should rule on at the same time (each already disclosed in earlier gates)

| Item | Finding |
|---|---|
| **R-2 / R-13 stature** | The mesh's vertical extent is **241.06 cm** (top vertex 43953 on the head), against the accepted ARM realization GOREF **230.9 cm** (nominal 229). R-13 stature is to the skull vertex excluding hair and keratin display, and was not separately measured on this lineage. 05P recorded the source-route stature issue as unresolved, and no later order settled it. |
| **R-6 measurement stance** | 05Q forbade stance correction on the source route; the RD stance work (05O / 05P) was rejected. R-6 compliance of the selected body has not been demonstrated or waived. |
| **§6.2 / §6.3 race and boundary tests** | The blind / neutralized structural-readability gate (05F re-entry condition; 05N / 05O criterion C5) was last **FAILED** on the source lineage and has not been rerun since. 05Q–U8A were local surface work. |
| **Feet** | 05P / 05Q list "paw-like toes" as unresolved within plantigrade anatomy. |

## Audit checklist (order §3)

| # | Check | Result |
|---|---|---|
| 1 | Selected scene and reconstructed result are the pinned files | **PASS**. `GO-05U8_cp1.blend` `2341d554…`, `return.npz` `89c1def3…` and `result.obj.gz` `e37740ec…` (`closure_hash_checks.json`). All 24 U8A gates PASS on it, exit 0. |
| 2 | `base.glb` unchanged | **PASS**. Re-hashed the copy on E: (`…\source\Gorrund-Male\Gorrund-Male_Rodin_base.glb.zip`): zip `b3fbfb2a…`, GLB inside `78ecfa87…a7b` (43,012,652 bytes), matching `rac-rmot05q-evidence/source/PROVENANCE.md`. |
| 3 | Provenance; reconstructed / edited skin labelled INFERRED | **PASS**. Source F1 indices pinned (05Q). The 35 cap faces carry U2 label 6 (edited source surface, INFERRED), and the 05S / U-series reconstruction is labelled in every gate. |
| 4 | Stature / scale / transforms / units / object identity | **Transforms and identity PASS**: identity transform, no modifiers, `rac_s3_vid1` one-to-one. Units are cm, consistent with every RAC ARM so far. **Stature: UNRESOLVED** (241.06 cm extent; see above). |
| 5 | No hidden mandatory acceptance failure after the author dispositions | **FAIL: R-7 / R-8 / R-12 (garments, jewellery, hair over landmarks)**, never author-resolved. Related unresolved items: R-2 / R-13, R-6, §6.2–6.3 readability. |
| 6 | Accepted race / canon direction of the recovered-source route | **PASS (direction)**. Leonine beastfolk head and tail retained; massive plantigrade humanoid body (GORRUND_V1; 05N). Not a different race. |
| 7 | No regression of U6 / U7 / U8 protection, manifold / intersection, crease, roughness, local quality | **PASS**. U8A check on U8 cp1: 24 / 24 (crease A 0.7788, crease B 0.3503, U6 target roughness 32.41, cap minimum 13.41, U7 12.68, U8 16.16, V2 / V3 / V5 / V6c-3). |
| 8 | Grask E3 unchanged | **PASS**. `reviews/rac-rmot05d-evidence` has had no commit since aaa3433. Grask E3 stays frozen as the accepted direction. |

## Stage C (order §5): not released

Stage C has a defined contract: 05E §9 and 05F §6. It is a combined run on Grask E3 plus the accepted Gorrund body, covering:
- the full W2C / W2D validator suites at stature endpoints and internal heights;
- matched heights, Frame extremes, low / reference / high composition;
- protected skeletal relations and clearance guards;
- the full-roster read;
- an author package.

That contract requires an **accepted** Gorrund reference, and RM-OT-05 is not closed, so Stage C is **not released and was not started**.

**For the author, when Stage C is eventually released:** the contract assumes Narrow / Broad, low / high-composition and stature variants. The source-route Gorrund is a single sculpted body with no derived variants: 05N–05Q say "scaffold NOT DERIVED", and the LOW was not rebuilt after 05P. Running Stage C will therefore also need an author decision on how Gorrund variants are derived from the accepted body. That is a scope choice, not something to invent.

## Author decision required (choose one; nothing is assumed)

1. **Authorize whole-body neutralization** of the selected body under the established local-surgery method: remove or replace the belt / loincloth, bracers, −X armband, shin wraps, necklace and over-body hair with labelled INFERRED skin, U-style protected and verified. Then rerun this closure audit.
2. **Rule a Gorrund-specific R-7 / R-8 / R-12 disposition**: for example, accept the fused garments as a temporary neutral-proxy exception for this Wave-1 reference state, with stated landmark exclusions. Only the author can make this ruling; it is not something to infer.
3. **Accept U8 cp1 with a narrower status** (for example, "accepted source-surface interface repair / visual reference", not an ARM), keeping RM-OT-05 and Stage C open until a neutralized ARM exists.

The same ruling should settle R-2 / R-13 stature bookkeeping (241.06 cm extent against GOREF 230.9), R-6 stance, and whether the §6.2 / §6.3 readability gate must be rerun on the selected lineage.

## State

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED**; U8 cp1 is the author-selected visual result; closure blocked |
| Grask E3 | FROZEN (unchanged) |
| RM-OT-05 | **OPEN** |
| Stage C | **BLOCKED / NOT STARTED** |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| Race specs / RMQ acceptance line | unchanged |
| `base.glb` | unchanged |
| Rodin | not run |

**→ STOP. RM-OT-05 CLOSURE BLOCKED — NEW MANDATORY CONTRADICTION** (ARM R-7 / R-8 / R-12 neutralization: the selected body retains fused garments, jewellery and hair over measured landmarks).

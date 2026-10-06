# RAC W1d — Author-Acceptance Gate (W1c blocker resolution pass)

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md`

## Recommendation: **EXACT REMAINING BLOCKERS — every one now waits on an author decision** (packets below)

- No diagnostic was promoted to canon.
- No race spec anatomy was edited. Only acceptance status lines were added for MF, SK, SG and SA.
- No constrained ARM was rebuilt, because none of their dependencies is accepted yet (work order item 8).
- The HV source-span re-run waits on FN, AE and VA acceptance (item 9).

## 1. Work order status

| # | Item | Result | Deliverable |
|---|---|---|---|
| 1 | Record acceptances and method rulings | **Done.** MF-M-R, MF-F-R, MF-FACE-PROJ-MAX, SK and SG are recorded as accepted W1 reference assets in the ARM records, RMQ (RM-UB-07, RM-CF-02, RM-OT-01) and the MF/SK/SG spec status lines. SA-M/SA-F acceptance is now also in the SA spec status line. Method rulings are recorded with their scope limits (`claude-rac-w1c-build-method.md` §5). FN/AE/VA/HV/DU/GR/GO are marked CONSTRAINED; PK/CG are diagnostic proxies. **MF-F-R globe:** the DER 2.44 cm globe is replaced by a fitting ordinary-human landmark globe of 2.30 cm (clearance 0.026 cm; the size is BUILDER-CHOSEN, decision G-D1). Placement, face and FPI are unchanged, **but the globe-dependent readings moved**: MF-F-R ORB E-proxy breadth ÷ HL 0.129 → 0.120 and aperture width 2.32 → 2.24 cm (`rac-w1c-evidence/tables.md`) | `reviews/rac-w1c-arm/*`, RMQ, specs |
| 2 | Pelvic morphology authorship packet (FN, AE, VA, DU, GR, GO, PK) | **Packet ready.** Per population: canon quotes, implied vs OPEN, minimum positive architecture proposals, skeleton vs composition, build and RM-UB-06 verification. Collision checks for DU–PK–CG, SK–GR–GO and FN–AE–VA. **22 decisions (PV-D1…PV-D22)** | `claude-rac-w1d-pelvic-morphology-packet.md` |
| 3 | Large-race girdle + Gorrund ALPC packet | **Packet ready.** Grask girdle GR-G1…G8; Gorrund girdle GO-G1…G8; **ALPC operational definition** (stations S1–S7, criteria ALPC-0…8; a scaled human trunk fails by construction); SK/GR/GO orderings with undetermined pairs kept undetermined; skeleton vs muscle vs MDC firewall. Diagnostic: the current W1c GO **fails** ALPC-1 and -2(a) on skin ratios (rest and R-6). ALPC-4 fails on rest geometry only. **15 decisions (AD-G1…AD-G15)** | `claude-rac-w1d-large-race-girdle-alpc-packet.md` |
| 4 | Non-human ear families | **Packet + schematic reference geometry** for FN, AE, VA, HV, GR and GO (plus the MF reference), each its own architecture law. Canon directions hold: FN greatest projection (marginal 2 % over VA); AE more upward **and** backward than FN; VA more lateral and backward than AE; VA broader base; GR late taper; GO short-to-moderate extent. **Exception: GO close-set projection is not demonstrated** (definition question E-D4). These are **schematic, not sculpt-quality**: a sculpting pass is needed before attachment. **6 decisions (E-D1…E-D6)** | `claude-rac-w1d-ear-family-packet.md`; `rac-w1d-evidence/ears/` |
| 5 | Fenn bony-orbit packet | **No defensible bony method exists on the current geometry.** Four proxies disagree in sign, and the best has repeatability worse than the effect. FN is **not shown to fail**, so it is **not rebuilt**; RM-CF-08 (FN ORB) is NOT DEMONSTRATED. The aperture is more open (diagnostic). Recommended method: a landmark orbital-margin ring (O-1). Comparator gap G-1 flagged. **4 decisions (O-D1…O-D4)** | `claude-rac-w1d-fenn-orbit-packet.md` |
| 6 | PK/CG native short-adult strategy + test bodies | **Option-2 workflow implemented. PK-NAT (107.00 cm) and CG-NAT (90.99 cm) built without a global uniform scale**, from the accepted human reference construction with explicit regional factors. All CG checks pass, including HH 11.81 cm and the narrow thorax. All PK checks pass except the marginal "pelvic vertical > MF" (0.0553 vs 0.0555). That is a **build issue**: the proxy's 0.062 came from the generator's minimum-height model, and the pelvic packet's own PK-P3 (≥ MF) also fails, so PV-D10 alone does not resolve it. The generator's minimum-height model is shown to be implausible (femur 23.8 < tibia 39.2 cm). **R-2 intent needs an author ruling** (only head, hands and feet depart from a uniform rescale of the race-target body). **4 decisions (S-D1…S-D4)** | `claude-rac-w1d-short-adult-native-strategy.md`; `rac-w1d-evidence/native-short/` |
| 7 | Saurin D-2 | **No closure-rig correspondence exists**: the closure body descends from a rig-less Hyper3D/Rodin mesh. The failed re-pose stays rejected. Joint-centre options J-1 (author-placed, recommended), J-2 (builder-placed, with acceptance) or J-3 (keep blocked). **2 decisions (J-D1, J-D2)** | `claude-rac-w1d-saurin-joint-centre-packet.md` |
| 8 | Rebuild constrained ARMs | **Not started** (correctly): every dependency (pelvis, girdle/ALPC, ears, orbit method) awaits acceptance | — |
| 9 | Re-run cross-race diagnostics, HV source span | **Not re-run**: no constrained ARM changed. The PK/CG native bodies were checked on their own (`native_short_checks.json`) | — |

## 2. Remaining blockers (exact)

| # | Blocker | Waiting on | Unblocks |
|---|---|---|---|
| B-1 | PK/CG R-2: is the option-2 native workflow acceptable, or is a sculpted base required? | **S-D1…S-D4** | PK and CG candidates replacing the proxies |
| B-2 | Ear-family architecture and magnitudes; sculpting pass; GO projection definition | **E-D1…E-D6**, then a sculpt pass | FN, AE, VA, HV, GR and GO head tests (R-11) |
| B-3 | Pelvic morphology authorship | **PV-D1…PV-D22** (PV-D1 is the core: whether a relational, human-homologous pelvis counts as "distinct") | DU, GO, FN, AE, VA, GR and PK pelvic items (RM-UB-06); DU/GO rebuilds |
| B-4 | Grask/Gorrund girdle and Gorrund ALPC definition | **AD-G1…AD-G15** (AD-G8: ALPC; AD-G14: skeletal-proxy rebuild method; AD-G13: AD-R15 wording) | GR/GO rebuild; RM-LR-01…06 rerun |
| B-5 | Fenn bony-orbit method and comparator | **O-D1…O-D4** | RM-CF-08 (FN); later RM-UF-01 / RM-SR-04 orbit items |
| B-6 | Saurin joint centres | **J-D1, J-D2** | SA RM-UB-01 limbs, RM-UB-04 |
| B-8 | MF-F-R landmark globe size | **G-D1** | Final MF-F-R aperture / orbit readings |
| B-7 | HV source-span re-run | FN/AE/VA acceptance (after B-2, B-3, B-5) | HV acceptance |

**New findings to note:**
- **A Cogling narrow-thorax check was added** (CG L98, L102): "thoracic breadth ÷ stature < MF". CG-NAT passes it (0.182 vs 0.190). The W1c CG **proxy fails** it (0.197). The W1c audit documents are kept as issued; the proxy is superseded if S-D1 is accepted.
- **G-D1 (new, small):** accept the 2.30 cm fitting globe for MF-F-R (builder-chosen; replaces the DER rule for this body).
- **DU's low femur ÷ leg is partly a generator artefact** of the minimum-height model. DU's rebuild should use the native-workflow source rather than the low height macro.
- **AD-R15 may be ambiguous** (girdle packet AD-G13), affecting whether GO > SK thoracic depth is a pass condition.
- **The PK "pelvic vertical > MF" check may overstate canon** (PV-D10).

**Correction note (RAC W1e, October 5, 2026; PV-D10):** the author ruled that the PK direction is pelvic vertical contribution ÷ stature **≥ MF**, not a strict "> MF" (PV-D10). PK-NAT's 0.0553 vs MF 0.0555 is therefore marginal within the 1 % diagnostic tolerance and **not a canon failure**. The text above is kept as issued. The PK pelvis was rebuilt to the accepted architecture in W1e (`reviews/claude-rac-w1e-rebuild-record.md`).

STOP.

— Claude

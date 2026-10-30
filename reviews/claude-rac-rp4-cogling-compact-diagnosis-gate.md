# Claude Gate — RAC RP4 Cogling Independent Compact Diagnosis / Production Gate

**Order:** `reviews/chatgpt-rac-rp4-cogling-independent-compact-diagnosis-order.md` (9424c72)
**Date:** 2026-10-30
**Evidence:** `reviews/rac-rp4-evidence/cogling/`
**Tools:** `tools/rac/rp/cogling_rp4_v001/`

## Result

**COGLING RP4 REQUIRES AUTHOR DECISION — c1 toe3_j1 / toe4_j1 MTP validator geometry (the Pipkin D4 probe double-scaling class, not applied automatically) + 76 cm fixed-resolution T-7 silhouette reading**

Everything else passes:
- **Sources and c2 anchor:** all three accepted sources regenerate exactly. `CGF91-NAT` = **COGLING CONFIG-2 CENTRAL REFERENCE PASS — READY FOR PRODUCTION DIAGNOSIS**, with one recorded reading (§1).
- **Branch:** a Cogling-specific `MPFB_COGLING_COMPACT_BRANCH_v001` (thumb MCP only, placement re-solved on Cogling) fixes every thumb. 0 quads > 4:1, no new contact, no new deformation class.
- **Firewalls:** Pipkin overlap 14 / 14 at 91 and 107; Durrim context 11 / 11; adult vs child 17–18 / 19; Marchfolk normalized 11 / 11 on every body; hidden-identity firewalls hold.
- **Immutables:** 69 / 69 unchanged.

**Not done, pending the ruling:** no production candidates (§19 requires all author-decision gates resolved), no freeze-candidate record, nothing frozen. The Pipkin exception was **not** applied and no failure was relabelled.

## 1. Sources and configuration-2 anchor (§3, §4) — `partA/`, `regen/`

**Regeneration (§3).** `du_regen.py` (recorded route, MPFB 2.0.17 / Blender 5.2.2) rebuilds each source bit-identically against its committed R-6 asset:

| Source | Role | Stature | Geometry identical | max abs dV |
|---|---|---|---|---|
| CGJ7 | c1 central (W1r) | 90.99 cm | yes | 0 |
| CG76H-NAT | min (RM-OT-05A §2) | 76.00 cm | yes | 0 |
| CG107-NAT | max (W2H) | 106.98 cm | yes | 0 |

CG76-NAT stays provenance only and was not used.

**CGF91-NAT construction (`partA/CGF91.cfg.json`, `cg_native_c2.py`):**
- MPFB configuration-2 base macro (MF-F-R 0.60595703125);
- the exact CGJ7 targets and bone scales (upperarm / lowerarm / thigh [0.95, 1, 0.95]);
- girth β 1.0;
- the exact CGJ7 head factor (0.51272);
- the native short-adult route solved to 91.000 cm;
- no Cogling sex shift.

A determinism rebuild is bit-identical.

**Why the head factor is copied rather than re-solved.** The first build re-solved a 12 cm head with native_short's head check. That check uses absolute-cm chin windows, and the measured head came out 12.83 cm (c2 / c1 +8.6 %, against Marchfolk −4.6 %), which is a Cogling-specific shift that §4 forbids. Copying the CGJ7 factor leaves the c2 / c1 head difference to the base itself:
- Cogling c2 / c1 −5.15 %; Marchfolk −4.60 %; Pipkin −4.33 %;
- c2 head 11.20 cm, inside the canon 11–13 cm.

Two independent measurements back this up (`CG_partA.json` `head_height_crosscheck`):
- a crown-to-menton cross-check;
- arm_measure, which reads 12.33 cm on c2 because its profile walk misplaces menton on the ~11 cm c2 face. On every other body the two measures agree to 0.05 cm.

**Anchor validation (`CG_partA.json`).** Normalized against Marchfolk 173 (MF-M-R / MF-F-R); the §4B rows are read against an equal-height Pipkin.

| Rows | c1 CGJ7 | c2 CGF91 | 76 | 107 |
|---|---|---|---|---|
| RM-SR-02 distal redistribution: upper arm / arm < MF, forearm / arm >, hand / arm >, finger / hand >, femur / leg <, lower leg / leg >, hand / stature > | 7 / 7 | 7 / 7 | 7 / 7 | 7 / 7 |
| near-human total (arm / leg / torso share within ±0.010 of MF) | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 |
| fine femoral shaft < MF | ✓ | ✓ | ✓ | ✓ |
| narrow core vs Pipkin (crest, thorax, pelvic AP per stature) | 3 / 3 | 3 / 3 | 3 / 3 | — |
| less pelvis-led than Pipkin (W2H §4B, 3 relations) | 3 / 3 | **2 / 3** | 3 / 3 | — |

**The recorded c2 reading.** At 91 cm c2 against the diagnostic Pipkin c2 (`PKF91-NAT` = the PKF107 route at 91 cm), crest / thoracic breadth reads +1.05…+1.21 % (Cogling side higher).
- **Cause:** a narrower thorax, not a broader pelvis. The Cogling c2 thorax is −6.9 % and its crest −5.9 % against Pipkin c2.
- **Origin:** a generator response to the same Cogling `torso-scale-horiz-decr` on the female base. Cogling c2 / c1 thorax is −10.3 % against Marchfolk −8.8 %. Pipkin shows the opposite residual (−6.0 %), the one recorded at Pipkin's own c2 gate.
- **Holding on c2:** pelvic vertical / thoracic vertical (−9.8 %) and pelvic AP / thoracic depth (−4.6 %), with every narrow-core and distal row.

I record this as a NARROWER-CORE INVERSION (author note), not as a pass.

**Report rows.**
- **Per-segment joint ratios:** wrist / forearm, knee / femur and ankle / shin are report rows. W2H reports them, does not score them, and they are inflated by the distal redistribution by design.
- **Sex consistency:** 14 / 24 rows sit within 1.5 % of Marchfolk. The rest are generator responses (Cogling sex anatomy stays OPEN).

## 2. Phase A — unbranched MPFB Family Base v005 (§5, §6) — `unbranched/`

**Propagation.** `propagate_core.py` (Standard v1) from the committed v005 core gives 57,842 V / 57,840 Q on every body:
- 1 component;
- 0 boundary / non-manifold / degenerate;
- T-1 / T-2 / T-3 pass and contact new 0 everywhere.

**Authoritative validator (D1+D3+D4+D5+D6):**

| Body | Firm | Failures |
|---|---|---|
| CG76H-NAT | 63 / 69 | thumb_mcp l / r (1 ring, closed-ring fallback, no crease pole); toe3_j1 / toe4_j1 l / r (0 loops, fallback, no crease pole) |
| CGJ7 | 63 / 69 | same |
| CGF91-NAT | 67 / 69 | thumb_mcp l / r (2 rings) |
| CG107-NAT | 63 / 69 | same as 76 / 91 c1 |

Neck and hips pass on every body.

**Face readiness.** Mouth 39–42 rings, orbits pass, 0 poles at the mouth corners.

**Landmark tool fix (Cogling-scoped).** The landmark tool's lip-slit search uses absolute-cm windows that find no lip rim on the ~12 cm Cogling head: the slit sits 3.5–3.9 cm below the eye, inside the fixed 4 cm exclusion. I scaled only those windows (and the TMJ estimate) by the head size, KH = (crown − eye) / 10.89 cm (`cg_landmarks.py`). Nothing else changed, and no other race uses it.

**T-7 at 76 cm (author item 2).** CG76H-NAT fails the authoritative T-7 already on v005:
- **Reading:** profile IoU 0.9931 against the 0.995 limit, with surface deviation p95 0.09 mm.
- **Cause:** T-7 rasterises at a fixed 3 px / cm, so a 76 cm body loses IoU to edge quantisation alone.
- **Scale-consistent check (`cg_t7_scaled.py`; same method, resolution × 173.143 / stature):** 0.9974–0.9980 on v005 and the branch alike (`branch_gates/CG_T7_scaled_*.json`).
- **91 / 107:** pass the authoritative T-7.

**Density (§6) — `unbranched/CG_density_v005.json`.** Mean / p95 edge as % of stature:

| Region | 76 | 91 c1 | 91 c2 | 107 | Pipkin 91 context |
|---|---|---|---|---|---|
| face orbit | 0.098 / 0.20 | 0.087 / 0.18 | 0.090 / 0.18 | 0.079 / 0.16 | 0.109 / 0.22 |
| face mouth | 0.132 / 0.30 | 0.117 / 0.27 | 0.114 / 0.25 | 0.105 / 0.24 | 0.146 / 0.33 |
| hand MCP | 0.174 | 0.171 | 0.158 | 0.168 | 0.162 |
| hand IP / tips | 0.139 / 0.109 | 0.137 / 0.107 | 0.125 / 0.093 | 0.134 / 0.105 | 0.125 / 0.105 |
| palm | 0.304 | 0.299 | 0.275 | 0.293 | 0.295 |
| toe joints | 0.115 | 0.115 | 0.106 | 0.115 | 0.118 |

- **Face:** within the 0.25 ceiling everywhere. No compact-scale face deficiency, so **no face topology**.
- **Long fingers:** finer local support than Pipkin (edge / finger length: MCP 0.029 vs 0.032, tips 0.018 vs 0.021), with every finger station 3 / 2 loops. Long fingers create no density deficit.
- **Feet:** ankle / heel / forefoot are above the ceiling exactly as on Pipkin, Durrim and Marchfolk (the family base), with no station failing. No foot density is added.

**Deformation, v005 vs native (`unbranched/CG_def_v005_vs_native.json`).** No new class on any body:
- 18 / 18 poses on c1 / c2 and 15 / 15 key poses on 76 / 107.
- The only new self-intersection pairs are 3 axillary arm–trunk pairs in trunk twist on c1. That contact class is present on the c2 native (7 pairs) and the Pipkin natives.

## 3. Inheritance diagnosis (§7, §9) — `inheritance/durrim_pipkin_branch_on_cogling.json`

I applied the frozen branches unchanged as a diagnostic:

| Body | v005 thumb | Durrim v002 thumb | Pipkin v001 thumb |
|---|---|---|---|
| CG76H | FAIL 1 / 1 | PASS 3 / 3 | PASS 3 / 3 |
| CGJ7 | FAIL 1 / 1 | PASS (fallback) 3 / 3 | PASS (fallback) 3 / 3 |
| CGF91 c2 | FAIL 2 / 2 | PASS (fallback) 4 / 4 | PASS 4 / 4 |
| CG107 | FAIL 1 / 1 | PASS (fallback) 3 / 3 | PASS (fallback) 3 / 3 |

Every case has 0 crease poles.

**Answers to §7:**
- **Does v005 fail?** Yes, on every body.
- **Compact stature, long fingers, or both?** Compact stature. The failure is the same 1–2-ring MCP band as Pipkin. Long fingers do not move the thumb grid: the v005 thumb grid rows on CGJ7 are identical to Pipkin's.
- **Does an existing architecture solve it?** Both do, with no crease poles. Unlike Pipkin, Durrim's placement does not break Cogling c2.
- **Does 76 cm need a denser solution?** No.
- **Does c2 add a crease / hip interaction?** No. The hips are unchanged everywhere, so the Durrim c2 hip sector is **not** inherited.

**Neck.** It passes on v005 on every body, so the jaw–neck reroute is **not** inherited.

**Placement.** As §7 requires, I did not inherit the exact Durrim / Pipkin placement, and re-solved it on Cogling (§5).

## 4. Toe stations (§8, §17) — author-decision package `inheritance/CG_toe_author_decision_package.json`

**Raw.** The c1 bodies (76 / 91 / 107) fail `toe3_j1_l/r` and `toe4_j1_l/r`:
- `FAIL_LOOPS`, closed-ring fallback, 0 loops, **no crease poles**;
- c2 passes raw.

**Size-consistent diagnostic (`inheritance/cg_toe_station_diag.json`).** The toe probe's joint-spacing term is taken in reference units, so it is not double-scaled under D4. **0 failures on all four bodies.** This is exactly the frozen Pipkin case:
- same stations, same raw signature;
- size-consistent pass (Pipkin diag included in the package).

Frozen Durrim is the reason global D4 stays: the same correction would newly fail DU137C `toe1_j1`.

**Conclusion.** Validator geometry, not topology. Under §8 I did **not** relabel, did not change D4 and added no foot topology.

**Options for the author:**
- **A (recommended):** a Cogling-specific exception with the Pipkin scope rule. Bodies CG76H-NAT / CGJ7 / CG107-NAT; the four stations; the documented raw case plus a size-consistent pass. This gives adjusted 69 / 69 on all four.
- **B:** a single shared compact-race record naming Pipkin and Cogling.
- **C:** a global D4 amendment (would fail frozen Durrim; not recommended).
- **D:** foot topology (forbidden by §8).

## 5. MPFB_COGLING_COMPACT_BRANCH_v001 (§10) — `branch/`, `branch_gates/CG_branch_gates.json`

**Definition.**
- **File:** `branch/MPFB_COGLING_COMPACT_BRANCH_v001.json` (sha256 `75ed801f698e…`).
- **Content:** thumb MCP two-direction compact support only.
- **Not included:** neck, hip sector, toes or face.
- **Engineering:** the Durrim / Pipkin thumb architecture. Its face list is identical to frozen Pipkin v001, because the v005 thumb grid rows are the same.
- **Placement:** Cogling-specific. `cg_thumb_relax.py` runs a joint on-surface relaxation over CGJ7 / CGF91 / CG76H / CG107, warm-started from Pipkin as an engineering start only. 464 / 480 vertex placements differ from Pipkin. The S weights are Cogling-only (`be7902f9…`).

**Map and determinism.**
- 58,162 V / 58,160 Q (+320 / +320, thumbs only).
- V = S · V_v005 and M = S · M_v005, with ≤ 4 non-zeros per S row.
- The face list and S are identical on all four bodies. A definition rebuild and a re-application are bit-identical.

**Per-body gates:**

| Body | Firm (raw) | thumb_mcp l / r | T-4 branch: angle flags / > 4:1 / max | v005 faces replaced: angle flags | T-1/2 | T-3 | T-6 | T-7 | Contact new |
|---|---|---|---|---|---|---|---|---|---|
| CG76H | 65 / 69 (toes) | PASS 3 / PASS (fallback) 3 | 3 / 0 / 3.82 | 6 | PASS | −0.19 mm | 0.0007 mm | auth. 0.9931 (fixed-raster), scaled 0.998 | 0 |
| CGJ7 | 65 / 69 (toes) | PASS (fallback) 3 / PASS 3 | 3 / 0 / 3.82 | 6 | PASS | −0.23 mm | 0.0007 mm | PASS | 0 |
| CGF91 c2 | **69 / 69** | PASS 4 / 4 | 3 / 0 / 3.82 | 7 | PASS | 0.00 mm | 0.0006 mm | PASS | 0 |
| CG107 | 65 / 69 (toes) | PASS (fallback) 3 / PASS 3 | 3 / 0 / 3.82 | 6 | PASS | −0.26 mm | 0.0007 mm | PASS | 0 |

- **Integrity:** 1 component, 0 boundary / non-manifold / degenerate, normals outward.
- **Rest self-intersections:** unchanged against v005.
- **Body T-4 angle flags:** −3 to −4 against v005.
- **Neck and hips:** unchanged.
- **Body deviation:** p95 ≤ 0.12 mm, max ≤ 1.15 mm.
- **Density:** palm 0.299 → 0.264 % at 91 c1 (76 cm moves inside the 0.30 ceiling). Face, feet, MCP / IP / tips are unchanged.

## 6. Deformation (§18) — `branch_gates/CG_def_branch_vs_v005.json`

| Body | Branch vs v005 | Result |
|---|---|---|
| c1 CGJ7 | 18 poses | 13 identical; 5 same class |
| c2 CGF91 | 18 poses | 14 identical; 4 same class |
| 76 / 107 | 15 key poses each | 10 identical + 5 same class each |

**No new topology class** on any body.

**What the same-class differences are.** Self-intersection, fold and flip counts are identical to v005 in every pose; only joint-zone strain moves. In thumb opposition the strain p95 rises (e.g. 17.3 → 23.3 % at 91 c1) and the max falls. This is the same response as the frozen Pipkin branch (PK-NAT 21.6 → 29.6 %).

**Hands and feet.**
- No grip / fist collapse: the fist is unchanged against v005.
- Wrist / thumb web are same class.
- Long-finger folding is unchanged: finger topology is v005.
- Ankle and toe poses are identical to v005.

Board I shows the worst hand and foot poses.

## 7. Firewalls (§11–§16) — `firewalls/CG_firewalls.json`

Source readings (T-1 holds, so these are the production readings).

| Firewall | Result |
|---|---|
| §12 Pipkin overlap, 91 c1 (CGJ7 vs PK91) | **14 / 14:** less pelvis-led (3 / 3, −4.0 / −9.5 / −4.9 %), narrower core (crest −6.3, thorax −2.4, pelvic AP −6.9 %), finer femoral shaft (−12 %), distal arm / leg redistribution, longer fingers (+7.7 %), larger hand / arm (+8.1 %) |
| §12 Pipkin overlap, 107 (CG107 vs PK-NAT) | **14 / 14** |
| §12 c2 91 (CGF91 vs PKF91, diagnostic) | 13 / 14. The crest / thorax ratio is the §1 narrower-core inversion; every narrow-core breadth holds |
| §13 Durrim context (CG107 vs DU122C, **real height**, not equal-height) | **11 / 11.** Stature gap 15.0 cm. Durrim thorax +26 % broader / +30 % deeper, femoral shaft +29 %, knee / femur +44 %, shorter limbs; Cogling more distal (forearm / arm −12 % for Durrim) and longer-fingered |
| §14 adult vs child (CG76H vs CHILD1 ~1.5 y toddler) | **17 / 19 separating.** Adult head share 0.145 vs 0.194 (head 11.04 vs 14.72 cm) |
| §14 adult vs child (CGJ7 vs CHILD3 ~3 y) | **18 / 19** (0.130 vs 0.179) |
| §14 adult vs child (CGF91 vs CHILD3) | **18 / 19** (0.123 vs 0.179) |
| §15 Marchfolk normalized | **11 / 11** on 76, 91 c1, 91 c2 and 107. Not a uniform scale: distal redistribution, fine shaft, near-human totals |
| §16 hands hidden | vs Pipkin 11 / 11 at 91 c1 and 107, 10 / 11 c2 (the §1 reading); vs Marchfolk 5 / 5 |
| §16 head + hands + feet hidden | the same: core and limb rows alone separate |

Identity does not collapse to "long fingers". Board F shows CG76H's mature face against the toddler's large cranium, short face and large orbits. No feature was exaggerated.

## 8. Boards (`sheets/`)

| Board | Content |
|---|---|
| A | Central sources c1 / c2 on v005: front, 3/4, side, rear, face, hand, foot, pelvis |
| B | Compact topology: v005 thumb, Durrim v002 and Pipkin v001 (diagnostic, aspect classes), Cogling branch (rings), long-finger IP close-ups, toes, face density — per body |
| C | Bounds 76 / 91 c1 / 91 c2 / 107: whole body, face, hand, foot (branch realizations, not candidates) |
| D | Cogling vs frozen Pipkin RP4 at equal real height 91 / 107, ears flattened |
| E | Cogling 107 vs frozen Durrim 122 at real height |
| F | Adult vs child, 76 (critical) and 91 |
| G | Normalized vs Marchfolk |
| H | Hands hidden; head + hands + feet hidden |
| I | Branch deformation: fist, opposition, wrist flex, toe extension |

Board note: ear "hiding" is a harmonic fill and leaves a soft residual bump in the side views (Pipkin board method).

## 9. Immutables (`immutable_hashes.txt`)

**69 / 69 unchanged vs 9424c72.** The check covers:
- MPFB Family Base v005;
- the frozen Durrim RP4 branch and production files;
- all 12 `*_FREEZE.json` records (including Pipkin RP4) and the Skarn family freeze report;
- the frozen Pipkin RP4 production files and branch;
- the Pipkin sources;
- the Cogling sources (CGJ7 / CG76H / CG107 R-6 + builds; CG76-NAT provenance);
- COGLING_V1 and PIPKIN_V1.

## 10. Author decisions required

1. **Toe stations (§4):** choose A / B / C / D. A is recommended: a Cogling-specific record using the Pipkin scope rule.
2. **76 cm T-7:**
   - accept the scale-consistent silhouette reading (0.998) for the 76 cm body as validator geometry; or
   - keep T-7 at 3 px / cm and rule the 0.9931 profile IoU (identical on v005 and the branch; surface p95 0.09 mm) non-blocking.
3. **Confirm c2 (§1):** the 91 cm c2 crest / thorax narrower-core inversion against the diagnostic Pipkin c2 (+1.1 %) is acceptable. The narrow core, the other two §4B relations and every distal row hold.

On rulings 1–3 the next order can create `CG_M_REF_RP4_v001` (CGJ7) / `CG_F_REF_RP4_v001` (CGF91-NAT) on `MPFB_COGLING_COMPACT_BRANCH_v001`. No further topology work is indicated.

## 11. Not done (STOP)

- No production candidates and no freeze-candidate record.
- Nothing frozen.
- Pipkin exception not applied; global D4 unchanged.
- Frozen Pipkin / Durrim untouched.
- No Saurin, rig, creator, UE5, materials, hair or clothing.

**STOP FOR CHATGPT REVIEW.**

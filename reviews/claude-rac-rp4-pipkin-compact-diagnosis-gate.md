# Claude Gate — RAC RP4 Pipkin Independent Compact Diagnosis / Production Gate

**Order:** `reviews/chatgpt-rac-rp4-pipkin-independent-compact-diagnosis-order.md` (25f7ba0; prior state f9b1040)
**Date:** 2026-10-30
**Evidence:** `reviews/rac-rp4-evidence/pipkin/`
**Tools:** `tools/rac/rp/pipkin_rp4_v001/`

## Result

**PIPKIN RP4 REQUIRES AUTHOR DECISION — toe 3 / toe 4 MTP validator stations fail on configuration 1 from D4 double-scaling of the toe probe radius (validator geometry, not topology)**

Everything else is ready:
- **c2 anchor:** PKF107-NAT passes.
- **Thumb gap:** the real Pipkin thumb-MCP gap is fixed by a Pipkin-specific branch, `MPFB_PIPKIN_COMPACT_BRANCH_v001`.
- **c2 validator:** configuration 2 is **69 / 69**.
- **Remaining c1 failures:** only `toe3_j1_l / r` and `toe4_j1_l / r` on PK91 / PK107, and `toe3_j1_l / r` on PK122, against the unchanged authoritative validator.
- **The toe failures are validator geometry.** With a probe of the same relative size as Marchfolk's, every Pipkin toe station passes on the same topology (§4).
- **The validator was not changed and no topology was added to satisfy it.** That choice is the author's (§10).

| Gate | c1 PK107 | c2 PKF107 | 91 | 122 |
|---|---|---|---|---|
| Validator (D1 + D3 + D4 + D5 + D6, unchanged) | 65 / 69 | **69 / 69** | 65 / 69 | 67 / 69 |
| Remaining failures | toe3_j1 ×2, toe4_j1 ×2 | — | toe3_j1 ×2, toe4_j1 ×2 | toe3_j1 ×2 |
| Same bodies with a size-consistent toe probe (diagnostic) | 69 / 69 | 69 / 69 | 69 / 69 | 69 / 69 |

No production candidates (`PK_M/F_REF_RP4_v001`) and no freeze candidate were written (order §16: only if all gates pass). They can be written directly from the branch once the author rules.

## 1. Sources and configuration-2 anchor (§3, §4)

**Regeneration.** PK91-NAT, PK-NAT and PK122-NAT regenerate exactly: geometry identical, max dV 0.0. Their r6 sha256 values equal the order values (`regen/`, `immutable_hashes.txt`).

**PKF107-NAT** (`partA/`):
- **Construction:**
  - MPFB configuration-2 base macro 0.60595703125 (the MF-F-R route, as DUF137C);
  - the exact PK-NAT targets;
  - bone scales pelvis [1, 1.06, 1] and spine_01 [1, 0.9, 1];
  - girth β 1.0;
  - neutral age, muscle, weight and proportions;
  - no Pipkin sex shift.
- **Stature and determinism:** stature 107.000 cm; a second rebuild is identical (dV 0).

**Validation (`partA/PK_partA.json`).** This uses the accepted W2H comparator rule: Pipkin is read as normalized ratios against Marchfolk 173 (MF-M-R for c1, MF-F-R for c2). It is never compared with a same-height human.

| RM-SR-01 relation (canon) | c1 PK107 | c2 PKF107 | PK91 | PK122 |
|---|---|---|---|---|
| torso share < MF (T-2) | −3.87 % | −3.91 % | ✓ | ✓ |
| skeletal pelvic vertical / stature ≥ MF (PK-P3) | +5.34 % | +5.22 % | ✓ | ✓ |
| pelvic vertical / thoracic vertical > MF (PK-P3) | +10.45 % | +10.83 % | ✓ | ✓ |
| crest / thoracic breadth > MF (PK-P5) | +6.3…+6.8 % | +10.8…+11.6 % | ✓ | ✓ |
| pelvic AP / thoracic depth > MF (PK-P4) | +4.4…+5.0 % | +6.1…+7.0 % | ✓ | ✓ |
| waist interval / torso < MF (PV-D15) | −5.54 % | −3.35 % | ✓ | ✓ |
| leg share ≤ MF (PK-P2a) | −0.17 % | −0.13 % | ✓ | MARGINAL (accepted AD-G10 class, as W2H) |

**Verdict: PIPKIN CONFIG-2 CENTRAL REFERENCE PASS — READY FOR PRODUCTION DIAGNOSIS.** All 7 relations hold on c2, and c2 matches c1 on all 7.

**Sex consistency (report).** I compared c2 / c1 for Pipkin against c2 / c1 for route-matched Marchfolk (MF107 / MFF107). 13 of 17 readings agree within 1.5 %. The four outside are generator responses to the same inputs, not an authored shift:
- crest / thorax −3.7 points;
- waist interval +2.4 points;
- thoracic breadth +3.2 points;
- ankle +5.3 points.

They most likely come from Pipkin's accepted girth β 1.0 against the generator allometry on the Marchfolk route. All PK-P directions still hold on c2, and c2 is the more pelvis-led of the two. Pipkin sex-related anatomy stays OPEN.

## 2. Phase A — unbranched MPFB Family Base v005 (§5, §6)

`unbranched/`. Propagation follows Standard v1 from the committed v005 core and hm08 map, with no topology edits.

| Body | Firm | Failures | Integrity | T-1 / T-2 / T-3 / T-7 | Contact new |
|---|---|---|---|---|---|
| PK91 | 63 / 69 | thumb_mcp ×2 (1 ring), toe3_j1 ×2, toe4_j1 ×2 (0 rings) | clean | PASS | 0 |
| PK107 c1 | 63 / 69 | same | clean | PASS | 0 |
| PKF107 c2 | **69 / 69** | — (thumb_mcp margin 0) | clean | PASS | 0 |
| PK122 | 65 / 69 | thumb_mcp ×2 (2 rings), toe3_j1 ×2 | clean | PASS | 0 |

- **Neck:** PASS on every body, so no jaw–neck failure exists. At 122 cm the submandibular pole pair is within 2 h of the band but not in the crease band.
- **Hip:** margin 0 on c1, PASS.
- **Density (§6, `PK_density_compare.json`):**
  - Face / hand / foot zone means are 0.152–0.166 / 0.136–0.152 / 0.195–0.207 % of stature, all within the §8 ceilings.
  - Orbit 0.100–0.109 %, mouth 0.133–0.146 % and MCP / IP / tip support are adequate.
  - The jaw-hinge sub-zone (0.32–0.44 %) is the same stature-sensitive watch item as Durrim; it is not a branch trigger.

## 3. Durrim v002 inheritance test (diagnostic only, §7)

`durrim_v002_diagnostic/`. The frozen `MPFB_COMPACT_BRANCH_v002` was applied unchanged and read with the authoritative validator.

| v002 component | On Pipkin | Ruling |
|---|---|---|
| Thumb MCP two-direction architecture | Fixes c1 thumbs (3 / 3 / 4 rings at 91 / 107 / 122). **Breaks c2:** a Durrim-placed transition pole sits in Pipkin's c2 thumb crease band (FAIL_CREASE_POLE), where v005 passed. 3 quads > 4:1. | **Concept: yes. Durrim placement: no.** Re-solved on Pipkin bodies (§5). |
| Jaw–neck reroute | Pipkin has no neck crease-pole failure | **Not inherited** |
| c2 unsplit hip sector | Pipkin bodies show no hand / hip-slab geometry (no thumb row within any hip slab) | **Not inherited** |

## 4. Toe 3 / 4 MTP failure — diagnosis (§14 "diagnose before editing topology")

**Probe sides collapse.** On c1 all four band probes of `toe3_j1` / `toe4_j1` are "merged" (both endpoints land on nearby vertices). The closed-ring fallback finds no ring within the probe radius. c2's slightly different foot leaves enough room.

**Cause: the probe radius is double-scaled under D4.**
- core3lib builds the toe probe from the body's own toe-joint spacing: rr = 0.5 |JC(j+1) − JC(j)| + 0.6 cm.
- On a short body that spacing is already stature-sized, and D4 then multiplies rr by s = stature / 173.143 again.
- For Pipkin 107 (s = 0.618), the probe radius relative to the body is 22 % smaller than Marchfolk's (1.65 vs 2.11 in stature-normalized units).

**Test (`durrim_v002_diagnostic/toe_station_diag.json`).** I re-ran only the toe stations with the joint-spacing term taken in reference units, so the probe is the same size relative to the body as on Marchfolk. The authoritative validator was not changed.

| Body | Authoritative toe failures | Size-consistent probe |
|---|---|---|
| PK91 / PK107 / PK122 | 4 / 4 / 2 | **0 / 0 / 0** |
| PKF107 c2 | 0 | 0 |
| MF-M-R v005 | 0 | 0 |
| **DU137C (frozen Durrim)** | 0 | **toe1_j1_l / r FAIL** |

**Conclusion.** The Pipkin toe failures are validator geometry, not missing topology. The same v005 toe topology passes with a size-consistent probe.

Correcting the probe is not neutral either: it would newly fail frozen Durrim's toe-1 MTP. So I neither changed the validator nor added foot topology to satisfy it; this needs an author ruling (§10).

## 5. MPFB_PIPKIN_COMPACT_BRANCH_v001 (§8)

**Definition and engineering.**
- **Definition:** `branch/MPFB_PIPKIN_COMPACT_BRANCH_v001.json` (sha256 `ff16400f…`).
- **Engineering reused from Durrim v002:** the two-direction architecture (×2 circumferential, ×3 axial in B→C), 2:1 fans only in the full-height P→Z / C→D strips, fan phases off the existing poles and UV seams, and seam-aware UVs.
- **Pipkin-specific:** no unsplit sector; every vertex re-placed by a joint on-surface relaxation over PK-NAT / PKF107 / PK91 / PK122.

**Placement constraints, measured on Pipkin's own bodies:**
- counted rings B / T1 / T2 inside the validator window and radius;
- transition poles outside the thumb crease band and outside every non-digit station band;
- fold guard on every quad normal;
- seams pinned.

**Not included:** a neck reroute, a hip sector or toe topology.

**Counts and map.**
- 58,162 V / 58,160 Q (+320 / +320 vs v005, thumbs only).
- V = S · V_v005 and M = S · M_v005, with ≤ 4 non-zeros per S row.
- v005 vertex order is preserved and new vertices are appended.
- **Determinism (`PK_determinism.json`):** identical face list and identical S on all four bodies; two rebuilds are bit-identical.

**Per-body gates (`branch_gates/`):**

| Body | Firm | thumb_mcp l / r | T-4 branch: angle flags / > 4:1 / max aspect | v005 faces replaced: angle flags | T-1 / T-2 / T-3 / T-7 | T-6 max | Contact new |
|---|---|---|---|---|---|---|---|
| PK91 | 65 / 69 (toes) | PASS 3 / 3 | 4 / 0 / 3.84 | 6 | PASS | 0.10 mm | 0 |
| PK107 c1 | 65 / 69 (toes) | PASS 3 / 3 | 4 / 0 / 3.84 | 6 | PASS | 0.12 mm | 0 |
| PKF107 c2 | **69 / 69** | PASS 4 / 4 | 4 / 0 / 3.84 | 6 | PASS | 0.12 mm | 0 |
| PK122 | 67 / 69 (toes) | PASS 4 / 4 | 4 / 0 / 3.84 | 6 | PASS | 0.13 mm | 0 |

- **Integrity:** 1 component, 0 boundary / non-manifold / degenerate.
- **Rest self-intersections and body T-4 totals:** unchanged.
- **Density:** the thumb-base palm sub-zone is 0.289 → 0.256 % at 107 c1 and 0.267 → 0.235 % at c2. MCP / IP / tips, face and feet are unchanged.

## 6. Deformation (§15)

`unbranched/deformation/`, `branch_gates/deformation/`, board H. The full 18-pose Standard v1 suite was run on c1 / c2 (native, v005, branch). The 11 key poses were run on 91 / 122 (v005, branch).

| | Result |
|---|---|
| c1 PK107 | all 18 poses identical to v005 (self-intersections / folds / flips) |
| c2 PKF107 | 17 / 18 identical. thumb_opposition shows 54 vs 44 self-contact pairs; all 54 map to existing v005 contact at the same place (0 unmatched, `PK_def_c2_opposition_match.json`): the same thumb–palm contact counted on finer faces |
| PK91 / PK122 | thumb opposition, fist, wrist flex / ext, hip flex, knee 140, ankle, toes, neck: identical to v005 |

There is no new topology class and no grip / fist collapse; neck poses are 0 / 0 / 0.

## 7. Anatomy and firewalls (§9–§13) — `PK_firewalls.json`

The branch only re-samples the v005 surface (T-1 / T-2 pass), so source readings are the production readings.

**§9 Pipkin anatomy:** RM-SR-01 holds as in §1 (low-set compact trunk, pelvis-led, compact waist). Limbs are adult; joints are lighter than Durrim (below).

**§10 PK122 vs DU122 at real height (W2H §4A carriers): 16 / 16.**

| Carrier | Durrim vs Pipkin |
|---|---|
| thorax depth / breadth (skeletal) | +26…+29 % / +22…+24 % |
| torso share | +8.1 % |
| arm / leg share | −3.8 / −3.5 % |
| crest / thorax (Durrim thorax-led) | −8.7…−9.3 % |
| pelvic vertical / thoracic vertical | −22.9 % |
| neck | −15.2 % |
| femoral shaft | +13…+15 % |
| wrist / knee / ankle / elbow | +34 / +24 / +6 / +22 % |
| hand share | +9.3 % |
| palm breadth / stature | +8.7 % |
| foot breadth / stature | +11.0 % |

- **Report only:** palm breadth / hand −0.5 % and foot share −1.1 %. Pipkin's foot is relatively long (the "somewhat substantial" foot); Durrim's is broader.
- **Broad Pipkin vs Narrow Durrim:** the W2H frame bodies are not committed reference assets, so per §10 they were not rebuilt. The accepted W2H result stands: PIP-BODY-14, 16 / 16 + 2 REPORT.

**§11 Adult vs child.** The proxies are generator human-child bodies (age macro (y − 1) × 0.01875; stature re-solved), diagnostic only. They reproduce W2H's head shares (0.165 / 0.179).

| Pair | Body readings separating ≥ 1 % | Head share adult / child |
|---|---|---|
| PK107 vs CHILD6 (~6 y) | 17 / 19 | 0.151 / 0.165 |
| PKF107 vs CHILD6 | 18 / 19 | 0.145 / 0.165 |
| PK91 vs CHILD3 (~3 y) | 19 / 19 | 0.159 / 0.179 |

No feature was enlarged to pass. Head share is allometry only.

**§12 Marchfolk normalized:** 7 / 7 RM-SR-01 relations on c1, c2 and 91; 6 / 7 at 122 (the accepted leg-share MARGINAL). Board F shows each body at equal display height.

**§13 Cogling context (W2H §4B carriers):** PK91 vs CGJ7 **11 / 11**, PK107 vs CG107 **11 / 11**.
- Pipkin is more pelvis-led, has a heavier femoral shaft and joints, and keeps its limbs proximal.
- Cogling is distal: forearm / arm and hand / arm are larger, upper arm / arm and femur / leg smaller.

**Blind visual review (independent reader, boards D–G).**
- **Adult head read:** clearly adult vs the child proxies (longer face, longer lower face, less domed skull).
- **No caricature crutch:** PASS.
- **Body-only at 107, Durrim / Pipkin at 122 and Pipkin / Cogling:** BORDERLINE. The reader saw the differences side by side but called them subtle (Durrim broader and deeper in the chest; Cogling narrower-headed with a narrower pelvis).
- **Pipkin vs normalized Marchfolk:** BORDERLINE ("not quite a uniform shrink", head relatively larger, less lean).

All numeric firewalls pass. The visual subtlety is the accepted W1 / W2H source anatomy, the same class as the accepted Durrim 152 cm note, and is raised for author attention. The artefacts the reader noted (mouth-corner seam, empty eye openings, faceted outlines on the r6 renders) are source / v005 properties, unchanged by the branch.

## 8. Boards (`sheets/`)

| Board | Content |
|---|---|
| A | central sources c1 / c2 on v005 |
| B | thumb: v005 / Durrim v002 diagnostic / Pipkin branch (aspect classes, counted rings), plus v005 toes |
| C | branch realizations c1 / c2 (not production candidates) |
| D | 122 cm Pipkin vs Durrim |
| E | adult vs child (ears hidden) |
| F | normalized vs Marchfolk |
| G | Pipkin vs Cogling |
| H | deformation close-ups |

## 9. Immutables (`immutable_hashes.txt`)

33 / 33 unchanged vs 25f7ba0. This covers:
- Pipkin, Marchfolk, Cogling and Durrim sources;
- the v005 map / core;
- the frozen Durrim branch and blends;
- all `*_FREEZE.json`.

Frozen Durrim and v005 are untouched.

## 10. Author decision required

**Toe 3 / 4 MTP stations on Pipkin configuration 1.** Choose one:

- **(A) Record a Pipkin toe-station validator-geometry exception (recommended).**
  - Accept `toe3_j1` / `toe4_j1` on c1 as passing under a documented D4 probe-scaling exception, with the size-consistent probe as the evidence (0 failures).
  - No topology change and no validator change for other races.
  - Production candidates `PK_M/F_REF_RP4_v001` can then be written from `MPFB_PIPKIN_COMPACT_BRANCH_v001` as-is.
- **(B) Amend D4 for toe probes** (scale only the constant term).
  - This changes the authoritative validator for every race.
  - It newly fails frozen Durrim `toe1_j1`, so it needs a full re-check of the frozen races. Not recommended inside this order.
- **(C) Authorize a Pipkin foot-zone support patch** to satisfy the unchanged probe.
  - This adds topology the anatomy does not need, and its effectiveness is not established (the failure is probe-size-driven).

Also for author attention:
- the blind visual-distinctness notes in §7 (source anatomy, accepted);
- the four sex-consistency residuals in §1 (Pipkin sex anatomy stays OPEN).

## 11. Not done (STOP)

- No production candidates and no freeze.
- No validator change and no foot topology.
- No Cogling, Saurin, rig, creator, UE5, materials, hair or clothing.
- Frozen Durrim and v005 untouched.

**STOP FOR CHATGPT REVIEW.**

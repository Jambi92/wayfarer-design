# RAC RP3 — Vael bounded body-source correction + craniofacial source gate

**Date:** 2026-10-28
**Order:** `reviews/chatgpt-rac-rp3-vael-body-face-source-order.md`
**Parent gate:** `reviews/claude-rac-rp3-vael-body-face-ear-gate.md` (0df5739)
**Evidence:** `reviews/rac-rp3-evidence/vael_rp3_source/` (25 sheets in `sheets/`)
**Tools:** `tools/rac/rp/vael_rp3_v001/`:
- `probe_va2.sh`, `va2_eval.py`, `va2_probe_matrix.py`;
- `build_vb.sh`, `build_va_r1.sh`, `skp_va2.sh`, `va2_pelvis.py`, `va2_sheets.py`;
- `run_va_prod.sh` and `va_manifest.py`, now parameterised for R1 / v002.

## RESULT — VAEL BODY NEEDS REVISION / FACE PASS — VB2 + VC2 is the recommended provisional source — ears stay LOCKED

| | c1 (VAL4-R1) | c2 (VALF178-R1) |
|---|---|---|
| Hip-joint ordering MF < Vael < Aelari < Fenn (VA-P2a, skeletal proxy) | **holds**: +0.10 / −0.11 / −2.38 % | **holds**: +0.05 / −0.29 / −2.45 % |
| VA-P6 waist interval / torso < Aelari | **holds**: −1.41 % (skin), −1.56 % (proxy) | **holds**: −0.25 % (skin), −0.29 % (proxy) |
| Pelvis hard gate (gating rules, all t) | **9 / 9** | **9 / 9** |
| Body canon rows | 18 / 19 | 18 / 19 |
| Body systems departing materially from humans | **4 / 8** (ribcage, foot base, pelvis/hip, shoulder/neck) | **4 / 8** (same) |
| Face systems departing materially from MF (§13) | **6 / 6** | **6 / 6** |
| Face canon vs Aelari / Fenn | 9 / 9 | 9 / 9 |
| v005 propagation | 57,842 V / 57,840 Q; face hash, map and UV identical | same |
| D1–D6 validator | **69 / 69** | **69 / 69** |
| T-1 / T-2 / T-3 / T-7 | pass | pass |
| Density, face rings | pass | pass |
| New contact failures | 0 | 0 |
| Deformation flip excess vs MF v005 | 3 | 1 |
| Read-back | byte-identical | byte-identical |

The canon-row miss in both configurations is the composite "central vertical < Aelari" row; §3 shows it cannot hold under the rest of the canon.

**Why "body needs revision":** every numeric body gate passes. The visual check does not.
- At equal height with ears hidden, the Vael body still reads as Marchfolk (sheets 02, 25).
- In the silhouette overlay the two bodies coincide almost everywhere.
- The four material systems are real but small: thorax depth +5.5 %, neck breadth +3.4–4.0 %, foot breadth +6.6–7.7 %, pelvic depth +2.3 %.
- Order §7 asks for a body that is "no longer visually reducible to a normal human body", and §6 says "do not choose by metrics alone".

On that standard the §14 human firewall does **not** pass. Ears therefore stay locked (§19, items 3 and 5).

**Why "face pass":** the §13 gate is met in both configurations.
- 6 / 6 systems depart materially from Marchfolk in the intended direction.
- The face is distinct from both frozen elves on all 9 canon rows.
- No eye or orbit feature carries the identity: the orbit region stays at 0.5 mm.
- Caveat on magnitude: the Vael face departs from Marchfolk by 1.14 mm whole-face RMS, versus 2.38 mm for Fenn and 2.61 mm for Aelari (`VA2_face_departure_scale.json`). It reads as Vael next to the elves, but only moderately non-human next to Marchfolk (sheets 12, 13).

## 1. Source probes and architecture

### Probe matrix

There are 16 body probes and 26 face probes, all on the VAL4 record with the height macro held. Files: `probe/probe_matrix.json` and `probe/probe_eval.json.gz`. The choices they drove:

**Body**
- Pelvis bone Y scale raises the hip-to-crest relationship without shortening the legs: 1.03 gives leg −0.16 %, waist interval −0.56 %, torso +0.40 %.
- `torso-scale-depth-incr` drives ribcage depth.
- `neck-scale-horiz-incr` drives shoulder–neck integration.
- `foot-scale-depth-incr` strengthens the foot base.

**Face**
- `head-oval` moves the cranium and the compact face together.
- `chin-height-decr` compacts the lower face.
- `cheek-inner-incr` adds mid-face depth.
- `cheek-trans-up` places the cheekbones.
- `head-scale-horiz-incr` broadens the cheeks.
- `head-diamond` makes the lower face gracile.
- Eyebrow translation sets the brow.

### Body correction (one architecture, identical on c1 / c2, stature re-solved)

| Component | VB1 | VB2 | VB3 |
|---|---|---|---|
| Pelvis bone scale (ordering + continuity) | [1.02, 1.045, 1.03] | same | same |
| Thigh / calf Y vs VAL4 | × 0.9975 | same | same |
| `torso-scale-depth-incr` | 0.18 | 0.25 | 0.33 |
| `neck-scale-horiz-incr` | 0.08 | 0.20 | 0.32 |
| `foot-scale-depth-incr` | 0.04 | 0.06 | 0.08 |

The order ruled out uniform leg shortening, pelvis truncation, whole-pelvis translation and configuration hacks; none is used. The thigh / calf × 0.9975 is a 0.25 % shared trim that centres the sub-1 % window.

**Iterations** (all in `vb_vc_definitions/`, every build record in `build_records/`):

| Iteration | Change | Why |
|---|---|---|
| VB1–3 (first pass) | pelvis Y 1.06 | Under-shot the foot share on c1 |
| VB2f | pelvis [1.02, 1.045, 1.03], foot depth 0.06 | Fixed foot share |
| VB2g (final) | limb trim × 0.996 → × 0.9975 | Moved the c2 hip margin over MF from +0.004 % (a tie) to +0.05 % |

### Face (VC) architecture

VC2 is:
- `head-oval` 0.15
- `forehead-scale-vert-incr` 0.03
- `head-scale-horiz-incr` 0.06
- `chin-height-decr` 0.20
- `cheek-inner-incr` 0.35
- `cheek-trans-up` 0.80
- `eyebrows-trans-backward` 0.015
- `chin-bones-incr` 0.30
- `head-diamond` 0.12

VC1 and VC3 are exactly 0.6× and 1.4× VC2: same keys, same signs, magnitude only. The face was built on the existing topology with no topology branch.

**Iterations:**

| Iteration | Problem found | Fix |
|---|---|---|
| 1 | Cheekbone height went the wrong way; cranium went above Aelari | Iteration 2 |
| 2 | 6 / 6, but the brow came out 10–27 % heavier than both humans | Iteration 3 |
| 3 (final) | — | Brow term reversed: Vael brow is now 4.5 / 7.9 % stronger than Aelari and 1.3 / 2.7 % lighter than humans (no scowl, no heavy human brow) |

**Author decision A.** The "intended direction" of the orbit/brow system against humans is taken as *lighter than humans*. "Stronger than Aelari" stays a separate canon row. If the author wants a brow heavier than humans, it is a one-term sign change.

### Selection (§12)

1. VB2 was selected provisionally.
2. VC1 / VC2 / VC3 were applied to it.
3. The body moved VB2f → VB2g, so VC2 was re-applied to the final body (VB2g + VC2 = R1).
4. VB1 + VC2 and VB3 + VC2 were also built.

Provenance is explicit in the build records.

| Candidate (c1 / c2) | Canon | Body systems (strong) | Face systems | Elf rows | Notes |
|---|---|---|---|---|---|
| VB1 + VC2 | 18 / 18 | 4 (3) / 4 (3) | 6 / 6 | 9 / 9 | Weakest body |
| **VB2 + VC2 = R1** | 18 / 18 | 4 (4) / 4 (3) | **6 / 6** | 9 / 9 | Recommended |
| VB3 + VC2 | 17 / 18 | 4 (4) / 4 (3) | 5 / 5 | 9 / 9 | Thorax +7.3–7.6 % (toward a barrel chest); neck target over-widens the jaw (mandible fails); c1 joints no longer gracile |
| VB2 + VC1 | 18 / 18 | 4 / 4 | 4 / 5 | 9 / 9 | Borderline (expected for a restrained candidate) |
| VB2 + VC3 | 18 / 17 | 4 / 4 | 6 / 6 | 8 / 8 | Head growth breaks the hip window on c2 (−0.02 % vs MF); cranium above Aelari |

VB3 is not visibly more elven than VB2 (sheet 01), which shows VB2 is not under-powered **on this target architecture**. More strength from the same targets pushes into the guard rails: barrel chest, heavy neck and jaw. VC3 shows the same limit for the face.

## 2. Body gate

### Against humans (Marchfolk / Sagekin)

Material means ≥ 1 % and beyond the Sagekin–Marchfolk difference in the Vael direction. Region RMS ≥ 1.25× the SG–MF baseline also counts.

| System | Result |
|---|---|
| Ribcage | Thorax depth / stature +5.5 / +5.7 % vs MF (human variation 3.0 / 3.8 %). Material. |
| Foot base | Foot breadth / length +7.7 / +6.6 %. Material. |
| Pelvis / hip | Pelvic AP depth (skin) +2.3 / +2.4 %. Material. |
| Shoulder / neck | Neck breadth / shoulder-joint breadth +3.4 / +4.0 %. Material. |
| Torso continuity | Not material. |
| Limb share | Not material. The leg is pinned by the 0.2–0.3 % MF–Aelari hip window; arm +0.9–1.0 % is inside human variation of 2.5 %. |
| Joints | Not material. The canon window between Aelari (joint mean −2.1 %) and Sagekin (−1.5 %) is narrower than the human variation. |
| Hand base | Not material. |

The original VAL4 had 2 / 8 (ribcage and foot base on c1; foot base and pelvis/hip on c2), so separation is measurably improved. Region RMS against Marchfolk stays below the Sagekin–Marchfolk RMS for trunk, arm, hand and leg. Only foot and neck exceed it (sheet 10).

**Visually** (sheets 02, 25), the Vael body at equal height is hard to tell from Marchfolk. The changes are depth changes, which do not show in a frontal silhouette.

### Against Fenn / Aelari — holds

- Thorax depth +11 / +13 % vs Fenn and +13 / +14 % vs Aelari.
- Torso share > Fenn.
- Extremity share < Fenn.
- Elbow, wrist, knee and ankle presence all > Fenn and > Aelari.
- Palm breadth > both.
- Foot breadth +14–22 %.
- Leg and arm share < both.
- Visually distinct (sheets 03, 25).

### Composite "central vertical < Aelari" — cannot hold under the canon

The stature partitions as hip-joint height + torso + neck + cranial + rest (the face below the outer canthus) = 1. Therefore:

> central(VA) − central(AE) = [leg(AE) − leg(VA)] + [rest(AE) − rest(VA)]

The canon requires leg(VA) < leg(AE) (VA-P2a). It also requires a craniofacial build more compact than Aelari, so rest(VA) < rest(AE). Both brackets are then positive, and the central share must exceed Aelari's. Measured excess: +0.31 % (c1) and +0.49 % (c2).

The component reading carries "less vertically elongated than Aelari":
- neck share −3.6 / −2.3 % vs Aelari;
- cranial share −0.65 / −0.46 %;
- waist interval / torso −1.4 / −0.25 %.

The torso share is +1.3 % above Aelari, because the corrected R1 Aelari keeps its verticality in head and neck, not torso. Its torso share (0.2777) is below Marchfolk's (0.2825).

**Author decision B:** retire this composite row in favour of its components plus VA-P6, or rule otherwise. Evidence: `VA2_vertical_partition.json`, sheet 07.

## 3. Pelvis hard gate (§8) — skeletal proxy, t = 0 / 0.5 / 1.0 cm

| Rule | c1 | c2 |
|---|---|---|
| VA-P2a > MF | +0.099 % | +0.054 % |
| VA-P2a < Fenn | −2.38 % | −2.45 % |
| VA-P2a < Aelari | −0.114 % | −0.289 % |
| VA-P2b bitroch / crest ≥ MF | +0.41 % | +0.44 % |
| VA-P3 no vertical iliac elongation (< Aelari) | −6.9 % | −6.7 % |
| VA-P4 AP depth > Fenn | +2.4 % | +2.8 % |
| VA-P4 AP depth > Aelari | +2.8 % | +4.1 % |
| VA-P4 AP depth ≈ MF | +2.7 % | +2.6 % |
| VA-P6 | −1.56 % | −0.29 % |

All 9 gating rules hold at every t on both configurations. Alignment residual is 0.08 / 0.35 cm.

**Margins, honestly classified (VA-P2a):** the sign is correct everywhere, but all three margins are below 1 %.
- The c2 margin over MF is 0.054 % (≈ 0.1 cm at 178 cm).
- The c1 margin under Aelari is 0.114 %.
- Both are inside a window the order itself calls sub-1 %. They are true signs on deterministic builds, not resolved anatomical differences.

**Report-only construction proxies** (VA-P2c / VA-P3 presence; no accepted numeric proxy):
- Hip-joint scale is > Fenn and Aelari but not gracile vs MF: +0.45 % on c1, +25 % on c2. The c2 figure is a known MFF178 trochanter-detection artefact and was identical before the correction.
- Iliac structural presence is > Fenn and Aelari, but is **not lighter than MF** (+3.9 %). It was already +3.6 % on the accepted VAL4, so the correction did not create it. Visually (sheet 06) the pelvis reads within the human envelope.

**Author decision C:** whether "lighter than MF" needs a numeric proxy. If it does, it conflicts with VA-P4 (AP depth ≥ Fenn / Aelari ≈ MF) unless the crest is narrowed.

## 4. Face gate (§13) — ears collapsed, neutral grey, similarity-aligned

Departures are vs Marchfolk, c1 / c2. The human baseline is ≤ 0.6 % on every descriptor.

| System | Descriptor(s), vs MF | Region RMS vs MF (SG–MF) | vs Aelari / Fenn |
|---|---|---|---|
| 1 Cranial / shared elven | Cranial height / face +4.1 / +4.2 %; cranial height / stature +2.5 / +2.6 % | Cranium 1.67 mm (0.03) | Cranial / stature −0.56 / −0.34 % vs Aelari (compact) |
| 2 Compact vertical | Face height / bizygomatic −4.6 %; lower face / HH −3.6 / −3.7 % | Jaw–chin 1.41 mm | Face height / bizygomatic −11 % vs Aelari |
| 3 Cheek / mid-face | Bizygomatic / HH +2.7 %; cheekbone height +1.1 / +1.2 % | Cheeks 2.73 mm (0.02) | +8.9 % vs Aelari |
| 4 Mid-face depth | Projection / HH +4.0 / +4.1 % | Cheeks | +12.5 / +13.1 % vs Aelari |
| 5 Orbit / brow | Brow −1.3 / −2.7 % (lighter than humans) | Orbit 0.5 mm (not material) | +4.5 / +7.9 % vs Aelari |
| 6 Mandible | Lower-face width / bizygomatic −1.5 % (gracile); jaw width +0.43 / +0.72 % (not material) | Jaw–chin 1.41 mm | Jaw +4.8 / +5.7 % vs Aelari, +2.8 / +3.5 % vs Fenn |

**Mandible note.** The jaw-width descriptor is pushed up by the body's neck target:
- VB2 body alone measures +2.9 / +3.2 %;
- the VC2 face takes it back down by about 2.5 %;
- the gonion landmark sits on the neck–jaw transition.

So the strict hidden-ear guard "jaw not heavier than both humans" misses by 0.43 / 0.72 %, which is not material. A stronger `head-diamond` (0.24) only reached +0.12 / +0.39 %, so it was not adopted. The brow guard holds.

**Caricature check** (sheets 11–17): no nose or mouth stereotype (the nose and mouth regions stay at 0.26–0.28 mm), no scowl, no giant eyes. Eye scale is the unchanged VAL4 value. No low-light physiology was added. VC3 is still humanoid, but it over-grows the head.

**Distinct from the frozen elves:**
- Vael vs Aelari region RMS is 3.2–4.9 mm.
- Vael vs Fenn is 2.1–3.5 mm.
- Vael is compact, broad-cheeked and deep through the mid-face. Aelari is vertical and narrow. Fenn has the CF2 cranium.

**Scale caveat:** the Vael whole-face departure from MF (1.14 mm) is about 45 % of Fenn's (2.38) and Aelari's (2.61). The SG–MF face baseline is only 0.02 mm, because the two human families share one face, so "beyond human-family variation" is a low bar.

## 5. Firewalls

**Human firewall (§14) — NOT PASSED.** With ears, pigmentation, hair, culture and low-light presentation removed:
- the head reads as a compact, broad-cheeked face that is related to the elves;
- the body reads as Marchfolk.

Together, the source does not yet carry Vael ancestry strongly enough. Ears stay locked.

**Three-elf firewall (§15) — PASSED.**
- Fenn: extremity-led and shallow-torsoed.
- Aelari: vertical, with gracile joints.
- Vael: deep-chested and compact, with more joint and base presence and a compact, deep-mid-face head.

They read as related without being copies (sheets 03, 13, 25).

## 6. Propagation, integrity, expressions

- **Production files** (v005 unchanged, PROVISIONAL, not frozen):
  - `VA_M_REF_RP3_bodyfam_v002` (sha 7bb7d70b…, from VAL4-R1)
  - `VA_F_REF_RP3_bodyfam_v002` (sha 8fdbfece…, from VALF178-R1)
- **Topology:** face list, UV, hm08 map and face-topology hash are identical to v005, with |V − M·hm08| = 0.
- **Validator and anatomy:** D1–D6 69 / 69 on both (sheet 22). T-1 / T-2 / T-3 / T-7 pass.
- **Density:** 9 zones pass (sheet 23).
- **Face rings:** mouth 37 / 33, orbit 43 / 43, no poles at the mouth corners.
- **Integrity:** 1 component, no boundary, non-manifold or degenerate geometry; normals outward.
- **Contact:** source-inherited (68 / 126), with 0 new contacts. v001 had 66 / 122.
- **Deformation:** worst flip excess vs MF v005 is 3 / 1, with no pose worse by more than 5 (sheet 24).
- **Determinism:** rebuilding under the versioned ids gives |dV| = 0 vs the candidate build, and regeneration is geometry-identical.
- **Read-back:** within 6e-8 m. The PC copies read back byte-identical.
- **Expression sanity** (diagnostic, run because the face passed §13; sheet 20): R1 matches the human-family baseline (original VAL4 / VALF178) with the same MPFB units.
  - Blink lid contact: 116 / 131 vs baseline 116 / 130.
  - Anger, sadness and surprise self-contacts and flips: within ±4 of baseline.
  - Smile flips on c2: 25 vs 22.
  - These are generic MPFB expression-unit / rig behaviours, not source defects. No facial weights or correctives were authored.

## 7. The 15 questions

1. **Is VALF178 still the valid c2 foundation?** Yes. VALF178-R1 is VALF178 plus the identical VB2g / VC2 changes, built deterministically. VALF178 is kept as ancestry.
2. **Which VB is recommended?** VB2 (final form VB2g). VB1 is weaker; VB3 drifts toward a barrel chest and a heavy neck and jaw without a better visual read.
3. **Does MF < Vael < Aelari hip-joint ordering now hold on c1 / c2?** Yes. Skeletal proxy: c1 +0.10 / −0.11 %, c2 +0.05 / −0.29 %; Fenn −2.4 %. The margins are sub-method-resolution (§3).
4. **Does VA-P6 now hold on c1 / c2?** Yes: −1.41 / −0.25 % on skin, −1.56 / −0.29 % on the proxy.
5. **Is Vael body separation from humans materially improved?** Numerically yes: 2 → 4 of 8 systems. Visually not enough: the body is still read as Marchfolk at equal height.
6. **Does Vael remain distinct from frozen Fenn and Aelari?** Yes, in body and face.
7. **Which VC is recommended?** VC2.
8. **Does hidden-ear facial identity pass against Marchfolk / Sagekin?** Yes per §13 (6 / 6), at a moderate magnitude: about 45 % of the Fenn / Aelari departure.
9. **Does Vael remain distinct from the frozen Fenn / Aelari faces?** Yes: 9 / 9 canon rows, regions 2–5 mm.
10. **Did any face region become caricatured?** No. VC3 is the limit: it over-grows the head and breaks the hip window.
11. **Did family topology remain unchanged?** Yes.
12. **Are both production candidates 69 / 69 D1–D6?** Yes.
13. **Did any new source, contact or deformation failure appear?** No.
14. **Is a non-ear topology branch needed?** No. The limit is the strength of the target architecture, not the topology.
15. **Is Vael ready to unlock ear prototyping?** No. The §14 human firewall does not pass (body).

## 8. Author decisions requested

- **A. Brow direction.** Brow lighter than humans and stronger than Aelari, as adopted here.
- **B. Composite central-vertical row.** Retire it in favour of its components plus VA-P6 (it cannot hold, §2).
- **C. VA-P3 "lighter than MF".** Visual only, or add a numeric proxy (conflicts with VA-P4, §3).
- **D. Body path (main decision).** MPFB targets cannot make the Vael body visibly non-human inside the canon windows and guard rails. Either:
  - authorise §3's third route, a **bounded deterministic custom source deformation** for the written torso-continuity, joint and extremity-base systems (frontal-silhouette signals rather than depth-only); or
  - accept a depth-led Vael body whose identity is read in profile and three-quarter views.
- **E. Face magnitude.** Accept VC2 at about 45 % of the elf face-departure scale, or authorise a stronger breadth / shape-led cranial term that keeps cranial height below Aelari. Height-led strength breaks the hip window (VC3).

## 9. Delivered / unchanged

- **Repository:**
  - `reviews/reference-assets/{r6,builds}/VAL4-R1*`, `VALF178-R1*` (manifest CANDIDATE);
  - evidence folder (evaluations, pelvis, hidden-ear, partition, expression, manifest / sidecars, validator / audit / anatomy / contact / deformation / regen, definitions, build records, probes, 25 sheets).
- **E:** `production/Vael/RP3/`:
  - `VA_{M,F}_REF_RP3_bodyfam_v002.{blend,json}`, `_landmarks.json`, `_hm08_map.npz`;
  - `VAEL_RP3_bodyfam_v002_propagation_manifest.json`;
  - `VAL4-R1` / `VALF178-R1` source sidecars.
  - Read-back is byte-identical (`pc_readback_sha256.txt`).
- **Unchanged** (`immutable_hashes.txt`, 14 / 14 equal to the previous gate): v005 blend / map / freeze, Fenn freeze, Aelari freeze, VAL4, VALF178, Fenn / Aelari sources, Fenn ear topology.
- **Not done, per the stop rules:** no Vael freeze, no ears, no Halvren, no low-light physiology, no creator morphs, no rig / UV / LOD / UE5 work.

**STOP FOR CHATGPT REVIEW.**

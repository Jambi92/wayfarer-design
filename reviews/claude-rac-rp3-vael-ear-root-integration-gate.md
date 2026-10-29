# RAC RP3 — Vael VA-E2 root / concha integration revision — gate

**Date:** 2026-10-28
**Order:** `reviews/chatgpt-rac-rp3-vael-ear-root-integration-order.md` (cbfc825)
**Parent gate:** `reviews/claude-rac-rp3-vael-ear-prototype-gate.md` (ccdaffd)
**Evidence:** `reviews/rac-rp3-evidence/vael_rp3_ear_root_integration/` (19 sheets in `sheets/`)
**Updated plan:** `reviews/claude-rac-rp3-vael-final-consolidation-plan.md` (prepared, not executed)

**Tools:**
- `tools/rac/rp/vael_rp3_v001/`:
  - `run_va_ri.sh` — builds, guard, audit, measure, blends, probes;
  - `va_ri_summary.py` — records, root / concha audit, projection, regression;
  - `va_ri_export.py` — definitions, topology, map, geometry;
  - `va_ri_sheets.py` — sheets.
- **Shared Fenn ear tools** (additive, inert without the new keys):
  - `ear_branch_lib.py`: `CAND` VA-E2-RI1 / RI2 / RI3; `cuff_build3` takes ring sizes from a read-only canon.
  - `ear_build.py`: candidate geo `cuff_skin_*` (skin-hugging cuff) and `presmooth`.
- **Reproducibility:** frozen Fenn E2, frozen Aelari AE-E2 and the reviewed VA-E2 prototype rebuild byte-identically with the edited tools (`VAEL_EAR_frozen_ear_reproducibility.json`, dV 0).

**E: (review files, not frozen):** `…/RaceBodies/production/Vael/RP3/ear_branch/root_integration/` (RI1 / RI2 / RI3 blends, c1 / c2, + summary). Read back byte-identical.

## RESULT — VAEL EAR ROOT-INTEGRATION PASS — VA-E2 READY FOR FINAL CONSOLIDATION

**RI3 is recommended.** It is VA-E2 with:
- the root brought down to the skin;
- a skin-hugging cuff;
- a bounded local Vael cuff topology derivative (one extra cuff ring).

In neutral clay, silhouette and section review, RI3 reads as **one continuous auricle**. The raised cuff mound that traced a smaller, human-like ear perimeter in front of the concha is gone, and the skin now runs straight into the concha / tragus root.

The VA-E2 outer silhouette is unchanged. All hard gates pass on both configurations, and topology quality is at the current VA-E2 class.

RI1 and RI2 improve the read too, but each leaves sliver root / cuff cells below the accepted class (§3). That is why the bounded RI3 derivative was required.

## 1. Diagnosis (what made the "ear inside an ear")

Sections (sheet 10) and the cuff maps show the cause directly.
- **Lifted ear.** The prototype lifted the whole ear 0.87 / 0.74 cm (h0) so that the deepest concha point cleared the hidden-ear skull by 0.15 cm. The anterior attachment line therefore stood 0.76 / 0.61 cm off the skin.
- **Raised mound.** The uniform biharmonic cuff had to climb that height across the 1.1 cm anterior band of the v005 root footprint. It formed a raised, rounded mound (anterior cuff p90 0.43 / 0.32 cm above the skin).
- **Second ear outline.** The mound's outline is the human-ear root footprint, so it read as a second, conventional ear nested inside the Vael leaf.

The concha floor lies **inside** the junction ring, over the head interior. It does not need to stay above the old skull level. Letting it sink is what releases the root.

## 2. RI1 / RI2 / RI3 (one VA-E2 outer geometry; `VAEL_EAR_RI_definitions.json`)

| | Change | Cuff topology |
|---|---|---|
| **RI1** reduced stand-off | Concha clearance −0.30 cm (prototype 0.15). The whole auricle lowers rigidly by 0.45 cm, so the attachment meets the skin. | Fenn v002 canon |
| **RI2** blended cuff / concha | RI1 + skin-hugging cuff, as below. | Fenn v002 canon |
| **RI3** local Vael derivative | RI2 on a six-ring cuff (52 / 56 / 60 / 64 / 66 / 68; Fenn: five rings, 52 … 68). The two extra rows next to the junction carry the fillet. | **VAEL_EAR_CUFF_CANON_v001** |

**RI2 skin-hugging cuff, in detail:**
- **Target:** the planar annulus position at the skin height (hidden-ear skull field + the root-loop residual).
- **Rise:** the target rises to the junction only within a fillet of max(0.45 × head scale, 1.4 × junction height) cm.
- **Pull:** the biharmonic fairing gets a data pull (weight 0.2) on the anterior attachment. The pull fades to zero at the root loop (0.45 cm) and near the rim / back junction (0.6 cm), so the attachment corners and the postauricular band stay biharmonic.
- **No v002 cuff pre-smoothing.** On a skin cuff it slides vertices across the fillet into contact.

**Outer silhouette preserved (§4):**
- The ear sheet (front / back / rim) of every RI equals the prototype VA-E2 sheet after a pure rigid lateral shift of −0.45 cm. The residual is ≤ 0.037 cm, from the quality pass at the junction (`silhouette` in the summary).
- Length, base breadth, projection angle (37.4°), backward tilt, sweep and taper are unchanged (sheet 12, silhouette only).

## 3. Results (`VAEL_EAR_root_integration_summary.json`; c1 / c2)

| | Current VA-E2 | RI1 | RI2 | **RI3** |
|---|---|---|---|---|
| Vertices / quads | 58,944 / 58,942 | same | same | **59,076 / 59,074** (+66 per side) |
| T-4 (branch) | 127 / 132 | 140 / 205 | 144 / 144 | **123 / 144** |
| cuff T-4 | 15 / 18 | 28 / 91 | 30 / 30 | **10 / 30** |
| min corner | 25.9° / 14.4° | **5.4° / 6.6°** (root band) | 6.3° / **2.1°** (cuff) | **25.9° / 14.9°** |
| aspect max (> 10) | 9.26 (0) | 9.45 / 9.27 (0) | 9.49 / 9.36 (0) | **9.26 / 9.26 (0)** |
| branch self-intersection | 0 | 0 | 0 | **0** |
| root crease max | 58° / 59° | 64° / 66° | 61° / 63° | **51° / 51°** |
| guard iterations | 0 / 1 | 0 / 0 | 0 / 1 | **0 / 0** |
| head / neck poses (contacts / flips / root inversions) | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | **0 / 0 / 0** |
| **Root / concha audit** | | | | |
| anterior cuff above skin, mean / p90 (cm) | 0.26 / 0.43 · 0.20 / 0.32 | 0.02 / 0.13 · −0.05 / 0.04 | 0.04 / 0.16 · 0.02 / 0.05 | **0.05 / 0.17 · 0.02 / 0.08** |
| cuff skin vs hidden-ear skull, mean / p95 (cm) | 0.455 / 0.936 · 0.402 / 0.832 | 0.24 / 0.57 · 0.21 / 0.46 | 0.27 / 0.57 · 0.22 / 0.47 | **0.28 / 0.59 · 0.23 / 0.48** |
| anterior junction above skin (cm) | 0.76 / 0.61 | 0.31 / 0.16 | 0.31 / 0.16 | **0.31 / 0.16** |
| concha floor min vs old skull level (cm) | +0.15 | −0.30 | −0.30 | **−0.30** |

Across all three alternatives:
- 1 component, all quads, 0 boundary / non-manifold / degenerate, outward normals;
- root valence 4 on all 52 per side;
- density mean edge 0.099–0.104 % of stature (limit 0.25 %);
- transition ring ≤ 0.063 cm;
- ear–head clearance ≥ 0.45 cm.

Configuration-to-configuration consistency:
- RI3 has one topology for c1 and c2 (face list identical);
- one parameter set;
- canon written once on c1, read-only afterwards.

**Determinism:** RI3 rebuilt independently, dV 0 on both configurations (`VAEL_EAR_RI3_determinism.json`).

**Selection (§9):**
- **RI1** and **RI2** remove most of the mound, but are not technically clean:
  - RI1: root-band slivers 5.4° / 6.6° and a c2 cuff at T-4 91;
  - RI2: a 2.1° cuff sliver on c2.
- Both fall below the current / accepted class. The v002 five-ring cuff has too few rows to carry the steeper fillet at the junction.
- **RI3** is the least invasive clean solution: one extra cuff ring, with root interface, root band, junction ring and sheet untouched. It is also the best-reading.

## 4. Visual-anatomical read (§14; neutral clay sheets 01–08, 12–14)

**If this were not pointed, would the root / concha still look like a coherent single ear?** Yes.
- Skin runs flat to the anterior attachment.
- The tragus / antitragus rise from it as the front of the concha.
- The concha floor sits at skin level and below.
- The antihelix forms the posterior concha wall and continues into the leaf.

**One auricle or two layered auricles?** One.
- The second perimeter (the raised cuff mound with the human root-footprint outline) is gone. Sections show the cuff now at skin level in front of the concha (sheet 10); the current version stood 0.3–0.7 cm off.
- The overlay (sheet 14) shows the removed mound, while the leaf coincides.

**Remaining note:**
- A short crease where the free upper anterior helix leaves the head (the upper end of the attachment, where the junction stands about 1.2–1.4 cm off the skin). It reads as the helix-root emergence and stays within the fillet slope cap.
- The concha bowl stays a defined cavity, as anatomy requires.

**Anatomy (sheet 07, 08; relief peaks identical to the prototype):** every required system is still present:
- helix, antihelix with superior / inferior crura;
- triangular fossa, cymba, cavum, crus of helix;
- tragus, antitragus, intertragic notch;
- lobe, upper extension.

The sheet relief is unchanged; only the root moved.

## 5. Projection / stand-off (§12; sheet 18)

| | Fenn E2 | Vael current | **Vael RI3** | Aelari AE-E2 |
|---|---|---|---|---|
| Auricle–body angle | 52.7° | 37.4° | **37.4°** | 27.2° |
| Mean free-ear stand-off / HH (c1 / c2) | 0.062 / 0.067 | 0.087 / 0.082 | **0.067 / 0.062** | 0.066 / 0.061 |
| Median free-ear stand-off / HH | 0.061 / 0.066 | 0.085 / 0.080 | **0.065 / 0.060** | 0.065 / 0.060 |
| Tip stand-off / HH | 0.113 / 0.118 | 0.136 / 0.132 | **0.117 / 0.111** | 0.102 / 0.097 |

"Free ear" = the sheet outside the junction ring, in the root frame. RI1 / RI2 equal RI3.

- Root integration lowers the whole auricle 0.45 cm and removes most of the excess stand-off.
- **Average lateral projection ordering:**
  - **c2:** Fenn > Vael > Aelari is restored on mean, median and tip.
  - **c1:** Vael sits 0.005 HH above Fenn on mean (≈ Aelari) and 0.004 HH above on tip.
- The auricle-body angle ordering holds on both.
- Per §12 the ear was not distorted to chase this. The small c1 residual is reported for the final consolidation decision.

## 6. Three-elf distinction (sheet 15)

Unchanged in kind:
- the broadest base;
- intermediate auricle angle;
- the tip carried most backward;
- a shorter / blunter taper.

Fenn remains the most upright / most angled; Aelari the longest / most upward. The revised Vael ear is not Fenn- or Aelari-like.

## 7. Deformation and probes (§15, §16; sheets 16, 19)

- **Static readiness:** 0 / 0 / 0 on all 8 poses (neck flex / extension 30°, yaw ±45°, pitch ±20°, roll ±20°), both configurations. No concha collapse and no cuff separation.
- **Shape probes (RI3, c1), 12 / 12:**
  - identical face list, 0 self-intersection, 0 boundary / non-manifold;
  - root valence 4, aspect < 10 (max 9.74);
  - every measure moves the intended way.
- **Probe T-4:** 111–178. The largest is length −10 %, the same as on the prototype. The smallest corner is 9.7° (length +10 %).
- In clay the root / concha stays one structure under every variation: no "inner ear fixed, outer shell moves".

## 8. Hidden-ear regression, unchanged inputs

- Outside the ear branch, RI3 is byte-identical to the accepted VF2 family body (55,378 v005 vertices, max |dV| 0). Only the bounded transition ring moves (≤ 0.063 cm).
- So VF2 body, VC2 face, hidden-ear firewalls and pelvis ordering are unchanged.
- **Immutable inputs:** VF2 / VC2 sources, v004 family, v005, frozen Fenn / Aelari records, Fenn ear topology / canon / map, and the VA-E1 / E2 / E3 prototype blends are sha256-equal to the previous gate: 40 / 40 (`immutable_hashes.txt`).
- **VAEL-CF-SHOULDER-1** stays registered and unchanged.

## 9. Topology / map (§19)

- `topology/VAEL_EAR_BRANCH_TOPOLOGY_v002.{json,npz}`: the local Vael cuff derivative.
  - Sheet layout and faces equal Fenn v002.
  - The 52-vertex v005 root interface and the removed v005 ear zone are the same as Fenn's.
  - +132 V / +132 Q in total.
  - Face-topology sha is recorded; identical for c1 / c2.
- `topology/VAEL_EAR_CUFF_CANON_v001.json`.
- `mapping/VAEL_EAR_BRANCH_MAP_v005_v002.npz`.
- `geometry/*_VA-E2-RI3_branch_geometry_RI3.npz` + `VAEL_EAR_BRANCH_GEOMETRY_RI3.json`.
- Per-alternative audits / builds / deform / measures in `ear/RI1–RI3/`; RI3 probes and zone report.

## 10. Answers (§19)

| Question | Answer |
|---|---|
| Does the revised ear read as one auricle rather than an ear layered on another ear? | **Yes** (RI3). |
| Which RI solution is recommended? | **RI3.** |
| Was a Vael-specific local cuff / concha topology derivative required? | **Yes, bounded.** One extra cuff ring (six instead of five), root interface / root band / junction / sheet unchanged. RI1 / RI2 on the Fenn cuff left root / cuff slivers (5.4° / 6.6°; 2.1°). |
| Is VA-E2's overall silhouette preserved? | **Yes**: rigid lateral shift only (sheet residual ≤ 0.037 cm); angle, length, breadth, tilt, sweep and taper unchanged. |
| Are all required ear anatomical systems still present? | **Yes.** |
| Did root integration improve visually? | **Yes**: no raised cuff perimeter; skin → concha → antihelix → leaf as one volume. |
| Did any new topology / deformation issue appear? | **No.** Hard gates pass; RI3 T-4 123 / 144, min corner 25.9° / 14.9° (current class); 0 / 0 / 0 poses. |
| What is the final average lateral projection ordering? | Angle: Fenn > Vael > Aelari (both). Mean / median / tip stand-off: Fenn > Vael > Aelari on c2; on c1 Vael is +0.005 HH over Fenn (≈ Aelari) — reported for final consolidation. |
| Does the revised ear remain distinct from frozen Fenn and Aelari? | **Yes.** |
| Is Vael ready for final consolidation / freeze review? | **Yes**, after author acceptance of RI3 and the local cuff derivative (plan updated, not executed). |

**Not done, per the stop rules:**
- no Vael freeze, no Halvren;
- VF2 / VC2 / frozen Fenn / frozen Aelari unchanged;
- no low-light physiology;
- no creator morphs, ear rigging, UV / materials, LODs or UE5.

**STOP FOR CHATGPT REVIEW.**

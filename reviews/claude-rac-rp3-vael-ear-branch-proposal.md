# RAC RP3 — Vael ear-branch proposal (proposal only; no ear geometry built)

**Date:** 2026-10-28
**Order:** `reviews/chatgpt-rac-rp3-vael-elf-frame-human-firewall-order.md` §21
**Gate:** `reviews/claude-rac-rp3-vael-elf-frame-human-firewall-gate.md`
**Evidence:** `reviews/rac-rp3-evidence/vael_rp3_elf_frame/VF_ear_root_interface.json`

This is a proposal only. No final ear has been built and no ear geometry is committed. It plans the next order.

## 1. Reuse of the frozen Fenn v002 engineering ear topology

**Recommendation: REUSE, engineering only.** The topology reuse covers:
- the 52-vertex root interface;
- the cuff;
- the tapered-leaf upper extension;
- the block layout;
- the deformation-aware guard.

Frozen Aelari AE-E2 already reused this connectivity cleanly. No Fenn or Aelari vertex geometry would be carried, and this is not a universal elf-ear freeze.

**Root-interface fit on the Vael VF2 head** (`vf_ear_root.py`). The root loop is the 52 v005 vertices per side, read on each family realization. Values are the mean of both sides, in cm.

| Head | Perimeter | Vertical extent | AP extent | Below vertex | Lateral | Plane tilt | Planarity RMS | Edge min–max |
|---|---|---|---|---|---|---|---|---|
| **Vael VF2 c1** | **14.94** | **5.33** | **3.41** | **13.35** | **7.76** | **10.9°** | **0.078** | **0.138–0.561** |
| **Vael VF2 c2** | **14.55** | **5.13** | **3.23** | **13.66** | **7.70** | **12.1°** | **0.062** | **0.139–0.531** |
| Fenn c1 (FNL4-CF2) | 14.64 | 5.37 | 3.21 | 13.36 | 7.43 | 11.4° | 0.065 | 0.124–0.547 |
| Fenn c2 (FNF181-CF2) | 14.24 | 5.14 | 3.04 | 13.65 | 7.36 | 12.7° | 0.048 | 0.136–0.516 |
| Aelari c1 (AEL1-R1) | 15.32 | 5.55 | 3.43 | 13.99 | 7.75 | 10.4° | 0.073 | 0.138–0.558 |
| Aelari c2 (AELF190-R1) | 14.94 | 5.33 | 3.26 | 14.30 | 7.69 | 11.6° | 0.057 | 0.148–0.528 |
| Marchfolk v005 c1 | 14.58 | 5.21 | 3.35 | 12.81 | 7.38 | 10.8° | 0.078 | 0.135–0.531 |

Every Vael root-loop measure sits inside the band already carried cleanly by frozen Fenn and Aelari:
- perimeter and extents lie between Fenn and Aelari;
- the lateral position is close to Aelari (the VC2 head is broader);
- plane tilt, planarity and edge lengths are equal.

**The root interface fits Vael cleanly.** No Vael-specific root topology is indicated.

**Topology capacity:** the Fenn and Aelari branches already express two different trajectories on this one connectivity:
- Fenn: body angle 52.7°, upper extension 32.3°, width / length 0.378;
- Aelari: body angle 27.2°, upper extension 38.0°, width / length 0.335.

The proposed Vael set (§2) sits between and beside them (broader base, intermediate projection, more backward tilt, shorter taper). It needs no new topology features, so the reuse does not make Vael a Fenn copy: identity is carried by geometry.

**Fallback:** a bounded Vael-derivative topology, used only if the guard, T-4 or aspect gates fail on the Vael base width. A broader base is the most likely stress point.

## 2. Proposed VA-E1 / VA-E2 / VA-E3 central geometries

Same construction parameters as the Fenn E2 and AE-E2 builders (`L_ref`, `wb_ref`, `proj_deg`, `tilt_deg`, `sweep_ref`, `thickness_ref`, `lobe_fraction`, taper). Evidence centre: the `ear_families` VA-elven values.

| Parameter | Fenn E2 (frozen) | Aelari AE-E2 (frozen) | **VA-E1** restrained | **VA-E2** balanced | **VA-E3** stronger |
|---|---|---|---|---|---|
| Relative length `L_ref` (cm, before head scale) | 8.6 | 9.4 | 7.9 | **8.5** | 9.1 |
| Base width `wb_ref` (half-width, cm) | 1.8 | 1.7 | 1.95 | **2.05** | 2.15 |
| Projection `proj_deg` | 50 | 24 | 30 | **35** | 40 |
| Tilt `tilt_deg` (backward) | 32 | 30 | 36 | **40** | 43 |
| Sweep `sweep_ref` (cm) | 1.6 | 1.7 | 1.4 | **1.7** | 2.0 |
| Taper (continuous start, exponent) | 0.30, 1.05 | 0.25, 0.95 | 0.42, 1.25 | **0.40, 1.25** | 0.38, 1.25 |
| Lobe fraction | 0.15 | 0.14 | 0.16 | **0.16** | 0.16 |
| Thickness `thickness_ref` | 0.27 | 0.25 | 0.29 | **0.29** | 0.29 |

**Upper extension:**
- VA-E2 is expected to be about 30–34°: below Aelari's 38° (Aelari is "more upward") and near Fenn's 32°.
- The tip should sit more backward than either, through tilt and sweep.

**Expected measured VA-E2 on the Vael head:**

| Measure | Expected VA-E2 | Fenn | Aelari |
|---|---|---|---|
| Body angle | 36–40° | 52.7° | 27.2° |
| Width / length | 0.40–0.43 (broadest) | 0.378 | 0.335 |
| Length / head height | 0.35–0.36 | 0.349 | 0.388 |

## 3. Anatomical distinctions

- **Versus frozen Fenn:**
  - less lateral projection (Fenn keeps the greatest average projection);
  - broader base;
  - more backward tilt;
  - shorter, blunter taper;
  - similar or slightly greater length relative to head height.
- **Versus frozen Aelari:**
  - more lateral and backward orientation;
  - noticeably shorter taper;
  - broader base;
  - less upward extension;
  - shorter relative length.
- **Shared elven ancestry:**
  - the same helix / antihelix / concha / tragus / lobe anatomy class;
  - the same cuff and root integration.
- **Overlap:** the three distributions overlap (canon: no ear classifies ancestry on its own). VA-E1 overlaps Fenn on length, and VA-E3 approaches Aelari on length.
- **Not bat-like, not universally short or thick:** thickness stays at the AE / Fenn class (0.29). Base width is broader, not heavy.

## 4. Gates for the ear order (proposed, same as Fenn / Aelari)

- **Topology:** 58,944 V / 58,942 Q; identical face list across c1 / c2 and VA-E1 / E2 / E3; root valence 4.
- **Quality:** T-4 ≤ the AE-E2 class; aspect < 10; branch self-intersection 0.
- **Deformation:** guard ≤ 1 iteration; 0 new branch flips or root inversions.
- **Density:** branch mean edge < 0.25 % of stature.
- **Visible-ear firewall:** vs frozen Fenn E2 and frozen Aelari AE-E2, on body angle, lateral extent / length, upper extension, width / length and sweep / length.
- **Hidden-ear identity unchanged:** VC2, and the VF2 body.

**Not done here** (per order §21): no ear geometry, no topology copy, no production ear.

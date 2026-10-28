# Fenn ear v002 — refinement provenance (order 0d9c70b §18: R1 / R2 / R3)

One shared c1 / c2 topology, one parameter set and one code path for every realization (both configurations and the ten probes). E2 parameters, root loop (52 vertices), junction ring J (70) and root-band topology are unchanged from v001. Every run reads the cuff canon `topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json`. It was written once on configuration 1 E2 and then held read-only.

## Development (before R1; not candidates)

Sweeps were run on the c1 / c2 E2 sheet and cuff only, with no blends written. They decided the R1 configuration:

| Item | Tried | Kept |
|---|---|---|
| A — upper extension | v001 kite block (F2) vs taper-following leaf (`ear_layout3.layout3`): rows marched at square cells from the crescent cut, columns 12 → 2 by 3 → 1 reductions, one diamond cap | leaf; `h_red 0.9, cap 1.8, gap 2, stagger 1` |
| A — crescent / cut | free cut vs cut held as a feature line (Hermite c1f → P_up) | held cut (a free cut drifted at P_up) |
| A — outline slide | slide_w 0.2 / 0.1 / 0.05; global vs local-window foot search | 0.05, local window (a global foot jumped across the narrow tip; 0.1+ crowded the rim at P_lo, aspect 23) |
| C — bridge corner | line-A end exponent a_ex 1.0 / 1.5 / 2.0 | 1.5 (the reflex corner of the 28 × 3 bridge block is structural; residual obtuse cells documented) |
| B — cuff count transitions | DP (v001) vs regular end bands 52/52/58/64/70; pole penalty 0.5 / 2.0; stagger 0 / 0.2 / 0.5 / 1.0 | v001 DP rule (sizes 52/56/60/64/68, pen 0.5, stagger 0). Every alternative raised cuff T-4 or aspect, so B improves through the 3-D quality pass rather than a count change. |
| B / C — cuff placement | old relax vs tangential pre-smoothing + 3-D corner-angle quality pass (`ear_quality3d`) with sizing, normal, transition, log-aspect and contact terms | quality pass. Untangle lowering with ring 1 free creased the root (151°), so rings 1–2 and the transition ring are protected in untangle, lowering is capped at 0.2, and a root-crease term was added. |
| D — lobe-cusp knob | lobe lift end / width / taper / attachment exemption, lobe thinning | `lobe_lift_end 0.0974, w 0.04, tw 0.5, att 0.4, lobe_thin 0.6`. Lobe-front J height 0.836 → 0.655 (c2, faired); the inferior-root crease this caused is held by the root-crease term. |

## R1 — primary refinement

- Configuration: layout3 as above, quality pass `lo 55, hi 125, ks 50, kn 4000, kt 20000, rho 0.5, ka 1000 (log ratio, amax 6), kr 500, th_cap 60`, contacts as active-set side pairs plus 0.7 proximity clearance, and a deformation-aware guard loop.
- Result:
  - c1 T-4 156 / 3518; c2 134 / 3518;
  - integrity, root and deformation clean on both;
  - probes 0 self-intersections.
- **Localized regression:** probe `tip_sharp` (taper_ex 1.5) has aspect 16.4 (4 faces > 10). The last 4 → 2 template collapses at a sharp tip.

## R2 — one correction for the R1 tip regression

- Near-tip rows tighten toward the tip (`step_min 0.6`), the last 4 → 2 reduction comes earlier (`h_red_last 1.6`), and the cap sits over the last 0.35 cm (`cap_d 0.35`).
- Adaptive tangential aspect repair (faces > 9.5; steps 0.5 / 0.25 / 0.125 / 0.0625; accepted only without contact).
- Guard strengthened:
  - degenerate (twisted) rest faces join the freeze list;
  - 2 freeze rings from the third iteration;
  - at most 6 iterations.
- Result:
  - `tip_sharp` aspect 9.43; all probes aspect ≤ 9.46;
  - c1 T-4 168 / 3718, c2 148 / 3718;
  - min angle 7.9 / 7.1.
- **Remaining small issue:** 2–3 root-band cells per configuration sharpened to 7–10° (v001 at the same cells 18–20°). They are the near-triangular root-band quads at ring positions 28 / 75 / 78 (a 165–177° corner in both versions; the root-band topology is locked).

## R3 — final bounded correction (root-band cells)

- Trial on c2 with the R2 guard list held: th_cap 60 / 64 / 67.
  - Raising the cap releases the cell at position 75 (min 7.1° → above 25°; the sharpest remaining root-band cell on c2 is then 12.7°).
  - Position 78 (12.7) does not move with the cap, so it is not crease-driven.
  - 64 and 67 give the same cells.
- Kept **th_cap 64**: root crease stays below v001 (c1 73.0 / 71.5, c2 64.6 / 66.5) and the v005 baseline (71.1 / 67.1).
- Full R3 run (both configurations, guard, audit, measure, blends, ten probes) in `/tmp/claude-0/rt/fn/ear/v002_r3`:
  - c1 T-4 165 / 3718, min angle 7.9. The position-75 cell does not move on c1; its vertices are contact-held (frozen in the contact cycles).
  - c2 T-4 145 / 3718, min angle 7.1 → 12.7.
  - Root crease max 64.0° on both configurations.
  - Guard converged in 1 iteration on both configurations.
- **R3 probe correction (same bounded step):** at th_cap 64, probe `sweep_m06` reached aspect 10.1 on one cuff band-0 face. The aspect repair's ring step made contact at every step size, so the repair stopped.
  - Fallback added, used only when the ring step fails: the faces' own cuff vertices, then one vertex at a time, with steps down to 1/32, accepted only if the worst aspect drops and no contact appears.
  - Configurations c1 / c2 and the other probes do not reach the fallback (their records show `fallback_rounds` absent), so they are unchanged.
  - `sweep_m06` and `len_m10` were rebuilt: aspect 8.91 / 9.06, 0 faces > 10.

No broad redesign. No anatomy restart. The R1 / R2 / R3 parameter files are the `ear_branch_lib.LAYOUT3_KW` / `GEO_V2` / `ear_build.Q3_KW` defaults in the committed tools.

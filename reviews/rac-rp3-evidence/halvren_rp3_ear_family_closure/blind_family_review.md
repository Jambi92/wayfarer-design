# Blind family reviews (independent agents; saw only the boards and the order's requirements, not the report)

## Round 1 — on the first HVEAR4 candidate (HE1 = HVEAR3 body at L 5.6; HE3 = recombined body with the HE2 rim / interior)

Verdict: **FAIL** — "HE1, HE2 and HE3 read as one ear at three sizes; HE3 is not clearly separated from HE2."
- HE3: elf-forward BORDERLINE (taller, sharper tip on HE2's outline); distinct from Fenn / Aelari / Vael PASS (broad leaf vs narrow swept blades); distinct from HE2 FAIL; one auricle c1 / c2 PASS (notes: crinkled cavity seam behind the rim in lower-rear 3/4, small notch near the base on c1).
- HE1: L 5.6 best fits human-forward; distinct from Marchfolk; only partly distinct from HE2 (same outline / interior, blunter tip); L 6.3 "plainly a shrunken HE2" — not acceptable as the human-forward minimum.
- Family: coherent but close to a uniform scale series; variation limited to tip sharpness and lower fullness; no change of silhouette type, rim treatment or interior design.
- Defects: synthetic stamped interior (shared sheet relief), base shelf at the cheek, dark gaps at the root / under the lobe, dark specks on the left ear in head views, small spike on the rear contour of HE1, pinched lower bulb in HE1 rear 3/4.

Action taken: HE1 given a human-family upper ear (rounded late corner, broader) and a broad rolled human rim; HE3 given an elven-derived thin crisp blade rim, stronger antihelix / crura / crus and a longer-drawn point (the silhouette outline itself is constrained by the shared sheet and the firewall: 18 further HE3 outline trials either self-intersected, re-aligned with an elf line (R2 0.73-0.88) or stayed at a normalized-silhouette IoU >= 0.83 with HE2). Stage-3 repair made symmetric.

## Round 2 — on the round-1-corrected HVEAR4 family (human rim on HE1, blade rim / stronger interior on HE3)

Verdict: **BORDERLINE, leaning FAIL** — "the family now reads as three different ears in the right order, but the surfaces are not production-clean."
- Family / roles: HE1 human-forward and HE3 elf-forward now read correctly; HE2 -> HE3 still partly reads as a stretch of the same outline (the shared-sheet / firewall limit recorded in round 1).
- Defects: HE1 lumpy rim and crinkles in the scapha / crura; HE3 crease lines and a zig-zag in the upper scapha.

Diagnosis: the crinkles / crease lines are FOLDED auricle-sheet quads (the two triangle splits of a quad disagree in orientation: HE1 34, HE3 18 on c1; HE2 frozen 4). Action taken: Halvren repair stage 4 (gated by the HE1 / HE3 `sheet_fold_fix` flag, HE2 untouched): symmetric umbrella relaxation of folded sheet quads, kept only while the fold count drops and every quad keeps corner >= 12 deg / aspect < 10 (HE1 34 -> 5, HE3 18 -> 6; moves <= 0.23 cm; silhouettes unchanged). Own audit of the rebuilt boards then found a dark speck in front of the tragus on HE1 c2 (a cuff edge creased 162 deg); stage 5 (same gate) relaxes cuff edges creased > 120 deg by a per-vertex pattern search with corner / aspect and a local no-new-crossing guard.

## Round 3 — after stages 4 / 5 (HE1 still the round-2 body)

Verdict: **FAIL** — "HE1 still reads as a shrunken, tip-cut HE2 rather than a human-leaning ear, and its upper rim / top corner are rougher than HE2's; HE3 acceptable."
- HE3: elf-forward PASS; distinct from HE2 BORDERLINE (taller / sharper tip, shares tilt / interior / lobe base); not a disguised elf ear PASS; one auricle c1 / c2 PASS.
- HE1: human-forward BORDERLINE; distinct from HE2 BORDERLINE leaning FAIL (only size + a blunted angular top).
- Family: ordered, but at head scale mostly a height ramp (BORDERLINE).
- Defects: HE1 wavy upper rim, faceted top corner, back-rim kink; HE3 crumpled cuff band / zig-zag crease on the skull-facing back (lower-rear 3/4) and a wavy seam (direct rear).

Own check: the HE3 back-side crumple is the shared RI3 cuff band and the HR2 back-sheet Z-kink, identical on the frozen HE2 (rear comparison HE2 / HE3 / HE1 / Fenn) -- a shared HR2 polish item already recorded as non-blocking, not an HE3 defect. Action taken on HE1 (6 + 6 rest trials, `he1u` in the record): a human-family OUTLINE -- upright (tilt 12 -> 9, sweep 0.65 -> 0.45), rounded egg-shaped upper ear with only a soft Halvren apex (taper 0.58 / 0.80 / 0.14 -> 0.52 / 0.70 / 0.06) -- and a fully rolled human helix (0.34 x 0.32 -> 0.42 x 0.40), smooth with stage 4.

## Round 4 — on the final HVEAR4 family (fresh reviewer, same brief)
__ROUND4__

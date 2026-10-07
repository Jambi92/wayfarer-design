# RAC W2A — Marchfolk Boundary Foundation (RM-UB-07) Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Author ruling (October 7, 2026; GitHub Issue #1 W2A ruling (2026-10-07T21:46Z); reviews/chatgpt-rac-w2a1-marchfolk-frame-closure-order.md):** W2A PARTIALLY ACCEPTED — 147 / 203 cm boundary bodies (both configurations; knee 0.6 / 0.3), routes as construction methods only, route kinks technical, composition evidence accepted; envelope values NON-CANON. Frames not closed: the breadth-only ±8 % write is insufficient for Marchfolk frame canon (shoulders, ribcage dimensions, pelvis, joint scale, skeletal visual mass) — W2A1 ordered. The analysis below is unchanged.
**Order:** `reviews/chatgpt-durrim-final-acceptance-rac-w2-kickoff-order.md` §W2A, the same text as GitHub Issue #1 comment 2026-10-07T21:18Z.
**Evidence:** `reviews/rac-w2a-mf-evidence/` (`tables.md` holds every number quoted)
**Construction record:** `tools/rac/w1/cfg/w2a/MF-boundary.json`

**Every value here is a NON-CANON diagnostic.** Nothing is accepted. The accepted 173 cm W1 ARMs (MF-M-R, MF-F-R) are unchanged and remain the central anchors.

## Recommendation: accept the W2A boundary bodies and route rule as Marchfolk W2 baseline evidence

RM-UB-07 holds at 147 and 203 cm in both configurations:
- no uniform scaling;
- adult at 147 cm;
- not Skarn-like and not elf-like at 203 cm;
- continuous with the central body, apart from small route kinks reported in §3.

**One bounded route correction is proposed, for the boundary construction only.** At 203 cm the generator height macro drops knee breadth below the generator's own adult allometric slope. Configuration 1 falls 10 % below it and reads more gracile than a matched-stature Aelari and Fenn; configuration 2 falls 4 % below it. A knee target (`measure-knee-circ-incr` 0.6 / 0.3) restores the knee to that slope (0.0640 vs expected 0.0643; 0.0597 vs 0.0603). Nothing else changes.

**No accepted Marchfolk canon needs to be challenged.** Marchfolk canon sets the 147–203 cm range and "no uniform scaling" but authors no allometric magnitudes. Everything below is diagnostic.

## 1. Construction (order item 1; record)

| Stature | Route | Configuration 1 | Configuration 2 |
|---|---|---|---|
| 147 cm | **Native regional route** (`native_short.py`), from each configuration's accepted base macro. One length factor; girth k^0.654, hands k^0.842, feet k^0.942, head k^0.688 (generator adult allometry slopes) | k_len 0.844 | from base macro 0.606 (new optional `base_height_macro`; default keeps W1 behaviour) |
| 173 cm | Accepted W1 ARMs | macro 0.500 | macro 0.606 |
| 203 cm | **Generator height macro** re-solved + knee restored | macro 0.718, knee 0.6 | macro 0.815, knee 0.3 |

**Why two routes.** The generator's height macro is the MPFB human allometry, but below ~159 cm it has an implausible femur (`native_short_allometry.json`). At 147 cm it shortens the rig femur ÷ leg by 17 % relative to the native route (route cross-check).

**Method limits:**
- The native route holds segment-length proportions. It carries allometry only in girth, hands, feet and head.
- The macro also changes segment proportions (femur ÷ leg +6.7 % at 203 cm, configuration 1).
- No construction value reached a search bound.

## 2. Measurements (order item 2; tables §1)

Skeletal = CIB, t = 0. Joints = stature-scaled slab.

| Reading | 1 · 147 | 1 · 173 | 1 · 203 | 2 · 147 | 2 · 173 | 2 · 203 |
|---|---|---|---|---|---|---|
| torso / stature | 0.2824 | 0.2834 | 0.2784 | 0.2846 | 0.2859 | 0.2803 |
| neck / stature | 0.0544 | 0.0547 | 0.0529 | 0.0623 | 0.0626 | 0.0595 |
| head height / stature | 0.1372 | 0.1300 | 0.1241 | 0.1317 | 0.1255 | 0.1198 |
| arm / stature | 0.4079 | 0.4072 | 0.4098 | 0.3853 | 0.3845 | 0.3910 |
| leg / stature | 0.5295 | 0.5321 | 0.5455 | 0.5209 | 0.5232 | 0.5387 |
| femur / leg | 0.4837 | 0.4837 | 0.5161 | 0.5132 | 0.5132 | 0.5427 |
| hand / stature | 0.1149 | 0.1125 | 0.1106 | 0.1055 | 0.1032 | 0.1027 |
| foot / stature | 0.1497 | 0.1490 | 0.1496 | 0.1345 | 0.1339 | 0.1367 |
| skeletal thoracic breadth / stature | 0.1694 | 0.1614 | 0.1540 | 0.1591 | 0.1516 | 0.1450 |
| skeletal thoracic depth / stature | 0.1242 | 0.1178 | 0.1120 | 0.1211 | 0.1145 | 0.1101 |
| skeletal crest breadth / stature | 0.1645 | 0.1558 | 0.1511 | 0.1809 | 0.1714 | 0.1644 |
| skeletal AP pelvic depth / stature | 0.0994 | 0.0946 | 0.0935 | 0.0914 | 0.0875 | 0.0878 |
| skeletal pelvic vertical / crest | 0.3365 | 0.3563 | 0.3492 | 0.2858 | 0.3018 | 0.3016 |
| elbow / wrist / knee breadth / stature | 0.0533 / 0.0329 / 0.0744 | 0.0511 / 0.0319 / 0.0688 | 0.0487 / 0.0310 / 0.0640 | 0.0475 / 0.0318 / 0.0680 | 0.0453 / 0.0309 / 0.0645 | 0.0434 / 0.0305 / 0.0597 |
| femoral S7 breadth / stature | 0.0795 | 0.0755 | 0.0698 | 0.0749 | 0.0711 | 0.0757 |

Palm, finger, foot breadth, within-arm distribution, waist and the t = 0.5 / 1.0 skeletal readings are in tables §1.

## 3. RM-UB-07 results (order item 3; tables §2)

| Check | Result |
|---|---|
| **No uniform scaling** | PASS. Head share is allometric in both configurations (147 > 173 > 203). 11–21 shares per boundary body depart from the central body by ≥ 1 % |
| **Not juvenile at 147 cm** (vs a 147 cm generator child proxy, ~11 y) | PASS. Head share 0.1372 / 0.1317 vs child 0.1409. Adult face: FVB +15 % / +11 % over the child |
| **Not Skarn-like at 203 cm** (configuration 1 vs accepted Skarn) | 5 / 5 PASS: skeletal thoracic depth, wrist, knee, shoulder-joint breadth, skin thoracic depth all below Skarn |
| **Not elf-like at 203 cm** (configuration 1 vs Aelari and Fenn carried to 203 cm by the generator's allometry slopes) | 7 / 7 scored PASS; wrist vs Aelari carries **no verdict** (see below) |
| **Continuity 147 → 173 → 203** | All readings monotonic or reversing by < 1 %, except the reversals listed below |

**Wrist vs Aelari carries no verdict.** The accepted central MF173 already reads −3.5 % on that row, so it does not discriminate. The configuration 2 elf rows are report-only, because the elf references are configuration 1.

**Continuity reversals (route kinks, not anatomy):**

| Reading | 147 vs 173 | 203 vs 173 | Cause |
|---|---|---|---|
| Configuration 1 skeletal pelvic vertical ÷ crest | −5.5 % | −2.0 % | The native route scales crest by girth (k^0.654) and vertical by length; the macro at 203 cm has its own pelvis |
| Configuration 2 femoral S7 breadth ÷ stature | +5.3 % | +6.4 % | The 173 cm anchor sits lowest: native girth allometry at 147 cm, the generator macro thickening the thigh at 203 cm |
| Configuration 2 ankle ÷ stature | +1.1 % | +3.4 % | Small |

None of these moves outside ordinary human readings, and Marchfolk canon authors no allometric direction.

**Route findings that shaped the construction:**
1. The **macro-only 203 cm knee** is fixed by the bounded knee target above. The 203 cm route sheet shows the macro-only body, the knee-restored body and the native cross-check.
2. **Configuration 2 at 147 cm from the default base macro (0.5)** read a skin crest ÷ thorax +16 % jump. Starting from configuration 2's accepted base (0.606) removes it (−14.3 % between the two). Tool change: an optional `base_height_macro`, default unchanged.

## 4. Frames and composition at 173 cm (order items 4–5; tables §5)

| Body | Result |
|---|---|
| Narrow / Broad, configurations 1 and 2 (breadth-only ±8 %, Broad pelvis ×1.08) | PASS. Lengths, head, skeletal depth and joints within 0.5 % of central; breadth moves −7.9 % / +7.8 % (config. 1 skeletal), −8.2 % / +10.5 % (config. 2 skin) |
| Broad configuration 1 vs Skarn | 3 / 3 PASS: skeletal thoracic depth, wrist, knee |
| Composition: config. 1 low, low muscle, high muscle, higher fat, high muscle + fat; config. 2 low, high muscle + fat | PASS. Torso, leg, arm and head shares within 1 % of central |
| Minimum composition (muscle 0 / weight 0, config. 1) | **Head share −1.6 %** (skin head height includes facial soft tissue at the composition extreme); skin diagnostic, not skeleton |

Skin composition diagnostics are kept separate from the skeletal layer. Configuration 2 composition bodies settle 0.5–2 cm short of 173 cm because the generator's muscle and weight macros move stature. Shares are unaffected.

## 5. Diagnostic envelope candidates (order item 7; NON-CANON; tables §4)

Min / max over the six boundary-set bodies, with source bodies, for every reading. For example:

| Reading | Range | Source bodies |
|---|---|---|
| head height / stature | 0.1198–0.1372 | F203 / M147 |
| leg / stature | 0.5209–0.5455 | F147 / M203 |
| skeletal thoracic breadth / stature | 0.1450–0.1694 | F203 / M147 |
| skeletal crest breadth / stature | 0.1511–0.1809 | M203 / F147 |
| knee breadth / stature | 0.0597–0.0744 | F203 / M147 |

These are candidates only, with no clamp and no tolerance. Frame and composition ranges are reported separately and are not merged into them.

## 6. Residuals and method limits (order item 8)

| Item | Status |
|---|---|
| Boundary knee | Bounded route correction proposed (§0); author call |
| Route kinks | Pelvic vertical ÷ crest (config. 1), femoral S7 (config. 2): native and macro routes meet at 173 cm |
| Native route at 147 cm | Holds segment-length proportions; the generator's segment allometry is unusable below ~159 cm |
| Minimum-composition head share | −1.6 % skin diagnostic |
| Wrist vs Aelari at matched stature | No verdict (central fails the same row) |
| Elf rows for configuration 2 | Report only (no configuration 2 elf references) |
| Rig "femur / tibia" | Joint-to-joint thigh ÷ shin, not an anatomical ratio; reported only |
| MF-FACE-PROJ-MAX | Not re-checked; no dependency arose (order item 6) |
| NOT RUN | Boundary × frame / composition combinations (out of W2A minimum scope) |

## 7. Canon statement

**No accepted Marchfolk canon needs to be challenged.** The accepted 173 cm ARMs are untouched. The only proposal is a boundary-route rule: native route at 147 cm; macro plus knee restored to the generator slope at 203 cm.

## 8. For the author

1. Accept the W2A boundary bodies (147 / 203 cm, both configurations) and the route rule as Marchfolk W2 baseline evidence, including the bounded knee correction.
2. Accept the continuity route kinks as route characteristics, or order a single-route rebuild.
3. Keep every envelope value NON-CANON until a later ruling.

Next W2 block not started.

STOP.

— Claude

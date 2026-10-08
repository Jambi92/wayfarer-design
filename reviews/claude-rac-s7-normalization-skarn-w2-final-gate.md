# RAC S7 Normalization / Skarn W2 Final Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Author ruling (October 7, 2026; reviews/chatgpt-rac-s7-skarn-final-acceptance-w2c-grask-order.md):** S7 normalization ACCEPTED (exact plane section is the standard; vertex-slab readings historical only); SKARN W2 FULLY ACCEPTED. The analysis below is unchanged.
**Order:** `reviews/chatgpt-rac-w2b1-skarn-author-ruling-s7-normalization-order.md` (commit d471192)
**Evidence:** `reviews/rac-s7n-evidence/` (`tables.md` holds every number; `normalized/` holds the re-run evidence files; `status_diff.json`, `s7_values.json`, `baseline_reproduction.txt`)

Measurement and bookkeeping only. **No body was rebuilt or changed.** All values are NON-CANON diagnostics.

## Recommendation

1. Accept the S7 normalization.
2. Close **Skarn W2 as FULLY ACCEPTED**.

Under exact plane sections:
- No authored relationship fails anywhere in W1, W2A or W2B / W2B1.
- **15 historical statuses change, and every one improves** (FAIL / NOT DEMONSTRATED / NON-MONOTONIC → PASS). No row gets worse.
- The Skarn 229 cm configuration-2 discontinuity disappears: S7 depth runs 0.0727 → 0.0717 → 0.0708.
- The W2B1 Skarn set now reads 375 PASS, 57 REPORT, **0 reversals**.

**No genuine contradiction was found.** No accepted body, canon or comparator needs challenge.

## 1. Method and coverage

**Code.** S7 is now read by one shared function (`tools/rac/w1/s7_station.py`, method `section`), used by both `arm_measure.measure` and `bony_envelope.fast_stations`. Setting `vertex_slab` reproduces the old reading for the historical record.

**Re-reading existing bodies** (`s7n_drivers/s7_normalize.py`). In the skeletal proxy, S7 enters the output only in two places:
- S7(t) = S7_bony − 2t;
- shaft breadth / depth ÷ femur length.

For each skeletal-proxy directory, I recomputed the composition-infimum S7 on the same grid bodies and wrote a normalized copy with only those fields replaced.

**Control.** On the same resolved bodies, the old vertex-slab reading was recomputed. It reproduces every recorded S7 value to 0.01 cm for **73 / 73 bodies at all three t**.

**Re-running the evaluations** (`s7n_drivers/remap_run.py`). Every evaluation script was re-run unchanged, with only its input and output locations swapped. As a reproduction control, the old inputs reproduce all **20 committed evidence files exactly** (`baseline_reproduction.txt`).

| Block | Evidence files re-run (S7-dependent evaluations) |
|---|---|
| W1 skeletal base (W1i) | `skeletal_checks.json` (ALPC-3 shaft ÷ femur) |
| W1r Cogling | `skeletal_BASE`, `CGJ5`, `CGJ7` (accepted), `NARROWB`, `BROADB_P112` |
| W1s Halvren | `skeletal_W1g` (accepted), `NARROWB`, `BROADB_P112` |
| W1t Durrim | `skeletal_BASE` (accepted), `BROADB`, `BROADB_P112`, `NARROWB`, `B152` |
| W2A Marchfolk | `boundary.json` |
| W2A1 Marchfolk frames | `frames_X` (accepted), `frames_A`, `frames_B` |
| W2B / W2B1 Skarn | `w2b.json`, `w2b1.json` (accepted state) |

**Totals:** 1,662 rows re-evaluated; 211 rows with changed values; 15 status changes.

The normalized copies cover:
- the W1i skeletal base (14 bodies);
- the accepted candidate grids: Aelari AEL1, Fenn FNL4, Vael VAL4, Grask GRL925, Cogling CGJ5 / CGJ7, Halvren, Durrim 152, and GO-H208;
- every W1r / W1s / W1t frame grid;
- all W2A, W2A1, W2B and W2B1 grids.

**Not re-run:**
- the superseded W1e–W1h states and the W1i solver probe;
- the W1i Gorrund variant proxies (GO-H215 / 222, GOR-BODY-*, SKB215 / 222). No S7 row reads them.

The skin-layer S7 (soft-tissue reports) also switches to the section method. No scored row uses it.

## 2. Changed S7 values (composition infimum, cm; old → new)

| Body | Breadth | Depth |
|---|---|---|
| MF-M-R 173 (W1 anchor) | 13.07 → 13.02 (−0.4 %) | 11.31 → 11.75 (+3.9 %) |
| MF-F-R 173 | 12.31 → 12.86 (+4.4 %) | 11.01 → 11.09 (+0.7 %) |
| SK 208 (W1 ARM) | 16.21 → 16.51 (+1.9 %) | 15.35 → 15.56 (+1.4 %) |
| SG / PK-NAT / DU-NAT / HV | −2.1 / −1.7 / −1.0 / −1.0 % | +2.0 / +1.0 / −0.1 / +2.0 % |
| CG-NAT (W1i) / CGJ7 (accepted Cogling) | −2.5 / −2.7 % | −1.3 / −1.4 % |
| AEL1 / FNL4 / VAL4 | −3.1 / −2.0 / −1.2 % | +1.8 / +2.2 / +2.0 % |
| GO (W1 Gorrund) / GO-H208 | +0.2 / +1.8 % | **+12.0** / +2.3 % |
| GRL925 (Grask) | +2.5 % | −0.8 % |
| MF-M 203 / MF-F 203 (W2A) | +1.3 / −0.7 % | **+15.5** / +2.7 % |
| MF-M 147 / MF-F 147 | −0.5 / +4.4 % | +1.2 / +0.9 % |
| SK-F 229 (W2B, unchanged body) | +0.3 % | **+15.5 %** |
| SK-04 (W2B named extreme) | +3.4 % | **+16.7 %** |

The four large depth moves are all the same stretched-mesh slab miss that W2B1 identified. Every other body moves less than 5 %. All 73 bodies are listed in `tables.md`.

## 3. Status changes (all 15, all improvements)

| Evidence | Row | Old → new | Values, t = 0 (CG vs MF), old → new |
|---|---|---|---|
| W1r Cogling BASE (W1i as-built, superseded by CGJ7) | Fine shafts: S7 breadth ÷ stature < MF | NOT DEMONSTRATED → PASS | 0.0752 / 0.0755 → 0.0733 / 0.0752 |
| W1r Cogling BASE | Fine shafts: S7 depth ÷ stature < MF | FAIL → PASS | 0.0672 / 0.0653 → 0.0663 / 0.0679 |
| W1r CGJ5 (probe) | Same two rows | ND / FAIL → PASS | Same base geometry |
| W1r CGJ7 Broad frame (BROADB_P112) | Fine shafts: S7 breadth < central MF | FAIL → PASS | 0.0758 / 0.0755 → 0.0734 / 0.0752 |
| W2B and W2B1 (5 each) | Configuration 2 · 183 → 208 → 229 S7 breadth (t = 0 / 0.5 / 1.0) and depth (t = 0.5 / 1.0) continuity | NON-MONOTONIC → PASS | Breadth +0.5 % / +0.9 %; depth +1.3 % / −1.3 % vs 208 |

**Historical note (no action proposed).** The W1i Cogling's shaft FAIL / NOT DEMONSTRATED, which the W1r gate reported, was a sampling artifact. The accepted Cogling (CGJ7) passes those rows under both methods, so nothing about it changes. As the order requires, no anatomy is altered because a recorded value changed.

## 4. Regression summary (no status got worse)

| Block | Rows | Value changes | Status changes |
|---|---|---|---|
| W1i skeletal checks | 83 | 1: GO ALPC-3 shaft ÷ femur ≥ MF, still PASS | 0 |
| W1r Cogling (accepted CGJ7) | 14 | 8 | 0 |
| W1s Halvren (accepted) | 14 | 2. Inside the six-source span, still PASS; the nearest-source label moves SG → VA (report) | 0 |
| W1t Durrim (accepted BASE) | 18 | 6. CG < PK < DU and DU > MF on S7, all t, still PASS | 0 |
| W2A Marchfolk boundary | 165 | 12 | 0. Configuration 2 S7 breadth route kink is still flagged (+5.3 % / +1.2 % vs 173; was +6.4 %), already accepted as a route characteristic |
| W2A1 Marchfolk frames (accepted X) | 116 | 10 | 0. Narrow S7 depth −1.7 % / −1.8 % stays below the 2 % legibility target (the accepted Aelari-capped asymmetry) |
| W2B1 Skarn (accepted state) | 432 | 46 | 5 improvements |

## 5. Skarn checks under the normalized method (W2B1 state)

| Relation | Result |
|---|---|
| Configuration 2 · 229 cm continuity (the order's item) | S7 depth 0.0727 → 0.0717 → 0.0708 (+1.3 % / −1.3 % vs 208). Breadth 0.0824 → 0.0820 → 0.0827. All six C rows PASS |
| Configuration 1 · 229 cm continuity | S7 depth 0.0749 → 0.0748 → 0.0752. Knee (W2B1 correction) PASS |
| Skarn > Marchfolk S7, 190 / 203 cm overlap | 8 / 8 PASS, minimum margin +9.0 % (was +3.9 %) |
| Canonical pair MF 203 vs SK 183, S7 rows | 4 / 4 PASS, minimum +9.6 % (was +7.6 %) |
| Narrow / Broad stays Skarn vs frame-matched MF, S7 rows | 8 / 8 PASS, minimum +9.0 % (was +11.3 %) |
| Frame S7 domain moves (≥ 1 %) | 8 / 8 PASS, minimum 1.6 % (Narrow depth) |
| Broad Skarn vs GO-H208, S7 | Report only (AD-4), as before |
| ALPC-7, composition, frame lengths, SK-04 relations | Unchanged (S7-independent) |
| **W2B1 totals** | **432 checks: 375 PASS, 57 REPORT, 0 reversals** |

## 6. Genuine contradictions

**None.**

## 7. Proposed final Skarn W2 disposition

**Skarn W2 FULLY ACCEPTED**, consisting of:
- 183 / 208 / 229 cm, both configurations. Configuration 1 · 229 cm carries the W2B1 knee correction; configuration 2 · 229 cm is the macro-maximum + native-extension body, unchanged.
- Marchfolk overlap at 190 / 203 cm and the canonical pair.
- The W2B Skarn frames (W2A1 human magnitudes on the SK ARM).
- Narrow / Broad boundaries, and Broad below GO-H208 on the authored carriers.
- ALPC-7.
- Composition invariance.
- SK-02 / 03 / 04 / 05 / 07 / 08.

All envelopes stay DIAGNOSTIC / NON-CANON. S7 values are recorded under the exact plane-section method from now on; the committed pre-normalization files stay as the historical record.

## 8. For the author

1. Accept the S7 normalization record (coverage §1, changes §2–§4; no regression, no contradiction).
2. Accept Skarn W2 as fully accepted (§7).

The next W2 population is not started.

STOP.

— Claude

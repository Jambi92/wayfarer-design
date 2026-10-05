# RAC Wave 1 — Completion Report

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-reference-anatomy-wave1-execution-order.md`

## Recommendation: **W1 PARTIAL — ASSET BUILD/ACCESS REQUIRED**

No canon contradiction was found. The program is blocked by missing compliant geometry, chiefly the Marchfolk baseline.

## ARMs

| State | Candidates |
|---|---|
| Technical PASS, author acceptance pending | SA-M (with R-5/R-6 stance note), SA-F |
| CONSTRAIN (correction required) | MF-M Iteration 3 (age, A-pose, no eyes) |
| FAIL | MF-F Iteration 3 (R-2 uniform scaling); Vael Rodin GLBs (not measurable, not a candidate) |
| Blocked — build required | MF-M-R, MF-F-R, MF-FACE-PROJ-MAX, SK, SG, FN, AE, VA, HV, DU, GR, GO, PK, CG (14 packets) |

Records: `reviews/rac-w1-arm/`. Packets: `reviews/rac-w1-packets/`. Preflight: `reviews/claude-rac-w1-00-preflight.md`.

## Measurements completed (diagnostic)

- **RM-CF-01** (Saurin): r3 FPI 0.3254 at both centres; pitch ±3° 0.318–0.333; corners 0.2857–0.3582; Part 7 index 0.2879; coupled corner at the 0.255 floor = r3 0.292.
- Saurin stature accounting for male centre, female centre and +10 % reference female: reproduces canon (lower trunk 32.0 / 33.6 / 34.3; pelvis 41.7 / 43.1; d÷w 0.880 / 0.922).
- Saurin per-region symmetry.
Details: `reviews/claude-rac-w1-measurements.md`.

## Diagnostic findings

1. The Saurin rostral floor and r3 FPI use different OC landmarks; same anatomy differs by ≈ 0.037 (D-1).
2. The frozen Saurin stance carries leg asymmetry up to 7.7 cm; anatomy is symmetric at the head (median 0.06 cm) (D-2).
3. The Iteration 3 Marchfolk bodies are MakeHuman defaults: every shape value is builder-chosen; the female body breaks R-2.
4. Cross-race: only the Saurin side runs; tail mandatory PASS; no failure found (`claude-rac-w1-cross-race-audit.md`).

## Canon changes

Only W1-A1 (Cogling 11–13 cm = head height menton–vertex) in `specs/cogling/COGLING_V1.md` and RMQ RM-SR-04, as ordered. No envelope, bound, control or race anatomy changed.

## Readiness for W2

Not ready. W2 needs accepted central ARMs; supply order: MF-M-R → MF-F-R → MF-FACE-PROJ-MAX → W1-03 sequence. Author decisions D-1…D-5 are in `claude-rac-w1-author-decisions-needed.md`.

STOP.

— Claude

# RAC W1 Continuation — Diagnostic Measurements

**Author:** Claude **Date / pass:** October 5, 2026, W1c pass 1 (after the independent audit corrections)

**Status:** **DIAGNOSTIC ONLY.**
- No value is canon, no envelope is adopted and no bound is moved.
- Every value is derived from **builder-chosen reference values that are not yet accepted** (REFERENCE_ANATOMY_V1 §7). Measuring these candidates confirms the builder's inputs; it cannot discover canon.

**Method:** `reviews/claude-rac-w1c-build-method.md`. Anatomy is read on the generator-authored rest geometry; shares use the R-6 stature.

**Raw data:**
- `reviews/rac-w1c-evidence/<ID>_meas.json`: full precision, rest and R-6 readings, ±3° pitch sensitivity, eye fit.
- `<ID>_inv.json`: rest vs R-6 invariance.

**Identification:**
- Pass W1c-1, October 5, 2026.
- Surface E-layer landmarks.
- Configuration 1 (MPFB gender 1.0) except MF-F-R.
- Geometry hashes are in each ARM record.

**Read with care:**
- **PK and CG are non-compliant uniform-scale proxies (R-2 FAIL).**
- FN, AE, VA, HV, DU, GR and GO are CONSTRAIN: their body proportions are measured, but their non-human ear and pelvis anatomy is not instantiated.

## 1. Shares and ratios (rest anatomy ÷ R-6 stature)

| Measure | MF-M-R | MF-F-R | MF-FACE-PROJ-MAX | SK | SG | FN | AE | VA | HV | DU | GR | GO | PK | CG |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Stature R-6 (cm) | 173.14 | 172.99 | 173.14 | 208.01 | 177.99 | 181.14 | 190.01 | 178.00 | 177.73 | 136.99 | 217.99 | 228.99 | 107.00 | 91.00 |
| torso (suprasternal-hip joint) / H | 0.283 | 0.286 | 0.283 | 0.296 | 0.277 | 0.271 | 0.276 | 0.284 | 0.280 | 0.315 | 0.265 | 0.277 | 0.277 | 0.278 |
| hip-joint height / H | 0.532 | 0.523 | 0.532 | 0.524 | 0.542 | 0.550 | 0.535 | 0.533 | 0.538 | 0.487 | 0.564 | 0.552 | 0.523 | 0.530 |
| arm (shoulder joint-fingertip) / H | 0.407 | 0.385 | 0.407 | 0.402 | 0.418 | 0.429 | 0.424 | 0.413 | 0.413 | 0.403 | 0.431 | 0.391 | 0.415 | 0.402 |
| span (DER) / H | 1.028 | 0.958 | 1.028 | 1.028 | 1.046 | 1.060 | 1.046 | 1.039 | 1.038 | 1.077 | 1.055 | 1.009 | 1.066 | 1.028 |
| upper arm / arm | 0.353 | 0.386 | 0.353 | 0.352 | 0.343 | 0.346 | 0.352 | 0.353 | 0.350 | 0.329 | 0.349 | 0.357 | 0.351 | 0.286 |
| forearm / arm | 0.371 | 0.345 | 0.371 | 0.355 | 0.375 | 0.374 | 0.372 | 0.366 | 0.374 | 0.323 | 0.377 | 0.356 | 0.347 | 0.384 |
| hand / arm | 0.276 | 0.268 | 0.276 | 0.293 | 0.282 | 0.280 | 0.276 | 0.280 | 0.277 | 0.348 | 0.274 | 0.287 | 0.301 | 0.330 |
| finger / hand | 0.435 | 0.440 | 0.435 | 0.438 | 0.459 | 0.468 | 0.436 | 0.436 | 0.448 | 0.433 | 0.469 | 0.412 | 0.432 | 0.470 |
| finger / palm | 0.771 | 0.785 | 0.771 | 0.779 | 0.848 | 0.880 | 0.774 | 0.773 | 0.810 | 0.765 | 0.884 | 0.700 | 0.762 | 0.885 |
| femur / leg | 0.484 | 0.513 | 0.484 | 0.490 | 0.490 | 0.474 | 0.502 | 0.496 | 0.484 | 0.380 | 0.478 | 0.538 | 0.388 | 0.342 |
| lower leg / leg | 0.516 | 0.487 | 0.516 | 0.510 | 0.510 | 0.526 | 0.498 | 0.504 | 0.516 | 0.620 | 0.522 | 0.462 | 0.612 | 0.658 |
| neck / H | 0.055 | 0.063 | 0.055 | 0.054 | 0.054 | 0.053 | 0.061 | 0.055 | 0.054 | 0.049 | 0.050 | 0.052 | 0.058 | 0.058 |
| thorax breadth (max) / H | 0.190 | 0.171 | 0.190 | 0.197 | 0.187 | 0.180 | 0.177 | 0.189 | 0.188 | 0.235 | 0.171 | 0.197 | 0.208 | 0.197 |
| thorax depth (max) / H | 0.132 | 0.124 | 0.132 | 0.142 | 0.127 | 0.124 | 0.122 | 0.136 | 0.130 | 0.167 | 0.121 | 0.144 | 0.147 | 0.141 |
| thorax depth / breadth | 0.696 | 0.729 | 0.696 | 0.723 | 0.679 | 0.686 | 0.686 | 0.719 | 0.691 | 0.711 | 0.707 | 0.729 | 0.709 | 0.718 |
| shoulder-joint breadth / H | 0.214 | 0.189 | 0.214 | 0.224 | 0.210 | 0.202 | 0.199 | 0.212 | 0.211 | 0.270 | 0.192 | 0.226 | 0.237 | 0.224 |
| elbow breadth / upper arm | 0.355 | 0.305 | 0.355 | 0.358 | 0.347 | 0.332 | 0.321 | 0.343 | 0.346 | 0.455 | 0.307 | 0.342 | 0.402 | 0.490 |
| wrist breadth / forearm | 0.212 | 0.232 | 0.212 | 0.263 | 0.204 | 0.187 | 0.200 | 0.218 | 0.202 | 0.347 | 0.193 | 0.265 | 0.252 | 0.251 |
| knee breadth / femur | 0.290 | 0.262 | 0.290 | 0.292 | 0.280 | 0.275 | 0.265 | 0.284 | 0.292 | 0.519 | 0.221 | 0.243 | 0.462 | 0.460 |
| palm breadth / hand | 0.438 | 0.438 | 0.438 | 0.434 | 0.418 | 0.412 | 0.435 | 0.441 | 0.429 | 0.436 | 0.410 | 0.445 | 0.439 | 0.414 |
| palm depth / hand | 0.185 | 0.181 | 0.185 | 0.172 | 0.175 | 0.170 | 0.174 | 0.181 | 0.181 | 0.181 | 0.162 | 0.187 | 0.192 | 0.181 |
| iliac-crest proxy breadth / H | 0.165 | 0.159 | 0.165 | 0.164 | 0.163 | 0.154 | 0.152 | 0.165 | 0.164 | 0.187 | 0.151 | 0.162 | 0.190 | 0.164 |
| bitrochanteric / H | 0.192 | 0.212 | 0.192 | 0.191 | 0.189 | 0.183 | 0.179 | 0.191 | 0.190 | 0.228 | 0.177 | 0.186 | 0.227 | 0.217 |
| pelvic AP depth / H | 0.129 | 0.129 | 0.129 | 0.124 | 0.127 | 0.125 | 0.122 | 0.128 | 0.127 | 0.147 | 0.115 | 0.124 | 0.139 | 0.142 |
| pelvic vertical (crest proxy - hip joint) / H | 0.056 | 0.051 | 0.056 | 0.053 | 0.055 | 0.054 | 0.053 | 0.055 | 0.055 | 0.063 | 0.051 | 0.051 | 0.062 | 0.060 |
| HH / H | 0.130 | 0.125 | 0.130 | 0.125 | 0.128 | 0.127 | 0.133 | 0.129 | 0.129 | 0.148 | 0.124 | 0.120 | 0.146 | 0.136 |
| HL / H | 0.119 | 0.114 | 0.126 | 0.114 | 0.117 | 0.116 | 0.113 | 0.119 | 0.118 | 0.135 | 0.109 | 0.109 | 0.131 | 0.127 |

## 2. Raw dimensions (cm; mean of left and right; the builds are mirrored, so see §4)

| Measure | MF-M-R | MF-F-R | MF-FACE-PROJ-MAX | SK | SG | FN | AE | VA | HV | DU | GR | GO | PK | CG |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| upper arm (cm) | 24.90 | 25.68 | 24.90 | 29.46 | 25.53 | 26.86 | 28.33 | 25.99 | 25.68 | 18.16 | 32.86 | 32.03 | 15.58 | 10.47 |
| forearm (cm) | 26.12 | 22.98 | 26.12 | 29.69 | 27.88 | 29.08 | 29.95 | 26.93 | 27.45 | 17.86 | 35.46 | 31.90 | 15.41 | 14.04 |
| hand (cm) | 19.48 | 17.86 | 19.48 | 24.50 | 20.95 | 21.76 | 22.22 | 20.60 | 20.31 | 19.22 | 25.72 | 25.69 | 13.37 | 12.07 |
| palm (cm) | 11.00 | 10.00 | 11.00 | 13.77 | 11.33 | 11.57 | 12.52 | 11.62 | 11.22 | 10.89 | 13.65 | 15.11 | 7.59 | 6.40 |
| femur (cm) | 41.11 | 42.65 | 41.11 | 48.99 | 43.67 | 43.54 | 46.89 | 43.34 | 42.70 | 22.89 | 54.50 | 62.63 | 19.80 | 15.14 |
| lower leg (cm) | 43.88 | 40.45 | 43.88 | 50.96 | 45.47 | 48.32 | 46.58 | 44.06 | 45.62 | 37.43 | 59.49 | 53.84 | 31.18 | 29.12 |
| foot length (cm) | 25.80 | 23.16 | 25.80 | 33.23 | 26.31 | 28.09 | 29.06 | 26.68 | 26.37 | 23.59 | 31.91 | 35.94 | 18.38 | 14.64 |
| elbow breadth (cm) | 8.84 | 7.84 | 8.84 | 10.56 | 8.87 | 8.92 | 9.10 | 8.93 | 8.89 | 8.26 | 10.08 | 10.96 | 6.26 | 5.13 |
| wrist breadth (cm) | 5.53 | 5.33 | 5.53 | 7.81 | 5.69 | 5.43 | 5.99 | 5.88 | 5.56 | 6.20 | 6.85 | 8.46 | 3.89 | 3.53 |
| knee breadth (cm) | 11.90 | 11.17 | 11.90 | 14.30 | 12.21 | 11.98 | 12.43 | 12.30 | 12.45 | 11.88 | 12.04 | 15.25 | 9.15 | 6.97 |
| torso length (cm) | 49.06 | 49.45 | 49.06 | 61.53 | 49.29 | 49.07 | 52.40 | 50.49 | 49.68 | 43.11 | 57.84 | 63.49 | 29.68 | 25.28 |
| thorax breadth max (cm) | 32.95 | 29.51 | 32.95 | 40.92 | 33.36 | 32.68 | 33.69 | 33.66 | 33.45 | 32.25 | 37.32 | 45.09 | 22.25 | 17.92 |
| thorax depth max (cm) | 22.93 | 21.51 | 22.93 | 29.57 | 22.64 | 22.42 | 23.11 | 24.18 | 23.13 | 22.94 | 26.38 | 32.88 | 15.78 | 12.86 |
| iliac-crest proxy breadth (cm) | 28.62 | 27.44 | 28.62 | 34.20 | 29.01 | 27.98 | 28.86 | 29.29 | 29.10 | 25.58 | 32.91 | 37.05 | 20.30 | 14.95 |
| bitrochanteric (cm) | 33.28 | 36.68 | 33.28 | 39.72 | 33.73 | 33.23 | 33.93 | 33.97 | 33.83 | 31.22 | 38.52 | 42.63 | 24.32 | 19.71 |
| pelvic depth (cm) | 22.26 | 22.34 | 22.26 | 25.72 | 22.54 | 22.68 | 23.19 | 22.75 | 22.61 | 20.13 | 25.13 | 28.39 | 14.85 | 12.96 |
| volume (L, rest) | 62.77 | 57.94 | 62.81 | 119.59 | 65.44 | 64.75 | 72.66 | 68.69 | 66.03 | 45.68 | 103.00 | 145.63 | 18.78 | 9.52 |

## 3. Craniofacial (r3, E layer; body frame as the FH\*-equivalent frame)

| Measure | MF-M-R | MF-F-R | MF-FACE-PROJ-MAX | SK | SG | FN | AE | VA | HV | DU | GR | GO | PK | CG |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HL (cm) | 20.646 | 19.807 | 21.846 | 23.743 | 20.908 | 21.026 | 21.505 | 21.098 | 20.968 | 18.463 | 23.798 | 24.995 | 14.067 | 11.540 |
| HH (cm) | 22.513 | 21.707 | 22.513 | 26.036 | 22.810 | 22.945 | 25.260 | 23.027 | 22.880 | 20.298 | 26.959 | 27.461 | 15.581 | 12.355 |
| FPI | 0.143 | 0.169 | 0.191 | 0.145 | 0.144 | 0.144 | 0.142 | 0.144 | 0.144 | 0.142 | 0.145 | 0.149 | 0.139 | 0.138 |
| MPI | 0.051 | 0.049 | 0.103 | 0.050 | 0.051 | 0.051 | 0.050 | 0.051 | 0.051 | 0.054 | 0.049 | 0.050 | 0.053 | 0.055 |
| MdPI | -0.003 | -0.033 | 0.052 | -0.004 | -0.003 | -0.003 | -0.003 | -0.003 | -0.003 | 0.002 | -0.004 | -0.004 | 0.002 | 0.002 |
| FVI | 0.841 | 0.795 | 0.841 | 0.840 | 0.842 | 0.839 | 0.862 | 0.839 | 0.842 | 0.862 | 0.841 | 0.840 | 0.874 | 0.889 |
| CBH | 1.077 | 1.056 | 1.077 | 1.076 | 1.077 | 1.077 | 1.038 | 1.077 | 1.077 | 1.116 | 1.040 | 1.119 | 1.080 | 1.106 |
| FVB | 0.816 | 0.793 | 0.816 | 0.817 | 0.817 | 0.814 | 0.863 | 0.814 | 0.817 | 0.808 | 0.846 | 0.786 | 0.845 | 0.849 |
| MVI | 0.265 | 0.259 | 0.265 | 0.265 | 0.266 | 0.264 | 0.254 | 0.263 | 0.266 | 0.263 | 0.273 | 0.265 | 0.259 | 0.257 |
| FDH | 0.907 | 0.923 | 1.012 | 0.907 | 0.907 | 0.910 | 0.835 | 0.910 | 0.906 | 0.889 | 0.877 | 0.908 | 0.877 | 0.903 |
| Eu-Eu (cm) | 14.619 | 14.555 | 14.619 | 16.886 | 14.810 | 14.897 | 15.580 | 14.949 | 14.855 | 13.441 | 16.927 | 18.526 | 9.910 | 7.955 |
| Zy-Zy (cm) | 13.990 | 13.821 | 13.990 | 16.144 | 14.172 | 14.254 | 14.981 | 14.304 | 14.214 | 12.858 | 16.182 | 17.685 | 9.486 | 7.526 |
| ORB breadth / HL (E proxy) | 0.149 | 0.120 | 0.141 | 0.145 | 0.143 | 0.126 | 0.128 | 0.152 | 0.151 | 0.128 | 0.145 | 0.151 | 0.140 | 0.149 |
| ORB height / HH (E proxy) | 0.096 | 0.121 | 0.096 | 0.108 | 0.114 | 0.125 | 0.088 | 0.096 | 0.091 | 0.198 | 0.093 | 0.130 | 0.217 | 0.184 |
| aperture width / orbit breadth | 0.676 | 0.945 | 0.676 | 0.709 | 0.709 | 0.847 | 0.771 | 0.675 | 0.683 | 0.795 | 0.707 | 0.701 | 0.689 | 0.651 |
| aperture height / orbit height | 0.332 | 0.321 | 0.332 | 0.300 | 0.276 | 0.348 | 0.325 | 0.343 | 0.347 | 0.150 | 0.335 | 0.247 | 0.130 | 0.159 |
| globe diameter (cm; DER except MF-F-R, fitting 2.30 cm by author ruling) | 2.400 | 2.300 | 2.400 | 2.763 | 2.431 | 2.445 | 2.451 | 2.453 | 2.438 | 2.196 | 2.769 | 3.030 | 1.617 | 1.297 |
| aperture width L/R (cm) | 2.08/2.08 | 2.24/2.24 | 2.08/2.08 | 2.44/2.44 | 2.12/2.12 | 2.24/2.24 | 2.12/2.12 | 2.16/2.16 | 2.16/2.16 | 1.88/1.88 | 2.44/2.44 | 2.64/2.64 | 1.36/1.36 | 1.12/1.12 |
| aperture height L/R (cm) | 0.72/0.72 | 0.84/0.84 | 0.72/0.72 | 0.84/0.84 | 0.72/0.72 | 1.00/1.00 | 0.72/0.72 | 0.76/0.76 | 0.72/0.72 | 0.60/0.60 | 0.84/0.84 | 0.88/0.88 | 0.44/0.44 | 0.36/0.36 |
| FPI pitch -3° / +3° | 0.132/0.154 | 0.160/0.178 | 0.180/0.199 | 0.133/0.155 | 0.132/0.154 | 0.132/0.154 | 0.130/0.153 | 0.132/0.154 | 0.132/0.154 | 0.130/0.152 | 0.132/0.156 | 0.137/0.159 | 0.127/0.149 | 0.127/0.148 |
| FH* proxy tilt Po*->Or* (deg, + = face up) | 11.4 | 11.6 | 11.4 | 8.0 | 8.2 | 8.1 | 12.2 | 11.3 | 8.5 | -8.9 | 11.7 | 9.1 | -8.9 | -4.5 |

**Notes:**
- **FAL** follows r3 L40 literally: the more anterior of subnasale and the soft-tissue alveolar point A'.
  - On every candidate it is subnasale.
  - An earlier draft took the anterior-most point of a 75 % upper-lip window. FAL then always fell on the window edge, so FPI was set by the window. That was replaced after the audit.
  - FPI moved by about −0.01 on every candidate: MF-M-R 0.143.
- **Pr** is a method choice: the cutaneous upper lip at 75 % from subnasale to labrale superius. MPI depends on it.
- The orbit E-proxies are **low confidence**: they read a soft-tissue rim, not bone.
- The globe diameter is DER from the generator socket: 2.76–3.03 cm in SK, GR and GO (generator allometry; gate item) and 1.30–1.62 cm in the PK and CG proxies.
- The Po\* proxy is the deepest concha point (no ear canal in the generator). The implied FH\* tilt is reported, not used.

## 4. Left / right readings (cm)

| Measure | MF-M-R | MF-F-R | MF-FACE-PROJ-MAX | SK | SG | FN | AE | VA | HV | DU | GR | GO | PK | CG |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| upper arm (cm) L/R | 24.90/24.90 | 25.68/25.68 | 24.90/24.90 | 29.46/29.46 | 25.53/25.53 | 26.86/26.86 | 28.33/28.33 | 25.99/25.99 | 25.68/25.68 | 18.16/18.16 | 32.86/32.86 | 32.03/32.03 | 15.58/15.58 | 10.47/10.47 |
| forearm (cm) L/R | 26.12/26.12 | 22.98/22.98 | 26.12/26.12 | 29.69/29.69 | 27.88/27.88 | 29.08/29.08 | 29.95/29.95 | 26.93/26.93 | 27.45/27.45 | 17.86/17.86 | 35.46/35.46 | 31.90/31.90 | 15.41/15.41 | 14.04/14.04 |
| hand (cm) L/R | 19.48/19.48 | 17.86/17.86 | 19.48/19.48 | 24.50/24.50 | 20.95/20.95 | 21.76/21.76 | 22.22/22.22 | 20.60/20.60 | 20.31/20.31 | 19.22/19.22 | 25.72/25.72 | 25.69/25.69 | 13.37/13.37 | 12.07/12.07 |
| palm (cm) L/R | 11.00/11.00 | 10.00/10.00 | 11.00/11.00 | 13.77/13.77 | 11.33/11.33 | 11.57/11.57 | 12.52/12.52 | 11.62/11.62 | 11.22/11.22 | 10.89/10.89 | 13.65/13.65 | 15.11/15.11 | 7.59/7.59 | 6.40/6.40 |
| femur (cm) L/R | 41.11/41.11 | 42.65/42.65 | 41.11/41.11 | 48.99/48.99 | 43.67/43.67 | 43.54/43.54 | 46.89/46.89 | 43.34/43.34 | 42.70/42.70 | 22.89/22.89 | 54.50/54.50 | 62.63/62.63 | 19.80/19.80 | 15.14/15.14 |
| lower leg (cm) L/R | 43.88/43.88 | 40.45/40.45 | 43.88/43.88 | 50.96/50.96 | 45.47/45.47 | 48.32/48.32 | 46.58/46.58 | 44.06/44.06 | 45.62/45.62 | 37.43/37.43 | 59.49/59.49 | 53.84/53.84 | 31.18/31.18 | 29.12/29.12 |
| foot length (cm) L/R | 25.80/25.80 | 23.16/23.16 | 25.80/25.80 | 33.23/33.23 | 26.31/26.31 | 28.09/28.09 | 29.06/29.06 | 26.68/26.68 | 26.37/26.37 | 23.59/23.59 | 31.91/31.91 | 35.94/35.94 | 18.38/18.38 | 14.64/14.64 |

## 5. Pose-invariance readings that bear on measurement (rest → R-6)

- Joint-to-joint segment lengths are unchanged (≤ 2e-5 cm).
- Foot length changes +0.08 to +0.20 cm and foot breadth −0.05 to −0.21 cm.
- Head is unchanged except CG (HL -0.0009 cm, from the proxy's rigid-set residual).
- **Pelvic depth changes +0.00 to +1.22 cm and bitrochanteric breadth -1.40 to -0.17 cm.** The gluteal and hip soft tissue moves when the thighs are re-aimed.
- **Maximum thorax breadth changes −0.84 to −3.22 cm** (axilla).

These are why anatomy is read on the rest geometry (gate D-W1c-1).

## 6. Items each candidate unlocks (W1 manifest) — status

| Item | Candidates | Status |
|---|---|---|
| RM-UB-07 (central, both configurations) | MF-M-R, MF-F-R | Measured (tables 1–2) |
| RM-LR-01 / 02 (ref) / 05 / 07 | MF-M-R, SK, GR, GO | Measured; directions in the audit. GR/GO pelvis and girdle not instantiated |
| RM-LR-06 (ALPC) | GO | **Not demonstrated** (qualitative; the evidence sheet reads lean) |
| RM-OT-01 | SG vs MF-M-R | Measured; all SG directions pass |
| RM-CF-02 (central + maximum) | MF-M-R / MF-F-R / MF-FACE-PROJ-MAX | FPI 0.143 / 0.169 / 0.191 (maximum builder-chosen) |
| RM-CF-03 / 04 central face | GR, GO | FPI 0.145 / 0.149 vs MF 0.143 |
| RM-CF-06 (CBH) | DU, GO vs MF | CBH 1.116 / 1.119 vs 1.077; TBP not run (no Go / Ec–Ec landmark set) |
| RM-CF-07 (FVB with MVI) | GR, AE, SK, MF | Table 3; audit |
| RM-CF-08 (ORB, aperture) | FN | **Not demonstrated:** ORB breadth ÷ HL 0.126 vs MF 0.149 (lower), ORB height ÷ HH 0.125 vs 0.096 (higher); aperture more open |
| RM-CF-10 / RM-SR-04 (HSR) | DU, GR, GO, PK\*, CG\* | HH ÷ H in table 1 (\* proxies); CG HH 12.36 cm |
| RM-UF-01 (MF aperture vs orbit) | MF-M-R | Aperture 2.08 × 0.72 cm; ratios in table 3 |
| RM-UB-01 | SK, SG, FN, AE, VA, HV, DU | Measured (table 1). **SA blocked** (no verified D-2 copy) |
| RM-UB-06 (PK pelvis) | PK\* | Proxy only; pelvis morphology OPEN |
| RM-SR-01 / 02 / 03 | PK\*, CG\*, DU | Proxies for PK and CG; DU measured |

— Claude

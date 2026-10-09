# RAC W2I3 — Saurin Reference-Quality Rebuild / Caudal-Base Closure Gate

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-w2i3-saurin-reference-rebuild-order.md` §1–§18

**Author ruling (October 8, 2026; `reviews/chatgpt-rac-w2i4-saurin-final-asset-order.md` §1-§3):** W2I3 evidence accepted. **L1 ACCEPTED** as the Saurin W2 leg-proportion target; **F2 ACCEPTED** as the Saurin W2 forearm distribution; **L1 + F2 body plan ACCEPTED** (no longer CONSTRAINED; remaining work is asset finish / surface regeneration / final verification); **stature-budget restoration ACCEPTED**; D-B accepted marginal and D-D accepted dependency preserved. **SAU-SILHOUETTE — ACCEPT WITH PRESENTATION CONTEXT:** the dark rounded front-view read is an inherent end-on projection of the approved free tail through the thigh gap in a strict orthographic front camera; no further tail, root-pitch, pelvic, yaw or caudal-base contour change is authorized; caudal biology frozen. Presentation note carried forward (not anatomy). W2I4 final asset finish / canonicalization prep authorized.

**Evidence:** `reviews/rac-w2i3-sa-evidence/`. `tables.md` is generated, and every number below comes from its JSON files.
**Status:** DESIGN / MEASUREMENT / CANDIDATE ONLY — NO UE5.
- **No accepted source anatomy was modified.** SA-M (aff1b52), SA-F (§263), the tool-chain sources and Saurin canon are unchanged.
- The rebuilt candidate exists only as copies. A canonicalization preview with hashes is in §8, and nothing was overwritten.

## Verdicts

| Item | Verdict | One line |
|---|---|---|
| **Clean L1 leg implementation** | **CONSTRAIN** | Reproduces the accepted L1 biology exactly, with no flipped faces, no morph-band crease, and neck strain eased from ×0.45 to ×0.66. The +9.2 cm thigh is still a uniform ×1.5 vertical elongation of the existing thigh relief, and the scale surface is not yet regenerated (§2). |
| **Clean F2 forearm implementation** | **ACCEPT** (candidate) | Forearm / arm 0.366 (inside Marchfolk) and total arm unchanged (−0.05 %). An axillary fold found in a first build was fixed (§3). |
| **Combined rebuilt reference (L1 + F2)** | **CONSTRAIN** | Every accepted W2I suite passes with 0 new failures. It stays a candidate because SAU-SILHOUETTE is unresolved and the scale surface still has to be regenerated (§4). |
| **Caudal-base silhouette candidate** | **REJECT — CAUDAL-BASE LEVER INSUFFICIENT** | C1–C3 do not change the front read on any of the six bodies. A removal test shows the read survives even with the whole caudal-base zone deleted, because it comes from the free tail seen end-on. C2 / C3 also raise a dorsal hump (§5). |
| **Tail coupling after caudal-base correction** | **NOT RUN** | No contour passes. Coupling on the rebuilt limbs is unchanged from W2I2 L1 + F2 (§6). |
| **Saurin stature-budget restoration** | **ACCEPT** | Lower trunk unchanged; legs no longer fund the excess; thoracic −13 %; neck −26 %; head height and head length unchanged (§1). |
| **Saurin W2I final overall** | **CONSTRAIN** | The body plan is restored. The front-view silhouette is the one open item, and it needs an author decision (§9). |

---

## 1. Stature-budget acceptance (order §12)

Ledger shares of standing height, with hip = pelvic station (`tables.md` §1):

| SA-M188 | ground → ankle | ankle → knee | knee → hip | lower trunk | thoracic | neck | head height |
|---|---|---|---|---|---|---|---|
| Frozen | 0.051 | 0.279 | 0.154 | **0.170** | 0.154 | 0.111 | 0.080 |
| W2I2 diagnostic L1 | 0.051 | 0.279 | 0.204 | **0.170** | 0.135 | 0.082 | 0.080 |
| **W2I3 rebuild** | 0.051 | 0.279 | 0.204 | **0.170** | 0.135 | 0.082 | 0.080 |

**Checks:**
- Lower axial trunk unchanged at every stature.
- Legs no longer fund the whole lower-trunk excess. Hip moves from 0.484 to 0.533 H, and leg length from 0.438 to 0.486 H.
- Thoracic vertical falls 13 % and neck vertical falls 26 % against the frozen body.
- Head height and head length are unchanged (31.871 cm). Head and rostrum are not used as levers.
- SA-F188, SA-M168, SA-M203 and SA-M208 show the same pattern to 3 decimals.

## 2. Clean L1 implementation (order §3–§4)

**What changed from the W2I2 study warp** (driver `w2i3_drivers/sa_rebuild.py`):

| Region | W2I2 study | W2I3 rebuild |
|---|---|---|
| Thigh | narrow band | the whole thigh from the knee fields to the hip crease, with a flat core, so the thigh lengthens uniformly |
| Neck | 13-cm band, compressed to ×0.45 | the whole free neck from inlet to below the chin, ×0.66 |
| Shoulder cap | carried rigidly (crease source) | arm vertices above the shoulder line follow the trunk / neck field, so the deltoid cap and trapezial slope move together |

Horizontal cross-sections are unchanged everywhere, so limb and neck girths stay as accepted.

**The biology reproduces the accepted L1 exactly** (`tables.md` §2):

| Reading | Rebuild | W2I2 diagnostic |
|---|---|---|
| Hip / H (SA-M188) | 0.5333 | 0.5333 |
| Leg length / H | 0.4864 | 0.4864 |
| Femur / leg | 0.420 | 0.420 |
| Thoracic / H | 0.1347 | 0.1348 |
| Neck / H | 0.0821 | 0.0820 |

- Durrim separation: 24 / 24 PASS, +1.1 … +3.5 %.
- Marchfolk: −4.3 … +0.5 %.
- Grask, and the elf single readings, are unchanged from L1.

**Surface strain against the frozen body** (edge-length ratio, SA-M188; `strain.json`):

| Region | W2I2 diagnostic: min / p1 / p99 / max | **W2I3 rebuild: min / p1 / p99 / max** |
|---|---|---|
| Thigh | 0.93 / 1.00 / 1.48 / 1.51 | 0.92 / 1.00 / 1.50 / 1.68 |
| Thorax | 0.49 / 0.85 / 1.10 / 2.04 | **0.55 / 0.85 / 1.05 / 1.74** |
| Neck | 0.45 / 0.48 / 1.00 / 1.01 | **0.66 / 0.67 / 1.00 / 1.02** |
| Arm | 0.41 / 0.78 / 1.34 / 1.76 | **0.55 / 0.78 / 1.26 / 1.62** |
| Flipped faces | 0 | **0** |

Female centre: same pattern, 0 flips.

**Inspection** (`sheets/w2i3_rebuilt_188.jpg`, family sheet, and close views of shoulders, neck, elbow, thigh and knee during the build):
- The W2I2 crease across the shoulder tops and under the chin is gone.
- Trapezial slope, hip crease, adductor flow and knee-to-thigh continuity read as continuous.
- No pinching, melting or duplication is visible.

**Why CONSTRAIN, not ACCEPT.**
- Adding 9.2 cm across the ~23-cm thigh band (knee fields to hip crease) is inherently a ×1.5 vertical elongation. The rebuild spreads it uniformly; it cannot be lower without changing the accepted femur / leg target.
- The existing muscle relief is therefore elongated, not re-modelled.
- The **scale-field surface realization (Gate 7 `g7surf` / `g7regs`) must be regenerated** on the rebuilt base before the reference is final. The current fields would stretch with the base.
- This rebuild is a procedural regeneration, not a hand sculpt. The author should decide whether the remaining thigh elongation is reference quality or needs an artist pass.

## 3. Clean F2 implementation (order §13)

Within-arm redistribution over the upper arm below the axilla and the whole forearm. Elbow and wrist zones are carried rigidly; peak densities are ×0.77 (upper arm) and ×1.28 (forearm).

**SA-M188, rebuild vs frozen:**

| Reading | Frozen | Rebuild |
|---|---|---|
| Total arm / H | 0.4007 | 0.4005 |
| Arm-to-wrist / H | 0.2884 | 0.2881 |
| Forearm / arm | 0.312 | **0.366** |
| Forearm / upper arm | 0.764 | 1.037 |
| Hand / arm | 0.280 | 0.281 |
| Elbow height | 117.0 | 127.0 cm (with L1) |

**Margins:**
- vs Marchfolk forearm / arm: −1.1 … +1.2 % (inside the band).
- vs Cogling: −5.4 … −9.2 %.
- vs Grask 208: below on every row.
- Total arm vs Marchfolk: −1.3 … −3.8 % (moderate).

**Fix found during the build.** A first build started the upper-arm band at 6 % of the shoulder → wrist chord and folded 148 axillary faces. The band now starts at 12–18 % and the fold is gone (0 flips). The rejected version is not used.

## 4. Combined rebuilt reference — full regression (order §11)

All 62 W2I bodies were rebuilt (`bodies_R.json`) and run through the accepted, unchanged evaluators:

| Suite | Result |
|---|---|
| Stature family 168 / 188 / 203 / 208 (SAU-BODY-01) | ST 64 / 64 |
| Continuity | C 26 / 26 |
| Frames (SAU-BODY-05) | FR 104 / 104 |
| Composition (SAU-BODY-06 / 07) | CO 96 / 96 |
| §263 sex cases (SAU-BODY-19) | 17 PASS + the 2 canon "request exceeds" cases; clamps reproduce |
| Lower-trunk floor 168 / 203 | LTF 8 / 8 |
| Matched-height directions (SAU-BODY-03 / 12 / 21 / 22, RM-OT-04 body) | M 138 / 138 |
| Body-only passing, with / without tail | P 76 / 76, P0 76 / 76 |
| Gorrund never-collapse | G 6 / 6 |
| Durrim leg separation (SAU-BODY-16 body rows) | 24 / 24 |
| Cogling forearm separation (SAU-BODY-15) | 8 / 8 |
| Grask reach (SAU-BODY-13) | 14 PASS + D-B Broad 208 span +0.52 % (accepted marginal) |
| SAU-BODY-04 / 17 / 18 | Tail, pelvis and caudal base move as one rigid unit; foot unchanged; TL as below |
| SAU-BODY-10 | Lean 8.43° (frozen 8.82°); no hunch or crouch |

**Result changes vs the frozen re-run:** one. SA-M208-B-T80 now passes the old SA-M-referenced lean guard, because the longer legs lower lean by about 0.4°.

**Result changes vs the W2I2 diagnostic:** none.

## 5. Caudal-base contour family C0–C3 (order §5–§10)

**Lever** (`sa_caudal.py`, in the accepted tail frame):
- Ventral offsets are scaled by (1 − a·w). Dorsal offsets are scaled by (1 + b·w), with b set so the ventral + dorsal half-depth sum is conserved.
- The weight w is 0 at the caudal-base landmark, ramps over 8 cm, is flat to 30 cm distal, then fades over 12 cm.
- Settings: a = 0 / 0.2 / 0.4 / 0.6 for C0 / C1 / C2 / C3.

**Invariants on every body:**
- Landmark shift 0.
- Every vertex outside the zone unchanged (pelvis, legs, stance).
- Root area −0.5 / −1.0 / −1.5 %; RSI_raw +0.7 / +1.3 / +2.0 %, inside the coupling solution.
- Δlean ≤ +0.07°.

**Results (rebuilt bodies):**

| Body | C0 visible extent / width | C1–C3 visible extent | Gap pixels: zone / free tail (C0 → C3) | Dorsal rise at 10 cm, C1 / C2 / C3 |
|---|---|---|---|---|
| SA-M188 | 11.5 cm / 13.1 | 11.5 / 11.5 / 11.5 | 0.64 / 0.36 → 0.64 / 0.36 | 2.4 / 4.8 / 7.2 cm |
| SA-F188 | 18.2 / 13.3 | 18.8 / 18.8 / 18.8 | 0.75 / 0.25 → same | 2.4 / 4.8 / 7.1 |
| SA-M168 | 9.7 / 11.8 | 9.7 / 9.7 / 9.7 | 0.58 / 0.42 → same | 2.1 / 4.3 / 6.4 |
| SA-F168 | 15.7 / 12.1 | 15.8 / 15.8 / 15.8 | 0.75 / 0.25 → same | 2.1 / 4.2 / 6.4 |
| SA-M208 | 20.8 / 14.3 | 21.5 / 21.5 / 21.5 | 0.74 / 0.26 → 0.75 / 0.25 | 2.7 / 5.3 / 8.0 |
| SA-F208 | 19.9 / 14.6 | 20.5 / 20.8 / 20.9 | 0.75 / 0.25 → 0.76 / 0.24 | 2.6 / 5.3 / 7.9 |

The female and 208 extents read high partly because the crotch rule lands on perineal tissue on those bodies; widths and gap decomposition are the robust readings.

**Visual read** (`sheets/w2i3_caudal_M188.jpg`, `_F188.jpg`: full front / profile / rear 3/4, close front, below-front, rear close root, side close root):
- The dark rounded mass between the thighs is unchanged in C1–C3.
- In profile, C2 and C3 show a clear **dorsal hump** behind the sacrum. That fails the order §7 firewall.
- C1 adds a smaller step with no front benefit.

**Why the lever cannot work** (`sheets/w2i3_zone_split_R188.jpg`, panels: full / caudal-base zone + proximal 42 cm deleted / zone only / free tail only):
- **With the whole caudal-base zone and the proximal 42 cm of tail deleted, the front read is essentially unchanged.**
- It is formed by the **free tail beyond about 42 cm from the landmark**, seen end-on through the thigh gap: a tapered section about 13 cm wide whose underside hangs 10–20 cm below the crotch.
- The W2I2 "tail removed" render had shown an extra dark form at the gap apex. That form belongs to the zone and does contribute, but removing it alone does not clear the read.
- Any change that does clear it needs the **free-tail path or its ventral contour**: carriage, which W2I2 showed needs about +14° and was rejected, or free-tail thickness, which is forbidden.

→ **CAUDAL-BASE LEVER INSUFFICIENT.** As ordered, no thinning, yaw, pelvic remodelling or larger pitch was tried.

## 6. Tail coupling (order §14)

**NOT RUN**, since no contour passes.

For the rebuilt limbs at neutral carriage, the tail is identical to W2I2 L1 + F2 and lean differs by ≤ 0.06°. The W2I2 same-state coupling run on L1 + F2 therefore stands (`rac-w2i2-sa-evidence/tailcap_L1F2.json`):

| Case | Same-state cap (RSI 1.19 base) |
|---|---|
| Balanced | 78.9 % |
| Broad | 80.4 % |
| Narrow + high fat | 79.75 % |
| Broad 208 | 79.9 % (D-B marginal holds) |

55 % still needs a substantial base.

## 7. Complete non-pass accounting

| Item | Classification |
|---|---|
| Leg contradiction / SAU-BODY-16 leg rows | **RESOLVED BY D-A CANDIDATE** (rebuilt L1; 24 / 24) — candidate only |
| Forearm contradiction | **RESOLVED BY D-A CANDIDATE** (rebuilt F2) — candidate only |
| W2I2 morph-band strain (neck ×0.45, shoulder crease) | **RESOLVED** in the rebuild (neck ×0.66, crease gone, 0 flips) |
| Thigh uniform ×1.5 elongation; scale surface not regenerated | **NAMED DEPENDENCY** (asset regeneration / optional artist pass before canonicalization) |
| SAU-SILHOUETTE | **UNRESOLVED** — distal carriage, root carriage and caudal-base contour all insufficient; the cause is the free tail seen end-on |
| Broad ~80 % / Broad 208 span +0.5 % | **ACCEPTED MARGINAL D-B** |
| Skeletal-mass rows | **ACCEPTED MEASUREMENT LIMIT D-D** |
| TL Balanced 80 %, Narrow + fat 78 % (base 1.15) | REPORT-ONLY |
| RM-UB-08 numeric ranges | **NAMED DEPENDENCY** |
| Facial dependencies (RM-OT-04 OPEN rows, RM-UF-04) | **NAMED DEPENDENCY** |
| Claw numeric ranges | **NAMED DEPENDENCY** |
| Final density / neutral idle / dynamic posture | **NAMED DEPENDENCY** |
| SAU-BODY-20 world-space | **OUT OF SCOPE** |

## 8. Source anatomy and canonicalization preview (order §16)

**Not modified:**
- `saurin_final_base.npz` (SHA-256 `a925e067…`);
- the §263 SA-F parameters;
- `tools/rodin/*`;
- `specs/saurin/SAURIN_V1.md`.

**Candidate hashes** (scratch preview files, not committed or deployed; `canon_preview.json`):

| Item | Value |
|---|---|
| Rebuilt SA-M188 base file | `f59b050f…` |
| Rebuilt SA-M188 vertex array | `36006753…` |
| Faces | unchanged topology, 1,124,235 vertices |
| Rebuilt SA-F188 realization | `20ad90bb…` |

**The candidate is NOT ready for canonical overwrite**, because SAU-SILHOUETTE is unresolved and the scale surface is not regenerated. If the author later accepts it, these would change:

1. **Mesh and PC asset files** (`RaceBodies/out/`):
   - a new frozen base replacing `saurin_final_base.npz`;
   - `saurin_final_surface_delta.npz`, `rebuild_final.py`, `SaurinFinal.blend` / `.fbx`;
   - the regenerated scale surface (`gate1/g7regs.py`, `g7surf.py`) and `g15reg` labels.
2. **Tool chain:**
   - `Lbase.pkl` (stations and labels; topology is unchanged, so labels carry over);
   - Part 7 `ref_metrics.json`;
   - the Gate 8 `axis.npy` (tail axis translated +9.2 cm with the pelvis);
   - `g7geo.py` `ARM` / `LEG` construction points: elbow, knee and hip (B1 hip, or the pelvic station adopted as hip joint);
   - the §263 `fsets3` re-verification.
3. **Canon text** (`specs/saurin/SAURIN_V1.md`):
   - the Part 7 reference metric tables (heights of hip / knee / costal / inlet / shoulder);
   - an explicit stature-budget line confirming L970;
   - the §17 forearm wording note (author 1B interpretation);
   - §258 bounds re-verified (neck ±15 %, leg ±6 %, arm ±6 %);
   - §263 accounting (lower trunk 32.0 → 33.6 unchanged).
4. **Records:**
   - `decisions/REFERENCE_ANATOMY_V1.md` ARM entry (new SA-M / SA-F hashes; the old ones kept as W1 / W2I provenance);
   - `cfg/w2i/SA-boundary.json`;
   - `rac-w1-evidence/saurin_w1.json`;
   - W2I / W2I1 / W2I2 evidence re-run on the new base;
   - `specs/STATUS.md`.

## 9. Author decision requested — SAU-SILHOUETTE

Three bounded levers have now failed for one geometric reason. A substantial tail that leaves the pelvis near crotch height and runs back nearly level is seen end-on through the thigh gap in a strict orthographic front view.

The remaining choices are the author's:
- **(a)** Accept that end-on read as inherent to the approved tail. Judge SAU-SILHOUETTE on shaded / material renders and the 3/4 front; the order's own question is about being "readily mistaken".
- **(b)** Authorize a free-tail neutral path change: a larger rest lift than +8°, or a higher proximal path.
- **(c)** Carry it as a named dependency to the posture / animation phase.

No anatomy change is proposed by the builder.

---

**STOP.** SA-M / SA-F were not overwritten and the rebuilt candidate is not marked canonical. Wave 3, the roster world-scale review, creator envelopes, the internal skeleton, UE5, rigging, animation, equipment and gameplay were not begun. The W2I3 package goes to the author for review.

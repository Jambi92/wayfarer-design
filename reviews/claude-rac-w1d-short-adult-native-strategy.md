# RAC W1d — Pipkin / Cogling Native Short-Adult Strategy and First Test Bodies

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §5 (work order item 6)
**Status:** METHOD + FIRST TEST BODIES FOR AUTHOR ACCEPTANCE.
- The PK and CG W1c proxies are **not replaced** until the author accepts.
- Stature canon is unchanged (PK 107 cm, CG 91 cm).

**Evidence:** `reviews/rac-w1d-evidence/native-short/`:
- `PK-NAT_*`, `CG-NAT_*` (geometry, measurements, invariance, evidence sheets);
- `native_short_checks.json`;
- allometry data in `allometry/allo.json`.

**Tools:** `tools/rac/w1/native_short.py`, `native_short_allometry.json`, `cfg/PK-NAT.json`, `cfg/CG-NAT.json`.

## 1. Why the W1c proxies cannot stand, and what the generator offers

- **Proxies:** the W1c PK and CG are MakeHuman's minimum-height adult (about 137 cm, configuration 1) **uniformly scaled** ×0.7675 and ×0.6373. That fails R-2.
- **Generator range:** about 137–243 cm (configuration 1; `allometry/allo.json`) and 123–229 cm (configuration 2; session probe, not retained as an evidence file). Neither reaches 107 or 91 cm natively.
- **Generator minimum-height model is anatomically implausible.** Measured on clean configuration-1 builds at age 35 (`allometry/allo.json`): at 137.6 cm the joint-to-joint femur is 23.8 cm and the tibia 39.2 cm. At 173 cm they are 41.1 and 43.9 cm.
  - The generator gets short stature mostly by collapsing the thigh.
  - This also affects the W1c **DU** candidate (height macro 0.03): its low femur ÷ leg (0.380) is partly a generator artefact. This is recorded for DU's rebuild.

## 2. Strategy options (order §5 hierarchy)

| # | Option | Status |
|---|---|---|
| 1 | **Purpose-built / sculpted short-adult base geometry** | **Preferred long-term.** It needs a sculpted base (outside this tool chain's procedural reach). Recommended for the final PK and CG ARMs |
| 2 | **Modelling workflow directly authored at target stature** | **Implemented here as the first test** (§3) |
| 3 | Another native base | Not available: no other generator in the tool chain reaches an adult at 91–107 cm |

## 3. The option-2 workflow as implemented

1. **Source anatomy.** Start from the accepted human reference construction (MF-M-R settings: MPFB adult, age 35, height macro 0.5) plus the race's generator targets (proportion directions). It is **not** the generator's minimum-height model.
2. **Regional re-proportioning at the target stature.** Each region gets its own factor, applied as a pose-bone scale in bone space with inherit-scale off, then baked into the rest mesh and the rig:

   | Region | Factor rule | PK | CG |
   |---|---|---|---|
   | Segment lengths (all non-head bones, bone Y) | One length factor, solved so the **R-6 stature equals the target** | 0.6153 | 0.5218 |
   | Trunk/limb breadth and depth, joints (bone X/Z) | Isometric with length (β = 1), see §4 | 0.6153 | 0.5218 |
   | Head (uniform) | PK: generator adult head allometry (β 0.688). CG: the factor that targets HH 12 cm, the midpoint of the canon "roughly 11–13 cm" (CG L1585, W1-A1; the midpoint is BUILDER-CHOSEN; measured HH 11.81 cm) | 0.7159 | 0.5127 |
   | Hands (uniform) | Generator adult hand allometry (β 0.842) | 0.6644 | 0.5784 |
   | Feet (uniform) | Generator adult foot allometry (β 0.942) | 0.6329 | 0.5419 |
   | Landmark globe | DER from the head-scaled socket | 1.72 cm | 1.23 cm |

3. **R-6 pose, measurement and checks** exactly as W1c, under the scope-limited D-W1c-1.
   - Stature: PK 107.00 cm; CG 90.99 cm.
   - Rigid sets ≤ 0.11 cm; volume −0.50 % / −0.72 %; eye fit clean (clearance 0.019 / 0.014 cm).

**The betas are BUILDER-CHOSEN.** They are log-log slopes of the generator's own adult size allometry over 159–243 cm; the implausible minimum-height builds are excluded. Extrapolating them to 91–107 cm is a choice, not a fact.

## 4. A rejected variant (disclosed)

The first native builds used the generator's girth allometry for the trunk and limbs (β 0.654). That made both bodies broad-chested: thorax breadth ÷ stature was 0.210 (PK) and 0.213 (CG) against MF 0.190 (session builds, superseded; not retained as evidence files). **This contradicts Cogling canon**: "comparatively narrow-to-moderate transversely" (CG L102), "narrow stable central core" (CG L98). It also strains Pipkin's "comparatively moderate" thorax (PK L133). Girth was therefore set isometric (β = 1), and the race targets then carry the canon directions. A check was added for CG: thorax breadth ÷ stature < MF.

## 5. Results (diagnostic)

| Ratio (÷ stature unless stated) | MF-M-R | PK-NAT | CG-NAT | PK proxy (W1c) | CG proxy (W1c) |
|---|---|---|---|---|---|
| Torso share | 0.283 | 0.273 | 0.281 | 0.277 | 0.278 |
| Leg share (hip-joint height) | 0.532 | 0.531 | 0.537 | 0.523 | 0.530 |
| Arm share | 0.407 | 0.414 | 0.415 | 0.415 | 0.402 |
| Femur ÷ leg | 0.484 | 0.485 | 0.477 | 0.388 | 0.342 |
| Upper arm ÷ arm | 0.353 | 0.346 | 0.291 | 0.351 | 0.286 |
| Forearm ÷ arm | 0.371 | 0.363 | 0.388 | 0.347 | 0.384 |
| Hand ÷ arm | 0.276 | 0.292 | 0.322 | 0.301 | 0.330 |
| HH ÷ H | 0.130 | 0.151 | 0.130 | 0.146 | 0.136 |
| HH (cm) | 22.51 | 16.19 | 11.81 | 15.58 | 12.36 |
| Thorax breadth | 0.190 | 0.188 | 0.182 | 0.208 | 0.197 |
| Pelvic vertical | 0.0555 | 0.0553 | 0.0551 | 0.062 | 0.060 |
| Iliac crest ÷ thorax breadth | 0.869 | 0.949 | 0.915 | 0.912 | 0.834 |
| Globe (cm) | 2.40 | 1.72 | 1.23 | 1.62 | 1.30 |

**Directional checks** (`native_short_checks.json`, same check set as W1c plus the CG narrow-thorax check):
- **CG-NAT: all CG checks pass.** That includes torso, arm and leg ≈ MF; the distal redistribution; HH 11.81 cm (inside 11–13); FVI ≥ MF; narrow thorax; and the structural-mass axis CG < PK < DU.
- **PK-NAT: all PK checks pass except "pelvic vertical contribution ÷ stature > MF"** (0.0553 vs 0.0555).
  - The pelvic packet (PV-D10) questions whether this per-stature check is canon.
  - **But its own proposal PK-P3 (≥ MF) is also failed, marginally.** So accepting PV-D10 does not by itself make PK-NAT pass.
  - The W1c proxy read 0.062 with the same `hip-scale-vert-incr` target. **The native workflow loses part of that Pipkin pelvic signal**: the generator's minimum-height model inflated it, and the 173 cm source does not. This is a build issue to correct after the pelvic packet is decided, not a canon issue.
- The femur ÷ leg artefact of the proxies is gone.

## 6. What remains questionable (author judgement)

1. **R-2 intent.** Only the head, hands and feet (and the globe) depart from a uniform rescale of the race-target body; trunk and limb girths are isometric by choice (§4). The body is authored at target stature region by region with explicit factors, but the author must rule whether that meets "never by uniform scaling from another population or stature". **If not, option 1 (sculpted base) is required.**
2. **PK head share** is 0.151 vs MF 0.130 (+16 %), produced purely by the allometric head rule. Canon allows "somewhat > MF only as allometry" (PK L33; RAC-04 L44). Whether +16 % is "somewhat" is an author call.
3. **Globe size.** DER from the scaled socket gives 1.72 cm (PK) and 1.23 cm (CG), far below an adult-human globe. Canon says PK and CG orbits and apertures stay "within the broad adult Marchfolk-compatible range" and are never enlarged (PK L299; CG L1199). Whether that range is **absolute** (adult-human globe size, which would make the eyes relatively large: juvenile risk) or **relative** (scaled, as here) is an author decision.
4. **CG FVI** is 0.877 vs MF 0.841. Canon says "at or slightly above" (CG L1131). Whether +4 % is "slightly" is the author's call.
5. **Ears** are the human auricle. The PK compact-rounded and CG fine-folded families are not yet built (the ear packet covers six families; PK and CG ears are derivable from a human-structured auricle, per the W1 canon brief).

## 7. Author decisions needed

- **S-D1:** accept the option-2 workflow (§3) as R-2 compliant for PK and CG, **or** require option 1 (sculpted base).
- **S-D2:** accept the builder-chosen factor rules: head (PK allometric; CG at HH 12 cm), hands and feet (allometric), girth isometric.
- **S-D3:** the PK and CG globe/orbit reading: absolute adult-human, or relative (scaled).
- **S-D4:** if S-D1 is accepted, replace the W1c proxies with PK-NAT and CG-NAT as CONSTRAINED candidates. The PK pelvis (pelvic packet PV-D decisions) and the PK/CG ears remain open.

— Claude

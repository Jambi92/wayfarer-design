# RAC W1s — Halvren W1 Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Order:** `reviews/chatgpt-cogling-final-acceptance-halvren-w1-order.md`, the same text as GitHub Issue #1 comment 2026-10-07T18:57Z.
**Evidence:** `reviews/rac-w1s-hv-evidence/` (`tables.md` holds every number quoted)
**Construction record:** `tools/rac/w1/cfg/w1s/HV.json`

Nothing here is accepted. Specs and `STATUS.md` are untouched. The HV body is a diagnostic anchor inside the mixed-population envelope, not a mandatory Halvren phenotype.

## Recommendation: accept HV as built (177.7 cm) as the Halvren W1 reference — no correction proposed

The as-built HV keeps a coherent mixed body. Measured against the six accepted sources directly (MF-M-R, SK, SG, Fenn FNL4, Aelari AEL1, Vael VAL4; no averaged Human or Elf parent):

| Check | Result |
|---|---|
| Every body reading inside the six-source span | 25 / 26 PASS; ankle ÷ stature MARGINAL (0.2 % below SG) |
| No domain duplicates one source | PASS in all three body domains (most: axial 5 / 7 within 1 % of SG; appendicular 9 / 14 of VA) |
| Body not a human with pointed ears / not an elf with human proportions | 13 of 26 body readings nearest an elven source, 13 nearest a human source |
| Not an arithmetic average | at most 5 of 22 discriminating readings at any human–elf midpoint (SK + FN); 0 of 3 for MF + VA |
| Joint coupling | spread across the four joints 3.9 points vs MF, inside the sources' own spreads (0.4–22.2) |
| Pelvis not a linear morph | skeletal-proxy pelvis inside the span at every t; MF→elf interpolation fractions differ by reading (FN −0.36…1.80, AE −0.30…0.12, VA −0.71…0.32) |
| Ear architecture | continuous elven taper law (human ear has none), length between families, taper starting later than any elven ear, human lobe; not a copy of any source ear |
| Existing directional rows (source span) | 8 / 8 |

**One scored row fails, and I don't think it can carry a verdict:** orbit breadth ÷ head length is +1.2 % above every source. Probes that change only the eye target show the reading is not stable:

| Eye-scale target | 0 (HVC1) | 0.05 (HVC2) | 0.1 (as built) |
|---|---|---|---|
| Orbit breadth vs MF | +0.5 % | −15.5 % | +1.2 % |

The eye itself is unchanged (eye diameter ÷ head height = MF). **Option for the author:** HVC1 removes the eye-scale target (body unchanged). It avoids anything like a "slightly larger eyes" marker (HALVREN L223; order item 11), but leaves HV with an essentially Marchfolk head (§3).

**No accepted canon is challenged.**

## 1. Expression recipe by domain (order items 4, 8; tables §1)

Nearest accepted source per reading; no ancestry percentages.

| Domain | Nearest human | Nearest elven | Where |
|---|---|---|---|
| Axial skeleton | 2 | 5 | Vael-nearest torso, neck, thoracic and shoulder breadth; Marchfolk-nearest thoracic depth (−4.0 % vs VA: not Vael depth) |
| Appendicular skeleton | 7 | 7 | Vael-nearest limb totals and leg segments; Sagekin-nearest forearm share and pelvis ratios; finer wrist than MF (−2.0 %) |
| Distal anatomy | 4 | 1 | Skarn/Sagekin-nearest finger ÷ palm and palm breadth; Aelari-nearest hand share |
| Craniofacial | 6 | 4 | Marchfolk head; see §3 |

**Thin-separation context:** HV is within 1 % of VA on 22 / 36 readings, of MF on 21, of SG on 21. The accepted sources at this height are themselves close: VA is within 1 % of MF on 16 / 26 body readings (HV vs any single source: at most 14 / 26). See `sheets/hv_vs_sources_178.jpg` for the visual call.

## 2. Source-boundary protection (order item 6)

- **Matched height:** SG and VA at 178 cm; MF 173; FN 181; AE 190; SK 208. All shares are stature-normalized.
- **Matched composition:** HV low (0.25 / 0.25) is within 1 % of MF-M-R-LOW on 11 / 21 body readings and of SK-LOW on 2 / 21 (tables §6). No low-composition Sagekin or elven bodies exist yet.
- No body domain duplicates any source; resemblance to VA, MF and SG is strong but partial.

## 3. Hidden-ear craniofacial (order item 10) — NOT DEMONSTRATED (source method limit)

HV's head readings differ from MF on only 2 of 10. But the accepted Fenn, Vael and Sagekin heads differ from MF on only 3, 2 and 3 of 10 themselves. Only Aelari (9 of 10) carries measurably elven head geometry. So with ears hidden, the RAC head measurement cannot yet tell a mixed face from a human one, because the source elven heads are not separated either.

Under the source-first rule (HALVREN L510), I did not invent elven craniofacial biology inside Halvren. The elf-leaning panel body (§4) shows the system can carry mixed craniofacial expression using Aelari-sourced head targets: 6 of 10 head readings nearest an elven source.

## 4. Diagnostic expression panel (order item 14; tables §7, `sheets/hv_expression_panel.jpg`)

These are builder-chosen diagnostic points, not ancestry percentages or creator presets, and each is a domain mosaic, not a slider.

| Point | Construction on HV | Stature | Scored rows | Nearest (human / elven) |
|---|---|---|---|---|
| Human-leaning mixed (HVH3) | Marchfolk torso; human limb totals with Fenn-like forearm and lower-leg shares; light finger and wrist change; eye target removed | 178.1 | all pass except orbit MARGINAL | axial 5 / 2, appendicular 7 / 7, distal 5 / 0, head 7 / 3 |
| Balanced mixed | HV central | 177.7 | as above | axial 2 / 5, appendicular 7 / 7, distal 4 / 1, head 6 / 4 |
| Elf-leaning mixed (HVE3) | Aelari-like neck and vertical face (moderated), evenly elongated limbs, finer joints, longer hands and fingers, shallower thorax; Marchfolk thoracic breadth and pelvis retained; eye target removed | 179.3 | all pass except orbit FAIL (unstable reading) | axial 3 / 4, appendicular 10 / 4, distal 4 / 1, head 4 / 6 |

**Finding:** the elf-leaning body's limb readings still sit nearest Sagekin (8 of 14). Sagekin's linear proportions overlap the elves' on limb shares, as already noted in the Aelari gate. Elven expression there reads through thorax, joints, neck and head.

The first panel attempts overshot the source span (forearm share, neck, leg segments). They were tuned once and replaced; the record keeps the final values.

## 5. Frames and composition (order items 7, 12, 13)

| Body | Result |
|---|---|
| Narrow / Broad (breadth only; Broad pelvis ×1.12) | Breadth readings leave the span of the central sources (thoracic breadth, shoulder, crest, pelvic ratios). These are frame rows against unmatched Balanced sources, so they don't veto under the accepted convention |
| Continuity (hip ÷ thorax) | central 0.946 (MF 0.946, SG 0.947, VA 0.964); Narrow 0.958; Broad 0.962 |
| Composition bodies | Built and rendered (`sheets/hv_composition_4view.jpg`); composition carries no ancestry rows |

Frames are skeletal presets, not elf-leaning or human-leaning states. The Narrow HV is not more elven: its nearest-source counts barely move.

## 6. Residuals and method limits

| Item | Status |
|---|---|
| Orbit breadth reading | Unstable under eye-target probes; author call on HV vs HVC1 |
| Ankle ÷ stature | MARGINAL, 0.2 % below the source span |
| Hidden-ear craniofacial | NOT DEMONSTRATED: accepted elven heads (except Aelari) are not separated from MF in RAC head geometry |
| Ear | One W1i reference ear family; 3 of 9 parameters (length, base width, thickness) sit at the MF / elven-mean midpoint, so the ear is a partial midpoint (report) |
| Pelvis | Inside span and not a linear morph by the fraction test; detailed pelvic inheritance stays OPEN (sex-related anatomy dependency, HALVREN L508) |
| NOT RUN (W2) | ancestry-envelope generation, source-extreme stress, tails (HV-49/50), matched-composition elven/Sagekin bodies, population-level hidden-ear and anti-generic tests |

## 7. Canon statement

**No accepted canon was challenged.** No correction was made; HV is unchanged. No accepted source body was touched. No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 8. For the author

1. **Central:** accept HV as built (recommended), or HVC1 (eye-scale target removed).
2. **Orbit-breadth reading:** accept that it carries no verdict (unstable under eye-target probes).
3. **Hidden-ear craniofacial:** accept NOT DEMONSTRATED as a source method limit, carried to W2 / source head work.
4. **Frames:** breadth-only, Broad pelvis ×1.12, as for the other races.

Durrim is not started.

STOP.

— Claude

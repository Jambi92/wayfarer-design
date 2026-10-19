# RAC RP1E — custom-cavity checkpoint: quantified residual-contact report (interim)

**Date:** 2026-10-19
**Order:** `reviews/chatgpt-rac-rp1e-transcription-and-contact-scope-ruling.md` (3816926), §6 mandatory checkpoint.
**Status:** custom cavities authored, ownership colours regenerated, progressive gate run. **Class-A residuals remain**, so this is *not* the micro-contact stop and *not* the final gate. Work continues (hands/feet web floors next). No tolerance relief requested here; the B-class list below is for the later author ruling.

## 1. What is in the cage now

| Feature | Topology authored (cloud design → Blender UI import) |
|---|---|
| Ears | Pinna sub-cages (crescent rings, concha, canal pocket); helix crus loop cuts with crest/upper/lower blade points; vertices on the three tragus-front knobs |
| Jaw / chin–chest | Jaw rings 172 / 175.3 / 178 / 181 plus a loop at 176.6 (jaw-rim pleats removed) |
| Pouch / groin | Pelvis-front/crotch sub-cage with both groin creases (lip / tip / lip rows); explicit crease-top patches running the creases up to z 107 |
| Axilla slits | Junction band per side: 30 columns (crease-weighted), lips carried by arc length, slit-wall rings, tips re-detected every 0.5 cm incl. enclosed voids; trunk ring rebuilt to 30 columns |
| Tail root / natal cleft | Annulus sub-cage; cleft tip vertex |
| Muzzle | Mouth-line crease (upper lip / tip / lower lip, 3 columns), philtrum slot, elbow-tip vertex (L) |

**UI-verified cage:** `GO_U_REF_RP1E_retopo_v009.blend` (sha 98df25c2…8960) = design v009 (3013 V / 3113 F, 204 tris). Imported through File > Import > Wavefront. Index-identical to the design, max deviation 0.00025 mm, closed, manifold, genus 0, 1 component, consistent normals, 0 coarse self-x, min edge 1.9 mm. Provenance: `rac-rp1e-evidence/import_v009/`.
`v008.blend` holds a stale copy of the OBJ: the PC copy kept the pre-fix file, so 5 slit-wall vertices sit at their degenerate positions. It is superseded and kept unchanged; v005–v007 are untouched.
**Current design:** v010c (cloud, 3037 V / 3118 F, 166 tris; sha 4572a394…883e) = v009 + the rebuilt axilla trunk rings. It is pending UI import.

**Stack (simulated):** Subsurf ×4. Each level runs per-colour Shrinkwrap Nearest, then 2 × (Smooth + Nearest). The final level adds Project ± 2 cm on the head colour only, then a regional Smooth (factor 0.5, ×3) with vertex group `fsm_v3` (axilla slit bands and trunk rings, perineum slot rows, ear and axilla-top fold neighbourhoods). Targets: `tg_r2m5`.

## 2. Progressive gate (v010c)

| Level | Self-x | Axilla | Perineum | Head/ears | Hand L / R | Foot L / R |
|---|---|---|---|---|---|---|
| L1 | 6 | 2 | 4 | 0 | 0 / 0 | 0 / 0 |
| L2 | 67 | 55 | 4 | 1 | 0 / 0 | 0 / 7 |
| L3 | 349 | 251 | 22 | 1 | 8 / 9 | 0 / 58 |
| L4 | 992 | 553 | 6 | 25 | 10 / 105 | 5 / 288 |

L1 equals the v007 baseline: 6 pairs, all slit-wall contacts (R groin crease walls 4, L axilla front-slit walls 2). For comparison, the v007 UI cage gave 1563 pairs at L4.

**L4 deviation** (source → product, mm: median / p95 / max; % of the zone over its limit; v007 values in brackets):

| Zone | median / p95 / max (mm) | Over limit | v007 |
|---|---|---|---|
| T-1 general (limit 3) | 0.023 / 0.25 / 12.8 | 0.07 % | 0.022 / 0.26 / 20.3, 0.38 % |
| T-2 head/muzzle/ears (limit 1.5) | 0.026 / 0.33 / 7.7 | 0.49 % | 1.24 % |
| Hand L | 0.045 / 0.47 / 12.9 | 2.78 % | |
| Hand R | 0.048 / 0.36 / 13.9 | 1.29 % | |
| Foot L | 0.018 / 0.20 / 11.7 | 1.07 % | |
| Foot R | 0.021 / 0.21 / 13.5 | 0.93 % | |
| Tail root | 0.017 / 0.06 / 0.24 | 0 % | |

Cross-sheet projection: none from the cage. The amplitude column in §3 flags the clusters where the product bridges a gap.

## 3. L4 self-intersection clusters — classification

Column key:
- **gap** = source opposed-sheet gap near the cluster.
- **face** = final face edge.
- **amp** = largest distance of an intersecting face from the source.
- **open** = fraction of rays escaping 3 cm, so ≥ 0.5 means exposed.

| Pairs | Zone / where | dot | gap | face | amp | open | Class |
|---|---|---|---|---|---|---|---|
| 252 | R foot, toe web (−26.9, −48.1, 1.7) | −0.94 | 1.5 mm | 1.5 mm | 0.19 mm | 0.38 | **B candidate** (web floor contact, on-surface) |
| 192 | R axilla apex (−18.9, −33.0, 140.8) | −0.29 | 0.4 mm | 0.09 mm (crushed) | 0.63 mm | 0.12 | B candidate (slit floor), crushed faces → needs ruling |
| 139 | R axilla front slit (−19.9, −38.5, 146.2) | −1.00 | 1.5 mm | 0.08 mm | 0.02 mm | 0.12 | **B candidate** |
| 117 | L axilla front slit pinch (23.5, −41.4, 146.7) | −1.00 | 0.4 mm | 1.3 mm | 3.5 mm | 0.46 | **A**: the source slit is pinched shut with an enclosed void behind it; the product bridges the void |
| 98 | R hand, fused digits (−32.5, −40.7, 93.0) | −0.76 | 1.3 mm | 2.9 mm | 6.0 mm | 0.15 | B candidate per §6 example (fused-source digit bridge); amp large because the source digits interpenetrate |
| 64 | L axilla slit (24.0, −39.6, 143.7) | −1.00 | 0.3 mm | 0.1 mm | 0.87 mm | 0.12 | B candidate |
| 39 | R axilla slit (−20.0, −35.6, 141.6) | −1.00 | 0.7 mm | 0.2 mm | 0.07 mm | 0.12 | **B candidate** |
| 28 + 3 | R foot toe cleft (−33.8, −43.4, 2.2) | −0.07 | 4 mm | 0.8 mm | 12.7 mm | 0.08 | **A**: cleft floor bridged |
| 24 | Ears: knob / blade underside folds (3 clusters) | +0.6…0.9 | — | 0.8–2.7 mm | 0.3–0.7 mm | 0.27–0.42 | **A** (folds) |
| 4 + 3 + 2 + 1 | Hand L small folds | +0.1…0.6 | | | 0.5–1.5 mm (one 13.8 mm) | | **A** |
| 4 + 2 + 1 | Hand R small folds / contacts | | | | ≤ 0.5 mm | | A |
| 4 + 3 + 2 + 1 | Feet small folds | | | | 0.06–2 mm | | A |
| 4 + 2 + 2 | Perineum slot micro-folds at source micro-artifacts (a 0.15 mm closed spike in the roof) | +0.5…1.0 | 1.3 mm | 0.1 mm | ≤ 0.5 mm | 0.08 | A (fold), source-artifact caused — ruling wanted |
| 1 | Philtrum | +0.97 | 2.6 mm | 5.5 mm | 1.3 mm | 0.23 | A |

Totals:
- **B candidates:** 252 + 192 + 139 + 98 + 64 + 39 + 2 = **786 pairs**, all opposed-normal contacts inside source slits, webs or fused digits.
- **A:** about 206 pairs:
  - L axilla pinch 117;
  - R foot cleft 31;
  - ears 24;
  - hand/foot folds about 25;
  - perineum micro-folds 8;
  - philtrum 1.

Visibility and deformation:
- **Skinning risk:** the axilla and groin B contacts lie on the arm and hip hinge lines.
- **Toe web:** at the toe web the contact is between two toes of the same foot segment.
- **Visible:** none of the B clusters is externally visible (open ≤ 0.38).

## 4. Deviation residuals (T-1 / T-2 blockers), classified

| Cluster | Max | Gap | Open | Class |
|---|---|---|---|---|
| L axilla front slit, void behind pinch (23.9, −40.1, 146.1) | 8.5 mm | 1.0 mm | 0.69 | hidden void surface behind a 0-gap pinch: B-type (source contact); needs ruling |
| L axilla slit spike at z 153 (23.4, −41.1, 152.9) | 12.8 mm | 2.0 mm | 0.04 | A (narrow sub-pocket not reached) |
| R axilla tips (−19.7, −38.1, 146.3) / (−18.6, −31.2, 141.9) | 4.6 / 4.4 mm | 1.2–2.5 mm | ≤ 0.12 | A (slit tip not reached; gap > face size) |
| Groin crease end R (10.6, −54.3, 107.5) | 3.8 mm | 2.4 mm | 0.19 | A |
| Natal cleft top (2.1, −28.7, 104.9) | 5.0 mm | 3.6 mm | 0.08 | A |
| Philtrum slot (2.0, −62.5, 182.2) | 7.7 mm | 3.7 mm | 0.38 | A |
| Nostrils (−1.4, −57.0, 192.5) / (5.6, −56.8, 192.0) | 6.6 / 4.7 mm | 3–5.6 mm | ≤ 0.12 | A (nostril slits not in the cage) |
| Chin underside (5.8, −46.4, 175.3) | 3.3 mm | open | 0.23 | A |
| Hands: inter-digit clefts/webs (hand L 378 pts exposed, open 0.58, max 12.9; others 7–14 mm, gaps 2–9 mm) | 12.9 / 13.9 mm | 2–9 mm | 0–0.58 | **A** (visible bridged webs) |
| Feet: toe clefts (L 11.7 / 9.3 / 7.2; R 13.5 exposed, 5.2, 3.8) | ≤ 13.5 mm | 2.3–11.7 mm | 0–0.58 | **A** |

## 5. What remains before the §6 stop or the final gate

1. **Hands and feet — the largest remaining A block.** The digit tubes of the frozen hand/foot designs start above the cleft floors, so the product bridges every inter-digit cleft and toe cleft; some of these bridges are exposed.
   - Single-vertex insertions at the cleft floors were tried and do not resolve them (deviation −0.2 %, self-x +240), so they were not kept.
   - Each cleft needs an explicit web-floor crease (lip / floor / lip), as for the groin.
2. **L axilla.**
   - The z 153 sub-pocket is not reached.
   - At z 146–148 the slit is pinched shut with an enclosed void behind it.
     - The void surface can only be reached through a 0-gap contact.
     - I propose treating it as a source-contact (B) surface; author ruling needed.
3. Ear / perineum / philtrum micro-folds (≤ 0.7 mm amplitude, ~35 pairs).
4. Nostril slits, R axilla slit tips, natal-cleft top, groin crease end R.
5. UI import of the current design (v010c) and of each later design (same provenance contract).

## 6. Proposed B threshold (for the later author ruling, not applied)

A pair is B only if all of the following hold:
- opposed normals (dot < −0.5);
- source opposed-sheet gap ≤ 1.6 mm (≈ one L4 face);
- amplitude ≤ 1.0 mm;
- openness ≤ 0.4;
- inside a slit, web or fused-digit contact listed above.

On v010c this test passes 496 of 992 pairs: the R toe web, three R axilla slit clusters and the L axilla slit at z 143.7.

Two clusters fail it although they look source-consistent; these are the two that need an explicit ruling:
- the R axilla apex, 192 pairs: dot −0.29, crushed faces;
- the R hand fused digits, 98 pairs: amplitude 6 mm, because the source digits interpenetrate.

## 7. Evidence

- `rac-rp1e-evidence/gate_v010c/`: log, clusters (`cls_V10c.json`), deviation clusters (`dev_V10c_*.json`).
- `gate_v007/`: UI-cage baseline.
- `import_v007/`, `import_v009/`: provenance.
- `designs/`: v008p … v010c, rings, smoothing groups.
- Tools: `tools/rac/rp/rp1e/` (`axslit.py`, `t1rebuild.py`, `loopcut.py`, `pathbevel.py`, `xpatch.py`, `edgeins.py`, `classify.py`, `devclass.py`, `sim.py`).
- Progress log: `rac-rp1e-evidence/RP1E_progress.md`.

# RAC RP1E — non-local sub-cage rebuild: v012 checkpoint (order a2f5ee5)

**Date:** 2026-10-19
**Order:** `reviews/chatgpt-rac-rp1e-nonlocal-subcage-rebuild-order.md`
**Status:** **CHECKPOINT — order still in progress. No §11 stop line is returned yet.**

I stopped at this point for two reasons. Rebuilds R1–R5 are now in one promoted, UI-imported cage (v012). The session log had also grown too large to carry on safely (handoff rule). Several open Class-A items are still not cleared. Some have not yet had a genuine support-topology rebuild (§4 below), so none of the three §11 lines is honest yet:

- **OPEN CLASS-A CLEAR** — not true.
- **PASS** — not true.
- **BLOCKED** — not yet proven for most of the remaining items.

The next session continues from v012. No Class-B waiver was assumed. The contract was not relaxed. No RP2, rigging, creator or UE5 work was done.

## 1. Promotion / provenance (v012)

| Step | Result |
|---|---|
| Design frozen | `designs/design_v012.npz`: 5043 V / 5170 F (4912 quads, 258 tris), closed, 0 non-manifold, Euler 2 (genus 0), 1 component, 0 bad orientations, min edge 0.82 mm, **0 coarse self-x**. npz sha 94b3896d…55c2. Colour/ownership file `design_v012_col.npy` (finger colours 17–24, targets `tg_r3m5`), smoothing group `fsm_v012.txt`, info `design_v012_info.json` |
| OBJ | `RP1E_cage_v012_design.obj` sha 4d35546d…a841, committed to `…\Gorrund\RP1\` and re-staged from the PC: same sha |
| UI import | Opened v011.blend → File > Import > Wavefront → Apply Rotation → old cage deleted → renamed `Cylinder` → Save As **`GO_U_REF_RP1E_retopo_v012.blend`** (new file, sha 25e9b53c…7f9c). v011.blend is not overwritten. |
| Verify (`exp_v014/verify_import_v012.json`) | max deviation **0.00025 mm**; bijective, faces identical by index; 0 boundary; 0 non-manifold; Euler 2; 1 component; 0 bad orientations; 0 coarse self-x |

Blender was closed afterwards. The Explorer tab I opened to launch it was also closed.

## 2. What v012 contains (relative to v011)

| Order item | Rebuild | Method / topology | Effect (L4) |
|---|---|---|---|
| **R1** L toe cleft 3 (+ all L toes) | Everything distal to the clean attachment ring K'' was replaced (`toegen.py`) | attach → M → M1 → O outer base loop → 12-vertex toe rings; adjacent toes share a 5-vertex crotch path on the traced cleft floor; 2 wall support rings; 4-vertex tip caps | foot L self-x 316 → **0**; max 11.4 → 2.1 mm; over 0.85 → 0.03 % |
| R6 R toes | Same generator (frame rotated 36.9°) | as above | foot R self-x 431 → 13; max 5.5 → 2.0 mm; over 0.42 → 0.06 % |
| **R2** both hands (web 3/4 etc.) | Digit bases rebuilt from the palm attach ring (`diggen.py`) | Oblique cleft planes spanned by adjacent finger axes; per-digit frames; wall cap 0.45 cm; fused R tips kept fused (extension rings over the fused blob) | R web 3/4 pocket 13.1 mm → cleared; hand R max 13.1 → 8.4 (fused zone); hand L over 1.74 → 0.94 % |
| **R3** L thumb web | New slit band (`slitgen.py`, 6 columns × 5 rows: lip / wall / floor / wall / lip) over a 12-face patch | Floor traced in planes normal to the floor polyline | 6.84 mm cluster → **cleared**; hand L over 0.94 → 0.63 % |
| **R4** nostrils | 8-ring pocket tubes (2 snapped rim rings + 4 depth rings from source cavity loops, `pockgen.py`) | Ring sampling now orientation-checked by signed area (fixes a twisted-ring bug) | nostril L 6.6 → cleared; nostril R 5.8 → **cleared** |
| R4 philtrum | Slit band, 3 columns | — | 7.7 → 2.6 mm (residual at the slot bottom) |
| R4 mouth line | Full-width slit band, 8 columns along the W-shaped mouth floor (x 0.25 → 3.75), replacing the old 2-vertex mouth floor | — | mouth-corner pockets 2.7 / 2.95 mm → **cleared**; head over 0.38 → 0.13 % |
| **R5** L axilla z153 crevice | Pocket tube in the crevice (J/WA/WT column 14 replaced) | — | 12.7 → 2.0 mm; 18 small contacts |

**L1 survival.** The rebuilt nostril pocket, mouth corners and L thumb-web slit are all entered by the L1 limit surface (`gate_v012/muzzle_nostrils_mouth_L0_L1_L4.png`, `thumbwebs_L0_L1_L4.png`). The fixes do not depend on tip overshoot.

## 3. Progressive gate (v012 = sim G12; `gate_v012/`)

**Self-intersection pairs by level** (v011 in brackets):

| Level | Total | General | Axilla | Perineum | Head | Hand L / R | Foot L / R |
|---|---|---|---|---|---|---|---|
| L1 | 23 [14] | 6 | 2 | 4 | 1 | 11 / 5 | 0 / 0 |
| L2 | 121 [82] | 16 | 12 | 4 | 2 | 37 / 65 | 0 / 1 |
| L3 | 926 [513] | 162 | 137 | 25 | 4 | 216 / 521 | 0 / 23 |
| L4 | **1104** [1109] | 180 | 172 | 8 | 55 | 346 / 510 | **0** / 13 |

The axilla and perineum columns are subsets of general.

**Deviation, source → product (% of the zone over its max; L4 also shows median / p95 / max in mm):**

| Zone (limit) | L1 | L2 | L3 | **L4** | v011 L4 |
|---|---|---|---|---|---|
| T-1 general (3.0) | 12.8 % | 2.25 % | 0.22 % | 0.023 / 0.25 / 16.1, **0.07 %** | 0.09 % |
| T-2 head (1.5) | 26.8 % | 10.8 % | 2.45 % | 0.025 / 0.27 / 2.89, **0.13 %** | 0.48 % (max 7.7) |
| Hand L (1.5) | 19.1 % | 5.06 % | 1.04 % | 0.031 / 0.23 / 9.81, **0.63 %** | 1.74 % |
| Hand R (1.5) | 21.8 % | 5.33 % | 1.51 % | 0.036 / 0.24 / 8.38, **1.17 %** | 1.31 % (max 13.1) |
| Foot L (1.5) | 7.7 % | 3.11 % | 0.69 % | 0.015 / 0.12 / 2.14, **0.03 %** | 0.85 % (max 11.4) |
| Foot R (1.5) | 12.7 % | 3.93 % | 0.24 % | 0.020 / 0.15 / 2.00, **0.06 %** | 0.42 % |
| Tail root (1.5) | 12.5 % | 0.18 % | 0 % | max 0.24, 0 % | 0 % |

- **Product → source maxima:** general 2.5, head 3.4, hand L 2.1, hand R 12.5 mm (the R fused-junction sheet).
- **Cross-sheet ownership:** no cage-caused ownership errors. The finger colours 17–24 give each digit its own target.

T-1 and T-2 do not pass yet: there are still over-limit points in every zone except the tail.

### L4 self-x clusters (`gate_v012/G12.cls`, `cls_G12.json`)

| Pairs | Where | dot | gap | amp | open | Proposed class |
|---|---|---|---|---|---|---|
| 475 | R fused digit junction (−33.1, −38.9, 93.0) | −0.88 | — | 1.6 mm | 0.46 | Provisional B (fused source contact; separating it would change the anatomy) |
| 207 | L little/ring web (39.1, −46.4, 100.5) | −1.00 | 0.6 mm | 0.20 mm | 0.04 | Provisional B / deferred (sealed web tunnel, §3B) |
| 139 | R axilla apex (−18.9, −32.8, 140.8) | −0.43 | 0.4 mm | 0.71 mm | 0.62 | B candidate (crushed apex), unchanged from v011 |
| 123 | L index/middle web (38.6, −55.9, 101.7) | −0.97 | 3.5 mm | 0.13 mm | 0.38 | B candidate (web contact) |
| 25 | Mouth lip line, L of the corner (−0.8, −60.8, 179.7) | +0.39 | 2.6 mm | 0.31 mm | 0.23 | Zero-width lip-contact crease beyond the corner. New with the mouth band → **A until shown to be a source contact** |
| 18 / 15 | L axilla z153 pocket / pinch mouth | −0.40 / +0.76 | | 0.16 / 0.20 mm | | A (small folds) |
| 16 | L thumb-web slit end (33.4, −55.8, 106.2) | +0.21 | | 1.4 mm | 0.23 | A (new band fold) |
| 14 + 11 + 8 + 2 | R hand fused zone edges | | | ≤ 1.0 mm | | A / B, to resolve with the fused-zone ruling |
| 12 + 12 + 9 + 5 + 3 + 1 | R toe web, nostril-L top ridge, philtrum, ear, nose | | | ≤ 1.0 mm | | A (folds) |

Approximate totals: B candidates ≈ 944 (fused 475, finger webs 330, R axilla apex 139); A ≈ 160.

### Over-limit deviation clusters still open (L4)

| Cluster | Max | Class / status |
|---|---|---|
| L axilla void behind the pinch (23.8, −40.6, 146.6) | 16.1 | **Deferred** (§3B) |
| Hand L web tunnel (38.5, −50.9, 100.5) | 9.8 | **Deferred** (§3B) |
| Hand R fused zone (−33.6, −40.3, 94.4), (−33.9, −39.5, 92.1), (−33.9, −38.0, 94.1) | 8.4 / 6.7 / 6.3 | Fused-source region. B / deferred candidate. Needs a ruling: the cage follows the visible fused surface. |
| R thumb web (−32.4, −46.6, 104.4) | 4.9 | **A.** This is a thin positive fin (web membrane about 2 mm thick, 3 mm proud), not a slit. A fin band was tried (`slitgen.py` `fin` mode, `exp_v014/trial_fin_thumbR_notkept.json`). It was 0 coarse self-x and cleared the deviation, but the stitch into the 2–5 cm surrounding faces folded at L1: hand R self-x 506 → 6600. Not kept. The next attempt should refine the surrounding thumb-base faces first. |
| Natal-cleft nub (2.1, −28.7, 104.9) | 5.0 | A, or a source micro-artifact: its z-slice is a tiny non-closed loop (§3D). Not attempted this order. |
| R axilla tips (−18.6, −31.2, 141.9), (−19.7, −38.1, 146.3) | 4.4 / 3.3 | A. Not attempted this order. |
| L axilla (24.2, −39.0, 143.6), (23.3, −40.3, 149.6) | 4.4 / 3.6 | A, next to the deferred void |
| R groin crease end (10.6, −54.3, 107.5) | 3.8 | A (sharp convex ridge end). Not attempted. |
| Hand L (39.1, −46.4, 100.9), thumb tip (28.1, −57.1, 98.9), wrist (33.7, −50.0, 114.5), palm crease (32.1, −52.7, 104.9) | 3.5 / 2.75 / 2.5 / 2.5 | A (shape misses; the palm crease continues the thumb-web slit) |
| Head: ear (12.9, −48.3, 197.4), chin lobe (5.9, −46.4, 175.2), philtrum slot bottom (2.05, −62.1, 181.9), upper lip (0.7, −63.5, 184.2), ear rims (13.5, −50.5, 200.9), (12.8, −49.5, 198.7) | 2.9 / 2.7 / 2.6 / 2.05 / 1.9 / 1.9 | A (T-2). A local limit-surface fit (`fitcage.py`) did not move the chin or ear (max 2.72 → 2.72) and produced 1 coarse self-x, so it was rejected. These overhang lobes need extra support rings. |
| Feet: L toe 4 tip (34.0, −58.6, 2.7), R toe tips/webs | 2.1 / ≤ 2.0 | A (small) |

## 4. Remaining work in this order (next session, from v012)

1. **R3 (R thumb fin).** Refine the thumb-base faces around the fin into a ring (graded density) before inserting the fin band. Accept only if L1 has no folds.
2. **R4.**
   - Philtrum slot bottom: deepen or extend the band to the lower slot.
   - Upper lip and chin lobe: add support rings.
   - The lip-line contact crease left of the mouth corner (25 pairs): measure the source gap. If it is 0, it is a lip-contact B candidate; otherwise end the mouth band with a crease row.
   - Ear rims: add support rings.
3. **R5.** Fold the L pinch mouth and the z153 pocket contacts out; check the L axilla points (24.2, −39.0, 143.6) and (23.3, −40.3, 149.6) against the deferred void.
4. **R6.**
   - R axilla tips: slit-band columns.
   - R groin ridge end: a ridge support loop.
   - Natal nub: classify it with slice evidence (§3D).
   - Hand L shape misses; foot tips.
5. **Then** promote v013, UI import, run the full L1→L4 gate, and return a §11 line.

Tool notes for that work (all in `tools/rac/rp/rp1e/`):

- `slitgen.py` now also takes:
  - `facev` patches (selected with `patchsel.py`);
  - `fin` mode;
  - `stitch: 2d | 3dn`;
  - `apron` rings.
- The arc-fraction stitch (the default) is fragile around large patches. Sweeping cols/wallmax and checking 0 coarse self-x is what worked.
- `chain.py` replays generator steps given in base-cage ids. The exact muzzle chain from `exp_v014/design_pC_axilla.npz` is `exp_v014/chain_face.json`; then `sl_thumbL.json` gives v012.

## 5. Evidence

- `reviews/rac-rp1e-evidence/designs/design_v012.npz`, `_col.npy`, `_info.json`, `fsm_v012.txt`, `remap_v011_to_v012.npy`
- `reviews/rac-rp1e-evidence/exp_v014/`:
  - import verification;
  - chain specs;
  - pre-muzzle design `design_pC_axilla.npz`;
  - sim logs N3 (nostril R), M1 (mouth), T1 (L thumb web), T2 / T3 (the R thumb fin trial, not kept).
- `reviews/rac-rp1e-evidence/exp_v013/`: feet rebuild.
- `reviews/rac-rp1e-evidence/gate_v012/`:
  - G12 L1–L4 log;
  - classification;
  - per-level deviation;
  - openness (`devopen_G12.npz`, `devopen.log`);
  - L0/L1/L4 slices.
- Scratch bundle `reviews/rac-rp1e-evidence/scratch/rp1e_s7.tgz`: all cloud scripts, the current cage, the r3 targets and colours.

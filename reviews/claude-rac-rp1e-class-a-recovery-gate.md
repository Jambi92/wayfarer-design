# RAC RP1E — Class-A recovery gate (order 4e2b1a9)

**Date:** 2026-10-19  
**Order:** `reviews/chatgpt-rac-rp1e-class-a-residual-recovery-order.md`  
**Result line:** **RP1E CLASS-A RECOVERY BLOCKED / AUTHOR DECISION REQUIRED**

The block has two parts, and the decision needed is set out in §6:

- **Source anatomy.** Some of the remaining Class-A deviation lies on sealed or near-sealed micro-cavities in the frozen source. Examples are the hand-web tunnels, the L axilla void and the 1 mm nostril slits. The product can only reproduce these by leaving contacts in faces smaller than the slit (Class-B type), or after the cavity is filled in the source.
- **Method.** The other remaining items are open pockets: the R hand web 3/4, L toe cleft 3, the philtrum slot, the L axilla z 153 crevice, the natal-cleft nub and the R groin ridge end. The bounded local repairs tried in this order did not reach them without new self-intersections. The cause is systematic, not a design slip (§4). These pockets need a non-local rebuild of the hand, foot and muzzle sub-cages, which goes beyond the "bounded local repair" this order allows.

No Class-B waiver was assumed. The final contract was not relaxed. No RP2, rigging, creator or UE5 work was done.

## 1. Import / provenance

| Step | Result |
|---|---|
| v010c → `GO_U_REF_RP1E_retopo_v010.blend` (first action) | sha 2e015133…36af; index-identical (0.00025 mm), closed, manifold, Euler 2, 1 component, normals consistent, 0 coarse self-x. v009 unchanged. |
| **design v011** frozen | `designs/design_v011.npz`: 3475 V / 3605 F (3341 quads, 264 tris); npz sha 9cc5e6f3…0d5; colour/ownership file `design_v011_col.npy` sha 4414b5bc…c0a3 |
| OBJ | `RP1E_cage_v011_design.obj` sha 1d3d378e…982e (re-staged from the PC: same sha) |
| UI import | File > Import > Wavefront → Apply Rotation → old cage deleted → renamed `Cylinder` → **`GO_U_REF_RP1E_retopo_v011.blend`** sha 5792e5d9…1857 |
| Verify (`import_v011/verify_v011.json`) | max deviation 0.00025 mm (index-matched); faces identical by index; 0 boundary; 0 non-manifold; Euler 2 (genus 0); 1 component; 0 bad orientations; **0 coarse self-x** |

- v009 and v010 are unchanged (v010 re-staged: same sha).
- `GO_U_REF_RP1E_retopo_v011.blend` is now the authoritative PC cage.

## 2. What v011 changes (relative to v010c)

1. **Feet (A2), toe tubes** (v011g, carried forward). Each toe tube gained a longitudinal loop (8-vertex tubes). The mandatory R foot cleft cluster at (−33.8, −43.4, 2.2) is gone: foot R deviation max went from 13.5 to 5.5 mm.
2. **L foot clefts 1–2 (A2).** I added an explicit lip / floor / lip crease at the crotch edges 1557–1550 and 1558–1563 (`midcleft.py`). The tips sit on the source cleft floor.
3. **Hands (A1) and head (A4).** I fitted the cage locally to the source (`fitcage.py`: least squares on the level-3 limit surface against the colour targets, with a Laplacian term).
   - It covers the dorsal knuckle and thumb-tip misses on hand L, the R hand tip, the chin and the ear rims.
   - The crotch vertices were held fixed.
   - This mainly fixes exposed misses caused by stretched L4 faces over the knuckles (for example a 1.2 cm L4 face on the L dorsal knuckle).
4. **L axilla pinch (A3).**
   - In front-crease columns 8–9 the arm wall ran past the trunk wall (crossed order) inside the zero-gap pinch. I moved the tip back to the pinch mouth and put the walls on their own sides at the mouth.
   - The enclosed zero-gap void behind the pinch is left as it is, for the later author ruling, as §4/A3 of the order allows.
5. **Crease-tip ownership, both axillae.**
   - The front-crease tip ring J now belongs to the trunk colour (1) instead of the arm colour (4 / 5). The trunk target covers both pocket walls; the arm target does not.
   - Before, the tip had mixed weights at L1, which pulled both sheets out of the slit.
   - This is a vertex-group (ownership) change only. It is recorded in `design_v011_col.npy`.

## 3. Progressive gate (v011 = sim V12c; `gate_v011/`)

**Self-intersection pairs by level** (v010c in brackets):

| Level | Total | General | Axilla | Perineum | Head | Hand L / R | Foot L / R |
|---|---|---|---|---|---|---|---|
| L1 | 14 [6] | 4 | 0 | 4 | 0 | 0 / 0 | 7 / 3 |
| L2 | 82 [67] | 8 | 4 | 4 | 1 | 2 / 8 | 32 / 31 |
| L3 | 513 [349] | 148 | 126 | 22 | 0 | 8 / 81 | 143 / 133 |
| L4 | **1109** [992] | 168 | 162 [553] | 6 | 19 [25] | 58 / 117 | 316 / 431 |

The axilla and perineum columns are subsets of general. At L4 the axilla zone fell from 553 to 162 pairs. The increase is in the feet: the toe-web contacts.

**Deviation, source → product (mm: median / p95 / max; % of the zone over its max):**

| Zone (limit) | L1 | L2 | L3 | **L4** | v010c L4 |
|---|---|---|---|---|---|
| T-1 general (3.0) | 12.8 % | 2.27 % | 0.23 % | 0.023 / 0.25 / 16.1, **0.09 %** | 0.07 % (max 12.8) |
| T-2 head (1.5) | 28.3 % | 12.2 % | 3.80 % | 0.026 / 0.33 / 7.7, **0.48 %** | 0.49 % |
| Hand L (1.5) | 27.9 % | 8.9 % | 3.68 % | 0.039 / 0.37 / 10.3, **1.74 %** | 2.78 % |
| Hand R (1.5) | 30.5 % | 7.5 % | 2.04 % | 0.043 / 0.28 / 13.1, **1.31 %** | 1.29 % |
| Foot L (1.5) | 13.4 % | 4.5 % | 1.71 % | 0.016 / 0.14 / 11.4, **0.85 %** | 1.07 % |
| Foot R (1.5) | 19.1 % | 5.5 % | 0.86 % | 0.020 / 0.16 / 5.5, **0.42 %** | 0.93 % (max 13.5) |
| Tail root (1.5) | 12.5 % | 0.18 % | 0 % | max 0.24, 0 % | 0 % |

- The general max rose from 12.8 to 16.1 mm. This is the hidden void behind the L axilla pinch, now left uncovered on purpose (openness 0.07).
- Cross-sheet ownership errors: none from the cage. The J-ring ownership change removed the mixed-weight pull-out at the axilla tips.

## 4. Why the remaining pockets resist local repair (diagnosis)

All products are made by the same stack, repeated at each level: Subdivision (limit surface on), then Shrinkwrap Project ±n, then Shrinkwrap Nearest.

- **At L1 the product sits on the cage's limit surface.** For a crease or pocket tip the limit point is (n²P + 4ΣE + ΣF)/(n(n+5)). That is about 44 % tip and 56 % neighbours.
- **The tip therefore retracts by about half the cage-edge depth** before the first snap. A Nearest snap then lands on the closest wall or the mouth, not the roof, and later levels cannot recover the pocket. Slices `Laxilla_z153_crevice_L0_L4.png` and `handL_web_pocket_L0_L4.png` show this: the L0 tip is inside the pocket, and L1 is already at the mouth.

Repairs tried in this order (`exp_v012/`):

| Trial | Change | Outcome |
|---|---|---|
| V11j | Hand crotch splits + floor lift | Hand R max 13.1 → 11.6; hand R self-x 117 → 591 |
| V11o | Crotch overshoot +0.8 cm | Deviation −0.1 %; self-x up; 2 coarse self-x |
| V11n | Axilla tip overshoot + deeper walls | z 153 crevice 12.8 → 10.8 only (the crevice is oriented in z; the crease columns are in the xy plane) |
| `limitsolve.py` | Exact L1-limit placement | Needs 1.6–4.2 cm cage moves → coarse self-x |
| V11k | Nostril creases | Nostril max 6.6 → 4.2 mm, but head self-x 25 → 2914 |
| V11l | Nostril pockets | Head self-x 8961: the slit is about 1 mm wide, smaller than the L4 face (2.5 mm) |
| V12b | Third L toe cleft crease | Foot L max 11.4 → 6.5, but foot L self-x 316 → 944 (bridging, amp 4 mm) |
| V12d | Limit surface off | Hands −0.2 %, total self-x 1109 → 2060 |

None of these was kept.

## 5. Remaining L4 classification (v011)

### Self-intersection clusters

| Pairs | Where | dot | gap | face | amp | open | Class |
|---|---|---|---|---|---|---|---|
| 427 | R toe web (−26.7, −48.4, 1.5) | −1.00 | 1.5 mm | 0.6 mm | 2.6 mm | 0.35 | B candidate (web floor contact). It grew from 252 with the v011g toe loops that removed the mandatory A cluster. |
| 144 + 72 | L toe webs 1–2 (28.7, −57.1, 2.7 / 5.1) | −1.00 | 0.3 / 2.1 mm | 1.3 / 0.7 mm | 0.12 / 0.05 mm | 0.04–0.08 | B candidate (new, from the A2 creases, sub-0.1 mm contacts) |
| 139 | R axilla apex (−18.9, −32.8, 140.8) | −0.43 | 0.4 mm | 0.09 mm | 0.7 mm | 0.62 | B candidate (crushed apex). The R front-slit contacts (139 + 39) are gone. |
| 97 | L toe cleft 3 (31.5, −55.4, 6.4) | −1.00 | 4.4 mm | 0.5 mm | 4.0 mm | 0.38 | **A** (cleft bridged) |
| 70 / 58 | Hand R / L web contacts | −1.00 | 0.9 / 0.6 mm | 0.4 / 0.15 mm | 0.04 / 1.6 mm | 0.12–0.15 | B candidate |
| 43 | R fused digits (−32.3, −40.7, 93.0) | −1.00 | 1.3 mm | 2.0 mm | 6.3 mm | 0.12 | B candidate (fused source) |
| 16 | L axilla pinch mouth (23.4, −41.8, 146.3) | +0.75 | 0.4 mm | 0.2 mm | 0.2 mm | 0.46 | A (small fold). It was 117 pairs with 3.5 mm amplitude. |
| 11 + 7 | Ear folds | +0.6 / +0.9 | | | 0.3 mm | 0.27–0.35 | A (folds) |
| 7 | L axilla z 153.6 | +0.98 | 3.2 mm | 0.04 mm | 0.09 mm | 0.12 | A (micro-fold) |
| 4 + 4 + 2 + 2 + 2 + 1 | Perineum, R foot, hand R, general, philtrum folds | | | | ≤ 1.8 mm | | A (small folds) |

Totals:

- **B candidates:** about 953 pairs (v010c: 786). They are now concentrated in toe webs and finger webs. The axilla B candidates fell from 434 to 139.
- **A:** about 156 pairs (v010c: about 206). The largest are toe cleft 3 (97) and the L pinch mouth (16).

### Deviation clusters over the limit

Ranked, with ray openness (`gate_v011/deviation_clusters_openness.txt`):

| Cluster | Max | Openness | Nature | Class / path |
|---|---|---|---|---|
| L toe cleft 3 (31.3, −54.8, 3.6) | 11.4 | 0.11 | Open cleft, 0.5–0.8 cm wide, 1 cm deeper than the crotch | A, rebuild of the toe 3/4 sub-cage |
| L axilla void behind pinch (23.8, −40.6, 146.6) | 16.1 | 0.07 | Enclosed, zero-gap neck | Source micro-cavity → author decision (order §4 A3) |
| Hand L web tunnels (38.5, −51.0, 100.4), (38.8, −46.4, 100.6) | 10.3 / 10.3 | 0.04 / 0.14 | Sealed tunnels under the dorsal web skin (closed loops in source slices, `handL_web_tunnels_src_slices.png`) | Source micro-cavity → author decision |
| Hand R web 3/4 pocket (−37.4, −46.6, 101.3) | 13.1 | 0.15 | Open pocket, 1 cm wide × 1.5 cm high, above the crotch | A, rebuild of the hand R web sub-cage |
| L axilla z 153 crevice (23.4, −41.1, 152.9) | 12.7 | 0.08 | Wedge crevice oriented in z: 0.7 cm mouth, 1.3 cm deep | A, needs local columns at 0.3 cm spacing |
| Hand L thumb web (33.5, −54.9, 105.4), (37.3, −54.8, 101.5) | 7.3 / 8.5 | 0.40 / 0.26 | Thumb-web cleft | A |
| Philtrum slot (2.1, −62.4, 182.1) | 7.7 | 0.28 | Notch 0.5 cm wide, 1.2 cm tall | A, rebuild of the muzzle slot |
| Nostrils (−1.4, −56.7, 192.1), (5.5, −56.8, 192.0) | 6.6 / 5.8 | 0.18 / 0.21 | Slits about 1 mm wide, 1 cm deep | Gap below the L4 face → author decision |
| R toe clefts (−32.1, −44.8, 5.4), (−28.8, −47.0, 5.4), (−26.6, −48.1, 1.9) | 5.5 / 4.6 / 4.9 | 0.10–0.40 | Narrow clefts | A |
| Hand R (−37.7, −37.9, 100.6), (−32.4, −46.7, 104.4) | 6.0 / 6.6 | 0.23 / 0.42 | Web / thumb web | A |
| Natal-cleft nub (2.1, −28.7, 104.9) | 5.0 | 0.22 | 4 mm free-standing source nub (closed slice loop) | A, or source micro-feature → author decision |
| R axilla tips (−18.6, −31.2, 141.9), (−19.7, −38.1, 146.3) | 4.4 / 3.3 | 0.13 / 0.23 | Slit tips | A |
| R groin crease end (10.6, −54.3, 107.5) | 3.8 | 0.39 | Sharp ridge end | A |
| Exposed residuals: L toe (34.0, −58.5, 2.8), chin (6.0, −46.3, 175.1), ear rims, toe tips | 2.2–3.1 | 0.6–1.0 | Shape misses on open surface | A, small, refit candidates |

## 6. Author decision required

1. **Source micro-cavities.** Decide whether the following are kept as identity geometry or filled or sealed in the source:
   - the sealed hand-web tunnels;
   - the L axilla zero-gap void behind the pinch;
   - the 1 mm nostril slits;
   - the natal-cleft nub.

   If they are kept, the product can only reproduce them with contacts inside slits narrower than the face. That means a Class-B ruling.
2. **Sub-cage rebuild.** The open pockets (R hand web 3/4, L toe cleft 3, thumb webs, philtrum slot, L axilla z 153 crevice, R axilla tips, R toe clefts) need pocket-ring topology with explicit overshoot. Rebuilding the hand, foot and muzzle sub-cages is not a bounded local repair. Please authorise it, or authorise a limited modifier-stack change instead. Note: switching the limit surface off was measured and is not recommended, because self-x doubles.
3. **Class-B list (still provisional).** About 953 pairs:
   - toe-web floor contacts R (427) and L (216, new from the A2 creases, amplitude ≤ 0.12 mm);
   - R axilla apex (139);
   - finger-web contacts (128);
   - R fused digits (43).

## 7. Evidence

- `reviews/rac-rp1e-evidence/import_v011/`: OBJ, design info, UI-imported cage `v011ui.npz`, `verify_v011.json`.
- `reviews/rac-rp1e-evidence/designs/design_v011.npz`, `_col.npy`, `_info.json`, `fsm_v011.txt`.
- `reviews/rac-rp1e-evidence/gate_v011/`:
  - L1–L4 self-x log;
  - classification (`V12c.cls`, `cls_V12c.json`);
  - per-level deviation (`deviation_L1_L3.txt`);
  - openness of over-limit points (`devopen_V12c.npz`, cluster list);
  - diagnostic slices.
- `reviews/rac-rp1e-evidence/exp_v012/`: logs of the trials that were not kept.
- Tools in `tools/rac/rp/rp1e/`: `fitcage.py`, `ccmat.py` (Catmull-Clark and limit matrices, checked against Blender to 6e-5 cm), `slitfit.py`, `limitsolve.py`, `devopen.py`, `writeobj.py`, `build_c3.sh` (the exact v011 build), and others.

# RP4 Durrim — compact branch v002: design notes and in-progress plan (handoff)

**Order in progress:** `reviews/chatgpt-rac-rp4-durrim-compact-branch-revision-closure-order.md` (8080f9f; reviewed 372fe20).
**Status:** design analysis only. No v002 geometry is built yet. Nothing in this file is a gate result.
**Previous gate:** `reviews/claude-rac-rp4-durrim-compact-branch-gate.md` (NEEDS REVISION) and evidence in `reviews/rac-rp4-evidence/durrim/`.

## 0. Rebuilding the workspace in a new session

The `/tmp/claude-0/rt/du` workspace lives in the session container. In a new session, rebuild it with the committed scripts in `tools/rac/rp/durrim_rp4_v001/`. Use `/home/claude/stc/bin/python3` (bpy) for every Blender-side step.

1. `run_a.sh`
   - Regenerates DU122C / DU152C with `du_regen.py`, and DU137C the same way.
   - Builds `nat/DUF137C / MF152 / MFF152` with `native_short.py`, using the cfg JSONs in `reviews/rac-rp4-evidence/durrim/partA/`.
   - **The cfgs must be written first** (`partA/DUF137C.cfg.json`; MF137 / MFF137 / MF152 / MFF152 cfgs = the MF-M-R / MF-F-R cfg with stature changed and targets = {}, plus `base_height_macro` 0.60595703125 for configuration 2).
2. `run_parta.sh`, then `du_partA.py WORK OUT.json`.
3. `run_b.sh`: the unbranched v005 pipeline.
   - **Needs** `/mnt/user-data/outputs/rp5/MF_M_REF_RP3_retopo_v005.blend` and `_hm08_map.npz`. These are on E:, `RaceBodies/production/Marchfolk/RP3/` (`MF_M_REF_RP3_retopo_v005.blend`, `MF_M_REF_RP3_retopo_v005_hm08_map.npz`).
   - **Needs** `/tmp/claude-0/rt/v5/cand/MF-{M,F}-R_v005.npz` and `/tmp/claude-0/rt/v5/audit/MF-{M,F}-R_v005_loops.npz` for `contact_prop.py`. These are the MF-M-R / MF-F-R v005 family realizations plus their audit loops, and can be rebuilt with the same `run_b.sh` `one()` steps on the MF-M-R / MF-F-R records.
   - **Needs** the eye reference `/tmp/claude-0/rt/hv/partA/ref/MF-M-R_rest.npz` for `run_candidate.py`: build_variant MF-M-R with `{}`.

## 1. Thumb MCP v002: binding constraints (measured on the v005 realizations)

**Validator (val2lib / core3lib):**
- `thumb_mcp_*` has no defined band sides, so it uses the D1 closed-ring fallback.
- A ring counts if all of these hold:
  - it is a closed edge loop of valence-4 vertices;
  - it encircles the thumb_02 axis;
  - its max radius is ≤ 3.0 s;
  - |mean axial offset| ≤ 0.8 s from the thumb_02 head;
  - s = stature / 173.143.
- Crease poles (D3) are poles with |axial| ≤ 0.5 h (h = median local edge) within the probe radius.

**v005 thumb rings.** The rings are 20-vertex closed loops, ordered along the axis from the seed ring (the one nearest t = 0):

| Ring | Z | A | B | C | D |
|---|---|---|---|---|---|
| t (cm) at 137 cm | −0.011 | 0.217 | 0.450 | 0.688 | 0.931 |
| r_max at 137 cm | 2.79 | 2.50 | 2.21 | 1.91 | 1.73 |
| t (cm) at 122 cm | −0.01 | 0.196 | 0.406 | 0.622 | 0.842 |
| r_max at 122 cm | 2.52 | 2.26 | 1.99 | 1.73 | 1.56 |

Limits:

| Body | radius limit | window |
|---|---|---|
| 122 cm | 2.11 | 0.56 |
| 137 cm | 2.37 | 0.63 |
| 152 cm | 2.63 | 0.70 |

- Only rings with t of about 0.32 s/0.705 … window and r_max ≤ limit can count, so **B plus two new rings inside the B→C strip are the only feasible counted set at 122 cm**.
- At 122 cm, B→C rings at u = 0.3 and 0.6 give t = 0.471 and 0.536.
- **Rings B, T1 and T2 must stay pole-free closed valence-4 loops.**
- **Segment lengths at 137 cm:** ring segments come in equal pairs (v005 is a 2× subdivision of hm08). There is one run of 4 long segments (0.64–0.83 cm on rings Z–B; about 0.55–0.64 on C / D); the others are 0.33–0.50 cm. Axial spacing is about 0.23 cm. The parent strip aspect is up to 3.6.
- **Aspect:** any axial refinement to about 0.07–0.09 cm without circumferential splitting gives aspect 4–9. That is the v001 failure.

**Feasible layout (to implement):**

| Region | Content |
|---|---|
| A→B (S1) | proximal transition sub-strip A → R (R at u ≈ 0.5–0.6 of S1, an uncounted ring that carries the transition 3-poles), then a fine sub-strip R → B |
| B→C (S2) | fine: circumferential ×2 on normal segments and ×3 on the long run, plus rings T1 (u 0.3) and T2 (u 0.6) |
| C→D (S3) | distal transition (fine C → coarse D); 3-poles on C (C is uncounted: outside the window), 5-poles on D |

**Transition templates** (all quads; new vertices are bilinear points in the parent quads, so they lie on the parent surface and map rows have 4 non-zeros):

- **×2 pair** (coarse A_k, A_{k+1}, A_{k+2}; fine r_k, rm_k, r_{k+1}, rm_{k+1}, r_{k+2}):
  - quads `[A_k, r_k, rm_k, A_{k+1}]`, `[rm_k, r_{k+1}, rm_{k+1}, A_{k+1}]`, `[rm_{k+1}, r_{k+2}, A_{k+2}, A_{k+1}]`;
  - A_{k+1} becomes a 5-pole and r_{k+1} a 3-pole. Push r_{k+1} toward the fine side (larger u) so the middle quad is a convex diamond rather than a 180° angle.
- **×3 single** (coarse A_k, A_{k+1}; fine r_k, m1, m2, r_{k+1}; interior p):
  - quads `[A_k, r_k, m1, p]`, `[p, m1, m2, r_{k+1}]`, `[A_k, p, r_{k+1}, A_{k+1}]`;
  - p and m2 become 3-poles, A_k and r_{k+1} 5-poles. Place p near the Fermat point of (A_k, m1, r_{k+1}) and push m2 toward the fine side.
- **Placement:** optimize the template parameters (uR, pushes, p, T1 / T2) once, as global constants, for min angle ≥ 45° and aspect ≤ 4 over DU122 / DU137 / DU152 / DUF137. Then verify validator counts (B, T1, T2 counted; no crease poles: the poles sit at t ≥ 0.2 s, outside the MCP band).
- **Expected count:** 3 rings, margin 0 at every body (the order accepts ≥ 0). Few or no aspect > 4 quads; the widest coarse segments in the proximal transition are the risk.

## 2. Jaw–neck pole reroute: key topological fact

- **The pole:** 5299 / 11904 is an **isolated** valence-5 pole. No other pole lies within 5 rings, and its 5 neighbours are valence 4. Position at 137 cm: x ±4.30, y 10.39, z 120.86. The neck station centre z is 120.93; offset / h = −0.20.
- **Required move:** about 2 edge rows **up** (+z, toward the jaw). This clears the band with margin on every body: 137 → about +1.8, 152 → about +2.1, 122 → about +1.5, c2 → about +4.9, MF152 → about +4. **Moving it down would push MF152 and c2 into the band.**
- **Why it is not a simple move:** a disk around an isolated 5-pole in an otherwise regular neighbourhood has a unique quad layout (5-sector grid: the separatrix lengths are forced equal by the fixed boundary). The pole cannot be moved by re-quadding a disk with the same boundary.
- **Local options, all keeping net index −1 inside the disk:**
  - (i) Move the 5-pole up and add a compensating 3-5 pair. All three poles must sit outside the neck crease band and away from the jaw-hinge / mouth rings, which costs extra poles.
  - (ii) Re-route along a full quad strip (strip insert + collapse). This is non-local and **not authorized**.
- **Plan:** implement (i) as a disk re-quad. Mark it clearly in the record as "pole moved + one 3/5 pair added".
  - Verify T-1 / T-2: new vertices are on the parent surface, so the deviation should be near 0.
  - Check that neck flex / rot deformation shows no new flips, folds or self-intersections, and that face rings are unchanged.
  - If (i) cannot keep all poles out of the band or hurts the jaw silhouette, return **DURRIM RP4 REQUIRES AUTHOR DECISION** with this topological fact.

## 3. After the branch passes

Re-run the full RP4 gate:
- production candidates `DU_M_REF_RP4_v001` / `DU_F_REF_RP4_v001` (fn_make_prod-style writer);
- T-1…T-7, 69 / 69 on c1 / c2 / 122 / 152;
- density (v005 vs v001 vs v002);
- the full deformation suite;
- the 152 cm production board, hidden-presentation adult-read boards and the blind review;
- reusability, immutable hashes, and a freeze candidate record if everything passes.

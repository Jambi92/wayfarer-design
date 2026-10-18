# RAC RP1 — Gorrund production-mesh pilot (HOLD)

**Status:** PREPARED BY CLAUDE in RP0 (`reviews/claude-rac-rp0-source-inventory-contract.md`). **HOLD**: not to be run until Tyler / ChatGPT release it.

**Release conditions** (all three must be recorded in the release):
1. Accept or amend the PROPOSED PRODUCTION TOLERANCES T-1, T-2 (including the Gorrund micro-detail list in §6), T-3, T-6 and T-7 in `specs/RAC_PRODUCTION_MESH_CONTRACT.md` §16.
2. Choose the retopology method (§5: M-A or M-B).
3. Accept the contract draft as the governing production standard for RP1.

**Governing documents:**
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`
- `reviews/chatgpt-rac-retopology-rigprep-master-plan.md` §4 RP1

## 1. Source (immutable)

| Item | Value |
|---|---|
| File | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/source/Gorrund-Neutral-C/05AW4/GO-05AW4_nails_final.blend` |
| SHA-256 | `5a4e45d40158e7dc92f6f8ba13d67ada2403e3e3dcda9048382323ee43a22d5e` |
| GLB | `GO-05AW4_nails_final.glb` `e6b325039993b48de1daf1b82da7054c9f466131daf41c2dcc14a0709adb6fc8` |
| Provenance | 05AX4 closure (977f671); Stage C ACCEPT, reference state only (e864a9f) |
| Object | 1 mesh `GO-05AB1_macro_corrected_clean`: 598,717 vertices, 1,124,538 triangles, metres, identity transform |
| Material, UVs, rig | 1 material slot (`model`); **no UVs**; no armature |
| Vertex groups | 27 vertex groups: 13 segment labels (trunk / upperarm / forearm / hand / thigh / shin / foot, L / R) plus AV / AW edit groups |
| Raw file state | 5,979 position-split pieces: UV-seam duplicates, 65,472 boundary edges, 59,899 coincident vertices |
| Position-welded state (RP0) | 562,265 vertices, 1 component, 0 boundary, 0 non-manifold, genus 3, outward normals |
| Stature / bbox | 204.5225 cm; bbox 84.67 × 134.20 × 204.52 cm |

**Hash rules:** verify the hash at entry and stop on a mismatch. Re-hash at exit. The source is never written.

## 2. Known topology debt (repair targets, carried from 05AX4 §6 / 05AU)

| # | Debt | RP1 handling |
|---|---|---|
| D-1 | Left-hand finger / thumb contact loop (genus handle) | The production mesh separates the contact with a **minimal** gap. Contact-site movement only, within T-2 max; recorded per vertex |
| D-2 | Right-hand finger contact loop | Same |
| D-3 | Left-axilla micro-tunnel (genus handle) | Closed in production topology (no tunnel). The axillary fold follows the source surface within T-2 |
| D-4 | Perineal / duplicate-position seam handling | The production mesh has no position seams (contract §6). Seam duplicates are welded only in a **derived working copy** (`GO_U_REF_RP1_weldsrc_v001`, hash recorded), never in the source |
| D-5 | Tail-root slivers; nail-support local-subdivision density step | Replaced by regular production topology with §7 tail-root rings and even toe / nail density |

**Target genus after RP1: 0.** All three handles are debt, not anatomy.

## 3. Immutable anatomy (must be reproduced, never redesigned)

1. **Head / leonine muzzle / ears.** Identity zone (T-2). The head share and muzzle form are accepted (05AU / 05AT).
2. **Tail.** Root position and axis (emergence about 52.96 % H, +1.4 cm / 9° off-midline, accepted 05AU) and the full tail length and taper (T-2 at the root, T-1 along the tail).
3. **Feet / heels / toes / nails.**
   - Foot length as frozen: 05AV 34.80 cm per side, plus AW4 nail projection +1.43 mm (L) / +2.43 mm (R). Re-measured on the source at RP1 entry, then held to ±T-3.
   - Plantigrade heel-to-toe contact.
   - Lesser-nail projection 1.55–1.58 mm and big toes 1.69–1.74 mm. **Race metric tolerance proposed: ±0.15 mm**; flag at release.
   - Feline taper and curl; no crack / inlay read.
4. **Hands.** Five digits, proportions, nail plates. T-2, except the D-1 / D-2 contact sites.
5. **Body composition** (05AT AC3 accepted; untrained soft tissue). Silhouette T-7.
6. **Stature 204.5225 cm** (native, Stage C D2(c)). No scaling.
7. **Asymmetry.** The source is not mirror-symmetric (mirror RMS 4.0 cm, mostly the tail). Shape asymmetry is preserved; topology may be symmetric.

## 4. Allowed operations

- Building a **new** quad production mesh fitted to the welded working copy (retopology).
- Projection / shrinkwrap of the new mesh onto the working copy.
- Local contact separation for D-1 / D-2 / D-3 only.
- UV **seam plan** (seam edge set) on the production mesh. Unwrap optional, non-final.
- Landmark fitting on the source and on the production mesh.

**Forbidden:**
- editing the source;
- any proportional, compositional or identity change;
- smoothing passes that move the surface outside the tolerances;
- reposing;
- scaling;
- rigging or skin weights;
- final UVs or materials;
- LODs;
- creator morphs;
- touching any other race.

**Authoring rule (Tyler's standing rule).** Final production-mesh construction is done **in the Blender UI on Tyler's PC**. Cloud scripts are used only for:
- the welded working copy;
- masks, groups and landmark fitting;
- deviation / topology / landmark measurement;
- gates, evidence and sheets.

Close every Blender instance when done.

## 5. Method (choose at release)

**M-A — guided automatic quad remesh plus manual loop work** (recommended for the pilot).
1. Blender UI QuadriFlow remesh of a decimated proxy at the §8 density, with symmetry off (shape asymmetry).
2. Shrinkwrap (project) onto the working copy.
3. Manual loop insertion and redirect in the §7 joint zones and the tail root.
4. Manual separation of D-1 / D-2 / D-3.
5. Final shrinkwrap pass with the identity zones masked to nearest-surface.

Risk: loop flow at the shoulders and hips needs manual correction.

**M-B — manual retopology.** Polygon-by-polygon in the UI with snapping to the working copy. Best edge flow, but slow; on the order of days of UI work.

## 6. Gates (contract §13 / §16)

| Gate | Requirement |
|---|---|
| Source | Hash in = hash out |
| Production topology | 1 component, 0 boundary, 0 non-manifold, 0 self-intersections, 0 duplicates / degenerates, **genus 0**, outward normals, ≥ 98 % quads (100 % in §7 zones), §7 loop minimums met, §8 density met; vertex count **reported, no budget gate** |
| Deviation | Body T-1 and identity zones T-2, both directions, by zone |
| Micro-detail exemptions | Allowed only for: toenail plate edge bevel, fingernail plate edges, fine skin creases. Each must be listed with its max deviation and appear in the author sheet; carried by a later normal map |
| Stature / bbox | T-3. Foot length ±T-3. Nail projections ±0.15 mm (proposed) |
| Landmarks | Full contract §12 set, with tail chain 12. Source-fit vs production-fit drift T-6 |
| Silhouette | Body-only IoU ≥ T-7, front / profile / rear |
| Visual | Author sheet: source vs production vs overlay plus deviation heat maps. Close-ups of head, hands (both), feet and nails, tail root, axilla and perineum |

## 7. Output

**Path:** `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Gorrund/RP1/`

| File | Content |
|---|---|
| `GO_U_REF_RP1_weldsrc_v001.blend` | Derived welded working copy |
| `GO_U_REF_RP1_retopo_v<NNN>.blend` | Production mesh; checkpoint versions kept |
| `.glb` | Of the final checkpoint |
| `<name>.json` sidecars | Per contract §2 |
| `GO_U_REF_RP1_landmarks.json` | Landmark package |

**Repository:**
- gate `reviews/claude-rac-rp1-gorrund-production-retopo-pilot-gate.md`;
- evidence `reviews/rac-rp1-evidence/`;
- tools `tools/rac/rp/`.

## 8. Stop conditions

- Source hash mismatch.
- Any identity-zone deviation over T-2 that cannot be removed without changing anatomy.
- D-1 / D-2 / D-3 separation needing more than T-2 max movement.
- Loop requirements in §7 that cannot be met without surface deviation beyond T-1.
- Any change to accepted anatomy.
- Disagreement between the method and the authoring rule.
- Completion: **STOP for author acceptance** (family-pilot rule, contract §15). RP2 does not start automatically.

## 9. Return

**Status line:** `RP1 Gorrund production-mesh pilot — PASS / CONSTRAIN / FAIL`.

**Also returned:**
- the vertex count;
- the deviation table;
- the topology report;
- the landmark file;
- the author sheet.

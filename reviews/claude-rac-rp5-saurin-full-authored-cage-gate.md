# RAC RP5 — Saurin full authored cage: targeted revision gate

Order: `reviews/chatgpt-rac-rp5-saurin-targeted-revision-until-pass-order.md` (236dddc), under the standing directive `reviews/chatgpt-claude-internal-audit-pass-before-submission-directive.md` (de3a185).
Evidence: `reviews/rac-rp5-evidence/saurin/full_cage/revision/`. Tools: `tools/rac/rp/saurin_rp5_v002/`.

Nothing is frozen. The canonical W2I6 files and the accepted tail module are unchanged (229 / 229 immutables unchanged, `revision/immutable_hashes_revision.txt`). No rig, UV, LOD, creator, UE5 or other-race work was done. No pilot `.blend` files were made, because §16 allows them only after an internal PASS.

## Decision

## REQUIRES AUTHOR DECISION — hand / foot web topology on the approved architecture

The order asks for webs that are "two coarse rows deep" (§6, §7). On the approved coarse architecture (§1), I can't build that locally. Every web strip in the quad mesh is either a whole-body edge loop or ends at the tail-root hole.

I traced all 28 web side-edges (`SA_web_strip_traces.json`):
- 24 close only after passing through fingers, arms, trunk, legs and head: 134 to 322 coarse quads per loop, 5 distinct loops.
- 4 end at the tail-root hole. Cutting there would change the accepted module's 128-vertex root ring, which is not allowed.

The local alternative is a pole-terminated web row (coarse inset of the web quad). I built and measured it: folded web quads went from 75 to 343 (finger) and from 99 to 379 (toe). So the only working ways to get two-row webs change the approved density architecture. That is the author's call.

The same audit found a defect class the T-4 definition does not catch: **folded and concave quads** (§3 below). They sit in the single-row webs and in the palm and forefoot 2:1 rows, and their fix depends on this decision.

**Please choose one:**

| Option | What it does | Cost | Expected effect |
|---|---|---|---|
| **A. Whole-body edge loops** | 5 coarse loops through the webs. Each loop runs along digits, arms, trunk, legs and head. | About +77k fine quads (+71 %). Architecture changes globally. | Two-row webs everywhere. Extra density also eases the palm and forefoot 2:1 rows. |
| **B. Local hand / foot density** | One extra subdivision level confined to hands and feet, with a fine-level 2:1 ring at the wrists and ankles. | About +68k fine quads (+63 %). Body architecture unchanged elsewhere. | Webs and 2:1 rows get 4× resolution and can wrap the creases without folding. |
| **C. Keep single-row webs** | Keep the approved architecture. Accept a bounded, documented residual of folded / concave quads in webs, 2:1 rows and orbit corners as an explicit exception class (like tip caps). | None | Needs an accepted tolerance. Currently 661 inverted / 486 concave quads outside the tip caps. |

**Second ruling requested:** add the fold census (`sa_foldcensus.py`) to T-4 as a gate criterion, with a tolerance. My recommendation is zero inverted and zero bow-tie quads outside tip caps after option A or B, and an explicit exception table under C.

My recommendation is **B**. It keeps the approved body architecture and the semantic loops untouched outside the hands and feet. It puts density only where the creases need it, and it fits the layered strategy, since the extra resolution is structural rather than scale detail.

## 1. What passed internally on the revised cage

**Cage:** `SA_RP5_full_cage_revision_t2.npz` (sha256 `cdbbd24d…`).
- 107,796 V / 107,794 Q, 100 % quads, one closed manifold with the tail.
- Shared c1 / c2 face list.
- The accepted tail module and its root ring are unchanged.

| Gate | SA-M188 | SA-F188 | Target | Result |
|---|---|---|---|---|
| T-1 median / p95 / max (mm) | 0.067 / 0.450 / **2.66** | 0.067 / 0.449 / **2.63** | ≤ 0.5 / 1.5 / 3.0 | PASS (was 5.08) |
| T-2 max head / hands / feet (mm) | 1.31 / 1.23 / 1.31 | 1.31 / 1.22 / 1.29 | ≤ 1.5 | PASS (was 2.65 / 2.07 / 1.92) |
| T-2 max tail root / stations (mm) | 1.18 / 1.22 | 1.18 / 1.41 | ≤ 1.5 | PASS (was 0.96 / 1.77–1.86) |
| T-2 median / p95 (every zone) | ≤ 0.09 / ≤ 0.67 | same | ≤ 0.3 / 0.8 | PASS |
| T-3 stature / bbox | PASS | PASS | | PASS |
| T-5 density | PASS | PASS | | PASS |
| T-6 landmarks max | 0.99 mm | 0.98 mm | ≤ 1.0 | PASS |
| T-7 silhouette with tail (min) | 0.9959 | 0.9964 | ≥ 0.995 | PASS |
| T-4 aspect > 4 (all / outside tips) | 36 / 29 | 37 / 29 | 0 outside tips | open: thumb re-seat residual (§2) |
| T-4 angles outside 45–135 | 0.54 % | 0.61 % | documented | open (tied to §3) |

**How each closure was made** (all within the order's bounded corrections):
- **Axillary vault (§3):** authored patch `sa_vault.py`, mirrored on both sides.
  - The patch is a disk of quads spanning the pocket mouth, inset twice. The result is two support rings plus a patch floor.
  - The rings sit at 1/3 and 2/3 of the source pocket depth; the floor sits on the vault apex.
  - Placement is by depth bands along the pocket axis, followed by source-driven sliding. cc5's row heights were not repeated.
  - T-1 max went from 5.08 to 2.66 mm.
- **Nostril pits (§5):** pit rings on both nostrils with depth placement. Head T-2 max went from 2.65 to 1.31 mm.
- **Shoulder–neck slope, mouth crease and tail stations:** closed by source-driven optimisation.
  - `sa_qopt.py`: candidate sliding with a coverage roll-back guard.
  - `sa_gopt.py`: joint gradient optimisation with shape, angle, convexity and coverage barriers, re-projection onto the source, and a per-vertex roll-back.
- **T-4 aspect:** two symmetric hip-root edge loops (`sa_loopcut.py`). Aspect > 4 outside tips went from 641 to 0 before the thumb re-seat (§2).

## 2. Thumbs were inside-out — fixed

The audit found that both thumb tubes were built inside out: 790 of 1,152 thumb quads faced into the body.
- **Cause:** `sa_design.py` chose the ring sense from the thumb hole's projected angles. The hole is seen nearly edge-on along the thumb axis, so the sense was ambiguous and produced a 180° twist.
- **Fix:** the ring correspondence is now chosen by the least 3-D distance over both senses and 4 phases.
  - The coarse face list is unchanged; only ring corners r1 / r2 swap 1 ↔ 3.
  - The fine thumbs were re-seated with `sa_thumbfix.py`. Thumb inversions went from 790 to 19.
- **Residual:** 29 thumb quads with aspect > 4 from the re-seat. This is local clean-up under any option.

## 3. New defect class: folded / concave quads (`sa_foldcensus.py`)

Two checks:
- **Inverted:** quad normal opposite the source normal under it.
- **Concave:** a dart or bow-tie corner.

T-4's unsigned 45–135° angle test misses both. They were present in the previous gate's cc4 cage too.

| Cage | Inverted (non-tip) | Concave / bow-tie (non-tip) | Main structures (concave) |
|---|---|---|---|
| cc4 (previous gate) | 1,203 | 614 | thumbs (inside-out), palm 2:1 row, webs, orbit fans, forefoot 2:1 row |
| revision t2 | 661 | 486 | palm 2:1 row 109, toe webs 80, finger webs 73, orbit fan 67, forefoot 2:1 row 53, vault patch 26, nostril 24 |

**What else I tried** (each built and measured, none adopted):
- **Fine-level untangling:**
  - harmonic / Tutte patch re-solve (`sa_untangle.py`);
  - parameter-space untangling on a flattened source disk (`sa_untangle2.py`);
  - Coons re-grid (`sa_regrid.py`);
  - source-parameterised coarse-quad re-sampling (`sa_reparam.py`).

  None of them reaches the web folds. The source under a web quad is not a disk that the quad's border can map onto, and the closest-point / ray projections collapse grid rows onto the crease.
- **Coarse redesign:**
  - Palm 2:1 moved one ring proximal (H0b 8 → H1 16): palm folds in cold builds went from 227 to about 82–107. Kept in `sa_design.py`, but not yet in the gated cage.
  - Forefoot 2:1 moved proximal: worse (107 → 349). Reverted.
  - Radius-matched orbit fans: within run-to-run noise.
  - Normal-ray projection in `sa_ccage.py` (`RAYPROJ`): orbit improves, palm worsens.

The webs remain the hard core, which is why I'm asking for the decision above.

## 4. Other order items — status

- **PD-2 creator ownership (§11), `SA_PD2_source_ownership.json`:** all 19 accepted states run, including the 6 new head states.
  - In high fat / high muscle / muscle + fat, 96 / 29 / 175 cage flips lie over source folds; the dense base folds 6,675 / 1,197 / 11,201 triangles.
  - One cage-owned flip exists in each of 4 states (T80, B-T80, FAHI, MUFAHI). It is a single thin perineal ring quad from a support patch that the current cage no longer contains. It must be re-checked on the post-decision cage.
- **Head creator states (§12), `cr_head.py`:** all six built on the shared face list with the accepted W3B route.
  - orbit spacing −8 % (dx −0.372) and +3 % (dx +0.128);
  - ridge m 0.90 and 1.30;
  - display root low (minimal ridges) and high structural (crest 2.42 cm).

  0 cage flips in all six. Hand and foot: NOT RUN, because no canonical driver exists.
- **Deformation ownership, 4 steps (§10), `sa_deform4.py`:** the tool is complete. It has:
  - region-masked scaffold, digit chains, fist / grasp / opposition / toe flex and ext;
  - heat-diffused improved weights;
  - a smooth dual-quaternion field applied to the cage and to the full-resolution source.

  On the interim cage (`SA_deformation_4step_interim_v2.json`), 14 poses carry 1–9 topology-only flips. All of them sit on fold-prone quads: thumb base, webs, vault patch, hip root. Their status depends on the decision.
- **Detail layer (§13), `sa_detail2.py`:** rerun on c1, c2 and the Narrow creator state.
  - Deviation median 0.068 mm, p95 0.45 mm.
  - Detail edge-jump p99.9 is 1.71 mm against the canonical 1.58 mm; max is 2.30 mm against the canonical 2.41 mm.
  - No cage-induced discontinuity.
- **Direct identity metrics (§14), `sa_identity2.py`:** all measured on the cage mesh itself (sections, the cage's own authored rings, projected ridge metric). Will run on the final cage.
- **Boards A–P (§15), `sa_boards_final.py`:** written, with no WIP labels. Will render on the final cage.
- **Pilot export (§16), `sa_pilot_export.py`:** bpy, with read-back. Held until internal PASS.

## 5. After the ruling

1. Apply the chosen web option, and the palm 2:1 redesign that is already in `sa_design.py`.
2. Re-run the scripted chain:
   - cold build;
   - vault and nostril patches;
   - `sa_qopt` and `sa_gopt` with convexity;
   - fold census.
3. Close the thumb residual and the deformation topology flips.
4. Rerun creator / PD-2, detail, identity, boards, pilot files and immutables.
5. Return a PASS gate.

STOP FOR AUTHOR / CHATGPT DECISION.

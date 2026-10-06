# RAC W1d — Saurin D-2 Joint-Centre Source: Search Result and Author-Decision Packet

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §10 (work order item 7)
**Status:**
- The failed inferred-joint re-pose is **rejected and not used**.
- SA-M and SA-F are unchanged.
- Section-centroid joint inference is **not repeated**.
- **No closure-rig correspondence exists.**
- Saurin limb/segment items **stay blocked** pending the decision below.

## 1. Search for a valid closure-rig correspondence

| Place searched | Finding |
|---|---|
| Repository (`tools/rodin/`, `reviews/`) | Saurin build scripts and metrics only; no armature, joint list or skin weights |
| PC `E:/UnrealProjects/Wayfarer 5.8/RaceBodies` (and `out/`) | `saurin_final_base.npz` (v, f only), `rebuild_final.py` (surface rebuild only), Iteration 3 MPFB race builds. The Iteration 3 Saurin had a generator rig, but the closure body does **not** derive from it |
| Closure working chain (`/tmp/claude-0/rodin`, the session that produced aff1b52) | The closure body descends from `base.obj`, a 500,036-vertex Blender export of a **Hyper3D/Rodin-generated mesh** (`load.py` → `mesh.npz`), then sculpt and upsample stages (`c12/build15.sh`: `igl.upsample`, region and surface passes). It has region labels (`Lbase.pkl`: head/torso/arm/leg/tail masks, section centrelines), **no skeleton** |

**Conclusion:** the closure reference never had a rig, so there is no correspondence to recover. Any Saurin joint centre would be a **new builder act on accepted anatomy**.

## 2. What Saurin canon says about limbs and joints

**Positive statements:**
- SAURIN L154: the pelvis is provisionally longer front-to-back and posteriorly organized; "the hip joints and proximal femora are positioned relative to that posterior mass".
- SAURIN L156: not a crouched-lizard pelvis; no forced splayed legs.
- SAURIN L259–260: "mature knees; distinct ankle/foot architecture".
- SAURIN L265–278: provisionally **plantigrade**; "Plantigrade does not mean human-foot anatomy".
- SAURIN L294–298: arms humanoid in functional reach, "need not duplicate human segment ratios"; forearms may carry somewhat greater proportional contribution than Marchfolk.
- SAURIN L526, L532: not rangy reach specialists; no Grask limb dominance and no Cogling distal redistribution.

**OPEN in canon:**
- SAURIN L302: "Exact humerus/forearm ratios remain OPEN."
- SAURIN L575: limb segment ratios are listed OPEN.

**Implication:** the joint centres **determine** the segment ratios that canon leaves OPEN. Placing them is identity-relevant (D-5 rule 4). It must not be done silently, and it must not be inferred from section centroids (failed, W1c).

## 3. Options

| Option | Method | Identity effect | Recommendation |
|---|---|---|---|
| **J-1 Author-placed joint centres** | Tyler or the author marks hip, knee, ankle, shoulder, elbow and wrist per side on the frozen SA-M in Blender (6 points per side), constrained by L154 (hip relative to posterior pelvic mass), plantigrade ankle, and mature knee | Segment ratios become **authored** for the reference only, recorded as reference construction values (not population canon) | **Recommended** if the limb items are needed in W1/W2 |
| J-2 Builder-placed, surface-landmark method | Claude places the joints from external landmarks with a stated rule (knee = midpoint of the femoral condyle region at the knee crease; ankle = midpoint of the malleolar prominences; elbow from epicondyle prominences; wrist from the styloid region; hip from the posterior-pelvic-mass relationship), with every choice listed | Builder-chosen ratios: the same identity effect, but authored by the builder; needs explicit acceptance | Acceptable only with acceptance of every placement |
| J-3 Keep blocked | No Saurin limb/segment readings | None | Valid. RM-UB-01 (SA limbs) and RM-UB-04 stay blocked; nothing else in W1/W2 depends on them except Saurin limb comparisons |

Under J-1 or J-2, the measurement copy is then re-posed **about those fixed joints** and verified by the D-2 invariance table:
- segment lengths constant by construction;
- region dimensions and volume within tolerance;
- tail and head untouched;
- stature from the frozen body.

## 4. Author decisions needed

- **J-D1:** choose J-1, J-2 or J-3.
- **J-D2:** if J-1 or J-2, confirm that the resulting Saurin segment ratios are **reference construction values**, not population canon (L302 and L575 stay OPEN).

— Claude

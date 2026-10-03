# Saurin Gate 5: Forelimb / Wrist / Hand Reconstruction (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-gate5-forelimb-hand-reconstruction-order.md` (43c90f4)
**Base:** accepted Gate 4, `7d5a128`. Arms and hands only. **Stopped for review**; whole-body integration not started.

**Images** are in `reviews/images/saurin-gate5/`:

| Required item | File |
|---|---|
| 1. Five full-body views | `g5_01_five_views.jpg` |
| 2. Close shoulder / upper arm | `g5_02_shoulder_upper_arm.jpg` |
| 3. Close elbow | `g5_03_elbow.jpg` |
| 4. Close forearm / wrist | `g5_04_forearm_wrist.jpg` |
| 5. Isolated hand: dorsal, palmar, radial, ulnar, front 3/4 (palmar and dorsal) | `g5_05_hand_isolated.jpg` |
| 6. Grasp readiness / thumb opposition | `g5_06_grasp_readiness.jpg` |
| 7. Before/after vs Gate 4, identical cameras (body and isolated hand) | `g5_07_before_after.jpg` |
| 8. Geometry-accounting overlay | `g5_08_accounting.jpg`, `g5_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `SaurinGate5_Arms.fbx` (full resolution; imports into Blender)
- `saurin_gate5.npz`

The mesh has 706,392 vertices and 1,412,696 triangles. It is watertight: 0 boundary, 0 non-manifold, 0 orientation conflicts. The `.blend` (34.8 MB) is over the 30 MB transfer limit and does not compress, so it was not sent. The FBX is the same mesh.

**Scripts:** `tools/rodin/gate1/`
- `hand.py`: the new hand.
- `blur_arms.py`: arm base low-pass.
- `g8.py`: the arm field.
- `assemble9.py`: surgery.
- `ev5.py`, `compose5.py`: accounting and sheets.

## 1. Method

**Skeleton kept.** Each arm keeps its B1 shoulder–elbow–wrist axis, so shoulder placement, arm length, hang and stance are unchanged. B1 is slightly asymmetric and that was preserved:
- **Shoulder:** left (−23.5, −6, 147); right (23, −5, 147).
- **Elbow:** left (−30.5, −4.5, 117); right (28.8, −3.5, 117).
- **Wrist:** left (−36.8, 6, 97); right (35.2, 7, 97).

**Surface, in three layers** (the same approach as the accepted Gate 3A and Gate 4 work):

1. **Base.** A 2.8 cm low-pass of B1's arm, computed together with the **closed** upper body. This keeps limb mass and silhouette while removing:
   - the human deltoid cap and its sharp lower rim;
   - the biceps/triceps belly map;
   - the old Rodin hand.

   Because the shoulder and armpit are part of the same closed low-pass, the upper arm **grows out of the thoracic/scapular mass** instead of plugging into a cap. An intermediate version that used only the arm surface left a crease and a band across the upper arm; that version was discarded.
2. **Load paths.** Surface-conforming paths with varying width and height, fading in and out and combining smoothly where they overlap (§2).
3. **Hand.** The hand is **replaced** by a new hand (§3), joined to the forearm through an overlapping carpal block.

## 2. Load-path organization (shoulder → wrist)

| Region | Structures |
|---|---|
| **Shoulder** | Three overlapping fans (**clavicular**, **acromial**, **scapular**) start on the thoracic/scapular surface and converge on the lateral humerus. They carry elevation, swing and stabilization. No deltoid ball; the locked Gate 2A torso was not altered to make the arm fit |
| **Upper arm** | A long **anterior flexor plane** that continues into the medial forearm. A **posterior extensor plane** with a **lateral slip**. Directional planes, not biceps/triceps bellies |
| **Elbow** | The upper arm ends in a **posterior extension ridge** (olecranon line), with **medial and lateral epicondylar stabilizers** and a soft **anterior hinge hollow**. The forearm's two main paths split below it. No spikes |
| **Forearm** | **Flexor mass** (palmar/medial) and **extensor mass** (dorsal/lateral). A **spiral rotational band** runs from the lateral elbow to the radial wrist, carrying pronation/supination. An **ulnar load ridge** and **two distal tendon paths** lead into the wrist. The forearm narrows without becoming a tube |
| **Wrist** | The forearm ends in a controlled narrowing that overlaps a distinct **carpal block**, which then widens into the metacarpal palm. An earlier version pinched into a thin stalk; that was fixed before this checkpoint |

## 3. Hand: full reconstruction

Wrist to claw tip is about **21 cm (0.11H)**, no larger than B1's hand. It is not a monster hand.

Chain:
1. **Carpal block**.
2. **Metacarpal palm**, with a **thenar mass** at the thumb base and a **hypothenar ridge** along the ulnar edge. The palm is a narrow, deep frame rather than a broad human palm.
3. **Knuckle row**.
4. **Phalanges 2-3-3-3-3** (I–V), with joint swellings so articulation reads in clay.
5. **Claws** that **grow from the terminal phalanx**: the claw continues the last segment and curves palmar. Claw geometry is basic, only enough to show the integration.

**Digits**
- Lengths differ: III is longest, then II and IV, then V.
- Spacing and splay are uneven.
- Pose: a relaxed, natural curl.

**Thumb**
- The metacarpal sits **palmar to the palm plane**, and the tip points across the palm toward II–III.
- This is a functional **opposable** thumb: a pinch or grip can close without re-rigging (`g5_06`).

**Not:** a paw, raptor talons, dragon claws, or a human hand with nails.

**Relationship to the foot**
- **Shared with the foot:** joint rhythm, joint swellings, and claws grown from the terminal phalanx.
- **Different from the foot:** the hand has no contact pads and no metatarsal fan; it is narrower and deeper, with an opposable thumb. The foot was not mirrored.

## 4. Lock accounting (vertex identity against Gate 4)

| Locked region | Vertices | Identical |
|---|---|---|
| Free tail (F < −45) | 34,263 | **34,263** |
| Gate 1 pelvis/sacrum/tail root, Gate 2A torso, Gate 3A neck, TS6.1 head (\|x\| < 19.5) | 382,380 | **382,380** |
| Of which head + neck (U > 150) | 117,471 | **117,471** |
| Gate 4 legs + feet (U < 86) | 284,246 | **284,246** |
| Gate 4 hips/thighs beside the hands | 10,128 | **10,128** |

- **Changed:** 7,944 Gate 4 vertices. All lie at \|x\| ≥ 19.5 and within 3.0 cm of B1's own arm/hand surface. This includes a small patch on the outer thigh where B1's hand touched it.
- **Seam:** 61 vertices relaxed (at most 0.93 cm). 184,231 vertices are new.
- **Height:** standing height 188.0 cm (187.96), unchanged.
- **Shoulder placement:** unchanged.

The Gate 4 hand in `g5_07` is cropped in the same hand frame as the new one. B1's hand hung at a slightly different angle, so the old crop is not perfectly aligned with the frame.

## 5. Self-assessment and open issues

**Delivered**
- Deltoid cap, biceps/triceps map and the Rodin hand removed.
- A continuous scapular/thoracic → upper arm → elbow → forearm → wrist → carpal → palm → digit → claw chain.
- An opposable-thumb grasping hand at B1 scale.
- Every lock is vertex-identical.

**Honest gaps (for whole-body integration)**
1. **Arm mass.** Upper-arm and forearm volume is B1's, low-passed. The paths organize it, but the overall arm proportion is still B1's athletic one, for the same reason as the Gate 4 thigh.
2. **Digit and claw rhythm.** The knuckle swellings are evenly spaced and bead-like in places, and the claws are small compared with the foot claws. Both are proportion calls for review.
3. **Hand vs body sculpt.** The hand is a clean construction and smoother than the body's sculpt, like the Gate 4 foot.
4. **Elbow and wrist richness.** Both are mechanically readable but still simple. These are already on the whole-body integration list.
5. **Mesh density.** The mesh is about 1.41 M triangles. A decimate/remesh pass is needed before rigging, and it would also bring the `.blend` under the transfer limit.

No scales, texture, pigmentation, horns, eye work, finished claws or UE5 work.

**STOP: Gate 5 checkpoint.**

— Claude

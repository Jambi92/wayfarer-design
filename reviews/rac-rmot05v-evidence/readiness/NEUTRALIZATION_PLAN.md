# RM-OT-05V neutralization plan (frozen before the production run)

**Order:** `reviews/chatgpt-rac-rm-ot-05v-gorrund-arm-neutralization-closure-order.md`.
**Start state:** U8 cp1, `GO-05U8_cp1.blend` (`2341d554…`), exported return `reviews/rac-rmot05u8-evidence/return/checks/return.npz` (`89c1def3…`).
- Both stay unchanged.
- Neutralization works on a separate state chain (N0 → S01 … S10), and the result is written to a new scene, `GO-ARM-N1.blend`.

**Tools (additive):** `tools/rac/w1/rmot05v_drivers/`. No upstream tool, verifier or pinned set was modified.

## 1. Method, and why it is scripted rather than hand-sculpted

| Item | U6–U8 practice | 05V reality |
|---|---|---|
| Work size | 1 to 16 vertices per block, typed in the desktop Blender sidebar | Fused garment surfaces of about 80,000 source faces (05Q inventory zones 1–3 and 5–10). None of them has skin beneath (class c), so every one needs new surface |

Direct desktop editing at that scale is not feasible, and could not be verified vertex by vertex. The order says "prefer" desktop work, not "require", so every group is a **deterministic local implicit rebuild** (`v_engine.py`, `v_rebuild.py`). A step works as follows:

1. A frozen **region** g < 0 is chosen. Most regions are Voronoi separations between the vertices to rebuild (A) and everything kept (B), so the boundary runs mid-way through air gaps and crosses the skin transversally.
2. Every face outside the region is copied **bit-exact**, with the same S3 identity (`rac_s3_vid1`).
3. Inside the region, an **INFERRED** field is extracted with surface nets. The field blends the source signed distance (at the boundary) into a smoothed, opened or offset source, plus primitives:
   - toe round-cones;
   - an inferred cranium and neck;
   - the mirrored bilateral counterpart;
   - the placed source tail.
4. The extracted patch is **bridged** to the kept loops. The seam is faired, and triangle quality is enforced at no less than 12° on new faces (verifier floor 10°, the U6–U8 local floor). Local self-intersections are repaired.
5. **Exception, step B2:** the −X arm is a mesh **transplant**. The +X arm faces are mirrored across the bilateral plane x = −0.5 (`symmetry_fit.json`) and bridged at the shoulder, so the transplanted geometry is exact mirror copies.

Every new face carries a group label (1 to 5 for A to E, 9 for seams). All of it is **INFERRED**.

## 2. Verification per step (`v_verify.py`, independent of the builder)

| Gate | Requirement |
|---|---|
| P1 | Every previous face entirely outside the region is present unchanged. Missing faces are allowed only within 2 rings of the region (bow-tie / spike cleanup) or in small detached debris components |
| P2 | Every new vertex lies inside the region (1 cm seam band), or for B2 is an exact mirror copy (or seam-band vertex) of the counterpart |
| P3 | Previous vertices outside the region are bit-exact |
| T1 | No non-manifold edge, consistent orientation, no new open boundary |
| T2 | No self-intersection that involves this step's faces, or that newly involves inherited faces (pymeshlab) |
| Q1 | Minimum angle of this step's faces ≥ 10°. Exact mirror copies of inherited source faces are documented separately |
| L1 | Every non-inherited face is labelled INFERRED |

**Tests:** `v_tests.py`, 8 / 8 as expected (`v_test_summary.json`).

## 3. Steps (order, groups, sets)

| # | Step | Group | Region | Inferred content |
|---|---|---|---|---|
| 1 | A1 | A | Box: front chest / throat, x ±26, y ≥ 4, z 140–183 | Opening r 3 + blur 1: front braids (lower parts), necklace, pendant teeth |
| 2 | A2 | A | Box: back braid, x ±10, y −42…−12, z 143–176 | Opening r 3 + blur 1 |
| 3 | B1 | B | Voronoi: +X forearm, z 102.8–146 (`v_sets.B1`) | Blur 1 → 2.4, offset 1 cm over the bracer (bracer removed) |
| 4 | B2 | B | Voronoi: −X arm wreck. The 05N contact-slab seam left the −X arm open from z 97 to 174, and its hand is fragments (`v_sets.B2`) | Transplant of the +X arm (after B1) as the bilateral counterpart, which also removes the −X armband |
| 5–6 | C1± | C | Box: lower leg + foot, each side | Blur 1 → 2.6 and offset 1.2 cm over the wraps; ground clip at z = 0 |
| 7–8 | C2± | C | Box: forefoot (`v_feet.py`) | Canon enforcement: five humanoid toes, hallux medial and longest, 0.5 cm clefts, ball pad, dorsal taper, raised nail plates, at the measured foot scale |
| 9 | D | D | Voronoi: slab z 66–147 minus both arm components (`v_sets.D`) | Opening r 4.5, blur 2.5, offsets 1–2 cm (belt, flaps, flank flare); crotch arch (elliptic cylinder, top at z 105, consistent with the source crotch ≈ 104–107 recorded in 05N); source tail study placed at the 05N review placement (`v_tail.py`, from the immutable `base.glb`) |
| 10 | E | E | Voronoi: head / neck / mane cap above z 168 (`v_sets.E`) | Facial mask and throat re-extracted from source; INFERRED cranial vault, neck and broad ear attachments; shoulders / upper back from the source with the mane shrunk 4 cm; ears = the −X source pinna and its bilateral counterpart (the +X side carries only a hair spike) |

**Group order.** The order's sequence A, B, C, D, E is kept. Within B, B1 runs before B2 because B2's transplant needs the neutral +X forearm. Each group ends at a verified checkpoint (A after S02, B after S04, C after S08, D after S09, E after S10).

## 4. Builder-chosen values (R-14; not canon)

Every number in `v_chain.py` PLAN, `v_feet.py`, `v_sets.py` and `v_tail.py` is a builder value:
- region bounds;
- blur, opening and offset amounts;
- toe layout and radii;
- cranium and neck primitives;
- ear attachment;
- tail placement (05N review values);
- the bilateral plane x0 = −0.5.

They are recorded as provenance, not as discovered anatomy.

## 5. Prototypes (disclosed)

The plan values were tuned on scratch copies before this plan was frozen. No prototype output is a candidate. The production chain regenerates everything from U8 cp1 with the frozen code.

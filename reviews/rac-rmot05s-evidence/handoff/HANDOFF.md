# RM-OT-05S direct-edit handoff: +X armband band-to-axilla interface

**Why this handoff exists.** The scripted direct study S1→S3 removed the garment ledge at both junctions:
- outside anatomy is bit-identical;
- there are 0 intersections, and no fold over 120°;
- seam continuity is 97.8 %.

It still leaves an **unresolved crinkled / notched strip along the posterior fold edge** (θ −86…−106°, s 2–8 cm) and a crease at θ ≈ −90°. Those defects need interactive anatomical judgement. Only a headless scripted pipeline was available here, with no interactive sculpt, so this kit hands that exact interface to a direct editor.

Nothing here contacts or hires anyone, and nothing incurs costs.

## Files

| File | Content |
|---|---|
| `GO-05S_interface_handoff.blend` | Blender 5.0.1 scene, compressed; the units are cm (scene scale 0.01). Objects are listed in the table below |
| `../repair/S3/GO-05S-S3.obj.gz` | The same working mesh as OBJ, for any tool |
| `../plan/PLAN.md`, `../plan/interface_sets.npz` | Interface definition and the protected set P05S, with the 274 newly authorised faces and their classes |
| `../compare/01–09` | Source / B2 / R3 / S3 closes and sections |

The objects in the .blend:

| Object | Use | Vertex groups |
|---|---|---|
| `GO-05S-S3_working` | The working mesh | `EDIT_posterior` (180 vertices), `EDIT_anterior` (170), `FROZEN_interface_boundary` (101), `FOCUS_posterior_crinkle` (57). Face attribute `rac_label`: 0 source, 2/3 05Q inferred, 4 05S transition, 5 05S inferred skin |
| `F1_source_reference` | Reference only: hidden and locked | — |
| `B2_reference` | Reference only: hidden and locked | — |

## Brief (scope is fixed by 05S §3–4)

1. **Edit only** vertices in `EDIT_posterior` / `EDIT_anterior`.
   - Local retopology inside those faces is allowed.
   - `FROZEN_interface_boundary` and every other vertex must stay **exactly** where they are.
2. **Posterior.** Replace the crinkled strip in `FOCUS_posterior_crinkle` with a clean arm-to-posterior-axillary-fold crease.
   - Keep the deltoid / triceps relief beside it.
   - Keep the tapered garment termination toward θ −136°: no lip and no cut end.
3. **Anterior.** Keep the smooth arm-to-pectoral transition, refining the termination only if needed.
4. **Do not:**
   - remove the full ring or separate the arm from the trunk;
   - rebuild the shoulder or axilla;
   - change pose, scale or limb length;
   - smooth or remesh globally;
   - project garment detail.
5. **Labelling.** All new skin is **INFERRED**. Do not invent recovered high-frequency anatomy.

## Verification setup

Export the whole working object as OBJ: triangulated, with **no** transform and no scale change. Then, from the package or repository root:

```bash
gunzip -c reviews/rac-rmot05q-evidence/source/F1_working.obj.gz > F1_working.obj
python3 tools/rac/w1/rmot05s_drivers/s_rematch.py --edited EDITED.obj --src F1_working.obj --plan reviews/rac-rmot05s-evidence/plan --out EDITED_rm
python3 tools/rac/w1/rmot05s_drivers/s_verify.py --src F1_working.obj --q05 reviews/rac-rmot05q-evidence --plan reviews/rac-rmot05s-evidence/plan \
        --res EDITED_rm.obj --maps EDITED_rm_maps.npz --labels EDITED_rm_face_labels.npy --out EDITED
```

- **`s_rematch.py`** recovers correspondence by **exact coordinates**. It reports any protected face that went missing or moved, and any such face means V1 FAIL.
- **Self-test:** running it on S3 itself recovers all 139,807 protected faces, and `s_verify` reproduces S3's scores (`selftest_*.json`).
- **Pass rules** are the pre-registered V1–V5 and V6c-1..3 in `../plan/PLAN.md`. Anatomical credibility is decided by the author.

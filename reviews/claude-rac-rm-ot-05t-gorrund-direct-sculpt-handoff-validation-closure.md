# RAC RM-OT-05T (executed under 05T1): direct-sculpt handoff validation, closure

**Orders:**
- `reviews/chatgpt-rac-rm-ot-05t-gorrund-direct-sculpt-handoff-validation-stop-order.md` (4aa9232);
- `reviews/chatgpt-rac-rm-ot-05t1-execute-handoff-validation-order.md` (98691ef).

**Evidence:** `reviews/rac-rmot05t-release/`. **Tools:** `tools/rac/w1/rmot05t_drivers/`.

## State

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED / DIRECT SCULPT REQUIRED** |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| Canon promotion | NOT PERFORMED |

The source master `base.glb` is unchanged (`78ecfa87…a7b`).

No S4, RD5, candidate generation, scripted morphology, interpolation or relaxation was done. Nothing was installed, nobody was contacted, and no credits were spent.

**→ STOP AWAITING DIRECT-SCULPT RETURN.**

## Outcome in short

- **The existing 05S handoff scene is geometrically correct.**
  - Its working mesh equals S3 at Blender's float32 storage.
  - Labels, groups, transforms, units and references are all correct.
  - Editable and frozen sets are disjoint, and the posterior focus lies inside the editable set.
- **Its export instruction was broken.** 05S `HANDOFF.md` said to export an OBJ and rematch it by exact coordinates.
  - Blender's OBJ exporter prints 6 decimals and converts axes by default.
  - The rematch recovered **0 of 139,807** protected faces, so **every return would have been rejected**.
- **Fixed, additively, in a release copy.**
  - An identity attribute plus a supported exporter (`t_export_blend.py`).
  - An exact reintegration (`t_reintegrate.py`) that restores the float64 coordinates of verified-unchanged vertices from S3, by bit-exact float32 agreement, not by guessing.
- **A blind spot in the 05S V1 check was found and covered.** V1 checks only original-source faces: a moved B2-retained frozen-boundary vertex passes V1 (demonstrated). The new P1 / P2 protection check rejects it.
- **All six disposable protection tests behaved as required.** The unchanged fixture round-trips **bit-identical** to S3, with identical gate scores.
- **Desktop UI behaviour is PENDING.** Brushes, mask display and face-set isolation were not tested; only headless bpy is available.

## 1. Validation of the existing 05S scene (`validation/V_05S_original_scene.json`, 18/18 checks pass)

The scene is `reviews/rac-rmot05s-evidence/handoff/GO-05S_interface_handoff.blend`, sha `114e69cf…4d89`, **unchanged**.

| Check | Result |
|---|---|
| Units | Metric, scale 0.01 (1 Blender unit = 1 cm) |
| Transforms | Identity on all three objects; no parents |
| Working mesh | 70,751 vertices / 141,194 triangles; faces equal the S3 OBJ; coordinates equal float32(S3), with a maximum difference of 7.6e-6 cm from the float64 OBJ (float32 storage); `rac_label` equals S3's labels |
| Vertex groups | `EDIT_posterior` + `EDIT_anterior` (350 vertices) equal the interface interior exactly; `FROZEN_interface_boundary` (101) equals the boundary ring exactly; the two sets are disjoint; posterior and anterior are disjoint; `FOCUS_posterior_crinkle` (57) lies inside `EDIT_posterior` |
| References | `F1_source_reference` and `B2_reference` equal float32(F1 / B2) |
| Reference objects | Hidden **and unselectable** (`hide_select`), which conflicts with the 05T requirement that they be inspectable |

## 2. Support-only release copy (`scene/`; the 05S scene is untouched)

| File | sha256 |
|---|---|
| `GO-05T_sculpt_handoff.blend` | `c7e591fe…60cc` |
| `GO-05T_references.blend` | `50992e45…d2a5` |

Built by `t_build_release_blend.py`. The working mesh geometry is unchanged. The additions:
- **Identity attributes:**
  - `rac_s3_vid1`, the S3 vertex index + 1;
  - `rac_src_vid1`, the F1 index + 1.
- **Sculpt mask:** `.sculpt_mask` = 1.0 on all 70,401 non-editable vertices and 0.0 on exactly the 350 editable ones.
- **Face sets:** `.sculpt_face_set` = 1 protected, 2 posterior (408 faces), 3 anterior (389 faces).
- **Edit-mode isolation:** every non-interface face is hidden; 797 faces stay visible.
- **References:** `F1_source_reference` and `B2_reference` are **linked** from `GO-05T_references.blend` in the collection `REFERENCES_linked_readonly`.
  - They are selectable and their transforms are locked.
  - `data.is_editable` and `object.is_editable` are both False: linked library data cannot become an edit target.
- **Units:** length unit set to centimetres.
- **Embedded note:** a text block `RAC_EXPORT_README` warns against the built-in exporter.

**Validation:** `validation/V_05T_release_scene.json`, 22/22 checks pass. The mask, face sets and hide state were also checked numerically against the edit sets: **M test PASS**.

Vertex groups stay selection aids. Protection comes from the mask and isolation while sculpting, and is **enforced** by the reintegration check.

## 3. Export audit and controlled identity scheme

**The built-in exporter fails the identity check.** `wm.obj_export` with identity axes (forward Y, up Z), triangulated, followed by the 05S `s_rematch.py` exact-coordinate rematch:
- recovered **0 / 139,807** protected faces (`tests/T5_rematch_rematch.json`);
- the cause is 6-decimal output; the default axis conversion is a second cause.

Exact protected-region checking was **not** weakened.

**The supported path:**
1. `t_export_blend.py`, run inside Blender or with bpy. It writes:
   - `return.npz` with the exact float32 positions, triangles (any n-gons triangulated on a copy and reported) and the identity attribute;
   - a `%.9g` OBJ for viewing.
2. `t_reintegrate.py`. It trusts a vertex's identity **only if** its float32 position equals float32(S3) bit-for-bit, then restores S3's exact float64 coordinates.
   - **P1:** every non-editable S3 vertex (source, B2-retained and frozen boundary: 70,401) must be present unchanged.
   - **P2:** every non-interface S3 face (140,397) must be present with the same vertices and orientation.
   - Any violation means **REJECTED**.
   - Otherwise it writes the result in the `s_verify` layout: P05S faces first.
3. `check_return.sh` runs the export, the reintegration, `s_verify` and identical-camera before / after renders.

**Finding during testing.** Blender interpolates the integer identity attribute onto vertices created by topology operations: in T4, all 30 new vertices carried non-zero ids. The bit-exact position rule rejects such ids. They are counted and reported as `with_nonzero_but_unverified_id`, never trusted.

## 4. Disposable protection tests (`tests/protection_tests.json`; all as expected)

Each test edits a disposable copy of the release scene by script; these are tooling fixtures, not sculpt candidates. Each then runs the real return path: export, then reintegrate, then `s_verify`.

| Test | Edit | Expected | Result |
|---|---|---|---|
| T0 unchanged fixture | none | accepted | **ACCEPTED.** The result OBJ is **bit-identical to S3** (sha `1d503833…`), and the `s_verify` output is identical to S3's (UNRESOLVED) |
| T1 allowed interface edit | 20 focus vertices moved 0.05 cm | accepted | **ACCEPTED.** 20 editable vertices recognised as moved, 80 interface faces edited, V1 passes |
| T2 protected source vertex | foot vertex moved 0.001 cm | rejected | **REJECTED.** P1: 1 moved; P2: 6 faces |
| T3 frozen boundary, non-source vertex | B2-retained ring vertex 70128 moved 0.001 cm | rejected | **REJECTED.** P1: 1 (frozen); P2: 4 faces |
| T3b frozen boundary, source vertex | ring vertex 57083 moved 0.001 cm | rejected | **REJECTED.** P1: 1; P2: 7 faces |
| T4 local topology change | 30 interface edges subdivided | accepted, outside preserved | **ACCEPTED.** All 70,751 original vertices verified, 30 new vertices, 100 interface faces edited, V1 passes |
| T3v V1 blind-spot demonstration | S3 with vertex 70128 moved, scored by `s_verify` alone | — | V1 **passes**, verdict unchanged, so V1 alone misses it; P1 / P2 catch it (`tests/T3v_V1_blindspot_demo.json`) |
| M mask / face sets / isolation | numeric attribute check | pass | **PASS** |

The original validators and all previous scores are unchanged. The P1 / P2 checks are additive and have no tolerance.

`check_return.sh` was also run end to end on the unchanged release scene: ACCEPTED, `s_verify` UNRESOLVED (same as S3), five render sheets produced.

## 5. Sculptor entry point and return contract

**`START_HERE.md`** (repository: `reviews/rac-rmot05t-release/START_HERE.md`; release: root) sets out the sequence:
- **Step 0:** a first-session desktop check on a disposable fixture: units and transforms, linked references, a mask stroke test, edit-mode isolation, export and check, a deliberate protected move that must be REJECTED. **Status: PENDING.**
- **Step 1:** sculpt only the committed interface.
- **Step 2:** export and check with the supported path only.
- **Step 3:** return the edited `.blend`, the `return.npz` / `.obj`, the reintegration / verify JSON and hashes, the before / after renders and `EDIT_LOG.md`.

Also in the release:
- **`BRIEF.md`:** the task, unchanged from 05S §3–4.
- **`views/`:**
  - posterior defect shaded;
  - posterior and anterior overlays with red focus / purple editable / amber frozen-boundary faces;
  - arm overview.

## 6. Pending and limitations (not claimed)

- **PENDING:** desktop Blender UI behaviour.
  - Whether sculpt brushes respect `.sculpt_mask` in practice.
  - Mask overlay display.
  - Face-set "show only".
  - Dyntopo and remesh behaviour with the identity attribute.
  - Saving through the UI.
  - Step 0 is the gate for these.
- **PENDING:** the actual direct sculpt and its verification and author review.
- **Not verified here:** the base.glb → F1 extraction itself. That remains a separate prerequisite (05Q REPLAY).

## 7. Release

The compact release `gorrund_05T_sculpt_handoff` is built by `t_package.py`. It has its own manifest and a clean-extraction check that includes running `check_return.sh` from the extracted release. Its hashes and delivery location are recorded in the package receipt, appended after the build.

**Next direct action:** a person opens `START_HERE.md`, completes Step 0, then sculpts the posterior fold-edge strip and returns the files listed in Step 3. When that asset arrives, it is verified under the preserved gates and returned for author review. There is no automatic expansion or promotion.

---

## Package receipt (appended after the build; `reviews/rac-rmot05t-release/package/PACKAGE_RECEIPT.json`)

**Release:** `gorrund_05T_sculpt_handoff.zip`, a **single ZIP**.

| Property | Value |
|---|---|
| Size | 26,982,065 bytes |
| SHA-256 | `8bb33bf0a106cfd54b75a7085c443f8e03e19e4e71f69ce80535482495e37d9e` |
| Own manifest | `PACKAGE_MANIFEST.sha256`, 69 entries |

**Clean extraction**, in an isolated empty directory:
- `unzip -t` reported no errors.
- 69 of 69 entries are present with equal hashes; nothing is unlisted or missing.
- All 3 decoded meshes are equal.
- 6 of 6 relative links resolve.
- The release's own `check_return.sh`, run on an unchanged copy of the packaged scene, gave **ACCEPTED**, with `s_verify` scores **identical to S3**. The renders were produced.
- **Limitation:** desktop UI behaviour is not exercised; Step 0 is PENDING.
- **Result: PASS.**

The first verify attempt aborted because the container disk was full (unzip write error). It was rerun after the scratch space was freed.

**Delivered to:**
- the chat, as the attached file;
- `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\sheets\gorrund_05T_sculpt_handoff\gorrund_05T_sculpt_handoff.zip`, where the size is confirmed on the device.

**→ STOP AWAITING DIRECT-SCULPT RETURN.**

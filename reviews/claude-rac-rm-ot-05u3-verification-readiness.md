# RAC RM-OT-05U3: verification readiness addendum (no sculpt)

**Order:** `reviews/chatgpt-rac-rm-ot-05u3-verification-readiness-no-sculpt-order.md` (26947f2). **Parent proposal:** 05U2 (53fd98f).
**Evidence:** `reviews/rac-rmot05u3-readiness/`. **Tools (additive, opt-in, non-production):** `tools/rac/w1/rmot05u3_drivers/`.

**Status: VERIFICATION READINESS REVIEW / BOUNDARY AWAITING AUTHOR APPROVAL.** No production approval is claimed.

**Nothing in production was changed:**
- the 05U RETURN and its release (`aed5711f…3159`);
- `base.glb`;
- the production scene, masks and face sets;
- the active protection rules: the default `t_reintegrate.py`, `t_export_blend.py` and `check_return.sh` are untouched.

No sculpt was done and no anatomical candidate was built. The proposed lists, the hashes and the 35-face / 15-vertex scope are unchanged.

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED** |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| Reconstructed skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |

## 1. What passes

| Item | Result |
|---|---|
| Opt-in U2 path implemented (§2) | Working, end to end, including on the real 05U RETURN `.blend` |
| Default path unchanged | `s_verify.py` default output is **byte-identical** on 3 historical runs; `t_reintegrate.py` and `check_return.sh` are unmodified; the default rule still REJECTS the U1 probe |
| Disposable validator probes (§3) | **13 / 13 as required** |
| Crease-depth baselines (§4) | Both sections unambiguous: **A 0.895 cm** (75 % limit 0.671 cm), **B 0.366 cm** (75 % limit 0.274 cm) |
| U2 baseline (unchanged 05U geometry in the U2 layout) | ACCEPTED_FOR_VERIFICATION_U2 with V1-U2 pass. Coordinates, topology and correspondence are identical to the committed 05U result |

## 2. The opt-in U2 verification path

### Files

| File | Role |
|---|---|
| `u3_reintegrate.py` | The U2 adapter |
| `check_return_u2.sh` | One command: supported export → U2 adapter → `s_verify` in U2 mode → crease check → guards (b) / (e) → renders → hashes |
| `u3_crease.py`, `u3_guards.py` | Crease-depth measurement (§4) and roughness / sliver guards |
| `u3_probes.py` | The disposable probe runner (§3) |
| `s_verify.py` | **Two additive options only** (nine added lines): `--prot_faces_file NPZ:KEY` and `--src_exempt NPY`. Defaults are unchanged |

### What the adapter enforces

1. **Pinned inputs.** The S3 OBJ (`1d503833…`), the 05U baseline return (`0989caf4…`), the F1 OBJ (`17591025…`) and the proposal list hashes must all match. Altered lists or hashes are REJECTED (probes U7a–c).
2. **Derived, not trusted, sets.** The 365 editable vertices, 106 frozen vertices and 832 editable faces are **derived** from S3 plus the 35 added faces, and must equal the committed preview and its hashes.
3. **No topology change.** `rac_s3_vid1` must cover the 70,751 S3 vertices one-to-one. The exported faces, mapped through those ids, must equal the S3 faces with the same orientation. Missing, reversed, extra and duplicate faces, invalid ids and duplicate ids are all REJECTED.
4. **Exact protection.**
   - Every vertex outside the 365 must equal the **frozen 05U baseline** bit-exactly at float32; its float64 baseline value is then restored. This includes all 106 frozen-ring vertices.
   - Every face outside the 832 must be preserved.
   - A moved vertex is accepted only if its own position-verified id is among the 365. Ids alone never authorize anything: a swap spoof fails the face check, and a duplicate-id spoof fails the identity check.
5. **Provenance is kept.** All vertices, including the 15 source vertices, keep their F1 correspondence (`src_vertex` is identical to S3).
   - **Contrast with the default 05T reintegration:** it sets the correspondence of moved vertices to −1. The U2 path does not, so V1 cannot pass by erasure.
6. **P05U2 source protection.**
   - The actual 139,772-face F1 index list (sha `02b608bc…`) and the committed coordinate hash `25ffe5ac…` are used.
   - `s_verify --src_exempt` excludes only the 15 authorized F1 vertices from the bit-identity requirement, and lists every one that moved.
7. **Labels.** The 35 added faces carry **label 6** ("edited source surface, 05U2", INFERRED). The original labels 0–5 are unchanged. How each consumer handles label 6:
   - **`s_verify`:** uses labels only to annotate outliers, and reports label 6;
   - **renderers:** palette index 6 already exists (cyan);
   - **default 05T path:** never sees label 6.
8. **Layout for the geometry gates.** The 139,772 P05U2 faces come first (P05S order), then every other face in S3 order. The face-order mapping is exported (`face_order_s3`). **The 35 added faces are inside the "new" set that V2–V6c evaluate:** V4 checks 1,422 faces (1,387 + 35), and V3 tests 2,979 faces.
9. **Legacy V1, reported faithfully.** The adapter runs the correspondence-aware diagnostic on the result in S3 order:
   - the original P05S hash, and whether it matches;
   - every source vertex that actually changed, with its F1 index;
   - every P05S face affected;
   - whether all of them lie inside the authorized 15 / 35.

   The 05S `s_verify` face-prefix V1 is **not** invoked on the U2 layout, because its P05S prefix does not apply there; its pass or fail is not presented as evidence.

V2–V6c: identical code, thresholds and verdict rules.

## 3. Disposable validator probes (`probes/`, `probe_summary.json`)

**These are probes, not repairs.** Each is a synthetic edit of a **copy** of the 05U baseline arrays: no Blender, no scene, no anatomical intent. They do not replace the real desktop mask and brush fixtures, which are still required after approval.

| Probe | Edit | Required | Result |
|---|---|---|---|
| U0 | None (unchanged 05U baseline) | accept | **ACCEPTED_U2** (geometry identity below) |
| U1 | Authorized added source vertex 61581, +0.02 cm | accept | **ACCEPTED_U2**. Legacy diagnostic: changed source = [61581] only (F1 61688); affected P05S faces = 7, all inside the 35; original V1 hash no longer matches, as expected. V1-U2 passes; exempt moved = [F1 61688] |
| U1b | Existing interface vertex 70402, +0.02 cm | accept | **ACCEPTED_U2** |
| U2 | Protected source vertex 61586, just outside the boundary | reject | **REJECTED** |
| U3 | New frozen-ring vertex 61771 | reject | **REJECTED** |
| U4 | Retained old frozen-ring vertex 70139 | reject | **REJECTED** |
| U5a | Protected face 100000 removed | reject | **REJECTED** |
| U5b | Protected face 100000 reversed | reject | **REJECTED** |
| U6a | Ids of protected 61586 and editable 61581 swapped (positions untouched) | reject | **REJECTED** |
| U6b | Editable vertex claims protected id 61586 | reject | **REJECTED** |
| U7a | One extra face appended to the added-face list | reject | **REJECTED** |
| U7b | Altered list hash in `proposal_region.json` | reject | **REJECTED** |
| U7c | P05U2 preview truncated | reject | **REJECTED** |

**U0 geometry identity:**
- The float64 coordinates are **identical** to the committed 05U `result.obj`, compared in S3 order through `rac_s3_vid1`.
- Topology is identical to S3, and `src_vertex` is identical to S3.
- **Expected metadata differences only:** the face order (P05U2 prefix) and the 35 faces carrying label 6 instead of 0.

**Historical default behaviour is unchanged:**
- The default `t_reintegrate.py` ACCEPTS U0, and its `result.obj` sha `6046f013…` equals the committed 05U result.
- It still **REJECTS** U1 (P1: 1 moved), so the authorized vertex can be edited only through the opt-in path.

**Regression of the `s_verify` defaults** (`regression/`): the patched `s_verify.py` in default mode reproduces three committed files **byte-identically**:
- the 05U `result_verify.json`;
- the S3 unchanged-fixture verify;
- the committed 05S `GO-05S-S3_verify.json`.

**End to end on the real 05U RETURN `.blend`** (sha `9593d201…`, `e2e_unchanged_05U_blend/`): `check_return_u2.sh` gives ACCEPTED_U2, its `result.obj` is identical to U0, and both crease checks pass at baseline.

## 4. Crease-depth baselines (`crease/crease_baseline.json`, `crease/crease_sections.png`; `u3_crease.py`)

**Definition** (centimetres; one Blender unit is 1 cm):

| Element | Definition |
|---|---|
| Frame | The 05Q arm frame: origin O, axis d, e1 = normalize(Y × d), e2 = d × e1 (`patch_selection.json`) |
| Plane | P(s0) = { x : (x − O)·d = s0 }, perpendicular to the arm axis, with s0 = (v − O)·d for the named S3 vertex |
| Section | Exact mesh/plane intersection, interpolating every crossing edge, then chained into polylines. The polyline through the region faces nearest the vertex is used. A closed loop is rotated to start on a non-region face, so a run cannot be split at the loop's start |
| Run and endpoints | The contiguous part lying on the 832 proposed editable faces must enter and exit the region **exactly once**; otherwise the section is AMBIGUOUS and not used. The endpoints lie on region/non-region edges, whose vertices are all frozen-ring vertices, so the chord is fixed geometry during any approved sculpt |
| Depth | Signed distance of each run point from the chord, within the plane, positive toward the axis point O + s0·d (into the groove). Crease depth is the maximum, and the deepest point is reported |

**Baselines on the unchanged 05U RETURN:**

| Section | s0 (cm) | Chord (cm) | Depth (cm) | 75 % limit (cm) | Deepest point (cm) |
|---|---|---|---|---|---|
| A (S3 v61581) | 9.0357 | 3.086 | **0.8951** | **0.6713** | (28.797, −12.817, 168.692) |
| B (S3 v61580) | 10.4628 | 2.056 | **0.3658** | **0.2743** | (29.370, −13.468, 170.327) |

**One correction during development, disclosed.** The first measurement reported both sections AMBIGUOUS. Each section is a closed loop, and the in-region run wrapped around the loop's start index. The definition was revised before any value was recorded: the loop is rotated to start outside the region. Neither baseline was adjusted afterwards, and both are committed with the definition.

### How the stop checks work together after approval

**All of these must hold. None alone establishes natural anatomy:**
- (a) **Visual:** the notch facets no longer read at yaw 0 / 20 and pitch −45, judged on the identical-camera before/after renders. This is the author's judgement.
- (b) **Roughness:** no vertex in the extended region exceeds the source p95 roughness of 36.3°.
- (c) **Crease depth:** depth ≥ 75 % of baseline on **both** sections. This guards against flattening the natural crease, which (b) alone would reward.
- (d) **Unchanged gates:** V1-U2 and P1 / P2 exact; V2–V6c reported.
- (e) **Sliver guard (new; see §5):** no face of the 35 below its baseline minimum angle, and none below 5°.

`check_return_u2.sh` computes (b) and (e) (`u3_guards.py`), (c) (`u3_crease.py`) and (d) automatically. (a) remains the author's call.

**Guard baselines on the unchanged 05U RETURN** (`e2e_unchanged_05U_blend/guards.json`):
- **(b) FAILS at baseline, as expected.** 7 of the 365 vertices exceed 36.3°; the maximum is 47.9°. These are the notches the revision would have to clear.
- **(e) passes at baseline.** Minimum angle 6.24°.

**Check on the guards themselves.** The U1 probe's arbitrary 0.02 cm nudge correctly **trips both guards**: (b) 8 over the limit, max 50.5°; (e) face 130139 at 5.52° and face 130353 worse than baseline. So a technically ACCEPTED return can still fail the stop conditions. That is the intended separation between protection and anatomy.

## 5. What remains unresolved, disclosed

1. **The U2 layout brings an existing F1 source sliver into V4.**
   - **The face:** S3 face 130139 (F1 face 130139), with vertices 61405, 61219 and 61581, all inside the proposed 365. Angles 163.9° / **6.24°** / 9.85°; edges 1.40 / 0.55 / 0.87 cm. It is a needle triangle and part of the notch itself.
   - **Effect on the U2 baseline:** V4 shows min angle 6.24° and 1 face below 10°.
   - **What does not change:** V4 was already failing on the 8 taper edges, and that is unchanged. The FAIL rule (any face below 5°) is not triggered.
   - **Proposal:** add stop guard (e) above: the face must not get worse, and no face may fall below 5°.
   - **Scope:** this is not a scope change. All three of its vertices are already editable.
2. **The U2 baseline gate values differ from 05U only because the new set now includes the 35 source faces.**
   - V5: 142 stitch edges, 97.89 % ≤ 35°. The two 05U seam outliers, 63.7° and 59.1°, are now interior.
   - V3: 2,979 faces tested, 0 intersections.
   - **No threshold or verdict rule was changed.**
3. **Still unresolved, unwaived and outside this scope:**
   - the V6c-1 crease at θ −90°: 74.4°;
   - the V4 taper edges: 8;
   - the anterior V6c-2 failure.
4. **Real desktop fixtures are still pending.** They are required after approval, before any production stroke:
   - mask display and a stroke across the new boundary;
   - rejection of an edit just outside the new boundary, and of a moved new-ring vertex and a moved retained-ring vertex;
   - bit-identical acceptance of the unchanged fixture.

   These probes do not substitute for them.
5. **Production handoff scene not built.** `GO-05U2_sculpt_handoff.blend` (mask on the 365, face set 4, groups) is deliberately **not built**; that happens only after approval.

## 6. What Tyler would be approving

| Element | Contents |
|---|---|
| **Boundary** | The 05U2 lists, unchanged: +35 source faces (sha `483ab7fe…`) and +15 source vertices (sha `5be5a27f…`), giving 365 editable vertices (sha `0154b2be…`), a 106-vertex frozen ring (sha `91725db2…`) and 832 editable faces. A **maximum region, not a quota** |
| **Method** | Smooth brush only, low strength, along the crease; no topology change; at most three passes; stop under (a)–(e) |
| **Verification** | `check_return_u2.sh` (opt-in), with V1-U2 on P05U2 (`25ffe5ac…`). The original V1 is reported separately with the legacy diagnostic: all changes inside the 15 / 35. V2–V6c unchanged. Crease limits 0.671 / 0.274 cm. Identical-camera renders. A new package with its own manifest and a clean-extraction check |
| **Not included** | Gorrund acceptance; Stage C; the V6c-1, V4-taper or V6c-2 repairs; any change to the default 05T/05U rule for other work |

**→ STOP. VERIFICATION READINESS REVIEW / BOUNDARY AWAITING AUTHOR APPROVAL.** No production handoff change and no sculpt until Tyler approves.

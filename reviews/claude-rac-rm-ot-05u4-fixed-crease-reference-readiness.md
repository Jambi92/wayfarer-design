# RAC RM-OT-05U4: fixed crease reference and enforced readiness result (no sculpt)

**Order:** `reviews/chatgpt-rac-rm-ot-05u4-fixed-crease-reference-correction-order.md` (3ec6ad8). **Parent:** 05U3 (12723d4).
**Evidence:** `reviews/rac-rmot05u4-readiness/`. **Tools (additive, opt-in, non-production):** `tools/rac/w1/rmot05u4_drivers/`.

**Status: READINESS REVIEW / BOUNDARY AND METHOD AWAITING TYLER'S APPROVAL.**

**Nothing in production was changed:**
- the 05U RETURN, its release (`aed5711f…`) and `base.glb`;
- the production handoff, masks and face sets;
- the 35-face / 15-added-vertex boundary;
- the default 05T/05U path and the V2–V6c criteria.

No sculpt was done and no candidate was built.

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED** |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| Reconstructed skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |

## 1. The finding, confirmed

The audit is correct. `u3_crease.measure` derived s0 and the section component from the mesh being measured, and both anchors (61581, 61580) are editable. Reproduced here (`u4_test_summary.json`, T2):

| Edit | Old moving-plane section | Frozen reference |
|---|---|---|
| 61581 moved +0.02 cm along the arm axis | Section A s0 9.0357 → **9.0557** | Section A stays at **9.035685055459137** |
| 61580 moved +0.02 cm along the arm axis | Section B s0 10.4628 → **10.4828** | Section B stays at **10.462839123694403** |

The 05U3 outputs are kept as historical evidence. `u3_crease.py` and the 05U3 `check_return_u2.sh` now carry a header naming the moving-plane limitation and pointing to the replacements.

## 2. The frozen reference (`crease_reference_v1.json`, sha `c1efefde5b50316b1ff4b2edaeae3fe702dc94b9722f52ba8da7f6d490772d51`)

**Built once** by `u4_crease_ref.py build` from the pinned, unchanged 05U RETURN (`0989caf4…`), S3 (`1d503833…`) and the proposal files, whose hashes are recorded inside it. The sha is **pinned in the tool**. `measure` refuses a missing reference, a reference with a different hash, or a version mismatch. A return can never supply or regenerate its own reference.

Indices are zero-based S3; `rac_s3_vid1` is the index + 1.

| | A (anchor S3 61581) | B (anchor S3 61580) |
|---|---|---|
| Plane | (x − O)·d = **9.035685055459137** cm | **10.462839123694403** cm |
| Entry edge (frozen ring) | 60845–60886 | 61355–61522 |
| Exit edge (frozen ring) | 62052–62713 | 62713–62890 |
| Chord endpoints | (27.84237, −15.15214, 168.26580) → (29.87121, −12.95050, 169.01566) | (28.63750, −13.86225, 170.07943) → (30.59945, −13.78625, 170.68836) |
| Baseline depth | **0.8950507787872758** cm | **0.3657983545462877** cm |
| 75 % threshold | **0.6712880840904568** cm | **0.27434876590971574** cm |

The reference also stores the frame (O, d), the plane normal, the unit chord direction u, the inward normal n (toward O + s0·d), the baseline run faces and the deepest point, all at full precision. Rounded values are used for display only.

**The baselines reproduce the 05U3 values exactly** at their published precision (0.8951 / 0.6713; 0.3658 / 0.2743), with the same chord endpoints.

**One definitional point, made explicit.** The plane passes exactly through its own anchor vertex, because s0 is taken from it. 05U3 put "on the plane" with the non-negative side, implicitly. The frozen definition states this **side rule** explicitly: negative means (x − O)·d − s0 < 0, and everything else is non-negative. It is deterministic and gives the identical baseline. Treating on-plane as ambiguous would have made the baseline itself unmeasurable.

**How a return is measured:**
1. Intersect the return with the **frozen** plane.
2. Starting from the **frozen entry edge**, walk face by face through region faces.
3. Require the walk to leave through the **frozen exit edge**.
4. Require both intersection points to reproduce the frozen chord endpoints within **1e-9 cm**. This is an interpolation tolerance only; vertex protection stays bit-exact and separate.
5. Measure depth against the **frozen** chord and inward normal.

Any of the following gives an explicit **FAILED_MEASUREMENT** rather than a pass:
- a face with other than two crossing edges;
- a different exit edge;
- moved endpoints;
- a non-finite value;
- a walk longer than 200 steps;
- a missing or mismatched reference.

There is no substitute section, no moving chord and no relaxed threshold.

**Why an unexpected exit needs moved frozen geometry.** With the frozen ring bit-exact, exactly two region-boundary edges cross each frozen plane (checked at build). So a different exit cannot happen without frozen geometry moving, and fixtures T4d1 / T4d2 simulate exactly that.

## 3. The aggregate result (`u4_aggregate.py`; `rmot05u4_drivers/check_return_u2.sh`)

The corrected opt-in command writes `aggregate.json` and **exits 0 only when the numerical stop conditions pass**:
- exit 3: stop conditions NOT MET;
- exit 2: export failed.

Diagnostics, renders and hashes are kept even on failure.

| Group | Items | Treatment |
|---|---|---|
| **Mandatory** (numerical stop conditions) | Protection (U2 reintegration ACCEPTED); V1-U2; no `s_verify` FAIL verdict (the existing hard rule); crease A; crease B; roughness (b); sliver (e) | Each must be PASS. MISSING, FAIL and FAILED_MEASUREMENT all block |
| **Crease identity** | Sections A and B | Compared by **identity**: section id, anchor, s0, threshold and a fingerprint of the frozen section must all match. No unchecked `zip` of lists |
| **Reported, not waived** | V4, V6c-1, V6c-2, V6 historical | Listed separately |
| **Pending, never automated** | Author visual review; real desktop fixtures | Always shown as PENDING |

The aggregate states that ACCEPTED_FOR_VERIFICATION_U2 means protection only.

## 4. Results

**The unchanged 05U RETURN `.blend`, end to end** (`e2e_unchanged_05U_blend/`):

| Check | Result |
|---|---|
| Protection | PASS |
| V1-U2 | PASS |
| No FAIL verdict | PASS |
| Crease A | PASS, 0.8951 ≥ 0.6713 |
| Crease B | PASS, 0.3658 ≥ 0.2743 |
| Sliver (e) | PASS |
| **Roughness (b)** | **FAIL**: 7 vertices over 36.3°, the notches |
| **Numerical stop conditions** | **NOT MET, exit 3**, as expected for the unrepaired baseline |

`result.obj` and `result_verify.json` are identical to the 05U3 run (`edd7fbd0…`, `eaae3e3c…`). V4, V6c-1 and V6c-2 remain disclosed failures.

**Focused regression tests** (`u4_test_summary.json`): **15 / 15 as required.** These are synthetic edits of copies of the baseline arrays: validator fixtures only.

| Test | Result |
|---|---|
| T1 unchanged baseline | Protection PASS; A and B PASS with **exactly** the baseline depths; roughness FAIL; exit 3 |
| T2 61581 / 61580 moved +0.02 cm along the arm axis | Frozen planes, thresholds and chords **invariant**, endpoint deviation 0.0 / 0.0. Measured depths: A 0.9060 / 0.8951, B 0.3658 / 0.3658. The old tool's planes moved, as listed in §1 |
| T3 synthetic flattening in the allowed region (section A) | Protection PASS. **A FAIL at the same fixed section** (0.4563 < 0.6713, s0 unchanged). Exit 3 |
| T4a missing reference | FAILED_MEASUREMENT, nonzero |
| T4b altered reference (hash) | FAILED_MEASUREMENT, nonzero |
| T4b2 measurement made with an altered, self-pinned reference | Aggregate FAILS it by fingerprint against the pinned frozen reference |
| T4c NaN in an editable run vertex | A FAILED_MEASUREMENT, **protection REJECTED** (see the correction below), aggregate NOT MET |
| T4d1 frozen entry vertex moved 0.01 cm (simulated breach) | Measurement FAILED ("chord endpoints moved"); protection REJECTED; NOT MET |
| T4d2 frozen exit edge moved across the plane (simulated breach) | FAILED_MEASUREMENT ("run exits through 62713–62890, frozen exit is 62052–62713"); no substitute section |
| T4e gross 3 cm axial push of the run vertices (informative) | **Depth alone still passes** (A 1.58 cm), but the aggregate is NOT MET: `s_verify` FAIL verdict, roughness (b) and sliver (e) |
| T5a section B omitted | B MISSING, nonzero |
| T5b sections swapped | Both FAIL on identity, nonzero |
| T5c sections truncated | Both MISSING, nonzero |
| T5d threshold tampered in the result | FAIL, nonzero |

T4e is why depth is one of several mandatory checks, plus visual review, and is never a sufficient condition.

**Retained checks:**
- The 13 05U3 protection probes were rerun with **identical verdicts**: U0 still identical to the committed 05U result, and the default 05T path still rejects U1 (`probe_rerun_summary.json`).
- The default `s_verify` on the 05U result is still **byte-identical**.
- `t_reintegrate.py`, `t_export_blend.py`, `check_return.sh`, `s_verify.py` and the V2–V6c criteria were not changed in 05U4.

## 5. Corrections made during this order, disclosed

1. **The first fixture for "unexpected entry/exit" (a 3 cm push) did not produce one.** Its expectation was wrong, not the validator: the run still exits through the frozen edge. It was replaced by the two breach fixtures (T4d1 / T4d2) and kept as the informative T4e.
2. **The U2 protection adapter accepted a non-finite coordinate on an editable vertex.** The aggregate still failed it, through the measurement. One additive line in `u3_reintegrate.py` now rejects non-finite coordinates. All 13 probe verdicts are unchanged.

## 6. Remaining blockers

1. **Tyler's approval** of the boundary (35 faces / 15 vertices, unchanged), the method (Smooth brush along the crease, no topology change, at most three passes) and this verification contract.
2. **After approval and before any production stroke:**
   - build the production U2 handoff (mask on the 365, face set 4);
   - run the **real desktop** mask, brush and protection fixtures.
3. **Context, unresolved and not waived:** the V6c-1 crease at θ −90° (74.4°), the V4 taper edges (8) and the anterior V6c-2 failure. The disclosed source sliver (S3 face 130139, 6.24°) remains under the (e) guard.

A corrected checker does not authorize the revision.

**→ STOP FOR READINESS REVIEW AND TYLER'S BOUNDARY / METHOD APPROVAL.**

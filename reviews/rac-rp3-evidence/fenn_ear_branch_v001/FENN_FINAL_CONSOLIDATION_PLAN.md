# Fenn final consolidation — preparation plan (order bdcd6a6 §19; prepared, NOT executed)

Nothing in this note has been run. It lists what the consolidation order would do once ChatGPT selects an ear candidate (or orders one bounded refinement first). Fenn is not frozen.

## 1. Inputs that are already accepted

| Item | Record |
|---|---|
| Fenn body reference | FNL4 (configuration 1), FNF181 (configuration 2); body architecture accepted (orders 57dc328 / 2de0e28) |
| Craniofacial source | CF2 accepted (order bdcd6a6 §1–2): `FNL4-CF2`, `FNF181-CF2` in `reviews/reference-assets/manifest.json` |
| Hidden-ear identity | body PASS, face (CF2) PASS — hard reference condition (FENN_V1 RP3 status) |
| Family base | MPFB Family Base v005, frozen, unchanged (`immutable_family_and_source_hashes.txt`) |
| Facial-rig carry-forward | FENN-CF-1 (configuration-2 mouth corner), register |

## 2. Inputs still open

- **Ear candidate selection** — E1 / E2 / E3 (this gate recommends E2).
- **Bounded topology refinement**, if ChatGPT orders it before the freeze. The candidate items are listed in the gate §8:
  - upper-extension tip region;
  - cuff count-transition shear;
  - attachment-corner cells.

## 3. Consolidation steps (for the next order)

1. **Freeze the branch topology.** Publish `topology/FENN_EAR_BRANCH_TOPOLOGY_v001` (refined to v002 if a refinement is ordered) and `mapping/FENN_EAR_BRANCH_MAP_v005_v001` as the accepted Fenn ear branch of v005. Record that it is Fenn-only and not a universal elf ear.
2. **Fix the ear geometry definition** of the selected candidate. That is:
   - its parameter set (`geometry/FENN_EAR_BRANCH_GEOMETRY_v001.json`);
   - the root-frame construction and placement rule;
   - the head-scale rule (HH ÷ HH MF-M-R);
   - the fairing / untangle settings.

   Both configurations are realized by the same code. No configuration-specific edits.
3. **Final production realizations.** Proposed names:

   | Configuration | File |
   |---|---|
   | 1 | `FN_M_REF_RP3_v001.blend` |
   | 2 | `FN_F_REF_RP3_v001.blend` |

   Each is the CF2 family realization (M_v005 @ CF2 hm08) outside the branch, plus the selected ear branch. Each ships with its `_branch_map.npz` sidecar: the v005 → branch map, the weight / zone proxy rows, and the root-frame offsets of the branch vertices.
4. **Re-run the full validation set** on both final files:
   - integrity and topology audit (`audit.py` + `ear_audit.py`);
   - validator v2 D1–D6 (`--d5 --d6-native`);
   - landmarks, face rings, anatomy;
   - the RP3 deformation set (`mf_deform.py`) and the ear head / neck readiness (`ear_deform.py`);
   - the hidden-ear body + face rerun. A failure reopens the source, not the ear.
5. **Freeze checklist** (`freeze_check.py` pattern, as Sagekin):
   - geometry and file hashes;
   - PC readback hashes;
   - immutable v005 / source hashes;
   - a `FENN_RP3_FREEZE.json` record;
   - register entries: FENN-CF-1, plus any ear-rig items found by the final deformation set;
   - manifest roles updated to "frozen reference";
   - FENN_V1 RP3 status updated.
6. **Out of scope at consolidation**, unless a later order adds them: production ear rig and ear movement (FENN_V1 §15 open), creator morphs, UV / materials, LODs, UE5.

## 4. Freeze acceptance conditions to check

- 100 % quads, one component, no boundary, no non-manifold, outward normals, no self-intersection (whole mesh no worse than the v005 baseline; branch adds 0).
- Outside-branch vertices byte-identical to the CF2 family realization. Transition ring displacement bounded (currently ≤ 0.06 cm).
- Ear density ≤ 0.25 % of stature (currently 0.107–0.122 %); no branch quad aspect > 10.
- Hidden-ear CF2 identity PASS (unchanged sources).
- Static head / neck readiness: no new self-intersection, no flipped branch faces, no root inversion.

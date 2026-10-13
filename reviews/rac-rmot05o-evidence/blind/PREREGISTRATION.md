# RM-OT-05O revised neutralized structural gate — pre-registration (written before any scoring)

**Candidate under test**

| Code | Mesh |
|---|---|
| GO-RD3-REF | `final/GO-RD3-REF.obj` (= RD3c) |
| GO-RD3-LOW | `final/GO-RD3-LOW.obj` |

**Protocol (unchanged from 05K / 05N)**
- `k_blind.py` set: 8 frozen human-family controls (Marchfolk and Skarn × ref / Narrow / Broad / low), frozen Grask E3 ref + low, and the Gorrund pair under the fixed key names GO-S-ref / GO-S-low.
- Body only, with head and neck removed at this body's neck root (z 203.75; the 05N cut of 191 carried +12.75 cm into the RD3 frame). The tail is not part of the REF / LOW meshes.
- Height-normalized, front + profile, neutral grey and silhouette.
- Two independent runs with new seeds (SID GO-RD3, sets K and L), 3 fresh uninformed scorers each. Keys are retained and never shown.
- Sheets are copied to neutral directories before scoring.

**Prompt.** `tools/rac/w1/rmot05o_drivers/o_scorer_prompt_05O.md`. It keeps all 05F fields and adds `structure`, `non_structural_factors` and `primary_driver`. The old prompt and old scores are untouched.

**Decision rules.** These are fixed now and will not be changed after the results are seen. Per run, over the 3 scorers, for the Gorrund REF and LOW codes:

| # | Condition | Rule (per run) |
|---|---|---|
| C1 | REF and LOW group stably as one structural body type | ≥ 2/3 scorers put REF and LOW in one group marked stable that contains no human control and no Grask code (= f_tally G3) |
| C2 | No collapse into ordinary scaled-up Marchfolk | ≥ 2/3 scorers neither group a Marchfolk (MF-*) code with REF / LOW nor give REF or LOW class A |
| C3 | No collapse into Skarn Broad | ≥ 2/3 scorers do not group SK-brd with REF / LOW |
| C4 | Distinct from Grask | ≥ 2/3 scorers place both Grask E3 codes outside the REF / LOW group (= f_tally G4) |
| C5 | Structural reasons, not fat, muscle, posture or boxiness | For REF AND for LOW, ≥ 2/3 scorers have **all** of: `primary_driver` ∈ {axial_section_shape, joint_integration, segment_relations, load_path}; `posture_pose`, `fat`, `muscularity`, `boxiness` each rated none or minor (not major); `posture_read` false |
| C6 | Compatible with the full leonine beastfolk presentation | Not decidable blind. Assessed in the full-organism confirmation, which runs only if C1–C5 pass in both runs |

The revised structural gate PASSES only if C1–C5 pass in **both** runs.

`limb_bulk` is reported but is not part of C5, because the order's C5 names fat, muscle, posture and boxiness. Bulk is reported separately as the order requires.

**Also reported (diagnostic only).**
- The old 05F criteria G1–G7 via the unchanged `f_tally.py` (provenance).
- Per-scorer group labels, counted separately from driver / cue keyword counts.
- The full explanation texts.

No failed output will be replaced or re-run.

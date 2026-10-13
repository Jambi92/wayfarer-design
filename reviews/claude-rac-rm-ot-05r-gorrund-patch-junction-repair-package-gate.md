# RAC RM-OT-05R: Gorrund armband patch junction repair and verified package, gate report

**Order:** `reviews/chatgpt-rac-rm-ot-05r-gorrund-patch-junction-repair-package-order.md` (13fc917).
**Evidence:** `reviews/rac-rmot05r-evidence/`. **Tools:** `tools/rac/w1/rmot05r_drivers/`. **Replay:** `reviews/rac-rmot05r-evidence/REPLAY.md`.
**Commits:** the plan (before any edit) is **f1e0cb7**; the result is the commit that adds this report; the package receipt is the commit after it (see "Package").

## Status

| Item | Status |
|---|---|
| Gorrund | UNACCEPTED |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| Canon promotion | NOT PERFORMED |

There was no Rodin generation, no credits, no replacement source and no other RAC work.

## Verdict

**Junction mesh repair: FAIL.**

The planned operation (R1) and its one bounded correction (R2/R3) do not produce credible junctions. The final run, R3:
- **passes:** outside-anatomy preservation, and boundary / manifold / orientation;
- **fails:** intersections, triangle quality, seam continuity, and the no-lip/no-fold test.

All of the failures sit inside the two junction regions.

**Posterior junction: blocked by a dependency.** The fill intersects and folds against the remaining band's top-lip curl, which merges into the posterior axillary fold edge (θ −99…−96°, s 5–6). A clean junction there needs that fold edge reshaped. That is axillary-contact work, which the order prohibits, so the mesh repair stopped as ordered.

**Anterior junction: unresolved by the method.** The lip itself now ends in a rounded, tapered termination instead of B2's sharp cut end. However, new slivers and a notch appear along the junction's upper boundary, where it meets the raised band surface rising into the pectoral fold.

B2 stays the rejected baseline. No result from 05R is offered as accepted or usable anatomy.

**Package: built and verified independently.** See the "Package" section and the receipt commit.

## Author ruling recorded

- **The 05Q gate report** has an append-only addendum carrying the author's rejection of B2 and the clothing-summary correction. The 05Q scores and verdict are unchanged.
- **The v121 package** has its integrity gap disclosed in that addendum: its manifest was the repository's evidence manifest, while the package held JPEG conversions and omitted meshes.

## §2 Repair boundary (plan f1e0cb7)

**Frozen inputs.**
- base.glb `78ecfa87…a7b`, external.
- F1 working copy `17591025…53b0`.
- B2 `0ed458b7…962a`, used as the repair baseline only.
- The 05Q plan, its attempts and RD evidence, all untouched.

**Junction regions J**, in the 05Q arm-local frame:

| | Posterior J | Anterior J |
|---|---|---|
| B2 faces | 134 | 121 |
| B2 new faces in θ window | 104 (θ −110…−82°) | 74 (θ 74…102°) |
| Source extension faces | 30 (11.06 cm²): 23 garment remnant + 7 skin seam | 47 (21.93 cm²): 39 garment remnant + 8 skin seam |
| Extension bounds | s ≥ s_lo − 1.8, s ≤ fold-edge line − 0.25, r < 11 | s ≥ s_lo − 1.8, s ≤ 4.5, r < 13 |
| Topology | 1 disk, 40-edge loop (edges 0.37–2.08 cm) | 1 disk, 39-edge loop (edges 0.30–2.26 cm) |

- **Extension beyond 05Q.** The 05Q removed region R had 879 faces. The extension adds **77 source faces (33.0 cm²)**, which are named in `plan/junction_sets.npz` (`ext_post_src`, `ext_ant_src`).
- **Not touched:** the full ring, the axillary contact, the fold edges and fold surfaces, the shoulder, and any second garment.
- **Protection.** P05R is the 05Q P minus those 77 faces: 140,004 faces with coordinate sha256 `15819a65…bfa3bf0`. The 05Q P (`28d2b7ae…aa34`) is preserved as is in the 05Q evidence.
- **Supplemental tests** V6b-1..3 and the verdict rules were pre-registered in the plan.
- **Plan images:**
  - `plan/J_*_selection_on_B2.png`: labelled closes;
  - `plan/J_*_profiles_src_vs_B2.png`: cross-sections;
  - `plan/J_*_layout_topology.png`: boundary topology, colour-coded garment / skin / B2-fill.

## §3 Repair runs (all kept in `repair/R1..R3/`: mesh gz, record, labels, maps, verification, profiles)

| Run | What | Result |
|---|---|---|
| **R1** (planned operation) | Two steps. **C1 seam correction:** flip of B2 faces 140820/140812, raising min angle 9.98° → 16.8°/15.1°. **Each J:** Tutte-oriented ellipse layout → Triangle q30 → uniform bi-Laplacian solve (boundary + 1-ring fixed; garment-side rows omitted) → 3-D Lawson flips (100 + 76) | FAIL: 45 inconsistent-orientation edges, 1 non-manifold edge, 8 intersections, min angle 3.53°, 58 folds |
| **R2** (bounded correction, part 1) | Orientation taken from the removed faces' boundary half-edges; flips may not create an edge that already exists anywhere in the mesh | FAIL: non-manifold 0, but 54 inconsistent edges remain. The diagnosis traced them to the flip routine assigning winding by normal sign, which is wrong on folded triangles |
| **R3** (bounded correction, part 2; same discrete issue) | Flip winding assigned topologically | **V2 now passes.** V3/V4/V5/V6b-3 still fail inside both junctions (below) |

There was no parameter sweep and no further method search. The remaining failures are not discrete implementation faults, so the work stopped there.

## §4 Verification of R3 (`repair/R3/GO-05R-R3_verify.json`)

Every check ran on the entire patch: the 595 retained B2 faces, plus C1, plus the 563 new junction faces.

| Area | Result | Verdict |
|---|---|---|
| **Outside-anatomy preservation** (V1) | P05R coordinate sha `15819a65…` equals the plan's. Index correspondence is exact and kept source vertices are bit-identical. 0 source vertices moved on the patch boundary | **PASS** |
| **Boundary / manifold / orientation** (V2) | The 320 boundary edges map, by vertex correspondence, exactly to the source's 320. 0 non-manifold edges, 0 inconsistent orientation, 0 degenerate faces | **PASS** |
| **Intersections** (V3) | **8** new-face pairs. All are posterior: J faces against source faces 130857 / 130952, which form the remaining top-lip curl at the fold edge (θ −99…−96°, s 5–6). There are 0 pre-existing source pairs in the box | **FAIL** |
| **Triangle quality** (V4, unchanged bounds) | 1,158 new faces. Minimum angle **3.73°**; 11 faces below 10°, 1 below 5°; 68 edges outside 0.25–2.5 cm (0.113–2.417 cm). Percentiles p1/p5/p50 = 10.2°/20.3°/39.5°. **All 71 outlier faces are junction faces** (51 anterior, 20 posterior). The central patch and C1 have none | **FAIL** |
| **Seam continuity** (V5, unchanged) | 120 stitch edges; **82.5 %** ≤ 35°. Percentiles p50/p90/p95/p99/max = 10.1/74.3/126.4/156.0/161.4°. Histogram over 0–10/10–20/20–35/35–45/45–60/60–90/90–180°: 58/25/16/2/3/5/11. Every outlier is at a junction (12 posterior, 9 anterior). Source-skin reference: p95 34.8° | **FAIL** |
| **Garment-ridge removal** (V6b-1, supplemental) | Steps at θ −80/−60/−40/−20/0/20/40/60/74 are 0.147/0.094/0.091/0.162/0.235/**0.336**/**0.371**/0.097/0.144 cm; the source has 0.28–3.35 cm. The two values over 0.3 cm are in **B2's central fill**, which 05R did not touch, not in the junctions. The ridge is gone at every angle, but the strict 0.3 cm bound is missed there | **FAIL** |
| **Anatomy against garment slope** (V6b-2, supplemental) | 28.3 % of top-zone faces are steep, against a limit of 55.2 % (source skin above the band: 45.2 %) | PASS |
| **No lip or fold** (V6b-3, supplemental) | Junction-internal maximum dihedral 160.3°; **31 folds** over 90° (22 posterior, 9 anterior) | **FAIL** |
| V6 (historical, 05Q definition) | 50 ledge faces in the core (the deltoid underside, unchanged from B2); steps as in 05Q | reported only |
| **Anatomical visual credibility** | Posterior: new notches where the fill meets the lip curl and fold edge (`compare/01`, `02`, row 3). Anterior: the lip termination is rounded and reads as a deliberate end, but a zig-zag notch and slivers sit along the upper J boundary at s ≈ 4.5 (`compare/03`, `04`, row 3). The central inferred skin is unchanged from B2 | not credible at the junctions |

**Scored with the same code**, B2 gives (`baseline/B2_scored_by_r_verify_verify.json`):
- V1–V3 pass;
- V4 min angle 0.98°, 10 faces below 10°, 22 edges out of range;
- V5 84.4 %;
- 17 folds;
- verdict FAIL under the 05R rules.

R3 removes most of B2's severe end slivers but introduces new junction defects. **Neither B2 nor R3 is acceptable.**

**Dependency, reported as ordered.**
- The posterior band remnant does not end; its top lip merges into the posterior axillary fold edge. Any J that stops short of that edge leaves a curled lip on the boundary, and the fill folds or intersects against it. A clean posterior junction would therefore need the fold edge reshaped (axillary-contact work) or a wider removal of the band under the fold. Both are prohibited, so the posterior mesh repair stops.
- The anterior band likewise continues into the pectoral fold beyond θ 102°.

**Images** (`compare/`; identical camera and material; rows are source F1 / B2 / R3):

| File | Content |
|---|---|
| `01_posterior_junction_shaded.png`, `02_posterior_junction_wire_labels.png` | Posterior junction at readable size: four views including underside, shaded, then wireframe with labels |
| `03_anterior_junction_shaded.png`, `04_anterior_junction_wire_labels.png` | Anterior junction at readable size, same layout |
| `05_arm_closes_shaded.png`, `06_arm_closes_wire_labels.png` | Front / lateral / rear / two 3/4 / underside |
| `07_full_figure_context.png` | Full figure: source and R3 with labels |
| `08_posterior_junction_sections_src_B2_R3.png`, `09_anterior_junction_sections_src_B2_R3.png` | Half-plane sections at 12 angles through each junction |

The labels are: blue/amber = 05Q inferred, purple = 05R junction inferred. Nothing claims a complete armband removal; the medial band remains.

## §5 Package

The package is built by `tools/rac/w1/rmot05r_drivers/r_package.py` with its own manifest. The release filename, size, SHA-256, volume layout, clean-extraction results and delivery location are recorded in the **package receipt**: the section appended below and `reviews/rac-rmot05r-evidence/package/PACKAGE_RECEIPT.json`, both committed after the build.

The repository evidence manifests (`SHA256SUMS.txt` in each evidence folder) are kept separate and are labelled as repository manifests inside the package.

## Stop

Stopped for author visual review. There is no second garment region, full-ring or axillary separation, RD5, LOW, blind study, scaffold, canon reconciliation or production transfer. The next body route needs a separate author order.

Gorrund is UNACCEPTED, Grask E3 FROZEN, RM-OT-05 OPEN and Stage C BLOCKED. The beastfolk identity and the body / plantigrade guardrails are preserved.

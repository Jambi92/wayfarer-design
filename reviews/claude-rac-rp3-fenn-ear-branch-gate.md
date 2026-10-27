# RAC RP3 — Fenn CF2 acceptance + ear-branch prototype gate

Order: `reviews/chatgpt-rac-rp3-fenn-ear-branch-order.md` (bdcd6a6). Date: 2026-10-27.
Evidence: `reviews/rac-rp3-evidence/fenn_ear_branch_v001/`. Tools: `tools/rac/rp/fenn_rp3_v001/` (`run_earbranch.sh` reproduces every number below; `ear_summaries.py` writes the summary records).

## Verdict

## FENN EAR BRANCH PASS — E2 RECOMMENDED

One shared all-quad Fenn ear topology was built on frozen v005 and realised six times (c1 / c2 × E1 / E2 / E3) with identical vertex count, face list and branch map. Every hard technical gate in §9 passes on all six. Root integration, static head / neck readiness and the ten shape probes are clean, and hidden-ear CF2 identity is unchanged.

E2 (W1e) is the best balanced central reference. It is also the candidate that most clearly carries Fenn's "greatest lateral projection" without reading wide or horn-like.

There is one honest weakness. The T-4 angle rule (all quad corners 45–135°) is broken on 13–20 % of branch faces, against 3.4 % in the v005 ear zone it replaces. It is a cell-shape issue, not an integrity one: no aspect > 10 anywhere (max 6.93, lower than the v005 ear zone's 7.87), no slivers below 5.6°, and every deformation and probe stays clean. I recommend **one bounded topology refinement before the freeze** (§8 below). Nothing is frozen.

---

## 1. CF2 acceptance (order §1–3)

| Item | Record |
|---|---|
| Accepted central craniofacial direction | CF2 (configuration 1 `FNL4-CF2`, configuration 2 `FNF181-CF2`) |
| Versioned R-6 sources | `reviews/reference-assets/r6/FNL4-CF2_r6.npz` (sha256 `b10fb791…`), `FNF181-CF2_r6.npz` (`3674b724…`) |
| Build records | `reviews/reference-assets/builds/FNL4-CF2_build.json` (`b5b2117c…`), `FNF181-CF2_build.json` (`4c1718e7…`) |
| Manifest | `reviews/reference-assets/manifest.json`: FNL4-CF2 and FNF181-CF2 entries with provenance (parent FNL4 / FNF181 + the CF2 hm08 target overrides from order 2de0e28). The FNL4 and FNF181 roles are marked superseded for craniofacial use; both stay the accepted body references. |
| Facial-rig carry-forward | **FENN-CF-1** in `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`: configuration-2 CF2 mouth-corner expression response. A facial-rig item, not a source / topology blocker. |
| Fenn spec status | `specs/fenn/FENN_V1.md` RP3 source status block: CF2 accepted; hidden-ear body + face identity PASS is a hard reference condition. |

## 2. Shared ear topology (order §6, §8, §11)

**Base:** MPFB Family Base v005, frozen and unchanged.

| Per side | v005 ear zone (removed) | Fenn branch |
|---|---|---|
| Interior vertices | 1,181 (zone = hm08 `w_ears` > 0.5 faces) | 1,300 patch vertices |
| Faces | 1,206 | 1,325 patch faces (1,427 counting the transition-ring faces) |
| Root loop | 52 vertices | the same 52 v005 vertices, positions and family rows unchanged, valence 4 kept on all 52 |

Whole mesh: 57,842 V / 57,840 Q → **58,080 V / 58,078 Q** for every realization.

**Structure.** A sheet (front + back) and a cuff join at a 70-vertex junction ring J = 2 (n_a + j_f + K_r), with n_a = 28, j_f = 3, K_r = 4 (u1 = 16, kb = 12, ka = 12). The blocks are:

- **Bridge:** attachment line A to notch curve U. It forms the attached concha floor and tragus region.
- **Crescent F1:** the antihelix / scapha band behind the concha.
- **Upper-extension block F2:** the tip region.
- **Rim strip:** K_r rows of quads round the whole free outline (lobe front → posterior rim → tip → anterior helix). This is the helix roll.
- **Cuff:**
  - a root band that keeps every v005 root vertex at valence 4;
  - five rings of 52 / 56 / 60 / 64 / 68 vertices to J;
  - ring counts change through DP-matched ±2 transition quads with valence guards (no valence-2 vertex; no consecutive transitions).
- **Transition ring:** one bounded ring of 102 v005 vertices (both sides) outside the root loop. Its topology is unchanged; only positions are faired, displacement ≤ 0.060 cm.

**Parameterisation.** Every sheet vertex carries fixed W1e ear parameters (s along the ear, t across). Candidates and heads differ only in the parameter → geometry map (outline, relief, orientation, head scale), never in topology. This gives the later `FENN_V1` controls a place to act: length, base width, tip length / sharpness, vertical angle, sweep, projection, upper-ear curvature, lobe size / attachment.

**Root frame.** Deterministic:

- O = root-loop centroid;
- n = lateral;
- u = world up projected onto the root plane;
- b = posterior.

Head scale = HH ÷ 22.51 (c1 1.032, c2 0.993). Placement is a fixed grid search inside the root footprint.

**Sharing proof.** All six `_branch.npz` face arrays are equal element-for-element. The v005 → branch map is one file for all six (`mapping/FENN_EAR_BRANCH_MAP_v005_v001.npz`, `identical_for` lists the six). No configuration- or sex-specific topology or rule.

**Records:**
- `topology/FENN_EAR_BRANCH_TOPOLOGY_v001.{json,npz}`
- `topology/FENN_EAR_BRANCH_CUFF_CANON_v001.json` (canonical cuff band list, written once on c1 E2, read-only for all realizations)
- `mapping/FENN_EAR_BRANCH_MAP_v005_v001.{json,npz}`
- `geometry/FENN_EAR_BRANCH_GEOMETRY_v001.json` + six `*_branch_geometry.npz` (root-frame coordinates of every patch vertex, frame, transition-ring positions)

## 3. Anatomy (order §7)

The ear is a new external ear on the W1e FN-elven basis, not the human auricle stretched. The v005 auricle interior is removed; only its 52-vertex root survives.

Relief parts carried by the sheet parameters (annotated on sheet 12):

- helix;
- antihelix stem;
- superior and inferior crura;
- triangular fossa;
- concha (cymba and cavum);
- crus of helix;
- tragus;
- antitragus;
- intertragic notch;
- lobe and lobe thickening;
- upper extension.

The rim strip carries the helix roll continuously round the outline, so the point is the end of the helix and the antihelix / scapha, not an added spike. The upper-extension block rises from the whole upper ear.

**Thickness and tip.**
- The median free-ear thickness is 0.28–0.30 cm; the upper extension is thicker, ≈ 0.41 cm. The ear is not paper-thin.
- Tip in-plane angle 1 cm from the point: 37° (E1), 33° (E2), 29–31° (E3). The point is not knife-like.
- Sections are on sheet 13b.

**Measured (left side; right mirrors it):**

| | c1 E1 | c1 E2 | c1 E3 | c2 E1 | c2 E2 | c2 E3 |
|---|---|---|---|---|---|---|
| Lobe → tip chord (cm) | 7.34 | 8.17 | 8.81 | 7.06 | 7.86 | 8.47 |
| Auricle height (cm) | 7.19 | 7.83 | 8.32 | 6.91 | 7.53 | 8.00 |
| Max width (cm) | 2.89 | 3.05 | 3.18 | 2.78 | 2.93 | 3.05 |
| Auricle–body angle (°) | 43.8 | 52.1 | 57.2 | 43.8 | 52.1 | 57.2 |
| Lateral extent from root plane (cm) | 1.99 | 2.63 | 3.17 | 2.02 | 2.63 | 3.16 |
| Upper-extension axis, side view (°) | 28.4 | 32.3 | 34.3 | 28.4 | 32.3 | 34.3 |
| Sweep (cm) | 0.51 | 0.72 | 0.85 | 0.49 | 0.69 | 0.82 |
| Min root-footprint margin (cm) | 0.38 | 0.29 | 0.14 | 0.41 | 0.31 | 0.14 |

Configurations differ only through head scale (HH 23.23 vs 22.35 cm); the angles are equal. No mandatory sex dimorphism is encoded in ear size or shape.

## 4. Integrity, T-4 and density (order §9)

Values are identical in kind across all six; ranges are given (full per-realization table: `FENN_EAR_technical_summary.json`; per-realization audits: `audit/*_audit.json`).

| Check | Result (all six) |
|---|---|
| Quads | 100 % (58,078 Q) |
| Components / boundary edges / non-manifold edges / degenerate faces | 1 / 0 / 0 / 0 |
| Winding consistent, outward normals | yes |
| Self-intersection, pairs touching the branch | **0** |
| Self-intersection, whole mesh | c1 60, c2 166 = the CF2 v005 family baseline exactly (pre-existing, outside the ear) |
| Outside-branch vertices | byte-identical to the CF2 family realization |
| Ear mean edge / stature | 0.107–0.122 % (limit 0.25 %); p95 ≤ 0.20 % |
| Aspect > 10 | 0; max 6.01–6.93; > 6 on 1–5 faces per realization |
| Min corner angle | 5.6–7.0° |
| Branch vertex valence | 3: 89, 4: 2,534, 5: 77, 6: 2 (one per side at cuff ring 1, forced by the v005 root's "1 2 1" corner pattern); no valence 2 |
| Branch poles | 168 (mostly the cuff count transitions and the sheet block corners) |

**Face count vs the §9 target.** The order targets about 1.5–2× the ear-zone face count "only if needed". The branch sits at 1.10× (patch) / 1.18× (with the transition ring). The anatomy reads cleanly at this density and mean edge is under half the limit, so I did not densify. If the refinement in §8 is ordered, a modest increase in the upper extension is the natural place.

**T-4 (honest).** A face counts as a violation if any corner is outside 45–135°.

| Realization | Violations / 2,854 branch faces | front | back | rim | cuff | transition |
|---|---|---|---|---|---|---|
| c1 E1 | 363 (12.7 %) | 106 | 88 | 9 | 144 | 16 |
| c1 E2 | 450 (15.8 %) | 150 | 132 | 10 | 142 | 16 |
| c1 E3 | 543 (19.0 %) | 204 | 168 | 9 | 146 | 16 |
| c2 E1 | 368 (12.9 %) | 106 | 88 | 9 | 149 | 16 |
| c2 E2 | 465 (16.3 %) | 150 | 132 | 10 | 157 | 16 |
| c2 E3 | 561 (19.7 %) | 204 | 168 | 9 | 164 | 16 |
| v005 ear zone (replaced) | 82 / 2,412 (3.4 %) | | | | | |

The sheet violations sit in the upper-extension kite: rhombic cells that shear as the tip narrows, which is why they grow from E1 to E3. The cuff violations sit at the ±2 count transitions and the attachment corners. The rim is almost clean. Heatmap: sheet 14.

**Verdict for §9:** the hard requirements pass on all six; T-4 is reported, and it is the refinement item.

## 5. Root integration (order §12)

- **Root loop:** 52 v005 vertices, positions and family rows unchanged, valence 4 on every root vertex both sides.
- **Root crease (dihedral across the root loop):**
  - mean 29–33° against v005 27–29°;
  - max 60–74° on five realizations against v005 67–71°;
  - c1 E1 left reaches 89.5° at one posterior-lip edge (sheet 9).
- **Transition ring:** 102 v005 vertices. Mean displacement ≈ 0.03 cm; max 0.053–0.060 cm.
- **Cuff skin against the hidden-ear CF2 skull** (v005 ear zone collapsed harmonically onto its root): ring 1 / ring 2 / ring 3 from the root are in `audit/FENN_EAR_root_deviation_by_ring.json`:

  | Realization | Ring 1 mean / max (cm) | Ring 2 mean / max | Ring 3 mean / max | Whole cuff max |
  |---|---|---|---|---|
  | c1 E1 | 0.09 / 0.20 | 0.14 / 0.30 | 0.17 / 0.35 | 0.52 |
  | c1 E2 | 0.10 / 0.24 | 0.16 / 0.36 | 0.20 / 0.45 | 0.60 |
  | c1 E3 | 0.10 / 0.26 | 0.17 / 0.40 | 0.22 / 0.51 | 0.68 |
  | c2 E1 | 0.11 / 0.22 | 0.16 / 0.32 | 0.19 / 0.39 | 0.62 |
  | c2 E2 | 0.12 / 0.25 | 0.18 / 0.39 | 0.22 / 0.49 | 0.67 |
  | c2 E3 | 0.12 / 0.27 | 0.18 / 0.43 | 0.24 / 0.54 | 0.74 |

  The skin rises progressively towards the junction ring, as it must to carry the attachment. There is no burial and no floating root.
- **Ear-to-head clearance** (free ear vs the head outside the branch): min 0.32–0.50 cm; 0 vertices below 0.2 cm.
- **Seam:** none. No boundary edge exists, and the transition ring is faired into the temple / scalp. Sheets 9 and 16 show it.

## 6. Static deformation readiness (order §13)

`ear_deform.py` poses the CF2 native rig with the branch carried by its smoothed weight proxy (head weight ≥ 0.96 on the free ear). Poses:

- neck flexion 30 and extension 30;
- head yaw ±45;
- head pitch ±20;
- head roll ±20.

| Check, all 8 poses × 6 realizations | Result |
|---|---|
| New self-intersections touching the branch | 0 |
| Flipped branch faces | 0 |
| Root-band inverted faces | 0 |
| Root-loop edge strain | equal to the v005 root strain in the same pose |
| Ear to neck / shoulder clearance | ≥ 3.16 cm in every pose |

Sheet 20 shows the poses.

**Ear-shape probes.** These are geometry-only; same topology, c1 E2 base, not production morphs:

- projection ±10°;
- tilt ±8°;
- sweep ±0.6;
- length ±10 %;
- tip blunt / sharp.

| Probe | Change | Self-int. (branch) | Aspect max | T-4 viol. | Clearance min (cm) | Chord (cm) | Angle (°) | Upper axis (°) | Tip (°) |
|---|---|---|---|---|---|---|---|---|---|
| proj_m10 | proj=40 | 0 | 5.79 | 443 | 0.39 | 8.17 | 42.2 | 35.7 | 33.0 |
| proj_p10 | proj=60 | 0 | 5.84 | 443 | 0.42 | 8.16 | 62.0 | 28.4 | 33.0 |
| tilt_m8 | tilt=24 | 0 | 5.81 | 510 | 0.40 | 8.45 | 51.7 | 25.9 | 32.7 |
| tilt_p8 | tilt=40 | 0 | 6.13 | 404 | 0.40 | 7.84 | 52.3 | 39.6 | 33.0 |
| sweep_m06 | sweep=1.0 | 0 | 5.90 | 438 | 0.36 | 8.25 | 51.6 | 27.1 | 34.1 |
| sweep_p06 | sweep=2.2 | 0 | 6.26 | 522 | 0.42 | 8.11 | 52.4 | 37.8 | 29.7 |
| len_m10 | L=7.74 | 0 | 6.52 | 364 | 0.49 | 7.29 | 52.0 | 33.4 | 36.1 |
| len_p10 | L=9.46 | 0 | 6.93 | 583 | 0.31 | 9.04 | 52.1 | 31.5 | 30.5 |
| tip_blunt | taper_ex=0.7 | 0 | 5.88 | 356 | 0.38 | 8.17 | 51.6 | 32.2 | 51.9 |
| tip_sharp | taper_ex=1.5 | 0 | 6.14 | 568 | 0.41 | 8.16 | 52.6 | 32.5 | 18.4 |

All ten probes use the base topology unchanged, are closed and manifold, and add 0 self-intersections. Aspect max is 6.93; clearance min is 0.31 cm. Each probe moves its own measure in the intended direction. T-4 rises with length and tip sharpness: the same tip-block weakness as §4.

Static readiness: **acceptable**.

## 7. Hidden-ear identity and craniofacial regression (order §4, §14)

Record: `FENN_EAR_hidden_ear_CF2_regression.json`.

- **Sources:** both CF2 R-6 sources are unchanged (hash proof: `immutable_family_and_source_hashes.txt`).
- **Descriptor landmarks:** every hm08 landmark used by the CF2 descriptors maps to a family vertex outside the branch. It is byte-identical in all six realizations.
- **Outside the branch:** every vertex is byte-identical to the CF2 family realization. The transition ring moves ≤ 0.060 cm.
- **Result:** hidden-ear CF2 body and face identity **remains PASS**.
- **Visible-ear read** (sheets 17, 19):
  - **E1** reads restrained and closest to a generic elf.
  - **E2** reads Fenn: strong lateral projection, upper extension rising from the whole ear. It does not read childlike, horn-like, animal-like, or as "human with pasted-on ears".
  - **E3** is the strongest. In front view it approaches cartoon-wide at central-population scale, and its attachment uses the full root footprint (margin 0.14 cm).

## 8. Candidate scoring and recommendation (order §17)

Scores: `FENN_EAR_candidate_scoring.json`. Each of the 10 criteria is scored 1–5; dimensions alone were not decisive.

| | E1 | E2 | E3 |
|---|---|---|---|
| Total / 50 | 40 | **42** | 36 |

- **E2 is recommended.**
  - It realizes the W1e FN-elven ear: c1 chord 8.2 cm, auricle–body angle 52°, lateral extent 2.6 cm.
  - Its upper-extension axis (32°) equals the target tilt.
  - It has a comfortable root margin (0.29–0.31 cm).
  - It reads clearly Fenn without caricature.
- **E1 is valid but under-expresses Fenn.** Of the three, it is the least distinct from Aelari / Vael.
- **E3 is technically valid but carries the costs.** It has the most T-4 outliers, a root margin at the footprint limit, and a borderline-wide front silhouette.

The aesthetic trade-off is not balanced enough to need author selection.

**Refinement recommended before the freeze (bounded; topology only, same root interface):**

1. **Upper-extension block:** replace the kite with a row layout that follows the taper, to remove the rhombic tip cells. This is the main T-4 cost.
2. **Cuff count transitions:** spread the shear of the ±2 transition quads, especially rings 1–2 near the posterior lip.
3. **Attachment corners:** improve the cells where the bridge meets the cuff at the two ends of line A (min angle 5.6–7°).
4. **Lobe-cusp knob:** remove the small cuff knob behind the lobe cusp (sheets 8 and 9).

None of these blocks a candidate selection. They would change the topology version (v001 → v002) and so must happen before the freeze, not after.

## 9. Elven-family firewall (order §15)

The branch is Fenn-only. No Aelari or Vael geometry was authored and no universal elf ear is declared. Reuse note: `FENN_EAR_ELF_REUSE_NOTE.md`. It covers:

- the root interface and cuff;
- the junction-ring and block structure;
- helix / antihelix row topology;
- the tip-support block and its known weakness.

## 10. Consolidation (order §19)

The consolidation is prepared, not executed: `FENN_FINAL_CONSOLIDATION_PLAN.md`. It covers:

- the accepted inputs;
- the open selection / refinement;
- final realization naming (`FN_M_REF_RP3_v001`, `FN_F_REF_RP3_v001`);
- the full re-validation set;
- the freeze checklist.

## 11. Review files

Review prototypes are on E: `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Fenn/RP3/ear_branch/`:

- `FN_{M,F}_REF_RP3_cf2_ear{E1,E2,E3}_proto_v001.blend`;
- the branch map;
- the sheet-17 pair.

The PC read-back hashes match (`production/pc_readback_sha256.txt`). The blends use the production frame, carry an `ear_branch` vertex group, and are marked "prototype — not accepted, not frozen". Branch faces carry placeholder UVs (UV is out of scope).

## 12. Answers to order §20

| Question | Answer |
|---|---|
| Is CF2 now recorded as the accepted Fenn central craniofacial direction? | **Yes.** Manifest FNL4-CF2 / FNF181-CF2 with versioned R-6 + build records; FENN_V1 RP3 status. |
| Is the CF2 facial-rig carry-forward recorded? | **Yes.** FENN-CF-1 (configuration-2 mouth corner) in the carry-forward register. |
| Was one shared Fenn ear topology built? | **Yes.** `FENN_EAR_BRANCH_TOPOLOGY_v001`: 1,300 V / 1,325 Q per side on the v005 52-vertex root. |
| Do c1/c2 and E1/E2/E3 share it exactly? | **Yes.** Six realizations have identical vertex count, face list and branch map. Geometry differs only by the root-frame construction and parameters. |
| Does it contain the required external-ear anatomy rather than a stretched human ear? | **Yes.** All §7 systems are present; the human auricle interior is removed; the point emerges from the helix / antihelix / upper extension. |
| Do integrity, T-4 and density pass? | **Integrity and density: pass** (100 % quads, manifold, 0 branch self-intersections, 0.107–0.122 % of stature, aspect ≤ 6.93). **T-4: reported, weaker than v005** (13–20 % vs 3.4 %); refinement item 1–3. |
| Is root integration clean? | **Yes.** Root unchanged at valence 4, transition ≤ 0.060 cm, no seam, no burial or floating. One c1 E1 posterior-lip crease edge is at 89.5° (v005 71°). |
| Is static deformation-readiness acceptable? | **Yes.** 8 poses × 6 realizations: 0 new self-intersections, 0 flips, 0 root inversions. The 10 shape probes are clean on the same topology. |
| Does hidden-ear identity remain PASS? | **Yes.** Sources unchanged; all descriptor landmarks are outside the branch and byte-identical. |
| Which E candidate is recommended? | **E2** (W1e central). |
| Is any topology refinement still needed? | **Recommended, bounded:** tip block, cuff transitions, attachment corners, lobe-cusp knob. Not blocking selection; must precede the freeze. |
| Is Fenn ready for final consolidation after author selection? | **Yes, after the bounded refinement** (or directly, if ChatGPT accepts the T-4 level as is). The plan is prepared; nothing is frozen. |

## 13. Committed items (order §20)

1. This gate.
2. Topology definition: `topology/`.
3. Mapping: `mapping/`.
4. Geometry for E1/E2/E3 × c1/c2: `geometry/`, plus build records `build/` and measurements `measure/`.
5. Sidecars / manifests:
   - `reviews/reference-assets/manifest.json`, `r6/FNL4-CF2_r6.npz`, `r6/FNF181-CF2_r6.npz`, `builds/*CF2*`;
   - `production/*.json`, `pc_readback_sha256.txt`.
6. Integrity audit: `audit/*_audit.json`.
7. T-4 / aspect audit: `audit/*_audit.json` (`T4`) and sheet 14.
8. Density audit: `audit/*_audit.json` (`density`) and sheet 15.
9. Root deviation: `audit/FENN_EAR_root_deviation_by_ring.json` and sheet 16.
10. Static deformation readiness: `deform/` and `probes/FENN_EAR_shape_probes.json`.
11. CF2 regression: `FENN_EAR_hidden_ear_CF2_regression.json`.
12. Visual sheets: `sheets/` (20 types × c1/c2, sheet 18 shared, sections 13b).
13. Scoring: `FENN_EAR_candidate_scoring.json`.
14. Consolidation note: `FENN_FINAL_CONSOLIDATION_PLAN.md`.
15. Immutable hashes: `immutable_family_and_source_hashes.txt`.
16. `specs/STATUS.md` (narrow).
17. `reviews/claude-session-handoff.md`.

Also committed: the carry-forward register, `specs/fenn/FENN_V1.md` status block, the elf reuse note, the technical summary and the tools.

**Stop rules (§21) honored:** v005 unchanged; Fenn not frozen; no Aelari / Vael / Halvren work; no universal elf ear; no ear rig, creator morphs, UV / materials, LODs or UE5.

**STOP FOR CHATGPT REVIEW.**

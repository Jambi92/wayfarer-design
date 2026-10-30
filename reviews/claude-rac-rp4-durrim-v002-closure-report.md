# Claude Gate — RAC RP4 Durrim Compact-Branch Revision / Closure (v002)

**Order:** `reviews/chatgpt-rac-rp4-durrim-compact-branch-revision-closure-order.md` (8080f9f; reviewed 372fe20)
**Date:** 2026-10-30
**Evidence:** `reviews/rac-rp4-evidence/durrim/v002/`
**Tools:** `tools/rac/rp/durrim_rp4_v002/` (search / optimisation scripts used to find the definition: `search/`)

## Result

**DURRIM RP4 COMPACT BRANCH PASS — READY FOR AUTHOR ACCEPTANCE / FREEZE**

All 13 criteria of §16 are met. Nothing is frozen. Two items are raised for author attention:
- A blind reader did not see Durrim 152 as structurally distinct from Marchfolk 152. This concerns the accepted source anatomy, which v002 does not change (§9).
- There is a small documented T-4 angle residual in the branch zones. It is equal in count to the v005 faces it replaces, with 0 quads over 4:1 (§4).

| # | Criterion | Result |
|---|---|---|
| 1 | c2 central anchor remains accepted | DUF137C-NAT regenerated from its committed build; r6 unchanged (immutables) |
| 2 | thumb MCP passes all Durrim bodies | `thumb_mcp_l / r` PASS on 122 / 137 / 152 / c2 (3 / 3 / 3 / 4 rings); 0 crease poles |
| 3 | jaw–neck neck-station failure eliminated | neck PASS on all five bodies. Moved poles sit 1.0 h / 1.39 h / 1.79 h above the band on 122 / 137 / 152; loops unchanged |
| 4 | c1 / c2 69 / 69 | DU137C **69 / 69**, DUF137C **69 / 69** |
| 5 | 122 / 152 branch diagnostics 69 / 69 | DU122C **69 / 69**, DU152C **69 / 69** (MF152 diagnostic also 69 / 69) |
| 6 | T-1…T-7 | T-1 / T-2 / T-3 / T-7 PASS; T-6 max drift 0.0008 mm; T-5 = 69 / 69 + density within §8; T-4 below |
| 7 | T-4 materially better than v001 | branch quads > 4:1: **0** (max 3.90) vs v001 100–105 (max 9.3). Branch T-4 flags 10 vs 10 in the v005 faces replaced. Body totals unchanged |
| 8 | adult-read / hidden presentation | blind review Q1 adult PASS, Q2 no nose / jaw crutch PASS, Q3 same population PASS. Artefacts flagged are present in v005 too (§9) |
| 9 | DU-P4 intact | sources byte-identical to the accepted ones; Part A values carried (pilot gate §2) |
| 10 | 152 cm equal-height identity | production topology does not change the source surface (T-1 ≤ 1.5 mm max, p95 0.17 mm). Board D. Blind visual read noted in §9 |
| 11 | no new topology-class deformation failure | c1: all 18 poses identical to v005. c2: +4 / +8 self-contact pairs at wrist_flex60 / hip_flex90 are the same v005 contacts counted on finer faces (0 unmatched). 122 / 152 thumb and neck poses identical |
| 12 | deterministic and reusable mapping | identical face list and identical S (structure and weights) on 122 / 137 / 152 / c2; two rebuilds bit-identical |
| 13 | frozen races / v005 untouched | 26 / 26 immutable inputs unchanged vs 8080f9f, including all 10 freeze records |

## 1. Answers to the order's questions

| Question | Answer |
|---|---|
| Thumb MCP passes on every Durrim body? | **Yes.** The counted rings are B, T1 and T2 (plus A on c2), all valence-4 closed loops inside the stature-scaled window and radius. |
| T-4 better than v001? | **Yes, materially.** The thumb zone has 496 quads: 8 angle flags (40.8–140.2°) and 0 aspect > 4 (max 3.90). The 200 v005 quads it replaces had 10 angle flags (31.4–149.1°). v001 added 100–105 quads over 4:1. |
| Neck crease pole removed with margin? | **Yes.** Pole t / h after reroute: 122 +1.50, 137 +1.89, 152 +2.29, c2 / MF152 > 3 h. All are ≥ 1 h outside the ±0.5 h band. |
| Jaw / chin / neck shape unchanged? | **Yes.** No vertex is added. Re-placed vertices lie on each body's own v005 surface (measured ≤ 0.04 mm, the triangulation residual). Neck length and circumference are untouched. |
| c1 / c2 identical topology? | **Yes.** One face hash `a791797f…` and one S on all bodies. The branch carries no Durrim shape. |
| Any other station affected? | **Yes, and it was diagnosed and fixed (§3):** on c2 the R-6 hand hangs inside the hip station's pole cylinder. |

## 2. MPFB_COMPACT_BRANCH_v002

**Definition:** `branch/MPFB_COMPACT_BRANCH_v002.json` (sha256 `aef4a30b…`).

**Map:** V = S · V_v005 and M = S · M_v005, with ≤ 4 non-zeros per S row.

**Counts:** 58,138 V / 58,136 Q, against v005's 57,842 / 57,840. Thumb zones add +296 V; the neck adds no vertices.

### 2.1 Thumb MCP — two-direction local densification

**Where.** Per thumb, six aligned v005 rings:
- **P (= Z−1):** the thenar transition ring, which already carries three v005 5-poles;
- **Z:** the MCP seed ring;
- **A, B, C, D.**

**Fine region Z…C.**
- Columns are split ×2 circumferentially.
- Two new rings T1 / T2 are inserted in B→C, so that strip is ×3 axially.
- The fine strips are regular grids with no poles.

**Transitions.** Only 2:1 fan templates (3 quads per column pair), placed in the full-height P→Z and C→D strips. 5-poles go on P / D and 3-poles on Z / C; none of these rings is counted.

**Why there and not in A→B:**
- The thumb_mcp crease axis is oblique to the rings, so on 122 cm part of A and of B lies inside the crease band. B must therefore stay a pole-free fine ring.
- Four wide columns (0.65–1.1 cm) next to the MCP make every parent strip about 3:1. A 2:1 transition squeezed into a part of one strip goes past 4:1. That is exactly the v001 failure.

**Phases and seams.**
- Left fan centres sit on even lines, right fan centres on odd lines. This avoids the existing P 5-poles (left 3 / 9 / 19, right 4 / 10 / 14).
- Both thumb UV seams (left 5 / 13, right 0 / 8) stay on kept rung edges.

**Unsplit sector.** Columns left 11–12 / right 0–1 stay ×1. This is the c2 hip slab sector (§3). Those columns' B→C sub-quads are about 0.36 × 0.11 cm (≈ 3.2:1).

**Placement.**
- One shared set of (v005 face, s, u) per vertex, found by a joint relaxation on DU137C / DUF137C / DU122C / DU152C.
- What it minimises: the T-4 hinge, cos² and aspect terms.
- Constraints it enforces:
  - counted-ring window and radius on every body;
  - every transition pole outside the thumb_mcp crease band;
  - every transition pole outside every non-digit station band;
  - a fold guard on every quad normal.
- Seams: v005 corners on seams are fixed, and T1 / T2 seam vertices slide only along the seam edge.

**UVs.**
- Each branch corner takes the bilinear parent-face UV in its own quad's chart.
- There are 0 UV fold-overs.
- Each seam line gains exactly its expected extra edges.

### 2.2 Jaw–neck reroute — "pole moved + one 3/5 pair added"

**Topology.**
- Four quad edge rotations per side; the right side is the L/R mirror. No vertex is added.
- Result: the submandibular 5-pole 5299 (11904) becomes the trio 735 (5) / 5290 (5) / 5300 (3) (right: 7455 / 11896 / 11905), two to four rows higher.
- It was found by a breadth-first search over distinct local states (depth ≤ 5). It is the smallest solution with three poles and ≥ 1 h margin on 137 / 152.
- It goes up, not down: a downward move would put c2 / MF152 into their bands.

**Placement.** The rotated faces and two rings around them are re-placed on the v005 surface by the same joint relaxation, with a pole-offset penalty.

## 3. The c2 hip-station finding (§8 "true topology or validator geometry")

**What happened.** The first v002 build gave c2 67 / 69 with `hip_l / hip_r FAIL_CREASE_POLE`.

**Cause.**
- In the c2 R-6 stance the hand hangs beside the hip.
- The hip station's pole search covers a 9.5 cm radius around the thigh axis and a ±0.5 h axial slab. It counts every pole there; D3 ownership scoping applies only to digit stations.
- So three new thumb transition poles (P_12, Z_12, Z_14 and their mirrors) were counted as hip crease poles.
- This is **validator geometry, not hip topology**. I did not change the validator.

**Fix.** I made the branch avoid the slab without broadening it:
- The two columns inside the slab sector stay unsplit, so they have no transition and no poles.
- The one remaining nearby 3-pole (Z_14 / Z_19) is held at ≥ 55 % of its rung toward A, outside the hip radius. On c2, pr / Rp = 1.003 left and 1.002 right; the validator test is pr ≤ Rp.
- No c1 body has a thumb pole within any hip radius.

**After the fix:** c2 69 / 69, and every other body is unchanged.

**Author note:** the c2 hip margin is thin (0.2–0.3 % beyond Rp). It is robust for these frozen sources but stance-dependent.

## 4. Quality (T-4) in the branch zones — `DU2_gates.json`

| Zone (per Durrim body) | v002 quads | angle flags | > 4:1 | v005 faces replaced: angle / > 4:1 |
|---|---|---|---|---|
| thumbs | 496 | 8 (40.8–140.2°) | 0 (max 3.90) | 200: 10 (31.4–149.1°) / 0 |
| neck | 136 | 2 (43.4–135.2°) | 0 (max 3.80) | 136: 0 / 0 |
| **total** | 632 | **10** | **0** | 336: **10** / 0 |

**Body totals (aspect / angle), v005 → v002:** identical on 122 / 137 / 152 / c2. MF152 diagnostic: +3 / +3.

**Neck residual:**
- 2 quads (one per side) next to the new 3-pole, with angles 43.4–45 / 135.1–135.2°.
- They straddle the submandibular ridge: their corner angles sum to about 270°, so the quads are folded across the jaw line.
- On-surface relaxation cannot bring them inside the band. I tested two other BFS topologies; both ended with the same residual.
- They are recorded here, are outside the crease band, and are deformation-clean.

## 5. Validator and gates per body (`validator/`, `audit/`, `anatomy/`, `contact/`)

| Body | v005 firm | v002 firm | thumb_mcp l / r | neck | self-x (rest) | contact new | T-1 / T-2 / T-3 / T-7 | T-6 max |
|---|---|---|---|---|---|---|---|---|
| DU122C | 67 | **69** | PASS 3 / 3 | PASS (4) | 160 = 160 | 0 | PASS | 0.0008 mm |
| DU137C | 66 | **69** | PASS 3 / 3 | PASS (7) | 122 = 122 | 0 | PASS | 0.0007 mm |
| DU152C | 66 | **69** | PASS 3 / 3 | PASS (9) | 74 = 74 | 0 | PASS | 0.0006 mm |
| DUF137C | 67 | **69** | PASS 4 / 4 | PASS (13) | 128 = 128 | 0 | PASS | 0.0006 mm |
| MF152 (diag.) | 69 | **69** | PASS 4 / 4 | PASS (10) | 124 = 124 | 0 | PASS | 0.0008 mm |

- **Integrity:** 1 component, 0 boundary / non-manifold / degenerate on all bodies; 100 % quads.
- **Surface deviation of re-placed vertices from the v005 surface:** neck ≤ 0.04 mm, thumb ≤ 0.23 mm. This is the residual from triangulating the bilinear reference; it is 0 on the bilinear surface by construction.

## 6. Density (`density/`, `v001_compare/`) — mean % of stature

| Body | face / hand / foot zones: v005 → v001 → v002 | palm sub-zone (contains the thumb base) mean / p95 |
|---|---|---|
| DU122C | 0.154 / 0.157 / 0.207 → 0.154 / 0.158 / 0.207 → 0.154 / 0.156 / 0.207 | 0.312 / 0.531 → 0.298 / 0.529 → **0.278 / 0.502** |
| DU137C | 0.149 / 0.155 / 0.206 → = → 0.149 / 0.154 / 0.206 | 0.307 / 0.524 → 0.293 / 0.521 → **0.274 / 0.495** |
| DU152C | 0.145 / 0.153 / 0.206 → (n/a) → 0.145 / 0.152 / 0.206 | 0.303 / 0.517 → **0.270 / 0.489** |
| DUF137C | 0.147 / 0.142 / 0.196 → = → 0.147 / 0.141 / 0.196 | 0.285 / 0.486 → 0.272 / 0.483 → **0.254 / 0.459** |

- All zone means stay within the §8 ceilings (0.25 / 0.3 / 0.3).
- MCP / IP / tip, wrist transition, face sub-zones and feet are unchanged.
- v002 densifies the thumb-base sub-zone more than v001, with no T-4 penalty.

## 7. Deformation (`deformation/`; board F)

**Suite.** 18 standard poses on c1 and c2, compared across native source, v005 and v002.

**c1.** Every pose is identical to v005:
- self-intersections, folds and flips are equal in total and in the branch zones;
- the neck poses are 0 / 0 / 0.

**c2.** Identical except two poses:
- wrist_flex60 shows +4 self-contact pairs and hip_flex90 +8 (folds and flips equal);
- every one of these v002 pairs maps to an existing v005 contact pair at the same place (0 unmatched);
- they are the same thumb–palm and thumb–thigh contacts counted on finer faces.

**122 / 152.** fist, thumb opposition, neck_flex30 and neck_rot45 are identical to v005.

**Conclusion.** No grip or fist collapse, no neck failure, and no new topology class.

## 8. Production candidates (not frozen) — `production/`

| Candidate | Source | blend sha256 | geometry hash | read-back |
|---|---|---|---|---|
| DU_M_REF_RP4_v001 | DU137C-NAT c1 | `55679333…` | `a6ff9218…` | faces equal; max \|dV\| 6e-8 m; UVMap; 1 component; 0 boundary |
| DU_F_REF_RP4_v001 | DUF137C-NAT c2 | `797b06d7…` | see record | idem |

**Contents of each candidate:**
- Production frame (m, Z up, faces −Y, origin = pelvis root on the ground).
- Vertex groups `compact_branch_thumb` / `compact_branch_neck`.
- Sidecar `_branch_map.npz` holding the exact M = S · M_v005 rows, S itself, the v005 → production identity map and the branch face lists.

**Location and status:**
- The `.blend` files are committed in `production/`, because this cloud session cannot reach E:. They also rebuild bit-identically from the definition with `run_v2_prod.sh`.
- Freeze-candidate record: `DURRIM_RP4_FREEZE_CANDIDATE.json`.

## 9. Adult read, hidden presentation, 152 cm, and the blind review

**Board E** (hidden presentation) shows bald, clean-shaven, neutral faces with the external ear (hm08 w_ears > 0.05) harmonically flattened, the same mask as the accepted hidden-ear gates; a low relief remains.

The independent blind reviewer, who had not seen the work, returned:

| # | Question | Verdict |
|---|---|---|
| Q1 | Adult read | **PASS** (soft, close to androgynous) |
| Q2 | No big-nose / heavy-jaw crutch | **PASS** |
| Q3 | Same population across c1 / c2 | **PASS** |
| Q4 | Head–neck integration | **BORDERLINE**: the jaw–neck line is clean, but c1's shadowed neck side looks lumpy |
| Q5 | 152 cm Durrim vs Marchfolk reads as structurally distinct | **FAIL**: they read near-identical at a glance |
| Q6 | Artefacts | mouth-corner notch, head-outline faceting, lumpy neck shading, hollow eyes, ear relief; **none at the thumb** |

**Were the Q4 / Q6 items caused by v002?** No.
- I rendered v005 and v002 of the same body under identical cameras (`sheets/DU2_H_…`, `DU2_v005_v002_render_diff.json`).
- The differences are sub-pixel silhouette edges plus a faint shading change under the jaw where the reroute is (≤ 275 px > 8 grey levels).
- The neck shading, mouth seam, faceting and eye openings are identical in v005. They are source / family-base properties, and the eyes are absent by design.

**Q5 is an author-attention item, not a v002 blocker.**
- The accepted W2H1 sources pass the 19 / 19 numeric equal-height directions (pilot gate §2): thoracic breadth +10–11 %, depth +13–14 %, neck −14 %, wrist +29 %, among others.
- In neutral full-body clay at board scale, those differences did not read to a naive viewer.
- v002 does not change this either way: the source surface is preserved (T-1).
- If the author wants a stronger visual read, that is a source / creator art-direction decision outside this order.

## 10. Reusability assessment (§14) — technical only, nothing propagated

**General: candidates to test later on Pipkin / Cogling.**
- The fine-band-plus-full-height-transition architecture:
  - ×2 circumferential and ×3 axial inside a band of pole-free counted rings;
  - 2:1 fans only in full-height strips on uncounted rings;
  - a phase chosen to avoid existing poles and UV seams.
- The (v005 face, s, u) definition format: S rows ≤ 4 non-zeros, M = S · M_v005, seam-aware UVs, and a deterministic face-slot policy.
- The joint multi-body on-surface relaxation with validator-derived penalties (ring windows, crease bands of all stations).

**Not general: must be rediagnosed per race.**
- The specific placement parameters: they are tuned on the Durrim family's hands.
- The unsplit sector: it exists only because c2's R-6 hand hangs in the hip slab.
- Whether ×2 / ×3 is enough: this depends on the race's hand allometry.

**Durrim-specific: must not propagate.**
- The jaw–neck reroute. It is tied to where Durrim's short neck puts the neck-station band relative to the v005 submandibular pole.
- Other races should not receive it unless their own validator shows the same failure.

## 11. Immutables and provenance

- `immutable_hashes_v002.txt`: 26 / 26 unchanged vs 8080f9f and vs the pilot record. Covered: Durrim builds and r6, DUF137C, MF-M-R / MF-F-R, the v005 freeze, map and core, and all 10 `*_FREEZE.json`.
- v005 was not re-read from E:. Propagation used the committed v005 face / UV core with the frozen hm08 map (hash = frozen value); `propagate_core.py` is identical in maths to `propagate.py`.
- The cloud v005 realization reproduces the committed v005 audit field-for-field (2,009 / 2,009). The committed unbranched validators reproduce byte-identically.

## 12. Not done (STOP)

- No freeze.
- No Pipkin / Cogling / Saurin.
- No rig, UE5, creator, hair, clothing or materials.
- No validator change.
- No change to accepted Durrim biology.

**STOP FOR CHATGPT REVIEW.**

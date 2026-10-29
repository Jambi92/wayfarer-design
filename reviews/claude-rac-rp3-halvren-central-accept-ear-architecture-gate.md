# RAC RP3 — Halvren central acceptance + mixed external-ear architecture gate

Order: `reviews/chatgpt-rac-rp3-halvren-central-accept-ear-architecture-order.md` (e9008f2, 2026-10-29).
Evidence: `reviews/rac-rp3-evidence/halvren_rp3_central_accept_ear/` (`hpb_validation/`, `ear/`, `sheets/` HVE_01..26).
Tools:
- `tools/rac/rp/halvren_rp3_v001/`: `hv_defs.py` (PELVIS HP-B), `hv_hpb_validation.py`, `hv_ear.sh`, `hv_ear_domains.py`, `hv_ear_summary.py`, `hv_ear_audit.py`, `hv_ear_collect.py`, `hv_ear_probes.sh`, `hv_ear_probe_eval.py`, `hv_ear_quick.py`, `hv_ear_sheets.py`;
- `tools/rac/rp/fenn_rp3_v001/ear_branch_lib.py`: additive Halvren candidates HVEAR2 + root geometry HR1; see §2.4 for the one shared-code change.

Workspace: `/tmp/claude-0/rt/hv/{hpe,hpv,ear}`.

## RESULT

## HALVREN EAR TOPOLOGY NEEDS DEDICATED BRANCH

- **Central body / face / pelvis: accepted and validated.**
  - HB2 + HF2 + HP-B is versioned as `HVC1-HB2HF2-HPB` / `HVF178-HB2HF2-HPB`.
  - HP-B passes every §6 check: 69 / 69, no hip / leg regression, still distinct from Fenn / Aelari / Vael, one-α firewall pass.
- **Ear architecture.**
  - The Halvren mixed-ear parameter architecture HVEAR2 is authored as a domain mosaic.
  - Its authored domains pass the ear arithmetic firewall: one-α R² ≤ 0.44 for every HE.
- **Topology.**
  - The shared elf engineering ear topology (Fenn v002 sheet; root variants rigid Fenn cuff / Vael RI3 / a bounded Halvren HR1 root geometry) cannot realise that architecture.
  - (a) **Its human end is already half-way to the elves.** Marchfolk ear parameters realised on it measure at median t 0.50–0.53 between the Marchfolk auricle and the elf mean.
  - (b) **The firewall fails as realised.** The human-family domains (projection, lobe, concha) do not survive realisation. The measured HE2 / HE3 become one-α blends (R² 0.93 / 0.93), failing the ear arithmetic firewall.
  - (c) **HE1 cannot be human-sized.** The shortest clean length is still about 25 % longer than the Marchfolk auricle.
  - (d) **The root holds on one head only.** Every root geometry fails technically somewhere in the HE1–HE3 range: the rigid cuff rebuilds the layered-ear mound; Vael RI3 gives slivers at human-forward lengths; HR1 is clean on c1 but fails on c2 for HE1 / HE2 / HE3.
- **Order rule applied.** §21: "Do not compromise biology to preserve reuse." A dedicated Halvren ear topology branch is required. Proposal: `reviews/claude-rac-rp3-halvren-ear-topology-branch-proposal.md` (not executed).
- **Not done.** No HE ear is recommended for the central production anchor yet. Nothing is frozen.

## Answers (§27)

| Question | Answer |
|---|---|
| HB2 and HF2 formally accepted as the central body / face pair? | **Yes.** Recorded (§1); the pair is unchanged. |
| HP-B formally accepted as the central pelvis direction? | **Yes.** Versioned sources `HVC1-HB2HF2-HPB` / `HVF178-HB2HF2-HPB` (manifest: "accepted for ear work; not final / not frozen"). §6 validation all PASS. |
| HP-B distinct from human and frozen elf pelves? | **Yes.** Pelvic vertical / crest +3.3 % vs Marchfolk (−6.8 % vs Aelari, +2.9 % vs Fenn); crest −2.5 %; AP depth −1.5 %. The only near-overlap is Vael pelvic vertical / crest (−0.4 %); the complete relation differs (body material vs VA 13 / 8 metrics). Leg share +0.34 % (no hip-height hack). |
| Can one ear topology support human-forward through elf-forward mixed Halvren? | **No.** See the RESULT section and §2. |
| If not, is a dedicated Halvren ear branch required? | **Yes.** Proposal committed, not executed. |
| HE1 / HE2 / HE3 domain-specific rather than one strength slider? | **As authored: yes.** Projection, lobe, base width and concha are non-monotone or flat across HE1 → HE3, and the design one-α R² ≤ 0.44. **As realised on the shared topology: no.** Measured domains move in near lockstep; only root_line is non-monotone. |
| HE1 avoids "human ear + point"? | **Yes.** It is a blunt, shouldered upper helix, not a tip. Eight non-tip domains depart from Marchfolk, and the one-α fit R² is ≤ 0.41. But it is about 25 % larger than the Marchfolk auricle (topology floor). |
| HE2 avoids arithmetic midpoint behaviour? | **Authored: yes** (R² ≤ 0.38). **Realised: no** (measured R² 0.93 MF→AE, α 0.72). |
| HE3 avoids duplicating Fenn / Aelari / Vael? | **Realised: no.** It differs from Aelari in only 3 of 11 domains (one-α R² 0.93). The topology elf end coincides with the source elves. |
| Fenn / Aelari / Vael diagnostics remain Halvren? | **Fenn-influenced: yes** (differs from Fenn in 4 domains, from Aelari in 9). **Aelari- and Vael-influenced: no** (3 domains from their source; one-α R² 0.91 / 0.95). **Human-forward diagnostic: yes.** |
| Ear reads as one auricle in every case? | **With HR1, yes** (anterior attachment p90 ≤ 0.19 cm, junction ≤ 0.31 cm; neutral clay HVE_09). **Rigid Fenn cuff: no** (layered mound 0.45–0.50 cm). **Vael RI3 root: borderline** (0.27–0.39 cm). |
| Ear arithmetic firewall passes? | **No, as realised** (HE2 / HE3 / two diagnostics fail). The authored architecture passes. The failure is a topology representation limit (§3). |
| Body / face / ear mosaic coherent? | **Yes where technically clean.** HB2+HF1 + HE3 (stronger ear, subtler face): clean, reads as one organism. HB2+HF3 + HE1: one 3.9° cuff sliver (HR1 fragility); visually coherent. |
| Technical gates pass? | **c1: HE1 / HE2 / HE3 and all four diagnostics pass** (100 % quads, 1 component, 0 boundary / non-manifold / degenerate, outward, 0 branch self-intersections, aspect < 10, min corner ≥ 10°, density ≤ 0.105 %, root valence 4 × 52, 8 head / neck poses clean). **c2: HE1 / HE2 / HE3 fail** (slivers, self-intersections at the lower postauricular cuff corner). Body / face / pelvis regression: outside-branch byte-identical in every case; 69 / 69 retained. |
| Which HE candidate is recommended for the central production anchor? | **None yet.** HE2 (HVEAR2) is the leading authored central geometry. It should be re-realised on the dedicated branch and re-audited before selection. |
| Ready for final consolidation after author review? | **No.** First the dedicated ear branch, then HE re-realisation and the ear firewall. §26 consolidation plan below (prepared, conditional). |

## 1. Central source acceptance + HP-B validation (§1–§6; `hpb_validation/HV_HPB_validation.json`)

- **Versioning.**
  - `hv_defs.py` adds `PELVIS['HP-B']` = pelvis bone [1.0, 1.02, 1.0] + `hip-scale-horiz-decr` 0.05; tag suffix `-HPB`.
  - Built with `build_hb.sh HB2HF2-HPB`. The independent build equals the body / face order's HP-B diagnostic build (dV 0, faces identical, both configurations).
  - Records are in `reviews/reference-assets`. Manifest entries `HVC1-HB2HF2-HPB` / `HVF178-HB2HF2-HPB`: "central … source candidate ACCEPTED FOR EAR WORK; not final / not frozen". The HB2HF2 ancestry entries are kept.
- **HP-B vs pelvis held (HP-A), c1 / c2:**

| | c1 | c2 |
|---|---|---|
| Validator D1–D6 | 69 / 69 | 69 / 69 |
| Technical pass (exact v005, integrity, regen, T-1/2/3/7, density, face rings) | yes | yes |
| Material vs Marchfolk (of 31) | 10 → 10 | 11 → 11 |
| Body groups with signal | 7 → 7 | 7 → 7 |
| One-α best R² (pass < 0.8) | 0.61 → 0.69 (MF-AE) | 0.70 → 0.73 (SG-AE) |
| Distinct from FN / AE / VA (material) | 17 / 13 / 13 | 12 / 12 / 8 |
| Face regions departing / anti-beauty | 3 / 7, unchanged | 3 / 7, unchanged |
| Worst flip excess vs MF v005 | 1 → 1 | 0 → 0 |
| Worst selfx excess | 22 → 20 | 17 → 19 |
| New contact class | 0 | 0 |

- **Hip / knee poses.**
  - Self-intersections hip-flex 90: 60 → 61; knee 90: 45 → 45; knee 140: 157 → 157.
  - Flips are unchanged.
  - **No new hip / leg alignment problem.** Leg share +0.34 % vs MF; no hip-joint-height term.
- **Stop rule (§6).** No coupled failure, so the ear work proceeded.

## 2. Ear topology audit (§9, §10, §21; `ear/HV_ear_summary.json` → `topology_audit`; sheet HVE_26)

One connectivity was tested: the Fenn v002 sheet with the 52-vertex v005 root interface. The cuff connectivity is either Fenn v002 (five rings) or Vael RI3 (six rings, read-only reuse).

Each geometry was realised with three root geometries:
- the **rigid Fenn cuff**;
- the **exact Vael RI3 root** (concha seat −0.30, skin cuff);
- **HR1**, a bounded Halvren root geometry: concha seat −0.50, corner fade 1.2, lobe lift 0.70. It is geometry only, with RI3 connectivity.

All builds are on c1 with the deformation guard.

| Geometry (c1) | Rigid Fenn cuff | Vael RI3 root | Halvren HR1 |
|---|---|---|---|
| Marchfolk ear parameters (human-forward bound) | clean · **mound 0.45** | **FAIL** (8 selfx, degenerate, 7.0°) | rest: 3.3° sliver (with the Halvren attachment) |
| HE1 (L 6.3) | clean · **mound 0.50** | **FAIL** (4.6°, poses) | **clean** · mound 0.06 |
| HE2 | clean · **mound 0.50** | clean · mound 0.35 | **clean** · mound 0.12 |
| HE3 | clean · **mound 0.50** | clean · mound 0.39 | **clean** · mound 0.18 |
| elf-forward bound (L 9.4, projection 42°) | clean · **mound 0.33** | **FAIL** (3.9°) | rest: **FAIL** (22 selfx, aspect 28.6) |
| HE1 / HE2 / HE3 on **c2** | — | — | **FAIL / FAIL / FAIL** (0.0° / 3.0° / 7.7°; selfx 20 / 0 / 22) |
| HE1 on HB2+HF3 head | — | — | **FAIL** (3.9°) |

(mound = anterior cuff height above the skin, p90, cm; one-auricle limit 0.20.)

- **Rigid Fenn cuff.** It reproduces the raised cuff mound that made the Vael prototype read as one ear layered on another: a human-ear-sized perimeter in front of the concha.
  - Frozen Fenn / Aelari parameters on this head show the same mound (0.30 / 0.44). Their long leaves hide it; Halvren's human-family concha does not.
- **Vael RI3 root.** It removes the mound, but fails at human-forward lengths and at the elf-forward bound.
- **HR1.** It is clean across HE1–HE3 on c1 only. On c2 and on the HF3 head the lower postauricular cuff corner (right side) collapses. The failures are non-monotone in length, e.g. HE1 at L 6.2 without the lobe lift: 10 self-intersections.
- **Length floor.**
  - Below L ≈ 6.2 the front sheet compresses: aspect > 10, slivers.
  - At the floor the free auricle measures 0.30 HH. The Marchfolk auricle measures 0.24 HH on the same head and rule.
- **Root interface (§10).**
  - The 52-vertex interface *is* the v005 human ear root loop, so it is anatomically right for human-influenced ears. Keep it.
  - The problem is the cuff / sheet between the root and the auricle, not the interface.
- **Determinism.** HE2 rebuilt independently: dV 0 on c1 and c2.
  - One face topology for every HE realisation on c1 and c2 (sha recorded).
- **Shared-code change (verified safe).** `ear_branch_lib.ear_sheet` now receives the candidate's merged geometry. Before this, candidate-level root keys (`tauA`, `phi0`, `lift_*`) were silently ignored.
  - Frozen Fenn E2 and Vael VA-E2-RI3 were rebuilt on the Halvren head after the change: dV 0, faces identical.
  - Every frozen candidate's geometry keys equal the defaults in those fields.

## 3. Ear arithmetic-average firewall + ear-only firewall (§17, §18; `ear/HV_ear_domains.json`, `ear/HV_ear_audit.json`; sheets HVE_16, HVE_17)

**Method.**
- **Common head and frame.** One common head (HB2+HF2+HP-B c1): face and pigment neutral, no hair. One root frame: the v005 root loop plus the hidden-ear skull field.
- **One measuring rule** for the Marchfolk family human auricle and for every branch ear, with frozen Fenn E2, Aelari AE-E2 and Vael VA-E2-RI3 realised with their frozen parameters on the same head. The frozen meshes are untouched.
- **11 domains, as ordered:**
  - length / HH;
  - base width / length;
  - auricle–body projection;
  - upward extension;
  - backward inclination;
  - tip angle;
  - lobe fraction;
  - root-line relation;
  - concha depth;
  - tragus / cavum level;
  - helix fullness.
- **Normalisation:** per domain by the pooled standard deviation of the four sources.
- **Fail rule:** one α explains an HE with R² ≥ 0.8 over ≥ 6 domains.

| | Authored (design) best R² | Realised (measured) best R² | Realised nearest | Domains differing from FN / AE / VA |
|---|---|---|---|---|
| HE1 | 0.30 | **0.41** | MF | 9 / 9 / 8 |
| HE2 | 0.38 | **0.93** (MF-AE α 0.72) | VA | 7 / 7 / 8 |
| HE3 | 0.44 | **0.93** (MF-AE α 0.87) | VA | 5 / **3** / 8 |
| Fenn-influenced | 0.42 | 0.88 (MF-FN) | FN | 4 / 9 / 7 |
| Aelari-influenced | 0.44 | 0.91 (MF-AE) | VA | 4 / **3** / 7 |
| Vael-influenced | 0.53 | 0.95 (MF-VA) | VA | 9 / 8 / **3** |
| Human-forward | 0.14 | 0.41 | MF | 10 / 8 / 10 |
| *control: Marchfolk parameters on the topology* | — | — | — | median t **0.50 / 0.53** (rigid / RI3) |
| *control: elf-forward bound* | — | 0.96 / 0.97 | AE | — |

**Why it fails.** The authored architecture is a mosaic. HE2 has human-family projection (23°), vertical angle (16°), concha (0.86), tragus, helix roll and lobe (0.20), with an elven early long upper extension, a broad Vael-class base and sweep. But on the shared topology:
- **Upward extension is fully elf-like even for Marchfolk parameters** (t 0.98).
- **Projection does not stay human.** Every branch ear measures 22–29° against the Marchfolk auricle's 6°, so the authored human projection realises at t 0.5–0.6.
- **Concha depth is shallower than every source** for HE2 / HE3 (t 1.2–1.6; HE1 0.83): the sheet has no human cavum bowl.
- **The lobe does not stay human.** It realises toward the elf value (HE2 t 0.40) despite the full human lobe parameter.

So the measured Halvren family collapses onto one Marchfolk→elf line. The HE1 → HE2 → HE3 domains move in lockstep, and the human-family share of the mosaic cannot be expressed. This is the representation failure the order warns about. It is not fixable by re-authoring parameters: the HVEAR1 → HVEAR2 revision moved the design R² from 0.87 to 0.38, but the measured R² went from 0.87 to 0.93.

**First pass, recorded.** HVEAR1 had HE2 at t 0.25–0.8 on every domain (design R² 0.87, measured R² 0.87). It was revised to HVEAR2 in this order and is recorded in `ear_branch_lib.py`.

## 4. HE definitions (HVEAR2; `ear_branch_lib.CAND`; §11–§14)

Tendency columns (one source per domain, none in lockstep):

| | Root / attachment | Base width | Concha / tragus | Lobe | Projection | Upper extension | Tip / taper | Sweep / vertical |
|---|---|---|---|---|---|---|---|---|
| **HE1** human-forward | HR1, human flare (φ0 30, τA 10) | 1.82 (≥ MF / FN / AE) | human (0.84 / 0.30) | human-plus (0.19) | human (23) | late, short (L 6.3, start 0.58) | blunt apex out of a human helix shoulder (ex 0.80, shoulder 0.12) | mild (tilt 17, sweep 0.65) |
| **HE2** balanced | HR1 (φ0 33, τA 12) | broad, Vael-class (2.00) | human (0.86 / 0.31) | full human (0.20) | human (23) | early, moderate length (L 7.8, start 0.36) | restrained, shouldered (ex 1.10, shoulder 0.06) | human vertical (tilt 16), elf sweep (1.4) |
| **HE3** elf-forward | HR1 (φ0 34) | 1.88 | human (0.86 / 0.31) | full human (0.20) | human (22) | long, early (L 8.8, start 0.30) | sharper (ex 1.25) | strongest sweep (1.9), tilt 22 |
| Fenn-influenced | as HE2 | as HE2 | human | human | **42** | as HE2 | as HE2 | sweep 1.6 |
| Aelari-influenced | as HE2 | as HE2 | human | human | human | **L 8.8, start 0.28, ex 0.95** | long taper | tilt **26** |
| Vael-influenced | as HE2 | **2.10** | human | human | human | short taper (start 0.45, ex 1.30) | | tilt **34**, sweep 1.5 |
| Human-forward | human flare | human (1.76) | human | human (0.19) | human (22) | L 6.7, late | blunt | mild |

- **No human↔elf slider.** There is no vertex interpolation of source ears and no 0.5 parameter averaging.
- **Halvren-only `halvren` taper law.** The helix shoulder `sh` carries human-family helix fullness into the apex; with sh = 0 it is the continuous law exactly.

## 5. Whole-ear anatomy, one auricle, mosaic, readiness, probes, regression

- **Anatomy (§15; HVE_11).** Every prototype carries all of these:
  - helix, antihelix stem, superior / inferior crura, triangular fossa;
  - cymba, cavum, crus of helix;
  - tragus, antitragus, intertragic notch;
  - lobe, and the upper extension.

  The relief system is the frozen W1e law. The point emerges from the whole upper ear, not a pasted tip: the continuous taper starts at s 0.30–0.58 of the length, carried by the helix shoulder.
- **One auricle (§20; HVE_09, HVE_12, HVE_15).**
  - With HR1 the anterior attachment is at skin level: mound p90 0.06 / 0.12 / 0.18 cm, junction 0.15 / 0.23 / 0.31 cm, concha floor 0.50 cm below the hidden-ear skull. There is no nested ear and no outer shell.
  - The rigid-cuff variants read as layered; see §2.
- **Mosaic (§19; HVE_22).**
  - HE1 / HE2 / HE3 on HB2+HF2+HP-B: c1 clean.
  - HB2+HF1 + HE3: clean, one organism (the stronger ear sits on the subtler face).
  - HB2+HF3 + HE1: visually coherent, one 3.9° cuff sliver.
  - Face and ear strengths need not match.
- **Readiness (§22; HVE_23).** HE2, HE1, HE3 and all diagnostics on c1 have 0 contacts / 0 flips / 0 root inversions over the 8 head / neck poses: flex / ext 30, yaw ±45, pitch ±20, roll ±20. On c2 HE1 and HE3 do not (10 / 7 events).
- **Probes (§22; `ear/HV_ear_probes_HE2.json`; HVE_24).** HE2 on c1 got 14 probes, a −/+ pair each for length ±10 %, projection ±8°, sweep ±0.4, tilt ±6°, base width ±8 %, tip exponent ×0.78 / ×1.28 and lobe ±0.04. All share one topology.
  - **11 / 14 are technically clean.** Slivers appear at lobe −0.04 (8.3°), sweep −0.4 (4.9°) and base width +8 % (1.8°), all on the same right-side cuff face (58925) that fails HE2 on c2.
  - **11 / 14 move their own domain in the right direction:** length, projection, sweep +, tilt, tip and base width.
  - **Lobe size does not move the measured lobe at all** (0.00 SD): it is not an independent control on this topology.
  - **Coupling.** Length drags the lobe fraction (±0.9–1.0 SD) and tilt drags the sweep curvature (+1.9 SD).
  - **Most controls do move independently, but not lobe size, and the probe range is not technically clean** — more evidence for the dedicated branch.
- **Regression (§23; HVE_25).**
  - Outside the ear branch every vertex is byte-identical to the HB2+HF2+HP-B family realisation for every HE item.
  - So HB2 / HF2 / HP-B are unchanged; the hidden-ear body / face pass (§1) and 69 / 69 stand.
  - No contact / deformation failure outside the branch.

## 6. Final-consolidation preparation (§26) — CONDITIONAL, not executed

The ear architecture did not pass, so this is the plan for **after** the dedicated branch passes. Inputs fixed now:
- HB2 body;
- HF2 face;
- HP-B pelvis (`HVC1-HB2HF2-HPB` / `HVF178-HB2HF2-HPB`).

Checklist:
1. Dedicated Halvren ear branch per the proposal, realised for HE1 / HE2 / HE3 + diagnostics on c1 / c2. Acceptance: §21 gates at both bounds and every probe; one auricle; concha ≥ Marchfolk at the human end.
2. Ear arithmetic firewall, measured one-α R² < 0.8 for every HE.
3. Ear-only firewall and source-duplicate checks.
4. Author selects the central HE. HE2 (HVEAR2) is the leading candidate; other HE ears remain valid Halvren phenotypes.
5. Ear topology / map record: v005 → Halvren branch map, canon read-only.
6. Family topology elsewhere = v005 (byte-identical outside the branch).
7. Body / face / pelvis firewalls re-confirmed: §1 numbers; hidden-ear identity.
8. Mosaic re-test.
9. D1–D6 69 / 69 both configurations.
10. Deformation carry-forwards: the elf-family selfx excess at the knee / hip, as in §1.
11. Production blends `HV_{M,F}_REF_RP3_v001` and E: read-back.
12. Freeze record + immutable hashes.

## 7. Immutable frozen-source hashes

`ear/immutable_hashes.txt`:
- v005 family base blend + hm08 map;
- Fenn / Aelari / Vael freeze records;
- the Fenn v002 cuff canon and the Vael cuff canon (reused read-only);
- the HB2HF2-HPB sources.

All frozen files are unchanged by this order.

## STOP

STOP FOR CHATGPT REVIEW.
- No Halvren freeze, no RP4.
- Fenn / Aelari / Vael and v005 are untouched.
- No ancestry slider, no genealogy percentages, no creator UI.
- No ear rigging, UV, LOD or UE5 work.

# RAC RM-OT-05 — roster stature / world-scale author gate

**Order:** `reviews/chatgpt-rac-rm-uf-05-final-ruling-rm-ot-05-order.md`
**Evidence:** `reviews/rac-rmot05-evidence/` — `register.json` (register, min / ref / max measurements, allometry check) and 9 sheets.
**Drivers:** `tools/rac/w1/rmot05_drivers/ot05_lineup.py`, `ot05_tables.py`.
**Scope:** RM-UF-05 writeback, plus a roster-scale record built from existing accepted canon and reference anatomy. No engine metrics, no new stature bounds, no distributions.

---

## 0. Verdicts

| Item | Verdict |
|---|---|
| **RM-UF-05 writeback** | **COMPLETE** (commit bee7fd3) |
| **RM-UF-05 architecture** | **FINAL CLOSED** — UFCA_V1 §17.1. Roster-wide numeric calibration: PARTIAL / DEFERRED. |
| **Option B diagnostic calibration recorded** | **YES** — current diagnostic calibration, N = 256. |
| **Option B numbers canonized as universal biology** | **NO** |
| **Saurin horizontal IOD UFCA conflict resolved** | **YES** — fixed in UFCA §4 / §12 / §19, the SAURIN slot-routing note and SAURIN §267.2. |
| **Saurin horizontal IOD state** | **Bound / DIR, −8 % … +3 %** (whole orbital complex moves together; +14.9 % is not a creator interval) |
| **Saurin vertical / AP placement** | **Bound-locked** |
| **Stale Tier-G pointers repaired** | **YES** — UFCA-06 §2.G: MF L253 / L261, SG L370, AE L479, VA L505, HV L381, DU L233, GR L739 / L740, GO L713 / L716. |
| **Explicit Skarn Tier-G row added** | **YES** — anti-stereotype L294–296; relationship-aware randomization L282–284; SK-12; W3C overlap validators; C1R is a reference, never a template. |
| **13-race stature register complete** | **YES** (§1) |
| **Current demonstrated roster minimum** | **Cogling, 76.0 cm** — `CG76-NAT` (W2H native route); COGLING L54 / COG-BODY-02. |
| **Current demonstrated roster maximum** | **Gorrund, 251.0 cm** — `GO251` (W2D, macro 0.972); GORRUND L29–31. The spec calls 251 the "current world-validation upper stature, never a permanent maximum". |
| **World envelope ≈ 76–251 cm confirmed** | **YES** — matches COGLING L54, GORRUND L29 and PIPKIN L119. The upper end is labelled by canon as a current validation stature, not a permanent maximum. |
| **Per-race RM-OT-05 status** | **SUPPORTED:** Marchfolk, Skarn, Fenn, Aelari, Vael, Durrim, Grask, Gorrund, Pipkin, Saurin. **CONSTRAINED:** Sagekin (configuration-2 boundaries not built), Cogling (76 cm head marginal). **NOT FULLY DEMONSTRATABLE:** Halvren (ancestry-conditional outer reach). No CONTRADICTION class. |
| **Contradictions found** | **No genuine canon contradiction.** Bookkeeping items in §5: Gorrund reference 229 vs ARM 230.9; one stale Halvren status pointer (fixed); stale registry / config notes in historical evidence. |
| **Frequency assumptions introduced** | **NONE** — frequency OPEN for all 13. |
| **Invented stature bounds introduced** | **NONE** |
| **Uniform-scale construction used** | **NO** (§3) |
| **Next author decisions required** | §6 |

---

## 1. Roster stature register

Authority order (PROJECT_RULES L79–87): race spec, then universal decisions, then later author resolutions, which supersede earlier text at the same level.

- **Sex and height:** R-SEX — hard bounds are open to either sex, and sex never forces stature.
- **Stature control:** UCCA L108–114 — stature is DIR inside the canon envelope, never uniform scaling.
- **Frequency:** OPEN for every race (UCCA §6.6). No stature distribution is authored anywhere. Saurin §263 centres are tissue tendencies and carry no stature shift.

| Race | Hard min | Hard max | Reference / central | Sex-related rule | Conditional reach | Controlling source | Demonstration | Frequency |
|---|---|---|---|---|---|---|---|---|
| Marchfolk | 147 | 203 | 173 (MF-M-R 173.14; MF-F-R 172.99) | No sex-specific restriction. Both configurations built at both bounds: identical | none | MARCHFOLK L62–64, L23, L249; W2A | min / ref / max, both configurations | OPEN |
| Skarn | 183 | 229 | 208 (SK 208.01; central face C1R) | Ordinary human configurations; bounds identical and demonstrated. Configuration 2 at 229 = macro 1.0 + native extension | none | SKARN L11–13; W2B / W2B1; W2C1 | min / ref / max, both configurations | OPEN |
| Sagekin | 152 | 208 | 178 (SG 177.99) | Both configurations allowed. **Configuration-2 boundaries not built** | none | SAGEKIN L70–72; W2E | configuration 1 min / ref / max | OPEN |
| Fenn | 157 | 211 | 181 (FNL4 181.16) | One configuration | none | FENN L22–24; W2F | min / ref / max | OPEN |
| Aelari | 168 | 221 | 190 (AEL1 190.01) | One configuration | none | AELARI L25–27; W2F (168 on the native route, R2) | min / ref / max | OPEN |
| Vael | 157 | 203 | 178 (VAL4 178.00) | One configuration | none | VAEL L15–17; W2F | min / ref / max | OPEN |
| Halvren | central envelope 152 (outer bound > 147, H-5) | central envelope 213 (outer bound < 229, H-5) | 178 (HVC1 177.73, diagnostic anchor) | Follows sources (AD-R22) | **Ancestry-conditional outer reach: 147.2 (Marchfolk-supported, bound-limited), 228.8 (Skarn-supported), 221.0 (Aelari-supported, source ceiling)**; H-1 … H-6; AD-W3A-1 … 4 | HALVREN L86–88, L481, L493–509; UCCA L296; W2G; W3A1 FINAL ACCEPT | central min / ref / max + 3 reach bodies | OPEN (tails are minority outcomes, H-6; conditional frequency is a named dependency) |
| Durrim | 122 | 152 | 137 (DU137C, D1 pelvis rebuild) | One configuration, no shift | none | DURRIM L15–19; W2H / W2H1 | min / ref / max | OPEN ("distribution left for later") |
| Grask | 198 | 239 | 218 (GR218R 217.99) | One configuration | none | GRASK L15–17; W2C | min / ref / max | OPEN |
| Gorrund | 208 | 251 | **229 nominal (R-2, GORRUND L29); accepted ARM GOREF 230.9** | One configuration | 251 is the current world-validation upper stature, "never a permanent maximum" | GORRUND L27–31; W1i / W1j / W2D | min (208.27) / ref / max; GO229 also exists | OPEN |
| Pipkin | 91 | 122 | 107 (PK-NAT) | One configuration | none | PIPKIN L25–27, L119; W2H | min / ref / max | OPEN |
| Cogling | 76 | 107 | 91 (CGJ7 90.99) | One configuration (sex via AC-U2) | none | COGLING L50–56 (provisional), L63, L1589; W2H | min / ref / max (76 cm head marginal) | OPEN |
| Saurin | 168 | 208 (tail excluded) | 188 (W2 reference 187.88) | No sex shift, no sex-specific bound (§263) | none (tail is coupled by §256, not by stature) | SAURIN L64–68, L3587–3593, §263; W2I D1 regional route; W2I6 | min / ref / max (W2 plan, regional route) | OPEN |

**No race's interval midpoint is treated as an average.**

The bounds are the accepted W2 boundaries. Most race specs still label them "first-pass / provisional"; only Halvren and Saurin carry a W2 stature writeback block (§6, decision 4).

## 2. Common-scale validation and measurements

### 2.1 Sheets

All sheets use one ground plane (u = 0), one orthographic scale (4 px / cm), the matched neutral reference stance, neutral grey material, and a centimetre grid.

| Sheet | Content |
|---|---|
| `ot05_A_reference_lineup.jpg` and `ot05_A2_reference_lineup_profile.jpg` | All 13 reference bodies, front and profile, ordered by stature. Saurin's tail extends behind the body; the tail is excluded from stature. |
| `ot05_B_minimum_lineup.jpg` | 13 minimum realizations. Halvren is shown twice: the central-envelope 152 and the Marchfolk-supported reach 147.2. |
| `ot05_C_maximum_lineup.jpg` | 13 maximum realizations. Halvren central 213 and the Skarn-supported reach 228.8 are both shown. |
| `ot05_D_world_extremes.jpg` | Cogling 76 / Marchfolk 173 reference / Gorrund 251, front and profile. |
| `ot05_E1_mf_hv_sk.jpg` | Marchfolk / Halvren / Skarn at matched 190 and 203. |
| `ot05_E2_elves_halvren.jpg` | Fenn / Aelari / Vael / Halvren at matched 190 and 203. |
| `ot05_E3_short_races.jpg` | Cogling / Pipkin at 91 and 107; Pipkin / Durrim at 122. |
| `ot05_E4_large_races.jpg` | Skarn / Grask / Gorrund at matched 208 and 229. |

- No body is outside its race's accepted interval.
- No matched body is fabricated: every one is an accepted W2 build or a C1R face layer on an accepted Skarn body.
- Halvren 190 / 203 use the accepted W2G central-envelope bodies (HV190M / HV203M).

### 2.2 Measurements (existing accepted conventions; `register.json`)

Head-height share is the R-6 head height ÷ stature (W1c / W2 convention). For Saurin the figure is head length ÷ H (SAURIN §258).

| Race | Min (cm / head share) | Reference | Max | Head share falls with stature? |
|---|---|---|---|---|
| Marchfolk | 147.0 / 0.1372 | 173.1 / 0.1300 | 203.0 / 0.1241 | yes |
| Skarn | 183.0 / 0.1300 | 208.0 / 0.1252 | 229.0 / 0.1215 | yes |
| Sagekin | 152.0 / 0.1350 | 178.0 / 0.1282 | 208.0 / 0.1226 | yes |
| Fenn | 157.0 / 0.1329 | 181.2 / 0.1267 | 211.0 / 0.1214 | yes |
| Aelari | 168.0 / 0.1361 | 190.0 / 0.1314 | 221.0 / 0.1255 | yes |
| Vael | 157.0 / 0.1339 | 178.0 / 0.1292 | 203.0 / 0.1244 | yes |
| Halvren (central) | 152.0 / 0.1356 | 177.7 / 0.1287 | 213.0 / 0.1223 | yes |
| Halvren (reach) | 147.2 / 0.1368 (MF-supported) | — | 228.8 / 0.1208 (SK-supported); 221.0 / 0.1213 (AE-supported) | yes |
| Durrim | 122.0 / 0.1468 | 137.0 / 0.1421 | 152.0 / 0.1379 | yes |
| Grask | 198.0 / 0.1271 | 218.0 / 0.1237 | 239.0 / 0.1203 | yes |
| Gorrund | 208.3 / 0.1189 | 230.9 / 0.1158 | 251.0 / 0.1130 | yes |
| Pipkin | 91.0 / 0.1590 | 107.0 / 0.1514 | 122.0 / 0.1459 | yes |
| Cogling | 76.0 / 0.1435 | 91.0 / 0.1298 | 107.0 / 0.1187 | yes (head height clamped to 11–13 cm absolute, L1589) |
| Saurin (head length ÷ H) | 168.0 / 0.1751 | 187.9 / 0.1696 | 208.0 / 0.1648 | yes, inside the §258 bound 0.156–0.184 |

**Further accepted ratios are in `register.json`:** torso share, leg share, arm share, shoulder breadth share and thorax depth ÷ breadth for MPFB bodies; lower trunk, shoulder, thorax depth ÷ width, tail % and foot ÷ H for Saurin. Notable values:
- Saurin thorax depth ÷ width is constant at 0.880 and tail is 64.3–64.9 % H. Both are §256.9 isometric, as required.
- Grask leg share 0.557–0.569 stays above Marchfolk's 0.530–0.546 across both ranges.

## 3. No uniform-scale shortcut

**Every body above was built on its accepted race route.** The routes:
- **MPFB height macro** (re-solved; Gorrund to 0.972, Grask to 0.935).
- **Native short-adult route** for Durrim / Pipkin / Cogling at every stature, and for the native-route minima of Marchfolk, Sagekin, Fenn, Aelari, Vael and Halvren. This route is one length factor, with girth k^0.654, hands k^0.842, feet k^0.942 and head k^0.688. That is not whole-body scaling, so head, hand, foot and girth respond allometrically.
- **Skarn configuration 2 at 229:** macro 1.0 plus the accepted native extension.
- **Saurin W2 regional route:** `sa_finish.build_f` on the canonical W2 plan; isometric tail per §256.9.

**Evidence that the allometry is real:** head-height share falls with stature inside **every** race (§2.2), which uniform scaling cannot produce. Frame bodies keep axial lengths (Saurin thorax depth ÷ width constant; MPFB frames are bone-scale width changes only).

**Excluded:**
- the historical Saurin Part 7 / §263 uniform 168 / 208 cross-check (W2I D1: history only);
- the Iteration-3 uniform-scaled references (not measurement truth).

No extreme needed **NOT DEMONSTRATED / REQUIRES REBUILD**.

## 4. World-scale readability audit (design audit only)

| Check | Result |
|---|---|
| Head-to-body proportion | Monotone allometry in every race. Pipkin keeps the largest head share at matched short stature (0.146–0.159; PIPKIN L292 directional). Cogling head height stays at canon 11–13 cm; the 76 cm body reads 10.91 cm (**MARGINAL**, already flagged in W2H). Saurin stays inside §258. |
| Limb / torso share | Unchanged from the accepted W2 gates. Grask long-leg relation is held across the overlap. Elf relations are reference-state relations (W2F R1), not matched-height ≥ 1 % clamps. |
| Joint, hand, foot scale | Native-route exponents preserved. No new joint metric was introduced. Joint-breadth authority stays the W2C1 plane section. |
| Tail / body | Saurin tail stays coupled and isometric (64.3–64.9 % H). The tail is excluded from stature by canon. |
| Silhouette at matched height | **E1 (190 / 203):** Marchfolk, Halvren and Skarn differ by trunk / shoulder / limb architecture (Skarn broader, deeper, more robust), not by height. **E2:** the three elves and Halvren remain distinct in proportion at equal height; Fenn is not a universal elf baseline. **E3:** Cogling / Pipkin at 91 and 107, and Pipkin / Durrim at 122, read as distinct adult builds, not child scaling (W2H 13 / 13, 18 / 18, 16 / 16). **E4:** Skarn / Grask / Gorrund at 208 and 229 are separated by Grask verticality and long legs and by Gorrund transverse mass and depth. Height is never their identity. |
| Locked identity statements | Short (DU / PK / CG), tall (AE, GR, GO), compact (DU), long-limbed (GR), large / robust (SK): all preserved on the common scale. Saurin is not humanized: body plan, tail and head unchanged. |
| Cross-race ordering | All accepted W2 equal-height validators stand: Skarn v1.4 §6 at 190; Sagekin §10 at 178; Durrim at 152; Pipkin / Durrim at 122; Cogling / Pipkin 91–107; COG-BODY-10A; AD-3; AD-R15; AD-R36. RM-OT-05 adds the common-scale visual confirmation. No ordering inverted. |
| Later production dependencies (not set here) | Door heights, weapon / equipment scale, camera heights, collision capsules, mounts, animation retargeting, and the creator height-control continuity across native ↔ macro junctions (REFERENCE_ANATOMY §10, existing dependency). |

## 5. Contradictions and bookkeeping

These are not genuine canon conflicts.

1. **Gorrund reference stature.**
   - R-2 and GORRUND L29 say 229. The accepted ARM GOREF measures **230.9**: the W1i skeleton route added height, and it was accepted in W1j and W2D with no range narrowed.
   - A separate GO229 body exists. The minimum body is 208.27 cm.
   - Bookkeeping is needed so the register can state one reference number (§6, decision 1).
2. **HALVREN L501 status** still said "returned for author review" although W3A1 was FINAL ACCEPTED. **Pointer corrected** (status note only).
3. **H-5 wording vs the Aelari-supported 221.0.** H-5 says tails "never automatically reach a named source population's own extreme". The 221.0 reach equals the Aelari maximum, but W3A1 explicitly accepted it as the source ceiling. The later author resolution governs; no conflict.
4. **Historical evidence notes left unedited (provenance):**
   - the MF-boundary config status line and W2A gate header still mention the reverted 203 knee settings;
   - the W2C registry points at pre-revert MF203 / SK229 bodies.
   - The current accepted bodies are the W2C1-reverted ones (used here).
5. **SG163 route note.** It was accepted on macro 0.329, below the later R2 ~0.40 native threshold, because W2E predates R2. It is not an extreme, and it is reported only.
6. **Repo geometry copies.** Several reference copies committed in earlier waves (W1h GR, W1g elves, W1c HV, W1d CG, W1e DU) differ from the accepted later bodies (GR218R, AEL1 / FNL4 / VAL4, HVC1, CGJ7, DU137C), which live only in scratch. This is a manifest dependency, not anatomy.

## 6. Next author decisions

1. **Gorrund reference number:** keep 229 as the nominal reference with GOREF 230.9 as the accepted ARM stature, or state 230.9 as the reference. Bookkeeping only.
2. **Sagekin configuration 2:** build and accept the 152 / 208 configuration-2 boundaries to move Sagekin to SUPPORTED, or accept configuration 1 as sufficient under R-SEX.
3. **Cogling 76 cm head (10.91 cm vs the canon 11–13 cm):** accept as a marginal construction result, or rebuild the 76 cm head to ≥ 11 cm.
4. **Race-spec stature writeback:** most specs still label the W2-accepted bounds "first-pass / provisional". Should RM-OT-05 write the accepted register back into each spec as final, as was done for Halvren and Saurin?
5. **Gorrund 251:** canon calls it "never a permanent maximum". Confirm whether the world envelope upper end stays an open validation stature.
6. **Halvren conditional frequency:** tail frequency stays a named dependency (H-6). Confirm it stays OPEN until frequency authoring.
7. **Reference-asset manifest:** commit the accepted later-wave reference geometries to the repo, as the C1R faces already are.

## 7. Persistent files changed

**RM-UF-05 writeback (commit bee7fd3):**
- `decisions/UFCA_V1.md` (§4, §12, new §17.1, §18, §19)
- `specs/saurin/SAURIN_V1.md` (§267.2 binding note; slot-routing note)
- `reviews/claude-ufca-06-validation-framework.md` (§2.G citations, Skarn row, §4 status)
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`

**RM-OT-05:**
- `reviews/claude-rac-rm-ot-05-world-scale-author-gate.md` (this gate)
- `reviews/rac-rmot05-evidence/` (`register.json`, `sheets/`)
- `tools/rac/w1/rmot05_drivers/`
- `specs/halvren/HALVREN_V1.md` (W3A1 status pointer only)
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md` (status lines)
- Scratch: `w3d/b/SKM229-C1R` (C1R face layer on the accepted SKM229 body, for the lineups)

## 8. Stop

Stopped after the RM-OT-05 author gate. Not begun: posture / locomotion, equipment fit, environmental scale, collision capsules, camera heights, UE5 creator, MetaHuman, rigging, animation and gameplay.

# RAC W3A — Halvren genealogy-conditioned stature tails / RM-OT-03 — AUTHOR GATE

**Order:** `reviews/chatgpt-rac-w2-final-acceptance-w3a-halvren-genealogy-tail-order.md`
**Author:** Claude (diagnostic block; returned for ChatGPT / author review)
**Evidence:** `reviews/rac-w3a-hv-evidence/` (tables, values, checks, samples, sheets) · cfg `tools/rac/w1/cfg/w3a/HV-tails.json` · drivers `tools/rac/w1/w3a_drivers/`
**Status:** DIAGNOSTIC. No Halvren canon, creator weight, genealogy distribution or height UI was written.

---

## 0. Verdicts

| Item | Verdict | One-line reason |
|---|---|---|
| **HV-49 lower-tail boundary** | **CONSTRAIN** | Every test passes at every searched stature down to **147.2 cm**. The tool cannot find a biological endpoint inside the H-5 bound. The native route applies race-agnostic adult allometry, so the Halvren–Marchfolk separation does not change with stature. The endpoint is **bound-limited / generator-limited**, not biological. |
| **HV-50 Skarn-supported upper tail** | **CONSTRAIN** | Source protection is strong: 22/24 readings separate from matched Skarn at every point. With the canon-named Skarn systems, the lower-leg share leaves the scored span at **~220.5 cm** (MARGINAL from 217). A probe carrying Skarn's own leg development is coherent to **228.8 cm**, but that probe is not authored. |
| **HV-50 Aelari-supported upper tail** | **CONSTRAIN** | Source-first cap: **≤ 221 cm** (the top of the valid Aelari range). With canon-named systems the lower-leg share fails at **~219.2 cm**. The Aelari leg-development probe is coherent at 220.8 cm. |
| **Halvren tail route / continuity** | **ACCEPT** | No anatomical pop, segment reversal or joint-size inversion was found in any tail series. Four flagged steps are classified as measurement artifacts (§9). The W2G native ↔ macro junction stays the carried creator dependency. |
| **RM-UB-05 biological limits** | **CONSTRAIN** | Lower: reachable to 147.2 cm (bound-limited). Upper: ~219–220.5 cm on the canon-named systems; to 228.8 cm only under an un-authored tail leg-development rule. Needs one author decision (§12, AD-W3A-1). |
| **RM-UB-05 conditional frequency model** | **NAMED DEPENDENCY** | Conditional *validity* inside each tail class was measured (§10). The conditional *probability of a tail stature* needs a within-class stature-development distribution, and none exists. |
| **RM-UB-05 population-wide frequencies** | **NOT IDENTIFIABLE** | No canonical Halvren genealogy-prevalence model exists. C was not invented (§11). |
| **RM-OT-03 source-passing statistics** | **CONSTRAIN** | The statistics use 180 real builds; the linear emulator failed its own validation. Upper tails show 0/112 near-duplicates and 0 ambiguous. The lower tail shows 9/68 near-duplicates of matched Marchfolk, all confined to the near-pure Marchfolk-expression corner (support coordinate ≥ 0.80; one at 0.799). The sample is below the "several thousand" target, as justified in §10, and the corner needs a validity decision (AD-W3A-4). |
| **W3A Halvren overall** | **CONSTRAIN** | No accepted W2G central anatomy changed and no source canon is challenged. The upper-tail reach depends on one new Halvren authorship decision, and the lower-tail endpoint is bound-limited. |

**Explicit statements (§20)**
- **Proposed lower-tail endpoint:** HV-49 is reachable to **147.2 cm** (demonstrated; resolution 0.2–0.3 cm; next point down would be the H-5 bound). Proposed reading: *Marchfolk-supported Halvren may reach to just above 147 cm*. This is not a measured biological minimum.
- **Proposed upper-tail endpoint(s):**
  - On the canon-named influence systems: Skarn-supported **~220 cm**, Aelari-supported **~219 cm**, combined **< 221 cm** (it already fails at 221).
  - Under AD-W3A-1 (tail leg development from the supporting source): Skarn-supported **228.8 cm** demonstrated, with only the H-5 bound above. Aelari-supported is capped at **221 cm** by its source range. The combined probe sits within 0.1 % of the span top at 228.8 cm (MARGINAL).
- **Does the endpoint depend on source condition?** **Yes**, on the upper tail. Skarn support reaches further than Aelari support (Aelari is source-capped at 221). The lower tail has one supporting source.
- **Does H-2 asymmetry emerge from evidence?** **Yes, without being forced.** Lower reach is 152 → 147.2 cm (≤ 4.8 cm, bound-limited). Upper reach is 213 → ~220 cm (canon-named systems) or → 228.8 cm (under AD-W3A-1). The lower tail is the narrower one in either case.
- **Can H-6 minority behaviour be shown without invented priors?** **Only structurally.** Tail statures need specific supporting sources (H-1). They also occupy a small part of each supporting class's reachable interval: 4.8 / 66 cm lower; 7–16 / 77 cm upper. No frequency was computed (§11).
- **Is any source canon challenged?** **No.** Marchfolk, Skarn, Aelari, Fenn, Vael and Sagekin W2 bodies were used as accepted, and no source rule was invented.
- **Is a new author decision required?** **Yes.**
  - **AD-W3A-1:** Does a source-supported upper tail inherit that source's leg-segment development, outside the HV-13…17 named systems? The answer decides 220 vs 228.8 cm.
  - **AD-W3A-2:** Accept HV-49 as bound-limited "just above 147 cm".
  - **AD-W3A-3:** Is the boundary-stature span the scoring rule for tails?
  - **AD-W3A-4:** Should a hidden validity rule exclude the near-pure Marchfolk-expression corner (lower tail; §10)?
- **Is any result generator-limited rather than biological?** **Yes.**
  - The HV-49 endpoint is limited by the bound and the generator, because the native route's allometry is shared across races.
  - The emulator was rejected, so RM-OT-03 runs on real builds at a smaller n.
  - The macro never saturates: 0.79–0.93, below 1.0. The upper limit is therefore not a generator ceiling.

---

## 1. Foundation preserved (§3)

The work starts from the final accepted W2G Halvren system with nothing reopened:
- the 152–213 cm envelope;
- HVC1 at ~178 cm;
- the native route below the junction and the macro route above it;
- the frame write (Narrow −8 %; Broad +8 % with pelvis ×1.12);
- composition via the muscle / weight macros;
- D1–D3;
- source-first inheritance;
- no ancestry slider.

All W2G central bodies (HV152…HV213) are reused unchanged as the central series. The W2G G rows were not re-scored. No W3A result required changing central anatomy.

## 2. Genealogy / source-condition manifest (§6, evidence 1–2)

Classes are **hidden test coordinates** of `tail_build.t_gen`. On each canon-named system (`hv_build.SYS`, HV-13…17) the value is a convex combination of HVC1's targets and each expressed source's own targets:

> (1 − Σe) · HVC1 + Σ e_s · source_s

A single source at 0.5 reproduces W2G `expr_targets`, and Marchfolk at 0.5 reproduces W2G HVXMF. These are not genealogy percentages, lore, controls or canon. No body is labelled "x % source".

| Class | Stature support (H-1) | Anatomy | Bodies |
|---|---|---|---|
| Lower C | Marchfolk | central Halvren (HVC1) | HL150/149/148/147.5/147.2C (native) |
| Lower M | Marchfolk | Marchfolk-expressed (e_MF 0.5) | HL150/148/147.2M |
| Lower X | Marchfolk | mixed human / elven (e_MF 0.5 + e_FN 0.5) | HL148X |
| Lower controls | none (H-1) | Fenn / Vael / Sagekin-expressed 0.5 | HL148FN / VA / SG |
| Upper C | Skarn / Aelari | central Halvren | HU217/219/221/225/228.8C (macro) |
| Upper S | Skarn | Skarn-expressed 0.5 | HU217/219/221/225/228.8S |
| Upper A | Aelari | Aelari-expressed 0.5 | HU217/219/220.8A; **HU225A = source-first probe beyond the Aelari range** |
| Upper SA | Skarn + Aelari | e_SK 0.5 + e_AE 0.5 | HU221/225/228.8SA |
| Upper controls | none (H-1) | Fenn / Vael / Sagekin / Marchfolk-expressed 0.5 | HU221FN / VA / SG / MF |
| Probes (not canon) | Skarn / Aelari | + supporting source's own leg development at half strength | HU221/225/228.8SD, HU220.8AD, HU228.8SAD |
| Matched sources | — | Marchfolk native (W2A configuration), Skarn W2B, Aelari W2F re-solved | MF147.2…150, SK217…228.8, AE217…220.8 + comps / Broad Skarn |

**RM-OT-03 seeds:** `w3a_sample.py`: L-MF 30491, U-SK 30502, U-AE 30513, U-SA 30524; validation 30535 + k.

**Coverage design:**
- stature uniform over the open tail interval (Aelari: up to its valid 221 cm);
- supporting-source coordinate uniform over 0–1;
- the rest Dirichlet(1) over HVC1 and the other five sources.

This is not a prevalence model. Every build record (route, macro, native factors, targets, bone scales) is in `construction.json`.

## 3. HV-49 lower-tail search (§8, evidence 3)

Search: 150 → 149 → 148 → 147.5 → 147.2 cm. The native short-adult route is used throughout. A re-solved macro would be ≪ 0.40 here, so the accepted rule applies. Every candidate is compared with **matched-height Marchfolk** built on the same native route.

| Test (§7) | 150 | 149 | 148 | 147.5 | 147.2 |
|---|---|---|---|---|---|
| 2 / 9 Source protection vs matched MF (24 readings; ≥ 2 separate by ≥ 1 %) | 10/24 PASS | 10/24 | 10/24 | 10/24 | **10/24 PASS** |
| Marchfolk-expressed class vs matched MF | 4/24 PASS | — | 4/24 | — | **4/24 PASS** |
| Mixed MF + FN class (148) | — | — | 16/24 PASS | — | — |
| 1 Coherence: 8 accepted Halvren readings inside the boundary-stature span (matched MF + nearest valid SG152 / FN157 / VA157) | 8/8 | 8/8 | 8/8 | 8/8 | **8/8 PASS** |
| 7 Adult read: head share ≤ matched MF | 0.1361 ≤ 0.1364 | … | … | … | **0.1368 ≤ 0.1371 PASS** |
| 3 / 8 Continuity 147.2 → 152 | smooth (≤ 0.4 % per step) | | | | |

**Mixed development / no uniform scaling.** HL147.2C differs from HV152 on 19 of 45 readings by ≥ 0.5 %, and uniform scaling would change none:
- head share +0.9 %;
- knee / segment +1.1 %;
- thoracic depth +1.1 %;
- femoral robusticity +1.1 %.

The native route re-proportions by region (length, girth, head, hand and foot exponents). The body is not a scaled 152 cm Halvren, and it carries no child proportions.

**Why the endpoint is not biological.**
- The Halvren-vs-Marchfolk separation is identical at 150, 149, 148, 147.5 and 147.2 cm: the same 10 readings at the same magnitudes.
- Both bodies use the same native allometry, so only their targets differ.
- Nothing in the tool degrades as stature falls toward 147. It cannot tell a biological lower limit from the authored H-5 bound.

**Classification:**
- demonstrated reachable tail: **147.2 cm**;
- demonstrated invalid beyond-tail region: **≤ 147 cm, by H-5 authorship only**;
- measurement / generator limit: **yes**;
- true biological endpoint: **NOT DEMONSTRATED** (do not canonize).

**Anatomy at the proposed HV-49 (147.2 cm)** — skeletal at t = 0. The full readings are in tables.md.

| Reading | HL147.2C | MF147.2 | HV152 |
|---|---|---|---|
| torso / leg / arm share | 0.2785 / 0.5351 / 0.4141 | 0.2824 / 0.5295 / 0.4079 | 0.2787 / 0.5356 / 0.4139 |
| head / neck share | 0.1368 / 0.0539 | 0.1371 / 0.0544 | 0.1356 / 0.0540 |
| forearm / arm, shin / leg | 0.3706, 0.5165 | 0.3678, 0.5163 | 0.3711, 0.5165 |
| hand / foot share | 0.1171 / 0.1491 | 0.1149 / 0.1497 | 0.1166 / 0.1490 |
| thorax breadth / depth (skin) | 0.1969 / 0.1386 | 0.1978 / 0.1399 | 0.1954 / 0.1372 |
| elbow / wrist / knee / ankle per segment (exact plane) | 0.365 / 0.202 / 0.284 / 0.276 | 0.368 / 0.211 / 0.286 / 0.282 | 0.362 / 0.200 / 0.281 / 0.275 |
| skeletal thoracic breadth / depth | 0.1688 / 0.1223 | 0.1693 / 0.1241 | 0.1672 / 0.1211 |
| skeletal shoulder-joint / crest / hip-joint spacing | 0.1893 / 0.1647 / 0.1335 | 0.1908 / 0.1644 / 0.1337 | 0.1898 / 0.1629 / 0.1322 |
| skeletal AP pelvic depth / pelvic vertical | 0.0997 / 0.0547 | 0.0994 / 0.0553 | 0.0988 / 0.0548 |

The accepted W1 Halvren G rows in the Halvren slot are scored against fixed W1 references at 173 cm, so at 147 cm they are report-level only. Thoracic depth and wrist / forearm sit outside the W1 span, exactly as at the accepted HV152.

Visual: `sheets/hv49_lower_tail.jpg`. Complete, adult, neutralized bodies (no ears, pigment or hair); no defect visible.

## 4. HV-50 upper-tail search (§9, evidence 4–6)

Search: 217 → 219 → 221 → 225 → 228.8 cm. The re-solved macro route is used; macro values run 0.79–0.89 for Halvren and up to 0.93 for Skarn, all < 1.0, so there is no generator ceiling.

**Source protection: all PASS, strongly.**
- vs matched Skarn: central 22/24, Skarn-expressed 22/24, Aelari-expressed 23/24, combined 23/24, at every stature.
- vs matched Aelari (≤ 221 cm): 17–21/24.
- vs Aelari 221 as **D1 ENDPOINT** evidence above 221: 14–21/24. This is labelled endpoint evidence and is never treated as matched height.

The Halvren is neither a Skarn body with mixed ears nor an Aelari body with human breadth. Against Skarn it separates by −16 to −28 % on the knee and wrist per segment, −5 to −13 % on thoracic depth and −4 to −6 % on torso share. Against Aelari it separates on skeletal crest breadth (+5 to +8 %), thoracic depth and neck share.

**Coherence (test 1): the binding result.**

- **Reading that fails:** lower-leg share (shin / leg). On the macro route it falls with stature in every family. Halvren falls from 0.4804 at 213 to 0.4684 at 228.8 cm.
- **Matched supporting sources keep longer shins:**
  - Skarn 0.5007 → 0.4900. Its accepted short-femur target is `upperleg-height-decr 1.0`.
  - Aelari 0.4912 → 0.4883. Its accepted W1m leg bone scales give thigh ×0.9875 and calf ×1.0523.
- **Why the Halvren falls below them:** the canon-named Halvren Skarn and Aelari influence systems (HV-13…17) do not include those leg systems.
- **Inside the central envelope this was harmless.** Marchfolk and Sagekin had matched adults whose shin share is as low (W2G 203: inside the span).
- **Above 213 cm, H-1 removes them.** The Halvren then carries human-family lower-leg allometry to statures where no human-family source has adults.

| Class | Leaves the scored span (SG208 floor 0.4799) | Fails (−1 %) at | Reading at the end of the search |
|---|---|---|---|
| central | 213.7 cm | **219.8 cm** | 0.4684 @ 228.8 (FAIL) |
| Skarn-expressed | MARGINAL already at 217 | **220.5 cm** | 0.4688 @ 228.8 (FAIL) |
| Aelari-expressed | MARGINAL already at 217 | **219.2 cm** | 0.4738 @ 220.8 (FAIL) |
| Skarn + Aelari | — | below at 221 | 0.4686 @ 228.8 (FAIL) |
| PROBE Skarn + Skarn leg development | never | never | 0.4843 @ 225, 0.4813 @ 228.8 (PASS) |
| PROBE Aelari + Aelari leg development | — | — | PASS @ 220.8 |
| PROBE Skarn + Aelari + leg development | — | — | 0.4945 @ 228.8 (MARGINAL, +0.1 % above FN211) |

Against the **matched supporting sources only** (Skarn and Aelari, a stricter report-level rule), every canon-named-system tail body is already 2.8–4.0 % short from 217 cm. That is the reason for AD-W3A-3.

All other accepted Halvren readings stay inside the span at every upper point: torso, leg, arm, forearm, thoracic depth, finger / hand, wrist.

**Classification:**

| | Skarn-supported | Aelari-supported |
|---|---|---|
| Demonstrated reachable (canon-named systems) | ~220 cm (MARGINAL band 217–220) | ~219 cm |
| Demonstrated invalid beyond | ≥ 221 cm under the scored rule | ≥ 220.8 cm under the scored rule; anything above 221 is source-first excluded |
| Under AD-W3A-1 | 228.8 cm (bound-limited thereafter) | ≤ 221 cm |
| True biological endpoint | depends on AD-W3A-1; not a generator limit | depends on AD-W3A-1; not a generator limit |

**Beyond-range Aelari probe (HU225A).** An Aelari-expressed Halvren at 225 cm still separates 16/24 from Aelari 221. That is the generator showing it *can* build the body; it says nothing about Aelari support. Source-first excludes Aelari stature support above 221 cm, and the probe is not used for any endpoint.

**Anatomy at the HV-50 candidates** (the full set is in tables.md):

| Reading | HU219S | HU228.8S | PROBE HU228.8SD | SK228.8 | HU219A | HU220.8A | AE220.8 |
|---|---|---|---|---|---|---|---|
| torso / leg / arm | 0.278 / 0.550 / 0.415 | 0.277 / 0.553 / 0.415 | 0.281 / 0.547 / 0.422 | 0.292 / 0.533 / 0.404 | 0.272 / 0.553 / 0.415 | 0.272 / 0.553 / 0.415 | 0.271 / 0.556 / 0.417 |
| head / neck | 0.1207 / 0.0517 | 0.1194 / 0.0513 | 0.1209 / 0.0520 | 0.1215 / 0.0525 | 0.1219 / 0.0550 | 0.1217 / 0.0549 | 0.1255 / 0.0531 |
| forearm / arm, shin / leg | 0.361, 0.476 | 0.359, **0.469** | 0.359, **0.481** | 0.351, 0.490 | 0.365, 0.475 | 0.365, **0.474** | 0.364, 0.488 |
| hand / foot | 0.113 / 0.152 | 0.113 / 0.152 | 0.114 / 0.154 | 0.116 / 0.159 | 0.110 / 0.147 | 0.110 / 0.147 | 0.113 / 0.151 |
| thorax breadth / depth (skin) | 0.181 / 0.128 | 0.174 / 0.126 | 0.176 / 0.127 | 0.184 / 0.137 | 0.174 / 0.119 | 0.174 / 0.118 | 0.168 / 0.115 |
| elbow / wrist / knee / ankle per segment | 0.312 / 0.213 / 0.239 / 0.309 | 0.304 / 0.213 / 0.234 / 0.313 | 0.301 / 0.212 / 0.245 / 0.313 | 0.333 / 0.254 / 0.290 / 0.337 | 0.300 / 0.187 / 0.218 / 0.286 | 0.299 / 0.187 / 0.217 / 0.287 | 0.296 / 0.193 / 0.217 / 0.282 |
| skeletal thoracic breadth / depth | 0.150 / 0.115 | 0.148 / 0.113 | — | 0.156 / 0.126 | 0.149 / 0.106 | 0.149 / 0.106 | 0.143 / 0.102 |
| skeletal shoulder-joint / crest / hip-joint | 0.190 / 0.148 / 0.118 | 0.187 / 0.147 / 0.116 | — | 0.202 / 0.154 / 0.122 | 0.182 / 0.147 / 0.117 | 0.182 / 0.147 / 0.117 | 0.178 / 0.139 / 0.113 |
| skeletal AP pelvic depth / pelvic vertical | 0.092 / 0.051 | 0.092 / 0.051 | — | 0.097 / 0.052 | 0.092 / 0.051 | 0.092 / 0.051 | 0.093 / 0.053 |

Visuals:
- `sheets/hv50_skarn_tail.jpg`
- `hv50_aelari_tail.jpg`
- `hv50_combined_tail.jpg`
- `tail_probes.jpg`

All show complete, adult, coherent bodies. The lower-leg difference is real but not a visible defect: it is a proportion reading.

## 5. Negative controls (§6 / §17 Q5, evidence 7)

Fenn (157–211), Vael (157–203) and Sagekin (152–208) have no valid adult below 152 or above 213 cm. Marchfolk (147–203) has none above 213. **H-1 therefore follows directly from the accepted source ranges.**
- Only Marchfolk reaches below the central floor.
- Only Skarn (≤ 229) and Aelari (≤ 221) reach above the ceiling.

The control bodies (HL148FN / VA / SG, HU221FN / VA / SG / MF) can all be *built*; the generator does not refuse them. However, each one either expresses its source at a stature where that source has no adult, or extends a source past its tallest or shortest adult.
- Lower controls vs their source's nearest valid adult: Fenn 14/17 separate, Vael 8/17, Sagekin 5/17.
- Upper controls: 9–12/17.

H-1 is a **support rule** (no source adult exists to supply that stature). It is not an anatomical impossibility, and the tool never shows a control tail as a source-supported phenotype. **Q5 (do Fenn / Vael / Sagekin extend a tail?): No.** No accepted source of theirs supplies the stature.

## 6. Frame stress (§10, evidence 10)

Narrow and Broad were built at HL147.2C, HU228.8S, HU220.8A and HU228.8SA.
- All 40 breadth rows move ≥ 1 % in the right direction.
- All 104 length, head, hand, neck and joint-keeping rows hold.
- Every framed body passes source protection: 14–15/24 vs matched Marchfolk; 22–24/24 vs Skarn; 18/24 vs Aelari; 19–21/24 vs Aelari 221 (D1).

Frame validity is not conditional at the tails. Frame changes breadth only and introduces no ancestry signal.

## 7. Composition stress (§10, evidence 11)

LOWMUS, HIMUS, LOWFAT and HIFAT were built at the same four endpoints. Each is compared with the **same-composition** matched source (MF147.2, SK228.8, AE220.8 compositions).
- All 16 invariance rows PASS: proportions are unchanged within 1 %.
- All 16 same-composition source-protection rows PASS: 8–10/17 vs Marchfolk, 16/17 vs Skarn, 10/17 vs Aelari. Same-composition Skarn 220.8 was not built, so for the Aelari endpoint Skarn is compared at reference composition: report rows, 23–24/24 at the frames.

No boundary depends on one composition state (Q10). High fat does not rescue anything, because nothing needed rescuing. The failing upper-tail reading (lower-leg share) is composition-invariant, so fat or muscle cannot rescue it either.

## 8. Collision matrix (§17)

| # | Question | Answer | Evidence |
|---|---|---|---|
| 1 | HV-49 mistaken systematically for matched Marchfolk? | **No** for central and mixed anatomy (10/24, 16/24). The **Marchfolk-expressed** class passes the protocol narrowly (4/24). In RM-OT-03, duplication appears only at high Marchfolk expression: 9 of 68 lower-tail samples. 8 of the 15 samples with Marchfolk coordinate ≥ 0.80 duplicate, against 1 of 53 below 0.80 (at 0.799). The duplication is localized, not systematic for Halvren in general. | §3, §10 |
| 2 | HV-50 mistaken systematically for matched Skarn? | **No** (22–23/24 at every point, every class, Broad and HIMUS included) | §4, §6, §7 |
| 3 | Aelari-supported HV-50 mistaken for Aelari? | **No** (17–21/24 matched; RM-OT-03 0/40 near-duplicates; minimum separation vs matched Aelari 8/17) | §4, §10 |
| 4 | Above the Aelari range, still Halvren vs Skarn + Aelari endpoint? | **Yes** (22–23/24 Skarn; 14–21/24 vs AE221 D1 endpoint) | §4 |
| 5 | Fenn / Vael / Sagekin extend a tail? | **No**: no supporting adult at that stature (H-1 follows from the source ranges) | §5 |
| 6 | Broad / high-muscle Halvren collapses into Skarn? | **No** (Broad vs Broad Skarn 16/17; HIMUS vs HIMUS Skarn 16/17) | §6, §7 |
| 7 | Narrow / low-mass collapses into Aelari / Fenn? | **No** (Narrow 220.8A vs AE220.8 18/24; Narrow 228.8 vs AE221 12–13/17; vs FN211 17/17; LOWFAT 147.2 vs LOWFAT MF 9/17) | §6, §7 |
| 8 | Short Halvren collapses into Marchfolk? | **No** for central anatomy at every stature. **Conditional** for strong Marchfolk expression (Q1) | §3, §10 |
| 9 | Identity survives ear / pigment / hair / culture neutralization? | **Yes.** All comparisons are body-only (meshes have no ears, pigment, hair or clothing; head and ear readings are excluded from the protocol) | protocol |
| 10 | Any boundary depends on one composition state? | **No** | §7 |

Scalar overlaps exist and are allowed, for example lower-tail shin share equals Marchfolk's. No complete-body duplication was found in any authored class.

## 9. Route / continuity audit (§16, evidence 12)

**Central series:** 147.2 → 147.5 → 148 → 149 → 150 → 152 → 163 → [junction] → 173 → 178 → 181 → 190 → 203 → 213 → 217 → 219 → 221 → 225 → 228.8.
**Condition series:** M, S, A, SA, the Skarn-development probe, and the Marchfolk / Skarn / Aelari source families.

| Category | Result |
|---|---|
| Anatomical pop | **none** (renders `hv_tail_series.jpg`; per-step changes ≤ 0.4 % across the lower tail, ≤ 0.7 % per step on skin readings above 213 except the item below) |
| Segment reversal / joint-size inversion | **none** in any tail series |
| Route junction | **HV163 → HV173**: the accepted W2G native ↔ macro junction (femur / leg −1.4 %, pelvic vertical +1.1 %, ankle −1.8 %) — unchanged, still the carried creator dependency. No new junction: the lower tail stays native, the upper tail stays macro. |
| Derivative outliers (measurement) | (a) skin thoracic-breadth step at 217 → 219 (central −2.2 %) and 219 → 221 (Skarn-expressed −3.2 %). The **same step occurs in the Skarn source family** (SK208 → 217 −4.9 %), and skeletal thoracic breadth is smooth: this is a skin-station artifact, not Halvren biology. (b) HU225C → HU228.8C skeletal-proxy thoracic breadth +3.4 % on that one body only. Skin thorax breadth is smooth (−0.5 %), and the S / SA bodies at 228.8 are smooth: a grid artifact. (c) Skeletal bitrochanteric / crest −1.5 % at HL147.2 → 147.5 (C and M) is skeletal-proxy jitter. Skin is identical. (d) Skarn source knee section +1.9 % at SK219 → SK221 is a source-side reading (W2C1 knee class), reported only. |
| Source-expression jump | Expression offsets (central → S / A / SA at the same stature) are anatomy, not stature, and are reported as such. Within each class the series is smooth. |
| Generator-only artifact | (b) and (c) above; the native route's shared allometry (§3) |

The future creator requirement (no visible pop under continuous height control) is unchanged and not implemented here.

## 10. RM-OT-03 — source-passing statistics (§11–12, evidence 13–15)

**Method.**
- A linear response emulator was built first (`w3a_emul.py`) so that several thousand samples per stratum would be practical. **It failed its own validation** on 20 real random builds.
  - Joint-breadth, thoracic-depth and neck readings respond non-linearly to the hidden coordinates: rms error 6.9 % wrist, 4.9 % knee, 3.7 % ankle and thoracic depth, 2.9 % neck, against a 1 % separation threshold.
  - It under-called Marchfolk duplication on 3 of 8 lower-tail validation bodies: it predicted 5–8 separating readings where the real bodies had 0–1.
  - Its rates are therefore **not reported as results**. The validation is kept in `emul.json` and tables.md as the reason.
- RM-OT-03 was run instead on **real generator builds**:
  - 160 deterministic coverage samples (`tail_build.py rs`: L-MF 60, U-SK 36, U-AE 36, U-SA 28);
  - plus the 20 validation builds;
  - **n = 68 / 41 / 40 / 31**, at reference frame and composition (§6–7 show frame and composition do not change the separations).
- Each sample is compared with all six sources: at matched height inside the source's valid range, otherwise against its nearest valid adult (labelled ENDPOINT; Aelari above 221 = D1).
- The comparison uses 17 body-only readings. With no skeletal grids for these samples, a near-duplicate call is **conservative**: the full 24-reading protocol can only separate more.

| Stratum | n | Near-duplicate of a matched source (95 % CI) | Accepted but ambiguous (2–3 readings) | Min separation vs supporting source (quantiles 0 / 25 / 50 %) | Endpoint (D1 / nearest-adult) duplicates |
|---|---|---|---|---|---|
| **L-MF** lower tail, Marchfolk-supported | 68 | **9 (13.2 %; 7.1–23.3 %)**, all Marchfolk | 13 (19 %; 11.5–30.0 %), all nearest Marchfolk | MF 0 / 3 / 7 | 0 |
| **U-SK** upper, Skarn-supported | 41 | **0 (0–8.6 %)** | 0 | SK 15 / 16 / 16 | 0 |
| **U-AE** upper, Aelari-supported (≤ 221) | 40 | **0 (0–8.8 %)** | 0 | AE 8 / 10 / 10; SK 15 / 16 / 16 | 0 |
| **U-SA** upper, Skarn + Aelari | 31 | **0 (0–11.0 %)** | 0 | SK 14 / 16 / 16 | 0 |

**Per source (controls / collision checks).**
- **Fenn, Vael, Sagekin:** 0 near-duplicates in every stratum. Minimum separations are 15, 4 and 4 readings (lower) and 13–14, 7–8 and 4–5 (upper).
- **Marchfolk** in the upper strata (endpoint): 0 near-duplicates, minimum 8.
- **Skarn** in the lower stratum (endpoint): 0 near-duplicates, minimum 13.

**Duplication frontier (L-MF), by the hidden Marchfolk coordinate:**

| e_MF | 0–0.2 | 0.2–0.4 | 0.4–0.6 | 0.6–0.7 | 0.7–0.8 | 0.8–0.9 | 0.9–1.0 |
|---|---|---|---|---|---|---|---|
| near-duplicate / n | 0/15 | 0/9 | 0/15 | 0/5 | 1/9 (0.799) | 7/10 | 1/5 |
| ambiguous | 0 | 0 | 0 | 1 | 5 | 3 | 4 |

The logistic 50 % point is e_MF ≈ 0.90 (bootstrap 0.81–1.07). Duplicates span 148.7–151.7 cm and show no stature dependence. That matches §3: on the native route, separation is stature-invariant. By that invariance, the same corner is expected in the native central range (152–163 cm); this was not tested there.

**Convergence.** Running L-MF duplicate rates are 0.10 / 0.10 / 0.13 / 0.10 / 0.10 / 0.13 at n = 10 / 20 / 30 / 40 / 60 / 68. The upper strata stay at 0 from n = 10.

**Sample-size justification (§12).** Several thousand per stratum was not practical here: real builds take ~0.5–1.5 min each on 2 CPUs, and the emulator was rejected. The smaller n is defensible for three reasons:
- **The classification is deterministic.** Given the hidden coordinates there is no sampling noise, so what n buys is resolution of the frontier. The frontier is resolved here: 0/44 duplicates below 0.70, 8/15 at ≥ 0.80.
- **Rates are design-conditional.** They are rates under a coverage design, not prevalence (§11). Tighter CIs would only refine a design-dependent number.
- **The upper-tail answer is robust.** 0/112 duplicates with minimum separation 8–15 readings is far from the 2-reading threshold.

The remaining uncertainty is reported with the CIs. The lower-tail rate is **design-dependent**: it scales with how much weight a sampler puts on e_MF ≥ 0.8.

**Rejected bodies (§12):** 9 duplicates (L-MF, Marchfolk), 0 adult-read failures, 0 others. Every sample is listed in tables.md and `rs.json`.

**Reading for the author.** Ambiguous and hard-to-classify Halvren exist; all 13 sit in the high-Marchfolk band. Systematic exact source duplication does **not** occur in any authored class or in the upper tail. It does occur in one **corner of the diagnostic coordinate space**: Marchfolk expression ≳ 0.8, where the Halvren-specific targets are mostly cancelled.
- **AD-W3A-4:** should that corner be excluded by a hidden validity rule (reject on the protocol), or treated as allowed passing? The order's rule ("some ambiguous individuals are valid; systematic duplication is not") suggests rejection. The threshold is the author's to set; the evidence shows the frontier lies between 0.7 and 0.9.

## 11. Frequency identifiability firewall (§13, evidence 16)

- **A. Biological reachability:** derived (§3, §4). The upper value is conditional on AD-W3A-1.
- **B. Conditional tail probability:** **NAMED DEPENDENCY.**
  - What can be measured is P(valid body | genealogy class, tail stature): the RM-OT-03 acceptance in §10.
  - What cannot is P(tail stature | genealogy class). That needs a within-class stature-development distribution, meaning how a Halvren's stature potential is drawn given its sources. No canonical one exists, and the diagnostic coverage sampler must not stand in for it.
  - **Minimum data to resolve:** for each tail class, an authored stature distribution (shape and centre relative to the supporting source's range), or a rule that derives it from the source populations' own stature distributions.
- **C. Population-wide frequency:** **NOT IDENTIFIABLE.**
  - It needs B plus a Halvren genealogy-prevalence model: how common Marchfolk-, Skarn- and Aelari-supported lineages are.
  - Equal source prevalence was **not** assumed, and creator randomization was not read as demography.
  - **Minimum data:** relative prevalence of the supporting-source lineage classes among Halvren, plus B.
- **H-6 (structural only):**
  - tails require specific supporting sources;
  - tails occupy 4.8 of 66 cm of the Marchfolk-supported class's reachable interval, and 7–16 of 77 cm of the Skarn-supported class's;
  - any stature distribution centred inside the central envelope therefore makes them minority outcomes.
  - No ordering of upper vs lower frequency was produced.

**Safe creator-behaviour constraint (§14; proposal, not canon):**
- keep 152–213 as the primary envelope;
- allow manual reach into the demonstrated tails only (lower to 147.2; upper to ~220, or to 228.8 if AD-W3A-1 is accepted) under the hidden validity rules (supporting source present, no matched-source duplication);
- Extreme randomization may reach tails but must not be guaranteed to reach source extrema;
- no hard clip at 152 / 213;
- no ancestry percentage UI;
- tail weights stay unset until B and C are authored.

## 12. Named dependencies and author decisions

- **AD-W3A-1 (new; decides HV-50).** Should a Skarn- or Aelari-supported upper-tail Halvren inherit that source's **leg-segment development**? For Skarn that is the short femur; for Aelari, the W1m thigh / calf scales. These sit outside the HV-13…17 named systems.
  - **No:** HV-50 ≈ 220 cm (Skarn) / ≈ 219 cm (Aelari).
  - **Yes**, at the probe's half strength: HV-50 reaches 228.8 cm (Skarn), with the H-5 bound above. Aelari stays capped at 221.
  - This is a Halvren-authorship question, not missing source biology. No source rule is missing.
- **AD-W3A-2.** Accept HV-49 as **bound-limited**: Marchfolk-supported Halvren reach to just above 147 cm, with no measured biological minimum above the H-5 bound. The tool cannot discriminate one (§3).
- **AD-W3A-3.** Confirm the tail coherence rule. Options:
  - (a) the **boundary-stature span**: matched supporting sources plus the nearest valid adult of every other span source. This is the scored rule used here.
  - (b) the stricter **matched supporting sources only** rule. Under it every canon-named upper-tail body fails from 217 cm, and even the AD-W3A-1 probe sits at 0.481–0.484 against Skarn 0.490.
- **AD-W3A-4.** Hidden validity rule for the near-pure Marchfolk-expression corner. On the lower tail, 8 of 15 real samples at e_MF ≥ 0.80 are near-duplicates of matched Marchfolk, against 1 of 53 below 0.80 (§10).
- **B / C** (§11): within-class stature distribution; genealogy-prevalence model.
- **Carried:** W2G native ↔ macro junction (creator interpolation); final creator clamp / interpolation; height UI; randomization weights. Not touched.
- **Measurement items:** the skin thoracic-breadth station step at 217–221 cm (all families) and the single-body skeletal-proxy artifacts (§9). These are recorded for any future measurement-pass review.
- **NOT RUN:**
  - skeletal-proxy grids for composition, control, probe, validation and RM-OT-03 sample bodies (their comparisons use the 17 non-skeletal readings, which is conservative);
  - the Skarn guard (K) skeletal rows at 219 cm on non-grid bodies;
  - the combined-condition frame and composition stress beyond the four endpoints.

## 13. Stop

W3A stops here, at its gate. Nothing else was started: no Saurin RM-UF-03 / 04 / RM-UB-08, RM-CF-09, RM-CF-05, RM-UF-05, roster review, creator implementation, UE5, rigging, animation, equipment or gameplay work.

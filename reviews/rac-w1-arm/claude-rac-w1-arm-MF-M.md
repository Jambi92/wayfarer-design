# ARM Acceptance Record — MF-M: Marchfolk configuration 1, Iteration 3 candidate (manifest #1)

**Order:** RAC W1, W1-02 **Date / pass:** October 5, 2026, W1 pass 1 **Inspector:** Claude
**Asset:** `RaceBodies/out/Marchfolk_Masc.blend`, SHA-256 `d1dea7b6…50d5`; evaluated with `tools/rac/w1/mf_extract.py` (Blender 5.0.1 bpy, depsgraph-evaluated "Marchfolk.body")
**Evidence:** `reviews/rac-w1-evidence/mf_checks.json`, `mf_Masc_inspect.jpg`

**Superseded (W1 continuation, October 5, 2026):** the corrected/rebuilt candidate is **MF-M-R** (`reviews/rac-w1c-arm/claude-rac-w1c-arm-MF-M-R.md`). This record stays as history.

## Technical verdict: **CONSTRAIN — requires correction before acceptance.** Not measured.

| Req. | Finding | Result |
|---|---|---|
| R-1 Central adult | Age macro "young" (MakeHuman ≈ 25 y), not mid-adult | **CONSTRAIN** |
| R-2 Stature | 173.000 cm; MPFB default male ≈ 172.98 cm, height essentially native | PASS |
| R-3 Central skeletal values | MakeHuman default proportions: **builder-chosen**, not derived from MF canon | needs author acceptance |
| R-4 Reference composition | muscle 0.5 / weight 0.5 macros: **builder-chosen** stand-ins | needs author acceptance |
| R-5 Symmetry | mirror median 0.0, p99 3.7e-7 cm | PASS |
| R-6 Stance | **A-pose**: upper arm 41.1° from vertical, elbow flexion 46.6°; wide stance: thigh 7.6°, shin 6.3° | **CONSTRAIN** — re-pose needed. Not attempted in W1: the order allows re-posing only if anatomy is unchanged, and a rig re-pose of this body (rig joints are not anatomical, see below) cannot be shown to meet that without a separate check |
| R-7…R-9 | No hair; neutral material | PASS |
| R-11 Mandatory anatomy | **No eyeballs** (empty sockets): OC, orbit and aperture landmarks absent | **CONSTRAIN** — RM-CF-02 and RM-UF-01 cannot run |
| Resolution | 13,380 evaluated vertices; median edge 0.73 cm | Too coarse for craniofacial items |
| Joint centres | Rig upper arm 25.18 cm < forearm 26.71 cm: rig joints are not anatomical joint centres | Rig cannot supply limb segment landmarks |
| R-14 Builder-chosen values | ethnic mix $as 0.33 / $ca 0.331 / $af 0.33; age young; muscle 0.5; weight 0.5; default proportions; height macro; A-pose | **listed; BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED** |

**Biological grounds:** the body reads as an ordinary adult human; nothing in it contradicts MF canon. It fails acceptance on state (age, stance, missing eyes), not on biology. Correction is specified in `reviews/rac-w1-packets/claude-rac-w1-packet-MF-M-R.md`. No measurement was taken (order §3 W1-02: measure only if accepted).

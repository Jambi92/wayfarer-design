# ChatGPT Order — RAC RP4 Cogling Final Author Acceptance / Freeze Closure

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Reviewed Claude commit:** `c800205e4bd8df4b8a854f04d05fd31cebd9e7e2`  
**Parent order:** `reviews/chatgpt-rac-rp4-cogling-author-rulings-final-production-order.md`  
**Scope:** record-only Cogling RP4 final freeze closure  
**Author ruling:** **COGLING RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FREEZE APPROVED**  
**Stop condition:** complete the record/status/canon/handoff closure and STOP FOR CHATGPT REVIEW.

---

# 1. Freeze the approved Cogling state

Freeze exactly:

## Final production references
- `CG_M_REF_RP4_v001`
- `CG_F_REF_RP4_v001`

## Final Cogling compact branch
- `MPFB_COGLING_COMPACT_BRANCH_v001`

## Source lineage
- c1 central source: `CGJ7`
- c2 technical production anchor: `CGF91-NAT`
- accepted minimum: `CG76H-NAT`
- accepted maximum: `CG107-NAT`
- superseded provenance only: `CG76-NAT`

No geometry, topology, proportion, foot anatomy, branch placement, validator logic, T-7 logic, or source anatomy change is authorized by this order.

Cogling sex-related anatomy remains OPEN.

---

# 2. Freeze source

Use the already-reviewed state from:

- `reviews/claude-rac-rp4-cogling-final-production-gate.md`
- `reviews/rac-rp4-evidence/cogling/final/COGLING_RP4_FREEZE_CANDIDATE.json`

Reviewed commit:
- `c800205e4bd8df4b8a854f04d05fd31cebd9e7e2`

This is **freeze-by-record**.

Do not rebuild or resave the approved production meshes merely to change embedded CANDIDATE text.

---

# 3. Freeze reviewed production hashes

## CG_M_REF_RP4_v001
- file SHA-256:
  `d605422ebc3cb3f97e4914f35fbf955b7054c4439877b45ee7b42446e7fc62cb`
- geometry hash:
  `7355ca55eb71e4ad2adbc16480fc613fe1be57fd6770cea1884aa910fb6208b1`

## CG_F_REF_RP4_v001
- file SHA-256:
  `9432594a376382c55115b90c98af37fd3a0497dae6f95687f2cd45271d74761b`
- geometry hash:
  `be9396ec7f2707e1d4fadd3fa1457f611f94dc5067ab4141b76ac13c6a07fff3`

## Shared topology
- face topology hash:
  `a11b8831506519db8ae17ba466540a0cd71faa5d82ca501f53c1fc1d5e3b76dc`
- 58,162 vertices
- 58,160 quads
- 100% quads
- identical c1/c2 topology

## Branch
- `MPFB_COGLING_COMPACT_BRANCH_v001`
- definition hash:
  `75ed801f698e78200c8ac3e2891b7f1d4c0459de4c4e6dc117b8629422965a5f`
- shared branch-map hash:
  `600e30713dea72103d819dec23594625047734a7294ce3e50633d59c0733f9eb`

Preserve all reviewed values exactly.

---

# 4. Promote the freeze record

Promote:

`reviews/rac-rp4-evidence/cogling/final/COGLING_RP4_FREEZE_CANDIDATE.json`

to:

`reviews/rac-rp4-evidence/cogling/final/COGLING_RP4_FREEZE.json`

Final status:

**COGLING RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

The final freeze record is authoritative over any embedded CANDIDATE / NOT FROZEN text inside production files.

---

# 5. Preserve the Cogling toe-validator exception exactly

Preserve:

`PASS_COGLING_TOE_PROBE_GEOMETRY_EXCEPTION`

Scope only:

## Bodies
- `CG76H-NAT`
- `CGJ7`
- `CG107-NAT`

## Stations
- `toe3_j1_l`
- `toe3_j1_r`
- `toe4_j1_l`
- `toe4_j1_r`

## Conditions
Only when:
1. raw status = `FAIL_LOOPS`;
2. loop mode = `closed_ring_fallback`;
3. no crease poles;
4. size-consistent toe-probe diagnostic passes;
5. no foot topology was added.

Raw authoritative validator history must remain unchanged.

Do not:
- reuse the Pipkin exception label;
- create a universal compact-race exception;
- change global D4;
- add Cogling foot topology;
- apply this automatically to Saurin or any later race.

---

# 6. Preserve permanent dual validator record

## Raw authoritative
- CG76H-NAT: 65/69
- CGJ7: 65/69
- CGF91-NAT: 69/69
- CG107-NAT: 65/69

## Author-adjusted production verdict
- CG76H-NAT: **69/69**
- CGJ7: **69/69**
- CGF91-NAT: **69/69**
- CG107-NAT: **69/69**

Both raw and adjusted states must remain permanent.

---

# 7. Preserve the 76 cm T-7 dual record

Preserve the Cogling-only small-body sampling exception:

`PASS_COGLING_T7_SMALL_BODY_SAMPLING_EXCEPTION`

Scope:
- `CG76H-NAT` only.

Permanent dual record:

## Raw fixed-resolution T-7
- minimum IoU ~0.9931
- nominal threshold 0.995
- raw failure retained

## Scale-consistent production verdict
- front/rear ~0.99735
- profiles ~0.9980
- PASS

Conditions remain:
- T-1/T-2 pass;
- same raw T-7 result exists on v005 and branch;
- scale-consistent reading passes;
- no geometry change is authorized to satisfy raster quantization.

Global T-7 remains unchanged.

Do not generalize this exception to other races without a separate author gate.

---

# 8. Preserve accepted c2 anchor residual

Record as accepted:

**ACCEPTED C2 TECHNICAL-ANCHOR NARROWER-CORE RATIO RESIDUAL**

For `CGF91-NAT`:
- crest / thoracic breadth ratio reads ~+1.05…+1.21% vs diagnostic Pipkin c2;
- crest itself remains ~5.7–6.1% narrower than Pipkin c2;
- thorax remains ~6.6–7.2% narrower;
- pelvic vertical / thoracic vertical remains ~9.8% lower;
- pelvic AP / thoracic depth remains ~4.6% lower;
- narrow-core and distal-redistribution identity remains intact.

Do not modify the c2 anatomy to force the ratio.

---

# 9. Preserve accepted Cogling anatomy

Do not reopen:

- accepted 76–107 cm stature envelope;
- reference ~91 cm;
- canonical 76 cm `CG76H-NAT`;
- Fine-Scale Elongated Articulation;
- narrow stable central core;
- broadly near-human total limb contribution;
- distal redistribution in forearm/lower leg;
- relatively emphasized adult hands/fingers;
- fine shafts / smaller adult joints;
- mature adult pelvis;
- adult head/body relationship;
- 76 cm adult-vs-child firewall;
- equal-height Pipkin separation;
- hidden-identity firewalls.

Do not exaggerate Cogling anatomy to strengthen neutral diagnostic-clay separation.

---

# 10. Final deformation / anatomy status

Record as accepted production evidence:

- c1: 18-pose suite, no new topology class;
- c2: 18-pose suite, no new topology class;
- CG76H / CG107 key poses: no new topology class;
- no new grip/fist collapse;
- no new long-finger folding class;
- no new foot/toe defect;
- no wrist/thumb-web failure;
- T-1 / T-2 / T-3 / T-6 pass;
- T-7 ordinary PASS except CG76H scoped exception;
- branch T-4 >4:1 = 0;
- contact new pairs = 0.

Same-class strain differences remain accepted report-only evidence.

---

# 11. Branch reuse status

Record:

`MPFB_COGLING_COMPACT_BRANCH_v001` is accepted for Cogling.

It is **not** a universal compact-race branch.

Its engineering face list may match Pipkin, but:
- placement is Cogling-specific;
- S weights are Cogling-specific;
- branch-map geometry is Cogling-specific;
- Cogling toe and T-7 exceptions are Cogling-specific.

Do not propagate:
- Cogling thumb placement;
- Cogling branch dimensions;
- Cogling toe exception;
- Cogling T-7 exception;
- Cogling source-anatomy assumptions

without a separate later-race gate.

---

# 12. Status / canon / handoff updates

Update at minimum:

- `specs/STATUS.md`
- `specs/cogling/COGLING_V1.md`
- `reviews/claude-session-handoff.md`
- `reviews/reference-assets/manifest.json` or normal freeze manifest/index
- carry-forward register only if a later-stage item genuinely belongs there

Top status:

**COGLING RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

State clearly:

- final refs:
  - `CG_M_REF_RP4_v001`
  - `CG_F_REF_RP4_v001`
- final branch:
  - `MPFB_COGLING_COMPACT_BRANCH_v001`
- c1 source:
  - `CGJ7`
- c2 technical anchor:
  - `CGF91-NAT`
- canonical min:
  - `CG76H-NAT`
- max:
  - `CG107-NAT`
- no geometry changed during freeze closure;
- raw and adjusted validator histories preserved;
- raw and adjusted T-7 histories preserved;
- c2 residual preserved as accepted;
- Cogling is closed;
- Saurin is next but NOT started in this order.

Mark the previous READY FOR AUTHOR FREEZE state as superseded.

---

# 13. Immutable verification

Re-hash and verify unchanged:

- MPFB Family Base v005;
- frozen Durrim RP4 branch and production refs;
- frozen Pipkin RP4 branch and production refs;
- Marchfolk;
- Skarn;
- Sagekin;
- Fenn;
- Aelari;
- Vael;
- Halvren;
- accepted Cogling sources;
- CG76-NAT provenance;
- CGF91-NAT anchor;
- all existing freeze records.

No frozen race may change.

---

# 14. Production copy

If the PC production path is available, copy the frozen Cogling production package to:

`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Cogling/RP4/`

Include:
- both .blend files;
- sidecars;
- branch maps;
- landmarks;
- freeze record;
- any required branch definition/read-back record normally stored with the production package.

Verify byte identity.

If the PC is not reachable, record the copy as pending without blocking repository freeze closure.

---

# 15. Final closure report

Return one concise report with:

- final freeze record path;
- c1/c2 file hashes;
- c1/c2 geometry hashes;
- topology hash;
- branch definition/map hashes;
- raw and adjusted validator summary;
- raw and adjusted 76 cm T-7 summary;
- c2 residual status;
- read-back result;
- immutable verification;
- production-copy status;
- accepted notes;
- status/canon/handoff updates;
- exact final state:

**COGLING RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

---

# 16. STOP CONDITION

Do not:
- modify Cogling geometry;
- modify Cogling feet;
- revise the thumb branch;
- alter global D4;
- alter global T-7;
- begin Saurin;
- begin rig finalization;
- begin character creator implementation;
- begin UE5 integration.

Complete only the record/status/canon/handoff freeze closure and **STOP FOR CHATGPT REVIEW**.

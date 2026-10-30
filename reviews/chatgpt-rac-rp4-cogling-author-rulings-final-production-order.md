# ChatGPT Order — RAC RP4 Cogling Author Rulings + Final Production Candidate Gate

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Reviewed Claude commit:** `6952ac1f3881d0515e64ce561dd90a38ad3e19d5`  
**Parent order:** `reviews/chatgpt-rac-rp4-cogling-independent-compact-diagnosis-order.md`  
**Scope:** authorize Cogling-specific validator/T-7 rulings, accept the c2 anchor residual, create final production candidates, run freeze-readiness  
**Stop condition:** complete the final Cogling production gate and STOP FOR CHATGPT REVIEW. Do not freeze.

---

# 1. Author ruling on current Cogling state

The following are accepted and must not be reopened:

- `CGJ7` c1 central source;
- `CG76H-NAT` canonical 76 cm minimum;
- `CG107-NAT` maximum;
- `CGF91-NAT` c2 technical central anchor;
- `MPFB_COGLING_COMPACT_BRANCH_v001`;
- Cogling-specific thumb MCP solution;
- no Durrim jaw-neck reroute;
- no Durrim c2 hip-sector inheritance;
- no face topology addition;
- no foot topology addition;
- no global D4 change;
- no automatic inheritance of the Pipkin exception.

Approved visual/anatomy rulings:
- 76 cm adult-vs-child/toddler firewall PASS;
- 91 / 107 cm Cogling-vs-Pipkin overlap PASS;
- Cogling-vs-Durrim context PASS;
- normalized Marchfolk firewall PASS;
- hands-hidden and head/hands/feet-hidden firewalls PASS;
- deformation/contact PASS;
- no anatomy exaggeration is authorized.

---

# 2. Cogling toe-station validator exception — APPROVED

Approve a **Cogling-specific validator-geometry exception** for the same D4 double-scaling measurement class independently demonstrated on Cogling.

Affected bodies:
- `CG76H-NAT`
- `CGJ7`
- `CG107-NAT`

Affected stations only:
- `toe3_j1_l`
- `toe3_j1_r`
- `toe4_j1_l`
- `toe4_j1_r`

The exception may apply only when all of the following are true:

1. the raw authoritative D1+D3+D4+D5+D6 status is `FAIL_LOOPS`;
2. the station is in `closed_ring_fallback`;
3. there are no crease poles;
4. the size-consistent toe-probe diagnostic passes;
5. no foot topology has been added to satisfy the measurement.

Use a Cogling-specific status label, e.g.:

`PASS_COGLING_TOE_PROBE_GEOMETRY_EXCEPTION`

or a project-consistent equivalent.

Do **not**:
- reuse the Pipkin status label;
- create a universal compact-race exception;
- change global D4;
- change frozen Pipkin or Durrim;
- add Cogling foot topology.

Preserve raw validator history permanently.

Expected adjusted result:
- CG76H-NAT: 69/69
- CGJ7: 69/69
- CGF91-NAT: 69/69
- CG107-NAT: 69/69

---

# 3. Cogling 76 cm T-7 small-body sampling exception — APPROVED

The fixed 3 px/cm T-7 result on `CG76H-NAT` is accepted as a raster-resolution artifact, not a geometry failure.

Preserve both records:

## Raw authoritative fixed-resolution reading
- profile IoU approximately 0.9931
- below nominal 0.995 threshold

## Scale-consistent small-body reading
Use the existing scale-consistent raster diagnostic:
- front/rear approximately 0.997354
- profiles approximately 0.9980
- PASS

Production status label may use:

`PASS_COGLING_T7_SMALL_BODY_SAMPLING_EXCEPTION`

or a project-consistent equivalent.

Conditions:
1. applies only to the 76 cm Cogling boundary body;
2. raw fixed-resolution T-7 remains stored and visible;
3. scale-consistent result must pass;
4. surface deviation must remain within T-1/T-2;
5. the same raw failure must be present on both v005 and the Cogling branch, proving it is not branch-induced.

Do **not** change the global T-7 standard in this order.

---

# 4. CGF91-NAT c2 narrow-core ratio residual — ACCEPTED

Accept the c2 diagnostic reading where:

`crest / thoracic breadth`

is about +1.1% relative to diagnostic Pipkin c2.

This is **not** interpreted as a Pipkin-like pelvis or a failure of Cogling identity.

Record the cause:

- Cogling c2 crest breadth is still ~5.7–6.1% narrower than Pipkin c2;
- Cogling c2 thorax breadth is ~6.6–7.2% narrower than Pipkin c2;
- the ratio reverses only because the thorax narrows slightly more than the pelvis;
- pelvic vertical / thoracic vertical remains lower than Pipkin by ~9.8%;
- pelvic AP / thoracic depth remains lower by ~4.6%;
- every distal-redistribution and narrow-core carrier remains intact.

Treat this as:

**ACCEPTED C2 TECHNICAL-ANCHOR NARROWER-CORE RATIO RESIDUAL**

Do not modify CGF91-NAT anatomy to force the ratio.

Cogling sex-related anatomy remains OPEN.

---

# 5. Preserve the approved Cogling branch

Use exactly:

`MPFB_COGLING_COMPACT_BRANCH_v001`

Reviewed branch definition hash:
`75ed801f698e78200c8ac3e2891b7f1d4c0459de4c4e6dc117b8629422965a5f`

Branch properties:
- thumb MCP two-direction compact support only;
- no neck reroute;
- no hip sector;
- no toe branch;
- no face branch;
- 58,162 V / 58,160 Q;
- 0 branch quads > 4:1;
- max branch aspect ~3.82;
- deterministic across 76 / 91 c1 / 91 c2 / 107;
- Cogling-specific placement.

Preserve the reviewed branch map / S exactly unless final production read-back exposes a reproducibility defect.

Do not revise branch placement for aesthetic reasons.

---

# 6. Create final production candidates

Create:

- `CG_M_REF_RP4_v001`
- `CG_F_REF_RP4_v001`

or project-consistent equivalents.

Sources:
- c1 = `CGJ7`
- c2 = `CGF91-NAT`

Both must:
- use identical `MPFB_COGLING_COMPACT_BRANCH_v001` topology;
- preserve accepted Cogling anatomy;
- retain source lineage;
- retain branch map;
- retain landmarks;
- retain UVMap;
- carry no per-config topology variation.

Embedded status must clearly say CANDIDATE / NOT FROZEN.

Do not freeze.

---

# 7. Final integrity / topology gate

For both production candidates require:

- one component;
- zero boundary edges;
- zero non-manifold edges / vertices;
- zero degenerate faces;
- outward normals;
- 100% quads;
- identical c1/c2 face topology;
- deterministic branch map;
- read-back faces equal candidate;
- read-back geometry within existing production precision.

Report:
- vertex count;
- quad count;
- file SHA-256;
- geometry hash;
- face topology hash;
- branch definition hash;
- branch-map hash;
- landmark hash.

---

# 8. Final validator record

Preserve both:

## Raw authoritative validator
Unchanged D1+D3+D4+D5+D6 outputs.

Expected raw state:
- CG76H-NAT: 65/69
- CGJ7: 65/69
- CGF91-NAT: 69/69
- CG107-NAT: 65/69

## Author-adjusted Cogling production validator
After the scoped Cogling toe exception:
- CG76H-NAT: 69/69
- CGJ7: 69/69
- CGF91-NAT: 69/69
- CG107-NAT: 69/69

Any failure outside the approved four toe3/toe4 j1 stations remains a blocker.

---

# 9. Final T-7 record

Preserve:
- raw fixed-resolution T-7;
- author-adjusted Cogling small-body verdict.

Expected:
- CGJ7: ordinary T-7 PASS
- CGF91-NAT: ordinary T-7 PASS
- CG107-NAT: ordinary T-7 PASS
- CG76H-NAT: raw fixed 3 px/cm profile ~0.9931, adjusted PASS only through the approved scale-consistent small-body exception

Any new T-7 failure on another body is a blocker.

---

# 10. Final anatomy preservation

Re-run source-vs-production:

- T-1;
- T-2;
- T-3;
- T-6;
- T-7 raw + adjusted record.

Confirm no change to:

- Fine-Scale Elongated Articulation;
- narrow stable central core;
- broadly near-human total limb contribution;
- distal arm redistribution;
- distal leg redistribution;
- long-finger / hand contribution;
- fine skeletal shafts;
- smaller adult joints;
- mature adult pelvis;
- adult head/body relationship;
- 76 cm adult firewall.

No source-anatomy correction is authorized.

---

# 11. Final firewalls

Re-run final production realization evidence for:

## Cogling vs Pipkin
- 91 cm equal height
- 107 cm equal height

Required:
- Cogling narrower core;
- finer skeletal scale;
- distal redistribution;
- longer fingers / greater hand share;
- less Pipkin-style pelvis-led organization.

## Cogling vs Durrim
- 107 Cogling vs 122 Durrim real-height context

## Adult vs child
- 76 cm critical comparison
- 91 cm support comparison

## Marchfolk normalized
Must remain non-uniformly scaled.

## Hidden identity
- hands hidden;
- head + hands + feet hidden.

Cogling identity must not collapse to long fingers alone.

---

# 12. Deformation gate

Run the full 18-pose suite on c1/c2 production candidates.

Run key poses on 76 / 107:
- shoulder;
- elbow;
- wrist flex/ext;
- fist;
- thumb opposition;
- hip flex;
- knee deep flex;
- ankle;
- toe flex/ext;
- trunk twist;
- neck flex/rotation.

Required:
- no new topology class;
- no grip/fist collapse;
- no new long-finger folding class;
- no new foot/toe defect;
- no new wrist/thumb-web failure.

Same-class strain differences are report-only if all fold/flip/contact classes remain unchanged.

---

# 13. Freeze-readiness record

If all gates pass, create:

`reviews/rac-rp4-evidence/cogling/final/COGLING_RP4_FREEZE_CANDIDATE.json`

or project-consistent equivalent.

It must include:

- source lineage;
- c2 anchor provenance;
- branch identity and hash;
- production file hashes;
- geometry hashes;
- topology hash;
- branch maps;
- landmarks;
- raw validator outputs;
- author-adjusted validator outputs;
- Cogling toe-exception record;
- raw and adjusted 76 cm T-7 record;
- accepted c2 ratio residual;
- T-1…T-7 results;
- deformation/contact results;
- firewall results;
- immutable verification.

Do not promote to final freeze.

---

# 14. Accepted notes to carry into candidate record

Record:

1. Cogling c1 toe3/toe4 j1 raw failures are a documented D4 probe-geometry artifact accepted under the Cogling-specific exception.
2. Cogling and Pipkin retain separate exception records; no universal compact-race exception exists yet.
3. Global D4 is unchanged.
4. The 76 cm raw T-7 failure is a fixed-raster sampling artifact; the scale-consistent diagnostic passes and is the accepted production verdict for that boundary body.
5. Global T-7 is unchanged.
6. CGF91-NAT's crest/thorax ratio inversion is an accepted technical-anchor residual caused by the thorax narrowing more than the pelvis; narrow-core and less-pelvis-led anatomy otherwise remain intact.
7. Cogling sex-related anatomy remains OPEN.
8. `MPFB_COGLING_COMPACT_BRANCH_v001` is Cogling-only and is not a universal compact-race branch.

---

# 15. Immutable verification

Verify unchanged:

- MPFB Family Base v005;
- frozen Durrim RP4 branch / production refs;
- frozen Pipkin RP4 branch / production refs;
- Marchfolk;
- Skarn;
- Sagekin;
- Fenn;
- Aelari;
- Vael;
- Halvren;
- accepted Cogling sources;
- CG76-NAT provenance asset;
- all existing freeze records.

No frozen race may change.

---

# 16. Final decision wording

Return exactly one:

## COGLING RP4 FINAL PRODUCTION PASS — READY FOR AUTHOR FREEZE

Use if:
- adjusted validator 69/69 on all four Cogling bodies;
- raw validator history preserved;
- 76 cm T-7 dual record preserved;
- c1/c2 production candidates clean;
- anatomy/firewalls pass;
- deformation passes;
- immutable references unchanged.

### OR

## COGLING RP4 FINAL PRODUCTION NEEDS REVISION — [exact blocker]

### OR

## COGLING RP4 REQUIRES AUTHOR DECISION — [exact unresolved issue]

---

# 17. Required return

Commit:

1. final Cogling production gate report;
2. production c1/c2 files;
3. sidecars;
4. branch maps;
5. landmarks;
6. read-back verification;
7. raw validators;
8. adjusted Cogling validator summary;
9. Cogling toe-exception record;
10. raw + adjusted 76 cm T-7 record;
11. c2 anchor residual record;
12. anatomy/firewall/deformation evidence;
13. final visual boards;
14. immutable hashes;
15. freeze candidate record if PASS;
16. narrow STATUS / handoff update.

---

# 18. STOP CONDITION

Do not:
- freeze Cogling;
- alter global D4;
- alter global T-7;
- add Cogling foot topology;
- revise Cogling anatomy;
- modify frozen Pipkin or Durrim;
- begin Saurin;
- begin rig finalization;
- begin creator implementation;
- begin UE5 integration.

Complete the final Cogling production candidate gate and **STOP FOR CHATGPT REVIEW**.

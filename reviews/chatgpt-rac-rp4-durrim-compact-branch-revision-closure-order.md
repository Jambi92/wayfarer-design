# ChatGPT Order — RAC RP4 Durrim Compact-Branch Revision / Closure Pass

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Reviewed Claude commit:** `372fe20f765fa3a2f8a48ebd61e89979b2414ee4`  
**Parent order:** `reviews/chatgpt-rac-rp4-durrim-compact-branch-pilot-order.md`  
**Scope:** bounded RP4 revision only — thumb MCP topology + jaw/neck pole routing, then resume the original Durrim production gate  
**Stop condition:** complete the bounded fixes and the resumed RP4 validation package, then STOP FOR CHATGPT REVIEW.

---

# 1. Author ruling on the first RP4 return

The following are accepted and must not be reopened:

- `DU137C-NAT` accepted c1 central source;
- `DUF137C-NAT` configuration-2 central technical anchor;
- accepted Durrim W2H1 anatomy;
- D1 pelvic correction: pelvis Z ×1.04;
- stature envelope 122–152 cm;
- Durrim-specific frame semantics;
- compact structural identity;
- current source allometry;
- current craniofacial / adult-read direction;
- non-elven humanoid ear foundation;
- all immutable MPFB / frozen-race inputs.

The first compact prototype `MPFB_COMPACT_BRANCH_v001` is **REJECTED as a final branch** because it fixes the thumb MCP loop count by creating excessive T-4 aspect-ratio failures.

Do not use that prototype as the production branch.

---

# 2. Remaining blockers

Exactly two local topology blockers remain.

## A. Thumb MCP support

Current v005 problem:
- every Durrim test body fails thumb MCP loop support;
- v005 gives only 1–2 usable rings where 3 are required.

The rejected prototype proves that extra local topology is needed, but its one-direction strip subdivision creates:
- about 100–105 quads over 4:1;
- max aspect about 9.3:1.

Required fix:
- replace the rejected one-direction ring insertion with a **two-direction local densification**;
- add the needed longitudinal MCP support;
- also add circumferential support so the new cells remain reasonably shaped;
- transitions must be local, valence-controlled, and outside the active crease band where possible.

## B. Jaw / neck pole placement

Current v005 problem:
- submandibular valence-5 poles 5299 / 11904 enter the neck crease band on c1 137 and c1 152;
- this produces `FAIL_CREASE_POLE` despite clean neck deformation;
- c1 122, c2 137 and Marchfolk 152 pass.

Author ruling:
- do **not** accept this as a carry-forward;
- authorize a **minimal local jaw–neck topology reroute** so the pole pair leaves the active neck crease band.

This is a topology-flow correction only.

Do not change:
- Durrim jaw silhouette;
- chin;
- mandibular breadth/depth;
- neck length;
- neck circumference;
- head-neck integration;
- craniofacial identity.

---

# 3. New branch target

Create a revised compact branch candidate.

Suggested identity:

`MPFB_COMPACT_BRANCH_v002`

or project-consistent equivalent.

It must contain only:

1. thumb MCP local branch refinement;
2. jaw–neck pole-routing refinement.

No other topology expansion is authorized.

---

# 4. Thumb MCP v002 requirements

## 4.1 Local topology design

Use the rejected prototype only as diagnostic evidence.

Design a clean local patch around each thumb MCP that provides:

- at least 3 firm anatomical support rings at every tested Durrim stature/config;
- no long sliver strip;
- no local face tunnel;
- no crease pole introduced into the MCP band;
- no high-valence concentration directly on the active joint crease.

Preferred architecture:
- longitudinal support rings;
- circumferential split/support;
- controlled transition fans or grid transitions outside the active MCP deformation zone.

Do not densify the entire hand.

## 4.2 Quality gate

Target:
- quad aspect ≤4:1 where practical;
- no systematic strip above 4:1;
- any unavoidable >4:1 faces must be few, local, outside the MCP crease core, and explicitly justified.

Hard reject if:
- the new patch recreates ~100+ aspect failures;
- max aspect remains near the rejected 9.3:1 class;
- thumb silhouette or palm anatomy changes visibly.

## 4.3 Validator gate

For:
- DU122C-NAT;
- DU137C-NAT;
- DU152C-NAT;
- DUF137C-NAT;

require:
- thumb_mcp_l PASS;
- thumb_mcp_r PASS;
- minimum margin ≥0 preferred;
- no new D3/D5 pole attribution failure.

---

# 5. Jaw–neck pole reroute requirements

## 5.1 Exact scope

Correct only the local topology around the v005 submandibular pole pair corresponding to:
- 5299;
- 11904;
and their immediately necessary surrounding faces/loops.

The goal is to move the topology singularity out of the neck-station crease band while preserving the same Durrim surface.

## 5.2 Required geometric behavior

For c1 137 and c1 152:
- no neck `FAIL_CREASE_POLE`;
- pole offset must clear the active crease band with a useful margin, not merely epsilon;
- preferably ≥1.0 local edge-height unit outside the forbidden band.

Also verify:
- c1 122 remains pass;
- c2 137 remains pass;
- Marchfolk 152 regression remains clean if the shared branch topology is applied diagnostically.

## 5.3 Surface preservation

The local reroute must stay within:
- T-1 body tolerance;
- T-2 identity-zone tolerance if the jaw/face zone is counted;
- silhouette unchanged at normal review scale.

No change to Durrim facial identity is permitted.

## 5.4 Deformation

Re-run:
- neck_flex30;
- neck_rot45;
- any standard neck/head pose in the family suite.

Required:
- no new flips;
- no new self-intersections;
- no new folds attributable to the reroute.

---

# 6. Branch mapping / reproducibility

The revised branch must have a documented map from MPFB Family Base v005.

Required:
- parent v005 vertex order preserved outside branch zones;
- new vertices appended or otherwise mapped deterministically;
- branch map/version recorded;
- UV interpolation path recorded;
- source-weight transfer path recorded;
- morph/target transfer compatibility recorded;
- c1 and c2 share the exact same revised compact topology;
- rebuild produces identical face list / branch map.

Do not encode Durrim shape into the branch.

The branch is technical support topology only.

---

# 7. Re-run compact branch on all Durrim test bodies

Apply v002 to:

- DU122C-NAT;
- DU137C-NAT;
- DU152C-NAT;
- DUF137C-NAT.

For each return:

- integrity;
- topology counts;
- T-1 / T-2 / T-3 / T-4 / T-5 / T-6 / T-7;
- validator D1+D3+D4+D5+D6;
- density;
- contact;
- deformation;
- source surface regression.

Boundary behavior must remain coherent across 122 / 137 / 152 cm.

---

# 8. 69/69 validator is now mandatory

The revised branch is not acceptable unless the central production candidates achieve:

- **69 / 69 firm PASS c1**
- **69 / 69 firm PASS c2**

Also require:
- DU122C branch diagnostic: 69 / 69;
- DU152C branch diagnostic: 69 / 69.

If another station fails:
- diagnose whether it is true topology or validator geometry;
- do not broaden the branch casually.

---

# 9. Resume production candidates after branch passes

Once v002 passes the topology gates, create:

- `DU_M_REF_RP4_v001`
- `DU_F_REF_RP4_v001`

or project-consistent equivalents.

Both must:
- use the same v002 compact topology;
- use the accepted c1 / c2 central sources;
- preserve Durrim source anatomy;
- contain no per-config topology variation.

Do not freeze automatically.

---

# 10. Full anatomy / identity regression

Re-run the original RP4 Durrim gates.

Required:

## Body / pelvis
- torso share;
- thoracic breadth/depth;
- DU-P2a / P2b / P3 / P4 / P5 / P6;
- arm / leg shares;
- structural joints / shafts;
- hands / feet;
- head share.

## Face
- adult read;
- compact craniofacial identity;
- head-neck integration;
- no giant-nose / heavy-jaw dependency;
- ears hidden test.

## Equal-height 152 cm
- corrected Durrim 152 vs accepted Marchfolk 152;
- Sagekin 152 as context;
- neutralized presentation.

## Adult-read
- bald;
- clean-shaven;
- ears hidden;
- neutral expression.

No cultural cues.

---

# 11. Face / hand / foot density gate

Re-run compact-density analysis after v002.

The goal is not arbitrary densification.

Confirm:

- face creator-density mean/p95;
- hand/palm/wrist;
- MCP/IP;
- foot/heel/forefoot;
- ball/toes;
- branch-zone edge quality.

Explicitly show:
- unbranched v005;
- rejected v001 prototype;
- revised v002.

The v002 branch should clearly solve the actual support problem without a large face-quality penalty.

---

# 12. Deformation gate

Run the full standard family suite on c1 / c2 production candidates.

At minimum:

- shoulder abd45 / abd90 / flex90;
- elbow90 / elbow130;
- wrist flex / ext;
- fist;
- thumb opposition;
- hip flex90;
- knee90 / 140;
- ankle dorsiflexion;
- toe flex / ext;
- trunk twist;
- neck flex / rotation.

Compare:
- native/source;
- unbranched v005;
- compact v002.

Required:
- no new topology-class failure;
- thumb patch does not create grip/fist collapse;
- jaw-neck reroute remains clean in neck poses.

---

# 13. 152 cm permanent comparison

After production candidates exist, produce the missing production comparison board:

- DU152C on compact v002;
- MF152 on family v005;
- optional SG152 context.

Views:
- front;
- front 3/4;
- side;
- pelvis;
- hand;
- foot;
- head.

Confirm the production topology has not weakened the accepted equal-height Durrim identity.

---

# 14. Compact-branch reusability decision

Return a technical assessment of v002.

Separate:

## General compact topology support
Potentially safe to test later on Pipkin / Cogling:
- thumb MCP support concept;
- compact facial density support, if any;
- hand / foot support patterns;
- mapping architecture.

## Durrim-specific
Must not automatically propagate:
- jaw-neck singularity location correction if it is Durrim-position-specific;
- any topology tied to Durrim head/neck proportions;
- Durrim-specific anatomical placement.

Do not propagate anything yet.

---

# 15. Required boards

### A. Thumb MCP revision
For 122 / 137 / c2:
- v005;
- rejected v001;
- v002;
- wire;
- aspect heat;
- validator rings.

### B. Jaw-neck reroute
For 122 / 137 / 152 / c2:
- before / after;
- wire;
- pole positions;
- neck crease band;
- surface deviation heat.

### C. Final central candidates
c1 / c2:
- front;
- 3/4;
- side;
- rear;
- head;
- hand;
- foot;
- pelvis.

### D. 152 cm permanent comparison
Durrim / Marchfolk / optional Sagekin.

### E. Hidden-presentation adult read
bald / clean-shaven / ears hidden.

### F. Deformation stress
worst poses + thumb and neck close-ups.

### G. Boundary stress
122 / 137 / 152 branch topology / density.

---

# 16. Acceptance criteria

Recommend:

**DURRIM RP4 COMPACT BRANCH PASS — READY FOR AUTHOR ACCEPTANCE / FREEZE**

only if all are true:

1. c2 central anchor remains accepted;
2. thumb MCP passes all Durrim bodies;
3. jaw-neck neck-station failure is eliminated;
4. c1 / c2 central candidates are 69 / 69;
5. 122 / 152 branch diagnostics are 69 / 69;
6. T-1…T-7 pass;
7. T-4 quality is materially better than rejected v001;
8. adult-read / hidden-presentation gates pass;
9. DU-P4 remains intact;
10. 152 cm equal-height identity passes;
11. no new topology-class deformation failure;
12. branch mapping is deterministic and reusable;
13. frozen prior races / v005 remain untouched.

Otherwise return:

**DURRIM RP4 COMPACT BRANCH NEEDS REVISION — [exact blocker]**

or

**DURRIM RP4 REQUIRES AUTHOR DECISION — [exact unresolved design choice]**

---

# 17. Required return

Commit:

1. updated `reviews/claude-rac-rp4-durrim-compact-branch-gate.md` or a v002 closure report;
2. `MPFB_COMPACT_BRANCH_v002` definition;
3. branch map / masks / provenance;
4. thumb MCP before/after audits;
5. jaw-neck before/after audits;
6. c1/c2 production candidates;
7. 122/137/152 branch diagnostics;
8. 69-station validators;
9. T-1…T-7;
10. density;
11. deformation;
12. 152 cm production comparison;
13. adult-read / hidden-presentation boards;
14. reusability assessment;
15. immutable hashes;
16. freeze candidate record if PASS;
17. narrow STATUS / handoff update.

---

# 18. STOP CONDITION

Do not:
- freeze Durrim automatically;
- begin Pipkin;
- begin Cogling;
- begin Saurin;
- broaden the compact branch outside the authorized local fixes;
- change accepted Durrim biology;
- begin rig finalization;
- begin UE5;
- begin creator implementation;
- begin hair / clothing / materials.

Complete this revision / closure pass and **STOP FOR CHATGPT REVIEW**.


---

# FINAL AUTHOR ACCEPTANCE / FREEZE CLOSURE (2026-10-30)

ChatGPT / author review of Claude commit `d92e677ca7d36cba4533ae5b53a6991e3a412cbd` is complete.

**Final ruling: DURRIM RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FREEZE APPROVED.**

This supersedes the earlier STOP-for-review state in this order.

## Freeze exactly
- `DU_M_REF_RP4_v001`
- `DU_F_REF_RP4_v001`
- `MPFB_COMPACT_BRANCH_v002`
- c1 source `DU137C-NAT`
- c2 technical anchor `DUF137C-NAT`

No geometry or topology changes are authorized.

Promote:
`reviews/rac-rp4-evidence/durrim/v002/DURRIM_RP4_FREEZE_CANDIDATE.json`

to:
`reviews/rac-rp4-evidence/durrim/v002/DURRIM_RP4_FREEZE.json`

Preserve all reviewed hashes exactly, including:
- DU_M file `556793330ea0997a5a03a748d63f8b69664014932a2e0028ebdf78537a30cf15`
- DU_M geometry `a6ff9218c9e6c53ba15d7b586383a46c2a5d72cbd81913536e15de9c3fd93586`
- DU_F file `797b06d7376ef9b4dcefe31e2c2790c240c78c4954cb05d52ecd758dec1bad9d`
- DU_F geometry `7354b28d8836d9d45ac9d6d6bf38d3db3af8b6ff6d0d62fe2c11f5e8c8036514`
- compact branch definition hash `aef4a30b60d736b77af0fa1f0c7f422dcac17b089b84a64ea446842dac15a9da`

Record final branch counts:
- 58,138 vertices
- 58,136 quads
- identical c1/c2 topology
- 69/69 on DU122C, DU137C, DU152C, and DUF137C

Record these as accepted non-blocking notes:
1. two local jaw-neck quads remain slightly outside the preferred T-4 angle range but are deformation-clean and have no >4:1 aspect failure;
2. the c2 thumb/hip diagnostic clearance is narrow but passing;
3. the 152 cm Durrim/Marchfolk visual distinction is intentionally subtle and the underlying W2H/W2H1 source anatomy remains author accepted.

Update:
- `specs/STATUS.md`
- `specs/durrim/DURRIM_V1.md`
- `reviews/claude-session-handoff.md`
- any normal freeze index/manifest used by the project

Final status text:

**DURRIM RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

Also record:
- Durrim is the completed RP4 compact-branch pilot;
- `MPFB_COMPACT_BRANCH_v002` is accepted for Durrim, but is **not** yet a universal compact-race topology;
- Pipkin is next and must be diagnosed independently before inheriting branch elements.

Do not begin Pipkin, Cogling, Saurin, rig finalization, creator implementation, or engine integration in this closure step.

Complete only the freeze-by-record promotion and status/canon/handoff bookkeeping, then **STOP FOR CHATGPT REVIEW**.

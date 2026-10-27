# RAC RP3 — MPFB Family Base v004 margin-hardening + Marchfolk/Skarn dual-validation order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT review of Claude Skarn propagation return `2f5de617a24f21239d48b4ea8bb1064ec25a0b82`.  
**Parent assets / gates:**  
- frozen Marchfolk family base v003, freeze record `MF_RP3_v003_FREEZE.json`;  
- `reviews/claude-rac-rp3-skarn-family-propagation-gate.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md` (currently draft).

This order authorizes one bounded **family-wide margin-hardening successor** to the frozen Marchfolk v003 base.

The existing v003 family base remains frozen and immutable.  
The new candidate is a **successor family base**, not an edit-in-place.

The goals are:

1. adopt D4 stature-normalized joint validation;
2. correct the posterior-heel mapping margin;
3. add one loop of reusable support margin at the hip and toe-2 / toe-3 root bands;
4. revalidate the successor on **all four accepted Marchfolk + Skarn configurations**;
5. if all four pass, freeze the successor as the active MPFB Family Base and accept the propagation standard for subsequent races.

No other race may begin until this gate returns.

---

# 1. Immutable parents / provenance firewall

Do not modify or overwrite:

## Frozen Marchfolk family base v003
- `MF_M_REF_RP3_retopo_v003.blend`
  - SHA-256 `5b793eda8d4513a31fa018ef095d2eff25821618b297014a243ec472f6e17276`
  - geometry `64ecbff04faf3615e45ee452bc117fc6a49195d9611edb2f1abce64c2f3041da`
- `MF_F_REF_RP3_retopo_v003.blend`
  - SHA-256 `a5d8adfe979e0c6314ddc825062f6f953a24a1288f79c987dff5232ef45dc188`
  - geometry `ebf5829d9e6d98192a1fb2771b48feb8983027b22f8c0875bfe1d9c14b6599d4`
- frozen face topology hash  
  `68f7b6a90a40917e40f2ab191218ab7ae2245d0cb1b1b20ede2fe5b56e5e8262`
- freeze record SHA-256  
  `4af62f81ff4ba55e0396f70397e1e4945739353bc7247bc2ded00b6c12d35ba9`

## Accepted source assets

### Marchfolk config 1
`MF-M-R`
- R-6 SHA-256 `2caaf056fff559c8c2c8b92dd5e2bc751be0c3efd9a98d0f8d4a7052f65be4d7`

### Marchfolk config 2
`MF-F-R`
- R-6 SHA-256 `c254fb4bc47225d90fcf7950514240cd74baace0ee3b48cd4d78fa38d9381761`

### Skarn config 1
`SK208-C1R`
- R-6 SHA-256 `fd8a43d2e6dc6e63f21306755baedd70cfef9151ff2b4fd442ad1a78ed4448d0`
- build SHA-256 `c1c54d286b23e1b3e2f7ad30ba36462fc0b2aaf560364f40fe0f34a4675f5231`

### Skarn config 2
`SKF208`
- R-6 SHA-256 `0245683ec889d36e4d284ad0fe4ae533a3c7ab8ce17c28e46cda92a99769ab4f`
- build SHA-256 `ddf77a849902c1843b825396a4f21272ea66d4d80e1bd78acdecab609d4c377a`

All sources, v001-v003 production files, maps, and freeze records must hash identically before/after.

Stop on mismatch.

---

# 2. AUTHOR DECISION D4 — ACCEPTED

Adopt **stature-normalized station geometry** as part of the standard MPFB-family validator.

Reference stature:

`173.143 cm` = Marchfolk configuration 1 reference stature.

For every race/configuration:

`station_scale = race_stature / 173.143`

Scale the station geometry consistently:

- band width;
- probe radius;
- pole radius;
- ring radius / axial window;
- anatomical fallback radius where appropriate.

D1 and D3 remain accepted and active.

Validator hierarchy:

1. ordinary band method;
2. D1 undefined-side fallback;
3. D3 same-digit pole ownership;
4. D4 stature-normalized station geometry.

Marchfolk must remain 69 / 69 firm PASS under D1 + D3 + D4.

Do not modify geometry merely because an unscaled legacy validator would fail.

---

# 3. Successor family-base version

Create a new family-base successor derived from frozen v003.

Do **not** overwrite or relabel v003.

Recommended race realization names:

- `MF_M_REF_RP3_retopo_v004.blend`
- `MF_F_REF_RP3_retopo_v004.blend`
- `SK_M_REF_RP3_retopo_v002.blend`
- `SK_F_REF_RP3_retopo_v002.blend`

Also create an authoritative family-core manifest, e.g.:

`MPFB_FAMILY_BASE_v004.json`

The exact naming may follow existing project convention, but the new successor must be unambiguous and versioned.

---

# 4. Family-wide correction A — posterior heel mapping margin

The Skarn config-1 T-2 feet miss is:

- max 1.70 mm;
- only 2 mirrored posterior heel vertices;
- inherited from linear face-centre rows;
- Marchfolk config 1 sits at 1.45 mm in the same family rows.

This is a **family-map margin problem**, not Skarn anatomy.

Correct the relevant shared map rows by replacing the off-surface linear quad-centre expression with a deterministic **on-source-surface barycentric representation**.

Requirements:

- topology unchanged by this correction itself;
- same map-row architecture for every family race;
- mirrored left/right construction;
- no heel silhouette change beyond the source fit;
- no sole-contact regression;
- no ankle-loop regression;
- no new foot self-intersections.

### Margin target

For all four Marchfolk/Skarn configurations:

- foot T-2 max <= **1.30 mm preferred**;
- absolute hard limit remains <= 1.50 mm.

If <=1.30 cannot be achieved without another regression, document the best clean value and stop for author review rather than chasing it.

---

# 5. Family-wide correction B — hip support margin

The frozen family base has **5 / 5** hip support at the Marchfolk reference and drops to **4 / 5** on Skarn config 1 under D4.

Add exactly one deterministic mirrored support ring / loop to the family core at the hip band.

The goal is **margin**, not a Skarn-only patch.

Requirements:

- same topology addition in every configuration/race;
- preserve groin, pelvis and gluteal anatomy;
- preserve hip-joint landmark;
- preserve source silhouette;
- no new groin/perineal self-intersections;
- no topology branch.

### Margin target

Under D1+D3+D4:

- Marchfolk reference should have **>= 6 loops** where the contract minimum is 5;
- both Skarn configs must have **>= 5**;
- preferred Skarn margin >=6 if naturally produced without over-density.

Do not add more than one ring in this cycle.

---

# 6. Family-wide correction C — toe-2 / toe-3 root margin

The frozen family base has toe-root j1 bands at exactly **2 / 2** on Marchfolk and drops to **1 / 2** on Skarn.

Add one deterministic mirrored support ring / loop at:

- toe2 MTP/root band;
- toe3 MTP/root band.

Use one shared family topology pattern.

Requirements:

- minimum 2 support loops under D4 on both Marchfolk + Skarn;
- preferred Marchfolk margin >=3;
- no own-digit crease poles;
- D3 adjacent-digit pole scoping still applies;
- preserve toe spacing;
- preserve web geometry;
- preserve MTP positions;
- preserve toe lengths;
- preserve sole/forefoot contact;
- no new foot self-intersections.

Do not add rings to other toes unless the shared transition absolutely requires them; if so, disclose and prove why.

---

# 7. Common topology requirement

The successor family base must be **one topology** shared by:

- Marchfolk M;
- Marchfolk F;
- Skarn M/C1R;
- Skarn F.

Required across all four realizations:

- identical vertex count;
- identical quad count;
- identical face list;
- identical face topology hash;
- identical hm08 → successor map structure;
- identical UV topology;
- identical added-loop architecture.

Race geometry remains fitted to its own accepted source through the common map.

No per-race topology.

No Skarn branch.

---

# 8. Mapping / transfer requirements

Produce:

- frozen-v003 → successor-base map;
- hm08 → successor-base map;
- weight-transfer proof;
- UV-transfer proof;
- MPFB target/morph-transfer proof.

Every successor vertex must have deterministic source provenance.

For new ring vertices:
- define them as deterministic linear/barycentric combinations of the source hm08 topology;
- use the same source-index/mapping structure across all family races.

For corrected heel rows:
- record original map row and new barycentric row.

---

# 9. Anatomy preservation — all four configurations

Rerun independently on:

1. MF-M-R;
2. MF-F-R;
3. SK208-C1R;
4. SKF208.

Required:

- T-1;
- T-2;
- T-3;
- T-7;
- stature;
- bbox;
- source→prod and prod→source;
- head;
- ears;
- hands;
- feet;
- pelvis/groin;
- shoulder;
- silhouette IoU.

### Hard Skarn identity gate

SK208-C1R must preserve the accepted **C1R central face**.

Do not regress toward the pre-C1R or generic Marchfolk/MPFB face.

Return the same identity comparison as the prior Skarn gate.

---

# 10. Contact / self-intersection gate

Compare successor vs frozen v003/frozen-family-fit baseline.

Mandatory:

- no new hand/foot self-intersections caused by the new hip/toe rings or heel mapping;
- no new groin/perineal self-intersections;
- no new toe/web intersections;
- no new sole overlap.

Existing accepted source-contact pairs may remain.

Any new family-base contact defect is a stop condition.

---

# 11. Full 69-station validator — all four configurations

Run:

- legacy for reference only;
- D1 + D3;
- D1 + D3 + D4 authoritative.

For the successor family base, require:

### Firm pass
**69 / 69** in:
- Marchfolk config 1;
- Marchfolk config 2;
- Skarn config 1;
- Skarn config 2.

### Margin report
For every station report:

- loop count;
- contract minimum;
- margin = loops - minimum;
- crease pole;
- same-digit pole ownership;
- fallback mode.

Create a specific **family margin table** highlighting stations with margin 0.

The goal is to reduce zero-margin shared stations before further propagation.

Do not change unrelated geometry in this order if some other margin-0 station is discovered; report it.

---

# 12. Creator density — all four configurations

Re-run all 9 zones.

All must pass.

Because the family topology gains a small number of loops, report:

- new vertex/quad count;
- zone mean edge/stature;
- p95 edge/stature;
- delta vs frozen v003 family topology;
- whether the successor becomes unnecessarily dense for Marchfolk.

Do not decimate.

---

# 13. T-4 quality

The margin-hardening changes must not materially regress T-4.

For Marchfolk and Skarn report:

- angle violations;
- aspect violations;
- union;
- per-zone distribution.

Hard rule:

- global successor T-4 union <= frozen v003 + **0.15 percentage point** for either Marchfolk configuration;
- local hip/toe patches must not create severe new slivers.

If the new support rings worsen local quality, fair them conservatively while staying within anatomy tolerance.

Do not reopen unrelated face/hand T-4 work.

---

# 14. Face / UFCA readiness

Reconfirm on all four:

- mouth rings;
- orbit rings;
- mouth-corner poles;
- eye-region poles;
- open pockets;
- jaw/cheek flow;
- face density.

No face topology is authorized to change.

C1R identity remains hard-gated.

---

# 15. Limited deformation sanity

Run the standard family sanity suite on all four:

- shoulder abd45 / abd90 / flex90;
- elbow 90 / 130;
- wrist flex / ext;
- fist;
- thumb opposition;
- hip flex90;
- knee 90 / 140;
- ankle dorsi;
- toe flex / ext;
- trunk twist;
- neck flex / rotation.

Compare:

- native hm08 source;
- frozen-family fit where available;
- successor-family fit.

Acceptance question:

> Did the successor margin changes create any new topology-class deformation failure?

Do not optimize weights.

Classify:
- topology;
- weights;
- joint placement;
- contact/setup.

---

# 16. Family propagation standard v1 — promotion criteria

Update:

`specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`

If the successor passes on all four configurations:

- change status from **DRAFT** to **AUTHOR-ACCEPTED TECHNICAL STANDARD v1**;
- incorporate D4 as accepted;
- replace known zero-margin warnings with the successor base metrics;
- make the successor family-base hash/manifest authoritative;
- preserve the rule that anatomy/identity review is never automated away.

Standardize the technical pipeline only.

Do not standardize:
- race anatomy judgments;
- face identity judgments;
- ear branches;
- compact-race branches;
- biological creator ranges.

---

# 17. Freeze / supersession logic

If every gate passes:

## Freeze the successor

Freeze the new Marchfolk successor realizations by record and create an authoritative family-base freeze manifest.

Do not delete or alter frozen v003.

Record:

> **v003 = historical accepted MPFB Family Base v1**  
> **successor = active MPFB Family Base v2 / margin-hardened**

Use project-consistent version naming in the actual files.

Then create Skarn freeze candidates on the exact same active family topology.

Do **not** automatically freeze Skarn unless the Skarn gate below passes.

---

# 18. Skarn acceptance decision

After successor validation return exactly one:

### SKARN FAMILY PROPAGATION PASS — READY FOR AUTHOR FREEZE

Use if:
- both Skarn configs use active family topology unchanged;
- C1R identity passes;
- T-1/T-2/T-3/T-7 pass;
- 69/69 firm pass under D1+D3+D4;
- density passes;
- face readiness passes;
- no topology-class deformation failure.

### SKARN NEEDS RACE-SPECIFIC BRANCH

Use only if a true Skarn anatomical feature—not family margin or validator scale—requires topology divergence.

### FAIL

Use only for a new blocking issue.

---

# 19. Required visual evidence

Provide actual images for **Marchfolk and Skarn**, both configurations where relevant:

1. successor family topology overview;
2. heel before/after mapping closeup;
3. hip added-ring closeup;
4. toe2/toe3 root-ring closeup;
5. counted-loop / D4 validator sheet;
6. margin table visualization;
7. source-vs-successor body overlay;
8. Skarn C1R face source vs successor;
9. density heatmaps;
10. T-4 heatmaps;
11. deformation comparison;
12. family topology change diagram.

Do not return the gate without the photos.

---

# 20. Required return

Commit:

1. `reviews/claude-rac-rp3-mpfb-family-base-v004-margin-hardening-gate.md`;
2. successor Marchfolk production files / sidecars;
3. successor Skarn production files / sidecars;
4. active family-base manifest candidate;
5. v003→successor map;
6. hm08→successor map;
7. D4 validator implementation;
8. full 69-station audits for all four;
9. family-margin tables;
10. anatomy audits;
11. contact/self-intersection audits;
12. density audits;
13. T-4 audits;
14. face/C1R audits;
15. deformation sanity;
16. visual sheets;
17. before/after immutable hashes;
18. updated propagation standard draft / accepted version;
19. narrow `specs/STATUS.md` update;
20. session handoff.

The gate must explicitly answer:

- Is D4 implemented and stable on Marchfolk + Skarn?
- Did the heel mapping correction bring Skarn config-1 feet within T-2?
- Did the hip band gain usable margin?
- Did toe2/toe3 roots gain usable margin?
- Are all four configurations on one identical successor topology?
- Do all four have 69/69 firm PASS?
- What zero-margin stations remain?
- Did any new self-intersection/contact defect appear?
- Did all anatomy gates pass?
- Is C1R identity preserved?
- Did density pass?
- Did T-4 stay within the regression budget?
- Did any topology-class deformation failure appear?
- Is the successor ready to freeze as the active MPFB Family Base?
- Is Skarn ready for freeze?
- Is MPFB Family Propagation Standard v1 ready for author acceptance?

---

# 21. Stop rules

After committing the gate:

**STOP FOR CHATGPT REVIEW.**

Do not proceed to:
- Sagekin;
- Fenn;
- Aelari;
- Vael;
- Halvren;
- Durrim;
- Pipkin;
- Cogling;
- family batch propagation;
- production rig finalization;
- creator morph implementation;
- final UV/materials;
- LODs;
- UE5.

---

## FINAL AUTHOR RULING

- D4 stature-normalized station geometry is **ACCEPTED**.
- Skarn does **not** currently justify a Skarn-specific topology branch.
- The exposed heel, hip-band and toe-root issues are **family-base margin issues**.
- Frozen Marchfolk v003 remains immutable historical base.
- One bounded family-wide successor / margin-hardening cycle is authorized.
- The successor must pass Marchfolk + Skarn before it can become the active MPFB family base.
- If it passes, promote the technical propagation workflow to an accepted reusable standard while keeping race-specific anatomy/identity review explicit.

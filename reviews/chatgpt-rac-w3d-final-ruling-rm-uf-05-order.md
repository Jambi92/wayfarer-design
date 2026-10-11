# WAYFARER RAC — W3D FINAL AUTHOR RULING / RM-CF-05 CANON WRITEBACK / RM-UF-05 DIAGNOSTIC ORDER

**Status:** AUTHOR RULING ISSUED; RM-CF-05 MAY BE CANONIZED; W3 MAY CLOSE AFTER WRITEBACK; RM-UF-05 DIAGNOSTIC WORK AUTHORIZED  
**Repository:** Jambi92/wayfarer-design  
**Scope:** reference-anatomy / creator-validation design only; no UE5 implementation  
**Stop condition:** return the RM-UF-05 author gate. Do not proceed into RM-OT-05, posture, equipment, rigging, animation or gameplay.

---

## 1. W3D FINAL AUTHOR RULING

The W3D gate is accepted.

Lock the following:

- **W3C — FINAL ACCEPT**
- **C1R central Skarn face — FINAL ACCEPT**
- **C1R neck correction — ACCEPT at `neck-scale-horiz-incr = 0.30`**
- **Configuration-2 C1R replication — PASS**
- **RM-CF-09 — FINAL CLOSED**
- **Mandibular-body depth — OPEN reference-generator capability gap**
- **Anterior maxillary / true midface depth — OPEN reference-generator capability gap**
- **Body-to-face soft-tissue coupling — OPEN reference-generator capability gap**
- **RM-CF-05 author decision — OPTION B: 0.05 r3 FPI**

Do not reopen accepted Skarn body anatomy.

Historical Skarn W1/W2 assets stay preserved for provenance. The canonical central Skarn facial pointer remains the C1R reference state created in W3D.

---

## 2. SKARN NECK-TO-JAW INTERPRETATION — IMPORTANT AUTHOR CLARIFICATION

The accepted `0.30` neck-width correction is final for the C1R reference construction.

However, the previously observed "more substantial neck-to-jaw transition" is a **central/reference population tendency**, not an invariant numerical clamp that must read as a positive NJT delta against matched Marchfolk on every frame, body-composition state, or sex-related configuration.

Therefore:

- configuration-1 C1R results around +1.7 to +2.0 % NJT are valid evidence of the central tendency;
- configuration 2 and Narrow / low-muscle parity are **not failures** when the absolute Skarn neck remains appropriately substantial and the complete-face/body read remains canon-valid;
- do not widen the neck to 0.50 merely to force an NJT percentage;
- do not create a creator minimum from NJT;
- do not make neck breadth a race-membership test;
- do not alter jaw anatomy to recover a ratio.

Record this clarification wherever W3D/C1R status is summarized.

---

# RM-CF-05 — FINAL AUTHOR DECISION

## 3. CANONICAL MARGIN

Canonize:

> **Required Saurin-to-non-Saurin rostral-projection separation: 0.05 r3 FPI.**

This is a **VAL / DIAG cross-architecture safety margin**, not a player control, not a race classifier, and not a statement of population frequency.

Current accepted comparison state:

- Saurin coupled minimum corner: **r3 FPI 0.29196 (~0.2920)**
- accepted Marchfolk maximum-valid diagnostic: **0.1905**
- demonstrated raw gap: **0.1015**
- conservative gap after the W3D uncertainty allowance: **~0.082**
- accepted required margin: **0.05**

The existing Saurin Part 7 minimum-projection floor **0.255 remains unchanged**.

No accepted comparator is invalidated.

---

## 4. RELATIONAL-CANON FIREWALL

The 0.05 value is relational canon.

It means:

> For any non-Saurin face being proposed as a valid maximum-projection member of its population, the accepted Saurin minimum-valid rostral architecture must remain separated from that comparator by at least 0.05 r3 FPI under the accepted comparison convention and uncertainty rules.

It does **not** mean that 0.242 is an eternal universal non-Saurin hard ceiling.

At the current Saurin minimum:

> 0.29196 − 0.05 = **0.24196**

This is the **current operational comparison limit** only.

If a future legitimately authored Grask, Gorrund, Marchfolk configuration-2, elf, Halvren, Durrim, Pipkin, Cogling, Sagekin, or other non-Saurin maximum-valid face exceeds that current operational limit or reduces the margin below 0.05:

1. do **not** automatically invalidate the race;
2. do **not** silently clip its creator envelope;
3. do **not** automatically raise the Saurin Part 7 floor;
4. do **not** weaken or delete the 0.05 margin;
5. mark the case **AUTHOR REVIEW REQUIRED — RM-CF-05 COLLISION**;
6. return the competing accepted anatomy and uncertainty package for an explicit author decision.

A later author ruling may adjust one of the involved authored envelopes or the margin, but no automatic solver may decide that.

This rule is specifically intended to prevent incomplete current comparator sampling from silently becoming permanent anatomy canon.

---

## 5. RM-CF-05 WRITEBACK

Update all authoritative cross-links that still say the FPI margin is unset or pending.

At minimum inspect and update, where applicable:

- `decisions/REFERENCE_ANATOMY_V1.md`
- `decisions/UFCA_V1.md`
- `reviews/claude-ufca-06-validation-framework.md`
- `reviews/claude-pass2-r5-reference-mesh-queue.md`
- `specs/STATUS.md`
- `specs/saurin/SAURIN_V1.md`
- any RM-CF-01…05 closure / decision register that currently marks the margin OPEN or provisional

Required writeback concepts:

- RM-CF-05 = **FINAL CLOSED**
- margin = **0.05 r3 FPI**
- Saurin Part 7 floor = **unchanged**
- current operational non-Saurin comparison limit = **0.24196**, explicitly conditional on the current Saurin minimum
- future comparator collision = **author-review trigger**, not automatic clipping
- the margin is VAL/DIAG only
- FPI remains one diagnostic dimension, never a species membership test
- the accepted W3D uncertainty note remains attached: precision is meaningful to hundredths, not thousandths

Do not overwrite historical reports. Add closure/writeback status.

---

## 6. W3 CLOSURE

After successful writeback:

- mark **RAC W3 FINAL CLOSED**
- preserve W3A/W3A1, W3B/W3B1, W3C and W3D evidence
- preserve all named OPEN generator capability gaps
- preserve all PD-1…PD-4 Saurin production dependencies as OPEN
- preserve GR-FACE-14 and GOR-FACE-05 as NOT DEMONSTRATED until they are actually built / accepted
- preserve all other unmeasured maximum-valid facial envelopes as NOT DEMONSTRATED

W3 closure does not authorize UE5 implementation.

---

# NEXT BLOCK — RM-UF-05
## Batch diversity / anti-convergence threshold

This is the next authorized RAC block.

The objective is to resolve the **measurement-deferred UFCA Tier-G batch-diversity validator** without inventing population frequencies, creator ranges, or implementation details.

---

## 7. RM-UF-05 PURPOSE

Determine a defensible diagnostic threshold / method for answering:

> Is a generated face batch genuinely diverse across the population's authorized facial anatomy, or is it collapsing toward clones, a small number of stereotyped bundles, a generic human/elf/half-elf face, or a single “ideal” face?

This is a **batch validator**.

It is not:

- a beauty metric;
- an attractiveness metric;
- a race-recognition score;
- a demand that every individual be maximally different;
- a requirement for equal use of every valid phenotype;
- a substitute for race-specific anatomy validators;
- permission to invent missing biological ranges;
- a production generator implementation.

---

## 8. AUTHORITATIVE RULES TO PRESERVE

Use the final UFCA rules without reinterpretation:

- face presets are ordinary valid appearance records;
- no preset-only anatomy;
- no stereotype bundles;
- randomization runs through population envelope -> SOFT/LAT drivers -> dependencies -> validators -> reject/resample invalid results -> batch diversity check;
- never “roll everything and repair”;
- Subtle / Diverse / Extreme affect sampling emphasis only and never unlock invalid anatomy;
- rare valid phenotypes remain manually creatable;
- generation frequencies are **OPEN** unless independently authored;
- seed + generator version + distribution version must reproduce an event;
- biological, Presentation and Acquired-History passes stay separate;
- no surface, hair, pigmentation, scars, cosmetics, grooming, expression or cultural presentation may compensate for structural convergence;
- Sagekin identity is population-statistical where canon says so;
- elf-family distinctions must survive population-level sampling;
- Halvren must not collapse into generic 50/50 “half-elf,” generic beauty, or one source midpoint;
- race-specific Tier-G tests remain authoritative.

---

## 9. DO NOT INVENT DISTRIBUTIONS

This firewall is mandatory.

A batch-diversity threshold cannot be derived by pretending every current DIR has a fully authored probability distribution.

For every population and every DIR/SOFT contributor, classify the source as:

- **NUMERIC VALID RANGE AUTHOR-ACCEPTED**
- **NAMED ACCEPTED ANCHORS / EXTREMES ONLY**
- **QUALITATIVE RANGE ONLY**
- **CENTRAL VALUE ONLY**
- **FREQUENCY AUTHORED**
- **FREQUENCY OPEN**
- **NOT DEMONSTRATED**

Do not turn qualitative words into numeric ranges.

Do not assume Gaussian, uniform, beta, normal, or any other biological distribution unless canon explicitly establishes it.

Diagnostic sampling may use a deliberately artificial coverage design, but it must be labelled **DIAGNOSTIC COVERAGE SAMPLING — NOT POPULATION FREQUENCY**.

---

## 10. BUILD A NORMALIZED FACIAL-DIVERSITY REPRESENTATION

RM-UF-05 calls for distance over DIR vectors. Define the representation carefully.

### Required principles

1. Only authorized **structural biological facial DIR values** participate in the core numeric diversity vector.
2. DER values may be reported for validation but may not double-count their parent DIR.
3. SOFT systemic inputs may be reported separately; do not count the same anatomical effect twice.
4. LAT values are generation-only and do not belong in the saved anatomical distance vector unless the distance is specifically a latent diagnostic.
5. PRES, hair styling, pigmentation presentation, cosmetics, scars and acquired history are excluded from the core structural distance.
6. VAL / DIAG indices such as FPI, MPI, MdPI, CBH, ORB, IOD, etc. are validators / observations and must not become artificial DIR axes.
7. Bound-locked anatomy is not a player-diversity axis.

### Normalization

Where an author-accepted numeric valid interval exists, normalize that DIR to its accepted biological span.

Where only accepted anchors/extremes exist, Claude may construct a **diagnostic anchor scale** for comparison but must not call it a creator interval.

Where no defensible span exists, mark the dimension **UNSCALED / EXCLUDED FROM NUMERIC THRESHOLD**, and report the coverage loss.

Do not hide missing coverage by assigning arbitrary min/max values.

---

## 11. SLOT-BALANCED DISTANCE

Test at least two candidate distance constructions:

### D1 — flat normalized DIR RMS
RMS / Euclidean distance over all available normalized DIR axes.

### D2 — UFCA-slot-balanced distance
First compute within-slot normalized distance; then combine slots with equal slot weight, so a population with many controls in one region does not make that region dominate the batch metric.

If useful, Claude may test one additional robust formulation (for example median-slot distance), but do not proliferate metrics unnecessarily.

Return which construction is most stable across populations with very different control counts.

Do not canonize a distance formula before the author gate.

---

## 12. REQUIRED BATCHES

For every population where the currently demonstrated control coverage supports it, run deterministic diagnostic batches.

Preferred minimum:

- **N = 256** per tested batch condition;
- at least **4 deterministic seeds / coverage designs** per population;
- use exactly reproducible manifests.

Where full sampling is impossible because ranges are OPEN, do not fake a batch. Use the largest defensible anchor-derived batch and mark the result **CONSTRAINED / NOT FULLY CALIBRATABLE**.

### Conditions

At minimum test:

- central / accepted reference concentration;
- broad diagnostic coverage of the currently demonstrated valid space;
- deliberately convergence-biased batch;
- deliberately stereotype/cliché-biased batch where the race has an explicit canonical anti-stereotype rule.

These are validator stress tests, not claims about production frequencies.

---

## 13. TIER-G CARRIED TESTS

Re-run / map the existing Tier-G population tests wherever the current assets permit.

At minimum preserve the logic of:

- Marchfolk — identity stress / randomization sample
- Sagekin — clone / stereotype
- Fenn — population randomization
- Aelari — generic-elf convergence
- Vael — cliché convergence
- Halvren — anti-generic-half-elf, anti-beauty, anti-50/50, family-source tests
- Durrim — population sampling
- Grask — biological diversity / anti-caricature
- Gorrund — minimum-stereotype / biological diversity
- Pipkin — existing integration diversity test
- Cogling — surface/creator anti-convergence tests, but structural score cannot be rescued by surface
- Saurin — existing creator/randomization anti-convergence tests

Skarn now uses the accepted C1R central face and the permanent overlap validators from W3C.

Do not replace any race-specific Tier-G test with the generic metric. The generic metric supplements them.

---

## 14. CLICHÉ-BUNDLE / CORRELATION TEST

A batch can have high pairwise distance and still collapse onto a stereotype if the same regional features are strongly correlated.

Therefore RM-UF-05 must include a separate **bundle-convergence** diagnostic.

For each population:

1. identify only cliché / stereotype bundles already prohibited or clearly implied by canon;
2. do not invent cultural stereotypes;
3. test whether independent or softly related regions collapse into one repeated combination;
4. measure correlation / concentration around the forbidden bundle separately from pairwise distance;
5. preserve legitimate biological coupling — a required FOLLOW/CLAMP relation is not a stereotype correlation.

Examples include, only where already canon-supported:

- generic elf convergence;
- generic half-elf midpoint / 50-50 convergence;
- Skarn “mandatory Viking face” convergence;
- Grask / Gorrund caricature convergence;
- juvenile-large-eye convergence for Pipkin / Cogling;
- a single “idealized attractive” Halvren face.

No new stereotype canon is authorized by this order.

---

## 15. ANTI-CLONE METRICS TO RETURN

For each supported batch, report at least:

- nearest-neighbour distance distribution;
- median nearest-neighbour distance;
- 5th-percentile nearest-neighbour distance;
- fraction of pairs / samples below candidate near-clone thresholds;
- effective number of occupied structural regions / clusters, if a defensible cluster method can be used without inventing biology;
- slot-wise variance / coverage;
- the most converged UFCA slot;
- the most common repeated multi-slot bundle;
- race-specific Tier-G pass/fail;
- cliché-bundle pass/fail.

Do not use image-embedding similarity as the sole authority. If used, it is secondary DIAG evidence only.

---

## 16. THRESHOLD OPTIONS — AUTHOR DECISION REQUIRED

Return at least three threshold policies:

### Option A — permissive anti-clone floor
Catches obvious duplicate / near-duplicate batches while tolerating substantial central clustering.

### Option B — robust anti-convergence rule
Recommended if evidence supports it: protects against clones and repeated stereotype bundles without requiring uniform population coverage.

### Option C — aggressive diversity floor
Forces broad structural spread; report whether it would incorrectly reject valid centrally concentrated or statistically defined populations.

For each option state:

- exact metric formula;
- threshold value(s);
- batch-size assumptions;
- coverage prerequisites;
- races that pass;
- races that are constrained because their valid ranges/frequencies are incomplete;
- false-positive risk;
- false-negative risk;
- whether it would distort Sagekin, elf-family, Halvren or other statistical identities;
- whether it accidentally converts OPEN frequency questions into canon.

Claude may recommend an option but may not canonize it.

---

## 17. VISUAL EVIDENCE

Produce compact comparison sheets for at least:

1. one obviously healthy diverse batch;
2. one near-clone failure batch;
3. one stereotype/cliché-bundle failure batch;
4. one statistically sensitive population case (Sagekin or an elf population);
5. Halvren anti-50/50 / source-passing example;
6. Skarn C1R batch showing central tendency without mandatory heavy-brow / square-jaw convergence.

Use N3/N4 neutralization where required so presentation cannot carry diversity.

---

## 18. REQUIRED GATE

Return:

**`reviews/claude-rac-rm-uf-05-diversity-author-gate.md`**

It must explicitly state:

- **RM-CF-05 writeback — COMPLETE / CONSTRAINED / FAIL**
- **RM-CF-05 = 0.05 r3 — recorded YES / NO**
- **Saurin Part 7 floor changed — expected NO**
- **W3 — FINAL CLOSED / STILL OPEN**
- **C1R pointer preserved — YES / NO**
- **RM-UF-05 evidence coverage by population**
- **D1 result**
- **D2 result**
- **recommended metric**
- **Option A threshold**
- **Option B threshold**
- **Option C threshold**
- **Claude recommendation — advisory only**
- **race-specific Tier-G regressions — list**
- **cliché-bundle regressions — list**
- **frequency assumptions introduced — expected NONE**
- **invented creator bounds introduced — expected NONE**
- **author decision required — YES**

Also list every persistent file changed.

---

## 19. STOP CONDITION

STOP after the RM-UF-05 author gate.

Do not begin:

- RM-UF-05 final canonization;
- RM-OT-05 world-scale distributions;
- posture;
- equipment;
- UE5 creator implementation;
- MetaHuman integration;
- rigging;
- animation;
- gameplay.

Return the diversity-threshold evidence and options for author review.

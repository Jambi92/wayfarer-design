# UFCA-04: Race-Specific Exception Map

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ufca-phase1-order.md` §8
**Status:** PROPOSAL for author review.

**Rule for this map:** an exception is solved in the slot binding, the control set or the validators. It is never solved by hiding anatomy in presets (order §8). Every exception below stays reachable in Advanced Mode, within that race's validity.

## 1. Exception matrix (slot × race)

How to read it:
- **=** means the shared variable set applies, with race envelopes and validators.
- A described cell means the binding differs.
- **A** means the slot is absent (hidden).
- **L** means anatomy exists but the control is locked or not authorized.

| Slot | Human family (MF, SK, SG) | Elves (FN, AE, VA) | HV | DU | GR | GO | PK | CG | SA |
|---|---|---|---|---|---|---|---|---|---|
| 1 Head & Proportions | = | = | = | Head contributes somewhat more; never oversized | Ratio OPEN | Ratio OPEN; anti-"tiny-head giant" | **Anti-juvenile**: head share never identity | **Anti-juvenile**; 11–13 cm head; camera, not enlargement | **Head scale DIR ±8 %** |
| 2 Cranium & Forehead | = | Elven cranial tendencies (ECR) | Inherited, no interpolation | CBH tendency | Vault "needs validation" | CBH tendency; part of TSC | IMFA cranial base | FSPI face-to-vault | **No vertical forehead**; structural ridge (non-zero floor) |
| 3 Brow & Orbit | = | Orbit ≠ visible presentation (ECR L141) | Four separate eye systems | Structural depth ≠ deep-set look | Orbit ≠ opening | Orbit ≠ opening; spacing envelope tied to cranial breadth | No infant orbits | Orbit ≠ opening | **Orbit-coupled set; spacing L** |
| 4a External Eye | = | AE longer/narrower; FN more open (tendencies) | Source-shifted probabilities | = | = | = | **Aperture ceiling**, no enlarged-eye envelope | **Aperture cannot be enlarged** | Inside orbit coupling |
| 4b Ocular | Round pupil (SILENT) | Round = baseline; VA low-light **L/OPEN** | Iris never averaged; pupil OPEN | Low-light not granted | Low-light, sclera **L/OPEN** | Low-light, sclera **L/OPEN** | = | No iris enlargement | **Vertical pupil (species)**; dilation range DIR; membrane **L** |
| 5 Cheeks & Midface | = | Elf tendencies | Inherited | **Midface depth = major identifier** | **Midface verticality = identifier**; projection **L** (OPEN) | TSC; projection **L** (OPEN) | Mature midface, **not shortened** | Not shortened | **Rostrum & Lateral Face**; no zygoma; FPI floor |
| 6 Nose | = | No "small elf nose" | No half-elf nose | **Nose never identifies**; no Nose Size | No Nose Size | No ogre nose | Small/upturned not a trait | No button nose | **Nasal Openings**; no pyramid |
| 7 Mouth | = | = | = | = | = | No exposed teeth at neutral | = | No permanent smile | **Mouth Line**; no lips |
| 8 Jaw & Chin | = | Lighter mass vs robust humans; strong jaws valid | Two jaw mechanisms (VA ≠ SK) | Skeleton ≠ muscle ≠ fat ≠ beard | Vertical ramus | Posterior jaw in TSC | Mature, not heavy | Fine, not weak | **Jaw**; chin **A**; coupled to rostrum |
| 9 Ears | Human auricle | Elven taper | **Mixed coupled** | Human-like | **Folded late-taper** | **Deep bowl** | **Compact rounded** | **Fine folded** (close view) | **Recessed opening** |
| 10 Hair / Display | Hair | Hair | Hair | Hair | Hair | Hair | Hair | Hair | **Cranial Display** |
| 11 Facial Hair & Brows | = | = | = | **Zero identity info** | Zero required | Zero required | = | = | **A** |
| 12 Skin & Surface | = | VA lighting invariance (now universal, ECR) | = | No faked depth | No warts | No warts | = | No readability exaggeration | **Scale fields, no global size** |
| 13 Asymmetry | = | = | Never deformity | = | = | = | **AC-U3** (spec silent) | = | Includes ridge/display; natural ≠ acquired |
| Sex (soft) | No shift | No shift | Separate; Class B dependency | OPEN | OPEN | OPEN | Allowed; magnitude OPEN | Allowed; magnitude OPEN | **None (closed)** |

## 2. Required inspections (order §8)

### 2.1 Human-family facial architecture (MF, SK, SG)

- **Shared:** all three use the full human slot set, the human auricle (MF L307, with the AC-4 pointers at SK L160 and SG L149) and human ocular anatomy.
- **Where they differ:**
  - **MF** is the reference distribution (breadth, not a feature).
  - **SK** carries robust tendencies that are never mandatory (L145–154). RM-CF-09 will quantify them later.
  - **SG** identity is **statistical**. Individual overlap with MF is accepted (SG-10; L195).
- **Exception:** none at the control level. The difference lies in **envelopes and SOFT distributions**, and in **validators**:
  - SK uses a per-individual equal-height test (L288).
  - SG uses a large-sample test (L356). SG's B-tier test is population-level, not per individual (UFCA-06 §2.B).
- **Guard:** "Race changes the supported ranges, not how the editor works" (SK L158). The architecture keeps this.

### 2.2 Shared elven family versus Fenn / Aelari / Vael

- **Shared:** one elven ear family (continuous taper; ECR L104) with one variable list:
  - length, base width, tip length and sharpness, vertical angle, sweep, lateral projection, curvature, lobe.
  - The list is common, but the **ranges and morphs are not identical** (ECR L104).
- **Differences**, as SOFT distributions and envelopes per race, not as different controls:
  - **FN:** greatest average lateral ear projection; compact face; more open visible presentation.
  - **AE:** facial verticality; longer, narrower visible eyes; upward/backward ears.
  - **VA:** compact vertical distribution; midface and mandibular presence; broader ear base.
- **Exception at the ocular level:** Vael low-light adaptation is a Vael-only candidate system with its mechanism OPEN (ECR L100). Slot 4b shows **no** low-light control for any elf. Vael validators keep the low-light lighting test set (VA L272).
- **Guard:** no single "Elf Head" with superficial morphs unless prototyping proves it reproduces the approved diversity (ECR L77). This is a technical constraint carried to implementation.

### 2.3 Halvren mixed craniofacial inheritance

Halvren are the one race whose valid envelope is **conditional on another input** (genealogy).

| Layer | Architecture |
|---|---|
| A. Genealogy | Lineage step, outside the face tree. Optional. Never an appearance slider (HV L463) |
| B. Ancestry-derived constraints | VAL envelopes per slot, computed from A and the source specs. Coupling uses the inheritance clusters (craniofacial; ear) as LAT, never as sliders (L33–41) |
| C. Phenotype | Ordinary DIR controls in every slot, valid inside B |

**Ears:** the Halvren family is a **union parameter set**: human foundation variables (root, helix, antihelix, concha, tragus, lobe) plus elven variables (length, taper, sweep, projection), all coupled (L198). It is **not** a pointiness interpolation.

**Source-race protection:** a whole-face VAL rejects any complete configuration that reproduces a source population's full craniofacial distribution (L227). Strong resemblance stays valid. RM-OT-03 measures source-passing statistics.

**Without genealogy:** B is the general Halvren mixed-population envelope (L82).

**No exception may be hidden in presets.** Preset codes I–M stay internal validation labels (L463).

### 2.4 Durrim compact structural concentration

- **Exception type:** validator-heavy, control-light. Durrim defines no controls (L234).
- Durrim **binds the same regional DIR variables** as every humanoid race. Its anatomy text states that these dimensions vary (L170–195).
- Its identity lives in a **combined validator**: craniofacial depth relative to facial height, through domains A–E (brow, orbit, zygoma, midface, mandible), measured as DIAG and **never as five sliders** (L300).
- Further validators:
  - the **no-single-feature-dependency** rule (L252);
  - "nose never identifies" (L252);
  - "facial hair carries zero information" (L252).
- **Numbers** are deferred to RM-SR-05 and RM-CF-06.

### 2.5 Grask: non-human face and ear identity

| Area | Architecture |
|---|---|
| Face | Shared regional variables. The identity validator is **multiregional verticality** (FVB *with* MVI, never one ratio; L473–475) |
| Prognathism / maxillary projection | Held to authored central values. The distribution is OPEN (L362); RM-CF-03 waits on it |
| Ear | **Own family**: folded cartilage, sustained upper-ear body, later terminal taper, recognizable lobe. Orientation alone never separates it from elves (L459). Length ranges OPEN |
| Teeth | Default dentition only. Tusk-like canines OPEN; no slot |
| Refused controls | Trollness, Monster, Brutality, Ugliness, Savagery (L406) |

### 2.6 Gorrund: deep, integrated midface and jaw, non-human ears

| Area | Architecture |
|---|---|
| Face | Shared regional variables. The identity validator is **Transverse Structural Continuity**: coherence of lateral brow/orbit, zygoma and posterior mandible (TBP; DIAG). Facial depth is supporting, not dominant (L423) |
| Neighbor rule | Cranial breadth shifts the **envelopes** of orbit spacing, zygoma and jaw breadth (ENVELOPE), without hard-locking every correlation (L371) |
| Decoupling | TSC (face) and ALPC (body) are separate systems; neither is a slider (L737) |
| Ear | **Own family**: deep bowl, strong antihelical folds, broad continuous rim, close skull attachment, no elongated point |
| Refused controls | Ogre-ness and similar (L371) |
| Tusk-like canines | OPEN and separate from Grask |

### 2.7 Pipkin: adult compact craniofacial identity

- **Exception type:** anti-juvenile ceilings and floors.
- **CLAMP rules:**
  - aperture stays within the MF-compatible adult range, with no enlarged-eye envelope (L297);
  - midface is never shortened (L309);
  - mandible is mature (L332);
  - head share is never a maturity signal (L199).
- **Combined-stress validators** (L444–453) carry forward, including "lower-valid midface height + larger aperture", which is critical.
- Identity is **IMFA**: cranial base → temple/zygoma → central midface. It is *supporting*; the body is primary.
- **Ear:** own compact rounded family; overlap with MF and DU is allowed.
- **Asymmetry:** spec SILENT (AC-U3).
- **Refused controls:** "Pipkin Face" and human → Pipkin (L205, L412).

### 2.8 Cogling: fine-scale facial articulation

- **Exception type:** scale and readability.
- **Rule: camera, not anatomy.** Readability at a ~11–13 cm head is solved by **creator camera and rendering** (slot 15 presentation tools: face and ear close-ups, §200). Eyes, head, nose, ears and mouth are never enlarged (L1583–1588; COG-FACE-24).
- **Identity:** FSPI validator: adult face-to-vault (FVI) plus planar junctions. RM-SR-04 supplies numbers.
- **Ear:** fine folded family. Fold clarity is a **close-view trait** and need not read at gameplay distance (L1594).
- **Relationship rejections** (§101: toddler, mini-elf, comic nose, oversized ear) are INVALID combinations.
- **Refused controls:** "Cogling Face" and "Cogling Proportion".

### 2.9 Saurin

| Area | Architecture |
|---|---|
| Skull identity | **Layered Rostral-Cranial Integration**: Saurin binds five slots under renamed labels (Rostrum & Lateral Face, Nasal Openings, Mouth Line, Jaw, Auricular Openings) and has chin, lips, zygoma, forehead and facial hair **Absent**. No human topology is forced (order §3) |
| Rostrum | DIR controls under the §259 bounds. The FPI floor (0.255, provisional, protective canon) is a VAL. Cross-race closure is DEFERRED to RM-CF-01…05. **No margin is set** |
| Orbit | **FOLLOW** coupling (orbit → lids, aperture, eyeball). Spacing Bound-locked |
| Ocular | Vertical pupil is species anatomy. Shape variation and dilation range are DIR; dilation state is preview only. The nictitating membrane is species anatomy (Bound-locked) |
| Auricular | Recessed opening with its own parameter set; never pinnae at extremes |
| Dentition | Species default, contained in the closed mouth; no control |
| Cranial keratin displays | Slot 10 (the Hair slot) under the §260 validators. **Structural ridges** stay in slot 2 as skull anatomy with a non-zero floor |
| Surface | Field-aware facial scales; no global scale size |
| Sex | **No craniofacial sex shift** (§263): the generator samples every face and display driver identically by sex |
| Presets and randomization | §264 driver → dependent order (UFCA-05 §4) |

## 3. Ear-architecture families (slot 9 routing)

| Family | Races | Family-specific variables (from canon) | Family identity validator |
|---|---|---|---|
| Human auricle | MF, SK, SG; DU ("broadly humanoid") | Length, breadth, lobe size/attachment, projection, vertical position, angle, curvature (MF L307; DU L195) | Not pointed; not elven taper; DU "never one Ear Size" |
| Elven continuous taper | FN, AE, VA | Length, base width, tip length/sharpness, vertical angle, sweep, lateral projection, upper curvature, lobe (FN L183; AE L231; VA L282) | Point emerges from the whole ear; not human with stretched tip |
| Mixed coupled | HV | Human foundation variables + elven variables, coupled (L198) | Never one midpoint ear; length is not a genealogy meter |
| Folded late-taper | GR | Length, sweep (backward/upward), upper-ear body volume, fold robustness, lobe (L445–459) | Sustained body before a late taper; lobe present; orientation alone never diagnostic |
| Deep-bowl broad-rim | GO | Projection, auricular breadth, upper contour (rounded ↔ mildly angular), bowl depth, fold expression (L449–458; GOR-EAR-01…06) | No elongated point; close to skull |
| Compact rounded | PK | Height, breadth, projection, rotation, helix thickness, antihelix, conchal depth, tragus, lobule (L340) | No point, GR taper, GO bowl, mandatory tiny or comic ears |
| Fine folded | CG | Height, width, projection, placement, rotation, lobe, upper contour, plus fold variables (helix roll, antihelix, crura, conchal depth, tragus, lobule) (L1335–1362) | Fold clarity, not size; non-pointed; never enlarged |
| Recessed opening | SA | Opening size, recess depth, rim prominence, orientation (L989–994) | Never a pinna at extremes |

**Rules across all families:**
- Acquired ear damage is never family anatomy (FN L191; GR L398; DU L195).
- Ear asymmetry is DIR within each family.
- Mobility is OPEN.

## 4. Things the architecture deliberately does **not** generalize

| Item | Why it stays race-specific |
|---|---|
| The Saurin orbit coupling | Other races keep orbit ≠ aperture as independent DIR controls, with eyeball DER |
| Saurin §263 sex closure | PR R-SEX last bullet |
| Vael low-light lighting tests | Do not imply low-light biology elsewhere (ECR L100) |
| The Durrim depth domains | DIAG, not a universal control scheme |
| Gorrund TSC and Grask verticality | Race identity validators, not universal axes ("never vertical-versus-horizontal sliders", GO L403) |

— Claude

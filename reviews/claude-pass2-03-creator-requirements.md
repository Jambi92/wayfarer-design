# Pass 2 — 03. Creator-System Requirements Report

**Author:** Claude (auditor). **Order tracks:** C, D and G. Finding IDs are defined in `claude-pass2-06-findings.md`.

**Scope:** this report states design **requirements** only. It does not prescribe implementation architecture, UI or schema (order §4G).

**Inputs:**
- the 13 canonical specs;
- PROJECT_RULES;
- the decision register, read as supporting history. It is stale after Sep 30 (F-08).

## 1. Can the four-layer model represent all 13 races? (order question 4)

**Yes, without redefining any race's biology,** provided the four layers carry race-conditional *content* and are complemented by a small number of **non-layer records** that canon already requires.

| Layer (PROJECT_RULES) | Universal content | Race-conditional content required by canon |
|---|---|---|
| **A. Biological Anatomy** | Skeleton and proportion relationships, craniofacial structure, inherited pigmentation and pattern, eye biology, hair biology, sex-related tendencies, Muscular Development Capacity | Tail anatomy (Saurin §145); rostrum (Saurin §146); scale fields (Saurin §147, §262); cranial display anatomy (Saurin §150, §260); claws (Saurin §151); ear architecture families (all races, see §5); Halvren phenotypic expression state (P1 §32–33); Saurin coelomic body wall (E) and ventral fullness (B) (§263) |
| **B. Skeletal Frame** | Narrow / Balanced / Broad as editable presets over a continuous Skeletal Frame (Marchfolk Part 1 §5; Halvren P1 §19–22) | What frame changes is race-specific. Examples: Saurin frame includes the frame component of the tail base and changes no lengths (§258); Gorrund "Narrow ≠ low depth" (P2 L220); Grask frame does not set foot breadth (P2C L320–324); Cogling frame may touch robusticity (§54, see F-22) |
| **C. Physical Composition** | Current Muscularity, Body-Fat Amount, Body-Fat Distribution, regional development | Saurin tail muscle and fat follow composition, root-concentrated caudal fat is FAIL (§256); per-race fat-distribution maps; Saurin E/B explicitly **not** composition (§263) |
| **D. Personal Presentation** | Hair style, facial hair grooming, clothing, cosmetics, tattoos, accessories, paint | Saurin decorative claw treatment and keratin caps (§137); Saurin has no hairstyle or facial-hair presentation (biologically empty) |

**Non-layer records canon already requires.** These are not new layers; they are data that lives beside the four.

1. **Skin Appearance Layers:** Natural / Environmental / Applied / Acquired. These are an *appearance* taxonomy, not inheritance storage (Marchfolk Part 1 §7; Saurin §122, §137). The count needs harmonizing (F-14).
2. **Acquired history:** scars, damage and breakage. It is a separate randomization domain and independently lockable (Saurin §142A, §144).
3. **Genealogical ancestry**, kept apart from phenotypic expression (Halvren CRes §4–5). It survives appearance editing (P5 §59–63).
4. **Cultural identity layers:** Ancestry / Birthplace / Culture / Background (Sagekin v1.3 §11). These sit on a social axis outside the four layers, and their relationship to them is unstated (F-09).
5. **Responsive state,** not saved identity: Saurin pupil dilation (§149); environmental wetness.

## 2. Separation requirements (order question 5)

Each requirement already holds in canon. The exceptions are listed in report 01 §C.

- **R-SEP-1. Frame never sets** height, Current Muscularity, Body-Fat Amount or Distribution, face, sex-related tendencies, hair, culture or personality. The rule is stated in Marchfolk v1.0 §6–8, Vael v1.1 §8–9, Aelari v1.1 §7, Pipkin P1 §50–58, Cogling §54 and Saurin §258.
- **R-SEP-2. Current Muscularity and Muscular Development Capacity are distinct.** Capacity is Biological Anatomy, a population distribution. Current muscularity is Composition. Sources: Grask P1 L72, Cogling §21, Saurin §22, Halvren CRes §1. *Correction needed:* the Skarn "more natural muscle volume" trait must be read as capacity (F-04).
- **R-SEP-3. Body-Fat Amount and Distribution are distinct parameters.** PROJECT_RULES §Character creation. Several specs are silent on this, and the rule governs them (F-16).
- **R-SEP-4. Sex-related tendencies are Biological Anatomy distribution influences.** They never alter frame, composition or presentation defaults (see §3).
- **R-SEP-5. Inherited surface biology** (pigment, pattern, hair biology, iris, claws, scales, displays) is Biological Anatomy, expressed through the Natural appearance layer. It is never Presentation, and Presentation never overwrites it. Sources: Saurin §137; Vael v1.4 §1; Aelari v1.4 §4; Halvren P4.
- **R-SEP-6. Skeletal depth and breadth are never faked with soft tissue.** Sources: Vael v1.1 §2; Durrim P1 L50; Gorrund P2 L179; Saurin §258.

## 3. Sex-related anatomy: required universal rule (track D; F-03)

**Requirement R-SEX.** The creator system must support **per-race, sex-conditioned soft distributions** under the following constraints:

- (a) **Hard bounds are identical across sexes** within a race.
- (b) **Overlap is mandatory.** An individual of either sex may occupy any valid point.
- (c) Sex is **never** a preset, a body package or a control named "female body" / "male body".
- (d) Sex never shifts stature, frame, composition, face or displays **unless that race's canon explicitly defines a shift.** Today only Saurin defines shifts (§263: trunk, pelvic band, E, B).
- (e) For every other race, magnitudes stay OPEN per race. The architecture must hold "no shift" as a valid, complete state.
- (f) Reproductive biology is never implied by the creator.

**Current status:**
- (a)–(c) and (f) are consistent with every spec that addresses sex.
- Skarn, Sagekin and Fenn are silent.
- The terminology varies: Aelari "anatomy configuration", Vael "body configuration".
- Halvren's class-B dependency (CRes §15–16) is satisfied by this *rule*. It does not need a numeric model.

## 4. Control inventory (order §4G and question 7)

### 4.1 Universal controls

These are valid for every race, with per-race envelopes, response curves and couplings.

- **Body:**
  - stature;
  - Skeletal Frame (Narrow / Balanced / Broad presets plus continuous);
  - Current Muscularity and regional development;
  - Body-Fat Amount and Distribution;
  - torso and limb segment proportions;
  - hand and foot multidimensional controls. Never a single "Hand Size" or "Foot Size": Durrim P2 L115/L121, Grask P2, Halvren P2 §20–26, Pipkin P1 §26–49, Marchfolk Part 1 §4.
- **Age:** age, using the **triad** of chronological / apparent biological / age presentation (Marchfolk Part 1 §8; Halvren P4 §53–55).
- **Craniofacial region groups:**
  - cranium, brow/orbit, eye aperture, cheek/zygoma, midface, jaw, chin, mouth;
  - asymmetry, with a Restore Symmetry control (Marchfolk v1.2 §3; Vael v1.2 §27).
  - *Universal as regions only.* The organization is provisional (PROJECT_RULES "Facial architecture status").
- **Surface:** natural pigmentation (melanin/undertone or race equivalent); environmental weathering and tanning; applied markings; acquired scars.
- **Eyes:** iris pigmentation, kept separate from ocular anatomy and from magical effects.
- **Presentation:** clothing, cosmetics, accessories.

### 4.2 Conditional controls (shared by some races)

| Control | Present for | Hidden or replaced for |
|---|---|---|
| External ear (auricle) | All except Saurin | Saurin: recessed auricular opening (§56) |
| Scalp hair biology and style | All except Saurin | Saurin: **Cranial Display** occupies the Hair slot (§150, §260) |
| Facial hair | Humans, Halvren, Durrim, Grask, Gorrund, Pipkin, Cogling; elves where valid (Aelari v1.3 §13, Vael v1.3 §15) | Saurin: biologically empty (§33 note, SAU-CC-19) |
| Eyebrows | All mammalian-haired races | Saurin: not transferable (§117) |
| Nose (external nasal pyramid) | All except Saurin | Saurin: rostral nasal openings (§52–53) |
| Elven ear variables (length, taper, sweep, lateral projection) | Fenn, Aelari, Vael, Halvren | Others use their own ear-architecture families (§5) |
| Pupil shape | Saurin (vertical, with dilation range, §149); Vael candidate (v1.2 §13–15) | Round default elsewhere; Saurin round pupil not offered |
| Tusk-like canine variation | Grask and Gorrund only, separately OPEN | — |
| Ancestry / genealogy inputs | Halvren (CRes §4–5) | "No Elf Percentage slider" (P1 §23–29) |

### 4.3 Race-specific controls

- **Saurin:**
  - tail group (length driver; base, taper, curvature and carriage dependents; no on/off toggle);
  - rostrum group;
  - field-aware scale controls;
  - pattern;
  - cranial display family;
  - claws;
  - E/B tissue tendencies, as sex-conditioned distributions, never as a "female body".
- **Cogling:** hand and finger internal distribution (§40–41); ear fold architecture (§97).
- **Pipkin:** ear fold architecture (P3 §15).
- **Gorrund and Grask:** ear architecture families (P3C).
- **Durrim:** five depth domains (C3) as a multidimensional face-depth requirement.

### 4.4 Biologically empty or prohibited controls

These must not be exposed:
- "Elf Percentage", "Elf Gracility", pointiness, neck size, lifespan % (Halvren P1, P2, P3, P5).
- Trollness, Monster, Brutality, Ugliness, Savagery (Grask P3 L404).
- Ogre-ness and variants (Gorrund P3 L367).
- "Cogling Proportion", "Cogling Face" master sliders (Cogling §33, §98).
- "Pipkin Face", human→Pipkin master slider (Pipkin P2 §69–86; P3 §15).
- Global scale size (Saurin §85).
- Tail toggle (Saurin §145).
- A single "Face Depth" or "Torso Size" control (Gorrund).
- Any racial "beauty" control.

## 5. Ear-architecture families

The creator must represent these as distinct anatomical families, not as points on a pointiness continuum (Marchfolk Part 2 §3–4 "Locked").

| Family | Races |
|---|---|
| Human auricle | Marchfolk, Durrim ("broadly humanoid"), Skarn and Sagekin (by human family; their specs are silent, F-18) |
| Elven continuous-taper auricle | Fenn, Aelari, Vael |
| Mixed coupled human + elven | Halvren |
| Folded, late-taper | Grask |
| Deep-bowl, broad-rim | Gorrund |
| Compact rounded | Pipkin |
| Fine folded | Cogling |
| Recessed opening, no pinna | Saurin |

## 6. Modes, presets, randomization, locks, saves and NPC parity

| Requirement | Canon basis | Gaps |
|---|---|---|
| **Simple** (Race → Preset → Confirm) and **Advanced** (Race → Preset → Customize → Confirm) share one data model | PROJECT_RULES; Saurin §138–139; Pipkin P6 §22; Cogling §191 | "Basic" naming collision (F-15). Simple Mode is not stated in Skarn, Sagekin, Fenn, Durrim, Grask or Gorrund (PROJECT_RULES governs) |
| Presets are legitimate outputs of the same system: no preset-only morphs, no subraces or castes, never assign class or stats | Every spec | Halvren preset codes I–M are internal labels only (CRes §4–5) |
| Race-aware randomization: weighted distributions; relationship-aware; drivers before dependents; FAIL shapes rejected before presentation; never "roll everything and repair" | Saurin §264; Skarn v1.4 §4; Fenn v1.4 §3–4; Grask P5; Gorrund P4/P5 | — |
| Randomization domains kept separate: Biological / Presentation / Acquired History | Saurin §141–142A; Cogling §194; Halvren P5 §17–22 | — |
| Selective randomization with attribute locks; a locked child cannot force an invalid parent; constraints are communicated, never silent resets | PROJECT_RULES; Saurin §144, §159; Cogling §196 | Not stated in Fenn, Gorrund or Durrim beyond mention. Register R:93 still PRELIMINARY (F-08) |
| Validity ≠ frequency: Advanced Mode keeps the full valid range; frequencies shape NPCs, randomization and presets only | Sagekin v1.2 §8; Aelari v1.4 §6–8; Saurin §134, §233 | Frequency tiers: 3 (Sagekin v1.2 §8) vs 4 (Sagekin v1.4 §4; Aelari) (F-19) |
| Saved appearances: semantic record across the four layers plus non-layer records (§1); schema versioning; deterministic regeneration | Marchfolk v1.5 §9–13; Saurin §156; Cogling §197; Halvren P5 §59–63 | Cross-race reuse needs semantic mapping, not raw slider copy (Cogling §198) |
| **NPC parity:** same validity system; narrative exceptions flagged non-baseline | Durrim P5 L506; Grask P5 L683; Gorrund P5 L687; Cogling §199; Saurin §157 | Not stated in Skarn or Fenn (PROJECT_RULES governs) |
| **Combined-proportion validity:** relationship-aware; PASS / CONSTRAIN / FAIL; clamps adapt unlocked dependents | PROJECT_RULES; Saurin §158–159, §255; Grask P2 L257; Gorrund P1 L121; Cogling §33, §70 | Outcome vocabulary is formalized only by Saurin. Register R:190 PRELIMINARY vs R:444 AGREED (F-08) |

## 7. Requirements handed to the Universal Facial Customization Architecture (order question 6)

The facial architecture must support all of the following. It is not designed here.

1. **Race-conditional region sets.** Shared region semantics wherever anatomy exists, plus race-only regions (Saurin rostrum and recessed auricular opening). A region that is biologically absent is hidden, never shown as a dead control. The register's R:71 "same seven facial regions" rule cannot hold literally for Saurin (F-08).
2. **No master race or ancestry sliders** (§4.4). Halvren mixed faces come from coupled inheritance, never from interpolation between source faces.
3. **Bony orbit, visible aperture and eyeball kept as separate concepts,** with race-specific couplings. Saurin couples orbit, lids, aperture and eyeball (§259). Pipkin and Cogling forbid aperture enlargement (Pipkin P3 §4; Cogling §79).
4. **Multidimensional depth and projection,** never one Face Depth control: Durrim domains A–E; Gorrund multiregional depth; Saurin rostral index.
5. **A common normalized landmark and metric set** (projection, depth : facial height, face-to-vault, cranial breadth : height, head : stature, orbit : aperture), so that per-race floors can be audited across races. Required by the Saurin rostral non-overlap floor (F-02).
6. **Ear-architecture families** (§5), each with its own parameters, asymmetry and acquired damage; ear mobility left OPEN.
7. **Anti-juvenile constraints** for the small races: head share, aperture, midface and jaw minima (Pipkin P1 §5–11; Cogling §76, §101).
8. **Cranial Display** in the Hair navigation slot for Saurin, with its footprint, clearance and crest-ceiling validity rules (§260).
9. **Facial Diagnostic Domains** (FD-STRUCT / SOFT / SURF / HAIR / PRES / OBS) as the diagnostic taxonomy, kept separate from creator layers (Durrim CRP; Cogling §101A, §132). FD-HAIR is permanently empty for Saurin.
10. **Body-to-face soft-tissue coupling** that never sets a deterministic facial-fat value (Skarn v1.2 §7 pending; Gorrund P3 §45–52).
11. **Sex:** soft correlations only, no binary face sets (Cogling §93; Durrim P3 §50–59). Saurin has no craniofacial sex shift (§62, §263).
12. **Lighting invariance and neutral reference lighting** in the creator (Vael v1.3 §6–7, v1.5 §15–17; elf review Part 3 §9–10).
13. **Close-view creator cameras** for traits that are only legible close up: Cogling head ~11–13 cm and fine ear folds (§99, §200); Saurin nictitating membrane.
14. **Source-race protection:** no unrestricted route that exactly recreates another population's complete facial distribution (Halvren P3 §45–47).

— Claude

# UCCA-05: Skeletal Frame Architecture

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §9
**Status:** PROPOSAL for author review.

## 1. Universal design meaning (proposed canonical definition)

**Skeletal Frame** is the continuous configuration of a character's skeletal breadth, depth, joint and robusticity variables:
- shoulder/clavicular breadth;
- thoracic width;
- thoracic depth where the race binds it;
- pelvic width (and depth where canon names it);
- joint scale;
- long-bone robusticity;
- the race-specific extras (Saurin limb/joint girth, hand/foot breadth, tail-base frame component);

each inside that population's envelope.

**Basis:**

| Source | Wording |
|---|---|
| PR L12–13, L66 | Frame rules and terminology |
| MF L27, L285 | "shoulder breadth, ribcage dimensions, pelvic breadth, joint scale, skeletal visual mass … continuous configuration" |
| AE L134 | "change the real skeleton: clavicle, ribcage and pelvic breadth, joint relationships" |
| VA L128 | Frame changes clavicles, ribcage, pelvis, joints |
| SA L4168 | Saurin frame scope |

**What frame is not:**
- Frame is **not** sex, body type, muscularity, fatness or stature (order §9; PR L13; MF L27; AE L134; VA L128; GR L249; GO L220; PK L68; CG L781).
- **Narrow / Balanced / Broad** are three **named starting points** on that continuum: editable, never castes (PR L13; DU L52; GO L80; PK L68).
- **Balanced is not the canonical, most correct or default body** (DU L128; GR L70; GO L80).

## 2. Frame state: no hidden permanent frame (AD-C2)

The **resolved skeletal values are the frame.** No persistent "frame = Broad" variable drives anything after the player edits a region.

**Operation:**
1. Choosing Narrow, Balanced or Broad is a **write operation**. It writes race-specific starting values for the frame variables.
   - For Cogling, it writes robusticity and joint scale only as **starting tendencies** that remain separately adjustable (AC-9, L783).
   - It never writes stature, segment lengths, composition, face, hair or sex-related anatomy (GR L249; GO L220; CG L781).
2. Regional edits then act on the values directly. Nothing pulls back toward the preset.
3. **Canon effects tied to a frame category are computed from resolved values.** The one canon case is Saurin's reachable tail length: ~78 % H Balanced, 80 % H Broad, ~72 % H Narrow high-fat (§256.5). It becomes a function of the resolved breadths and composition. The function passes through the canon points; between them it is measurement-deferred (RM-UB-04).
4. "Started from: Broad" may be kept as **non-driving provenance** for display. A saved or reusable appearance never depends on it (UCCA-08).

**Justification for allowing no persistent state:** none was found in canon. No race requires a frame label to persist after regional edits. Saurin's frame-dependent tail cap is the only frame-category effect, and it can be computed from values.

## 3. Correlated dimensions: influence vs dependency

- Frame **may influence** several skeletal dimensions **at the moment it is applied** (ENVELOPE / write).
- **Correlated dimensions remain independently editable where canon allows:**

| Race | Canon basis |
|---|---|
| CG | AC-9: robusticity and joint scale never hard-determined by frame |
| GR | Foot breadth is a tendency only; "frame does not directly determine foot breadth" (L326) |
| GO | "Broad frame never hard-links to maximum thoracic depth" (L224) |
| DU | Broad increases breadths "never every dimension equally" (L129) |
| PK / GR / GO | "Population-level anatomical correlation does not automatically create a hard creator-control dependency" (PK L98, L205; GR L330; GO L220) |

**Hard limits that stay hard:** joint hard minimums (FN L115; AE L130; VA L132), plus each race's frame boundary rule:

| Race | Boundary rule |
|---|---|
| SK | Broad Skarn ≠ Gorrund (L32) |
| GR | Broad Grask ≠ Skarn / Gorrund; Narrow ≠ Aelari (L249) |
| GO | Narrow Gorrund keeps ALPC, "a critical identity test" (L719) |
| PK | Broad ≠ Durrim; Narrow ≠ child or Fenn (L45–46, L166) |
| CG | Broad ≠ Durrim; Narrow ≠ Fenn or child (§55–56) |
| SA | Broad ≠ Gorrund; numeric boundary OPEN (§21; §265) |
| VA | Narrow ≠ scaled-down Broad (L122) |

## 4. Population binding table

| Race | Frame writes / may change | Frame never changes | Special |
|---|---|---|---|
| MF | Shoulder, ribcage, pelvis, joints, skeletal visual mass | Muscle, fat, fitness, personality; height range | Athletic is a composition preset, not a frame (L5, L281) |
| SK | Skarn-range breadths and joints | — | Broad ≠ Gorrund |
| SG | Breadths within the Sagekin range | — | Never means narrow or thin (L93) |
| FN | Light-boned breadths; joints above hard minimums | — | Broad stays light-boned (L107) |
| AE | Clavicle, ribcage, pelvic breadth, joints, skeletal presence | Muscle, fat, sex, height, presentation (L134) | Broad gains real skeletal breadth (L125) |
| VA | Clavicles, ribcage, pelvis, joints | Muscle, fat, height, sex, presentation (L128) | **Spec omits shoulder/pelvic width from its torso control list (L121)**, but frame changes them, so they are bound through Slot 3 |
| HV | Breadths and joints inside the **ancestry-dependent** valid range (L54) | **Never encodes ancestry** (L137) | Joint-bridging coherence validator (L133). No Elf Gracility slider |
| DU | Ribcage, shoulder, pelvic breadth, joints, unequally | Muscle (never represented by muscle alone, L50); height (no packages) | Narrow inside Durrim structural minimums (L127) |
| GR | **Breadth relationships only** | Height, limb/hand/foot length, muscle, fat (L249) | Knees and ankles substantial in absolute terms |
| GO | **Skeletal breadth only** | Height, muscle, fat, hand/foot size, face (L220) | Bone and joints never linear with stature (L224) |
| PK | Shoulder, thoracic, pelvic breadth, joints | Height, muscle, fat, face, hair (L68) | Narrow keeps a mature pelvis (L45) |
| CG | Clavicle, thoracic, pelvic breadth; robusticity and joints as **tendencies** | Height, muscle, fat, face, sex, culture (L781) | Two tiers: frame preset vs neutral coverage preset (§193) |
| SA | Shoulder breadth, thoracic width (depth ±2 % only), pelvic width, limb/joint girth, hand/foot breadth, tail-base frame component; sets reachable tail cap | **Stature, long-bone/axial lengths, the skull, pelvic depth / sacral-caudal organization** (L4168) | Frame receives no sex shift (L4218) |

## 5. The Manny/Quinn placeholder

**The problem (level 6 prototype material):**
- The prototype's "Frame" control swaps the **Manny** and **Quinn** mannequins (plan L82, gap #1).
- That mixes sex-related anatomy with frame (audit 01 L24) and "changes the whole body type, not just skeletal breadth" (audit 05 L13).
- Height and race size are also uniform scaling (plan L84–86).

**How UCCA supersedes it at the design level:**
1. **Frame** is the continuous skeletal configuration defined in §1. It is not a mannequin, base-mesh or body-type selection.
2. **Sex-related anatomy** is a separate body-level selection (Slot 7). It shifts only soft generation centres (AD-C6), and it is never coupled to frame.
3. **Body type / composition** (Athletic, Heavy and so on) is Slot 6 and never touches frame.
4. Any future implementation must be able to represent **all frame × sex-related anatomy × composition combinations independently**, inside each race envelope. That is the test (tier I, UCCA-09).

**What UCCA does not decide** (order §9; PR L24–29):
- whether Manny/Quinn assets are kept, replaced or used as technical bases;
- the mesh, morph or skeleton approach.

It only states that **a mannequin swap cannot be the design meaning of Frame.** The prototype stays non-authoritative until an implementation order addresses it.

## 6. Saurin binding needs

| Need | Canon |
|---|---|
| Frame scope | Exactly §258 L4168 (above) |
| Thoracic width vs depth | Frame moves width with its own ±7 % bound; depth moves only ±2 % (separate ±8 % DIR bound). The depth/width ratio guard 0.80–1.00 (L4166) applies after frame and E/B (§263 L4245) |
| Tail | Frame supplies the tail-base frame component (follows pelvic width, §256.10) and the reachable length cap (§256.5) |
| Validation | Frame × composition × joint combined validity (§158 L2575); SAU-CC-09 frame × composition extremes; SAU-BODY-05 |

— Claude

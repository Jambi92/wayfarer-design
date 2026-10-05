# Pass 2 — 05. OPEN-Item Triage

**Author:** Claude (auditor). **Order track:** J. Finding IDs are defined in `claude-pass2-06-findings.md`.

**Sources collected:**
- every OPEN list in the 13 canonical specs;
- `register/decision-register.md`, cited as R:line. It was last updated Sep 30 and has no Saurin section (F-08);
- PROJECT_RULES "Reviews still required".

Most items are classified at **category level** with representative citations. An item-by-item copy of roughly 400 race OPEN entries would only restate the specs. The full per-race lists stay authoritative in each spec:
- Saurin §249–§252, §265;
- Cogling §207;
- Pipkin P6 §32;
- Durrim P5 §84–85;
- Grask P5 §101–105, plus the Decision Register (HK);
- Gorrund P5 §128–135, plus the Decision Register;
- Halvren CRes §15–16;
- Vael v1.5 §30;
- the elf review Part 4 register;
- the Marchfolk, Skarn, Sagekin, Fenn and Aelari version lists.

**No OPEN item was resolved by this audit.**

## 1. Pass 2 blocking

These must be decided before the next shared design stage: the Universal Facial Customization Architecture (UFCA) and the universal creator-control review. Both are scheduled to follow Pass 2 (PROJECT_RULES; register R:588, R:600, R:617).

| ID | Item | Why it blocks | Sources |
|---|---|---|---|
| B-1 | **Large-Race Comparative Anatomy Review** (Skarn, Grask, Gorrund) | Required by PROJECT_RULES and never performed. The Skarn–Gorrund distinction at 208–229 cm is unquantified, and Gorrund limb proportions are defined only against Grask | PROJECT_RULES "Reviews still required"; Grask P1 §60–70 L108, P5 L709; Gorrund P1 L108, P5 L667; not in the register (F-01) |
| B-2 | **Common normalized craniofacial landmark and metric set**, plus the cross-race projection ranges it enables | The Saurin non-overlap rostral floor depends on Marchfolk, Grask and Gorrund projection values that do not exist. The UFCA must carry per-race floors on one comparable metric | Saurin §39, §146, §259, §265; Grask P3 L360; Gorrund P3 L308; Durrim C3 L313–318 (F-02) |
| B-3 | **Universal sex-related anatomy rule** (rule only; per-race magnitudes stay OPEN) | Halvren's class-B dependency, Durrim's "pending the universal system", and register R:26. The UFCA and the creator need the rule to hold sex-related tendencies | Halvren CRes §15–16; Durrim P1 §37–39; register R:26; rule proposed as R-SEX in report 03 (F-03) |
| B-4 | **Terminology decisions** | Implementation-error risks feed straight into the UFCA and creator architecture: T-1 "race", T-2 comparator rule, T-4 Simple/Basic, T-5 ridge, T-6 Skin Appearance Layers, T-7 Muscular Development Capacity | Halvren CRes §6–9; register R:551; report 04 (F-05, F-07, F-09, F-14, F-15, F-24) |
| B-5 | **Authority hierarchy and register currency** | PROJECT_RULES and the decision register both claim decision authority with no stated precedence. The register is stale and internally inconsistent on two universals (combined-proportion validity; selective randomization with locks) | Register R:44, R:93 vs R:992, R:190 vs R:444 (F-08) |

## 2. Pass-2-relevant but not blocking

These are required inputs before creator **validators** are implemented. The design architecture can parameterize them.

| Item | Note | Sources |
|---|---|---|
| Numeric body-proportion envelopes behind each race's primary identifier | Examples: Pipkin trunk share, Cogling segment ratios, the Grask limb floor, Gorrund vs Skarn proportions, Skarn magnitudes, Sagekin long-limb tendency | Pipkin P6 §32; Cogling §207; Grask P1C L166; Gorrund P1 L157; Skarn v1.0 §8; Sagekin FD §4 (F-06) |
| Head-to-stature envelopes | Needed by the UFCA anti-juvenile constraints and world scale; must be parameterized per race | Grask P3 L429; Gorrund P3 L295; Pipkin P1 §5–11; Cogling §18, §207; register R:718, R:839, R:916, R:1028. Saurin is bounded (§258) |
| Final stature distributions / roster world-scale review | Every height range is provisional pending world validation. No named roster world-scale review exists | All specs §stature; register R:102 |
| Statistical spreads and frequencies | Validity ≠ frequency, so this never blocks design | Register R:170 and the per-race frequency rows |
| Muscular Development Capacity per race | The concept is agreed (R:542); the per-race distributions are OPEN | Register R:660, R:797, R:917, R:1028 |

## 3. Later biological

Representative coverage:

- **Pelvic and shoulder morphology:** Fenn, Aelari, Vael, Halvren (elven pelvis is class B, but only for Halvren v1.1), Durrim, Grask, Gorrund, Pipkin, Cogling, Saurin.
- **Thoracic, vertebral, rib and limb-segment ratios:** all non-human races.
- **Joint and robusticity distributions.**
- **Reproductive life history and physiology:**
  - Saurin §263 (gestation, egg vs young, provisioning, organs, B ↔ reproductive fat body);
  - fertility and lifecycle in Marchfolk, Durrim, Grask, Gorrund, Pipkin, Cogling and Halvren;
  - pelvic inlet/outlet in Cogling §47.
  - *Kept out of Pass 2 per order §8.*
- **Sex-related magnitudes** for every race except Saurin; facial and body hair sex distributions.
- **Lifespan, maturation and senescence:** all races, including elven lifespans.
- **Ocular physiology:** Vael low-light, pupil and daylight; **Fenn low-light** (Fenn v1.3 §9; this item is missing from the elf review's final register, F-20); Saurin nictitating-membrane details; Durrim, Grask and Gorrund low-light.
- **Ear mobility** (elves, Halvren, Pipkin, Cogling) and **hearing.**
- **Dentition:** Grask and Gorrund tusk-like canines (separately); Pipkin and Cogling counts; Saurin.
- **Pigment mechanisms**, rare pigmentation, skin thickness, blood and flushing, sun response.
- **Hair:** texture distributions, graying, silver/white validity (Aelari).
- **Saurin-specific:** scale microanatomy and shedding, per-field scale ranges, claw ranges, orbital tolerance, display frequency, the display mass-moment limit and prominent structures beyond the validated families, living balance and posture, the caudal-base landmark.
- **Genetics and inheritance depth:** Halvren and the register.
- **Regional subpopulations:** Sagekin and Marchfolk.

## 4. Gameplay

Kept out of anatomy per order §8. **Catalogued only.**

- **Race/class restrictions and racial attribute bonuses:** PROJECT_RULES says non-authoritative; the register R:28 says "neither removed nor approved"; the race → biology → gameplay review is OPEN (R:40, R:419).
- **Legacy traits** (F-17):
  - Skarn breath 1.5× "kept as is" (v1.0 §9);
  - Durrim breath and poor swimming;
  - Grask breath 2× and swim;
  - Gorrund slow swimmer and easy to spot;
  - Fenn sneak and swim;
  - Pipkin stealth;
  - Saurin 5× breath and fastest swimmer;
  - Cogling dexterity (superseded as automatic by Cogling §140).
- **Size consequences** for collision, reach, movement and combat. Deferred "until all 13 done" (R:30, R:49); that trigger has now fired.
- **Movement performance:** speed, jump, climb, stealth, encumbrance.

## 5. Equipment, world and camera

- Camera heights and first-person view (all races; R:27, R:106).
- Helmets and hoods for elven, Grask and Gorrund ears.
- Saurin tail equipment coverage. This is partly decided in Saurin §195/§225 but still listed OPEN in §115, §124 and §251 (F-13).
- Furniture, doors and stairs across the 76–251 cm span. Short-race review §15: "cannot be a single 'short race' interaction offset".
- Mounts; equipment fitting and canonical dimensions; beard physics and armor; Saurin longest-tail world validation (~170 cm behind the heel).

## 6. Animation and rigging

- Shared, retargeted, IK or specialized animation (all races).
- Saurin gait and tail counter-response; Saurin living balance (§257).
- Elf skeleton architecture.
- Facial animation and lip-sync for the Saurin rostral mouth.
- Nictitating-membrane triggers; ear mobility, if approved.

## 7. Technical / UE5

- Skeleton, mesh and morph architecture; MetaHuman suitability.
- Serialization and schema versioning; networking; LOD and performance.
- Material, SSS and shader architecture.
- **Production-safe fat displacement** (Saurin §252, from the female closure).
- Implementation-level prototype conflict audits, deferred until project files are accessible (PROJECT_RULES; Gorrund FC).

## 8. Culture and presentation

- Culture and background design (all races).
- Settlements and homelands (Sagekin, Fenn, Vael).
- Presentation preset libraries.
- Tattoo, cosmetic and marking catalogues.
- **In-game race descriptions:**
  - neutral vs in-world creator voice, deferred "until all 13 done" (R:50);
  - Pipkin and Cogling revisions;
  - the character-creation brief descriptors that contradict canon (F-10).

## 9. Housekeeping found during triage

These are not new OPEN items. They are inconsistencies in the OPEN lists themselves:

- Several OPEN lists still contain items resolved by later Parts. They are not marked superseded, though later lists govern:
  - Cogling §35, §72;
  - Pipkin P1 §116–118;
  - Durrim and Grask per-part status lines;
  - Saurin §115, §124, §251 tail coverage.
- **Cogling §207** "consolidated" list omits §150 centre of mass and §196 lock UI (F-22).
- **Elf review final register** omits Fenn low-light (F-20).
- **Register:**
  - about 12 OPEN rows are closed by later rows (R:661, 663, 717, 795, 799, 813, 838, 851, 864, 887, 888, 915, 932);
  - three rows say "RESOLVED" in their text but keep OPEN status (R:505, 575, 595);
  - there is no Saurin section;
  - the Short-Race review is still shown as queued (R:994) (F-08).
- **PROJECT_RULES** still lists the Short-Race review as required, though STATUS records it as accepted (F-11).

— Claude

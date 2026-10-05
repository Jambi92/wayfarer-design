# Pass 2 — 04. Terminology and Consistency Report

**Author:** Claude (auditor). **Order track:** H. Finding IDs are defined in `claude-pass2-06-findings.md`.

**Scope:** these are recommendations only. No spec text was changed. The goal is a shared vocabulary that does **not** flatten race-specific anatomical terms. Saurin "rostrum", Gorrund "Transverse Structural Continuity", Pipkin "Low-Set Compact Trunk Architecture" and similar terms stay as they are.

## 1. Collisions capable of causing implementation errors (order question 8)

### T-1. "race" (F-09, MAJOR)

**Problem.** The word "race" currently means four things at once (Halvren CRes §6–9; register R:551 OPEN):
- biological population;
- playable creation category;
- cultural identity;
- social identity.

A Halvren's genealogy, its playable classification and its culture can each differ.

**Recommendation.** Adopt separate canonical terms:
- **population** (biological);
- **playable lineage / creation category**;
- **culture**;
- **social identity**.

In data, store genealogy separately from playable classification (Halvren CRes §4–9).

### T-2. Unnamed comparators (F-05, MAJOR)

**Problem.** Comparative phrases appear without a named reference population:
- "humans" — Fenn, Aelari, Vael, Saurin §7;
- "taller humanoids" / "tall humanoids" — Durrim P1 L21, L34; Pipkin P1 §5–11, P3 §3;
- "smaller humanoids" and "relevant comparison populations" — Gorrund P1 L41, L76;
- "human reference anatomy" — Grask P1 L59, P2 L213/L215/L225;
- "near-human" — Cogling, about 20 uses;
- "robust humans" — Halvren P1 §16;
- bare "moderate" or "comparatively" with no comparator — Pipkin P1, P2, P6; Saurin §6–7, §14, §17–18.

The elf review terminology rule and Halvren CRes §2–3 already require a named population. Register R:466 fixes "Human Reference Population". The specs predate or ignore those rules.

**Recommendation.** Adopt a project rule:
- A comparative claim names its reference population.
- **"human" with no qualifier means the Marchfolk Human Reference Population at matched normalized height.**
- "near-human" means "within the Marchfolk adult envelope".

This rule resolves most existing text by interpretation. New text should name the population explicitly.

### T-3. "baseline" (MINOR, part of F-05)

**Problem.** Register R:466 and Marchfolk Part 1 §6 retire "baseline" in favour of **Human Reference Population** and **Reference Height**. The word persists in:
- Skarn v1.0 §9 ("1.5× as long as the baseline" — undefined);
- Skarn v1.1 §1–2 (meaning the Skarn central tendency);
- Marchfolk v1.0 headings;
- Aelari v1.5 §25;
- Grask/Gorrund "first-pass baseline" for dentition;
- the character-creation brief throughout.

**Recommendation.**
- Use "central tendency" for a population centre.
- Use "Human Reference Population" for the comparator.
- Use "first-pass default" for a design default.

### T-4. Simple vs Basic (F-15, MINOR)

**Problem.** PROJECT_RULES uses **Simple Mode / Advanced Mode**. "Basic" appears in three other senses:
- a body-editing tier (Marchfolk v1.1 §1);
- a face tier (Marchfolk v1.2 §1);
- in Aelari v1.5 §22 ("Basic and Advanced continuity") and register R:463.

**Recommendation.** Reserve **Simple Mode** for the creator mode. If an in-Advanced simplified tier is needed, give it a distinct name such as "Quick controls".

### T-5. "ridge" (F-07, MAJOR, Saurin)

**Problem.** In Saurin, §36a structural ridges and planes are skull form, present on every adult and "cannot be toggled off". But "ridge" is also used for:
- integumentary keratin ridges in the display family (§100, §260 "minimal ridges");
- "ridge-absent" individuals (§140, §234, §247, SAU-CC-12);
- a lock group (§144);
- a coupling (§158);
- "ridge controls … FD-SURF" (§155).

An implementer could reasonably toggle structural ridges off.

**Recommendation.**
- **Structural ridge/plane** = skull, never toggled.
- **Keratin ridge** = minimal display expression, may be absent.
- "ridge-absent" should read "keratin-ridge-absent / naked display".

### T-6. Skin Appearance Layers count (F-14, MINOR)

**Problem.** Marchfolk Part 1 §7, Pipkin, Cogling, register R:18/R:467 and Saurin §231 use **three** layers: Natural / Environmental / Applied or Acquired. Saurin §122 defines **four**, separating Applied (paint, dye) from Acquired (scars, damage). Saurin also keeps Acquired History as its own randomization and lock domain (§142A, §144).

**Recommendation.** Standardize on four layers: Natural / Environmental / Applied / Acquired. Saurin shows the split is useful, because acquired history is lockable separately and never inherited. Saurin §231 should then be conformed.

### T-7. Muscular Development Capacity (F-24, MINOR)

**Problem.** The term is used by Grask, Gorrund, Pipkin, Cogling, Saurin, Halvren and register R:542, with inconsistent capitalization. It is absent from PROJECT_RULES, which lists only Current Muscularity, Body-Fat Amount and Body-Fat Distribution.

**Recommendation.** Add **Muscular Development Capacity** (Biological Anatomy, population distribution) to PROJECT_RULES alongside **Current Muscularity** (Physical Composition).

### T-8. Sex-related anatomy vocabulary (F-03)

**Problem.** Several terms are in use:
- "sex-related anatomy" — most specs;
- "anatomy configuration" — Aelari v1.1 §5, §7; register;
- "body configuration" — Vael v1.5 §24–26;
- "dimorphism" — Grask, Gorrund, Pipkin, Cogling; not used by Durrim;
- "feminized" / "masculinized" as face guards — Halvren P3 §5–10; Pipkin P2 §7–17.

**Recommendation.**
- Use **sex-related anatomy** for the biological category.
- Use **sex-related tendency** for a distribution shift.
- Retire "anatomy configuration" and "body configuration".
- Keep the "feminized/masculinized" guards only as anti-stereotype language, never as a model.

### T-9. Frame vs composition words (F-16, MINOR)

**Problem.** Several specs list "Broad" among composition examples:
- Fenn v1.0 §8;
- Aelari v1.0 §12;
- Vael v1.0 §13.

Other blurred terms:
- "lean" and "rangy" inside skeletal identity (Grask P1 L9, L31);
- "physique" (Marchfolk v1.0 §12–14, v1.1 §1);
- "thickness" (Marchfolk v1.1 §5; Skarn v1.1 §1, §8; Sagekin v1.1 §3–5). Marchfolk Part 1 §3 already requires decomposition;
- "massive" (Gorrund — defined as skeletal at P1 L19, but read colloquially as composition);
- "structural mass" (Durrim P1 L54, which blends skeleton and composition) vs "structural presence".

**Recommendation.**
- Reserve Narrow / Balanced / Broad for frame.
- Reserve lean / heavy / muscular for composition.
- Use **skeletal structural presence** for skeleton and **visual mass** for the combined result.

### T-10. Frame preset vocabulary (MINOR)

**Problem.** Frame presets go by several names:
- "Frame Preset" vs "Skeletal Frame" — Marchfolk Part 1 §5; Halvren;
- "frame presets" — Durrim;
- "editable starting configurations" — Gorrund;
- "universal frames" — Skarn v1.0 §4;
- "frame/proportion presets" — Saurin §137, which conflicts with §258, where frame changes no lengths.

**Recommendation.** Use the Marchfolk Part 1 §5 pair everywhere: **Skeletal Frame** (continuous) and **Frame Preset** (starting point).

### T-11. Section and ID schemes (F-21, MINOR)

**Problem.**
- Durrim, Grask, Gorrund and Pipkin restart § numbering in each Part, so a citation like "§70" is ambiguous (Grask HK L728).
- Validation-ID prefixes collide: Grask uses **GR-**, Gorrund uses **GRR-**/**GOR-** mixed.

**Recommendation.** Cite as Part.§ for those specs, and give Gorrund one prefix (for example **GOR-** throughout).

### T-12. Process tokens in canon (part of F-13)

**Problem.** Saurin §263 contains review-process labels: "A50", "Gate 6 skull", "Gate 7 scale-field topology", "A-structure + E + B", "Pass-2 comparison D".

I wrote these myself during the October 5 reconciliation. They are not defined in the spec. "A50" is not defined in §256: it is the mid-tail area ratio that §256.3 states in words.

**Recommendation.** Replace them with spec-defined wording:
- "A50" → "mid-tail area ratio (§256.3)";
- "Gate 6 skull" → "accepted naked skull (§259)";
- "Gate 7 scale-field topology" → "Regional Scale Architecture field topology (§80–85)".

Because §263 is canon, this needs author approval.

## 2. Other consistency items (no implementation risk)

- **Ordinal labels.**
  - Two legacy-trait labels: "LEGACY GAMEPLAY TRAIT — SUBJECT TO LATER REVIEW" vs "OPEN / SUBJECT TO LATER GAMEPLAY REVIEW" (Durrim, Gorrund).
  - Two authority-chain spellings (Gorrund P2C L279 vs FC L741).
- **Frequency tiers.** Sagekin v1.2 §8 uses 3 tiers; Sagekin v1.4 §4 and Aelari use 4. Adopt the four tiers: Very Common / Common / Uncommon / Rare.
- **"Proposed universal" labels.** These persist in Skarn, Sagekin and Vael for rules later adopted roster-wide (lighting invariance, derived mass, selective randomization). Mark them adopted or not.
- **External references in canon.** "Iksar-inspired" (Saurin §95), "Dragon's Dogma 2" (Marchfolk v1.1 §8), "Wood Elf", "High Elf", "Dark Elf", "Troll", "Halfling" aliases. These are acceptable as inspiration labels and should never become anatomy definitions.

## 3. Recommended canonical glossary additions to PROJECT_RULES

These are for author decision:
- **Population**
- **Playable lineage**
- **Culture**
- **Social identity**
- **Human Reference Population** (Marchfolk)
- **Reference Height**
- **Central tendency**
- **Skeletal Frame / Frame Preset**
- **Current Muscularity / Muscular Development Capacity**
- **Body-Fat Amount / Body-Fat Distribution**
- **Skeletal structural presence / Visual mass**
- **Sex-related anatomy / Sex-related tendency**
- **Skin Appearance Layers** (Natural, Environmental, Applied, Acquired)
- **Facial Diagnostic Domains**
- **Simple Mode / Advanced Mode**
- **PASS / CONSTRAIN / FAIL**
- **Validity vs frequency**
- **Structural ridge vs keratin ridge** (Saurin)

— Claude

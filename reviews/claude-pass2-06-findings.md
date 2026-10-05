# Pass 2 — 06. Final Findings Report: Roster-Wide Comparative and System Review

**Author:** Claude (auditor)
**Responds to:** `reviews/chatgpt-pass2-roster-wide-comparative-system-review-order.md` (b5c9f48)
**Phase:** design only. No canonical race spec, PROJECT_RULES, STATUS or register entry was edited. Every substantive finding is returned to ChatGPT for author resolution (order §6).

**The package:**

| # | Report | Order tracks |
|---|---|---|
| 01 | `claude-pass2-01-comparative-anatomy.md` | A–F |
| 02 | `claude-pass2-02-collision-matrix.md` | I |
| 03 | `claude-pass2-03-creator-requirements.md` | C, D, G |
| 04 | `claude-pass2-04-terminology.md` | H |
| 05 | `claude-pass2-05-open-triage.md` | J |
| 06 | this report | findings and final questions |

**Inputs:**
- all 13 `specs/<race>/<RACE>_V1.md`, read in full;
- `decisions/PROJECT_RULES.md` and `specs/STATUS.md`;
- `reviews/elf-comparative-review.md` and `reviews/short-race-comparative-anatomy-v1.md`;
- `register/decision-register.md` and `rules/character-creation-brief.md`, read as supporting history.

## 1. Headline

**No BLOCKING CONTRADICTION was found.**
- No two approved anatomical envelopes contradict each other numerically.
- Every stature figure quoted across specs agrees with its source.
- No race's canonical identity rests primarily on height, attractiveness, culture, equipment, animation or surface phenotype.
- **No race needs its first-pass completion reopened.**

The roster's real weaknesses are four:
1. One review required by project rules was never carried out: the Large-Race review.
2. Distinctions between neighbouring populations are stated relationally but are **unquantified**.
3. The Saurin cross-race facial floor has a latent dependency on values that do not exist yet.
4. Terminology and authority documents have drifted, and some of that drift could cause implementation errors.

## 2. Finding register

Severity scale: BLOCKING CONTRADICTION / MAJOR / MINOR / INFORMATIONAL.

"By authority" means the finding is already resolvable from the authority hierarchy or newer canon, so it is **not** a live contradiction. It still needs a conforming text edit, with author approval.

### MAJOR

**F-01. The Large-Race Comparative Anatomy Review was never performed.**
- PROJECT_RULES requires it (Skarn, Grask, Gorrund). Grask P1 §60–70 L108 and P5 L709, and Gorrund P5 L667, both defer it ("not performed here"). It is not in the register or STATUS.
- Consequences:
  - The Skarn–Gorrund distinction at 208–229 cm rests on unquantified breadth, depth and joint magnitudes and partly on absolute-scale claims (Gorrund P1 L9, L76; P2 L237).
  - Gorrund limb and torso proportions are defined only against Grask (P2 L194–198), so a Gorrund with Skarn-like proportions is valid.
  - Skarn's spec never mentions Grask.
- **Recommendation:** author order for the Large-Race review as a Pass 2 sub-review.

**F-02. The Saurin non-overlap rostral floor depends on values that do not exist (latent contradiction).**
- Saurin §39 and §146 require the minimum rostrum to stay "clearly outside the approved adult projection ranges of Marchfolk, Grask and Gorrund". §259 records that none of those ranges exist.
- Grask keeps projection OPEN (P3 L360) and Gorrund keeps prognathism OPEN (P3 L308).
- **Recommendation:** define a common normalized craniofacial landmark and metric set before the Universal Facial Customization Architecture (UFCA). When Grask and Gorrund projection distributions are set, they must be checked against Saurin's index floor of 0.255.

**F-03. There is no roster-level sex-related anatomy rule (structural gap; no contradiction).**
- Skarn, Sagekin and Fenn are silent on sex.
- Aelari uses "anatomy configuration" and Vael uses "body configuration".
- Durrim's sex anatomy is "pending the universal system" (P1 §37–39).
- Halvren has a class-B dependency (CRes §15–16); see also register R:26.
- No spec has a hard envelope, a human-dimorphism import, or a sex restriction on face, stature, frame, muscle or fat. **Saurin §263 is preserved exactly.**
- **Recommendation:** canonize rule R-SEX (report 03 §3) as a universal *rule*. Per-race magnitudes stay OPEN; "no shift" is a valid complete state.

**F-04. The Skarn composition trait sits inside its skeletal identity.**
- Skarn lists "more natural muscle volume" under its skeletal foundation and core proportional identity (v1.0 §3; v1.1 §1).
- That conflicts with v1.0 §1 ("not automatically muscular"), v1.0 §5 and the PROJECT_RULES layer separation.
- **By authority (partial):** Halvren CRes §1 reinterprets it as Muscular Development Capacity, and Gorrund P2 L237 says "muscle-volume potential". But a randomizer reading the Skarn spec would raise Current Muscularity.
- **Recommendation:** conform the Skarn text to "greater Muscular Development Capacity", which is Biological Anatomy.

**F-05. Comparators are unnamed across the roster.**
- Examples: "humans" (Fenn, Aelari, Vael, Saurin §7), "taller humanoids" (Durrim, Pipkin), "smaller humanoids" and "relevant comparison populations" (Gorrund), "human reference anatomy" (Grask), "near-human" (Cogling), "robust humans" (Halvren), "baseline" (Skarn v1.0 §9 and others).
- This conflicts with the elf review terminology rule, Halvren CRes §2–3 and register R:466.
- **Recommendation:** adopt rule T-2 (report 04): unqualified "human" means the Marchfolk Human Reference Population at matched normalized height. Retire "baseline".

**F-06. Identity envelopes are unquantified at critical overlaps.**
- Cases:
  - Pipkin–Cogling at 91–107 cm: SR-COMP-01/02 are qualitative, and Pipkin's primary identifier has no metric (P6 §32).
  - Cogling's distal emphasis is shared in part with Sagekin, Grask, Fenn and Pipkin; it is separated only by a conjunction of traits (§63–§67A).
  - Grask's short-limb floor "enough limb contribution to read Grask" is undefined (GR-BODY-10).
  - Skarn's carriers are all Marchfolk-relative magnitudes.
- Canon deliberately avoided invented numbers, which is consistent with "no invented numbers" (Grask P1C L166) and Durrim C3.
- **Not blocking for design.** It is blocking for implementing creator validators.
- **Recommendation:** derive numeric diagnostic envelopes from reference meshes when they exist, the same way Saurin Part 7 did.

**F-07. "Ridge" is ambiguous in Saurin.**
- §36a says structural ridges are on every adult and "cannot be toggled off".
- Yet §140, §234, §247 and SAU-CC-12 allow "ridge-absent" Saurin, and there is a "ridges" lock group (§144) and coupling (§158). §155 says "ridge controls … FD-SURF".
- **Recommendation:** split the term into structural ridge vs keratin ridge (report 04 T-5).

**F-08. The authority documents have drifted.**
- `register/decision-register.md` stops at Sep 30. It has no Saurin section and shows the Short-Race review as queued (R:994).
- It contradicts itself on two universals:
  - combined-proportion validity is PRELIMINARY at R:190 but AGREED at R:444;
  - selective randomization with locks is PRELIMINARY at R:93 but AGREED at R:992.
- About 12 OPEN rows are closed by later rows.
- PROJECT_RULES and the register both claim decision authority with no stated precedence (register R:44).
- PROJECT_RULES lacks several AGREED universals: Skin Appearance Layers, Facial Diagnostic Domains, the Human Reference Population rule, Muscular Development Capacity, the source-first rule.
- The register's R:71 "same seven facial regions" rule cannot apply literally to Saurin.
- **Recommendation:** state the precedence (suggested order: approved race specs → PROJECT_RULES → register → reviews → prototype). Then refresh the register or mark it historical.

**F-09. "Race" is overloaded.**
- The word means biological population, playable classification, culture and social identity at once (Halvren CRes §6–9; register R:551 OPEN).
- Sagekin's identity layers (Ancestry / Birthplace / Culture / Background, v1.3 §11) are not reconciled with the four architecture layers.
- **Recommendation:** adopt T-1 (report 04): population / playable lineage / culture / social identity, with genealogy stored apart from classification.

### MINOR

**F-10. `rules/character-creation-brief.md` is stale and not marked superseded.**
- It still presents the old three-layer model (B:25–31).
- Its amendment layer C omits Body-Fat Amount.
- Its race descriptors contradict canon:
  - Pipkin "large head";
  - Gorrund "long arms";
  - Grask "thick skin, strong swimmers, regeneration";
  - Vael "lean, larger eyes";
  - Halvren "in-between skeleton";
  - Cogling "expressive face".
- It also says "baseline" throughout.
- **By authority:** approved specs govern.
- **Recommendation:** add a superseded banner.

**F-11. Stale status and process wording.**
- Pipkin header "(in progress)" (L1–3) vs P6 §38 FIRST-PASS COMPLETE.
- "Short-Race review queued" in Pipkin (P1 §82–94, P6 §36, P6 §38(6), L1669) and in PROJECT_RULES.
- Durrim says Pipkin and Cogling are undesigned (L66, L259, L502) and Gorrund is "once defined" (L480).
- Gorrund FC L741 says Pipkin is "not started".
- Grask claims "currently tallest" at 239 cm (P1C L178, P5 L671).
- "Next race" lines: Skarn header (Sagekin), Sagekin header (Fenn), Marchfolk Part 2 §16–17 (Halvren).
- Aelari and Vael say the elf review is pending; Vael says "Durrim aren't designed".
- Halvren's preamble is stale.
- Pipkin P1 §95–115 calls the roster envelope provisional "because Saurin is undesigned".
- Equal-height wording varies: Durrim 150 vs 152 cm; Gorrund–Grask 208–239 vs 218–229 cm.
- **By authority:** STATUS and the newer text govern.

**F-12. Dangling references.**
- "(see Notes)" in Durrim P5 §86–88 and Grask P5 §106–107, but neither file has a Notes section.
- Gorrund P5 §136–137 "full list in §136" does not exist.
- Gorrund FC L731 "added to the §134 identity statement" was never applied to L689.
- Halvren CRev cites "Part 1 notes", which do not exist.
- Durrim HK cites a Part 5 header instruction that does not exist.

**F-13. Saurin internal residuals not covered by the §249 pointers.**
- §230 "no true horns" vs §100 and §260 (later governs).
- §100 lists prominent horns, spikes and plates, while §265 lists them OPEN beyond the validated families.
- Tail garment coverage is OPEN in §115, §124 and §251 but decided in §195 and §225.
- §36a still says "PROVISIONAL pending Targeted Sculpt 6".
- §231 says three Skin Appearance Layers; §122 defines four.
- §44 treats orbit, opening and eyeball as separate; §259 couples them.
- Nostril placement: §52 vs §36a.
- Reference tail: 64.6 % (§256) vs 64.7 % (§263).
- **My own error:** I introduced undefined process tokens into §263 during the October 5 reconciliation ("A50", "Gate 6/7", "A-structure/E/B", "comparison D"). Corrective wording is proposed in report 04 T-12. It needs author approval because §263 is canon.

**F-14. Skin Appearance Layers count.**
- Three in Marchfolk, Pipkin, Cogling and the register; four in Saurin §122.
- **Recommendation:** standardize on four (T-6).

**F-15. Simple vs Basic.**
- "Basic" is used for body and face tiers (Marchfolk v1.1 §1, v1.2 §1) and for modes (Aelari v1.5 §22; register R:463).
- **Recommendation:** reserve Simple Mode for the creator mode (T-4).

**F-16. Layer wording leaks.**
- Body-Fat Amount and Distribution are not separated in Skarn, Sagekin, Fenn, Aelari or Vael.
- "Broad" appears among composition examples (Fenn v1.0 §8; Aelari v1.0 §12; Vael v1.0 §13).
- Grask has "relatively lean structural silhouette" (P1 L9).
- "physique" and "thickness" are undefined.
- **By authority:** PROJECT_RULES governs.

**F-17. Legacy racial gameplay traits remain in canon text.**
- Skarn breath 1.5× is "kept as is" (v1.0 §9), against PROJECT_RULES ("racial stats remain non-authoritative unless explicitly approved").
- Others are labelled "subject to review" under two different labels.
- Catalogued only, per order §8.

**F-18. Ear-anatomy gaps.**
- Skarn and Sagekin state no ear anatomy, yet Sagekin v1.2 says "ear biology" is approved.
- Fenn's own spec states no Fenn ear tendency; it lives in the Aelari and Vael specs and the elf review.
- **Recommendation:** confirm that the Marchfolk Part 2 §3–4 human auricle governs the whole human family, and record the Fenn tendency in the Fenn spec.

**F-19. Sagekin tensions.**
- Hands: "normal human hands and feet" (v1.0 §3) vs longer hands and fingers (v1.1 §1).
- Ribcage: "narrower" (v1.0 §3) vs "less depth" (v1.1 §1).
- The longer-limb tendency was escalated from "possible" (FD §4) without recorded validation.
- Frequency tiers: three (v1.2 §8) vs four (v1.4 §4).
- The elf boundary test is still "reserved" (v1.5 §9).
- Pigmentation is tied to the "warm maritime homeland" (FD §1, §5) with no "not any one real-world population" disclaimer like Marchfolk Part 2 §1–2. A disclaimer is recommended.

**F-20. Elf-family residuals.**
- Fenn's "slightly larger orbits" (v1.2) vs the review's "open presentation", with Vael's orbits also "somewhat large". This is a terminology overlap.
- Vael's "lower center of mass than Aelari" (v1.1 §20–23) is not carried into the review.
- Vael's nose tendency vs the review's E classification.
- Fenn low-light (v1.3 §9) was dropped from the review's final register.
- Aelari's neck comparator ("than humans and Fenn") vs the review ("than Fenn and Vael").
- **By authority, mostly:** the elf review governs its interpretations.

**F-21. Section and ID schemes.**
- Per-Part § restarts in Durrim, Grask, Gorrund and Pipkin make citations ambiguous.
- Gorrund mixes GRR- and GOR- prefixes, which collides with Grask's GR-.

**F-22. Cogling residuals.**
- The §207 consolidated OPEN list omits §150 (centre of mass) and §196 (lock UI).
- FD-HAIR is defined two ways: §101A includes eyebrows, §132 does not.
- Frame may influence robusticity and joints (§54) while §53 and §69 treat them as separate parameters; the relationship is unspecified.

**F-23. Halvren residuals.**
- The P2 §10–14 and P3 §7–8 comparatives are normalized only by the CRes table, not by text edits.
- "Skarn … muscular neck presence" (P2 §15–19) remains.
- The "feminized/masculinized" guards have no model behind them.

**F-24. Muscular Development Capacity is missing from PROJECT_RULES.**
- It is used by six specs and the register (R:542) with inconsistent capitalization.
- **Recommendation:** add it to PROJECT_RULES (T-7).

**F-25. Saurin cross-race coverage gaps.**
- The §31 boundary list omits Sagekin, Halvren and Pipkin (Pipkin is covered in §9 and §71).
- The face comparisons (§66–72) and §248 omit Skarn, Sagekin and Halvren.
- Risk is low because the tail, rostrum and auricular opening carry the read.

### INFORMATIONAL

- **I-01.** All stature figures agree across specs and reviews. The roster spans 76–251 cm (3.3×).
- **I-02.** Sagekin (with Marchfolk) and Halvren (with its sources) are recognizable only at population level, and individuals may collapse into a neighbour. This is accepted by design (Sagekin v1.0 §10; Halvren P1 §30–31) and is not a defect.
- **I-03.** Grask's Gorrund placeholders were superseded by the later Gorrund spec (Grask P1C L178; P2C L316–318).
- **I-04.** The shared Durrim/Gorrund tendency wording was resolved by Gorrund P3C and FC with matched-scale tests.
- **I-05.** Fenn is not used as the elven complexion baseline anywhere, and Marchfolk is not "human" by default ("Human never equals Marchfolk").
- **I-06.** The Saurin October 5 sex-anatomy closure is intact and consistently pointed to from every older section.
- **I-07.** Every spec rejects its race's fantasy stereotype explicitly:
  - dwarf (Durrim);
  - halfling (Pipkin);
  - gnome and tinker (Cogling);
  - troll (Grask);
  - ogre (Gorrund);
  - dragon and lizardfolk (Saurin);
  - "pointed-ear human" (elves);
  - "half-elf" (Halvren).

## 3. Answers to the final audit questions (order §9)

**1. Are all thirteen races still positively distinguishable at their meaningful overlap points?**
- **Yes in design intent.** Every overlap band has named positive carriers and canonical tests (report 01 §A4; report 02).
- **Two unaccepted high risks** are distinguishable only qualitatively: Skarn–Gorrund (F-01) and Pipkin–Cogling (F-06).
- Marchfolk–Sagekin and Halvren–sources converge at the individual level **by design** (I-02).

**2. Does any race depend on height, attractiveness, culture, equipment, animation or surface phenotype as its primary identity?**
- **No.** Every spec names skeletal and craniofacial carriers and guards against these explicitly.
- Residual risks:
  - Skarn and Gorrund partly rely on magnitude and absolute scale (F-01, F-04).
  - Sagekin lists surface distributions among its differentiators within a deliberately population-level identity (F-19).
  - Vael's surface risk is acknowledged and guarded by the strictest neutralization tests of the elves.

**3. Are any approved anatomical envelopes mutually contradictory?**
- **No.** There is one **latent** contradiction: the Saurin rostral floor vs the still-OPEN Grask and Gorrund projection ranges (F-02). It becomes real only if those ranges are later set high.

**4. Can the four-layer creator model represent all thirteen races without redefining their biology?**
- **Yes**, with race-conditional layer content and the non-layer records canon already requires:
  - Skin Appearance Layers;
  - acquired history;
  - Halvren genealogy;
  - cultural identity layers;
  - responsive state.
- See report 03 §1.

**5. Are frame, composition, sex-related anatomy and presentation cleanly separated across the roster?**
- **Yes in substance.** Exceptions are wording-level and resolvable by PROJECT_RULES (F-16).
- One real leak: Skarn's muscle trait (F-04).
- Sex-related anatomy is cleanly separated wherever stated; the gap is the missing universal rule (F-03).

**6. Which facial requirements must the future UFCA support?**
- Report 03 §7 lists 14 requirements. Among them:
  - race-conditional region sets with hidden empty regions;
  - no master race sliders;
  - orbit, aperture and eyeball kept separate, with race couplings;
  - multidimensional depth and projection;
  - **a common normalized landmark set** (F-02);
  - eight ear-architecture families;
  - anti-juvenile constraints;
  - Saurin Cranial Display in the Hair slot;
  - Facial Diagnostic Domains;
  - soft-correlation-only sex handling;
  - lighting invariance;
  - close-view cameras;
  - source-race protection.

**7. Which controls must be universal, conditional or race-specific?**
- Report 03 §4. In outline:
  - **Universal:** stature, frame, composition, segment proportions, multidimensional hands and feet, the age triad, craniofacial region groups, pigmentation, iris, presentation.
  - **Conditional:** auricle, scalp hair, facial hair, eyebrows, external nose, elven ear variables, pupil shape, tusk-like canines, genealogy.
  - **Race-specific:** the Saurin tail, rostrum, scale fields, display family, claws and E/B tendencies; Cogling and Pipkin ear-fold and hand architectures; Durrim depth domains.
  - **Prohibited:** every master race, ancestry, "-ness" and beauty slider.

**8. Are there unresolved terminology collisions capable of causing later implementation mistakes?**
- **Yes:**
  - "race" (F-09);
  - unnamed comparators and "baseline" (F-05);
  - "ridge" in Saurin (F-07);
  - Simple vs Basic (F-15);
  - Skin Appearance Layers count (F-14);
  - Muscular Development Capacity (F-24);
  - sex vocabulary (F-03);
  - ID prefixes (F-21).
- See report 04.

**9. Which OPEN items truly block the next design stage?**
- Five (report 05 §1):
  - **B-1** the Large-Race review;
  - **B-2** the common craniofacial landmark and metric set;
  - **B-3** the universal sex-related anatomy rule;
  - **B-4** the terminology decisions;
  - **B-5** the authority hierarchy and register currency.
- Nothing else blocks. Numeric body envelopes, head ratios, frequencies and spreads are needed before validators are implemented, not before design.

**10. Did this audit discover any reason to reopen a race's first-pass completion?**
- **No.**
- F-01 calls for a comparative review, not a Skarn or Gorrund redesign.
- Every other finding is a terminology, housekeeping or quantification item, resolvable without changing any approved anatomy.

## 4. Self-audit for cross-file consistency

- Finding IDs F-01 to F-25 and I-01 to I-07 are defined only here and cited consistently in reports 01–05.
- Blocking items B-1 to B-5 appear only in report 05 and in answer 9.
- Stature figures in reports 01 and 02 match each other and the specs.
- The pair risk ratings in report 02 match the narrative risk notes in report 01 §B.
- Severity labels follow order §5.
- **No canonical file was edited.** My own October 5 §263 wording issue is reported as F-13 rather than silently fixed.

STOP. Findings are returned to ChatGPT for author resolution. No canonical race spec was edited, the Universal Facial Customization Architecture has not been started, and no UE5 work was done.

— Claude

<!-- RAC Phase 1 evidence extraction (agent-produced, line-checked at HEAD 218f64a). Not canon; supporting evidence for reviews/claude-rac-01…12. -->
# D — Evidence extraction: Halvren inherited stature tails; Saurin open items

Repo: `/home/claude/wayfarer-design` (read-only). Every quote is verbatim, single-line and was machine-checked against the line cited. Markdown emphasis inside the source (`**…**`) is left out of quotes; the words are unchanged.

**Source keys**

| Key | File |
|---|---|
| HALV | specs/halvren/HALVREN_V1.md |
| MARCH | specs/marchfolk/MARCHFOLK_V1.md |
| SKARN | specs/skarn/SKARN_V1.md |
| SAGE | specs/sagekin/SAGEKIN_V1.md |
| FENN | specs/fenn/FENN_V1.md |
| AEL | specs/aelari/AELARI_V1.md |
| VAEL | specs/vael/VAEL_V1.md |
| GORR | specs/gorrund/GORRUND_V1.md |
| GRASK | specs/grask/GRASK_V1.md |
| ELF | reviews/elf-comparative-review.md |
| UCCA | decisions/UCCA_V1.md |
| UFCA | decisions/UFCA_V1.md |
| UCCAORD | reviews/chatgpt-ucca-phase2-canonicalization-order.md (author order: AD-C3b, T-5, T-12) |
| RMQ | reviews/claude-pass2-r5-reference-mesh-queue.md |
| SAUR | specs/saurin/SAURIN_V1.md |
| SREG | reviews/saurin-creator-parameter-register.md (diagnostic, explicitly not canon) |
| SVAR | reviews/claude-saurin-creator-biology-variation.md (diagnostic report) |
| SCLO | reviews/claude-saurin-creator-biology-closure.md |

**Tags.** [POS] canon positive statement. [OPEN] canon says this is open. [TEST] a validation target. [BAN] a prohibition. [NUM] a canon or measured number. [SILENT] canon says nothing; any text under this tag is my derivation, not canon. **Derived** marks arithmetic or inference from canon numbers that the canon does not state itself.

---

# PART 1 — Halvren inherited stature tails

## 1.1 Which populations are Halvren sources (confirmed)

- [POS] There are two families and six named source populations. — "human (Marchfolk, Skarn, Sagekin) and elven (Fenn, Aelari, Vael)" (HALV L9)
- [POS] The §8 table restates the six sources. — "The architecture supports contributions from Marchfolk, Skarn and Sagekin (human family) and Fenn, Aelari and Vael (elven family)." (HALV L22)
- [POS] The v1.0 decision summary has the same list. — "Human: Marchfolk, Skarn, Sagekin. Elven: Fenn, Aelari, Vael" (HALV L407)
- [POS] No individual has to show traits from one named source of each family. — "Not every Halvren visibly shows traits from one named human and one named elven population" (HALV L22)
- [BAN] No generic parent exists in either family. — "no averaged elven source that erases Fenn, Aelari and Vael differences" (HALV L50)
- [POS] Marchfolk are the primary human reference, and Skarn and Sagekin are equally valid sources. — "Marchfolk stay the primary Human Reference Population, but Skarn and Sagekin are also valid human-family ancestry." (HALV L50)
- [POS] The Marchfolk pre-inheritance resolution sets the same scope. — "The framework can represent ancestry from any established human-family and elven-family population." (MARCH L324)
- [SILENT] No other roster population is a Halvren source: Durrim, Grask, Gorrund, Pipkin, Cogling and Saurin are not named anywhere as Halvren ancestry. The ancestry structure is only human-family plus elven-family. There is no Skarn-only or third-family branch beyond Skarn's place inside the human family.

## 1.2 Genealogy structure and depth

- [POS] Halvren are not a 50/50 cross. Many generational histories are valid. — "valid histories include first-generation human and elven ancestry, Halvren plus human, Halvren plus elf, Halvren plus Halvren, multigenerational mixing" (HALV L13)
- [OPEN] The depth of the genetic model is unresolved. — "Genetic simulation depth is unresolved." (HALV L13)
- [POS] Halvren are a persistent population, not a dead end. — "Halvren can form persistent multigenerational populations and aren't biological dead ends" (HALV L20)
- [POS] Genealogy (family history) and phenotype (visible anatomy) are distinct. — "Genealogy is never inferred from one visible feature." (HALV L29)
- [POS] **The A→B→C model** (consistency resolution §4–5). Constraints B are "the valid distributions that genealogy produces" (HALV L467). Phenotype edits never write back to A: — "Editing visible phenotype never silently rewrites genealogy" (HALV L467)
- [POS] UCCA canonizes A→B→C for the body, with B recomputed and never stored. — "Genealogy (A) → ancestry-derived constraints (B, recomputed, never stored) → phenotype (C)" (UCCA L292)
- [POS] UCCA: lineage is optional and sits only in Slot 0. — "Lineage is optional and lives only in Slot 0." (UCCA L292)
- [POS] UFCA: with no lineage entered, a general envelope applies. — "With no genealogy set, the general Halvren mixed-population envelope applies." (UFCA L223)
- [POS] Randomization respects genealogy without making phenotype deterministic. — "When genealogy is set, randomization respects it but still allows multiple valid phenotypes, never one deterministic appearance per ancestry history." (HALV L351)
- [TEST] Family validation sets exist. — "Multigenerational family (older generation, adult and younger adult descendants), validating trait persistence and reappearance, resemblance, non-midpoint inheritance" (HALV L358)
- [OPEN] The genetic model, genealogy representation and frequencies stay open. — "the mixed-ancestry genetic model; genealogy representation; player-facing ancestry UI; inheritance correlations; ancestry population frequencies" (HALV L421)
- [OPEN] Choosing a non-Halvren ruleset together with mixed genealogy is unresolved. — "Whether a player may pick a non-Halvren ruleset while also specifying mixed genealogy is" … OPEN character-creator design (HALV L477)
- [SILENT] Canon never says whether HV-49/HV-50 tail statures can be reached without a lineage entry. UFCA L223 says only that the "general Halvren mixed-population envelope" applies. It does not say whether that general envelope includes the tails or only the 152–213 central range. This bears directly on whether a Simple Mode player can create a tail Halvren.

## 1.3 Source stature canon (exact)

| Population | Min | Ref | Max | Line | Extra canon wording |
|---|---|---|---|---|---|
| Marchfolk | about 147 | about 173 | about 203 | MARCH L21 (also L64) | Approved playable envelope |
| Skarn | 183 | 208 | 229 | SKARN L13 | Provisional |
| Sagekin | 152 | 178 | 208 | SAGE L72 | Provisional |
| Fenn | 157 | 181 | 211 | FENN L24 | Provisional |
| Aelari | 168 | 190 | 221 | AEL L27 | Provisional |
| Vael | 157 | 178 | 203 | VAEL L17 | Provisional |
| Halvren (central) | about 152 | about 178 | about 213 | HALV L88 | Central envelope, tails allowed |

Halvren restates the six ranges at HALV L94–L99, and they match the source specs.

- [NUM] Marchfolk. — "About 147 cm (4'10\") | About 173 cm (5'8\") | About 203 cm (6'8\")" (MARCH L21). The text after the table: "This is the approved first-pass playable envelope." (MARCH L23)
- [POS] Marchfolk distributions are only gestured at. — "population distributions may differ where appropriate, individual overlap stays broad, and a player character can sit anywhere in the supported range." (MARCH L23)
- [POS] The Marchfolk minimum and maximum are the playable envelope. — "Minimum and maximum remain the approved playable envelope" (MARCH L286)
- [NUM] Skarn: "| 183 cm (6'0\") | 208 cm (about 6'10\") | 229 cm (7'6\") |" (SKARN L13)
- [POS] Skarn ranges are provisional and set no separate biological height limits. — "Biological anatomy sets no separate height limits. These values await visual and technical validation." (SKARN L15)
- [POS] Skarn are not scaled Marchfolk. — "They are not scaled-up Marchfolk and not automatically muscular." (SKARN L7)
- [NUM] Sagekin: "| 152 cm (5'0\") | 178 cm (5'10\") | 208 cm (about 6'10\") |" (SAGE L72)
- [POS] Sagekin height is not a racial marker. — "Height overlaps heavily with Marchfolk and is never the main racial marker." (SAGE L74)
- [NUM] Fenn: "| 157 cm (about 5'2\") | 181 cm (about 5'11\") | 211 cm (about 6'11\") |" (FENN L24)
- [POS] Fenn: "height never defines Fenn" (FENN L26)
- [NUM] Aelari: "| 168 cm (about 5'6\") | 190 cm (about 6'3\") | 221 cm (about 7'3\") |" (AEL L27)
- [POS] Aelari: "Height supports Aelari identity but doesn't create it." (AEL L29)
- [NUM] Vael: "| 157 cm (about 5'2\") | 178 cm (about 5'10\") | 203 cm (about 6'8\") |" (VAEL L17)
- [POS] Vael: "Height never defines Vael" (VAEL L19)
- [POS] Elves as a family are not tall. — "Not an elven trait: elves aren't universally tall" (ELF L28)
- [POS] Aelari's "taller" tendency is normalized, with named comparators. — "Population height distribution trends taller than Marchfolk, Fenn and Vael reference populations, with overlapping individuals" (HALV L457)
- [SILENT] No source spec authors a distribution shape: no SD, skew, percentile or frequency at its min or max. UCCA confirms this roster-wide. — "Population stature and proportion distributions are OPEN or SILENT for every race" (UCCA L113)
- [SILENT] No source spec separates a playable envelope from a biological tail. The source mins and maxes are the only edges that exist. Skarn is the exception: it says anatomy "sets no separate height limits" (SKARN L15).

## 1.4 The central envelope and the tail revision

- [POS] **Original Part 2:** 152–213 was the Halvren range. It was already reworded in place. — "not an absolute biological wall (ancestry-dependent tails are allowed). It overlaps strongly with both families without covering every source extreme." (HALV L90)
- [NUM] "| About 152 cm (5'0\") | About 178 cm (5'10\") | About 213 cm (7'0\") |" (HALV L88)
- [OPEN] Part 1 left height deliberately unlocked. — "Height isn't locked in Part 1." (HALV L54). Part 1's OPEN list: "OPEN, never silently resolved: target height envelope, reference height and distribution" (HALV L74)
- [POS] The consistency review stated the problem before the resolution. Lower edge: — "no elven source goes below 157 cm" (HALV L436)
- [POS] Same finding, upper edge. — "The minimum Skarn (183 cm) is already above the Halvren reference (178 cm)." (HALV L436)
- [POS] **Resolution §10–14:** 152–213 is now the central envelope. — "no longer an absolute hard biological envelope." (HALV L481)
- [POS] What the central envelope describes. — "describing the expected primary playable and population distribution" (HALV L481)
- [POS] **Which ancestries extend downward:** — "strong ancestry from shorter human-family distributions may allow some Halvren below 152 cm" (HALV L481)
- [POS] **Which ancestries extend upward:** — "strong Skarn or Aelari ancestry may allow some above 213 cm" (HALV L481)
- [BAN] Four mechanisms are banned. — "These limits are never set by hard clipping, compressing all inherited heights into 152–213, uniform scaling or parental averaging." (HALV L481)
- [POS] The conceptual model. — "central Halvren distribution plus ancestry-informed probability shifts plus biologically constrained tails" (HALV L481)
- [OPEN] Tail limits and frequencies are open. — "exact tail limits and frequencies are OPEN" (HALV L481)
- [POS] **Guardrail:** "tails don't make any source-race height automatically valid. The mixed developmental system still governs validity" (HALV L481)
- [POS] Guardrail, continued. — "strong Skarn ancestry may support unusually tall Halvren without authorizing the full Skarn height and structure distribution, and likewise for Aelari or Marchfolk extremes" (HALV L481)
- [TEST] The central edges are renamed. — "Central short boundary, about 152 cm (renamed from short boundary)" (HALV L485). "Central tall boundary, about 213 cm (renamed from tall boundary)" (HALV L486)
- [TEST] HV-49: "Lower-tail Halvren below 152 cm where ancestry supports it, not automatically a minimum" (HALV L487)
- [TEST] HV-50: "Upper-tail Halvren above 213 cm where ancestry supports it, not automatically a maximum" (HALV L488)
- [OPEN] "Exact tail heights are unresolved until the ancestry-dependent distribution is designed." (HALV L490)
- [POS] The Part 2 decision line was reconciled under T-5. — "ancestry-dependent tails may fall outside it, with limits OPEN" (HALV L156)
- [POS] UCCA §22 calls 152–213 the established central population envelope (bold in source), "not the complete biological hard bound." (UCCA L294)
- [POS] UCCA §22: the architecture supports ancestry-dependent stature tails outside it (bold in source) "through envelope B." (UCCA L294)
- [POS] UCCA §22: inherited stature is never hard-clipped (bold in source) "to 152–213 cm." (UCCA L294)
- [OPEN] UCCA §22 defers tail numbers to biology and measurement. — "They are derived later from approved source-population biology, Halvren inheritance/development rules and reference-mesh measurement." (UCCA L295)
- [BAN] "No tail number is invented." (UCCA L295)
- [POS] T-12: interim central-only test scope is allowed if labelled. — "Any temporary central-only testing scope must be" … explicitly labelled non-canonical interim test scope, "(T-12)." (UCCA L296)
- [TEST] UCCA §22 keeps the HV targets. — "HV-49 / HV-50 stay validation targets. Tails never make a source-race height automatically valid." (UCCA L297)
- [POS] Author order AD-C3b: do not invent tail limits and do not hard-clip — "invent tail limits now and do" … "hard-clip inherited stature to 152–213 cm." (UCCAORD L26). It continues: "Actual tail limits remain BIO/MEAS deferred" (UCCAORD L28)
- [POS] AD-C3b says the question does not block architecture. — "This unresolved numeric question does not block UCCA architecture closure." (UCCAORD L30)
- [POS] T-12. — "152–213 cm is not to be canonized as a hard inherited biological clip." (UCCAORD L129)
- [OPEN] RM-UB-05 is the measurement item, and it is ordered: author the biology first, then measure. — "biological authorship first (source-population biology, Halvren inheritance/development rules), then reference-mesh measurement; never hard clipping" (RMQ L83)
- [TEST] RM-UB-05 names its cases. — "Halvren genealogy cases with strong short-human, Skarn or Aelari ancestry; HV-49 / HV-50" (RMQ L83)
- [POS] The Grask equal-height rule respects the tails. — "a Grask–Halvren comparison uses an actually valid ancestry-informed Halvren configuration, and no Halvren tail is invented to make one." (GRASK L150)
- [POS] The Grask cross-race row. — "Only at a stature valid for the selected ancestry and phenotype, no invented tail and no hard central maximum" (GRASK L271)

## 1.5 Which sources can and cannot extend the envelope (derived from canon numbers)

Edge test: the source min must be below 152 for a lower tail, and the source max above 213 for an upper tail.

| Source | Min vs 152 | Max vs 213 | Can it supply a tail? | Does canon name it? |
|---|---|---|---|---|
| Marchfolk | 147 (5 below) | 203 (10 below) | Lower only | Lower: "shorter human-family distributions" (L481). Also named in the guardrail's "Marchfolk extremes" (L481) |
| Sagekin | 152 (equal) | 208 (5 below) | **Neither**, by range edge | Implicitly in "human-family distributions" (plural); see the note below |
| Skarn | 183 (31 above) | 229 (16 above) | Upper only | Named (L481) |
| Fenn | 157 (5 above) | 211 (2 below) | Neither | Not named |
| Aelari | 168 (16 above) | 221 (8 above) | Upper only | Named (L481) |
| Vael | 157 (5 above) | 203 (10 below) | Neither | Not named |

- **Derived.** The only source whose canon minimum lies below the central envelope is Marchfolk (147). The lower tail is therefore human-family and, numerically, Marchfolk-only. Its maximum source room is ~5 cm (147–152).
- **Derived.** Two sources exceed the upper edge: Skarn, with ~16 cm of room (to 229), and Aelari, with ~8 cm (to 221). These two are the ones canon names.
- **Derived / note.** Canon says "shorter human-family distributions" in the plural (HALV L481). Sagekin's canon minimum is exactly 152 (SAGE L72), so a Sagekin source cannot push below 152 on range-edge grounds. The plural could cover Sagekin's lower distribution in combination with Marchfolk, but canon does not say so. Either way, Marchfolk is the only human source below 152.
- **Derived.** No elven source can supply a lower tail. Every elven minimum (157, 168, 157) is above 152, and the review said so outright: "no elven source goes below 157 cm" (HALV L436). Fenn's max (211) and Vael's max (203) are below 213, so neither can supply an upper tail. Only Aelari can, from the elven family.
- **Derived.** The union of all source ranges is 147–229 cm. Canon forbids inheriting "the union of every source population's valid extremes" (HALV L82), which supports reading 147 and 229 as outer limits that a Halvren tail would not exceed. **[SILENT]** Canon does not state that the Halvren tails are capped at the source extremes, or how far inside them they stop.

## 1.6 Tail asymmetry

- [SILENT] The word "asymmetric" never appears for stature tails. Canon only names different contributors per side (L481).
- **Derived.** The asymmetry is structural.
  - (a) Source room: up to ~5 cm below vs up to ~16 cm above.
  - (b) Families: the lower tail comes from one family (human, effectively Marchfolk). The upper tail can come from both families (Skarn, human; Aelari, elven).
  - (c) Opposing pull on the lower tail: elven ancestry, which by definition is present in every Halvren, has no source below 157. In a "probability shift" model, elven contribution pulls away from the lower tail. Canon does not state this inference.
  - (d) Reinforcing pull on the upper tail: Skarn × Aelari genealogy combines two tall sources from different families. Canon cites exactly this pair as a non-midpoint example. — "A child of a very tall Skarn parent and an Aelari parent isn't automatically their midpoint" (HALV L101)
- [POS] Canon assigns these distribution shift directions. — "more Skarn or Aelari ancestry toward the taller part of the envelope, Marchfolk toward a broad human-centered spread" (HALV L101)
- [POS] For the other three sources, canon gives no direction. — "Sagekin, Fenn and Vael toward their own population tendencies" (HALV L101)
- **Derived.** Sagekin (178), Fenn (181) and Vael (178) have references at or near the Halvren reference (178). Their "own tendencies" therefore sit centrally. Marchfolk (173) is the only source reference below 178.
- [POS] Skarn's position is unusual: the whole Skarn range is at or above Halvren's reference, per the review's line "The minimum Skarn (183 cm) is already above the Halvren reference (178 cm)." (HALV L436)

## 1.7 Developmental plausibility and the mixed developmental system

- [POS] Coherence is locked. — "a character can't inherit unrelated extremes from different populations if the result is implausible." (HALV L31)
- [POS] Mixed developmental space. — "Halvren occupy a mixed developmental space between the human and elven skeletal families" (HALV L105)
- [POS] Extremes are damped. — "Halvren don't normally reproduce the most population-specific skeletal extremes of a pure source population." (HALV L105)
- [POS] Joint bridging. — "Joints (shoulders, elbows, wrists, hips, knees, ankles) bridge connected long bones coherently and respond to connected anatomy." (HALV L133)
- [BAN] The joint-bridging failure case. — "It fails if a highly gracile long bone connects through an implausibly massive joint just because two ancestry values were inherited independently." (HALV L133)
- [POS] Stature edges must be reached by proportion, not by scaling. — "Halvren near 152 or 213 cm stay proportionally coherent, never reached by uniform scaling" (HALV L101)
- [TEST] HV-11 checks the central short boundary. — "About 152 cm, validating proportions, face, hands and feet, equipment and world, never uniform scaling" (HALV L369)
- [TEST] HV-12 checks the central tall boundary. — "About 213 cm, same checks, never uniform scaling" (HALV L370)
- [POS] Height is complex and non-averaged. — "Height is never an average of parental or reference heights." (HALV L101)
- [POS] Non-midpoint multigenerational outcomes are valid. — "a multigenerational Halvren may be unexpectedly tall or short relative to recent ancestors while staying valid" (HALV L101)
- [POS] UCCA §6: stature is the only absolute size control, and other dimensions follow through race allometry. — "Head, hands, feet, joints and bone breadth never follow stature by one shared scale factor." (UCCA L110)
- [OPEN] RM-UB-02 is per-race allometry. For Halvren, the allometry of a tail body is itself an inheritance question. — "Per-race allometric response of head, hands, feet, joints, bone breadth and torso breadth/depth to stature" (RMQ L80)
- [POS] Source-first rule: tail biology may not be invented inside Halvren and pushed back into the sources. — "Halvren must not invent missing human or elven biology and then retroactively make that invention canonical for the source populations." (HALV L499)
- [OPEN] The shared elven pelvis and sex-related anatomy are Class B, potential blockers of detailed anatomy. — "Never invented inside Halvren. If v1.1 needs either for a definitive rule, that section stops" (HALV L497)

## 1.8 Why source extrema do not automatically become Halvren extrema

- [BAN] No union of extremes. — "Halvren don't inherit the union of every source population's valid extremes, or a Halvren creator could reproduce a pure Skarn, Marchfolk, Fenn, Aelari or Vael body" (HALV L82)
- [POS] Halvren have their own envelope. — "Halvren have their own mixed-population validity envelope" (HALV L82)
- [POS] The tail guardrail, as quoted in 1.4. — "tails don't make any source-race height automatically valid" (HALV L481)
- [POS] Strong Skarn ancestry does not authorize the Skarn distribution. — "without authorizing the full Skarn height and structure distribution" (HALV L481)
- [TEST] HV-49 and HV-50 are each "not automatically a minimum" or "not automatically a maximum" (HALV L487–L488).
- [POS] Preset I protects against shrunken Skarn. — "Skarn-influenced: more structural presence without becoming a small Skarn" (HALV L341)
- [POS] Skarn guard. — "Not a smaller Skarn with pointed ears, since elven ancestry stays developmentally integrated." (HALV L111)
- [POS] Skarn guard, continued. — "Skarn ancestry gets explicit protection against simplification" (HALV L111)
- [POS] Preset K protects against the stereotype tall Halvren. — "Aelari-influenced: vertical influence without the generic tall beautiful half-elf" (HALV L343)
- [POS] Aelari guard. — "Never a generic \"tall and elegant\" phenotype" appears at HALV L113. Plain check: "evenly elongated limb segments, long hands and fingers, elongated feet, strong gracility" (HALV L113)
- [POS] Marchfolk guard (relevant to the lower tail). — "Highly diverse, so never one narrow phenotype" (HALV L115)
- [POS] HV-01, the human-leaning case the review tied to the lower edge. — "never a literal human preset under another label" (HALV L359)

## 1.9 Source protection, source-passing and phenotypic boundary protection

- [POS] Phenotypic boundary protection. — "ancestry controls can't simply recreate another playable race." (HALV L141)
- [POS] The whole configuration stays inside the envelope. — "the complete configuration stays inside the Halvren envelope" (HALV L141)
- [TEST] Source-passing test. — "Some hard-to-classify individuals are fine, but systematic exact duplication means the mixed-ancestry constraints are too weak" (HALV L145)
- [TEST] Equal-height test. — "Height isn't the primary ancestry signal." (HALV L147)
- [TEST] Extreme combinations. — "Reject only invalid combined anatomy, never combinations that are just uncommon" (HALV L148)
- [POS] Face-level source protection. — "the system shouldn't give an unrestricted way to exactly recreate another population's complete craniofacial distribution" (HALV L227)
- [POS] UFCA whole-face protection. — whole-face source-race protection "rejects exact recreation of a source population's complete craniofacial distribution." (UFCA L231)
- [POS] UCCA extends source protection to the body. — "Source protection applies to body and face." (UCCA L293)
- [OPEN] RM-OT-03 is a statistics item (P3). — "Halvren source-passing statistics over a generated sample" (RMQ L91)
- **Derived relevance to tails.** Source protection is the canon reason a tail Halvren at, say, 225 cm (inside Skarn, outside Aelari) must not be a Skarn body relabelled. At tail statures the only available comparators are Skarn (upper) and Marchfolk (lower). The source-passing risk therefore concentrates exactly where tails live. **[SILENT]** No stature-specific source-passing threshold exists.

## 1.10 Frequency language

- [POS] Validity is not frequency (§9). — "aren't all equally common just because biology allows them" (HALV L23)
- [POS] Probability does not lock height to ancestry. — "Probability isn't validity" (HALV L101)
- [POS] Valid rare traits stay manually creatable. — "manual creation generally allows valid rare traits, while random generation follows population frequency" (HALV L262)
- [POS] The Extreme randomization strength is defined. — "(uncommon valid combinations near approved boundaries), where Extreme never means deformed, impossible, every slider at maximum or maximum exotic traits" (HALV L351)
- [POS] UFCA Extreme samples toward tails. — "Deliberately samples toward valid tails and unusual combinations." (UFCA L301)
- [POS] Internal frequency vocabulary. — "These describe generation, preset and NPC weighting only, never biological validity." (UFCA L309)
- [POS] Interim weights. — "Interim weights are never canon." (UCCA L267)
- [OPEN] Tail frequencies. — "exact tail limits and frequencies are OPEN" (HALV L481)
- [OPEN] Ancestry frequencies. — "ancestry population frequencies" (HALV L421)
- [SILENT] Nothing says tail statures are rare, uncommon or anything else. The tails are framed as "some Halvren" (HALV L481), and the central envelope as "the expected primary playable and population distribution" (HALV L481). That implies, without quantifying, that tails are minority outcomes.

## 1.11 Adjacent constraints

- [POS] World validation covers the full approved envelope. Prototype limits do not constrain anatomy. — "prototype limits don't redefine anatomy" (HALV L152)
- [OPEN] World-scale stature extremes across the roster are queued separately. — "Stature distributions and world-scale extremes (76–251 cm)" (RMQ L93)
- [POS] RMQ derivation rules apply to RM-UB-05 when it is run. — "Central values alone never establish a boundary." (RMQ L98)
- [POS] RMQ derivation rules, continued. — "Canonize it only by author acceptance, as Saurin Part 7 did." (RMQ L100)

## 1.12 Candidate classification — Part 1

1. **Which sources can extend the envelope** (lower: human-family / Marchfolk; upper: Skarn, Aelari; none: Fenn, Vael, and Sagekin by edge). **A.** L481 already names the contributors, and the edge arithmetic follows directly from the canon ranges.
   - *Suggestion (S1):* the author could ratify the derived table in 1.5 as explicit canon, including the Sagekin-at-152 point. That removes the "distributions" plural ambiguity at no cost.
2. **Tail asymmetry** (direction). **B.** The direction (narrow lower tail from one family, wider upper tail from two families) is authorable now from canon ranges. The magnitudes wait for RM-UB-05.
   - *Suggestion (S2):* state "the upper tail may be wider than the lower tail" as a qualitative directive, without numbers.
3. **Numeric tail limits.** **B → C.** UCCA and RMQ order biological authorship first and measurement second (RMQ L83). A useful number needs the Halvren mixed developmental rules plus reference meshes, but the authorship step (how far toward a source extreme) is B.
   - *Suggestion (S3):* author qualitatively that tails stay strictly inside the union of source extremes (147–229) and short of each named source's own extreme. That is consistent with L82 and L481, invents no number, and gives RM-UB-05 a bounding frame.
4. **Developmental plausibility at the tails.** **A** qualitatively, since L31, L105, L133 and L481 already lock coherence, joint bridging and no uniform scaling. **C** for numeric validators: allometry (RM-UB-02) and joint envelopes (RM-UB-03) are mesh-dependent.
5. **Source protection at tail statures.** **A** for the principle (L141, L481, UCCA L293). **C** for RM-OT-03 statistics.
   - *Suggestion (S4):* add a tail-specific source-passing pair. HV-50 vs a matched-stature Skarn and Aelari, and HV-49 vs a matched-stature Marchfolk, as permanent tests.
6. **Tail frequencies.** **B / E.** The direction (minority outcomes) is implicit. Weights are generation-system work and interim weights are never canon (UCCA L267).
7. **Whether tails are reachable without genealogy** (UFCA L223 general envelope). **E.** This is a creator/system decision, currently SILENT.
   - *Suggestion (S5):* decide explicitly whether the no-lineage general envelope is central-only, or central plus tails reachable through manual creation and Extreme randomization.
8. **Genetic model depth / multigenerational stature math.** **D.** HALV L13 and L421 keep this open, and it needs no resolution for tails at a qualitative level.
9. **Blocker assessment.** Not a blocker for building or validating the central Halvren reference body (about 178 cm). HV-11 and HV-12 sit at the central-envelope edges, not in the tails. T-12 permits labelled central-only interim testing (UCCA L296), and AD-C3b says it "does not block UCCA architecture closure" (UCCAORD L30). It is a blocker only for HV-49/HV-50 validation and for world-scale extremes.

---

# PART 2 — Saurin open items

## 2.0 Baseline facts used throughout

- [NUM] Stature is excluding tail. — "Provisional standing-height envelope, measured to the top of the head in neutral upright stance and" (SAUR L64)
- [NUM] "| ~168 cm / 5'6\" | ~188 cm / 6'2\" | ~208 cm / 6'10\" |" (SAUR L68)
- [OPEN] Stature is still conditional, including on tail/world-space validation. — "tail/world-space validation;" (SAUR L72)
- [POS] Stature overlap explicitly includes Halvren. — "Individuals may overlap Marchfolk, Sagekin, Fenn, Aelari, Vael and Halvren stature ranges." (SAUR L76)
- [NUM] Stature is a racial hard bound, independent of the creator bounds. — "Stature 168–208 cm remains the racial hard bound (§4) and is" … independent (SAUR L4166)
- [POS] Stature stays provisional. — "These values remain provisional until final roster-wide scale/world review." (SAUR L3588)
- [NUM] The frozen reference (aff1b52) stands 187.88 cm. — "Standing height 187.88 cm." (SREG L23). The provenance line: "taken on the frozen closure reference (aff1b52) and on warps derived from it" (SREG L6)
- [POS] All Part 7 validation came from aff1b52. — "All validation was derived from the frozen closure reference (aff1b52) without modifying it." (SAUR L4128)
- [POS] The register is diagnostic, not canon. — "candidate numbers there are" … not canon unless restated (SAUR L4126). The register: "canon until the author accepts it" (SREG L4), preceded by bold "not"
- [POS] §255 value categories. — "Deliberately carried forward" (SAUR L4139) is the definition of OPEN.
- [POS] The OPEN-list authority rule means earlier OPEN lists stay in force. — "The OPEN lists in Parts 1–5 remain in force unless a later accepted section explicitly resolves an item." (SAUR L4036)
- **Note on where the ten items live.** The task's list of ten matches the UCCA §25 BIO OPEN carry-list (UCCA L355), not §265 alone. Three of the ten are **not** in §265: thermoregulation (§124 L2050; §249 L4013), acquired tail/rostral/jaw loss (§113, §133, §142A, §225, §249), and tail-equipment construction (§251 L4069). They are carried by the earlier registers under the authority rule at L4036.

---

## 2.1 Balanced posture and density model

**Canon text**
- [POS] Posture is upright, with no forced hunch. — "Neutral Saurin posture is upright and adult." (SAUR L411)
- [POS] Some compensation is allowed. — "The tail may require subtle whole-body compensation" (SAUR L413)
- [POS] Resting alignment is anatomy, not presentation. — "Anatomical Resting Alignment ≠ Cultural/Personal Body Language." The source has bold; plain check: "Anatomical Resting Alignment" (SAUR L421)
- [POS] Centre of mass is a derived quantity. — "Saurin center of mass must eventually be derived from:" (SAUR L240)
- [POS] The tail participates in balance biomechanically. — "in balance, turning, acceleration, swimming motion and body language through real counterbalancing mass and axial movement." (SAUR L248)
- [BAN] No automatic gameplay bonus. — "automatically grant statistical/gameplay bonuses to balance, knockback resistance, agility, turning, acceleration or swimming." (SAUR L250)
- [POS] Locomotor posture. — "Neutral standing and locomotion remain upright." (SAUR L2790)
- [POS] Rest behaviour. — "At rest, the tail remains supported by its own anatomy." (SAUR L2821)
- [NUM] The frozen reference stance (§257). — "the reference stance would need ~" … 8.8° of forward whole-body lean (SAUR L4162). Plain check: "centre of mass lies ~6.3 cm behind the heel contact" (SAUR L4162)
- [POS] Anatomy is not reopened. — "Anatomy is not reopened for this." (SAUR L4162)
- [POS] The frozen pose is not the final idle. — "The frozen pose is an anatomical/reference stance, not the final dynamically balanced neutral standing pose." (SAUR L4162)
- [OPEN] Living balance is deferred. — "Living balance (axial inclination, pelvic organization, knees/ankles, tail carriage) is carried forward to the posture/locomotion/animation phase" (SAUR L4162)
- [NUM] The creator guard is relative. — "This is a guard relative to the frozen reference, not a claim that the reference stance is the final idle (§257)." (SAUR L4150)
- [NUM] +3° guard. — "of additional forward whole-body lean beyond the frozen reference under the uniform-density static model." (SAUR L4150)
- [POS] Carriage is separate from balance. — "carriage changes clearance and reach, not balance." (SAUR L4154)
- [OPEN] §265, first item. — "Balanced neutral standing posture and living balance (posture/locomotion/animation phase); final density model for balance." (SAUR L4263)
- [OPEN] §265, second item. — "Absolute (rather than reference-relative) balance limits once posture is fixed." (SAUR L4264)
- [NUM] Diagnostic density basis (SREG). — "Uniform-density centre of mass at f = −11.5 cm, which is 6.3 cm behind the heel contact" (SREG L39)
- [NUM] Volumes. — "Body volume 136.9 L; free-tail volume 21.2 L (15.5 %)." (SREG L38)
- [OPEN] The density question as posed by the diagnostic. — "for balance: uniform here. Should lungs and tail tissue be modelled?" (SVAR L416)
- [OPEN] The diagnostic said posture must precede absolute tail limits. — "This must be decided before tail limits become absolute." (SVAR L402)

**Closed qualitatively:** upright, adult, no hunch, crouch, drag or splay. The tail is self-supported and non-dragging. Compensation is "subtle". Anatomy is frozen against posture. Carriage is separate from proportions. There are no gameplay effects.

**OPEN:** the actual balanced neutral pose; the density model (uniform vs tissue-differentiated); absolute balance limits.

**Frozen reference embodies:** a reference stance (not balanced), uniform-density CoM 6.3 cm behind the heel, 8.8° lean deficit, and +3° as the relative creator guard. These are measured values on aff1b52, and §256.4/§257 canonize them only as relative and diagnostic.

**Effect on the central reference body:** **not a blocker** for building or validating the reference body (SAUR L4162 says anatomy is not reopened). It does block absolute balance limits, final tail-range absolutes (SVAR L402), and any posed idle or animation.

**Candidate classification: E** (posture/locomotion/animation phase) with a **D** sub-item (tissue density model). The canon routes it to the animation phase, and the density question is biological.
- *Suggestion (S6):* keep the +3° relative guard as the sole creator balance validator until the animation phase. If wanted, record in canon the qualitative directive that the balanced idle reaches equilibrium through axial inclination, pelvic organization and tail carriage, never through anatomy edits (L4162 already lists these).

---

## 2.2 Caudal-base landmark

**Canon text**
- [NUM] The tail envelope and how it is measured. — "Provisional neutral tail length: approximately" … 55–80% … "measured anatomically from the caudal base to tip along the relaxed centerline" (SAUR L174). Plain check: "measured anatomically from the caudal base to tip along the relaxed centerline." (SAUR L174)
- [NUM] The frozen reference measurement. — "Measured on the frozen reference (tail 121.4 cm along the relaxed centreline, 64.6 % of standing height):" (SAUR L4145)
- [POS] Tail length is a % of stature. — "for every tail relationship; tail length is defined in % of standing height." (SAUR L4155)
- [BAN] The pelvis and sacrum are frozen. — "The frozen pelvis/sacral-caudal architecture is never altered to support tail extremes" (SAUR L4156)
- [OPEN] §265. — "Exact caudal-base landmark for measuring tail length." (SAUR L4265)
- [NUM] The landmark the diagnostic actually used. — "Tail length here is measured from the axis point at the posterior pelvic plane (121.4 cm on the reference)." (SVAR L406)
- [OPEN] The diagnostic's framing. — "Canon says \"from the caudal base\"; the exact landmark needs fixing." Plain check: "the exact landmark needs fixing." (SVAR L406)
- [NUM] Register. — "Length along the relaxed centreline, caudal base to tip: 121.4 cm (64.6 % H)." (SREG L34)
- [OPEN] The Part 1 OPEN list also left sacral/caudal anatomy open. — "sacral/caudal skeletal anatomy;" (SAUR L569)

**Closed qualitatively:** length runs along the relaxed centreline from the caudal base to the tip, is expressed in % H, is isometric with stature, and the pelvis and sacrum are frozen.

**OPEN:** the precise anatomical point where "caudal base" starts.

**Frozen reference embodies:** a de facto value. Every Part 7 tail number (64.6 % reference; ~78 / 80 / ~72 % caps; 55 % / 78 % / 80 % on the reference female, L4252) was measured from "the axis point at the posterior pelvic plane" (SVAR L406). That convention is diagnostic, not canon.

**Effect on the central reference body:** **not a blocker** for building it, since the mesh exists and the tail is frozen. It is a **latent validation risk**. If canon later picks a different landmark, every % H tail figure in §256 shifts by a constant offset, and the 55–80 % envelope and the 78/80/72 caps would need restatement. It should be fixed before any tail validator is implemented, and before RM-UB-04.

**Candidate classification: A.** Choosing a landmark is a definitional decision that can be made now. Ratifying the diagnostic convention needs no new measurement. It becomes **C** only if a different landmark is chosen, which would force re-measurement.
- *Suggestion (S7):* ratify "axis point at the posterior pelvic plane" as the canonical caudal-base landmark, with a one-line note that all §256 figures already use it.

---

## 2.3 Numeric lower-trunk minimum (vs Marchfolk)

**Canon text**
- [POS] Direction. — "lower axial trunk has greater longitudinal contribution than a typical Marchfolk relationship;" (SAUR L96)
- [POS] The trunk is not a human torso. — "The Saurin trunk is not a human torso with a tail socket." (SAUR L92)
- [OPEN] "Exact vertebral count and rib arrangement remain OPEN." (SAUR L103)
- [POS] Stature-share accounting (Part 2) says how the long trunk is paid for. — "The elongated lower axial trunk is therefore paid for primarily through modestly reduced vertical head/thoracic contribution rather than by forcing shortened legs." (SAUR L970)
- [OPEN] "Exact proportional distributions remain OPEN and must still satisfy SAU-FACE-22." (SAUR L970)
- [POS] T-1 reconciliation: the stature-share statement describes the reference and central morphology only. — "this stature-share statement is a reference / central-morphology description." (SAUR L972)
- [NUM] Creator hard bound. — "axial trunk length ±10 %;" (SAUR L4166)
- [NUM] The sex-shifted centre sits inside the same bound. — "a soft distribution inside the unchanged ±10 % species bound." (SAUR L101)
- [NUM] Reference accounting. — "lower trunk 32.0 → 33.6 / 34.3 cm" (SAUR L4236), at equal stature 187.9 cm, male → female centre / reference female.
- [POS] REDISTRIBUTE: UCCA treats Saurin stature accounting as the only canon case. — "stature accounting is the only canon REDISTRIBUTE (§5);" (UCCA L308)
- [OPEN] §265. — "Numeric lower-trunk minimum relative to Marchfolk (§6) and a numeric Broad-vs-Gorrund boundary." (SAUR L4267)
- [OPEN] Register A17. — "Lower trunk must stay longer than the Marchfolk tendency (§6) | Numeric cross-race floor OPEN" (SREG L61)
- [OPEN] Diagnostic. — "The trunk must stay longer than the Marchfolk tendency (§6). A numeric cross-race floor is needed for A17." (SVAR L408)
- [OPEN] The Marchfolk side has no number. RM-LR-01 measures "Torso share (suprasternal → hip joint ÷ stature)" for the "Skarn, Grask and Gorrund references; Marchfolk reference" (RMQ L27), and RM-UB-01 gives per-race segment-share bands (RMQ L79). [SILENT] Marchfolk canon contains no numeric lower-trunk or torso share.

**Closed qualitatively:** the Saurin lower trunk is longer than the typical Marchfolk relationship, is paid for by the head and thoracic share, not the legs, sits within a ±10 % creator bound, and carries a +7 % female soft centre.

**OPEN:** the numeric floor ensuring that the −10 % end (and any male-low individual) still exceeds Marchfolk.

**Frozen reference embodies:** 32.0 cm lower trunk at 187.9 cm (male reference), so the reference itself is the measured central value. **Derived:** −10 % gives ~28.8 cm at 187.9 cm. Whether that still exceeds a matched Marchfolk cannot be known without a Marchfolk reference mesh.

**Effect on the central reference body:** **not a blocker.** The reference is accepted and frozen, and it carries the identity. It blocks only the creator lower-bound validator (A17) at the −10 % corner.

**Candidate classification: C.** Marchfolk canon has no numeric trunk share, so no useful number exists without measuring a Marchfolk reference mesh (RM-LR-01 / RM-UB-01).
- *Suggestion (S8):* until then, keep the creator floor at −10 % and add an explicit **[TEST]**. The −10 % lower-trunk Saurin at 168 cm and at 208 cm, compared at matched stature against a Marchfolk at the same height (Marchfolk overlap is 168–203 cm), must still show the longer lower-trunk relationship.

---

## 2.4 Numeric Broad-vs-Gorrund boundary

**Canon text**
- [BAN] "A Broad Saurin cannot become Gorrund simply through breadth." (SAUR L354)
- [POS] Frames are not castes. — "They are editable starting points, not castes." (SAUR L350)
- [POS] Comparative boundary. — "Saurin are not massive load-bearing humanoids. Broad Saurin retain different axial organization and substantially lower skeletal mass." (SAUR L529)
- [BAN] Face. — "A broad Saurin cannot become a scaled Gorrund." (SAUR L1152)
- [TEST] SAU-BODY-14. — "Gorrund-normalized structural-mass comparison" (SAUR L551)
- [POS] Frame scope (§258). — "Frame changes shoulder breadth, thoracic width (depth ±2 % only), pelvic width, limb and joint girth, hand/foot breadth and the frame component of the tail base." (SAUR L4170)
- [BAN] Frame cannot change axial architecture. — "change stature, long-bone or axial lengths, the skull, or pelvic depth / sacral-caudal organization." (SAUR L4170)
- [NUM] Shared guards. — "thoracic depth/width ratio stays 0.80–1.00" (SAUR L4168); "shoulder breadth ±8 %; pelvic width ±7 %;" (SAUR L4166)
- [BAN] Composition. — "generic bodybuilder-width transformation, uniform inflation." (SAUR L4172)
- [OPEN] §265 L4267 (quoted in 2.3).
- [OPEN] Diagnostic. — "The Broad frame here is girdle/girth only. A numeric \"never Gorrund\" check needs Gorrund reference dimensions." Plain check: "needs Gorrund reference dimensions." (SVAR L409)
- [POS] Diagnostic finding. — "Broad gets broader without becoming massive. It is a girdle-and-girth change, not a Gorrund-style axial mass change." (SVAR L123)
- [NUM] Gorrund stature. — "| about 208 cm (6'10\") | about 229 cm (7'6\") | about 251 cm (8'3\") |" (GORR L29)
- **Derived.** Saurin (168–208) and Gorrund (≥208) share only the single point of ~208 cm. Under UCCA §6.7, where no stature is shared, matched-scale (bold in source) "comparison is diagnostic only." (UCCA L114). A Broad-vs-Gorrund check is therefore essentially matched-scale, normalized and diagnostic.
- [OPEN] The measurement route is RM-LR-02 / RM-LR-06 (Gorrund depth and breadth ratios, axial load-path) (RMQ L28, L32). [SILENT] Gorrund canon contains no numeric breadth or depth ratios.

**Closed qualitatively:** Broad is girdle and girth only, with no change to axial or pelvic depth. The thorax d/w guard is 0.80–1.00. There is a ban on bodybuilder width and uniform inflation. Saurin are "substantially lower skeletal mass".

**OPEN:** a number expressing "never Gorrund".

**Frozen reference embodies:** the Balanced reference plus the validated Broad frame multipliers in the diagnostic. The register's frame table shows Broad thoracic depth ×1.02 and d/w Broad 0.82 (SREG L87). Those are diagnostic values; canon fixes only the ±7/±8 % bounds.

**Effect on the central reference body:** **not a blocker**, since the reference is Balanced. It affects validation of the Broad + high-muscle corner only.

**Candidate classification: C.** A useful number requires Gorrund reference measurements. Qualitatively the frame-scope ban (L4170) already does most of the work.
- *Suggestion (S9):* treat the existing frame-scope ban (frame cannot touch axial lengths or pelvic depth) plus the d/w ≤ 1.00 guard as the interim structural "never Gorrund" rule, and note in canon that they are the interim boundary.

---

## 2.5 Claw and digit ranges

**Canon text**
- [POS] Hand claws. — "Saurin fingers terminate in" keratinous claw-like nails (bold in source) (SAUR L1741)
- [POS] Hand claw properties. — "modestly projecting;" (SAUR L1745); "compatible with functional grasp;" (SAUR L1747); "not oversized talons." (SAUR L1749)
- [BAN] No automatic gameplay effect. — "They do not automatically grant climbing, unarmed-damage or weapon bonuses." (SAUR L1751)
- [POS] Foot claws. — "They must remain compatible with the approved plantigrade foot." (SAUR L1760)
- [BAN] "Saurin do not stand on giant talons." (SAUR L1762)
- [BAN] Invalid extremes. — "Extreme values that interfere with ordinary grasp, footwear or plantigrade stance are biologically invalid." (SAUR L1774)
- [POS] §151 creator rule. — "Hand values must preserve grasp." (SAUR L2486); "Foot values must preserve plantigrade contact and footwear compatibility." (SAUR L2487)
- [NUM] §261 diagnostic finding (canon-restated). — "brings their tips to the ground plane at about +15 % length in neutral stance" (SAUR L4205)
- [POS] Consequence of that finding. — "foot-claw length above ~+15 % requires a compensating curvature or tip change to preserve plantigrade contact." (SAUR L4205)
- [OPEN] "No numeric creator range is canonized" (source bold); plain check: "grasp, footwear and glove compatibility cannot be validated without a grip pose and equipment" (SAUR L4205)
- [OPEN] Routed onward. — "hand and foot claw ranges remain OPEN for the universal creator-control review." (SAUR L4205)
- [OPEN] §265. — "Hand and foot claw / digit numeric ranges (grasp, footwear, gloves)." (SAUR L4271)
- [OPEN] Register A31. — "Not exercised geometrically this pass | OPEN test" (SREG L75)
- [OPEN] Claw growth and wear stay open in the biology register. — "claw growth and wear." (SAUR L4032)

**Closed qualitatively:** five digits with opposable-thumb function, plantigrade, integrated non-retractable modest claws, no talons, grasp and footwear preservation as validity criteria, and the +15 % foot-claw ground-contact coupling.

**OPEN:** numeric ranges for length, curvature, width, thickness and tip, for hands and feet; and digit proportions.

**Frozen reference embodies:** the reference claws and digits ("The accepted reference hand and foot anatomy is retained", SAUR L4205), plus the measured +15 % ground-contact point.

**Effect on the central reference body:** **not a blocker.** It blocks the claw creator validator and glove/footwear fitting only.

**Candidate classification: E.** Canon itself says it cannot be validated "without a grip pose and equipment" (L4205). It has a **C** component (measuring the grip pose).
- *Suggestion (S10):* promote the +15 % foot-claw ground-contact finding into an explicit coupled rule now (length above +15 % requires curvature or tip compensation). It is already in canon text as a requirement, so this is presentation of an existing rule, not a new number.

---

## 2.6 Per-field scale ranges

**Canon text**
- [POS] Regional Scale Architecture. — "protective structural fields → transitional articulation fields → fine expressive fields" (SAUR L1343)
- [POS] "Larger" is relative. — "is relative to the individual Saurin's scale system and does not imply armor statistics." (SAUR L1360)
- [BAN] Articulation fields. — "These regions cannot use rigid plate-like geometry that visually or mechanically prevents the approved range of motion." (SAUR L1376)
- [BAN] Ventral. — "form continuous belly-scute plating." (SAUR L1405)
- [BAN] No global slider. — "slider cannot validly enlarge eyelid scales and dorsal trunk scales identically." (SAUR L1422)
- [POS] §147. — "A global scale slider cannot violate Regional Scale Architecture." (SAUR L2412)
- [POS] §262. — "field boundaries and functions are locked; expressive and articulation fields never coarsen toward structural size." (SAUR L4209)
- [OPEN] §262. — "Numeric per-field ranges have not been geometrically validated and remain first-pass rules, not numeric canon." (SAUR L4209)
- [OPEN] §265. — "Numeric per-field scale ranges." (SAUR L4272)
- [NUM] Diagnostic candidate, **not canon**. — "Within each field: structural size ±20 %, relief ±25 %; fine fields ±10 %" (SREG L76)
- [POS] Closure confirmation. — "Per-field scale ranges, claw ranges, orbital-spacing tolerance and the display moment limit were not made canon." (SCLO L108)
- [OPEN] The facial-field measurement route. — "Saurin structural-ridge strength and facial scale-field ranges" (RMQ L70)

**Closed qualitatively:** field topology, field functions, no global slider, articulation fields stay small and flexible, no belly scutes, and fields deform smoothly under E/B.

**OPEN:** numeric per-field size and relief ranges.

**Frozen reference embodies:** the field topology (§80–85) on aff1b52 ("RSA" is the register's Ref value at SREG L76). The register candidates of ±20/±25/±10 % are not canon.

**Effect on the central reference body:** **not a blocker.** Topology is fixed on the reference, and ranges matter only for creator variation and the surface/material pass.

**Candidate classification: C.** The ranges need geometric validation on meshes (RM-UF-04 for the face, plus a body equivalent). The qualitative rules are already closed.
- *Suggestion (S11):* add a body-field analogue of RM-UF-04 to RMQ §3B. Only the facial-field item is currently queued (RMQ L70).

---

## 2.7 Tail world-space validation

**Canon text**
- [OPEN] Part 1 OPEN list. — "tail world-space requirements for backed seating, benches, beds, crowds/multiplayer collision, closing doors, capes/cloaks/back armor, mounts and rear camera framing;" (SAUR L574)
- [TEST] SAU-BODY-20. — "Tail plus canonical chair/door/corridor proxy to expose world-space consequences without solving them" (SAUR L557)
- [OPEN] §166 gates the final tail range. — "Before final tail ranges are approved, creator tail extremes must also be validated against the Part 1 world-space proxies in SAU-BODY-20" (SAUR L2738)
- [POS] §206. — "The tail occupies real world space." (SAUR L3257)
- [BAN] §206. — "But it cannot be treated as nonexistent merely for convenience." (SAUR L3265)
- [OPEN] "Exact collision behavior remains OPEN." (SAUR L3267)
- [BAN] No punishment. — "Real visual/world-space presence does not automatically make the tail a combat or traversal liability." (SAUR L3271)
- [POS] Separation principle. — "keep visual/world accommodation separate from punitive gameplay hit detection and control." (SAUR L3282)
- [POS] §209. — "Tests must include tail sweep and maximum valid creator dimensions." (SAUR L3313)
- [BAN] §210. — "The tail cannot simply clip through a chair back." (SAUR L3329)
- [POS] §211. — "A valid Saurin should be able to use world rest systems without tail deletion." (SAUR L3339)
- [TEST] SAU-WORLD-01. — "Door/corridor/90° turn across maximum body/tail envelope, including a door closing while the tail is within the doorway" (SAUR L3440)
- [TEST] SAU-WORLD-02. — "Chair/stool/bench seating without tail deletion" (SAUR L3441)
- [TEST] SAU-WORLD-03. — "Bed/rest pose across tail-length extremes" (SAUR L3442)
- [TEST] SAU-WORLD-05. — "Crowd/multiplayer spacing with visible tail volume" (SAUR L3444)
- [OPEN] §228. — "Exact final range awaits world-space validation." (SAUR L3620)
- [OPEN] §249. — "exact tail range after world validation;" (SAUR L4017)
- [OPEN] §251. — "tail collision policy;" (SAUR L4072); "exact world-clearance standards." (SAUR L4079)
- [NUM] §265. — "World-space validation of the longest tails (up to ~170 cm tail reach behind the heel at the stature/tail extremes)." (SAUR L4274)
- [NUM] Diagnostic. — "the 208 cm + 80 % extreme reaches 170 cm behind the heel, about 208 cm overall body length." (SVAR L236)
- [NUM] The reachable cap is a racial envelope, not an entitlement. — "The 80 % endpoint is a racial envelope, not an entitlement for every body." Source bold; plain check: "endpoint is a racial envelope, not an entitlement for every body." (SAUR L4151)
- [OPEN] RM-UB-04. — "Saurin reachable tail-length cap as a continuous function of resolved frame and composition" (RMQ L82)
- [POS] Carriage range. — "Validated carriage +8° lift … +10° droop with no ground contact" (SAUR L4154)

**Closed qualitatively:** the tail is real in world space, never deleted or clipped, and accommodated by world design. Visual and world accommodation are separate from hit detection. There are no traversal penalties. Carriage is validated within +8° to +10° without ground contact.

**OPEN:** actual world-fit validation of the extreme tails (~170 cm behind the heel), collision policy, clearance standards, and therefore the final tail range itself (L2738, L3620, L4017).

**Frozen reference embodies:** reference tail 121.4 cm (64.6 % H), and diagnostic extremes (208 cm + 80 % → 170 cm reach).

**Effect on the central reference body:** **not a blocker** for the reference (64.6 % H is central). It is a **blocker for finalizing the 55–80 % envelope** (L2738 makes world validation a precondition for approving final tail ranges) and for RM-UB-04 becoming canon.

**Candidate classification: E.** World, furniture, collision and camera system work, explicitly routed to Part 5 and §251.
- *Suggestion (S12):* run SAU-BODY-20 / SAU-WORLD-01–05 first at the 208 cm + 80 % Broad extreme. It is the single worst case canon identifies (~170 cm reach).

---

## 2.8 Acquired tail, rostral and jaw loss

**Canon text**
- [OPEN] §11a. — "Major tail loss remains an OPEN injury-system question and is never a normal creator substitute." (SAUR L209)
- [POS] Acquired minor states are allowed. — "scars, damaged scales, chipped keratin, localized pigment change, occupational wear and minor healed injuries." (SAUR L209)
- [OPEN] §113. — "Major tail, rostral or jaw loss remains OPEN as established previously." (SAUR L1876)
- [OPEN] §133. — "Major rostral, jaw or tail loss remains OPEN." (SAUR L2181)
- [POS] §133. — "Acquired history is not genetic inheritance." (SAUR L2183)
- [BAN] §142A excludes loss from randomization. — "Major rostral, jaw or tail loss remains OPEN and is excluded from randomization until explicitly designed." (SAUR L2326)
- [POS] §225 authority. — "It is never removed, toggled off, or hidden" (SAUR L3549)
- [OPEN] §225. — "Acquired tail loss/injury remains OPEN and is not equivalent to a creator toggle." (SAUR L3559)
- [OPEN] §249. — "acquired major rostral loss;" (SAUR L4014); "acquired major jaw loss;" (SAUR L4015); "acquired tail loss/injury;" (SAUR L4016)
- [BAN] UCCA. — "Acquired never creates major tail, rostral or jaw loss." (UCCA L264)
- [OPEN] UCCA. — "Acquired tail loss/injury remains OPEN and is never generated." (UCCA L150)
- [POS] Displays: breakage belongs to the acquired layer. — "breakage and injury belong to the acquired/presentation-history layer." (SAUR L4201)

**Closed qualitatively:** minor acquired states are supported and randomizable. Major loss is never generated, never a creator toggle and never a substitute for the mandatory tail. Acquired is not inherited.

**OPEN:** whether and how major loss exists at all (injury system).

**Frozen reference embodies:** nothing. The reference is intact and the question does not apply.

**Effect on the central reference body:** **not a blocker.**

**Candidate classification: E** (injury, acquired-history and gameplay system), with **D** for the biology of healing.
- *Suggestion (S13):* none needed. The current ban-plus-OPEN state is fully specified for creator purposes.

---

## 2.9 Thermoregulation

**Canon text**
- [OPEN] §124. — "thermoregulation/metabolic strategy; no automatic cold vulnerability, heat resistance or temperature-related gameplay modifier is implied while OPEN;" (SAUR L2050)
- [OPEN] §249. — "thermoregulation/metabolic strategy;" (SAUR L4013)
- [OPEN] §250 (gameplay). — "any environmental resistance/vulnerability." (SAUR L4062)
- [BAN] §250. — "No OPEN item should be inferred from visual anatomy." (SAUR L4064)
- [POS] Soft tissue is not prohibited (relevant to any cold-blooded-means-lean inference). — "Adipose tissue is not prohibited by scales or reptilian ancestry." (SAUR L379)
- [BAN] "No universal “dry lizard” silhouette is allowed." (SAUR L381)
- [SILENT] No section authors ectothermy, endothermy or any intermediate strategy. A grep for "temperature", "heat", "cold" or "bask" returns only L2050 for this topic.
- [SILENT] §265 does not list thermoregulation. It is carried through §124, §249 and UCCA L355.

**Closed qualitatively:** no implied gameplay temperature modifiers. Anatomy does not imply a strategy.

**OPEN:** the metabolic and thermoregulatory strategy.

**Frozen reference embodies:** nothing relevant.

**Effect on the central reference body:** **not a blocker.** No anatomy depends on it per canon.

**Candidate classification: D.** This is later biology, firewalled from gameplay.
- *Suggestion (S14):* none. If authored later, it must not retroactively alter the frozen anatomy (§252 principle: "No choice in this list may retroactively redefine approved anatomy.", SAUR L4101).

---

## 2.10 Tail-equipment construction and coverage

**Canon text**
- [POS] Permission is resolved. — "armor, clothing and accessories may partially cover, drape over or sheath the tail, provided it remains a persistent anatomical and silhouette feature." (SAUR L1895)
- [OPEN] Construction. — "exact tail-equipment construction remains OPEN (§251)." (SAUR L1895)
- [BAN] Equipment never implies an optional tail. — "Equipment design must never imply that the tail is biologically optional." (SAUR L1905)
- [POS] Applied presentation on the tail. — "Armor and clothing may cover or lie on the tail but cannot cosmetically erase its presence." (SAUR L211)
- [POS] §194, pelvic and tail-base equipment. — "Waist, hip and pelvic equipment must accommodate the integrated caudal base." (SAUR L3112)
- [OPEN] §194. — "Exact equipment construction remains later design work." (SAUR L3120)
- [POS] §195 permission. — "may partially cover, drape over or sheath portions of the tail" (SAUR L3124)
- [BAN] §195. — "use clothing as a substitute for solving tail fit." (SAUR L3131)
- [POS] §195 preservation list. — "collision/clearance assumptions;" (SAUR L3139)
- [BAN] §195. — "Full concealment cannot be used to validate an otherwise incorrect Saurin body." (SAUR L3142)
- [POS] §225. — "Coverage cannot make a Saurin functionally tailless." (SAUR L3551)
- [OPEN] §251. — "tail equipment construction and coverage extent (permission to cover resolved §195/§225);" (SAUR L4069)
- [OPEN] UCCA. — "tail-equipment construction and coverage extent remain OPEN." (UCCA L149)
- [TEST] SAU-EQP-03. — "Pelvic armor at tail-base extremes" (SAUR L3435)
- [TEST] SAU-EQP-04. — "Cloak/backpack/sheath vs tail sweep" (SAUR L3436)

**Closed qualitatively:** partial cover, drape and sheath are permitted. The tail must never be erased, hidden at the base or made functionally absent, and coverage can never stand in for valid anatomy. Articulation, mass, taper and clearance must be preserved.

**OPEN:** construction method and coverage extent (how much can be covered).

**Frozen reference embodies:** nothing beyond the naked tail anatomy that equipment must fit.

**Effect on the central reference body:** **not a blocker.** §195 L3142 explicitly forbids using equipment to validate the body, so body validation is naked-first by rule.

**Candidate classification: E** (equipment system).
- *Suggestion (S15):* the coverage-extent half could become **B**: author a qualitative ceiling now (for example "caudal base and some visible tail length always readable in silhouette"). §195 L3127–L3129 already implies this without numbers.

---

## 2.11 Other §265 OPEN items not on the requested list

1. [OPEN] "Absolute (rather than reference-relative) balance limits once posture is fixed." (SAUR L4264). Tied to 2.1. **Classification E**, after posture.
2. [OPEN] "Cross-race numeric rostral-floor comparison (Marchfolk, Grask, Gorrund normalized midface/rostral projection ranges) in the universal comparative review." (SAUR L4266)
   - Related canon: "the cross-race numeric check (§146) is OPEN because Marchfolk, Grask and Gorrund canon contain no numeric projection ranges." (SAUR L4181)
   - Queue: RM-CF-01–05 (RMQ L50–L54); the Grask item runs only after Grask's projection distribution is authored (RMQ L52).
   - **Classification C.** It depends on other races' authored distributions plus measurement. The reference rostral index 0.288 is embodied on aff1b52 (SAUR L4181).
3. [OPEN] "Population adipose tendencies." (SAUR L4268). The canon form is "Exact population adipose tendencies remain OPEN." (SAUR L4172). The diagnostic candidate pattern is SREG L103 (not canon). **Classification B.** A direction exists in canon (fat regions listed at L4172), and the tendencies and weights come later.
4. [OPEN] "Display mass-moment limit and neck clearance through head/neck range of motion; prominent horns/spikes/plates beyond the validated families (§100) and crest heights above ~2.5 cm." (SAUR L4269). **Classification E/C.** Range of motion is animation, and the moment limit needs measurement. The frozen display family and crest of 2.43 cm are embodied (SAUR L4197).
5. [OPEN] "Orbital placement/spacing tolerance." (SAUR L4270). Locked in canon: "their numeric tolerance is OPEN (no clean validation without rebuilding the brow/postorbital planes)." (SAUR L4187). Queue RM-UF-03 (RMQ L69). **Classification C.** The locked placement is embodied on aff1b52.
6. [OPEN] "Reproductive life history and physiology (§263); statistical spreads of the sex-shifted distributions around their centres." (SAUR L4273). **Classification D** (reproduction) plus **B** (spreads: the centres are authored at L4227–L4230, the spreads come later).
7. [OPEN] "Statistical calibration of soft distributions" (SAUR L4275). Also: "Soft distributions remain provisional." (SAUR L4259). **Classification B/E.** Centres exist, and calibration is generation-system work. UCCA L113 notes that Saurin §263 centres are "the only authored soft centres" roster-wide.

The §265 entries "Numeric lower-trunk minimum …", "Hand and foot claw / digit numeric ranges", "Numeric per-field scale ranges", "Exact caudal-base landmark" and "World-space validation of the longest tails" are covered in 2.2–2.7.

**Discrepancy noted.** The closure review's §4 list (SCLO L112–L126) still includes "13. Sex-related anatomy." (SCLO L124). The spec's §265 replaced that entry after §263 closed on October 5 (SAUR L4213, L4273). Canon (SAUR) governs. The review is historical.

**Cross-link to Part 1.** RM-OT-04, "Saurin vs Sagekin and Halvren matched-height checks (body and face)" (RMQ L92), uses a Halvren stature. Under UCCA L297 and GRASK L150 it must use a valid Halvren configuration. Saurin overlap (168–208) lies wholly inside the Halvren central envelope, so this check needs **no** Halvren tail. **Derived.**

## 2.12 Candidate classification — Part 2 summary

| # | Item | Class | Blocks central reference body? | Frozen ref (aff1b52) embodies a value? | One-line justification |
|---|---|---|---|---|---|
| 1 | Balanced posture and density model | **E** (+D density) | No; anatomy not reopened (SAUR L4162) | Yes, diagnostic: CoM 6.3 cm behind heel; 8.8° lean; +3° relative guard | Canon routes it to the posture/locomotion/animation phase |
| 2 | Caudal-base landmark | **A** (C if a new landmark is chosen) | No; latent validation risk for all % H figures | Yes, de facto: posterior-pelvic-plane axis point, 121.4 cm / 64.6 % H | Definitional; ratifying the diagnostic convention needs no new work |
| 3 | Numeric lower-trunk minimum vs Marchfolk | **C** | No | Yes: 32.0 cm at 187.9 cm; ±10 % bound | Marchfolk canon has no trunk number, so a Marchfolk mesh is needed |
| 4 | Numeric Broad-vs-Gorrund boundary | **C** | No (reference is Balanced) | Partly: Broad multipliers are diagnostic only | Gorrund has no numeric ratios, and stature overlap is only at ~208 cm |
| 5 | Claw/digit ranges | **E** (+C) | No | Yes: reference claws; +15 % foot-claw ground-contact point | Canon: cannot be validated without grip pose and equipment |
| 6 | Per-field scale ranges | **C** | No | Topology yes; ranges no (register ±20/25/10 % not canon) | Needs geometric validation per field |
| 7 | Tail world-space validation | **E** | No for the reference; yes for final tail-envelope approval (L2738) | Yes: 121.4 cm reference; diagnostic 170 cm reach at 208 cm + 80 % | World, collision and furniture system work |
| 8 | Acquired tail/rostral/jaw loss | **E** (+D) | No | N/A | Injury system; already banned from generation |
| 9 | Thermoregulation | **D** | No | N/A | Later biology; gameplay-firewalled |
| 10 | Tail-equipment construction/coverage | **E** (coverage extent could be B) | No (equipment can never validate a body, L3142) | N/A | Equipment system; permission already resolved |

**Labelled suggestions (consolidated).**
- S1: canonize the Halvren tail-contributor table (1.5).
- S2: canonize the qualitative upper-wider-than-lower tail asymmetry.
- S3: bound the Halvren tails qualitatively, strictly inside the source union (147–229) and short of the named source extremes.
- S4: add tail source-passing tests (HV-50 vs Skarn and Aelari; HV-49 vs Marchfolk).
- S5: decide tail reachability without lineage.
- S6: keep the +3° relative guard as the only balance validator until animation.
- S7: ratify the posterior-pelvic-plane caudal-base landmark.
- S8: add a −10 % lower-trunk vs matched-height Marchfolk test.
- S9: declare the frame-scope ban plus d/w ≤ 1.00 as the interim never-Gorrund rule.
- S10: present the +15 % foot-claw coupling as an explicit rule.
- S11: queue a body scale-field RM item.
- S12: run world validation first at the 208 cm / 80 % Broad worst case.
- S13: no change for acquired loss.
- S14: no change for thermoregulation.
- S15: author a qualitative tail-coverage ceiling.

None of these is canon. Each needs author acceptance.

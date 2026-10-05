import json
D = '/home/claude/wayfarer-design/tools/pass2/'
rows = json.load(open(D + 'conforming_rows.json'))
def cell(s):
    return s.replace('|', '\\|').replace('\n', ' ⏎ ')

TITLES = {
 'E1': 'E1. Muscular Development Capacity (Skarn "natural muscle volume" and relatives)',
 'E2': 'E2. Comparator wording still ambiguous after the "unqualified human = Marchfolk HRP" rule',
 'E3': 'E3. "baseline"',
 'E4': 'E4. "Basic" as a creator mode/tier',
 'E5': 'E5. Saurin structural ridge vs keratin ridge',
 'E6': 'E6. Skin Appearance Layers → four (Natural / Environmental / Applied / Acquired)',
 'E7': 'E7. Stale process/status wording',
 'E8': 'E8. rules/character-creation-brief.md',
 'E9': 'E9. Saurin §263 process tokens',
 'E10': 'E10. Stale OPEN items already resolved by later canon (pointer/annotation, no deletion)',
 'E11': 'E11. Gorrund ID prefix and ambiguous Part.§ citations',
 'E12': 'E12. Sex-related terminology and R-SEX conformance',
 'E13': 'E13. Frame words inside composition lists',
}
NOTES = {}
NOTES['E1'] = """
Not edited: Halvren L427 (historical findings table quoting the old wording — leave as history); Durrim L381 "Muscle volume" (aging of Current Muscularity, correct sense); the six specs already using **Muscular Development Capacity** (Cogling, Grask, Pipkin, Saurin, Halvren, Gorrund) — capitalization varies ("muscular-development capacity" Gorrund L82/L691, Grask L138, Pipkin L123; "Muscular development capacity" Halvren L111/L443). Optional: normalize capitalization when PROJECT_RULES gains the glossary entry (order T-7); no row proposed.
"""
NOTES['E2'] = """
**Resolved by rule — counts only, no edits** (raw whole-word counts of `human`/`humans`, which include adjectival uses such as "human pelvis"; `near-human`; `human reference anatomy`):

| File | human(s) | near-human | human reference anatomy |
|---|---|---|---|
| AELARI | 35 | 0 | 0 |
| COGLING | 49 | 24 | 0 |
| DURRIM | 37 | 0 | 0 |
| FENN | 35 | 0 | 0 |
| GORRUND | 83 | 0 | 2 |
| GRASK | 75 | 0 | 5 |
| HALVREN | 162 | 0 | 0 |
| MARCHFOLK | 36 | 0 | 0 |
| PIPKIN | 42 | 2 | 0 |
| SAGEKIN | 22 | 0 | 0 |
| SAURIN | 122 | 0 | 0 |
| SKARN | 5 | 0 | 0 |
| VAEL | 36 | 0 | 0 |

Note: the adopted §3 rule covers unqualified "human" only; "near-human" (Cogling ×24, Pipkin ×2) is covered by the Pass-2 T-2 proposal ("within the Marchfolk adult envelope"), which the author order did not restate. **AUTHOR CONFIRM** that the T-2 near-human reading is adopted; otherwise Cogling needs a one-line definition (suggest at Cogling §3, first use: "near-human (within the Marchfolk adult envelope)").

**Located but no edit proposed — absolute-size consequences, true against any taller/smaller population, no implementation risk:**
Durrim L34 "Lower than equivalently proportioned taller humanoids" (centre of mass height); Durrim L433 stride "than much taller humanoids"; Durrim L357 "relative to other humanoids" (OPEN statement); Pipkin L56 "less absolute reach than tall populations", L723/L778/L891 "taller populations" (gait cycles, stride, reach), L861/L1074/L1277 "taller race(s)"; Cogling L2205 "larger humanoids", L2217/L2248 "taller races", L2598/L2602/L3063 validation-cast "larger/taller race"; Gorrund L76 "greater absolute cross-sectional structural scale than smaller humanoids"; Gorrund L82 "differs from humans or other races" (OPEN); Gorrund L150, L403 failure-mode labels ("a tall human", "other tall populations").
**Already named / acceptable:** Aelari L211 "robust humans such as Skarn"; Aelari L480/L598, Skarn L293, Vael L516 "robust human(s)" used as a description of Skarn; Grask L259/L429/L491 and Pipkin L141/L164/L270 "ordinary/normal human…" (rule resolves; Pipkin L164 already names Marchfolk).
"""
NOTES['E3'] = """
**Other "baseline" occurrences — different sense, no edit** (Saurin uses "baseline" consistently for *canonical species anatomy*, with "non-baseline" defined in §157 as an approved anatomical exception; this is neither comparator nor population centre):
Saurin L160 (§10 "All baseline Saurin possess a biological tail"), L265 (§15 heading "Plantigrade baseline"), L604, L830, L891, L932, L972, L1000 (historical), L1319, L1427, L1462, L1550, L1563, L1598, L1602, L1631 (historical quote), L1633, L1725, L1899, L1971, L2425, L2429, L2554 (×2, defines non-baseline), L2819, L3188, L3614, L3636, L3647, L3656, L4229.
Cogling L1721 "baseline melanin level" and L2046 "Natural — baseline pigmentation" (base/underlying level), L2591–2592 "Swim/Jump baseline" (validation of no-modifier behaviour). Gorrund L92 "locomotion baseline is upright humanoid bipedal" and L611 "as baseline" (canonical default motion), Grask L239 nails, L564 sclera/pupils, L618 ×2 locomotion (canonical anatomy/motion). STATUS.md L47 "first-pass biological/design baseline" (authority basis).
Optional (AUTHOR DECIDE): if "baseline" is to be retired everywhere, Saurin's sense maps to "canonical" ("All Saurin possess…", "canonical Saurin anatomy", "non-canonical exception").

**PROJECT_RULES:** no occurrence. **Brief** (L51, L67, L75, L84, L116 — "baseline" = Marchfolk comparator): covered by the E8 banner; if line edits are wanted, each → "the Marchfolk Human Reference Population".
**Register** (not in scope for edits): Marchfolk consistency resolution §6 already retires the term there.
"""
NOTES['E4'] = """
Also: register R:463 repeats "Basic Mode conceptually supports both" (supporting/historical; fix when the register is reconciled). Vael L600 already says "Simple and Advanced continuity" — consistent with E4-07.
**AUTHOR DECIDE (E4-01…06):** the Marchfolk v1.1/v1.2 "Basic" tier is an in-Customize quick tier, not Simple Mode (Simple Mode has no sliders). "Quick controls / Detailed controls" is a placeholder name per T-4.
"""
NOTES['E5'] = """
**Classification of all 48 lines (52 matches) containing "ridge" in SAURIN_V1.md**

| Class | Lines | Action |
|---|---|---|
| Structural (skull/body form, §36a) — already explicit | L669, L673, L692, L693 | none |
| Structural — implicit | L716 (§36a creator variation) | E5-01 |
| Human comparison | L793 "human-style brow ridge" | none |
| Keratin — already explicit ("keratin"/"keratinous"/"integumentary") | L205, L1640, L1843, L1970, L1981, L2034 | none |
| Keratin — implicit, now qualified | L1633, L1663, L1686, L1707, L1864, L1938, L1984, L2115, L2166, L2183, L2232, L2264 (×2), L2282, L2310, L2352, L2521, L2532, L2568, L2617, L2688, L2730, L3714 (×2), L3943, L3963, L4005, L4178 | E5-02…E5-35 |
| Both (structural strength + keratin display) | L2153 §132, L2508 §154, L2629 §161A, L3421 SAU-EQP-01, L3732 §235, L3779 §237, L3816 §239 | name both |
| Historical/superseded quotes | L671 (§36a status, see E10-05), L1631 (§100 quoting old rule), L2437 (§150 revision note) | none |
| §230 summary | L3654 + "no true horns" L3653 | E5-27 |

Related: §58 heading "Horn firewall" (L996) already carries a supersession banner; §59 list fixed by E5-36. "§113/§142A damaged low-profile ridges" → E5-06/E5-16 (drop the stale "low-profile" qualifier).
"""
NOTES['E6'] = """
Durrim, Grask and Gorrund name no Skin Appearance Layer count (no edit). Saurin §122 (L1977–1986) already has four layers and is the model. Register R:18/R:467 also say three (fix at register reconciliation).
**AUTHOR DECIDE:** "dirt" is listed under Applied-or-Acquired in Marchfolk/Skarn/Fenn/Aelari but under **Environmental** in Saurin §122. Rows E6-02/06/08/09 keep dirt in Applied to avoid reclassifying silently.
"""
NOTES['E7'] = """
**Noted, no edit (historical per-part lines, not headers/status):**
- "vX.0 stays in progress" in clarification patches: Durrim L232, L322; Grask L142, L304, L437, L568; Gorrund L256, L413, L564.
- "Part N is complete, and v1.0 as a whole isn't": Pipkin L123, L244.
- Forward references that remain true as written or are clearly dated: Durrim L66 ("aren't pre-designed here"), L259, L480 ("Gorrund once … defined"), L502 first sentence ("Once Pipkin and Cogling are designed…"), Durrim L145 (already updated: "Pipkin and Cogling are now designed"); Aelari L251 ("Halvren aren't designed now"), L295, L435; Vael L11, L171, L264, L286, L478, L592; Fenn L246, L260; Gorrund L647, L662 ("future Pipkin and Cogling… only once approved"); Cogling L27, L59, L3230 (already updated); Pipkin L1628 (already updated); Sagekin L238 (mixed ancestry "isn't designed").
- Marchfolk header / v1.2–v1.4 "pending further refinement" (true, not stale). Saurin header already current.
- Equal-height wording drift (F-11: Durrim 150 vs 152 cm; Gorrund–Grask 208–239 vs 218–229 cm) — numeric, not process wording; left for the Large-Race review.
"""
NOTES['E8'] = """
**Descriptors / statements in the brief that contradict approved canon** (banner E8-01 resolves authority; no line edits proposed):

| Brief line | Brief says | Canon |
|---|---|---|
| L25–31 "Three layers" | Race / Individual / Presentation model | Four Character Architecture Layers (PROJECT_RULES; amendment v0.1 later in the same file) |
| L135 amendment layer C | "Muscularity, fat distribution, …" | Body-Fat Amount and Body-Fat Distribution are separate (PROJECT_RULES; Marchfolk CRes §2) |
| L51, L67, L75, L84, L116 | "baseline" | Marchfolk Human Reference Population (Marchfolk CRes §6) |
| L52 Skarn | "thick joints", "Enormous humans" | Ranges, not identical proportions (Skarn v1.0 §3); "thickness" decomposed (Marchfolk CRes §3) |
| L54 Fenn | "Lean" | Fenn identity never depends on thinness (Fenn v1.0 §8) |
| L55 Aelari | "narrow waist" | No mandatory hip/waist width (Aelari v1.1 §2–5) |
| L56 Vael | "Lean and controlled, slightly larger eyes" | More compact, deeper-bodied (Vael header, v1.0); orbits "moderate to somewhat large", broad eye-size variation (Vael v1.2 §10–12) |
| L57 Halvren | "An in-between skeleton" | Developmentally viable mixed structure, not a linear morph (Halvren P2 §15–19) |
| L59 Grask | "Heavy torso, thick textured skin, dense muscle, strong swimmers. Regeneration" | Rangy, limb-dominant skeleton (P1 §1–2, P5 §101–105); skin thickness OPEN (P4 L508, L564); swimming a legacy gameplay trait, aquatic specialization not established (P1 §54–59); regeneration not approved anywhere in canon |
| L60 Gorrund | "long arms" | Superseded: large absolute arms, no unusual proportional reach (Gorrund FC §21–25) |
| L61 Pipkin | "large head" (also L68 "relatively large head") | Head secondary, never oversized (Pipkin P1 §5–11, P3 §3) |
| L62 Cogling | "expressive face" | Not a facial specification; not biologically more expressive (Cogling §26, §92) |
| L63 / L84 Saurin | 1.05× height; "possibly a modified leg and foot structure"; tail used for "swimming, acceleration" | Stature 168–208 cm (§4, §258); plantigrade (§15); tail never an automatic gameplay modifier (§201, §226) |
| L15 Movement | "Gorrund carry big momentum… Saurin move like reptiles" | Movement derives from anatomy; no automatic movement traits (Gorrund P5, Saurin P5) |
| Table L47 + all rows | height/mass multipliers | Superseded by each spec's provisional stature ranges; mass is derived, never a primary input (Skarn v1.1 §7) |
| L97, L125 | "three formal specifications" per race; "next task is Marchfolk v1.0" | Single `specs/<race>/<RACE>_V1.md`; all 13 FIRST-PASS COMPLETE |
| L133, L139–140 | "anatomical configuration" | Retired; use sex-related anatomy (order §3) |

Existing in-brief SUPERSEDED notes (Pipkin movement L15/L69, Cogling L62/L76–77) are consistent with canon and stay.
"""
NOTES['E9'] = """
Line references: §263 opens at L4198. E/B letters stay because §263's own table defines them ("Coelomic body-wall fullness (E)", "Ventral / ventrolateral fullness (B)"). "aff1b52" (header L3, Part 7 L4115) is a commit reference, not a process token — left (AUTHOR may prefer "frozen closure reference").
"""
NOTES['E10'] = """
Not proposed: Pipkin P5 §38 "Planned Part 6 scope" (historical, clearly dated). Elf review edit (E10-15) is in `reviews/`, not a spec — author may prefer to record Fenn low-light in the Fenn spec instead (Fenn v1.3 §9 already lists it as unresolved).
Also related but outside this order: register OPEN rows closed by later rows (05 §9) — handled at register reconciliation.
"""
NOTES['E11'] = """
**Gorrund prefix census (GORRUND_V1.md):** `GRR-` 30 occurrences on 25 lines (L127–L250): GRR-BODY-01…18 (BODY-01/02/03/06/09/10/11 ×2, BODY-04 ×3, BODY-16 ×3, others ×1) and GRR-STRESS-01 (02–09 written as bare numbers). `GOR-` 25 occurrences: GOR-EAR (+GOR-EAR-01), GOR-FACE-01…15 (FACE-12 ×2), GOR-SKIN-01, -11, -12, -13 (02–10 as bare numbers), GOR-MOVE, GOR-INT, GOR-EQUIP. **Proposal: GOR- throughout** (E11-01, one global replace; no "GOR-BODY" or "GOR-STRESS" ID exists yet, so no collision). External citations of GRR- in `reviews/claude-pass2-01/04/06` and `audits/10-gorrund.audit.md` stay historical.

**Per-Part § restarts:** Durrim, Grask, Gorrund, Pipkin (and Halvren, Skarn/Fenn/Aelari/Vael/Sagekin/Marchfolk per version). Recommended citation convention (no text edit): "Part N §x" / "vX.Y §x". Only the four dangling/ambiguous citations above are edited. The Grask housekeeping §101/§104 citations (L728) are unambiguous (only Part 5 reaches 101).
"""
NOTES['E12'] = """
**"configuration" uses with a sex-related qualifier — no edit** (qualified, unambiguous): Cogling L871, L2940; Pipkin L152; Saurin L556 (SAU-BODY-19), L1254 (SAU-FACE-19), L2015 (SAU-SURF-24). Different sense, no edit: Durrim L436 "no body configuration needing a different kind of locomotion", Pipkin L1293 "extreme valid body configurations". Register L252 "anatomy configuration" (fix at reconciliation). Brief L133/L139/L140 (E8 banner).

**Correction to Pass-2 T-8:** Vael L600 "body configuration" is the Vael copy of Aelari §20–21's "skeleton and body" list item, not the sex-related category (E12-03).

**R-SEX conformance audit (13 specs): no conflict found.** Every non-Saurin spec either leaves sex-related anatomy OPEN with explicit anti-dimorphism guards (Durrim P1 §37–39, P3 L219/L222; Grask P1 L76, P3 L400/L429; Gorrund P1 L82, P3 L407, P4 L556; Pipkin P1 L72, P3 L373; Cogling §21-area L339, §61, L779, L1813; Halvren P1 §19–22; Vael v1.1 L128; Marchfolk v1.0 L23/L35 "no hard sex-specific height restriction… population distributions may differ… overlap stays broad") or says nothing. No spec sets hard sex bounds, forces frame/stature/muscle/fat/face/displays/coloration, or assumes human dimorphism. Saurin §154, §235, §263–264 match R-SEX exactly (identical hard bounds, mandatory overlap, soft centres only).
Minor notes (no conflict): Pipkin P2 L152 / PIP-BODY-28/29 / PIP-FACE-22/23 / PIP-INT-21 use male-vs-male / female-vs-female like-for-like comparisons — compatible with R-SEX (they test comparison hygiene, not magnitudes). "feminized/masculinized" guards (Halvren P3 L174–177; Pipkin P2 L149) are anti-stereotype language only (T-8); keep. Stale "pending the universal system" pointers: Durrim L58 (E10-16), Durrim L207, Grask L400, Gorrund L361, Pipkin L373 — optional identical pointer "(universal rule: R-SEX; magnitudes OPEN)".
"""
NOTES['E13'] = """
Not edited: Fenn L345, Aelari L159/L468, Vael L150/L151/L517 etc. — explicit "Frame and composition" combination tests, already correct usage. Grask L31 "looking relatively lean compared with total height" is the definitional sentence for E13-04 (keep; optional "relatively slender"). Grask "rangy" (P1 L5, L9, L29; header) is explicitly defined as skeletal in §6–7 — keep (race-specific vocabulary). Marchfolk "physique" (v1.1 §1 table, v1.0 L35) and "thickness" (Skarn v1.1 §8 "Limb thickness") flagged by T-9 but outside this order's list.
"""

out = ["# Conforming-Edit Plan — Pass 2 resolution sequence §7 (author-reviewable, NOT APPLIED)",
"",
"**Basis:** `reviews/chatgpt-pass2-resolution-sequence-order.md` §3–4, §7. **Scope:** 13 canonical specs, `specs/STATUS.md`, `decisions/PROJECT_RULES.md`, `rules/character-creation-brief.md` (+1 row in `reviews/elf-comparative-review.md`). No repo file was edited.",
"",
"**How to read the rows.** `Current` is the exact string to replace (verified: occurs exactly once in the file at HEAD `eb837b8`, except E11-01 = 30). In the tables `⏎` marks a newline and `\\|` a literal pipe. All 166 rows were applied sequentially in memory with zero misses. The raw strings (no escaping) are in `tools/rows.json` next to this file for programmatic application (`str.replace(cur, new)`, file order as listed). Line = line of the first character of `Current`. Section = Part/version heading > § heading.",
"",
"Rows marked **AUTHOR CONFIRM** add an interpretation the canon does not state explicitly; all others are terminology/pointer edits only. No row changes a race's positive anatomy.",
""]
by = {}
for r in rows: by.setdefault(r['id'].split('-')[0], []).append(r)
summary = ["| Item | Rows | Files |", "|---|---|---|"]
for k in TITLES:
    rs = by.get(k, [])
    summary.append(f"| {k} | {len(rs)} | {', '.join(sorted(set(r['f'].split('/')[-1].replace('_V1.md','').replace('.md','') for r in rs)))} |")
out += ["## Summary", ""] + summary + [""]
for k, t in TITLES.items():
    out += [f"## {t}", "", "| ID | File | Line | Section | Current (verbatim) | Proposed | Reason |", "|---|---|---|---|---|---|---|"]
    for r in by.get(k, []):
        out.append(f"| {r['id']} | {r['f']} | {r['line']} | {cell(r['sec'])} | {cell(r['cur'])} | {cell(r['new'])} | {cell(r['why'])} |")
    out += ["", NOTES.get(k, '').strip(), ""]
open(D + 'conforming_edits.md', 'w').write('\n'.join(out))
print(summary)

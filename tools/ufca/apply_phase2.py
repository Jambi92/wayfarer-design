"""UFCA Phase 2 minimal conforming edits (order: reviews/chatgpt-ufca-phase2-canonicalization-order.md §6).
Each edit inserts a pointer paragraph after a unique anchor line or replaces a unique substring;
Note: after the regression audit, wording fixes were applied directly (OPEN-list annotations changed from "resolved" to "canonicalized; UFCA closure pending author review"; Durrim depth-domain and Gorrund coverage wording). See reviews/claude-ufca-phase2-canonicalization-report.md §8.
every anchor must occur exactly once. Original text is preserved."""
import pathlib, sys
R = pathlib.Path(__file__).resolve().parents[2] / "specs"
D = "October 5, 2026"
PTR = ("**UFCA status (UFCA Phase 2, {d}):** the universal facial creator organization is now canonical in "
       "`decisions/UFCA_V1.md`. The {race} facial control organization in this spec stays as approved requirements and is routed to its "
       "UFCA slots (`reviews/claude-ufca-08-phase1-architecture-audit.md` Appendix A); {race} anatomy, tendencies, validators, tests and OPEN items are unchanged.")
EYE = (' Under UFCA AC-U1, "eye size" in this spec means bony orbit size (direct control) plus visible eye aperture (direct control); '
       "eyeball size is derived from the orbit and is never an independent slider.")

def ptr(race, extra=""):
    return PTR.format(d=D, race=race) + extra

EDITS = [
 # (file, anchor substring identifying a whole line, inserted paragraph)  -> insert after that line
 ("marchfolk/MARCHFOLK_V1.md", "**Classification (Durrim consistency-resolution patch):** the three-level facial editing model",
  ptr("Marchfolk", " The three editing levels map to Starting Face / Quick controls / Detailed controls, and the seven regions to UFCA slots 2–9 with asymmetry in slot 13. "
      "Orbit and midface controls are bound, as required by the v1.5 face validation (§2–6). Forehead controls stay hidden pending author confirmation, because this spec does not state forehead variation (UFCA §19.2).")),
 ("skarn/SKARN_V1.md", "**Interpretation (Durrim consistency-resolution patch):** \"the same seven regions as Marchfolk\"",
  ptr("Skarn", " Mouth and lips are bound through normal human-family coverage (UFCA AD-U12; a coverage clarification, not new Skarn anatomy). "
      "Ears use the human-auricle family (Pass 2 AC-4)." + EYE)),
 ("sagekin/SAGEKIN_V1.md", "**Classification (race-specific facial-control organization status):** where this spec defines facial regions",
  ptr("Sagekin", " Ears use the human-auricle family (Pass 2 AC-4)." + EYE)),
 ("fenn/FENN_V1.md", "**Classification (race-specific facial-control organization status):** where this spec defines facial regions",
  ptr("Fenn", " Brow structure and brow-to-eye distance are bound as stated in §2–7; forehead height/slope and further brow dimensions stay hidden pending author confirmation (UFCA §19.2)." + EYE)),
 ("aelari/AELARI_V1.md", "**Classification (race-specific facial-control organization status):** where this spec defines facial regions",
  ptr("Aelari", EYE)),
 ("vael/VAEL_V1.md", "**Classification (race-specific facial-control organization status):** where this spec defines facial regions",
  ptr("Vael", EYE + " Naturalize Face stays provisional (UFCA §19.1).")),
 ("halvren/HALVREN_V1.md", "**Classification (race-specific facial-control organization status):** the possible Advanced Mode facial organization above",
  ptr("Halvren", " \"Overall relationships\" maps to UFCA slot 1 (facial soft tissue); no broad relationship tools exist in v1 (UFCA AD-U3). "
      "Genealogy, ancestry-derived constraints and phenotype follow UFCA §11, consistent with the critical system distinction in the consistency resolution below.")),
 ("durrim/DURRIM_V1.md", "**Universal Facial Customization Architecture is deferred until all 13 first-pass races are complete**",
  ptr("Durrim", " Durrim binds the shared regional controls where its anatomy states variation (UFCA AD-U12). The depth domains A–E remain diagnostic/validator-only, never sliders. "
      "Sclera/ocular-tissue visibility is not a player control pending author confirmation (UFCA §19.2). Facial technical architecture stays OPEN.")),
 ("grask/GRASK_V1.md", "No universal facial-control hierarchy is finalized: any control organization proposed during Grask first-pass work",
  ptr("Grask", " The required anatomical coverage and named invalid combinations above are bound and enforced under UFCA. Prognathism and tusk-like canine questions stay OPEN, and projection is drawn only from authored central values until its distribution is authored.")),
 ("gorrund/GORRUND_V1.md", "> **Gorrund face-control organization is an APPROVED FIRST-PASS FUNCTIONAL REQUIREMENT / PROVISIONAL CONTROL ORGANIZATION.**",
  ptr("Gorrund", " Transverse Structural Continuity stays a validator, never a slider. Prognathism and tusk-like canine questions stay OPEN.")),
 ("pipkin/PIPKIN_V1.md", "Race-specific facial controls remain **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION** pending",
  ptr("Pipkin")),
 ("pipkin/PIPKIN_V1.md", "There is no \"Pipkin Face\" master slider. Validity is relationship-aware.",
  "**Natural facial asymmetry (author confirmation UFCA AC-U3, " + D + "):** ordinary biological left/right facial variation is available to Pipkin, consistent with the universal individuality architecture. "
  "It does not create deformity, pathology, juvenile cues, a racial identifier or an acquired-injury system, and it stays distinct from Acquired history."),
 ("cogling/COGLING_V1.md", "Controls may later be split, merged, renamed or reorganized during the Universal Facial Customization Architecture Review.",
  ptr("Cogling", " The sex-related anatomy capability is met by the body-level sex-related anatomy selection plus any canonically permitted soft facial distribution; there is no face-level sex slider and the magnitude stays OPEN (UFCA AC-U2).")),
 ("saurin/SAURIN_V1.md", "The following are **first-pass functional requirements / provisional control organization**, consistent with the project-wide facial architecture status.",
  ptr("Saurin", " Saurin routing follows UFCA §12: rostral controls sit in Rostrum & Lateral Face, nasal openings in Nasal Openings, the mouth line in Mouth Line, the jaw in Jaw, auricular controls in Auricular Openings, "
      "structural ridges in Cranium & Forehead and the keratin display in Hair / Cranial Display. No human forehead, cheek, chin, lip, nose or pinna controls exist (UFCA AC-U4). "
      "Orbital spacing below is Bound-locked by §259, which governs.")),
]
REPL = [
 ("pipkin/PIPKIN_V1.md", "- final creator-facing facial-control organization;",
  "- final creator-facing facial-control organization (resolved: `decisions/UFCA_V1.md`, " + D + ");"),
 ("pipkin/PIPKIN_V1.md", "- Universal Facial Customization Architecture Review;",
  "- Universal Facial Customization Architecture Review (performed; canonical in `decisions/UFCA_V1.md`);"),
 ("cogling/COGLING_V1.md", "- the Universal Facial Customization Architecture Review;",
  "- the Universal Facial Customization Architecture Review (performed; canonical in `decisions/UFCA_V1.md`);"),
 ("saurin/SAURIN_V1.md", "- Universal facial-control architecture and statistical calibration of soft distributions.",
  "- Statistical calibration of soft distributions (the universal facial-control architecture is resolved by `decisions/UFCA_V1.md`, " + D + ")."),
 ("durrim/DURRIM_V1.md", "facial technical architecture; the Universal Facial Customization Architecture; mount compatibility;",
  "facial technical architecture; mount compatibility;"),
]
DURRIM_NOTE = ("durrim/DURRIM_V1.md", "These stay OPEN and aren't resolved just to declare the race complete:",
  "*(UFCA Phase 2, " + D + ": the Universal Facial Customization Architecture, formerly listed above, is canonical in `decisions/UFCA_V1.md`; facial technical architecture stays OPEN.)*")

def main():
    files = {}
    def get(f):
        if f not in files: files[f] = (R / f).read_text().split("\n")
        return files[f]
    for f, a, b in REPL:
        lines = get(f); hits = [i for i, l in enumerate(lines) if a in l]
        assert len(hits) == 1, (f, a, len(hits))
        lines[hits[0]] = lines[hits[0]].replace(a, b)
    for f, a, ins in EDITS + [DURRIM_NOTE]:
        lines = get(f); hits = [i for i, l in enumerate(lines) if a in l]
        assert len(hits) == 1, (f, a, len(hits))
        i = hits[0]
        lines[i+1:i+1] = ["", ins]
    for f, lines in files.items():
        (R / f).write_text("\n".join(lines))
    print("applied", len(EDITS) + 1, "insertions,", len(REPL), "replacements in", len(files), "files")
main()

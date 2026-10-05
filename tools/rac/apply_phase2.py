"""RAC Phase 2 minimal canonical edits (order: reviews/chatgpt-reference-anatomy-closure-phase2-order.md).
REPL: replace a unique substring. INSERT: add a paragraph after the unique line containing the anchor.
APPEND: add a Reference-anatomy status note at the end of each race spec.
Every anchor must occur exactly once. Anatomy, numbers, tests and OPEN items are otherwise unchanged.
Note: after the regression audit, further fixes were applied directly (Gorrund approved-list body-hair line; Grask GR-FACE-14 definition and
envelope clause; parenthesis normalization). See reviews/claude-rac-phase2-canonicalization-report.md §6."""
import pathlib
S = pathlib.Path(__file__).resolve().parents[2] / "specs"
D = "October 5, 2026"
RA = "`decisions/REFERENCE_ANATOMY_V1.md`"
T = f"(RAC Phase 2, {D})"

REPL = [
 ("durrim/DURRIM_V1.md", "greater torso and lower leg and overall limb contribution to total height",
  "greater torso contribution and lower (leg and overall limb) contribution to total height"),
 ("durrim/DURRIM_V1.md", "Body-hair biology is OPEN, identity never comes from universal hairiness",
  f"Body hair may occur with broad individual variation in density and distribution; it is never universal, never a racial identifier and never inferred from size or stature (RAC Phase 2, {D}; AD-R23). Sex-related and population distributions stay OPEN, identity never comes from universal hairiness"),
 ("grask/GRASK_V1.md", "Body-hair distribution is **OPEN**, without universal hairiness.",
  f"Body hair may occur with broad individual variation in density and distribution; it is never universal, never a racial identifier and never inferred from size or stature (RAC Phase 2, {D}; AD-R23). Sex-related and population **distributions stay OPEN**, without universal hairiness."),
 ("gorrund/GORRUND_V1.md", "body hair is **OPEN**, never inferred from size.",
  f"body hair may occur with broad individual variation in density and distribution, never universal and never a racial identifier, and is never inferred from size or stature (RAC Phase 2, {D}; AD-R23); sex-related and population distributions stay **OPEN**."),
 ("pipkin/PIPKIN_V1.md", "Body-hair biology belongs to the later universal/race surface review. Pipkin do not require hairy feet or unusually hairy bodies.",
  "Body-hair biology is set in Part 4 §11 below (superseding the earlier pointer to a later review; RAC Phase 2). Pipkin do not require hairy feet or unusually hairy bodies."),
 ("grask/GRASK_V1.md", "or extreme underbite |",
  f"or extreme underbite. **Central projection (RAC Phase 2, {D}; AD-R41):** projection is **not** a Grask racial carrier; central anterior facial projection trends approximately within the Marchfolk adult central relationship, never shifted forward as a race; valid individual variation stays non-muzzle, non-ape-like and below the Saurin rostral floor; the long midface is a **vertical** relationship and is never converted into anterior prognathism. Greatest-valid-projection diagnostic: **GR-FACE-14**. The projection envelope numbers stay OPEN (RM-CF-03) |"),
 ("fenn/FENN_V1.md", "Slightly larger orbits, slightly more eye prominence, wide eye-angle range, distinct brow and orbit relationships |",
  f"Slightly larger orbits, slightly more eye prominence, wide eye-angle range, distinct brow and orbit relationships. **Reading (RAC Phase 2, {D}; AD-R44):** bony orbit size (ORB) slightly larger **and** visible presentation (aperture) slightly more open, two separately measured quantities (UFCA AC-U1) |"),
 ("saurin/SAURIN_V1.md", "- Exact caudal-base landmark for measuring tail length.",
  f"- Exact caudal-base landmark for measuring tail length — **resolved (RAC Phase 2, {D}; AD-R35):** the axis point at the posterior pelvic plane. Every §256 and §263 tail figure already uses it, so no number changes."),
 ("saurin/SAURIN_V1.md", "- Numeric lower-trunk minimum relative to Marchfolk (§6) and a numeric Broad-vs-Gorrund boundary.",
  f"- Numeric lower-trunk minimum relative to Marchfolk (§6) and a numeric Broad-vs-Gorrund boundary. Numbers stay OPEN; interim rules (RAC Phase 2, {D}; AD-R36): the −10 % lower-trunk Saurin at 168 cm and at 203 cm, against matched-stature Marchfolk, must still show the longer lower-trunk relationship; the frame-scope ban (§258: frame never changes axial lengths or pelvic depth) plus the thoracic d/w ≤ 1.00 guard is the interim structural never-Gorrund boundary."),
 ("saurin/SAURIN_V1.md", "- Numeric per-field scale ranges.",
  "- Numeric per-field scale ranges (body fields queued as RM-UB-08; RAC Phase 2)."),
]

INSERT = [
 ("saurin/SAURIN_V1.md", "**Reconciliation T-1 (UCCA Phase 2, October 5, 2026; `decisions/UCCA_V1.md`):**",
  f"**Metric note (RAC Phase 2, {D}; AD-R13):** this section speaks of head-**height** share (head height ÷ standing height); the §258 bound is on head **length** ÷ standing height, which includes the rostrum. They are different measurements, which is why T-1 found no conflict. No number is added."),
 ("gorrund/GORRUND_V1.md", "moderate forward projection may be valid without a muzzle, snout or ape-like prognathism, and the prognathism distribution is **OPEN**",
  f"**Projection comparator (RAC Phase 2, {D}; AD-R42):** \"moderate\" forward projection is moderate **relative to the Marchfolk adult range**. The maximum-valid projection case for measurement (RM-CF-04) is **GOR-FACE-05** (greater facial depth: never a muzzle, ape-like face or extreme prognathism). Facial depth and Transverse Structural Continuity stay separate from projection. The distribution's numbers stay OPEN."),
 ("gorrund/GORRUND_V1.md", "Projection from the attachment is generally **short-to-moderate relative to elven and Grask long-ear possibilities** (range **OPEN**).",
  f"**Ear variables (RAC Phase 2, {D}; AD-R43):** two variables are kept separate. (i) **Auricle projection from the skull:** population tendency close-set, individual range lower → greater (clarification below). (ii) **Outward extent:** short-to-moderate relative to elven and Grask long ears (this paragraph). The OPEN range applies to both, measured separately (RM-UF-02)."),
 ("grask/GRASK_V1.md", "never \"large Fenn ears on a troll head.\" Length ranges from modera",
  f"**Ear length (RAC Phase 2, {D}; AD-R43):** Grask ear length is read **relative to head height**, from moderate to strong elongation; the longest valid case is the GR-EAR-02 class. No comparator to elven maxima is implied. Base size stays in the measured variable set. Exact ranges stay OPEN (RM-UF-02)."),
 ("halvren/HALVREN_V1.md", "Exact tail heights are unresolved until the ancestry-dependent distribution is designed.",
  f"""**Stature-tail authorship (RAC Phase 2, {D}; AD-R28–R34; `reviews/claude-rac-09-halvren-stature-tail-authorship.md`):**
- **H-5 (outer bounding rule):** inherited stature tails stay strictly inside the union of source-population stature extremes, currently 147–229 cm, and never automatically reach a named source population's own extreme. This is a bound, **not** the final Halvren minimum or maximum; RM-UB-05 determines the actual valid limits and frequencies. 152–213 cm stays the central envelope, not a hard clip.
- **H-1 (contributors, under H-5):** the lower tail is supported only by human-family ancestry, and among the sources only Marchfolk ancestry reaches below 152 cm; the upper tail by Skarn ancestry and Aelari ancestry. Fenn, Vael and Sagekin ancestry do not by themselves extend either tail.
- **H-2:** the tails are asymmetric in direction; the lower tail is narrower and has fewer contributing ancestries. No magnitude is set.
- **H-3:** a tail Halvren must remain Halvren against the matched-stature source it approaches. Permanent tests: HV-50 vs matched-stature Skarn and vs matched-stature Aelari; HV-49 vs matched-stature Marchfolk, each under N3/N4.
- **H-4:** a tail stature is valid only if the whole body reaches it through Halvren mixed development (coherent segment shares, allometry and joints), never by one source's stature on another source's proportions.
- **H-6:** tails are minority outcomes relative to the central envelope; no ordering between upper and lower tail is authored.
- **Reachability (Y-2):** valid tail statures may be created manually without a player-entered genealogy and may appear through Extreme biological randomization, under the same hidden inheritance/development validity system, source-protection tests and eventual frequency weights. This creates no ancestry-percentage slider, no visible genealogy requirement and no guaranteed random access to source extrema."""),
]

COMMON = ("**Reference-anatomy status (RAC Phase 2, {d}):** the reference-anatomy method (approved reference meshes, reference composition, measurement stance, acceptance and circularity rules, measurement waves) is canonical in {ra}. Measurement has not started; no new numeric envelope is set. "
          "{race} directional constraints for measurement are consolidated in `reviews/claude-rac-03-pelvis-axial-closure.md` §2 and `reviews/claude-rac-04-segment-stature-closure.md` §2 (constraints, not magnitudes).")
EXTRA = {
 "Marchfolk": " **Sex-related anatomy:** ordinary human sex-related anatomy, with no race-specific shift unless separately authored (AD-R20, AD-R22). **Body hair:** ordinary human body-hair biology with broad individual variation, independent of hairstyle, culture, class and personality (AD-R24). **Facial hair** is biology (growth capability varies) as well as presentation. **Projection (AD-R40):** Marchfolk valid adult facial projection spans ordinary adult human variation; the most-projecting valid case is an adult human face with no muzzle-like or non-human maxillary architecture, embodied in the diagnostic head **MF-FACE-PROJ-MAX** (RM-CF-02). Marchfolk is the first measurement baseline (RM-UB-07).",
 "Skarn": " **Sex-related anatomy:** ordinary human sex-related anatomy, no race-specific shift unless separately authored (AD-R20, AD-R22). **Body hair:** ordinary human body-hair biology with broad individual variation, independent of hairstyle, culture, class and personality (AD-R24). **Facial hair** is biology as well as presentation. **Arm span:** no racial span tendency; span is derived from shoulder and segment anatomy (AD-R11). The v1.0 promise of later craniofacial ranges is discharged directionally by v1.2; numbers via RM-CF-09.",
 "Sagekin": " **Sex-related anatomy:** ordinary human sex-related anatomy, no race-specific shift unless separately authored (AD-R20, AD-R22). **Body hair:** ordinary human body-hair biology with broad individual variation, independent of hairstyle, culture, class and personality (AD-R24). The ribcage tendency is reduced **depth** (this spec governs; Halvren's normalization defers to it).",
 "Fenn": " **Sex-related external biology is deferred** to a later focused pass; human or humanoid soft tissue is not imported by assumption; independence rules stand (AD-R21). **Body hair stays hidden/deferred**; facial-hair permission is not extended to body hair. **Neck:** intermediate relative contribution among the elves (Aelari > Fenn ≥ Vael; Elf Comparative Review).",
 "Aelari": " **Sex-related external biology is deferred** to a later focused pass; human or humanoid soft tissue is not imported by assumption; independence rules stand (AD-R21). **Body hair stays hidden/deferred**; facial-hair permission is not extended to body hair.",
 "Vael": " **Sex-related external biology is deferred** to a later focused pass; human or humanoid soft tissue is not imported by assumption; independence rules stand (AD-R21). **Body hair stays hidden/deferred**; facial-hair permission is not extended to body hair.",
 "Halvren": " Stature-tail authorship (H-1…H-6, Y-2) is recorded in the height-envelope section above. **Sex-related anatomy and body hair follow the sources and development rules; nothing is invented inside Halvren** (AD-R22).",
 "Durrim": " **Sex-related anatomy:** no authored shift in skeleton, stature, frame or composition (R-SEX \"no shift\"); magnitude stays OPEN; second-configuration external biology needs per-race authorship and never transfers human patterns (AD-R18, AD-R22). **Body hair:** baseline above (AD-R23). **Terminology:** \"compact structural concentration\" (Short-Race Comparative Anatomy Review) names this spec's compact skeletal architecture. **Head share** is in the RM-CF-10 / RM-SR-04 measurement scope.",
 "Grask": " **Sex-related anatomy:** no authored shift in skeleton, stature, frame or composition; magnitude stays OPEN; second-configuration external biology needs per-race authorship and never transfers human patterns (AD-R18, AD-R22). **Projection, ears and body hair:** clarified in place above (AD-R41, AD-R43, AD-R23). The UFCA routing's \"authored central values\" for projection now refers to the central-projection statement in the Prognathism row.",
 "Gorrund": " **Sex-related anatomy:** no authored shift in skeleton, stature, frame or composition; magnitude stays OPEN; second-configuration external biology needs per-race authorship and never transfers human patterns (AD-R18, AD-R22). **Projection comparator, ear variables and body hair:** clarified in place above (AD-R42, AD-R43, AD-R23). The UFCA routing's \"authored central values\" for projection now refers to that comparator. Skarn–Gorrund torso/limb separation stays undetermined by design (AD-4).",
 "Pipkin": " **Sex-related anatomy:** no authored shift by default; the regions that may later shift are already named; magnitude OPEN; second-configuration external biology needs per-race authorship and never transfers human patterns; PIP-BODY-29 and other second-configuration tests wait (AD-R19, AD-R22). **Neck:** adult neck contribution within the human-adult range, neither Durrim-compact nor Aelari-elongated by default (AD-R7). **Arm span:** no racial span tendency; derived (AD-R11). **Trunk share (T-2):** constraints adopted (AD-R12); the numeric split stays deferred.",
 "Cogling": " **Sex-related anatomy:** no authored shift by default; regions already named; magnitude OPEN; second-configuration external biology needs per-race authorship and never transfers human patterns; the reference-preset requirement for multiple sex-related configurations waits for it (AD-R19, AD-R22). **Arm span:** no racial span tendency; derived (AD-R11). **OPEN question:** whether the \"roughly 11–13 cm\" adult head size is head height or head length.",
 "Saurin": " Saurin canon governs: the caudal-base landmark, the interim lower-trunk test and never-Gorrund rule, and the head-metric note are recorded in place (AD-R35, AD-R36, AD-R13). **Foot-claw coupling (AD-R37):** foot-claw length above ~+15 % requires a compensating curvature or tip change to preserve plantigrade contact (§261). Male-centre candidate: the closure reference aff1b52; female-centre candidate: the §263 female-centre configuration derived from it (the +10 % reference female is above the centre and is not this candidate); both still need the reference-mesh acceptance record. Sex-related anatomy stays exactly §263.",
}
APPEND = [("marchfolk/MARCHFOLK_V1.md","Marchfolk"),("skarn/SKARN_V1.md","Skarn"),("sagekin/SAGEKIN_V1.md","Sagekin"),
 ("fenn/FENN_V1.md","Fenn"),("aelari/AELARI_V1.md","Aelari"),("vael/VAEL_V1.md","Vael"),("halvren/HALVREN_V1.md","Halvren"),
 ("durrim/DURRIM_V1.md","Durrim"),("grask/GRASK_V1.md","Grask"),("gorrund/GORRUND_V1.md","Gorrund"),("pipkin/PIPKIN_V1.md","Pipkin"),
 ("cogling/COGLING_V1.md","Cogling"),("saurin/SAURIN_V1.md","Saurin")]

def main():
    texts = {}
    def get(f):
        if f not in texts: texts[f] = (S / f).read_text()
        return texts[f]
    for f, old, new in REPL:
        t = get(f); n = t.count(old); assert n == 1, (f, old[:60], n)
        texts[f] = t.replace(old, new)
    for f, anchor, para in INSERT:
        t = get(f); n = t.count(anchor); assert n == 1, (f, anchor[:60], n)
        i = t.index(anchor); j = t.find("\n", i); j = len(t) if j < 0 else j
        texts[f] = t[:j] + "\n\n" + para + t[j:]
    for f, race in APPEND:
        t = get(f).rstrip("\n")
        texts[f] = t + "\n\n" + COMMON.format(d=D, ra=RA, race=race) + EXTRA[race] + "\n"
    for f, t in texts.items():
        (S / f).write_text(t)
    print("edited", len(texts), "files")

if __name__ == "__main__":
    main()

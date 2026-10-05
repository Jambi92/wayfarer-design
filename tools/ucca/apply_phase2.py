"""UCCA Phase 2 minimal conforming edits (order: reviews/chatgpt-ucca-phase2-canonicalization-order.md §3, §5).
INSERT: add a paragraph after the unique line containing the anchor.
REPL:   replace a unique substring.
APPEND: add a UCCA status pointer at the end of each race spec.
Every anchor/substring must occur exactly once. Original text is otherwise preserved.
Note: after the regression audit, wording fixes were applied directly (Durrim Environmental sentence no longer calls sun exposure/weathering transient;
register Aelari preset line; RM-SR-05 152 cm). See reviews/claude-ucca-phase2-canonicalization-report.md §7."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
S = ROOT / "specs"
D = "October 5, 2026"
TAG = f"(UCCA Phase 2, {D}; `decisions/UCCA_V1.md`)"

INSERT = [
 # T-1 Saurin head share
 ("saurin/SAURIN_V1.md", "Exact proportional distributions remain OPEN and must still satisfy SAU-FACE-22.",
  f"**Reconciliation T-1 {TAG}:** this stature-share statement is a reference / central-morphology description. "
  "The §258 head-to-body creator bound (±8 %, head length 0.156–0.184 of standing height, with the +8 % head-scale decision as the centre) is authoritative for creator variation. "
  "The two describe different things and are not competing hard controls. No new number is introduced."),
 # T-2 Pipkin trunk-share absorption
 ("pipkin/PIPKIN_V1.md", "The reduced trunk share is absorbed primarily through **sustained limb contribution and pelvic vertical contribution, not through enlargement of the head**.",
  f"**Reconciliation T-2 {TAG}:** the absorption of the reduced trunk share is relationship-aware stature/proportion behaviour, never permission for global scaling or juvenile proportions. "
  "It operates inside the leg rule below (legs never automatically exceed ordinary human adult proportions; Pipkin are not defined by long legs), so the positive identity is the low-set compact trunk on a mature pelvic foundation. "
  "The numeric split between limb and pelvic contribution stays deferred (UCCA RM-UB-01; short-race RM-SR items); no winner is invented."),
 # T-9 Gorrund calluses
 ("gorrund/GORRUND_V1.md", "Calluses come from occupation, activity, footwear or repeated exposure, acquired rather than racial",
  f"**Callus layer (T-9 / AD-C9) {TAG}:** \"acquired rather than racial\" above means not racial. In layer terms, ordinary environmental callusing is **Environmental-persistent**; "
  "only a permanent, history-like tissue alteration is the **Acquired** layer. Neither is ever forced by race, class, culture or occupation."),
 # T-9 / AD-C9 Durrim environmental subtypes
 ("durrim/DURRIM_V1.md", "which are transient environmental states (Environmental Skin Appearance Layer).",
  f"**Environmental subtypes (AD-C9) {TAG}:** within the Environmental layer, sun exposure / tanning and weathering are **Environmental-persistent**; "
  "dirt, mud, dust, soot, sweat, water, blood, snow, frost and rain wetness are **Environmental-transient**. The separation from biological appearance above is unchanged."),
]

REPL = [
 # T-3 Aelari presentation presets: one system (v1.4 §4 governs)
 ("aelari/AELARI_V1.md",
  "The presets are White-Tower Formal, Artisan Practical, Arcane Institutional, Military Formal, Traveler, Rural/Provincial, Foreign/Urban and Ceremonial. They affect grooming, hair, markings, accessories and clothing, and never overwrite ancestry, skeleton, height, frame, muscle, fat, face, ears or natural pigmentation.",
  f"**Unified (T-3) {TAG}:** Aelari has one presentation-preset system, listed in the v1.4 presets section, §4 (Presentation presets), below. This earlier list is merged into it; presentation presets never alter biology."),
 ("aelari/AELARI_V1.md",
  "The presets are White-Tower Formal, Institutional Practical, Artisan, Military, Traveler, Provincial, Ceremonial and Foreign/Urban. They may change hair and grooming, markings, accessories, clothing and styling. They never overwrite ancestry, height, skeleton, frame, proportions, muscle, fat, face, ears or natural skin pigmentation.",
  "The single Aelari presentation-preset system (union of the v1.3 §24 and v1.4 lists, T-3, UCCA Phase 2) is: White-Tower Formal, Arcane Institutional, Institutional Practical, Artisan (Practical), Military (Formal), Traveler, Rural/Provincial, Foreign/Urban and Ceremonial. "
  "They may change hair and grooming, markings, accessories, clothing and styling. They never overwrite ancestry, height, skeleton, frame, proportions, muscle, fat, face, ears or natural skin pigmentation."),
 # T-4 Saurin tail muscularity
 ("saurin/SAURIN_V1.md", "- taper;\n- muscularity;\n- segment/curvature relationships;",
  "- taper;\n- muscularity (**superseded by §256.6, T-4, UCCA Phase 2:** tail muscularity follows Physical Composition; there is no independent tail-muscle slider);\n- segment/curvature relationships;"),
 # T-5 Halvren old height wording
 ("halvren/HALVREN_V1.md",
  "the provisional height range is **152–213 cm (5'0\"–7'0\")** with reference **about 178 cm (5'10\")**;",
  "the provisional height range is **152–213 cm (5'0\"–7'0\")** with reference **about 178 cm (5'10\")** (reconciled T-5, UCCA Phase 2: per §10–14 this is the **central population envelope**, not a hard bound; ancestry-dependent tails may fall outside it, with limits OPEN);"),
 ("halvren/HALVREN_V1.md",
  "| Height | Provisional 152–213 cm (5'0\"–7'0\"), reference about 178 cm (5'10\") |",
  "| Height | Central population envelope about 152–213 cm (5'0\"–7'0\"), reference about 178 cm (5'10\"); ancestry-dependent tails outside it, limits OPEN (§10–14; T-5, UCCA Phase 2) |"),
 # T-6 Durrim equal-height point
 ("durrim/DURRIM_V1.md",
  "A Durrim and a Marchfolk at about 150–152 cm, matched in age",
  "A Durrim and a Marchfolk at **152 cm** (the corrected comparison point, T-6, UCCA Phase 2; earlier \"about 150–152 cm\" is historical context only), matched in age"),
 ("durrim/DURRIM_V1.md",
  "about 150 cm Durrim against about 150 cm Marchfolk where ranges overlap",
  "152 cm Durrim against 152 cm Marchfolk (corrected from about 150 cm; T-6, UCCA Phase 2)"),
 # T-7 Grask tallest
 ("grask/GRASK_V1.md",
  "At a provisional maximum of about **239 cm**, Grask set the tallest approved playable stature among first-pass races at the time of writing (Gorrund, provisional maximum about 251 cm, now exceeds it), so world validation",
  "At a provisional maximum of about **239 cm**, Grask are a very tall playable population (Gorrund, provisional maximum about 251 cm, exceeds them; T-7, UCCA Phase 2), so world validation"),
 # T-10 Vael torso list
 ("vael/VAEL_V1.md",
  "Controls: torso length, ribcage length, width and depth, waist and lumbar length | All relationship-aware |",
  "Controls: torso length, ribcage length, width and depth, waist and lumbar length; shoulder and pelvic breadth are Skeletal Frame variables because frame changes them (below; T-10, UCCA Phase 2; no ranges added) | All relationship-aware |"),
]

PTR = ("**UCCA status (UCCA Phase 2, {d}):** the universal whole-character creator organization is canonical in `decisions/UCCA_V1.md` "
       "(15-slot navigation, control classes, Skeletal Frame and Physical Composition separation, presets, randomization, locks, saved appearance and validation). "
       "The {race} body-control organization in this spec stays as approved requirements routed to UCCA slots "
       "(`reviews/claude-ucca-11-phase1-architecture-audit.md` Appendix A); {race} anatomy, tendencies, bounds, validators, tests and OPEN items are unchanged. "
       "Natural subtle body asymmetry is available as ordinary individual variation (UCCA §16); body hair follows UCCA §13.")
EXTRA = {
 "Halvren": " Stature: 152–213 cm is the central envelope; ancestry-dependent tails are supported and never hard-clipped, and their limits stay OPEN (UCCA §22, RM-UB-05).",
 "Saurin": " Saurin canon governs wherever it is more specific (UCCA §23): mandatory tail (Slot 5), §256 coupling, §258 bounds, §263 E/B and anti-hourglass rules.",
 "Cogling": " Muscular Development Capacity is a Detailed control under §69 (UCCA §10).",
 "Vael": " Shoulder and pelvic breadth are bound through Skeletal Frame (T-10).",
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
    for f, anchor, para in INSERT:
        t = get(f); n = t.count(anchor); assert n == 1, (f, anchor[:60], n)
        i = t.index(anchor); j = t.find("\n", i); j = len(t) if j < 0 else j
        texts[f] = t[:j] + "\n\n" + para + t[j:]
    for f, old, new in REPL:
        t = get(f); n = t.count(old); assert n == 1, (f, old[:60], n)
        texts[f] = t.replace(old, new)
    for f, race in APPEND:
        t = get(f).rstrip("\n")
        texts[f] = t + "\n\n" + PTR.format(d=D, race=race) + EXTRA.get(race, "") + "\n"
    for f, t in texts.items():
        (S / f).write_text(t)
    print("edited", len(texts), "files")

if __name__ == "__main__":
    main()

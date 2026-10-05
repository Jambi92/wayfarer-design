"""Generate RAC W1 ARM Build Packets (one per purpose-built or rebuild candidate) from one table, so all packets share one format."""
import pathlib, re
OUT = pathlib.Path(__file__).resolve().parents[3] / "reviews" / "rac-w1-packets"
COMMON_STATE = """- **Reference state** (`decisions/REFERENCE_ANATOMY_V1.md` §3): central-tendency adult (R-1); central skeletal values, not "Balanced" as a default (R-3); reference composition: population-centre muscularity and fat amount, neutral distribution, no regional offsets (R-4); zero natural asymmetry, bilaterally mirrored (R-5); measurement stance R-6 (upright; head neutral; arms hanging with a small fixed abduction, palms toward the thighs; feet hip-width, parallel, full plantigrade; hips and knees extended; neutral adult spinal curvature); N3 (R-7); no scalp, facial or body hair over landmarks (R-8); one neutral matte material, no displacement that changes the silhouette (R-9); real-world units, stature to the vertex (R-13).
- **Builder-chosen values:** every numeric value not stated in canon is a **BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED** value and must be listed in the provenance record (R-14). It may shape the candidate; it can never become canon by measuring the candidate (§7 circularity rule).
- **Geometry/file form needed for measurement:** one triangle or quad mesh (OBJ, PLY, GLB, FBX or .blend) of the whole body in real-world units with a stated up axis; joint centres supplied as an armature or marker points (shoulder, elbow, wrist, hip, knee, ankle, plus spine and neck joints) built to anatomical joint centres; **separate eyeball meshes** (needed for orbit/eye-centre landmarks); head-region edge length about 0.3 cm or finer for craniofacial items; no hidden helper geometry; a SHA-256 or other immutable identifier recorded at hand-off.
- **Acceptance:** the candidate is inspected against R-1…R-14 and §6 by Claude (ARM acceptance record), then accepted or rejected by the author. Measurements stay DIAGNOSTIC."""
P = [
 # id, title, stature, config, canon constraints, tests, unlocks, notes
 ("MF-M-R", "Marchfolk configuration 1 (correction of the Iteration 3 candidate)", "173 cm", "Configuration 1, ordinary human sex-related anatomy",
  "Human Reference Population; recognizably human skeleton (MF L15); no race multipliers; Apparent Biological Age mid-adult (the Iteration 3 candidate uses MakeHuman's 'young' age macro).",
  "MF permanent height character at the reference (MF L249); N3 identity; acceptance §6.",
  "RM-UB-07 (central), MF sides of RM-LR-01/05/07 and RM-OT-01; RM-CF-02 central and RM-UF-01 only once eyeballs exist.",
  "**Correction, not a new design:** start from `RaceBodies/out/Marchfolk_Masc.blend` (sha256 d1dea7b6…). Required: (1) re-pose to R-6 by the rig (arms down from ~41° upper-arm abduction and ~47° elbow flexion; legs from ~7.6° thigh abduction to hip-width parallel) **with a check that no soft-tissue shape changes outside the joint regions**; (2) set the age macro to a mid-adult value (author to confirm the value; builder-chosen); (3) add eyeballs; (4) re-check stature after the stance change (the A-stance lowers it by about 0.6 cm). Inputs to list as builder-chosen: MakeHuman ethnic-mix weights (0.33 / 0.331 / 0.33), muscle 0.5, weight 0.5, proportions, height macro."),
 ("MF-F-R", "Marchfolk configuration 2 (rebuild)", "173 cm", "Configuration 2, ordinary human sex-related anatomy",
  "As MF-M-R. **R-2:** stature must be reached by proportion, never by uniform scaling: the Iteration 3 candidate is MPFB's 159.05 cm default female **uniformly scaled ×1.0877 to 173 cm**, which fails R-2.",
  "As MF-M-R; partner for PIP-BODY-29 / COG-BODY-14 like-for-like tests when those races have a matching configuration.",
  "RM-UB-07 (central, configuration 2).",
  "**Rebuild:** generate the female human at 173 cm through the height macro (not by scaling), same R-6 stance, mid-adult age, eyeballs. List builder-chosen inputs as for MF-M-R plus breast-size/firmness macros."),
 ("MF-FACE-PROJ-MAX", "Marchfolk most-projecting valid adult face (diagnostic head)", "head on MF-M-R (173 cm)", "As MF-M-R",
  "MARCHFOLK reference-anatomy note (AD-R40): the most-projecting valid adult human face, with no muzzle-like or non-human maxillary architecture. FAL per r3: subnasale–upper alveolar region, never pronasale.",
  "Reads as an ordinary adult human; not a muzzle; r3 FAL/Pr/Gn/N*/OC landmarks placeable.",
  "RM-CF-02 maximum-valid case (FPI, MPI, MdPI).",
  "The projection amount is necessarily **builder-chosen** (canon gives only the rule). The author accepts or rejects it as the Marchfolk maximum."),
 ("SK", "Skarn central ARM", "208 cm", "One configuration (ordinary human; second available later)",
  "Torso share slightly > MF; greater torso depth; broader clavicles; deeper ribcage; heavier joints; larger absolute hands/feet; more substantial neck base and pelvis; lower body carries the mass; never Gorrund (SK L22–26, L75–94, L300); no racial arm-span tendency.",
  "SK-01; SK-11 N3 identity; no Gorrund recreation.",
  "RM-LR-01/02 (ref)/05/07; RM-UB-01 (SK central).",
  "Iteration 3 Skarn S2 is **not** measurement truth (AD-R46); it may be visual reference only."),
 ("SG", "Sagekin central ARM", "178 cm", "One configuration (ordinary human)",
  "Slightly greater leg share, slightly shorter torso, reduced ribcage **depth**, slightly longer forearms, hands and fingers, slightly narrower hands; never elven (SG L89, L137–140, L147, L156).",
  "SG-01; SG-12/13 neutralization.", "RM-OT-01; RM-UB-01 (SG).", ""),
 ("FN", "Fenn central ARM", "181 cm", "One configuration (second deferred, AD-R21)",
  "Smaller torso share; shallower, moderately narrow ribcage; longer limbs, greater forearm and lower-leg share; longer palms and fingers; narrow wrists/ankles; joints smaller relative to limb length above hard minimums; distinct elven pelvis; elven ear family; orbit slightly larger **and** aperture slightly more open as separate quantities (FN L32–52, L110–124, L173).",
  "FN-01; hidden-ear body identity.", "RM-UB-01 (FN); RM-CF-08 (central).", ""),
 ("AE", "Aelari central ARM", "190 cm", "One configuration (second deferred)",
  "Whole-body vertical elongation incl. cranium, neck, torso; even upper-arm/forearm and thigh/lower-leg elongation; neck longer than FN and VA; relatively shallow ribcage, never implausibly shallow; gracile joints with hard minimums; distinct elven pelvis (AE L33–58, L123–155).",
  "AE-01; AE-39…44 neutralization.", "RM-UB-01 (AE); RM-CF-07 (AE central).", ""),
 ("VA", "Vael central ARM", "178 cm", "One configuration (second deferred)",
  "Greater torso share than FN; deeper ribcage than FN/AE (skeletal); strong torso-pelvis continuity, natural lumbar curve; balanced segments; broader palms and feet; more joint presence than FN/AE (VA L35–46, L114–141).",
  "VL-01; VL-16/17/18.", "RM-UB-01 (VA).",
  "The Vael Rodin source-master GLBs are relief reconstructions of 2D sheets and are **not** usable geometry."),
 ("HV", "Halvren central ARM (no-lineage general envelope)", "178 cm", "One configuration; follows sources",
  "General Halvren envelope (UFCA §11; race spec); mixed developmental structure, not a linear morph and not 50/50 (HV L105, L122, L361); joint bridging (HV L133); never a source body relabelled.",
  "HV core validation; source-passing against the W1 source ARMs at 178 cm where valid.", "RM-UB-01 (HV general envelope); baseline for RM-OT-03.", ""),
 ("DU", "Durrim central ARM", "137 cm", "One configuration; no authored shift",
  "Greater torso contribution and lower leg/limb contribution than equal-height MF; broad, deep thorax; substantial joints and long bones; hands large for stature; short neck with visible transition; head share somewhat > MF as allometry only; adult read (DU L11–40, L93–121).",
  "Durrim reference; composition neutralization (DU L73); adult read (DU L76).", "RM-SR-03 (DU); RM-SR-04 / RM-CF-10 (DU head share); RM-UB-01.", ""),
 ("GR", "Grask central ARM", "218 cm", "One configuration; no authored shift",
  "Lower torso share than MF and SK; greater leg share, upper arm, forearm and span; finger:palm > MF/SK; moderate breadth, meaningful thoracic depth; pelvis for long legs, never a scaled human pelvis; **central anterior projection ≈ Marchfolk; long midface is vertical, never prognathism** (GR L37–45, L198–235, Prognathism row); ears per GR-EAR family.",
  "GR-BODY-01; silhouette neutralization (GR L98).", "RM-LR-01/02 (ref)/05/07; RM-CF-10 (GR); central face for RM-CF-03/07.", ""),
 ("GO", "Gorrund central ARM", "229 cm", "One configuration; no authored shift",
  "Greater torso share than GR; less limb and span than GR; substantial thoracic depth relative to stature and breadth; ALPC (GO L711–723); load-bearing pelvis; strongest joint signal; **projection moderate relative to the Marchfolk adult range** (GORRUND projection note); two ear variables (projection from skull; outward extent).",
  "GOR-BODY-01; neutralized recognition (GO L691); ALPC at central breadth.", "RM-LR-01/02 (ref)/05/06 (ref)/07; RM-CF-06, -10 (GO); central face for RM-CF-04.", ""),
 ("PK", "Pipkin central ARM", "107 cm", "One configuration; no authored shift (PIP-BODY-29 waits)",
  "LSCTA: moderate thorax → compact lower trunk → mature, structurally broad pelvis → sustained limbs; trunk share modestly < MF, absorbed by limbs and pelvic vertical contribution, **not** head enlargement; legs never automatically above ordinary human proportions; hands moderate; adult read; never juvenile, never Durrim (PK L33–68, L133–178, L201–205).",
  "PIP-BODY-01; PIP-BODY-17; PIP-BODY-28 or -29 against the matching MF ARM.", "RM-SR-01, -03, -04 (central), RM-CF-10 (PK); RM-UB-06 (PK).", ""),
 ("CG", "Cogling central ARM", "91 cm", "One configuration; no authored shift (multi-configuration preset rule waits)",
  "Narrow stable central core; torso and total limb share ≈ MF; distal redistribution within limbs (upper arm ↓, forearm ↑, hand ↑, fingers ↑; femur ↓, lower leg ↑); fine shafts, small articulated joints, never fragile; adult read; **head height roughly 11–13 cm (menton–vertex, W1-A1)** without deliberate head enlargement (CG L100–145, L236, L280, L558–624, L755).",
  "COG-BODY-01; COG-BODY-07/08; COG-BODY-14/28 against the matching MF ARM.", "RM-SR-02 (central), -03, -04 (central), RM-CF-10 (CG).", ""),
]
for pid, title, st, cfg, canon, tests, unlocks, notes in P:
    canon = re.sub(r" \((?:[A-Z]{2} L[^)]*)\)", " (race spec; line citations to be confirmed by the builder)", canon)
    txt = f"""# ARM Build Packet — {pid}: {title}

**Order:** `reviews/chatgpt-reference-anatomy-wave1-execution-order.md` §4, §8
**Status:** BUILD REQUIRED. This packet is a specification, **not a mesh**. No measurement exists for this candidate.

| Field | Content |
|---|---|
| Population / candidate | {title} |
| Reference stature | {st} |
| Sex-related configuration | {cfg} |
| Frame / composition | Central skeletal values; reference composition (R-3, R-4) |
| Neutralization | N3 body; N-Head only for body tests that require it |
| Canon constraints the candidate must embody | {canon} |
| Comparison tests to pass | {tests} |
| Measurements it unlocks | {unlocks} |

{COMMON_STATE}
""" + (f"\n**Packet notes:** {notes}\n" if notes else "")
    (OUT / f"claude-rac-w1-packet-{pid}.md").write_text(txt)
print(len(P), "packets")

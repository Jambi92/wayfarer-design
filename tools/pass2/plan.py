# Conforming-edit plan generator. Every `cur` string is verified against the repo
# (exact occurrence count) and its line number / section heading is computed.
import re, sys
R = '/home/claude/wayfarer-design/'
S = {'MF':'specs/marchfolk/MARCHFOLK_V1.md','SK':'specs/skarn/SKARN_V1.md','SG':'specs/sagekin/SAGEKIN_V1.md',
     'FN':'specs/fenn/FENN_V1.md','AE':'specs/aelari/AELARI_V1.md','VA':'specs/vael/VAEL_V1.md',
     'HV':'specs/halvren/HALVREN_V1.md','DU':'specs/durrim/DURRIM_V1.md','GA':'specs/grask/GRASK_V1.md',
     'GO':'specs/gorrund/GORRUND_V1.md','PI':'specs/pipkin/PIPKIN_V1.md','CO':'specs/cogling/COGLING_V1.md',
     'SA':'specs/saurin/SAURIN_V1.md','ST':'specs/STATUS.md','PR':'decisions/PROJECT_RULES.md',
     'BR':'rules/character-creation-brief.md','ER':'reviews/elf-comparative-review.md'}
E = []
def e(i, f, cur, new, why, n=1):
    E.append(dict(id=i, f=S[f], cur=cur, new=new, why=why, n=n))

# ---------------- E1 Muscular Development Capacity ----------------
e('E1-01','SK','- greater skeletal robustness and more natural muscle volume',
  '- greater skeletal robustness and a higher Muscular Development Capacity (biological range; Current Muscularity stays free, §5)',
  'v1.0 §3 lists muscle volume inside Skeletal foundation; §5 says composition is independent. Capacity term removes the default-muscularity reading (Halvren CRes §1).')
e('E1-02','SK','- larger hands and feet\n- more natural muscle volume',
  '- larger hands and feet\n- a higher Muscular Development Capacity (not a default Current Muscularity)',
  'v1.1 §1 same ambiguity; R-SEX/PROJECT_RULES keep Current Muscularity independent.')
e('E1-03','SG','Their scholarly reputation never reduces muscle potential.',
  'Their scholarly reputation never reduces Muscular Development Capacity.',
  'Sagekin v1.0 §6: "muscle potential" = capacity; use adopted term.')
e('E1-04','HV','Aelari ancestry may raise proportional neck contribution and Skarn ancestry structural and muscular neck presence, which are different tendencies',
  'Aelari ancestry may raise proportional neck contribution and Skarn ancestry structural neck presence and neck Muscular Development Capacity (never current neck muscularity), which are different tendencies',
  'P2 §15–19 residual flagged by F-23; aligns with Halvren CRes §1 (capacity vs current composition).')
e('E1-05','GO','the already-approved greater natural muscle-volume potential,',
  'the already-approved higher Muscular Development Capacity (not a default Current Muscularity),',
  'P2 Skarn comparison row; same term mismatch with Skarn spec.')

# ---------------- E2 Comparator wording ----------------
HRP='the Marchfolk Human Reference Population'
e('E2-01','DU','a somewhat greater head-to-total-height contribution than taller humanoid populations,',
  'a somewhat greater head-to-total-height contribution than '+HRP+' and other taller populations,',
  'Proportional claim with unnamed comparator ("taller humanoid populations").')
e('E2-02','DU','the head may contribute somewhat more to stature than in taller humanoids,',
  'the head may contribute somewhat more to stature than in '+HRP+' and other taller populations,',
  'Same allometric claim, P3 §3–7.')
e('E2-03','PI','somewhat greater head contribution to standing height than taller humans as a natural consequence',
  'somewhat greater head contribution to standing height than '+HRP+' as a natural consequence',
  '"taller humans" conflicts with the matched-normalized-height default; name the population.')
e('E2-04','PI','Pipkin may trend toward somewhat greater head contribution to total stature than tall humanoids,',
  'Pipkin may trend toward somewhat greater head contribution to total stature than '+HRP+' and other taller populations,',
  'P3 §3 unnamed comparator.')
e('E2-05','CO','than a tall adult population simply because of allometric scaling',
  'than '+HRP+' or other taller populations simply because of allometric scaling',
  'P1 §18 unnamed comparator.')
e('E2-06','CO','the head\'s proportional contribution to total height relative to much taller adults.',
  'the head\'s proportional contribution to total height relative to '+HRP+' and other much taller populations.',
  'P2 §51 unnamed comparator.')
e('E2-07','CO','make the head a somewhat larger fraction of total height than in tall adults,',
  'make the head a somewhat larger fraction of total height than in '+HRP+' and other taller populations,',
  'P3 §77 unnamed comparator.')
e('E2-08','CO','Against ordinary human populations:',
  'Against human populations (the Marchfolk Human Reference Population and other human-family populations):',
  'P3 §90 "ordinary human populations" undefined.')
e('E2-09','GO','| Thoracic breadth | Trends high relative to relevant comparison populations,',
  '| Thoracic breadth | Trends high relative to '+HRP+' at matched normalized height (Skarn and Grask comparison pending the Large-Race Comparative Anatomy Review),',
  'P1 §11–25 "relevant comparison populations" undefined. AUTHOR CONFIRM: no Skarn/Grask magnitude is asserted.')
e('E2-10','GA','greater lower-limb contribution to standing height than equivalent-height human populations where comparison is possible,',
  'greater lower-limb contribution to standing height than human populations (Marchfolk Human Reference Population, Sagekin, Skarn) at matched normalized height,',
  'P1 §18–33: "equivalent-height" (absolute) vs matched normalized height; proportional claim needs the normalized method and named populations. AUTHOR CONFIRM Sagekin inclusion.')
e('E2-11','HV','more gracility than equivalent robust humans,',
  'more gracility than equivalent robust human populations such as Skarn (per consistency resolution §2–3),',
  'P1 §15–18 "robust humans" (inherited from Elf Review) — CRes §2–3 requires a named human population. Mirrors accepted Aelari wording "robust humans such as Skarn". AUTHOR CONFIRM referent.')
e('E2-12','HV','Elven ancestry may lower average apparent mandibular mass relative to robust humans,',
  'Elven ancestry may lower average apparent mandibular mass relative to robust human populations such as Skarn,',
  'P3 §15–20 same issue. AUTHOR CONFIRM referent.')

# ---------------- E3 baseline ----------------
e('E3-01','SK','Skarn hold their breath about 1.5× as long as the baseline.',
  'Skarn hold their breath about 1.5× as long as '+HRP+'.',
  'Comparator sense (undefined "the baseline"). Trait itself stays a legacy gameplay item (F-17, catalogued only).')
e('E3-02','SK','Relative to Marchfolk, the baseline trends toward:',
  'Relative to Marchfolk, the Skarn central tendency trends toward:', 'Population-centre sense → central tendency.')
e('E3-03','SK','The baseline is slightly more torso-dominant than Marchfolk,',
  'The Skarn central tendency is slightly more torso-dominant than Marchfolk,', 'Population-centre sense.')
e('E3-04','SK','The baseline tends toward:\n\n- a slightly larger, more robust skull',
  'The Skarn facial central tendency trends toward:\n\n- a slightly larger, more robust skull', 'v1.2 §1 population-centre sense.')
e('E3-05','MF','## 1–3. Core identity, baseline role and locked foundation',
  '## 1–3. Core identity, Human Reference Population role and locked foundation',
  'Consistency resolution Part 1 §6 states the v1.0 section now uses Human Reference Population; heading was missed.')
e('E3-06','MF','skin and hair biology and baseline locomotor anatomy,',
  'skin and hair biology and human locomotor anatomy,', 'Comparator/role sense; heading-level retirement per §6.')
e('E3-07','DU','Marchfolk within range keep baseline human proportions;',
  'Marchfolk within range keep Human Reference Population proportions;', 'Comparator sense.')
e('E3-08','DU','hold their breath longer than baseline humans"',
  'hold their breath longer than the Marchfolk Human Reference Population"',
  'Comparator sense inside a quoted legacy trait; AUTHOR may prefer to leave the quoted prototype text verbatim.')
e('E3-09','SG','never reproduces Fenn or Aelari baseline anatomy,',
  'never reproduces Fenn or Aelari central-tendency anatomy,', 'Population-centre sense.')
e('E3-10','SG','| Marchfolk | Broad baseline human variation |',
  '| Marchfolk | Human Reference Population; broad human variation |', 'Comparator-role sense.')
e('E3-11','SG','| Marchfolk | Deep baseline human customization |',
  '| Marchfolk | Human Reference Population; deep human customization |', 'Comparator-role sense.')
e('E3-12','AE','| Marchfolk | Baseline broad human customization |',
  '| Marchfolk | Human Reference Population; broad human customization |', 'Comparator-role sense.')
e('E3-13','SA','- Marchfolk — human baseline;','- Marchfolk — Human Reference Population;','§248 comparator sense.')
e('E3-14','CO','Five digits per hand are the first-pass humanoid baseline unless',
  'Five digits per hand are the first-pass humanoid default unless','Design-default sense.')
e('E3-15','CO','Cogling use the project baseline of **functional adult humanoid dentition,',
  'Cogling use the project first-pass default of **functional adult humanoid dentition,','Design-default sense.')
e('E3-16','PI','follows the existing functional adult humanoid baseline used elsewhere',
  'follows the existing functional adult humanoid first-pass default used elsewhere','Design-default sense.')
e('E3-17','GA','> **Grask possess a functional humanoid dentition as the first-pass baseline. Exact tooth morphology, dietary specialization and biological dietary range remain OPEN** (wording',
  '> **Grask possess a functional humanoid dentition as the first-pass default. Exact tooth morphology, dietary specialization and biological dietary range remain OPEN** (wording',
  'P3 §16–26 design-default sense.')
e('E3-18','GA','> **Grask possess a functional humanoid dentition as the first-pass baseline. Exact tooth morphology, dietary specialization and biological dietary range remain OPEN.**',
  '> **Grask possess a functional humanoid dentition as the first-pass default. Exact tooth morphology, dietary specialization and biological dietary range remain OPEN.**',
  'P3 clarification §21–22 duplicate.')
e('E3-19','GO','Dentition is **functional humanoid** as a baseline,',
  'Dentition is **functional humanoid** as the first-pass default,','P3 §22–39 design-default sense.')

# ---------------- E4 Basic ----------------
e('E4-01','MF','Basic and Advanced editing use the same character data,',
  'Quick and detailed body controls (both within Advanced Mode\'s Customize step) use the same character data,',
  'v1.1 §1 tier is NOT Simple Mode (Simple Mode = Race → Preset → Confirm, no sliders). AUTHOR CONFIRM tier placement.')
e('E4-02','MF','| Basic | Starting body frame, height,','| Quick controls | Starting body frame, height,','Same tier.')
e('E4-03','MF','| Advanced | All Basic controls, plus individual body regions,',
  '| Detailed controls | All quick controls, plus individual body regions,','Avoid "Advanced" as both mode and tier.')
e('E4-04','MF','| Basic | Accessible adjustments to the major features |',
  '| Quick controls | Accessible adjustments to the major features |','v1.2 §1 face tier, same reasoning.')
e('E4-05','MF','| Advanced | Detailed regional controls, anatomical proportions and optional asymmetry |',
  '| Detailed controls | Detailed regional controls, anatomical proportions and optional asymmetry |','Same.')
e('E4-06','MF','and Basic Mode conceptually supports both.',
  'and the quick body controls (v1.1 §1) conceptually support both.','"Basic Mode" here means the body tier, not a creator mode.')
e('E4-07','AE','save and load continuity, Basic and Advanced continuity,',
  'save and load continuity, Simple Mode and Advanced Mode continuity,','v1.5 §22 means creator modes (cf. Vael v1.5 "Simple and Advanced continuity").')
e('E4-08','DU','menu hierarchy, Basic or Advanced controls,','menu hierarchy, Simple Mode or Advanced Mode controls,','Mode sense.')
e('E4-09','DU','presets, Basic and Advanced editing,','presets, Simple Mode and Advanced Mode editing,','Mode sense.')

# ---------------- E5 Saurin ridge ----------------
e('E5-01','SA','- Creator variation (ridge prominence, transition strength,',
  '- Creator variation (structural-ridge prominence, transition strength,','§36a: structural ridges vary in strength only, never toggled.')
e('E5-02','SA','Expression ranges from subtle ridges and low hornlets through',
  'Expression ranges from subtle keratin ridges and low hornlets through','§100 keratin display.')
e('E5-03','SA','- nearly flat/minimal cranial ridges;','- nearly flat/minimal cranial keratin ridges;','§101 keratin display.')
e('E5-04','SA','Examples are low dorsal ridges, small keratinous scutes','Examples are low dorsal keratin ridges, small keratinous scutes',
  '§101a: distinguishes from §36a structural "low dorsal vertebral line".')
e('E5-05','SA','- horn/ridge surface morphology;','- horn/keratin-ridge surface morphology;','§102 display variation.')
e('E5-06','SA','- damaged low-profile ridges.','- damaged keratin ridges.','§113: keratin; "low-profile" is stale after §100 widened the display range.')
e('E5-07','SA','- ridge variation;\n- claw morphology.','- keratin-ridge variation;\n- claw morphology.','§119 surface randomization.')
e('E5-08','SA','chipped claws, damaged ridges, localized pigment change','chipped claws, damaged keratin ridges, localized pigment change','§122 Acquired layer.')
e('E5-09','SA','- claw/ridge wear;','- claw/keratin-ridge wear;','§129 aging.')
e('E5-10','SA','- ridge expression;\n- scale/pattern distribution;','- structural-ridge strength and keratin-display expression;\n- scale/pattern distribution;','§132 asymmetry: both may be asymmetric; name both.')
e('E5-11','SA','- damaged scales;\n- chipped claws;\n- damaged ridges;','- damaged scales;\n- chipped claws;\n- damaged keratin ridges;','§133 acquired.')
e('E5-12','SA','- ridge frequency;','- keratin-ridge frequency;','§134: structural ridges are present on every adult, so "frequency" can only mean keratin.')
e('E5-13','SA','biological eye traits, ridges and claw keratin are stored in **Biological Anatomy**.',
  'biological eye traits, keratin ridges and claw keratin are stored in **Biological Anatomy**.','§D Personal Presentation note.')
e('E5-14','SA','- include ridge-present and ridge-absent individuals;',
  '- include keratin-ridge-present and keratin-ridge-absent (naked display) individuals;','§140 adopted term.')
e('E5-15','SA','- eyes;\n- ridges;\n- claws;\n- adult age biology.','- eyes;\n- keratin ridges / cranial display;\n- claws;\n- adult age biology.',
  '§141: structural ridges are sampled with craniofacial anatomy, never as a presence toggle.')
e('E5-16','SA','- damaged low-profile ridges;','- damaged keratin ridges;','§142A acquired-history.')
e('E5-17','SA','- pattern;\n- ridges;\n- age biology;','- pattern;\n- keratin ridges / cranial display;\n- age biology;','§144 lock group (structural ridges lock with "head").')
e('E5-18','SA','- sex selection cannot silently force frame, muscularity, rostrum, ridge, pigmentation or personality;',
  '- sex selection cannot silently force frame, muscularity, rostrum, structural-ridge strength, cranial keratin display, pigmentation or personality;','§154; consistent with §263 (no sex shift for skull or display).')
e('E5-19','SA','- ridge controls remain Natural/FD-SURF rather than being mislabeled genetically as hair.',
  '- keratin-ridge and other cranial-display controls remain Natural/FD-SURF rather than being mislabeled genetically as hair (structural ridges stay skull anatomy, §36a).','§155 named in brief.')
e('E5-20','SA','pattern, scale morphology, eye biology, ridges and claw keratin;','pattern, scale morphology, eye biology, keratin ridges and claw keratin;','§156 saved appearances.')
e('E5-21','SA','- ridge size × cranial surface support.','- keratin-ridge/display size × cranial surface support.','§158 coupling.')
e('E5-22','SA','scale morphology, eye biology, ridges, claw keratin and other inherited phenotype','scale morphology, eye biology, keratin ridges, claw keratin and other inherited phenotype','§161.')
e('E5-23','SA','- scales;\n- ridges;\n- eyes;\n- age','- scales;\n- structural ridges or keratin display;\n- eyes;\n- age','§161A gameplay firewall applies to both.')
e('E5-24','SA','| SAU-CC-12 | Ridge absent/present extremes both remain valid Saurin |',
  '| SAU-CC-12 | Keratin-ridge-absent (naked display) / keratin-ridge-present extremes both remain valid Saurin |','Named in T-5.')
e('E5-25','SA','pigmentation, pattern, eyes, ridges, claws, age and asymmetry,','pigmentation, pattern, eyes, keratin ridges, claws, age and asymmetry,','§167 identity statement.')
e('E5-26','SA','| SAU-EQP-01 | Helmet fit across rostrum/ridge extremes |','| SAU-EQP-01 | Helmet fit across rostrum, structural-ridge and cranial-display extremes |','Helmets must fit both.')
e('E5-27','SA','- no true horns;\n- optional low-profile integumentary keratinous ridges/scale crests.',
  '- no mandatory or default horns;\n- optional Cranial Keratin Display expression (§100–102, §260), from keratin-ridge-absent/naked display through keratin ridges, scale crests, hornlets and restrained crests.',
  '§230 contradicts §100 ("true horns" rule superseded) and §260 (family range). Item named in brief.')
e('E5-28','SA','- ridge-absent or ridge-present where valid.','- keratin-ridge-absent (naked display) or keratin-ridge-present where valid.','§234.')
e('E5-29','SA','- adiposity;\n- rostrum;\n- ridges;','- adiposity;\n- rostrum;\n- structural ridges or keratin display;','§235; consistent with §263.')
e('E5-30','SA','- ridge expression.\n\nExplicitly unapproved','- structural-ridge or keratin-display expression.\n\nExplicitly unapproved','§237 gameplay firewall.')
e('E5-31','SA','- recessed auricular openings;\n- optional ridges;',
  '- recessed auricular openings;\n- structural cranial ridges and optional Cranial Keratin Display structures (§100–102, §260);',
  '§239: equipment must fit mandatory structural ridges AND the full display family, not only "optional ridges".')
e('E5-32','SA','pattern, eyes, ridges, claws and skin layers;','pattern, eyes, keratin ridges, claws and skin layers;','§246 SAU-SURF scope.')
e('E5-33','SA','- ridge absent/present;','- keratin ridge absent (naked display)/present;','§247.')
e('E5-34','SA','- exact ridge frequency/distribution;','- exact keratin-ridge frequency/distribution;','§249.')
e('E5-35','SA','neutral/naked; minimal ridges (near-naked end);','neutral/naked; minimal keratin ridges (near-naked end);','§260 display family.')
e('E5-36','SA','- cobra hoods;\n- dinosaur crests;\n- dragon fins;\n- cheek spikes;\n- eyebrow horns.',
  '- cobra hoods;\n- dinosaur crests;\n- dragon fins;\n- cheek spikes;\n- eyebrow horns (mammal-style brow horns; brow-region keratin hornlets of the §100–102 family are valid per the reconciliation note above).',
  '§59 list still reads as excluding brow-region hornlets that the §59 reconciliation note and §101 approve.')

# ---------------- E6 Skin Appearance Layers ----------------
e('E6-01','MF','The three layers stay independently editable.','The four layers stay independently editable.','v1.3 §1.')
e('E6-02','MF','| Applied or acquired | Scars, tattoos, makeup, dirt, paint, decorative markings |',
  '| Applied | Tattoos, makeup, dirt, paint, decorative markings |\n| Acquired | Scars |',
  'v1.3 §1. "dirt" kept in Applied to avoid reclassification; NOTE Saurin §122 puts dirt in Environmental — AUTHOR DECIDE.')
e('E6-03','MF','keeping the Natural, Environmental and Applied or Acquired layers separate.','keeping the Natural, Environmental, Applied and Acquired layers separate.','v1.5 §7–8.')
e('E6-04','MF','**Skin Appearance Layers** are 1, Natural; 2, Environmental; and 3, Applied or Acquired.',
  '**Skin Appearance Layers** are 1, Natural; 2, Environmental; 3, Applied; and 4, Acquired.','Consistency resolution Part 1 §7 — the definitional source.')
e('E6-05','SK','The three layers stay, as in Marchfolk v1.3.','The four layers stay, as in Marchfolk v1.3 (as conformed).','v1.3 §2.')
e('E6-06','SK','| Applied or acquired | Scars, tattoos, paint, makeup, dirt, decorative markings |',
  '| Applied | Tattoos, paint, makeup, dirt, decorative markings |\n| Acquired | Scars |','v1.3 §2 (dirt note as E6-02).')
e('E6-07','SG','The universal three layers stay: natural, environmental and applied or acquired.',
  'The universal four layers stay: natural, environmental, applied and acquired.','v1.3 §2.')
e('E6-08','FN','The universal three layers stay: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (sun and tanning, weathering, roughness, dryness, calluses, localized wear), and applied or acquired (scars, tattoos, body paint, dirt, makeup, ceremonial markings).',
  'The universal four layers stay: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (sun and tanning, weathering, roughness, dryness, calluses, localized wear), applied (tattoos, body paint, dirt, makeup, ceremonial markings) and acquired (scars).','v1.3 §5.')
e('E6-09','AE','The universal three layers stay: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (tanning, sun, weathering, dryness, roughness, calluses) and applied or acquired (scars, tattoos, makeup, paint, dirt, markings).',
  'The universal four layers stay: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (tanning, sun, weathering, dryness, roughness, calluses), applied (tattoos, makeup, paint, dirt, markings) and acquired (scars).','v1.3 §4–5.')
e('E6-10','VA','The universal natural, environmental and applied layers stay.','The universal Natural, Environmental, Applied and Acquired layers stay.','v1.3 §4–5 omitted Acquired entirely.')
e('E6-11','HV','The three Skin Appearance Layers stay separate: **Natural** (inherited and developmental), **Environmental** (tanning, weathering, exposure) and **Applied or Acquired** (tattoos, cosmetics, scars, acquired markings).',
  'The four Skin Appearance Layers stay separate: **Natural** (inherited and developmental), **Environmental** (tanning, weathering, exposure), **Applied** (tattoos, cosmetics) and **Acquired** (scars, acquired markings).','P4 §1–3.')
e('E6-12','HV','Tattoos and cosmetics are Applied or Acquired and may communicate','Tattoos and cosmetics are Applied and may communicate','P4 §32–36.')
e('E6-13','HV','Natural, Environmental and Applied-Acquired layers stay separate','Natural, Environmental, Applied and Acquired layers stay separate','P4 §56–57.')
e('E6-14','PI','- **Layer 3 — Applied or Acquired:** scars, tattoos, cosmetics, paint and comparable history/presentation marks.',
  '- **Layer 3 — Applied:** tattoos, cosmetics, paint and comparable presentation marks.\n- **Layer 4 — Acquired:** scars and comparable history marks.','P4 §16.')
e('E6-15','CO','3. **Applied or Acquired** — scars, burns, tattoos, cosmetics, paint and comparable acquired/applied surface changes.',
  '3. **Applied** — tattoos, cosmetics, paint and comparable applied surface changes.\n4. **Acquired** — scars, burns and comparable acquired surface changes.','§132.')
e('E6-16','SA','The three Skin Appearance Layers remain:\n- **Natural**;\n- **Environmental**;\n- **Applied or Acquired**, whose two halves distinguish deliberately applied presentation from acquired history/injury/wear.',
  'The four Skin Appearance Layers (§122) remain:\n- **Natural**;\n- **Environmental**;\n- **Applied** — deliberately applied presentation;\n- **Acquired** — acquired history/injury/wear.','§231 contradicts §122 (F-13).')

# ---------------- E7 stale status/process ----------------
e('E7-01','PI','# Pipkin Character Design v1.0 (in progress)','# Pipkin Character Design v1.0 (first pass complete)','Header contradicts P6 §38 FIRST-PASS COMPLETE.')
e('E7-02','PI','v1.0 arrives in parts: Part 1 (biological foundation, stature and core skeletal architecture) and Part 2 (detailed body proportions, human differentiation, hands, feet and composition architecture) are complete, Part 3 (craniofacial anatomy, ears, hair and facial-hair biology) is now authored for audit. Pipkin v1.0 as a whole isn\'t complete.',
  'v1.0 arrived in six parts, all complete: Part 1 (biological foundation, stature and core skeletal architecture), Part 2 (detailed body proportions, human differentiation, hands, feet and composition architecture), Part 3 (craniofacial anatomy, ears, hair and facial-hair biology), Part 4 (surface phenotype and visible biological traits), Part 5 (movement, posture, locomotion and whole-character physical expression) and Part 6 (equipment, world compatibility, character-creation integration and final first-pass review). **Pipkin Character Design v1.0 is FIRST-PASS COMPLETE** (Part 6 §38).','Header preamble stale.')
e('E7-03','PI','This remains a provisional roster envelope because **Saurin is still undesigned**.',
  'This remains a provisional roster envelope pending world validation (Saurin, now FIRST-PASS COMPLETE at 168–208 cm, falls inside it).','P1 §95–115 stale reason.')
e('E7-04','PI','| Short-Race Comparative Anatomy Review | After Cogling\'s first pass: Durrim, Pipkin and Cogling, not finalized now |',
  '| Short-Race Comparative Anatomy Review | Durrim, Pipkin and Cogling — ACCEPTED / COMPLETE (`reviews/short-race-comparative-anatomy-v1.md`; `specs/STATUS.md`) |','P1 §82–94.')
e('E7-05','PI','- Short-Race Comparative Anatomy Review after Cogling.','- Short-Race Comparative Anatomy Review (ACCEPTED / COMPLETE; `specs/STATUS.md`).','P6 §36.')
e('E7-06','PI','6. Short-Race Comparative Anatomy Review remains queued for after Cogling rather than being falsely treated as completed.',
  '6. Short-Race Comparative Anatomy Review remains queued for after Cogling rather than being falsely treated as completed. *(Since satisfied: the review is ACCEPTED / COMPLETE — `specs/STATUS.md`.)*','P6 §38 criterion: keep as historical, annotate.')
e('E7-07','PI','The Short-Race Comparative Anatomy Review remains queued until Cogling is designed.',
  'The Short-Race Comparative Anatomy Review was then queued until Cogling was designed; it is now ACCEPTED / COMPLETE (`specs/STATUS.md`).','P6 §38 status line.')
e('E7-08','PR','- Short-Race Comparative Anatomy Review after Durrim, Pipkin, and Cogling.',
  '- ~~Short-Race Comparative Anatomy Review after Durrim, Pipkin, and Cogling.~~ ACCEPTED / COMPLETE (`specs/STATUS.md`).','F-11; STATUS records acceptance.')
e('E7-09','ST','**PASS 1 COMPLETE — all 13 playable races are FIRST-PASS COMPLETE.** Next phase: Pass 2 roster-wide comparative and system review. Do not begin UE5 implementation.',
  '**PASS 1 COMPLETE — all 13 playable races are FIRST-PASS COMPLETE.** Pass 2 roster-wide comparative and system review delivered (`reviews/claude-pass2-01`…`06`); current work follows `reviews/chatgpt-pass2-resolution-sequence-order.md` (Large-Race Comparative Anatomy Review → common craniofacial comparison framework → conforming cleanup → UFCA). Do not begin UE5 implementation.','"Current next action" stale.')
e('E7-10','SK','The next race is Sagekin, and scholarly culture must never','The next race was Sagekin, whose scholarly culture must never','Header roster pointer (tense only; design rule kept).')
e('E7-11','SG','This is the working concept for Sagekin before their customization spec begins.',
  'This document opens with the working concept written before the Sagekin customization spec began.','Header stale.')
e('E7-12','SG','The next race is Fenn, and Sagekin stay fully human,','The next race was Fenn; Sagekin stay fully human,','Header roster pointer.')
e('E7-13','FN','The next race is Aelari (High Elf), who must never simply be taller Fenn.','The next race was Aelari (High Elf), who must never simply be taller Fenn.','Header roster pointer.')
e('E7-14','AE','The next race is Vael (Dark Elf), who must never be dark-skinned Aelari or subterranean Fenn, and the Elf Comparative Review follows Vael v1.5.',
  'The next race was Vael (Dark Elf), who must never be dark-skinned Aelari or subterranean Fenn, and the Elf Comparative Review followed Vael v1.5 (`reviews/elf-comparative-review.md`).','Header.')
e('E7-15','VA','Next is the Elf Comparative Review v1.0.','The Elf Comparative Review v1.0 followed (`reviews/elf-comparative-review.md`).','Header.')
e('E7-16','VA','The Elf Comparative Review v1.0 comes next, sorting features','The Elf Comparative Review v1.0 came next (`reviews/elf-comparative-review.md`), sorting features','v1.5 completion status line.')
e('E7-17','VA','Durrim aren\'t designed yet, so flexibility stays |','Durrim weren\'t designed when this was written, so flexibility stayed; Durrim v1.0 is now FIRST-PASS COMPLETE and the comparison uses it |','v1.1 §25–27 boundary row asserts a now-false state.')
e('E7-18','HV','A consistency review against the source specs follows Part 5, and v1.1 isn\'t begun.',
  'The consistency review against the source specs and its resolution patch follow Part 5, and v1.1 isn\'t begun.','Header (F-11 "Halvren preamble stale").')
e('E7-19','HV','The next step is Halvren Character Design v1.1 (detailed body proportions and mixed-ancestry morphology).',
  'The next step was then Halvren Character Design v1.1 (detailed body proportions and mixed-ancestry morphology); current sequencing is in `specs/STATUS.md`.','CRes §17–18 status line.')
e('E7-20','MF','The next step waits for Halvren Character Design v1.0 (mixed-ancestry biological foundation).',
  'The next step then waited for Halvren Character Design v1.0 (mixed-ancestry biological foundation), since completed.','Part 2 §16–17 status line.')
e('E7-21','GA','Grask currently set the tallest approved playable stature among completed or active first-pass races,',
  'Grask set the tallest approved playable stature among first-pass races at the time of writing (Gorrund, provisional maximum about 251 cm, now exceeds it),','P1C §19–21 stale "currently tallest".')
e('E7-22','GA','Grask currently set the tallest approved playable anatomy at about **239 cm (7\'10")**, not a permanent project maximum.',
  'Grask\'s provisional maximum is about **239 cm (7\'10")**; Gorrund (about 251 cm) now sets the tallest approved playable anatomy.','P5 §51–60 stale.')
e('E7-23','GA','| Future Large-Race Comparative Anatomy Review | Once Gorrund is designed, compare',
  '| Future Large-Race Comparative Anatomy Review | (Gorrund is now designed; review ordered — PROJECT_RULES, `reviews/chatgpt-pass2-resolution-sequence-order.md` §5.) Once Gorrund is designed, compare','P1 §60–70 pointer.')
e('E7-24','GA','Gorrund isn\'t started automatically, and no UE5 change is authorized.','Gorrund wasn\'t started automatically (it is now FIRST-PASS COMPLETE), and no UE5 change is authorized.','P5 §106–107 status line.')
e('E7-25','GA','Gorrund isn\'t started, and no UE5 change is authorized.','Gorrund wasn\'t started by this patch (it is now FIRST-PASS COMPLETE), and no UE5 change is authorized.','Final housekeeping status line.')
e('E7-26','GO','The recommended next race is **Pipkin — Halfling**, not started.','The recommended next race was **Pipkin — Halfling** (since FIRST-PASS COMPLETE).','FC §21–25 status line.')
e('E7-27','DU','The next race isn\'t started independently.','The next race wasn\'t started independently (current roster status: `specs/STATUS.md`).','P5 §86–88 status line.')
e('E7-28','DU','The next first-pass race in roster order is **Grask — Troll**, not started by this patch.',
  'The next first-pass race in roster order was **Grask — Troll**, not started by this patch (since FIRST-PASS COMPLETE).','Housekeeping status line.')
e('E7-29','DU','and Pipkin and Cogling aren\'t defined yet |','and Pipkin and Cogling weren\'t defined yet (now FIRST-PASS COMPLETE; see `reviews/short-race-comparative-anatomy-v1.md`) |','P5 §65–73 row asserts a now-false state.')
e('E7-30','CO','- the Short-Race Comparative Anatomy Review;\n- the Universal Facial',
  '- the Short-Race Comparative Anatomy Review (ACCEPTED / COMPLETE; `specs/STATUS.md`);\n- the Universal Facial','§207B dependency now closed.')

# ---------------- E8 brief ----------------
e('E8-01','BR','# Character Creation & Race Design\n',
  '# Character Creation & Race Design\n\n> **SUPERSEDED — HISTORICAL BRIEF (September 30, 2026).** This is Tyler\'s original direction and is retained for history only. It does not govern anatomy, terminology, creator modes, layers, height/mass values or gameplay. Authority order (`reviews/chatgpt-pass2-resolution-sequence-order.md` §2): approved race specifications (`specs/<race>/<RACE>_V1.md`) → `decisions/PROJECT_RULES.md` → accepted cross-race reviews / explicit author resolutions → `register/decision-register.md`. Where this brief conflicts with any of them (including its three-layer model, "baseline" wording, height/mass multipliers and race descriptors), the approved source governs.\n',
  'F-10: stale brief not marked superseded.')

# ---------------- E9 Saurin process tokens ----------------
e('E9-01','SA','Female reference package: A-structure + E coelomic body wall + B subtle ventral fullness. Paired breasts (Pass-2 comparison D) were **rejected**.',
  'Female reference package: sex-shifted lower axial trunk length and skeletal pelvic band (A), coelomic body-wall fullness (E) and subtle ventral fullness (B), as tabulated below. Paired breasts were evaluated diagnostically and **rejected**.','"A-structure" and "comparison D" are undefined review tokens; A is defined here by its two table rows. Letters E/B stay (defined in the table).')
e('E9-02','SA','C-level ventral fullness (up to 3.0 cm) is valid individual variation',
  'Higher ventral fullness (B up to its 3.0 cm ceiling) is valid individual variation','"C-level" is a Pass-2 diagnostic token.')
e('E9-03','SA','tail RSI 1.01–1.02;','tail root-sufficiency index (§256.1) 1.01–1.02;','"RSI" abbreviation undefined in §256.')
e('E9-04','SA','tail length → base → RSI / taper / A50 coupling (§256),',
  'tail length → base → root-sufficiency index / abrupt-taper guard / mid-tail area ratio coupling (§256.1–3),','"A50" = mid-tail area ratio (§256.3); "RSI" undefined.')
e('E9-05','SA','Unchanged by sex: Gate 6 skull, rostrum,','Unchanged by sex: the accepted naked skull (§259), rostrum,','"Gate 6 skull" review token.')
e('E9-06','SA','tail root; Gate 7 scale-field topology;','tail root; Regional Scale Architecture field topology (§80–85);','"Gate 7" review token.')

# ---------------- E10 stale OPEN items ----------------
e('E10-01','SA','## 115. Garment visibility decision remains OPEN\n',
  '## 115. Garment visibility decision remains OPEN\n\n> **Resolved by §195 and §225:** armor, clothing and accessories may partially cover, drape over or sheath the tail, provided it remains a persistent anatomical and silhouette feature. The list below is historical; exact tail-equipment construction remains OPEN (§251).\n',
  'F-13: decided in Part 5/6, still headed OPEN.')
e('E10-02','SA','- garment/armor coverage of tail;','- garment/armor coverage of tail (permission resolved §195/§225; construction OPEN §251);','§124.')
e('E10-03','SA','- tail equipment coverage;\n- exact helmet','- tail equipment construction and coverage extent (permission to cover resolved §195/§225);\n- exact helmet','§251.')
e('E10-04','SA','**Carried OPEN questions:** whether garments may partially cover the tail;',
  '**Carried OPEN questions:** whether garments may partially cover the tail (since resolved, §195/§225);','Part 1 status (historical annotate).')
e('E10-05','SA','**Status: PROVISIONAL, pending Tyler/ChatGPT acceptance of the Targeted Sculpt 6 diagnostics.** Strength values, exact ridge placement and transition sharpness remain open until that review.',
  '**Status: ACCEPTED** — the TS6/TS6.1 head was accepted and cranial identity is closed in §259 (originally PROVISIONAL pending acceptance of the Targeted Sculpt 6 diagnostics). Numeric structural-ridge strength, exact placement and transition sharpness remain OPEN beyond the §259 constraints.',
  '§36a stale PROVISIONAL. AUTHOR CONFIRM wording of acceptance (TS6.1 acceptance is recorded in reviews, not in §36a).')
e('E10-06','SA','**Orbital size ≠ visible eye opening ≠ eyeball size.**\n\nThese remain separate anatomical controls.',
  '**Orbital size ≠ visible eye opening ≠ eyeball size.**\n\nThese remain separate anatomical quantities.\n\n> **Reconciled by §259:** the orbit-size control scales orbit, lids, aperture and eyeball together, and the eyeball never scales independently of its orbit; visible-opening variation (§149) operates within that coupling.',
  '§44 vs §259 (F-13). AUTHOR CONFIRM.')
e('E10-07','SA','Saurin nasal openings are positioned on the anterior-to-dorsal rostral region rather than using a projecting human external nose.',
  'Saurin nasal openings are positioned on the anterior-to-dorsal rostral region rather than using a projecting human external nose. *(Refined by §36a: the anterior rostrum ends in a terminal plane bearing laterally placed nostrils.)*','§52 vs §36a.')
e('E10-08','SA','Head length/H (0.170) and tail length (64.7 % H) unchanged;','Head length/H (0.170) and tail length (frozen reference, §256) unchanged;','64.7 % (§263) vs 64.6 % (§256); remove the conflicting figure rather than pick one.')
e('E10-09','SA','The **capacity** for these structures is racial biology.',
  '> **Creator scope (§260, §265):** the validated first-pass display families are those listed in §260; prominent horns, spikes and plates beyond them, and crests above ~2.5 cm, remain OPEN for creator validation (§265).\n\nThe **capacity** for these structures is racial biology.','§100 lists prominent forms that §265 keeps OPEN (F-13).')
e('E10-10','CO','- final locomotion speeds;\n- acceleration/turning;','- exact center-of-mass values (§150);\n- final locomotion speeds;\n- acceleration/turning;','§207 omits §150 (F-22).')
e('E10-11','CO','- networking;\n- schema/version migration;','- networking;\n- exact attribute-lock UI behavior (§196);\n- schema/version migration;','§207 omits §196 (F-22).')
e('E10-12','CO','## 35. Part 1 status and OPEN items\n',
  '## 35. Part 1 status and OPEN items\n\n> *Historical Part 1 list. Items later defined at first-pass level in Parts 2–6 (e.g. craniofacial anatomy, ears, surface phenotype, movement) are governed by the consolidated OPEN list in §207.*\n','Stale OPEN list (05 §9).')
e('E10-13','CO','## 72. Part 2 OPEN items\n',
  '## 72. Part 2 OPEN items\n\n> *Historical Part 2 list; the consolidated OPEN list in §207 governs.*\n','Stale OPEN list (05 §9).')
e('E10-14','PI','OPEN (non-exhaustive): final height range; head-to-body ratio;',
  'OPEN (non-exhaustive; historical Part 1 list — Part 6 §32 governs): final height range; head-to-body ratio;','P1 §116–118 lists face, ears, pigmentation, movement etc. later designed.')
e('E10-15','ER','These stay open and are never silently resolved during implementation: exact shared pelvic morphology,',
  'These stay open and are never silently resolved during implementation: Fenn low-light vision relative to the Marchfolk Human Reference Population (Fenn v1.3 §9); exact shared pelvic morphology,','F-20: Fenn low-light dropped from the elf review final register (reviews file, authority level 3). AUTHOR CONFIRM.')
e('E10-16','DU','pending the universal system (OPEN).','pending the universal system (OPEN; universal rule now adopted as R-SEX, `reviews/chatgpt-pass2-resolution-sequence-order.md` §4 — Durrim magnitudes stay OPEN).','P1 §37–39 dependency now partly closed.')

# ---------------- E11 IDs and citations ----------------
e('E11-01','GO','GRR-','GOR-','Single Gorrund prefix (GOR- already used by EAR/FACE/SKIN/MOVE/INT/EQUIP; avoids GRR-/GR- (Grask) collision). Global replace, 30 occurrences on 25 lines (GRR-BODY-01…18, GRR-STRESS-01). Reviews/audits citing GRR- stay historical.', n=30)
e('E11-02','GA','§70 no longer asserts anything about the prototype\'s stealth values.',
  'Part 5 §61–72 no longer asserts anything about the prototype\'s stealth values.','Grask restarts § per Part; "§70" exists in P1 (§60–70), P4 (§69–81) and P5 (§61–72). Stealth text is in P5 §61–72. AUTHOR CONFIRM.')
e('E11-03','GA','No contradiction blocks completion (see Notes),','No contradiction blocks completion (see `audits/09-grask.audit.md`),','No Notes section exists (F-12). Alternative: delete the parenthetical.')
e('E11-04','DU','No unresolved contradiction needs immediate correction (see Notes),','No unresolved contradiction needs immediate correction (see `audits/08-durrim.audit.md`),','Same (F-12).')
e('E11-05','GO','was audited against the full list in §136.','was audited in full (the final-audit checklist is not reproduced in this spec; see `audits/10-gorrund.audit.md`).','§136 is this section; no list exists (F-12).')
e('E11-06','GO','(Added to the §134 identity statement.)','(Supplements the Part 5 §128–135 identity statement; read the two together.)',
  'Never applied to L689 (F-12). Alternative: append the sentence to the §128–135 blockquote.')
e('E11-07','HV','stay as prototype, as recorded under the Part 1 notes.','stay as prototype (no Part 1 notes section is retained; Part 5 §52–58 and §59–63 govern gameplay and prototype authority).','F-12 dangling reference.')
e('E11-08','DU','Part 5\'s header instruction now reads','Part 5\'s header instruction (not retained in this consolidated spec) was corrected to read','Dangling reference (F-12).')

# ---------------- E12 sex-related terminology ----------------
e('E12-01','AE','No mandatory hip width by race or anatomy configuration |','No mandatory hip width by race or sex-related anatomy |','v1.1 §2–5 (retired term).')
e('E12-02','AE','Frame stays separate from muscle, fat, anatomy configuration, height and presentation.','Frame stays separate from muscle, fat, sex-related anatomy, height and presentation.','v1.1 §7.')
e('E12-03','VA','(ancestry, body configuration, composition, face,','(ancestry, skeleton and body, composition, face,',
  'v1.5 §24–26: parallel Aelari §20–21 list reads "skeleton and body" — here "body configuration" is NOT the sex-related category (correcting T-8). Retire the ambiguous term anyway.')
e('E12-04','MF','from the selected anatomy or starting frame:','from the selected sex-related anatomy or starting frame:','v1.0 §4–5: "selected anatomy" means the sex-related selection; optional clarity edit.')

# ---------------- E13 frame vs composition ----------------
e('E13-01','FN','Very lean, average, Broad, highly muscular, high-body-fat and elder Fenn are all explicitly allowed.',
  'Very lean, average, Broad-framed, highly muscular, high-body-fat and elder Fenn are all explicitly allowed.','v1.0 §8: Broad is a Skeletal Frame term.')
e('E13-02','AE','Explicitly supported: Narrow and lean, Narrow and muscular, Balanced, Broad, Broad and highly muscular, high body fat, and elder composition.',
  'Explicitly supported frame × composition combinations: Narrow and lean, Narrow and muscular, Balanced, Broad, Broad and highly muscular, high body fat, and elder composition (Narrow/Balanced/Broad are Skeletal Frame presets).','v1.0 §12.')
e('E13-03','VA','Narrow and lean, Narrow and muscular, Balanced, Broad, Broad and highly muscular, high body fat, and elder composition.',
  'Narrow and lean, Narrow and muscular, Balanced, Broad, Broad and highly muscular, high body fat, and elder composition (Narrow/Balanced/Broad are Skeletal Frame presets combined with composition).','v1.0 §13.')
e('E13-04','GA','a relatively lean structural silhouette,','a skeletal silhouette with moderate structural size relative to stature (a skeletal, not composition, tendency; §6–7),',
  'P1 §1–2 identity statement uses composition word "lean"; §6–7 defines the intended skeletal meaning. Positive anatomy unchanged. AUTHOR CONFIRM.')

# ---------------- verify + render ----------------
bad = 0
cache = {}
def text(f):
    if f not in cache: cache[f] = open(R+f).read()
    return cache[f]
def locate(f, cur):
    t = text(f); i = t.find(cur); line = t.count('\n', 0, i) + 1
    h1 = h2 = ''
    for k, l in enumerate(t.split('\n')[:line], 1):
        if l.startswith('# '): h1 = l[2:].strip(); h2 = ''
        elif l.startswith('##'): h2 = l.lstrip('#').strip()
    return line, (h1[:45] + (' > ' + h2[:55] if h2 else ''))
rows = []
for x in E:
    c = text(x['f']).count(x['cur'])
    if c != x['n']:
        print('COUNT MISMATCH', x['id'], x['f'], c, 'expected', x['n'], repr(x['cur'][:80])); bad += 1; continue
    ln, sec = locate(x['f'], x['cur'])
    rows.append((x, ln, sec))
print('entries', len(E), 'ok', len(rows), 'bad', bad)
import json
json.dump([dict(id=x['id'], f=x['f'], line=ln, sec=sec, cur=x['cur'], new=x['new'], why=x['why'], n=x['n']) for x, ln, sec in rows],
          open('/home/claude/wayfarer-design/tools/pass2/conforming_rows.json', 'w'), ensure_ascii=False, indent=1)

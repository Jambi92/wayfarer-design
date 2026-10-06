# RAC W1e — Canonicalization record (pelvic / girdle / ALPC architecture)

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1d-author-decisions-continuation-order.md` §2, §3, §9 item 1
**Sources of wording:** `claude-rac-w1d-pelvic-morphology-packet.md`, `claude-rac-w1d-large-race-girdle-alpc-packet.md`

Only author-accepted relational architecture was inserted. **No anatomical number was added to any race spec.** Every insertion ends with "Exact morphology and numeric envelopes remain OPEN" (PV-D22). Each bullet names its packet ID and the deciding item.

## 1. Where the text went

| File | Insertion | Decisions applied |
|---|---|---|
| `specs/fenn/FENN_V1.md` | Pelvic architecture after the "Pelvis and hips" skeletal-region row | PV-D1, PV-D2 (E-A1…E-A3), PV-D3 (a), PV-D4 (a), PV-D13, PV-D15…D17, PV-D19, PV-D20, PV-D22 |
| `specs/aelari/AELARI_V1.md` | Pelvic architecture after the "Pelvis" row | as FN but PV-D5 (vertical elongation) in place of PV-D4 |
| `specs/vael/VAEL_V1.md` | Pelvic architecture after the "Pelvis" row | PV-D1, PV-D2, PV-D6 (a), PV-D7 (a), PV-D13, PV-D15…D17, PV-D20, PV-D22 |
| `specs/durrim/DURRIM_V1.md` | Pelvic architecture after the pelvis row | PV-D1, PV-D8, PV-D9, PV-D13, PV-D15…D17, PV-D19, PV-D20, PV-D22 |
| `specs/grask/GRASK_V1.md` | Shoulder-girdle architecture (AD-G1…G4, AD-G10, AD-G15) and pelvic architecture (PV-D12 (b)) after the pelvic-breadth row | AD-G1…G4, AD-G10, AD-G15; PV-D1, PV-D12 (b), PV-D13, PV-D16, PV-D17, PV-D19, PV-D20, PV-D22. AD-G4 keeps GR vs MF shoulder breadth / stature **undetermined** |
| `specs/gorrund/GORRUND_V1.md` | Girdle / thorax and pelvis paragraphs (GO-G1…G6, AD-G6, AD-G7, PV-D14 full) and the ALPC operational definition (stations S1–S7, ALPC-0…8, ALPC-1b adopted, ALPC-1c report-only) | AD-G5…AD-G10, AD-G15; PV-D1, PV-D14…D17, PV-D19, PV-D20, PV-D22 |
| `specs/pipkin/PIPKIN_V1.md` | Pelvic architecture (PV-D10 written as "≥ MF", PV-D11 convergent femora as a frame statement) | PV-D1, PV-D10, PV-D11, PV-D13, PV-D15…D17, PV-D19, PV-D20, PV-D22 |
| `specs/halvren/HALVREN_V1.md` | One note: the shared-elven pelvic dependency comes from PV-D2; the Halvren sex-related dependency stays separate | PV-D18 |
| `decisions/REFERENCE_ANATOMY_V1.md` | Pelvic method clarification (human-homologous plan is acceptable, skeletal validation, obstetric firewall) and the AD-R15 scope sub-bullet | PV-D1, PV-D16, PV-D20, AD-G13 |
| `reviews/claude-pass2-r5-reference-mesh-queue.md` | RM-LR-02 and RM-LR-06 pass conditions; RM-UB-06 new readings; build-route note | AD-G1…G10, AD-G13, AD-G14, PV-D15, PV-D21 |
| `reviews/claude-rac-05-frame-joint-robusticity.md` | Scope note: AD-R15 covers only SK vs GR thoracic depth and SK vs GO / SK vs GR joint scale; GO > SK thoracic depth stays canon | AD-G13 |
| `reviews/claude-rac-w1d-author-acceptance-gate.md`, `claude-rac-w1d-short-adult-native-strategy.md`, `claude-rac-w1c-cross-race-audit.md` | PV-D10 correction notes **appended** (the issued text is kept as issued): PK pelvic vertical ÷ stature is "≥ MF", not a strict "> MF" | PV-D10 |

**Line citations.** The insertions were drafted against HEAD `352aa4e` line numbers. After insertion, every citation inside the inserted text was renumbered to the post-insertion file (scripted with a line-map diff of HEAD against the edited file, then spot-checked). The same was done for the canon strings in `tools/rac/w1/directional_checks.py`. **Limitation:** earlier review documents that cite these seven specs below the insertion points (W1c / W1d packets, audits and other reviews) were not renumbered. They are correct for their own commit and stale against the current files.

Skarn received no text (AD-G12). The 1 % marginal threshold (AD-G10) appears only in the RMQ and the check tools.

## 2. Flags for the author

- **F-1 — 30 bullets without their own decision item.** These are tagged in the specs as *(PV-D1/PV-D22 general acceptance)*: FN 3, AE 3, VA 5, DU 6, GR 5, GO 1, PK 7. They are the per-race P-1…P-6 resolutions that PV-D1 accepted as a whole and PV-D22 says to canonicalize; PV-D15 also presupposes several of them. **If "accepted" is meant more narrowly, these bullets come out and nothing else changes.**
- **F-2 — PV-D12 (b) reading.** The removed clause is "hip apparatus large relative to pelvic breadth". GR keeps "bitrochanteric ÷ iliac-crest breadth not lower than MF" (the same hip-spacing reading as elven E-A2). The phrase "even where the pelvis reads slender relative to stature" was dropped too, so it cannot imply the removed relation. Please confirm.
- **F-3 — girdle items not canonicalized.** GR-G6 and GR-G8 (frame behaviour) and RM-LR-02 item (f) (Narrow GO thoracic depth ÷ stature > GR, GO L245) were not AD-G decision items. GO-G8 (GO vs SK girdle undetermined) appears only as a restatement of existing canon (R2 L56).
- A drafting flag about the Skarn status line was **withdrawn**: SKARN L386 already carries the W1 acceptance update.

— Claude

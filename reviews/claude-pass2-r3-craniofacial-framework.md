# Common Craniofacial Landmark & Metric Framework (Pass 2)

**Author:** Claude (auditor). **Order:** `reviews/chatgpt-pass2-resolution-sequence-order.md` §6. **Phase:** design only. This is a comparison and measurement framework for the Universal Facial Customization Architecture (UFCA). It is **not** a creator control set, and it does not start the UFCA.

## 1. Design principles

1. **Homology, not topology.**
   - Landmarks are defined on structures that exist in every playable population: the braincase, orbits, the ear canal or auricular opening, the zygomatic arch, the upper jaw, the mandible, and the midline.
   - They are never defined on human-only soft tissue (nasal pyramid, lips, chin pad, pinna).
   - A landmark that has no homolog in a population is **N/A**, never forced.
2. **Two measurement layers.**
   - **S (skeletal):** used where an approved skull exists.
   - **E (external surface proxy):** used on approved reference sculpts, which are surface meshes.
   - Every index states which layer it uses. Cross-race comparisons use the same layer for every population involved.
3. **Comparison landmarks are not creator controls.** The UFCA may expose any controls it likes. Validators measure through this framework.
4. **No values are supplied.** Distributions come only from approved reference meshes (`claude-pass2-r5-reference-mesh-queue.md`). Canon numbers are quoted only where canon already has them (Saurin §258–§259).

## 2. Orientation frame

| Element | Definition | Applicability |
|---|---|---|
| **Midsagittal plane (MSP)** | Best-fit plane of bilateral symmetry of the cranium | All |
| **Auricular reference (Po\*)** | Superior-most point of the external auditory opening. On reference meshes, the centroid of the ear-canal entrance | All. Saurin: the recessed auricular opening (§56); pinna-bearing races: the canal entrance, not the pinna |
| **Orbital floor point (Or\*)** | Lowest point of the inferior orbital rim (E proxy: lowest point of the lower lid–cheek junction over the rim) | All |
| **Frankfort-equivalent plane (FH\*)** | Plane through left and right Po\* and the left Or\* | All. It defines "horizontal" for projection and depth measures. Saurin's reference head orientation is consistent with it (head-local frame of the Part 7 tools) |
| **Facial axis (f)** | Within the MSP, parallel to FH\*, positive forward | All |

## 3. Universal landmarks (homologous)

| Code | Landmark | S definition | E proxy (reference meshes) | Notes |
|---|---|---|---|---|
| V | Vertex | Highest cranial point relative to FH\* | Highest scalp, skin or scale surface point, excluding hair and displays | Saurin: exclude cranial keratin displays (§100); structural ridges are included |
| Op | Opisthocranion | Most posterior midline braincase point | Most posterior head surface point (Saurin Part 7: "occ") | — |
| Eu | Euryon (pair) | Maximum cranial breadth points | Same on the surface, above the ear region | — |
| G\* | Frontal-orbital midpoint | Midline point between the supraorbital margins (glabella-equivalent) | Same | Saurin: brow-temporal platform midline (§42) |
| N\* | Fronto-facial junction | Midline junction of the frontal bone and the facial or rostral skeleton, between the orbits | Deepest midline point between the orbits | All. Saurin: rostral root between the orbits |
| OC | Orbit / eye centre (pair) | Centre of the bony orbit aperture | Eyeball centre (Saurin Part 7 used eye centres) | All |
| Ec / Mf | Lateral / medial orbital rim (pair) | Ectoconchion / maxillofrontale | Lateral and medial canthal-rim points over bone | Orbit breadth and interorbital measures |
| Zy | Zygion (pair) | Maximum bizygomatic breadth | Same on the surface | All. Saurin: lateral facial integration (§54) |
| **FAL** | **Facial anterior limit** | Most anterior midline point of the upper-jaw or rostral skeleton: prosthion in humanoids; rostral tip in Saurin | Most anterior midline point of the face **excluding the external nasal pyramid, lips and any keratin display**. Humanoids: subnasale–upper alveolar region (the more anterior of the two). Saurin: rostral tip | **The key homolog for projection.** Using pronasale (nose tip) for humans would impose human soft anatomy and falsely inflate human projection |
| Pr | Upper alveolar midline | Prosthion | Upper-lip base over the alveolus (humanoids); upper jaw margin under the rostral tip (Saurin) | Maxillary projection |
| Me / Gn | Menton / gnathion | Lowest and most anterior-inferior mandibular midline points | Same, excluding chin soft tissue and beard | Saurin has no chin (§47). Gn is still defined as the anterior-inferior mandibular midline |
| Go | Gonion (pair) | Mandibular angle | Same | Posterior jaw depth (Saurin §259) and bigonial breadth |
| Co | Condylion (pair) | Top of the mandibular condyle | Pre-auricular surface point over the joint | Ramus height |

## 4. Race-conditional landmarks

These are used only where the structure exists. They are never comparison anchors across families.

| Structure | Races | Landmarks |
|---|---|---|
| External nasal pyramid | All except Saurin | Pronasale, alar base, nasal bridge (soft-tissue nose indices) |
| Lips and chin pad | All except Saurin (§49 no default lips; §47 no chin) | Labrale, pogonion (soft) |
| Pinna | All except Saurin | Superaurale, subaurale, auricle tip, auricle projection. **Family-specific parameter sets** (report 03 §5) |
| Rostral nasal openings | Saurin | Nostril centre on the rostrum (§52) |
| Cranial keratin displays | Saurin | Display base footprint, chord, crest height (§260) |
| Tusk-like canines | Grask and Gorrund only, if later approved | Canine tip vs occlusal plane |

## 5. Comparison indices

Unless stated otherwise, every distance is measured in the MSP / FH\* frame. "Head length" **HL = f(FAL) − f(Op)**. "Head height" **HH = V − Me** (vertical).

| Index | Formula | Layer | Purpose / canon link |
|---|---|---|---|
| **FPI — facial projection index** | (f(FAL) − f(OC_mid)) ÷ HL | E (S where a skull exists) | General projection. **Saurin rostral index** in canon is this form, measured on the Part 7 surface reference: tip, eye centres, occiput; reference 0.288; creator band 0.255–0.335 (§259). It needs a confirmation re-measure under this framework's FAL definition (RM-CF-01) |
| MPI — maxillary projection | (f(Pr) − f(N\*)) ÷ HL | S/E | Grask "maxillary projection distribution OPEN" (GR L362; central projection authored RAC Phase 2); Gorrund prognathism OPEN (GO L312; comparator authored RAC Phase 2) |
| MdPI — mandibular projection | (f(Gn) − f(N\*)) ÷ HL | S/E | Same |
| CI — cranial index | Eu–Eu ÷ (f(G\*) − f(Op)) | S/E | Vault breadth to length |
| CBH — cranial breadth to height | Eu–Eu ÷ (V − Po\*) | S/E | Durrim (P3 L170) and Gorrund (GO L301): "greater cranial breadth relative to cranial height than Marchfolk" |
| FVB — facial vertical to breadth | (N\* − Me) ÷ Zy–Zy | S/E | Grask facial verticality (GR L349). Must be paired with MVI, because canon says it is "not defined solely by height-to-width" (GR L471–473) |
| MVI — midface vertical | (N\* − Pr) ÷ HH | S/E | Grask midface (GR L358); Pipkin midface "not shortened" (P3 §6) |
| FDH — facial depth to facial height | (f(FAL) − f(Po\*)) ÷ (N\* − Me) | S/E | Durrim depth : facial height tendency (C2 L282). Durrim's five depth domains A–E use regional variants of this (C3 L292–298) |
| FVI — face to vault | (N\* − Me) ÷ (V − Po\*) | S/E | Cogling face-to-vault "at or slightly above the Marchfolk adult" (§75); Pipkin/Cogling anti-juvenile |
| ORB — orbit size | Orbit breadth (Ec–Mf) ÷ HL; orbit height ÷ HH | S/E | Orbit size ≠ visible aperture: the aperture is a soft measure, kept separate (Pipkin P3 §4; Cogling §79; Saurin couples them, §259) |
| IOD — interorbital | Mf–Mf ÷ Zy–Zy | S/E | Orbit spacing (Saurin §43 "greater lateral spacing than Marchfolk") |
| TBP — transverse breadth profile | (Ec–Ec, Zy–Zy, Go–Go) ÷ Zy–Zy | S/E | Gorrund Transverse Structural Continuity: lateral brow/orbit, zygoma and posterior mandible breadth coherence (GO L419–431) |
| JDI — jaw depth | (Co − Go) ÷ HH; posterior jaw depth = (Or\* level − Go) ÷ HH | S/E | Saurin posterior jaw depth bound −12 % / +15 % (§259); Grask vertical ramus (GR L370) |
| HSR — head to stature | HH ÷ standing height; HL ÷ standing height | E | Saurin head length/H 0.156–0.184 (§258); OPEN for Grask, Gorrund, Pipkin and Cogling |

**Never cross-race:**
- soft nasal indices;
- lip indices;
- pinna indices across ear families;
- display indices.

These stay race-conditional.

## 6. Applicability check (order stop condition)

| Family | Universal landmarks available? | Imposition risk | Result |
|---|---|---|---|
| Human populations, Halvren | All | None | OK |
| Elves | All | None. Elven pinna is excluded from universal indices | OK |
| Durrim, Pipkin, Cogling | All | Small heads (Cogling ~11–13 cm): E-layer precision limits, not a homology problem | OK |
| Grask, Gorrund | All | Tusk-like canines are excluded from FAL and Pr | OK |
| Saurin | All. Po\* = auricular opening; N\* = rostral root; FAL = rostral tip; Gn defined without a chin | **Avoided** by defining FAL without the nasal pyramid or lips, and Gn without a chin pad | OK |

**No universal index requires imposing the wrong anatomy.** The stop condition in order §10 is not triggered.

## 7. Audit: the Saurin rostral floor vs Marchfolk, Grask and Gorrund

**Requirement** (Saurin §39, §146, §259): the minimum valid Saurin rostrum (FPI floor 0.255, provisional) "remains clearly outside the approved adult projection ranges of Marchfolk, Grask and Gorrund".

**Findings:**
1. **The source ranges cannot be derived legitimately today.**
   - Marchfolk canon has no projection values.
   - Grask keeps maxillary and mandibular projection numbers OPEN (GR L362; central ≈ Marchfolk authored RAC Phase 2).
   - Gorrund keeps prognathism numbers OPEN (GO L312; comparator authored RAC Phase 2).
   - No approved reference meshes exist for these populations.
   - Under order §8, no value is fabricated.
2. **The Saurin value is not yet framework-conformant.** The Part 7 rostral index used the frozen surface reference (tip, eye centres, occiput). It needs a re-measure under this framework's FAL and OC definitions to confirm 0.288 and the 0.255 floor. This is expected to be identical or close, because the Saurin tip has no nasal pyramid or lips, but it must be verified.
3. **Saurin identity is not weakened.** The floor stays a provisional Saurin requirement (§259). The comparison direction is fixed: the Saurin floor must exceed the **maximum valid** FPI of each comparison population, with a margin the author sets.

**Status:** cross-race numeric closure **OPEN, deferred with named input.** The measurements required are:

| ID | Population | Measurement |
|---|---|---|
| RM-CF-01 | Saurin | FPI on the frozen reference (aff1b52) under this framework. Also FPI at the minimum-rostrum creator extreme and at the cranial-length × rostrum-floor coupling corner (§259) |
| RM-CF-02 | Marchfolk | FPI, MPI and MdPI distribution over an approved reference set spanning its facial range, including the most prognathic valid adult face |
| RM-CF-03 | Grask | FPI, MPI and MdPI at the reference and at the maximum valid midface / projection extremes. Prerequisite authored RAC Phase 2 (GR L362; GR-FACE-14) |
| RM-CF-04 | Gorrund | Same as RM-CF-03, with the Gorrund comparator authored RAC Phase 2 (GO L312; GOR-FACE-05) |
| RM-CF-05 | Decision | Author sets the required FPI margin between the Saurin floor and max(RM-CF-02…04) |

## 8. What the UFCA inherits from this framework

1. One orientation frame (FH\*) and one landmark dictionary, with per-race N/A flags.
2. Validators that compute comparison indices, never as creator sliders.
3. Race-conditional soft and auricular measures, kept outside cross-race comparison.
4. The rule that per-race floors (Saurin FPI, future others) are checked against other populations' **valid maxima** on the same layer.

— Claude

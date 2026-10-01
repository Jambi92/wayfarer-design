# Audit: Cogling v1.0 Part 3, Craniofacial anatomy, ears and facial customization requirements

**Auditor:** Claude
**Audited file:** `specs/cogling/COGLING_V1.md` at commit `c1e03c9`
**Request:** `reviews/cogling-part-3-audit-request.md`
**Compared against:**
- Cogling Parts 1–2
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`, including the AGREED Facial Diagnostic Domain rule
- the approved craniofacial sections of Pipkin (Part 3), Durrim, Fenn, Sagekin, Grask, Gorrund and Marchfolk

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Part 3 has very strong anti-child safeguards:
- the midface is never shortened, and the lower face is mandatory (§81, §83, §85)
- the orbit is separate from the eye opening, with no enlarged eyes (§79)
- readability is solved by camera, animation and rendering, not by enlarging features (§99)
- "expressive face" is firewalled from personality and biology (§92)
- the attractiveness, sex, age and asymmetry firewalls are all present (§93–96)
- invalid-combination rules and a broad validation cast are included (§101–102)

There are no contradictions with project rules.

One finding should be resolved before acceptance (4a): **the positive facial anchor describes a well-formed small adult face, not a Cogling-specific relationship**, and the facial boundaries with the approved Pipkin, Durrim, Fenn and Sagekin faces aren't stated. This is the same pattern the Pipkin Part 3 audit found (4a there), and it was fixed the same way.

## 2. The sixteen requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Fine-Scale Planar Integration is positive, not generic | **Needs clarification** (4a) |
| 2 | Adult maturity at about 76 cm | PASS (§76, §81, §83, §85, §94, COG-FACE-02 and 20) |
| 3 | Eyes not enlarged | PASS (§79, §99, COG-FACE-04) |
| 4 | Midface and mandible prevent toddler coding | PASS (§81, §83, §85, §101) |
| 5 | Nose avoids button and gnome stereotypes | PASS (§82, COG-FACE-08 and 09) |
| 6 | Brow, orbit, zygoma and lower face coherent | PASS (§78–85) |
| 7 | Fine Folded Auricular Architecture is positive and distinct | Partly: distinct from elf, Grask and Gorrund ears, but Pipkin and Durrim are missing, and the ear overlaps human ears (4c) |
| 8 | "Expressive face" firewalled | PASS (§84, §92) |
| 9 | Sex, age, adiposity, attractiveness and asymmetry independent | PASS (§91, §93–96) |
| 10 | No convergence with Fenn, Sagekin, Durrim or Pipkin | **Not yet demonstrated** (4a, 4b) |
| 11 | Readability as a camera and rendering problem | PASS (§99, COG-FACE-24), with a note in 4c |
| 12 | Functional requirements without freezing the UI | PASS (§97–98) |
| 13 | Combined-proportion validity | PASS (§101) |
| 14 | Validation cast | Good; see §5 |
| 15 | Surface stays deferred | PASS (§100) |
| 16 | Nothing about movement, gameplay or UE5 decided | PASS |

**Dependency question (request note):** Cogling Part 3 doesn't depend on any face that hasn't been designed. Pipkin, Durrim, Fenn, Sagekin, Grask, Gorrund and Marchfolk all have approved craniofacial anatomy. COG-FACE-16's phrase "once Pipkin comparison is applied" should therefore read as a present requirement, not a later dependency. Pipkin's face (Integrated Mature Facial Architecture) is FIRST-PASS ACCEPTED.

## 3. Contradictions

None.

## 4. Findings

### 4a. The anchor doesn't name a Cogling-specific relationship, and facial boundaries are missing (should be resolved before acceptance)

Fine-Scale Planar Integration is "a compact adult cranial envelope [supporting] a proportionally mature face whose brow, orbital margins, zygomatic region, midface and mandibular framework remain clearly differentiated at very small absolute scale, with relatively fine skeletal transitions."

Apart from "fine" relief, every element of that sentence describes any healthy adult face: differentiated planes, a mature midface and a mature lower face. No relationship differs from Marchfolk at normalized size.

"Fine" relief (§78, §80, §83: modest brows, fine zygomas, fine mandible) also matches approved **Fenn** tendencies ("slightly lighter mid-face," "somewhat lighter jaw," a narrower skull) and the gracile end of **Sagekin** and Marchfolk. So COG-FACE-17, 18 and 19 have nothing specific to check, which is exactly the gap the Pipkin Part 3 audit found.

The approved faces Cogling must stand apart from are:

| Race | Approved facial anchor |
| --- | --- |
| Durrim | Greater cranial breadth relative to cranial height; compact vertical facial relationships; greater depth relative to facial height |
| Pipkin | Integrated Mature Facial Architecture: a moderately broad cranial base flowing through temple and zygoma into the central midface; Marchfolk-range depth; adult structures never shortened |
| Fenn | Slightly larger orbits; higher cheekbones; lighter midface and jaw; narrower skull |
| Sagekin | Human face; moderate to slightly longer face; somewhat higher forehead |

Cogling §75–86 contrasts none of these except Durrim (by mass only, §86).

**Recommended:**
1. **Name one or two relational tendencies against Marchfolk** that mirror the body system and point away from a child. Two possible directions, for ChatGPT to choose or replace:
   - **Face-to-cranium relationship.** Facial skeletal height relative to cranial vault size sits at or slightly above the Marchfolk adult relationship. Toddlers have the opposite: a large vault over a small face. This gives "compact cranial envelope" a measurable meaning and reinforces adulthood.
   - **Distinct planar junctions.** Junctions such as orbit-to-zygoma, zygoma-to-maxilla and the gonial angle are clearly angled, even where overall relief is modest. "Planar" then means defined transitions with low mass, which separates Cogling from Fenn's lightness and from a soft toddler face.
2. **Add a facial boundary section**, parallel to body §63–67, with Pipkin, Durrim, Fenn and Sagekin rows built on the approved anchors in the table above. For example:
   - **Durrim:** Cogling aren't vertically compact or depth-dominant.
   - **Pipkin:** Cogling don't use the broad cranial base flowing through temple and zygoma into the midface.

   Then give COG-FACE-16, 18 and 19 explicit pass criteria based on those rows.

### 4b. "Compact cranial envelope" reuses the overloaded term (minor)

The body was renamed to a "narrow stable central core" to get away from the Durrim and Pipkin "compact" terms. §75 and §104 reintroduce "compact" for the cranium. If option 1 in 4a is adopted, "adult cranial envelope" or "moderate cranial envelope" works. Otherwise, leave it for the Short-Race Review.

### 4c. Ears: Pipkin and Durrim rows are missing, and the fine detail will rarely be visible

**Comparison.** Fine Folded Auricular Architecture ("compact adult ear, clearly defined helix, antihelix and conchal bowl, fine cartilage, rounded upper contour") is close to the approved Pipkin ear tendency. That tendency is "compact rounded … clear but not deep conchal bowl, continuous moderate helix," explicitly overlapping Marchfolk and Durrim ears. §90 compares elves, Grask, Gorrund and humans, but not **Pipkin** or **Durrim**, the two closest. The only difference is fold crispness and fine cartilage.

**Visibility.** At an adult-valid head height of about 11–13 cm, the ear is roughly 2.5–3.5 cm tall. Its "fold clarity at fine scale" will be visible in creator close-ups but rarely at gameplay or dialogue distance.

**Recommended:**
- Add Pipkin and Durrim rows to §90.
- State, as Pipkin did, that Cogling ears are a **secondary central tendency** that overlaps other humanoid ears and is not a primary identifier. §90 says this for humans already; extend it to all humanoid ears.
- Note in §99 that the fold detail is a close-view trait.

### 4d. Facial Diagnostic Domains not used (minor)

The AGREED terminology (Durrim consistency patch) labels facial diagnostics as FD-STRUCT, FD-SOFT, FD-SURF, FD-HAIR, FD-PRES and FD-OBS. Pipkin Part 3 uses them. Cogling §100–102 describe the same separations in other words. Labeling the validation cast with FD domains would keep the two short races consistent.

## 5. Validation cast

The validation cast is strong on child read (COG-FACE-02, 20 and 23), eyes, nose, adiposity, ears, sex range, asymmetry and camera readability (COG-FACE-24).

Recommended additions or edits:
- **Pass criteria.** Give COG-FACE-16, 18 and 19 explicit pass criteria from the 4a boundary rows.
- **Durrim, normalized face.** Add a normalized-head Cogling vs Durrim face test. COG-FACE-06 tests mass, not the vertical-compactness and depth relationship.
- **Like-for-like sex.** Make the sex comparison like-for-like against Marchfolk (male vs male, female vs female), matching Pipkin PIP-FACE-22 and 23 and Cogling body COG-BODY-28. COG-FACE-21 tests range, not same-sex comparison.

## 6. Completion recommendation

1. ChatGPT patches 4a: a relational anchor plus facial boundary rows.
2. Recommended alongside it: 4c and the §5 test edits. 4b and 4d are optional.
3. I re-audit.
4. On a PASS and Tyler's approval, Part 3 is accepted.

Part 4 should not begin until then.

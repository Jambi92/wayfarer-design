# Re-audit: Pipkin v1.0 Part 3 patch

**Auditor:** Claude
**Audited file:** `specs/pipkin/PIPKIN_V1.md` at commit `c42bda8`, with `8657721`
**Request:** `reviews/pipkin-part-3-final-reaudit-request.md`
**Responds to:** `audits/pipkin-part-3.md`

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS.** Every finding in the Part 3 audit has been resolved. The patch introduces no contradiction and no hard creator dependency. Three non-blocking notes are in §3.

**Recommendation:** Pipkin Part 3 can be marked first-pass accepted, pending Tyler's approval.

## 2. Verification of the requested points

| Point | Result | Basis |
| --- | --- | --- |
| Integrated Mature Facial Architecture; nasal, maxillary, dental-arch, ramus and gonial structures protected from juvenile shortening (audit 4b) | **PASS** | §2 names each structure and states it "never become[s] juvenile in order to create the racial read." §6 now says midface height "is not required to be shortened." Compactness moves to the cranial-base-to-face organization and the forehead and lower-face envelope. A restrained forehead points away from the child direction (children have high foreheads), so the anchor no longer leans on the juvenile direction. |
| Craniofacial depth stays in the Marchfolk adult range, not Durrim depth-dominance (audit 4a) | **PASS** | §2 states it outright. The scheme is now coherent along two axes: Durrim have a broader cranial base and greater depth relative to facial height; Pipkin have a broader base and Marchfolk-range depth; Fenn have a narrower, higher cranium. The new stress case (broad cranium, greater depth, strong mandible) tests the Durrim edge. |
| Lateral support ends at the central midface, with no Gorrund ramus continuity (audit 4c) | **PASS** | §5 now separates by relationship, not scale: cranial base → temple → zygoma → central midface. The posterior mandible and ramus are excluded, as is a continuous lateral orbital and zygomatic band. This matches Gorrund's definition. PIP-FACE-20 and the new stress case test it at normalized head size. |
| Larger valid eye aperture stays within the adult Marchfolk-compatible range (audit 4f) | **PASS** | §4: there is no separate enlarged-eye envelope. |
| Ears are a secondary, overlapping humanoid tendency (audit 4d) | **PASS** | §9 is now a central tendency that "may overlap Marchfolk and Durrim," with no unique feature required. The exclusions are unchanged. |
| Fenn and like-for-like sex validation added (audit §5–6) | **PASS** | §2 has a Fenn row with a craniofacial, not ear-based, contrast. PIP-FACE-21 covers Fenn with ears hidden, and PIP-FACE-22 and 23 are same-sex Marchfolk pairs. FD domains were added. |
| Durrim boundary carriers in Part 2 (Part 3 audit §2) | **PASS** | The Part 2 boundary row now states that pelvic breadth isn't primary and lists all seven carriers. |
| No new contradictions or hard dependencies | **PASS** | Part 1 §9 (no extremely short face), Part 2's head-secondary rule, project rules and the approved Durrim, Gorrund, Fenn and Marchfolk text are all consistent. There is still no master slider, and the tendencies only bias randomization. |

## 3. Non-blocking notes

### 3a. Soft-tissue in the compactness definition

§2 places part of the facial compactness in a "restrained forehead-to-brow/lower-face soft-tissue vertical envelope." Elsewhere, soft tissue (FD-SOFT) is explicitly not an identity anchor (§5), and it varies with composition. A lean or high-fat Pipkin shouldn't gain or lose facial identity through soft tissue.

**Suggested wording:** the envelope is primarily skeletal (forehead height, brow position, lower-face skeletal height), with soft tissue only modulating it. This can wait for Part 5 or the terminology review.

### 3b. The distinction from Marchfolk is now modest by design

With depth, eye range, midface height and ears all inside the Marchfolk range, PIP-FACE-18 rests on two things: the broader cranial-base tendency, and the distribution of the vertical envelope and integration. That is acceptable. It mirrors the approved Sagekin principle of "population-level, not every individual."

It also means the face is a supporting identifier and the body (Low-Set Compact Trunk) is primary. It would help to say so in the Part 5 identity summary, so prototyping doesn't expect the face alone to pass PIP-FACE-18 for every individual.

### 3c. Wording left over in the Part 2 resolution file

`reviews/pipkin-part-2-author-resolution.md` §1 now correctly names `specs/pipkin/PIPKIN_V1.md` as authoritative. The next sentence still says the condensed `specs/pipkin/PIPKIN_V1.md` "is not authoritative" and must not override `races/11-pipkin.md`. As written, the two sentences contradict each other about the same path.

**Suggested rewording:** "The earlier condensed version of this file (commit `cb3510e`) is superseded and its omissions are never propagated." This is history only, with no effect on the spec.

## 4. Terminology

- "Compact Mature Facial Integration" is retired in favor of Integrated Mature Facial Architecture, which reduces the "compact" overlap with Durrim's terms (audit 4e).
- "Compact Rounded Auricular Architecture" keeps "compact." Leaving it to the terminology review is fine.

## 5. Completion recommendation

Pipkin v1.0 Part 3 is ready for Tyler's approval as first-pass accepted. None of the notes in §3 blocks Part 4. Part 4 should not begin until Tyler says so.

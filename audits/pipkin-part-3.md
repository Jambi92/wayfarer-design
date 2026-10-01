# Audit: Pipkin v1.0 Part 3, plus the Part 2 patch check

**Auditor:** Claude
**Audited file:** `specs/pipkin/PIPKIN_V1.md` at commit `da3692b`
**Request:** `reviews/pipkin-part-3-audit-request.md`
**Compared against:**
- Pipkin Parts 1–2
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the Marchfolk, Durrim, Gorrund, Grask, Fenn, Aelari, Vael and Halvren specs in `specs/`

These are findings, not changes. The spec was not edited.

## 1. Result

**Part 3: PASS WITH CLARIFICATIONS.** Nothing in Part 3 contradicts Parts 1–2, project rules or another approved race. Two clarifications (4a and 4b) should be resolved before Part 3 is accepted, because the positive facial anchor currently overlaps Durrim's approved facial tendencies and leans on scale to separate from Gorrund.

**Part 2 patch: PASS.** It introduces no contradiction. One approved item wasn't written in (§2).

## 2. Part 2 patch check

- **Patched in, consistent with the re-audit:**
  - the vertical-trunk, lumbar and pelvic anchor
  - the rule that the shorter trunk is made up by limbs and pelvic height, not by a larger head
  - the like-for-like sex row
  - PIP-BODY-28 and PIP-BODY-29
- **Not patched in:** the Durrim-boundary carriers (author resolution §4). Tyler approved the whole clarification package, but the spec's Durrim boundary row still lists Part 2's original traits. It doesn't state that pelvic breadth isn't the primary discriminator, and it doesn't name torso vertical organization and long-bone robusticity as boundary carriers. This is minor. It can go in with the Part 3 patch.
- **Stale wording:** `reviews/pipkin-part-2-author-resolution.md` §1 still names `races/` as authoritative. The Part 3 request correctly treats `specs/` as authoritative, so this is a one-line fix to an old file, logged as history in the register.

## 3. Contradictions

None.

- Part 1 §9 forbids an "extremely short face"; Part 3 §6 keeps the midface "modestly compact."
- Part 2 requires adulthood without facial hair, wrinkles, severe features, a large nose or a heavy jaw; Part 3 §1, §8 and §14 deliver that.
- Head contribution stays secondary, consistent with the Part 2 rule against absorbing trunk share into the head.

## 4. Ambiguities and missing positive anchors

### 4a. The facial anchor overlaps Durrim's approved tendencies (should be resolved before acceptance)

Durrim Part 3 already approved, as Durrim population tendencies against Marchfolk:
- greater cranial breadth relative to cranial height
- compact vertical facial relationships (lower vertical contribution relative to breadth and depth)
- strong midface integration

The Durrim depth clarification adds a fourth: greater craniofacial depth relative to facial vertical height.

The Pipkin anchor is "a moderately broad cranial base … integrated into a vertically compact … midface and lower face." That is the same two tendencies as Durrim (broad cranium, vertically compact face), described as "moderate." The only Durrim trait left to separate them is depth, and Part 3 never says what Pipkin facial depth is. §2 describes Durrim as having "greater cranial breadth/depth," and PIP-FACE-19 tests "compact maturity vs structural depth/mass." But the Pipkin side of that comparison isn't defined.

At normalized head size, which PIP-FACE-19 requires, the distinction comes down to degree. This is the same problem the Part 2 audit found with pelvic breadth.

**Recommended (requested item 2):**
- State the Pipkin depth relationship. For example: craniofacial depth relative to facial height stays within the Marchfolk adult range, never trending toward Durrim depth-dominance.
- Name what is Pipkin-specific in the facial integration, beyond "less of the Durrim recipe." Candidates:
  - how the compactness is distributed (which vertical segments are shorter)
  - the relationship of the cranial base to the midface
  - the zygomatic-to-orbit placement

### 4b. The anchor's compact direction is the juvenile direction, so adulthood rests on qualifiers (requested items 1 and 3)

Compared with adults, human children have:
- a cranial vault that is large relative to the face
- a vertically short face
- a short midface and short mandibular ramus
- a low nasal bridge
- relatively large orbits

The Part 3 anchor (moderately broad cranium, vertically compact midface and lower face) points the same way. It then restores adulthood through qualifiers: "clear adult orbital, nasal, maxillary and mandibular development" and "without juvenile enlargement."

That is the reverse of Part 2. There, the trunk anchor pointed away from a child (children have relatively long trunks). Here, the positive anchor points toward a child, and the maturity requirements act as a counterweight. So, on requested item 1, the anchor is positive, but its distinctive component is the one most at risk of a child read, and the adult read depends on the anti-child checklist.

**Recommended:** say which facial components carry the vertical compactness and which never do. The dimensions that are short in children should be explicitly exempt and stay at adult relationships:
- mandibular ramus height relative to the face
- nasal bridge development
- maxillary and dental-arch depth
- adult gonial definition

Compactness should come from elsewhere. Possible sources:
- forehead-to-brow distribution
- a modestly shorter lower-face soft-tissue height
- the overall face-to-cranium vertical relationship within adult limits

This also helps 4a, since Durrim compactness comes with added depth and Pipkin compactness would have its own distribution.

### 4c. The temple and zygomatic system separates from Gorrund by scale, which fails at normalized head size (requested item 5)

Gorrund Transverse Structural Continuity is relational. It is defined as coordinated continuity across:
- cranial breadth
- the lateral brow and orbital margins
- zygomatic placement
- the temporal transition
- the posterior mandible and ramus

Gorrund's spec says a narrower Gorrund keeps it "within a narrower envelope," so it doesn't depend on mass.

The Pipkin anchor also links cranial breadth to temple and zygomatic support. §5 separates the two only by mass: "do not require massive lateral brow-orbital structures, heavy temporal mass, or a broad load-bearing mandible." At normalized head size (PIP-FACE-20), mass is the variable being controlled for.

**Recommended:** a relational distinction. For example:
- Pipkin lateral support links the cranium to the central midface (cranium → temple → zygoma → midface).
- The posterior mandible and ramus take no part in the Pipkin lateral framework.
- Lateral orbital margins and zygomatic arches don't form a continuous transverse band.

### 4d. Pipkin ears read as ordinary human ears (requested item 6)

"Moderate projection, rounded-to-softly-angular upper contour, clear but not deep concha, continuous moderate helix, close attachment" describes a typical Marchfolk ear. It also fits Durrim ears, which are approved as "broadly humanoid … broad compact-humanoid range."

The exclusions against the elven point, the Grask taper and the Gorrund deep bowl are sound. But nothing positively separates Pipkin ears from Marchfolk or Durrim ears.

Ears are secondary and must not carry identity (PIP-FACE-13), so this isn't blocking. Choose one of:
- **(a)** name one or two positive differences from Marchfolk (for example ear height relative to head height, breadth-to-height ratio, or lobule proportion), or
- **(b)** say plainly that Pipkin ears sit within the humanoid ear range, are not a racial identifier, and that "Compact Rounded Auricular Architecture" describes the central tendency only.

Option (b) is honest and low-risk.

### 4e. "Compact" is overloaded

Pipkin now carry three "compact" terms:
- Low-Set Compact Trunk
- Compact Mature Facial Integration
- Compact Rounded Auricular

Durrim's core terms are "compact structural concentration" and "compact craniofacial foundation."

Shared vocabulary between the two short races invites exactly the convergence in 4a. Consider a distinct word for the Pipkin face (for example "Integrated Mature Facial Architecture") or ear term. This belongs in the terminology review, so it isn't required now.

### 4f. Larger visible eye openings (requested item 4)

The terminology is right:
- the orbit is separate from the visible aperture
- "do not possess biologically oversized eyes"
- PIP-FACE-07 and the stress combination for lower midface plus larger aperture are present

One addition: define "larger-valid" visible aperture and orbital size relative to the face as staying within the Marchfolk adult range. Combined with a vertically compact face, an aperture that is large only by Pipkin's own standard would still read large relative to the face.

## 5. Cross-population conflicts

- **Durrim:** see 4a. Their recipes overlap on cranial breadth and vertical compactness.
- **Gorrund:** see 4c. Separated only by scale at matched head size.
- **Fenn and the elven family (requested item 2):** §2 contrasts the elves only by "elven craniofacial family and ear biology." Approved Fenn facial tendencies include:
  - slightly larger orbits and more eye prominence
  - higher cheekbones
  - a lighter midface
  - a lighter jaw

  A soft-featured Pipkin with a larger valid aperture, moderate jaw and integrated zygomatic support is close to a short Fenn face with round ears. Hiding the ears removes the main elven contrast. Recommended:
  - state a craniofacial (not ear) contrast with Fenn, for example the Pipkin cranial-breadth tendency against Fenn's narrower skull and greater cranial height
  - add a validation case (Pipkin vs Fenn at normalized head size, ears hidden)
- **Halvren:** not mentioned. A human-leaning Halvren with rounded ears isn't defined against Pipkin. Low priority, since stature separates them, but the Part 1 comparative table has a Halvren row and Part 3 could mirror it.
- **Marchfolk:** PIP-FACE-18 covers it. Its pass condition depends on 4a and 4b defining what is specifically Pipkin.
- **Grask:** no conflict. The ear exclusion is correct.

## 6. Sex, culture and presentation (requested item 7): PASS

- Facial hair is never required for adult or male recognition.
- Sex-related facial-hair distributions stay OPEN and use soft correlations.
- Lips are not sex-locked.
- Eyelashes are never sex or youth shorthand.
- No hairstyle is biological.
- There is no curly, shaggy, rustic or hairy-feet requirement.
- Grooming is presentation.

**Recommended addition:** make the face validation cast like-for-like by sex, matching Part 2's PIP-BODY-28 and 29. Facial dimorphism (brow, jaw, chin) interacts directly with the child-read risk, especially for soft-featured faces.

## 7. Hard dependencies (requested item 8): PASS

- There is no "Pipkin Face" master slider.
- Control families are independent or relationship-aware.
- Population tendencies bias randomization without forcing controls to move together.
- The facial-control status label matches project rules.

## 8. Prototype conflicts

None known. The prototype has no facial customization, so there is nothing to reconcile. The UE5 project was not opened.

## 9. Validation coverage (requested item 10)

Strong on child-read risk:
- PIP-FACE-02, 03, 07 and 17
- the four anti-child stress combinations

Recommended additions:
- **PIP-FACE-21:** Pipkin vs Fenn at normalized head size, ears hidden (5).
- **PIP-FACE-22 and 23:** like-for-like sex comparisons against Marchfolk (6).
- **Stress case:** broad cranium plus greater facial depth plus strong mandible at normalized head size; must not become Durrim (4a).
- **Stress case:** broad cranium plus broad zygomatics plus a strong ramus at normalized head size; must not form Gorrund Transverse Structural Continuity (4c).
- **FD domains:** label the diagnostics with the facial diagnostic domains (FD-STRUCT, FD-SOFT, FD-SURF, FD-HAIR, FD-PRES, FD-OBS), as Durrim, Grask and Gorrund do. This is AGREED terminology per the Durrim consistency-resolution patch.

## 10. Completion recommendation

1. ChatGPT patches 4a, 4b and 4c. These are needed before Part 3 is accepted.
2. Recommended alongside them:
   - 4d (option (b) is enough)
   - 4f
   - the Fenn contrast and validation additions in §5, §6 and §9
   - the Part 2 Durrim-boundary carriers (§2)
3. 4e can wait for the terminology review.
4. With those in place, Part 3 can be marked first-pass accepted.

Part 4 should not begin until Tyler says so.

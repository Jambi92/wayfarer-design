# Audit: Fenn Character Customization v1.5 (first-pass complete)

Auditor: Claude. These are notes to check, not changes. Nothing here overrides the spec in `specs/fenn/FENN_V1.md`; Tyler decides what, if anything, changes.

## Open notes

- **Matches the brief.** The 181 cm reference is about 1.05× Marchfolk's 173 cm, which matches the brief's Fenn height (§16.4).
- **Traits already in the game.** The game gives Fenn a 0.8× sneak-noticeability multiplier and 1.1× swim speed. That matches §11, and the values stay as they are.
- **Game scale.** The game currently draws Fenn at 0.95× scale, which is shorter than Marchfolk. The spec makes Fenn slightly taller on average (1.05×). This is a placeholder, but it runs the opposite way to the spec.
- **Skeleton plan.** The earlier race-models plan had Fenn starting from a MetaHuman with pointed ears and a lighter frame, possibly sharing one elven skeleton with Aelari and Vael. A genuinely non-human skeleton (§1, §3) means Fenn need their own proportions and joint layout. They can still share core bone names so animations transfer. This goes to the skeleton-strategy review.
- **Game description.** The in-game text ("quick, graceful, and at home among the trees") fits, as long as "graceful" isn't read as "thin".

* **Proportion rule is already agreed (v1.1 §1).** "Connected anatomy, not mesh stretching" is already an agreed universal rule from the master brief (§7), Marchfolk v1.1 §6 and Skarn v1.1 §8. v1.1 applies it to Fenn and adds "the player sets the proportion, the system keeps coherence". The register records this under the existing agreed rule rather than as a new proposal.
* **Combined limits and randomization (v1.1 §11).** Combined-proportion validation is the same mechanism that relationship-aware randomization (Skarn v1.4 §4) needs, so one rule set can serve both the manual sliders and the randomizer.

- **Attractiveness rule is already in the brief (v1.2 §13).** The master brief's §17 already says to avoid "every character being young and conventionally attractive". v1.2 restates it as a universal principle, so the register marks it agreed.
- **Headwear and ears (v1.2 §8–9).** Long, swept or projecting Fenn ears will clash with helmets and hoods built for human heads. This adds to the headwear question already open from Marchfolk v1.2.

* **Vael direction matches the brief (v1.3 §3).** The retained Vael palette matches the master brief's §16.6, so nothing conflicts.
* **Night sight isn't in the game yet (v1.3 §9).** The game has no low-light vision trait for any race. The race code only notes that "night sight" gifts will come with later systems, so leaving Fenn low-light vision open costs nothing now.
* **Settlements and other races (v1.3 §11).** Making Fenn settlements usable by other races lines up with Skarn v1.5's proposed world-compatibility rule. Canopy bridges, lifts and doorways will need to fit Skarn and Gorrund too.

- **Randomize split and earlier lists (v1.4 §12).** The biological versus presentation split tidies up the randomize lists already on file: brief §13, Skarn v1.4 §3 and Sagekin v1.4 §11. Body, face, hair and skin details fall under biological, and clothing, markings and presentation fall under presentation. It's worth using this split when the one merged list is written for the creator UI.

* **MetaHuman isn't assumed (v1.5 §1).** The main plan tab's race-models table still lists Fenn (and Aelari, Vael, Halvren) as "Start from: MetaHuman". Under v1.5, that's a candidate to test, not a decision. Resolved September 30: the main plan table now lists candidate technical foundations only, and the skeleton strategy stays open.
* **The game uses one human animation set today (v1.5 §3–4).** Every race currently plays the same retargeted human clips at uniform scale. Resolved September 30: the main plan now labels this CURRENT IMPLEMENTATION (a prototype placeholder), separate from the TARGET DESIGN REQUIREMENT for per-race validation, with no refactor now.

# Audit: Skarn Character Customization v1.5 (first-pass complete)

Auditor: Claude. These are notes to check, not changes. Nothing here overrides the spec in `races/02-skarn.md`; Tyler decides what, if anything, changes.

## Open notes

- **Matches the brief.** The 208 cm reference is 1.20× the Marchfolk 173 cm, which matches the brief's Skarn height reference.
- **Breath trait.** The game already gives Skarn 1.5× breath, so §9 matches what's built. Nothing changes.
- **Game scale.** The game currently draws Skarn at 1.12× Marchfolk scale, a placeholder that is smaller than the 1.20× reference. It stays until the specs are implemented.
- **Game description text.** Today's in-game Skarn description says they "trust muscle and the old spirits over books". That ties culture to personality, which §18 of the brief avoids. The wording could be revisited when the race text is rewritten.
- **Existing class limits.** The game already has EverQuest-style race and class limits: Skarn can only be Vanguard, Veilrunner or Spiritcaller. The Decision Register lists this as open, so it's worth deciding whether it stays.

* **Weight as a slider (v1.1 §7).** The master brief (§3, individual layer) lists "Weight" as a body control. v1.1 proposes that weight is derived, not set. v1.1 is logged as a proposed universal principle awaiting confirmation. Once confirmed, the brief's "Weight" entry would read as the body-fat and composition controls.

- **Two kinds of preset (v1.3 §8).** Presentation presets would sit beside the anatomical presets from the brief and Marchfolk v1.4. The creator flow (Race → Preset → Customize) would need to decide whether players pick them separately, for example a body preset plus a look preset.
- **Culture in the game today (v1.3 §9).** The current in-game race text bakes culture into race, for example Skarn are "folk of the frozen north". That's fine as lore for now. If culture becomes its own choice, the race text and starting cities will need splitting.

* **Randomization overlap (v1.4 §3).** The brief's §13 already lists the randomize options: everything, face, body, hair, appearance, clothing, and scars and tattoos. v1.4 renames and extends that set with skin details, markings and presentation. The two lists should be merged into one when the creator UI is designed.
* **Preset count.** Marchfolk has 6 preset themes (v1.4) and Skarn has 8. That's fine, but worth deciding whether each race should have a similar number.

- **The game today uses uniform scaling (v1.5 §2, §5).** Each race is currently drawn by uniformly scaling the one mannequin (Skarn at 1.12×), and held weapons scale with the body. Both are placeholders that v1.5 rules out for the final system: no uniform scaling, and weapons keep their true size. Nothing changes now. This is a known gap for the technical review.
- **The game today has one camera and collision size (v1.5 §3–4).** The capsule, camera height and melee reach currently follow the uniform scale. These are exactly the questions v1.5 leaves open.

# Audit: Aelari Character Customization v1.5 (first-pass complete)

Auditor: Claude. These are notes to check, not changes. Nothing here overrides the spec in `specs/aelari/AELARI_V1.md`; Tyler decides what, if anything, changes.

## Open notes

- **Matches the brief.** The 190 cm reference is 1.10× Marchfolk's 173 cm, exactly the brief's Aelari height (§16.5).
- **Game scale (CURRENT IMPLEMENTATION).** The game draws Aelari at 1.02×. That's a placeholder under the audit (gap 5), not design data.
- **In-game description (audit gap 9).** Today's text reads "Proud elves of the white towers. Deeply wise and gifted in magic, and they rarely let anyone forget it." It states pride and wisdom as racial facts, which §13 and §14 rule out as biology. It goes into the race-description rewrite and may survive as reputation.
- **Racial stats (audit gap 7).** Aelari currently get Wisdom 95 and Intelligence 92 and the lowest Strength (55). Like Sagekin, these echo culture and reputation, and they belong in the Race → Biology → Gameplay Attributes Review.
- **Class limits (audit gap 8).** Aelari are currently limited to Lightkeeper, Oathsworn, Spellwright, Elementalist and Mindweaver. They stay open in the register.

* **Frame is now defined as skeletal (v1.1 §7).** This is the first spec to spell out that frame changes the actual skeleton (clavicle, ribcage and pelvic breadth, joints). It fits amendment v0.1 and sharpens audit gap 1: today's Manny and Quinn frame switch changes the whole body type, not just skeletal breadth.
* **Pelvis shape is open again.** Like Fenn v1.1 §4, the exact Aelari pelvis awaits prototyping. Both are logged together in the register.

- **Hair color data (v1.3 §12).** Keeping "naturally silver" separate from "gray with age" means the appearance record needs natural hair color and an age-graying amount as two values, not one final color. This feeds the future appearance-data schema (audit gap 2).
- **Old description resolved (v1.3 §17).** The in-game Aelari text is now formally reinterpreted as civilization and reputation, covered by the audit's race-description rewrite (gap 9).

* **Presentation preset names changed (v1.4 §4).** v1.3 §24 listed Artisan Practical, Arcane Institutional, Military Formal and Rural/Provincial. v1.4 lists Artisan, Institutional Practical, Military and Provincial. v1.4 is treated as current, and the register entry is updated.
* **Randomize groups extended (v1.4 §10).** Ears and natural appearance are now their own randomize groups, the first spec to split them out. They join the biological side of the Fenn v1.4 §12 split.

# Audit: Vael Character Customization v1.5 (first pass complete)

Auditor: Claude. These are notes to check, not changes. Nothing here overrides the spec in `specs/vael/VAEL_V1.md`; Tyler decides what, if anything, changes.

## Open notes

- **Height versus the brief.** The brief's §16.6 Vael reference is about 1.05× Marchfolk (about 182 cm). The new 178 cm reference is about 1.03×. The spec is newer and treated as current. It also puts Vael slightly below Fenn (181 cm), which fits "more compact".
- **Mass versus the brief.** The brief lists Vael mass at about 0.90×, the same as Aelari. A deeper ribcage and more joint presence may put Vael somewhat heavier than Aelari at equal height. Under the proposed derived-mass rule (Skarn v1.1 §7), that falls out of the anatomy and needs no separate decision.
- **In-game description (audit gap 9).** Today's text reads "Cunning, ambitious and sharp-minded, distrusted on the surface, and they like it that way." That states personality as a racial trait, which §1 rules out as biology. It goes into the race-description rewrite and may survive as reputation.
- **Racial stats (audit gap 7).** Vael currently get Intelligence 99, the second highest after Sagekin. That echoes reputation, and it belongs in the Race → Biology → Gameplay Attributes Review.
- **Class limits (audit gap 8).** Vael are limited to eight classes, including Dreadblade and Bonebinder. That stays open in the register. Pairing Vael with the darker classes could read as "biologically sinister", which §1 rejects, so it's worth checking during that review.
- **Game scale.** The game draws Vael at 0.95×, a placeholder (audit gap 5).
- **Low-light vision.** No race has night vision in the game yet, so the open question costs nothing now. It pairs with the open Fenn low-light question in the register.

* **Palette matches the brief (v1.3 §1).** The color families match the master brief's §16.6 Vael direction and the direction Fenn v1.3 §3 kept, so nothing conflicts.
* **Lighting invariance and the lighting work in progress (v1.3 §6–7).** The creator needs a neutral lighting setup to judge skin. The overworld currently reads bright and hazy (noted in the terrain work), so a separate neutral creator lighting rig will matter for every race, not just Vael.
* **Old description resolved (v1.3 §21).** "Cunning, ambitious, distrusted on the surface" is now formally culture, history or individual possibility, covered by audit gap 9.

- **Co-op makes reproducible generation a real requirement (v1.4 §16).** It says "multiplayer consistency if applicable," and Wayfarer is a co-op listen server, so both players must see the same generated NPCs and characters. That makes it a requirement, with no implementation chosen.
- **Randomization versus the current game (v1.4 §7–13).** The current appearance record (frame, height, primary and accent colors, finish) has no population distributions, locks or strength levels. This is the known audit gap, so nothing changes now.

* **Networked appearance sync applies (v1.5 §30).** The spec lists networking as "if applicable," and it is, since Wayfarer is co-op. The current `FWayfarerAppearance` record already replicates, so this is about what the eventual richer appearance data needs, not a present bug.
* **The Vael description in game (v1.5 §29).** The in-game race text, 0.95 scale, Int-leaning attributes and allowed classes all stay as prototype. Racial attributes and class restrictions are in the open list.

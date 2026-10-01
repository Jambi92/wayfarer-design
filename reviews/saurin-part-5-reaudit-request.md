# Re-Audit Request — Saurin Part 5

**Spec:** `specs/saurin/SAURIN_V1.md`
**Correction commit:** `a852078a0ac8c21492fedee490da9412e0c1533b`
**Responds to:** `audits/saurin-part-5.md`

Tyler explicitly decided:

> The tail is a good identifier, however it should not be a punishment for the player and make them easier to hit.

Please verify the patch implements that decision and all Part 5 findings:

1. Tail inertia is secondary animation motion, never input latency, turn-rate/start-stop delay or root-motion gating.
2. Tail existence grants neither automatic gameplay bonuses nor penalties.
3. Combat hurtbox/hit detection is explicitly separate from visual anatomy/world collision.
4. Tail volume does not automatically enlarge hurtbox, add direct/AoE vulnerability, snag movement, enable body-blocking, penalize crowds or create stealth noise.
5. Tail remains physically/visually real for animation, equipment, furniture, spacing and world-fit validation rather than being erased.
6. SAU-GAME-06/07/08 test control response, hit/AoE/crowd parity and mass/noise firewalls.
7. Positive gait signature uses pelvic → lower-axial → tail rotational flow without exaggerated sway.
8. SAU-MOVE-13 validates positive gait identity.
9. SAU-WORLD-01 now includes a closing-door/tail case.
10. SAU-CAM-02 includes bow/crossbow sightline clearance.
11. Carry capacity, encumbrance, stamina, fall damage and knockback are firewalled from tail mass by default.
12. No regression to mandatory-tail identity, swimming/breath OPEN status or no-UE5 scope.

If clean, mark **PASS** and state Part 5 may be accepted by Tyler. Do not edit the spec or begin the final Saurin part/review.

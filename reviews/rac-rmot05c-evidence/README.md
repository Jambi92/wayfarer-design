# RAC RM-OT-05C — Grask / Gorrund base-surface candidate evidence

These are non-canon diagnostics for `reviews/claude-rac-rm-ot-05c-grask-gorrund-base-surface-candidate-gate.md`. Every candidate is **PENDING AUTHOR / NOT ACCEPTED**. This is an author candidate gate, not a promotion.

## Route

The skeleton is the accepted RM-OT-05B skeleton route: the 05A architecture plus the 05B knee / residual corrections and the Narrow holds (`reviews/rac-rmot05b-evidence/cfg_final.json`). The 05B surface stage is **not** used.

Build order:

1. accepted skeleton;
2. 05A architecture;
3. the 05C race base-surface organization (`tools/rac/w1/race_base.py`, `organize()`);
4. composition amount;
5. surface.

The organization is applied to every composition state's composed surface: the reference, every grid body that feeds the composition-infimum bony envelope, and the low-composition states. The spec rides in the skeleton's meta. The raw skeleton (`-LEAN`) is never rewritten.

A skeleton guard keeps the bony readings of the accepted route:

- outward-normal clamp;
- horizontal-section clamp;
- exact restoration of composition states that were already inside the skeleton.

## Contents

| Path | What |
|---|---|
| `candidates.json` | the six candidate specs (Grask A / B / C, Gorrund A / B / C) |
| `sheets/c_GR_*`, `sheets/c_GO_*` | candidate sheets. Grask at 218 cm, Gorrund at 230.9 cm. Each sheet includes Skarn at matched height, the Marchfolk reference control and the provisional 05B body. Views: front / front ¾ / profile / rear ¾ in neutral grey, plus front / profile in pure silhouette. All bodies are shown body only. |
| `sheets/c_GR_low_*`, `sheets/c_GO_low_*` | low-composition diagnostic (muscle 0 / weight 0.5) of every candidate, with the Skarn and 05B low states; grey and silhouette |
| `sheets/c_GR_frames_*`, `sheets/c_GO_frames_*` | Narrow / reference / Broad frame diagnostic of every candidate |
| `sheets/c_GR_229_*` | Grask matched-height comparison at 229 cm against Skarn 229 |
| `sheets/c_218_*`, `sheets/c_229_*` | close architecture strips: shoulder, thorax, pelvis, knee, elbow, hand, foot and ankle. Grask is at 218; Gorrund is at 230.9 against Skarn 229. Each tile is centred on that body's own joint. |
| `blind/` | the blind read (see below) |
| `guards/guard_all.json` | minimal-guard results for all 27 candidate bodies (§8) |
| `construction/` | build records, skin measurements and composition-infimum envelopes of every candidate body |
| `search/` | the search history: specs `s1`–`s15` with their generators `mk*.py`, combined preview sheets `cmb_*` and the uninformed probe `blindq_q9` |

### Blind read files

- `blind_R_grey.jpg` and `blind_R_sil.jpg`: the 20-body set.
- `key_C05.json`: the key, never shown to the scorers.
- `blind_results.json`: the gate run on the delivered bodies.
- Earlier runs: `*_run1_preguard`, made before the outward-normal guard, and `*_run2`, made before inside-state restoration.

## Drivers

All drivers are in `tools/rac/w1/rmot05c_drivers/`:

| Driver | Purpose |
|---|---|
| `c_build.py` | candidate builds |
| `c_package.py` | the sheets |
| `c_blind.py` | the blind set |
| `c_guard.py` | the minimal guards |
| `c_evidence.py` | builds this directory and the manifest entries |
| `c_preview.py`, `c_try.py`, `c_lean.py`, `c_sx.py`, `c_blindq.py` | search tools |

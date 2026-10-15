# RM-OT-05Z §6 — dry-run preparation for candidate 03 (NO submission authorized)

This file prepares the dry run only. **No paid submission is authorized by this file or by the image PASS.**

## Job metadata

| Item | Value |
|---|---|
| Source image | Candidate 03, SHA-256 `49b72dfca83d9e2fb58a8560153d3f15de88824d17f95b3c2f563ec26f9c27ba` (1,769,740 bytes, 1024 × 1536) |
| Pipeline input path | `E:\Wayfarer-Rodin\Source-Images\Wayfarer Gorrund Neutral Character Reference Sheet.png`. Claude copied the image there, byte-identical, on 2026-10-15. The pipeline's `C:\Users\Tyler\Wayfarer-Rodin\Source-Images` folder resolves to the same location through its symlink (verified: the file is listed there at 1,769,740 bytes). |
| AssetName | `Gorrund-Neutral` |
| Duplicate guard | Last checked 2026-10-15: no `Jobs\Gorrund-Neutral*` record and no `Source-Masters\Gorrund-Neutral\` folder exist. |
| Tier | Gen-2.5-High, the pipeline's production tier. It is not changed. |
| Input mode | One image (the pipeline sends a single image). |
| Estimated cost | About **0.5 credits** for one job, based on the Vael-Female job record (`"consumed": 0.5`). This is an estimate; the balance is not visible from here. |
| Expected output | `Source-Masters\Gorrund-Neutral\Gorrund-Neutral.glb` (immutable), with its SHA-256 in `Jobs\Gorrund-Neutral-manifest.json` |

## Commands

Run these in Tyler's PowerShell, from `C:\Users\Tyler\Wayfarer-Rodin`. This session cannot run commands on the PC.

**1. Dry run.** No credits, no approval needed:

```
.\Scripts\wayfarer-rodin.ps1 -ImagePath "Source-Images\Wayfarer Gorrund Neutral Character Reference Sheet.png" -AssetName "Gorrund-Neutral"
```

**2. Submit.** This **spends credits**. Run it **only after Tyler explicitly approves this exact image and AssetName immediately beforehand**:

```
.\Scripts\wayfarer-rodin.ps1 -ImagePath "Source-Images\Wayfarer Gorrund Neutral Character Reference Sheet.png" -AssetName "Gorrund-Neutral" -Submit
```

If anything fails, **do not resubmit**. Use `-Resume` only for recovery, as described in the pipeline `CLAUDE.md`.

## After generation

Run `z_single_body_gate.py` on the new GLB before anything else (05Z §7):
- the exact hash is recorded;
- the file must contain exactly one body;
- it must not contain duplicate front, side or back bodies;
- it must not contain hidden merged shells.

Only after that gate passes does the whole-source anatomy review start. The **first question** for that review is whether the body reads as Gorrund from its deep ribcage and robust pelvis and joints, rather than as a large, heavy human.

**State:** STOP AT THE PAID-SUBMIT GATE.

## Approval record

**2026-10-15, 12:32 PT.** Tyler, in chat: "I approve the Gorrund-Neutral Rodin submission."

That approval covers this exact image (`49b72dfc…`) and this AssetName (`Gorrund-Neutral`) only.

**Claude did not run the submission.** This session has no shell on the PC, and `RODIN_API_KEY` exists only in Tyler's Windows user environment. Terminal apps cannot be typed into through remote computer control. The dry run and the `-Submit` are therefore run by Tyler in PowerShell.

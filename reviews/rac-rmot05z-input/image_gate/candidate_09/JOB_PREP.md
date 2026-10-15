# Job preparation — Gorrund-Neutral-C counter-bias calibration (no submission authorized)

| Item | Value |
|---|---|
| Image | Candidate 09, SHA-256 `34169ee847af79118c14343db4cf3c792abe2f4fe56ba2943395eac89e10346e` (1,769,056 bytes) |
| AssetName | `Gorrund-Neutral-C` |
| Paid generations allowed | **1** (05Z3 §2). If the result fails Q1/Q2 for heroic musculature, the outcome is RODIN GORRUND ARM ROUTE RETIRED. **No retry.** |
| Duplicate guard | Checked 2026-10-15: no `E:\Wayfarer-Rodin\Source-Masters\Gorrund-Neutral-C\` exists. The `C:\…\Jobs` folder is not reachable from this session; Tyler should check it before running the pipeline. |
| Pipeline copy of the image | Placed byte-identical at `E:\Wayfarer-Rodin\Source-Images\Wayfarer Gorrund NeutralC Character Reference Sheet.png` |
| Approval needed | Tyler's explicit approval in chat, immediately beforehand, naming: (1) candidate 09, (2) `Gorrund-Neutral-C`, (3) the tier and settings |

## Before any website run (05Z3 §7)

Fill in `../RODIN_SETTINGS_RECORD_05Z3.md`, or paste a screenshot of the settings panel in chat, covering:
- tier / model;
- geometry quality;
- detail;
- smoothing / surface mode;
- polygon / mesh setting;
- symmetry;
- prompt field;
- any other visible option.

Choose the **smoothest, least anatomy-emphasizing** option that is still usable for production. Write **NOT AVAILABLE** for any setting the site does not offer.

## Option B — PC pipeline (Gen-2.5-High, about 0.5 credits, estimated)

Run from `C:\Users\Tyler\Wayfarer-Rodin`. First the dry run, which costs no credits:

```
.\Scripts\wayfarer-rodin.ps1 -ImagePath "Source-Images\Wayfarer Gorrund NeutralC Character Reference Sheet.png" -AssetName "Gorrund-Neutral-C"
```

Then, **only after approval**, the same command with `-Submit`. If it fails, do not resubmit; `-Resume` is for recovery only.

## After generation (05Z3 §8)

1. Capture the hash.
2. Run the single-body gate.
3. Run the Q1–Q4 review.
4. Compare body-only against A (`aaeee37b…`) and B (`895d8854…`).

**Pass requires all of:**
- Q1 = YES;
- Q2 = YES;
- less heroic muscle than B;
- no obesity compensation.

**STATE: STOP AT PAID-SUBMIT GATE.**

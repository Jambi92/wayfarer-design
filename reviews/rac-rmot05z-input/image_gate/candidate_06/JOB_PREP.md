# Job preparation — candidate 06 (no submission authorized)

| Item | Value |
|---|---|
| Image | Candidate 06, SHA-256 `8304214895837e768c9882e51bb29e7da0a258fc835272f10693f3c00f6d193d` (the 13:26 chat attachment) |
| AssetName | `Gorrund-Neutral-B`. The earlier `Gorrund-Neutral` (`aaeee37b…`, from candidate 03) stays as failed-source evidence. |
| Approval needed | Tyler's explicit approval, immediately beforehand, naming: (1) this image, (2) `Gorrund-Neutral-B`, (3) the Rodin tier and settings |

## Option A — Rodin website (as used for `aaeee37b…`)

Upload **only** candidate 06 as a single image. Before you press generate, record:
- the **tier / model**;
- the **quality / detail / smoothing** settings;
- any other visible option, such as polygon count, symmetry or a prompt.

Choose a smoother, lower-detail surface if the site offers that option. Then download the GLB and attach it in chat.

## Option B — PC pipeline

The pipeline input folder currently holds **candidate 03** under the Gorrund-Neutral name. To use the pipeline, Claude first saves candidate 06 as
`E:\Wayfarer-Rodin\Source-Images\Wayfarer Gorrund NeutralB Character Reference Sheet.png`.
Tyler then runs these at home:

```
.\Scripts\wayfarer-rodin.ps1 -ImagePath "Source-Images\Wayfarer Gorrund NeutralB Character Reference Sheet.png" -AssetName "Gorrund-Neutral-B"
```

The command above is the dry run. After explicit approval, run the same command with `-Submit` added. It uses Gen-2.5-High and costs about 0.5 credits (estimate).

## After generation (05Z2 §7)

1. Capture the exact hash.
2. Run `z_single_body_gate.py`.
3. Run the Q1–Q4 review.
4. Compare directly, body only, with `aaeee37b…`.

Success requires **Q1 = YES** and **Q2 = YES**.

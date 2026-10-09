# RAC W2I6 — Saurin W2I4 canonicalization / W2I final closure evidence

Order `reviews/chatgpt-rac-w2i6-saurin-canonicalize-w2i4-order.md`; report `reviews/claude-rac-w2i6-saurin-canonicalization-final-closure-report.md`.

| File | Driver (`tools/rac/w1/w2i6_drivers/`) | Content |
|---|---|---|
| `canon6.json` | `sa_canon6.py` | the canonical W2 file set (promoted exact W2I4 candidate arrays) with SHA-256, array hashes, export record, W1 provenance hashes |
| `verify6.json` | `sa_verify6.py` | verification: on-disk hashes, identity with the audited W2I4 candidate, shipped-rebuild reproduction, W2I5-not-promoted proof, SA-M188 / SA-F188 measurements vs W2I4, W1 provenance, W1 tool-chain git diff |
| `pc_deploy6.json` | (read-back) | hashes of the W2 and W1 files read back from `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/out` after deployment |

Tool chain: `tools/rodin/w2/` (`ref_metrics_w2.json`, `axis_w2.npy`, `g7geo_w2_points.json`, `lbase_w2_stations.json`, `s263_w2.json`) written by `sa_toolchain6.py`. W1 tool chain (`tools/rodin/gate1`, `gate8`, `creator-biology`, `female`) unchanged.

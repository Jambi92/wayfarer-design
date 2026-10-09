# RAC W2I4 — Saurin final asset finish / canonicalization-prep evidence

Order `reviews/chatgpt-rac-w2i4-saurin-final-asset-order.md`; gate `reviews/claude-rac-w2i4-saurin-final-asset-gate.md`. FINAL CANDIDATE COPIES; the frozen SA-M / SA-F, the tool chain and canon are unchanged.

| File | Driver (`tools/rac/w1/w2i4_drivers/`) | Content |
|---|---|---|
| `bodies_F.json` | `sa_w2i4_build.py full` | full W2I body list built with the final asset route (`sa_finish.build_f` = W2I3 L1 + F2 rebuild + W2I4 finish delta), W2I measure + J-2 limbs + ledger |
| `compare_F.json`, `saeval_F.json` | W2I `sa_compare.py`, `sa_eval.py` (unchanged; no extra-body file) | cross-race and internal suites |
| `eval_F.json` | W2I2 `sa_w2i2_eval.py` (unchanged) | limb / budget rows vs the frozen re-run (`rac-w2i2-sa-evidence/bodies_AS.json`) |
| `tailcap_F.json` | `run_tailcap_fin.py` (W1 `sa_tailcap2.py`, `TGT=rsi119`) | same-state tail caps on the final asset |
| `fieldcheck.json` | `sa_fieldcheck.py` | scale-field correlation-length anisotropy (frozen control / carried / regenerated) and seed spacing |
| `quality.json` | `sa_quality.py` | strain, flipped faces (62-body census), surfaced topology, thigh relief metric, finish-delta magnitudes |
| `thigh_relief.json` | `sa_thighrelief.py` | thigh fine-relief correlation length by sector (frozen / W2I3 / W2I4) |
| `tailcap_R_control.json` | `run_tailcap_fin.py` with `FINISH=0` | tail-coupling control on the W2I3 rebuild (isolates the finish from the rebuild) |
| `surface_info.json` | `sa_surface.py` | scale-surface regeneration record |
| `canon_prep.json` | `sa_canon_prep.py` | exact candidate files and SHA-256 (scratch stage; nothing overwritten) |
| `sheets/*.jpg` | `sa_w2i4_render.py` | final SA-M188 / SA-F188, family, W2I3 vs W2I4, thigh relief and scale field before / after |
| `tables.md` | `../../tools/rac/w1/gen_w2i4_docs.py` | generated tables |

Finish: `sa_finish.py` (zone fairing, native-scale thigh fine-relief re-model, measurement holds, fold guards). Surface: `sa_surface.py` + `g7surfc_moved.py` (accepted gate-1 `g7surfc.py` unchanged; carried region fields; saved seeds). Seed-recovery attempt: `sa_seeds.py`.

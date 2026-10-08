# RAC S7 normalization AS RUN (scratch paths = this session's working directories; kept for provenance)
# 1. normalized SKP copies (no body rebuilt): W1i skeletal base, then every candidate / frame / W2 grid SKP directory
bash /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/s7n/base.sh        # s7_normalize.py -> s7n/w1i_base (+ CG/DU/PK slot aliases and SKB = SKB229 alias copied after)
bash /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/s7n/all.sh         # s7_normalize.py for 58 SKP directories
# 2. evaluations re-run unchanged (remap_run.py): base = reproduction control, norm = normalized inputs
bash /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/s7n/evals.sh base; bash /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/s7n/evals.sh norm
# 3. comparison
python3 s7n_drivers/compare.py /home/claude/wayfarer-design /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/s7n/RB $(cat /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/s7n/files.txt)
python3 s7n_drivers/status_diff.py /home/claude/wayfarer-design /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/s7n/RN reviews/rac-s7n-evidence/status_diff.json $(cat /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/s7n/files.txt)

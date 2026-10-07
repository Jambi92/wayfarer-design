# RAC W1r AS RUN: Cogling composition variants on the W1r candidate CGJ7 (generator macros), then measurements
cd /home/claude/wayfarer-design/tools/rac/w1; D=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1r/comp; mkdir -p $D
for a in "CG-LOWMUS 0.0 0.5" "CG-HIMUS 1.0 0.5" "CG-HIFAT 0.5 1.0" "CG-HIBOTH 1.0 1.0" "CG-LOW 0.25 0.25"; do set -- $a
  echo "{\"muscle\": $2, \"weight\": $3}" > $D/$1.ov.json; python3 build_variant.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1r/probe/CGJ7_build.json $D/$1.ov.json $D $1 && python3 run_candidate.py $D $1 /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1f/final/MF-M-R_rest.npz; done
echo COMP_DONE

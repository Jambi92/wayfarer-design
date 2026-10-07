# RAC W1t AS RUN: Durrim composition variants on DU-NAT as built (generator macros), then measurements
cd /home/claude/wayfarer-design/tools/rac/w1; D=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1t/comp; mkdir -p $D
for a in "DU-LOWMUS 0.0 0.5" "DU-HIMUS 1.0 0.5" "DU-HIFAT 0.5 1.0" "DU-HIBOTH 1.0 1.0" "DU-LOW 0.25 0.25"; do set -- $a
  echo "{\"muscle\": $2, \"weight\": $3}" > $D/$1.ov.json; python3 build_variant.py /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1f/final/DU-NAT_build.json $D/$1.ov.json $D $1 && python3 run_candidate.py $D $1 /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1f/final/MF-M-R_rest.npz; done
echo COMP_DONE

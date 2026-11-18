N=c1-M208-B@0.75; D=/tmp/claude-0/rp6/adapt3/$N/it2; BD=/tmp/claude-0/rp6/blend_bodies
cd /home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001; export SA_W=/tmp/claude-0/rp5clean OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 SWEEP_SET=all SWEEP_STEP_OTHER=0.125
if [ ! -f $D/SW_$N.json ]; then t=$(date +%s)
  for i in 0 1; do [ -f $D/SW_$N.s${i}of2.json ] || SWEEP_SHARD=$i/2 nice python3 sa6_bake_sweep.py $N $BD $D $D >> $D/../log_$N.txt 2>&1 & done; wait
  python3 sa6_bake_sweep_merge.py $N $D 2 >> $D/../log_$N.txt 2>&1 && rm -f $D/SW_$N.unsharded_partial.json
  echo "{\"body\": \"$N\", \"stage\": \"sweep_2shards_resumed\", \"host\": \"cloud\", \"wall_s\": $(( $(date +%s) - t )), \"rc\": $?}" >> /tmp/claude-0/rp6/adapt3/timings.jsonl; fi
/tmp/claude-0/rp6/adapt3/refit.sh $N /tmp/claude-0/rp6/adapt2/$N/it1/BK_$N.json
/tmp/claude-0/rp6/adapt3/dense.sh $N ankle_plantar25_xpos,ankle_dorsi25_xpos,foot_pushoff_xpos,foot_curl_xpos,ankle_plantar25_xneg,ankle_dorsi25_xneg,foot_pushoff_xneg,foot_curl_xneg,jaw_open_32,jaw32_head_pitch_up
echo Q3DONE

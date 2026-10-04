cd /tmp/claude-0/rodin/g8
for j in jobE_minimal_ridges jobE_low_hornlets jobE_swept_paired jobE_mixed_asym jobE_crest jobDf jobDh jobC jobA jobB; do
  python3 g8render.py $j.json > log_$j.txt 2>&1; echo "RUN $j $(grep -c JOB log_$j.txt) $(date +%H:%M)" >> g8.log
done
echo ALLDONE >> g8.log

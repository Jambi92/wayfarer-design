cd /tmp/claude-0/rodin/g8
for j in jobC2 jobA jobB; do python3 g8render.py $j.json > log2_$j.txt 2>&1; echo "RERUN $j $(grep -c JOB log2_$j.txt) $(date +%H:%M)" >> g8.log; done
python3 g8metrics.py > metrics.log 2>&1; echo "RERUNDONE $(date +%H:%M)" >> g8.log

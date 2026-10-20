#!/bin/bash
# runfeats.sh LIST IN PREFIX : chain feat.sh over a feature list
IN=$2; k=0
while IFS='|' read nm c rs er ex; do
  k=$((k+1)); OUT=/tmp/claude-0/$3$k.npz
  if [ "$ex" == "T" ]; then R=$(./feat.sh $IN $OUT "$c" "$rs" $er /tmp/claude-0/dmT_faces.npy 1 2>&1 | tail -3); else R=$(./feat.sh $IN $OUT "$c" "$rs" $er 2>&1 | tail -3); fi
  echo "== $nm"; echo "$R" | cut -c1-400
  if [ -f $OUT ]; then IN=$OUT; echo "STEP $nm $c $(echo "$R" | grep ACCEPT)" >> /tmp/claude-0/steps_$3.log; fi
done < $1; echo LAST $IN

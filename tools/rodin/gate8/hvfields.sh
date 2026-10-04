cd /tmp/claude-0/rodin/g8; G=/tmp/claude-0/rodin/g1
for V in baseline minimal_ridges low_hornlets swept_paired crest mixed_asym; do U=$V; [ "$V" = crest ] && U=crest_c
 python3 g8fields.py $G/hvu_$U.npz $G/hvrc_$V.npz $G/hvsc_$V.npz fld_hv_$V.npz > fld_hv_$V.log 2>&1; echo HVF $V >> g8.log; done

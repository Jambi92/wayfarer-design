# linfix.sh MESH : linearize PN midpoints near self-intersections until 0 pairs
for it in 1 2 3 4; do
PR=$(/home/claude/stc/bin/python3 /tmp/claude-0/rp2/sxq.py $1 /tmp/np.npy 2>/dev/null| head -1 | awk '{print $2}'); echo "pairs $PR"; [ "$PR" = "0" ] && break
python3 - $1 <<'EOF2'
import numpy as np,sys
d=dict(np.load(sys.argv[1])); pr=np.load('/tmp/np.npy'); n0=d['parent_vertex'].sum(); F=d['Q']; m=np.zeros(len(d['V']),bool); m[np.unique(F[pr.ravel()])]=True
e=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]
for _ in range(3): s=np.zeros(len(m),bool); s[e[m[e[:,1]],0]]=True; m|=s
new=np.nonzero(m[n0:])[0]; d['V'][n0+new]=d['lin_mid'][new]; np.savez(sys.argv[1],**d)
EOF2
done

#!/bin/bash
# clus.sh MESH.npz zmin zmax xabsmin
/home/claude/stc/bin/python3 sxpairs.py -- $1 2>&1 | grep PAIR | awk -v a=$2 -v b=$3 -v c=$4 '{gsub(/[\[\],]/," "); if ($6>a && $6<b && ($4>c || $4<-c)) print $4,$5,$6,$7,$8,$9}' | python3 -c "
import sys,numpy as np
P=np.array([[float(x) for x in l.split()] for l in sys.stdin])
if len(P)==0: print('none'); sys.exit()
from scipy.cluster.hierarchy import fcluster, linkage
Q=(P[:,:3]+P[:,3:])/2
L=fcluster(linkage(Q,'single'),2.0,'distance') if len(Q)>1 else np.array([1])
for k in np.unique(L): m=L==k; print(k,m.sum(),Q[m].mean(0).round(1), Q[m].min(0).round(1), Q[m].max(0).round(1))
"

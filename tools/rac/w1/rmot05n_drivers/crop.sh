#!/bin/bash
# crop.sh OBJ OUT xlo xhi zlo zhi : close renders of a box of the body (x recentred)
D=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad
python3 - "$@" <<'PY'
import sys, trimesh, numpy as np
m=trimesh.load(sys.argv[1],process=False); V=m.vertices; x0,x1,z0,z1=map(float,sys.argv[3:7])
k=(V[:,0]>=x0)&(V[:,0]<=x1)&(V[:,2]>=z0)&(V[:,2]<=z1); f=m.faces[k[m.faces].all(1)]
vi=np.unique(f); mp=-np.ones(len(V),int); mp[vi]=np.arange(len(vi)); W=V[vi].copy(); W[:,0]-=(x0+x1)/2
trimesh.Trimesh(W,mp[f],process=False).export(sys.argv[2]+'.crop.obj')
PY
python3 $D/close.py $2.crop.obj $2 $5 $6 >/dev/null 2>&1

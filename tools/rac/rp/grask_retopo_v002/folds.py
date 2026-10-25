# folds.py PROD.npz : folded-face audit -- edges whose two face normals disagree by > 120 deg (dihedral fold), and faces
# facing against the nearest source normal
import numpy as np, sys, collections
sys.path.insert(0,'/tmp/claude-0/rt'); from common import PARTS
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']
n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]); n/=np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]
E=np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]); F=np.tile(np.arange(len(Q)),4)
Es=np.sort(E,1); o=np.lexsort((Es[:,1],Es[:,0])); Es=Es[o]; F=F[o]
f0=F[0::2]; f1=F[1::2]; dot=(n[f0]*n[f1]).sum(1)
for th in (-0.5,0.0):
    m=dot<th; print('edges with dihedral normal dot <',th,':',int(m.sum()), collections.Counter([PARTS[FP[f]] for f in f0[m]]).most_common(8))

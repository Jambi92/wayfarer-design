# loopcut.py CAGE COL RING.json JPOS.json OUT : insert one edge loop across the face ring; JPOS = {"a,b":[x,y,z]} per rung (default midpoint)
import numpy as np, sys, json
z=np.load(sys.argv[1]); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(sys.argv[2]).tolist()
R=json.load(open(sys.argv[3])); J=json.load(open(sys.argv[4])); out=sys.argv[5]
jid={}
for a,b in R['rungs'][:-1]:
    k='%d,%d'%(a,b); p=J.get(k,((np.array(V[a])+np.array(V[b]))/2).tolist())
    V.append(list(p)); cc.append(cc[a]); jid[frozenset((a,b))]=len(V)-1
newF=[]
for fi in R['faces']:
    q=F[fi]; es=[frozenset((q[i],q[(i+1)%4])) for i in range(4)]
    ii=[i for i in range(4) if es[i] in jid]; assert len(ii)==2 and (ii[1]-ii[0])==2, (fi,q)
    i=ii[0]; m1=jid[es[i]]; m2=jid[es[i+2]]
    # q = [q0,q1,q2,q3], cut edges (q_i,q_i+1) and (q_i+2,q_i+3)
    a0,a1,a2,a3=q[i],q[(i+1)%4],q[(i+2)%4],q[(i+3)%4]
    newF.append((fi,[a0,m1,m2,a3])); newF.append((fi,[m1,a1,a2,m2]))
rm=set(R['faces']); F2=[f for k,f in enumerate(F) if k not in rm]+[f for _,f in newF]
Fa=np.full((len(F2),4),-1)
for k,f in enumerate(F2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=np.array(V),F=Fa); np.save(out.replace('.npz','_col.npy'),np.array(cc))
json.dump(dict(removed_faces=sorted(rm),j={'%d,%d'%tuple(sorted(k)):v for k,v in jid.items()}),open(out.replace('.npz','_lc.json'),'w'))
print('V',len(V),'F',len(F2))

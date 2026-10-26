import numpy as np, sys, collections, json
sys.path.insert(0,'/tmp/claude-0/rt'); from common import PARTS
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']
ang=[]
for i in range(4):
    a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
    ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
ang=np.stack(ang,1); el=np.stack([np.linalg.norm(V[Q[:,(i+1)%4]]-V[Q[:,i]],axis=1) for i in range(4)],1)
asp=(el[:,0]+el[:,2])/np.maximum(el[:,1]+el[:,3],1e-12); asp=np.maximum(asp,1/np.maximum(asp,1e-12))
hard=np.nonzero((ang.min(1)<20)|(ang.max(1)>160)|(asp>8))[0]
fc=V[Q].mean(1)
# cluster by connectivity-ish: round 1 cm
cl=collections.defaultdict(list)
for f in hard: cl[(PARTS[FP[f]],)+tuple(np.round(fc[f]).astype(int))].append(f)
rows=[]
for k,fs in sorted(cl.items(),key=lambda x:-len(x[1])):
    fs=np.array(fs); rows.append(dict(part=k[0],centre_cm=list(map(int,k[1:])),n=len(fs),min_angle=round(float(ang[fs].min()),1),max_angle=round(float(ang[fs].max()),1),max_aspect=round(float(asp[fs].max()),1)))
for r in rows[:40]: print(r)
print(len(hard),'hard in',len(rows),'clusters')
json.dump(dict(n=len(hard),clusters=rows),open(sys.argv[2],'w'),indent=1) if len(sys.argv)>2 else None

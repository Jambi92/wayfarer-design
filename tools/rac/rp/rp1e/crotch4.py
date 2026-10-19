# crotch4.py CAGE COL OUT DESIGN.json
# Pelvis-front/crotch sub-cage: rows from the front (rung0 = ring 105.7 front) down the belly front (z-rows) and back
# through the crotch (y-rows) to rung6 (back). Each row: 7 interior points [lA_R, tip_R, lB_R, ctr, lB_L, tip_L, lA_L]
# (lA = thigh-side lip, tip = crease bottom, lB = belly/flap-side lip), ends = thigh chain verts (main rows) or none (sub rows,
# side faces = triangles). rung0 (3 interior) -> first row: fans at the crease tops (637, 613); last row -> rung6: fans at 1267/1264.
import numpy as np, sys, json, collections
cg,colf,out,dj=sys.argv[1:5]; D=json.load(open(dj))
z=np.load(cg); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colf).tolist()
hole=D['hole']; R=D['R']; L=D['L']; r0=D['rung0']; r6=D['rung6']
F=[f for i,f in enumerate(F) if i not in set(hole)]
rows=[]; km=0
for rg in D['rows']:
    ids=[]
    for p,c in zip(rg['pts'],rg['cols']): V.append([float(t) for t in p]); cc.append(int(c)); ids.append(len(V)-1)
    if rg.get('sub'): rows.append([None,ids,None])
    else: rows.append([R[km],ids,L[km]]); km+=1
assert km==len(R)==len(L), (km,len(R))
Fn=[]
def strip(a,b,fans):
    out=[]; j=0
    for i in range(len(a)):
        if i in fans: out.append([a[i],b[j+2],b[j+1],b[j]]); j+=2
        if i<len(a)-1: out.append([a[i],a[i+1],b[j+1],b[j]]); j+=1
    assert j==len(b)-1,(j,len(b)); return out
# front: rung0 interior -> row1 interior, fans at 0 and 2
A_R,A_L=r0[0],r0[-1]
FANS=[0,2] if len(rows[0][1])==7 else [0,1,2]
Fn+=strip(r0[1:-1],rows[0][1],FANS)
Fn.append([A_R,r0[1],rows[0][1][0]]); Fn.append([r0[-2],A_L,rows[0][1][-1]])
if rows[0][0] is not None: raise SystemExit('first row must be sub')
prevR,prevL=A_R,A_L
for k in range(1,len(rows)):
    a,b=rows[k-1][1],rows[k][1]
    Fn+=strip(a,b,[])
    if rows[k][0] is None:
        Fn.append([prevR,a[0],b[0]]); Fn.append([a[-1],prevL,b[-1]])
    else:
        Fn.append([prevR,a[0],b[0],rows[k][0]]); Fn.append([a[-1],prevL,rows[k][2],b[-1]]); prevR,prevL=rows[k][0],rows[k][2]
# back: last row -> rung6
b=rows[-1][1]; Rl,Ll=rows[-1][0],rows[-1][2]
assert Rl is not None
Fn+=[q[::-1] for q in strip(r6[1:-1],b,FANS)]
Fn.append([r6[1],r6[0],Rl,b[0]][::-1]); Fn.append([r6[-1],r6[-2],b[-1],Ll][::-1])
def ok(Fs):
    de=collections.Counter((f[i],f[(i+1)%len(f)]) for f in Fs for i in range(len(f)))
    return all(n==1 for n in de.values()) and all((y,x) in de for (x,y) in de), de
# orient each new face consistently: try global flip, then per-face greedy fix
for flip in (False,True):
    F2=F+([q[::-1] for q in Fn] if flip else Fn); good,de=ok(F2)
    if good: break
if not good:
    # greedy: flip individual patch faces to minimise duplicate directed edges
    Fp=[list(q) for q in Fn]
    for it in range(20):
        changed=False
        for i in range(len(Fp)):
            base=collections.Counter((f[k],f[(k+1)%len(f)]) for f in F+Fp for k in range(len(f)))
            q=Fp[i]; dup=sum(base[(q[k],q[(k+1)%len(q)])]>1 for k in range(len(q)))
            if dup: Fp[i]=q[::-1]; changed=True
        if not changed: break
    F2=F+Fp; good,de=ok(F2)
    if not good:
        bad=[e for e,n in de.items() if n>1]; bnd=[e for e in de if (e[1],e[0]) not in de]; print('dup',bad[:8],'bnd',bnd[:8]); raise SystemExit('orientation failed')
used=sorted(set(i for f in F2 for i in f)); remap={o:n for n,o in enumerate(used)}
V2=np.array([V[i] for i in used]); F3=[[remap[i] for i in f] for f in F2]; cc2=np.array([cc[i] for i in used])
Fa=np.full((len(F3),4),-1)
for k,f in enumerate(F3): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),cc2)
json.dump(dict(design=dj,rows=[[remap[i] for i in ([r[0]] if r[0] is not None else [])+r[1]+([r[2]] if r[2] is not None else [])] for r in rows],
   removed=[i for i in range(len(z['V'])) if i not in remap]),open(out.replace('.npz','_crotch.json'),'w'))
print('V',len(V2),'F',len(F3),'tris',sum(1 for f in F3 if len(f)==3))

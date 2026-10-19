# pocket.py IN.npz OUT.npz FACE "Ox,Oy,Oz" "Tx,Ty,Tz" hu hv [d1f d2f] [ux,uy,uz]
# inset cage face FACE into a 3-ring pocket: rim ring around the opening centre O (plane normal to O-T),
# mid ring at depth d1f*|O-T|, cap ring at d2f*|O-T| (4-vertex cap). hu/hv: rim half-sizes along u (slit long axis) / v.
import numpy as np, sys, shutil
from orient import orient_patch, check
a=sys.argv[1:]; z=np.load(a[0]); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]
cc=np.load(a[0].replace('.npz','_col.npy')).tolist()
k=int(a[2]); O=np.array(eval(a[3])); T=np.array(eval(a[4])); hu,hv=float(a[5]),float(a[6])
d1f=float(a[7]) if len(a)>7 else 0.5; d2f=float(a[8]) if len(a)>8 else 1.2
D=np.linalg.norm(T-O); n=(T-O)/D
u=np.array(eval(a[9])) if len(a)>9 else np.array([0,0,1.0]); u=u-(u@n)*n; u/=np.linalg.norm(u); v=np.cross(n,u)
f=F[k]; assert len(f)==4
Pf=np.array([V[i] for i in f]); c=Pf.mean(0)
offs=[hu*u,hv*v,-hu*u,-hv*v]
# assign rim offsets to face corners by angle (keep cyclic order and orientation)
ang=lambda p:np.arctan2((p-c)@v,(p-c)@u)
fa=np.array([ang(p) for p in Pf]); oa=np.array([np.arctan2(o@v,o@u) for o in offs])
best=None
for sh in range(4):
    for dr in (1,-1):
        idx=[(sh+dr*i)%4 for i in range(4)]
        cost=sum(abs(np.angle(np.exp(1j*(fa[i]-oa[idx[i]])))) for i in range(4))
        if best is None or cost<best[0]: best=(cost,idx)
idx=best[1]
def add(p):
    V.append(np.asarray(p).tolist()); cc.append(cc[f[0]]); return len(V)-1
R1=[add(O+offs[idx[i]]) for i in range(4)]
R2=[add(O+n*D*d1f+0.6*offs[idx[i]]) for i in range(4)]
R3=[add(O+n*D*d2f+0.25*offs[idx[i]]) for i in range(4)]
G=[g for j,g in enumerate(F) if j!=k]
new=[]
for ring_a,ring_b in ((f,R1),(R1,R2),(R2,R3)):
    for i in range(4): new.append([ring_a[i],ring_a[(i+1)%4],ring_b[(i+1)%4],ring_b[i]])
new.append(R3[::-1])
new=orient_patch(G,new); G+=new; d,b=check(G)
if d or b: raise SystemExit('topology dup %d bnd %d'%(d,b))
Fa=np.full((len(G),4),-1)
for j,g in enumerate(G): Fa[j,:len(g)]=g
np.savez_compressed(a[1],V=np.array(V),F=Fa); np.save(a[1].replace('.npz','_col.npy'),np.array(cc))
print('V',len(V),'F',len(G),'rim',R1,'mid',R2,'cap',R3)

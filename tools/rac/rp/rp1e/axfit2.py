"""Axilla junction-on-crease layout (design only). Usage: python3 axfit2.py SIDE CAGE_IN.npz CAGECOL_IN.npy SRC_COL.npy TPREFIX OUT.npz [INSET ITERS DMAX]
J = arm junction ring (arm_rings[-2]); its verts within DMAX of the crease curve are snapped onto the curve (order kept);
arm rings (<= rings[-3]) colour 2; non-ring neighbours of the snapped J verts colour 1 (trunk); movable = e30 axilla set of this
side + ring[-3] + those trunk neighbours; free movable verts are placed INSET cm inside their own colour target, Laplacian relaxed."""
import numpy as np, sys, json, igl
a=sys.argv[1:]; s,cin,colin,scolp,tp,out=a[:6]; INSET=float(a[6]) if len(a)>6 else 0.6; ITERS=int(a[7]) if len(a)>7 else 30; DMAX=float(a[8]) if len(a)>8 else 5.0
sys.argv=['x',s]
exec(open('ring11.py').read().split("if __name__=='__main__':")[0])
from scipy.spatial import cKDTree
z=np.load(cin); V=z['V'].astype(float).copy(); V0=V.copy(); F=z['F']; cc=np.load(colin).copy()
sg=-1 if s=='R' else 1
rings=arm_rings(s); J=list(rings[-2]); armset=set(v for r in rings[:-2] for v in r)
Q=np.load('ccurve_%s.npy'%s); T=cKDTree(Q); d,k=T.query(V[J])
Js=[(v,kk) for v,dd,kk in zip(J,d,k) if dd<DMAX]
# order-preserving: walk J in ring order, keep t monotone along the ring
ts=[kk for v,kk in Js]
print(s,'J snapped',[(int(v),int(kk)) for v,kk in Js])
for v,kk in Js: V[v]=Q[kk]
Jsn=set(v for v,_ in Js)
for r in rings[:-2]:
    for v in r: cc[v]=2
trunk=set()
for v in Jsn:
    for n in adj[v]:
        if n not in armset and n not in set(J): trunk.add(n); cc[n]=1
mv=json.load(open('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/axilla_ui_moves_e30.json'))
P=np.array(list(mv.values())); dd,Mi=cKDTree(V0).query(P); M=set(int(i) for i in Mi if V0[i,0]*sg>0)
M|=set(rings[-3])|trunk
M-=Jsn
print('movable',len(M),'trunk nbrs',sorted(trunk))
TG={c:(lambda t:(t['V'].astype(float),t['F'].astype(np.int64)))(np.load('%s_c%d.npz'%(tp,c))) for c in (1,2)}
free=np.array(sorted(M),int)
def place():
    for c,(TV,TF) in TG.items():
        idx=free[cc[free]==c]
        if not len(idx): continue
        S2,I,C=igl.point_mesh_squared_distance(V[idx],TV,TF)
        T3=TV[TF[I]]; N=np.cross(T3[:,1]-T3[:,0],T3[:,2]-T3[:,0]); N/=np.linalg.norm(N,axis=1)[:,None]
        V[idx]=C-INSET*N
for it in range(ITERS):
    place(); Vn=V.copy()
    for i in free: Vn[i]=0.5*V[i]+0.5*V[list(adj[i])].mean(0)
    V[:]=Vn
place()
np.savez_compressed(out,V=V,F=F); np.save(out.replace('.npz','_col.npy'),cc)
sh=np.linalg.norm(V-V0,axis=1); print('moved >1mm',int((sh>0.1).sum()),'mean shift of moved %.2f max %.2f'%(sh[sh>0.1].mean(),sh.max()))
json.dump(dict(J=[int(v) for v in Jsn],M=[int(i) for i in free]),open(out.replace('.npz','_ax.json'),'w'))

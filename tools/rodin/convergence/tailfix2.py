# convergence pass: tail mass-decay curve. Target planar cross-section area A(s) (s = arc length from the tip along the fixed
# anatomical axis) built from a prescribed loss-rate curve dA/ds: slow near the tip (fine terminal taper kept), a long even
# loss through the mid tail, gently rising into the root -- endpoints A(12 cm) and A(98 cm) and everything outside unchanged.
# Applied as an axis-centred radial scale per station (cross-section shapes kept), field smoothed over the surface, iterated
# against true planar sections.  argv: in.npz(V,F) out.npz
import numpy as np, sys
from scipy.sparse import coo_matrix, diags
sys.path.insert(0,'/tmp/claude-0/rodin/p9'); from tailprof import profile; from slicearea import sections
z=np.load(sys.argv[1]); V=z['V'].astype(np.float64); F=z['F'].astype(np.int64); V_in=V.copy(); n=len(V)
C=np.load('/tmp/claude-0/rodin/g8/axis.npy'); ST=np.arange(2,214); S=ST*0.5
def ss(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
A0=sections(V,F,C,ST); ok=~np.isnan(A0[:,1]); Ac0=np.interp(S,A0[ok,0],A0[ok,1])
s0,s1=12.0,98.0; a0=np.interp(s0,S,Ac0); a1=np.interp(s1,S,Ac0); m0=(np.interp(s0+2,S,Ac0)-np.interp(s0-2,S,Ac0))/4
g=np.linspace(s0,s1,861); extra=3.0
base=m0+(g*0); rise=ss(12,40,g); root=ss(88,98,g)
k=(a1-a0-np.trapz(base,g)-extra*np.trapz(root,g))/np.trapz(rise,g)
dA=m0+k*rise+extra*root; At=a0+np.concatenate([[0],np.cumsum(0.5*(dA[1:]+dA[:-1])*np.diff(g))])
AT=np.interp(S,g,At); AT=np.where((S>=s0)&(S<=s1),AT,Ac0)
np.save('tail_target2.npy',np.stack([S,Ac0,AT],1)); print('loss-rate plateau k=%.2f cm2/cm (m0 %.2f)'%(m0+k,m0))
E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(n,n)).tocsr(); A=((A+A.T)>0).astype(np.float32); LAP=diags(1/np.asarray(A.sum(1)).ravel())@A
for it in range(4):
    Am=sections(V,F,C,ST); okk=~np.isnan(Am[:,1]); Ac=np.interp(S,Am[okk,0],Am[okk,1])
    K=np.sqrt(AT/Ac); K=np.where((S>=s0)&(S<=s1),K,1.0)
    print('iter',it,'max |A/target-1| in 12..98: %.3f'%np.abs(Ac[(S>=s0)&(S<=s1)]/AT[(S>=s0)&(S<=s1)]-1).max(),flush=True)
    ci,th,R=profile(V,C); ci2=np.clip(ci,1,len(C)-2); T=C[ci2+1]-C[ci2-1]; T/=np.linalg.norm(T,axis=1,keepdims=True)
    sf=ci*0.5+np.einsum('ij,ij->i',V-C[ci],T); r=V-C[ci]; r-=T*np.einsum('ij,ij->i',r,T)[:,None]
    tail=(V[:,1]<-26)&(V[:,2]>40)&(np.linalg.norm(r,axis=1)<22)&(sf<s1+1)
    kk=np.where(tail,np.interp(sf,S,K),1.0)
    for _ in range(200): kk=LAP@kk; kk[~tail]=1.0
    V=V+(kk-1)[:,None]*r
Am=sections(V,F,C,ST); okk=~np.isnan(Am[:,1]); Ac=np.interp(S,Am[okk,0],Am[okk,1])
print('final max |A/target-1| %.3f'%np.abs(Ac[(S>=s0)&(S<=s1)]/AT[(S>=s0)&(S<=s1)]-1).max())
mv=np.linalg.norm(V-V_in,axis=1); np.savez(sys.argv[2],V=V,F=F,MVT=mv.astype(np.float32)); print('max move %.2f cm'%mv.max())

# regional deviation both ways (excluding D vertex masks) with per-zone limits; prints PASS/FAIL token
import sys,numpy as np,igl
p=sys.argv[1]; c=np.array(eval(sys.argv[2])); R=float(sys.argv[3]); ex=sys.argv[4].split(',') if len(sys.argv)>4 and sys.argv[4]!='-' else []
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); SF=np.load('/home/claude/stc/rp1/weld.npz')['F'].astype(np.int64)
zz=np.load('/home/claude/stc/rp1/zones.npz'); zone=zz['zone']; names=list(zz['names'])
lim=np.array([3.0 if n=='general' else 1.5 for n in names])
z=np.load(p); V=z['V'].astype(float).copy(); V[:,1]*=-1; F=z['F'].astype(np.int64)
keep=np.ones(len(S),bool)
for e in ex: keep[np.load(e)]=False
m=np.where((np.linalg.norm(S-c,axis=1)<R)&keep)[0]
fs=np.linalg.norm(V[F].mean(1)-c,axis=1)<R+1
d,_,_=igl.point_mesh_squared_distance(S[m],V,F[fs]); d=np.sqrt(d)*10; over=d>lim[zone[m]]
pv=np.where(np.linalg.norm(V-c,axis=1)<R)[0]; sf=np.linalg.norm(S[SF].mean(1)-c,axis=1)<R+1
Fr=F[np.linalg.norm(V[F].mean(1)-c,axis=1)<R]; PP=np.vstack([V[pv],V[Fr].mean(1),(V[Fr[:,0]]+V[Fr[:,1]])/2]); pv=np.r_[pv,-np.ones(2*len(Fr),int)]
d2,I2,_=igl.point_mesh_squared_distance(PP,S,SF[sf]); d2=np.sqrt(d2)*10; z2=zone[SF[sf][I2,0]]; over2=d2>lim[z2]
print('src->prod max %.2f p95 %.2f over %d | prod->src max %.2f over %d  %s'%(d.max(),np.percentile(d,95),over.sum(),d2.max(),over2.sum(),'DEVPASS' if over.sum()+over2.sum()==0 else 'DEVFAIL'))
for k in np.argsort(-d)[:4]:
    if over[k]: print('   src',m[k],S[m[k]].round(2),'%.2f'%d[k],names[zone[m[k]]])
for k in np.argsort(-d2)[:3]:
    if over2[k]: print('   prod',pv[k],(PP[k]*[1,-1,1]).round(2),'%.2f'%d2[k])

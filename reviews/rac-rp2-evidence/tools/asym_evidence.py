# asym_evidence.py : RP2 asymmetry diagnostic tables (E3, mirrored E3, bilateral average S*, W2 GR218R, Grask family).
import numpy as np, json, igl, scipy.sparse as sp
R='/tmp/claude-0/rp2/'; A='/home/claude/wayfarer-design/reviews/reference-assets/r6/'
src=np.load(A+'GR5DE3_r6.npz'); keep=src['keep'].astype(bool); J=json.loads(str(src['joints']))
mir=np.load(R+'mir_body.npy'); E=np.load(R+'e3_body.npz'); V=E['V'].astype(float); Q=E['Q']
def asym(X):
    M=X[mir]*np.array([-1,1,1]); return X-M          # vector to mirror image; |.|/2 = distance to bilateral average
def body(f): return np.load(A+f)['V'][keep].astype(float)
aE=asym(V); mE=np.linalg.norm(aE,1)*10 if False else np.linalg.norm(aE,axis=1)*10
W=body('GR218R_r6.npz'); aW=asym(W); mW=np.linalg.norm(aW,axis=1)*10
out={'units':'mm; mirror deviation = |X - mirror(X)| (twice the distance to the bilateral average)'}
st=lambda d: dict(rms=float(np.sqrt((d**2).mean())),p50=float(np.median(d)),p95=float(np.percentile(d,95)),p99=float(np.percentile(d,99)),max=float(d.max()))
out['global']={'E3':st(mE),'W2_GR218R':st(mW)}
# regions
z=V[:,2]; ax=np.abs(V[:,0]); f=V[:,1]
Wb=dict(np.load(R+'weights_body.npz'))
arm=sum(Wb[k] for k in Wb if any(s in k for s in ('upperarm','lowerarm','hand','fingers')))
leg=sum(Wb[k] for k in Wb if any(s in k for s in ('thigh','calf','foot','ball')))
reg={
 'head_face (z>=195)': z>=195,
 'shoulder_neck_trapezius (170<=z<195, trunk)': (z>=170)&(z<195)&(arm<0.5),
 'upper_arm_deltoid (z>=150, arm)': (z>=150)&(arm>=0.5),
 'axilla_scapular (150<=z<170, trunk)': (z>=150)&(z<170)&(arm<0.5),
 'chest_abdomen_band (120<=z<150, trunk)': (z>=120)&(z<150)&(arm<0.5),
 'pelvis_crotch (100<=z<120, trunk)': (z>=100)&(z<120)&(arm<0.5)&(leg<0.5),
 'forearm_hand (z<150, arm)': (z<150)&(arm>=0.5),
 'thigh_knee (40<=z<100, leg)': (z>=40)&(z<100)&(leg>=0.5),
 'shin_ankle_foot (z<40)': z<40}
out['regions']={k:{'n':int(m.sum()),'E3':st(mE[m]),'W2':st(mW[m])} for k,m in reg.items()}
# family correlation of the asymmetry field
fam={}
for nm in ('GR5B218','GRA218','GR5CA','GR5CB','GR5CC','GR5DE1','GR5DE2','GR5B198','GR5B239'):
    try: a=asym(body(nm+'_r6.npz'))
    except Exception as e: continue
    c=float((a*aE).sum()/np.sqrt((a*a).sum()*(aE*aE).sum())); fam[nm]=dict(corr_with_E3=c, p99_mm=float(np.percentile(np.linalg.norm(a,axis=1)*10,99)))
out['family_asymmetry_correlation']=fam
# smoothing reproduction: uniform Laplacian on the symmetric W2 on the shared (asymmetric) hm08 quad graph
n=len(W); e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
Ad=sp.coo_matrix((np.ones(2*len(e)),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); Ad.data[:]=1
Dg=np.asarray(Ad.sum(1)).ravel(); Wl=W.copy()
for it in range(40): Wl=0.5*Wl+0.5*(Ad@Wl)/Dg[:,None]
aL=asym(Wl); out['smoothing_reproduction']=dict(iterations=40,lambda_=0.5,p99_mm=float(np.percentile(np.linalg.norm(aL,axis=1)*10,99)),max_mm=float(np.linalg.norm(aL,axis=1).max()*10),corr_with_E3=float((aL*aE).sum()/np.sqrt((aL*aL).sum()*(aE*aE).sum())))
# graph asymmetry of the hm08 quad graph: edges whose mirrored edge is not an edge
es=set(map(tuple,np.sort(e,1).tolist())); me=np.sort(mir[e],1); bad=[tuple(x) not in es for x in me.tolist()]
out['topology_mirror_inconsistent_edges']=int(sum(bad))
# landmarks (rig joints) side table
lm={}
for k,v in J.items():
    if k.endswith('_l') and k[:-2]+'_r' in J:
        a_=np.array(J[k],float); b_=np.array(J[k[:-2]+'_r'],float)*np.array([-1,1,1])
        lm[k[:-2]]=float(np.abs(a_-b_).max()*10)
out['landmark_side_difference_mm_max']=dict(max=max(lm.values()),per_joint=lm)
json.dump(out,open(R+'evpkg/asym_tables.json','w'),indent=1)
np.save(R+'evpkg/asymE3_mm.npy',mE); np.save(R+'evpkg/asymW2_mm.npy',mW)
print(json.dumps({k:out[k] for k in ('global','family_asymmetry_correlation','smoothing_reproduction','topology_mirror_inconsistent_edges')},indent=0)); print('landmark max',out['landmark_side_difference_mm_max']['max'])
for k,v in out['regions'].items(): print('%-48s n%5d E3 p95 %.2f max %.2f | W2 p95 %.2f max %.2f'%(k,v['n'],v['E3']['p95'],v['E3']['max'],v['W2']['p95'],v['W2']['max']))

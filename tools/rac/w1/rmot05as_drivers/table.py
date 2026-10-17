import sys, json; sys.path[:0]=['/home/claude/as','/home/claude/aq','/home/claude/al','/home/claude/an']; import numpy as np, aqmetrics as Q, aqsim as A, dryrun as D, predict_an as PA, dihed as DH
import scipy.sparse as sp
V=Q.V0; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; M=np.load(sys.argv[1]); St=np.load('/home/claude/ar/sets.npz'); z0=V[:,2].min()
G=DH.Gate(V,F,M); Avg=D.adjacency(F,len(V)); Y=V+A.vnormals(V,F)*(-0.007919*(1-M))[:,None]
ref,_=PA.reference(F,V); vf=sp.csr_matrix((np.ones(F.size),(F.ravel(),np.repeat(np.arange(len(F)),3))),shape=(len(V),len(F))); rv=PA.ringang(V,F,vf); s0=set(A.si(V,F).tolist())
HC={s:i[M[i]>=1] for s,i in Q.HB.items()}; rows=[]; S=Y; done=0
for n in [0]+[int(x) for x in sys.argv[2].split(',')]:
    S=PA.laplace_iter(S,Avg,M,n-done); done=n
    r=PA.predict(V,F,M,lambda X:S,ref=ref); r.pop('S'); rs=PA.ringang(S,F,vf)
    g,_=G.eval(S); dd=np.linalg.norm(S-V,axis=1)*1000
    row=dict(events=n,new_si=len(set(A.si(S,F).tolist())-s0),flips=len([f for f in r['flips'] if rs[f]>45]),raw_flips=len(r['flips']),new_local_inv=len(r['local_new_inversions']),collapse=len(A.collapse(V,S,F)),
        **g,ring_max_mm=round(float(dd[St['ring']].max()),3),core_max_mm=float(dd[St['core']].max()),pelvis_pct=round((Q.pelvis_width(S)/Q.pelvis_width(V)-1)*100,3),
        hip_core_mm={s:round(float(np.linalg.norm(S[i].mean(0)-V[i].mean(0))*1000),4) for s,i in HC.items()},thigh_pct=Q.thigh_radius(S),
        depth_change_mm={s:round(Q.profile_depth(S)[s]-Q.profile_depth(V)[s],2) for s in 'LR'})
    rows.append(row); print(json.dumps({k:v for k,v in row.items() if k!='chains_over_40mm'}),'chains',len(row['chains_over_40mm']),row['chains_over_40mm'][:3],flush=True)
    np.savez(f'sim_{sys.argv[3]}_{n}.npz',V=S,F=F)
json.dump(rows,open(f'table_{sys.argv[3]}.json','w'),indent=1)

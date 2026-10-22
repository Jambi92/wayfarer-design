# refix.py KEY : apply the fold repair to an existing drape result (no re-relaxation)
import sys,numpy as np; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from drape import *; from patches import boundary_loops
k=sys.argv[1]; z=dict(np.load('/tmp/claude-0/hand/drape_%s.npz'%k)); P2=z['P2']; Q=z['Ql']
D=Domain(z['Xl'],z['Fl'],z['U']); sgn=np.sign(np.median(orient2(P2,Q)))
bl=np.array(boundary_loops(Q)[0][0]); fixed=np.zeros(len(P2),bool); fixed[bl]=True
apex=D.lift(P2,D.locate(P2)); hard=np.zeros(len(P2),bool)
# keep the vertex sitting on the claw apex
import pickle; rp=pickle.load(open('/tmp/claude-0/hand/rpatch.pkl','rb'))[k]; ha=int(np.argmin(np.linalg.norm(apex-rp['apex'],axis=1))); hard[ha]=(len(sys.argv)<3)
P2=pin_star_fix(P2,Q,sgn,ha,fixed,log=print)
print('before',int((orient2(P2,Q)*sgn<=1e-14).sum()))
for rep in range(4):
    P2=smooth_fix(P2,Q,sgn,~hard&~fixed,log=print); P2=star_fix(P2,Q,sgn,~hard,iters=10,log=print)
    if not (orient2(P2,Q)*sgn<=1e-14).any(): break
print('after',int((orient2(P2,Q)*sgn<=1e-14).sum()))
z['P2']=P2; z['X3']=D.lift(P2,D.locate(P2)); np.savez('/tmp/claude-0/hand/drape_%s.npz'%k,**z)

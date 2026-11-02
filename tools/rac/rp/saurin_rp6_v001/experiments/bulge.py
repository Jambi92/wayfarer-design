import sys,os,time,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');sys.path.insert(0,'/tmp/claude-0/rp6/exp')
import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC; from dqs import dqs
def bulge(R,S,T,P,V0,smooth=40,iters=5,tol=5.0,comp_pow=1.0):
    W=R.W;Rb=np.stack([T[b][0] for b in R.DB]);M=(W@Rb.reshape(len(R.DB),9)).reshape(-1,3,3)
    spread=np.zeros(R.nv)
    for j in range(len(R.DB)):
        m_=W[:,j]>0
        if m_.any(): spread[m_]+=W[m_,j]*np.linalg.norm(Rb[j][None]-M[m_],axis=(1,2))
    if spread.max()<1e-6: return P
    wv=np.clip(spread/max(np.percentile(spread[spread>1e-6],95),1e-9),0,1);wv=3*wv**2-2*wv**3
    excl=[R.bi[b] for b in R.DB if b=='jaw' or b.startswith(('finger','thumb','toe','meta'))];wv[W[:,excl].sum(1)>0]=0
    Q=R.Q;deg=np.asarray(S.A1.sum(1)).ravel()
    def varea(P_):
        a_=np.zeros(R.nv);qa=0.5*np.linalg.norm(np.cross(P_[Q[:,2]]-P_[Q[:,0]],P_[Q[:,3]]-P_[Q[:,1]]),axis=1)
        for k in range(4): np.add.at(a_,Q[:,k],qa/4)
        return a_
    ratio=varea(P)/np.maximum(varea(R.V),1e-12)
    # crease = strongly compressed surface: keep the push OFF the crease itself (flesh bulges around it, not into the fold)
    crease=np.clip((0.85-ratio)/0.25,0,1)
    for _ in range(5): crease=0.5*crease+0.5*(S.A1@crease)/deg
    g=wv*(1-crease)
    for _ in range(smooth): g=0.5*g+0.5*(S.A1@g)/deg
    g[S.rigid]=0; g[W[:,excl].sum(1)>0]=0
    U_,_,Vt_=np.linalg.svd(M);Mr=U_@Vt_
    n_rest=np.zeros_like(R.V)
    for k in range(4): np.add.at(n_rest,Q[:,k],np.cross(R.V[Q[:,(k+1)%4]]-R.V[Q[:,k]],R.V[Q[:,(k+3)%4]]-R.V[Q[:,k]]))
    n=np.einsum('vij,vj->vi',Mr,n_rest);n/=np.linalg.norm(n,axis=1,keepdims=True)+1e-12
    P=P.copy()
    for _ in range(iters):
        dV=S.body_volume(P)-V0
        if abs(dV)<tol: break
        # dV/dalpha numerically
        e=1e-3;dd=(S.body_volume(P+e*g[:,None]*n)-S.body_volume(P))/e
        if abs(dd)<1e-9: break
        P+=(-dV/dd)*g[:,None]*n
    return P
if __name__=='__main__':
    R=SP.Rig('M','/tmp/claude-0/rp6/W_M.npz');S=CC.Solver(R);S.V0=S.body_volume(R.V);PS=FT.pose_set(R)
    F=np.r_[R.Q[:,[0,1,2]],R.Q[:,[0,2,3]]].astype(np.int64);w0=FT.wn_out(R.V,F)
    def st(P,T): return int((R.relcos(P,T)<0).sum()),int(FT.penetration(R,P,F,w0).sum()),round(S.body_volume(P)-S.V0)
    for pn in sys.argv[1].split(','):
        T=R.pose(PS[pn]);P=R.skin(T);Pd=dqs(R,T);Pd,_=S.unfold(T,Pd,R.relcos)
        for nm,P0 in (('lbs',P),('dqs+u',Pd)):
            for sm in (20,60,150):
                Pb=bulge(R,S,T,P0,S.V0,smooth=sm);a=st(Pb,T);Pu,_=S.unfold(T,Pb,R.relcos);print('%-22s %-6s sm%3d bulge %s maxd %.2f -> +unfold %s'%(pn,nm,sm,a,np.linalg.norm(Pb-P0,axis=1).max(),st(Pu,T)),flush=True)

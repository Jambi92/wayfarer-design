# subdiv_region.py IN OUT "expr on x,f,z (face centroid)" : conforming 1:4 subdivision of selected faces (red-green closure), PN-triangle midpoints
import sys, numpy as np, igl
d=np.load(sys.argv[1]); V=d['V'].astype(float); F=d['Q'].astype(np.int64); n=len(V)
c=V[F].mean(1); x,f,z=c.T; sel=eval(sys.argv[3])
E=np.r_[F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]; Es=np.sort(E,1)
u,inv=np.unique(Es,axis=0,return_inverse=True); inv=inv.reshape(3,-1).T   # face -> 3 edge ids (edges 01,12,20)
split=np.zeros(len(u),bool); split[inv[sel].ravel()]=True
# PN midpoint
N=igl.per_vertex_normals(V,F)
a=V[u[:,0]]; b=V[u[:,1]]; na=N[u[:,0]]; nb=N[u[:,1]]
b210=(2*a+b-((b-a)*na).sum(1)[:,None]*na)/3; b120=(2*b+a-((a-b)*nb).sum(1)[:,None]*nb)/3
mid=(a+3*b210+3*b120+b)/8
eid=-np.ones(len(u),int); eid[split]=n+np.arange(split.sum()); NV=np.r_[V,mid[split]]
out=[]
for k,(v0,v1,v2) in enumerate(F):
    e01,e12,e20=inv[k]; m01,m12,m20=eid[e01],eid[e12],eid[e20]; s=int(m01>=0)+int(m12>=0)+int(m20>=0)
    if s==0: out.append((v0,v1,v2))
    elif s==3: out+= [(v0,m01,m20),(m01,v1,m12),(m20,m12,v2),(m01,m12,m20)]
    elif s==1:
        if m01>=0: out+=[(v0,m01,v2),(m01,v1,v2)]
        elif m12>=0: out+=[(v0,v1,m12),(v0,m12,v2)]
        else: out+=[(v0,v1,m20),(m20,v1,v2)]
    else:
        # two split edges: rotate so that unsplit edge is (v2,v0) i.e. e20 unsplit
        tri=[v0,v1,v2]; ms=[m01,m12,m20]
        r=[i for i in range(3) if ms[(i+2)%3]<0][0]   # rotation so that edge (r-1 -> r) ... choose r with ms[r-1] unsplit
        A,B,C=tri[r],tri[(r+1)%3],tri[(r+2)%3]; mAB,mBC=ms[r],ms[(r+1)%3]
        out+=[(A,mAB,C),(mAB,B,mBC),(mAB,mBC,C)]
NF=np.array(out,np.int64)
np.savez(sys.argv[2],V=NV,Q=NF,parent_vertex=np.r_[np.ones(n,bool),np.zeros(split.sum(),bool)],mid_edge=u[split],lin_mid=((a+b)/2)[split])
Es=np.sort(np.r_[NF[:,[0,1]],NF[:,[1,2]],NF[:,[2,0]]],1); uu,cc=np.unique(Es,axis=0,return_counts=True)
print('V',len(NV),'F',len(NF),'boundary',(cc==1).sum(),'nonmanifold',(cc>2).sum(),'euler',len(NV)-len(uu)+len(NF))

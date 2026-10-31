import sys,time,pickle,numpy as np; sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v002'); t=time.time()
import sa_design as SD
D=SD.D; Q=np.array(D.Q); C=np.array(D.C)
E={}
for q in Q:
    for k in range(4): e=(min(q[k],q[(k+1)%4]),max(q[k],q[(k+1)%4])); E[e]=E.get(e,0)+1
print('V',len(C),'E',len(E),'F',len(Q),'chi',len(C)-len(E)+len(Q),'boundary edges',sum(1 for v in E.values() if v==1),'nonmanifold',sum(1 for v in E.values() if v>2))
# directed edge consistency
de={}
for qi,q in enumerate(Q):
    for k in range(4): de.setdefault((q[k],q[(k+1)%4]),[]).append(qi)
bad=[(e,v) for e,v in de.items() if len(v)>1]; print('inconsistent directed edges',len(bad))
for e,v in bad[:10]: print('  ',D.name[e[0]],D.name[e[1]],[D.qlab[i] for i in v])
bnd=[e for e,v in E.items() if v==1]; print('boundary', [(D.name[a],D.name[b]) for a,b in bnd][:20])
pickle.dump(dict(C=C,Q=Q,name=D.name,qlab=D.qlab,hint=D.hint,fixed=D.fixed,pins=D.pins,loops=D.loops,head=D.head,arcs=D.arcs),open('/tmp/claude-0/rt/sa/cage/design.pkl','wb'))

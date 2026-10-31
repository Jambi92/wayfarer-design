import sys,pickle,numpy as np; sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v002'); import sa_geo as G
d=pickle.load(open('/tmp/claude-0/rt/sa/cage/design.pkl','rb')); C=d['C']; nm=d['name']; bad=[]
for qi,q in enumerate(d['Q']):
    P=C[q]; c=P.mean(0); n=G.VN[G.snap(c)]
    # signed area of each corner's triangle (prev, this, next) about n
    s=[np.cross(P[k]-P[k-1],P[(k+1)%4]-P[k])@n for k in range(4)]
    if min(s)<=0: bad.append((qi,d['qlab'][qi],[nm[i] for i in q],np.round(s,1).tolist()))
print(len(bad))
import collections; print(collections.Counter(b[1] for b in bad))
for b in bad[:60]: print(b)

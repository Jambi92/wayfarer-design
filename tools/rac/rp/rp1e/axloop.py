"""Junction loop through the cage graph (design only). Usage: python3 axloop.py SIDE CAGE.npz [K]
P1 = cheapest cage-vertex path between the verts nearest the crease-curve ends, cost = len + K*d(mid,curve)^2;
P2 = cheapest return path avoiding P1 interior, restricted to arm-root region, cost = len + K2*penalty(z<zc) .
Prints loop and distances; saves axloop_SIDE.json"""
import numpy as np, sys, json, networkx as nx
s=sys.argv[1]; cg=sys.argv[2]; K=float(sys.argv[3]) if len(sys.argv)>3 else 3.0
sys.argv=['x',s]
exec(open('ring11.py').read().split("if __name__=='__main__':")[0])
from scipy.spatial import cKDTree
z=np.load(cg); V=z['V']
sg=-1 if s=='R' else 1
Q=np.load('ccurve_%s.npy'%s); T=cKDTree(Q)
reg=[i for i in range(len(V)) if 12<V[i,0]*sg<34 and 125<V[i,2]<172 and -55<V[i,1]<-10]
G=nx.Graph()
for i in reg:
    for j in adj[i]:
        if j in set(reg) and i<j:
            m=(V[i]+V[j])/2; d,_=T.query(m)
            G.add_edge(i,j,w=np.linalg.norm(V[i]-V[j])+K*d*d, l=np.linalg.norm(V[i]-V[j]))
_,a=cKDTree(V[reg]).query(Q[0]); _,b=cKDTree(V[reg]).query(Q[-1]); a=reg[a]; b=reg[b]
P1=nx.shortest_path(G,a,b,weight='w')
d1,_=T.query(V[P1])
print(s,'P1',P1,'dist to crease',d1.round(2))
rings=arm_rings(s); armset=set(v for r in rings for v in r)
# return path: remove P1 interior; prefer upper region (shoulder top) near the arm-root rings
G2=G.copy(); G2.remove_nodes_from(P1[1:-1])
for i,j in G2.edges():
    zc=min(V[i,2],V[j,2]); G2[i][j]['w2']=G2[i][j]['l']*(1+ (3.0 if zc<148 else 0.0))
P2=nx.shortest_path(G2,b,a,weight='w2')
print('P2',P2,'z',V[P2,2].round(1))
loop=P1+P2[1:-1]
json.dump(dict(P1=[int(v) for v in P1],P2=[int(v) for v in P2],loop=[int(v) for v in loop]),open('axloop_%s.json'%s,'w'))
# flood sides
G3=nx.Graph(); 
for i in range(len(V)):
    for j in adj[i]:
        if i<j and i not in set(loop) and j not in set(loop): G3.add_edge(i,j)
comps=list(nx.connected_components(G3)); arm=[c for c in comps if rings[3][0] in c]; print('components',len(comps),'sizes',sorted(len(c) for c in comps)[-4:],'arm comp size',len(arm[0]) if arm else None)

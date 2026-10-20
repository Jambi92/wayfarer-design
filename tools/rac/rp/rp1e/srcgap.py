# srcgap.py "c" R : opposed-sheet source gap near c (min dist to a source vertex with opposing normal, excluding the local sheet)
import numpy as np, sys, igl
from scipy.spatial import cKDTree
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64); N=igl.per_vertex_normals(S,SF)
c=np.array(eval(sys.argv[1])); R=float(sys.argv[2]); idx=np.where(np.linalg.norm(S-c,axis=1)<R)[0]; T=cKDTree(S)
g=[]
for i in idx:
    nb=T.query_ball_point(S[i],0.6); nb=[j for j in nb if N[j]@N[i]<-0.5 and (S[j]-S[i])@N[i]>0]
    g.append(min([np.linalg.norm(S[j]-S[i]) for j in nb]) if nb else np.inf)
g=np.array(g); f=np.isfinite(g); print('pts',len(idx),'with opposed sheet <6mm',f.sum(),'gap mm min/med',(g[f].min()*10).round(2) if f.any() else None,(np.median(g[f])*10).round(2) if f.any() else None)

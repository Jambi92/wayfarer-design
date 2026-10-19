import numpy as np,json,sys
cg=sys.argv[1]; side=sys.argv[2]
z=np.load(cg);F=z['F'];V=z['V'];P=np.load(cg.replace('.npz','_pairs.npy'));J=json.load(open(cg.replace('.npz','_ax%s.json'%side)))
lab={}
for k,r in J['rings'].items():
  for i,v in enumerate(r): lab[v]='%s.%d'%(k,i)
for i,v in enumerate(J['inner']): lab[v]='in.%d'%i
for i,v in enumerate(J['outer']): lab[v]='out.%d'%i
for i,j in P:
  a=[(lab.get(int(v),'x'),V[v].round(1).tolist()) for v in F[i] if v>=0]; b=[(lab.get(int(v),'x'),V[v].round(1).tolist()) for v in F[j] if v>=0]; print(a,'|',b)

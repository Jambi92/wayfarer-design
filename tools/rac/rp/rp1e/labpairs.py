import numpy as np,json,sys
cg=sys.argv[1]; z=np.load(cg);F=z['F'];V=z['V'];P=np.load(cg.replace('.npz','_pairs.npy'));J=json.load(open(sys.argv[2]))
lab={}
for k,r in enumerate(J['rings']):
  for i,v in enumerate(r): lab[v]='R%d.%d'%(k-1,i) if k else 'T.%d'%i
for k,r in enumerate(J.get('pocket',[])):
  for i,v in enumerate(r): lab[v]='P%d.%d'%(k,i)
for i,v in enumerate(J['loop']): lab[v]='B.%d'%i
for i,j in P:
  print([lab.get(int(v),int(v)) for v in F[i] if v>=0],'|',[lab.get(int(v),int(v)) for v in F[j] if v>=0])

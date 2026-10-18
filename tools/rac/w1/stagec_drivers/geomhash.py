import numpy as np, hashlib, sys
def gh(p):
    z=np.load(p,allow_pickle=True); V=np.ascontiguousarray(z['V'].astype(np.float32)); F=np.ascontiguousarray(z['F'].astype(np.int32))
    return hashlib.sha256(V.tobytes()+F.tobytes()).hexdigest()
def fh(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
if __name__=='__main__':
    for p in sys.argv[1:]: print(p.split('/')[-1], 'geom', gh(p)[:16], 'file', fh(p)[:16])

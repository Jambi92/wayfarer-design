# movev.py CAGE COL OUT 'id:x,y,z;id:x,y,z'
import numpy as np, sys
z=np.load(sys.argv[1]); V=z['V'].copy(); F=z['F']
for it in sys.argv[4].split(';'):
    i,p=it.split(':'); V[int(i)]=[float(t) for t in p.split(',')]
np.savez_compressed(sys.argv[3],V=V,F=F); np.save(sys.argv[3].replace('.npz','_col.npy'),np.load(sys.argv[2]))

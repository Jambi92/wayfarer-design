# writeobj.py IN.npz OUT.obj NAME TAG : cage (Blender cm) -> OBJ in metres, Y-up (x, z, -y) for the default Blender OBJ import
import numpy as np, sys
z=np.load(sys.argv[1]); V=z['V']/100.0; F=z['F']; name=sys.argv[3]; tag=sys.argv[4]
with open(sys.argv[2],'w') as f:
    f.write('# RP1E %s cage design (cloud), Blender metres written Y-up (x, z, -y) for default OBJ import\n'%tag)
    f.write('o %s\n'%name)
    for v in V: f.write('v %.7f %.7f %.7f\n'%(v[0],v[2],-v[1]))
    for q in F: f.write('f '+' '.join(str(int(i)+1) for i in q if i>=0)+'\n')

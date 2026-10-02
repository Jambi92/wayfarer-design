import numpy as np, sys
sys.path.insert(0,"/tmp/claude-0/rb")
import wf_saurin_body8 as B8
B8.sdf=lambda X,F,U: B8.head((X,F,U)); B8.BOX=(-11.0,11.0,-15.0,25.0,162.0,191.0)
v,f=B8.mesh(0.15,log=lambda *a:None); np.savez("ts61_head.npz",v=v,f=f); print(len(v), v.min(0).round(1), v.max(0).round(1))

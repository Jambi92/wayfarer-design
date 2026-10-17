# RM-OT-05AO upper-arm mask from the rig's dominant-weight regions (vertex IDs), precedent: 05AL s3 mask transfer by vertex ID.
# sculptable core = upper-arm dominant vertices; mask = 1 everywhere else; inside the arm the mask ramps from 1 at the
# region boundary (shoulder / armpit / elbow) to 0 over a feather produced by graph diffusion (k iterations) of the outside indicator.
import sys, numpy as np
sys.path.insert(0,'/home/claude/al'); import dryrun as D
def build(V, F, W, names, k=300, gain=2.0, sides='LR'):
    Avg=D.adjacency(F,len(V)); lab=W.argmax(1)
    arm=np.isin(lab,[names.index(f'upperarm_{s}') for s in sides])
    c=(~arm).astype(float)
    for _ in range(k): c=Avg@c
    m=np.ones(len(V)); m[arm]=np.clip(gain*c[arm],0,1); return m, arm

# Emulation of the UI mask build: box masks through depth in front / right orthographic views (calibrated screen mapping),
# Mask > Invert, Mask > Smooth Mask (k neighbour-average iterations per op). Used only to design box sizes / pass counts.
import numpy as np, sys
sys.path.insert(0,'/home/claude/al'); import dryrun as D
class Emu:
    def __init__(s, V, F):
        s.V=V; s.z0=V[:,2].min(); Z=(V[:,2]-s.z0)*100
        s.front=np.c_[601+V[:,0]*100*2.606, 670-Z*2.606]; s.right=np.c_[421+(V[:,1]*100+67.9)*2.6, 669-Z*2.6]
        s.Avg=D.adjacency(F,len(V)); s.M=np.zeros(len(V))
    def clear(s): s.M[:]=0
    def box(s,x0,y0,x1,y1,view='front'):
        P=s.front if view=='front' else s.right; m=(P[:,0]>=min(x0,x1))&(P[:,0]<=max(x0,x1))&(P[:,1]>=min(y0,y1))&(P[:,1]<=max(y0,y1)); s.M[m]=1
    def invert(s): s.M=1-s.M
    def smooth(s,k):
        for _ in range(k): s.M=s.Avg@s.M

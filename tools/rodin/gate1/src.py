# Gate 1 sources: untouched B1 (c12) and B2 (c11) in canonical frame, centimetres (B1 standing height -> 188).
import numpy as np, sys
sys.path.insert(0,"/tmp/claude-0/rodin/adopt")
from donor import canon
H_CM=188.0
def load():
    P1,f1,H1=canon(12,-4.0); P2,f2,H2=canon(11,60.0)
    s=H_CM/H1                      # one common scale (Rodin units -> cm), B2 uses the SAME factor
    return P1*s, f1, P2*s, f2, s
if __name__=="__main__":
    P1,f1,P2,f2,s=load(); np.savez("src.npz",P1=P1,f1=f1,P2=P2,f2=f2,s=s)
    print("B1 H",np.ptp(P1[:,2]),"B2 H",np.ptp(P2[:,2]),"scale",s)

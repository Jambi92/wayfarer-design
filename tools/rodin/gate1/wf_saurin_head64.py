# TS6.4: uniform head-scale wrapper around the TS6.3 naked skull. Scaling is about a pivot on the cranial roof so the
# skull top (standing height) stays fixed and rostrum : cranium proportions are preserved exactly.
import os, numpy as np
import wf_saurin_head65 as H          # head65 = head63 skull (+ optional display variant)
S=float(os.environ.get("HEAD_SCALE","1.06")); PIV=np.array([0.0,-3.0,8.6])   # head-local (x, f, u); roof apex ~ u 8.7
P=H.P; EYE=H.EYE
def head_sdf(X,F,U,neck_rings,cut_u):
    x=(X-PIV[0])/S+PIV[0]; f=(F-PIV[1])/S+PIV[1]; u=(U-PIV[2])/S+PIV[2]
    return H.head_sdf(x,f,u,neck_rings,cut_u)*S
def eye_centers():
    (e1,e2),er,yaw=H.eye_centers()
    sc=lambda c: tuple((np.array(c)-PIV)*S+PIV)
    return [sc(e1),sc(e2)],er*S,yaw

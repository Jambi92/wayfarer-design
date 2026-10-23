# zones.py: identity (T-2) zones, contact zones, part labels for the Grask production branch (analysis frame, cm)
import numpy as np, json
def base_zones(V, W, J):
    n = len(V); g = lambda *k: sum(W[x] for x in k)
    z = {}
    z['head_face'] = g('head', 'ears') > 0.5
    z['hands'] = g('hand_l', 'hand_r', 'fingers_l', 'fingers_r') > 0.5
    z['feet'] = g('foot_l', 'foot_r', 'ball_l', 'ball_r') > 0.5
    gh = [np.array(J['upperarm_%s' % s][0]) for s in 'lr']
    z['girdle_shoulder'] = (g('clavicle_l', 'clavicle_r') > 0.3) | (np.min([np.linalg.norm(V - c, axis=1) for c in gh], 0) < 12)
    jc = [np.array(J['lowerarm_%s' % s][0]) for s in 'lr'] + [np.array(J['hand_%s' % s][0]) for s in 'lr'] + \
         [np.array(J['calf_%s' % s][0]) for s in 'lr'] + [np.array(J['foot_%s' % s][0]) for s in 'lr']
    z['joints'] = np.min([np.linalg.norm(V - c, axis=1) for c in jc], 0) < 6
    z['pelvis'] = W['pelvis'] > 0.5
    s3 = np.array(J['spine_03'][0]); z['keel_chest'] = (W['spine_03'] > 0.5) & (V[:, 1] > s3[1])
    z['T2'] = np.any([z[k] for k in list(z)], 0)
    return z

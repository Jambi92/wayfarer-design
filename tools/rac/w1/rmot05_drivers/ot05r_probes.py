# RAC RM-OT-05 readability correction search (diagnostic quick probes on the accepted W2 routes; only canon-named directions).
# Grask (GRASK L54 / L59 / L164-174 / L233-253; W2C named extreme GR-BODY-11 region): torso contribution down, forearm / upper-arm up,
#   femur slightly down (stature held), large integrated hands and feet.
# Gorrund (GORRUND L19 / L63 / L74-76 / L179-189; ALPC): joint structural presence (knee / ankle / wrist / elbow cross-section), long-bone
#   structural cross-section, thoracic depth and lower-trunk continuity (sculpt), larger hands / feet in absolute terms.
import os, sys, json
T = '/home/claude/wayfarer-design/tools/rac/w1'; sys.path.insert(0, T + '/w2c_drivers'); sys.path.insert(0, T + '/w2d_drivers')
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; Q = S + '/rmot05r/q'
K = ['torso_share', 'leg_share', 'arm_share', 'forearm_over_arm', 'shin_over_leg', 'hand_share', 'foot_share', 'shoulder_joint_share', 'thorax_breadth_share', 'thorax_depth_share',
     'knee_over_femur', 'elbow_over_humerus', 'wrist_over_forearm', 'ankle_over_shin', 'crest_share', 'pelvic_depth_share', 'thorax_d_over_b']
GR = {'GRQ1': {'measure-napetowaist-dist-decr': 0.5, 'measure-lowerarm-length-incr': 0.9, 'measure-upperarm-length-incr': 0.1, 'LR:hand-scale-incr': 0.3, 'LR:foot-scale-incr': 0.25},
      'GRQ2': {'measure-napetowaist-dist-decr': 0.65, 'measure-lowerarm-length-incr': 1.0, 'measure-upperarm-length-incr': 0.15, 'LR:hand-scale-incr': 0.35, 'LR:foot-scale-incr': 0.3, 'measure-upperleg-height-decr': 0.45}}
GO = {'GOQ1': ({'bone_scales': {'LR:upperarm': [1.08, 1, 1.08], 'LR:lowerarm': [1.08, 1, 1.08], 'LR:calf': [1.08, 1, 1.08]}},
               {'measure-knee-circ-incr': 0.5, 'measure-ankle-circ-incr': 0.4, 'measure-wrist-circ-incr': 0.4, 'LR:hand-scale-incr': 0.15, 'LR:foot-scale-incr': 0.15}),
      'GOQ2': ({'bone_scales': {'LR:upperarm': [1.10, 1, 1.10], 'LR:lowerarm': [1.10, 1, 1.10], 'LR:calf': [1.10, 1, 1.10], 'LR:thigh': [1.04, 1, 1.04]}, 'kp': 1.05, 'kd_from': 0.18, 'kb_nodes': [1.0, 1.0, 1.06, 1.06, 1.0, 1.0]},
               {'measure-knee-circ-incr': 0.6, 'measure-ankle-circ-incr': 0.5, 'measure-wrist-circ-incr': 0.5, 'LR:hand-scale-incr': 0.2, 'LR:foot-scale-incr': 0.2})}
if __name__ == '__main__':
    out = {}
    import gr_body as G
    for n, t in GR.items():
        r = G.quick(n, 'ref', None, t, Q + '/' + n); out[n] = dict(targets=t, stature=r['stature'], **{k: r['ratio'].get(k) for k in K}); print(n, {k: round(out[n][k], 4) for k in K[:9]}, flush=True)
    import go_body as GB
    for n, (fr, t) in GO.items():
        r = GB.quick(n, 0.8369140625, fr, t, Q + '/' + n); out[n] = dict(frame=fr, targets=t, stature=r['stature'], **{k: r['ratio'].get(k) for k in K}); print(n, {k: round(out[n][k], 4) for k in K}, flush=True)
    json.dump(out, open(S + '/rmot05r/probes.json', 'w'), indent=1)

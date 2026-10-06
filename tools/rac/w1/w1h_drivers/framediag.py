# RAC W1h driver AS RUN: W1g frame shaft / lower-thorax diagnosis (with / without the frame pelvis write and kb nodes)
import sys, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn3, gn4
x = json.load(open('/home/claude/wayfarer-design/reviews/rac-w1g-evidence/solver/GO_params.json'))['x']
FR = {"F04": {"bone_scales": {"LR:clavicle": [1, 0.92, 1], "pelvis": [0.91, 1, 1]}, "kb_nodes": [0.95, 0.93, 0.92, 0.83, 0.85, 0.92]},
      "F04nopel": {"bone_scales": {"LR:clavicle": [1, 0.92, 1]}, "kb_nodes": [0.95, 0.93, 0.92, 0.83, 0.85, 0.92]},
      "F04nokb": {"bone_scales": {"LR:clavicle": [1, 0.92, 1], "pelvis": [0.91, 1, 1]}},
      "F12": {"bone_scales": {"LR:clavicle": [1, 0.88, 1], "pelvis": [0.865, 1, 1]}, "kb_nodes": [0.925, 0.895, 0.88, 0.75, 0.78, 0.88]},
      "F12nopel": {"bone_scales": {"LR:clavicle": [1, 0.88, 1]}, "kb_nodes": [0.925, 0.895, 0.88, 0.75, 0.78, 0.88]}}
wd = gn3.G + '/framediag'
for n, fr in FR.items():
    B, sc = gn4.unpack(x, frame=fr); gn3.build("GO", n, B, sc, wd=wd); rows = gn3.checks("GO", n, wd=wd)
    for y in rows:
        if y['cand'] == 'GO' and ('shaft' in y['check'] or 'lower-thorax breadth' in y['check'] or 'proximal-femur' in y['check']):
            print(n, y['check'][:55], {t: (round(v['va'], 4), round(v['vb'], 4), v['result'][:4]) for t, v in y['by_t'].items()}, flush=True)
    sk = json.load(open(wd + '/skp_%s/%s_skp.json' % (n, n))); print(n, 'shaft S7 cm', round(sk['by_t']['0.0']['alpc_stations']['S7'][0], 2), 'femur', round(sk['by_t']['0.0']['extra']['femur_len'], 2), flush=True)

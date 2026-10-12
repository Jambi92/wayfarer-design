# RAC RM-OT-05L GO-RS2-REF brush pass (order §5, §17): hand-drawn sculpt strokes on the finished RS2 clay surface.
# Each line = one stroke (brush, path drawn on the body's left side and mirrored, radius cm, strength). Control points are snapped
# to the nearest surface vertex before the stroke (the brush is drawn ON the body).   Usage: python3 l_rs2_brush.py IN.obj OUT.obj
import sys, numpy as np
from l_brush import Mesh, stroke
STROKES = [
 # girdle / thorax
 ('draw',    [(5, 9, 188), (12, 7, 187), (19, 4, 184.5)], 2.5, 0.5, 'clavicle line carrying the girdle'),
 ('flatten', [(0, 19, 170), (0, 19, 158)], 7.0, 0.5, 'sternal plane'),
 ('crease',  [(2, 18, 151), (8, 16, 148), (14, 12, 146), (18, 6, 145)], 2.5, 0.7, 'costal arch: rib cage edge over the lower axial wall'),
 ('flatten', [(0, 11, 140), (0, 11.5, 130), (0, 11, 122)], 9.0, 0.6, 'planar lower axial anterior wall (no belly)'),
 ('crease',  [(0, 11, 145), (0, 11.5, 122)], 1.5, 0.2, 'median line, faint'),
 ('crease',  [(19, 9, 178), (22, 8, 170)], 1.8, 0.3, 'girdle / upper-arm separation (front)'),
 # pelvis
 ('crease',  [(9, 10, 127), (15, 4, 129), (17, -4, 128), (13, -11, 126)], 2.2, 0.5, 'iliac crest line'),
 ('draw',    [(12, 10, 125)], 2.5, 0.4, 'anterior iliac spine'),
 ('flatten', [(20, 0, 112), (20, 0, 100)], 8.0, 0.7, 'lateral hip plane (proximal femur under the load path, no outrigger)'),
 ('flatten', [(5, -15, 120), (5, -15, 108)], 8.0, 0.7, 'sacral platform'),
 ('smooth',  [(9, -12, 105), (13, -10, 100)], 7.0, 0.8, 'sacrum -> hamstring continuity (no gluteal apex)'),
 # posterior axial chain
 ('draw',    [(4.5, -16.5, 178), (4.5, -14, 150), (4.5, -12.5, 128)], 3.0, 0.6, 'paired low axial columns'),
 ('crease',  [(0, -17, 178), (0, -13.5, 128)], 1.6, 0.35, 'shallow median furrow (no trench)'),
 ('crease',  [(8, -16.5, 180), (9, -16.5, 168), (12, -15, 160)], 1.8, 0.3, 'scapular medial border'),
 ('flatten', [(14, -15, 175)], 6.0, 0.4, 'scapular plane on the thorax'),
 # knee / shank / ankle
 ('flatten', [(13.2, 10.5, 62), (13.2, 10, 58)], 4.5, 0.7, 'patellar plane'),
 ('crease',  [(9.5, 9, 56), (13.2, 9.5, 54.5), (17, 9, 56)], 1.8, 0.4, 'infrapatellar margin'),
 ('flatten', [(21.5, 2, 61)], 5.0, 0.6, 'lateral knee plane'),
 ('flatten', [(4.5, 2, 61)], 5.0, 0.6, 'medial knee plane'),
 ('flatten', [(13.5, 9.5, 52), (13.0, 7, 30), (12.8, 5.5, 18)], 3.5, 0.6, 'anterior tibial plane'),
 ('crease',  [(9.5, 5.5, 50), (8.5, 3.5, 28)], 1.8, 0.3, 'medial tibial border'),
 ('crease',  [(10, -6.5, 20), (10, -7, 12)], 1.5, 0.3, 'Achilles margin'),
 # upper limb
 ('draw',    [(30, -9, 149)], 2.5, 0.3, 'olecranon'),
 ('flatten', [(31.5, 5, 140), (33.5, 5, 122)], 3.0, 0.5, 'anterior forearm plane'),
 ('crease',  [(31, 4, 116), (35, 4, 116)], 1.4, 0.3, 'wrist margin'),
]
if __name__ == '__main__':
    V = [[float(t) for t in l.split()[1:4]] for l in open(sys.argv[1]) if l.startswith('v ')]
    F = [[int(t) - 1 for t in l.split()[1:4]] for l in open(sys.argv[1]) if l.startswith('f ')]
    M = Mesh(V, F); log = []
    for kind, pts, r, s, lab in STROKES:
        snapped = [M.V[np.argmin(np.linalg.norm(M.V - np.asarray(p, float), axis=1))].tolist() for p in pts]
        stroke(M, kind, snapped, r, s); log.append((kind, lab, [[round(x, 1) for x in q] for q in snapped]))
    with open(sys.argv[2], 'w') as o:
        o.write('# RAC RM-OT-05L GO-RS2-REF (clay l_rs2.py -> finish -> brush pass l_rs2_brush.py); cm, Z up, +Y anterior, +X body left\n')
        for v in M.V: o.write('v %.4f %.4f %.4f\n' % tuple(v))
        for t in M.F: o.write('f %d %d %d\n' % tuple(t + 1))
    import json; json.dump(log, open(sys.argv[2].replace('.obj', '_strokes.json'), 'w'), indent=0); print(len(log), 'strokes')

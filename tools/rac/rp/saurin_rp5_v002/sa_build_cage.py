# sa_build_cage.py DESIGN.pkl OUT.npz : coarse authored cage -> fine production cage (sa_layout), tail module attached.
import sys, os, time, pickle, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa_layout as LY, sa_geo as GEO
TARGET = dict(head=0.30, rostrum_cap=0.25, orbit=0.22, eye=0.22, display_root=0.30, neck=0.55, trunk=0.85, pelvis=0.85, shoulder=0.75, upper_arm=0.75, elbow=0.6,
              forearm=0.7, wrist=0.5, palm=0.32, finger=0.25, finger_cap=0.2, finger_web=0.25, thumb=0.25, thumb_cap=0.2, hip=0.85, thigh=0.85, knee=0.7, shin=0.8,
              ankle=0.45, foot=0.4, forefoot=0.35, toe=0.28, toe_cap=0.2, toe_web=0.28)
if __name__ == '__main__':
    d = pickle.load(open(sys.argv[1], 'rb')); t = time.time()
    L = LY.Layout(d['C'], d['Q'], d['qlab'], edge_hint=d['hint'], fixed=d['fixed'], targets=TARGET, arcs=d.get('arcs'))
    L.names = d['name']; L.paths(); print('paths %.0fs' % (time.time() - t), flush=True)
    L.regions(); print('regions %.0fs' % (time.time() - t), flush=True)
    L.chords(); L.build(); print('build %.0fs' % (time.time() - t), flush=True)
    np.savez_compressed(sys.argv[2], V=L.fV, Q=L.fQ, qsrc=L.fQsrc, qlab=np.array(L.fQlab), counts=np.array([[a, b, k] for (a, b), k in L.count.items()]))
    pickle.dump(dict(P={k: v for k, v in L.P.items()}, count=L.count, grid=L.grid, cv=L.cv), open(sys.argv[2] + '.layout.pkl', 'wb'))

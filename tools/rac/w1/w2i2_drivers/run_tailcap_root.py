# RAC W2I2 §15: RM-UB-04 regression under a root-carriage candidate. Imports sa_cand (in-memory root-pitch extension of vary.warp), then runs the
# unchanged W2I1 sa_tailcap2.py with env RPITCH / RLEN (and STATES / TGT).  Usage: RPITCH=.. RLEN=.. python3 run_tailcap_root.py OUT.json
import sys, os, runpy
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_cand  # noqa: F401  (patches vary.warp in memory)
sys.argv = [os.path.join(os.path.dirname(D), 'w2i_drivers', 'sa_tailcap2.py')] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')

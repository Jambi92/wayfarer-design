# ident_finish.py CAND.npz OUT.npz : unchanged-region silhouette rim lock (onto H, only where the identity edit is ~0), then storage-safe pass.
import sys, os, subprocess, numpy as np
R='/tmp/claude-0/rp2/'; P=np.load(sys.argv[1]); V0=np.load(R+'cand_h4_12.npz')['V']
d=np.linalg.norm(P['V']-V0,axis=1)
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
m=1-ss(d/0.03); np.save('/tmp/rl_mask.npy',m)
env=dict(os.environ,MASK='/tmp/rl_mask.npy')
subprocess.run(['/home/claude/stc/bin/python3',R+'tools/rimlock.py',sys.argv[1],'/tmp/rl.npz',R+'hstar.npz','0.3'],check=True,env=env)
subprocess.run(['python3',R+'tools/f32safe.py','/tmp/rl.npz',sys.argv[2]],check=True)

# batchins.py IN.npz OUT.npz "x,y,z;..." : insert vertices one at a time at points (nearest edge), keep only those with 0 coarse self-x
import numpy as np, sys, subprocess
pts=sys.argv[3].split(';'); cur=sys.argv[1]; curc=cur.replace('.npz','_col.npy'); kept=[]
for k,p in enumerate(pts):
    out='/tmp/claude-0/bi_%d.npz'%k
    r=subprocess.run(['python3','edgeins.py',cur,curc,out,p,p],capture_output=True,text=True)
    if r.returncode: print('fail',p); continue
    s=subprocess.run(['/home/claude/stc/bin/python3','selfx_npz.py','--',out],capture_output=True,text=True).stdout
    n=int([l for l in s.splitlines() if l.startswith('SELFX')][0].split()[-1])
    print(p,'selfx',n, r.stdout.splitlines()[0])
    if n==0: cur,curc=out,out.replace('.npz','_col.npy'); kept.append(p)
import shutil; shutil.copy(cur,sys.argv[2]); shutil.copy(curc,sys.argv[2].replace('.npz','_col.npy')); print('kept',len(kept),kept)

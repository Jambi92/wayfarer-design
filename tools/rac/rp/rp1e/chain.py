# chain.py BASE.npz STEPS.json OUT.npz : apply generator steps with ids given in BASE indices; writes OUT + composed remap
import json,sys,subprocess,numpy as np,shutil
base,stp,out=sys.argv[1:4]; steps=json.load(open(stp)); cur=base; comp=np.arange(len(np.load(base)['V']))
for k,(tool,S) in enumerate(steps):
    S=dict(S); m=lambda v:int(comp[v])
    if 'remove' in S: S['remove']=[m(v) for v in S['remove']]
    if 'facev' in S: S['facev']=[[m(v) for v in q] for q in S['facev']]
    sp='/tmp/claude-0/ch_s%d.json'%k; json.dump(S,open(sp,'w')); o='/tmp/claude-0/ch_%d.npz'%k
    r=subprocess.run(['python3',tool,cur,sp,o],capture_output=True,text=True); print(tool,r.stdout.strip()[-80:],r.stderr.strip()[-200:])
    if r.returncode: sys.exit(1)
    rm=np.load(o.replace('.npz','_remap.npy')); comp=np.array([rm[x] if x>=0 else -1 for x in comp]); cur=o
shutil.copy(cur,out); shutil.copy(cur.replace('.npz','_col.npy'),out.replace('.npz','_col.npy')); np.save(out.replace('.npz','_remap.npy'),comp)
print('final',len(np.load(out)['V']))

import json,subprocess,sys,shutil,numpy as np
T=json.load(open(sys.argv[1])); cur=sys.argv[2]; out=sys.argv[3]; R1=float(sys.argv[4]); R2=float(sys.argv[5]); k=0
for ent in T:
    name,c=ent[0],ent[1]; Rs=ent[2:] if len(ent)>2 else (R1,R2)
    ok=True; base=cur
    for R in Rs:
        sp='/tmp/claude-0/rfl_s.json'; json.dump({"centre":c,"R":R},open(sp,'w')); o='/tmp/claude-0/rfl_%d.npz'%k; k+=1
        r=subprocess.run(['python3','refine.py',base,sp,o],capture_output=True,text=True)
        if r.returncode: print(name,'fail',r.stderr[-200:]); ok=False; break
        sx=subprocess.run(['/home/claude/stc/bin/python3','selfx_npz.py','--',o],capture_output=True,text=True).stdout.split()[-1]
        if sx!='0': print(name,'R',R,'selfx',sx,'-> skip level'); break
        base=o
    print(name,r.stdout.strip(),'kept' if base!=cur else 'none'); cur=base
shutil.copy(cur,out); shutil.copy(cur.replace('.npz','_col.npy'),out.replace('.npz','_col.npy')); n=len(np.load(out)['V']); np.save(out.replace('.npz','_remap.npy'),np.arange(len(np.load(sys.argv[2])['V'])))
print('final V',n)

import numpy as np, sys
fs=sys.argv[1:]; sys.argv=['x','cand_s3.npz','/tmp/t.json']
exec(open('/tmp/claude-0/rp2/tools/gate_t367.py').read().split('out = {}')[0])
ref={v:sil(SS['V'],SS['Q'],v) for v in ('front','profile')}; refE={v:sil(E3['V'],E3['Q'],v) for v in ('front','profile')}
for f in fs:
    D=np.load(f); r=[]
    for v in ('front','profile'):
        a=sil(D['V'],D['Q'],v); r+= [round(iou(a,ref[v]),4), round(iou(a,refE[v]),4)]
        if v=='front':
            H=a.shape[0]; ys,xs=np.nonzero(a^ref[v]); z=(H-ys)/3-2; h,_=np.histogram(z,bins=np.arange(0,226,25))
    print(f, 'front S*/E3', r[:2], 'profile S*/E3', r[2:], 'front diff by z/25cm', h)

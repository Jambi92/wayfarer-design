import numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/rp2/v4'); from prof import runs
from PIL import Image
a=np.asarray(Image.open('/tmp/claude-0/rp2/v4/target.png').convert('RGB')).astype(int); m=np.abs(a-np.array([192,190,190])).sum(2)>40
P=m[:,440:700]; crown,sole=71,1376; H=sole-crown; st=217.95
Ms=[(f.split('/')[-1][:-4],np.load(f)['V']) for f in sys.argv[1:]]
def mesh(V,z):
    s=V[(np.abs(V[:,2]-z)<0.5)&(np.abs(V[:,0])<17)]; return s[:,1].max()-s[:,1].min(), s[:,1].min(), s[:,1].max()
print('z    target d/backrel  '+'  '.join('%s d/backrel/front'%n for n,_ in Ms))
tb0=None; b0={}
for z in range(108,178,4):
    y=int(crown+(1-z/st)*H); rs=runs(P[y]); r=max(rs,key=lambda r:r[1]-r[0]); d=(r[1]-r[0])/H*st; back=r[1]/H*st
    if tb0 is None: tb0=back
    row='%3d  %5.1f %5.1f   '%(z,d,back-tb0)
    for n,V in Ms:
        dd,bb,ff=mesh(V,z); b0.setdefault(n,bb); row+='  %5.1f %5.1f %5.1f   '%(dd,-(bb-b0[n]),ff)
    print(row)

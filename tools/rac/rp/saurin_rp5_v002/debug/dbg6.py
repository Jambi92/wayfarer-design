import sys,pickle,os,numpy as np
TAG=sys.argv[1]; CEN=np.array([float(x) for x in sys.argv[2].split(',')]); RAD=float(sys.argv[3]); VIEWS=sys.argv[4]
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v002')
import sa_layout as LY, sa_geo as G, sa_build_cage as B
d=pickle.load(open('design.pkl','rb')); nm=d['name']
if not os.path.exists('dbgL.pkl'):
    L=LY.Layout(d['C'],d['Q'],d['qlab'],edge_hint=d['hint'],fixed=d['fixed'],targets=B.TARGET,arcs=d['arcs']); L.names=nm
    try: L.paths()
    except RuntimeError: pass
    pickle.dump(dict(P=L.P,fails=L.fails,cv=L.cv,res=L.res),open('dbgL.pkl','wb'))
Ld=pickle.load(open('dbgL.pkl','rb'))
os.environ['SA_OUT']='/tmp/claude-0/rt/sa/insp'; sys.argv=[sys.argv[0]]
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v001'); import sa_render as R
V,F=G.V,G.F
m=np.all(np.linalg.norm(V[F]-CEN,axis=2)<RAD,axis=1); Fk=F[m]; u=np.unique(Fk); mp=-np.ones(len(V),int); mp[u]=np.arange(len(u)); Vk=V[u]; Fk=mp[Fk]
col=np.tile([0.8,0.8,0.8],(len(Vk),1))
for e,p in Ld['P'].items():
    q=mp[p]; col[q[q>=0]]=[0.1,0.6,0.1]
for (c,e),x in Ld['res'].items():
    if mp[x]>=0: col[mp[x]]=[0.1,0.1,0.9]
from scipy.spatial import cKDTree; kd=cKDTree(Vk)
for e in Ld['fails']:
    A,Bp=V[Ld['cv'][e[0]]],V[Ld['cv'][e[1]]]
    for t in np.linspace(0,1,25):
        for i in kd.query_ball_point(A+t*(Bp-A),0.12): col[i]=[0.9,0.1,0.1]
for c in Ld['cv']:
    if mp[c]>=0: col[kd.query_ball_point(V[c],0.15)]=[0.95,0.8,0.0]
vs=[(f'v{i}',tuple(float(x) for x in v.split(',')),CEN,RAD*1.5) for i,v in enumerate(VIEWS.split(';'))]
for f in os.listdir(R.TMP):
    if f.startswith(TAG+'_'): os.remove(os.path.join(R.TMP,f))
R.job(TAG,Vk,Fk,col,vs,px=1000); R.run()
from PIL import Image
M=Image.new('RGB',(800*len(vs),800),'white')
for i,v in enumerate(vs): M.paste(Image.open(R.TMP+'/%s_%s.png'%(TAG,v[0])).convert('RGB').resize((800,800)),(800*i,0))
M.save('/tmp/claude-0/rt/sa/insp/%s.png'%TAG)

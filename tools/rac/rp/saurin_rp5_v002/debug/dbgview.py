import sys, os, numpy as np, pickle
TAG=sys.argv[1]; CEN=np.array([float(x) for x in sys.argv[2].split(',')]); RAD=float(sys.argv[3]); VIEWS=sys.argv[4]
os.environ['SA_OUT']='/tmp/claude-0/rt/sa/insp'
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v001'); import sa_render as R
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v002'); import sa_geo as G
d=pickle.load(open('/tmp/claude-0/rt/sa/cage/design.pkl','rb'))
V,F=G.V,G.F
m=np.all(np.linalg.norm(V[F]-CEN,axis=2)<RAD,axis=1); Fk=F[m]; u=np.unique(Fk); mp=-np.ones(len(V),int); mp[u]=np.arange(len(u)); Vk=V[u]; Fk=mp[Fk]
col=np.tile([0.78,0.78,0.78],(len(Vk),1))
from scipy.spatial import cKDTree
kd=cKDTree(Vk)
for e,P in d['arcs'].items():
    for i in kd.query_ball_point(P,0.06): col[i]=[0.2,0.7,0.2]
lab=sys.argv[5] if len(sys.argv)>5 else ''
for i,c in enumerate(d['C']):
    if np.linalg.norm(c-CEN)>RAD: continue
    col[kd.query_ball_point(c,0.12)]=[0.9,0.1,0.1]
vs=[(f'v{i}',tuple(float(x) for x in v.split(',')),CEN,RAD*1.6) for i,v in enumerate(VIEWS.split(';'))]
for f in os.listdir(R.TMP):
    if f.startswith(TAG+'_'): os.remove(os.path.join(R.TMP,f))
R.job(TAG,Vk,Fk,col,vs,px=900); R.run()
from PIL import Image
M=Image.new('RGB',(700*len(vs),700),'white')
for i,v in enumerate(vs): M.paste(Image.open(R.TMP+'/%s_%s.png'%(TAG,v[0])).convert('RGB').resize((700,700)),(700*i,0))
M.save('/tmp/claude-0/rt/sa/insp/%s.png'%TAG)

import sys, os, numpy as np, pickle
TAG=sys.argv[1] if len(sys.argv)>1 else 'c'
os.environ['SA_OUT']='/tmp/claude-0/rt/sa/insp'
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v001'); import sa_render as R
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp5_v002')
import sa_design as SD
D=SD.D; C=np.array(D.C); Q=np.array(D.Q)
pickle.dump(dict(C=C,Q=Q,name=D.name,qlab=D.qlab,hint=D.hint,fixed=D.fixed,pins=D.pins,loops=D.loops),open('/tmp/claude-0/rt/sa/cage/design.pkl','wb'))
tag=TAG
c0=np.array([0,-20,100.]); B=[('front',(0,1,0.05),c0,200),('side',(1,0,0.05),c0,200),('back',(0,-1,0.05),c0,200),('tq',(0.7,0.7,0.2),c0,200)]
for f in os.listdir(R.TMP):
    if f.startswith(tag+'_'): os.remove(os.path.join(R.TMP,f))
R.job(tag+'_body',C,Q,None,B,wire=True,px=900)
for s in ('xpos',):
    hc=SD.LM['wrist_'+s]+np.array([5,2,-8.]); R.job(tag+'_hand',C,Q,None,[('a',(1,0.2,0.1),hc,20),('b',(-1,0.2,0.1),hc,20),('c',(0,1,0),hc,20),('d',(0,-1,0.0),hc,20)],wire=True,px=700)
R.run()
from PIL import Image
for nm,vs in ((tag+'_body',['front','side','back','tq']),(tag+'_hand',['a','b','c','d'])):
    M=Image.new('RGB',(450*len(vs),450),'white')
    for i,v in enumerate(vs): M.paste(Image.open(R.TMP+'/%s_%s.png'%(nm,v)).convert('RGB').resize((450,450)),(450*i,0))
    M.save('/tmp/claude-0/rt/sa/insp/%s.png'%nm)

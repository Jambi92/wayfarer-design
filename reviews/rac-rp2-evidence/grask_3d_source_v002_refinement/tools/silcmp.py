# v6sil.py MESH.npz OUTPREFIX : normalized silhouette overlay vs target (front, profile) + width/depth table
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/rp2/v4'); from prof import runs
from ourprof import sil
from PIL import Image
R='/tmp/claude-0/rp2/'
a=np.asarray(Image.open(R+'v4/target.png').convert('RGB')).astype(int); d_=np.abs(a-np.array([192,190,190])).sum(2); m=d_>40
m[1330:]=d_[1330:]>75     # floor shadow below the ankles: stricter threshold
TF=m[68:1381,0:440]; TP=m[71:1377,440:700]
D=np.load(sys.argv[1]); V=D['V']
out={}
for view,T in (('front',TF),('profile',TP)):
    QQ=D['Q']; QQ=np.c_[QQ,QQ[:,0]] if QQ.shape[1]==3 else QQ
    M,ppc=sil(V,QQ,'front' if view=='front' else 'left'); H=M.shape[0]
    c=int(H-(V[:,2].max()+2)*ppc); s=int(H-(V[:,2].min()+2)*ppc); M=M[c:s+1]
    ys,xs=np.nonzero(M); M=M[:,xs.min():xs.max()+1]
    if view=='profile': M=M[:,::-1]     # mesh profile faces the other way: mirror to face image-left like the target
    # scale mesh mask to target height
    h=T.shape[0]; sc=h/M.shape[0]; Mi=Image.fromarray((M*255).astype(np.uint8)).resize((max(1,int(M.shape[1]*sc)),h),Image.NEAREST); M=np.array(Mi)>127
    if view=='front':
        # align midlines: target figure centre = mean x of rows 400-800 centre runs; mesh centre = width/2
        tc=np.median([np.mean(np.nonzero(T[y])[0]) for y in range(300,900,20)]); mc=M.shape[1]/2
    else:
        # profile: align on the back of the calf/heel region (posterior edge at 85-90 %)
        tc=np.median([np.nonzero(T[y])[0].max() for y in range(int(.84*h),int(.9*h),5)]); mc=np.median([np.nonzero(M[y])[0].max() for y in range(int(.84*h),int(.9*h),5)])
    W=int(max(T.shape[1],M.shape[1])*1.4); img=np.full((h,W,3),255,np.uint8); off=W//2
    tx=lambda x,c0: (x-c0+off).astype(int)
    for y in range(h):
        xt=np.nonzero(T[y])[0]; xm=np.nonzero(M[y])[0]
        a_=np.zeros(W,bool); b_=np.zeros(W,bool)
        if len(xt): a_[np.clip(tx(xt,tc),0,W-1)]=True
        if len(xm): b_[np.clip(tx(xm,mc),0,W-1)]=True
        img[y,a_&~b_]=(220,60,60); img[y,b_&~a_]=(60,90,220); img[y,a_&b_]=(150,150,150)
    Image.fromarray(img).save(sys.argv[2]+'_%s.png'%view)
    st=dict(front=[('head',0.06),('neck',0.135),('shoulders',0.185),('upper_ribcage',0.25),('lower_ribcage',0.33),('waist',0.40),('pelvis',0.48),('proximal_thigh',0.56),('mid_thigh',0.62),('knee',0.69),('calf_max',0.76),('ankle',0.91),('forefoot',0.985)],
            profile=[('head',0.06),('neck',0.14),('chest',0.25),('abdomen',0.40),('glute',0.49),('thigh',0.58),('calf',0.76),('foot',0.985)])[view]
    tab={}
    for nm,t in st:
        y=int(t*h); rt=runs(T[y]); rm=runs(M[y])
        def w(rs,full=False):
            if not rs: return 0
            return (rs[-1][1]-rs[0][0])/h
        def widest(rs): return max((b-a for a,b in rs),default=0)/h
        tab[nm]=dict(t=t,target_full=w(rt),mesh_full=w(rm),target_widest_run=widest(rt),mesh_widest_run=widest(rm))
    out[view]=tab
json.dump(out,open(sys.argv[2]+'_table.json','w'),indent=1)
for v in out:
    print(v); print('%-15s %5s  full: tgt  mesh  ratio | widest run: tgt  mesh  ratio'%('station','t'))
    for k,r in out[v].items(): print('%-15s %5.3f  %.3f %.3f %.2f | %.3f %.3f %.2f'%(k,r['t'],r['target_full'],r['mesh_full'],r['mesh_full']/max(r['target_full'],1e-6),r['target_widest_run'],r['mesh_widest_run'],r['mesh_widest_run']/max(r['target_widest_run'],1e-6)))

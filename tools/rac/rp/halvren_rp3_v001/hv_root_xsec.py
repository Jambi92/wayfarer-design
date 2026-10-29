# hv_root_xsec.py OUT.png LABEL=BRANCH.npz ... (env XS_U=u1,u2,... root-frame heights, cm): Halvren root visual-integration order diagnosis -- horizontal
# cross-sections (constant root-frame u) of the left ear root in the root frame (x = b posterior, y = n lateral), coloured by part (front orange, back violet,
# rim yellow, cuff blue, transition green, v005 head grey): shows the pedestal / cliff behind the pinna and the raised cuff tab beside the lobe.
import sys,json,numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out=sys.argv[1]; items=[a.split('=') for a in sys.argv[2:]]; import os; US=[float(x) for x in os.environ.get('XS_U','-1.6,-2.0,-2.3,-2.6,-2.8').split(',')]
COL=dict(front='#d08060',back='#9070c0',rim='#d0b040',cuff='#5090d0',transition='#40b040',v005='#888888')
fig,axs=plt.subplots(len(items),len(US),figsize=(4*len(US),3.6*len(items)),squeeze=False)
for r,(t,p) in enumerate(items):
    z=np.load(p); rec=json.load(open(p.replace('.npz','.json'))); fr=rec['sides']['l']['frame']; O,n,b,u=[np.array(fr[k]) for k in 'Onbu']
    V=z['V']; Q=z['Q']; P=z['part']; X=np.c_[(V-O)@b,(V-O)@u,(V-O)@n]; near=np.linalg.norm(V-O,axis=1)<5; F=Q[near[Q].all(1)]
    for c,u0 in enumerate(US):
        ax=axs[r,c]
        for q in F:
            pts=[]
            for k in range(4):
                a,bb=X[q[k]],X[q[(k+1)%4]]
                if (a[1]-u0)*(bb[1]-u0)<0: s=(u0-a[1])/(bb[1]-a[1]); pts.append(a+s*(bb-a))
            if len(pts)==2:
                pp=P[q]; pr=[x for x in pp if x!='v005']; col=COL[pr[0]] if pr else COL['v005']
                ax.plot([pts[0][0],pts[1][0]],[pts[0][2],pts[1][2]],c=col,lw=1.5)
        ax.set_aspect('equal'); ax.set_xlim(-2.5,3.5); ax.set_ylim(-1.5,2.5); ax.grid(alpha=.3); ax.set_title('%s u=%.1f'%(t,u0),fontsize=9)
fig.tight_layout(); fig.savefig(out,dpi=60)

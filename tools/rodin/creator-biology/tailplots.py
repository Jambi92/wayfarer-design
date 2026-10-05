import json, pickle, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, sys
sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import evaluate as EV
S=json.load(open('sweep.json')); G=json.load(open('tailgrid.json')); PR=pickle.load(open('profiles.pkl','rb'))
BG='#1b1b20'; AX='#24242a'
def sty(a):
    a.set_facecolor(AX); a.tick_params(colors='#ccc'); [q.set_color('#666') for q in a.spines.values()]; a.grid(color='#3a3a44'); a.title.set_color('#eee'); a.xaxis.label.set_color('#ccc'); a.yaxis.label.set_color('#ccc')
# 1. normalized profiles
fig,ax=plt.subplots(1,3,figsize=(21,6.2),dpi=110); fig.patch.set_facecolor(BG)
sets=[('Length / base / composition',['ref','tn_lo','tn_hi','tb_lo','tb_hi','mu_hi','fa_hi']),('Taper profile',['ref','tt_lo','tt_hi','x21','x22']),('Coupling cases',['ref','x03','x04','x26','x25','x20'])]
cols=['#e8e8e8','#5aa9e6','#f28e2b','#7bc96f','#e15759','#b07aa1','#edc948','#9c755f']
for a,(tt,ids) in zip(ax,sets):
    for c,i in zip(cols,ids):
        if i not in PR: continue
        s,A=PR[i]; Lt=s.max(); Ar=np.interp(Lt,s,A)
        a.plot(s/Lt,A/Ar,color=c,lw=2.4 if i=='ref' else 1.8,label='%s: %s'%(i,S[i]['label']))
    a.set_title(tt); a.set_xlabel('normalized length from tip (1 = free-tail root)'); a.set_ylabel('area / root area'); sty(a)
    a.axhspan(0,0,color='none'); a.legend(fontsize=8.5,facecolor=AX,labelcolor='#ddd',loc='upper left')
    a.plot([0.5,0.5],[EV.RULES[4][1],EV.RULES[4][2]],color='#ff5050',lw=5,alpha=0.5)
plt.tight_layout(); plt.savefig('P_tail_profiles.png',facecolor=BG)
# 2. coupling envelope from the grid
fig,ax=plt.subplots(1,3,figsize=(21,6.5),dpi=110); fig.patch.set_facecolor(BG)
for a,t in zip(ax,(0.85,1.0,1.15)):
    g=[r for r in G if abs(r['t']-t)<1e-6]
    for r in g:
        m=dict(r); m['height']=EV.HREF; m['lean_req_deg']=r['lean_req_deg']; m['rostral_index']=0.288; m['head_len_ratio']=0.17; m['thorax_d_over_w']=0.88
        d,hard,soft=EV.classify(m)
        col='#59a14f' if not hard and not soft else ('#edc948' if not hard else '#e15759')
        a.scatter(r['tail_len_pct'],r['b'],s=260,c=col,edgecolors='#111',zorder=3)
        a.text(r['tail_len_pct'],r['b'],'%.2f'%d['tail_RSI_n'],fontsize=7,ha='center',va='center',color='#111',zorder=4)
    a.axvspan(55,80,color='#ffffff',alpha=0.05); a.axvline(55,color='#888',ls='--'); a.axvline(80,color='#888',ls='--')
    a.set_title('Tail taper/fullness x%.2f: green = soft core, yellow = valid edge, red = invalid'%t,fontsize=10.5); a.set_xlabel('tail length (% standing height)'); a.set_ylabel('tail base multiplier'); sty(a)
plt.tight_layout(); plt.savefig('P_tail_envelope.png',facecolor=BG)
# 3. balance
fig,ax=plt.subplots(1,2,figsize=(16,6),dpi=110); fig.patch.set_facecolor(BG)
for j,d in S.items():
    m=EV.derived(d['metrics']); a=ax[0]; c='#e15759' if m['d_lean']>3 else ('#edc948' if m['d_lean']>1.5 else '#59a14f')
    a.scatter(100*m['tail_mass_share'],m['lean_req_deg'],c=c,s=40,edgecolors='#111'); 
    if abs(m['d_lean'])>1.0: a.text(100*m['tail_mass_share']+0.1,m['lean_req_deg'],j,fontsize=7,color='#ccc')
ax[0].axhline(EV.REF['lean_req_deg'],color='#ddd',ls='--'); ax[0].axhline(EV.REF['lean_req_deg']+3,color='#e15759',ls=':')
ax[0].set_xlabel('free-tail volume share of body (%)'); ax[0].set_ylabel('forward lean needed to stand over the feet (deg)'); ax[0].set_title('Counterbalance: every variant (uniform density)'); sty(ax[0])
for t,c in ((0.85,'#5aa9e6'),(1.0,'#e8e8e8'),(1.15,'#f28e2b')):
    for b,ls in ((0.85,':'),(1.0,'-'),(1.15,'--')):
        g=sorted([r for r in G if abs(r['t']-t)<1e-6 and abs(r['b']-b)<1e-6],key=lambda r:r['k'])
        ax[1].plot([r['tail_len_pct'] for r in g],[r['lean_req_deg'] for r in g],color=c,ls=ls,label='taper x%.2f base x%.2f'%(t,b))
ax[1].axhline(EV.REF['lean_req_deg']+3,color='#e15759',ls=':'); ax[1].set_xlabel('tail length (% H)'); ax[1].set_ylabel('lean needed (deg)'); ax[1].set_title('Lean vs tail length / base / fullness'); sty(ax[1]); ax[1].legend(fontsize=7,facecolor=AX,labelcolor='#ddd',ncol=3)
plt.tight_layout(); plt.savefig('P_balance.png',facecolor=BG); print('ok')

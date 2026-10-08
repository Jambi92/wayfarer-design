import sys, os, json, glob
sys.path.insert(0,'w1g_drivers'); import gn3
S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
gn3.SKP = S + '/s7n/w1i_base'
P={}
for n in ["GON","GONF","GON3","GON4","GON5","GOB","GOBF","GOB3","GOB4","GOB5","GOB6","GOB7","GOX12_92","GOX12_935","GOX12_89","GOX12_86","GOX14_98","GOX14_97","GOX14_95","GOX14_92","GOX14_89","GOD14_95","GOD14_9","GOD14_85","GON3_218","GON4_218","GON5_218","GOB7_218","GOD14_9_218","GO14_218"]:
    rec=json.load(open(S+'/w2d/b/%s/%s_w2d.json'%(n,n)))
    rows=[x for x in gn3.checks("GO",n,wd=S+"/w2d/b/"+n) if (x['cand']=='GO' or x.get('b')=='GO') and x['result'] not in ('REPORT','NOT RUN')]
    bad=[x for x in rows if x['result']!='PASS']
    P[n]={"height_macro":rec["height_macro"],"stature":rec["stature_r6"],"frame":rec["frame"],"skeletal_rows":len(rows),
          "non_pass":[{"check":x['check'],"result":x['result'],"by_t":{t:[w['va'],w['vb']] for t,w in x['by_t'].items()}} for x in bad]}
    print(n, len(bad), flush=True)
json.dump(P, open(S+'/w2d/out/probes.json','w'), indent=1, default=float)
C={}
for f in sorted(glob.glob(S+'/w2d/b/*/*_w2d.json')):
    d=json.load(open(f)); C[d["name"]]=d
json.dump(C, open(S+'/w2d/out/construction.json','w'), indent=1, default=float); print(len(C),'construction')

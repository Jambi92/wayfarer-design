import sys, os; sys.path.insert(0,'w1g_drivers'); import gn3
S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
R=lambda v: None if v is None else round(v,4)
for n in sys.argv[1:]:
    rows=gn3.checks("GO",n,wd=S+"/w2d/b/"+n)
    bad=[x for x in rows if x['result'] not in ('PASS','NOT RUN') and not str(x['result']).startswith('REPORT') and (x['cand']=='GO' or x.get('b')=='GO')]
    print(n,'nonpass',len(bad), flush=True)
    for x in bad: print('  ',x['check'][:70],x['result'],{t:(R(v.get('va')),R(v.get('vb'))) for t,v in x['by_t'].items()})

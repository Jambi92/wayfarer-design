import numpy as np, json, sys
# usage: movegen.py hide.json moves.json view(cx,cy,cyw,czw,s,axis) OUT
hid=json.load(open(sys.argv[1])); vis=hid['vis']
mv={int(k):np.array(v) for k,v in json.load(open(sys.argv[2])).items()}
cx,cy,ah,av,s=[float(x) for x in sys.argv[3].split(',')]; hax,vax,hs=[int(x) for x in sys.argv[4].split(',')]
out=sys.argv[5]; minsep=float(sys.argv[6]) if len(sys.argv)>6 else 10
U=np.load(sys.argv[7] if len(sys.argv)>7 else 'ui_v005.npz')['V'].copy()
todo=[k for k in mv if k in set(vis) and np.linalg.norm(U[k]-mv[k])>0.01]
print('todo',len(todo),'of',len(mv))
def scr(p): return np.array([cx+hs*(p[hax]-ah)*s, cy-(p[vax]-av)*s])
def fmt(v):
    s='%.4f'%(v/100.0)
    s=s.replace('0.','.',1) if s.startswith('0.') else s.replace('-0.','-.',1)
    return s
keys={'.':'period','-':'minus'}
acts=[];order=[]
cur={k:U[k].copy() for k in vis}
while todo:
    best=None
    for k in todo:
        p=scr(cur[k]); d=min(np.linalg.norm(scr(cur[j])-p) for j in vis if j!=k)
        if not (5<p[0]<1035 and 50<p[1]<700) or (p[0]>970 and p[1]<190): d=-1
        if best is None or d>best[0]: best=(d,k,p)
    d,k,p=best
    if d<minsep: print('stuck: remaining',len(todo),'best sep',round(d,1)); break
    order.append((k,round(d,1)))
    acts.append({"action":"left_click","coordinate":[int(round(p[0])),int(round(p[1]))]})
    acts.append({"action":"double_click","coordinate":[1110,92]}); acts.append({"action":"wait","duration":0.5}); acts.append({"action":"key","text":"ctrl+a"})
    for ci,c in enumerate(mv[k]):
        if ci>0: acts.append({"action":"key","text":"Tab"})
        for ch in fmt(c): acts.append({"action":"key","text":keys.get(ch,ch)})
    acts.append({"action":"key","text":"Return"})
    cur[k]=mv[k].copy(); todo.remove(k)
json.dump(acts,open(out,'w')); json.dump(order,open(out.replace('.json','_order.json'),'w'))
print('verts',len(order),'min sep',min(o[1] for o in order),'actions',len(acts))

import json,sys
T=json.load(open(sys.argv[1])); T.update(correctives=True, corr_rounds=8, crease_iters=20, crease_grow=6, corr_max_mm=10.0)
for kv in sys.argv[3:]:
    k,v=kv.split('='); T[k]=json.loads(v)
json.dump(T,open(sys.argv[2],'w'),indent=1)

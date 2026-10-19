# maphole.py HOLE_on_base.json EAR_json_of_applied_design OUT.json : map face/vertex ids from the base cage to the cage after an ear design
import json, sys, bisect
H=json.load(open(sys.argv[1])); E=json.load(open(sys.argv[2]))
rem=sorted(E['removed']); hole=sorted(E['hole'])
assert not set(H['reg'])&set(hole)
mv=lambda v: v-bisect.bisect_left(rem,v)
mf=lambda f: f-bisect.bisect_left(hole,f)
assert not set(H['loop'])&set(rem)
json.dump(dict(reg=[mf(f) for f in H['reg']],loop=[mv(v) for v in H['loop']]),open(sys.argv[3],'w'))

# mapids.py DESIGN_JSON HOLE_JSON(applied) IN_HOLE_JSON IN_RINGS_JSON OUT_HOLE OUT_RINGS : map face/vertex ids from the base cage to the cage after one applied design
import json, sys, bisect
E=json.load(open(sys.argv[1])); H=json.load(open(sys.argv[2]))['reg']
rem=sorted(E['removed']); hole=sorted(H)
mv=lambda v: v-bisect.bisect_left(rem,v); mf=lambda f: f-bisect.bisect_left(hole,f)
h=json.load(open(sys.argv[3]))['reg']; assert not set(h)&set(hole)
R=json.load(open(sys.argv[4])); assert not set(v for r in R for v in r)&set(rem)
json.dump(dict(reg=[mf(f) for f in h]),open(sys.argv[5],'w')); json.dump([[mv(v) for v in r] for r in R],open(sys.argv[6],'w'))

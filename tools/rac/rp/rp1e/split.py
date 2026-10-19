import json,sys
a=json.load(open(sys.argv[1])); r0,r1=int(sys.argv[2]),int(sys.argv[3])
blocks=[];cur=None
for x in a:
    if x['action']=='left_click': cur=[];blocks.append(cur)
    cur.append(x)
out=[{"action":"mouse_move","coordinate":[700,450]}]
for b in blocks[r0:r1]: out+=b
out+=[{"action":"mouse_move","coordinate":[1000,650]},{"action":"wait","duration":0.3},{"action":"screenshot","scale":0.5}]
print(json.dumps(out))

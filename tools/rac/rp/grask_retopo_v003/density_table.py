# density_table.py OUT.md OUT.json : density study table (x1, x2 raw, v002, v001 reference)
import json, sys, numpy as np
R='/tmp/claude-0/rt/'; J=lambda f: json.load(open(R+f))
rows=[('x1 (cage21 x1)','L1'),('x2 raw (cage21 x2)','L2v'),('v002 (cage27 x2)','v002'),('v003 selected (cage29 x2)','v003_rb'),('v001 reference (cage21 x3)','final')]
T1=(0.5,1.5,3.0); T2=(0.3,0.8,1.5); out={}
for lab,t in rows:
    g=J(t+'_gate.json'); d=J(t+'_dev.json'); la=J(t+'_loops_audit.json') if t!='final' else J('final_loops_audit_v2method.json')
    io=J(t+'_iou.json'); lmf=t+'_lmdrift.json' if t!='final' else 'final_lmdrift2.json'; lm=J(lmf)
    def zp(z,lim):
        r=[]
        for side in ('src_to_prod','prod_to_src'):
            s=d[z][side]; r.append(s['median']<=lim[0] and s['p95']<=lim[1] and s['max']<=lim[2])
        return all(r)
    t1=zp('body_general',T1); t2={z:zp(z,T2) for z in ('head_face','ears','hand_l','hand_r','foot_l','foot_r')}
    mx=lambda z: max(d[z]['src_to_prod']['max'],d[z]['prod_to_src']['max'])
    a=np.array; zq=g['zones']
    hard=sum(1 for _ in [0]) 
    try: hq=J(t+'_hard.json'); nh=sum(c['n'] for c in hq['clusters'])
    except Exception: nh=None
    sxf=R+t+'_sx.npy'; 
    try: nsx=int(len(np.load(sxf)))
    except Exception: nsx=0
    iou3={k:io['views'][k]['iou'] for k in io['views'] if k in ('front','profile_left','profile_right','rear')}
    fails=[k for k,v in la['joints'].items() if not v['pass']]
    out[lab]=dict(verts=g['verts'],quads=g['quads'],tri_equiv=2*g['quads'],
      mean_edge_mm={z:round(v['edge_mean_mm'],2) for z,v in zq.items()},density_pass={z:v['density_pass'] for z,v in zq.items()},
      T1=dict(pass_=t1,max_mm=round(mx('body_general'),2)),T2=dict(pass_=all(t2.values()),zones_failing=[z for z,v in t2.items() if not v],max_mm={z:round(mx(z),2) for z in t2}),
      T3=dict(stature_diff_mm=round(g['T3_stature_diff_mm'],3),bbox_maxdiff_mm=round(g['T3_bbox_maxdiff_mm'],3),pass_=abs(g['T3_stature_diff_mm'])<=1.0 and g['T3_bbox_maxdiff_mm']<=2.0),
      T6=dict(max_mm=round(lm['max_mm'],2),over_1_5=lm['over_1_5mm'],pass_=lm['max_mm']<=1.5),T7=dict(min_iou=round(min(iou3.values()),5),pass_=min(iou3.values())>=0.995),
      loops=dict(pass_=la['all_pass'],failing=fails),quality=dict(hard_quads=nh,angle_45_135_pct=round(g['angle_in_45_135_pct_all'],2),aspect_le4_pct=round(g['aspect_le4_pct_all'],2),
      min_angle=round(min(v['angle_min'] for v in zq.values()),1),max_angle=round(max(v['angle_max'] for v in zq.values()),1),max_aspect=round(max(v['aspect_max'] for v in zq.values()),2)),
      self_intersection_pairs=nsx)
    MP={'v002':'v002_rb'}.get(t,t); zz=np.load(R+MP+'.npz'); Vv=zz['V']; Qq=zz['Q']
    el=np.stack([np.linalg.norm(Vv[Qq[:,(i+1)%4]]-Vv[Qq[:,i]],axis=1) for i in range(4)],1); err=el.max(1)/el.min(1)
    pf=[k for k,v in la['joints'].items() if v.get('loops_path_count',99)<v['required']]
    out[lab]['edge_ratio']=dict(max=round(float(err.max()),2),over_8=int((err>8).sum()),over_10=int((err>10).sum())); out[lab]['path_count_failing']=pf
    o=out[lab]; o['verdict']='PASS' if (o['T1']['pass_'] and o['T2']['pass_'] and o['T3']['pass_'] and o['T6']['pass_'] and o['T7']['pass_'] and o['loops']['pass_'] and all(o['density_pass'].values()) and (nh==0) and nsx==0 and o['edge_ratio']['over_10']==0) else 'FAIL'
json.dump(out,open(sys.argv[2],'w'),indent=1)
P=lambda b: 'PASS' if b else 'FAIL'
L=['| | '+' | '.join(r[0] for r in rows)+' |','|---|'+'---|'*len(rows)]
def row(name,f): L.append('| '+name+' | '+' | '.join(f(out[r[0]]) for r in rows)+' |')
row('Vertices',lambda o:'{:,}'.format(o['verts'])); row('Quads',lambda o:'{:,}'.format(o['quads'])); row('Triangle equivalent',lambda o:'{:,}'.format(o['tri_equiv']))
for z in ('head_face','ears','hands','feet','trunk_limbs'): row('Mean edge %s (mm)'%z,lambda o,z=z:'%.2f %s'%(o['mean_edge_mm'][z],'' if o['density_pass'][z] else '**over ceiling**'))
row('T-1 body max (mm)',lambda o:'%s (%.2f)'%(P(o['T1']['pass_']),o['T1']['max_mm']))
row('T-2 identity zones',lambda o:P(o['T2']['pass_'])+(' — fails '+', '.join(o['T2']['zones_failing']) if o['T2']['zones_failing'] else '')+' (max %.2f)'%max(o['T2']['max_mm'].values()))
row('T-3 stature / bbox (mm)',lambda o:'%s (%.2f / %.2f)'%(P(o['T3']['pass_']),o['T3']['stature_diff_mm'],o['T3']['bbox_maxdiff_mm']))
row('T-6 landmark max (mm)',lambda o:'%s (%.2f)'%(P(o['T6']['pass_']),o['T6']['max_mm']))
row('T-7 min IoU front/profile/rear',lambda o:'%s (%.4f)'%(P(o['T7']['pass_']),o['T7']['min_iou']))
row('Loop audit (69 joints)',lambda o:P(o['loops']['pass_'])+('' if o['loops']['pass_'] else ' — %d fail'%len(o['loops']['failing'])))
row('Hard-limit quads',lambda o:str(o['quality']['hard_quads']))
row('Quads 45–135° / aspect ≤4 (%)',lambda o:'%.1f / %.1f'%(o['quality']['angle_45_135_pct'],o['quality']['aspect_le4_pct']))
row('Worst angle min / max (°), max aspect',lambda o:'%.1f / %.1f, %.2f'%(o['quality']['min_angle'],o['quality']['max_angle'],o['quality']['max_aspect']))
row('Edge ratio longest/shortest: max, >8, >10',lambda o:'%.2f, %d, %d'%(o['edge_ratio']['max'],o['edge_ratio']['over_8'],o['edge_ratio']['over_10']))
row('Joints failing the path-only count (diagnostic; see ring evidence)',lambda o:', '.join(o['path_count_failing']) or 'none')
row('Self-intersection pairs',lambda o:str(o['self_intersection_pairs']))
row('**Verdict**',lambda o:'**'+o['verdict']+'**')
open(sys.argv[1],'w').write('\n'.join(L)+'\n'); print('\n'.join(L))

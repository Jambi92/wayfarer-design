# RAC W1i driver AS RUN: contour / flank flare / arm tests / continuity profiles, ocular, ears, render sheets (order §7)
cd /home/claude/wayfarer-design/tools/rac/w1
S=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad; F=$S/w1f; G=$S/w1g; R=/home/claude/wayfarer-design/reviews
EV=$S/w1i/ev; SH=$S/w1i/sheets; mkdir -p $EV $SH
python3 -c "
import json, sys, profile_bump as PB, arm_clearance as AC
sys.path.insert(0, 'w1i_drivers'); import gn6
S='$S'; F=S+'/w1f'; G=S+'/w1g'; R='$R'
B={'MF-M-R':F+'/final/MF-M-R_r6.npz','SK':F+'/final/SK_r6.npz','SG':F+'/final/SG_r6.npz','DU-NAT':F+'/final/DU-NAT_r6.npz','GR':G+'/final/GR_r6.npz',
 'GO W1g':R+'/rac-w1g-evidence/geometry/GO_r6.npz','GO W1h':R+'/rac-w1h-evidence/geometry/GO_r6.npz','GO W1i':G+'/final/GO_r6.npz',
 'GO W1h skeleton':R+'/rac-w1h-evidence/skeleton/GO-LEAN_r6.npz','GO W1i skeleton':G+'/final_lean/GO-LEAN_r6.npz',
 'AE':F+'/final/AE_r6.npz','VA':F+'/final/VA_r6.npz','FN':F+'/final/FN_r6.npz',
 'GOR-BODY-02 (208)':G+'/stress/GOR-BODY-02_r6.npz','GO 215':G+'/stress/GO-H215_r6.npz','GO 222':G+'/stress/GO-H222_r6.npz','GOR-BODY-03 (251)':G+'/stress/GOR-BODY-03_r6.npz',
 'GOR-BODY-04':G+'/stress/GOR-BODY-04_r6.npz','GOR-BODY-05 (Broad)':G+'/stress/GOR-BODY-05_r6.npz','GOR-BODY-12':G+'/stress/GOR-BODY-12_r6.npz','GOR-BODY-14':G+'/stress/GOR-BODY-14_r6.npz','GOR-BODY-16':G+'/go16/GOR-BODY-16_r6.npz'}
out={'contour':{},'arm_clearance':{},'arm_tube':{},'continuity':{}}
for k,p in B.items():
  out['contour'][k]={'chest_lead':PB.chest_lead(p),'buttock_lead':PB.buttock_lead(p),'flank_flare':PB.flank_flare(p)['flank_flare']}
  c=AC.clear(p)['l']; out['arm_clearance'][k]={**c,'signed_clearance_both_sides_cm':AC.signed_clearance(p)}
  out['arm_tube'][k]=AC.arm_tube_test(p)
  out['continuity'][k]=gn6.cont(p.replace('_r6.npz','_rest.npz') if __import__('os').path.exists(p.replace('_r6.npz','_rest.npz')) else p)
  print(k, round(out['contour'][k]['flank_flare'],4), c['verts_inside_trunk_section'], round(out['arm_clearance'][k]['signed_clearance_both_sides_cm'],3), out['arm_tube'][k]['l']['trunk_verts_inside_arm_tube'], out['arm_tube'][k]['r']['trunk_verts_inside_arm_tube'], {a:round(b,3) for a,b in out['continuity'][k].items()})
out['continuity_limits']=gn6.LIM; out['continuity_references']=gn6.RC
out['low_comp_waist']={'GOR-BODY-16 W1i':gn6.waist_rise(G+'/go16/GOR-BODY-16_rest.npz'),'GOR-BODY-16 W1h':gn6.waist_rise(S+'/w1i/W1h_GOR-BODY-16_rest.npz'),'MF-M-R low composition':gn6.waist_rise(F+'/low/MF-M-R-LOW_rest.npz'),'SK low composition':gn6.waist_rise(F+'/low/SK-LOW_rest.npz')}
out['continuity'].pop('GO W1g', None); out['continuity']['GO W1h skeleton']=gn6.cont(S+'/w1i/W1h_GO-LEAN_rest.npz'); out['continuity']['GO W1h']=gn6.cont(S+'/w1i/W1h_GO_rest.npz')
json.dump(out,open('$EV/contour_clearance.json','w'),indent=1,default=float)
" > $EV/contour.log 2>&1
rm -rf $G/cf; mkdir -p $G/cf; for f in $F/final/*_rest.npz $F/final/*_r6.npz; do ln -sf $f $G/cf/; done; for x in GR GO; do for s in rest r6; do ln -sf $G/final/${x}_$s.npz $G/cf/; done; done; cp $G/cand/*_meas.json $G/cf/
python3 ocular_w1f.py $G/cf $EV/ocular_w1i.json FN AE VA PK-NAT CG-NAT DU-NAT GR GO MF-F-R > $EV/ocular.log 2>&1
mkdir -p $S/w1i/ears; python3 ear_attach_sheet.py $G/cf $S/w1i/ears > $EV/ears_attach.log 2>&1
python3 ear_checks.py $R/rac-w1e-evidence/ears/ear_families_v2.json $S/w1i/ears/ears_attached.json $G/cf $EV/ear_checks.json > $EV/ears.log 2>&1
W=w1i_drivers/sheet4.py
python3 $W $SH/go_stature_series_4view.jpg --cols 1 --pp 1.6 "GOR-BODY-02 210.8 cm (208 cm donor)=$G/stress/GOR-BODY-02_r6.npz" "GO 215 cm=$G/stress/GO-H215_r6.npz" "GO 222 cm=$G/stress/GO-H222_r6.npz" "GO W1i reference 229 cm=$G/final/GO_r6.npz" "GOR-BODY-03 253.0 cm=$G/stress/GOR-BODY-03_r6.npz"
python3 $W $SH/go_frames_composition_4view.jpg --cols 1 --pp 1.6 "GO W1i reference=$G/final/GO_r6.npz" "GOR-BODY-04 Narrow frame=$G/stress/GOR-BODY-04_r6.npz" "GOR-BODY-05 Broad frame=$G/stress/GOR-BODY-05_r6.npz" "GOR-BODY-16 low composition 0.25 / 0.25=$G/go16/GOR-BODY-16_r6.npz" "GO W1i skeleton (minimum composition)=$G/final_lean/GO-LEAN_r6.npz" "GO W1h reference (before)=$R/rac-w1h-evidence/geometry/GO_r6.npz"
python3 $W $SH/references_4view.jpg --cols 1 --pp 1.6 "GO W1i 229 cm=$G/final/GO_r6.npz" "SK 208 cm=$F/final/SK_r6.npz" "GR 218 cm=$G/final/GR_r6.npz" "MF-M-R 173 cm=$F/final/MF-M-R_r6.npz" "DU-NAT=$F/final/DU-NAT_r6.npz"
python3 $W $SH/trunk_crop_noarms.jpg --crop trunk --noarms --pp 2.6 --cols 2 "GO W1h (before)=$R/rac-w1h-evidence/geometry/GO_r6.npz" "GO W1i=$G/final/GO_r6.npz" "GO W1h skeleton (before)=$R/rac-w1h-evidence/skeleton/GO-LEAN_r6.npz" "GO W1i skeleton=$G/final_lean/GO-LEAN_r6.npz" "GOR-BODY-16 low composition=$G/go16/GOR-BODY-16_r6.npz" "GOR-BODY-02 210.8 cm (208 cm donor)=$G/stress/GOR-BODY-02_r6.npz" "GOR-BODY-03 253.0 cm=$G/stress/GOR-BODY-03_r6.npz" "GOR-BODY-04 Narrow=$G/stress/GOR-BODY-04_r6.npz" "GOR-BODY-05 Broad=$G/stress/GOR-BODY-05_r6.npz" "SK=$F/final/SK_r6.npz" "SK skeleton=$F/final_lean/SK-LEAN_r6.npz" "GR=$G/final/GR_r6.npz" "MF-M-R=$F/final/MF-M-R_r6.npz" "DU-NAT=$F/final/DU-NAT_r6.npz"
python3 $W $SH/axilla_close.jpg --crop axilla --pp 5 "GO W1i reference=$G/final/GO_r6.npz" "GOR-BODY-02 210.8 cm (208 cm donor)=$G/stress/GOR-BODY-02_r6.npz" "GOR-BODY-03 253.0 cm=$G/stress/GOR-BODY-03_r6.npz" "GOR-BODY-05 Broad=$G/stress/GOR-BODY-05_r6.npz" "SK (accepted reference)=$F/final/SK_r6.npz"
python3 skeleton_sheet.py $SH/skeletal_proxy_sheet.jpg "W1i skeletal proxy (CIB) over reference bodies" $F/final/MF-M-R_r6.npz $F/final_lean/MF-M-R-LEAN_r6.npz $G/final/GO_r6.npz $G/final_lean/GO-LEAN_r6.npz $G/final/GR_r6.npz $G/final_lean/GR-LEAN_r6.npz GR
python3 side_lineup.py $G/cf $SH/side_lineup.jpg MF-M-R FN AE VA HV SK GR GO DU-NAT PK-NAT CG-NAT
cp $EV/alpc8.jpg $SH/ 2>/dev/null; cp $S/w1i/ears/ears_attached_sheet.jpg $SH/
echo POST3 DONE

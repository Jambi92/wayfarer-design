import sys,numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_pose as SP,sa6_fit as FT,sa6_correctives as CC
P_=['shoulder_abd45_xpos','shoulder_abd90_xpos','shoulder_flex60_xpos','shoulder_abd90_xneg','shoulder_flex60_xneg','elbow_130_xpos','hip_flex70_xpos','knee_90_xpos','neck_rot_40','neck_flex_30','trunk_twist_30','lower_axial_flex_25','tail_root_lateral_30','tail_root_vertical_25','tail_twist_30','shoulder_flex60_xpos_rp5lit','hip_flex70_xpos_rp5lit']
for wf in sys.argv[1:]:
    R=SP.Rig('M',wf);PS=FT.pose_set(R);S=CC.Solver(R);V0=S.body_volume(R.V);tf=0;tv=0;out=[]
    for pn in P_:
        T=R.pose(PS[pn]);P=R.skin(T);f=(R.relcos(P,T)<0).sum();dv=S.body_volume(P)-V0;tf+=f;tv+=abs(dv);out.append('%s:%d/%.0f'%(pn.replace('shoulder','sh').replace('_xpos','L').replace('_xneg','R')[:14],f,dv))
    print(wf,'TOTAL flips',tf,'sum|dV|',round(tv),' '.join(out),flush=True)

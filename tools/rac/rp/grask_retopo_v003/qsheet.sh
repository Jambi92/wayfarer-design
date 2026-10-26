# qsheet.sh MESH TAG OUTDIR : quad-quality crops (hard red, soft orange) at the repair regions and worst remaining quads
M=$1; T=$2; O=$3; cd /tmp/claude-0/rt
cr(){ python3 - "$@" <<'PY'
import sys,math
c=[float(v) for v in sys.argv[1].split(',')]; n=[float(v) for v in sys.argv[2].split(',')]; R=float(sys.argv[3])
L=math.sqrt(sum(v*v for v in n)); n=[v/L for v in n]
print("((x-(%g))**2+(f-(%g))**2+(z-(%g))**2<%g)"%(c[0],c[1],c[2],R*R), "%g,%g"%(math.degrees(math.atan2(n[0],n[1])),math.degrees(math.asin(n[2]))))
PY
}
go(){ read crop view < <(cr $2 $3 $4); python3 wireh.py $M $O/q_${T}_$1.png "$crop" $view color 150; }
go ear 7.5,0.5,200 1,0,0 4.5
python3 wireh.py $M $O/q_${T}_axilla.png "(x>12)&(z>138)&(z<168)" 0,-25 color 150
go web_index_middle 32,5,88.5 0,1,0.2 2.5
go web_thumb 29,6,92 0.3,1,0 4
go web_toe4_5_r -25.3,14.8,1.2 -0.2,0.5,0.85 2
go hallux_toe2_l 16.4,17.4,4 0.2,0.85,0.45 2
python3 wireh.py $M $O/q_${T}_groin.png "(z>92)&(z<118)&(abs(x)<15)" 0,-35 color 150
go shoulder 22,0,165 0.6,0.3,0.6 7
echo $T qsheet
if [ "$T" = v002 ]; then
go worst_angle_1 -10.73,-10.48,3.24 0.876,-0.043,-0.48 1.5
go worst_angle_2 0.23,-11.62,115.83 -0.105,-0.799,-0.592 2
go worst_angle_3 -16.48,17.31,3.93 -0.187,0.809,0.558 1.5
go worst_aspect_1 19.49,-11.33,153.4 -0.608,-0.101,-0.787 3
go worst_aspect_2 21.12,-9.22,148.63 -0.97,0.148,-0.195 3
go worst_aspect_3 -33.67,-1.34,89.03 0.292,-0.605,-0.741 1.5
fi

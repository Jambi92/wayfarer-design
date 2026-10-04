cd /tmp/claude-0/rodin/c12; R=/tmp/claude-0/rodin/g1; L=c12.log; C11=/tmp/claude-0/rodin/c11
while ! grep -q "^SNAP" $L; do sleep 20; done
python3 mk15.py > mk15.log 2>&1
FULL="front:0:0:0:0:94:198;profile:90:0:0:0:94:198;rear:180:0:0:0:94:198;front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198"
ORB="hF:0:3:0:10:180:22;hP:90:0:0:6:181:26;hF34:40:12:0:8:181:24;hR34:145:15:0:0:181:24;hT:0:89:0:4:184:22;oC:60:10:4.5:6:183:10;oP:90:2:5:4:183:12"
VIEWS="$FULL;$ORB" NPZ=cs15.npz TAG=$PWD/Y15 RES=1000 python3 $R/rclose.py > /dev/null 2>&1; echo RY15 >> $L
python3 $C11/kcurv.py g15_body.npz kc15.npz
KV="hF:0:3:0:10:180:22;hF34:40:12:0:8:181:24;hP:90:0:0:6:181:26;hR34:145:15:0:0:181:24;oC:60:10:4.5:6:183:10;oP:90:2:5:4:183:12;hT:0:89:0:4:184:22"
for t in 14 15; do NPZ=kc$t.npz; [ $t = 14 ] && NPZ=$C11/kc14.npz; VIEWS="$KV" NPZ=$NPZ TAG=$PWD/K$t RES=800 python3 $R/rclose_rgb.py >/dev/null 2>&1; done
VIEWS="profile:90:0:0:0:94:198;hF34:40:12:0:8:181:24;hP:90:0:0:6:181:26" NPZ=map15.npz TAG=$PWD/M15 RES=900 python3 $R/rclose_rgb.py >/dev/null 2>&1
VIEWS="hF34:40:12:0:8:181:24;hP:90:0:0:6:181:26;front34:45:0:0:0:94:198;oC:60:10:4.5:6:183:10" NPZ=heat15.npz TAG=$PWD/H15 RES=900 python3 $R/rclose_rgb.py >/dev/null 2>&1
VIEWS="hF34:40:12:0:8:181:24;hP:90:0:0:6:181:26" NPZ=$C11/map14.npz TAG=$PWD/M14 RES=900 python3 $R/rclose_rgb.py >/dev/null 2>&1
echo RK15 >> $L

cd /tmp/claude-0/rodin/c11; R=/tmp/claude-0/rodin/g1; L=c11.log
while ! grep -q "^SURF" $L; do sleep 20; done
python3 mk14.py > mk14.log 2>&1
(cd /tmp/claude-0/rodin/g8; SEEDS=/tmp/claude-0/rodin/c11/seeds14.npy python3 g8fields.py /tmp/claude-0/rodin/c11/g14up.npz /tmp/claude-0/rodin/c11/g14reg.npz /tmp/claude-0/rodin/c11/g14_surf.npz /tmp/claude-0/rodin/c11/fld14.npz > /tmp/claude-0/rodin/c11/fld14.log 2>&1); echo FLD14 >> $L
FULL="front:0:0:0:0:94:198;profile:90:0:0:0:94:198;rear:180:0:0:0:94:198;front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198"
ORB="hF:0:3:0:10:180:22;hP:90:0:0:6:181:26;hF34:40:12:0:8:181:24;hR34:145:15:0:0:181:24;hT:0:89:0:4:184:22;oC:60:10:4.5:6:183:10;oP:90:2:5:4:183:12"
TAIL="tprof:90:0:0:-50:94:200;ttop:0:89:0:-50:80:200;tr34:145:10:0:-60:82:110;tailP:90:5:0:-70:84:120;tsc:100:20:0:-50:86:40"
SC="hd:120:20:0:0:180:30;back:180:10:0:-5:140:60;nape:150:20:0:-6:160:30;arm2:90:0:33:0:105:40;shin:20:5:18:4:35:35"
ART="elbow:100:0:29:-4:117:14;knee:20:5:15:5:60:18;axilla:60:5:20:0:138:20;wrist:75:5:34:6:95:16;throat:0:-20:0:8:168:20;fa:90:0:31:4:110:14"
VIEWS="$FULL;$ORB;$TAIL;$SC;$ART" NPZ=/tmp/claude-0/rodin/c10/cs13.npz TAG=$PWD/Y13 RES=1000 python3 $R/rclose.py > /dev/null 2>&1; echo RY13 >> $L
VIEWS="$FULL;$ORB;$TAIL;$SC;$ART" NPZ=cs14.npz TAG=$PWD/Y14 RES=1000 python3 $R/rclose.py > /dev/null 2>&1; echo RY14 >> $L
V4="profile:90:0:0:0:94:198;hF34:40:12:0:8:181:24;tailP:90:3:0:-72:82:110;rear34:150:0:0:0:94:198"
VIEWS="$V4" NPZ=map14.npz TAG=$PWD/M14 RES=900 python3 $R/rclose_rgb.py >/dev/null 2>&1
VIEWS="$V4;back:180:10:0:-5:140:60" NPZ=size14.npz TAG=$PWD/SZ14 RES=900 python3 $R/rclose_rgb.py >/dev/null 2>&1
VIEWS="front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198;profile:90:0:0:0:94:198;hF34:40:12:0:8:181:24;fa:90:0:31:4:110:14" NPZ=heat14.npz TAG=$PWD/H14 RES=900 python3 $R/rclose_rgb.py >/dev/null 2>&1
echo RWB14 >> $L
python3 /tmp/claude-0/rodin/g8/g8render.py job14.json > log_job14.txt 2>&1; echo G8R14 >> $L

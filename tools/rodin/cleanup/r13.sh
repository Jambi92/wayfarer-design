cd /tmp/claude-0/rodin/c10; R=/tmp/claude-0/rodin/g1
FULL="front:0:0:0:0:94:198;profile:90:0:0:0:94:198;rear:180:0:0:0:94:198;front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198"
LOC="chest:10:5:0:5:135:45;back:180:10:0:-5:130:50;nape:150:20:0:-6:160:30;shoulder:60:10:20:0:140:35;arm:90:0:30:0:115:45;hip:120:0:12:-5:90:40;ing:20:-5:10:8:92:34;ankle:60:10:22:4:12:25;ankf:0:5:22:6:14:22;heel:160:5:22:0:14:22;nk:110:10:0:-2:170:35;nkc:110:10:5:-4:166:16;pF34:40:12:0:8:181:24;pP:90:0:0:6:181:26;poC:90:2:5:3:182:11;tprof:90:0:0:-50:94:200;ttop:0:89:0:-50:80:200;tr34:145:10:0:-60:82:110"
VIEWS="$FULL;$LOC" NPZ=/tmp/claude-0/rodin/p9/cs12.npz TAG=$PWD/B12 RES=1000 python3 $R/rclose.py > /dev/null 2>&1; echo RB12 >> c10.log
VIEWS="$FULL;$LOC" NPZ=cs13.npz TAG=$PWD/B13 RES=1000 python3 $R/rclose.py > /dev/null 2>&1; echo RB13 >> c10.log
V4="profile:90:0:0:0:94:198;hF34:40:12:0:8:181:24;tailP:90:3:0:-72:82:110;rear34:150:0:0:0:94:198"
VIEWS="$V4" NPZ=map13.npz TAG=$PWD/M13 RES=1000 python3 $R/rclose_rgb.py >/dev/null 2>&1
VIEWS="front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198;profile:90:0:0:0:94:198;hF34:40:12:0:8:181:24;ankle:60:10:22:4:12:25" NPZ=heat13.npz TAG=$PWD/H13 RES=1000 python3 $R/rclose_rgb.py >/dev/null 2>&1
echo RWB13 >> c10.log

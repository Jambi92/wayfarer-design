cd /tmp/claude-0/rodin/p9; R=/tmp/claude-0/rodin/g1
FULL="front:0:0:0:0:94:198;profile:90:0:0:0:94:198;rear:180:0:0:0:94:198;front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198"
TAIL="tprof:90:0:0:-50:94:200;tailP:90:3:0:-72:82:110;ttop:0:89:0:-50:80:200;dorsT:180:60:0:-70:80:110;trc:130:15:0:-26:90:34;tr34:145:10:0:-60:82:110"
HEAD="hF:0:3:0:10:180:22;hP:90:0:0:6:181:26;hF34:40:12:0:8:181:24;hR34:145:15:0:0:181:24;hT:0:89:0:2:184:30;bF34:40:15:0:5:184:14;bP:90:2:0:5:184:15"
for T in 7 12; do NPZ=$([ $T = 7 ] && echo $R/cs7c.npz || echo cs12.npz)
 VIEWS="$FULL;$TAIL;$HEAD" NPZ=$NPZ TAG=$PWD/N$T RES=1100 python3 $R/rclose.py > /dev/null 2>&1; echo N$T >> p9.log; done
VIEWS="profile:90:0:0:0:94:198;hF34:40:12:0:8:181:24;tailP:90:3:0:-72:82:110;rear34:150:0:0:0:94:198" NPZ=$R/g7map.npz TAG=$PWD/M7 RES=1000 python3 $R/rclose_rgb.py >/dev/null 2>&1
VIEWS="profile:90:0:0:0:94:198;hF34:40:12:0:8:181:24;tailP:90:3:0:-72:82:110;rear34:150:0:0:0:94:198" NPZ=map12.npz TAG=$PWD/M12 RES=1000 python3 $R/rclose_rgb.py >/dev/null 2>&1
VIEWS="front34:45:0:0:0:94:198;profile:90:0:0:0:94:198;rear34:150:0:0:0:94:198;hF34:40:12:0:8:181:24;tailP:90:3:0:-72:82:110" NPZ=heat12.npz TAG=$PWD/H12 RES=1000 python3 $R/rclose_rgb.py >/dev/null 2>&1
echo RWB >> p9.log

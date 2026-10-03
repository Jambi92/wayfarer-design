cd /tmp/claude-0/rodin/g1
FULL="front:0:0:0:0:94:198;profile:90:0:0:0:94:198;rear:180:0:0:0:94:198;front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198"
HEAD="hF:0:3:0:10:180:22;hP:90:0:0:6:181:26;hF34:40:12:0:8:181:24;hR34:145:15:0:0:181:24"
TR="tv:62:0:14:4:122:40;ax:50:5:20:0:138:30;ing:30:-5:10:8:92:34;nh:125:10:0:-2:174:30;wh:75:5:34:6:95:26;af:50:15:22:4:9:28;trc:130:15:0:-26:90:34;pR34:145:10:0:-14:90:52"
python3 crop8.py
VIEWS="$FULL;$HEAD;$TR" NPZ=cs7c.npz TAG=$PWD/E11 RES=1200 python3 rclose.py > /dev/null 2>&1; echo E11
VIEWS="$TR" NPZ=cur_s7.npz TAG=$PWD/E10 RES=1200 python3 rclose.py > /dev/null 2>&1; echo E10tr
HV="hD:92:9:37.1:9.7:88.4:27;hPal:-88:-9:37.1:9.7:88.4:27;hP34:-55:-25:37.1:9.7:88.4:27;hTip:31:-60:38.5:12:82:20"
FV="fD:0:80:23:12:5:30;fPl:0:-85:23:12:5:30;fL:90:5:23:12:5:30;f34:35:25:23:12:5:30"
for T in D C; do
 VIEWS="$HV" NPZ=hand8$T.npz TAG=$PWD/HA8$T RES=1100 python3 rclose.py > /dev/null 2>&1
 VIEWS="$FV" NPZ=foot8$T.npz TAG=$PWD/FO8$T RES=1100 python3 rclose.py > /dev/null 2>&1
done; echo HF
echo R11DONE

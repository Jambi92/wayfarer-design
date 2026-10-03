cd /tmp/claude-0/rodin/g1
FULL="front:0:0:0:0:94:198;profile:90:0:0:0:94:198;rear:180:0:0:0:94:198;front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198"
PEL="pR:180:5:0:-12:88:52;pP:90:0:0:-12:88:56;pR34:145:10:0:-14:90:52;pLow:160:-40:0:-14:84:52;pUnd:0:-80:0:-6:84:56"
TC="tailC:125:12:0:-50:84:100"
python3 ac10.py
VIEWS="$FULL;$PEL;$TC" NPZ=cur_s7.npz TAG=$PWD/E10 RES=1200 python3 rclose.py > /dev/null 2>&1; echo E10done
VIEWS="$TC" NPZ=cur_g9.npz TAG=$PWD/E9 RES=1200 python3 rclose.py > /dev/null 2>&1; echo E9done
VIEWS="fD:0:80:23:12:5:30;fPl:0:-85:23:12:5:30;fL:90:5:23:12:5:30;f34:35:25:23:12:5:30" NPZ=foot7.npz TAG=$PWD/FO7 RES=1200 python3 rclose.py > /dev/null 2>&1; echo FOdone
VIEWS="rear34:150:0:0:0:94:198" NPZ=g7map.npz TAG=$PWD/MP RES=1200 python3 rclose_rgb.py > /dev/null 2>&1; echo MPdone
VIEWS="front:0:0:0:0:94:198;rear34:150:0:0:0:94:198;hF34:40:12:0:8:181:24;pR34:145:10:0:-14:90:52" NPZ=ac10.npz TAG=$PWD/AC10 RES=1200 python3 rclose_rgb.py > /dev/null 2>&1; echo ACdone
python3 ev10.py > /dev/null; echo RDONE

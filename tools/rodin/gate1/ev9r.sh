cd /tmp/claude-0/rodin/g1
FULL="front:0:0:0:0:94:198;profile:90:0:0:0:94:198;rear:180:0:0:0:94:198;front34:45:0:0:0:94:198;rear34:150:0:0:0:94:198"
PEL="pR:180:5:0:-12:88:52;pP:90:0:0:-12:88:56;pR34:145:10:0:-14:90:52;pLow:160:-40:0:-14:84:52;pUnd:0:-80:0:-6:84:56"
HEAD="hF:0:3:0:10:180:22;hP:90:0:0:6:181:26;hF34:40:12:0:8:181:24;hR34:145:15:0:0:181:24"
VIEWS="$FULL;$PEL;$HEAD" NPZ=cur_g9.npz TAG=$PWD/E9 RES=1200 python3 rclose.py > /dev/null 2>&1
VIEWS="$FULL;hF34:40:12:0:8:181:24;pR34:145:10:0:-14:90:52;pLow:160:-40:0:-14:84:52" NPZ=acct9.npz TAG=$PWD/AC9 RES=1200 python3 rclose_col.py > /dev/null 2>&1
echo RDONE

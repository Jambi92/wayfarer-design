cd /tmp/claude-0/rodin/c11; L=c11.log
while ! grep -q "^SURF" $L; do sleep 20; done
python3 kcurv.py /tmp/claude-0/rodin/c10/g13_body.npz kc13.npz; python3 kcurv.py g14_body.npz kc14.npz
for t in 13 14; do VIEWS="hF34:40:12:0:8:181:24;hP:90:0:0:6:181:26;oC:60:10:4.5:6:183:10;hT:0:89:0:4:184:22" NPZ=kc$t.npz TAG=$PWD/K$t RES=800 python3 /tmp/claude-0/rodin/g1/rclose_rgb.py >/dev/null 2>&1; done; echo RK >> $L

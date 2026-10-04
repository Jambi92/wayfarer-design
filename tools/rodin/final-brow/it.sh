# usage: it.sh TAG [env assignments via environment]
T=$1; C=/tmp/claude-0/rodin/c12; G=/tmp/claude-0/rodin/g1
cd $G; BROW_INT=${BI:-5} CLOSURE=1 HEAD_SCALE=1.08 python3 g10.py 0.2 $C/p_$T.npz -16,16,-34,28,161,203 > $C/p_$T.log 2>&1
cd $C; python3 pcurv.py p_$T.npz pk_$T.npz
ORB="hF:0:3:0:10:180:22;hP:90:0:0:6:181:26;hF34:40:12:0:8:181:24;hR34:145:15:0:0:181:24;hT:0:89:0:4:184:22;oC:60:10:4.5:6:183:10;oP:90:2:5:4:183:12"
VIEWS="$ORB" NPZ=pn_$T.npz TAG=$C/N_$T RES=600 python3 $G/rclose.py >/dev/null 2>&1
VIEWS="hF34:40:12:0:8:181:24;hP:90:0:0:6:181:26;oC:60:10:4.5:6:183:10;hT:0:89:0:4:184:22;oP:90:2:5:4:183:12" NPZ=pk_$T.npz TAG=$C/K_$T RES=600 python3 $G/rclose_rgb.py >/dev/null 2>&1
python3 -c "
from PIL import Image; import sys
T='$T'; a=['N_%s_%s.png'%(T,v) for v in ['hF','hP','hF34','hR34','hT','oC','oP']]+['K_%s_%s.png'%(T,v) for v in ['hF34','hP','oC','hT','oP']]
W=Image.new('RGB',(600*6,600*2),(30,30,34))
for i,n in enumerate(a[:12]):
  im=Image.open(n).convert('RGBA'); bg=Image.new('RGBA',im.size,(40,40,46,255)); bg.alpha_composite(im); W.paste(bg.convert('RGB'),((i%6)*600,(i//6)*600))
W.thumbnail((1900,1900)); W.save('S_'+T+'.jpg')"
echo IT_DONE $T

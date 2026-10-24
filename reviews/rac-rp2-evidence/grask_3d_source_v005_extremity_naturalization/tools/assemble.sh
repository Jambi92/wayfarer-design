#!/bin/bash
# assemble.sh : stitch new hands + feet into v003 -> v5/w/asm.npz
cd /tmp/claude-0/src3d; T=v5/tools
read WLX WLY WLZ E0LX E0LY E0LZ < <(python3 -c "
import sys;sys.path.insert(0,'$T');from hand_frame import frame;W,M=frame('L');o=W-6*M[:,0];print(*o.round(5),*M[:,0].round(6))")
read WRX WRY WRZ E0RX E0RY E0RZ < <(python3 -c "
import sys;sys.path.insert(0,'$T');from hand_frame import frame;W,M=frame('R');o=W-6*M[:,0];print(*o.round(5),*M[:,0].round(6))")
python3 $T/stitch_part.py v5/v004.npz v5/w/HL.npz v5/w/a1.npz $WLX $WLY $WLZ $E0LX $E0LY $E0LZ "(x>15)&(z>60)&(z<125)" &&
python3 $T/stitch_part.py v5/w/a1.npz v5/w/HR.npz v5/w/a2.npz $WRX $WRY $WRZ $E0RX $E0RY $E0RZ "(x<-15)&(z>60)&(z<125)" &&
python3 $T/stitch_part.py v5/w/a2.npz v5/w/FL.npz v5/w/a3.npz 0 10.5 0 0 1 0 "(x>3)&(z<14)" &&
python3 $T/stitch_part.py v5/w/a3.npz v5/w/FR.npz v5/w/asm.npz 0 10.5 0 0 1 0 "(x<-3)&(z<14)"

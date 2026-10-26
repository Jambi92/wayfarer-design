#!/bin/bash
# render_all.sh WORKDIR : identical-camera clay renders of v005 (clay) and v003 (clay + wire), whole body, closeups, hands, feet
set -e; W=$1; T=$(cd "$(dirname "$0")" && pwd); BP=${BP:-/home/claude/stc/bin/python3}; . $T/views.sh; mkdir -p $W/r
R() { $BP $T/render.py -- "$@" >/dev/null 2>&1; }
R /tmp/claude-0/src3d/v5/v005.npz $W/r v005 "$BODY" 0 1200; R /tmp/claude-0/rt/frz/v003_frz.npz $W/r v003 "$BODY" 0 1200
WIRE_T=0.0012 R /tmp/claude-0/rt/frz/v003_frz.npz $W/r v003w "$BODY" 1 1200
R /tmp/claude-0/src3d/v5/v005.npz $W/r v005 "$CLOSE" 0 900; WIRE_T=0.0005 R /tmp/claude-0/rt/frz/v003_frz.npz $W/r v003w "$CLOSE" 1 900
for s in l r; do eval H=\$HAND_$s; eval FT=\$FOOT_$s
  R $W/hand_v005_$s.npz $W/r v005_hand_$s "$H" 0 900; WIRE_T=0.00035 R $W/hand_v003_$s.npz $W/r v003w_hand_$s "$H" 1 900
  R $W/foot_v005_$s.npz $W/r v005_foot_$s "$FT" 0 900; WIRE_T=0.00045 R $W/foot_v003_$s.npz $W/r v003w_foot_$s "$FT" 1 900
done
R $W/noarm_v005.npz $W/r v005na "$HIPNA" 0 900; WIRE_T=0.0005 R $W/noarm_v003.npz $W/r v003wna "$HIPNA" 1 900
echo RENDERS_DONE

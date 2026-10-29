# hv_ear_probes.sh WORK CAND HEAD : Halvren mixed-ear order §22 geometry probes on one HE realization folder (same topology / canon, geometry only; no guard):
# length, projection, sweep, vertical angle (tilt), base width, tip sharpness (taper exponent), lobe size -- each - / + about the candidate value.
W=$1; C=$2; H=$3; B=/home/claude/stc/bin/python3; T=/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001
export EAR_CF=${EAR_CF:-/tmp/claude-0/rt/hv/hpe} EAR_TOPO=v002 EAR_UNT_MODE=${EAR_UNT_MODE:-contacts}; cd $W
V=$(python3 -c "
import sys; sys.path.insert(0,'$T'); import ear_branch_lib as E; p=E.CAND['$C']
print(' '.join(['len_m=L=%.3f'%(p['L']*0.9),'len_p=L=%.3f'%(p['L']*1.1),'proj_m=proj=%.1f'%(p['proj']-8),'proj_p=proj=%.1f'%(p['proj']+8),'sweep_m=sweep=%.2f'%(p['sweep']-0.4),'sweep_p=sweep=%.2f'%(p['sweep']+0.4),
 'tilt_m=tilt=%.1f'%(p['tilt']-6),'tilt_p=tilt=%.1f'%(p['tilt']+6),'wb_m=wb=%.3f'%(p['wb']*0.92),'wb_p=wb=%.3f'%(p['wb']*1.08),'tip_blunt=taper_ex=%.2f'%(p['taper'][2]*0.78),'tip_sharp=taper_ex=%.2f'%(p['taper'][2]*1.28),
 'lobe_m=lobe=%.3f'%(p['lobe']-0.04),'lobe_p=lobe=%.3f'%(p['lobe']+0.04)]))")
run(){ n=${1%%=*}; kv=${1#*=}; mkdir -p probe/$n; $B $T/ear_build.py $H $C probe/$n --canon canon_branch_topology.json --probe $kv > probe/$n/build.log 2>&1
  $B $T/ear_audit.py -- probe/$n/${H}_${C}_branch.npz $EAR_CF/fam/${H}_fam.npz probe/$n/audit.json > probe/$n/audit.log 2>&1; python3 $T/ear_measure.py probe/$n/${H}_${C}_branch.npz probe/$n/measure.json > /dev/null 2>&1; echo "PROBE $n $kv"; }
export -f run; export B T H C EAR_CF EAR_TOPO EAR_UNT_MODE
printf '%s\n' $V | xargs -P 2 -I{} bash -c 'run {}'
echo PROBES_DONE

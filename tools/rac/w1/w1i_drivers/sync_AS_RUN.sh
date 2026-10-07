# RAC W1i AS RUN: evidence assembly
S=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad; G=$S/w1g; E=/home/claude/wayfarer-design/reviews/rac-w1i-evidence; EV=$S/w1i/ev
rm -rf $E/cib $E/skeletal $E/candidates $E/geometry $E/skeleton $E/go-variants $E/solver $E/ocular $E/ears $E/sheets; mkdir -p $E/{cib,skeletal,candidates,geometry,skeleton,go-variants,solver,ocular,ears,sheets}
cp $G/cib/*.json $E/cib/; for f in $G/stress/*_cib.json; do cp $f $E/cib/; done; cp $G/final/GO_cib.json $E/cib/
cp $G/skp/*_skp.json $E/skeletal/; rm -f $E/skeletal/skeletal_checks*.json; cp -rL $G/skp/t0.0 $G/skp/t0.5 $G/skp/t1.0 $E/skeletal/; rm -f $E/skeletal/t*/SKB_meas.json
for d in $G/stress/skp_*; do n=${d##*/skp_}; cp $d/${n}_skp.json $E/skeletal/ 2>/dev/null; for t in 0.0 0.5 1.0; do mkdir -p $E/go-variants/skp/t$t; cp $d/t$t/${n}_meas.json $E/go-variants/skp/t$t/ 2>/dev/null; done; done
cp $EV/skeletal_checks.json $EV/alpc_w1i.json $EV/alpc8.json $EV/alpc8.jpg $EV/contour_clearance.json $EV/alpc6_attrib_W1i.json $EV/alpc6_attrib_W1h.json $EV/waist_slab_vs_section.log $E/skeletal/
cp $G/final/GO_meas.json $G/final/GO_inv.json $G/final/GO_evidence.jpg $E/candidates/; cp $G/final/GO_r6.npz $E/geometry/; cp $G/final/GO-LEAN_r6.npz $G/final/GO-LEAN_build.json $E/skeleton/
cp $G/final/GO_params.json $S/w1i/GO_W1i_x.json $E/solver/; cp $G/gn6_I*.log $E/solver/; cp $S/w1i/ref_continuity.json $E/solver/
for n in GOR-BODY-02 GO-H215 GO-H222 GOR-BODY-03 GOR-BODY-04 GOR-BODY-05 GOR-BODY-12 GOR-BODY-14 SKB215 SKB222; do cp $G/stress/${n}_r6.npz $E/go-variants/; done
cp $G/go16/GOR-BODY-16_meas.json $G/go16/GOR-BODY-16_r6.npz $G/stress/stress_builds.json $E/go-variants/
cp $EV/directional_checks.json $EV/w1e_checks.json $E/; cp $EV/ocular_w1i.json $E/ocular/; cp $EV/ear_checks.json $E/ears/; cp $S/w1i/ears/ears_attached.json $E/ears/ 2>/dev/null
cp $S/w1i/sheets/*.jpg $E/sheets/
[ -f $EV/sensitivity_w1i.json ] && cp $EV/sensitivity_w1i.json $E/solver/
du -sh $E
cp -r $S/w1i/i9point $E/solver/; cp $S/w1i/gn6_I*.out $E/solver/ 2>/dev/null; for f in $E/solver/gn6_I*.out; do grep -v "^SKP" $f > $f.tmp; mv $f.tmp $f; done
cp $EV/true208.json $E/skeletal/; cp $G/true208/GO-H208_r6.npz $E/go-variants/
cp $EV/skb_continuity.json $E/skeletal/

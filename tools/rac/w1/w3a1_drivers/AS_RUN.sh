# RAC W3A1 AS RUN (scratch W = session scratchpad/w3a1)
cd /home/claude/wayfarer-design/tools/rac/w1/w3a1_drivers
python3 w3a1_build.py family; python3 w3a1_build.py ksweep; python3 w3a1_build.py src     # family: Skarn+Aelari bodies rebuilt after the signed femur-system fix
python3 w3a1_build.py central; python3 w3a1_build.py rsup; python3 w3a1_build.py stress; python3 w3a1_build.py onset
python3 w3a1_post.py joints; python3 w3a1_post.py grids
python3 w3a1_spec.py $W/spec.json; python3 w3a1_reg.py $W/registry.json
python3 ../w2g_drivers/w2g_eval.py $W/registry.json $W/spec.json $W/w3a1.json <W3A jf.txt joint files> $W/joint_sections.json
python3 w3a1_rs.py $W/w3a1.json <W3A rs.json> $W/rs.json
bash render_AS_RUN.sh

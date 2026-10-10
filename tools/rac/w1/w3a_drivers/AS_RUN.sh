# RAC W3A AS RUN (order of execution; scratch = session scratchpad/w3a)
cd /home/claude/wayfarer-design/tools/rac/w1/w3a_drivers
python3 tail_build.py search; python3 tail_build.py controls; python3 tail_build.py mix      # mix: combined classes rebuilt with the additive t_gen construction
python3 tail_build.py stress; python3 tail_build.py cal; python3 tail_build.py val; python3 tail_build.py refine; python3 tail_build.py probe; python3 tail_build.py rs
python3 w3a_post.py joints; python3 w3a_post.py grids
python3 w3a_spec.py $W/spec.json; python3 w3a_reg.py $W/registry.json
python3 ../w2g_drivers/w2g_eval.py $W/registry.json $W/spec.json $W/w3a.json <W2 joint_sections*.json> $W/joint_sections.json
python3 w3a_rs.py $W/w3a.json $W/rs.json; python3 w3a_emul.py $W/w3a.json $W/emul.json; python3 w3a_audit.py $W/w3a.json $W/audit.json
python3 w3a_tables.py $W/w3a.json $W/emul.json $W/registry.json EVID/tables.md EVID/construction.json $W/rs.json $W/audit.json
bash render_AS_RUN.sh

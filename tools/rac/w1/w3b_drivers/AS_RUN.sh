# RAC W3B AS RUN (scratch W = session scratchpad/w3b; one heavy job at a time - the session memory cgroup kills concurrent 4.5M-vertex jobs)
cd /home/claude/wayfarer-design/tools/rac/w1/w3b_drivers
# canonical hashes before: sha256sum w2i6/canon/* > W/canon_hash_before.txt
python3 w3b_orbit_run.py sweep; python3 w3b_orbit_run.py cases "-0.45@ref,-0.5@ref,-0.55@ref,0.65@ref,0.7@ref,0.75@ref"
python3 w3b_orbit_run.py corners "-0.45,-0.4,-0.3,-0.2,0.2,0.4,0.6,0.65"
python3 w3b_orbit_run.py cases "0.05@cw-8,0.1@cw-8,0.15@cw-8,0.05@comb-in,0.1@comb-in,0.15@comb-in,0.05@comb-out,0.1@comb-out,0.15@comb-out,0.62@ref,-0.42@ref"
python3 w3b_orbit_eval.py
python3 w3b_ridge_run.py global 1.0,0.0,0.25,0.4,0.5,0.6,0.7,0.8,0.9,1.25,1.3,1.4,1.5,1.75,2.0,2.5,3.0
for k in canthal supraorbital temporal jugal occipital mandibular; do python3 w3b_ridge_run.py family $k 0.25,0.5,1.5,1.75,2.0,2.5; done
python3 w3b_ridge_eval.py
python3 w3b_scale_canon.py
python3 w3b_scale_run.py relief face; python3 w3b_scale_run.py relief body; python3 w3b_scale_run.py size face; W3B_OUT=results_sizebody.json python3 w3b_scale_run.py size body
python3 w3b_scale_eval.py
python3 w3b_bodies.py; python3 w3b_extremes.py; python3 w3b_extremes.py clamp
python3 w3b_seeds.py
python3 w3b_interact.py "I0_ref@1.0@1.0@1.0;I1_minR_minRel@0.4@rmin@1.0;I2_minR_maxRel@0.4@rmax@1.0;I3_maxR_minRel@1.3@rmin@1.0;I4_maxR_maxRel@1.3@rmax@1.0;I5_ref_minSize@1.0@1.0@smin;I6_ref_maxSize@1.0@1.0@smax"
python3 w3b_scale_sheets.py interact; python3 w3b_scale_sheets.py face; python3 w3b_scale_sheets.py body; python3 w3b_scale_sheets.py extreme
python3 w3b_tables.py EVIDENCE/tables.md
# canonical hashes after: identical (canon_hash_check.json)

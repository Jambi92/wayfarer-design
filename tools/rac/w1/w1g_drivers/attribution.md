# Method attribution run (AS RUN, W1g)

`reviews/rac-w1g-evidence/skeletal/method_attribution_checks.json` = `skeletal_checks.py` on a copy of the W1g skeletal t-dirs in
which GO and GR are replaced by the UNCHANGED W1f bodies read through CIB:
- GO: `skeletal_proxy.py <w1f final> <w1f final_lean> GO <dir> cib/GO-W1f_cib.json` (CIB from `bony_envelope.assemble_grid` with
  the W1f skeleton `GO-LEAN` + GO0 donor grid, then `bony_envelope.cib`);
- GR: `w1g_drivers/gn3.py GR GRT0 '{}'` (W1e/W1f GR skeleton, no change) -> `cib/GR-W1f_cib.json`, `skp_GRT0`.
Everything else is the W1g reading (the crest-dependent rows of the other races are not affected by the GO / GR substitution).

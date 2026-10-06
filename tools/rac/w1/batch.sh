#!/bin/bash
cd "${W1C_WORKDIR:?set W1C_WORKDIR to a work dir containing cfg/ and out/}"
for id in "$@"; do
  timeout 1500 python3 "$(dirname "$0")"/build_arm.py cfg/$id.json out > log_$id.txt 2>&1
  grep -E "BUILT|UNREACH|Error" log_$id.txt | tail -2
  python3 "$(dirname "$0")"/run_candidate.py out $id >> log_$id.txt 2>&1; tail -1 log_$id.txt
done

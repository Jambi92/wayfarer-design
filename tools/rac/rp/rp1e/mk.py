import json,sys,subprocess
a=json.loads(subprocess.check_output(['python3','split.py',sys.argv[1],sys.argv[2],sys.argv[3]]))
a=a[:-3]+[{'action':'mouse_move','coordinate':[700,450]},{'action':'key','text':'ctrl+s'},{'action':'wait','duration':1.5}]
print(json.dumps(a,separators=(',',':')))

import sys
import os
import subprocess
from proxy import proxies

dryrun="--dry-run" in sys.argv or "-D" in sys.argv

if len(sys.argv)==1:
    print("switch register and proxy")
elif sys.argv[1]=="update":
    res=subprocess.run(['git','status'],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL,cwd=os.path.dirname(__file__))
    if res.returncode==0:
        subprocess.run(['git','pull'],cwd=os.path.dirname(__file__))
    else:
        print("[not installed by git]")
elif sys.argv[1]=="mirror":
    pass
elif sys.argv[1]=="proxy":
    label=None
    if len(sys.argv)<4:
        print("\t srp proxy <tool> <proxy>")
        print("\t srp proxy rm <tool>")
    elif sys.argv[2]=="rm":
        label=sys.argv[3]
        args=sys.argv[5:-1]
    else:
        label=sys.argv[2]
        proxy=sys.argv[3]
        args=sys.argv[4:-1]

    if label and label in proxies.keys():
        handler=proxies.get(label)
        handler.dryrun=dryrun
        handler.rm(args) if sys.argv[2]=="rm" else handler.set(proxy,args)
    else:
        print("available tool support")
        for p in proxies.keys():
            print(f"\t {p}")


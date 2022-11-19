import sys
import os,subprocess
from pathlib import Path
from md5 import md5_dir_write
import shutil

username="orangepi"
ip_addr="192.168.31.2"


def ssh(cmd,capture=False):
    tmpfile=Path.cwd().joinpath(".a.txt")
    if capture:
        with open(tmpfile,"w") as f:
            subprocess.run(f"ssh {username}@{ip_addr} {cmd}",stdout=f)
        f=open(tmpfile,"r")
        a=f.read()
        f.close()
        return a
    else:
        subprocess.run(f"ssh {username}@{ip_addr} {cmd}")
proj=Path(__file__).parent
md5script=proj.joinpath("md5.py")

remote="/home/orangepi/Calibre Library/"
local=Path(r"E:\Applications\Scoop\apps\calibre\current\Calibre Library")
md5_remote_file=Path.cwd().joinpath("remote-md5.txt")
md5_local_file=Path.cwd().joinpath("local-md5.txt")

if "a" in sys.argv or "r" in sys.argv:
    print("计算远程文件md5",remote)
    subprocess.run(f"scp {md5script} {username}@{ip_addr}:/tmp/md5.py")
    ssh(f"python3 /tmp/md5.py \\\"{remote}\\\" /tmp/md5.txt")
    subprocess.run(f"scp {username}@{ip_addr}:/tmp/md5.txt remote-md5.txt",cwd=Path.cwd())
    subprocess.run(f"python3 /tmp/md5.py {md5_remote_file}",cwd=Path.cwd())

if "a" in sys.argv or "l" in sys.argv:
    print("计算本地文件md5",local)
    md5_dir_write(local,md5_local_file)

def read_md5(file):
    md5s=[]
    with open(file,"r") as f:
        for line in f.readlines():
            l=line.split("\t")
            if len(l)>=2:
                md5s.append((l[1].strip().replace("\\","/").strip(),l[0].strip()))
    return md5s

print("比较md5")
md5_local=read_md5(md5_local_file)
md5_remote=read_md5(md5_remote_file)
files=[]
files_rm=[]
for r,c in md5_local:
    copy=True
    for rr,cr in md5_remote:
        if rr==r and cr==c:
            copy=False
            break
    if copy:
        files.append(r)
for rr,cr in md5_remote:
    remove=True
    for r,c in md5_local:
        if rr==r:
            remove=False
            break
    if remove:
        files_rm.append(rr)

print("total local file:", len(md5_local),"copy",len(files))
print("total remote file",len(md5_remote),"rm",len(files_rm))


tmpdir=Path.cwd().joinpath("tmp")
if not tmpdir.exists():
    os.mkdir(tmpdir)
tmpfiles=[]
cmds=[]
for r in files_rm:
    relative=r.replace("\\","/")
    cmds.append(f"rm \"{remote}{relative}\"")

for i,r in enumerate(files):
    file_local=local.joinpath(r)
    tmpfilename=str(i)+".tmp"
    tmpfiles.append(tmpfilename)
    shutil.copy(file_local,tmpdir.joinpath(tmpfilename))
    relative=r.replace("\\","/")
    cmds.append(f"file=\"{remote}{relative}\"")
    cmds.append(f"mkdir -p \"$(dirname \"$file\")\"")
    cmds.append(f"mv /tmp/{tmpfilename} \"$file\"")

if "a" in sys.argv or "s" in sys.argv:
    print("传输差异")
    for i,tmpfilename in enumerate(tmpfiles):
        file_local=local.joinpath(files[i])
        temp_local=tmpdir.joinpath(tmpfilename)
        cmd=f"scp \"{file_local}\" \"{username}@{ip_addr}:/tmp/{tmpfilename}\""
        subprocess.run(cmd)

if "a" in sys.argv or "s2" in sys.argv:
    updatesh=proj.joinpath(".update.sh.txt")
    with open(updatesh,"w") as f:
        f.write("\n".join(cmds))
    cmd=f"scp \"{updatesh}\" \"{username}@{ip_addr}:/tmp/update.sh\""
    subprocess.run(cmd)


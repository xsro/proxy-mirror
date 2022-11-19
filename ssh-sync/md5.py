import sys
import hashlib
from pathlib import Path
import os

def md5(file):
    with open(file, 'rb') as fp:
        data = fp.read()
    file_md5= hashlib.md5(data).hexdigest()
    return file_md5

def _md5_dir(folder:Path,collector,dry_run=True):
    for _file in os.listdir(folder):
        src=folder.joinpath(_file)
        if src.is_file():
            print(src)
            collector.append((md5(src),src))
        if src.is_dir():
            _md5_dir(src,collector,dry_run=dry_run)

def md5_dir(folder,dry_run=True):
    collector=[]
    _md5_dir(folder,collector,dry_run=dry_run)
    return collector

def md5_dir_write(folder,file):
    md5s=md5_dir(folder)
    def fmt(x):
        c,p=x
        return f"{c}\t{p.relative_to(folder)}"
    text="\n".join(list(map(fmt,md5s)))
    with open(file,"w") as f:
        f.write(text)

if __name__=="__main__":
    print("computing md5",sys.argv)
    if sys.argv.__len__()==3:
        md5_dir_write(Path(sys.argv[1]),sys.argv[2])
    else:
        src=Path(r"E:\Applications\Scoop\apps\calibre\current\Calibre Library")
        md5s=md5_dir(src)
        print(md5s)


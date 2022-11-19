import matplotlib
import os
from pathlib import Path

fname=matplotlib.matplotlib_fname()
dst=Path.home().joinpath("./.matplotlib/matplotlibrc")#.replace("$HOME",str(Path.home()))
print(fname,dst.parent)
if not os.path.exists(dst.parent):
    os.makedirs(dst.parent)
with open(fname,'r',encoding="utf-8") as f:
    content=f.read()
    text=content.replace("#font.family:  sans-serif","font.family   :  Microsoft YaHei, sans-serif")
    with open(dst,'w',encoding="utf-8") as f2:
        f2.write(text)



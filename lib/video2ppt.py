import sys
import matplotlib.pyplot as plt
import numpy as np 
import os

def video2png(video:str,split=True):
    dstFolder="tmp-frames/"
    os.makedirs(dstFolder,exist_ok=True)
    if split:
        os.system(f"ffmpeg -i {video} -r 2 {dstFolder}/%06d.png")
    return f"{dstFolder}/%06d.png"
    
def compare(video,d=False,similarity=50000):
    idx=1
    def png(video:str,idx):
        return video.replace("%06d",f"{idx:6d}".replace(" ","0"))
    
    lastFrame=None
    lastIdx=0
    diffs=[]
    for idx in range(1,999999):
        file=png(video,idx)
        if not os.path.exists(file):
            continue
        frame=plt.imread(file)
        if type(lastFrame)==np.ndarray:
            diff=np.abs(frame-lastFrame)
            diff=np.sum(diff)
            diffs.append(diff)
            print(idx,diff)
            if diff<similarity and d==False and os.path.exists(png(video,lastIdx)):
                print("rm ",lastIdx)
                os.remove(png(video,lastIdx))
        lastFrame=frame
        lastIdx=idx
        idx=idx+1
        file=png(video,idx)
    plt.plot(diffs)
    plt.show(block=d)

def main(args:list):
    if len(args)==0:
        print("srp v2ppt <video>")
    else:
        similarity=int(args[1]) if len(args)>1 else None
        print("split the video")
        frames=video2png(args[0],True)
        print("remove similar frame")
        compare(frames,similarity=similarity)

if __name__=="__main__":
    main(sys.argv[1:])
    # main([ "F:\Screenrecorder-2022-10-14-19-04-45-885.mp4"])


import os

class Base:
    dryrun=False
    def exec(self,cmd):
        if self.dryrun:
            print("dryrun:",cmd)
        else:
            print("run:",cmd)
            os.system(cmd)
    def addText(self,path:str,text:str):
        skip_write=False
        if os.path.exists(path):
            with open(path,encoding="utf-8") as f:
                contents = f.read()
                if contents.find(text)!=-1:
                    print(f"already exists in file {path}")
                    skip_write=True  
        if not skip_write:
            if self.dryrun:
                print(f"write to {path}")
                print(contents+"\n"+text)
            else:
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                with open(path,'w',encoding="utf-8") as f:
                    f.write(contents+"\n"+text)
                    print(f"writed {path}")

    def rmText(self,path:str,text:str):
        new=None
        if os.path.exists(path):
            with open(path,'r',encoding="utf-8") as f:
                contents = f.read()
                if contents.find(text):
                    if self.dryrun:
                        print(f"rm following content in {path}")
                        print(text)
                    else:
                        new=contents.replace(text,"")
        if new: 
            with open(path,'w',encoding="utf-8") as f:
                f.write(new)
                print(f"writed {path}")
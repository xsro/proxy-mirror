from pathlib import Path
import os
from .util import Base

class Git(Base):
    def set(self,proxy:str,args:list):
        if "github" in args:
            self.exec(f"git config --global https.https://github.com.proxy {proxy}")
        else:
            self.exec(f'git config --global https.proxy {proxy}')
    
    def rm(self,args:list):
        if "github" in args:
            self.exec(f"git config --global --unset https.https://github.com.proxy")
        else:
            self.exec('git config --global --unset https.proxy')

class GitSsh(Base):
    description="set ssh proxy for github"
    message="set proxy like 127.0.0.1:7890"
    sshconfig=os.path.join(Path.home(),".ssh/config")
    def set(self,proxy:str,args:list):
        self.text=f"Host github.com\n\tProxyCommand connect -S {proxy} %h %p"
        self.addText(self.sshconfig,self.text)
    def rm(self,args:list):
        proxy="127.0.0.1:7890"
        self.text=f"Host github.com\n\tProxyCommand connect -S {proxy} %h %p"
        if self.text:
            self.rmText(self.sshconfig,self.text)
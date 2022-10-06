import configparser;
import os;

class Cargo:
    mirrors=["ustc"]

    def __init__(self) -> None:
        conf=configparser.ConfigParser()
        p=os.path.join(__file__,"../cargo.ini")
        conf.read(p,encoding="utf-8")
        print(conf.sections())

    def switch_registry():
        
        if os.path.exists()
            pass

a=Cargo()
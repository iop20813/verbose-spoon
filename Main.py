from Module import adb
from Control import  LineageM

class Main():
    def __init__(self):
        self.LM = LineageM.LM(Device_Name="emulator-5564")


    def start(self):
        pass




if __name__ == "__main__":
    obj = Main()
    obj.start()
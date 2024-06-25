import os
import subprocess
from PIL import ImageGrab
import numpy as np
import win32gui
from threading import Thread
import time
from PIL import Image

class ADB:
    def __init__(self,Device_Name,Screen_Size):

        self.ADB_Path = "../Tool/adb.exe"
        self.Screen_Size = Screen_Size
        # 裝置名稱
        self.Device_Name = Device_Name
        self.LD_Path = r"C:\LDPlayer\LDPlayer9\\"
        self.Hwnd = 0
        self.ScreenHot = None

    def Keep_Game_ScreenHot(self,Emu_Index,file_name):
        th = Thread(target=self.Keep_Game_ScreenHot_fn,args=[Emu_Index,file_name])
        th.start()
    
    # 跟螢幕有關
    def Keep_Game_ScreenHot_fn(self,Emu_Index,file_name):
        print('Emu_Index')
        print(Emu_Index)
        self.Hwnd = self.Get_Self_Hawd(Emu_Index)
        while 1:
            self.window_capture(hwnd=self.Hwnd,filename=file_name)
            time.sleep(1)
#Index_Num = 0
    def Get_Self_Hawd(self,Index_Num):
        Device_List = self.LD_Call()

        for k, Device_Data in enumerate(Device_List):
            if k != Index_Num:
                continue
            hawd = Device_Data[3]
            print('Device_Data')
            print(Device_Data)
            return hawd
     

    def Get_Rect_Img(self,x1,y1,x2,y2):
        pass

    def LD_Call(self):
        File_Path = self.LD_Path + "ldconsole.exe"

        output = subprocess.Popen([File_Path,'list2'],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        end = []
        for line in output.stdout.readlines():
            output = line.decode('BIG5')
            output = output.strip()
            if output != "":
                output = output.split(",")
                end.append(output)
        return end

    def window_capture(self,hwnd,filename):
        print('hwnd')
        print(hwnd)
        game_rect = win32gui.GetWindowRect(int(hwnd))
        src_image = ImageGrab.grab(game_rect)

        src_image = src_image.resize(self.Screen_Size,Image.LANCZOS)
        print('filename')
        print(filename)
        src_image.save(filename)
        self.ScreenHot = src_image
        print(type(src_image))

    def Touch(self,x,y):
        x = str(x)
        y = str(y)
        self.adb_call(self.Device_Name,['shell','input','tap',x,y])

    def adb_call(self,device_name,detail_list):
        command = [self.ADB_Path,'-s',device_name]
        for order in detail_list:
            command.append(order)
        print(command)
        subprocess.Popen(command)
        
    def adb_call_new(device_name, args):
        adb_path = r'C:\Tool\adb.exe'  # 使用原始字符串格式
        if not os.path.exists(adb_path):
            raise FileNotFoundError(f"adb.exe not found at {adb_path}")
        command = [adb_path, '-s', device_name] + args
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error: {stderr.decode()}")
        else:
            print(stdout.decode())

    def Drag(self,x1,y1,x2,y2,x3,y3,delay_time=1):
        x1 = x1 * 19199 / self.Screen_Size[0]
        y1 = y1 * 10799 / self.Screen_Size[1]
        x2 = x2 * 19199 / self.Screen_Size[0]
        y2 = y2 * 10799 / self.Screen_Size[1]
        x3 = x3 * 19199 / self.Screen_Size[0]
        y3 = y3 * 10799 / self.Screen_Size[1]

        CREATE_NO_WINDOW = 134217728
        devnull = open(os.devnull, 'w')

        # if os.path.isfile('../Tool/dn_drag.bat') == 1:
        #     print("dndrag存在")
        # else:
        #     print("dndrag不存在")



        main_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

        command = [main_path+'\\Tool\\dn_drag.bat',main_path+"\\Tool\\adb.exe",
                   self.Device_Name, str(x1), str(y1), str(x2), str(y2), str(x3), str(y3), str(delay_time)]

        cmd_str = " ".join(command)
        print(command)


        output = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        print(output.stdout.readlines())
        # os.system(cmd_str)
    
    def list_devices():
        adb_path = r'C:\Tool\adb.exe'  # 使用原始字符串格式
        if not os.path.exists(adb_path):
            raise FileNotFoundError(f"adb.exe not found at {adb_path}")
        command = [adb_path, 'devices']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(f"Error: {stderr.decode()}")
        else:
            print(stdout.decode())

    def adb_command(self,device_name, args):
        adb_path = r'C:\Tool\adb.exe'  # 确保这个路径是正确的
        if not os.path.exists(adb_path):
            raise FileNotFoundError(f"adb.exe not found at {adb_path}")
        command = [adb_path, '-s', device_name] + args
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"Error: {stderr.decode()}")
        return stdout.decode()

    def get_screen_size(device_name):
        size_str = adb_command(device_name, ['shell', 'wm', 'size'])
        size_str = size_str.strip().split(': ')[-1]
        width, height = map(int, size_str.split('x'))
        return width, height

    def get_screen_density(self,device_name):
        density_str = self.adb_command(device_name, ['shell', 'wm', 'density'])
        density_str = density_str.strip().split(': ')[-1]
        return int(density_str)

    def take_screenshot(device_name, local_path='screenshot.png'):
        try:
            # 確保設備連接
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            if device_name not in result.stdout:
                print(f"Device {device_name} not found. Please ensure the device is connected and USB debugging is enabled.")
                return
            
            # 截取屏幕並保存到設備，並將截圖從設備拉取到本地
            subprocess.run(['adb', '-s', device_name, 'shell', 'screencap', '-p', '/sdcard/screenshot.png'], check=True)
            subprocess.run(['adb', '-s', device_name, 'pull', '/sdcard/screenshot.png', local_path], check=True)
            
            print(f"Screenshot saved to {local_path}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
        except FileNotFoundError as e:
            print(f"adb not found: {e}")


if __name__ == '__main__':
    obj = ADB(Device_Name="emulator-5554",Screen_Size=[1024,576])
    # obj.Touch(740,520)
    hawd = obj.Get_Self_Hawd(0)



    # try:
    #     list_devices()  # 列出设备，确认设备ID
    #     adb_call_new("emulator-5554", ['shell', 'input', 'tap', '640', '360'])
    #     print('touch pass')
    # except FileNotFoundError as e:
    #     print(e)

    obj.window_capture( hawd,'123.png')
#    obj.Keep_Game_ScreenHot _fn(int(hawd),'123.png')
# [['0', 'LDPlayer', '526138', '524928', '1', '11648', '29932', '1920', '1080', '280']]
#     obj.window_capture(hawd,'test.png')
#     obj.Drag(1164,467,1164,400,1164,370)
#     obj.Touch(1406, 954)


#emulator-5554 是雷電
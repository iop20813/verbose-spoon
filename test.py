import subprocess
import os
import time
import cv2
import numpy as np

def adb_call(device_name, args):
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

        
def adb_callnew(device_name, args):
    adb_path = r'C:\Tool\adb.exe'  # 使用原始字符串格式
    if not os.path.exists(adb_path):
        raise FileNotFoundError(f"adb.exe not found at {adb_path}")
    
    command = [adb_path, '-s', device_name] + args
    print(f"Executing command: {' '.join(command)}")  # 打印命令以调试
    
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=10)  # 设置超时时间
        if process.returncode != 0:
            print(f"Error: {stderr.decode()}")
        else:
            print(stdout.decode())
    except subprocess.TimeoutExpired:
        print('卡住')
        process.kill()
        print("Process timed out")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
# 获取连接的设备列表
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

def check_connected_devices():
    try:
        # 运行 adb devices 命令
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)

        # 解析输出
        lines = result.stdout.splitlines()
        print('lines')
        print(lines)
        devices = []
        
        for line in lines:
            if '\tdevice' in line:
                # 提取设备名称
                device_name = line.split('\t')[0]
                devices.append(device_name)
        
        return devices
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return []


def adb_command(device_name, args):
    adb_path = r'C:\Tool\adb.exe'  # 确保这个路径是正确的
    # if not os.path.exists(adb_path):
    #     raise FileNotFoundError(f"adb.exe not found at {adb_path}")
    command = [adb_path, '-s', device_name] + args
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # if process.returncode != 0:
    #     raise RuntimeError(f"Error: {stderr.decode()}")
    return stdout.decode()


def get_screen_size(device_name):
    size_str = adb_command(device_name, ['shell', 'wm', 'size'])
    size_str = size_str.strip().split(': ')[-1]
    width, height = map(int, size_str.split('x'))
    return width, height

def check_device_connection(device_name):
    try:
        # 檢查設備是否連接
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if device_name not in result.stdout:
            print(f"Device {device_name} not found. Please ensure the device is connected and USB debugging is enabled.")
            print('reconnect server')
            subprocess.run(['adb', 'kill-server'], check=True)
            subprocess.run(['adb', 'start-server'], check=True)
        else:
            print('connect to server')
            return True
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while checking the device connection: {e}")
        return False
    except FileNotFoundError as e:
        print(f"adb not found: {e}")
        return False
    

def take_screenshot(device_name, local_path='screenshot.png'):

    try:
        # 截取屏幕並保存到設備，並將截圖從設備拉取到本地
        subprocess.run(['adb', '-s', device_name, 'shell', 'screencap', '-p', '/sdcard/screenshot.png'], check=True)
        subprocess.run(['adb', '-s', device_name, 'pull', '/sdcard/screenshot.png', local_path], check=True)
        
        print(f"Screenshot saved to {local_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except FileNotFoundError as e:
        print(f"adb not found: {e}")


def analyze_image(image_path):
    # 使用 OpenCV 加載圖片
    img = cv2.imread(image_path)
    # 將圖片轉換為灰度圖像
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low_range = np.array([0, 123, 100])
    high_range = np.array([5, 255, 255])
    mask = cv2.inRange(gray_img, low_range, high_range)
    x, y, w, h = (1168, 510, 65, 63)
    mask_region = mask[y:y+h, x:x+w]

    white_pixel_count = cv2.countNonZero(mask_region)
    if white_pixel_count >= 10:
        return True
    else:
        False

def restart_adb():
    try:
        subprocess.run(['adb', 'kill-server'], check=True)
        subprocess.run(['adb', 'start-server'], check=True)
        print("ADB server restarted.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def restart_device(device_name):
    try:
        subprocess.run(['adb', '-s', device_name, 'reboot'], check=True)
        print(f"Device {device_name} rebooted.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def reconnect_device(device_name):
    try:
        # 断开设备
        subprocess.run(['adb', '-s', device_name, 'disconnect'], check=True)
        # 重新连接设备
        subprocess.run(['adb', 'connect', device_name], check=True)
        print(f"Device {device_name} reconnected.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

########
# Tool #
########
def monitor_hit(device_name):
    for i in range(1000):
        if take_screenshot(device_name):
            pass_1 = analyze_image('screenshot.png')
            if pass_1: 
                print('hit')
                start_time = time.time()
                adb_callnew("emulator-5554", ['shell', 'input', 'tap', '901', '603'])
                end_time = time.time()
                all_time = end_time  - start_time
                print(f'all_time {all_time}')
                continue
        time.sleep(1)  # 避免无限循环占用过多 CPU，适当休眠
def select_region(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load image")
        return None

    # 使用 OpenCV 的选择ROI函数
    r = cv2.selectROI("Select Region", img, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Region")
    # r 返回一个包含 (x, y, w, h) 的元组
    return r
#(1168, 510, 65, 63)

# 測試代碼
if __name__ == "__main__":
    # branch 1 
    device_name = "emulator-5554" 
    #device_name1  = "emulator-5556"
    check_device_connection(device_name)
    monitor_hit(device_name)

#
   # restart_device(device_name1)
   # reconnect_device(device_name1)
   # restart_adb()
    # devices = check_connected_devices()
    # if devices:
    #     print("Connected devices:")
    #     for device in devices:
    #         print(f" - {device}")
    # else:
    #     print("No devices connected")

# (901, 603, 55, 56)  #順捲
    # r = select_region('screenshot.png')
    # print(r)



# # 顯示邊緣檢測結果
# cv2.imshow('Edges', edges)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




# 替换为你的设备ID

start_time = time.time()
device_name = "emulator-5554"  
take_screenshot(device_name)
end_time = time.time()
all_time = end_time  - start_time
print(f'all_time {all_time}')





# 示例调用
# try:
#     device_name = "emulator-5554"  # 替换为你的设备ID
#     width, height = get_screen_size(device_name)
#     density = get_screen_density(device_name)
#     print(f"Screen size: {width}x{height}")
#     print(f"Screen density: {density} dpi")
# except (FileNotFoundError, RuntimeError) as e:
#     print(e)

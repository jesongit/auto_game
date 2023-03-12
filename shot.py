import cv2
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np

from tools import init_data

GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC

# 排除缩放干扰
windll.user32.SetProcessDPIAware()

def capture(handle: HWND):
    """窗口客户区截图

    Args:
        handle (HWND): 要截图的窗口句柄

    Returns:
        numpy.ndarray: 截图数据
    """
    # 获取窗口客户区的大小
    r = RECT()
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
    # 开始截图
    dc = GetDC(handle)
    cdc = CreateCompatibleDC(dc)
    bitmap = CreateCompatibleBitmap(dc, width, height)
    SelectObject(cdc, bitmap)
    BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
    # 截图是BGRA排列，因此总元素个数需要乘以4
    total_bytes = width*height*4
    buffer = bytearray(total_bytes)
    byte_array = c_ubyte*total_bytes
    GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    DeleteObject(bitmap)
    DeleteObject(cdc)
    ReleaseDC(handle, dc)
    # 返回截图数据为numpy.ndarray
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
import time
import ctypes

hwnd_target = 0x00480362 #Chrome handle be used for test

left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
w = right - left
h = bot - top

win32gui.SetForegroundWindow(hwnd_target)
time.sleep(1.0)

hdesktop = win32gui.GetDesktopWindow()
hwndDC = win32gui.GetWindowDC(hdesktop)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hdesktop, hwndDC)

if result == None:
    #PrintWindow Succeeded
    im.save("test.png")

import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
import time
import ctypes

hwnd_target = 0x00480362  # Chrome handle be used for test

left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
w = right - left
h = bot - top

win32gui.SetForegroundWindow(hwnd_target)
time.sleep(1.0)

hdesktop = win32gui.GetDesktopWindow()
hwndDC = win32gui.GetWindowDC(hdesktop)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

saveDC.SelectObject(saveBitMap)

result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

im = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hdesktop, hwndDC)

if result == None:
    # PrintWindow Succeeded
    im.save("test.png")

if __name__ == "__main__":
    hwnd = init_data()
    image = capture(hwnd)
    cv2.imshow("Capture Test", image)
    cv2.waitKey()
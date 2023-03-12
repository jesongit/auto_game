import win32api
import win32con
import win32gui

from tools import do_click


def click():
    """ 模拟点击 """
    '''通过spy++拿到应用程序主窗口的类名和窗口标题'''
    hwnd = win32gui.FindWindow("Intermediate D3D Window", None)

    '''根据GetWindowRect拿到主窗口的左顶点的位置坐标(x,y)和窗口的宽高(w*h)'''
    rect = win32gui.GetWindowRect(hwnd)
    print(rect)
    x, y = rect[0], rect[1]
    w, h = rect[2] - x, rect[3] - y

    # 模拟鼠标指针， 传送到指定坐标
    long_position = win32api.MAKELONG(x, y)

    # 模拟鼠标按下
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)

    # 模拟鼠标弹起
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)


if __name__ == '__main__':
    cw, ch = 13, 24
    handle = win32gui.FindWindow("Chrome_WidgetWin_0", "山海北荒卷")

    rect = win32gui.GetWindowRect(handle)
    per = 1.5
    print(rect)
    # rect = [int(i * per) for i in rect]
    # print(rect)

    x1, y1, x2, y2 = rect[0], rect[1], rect[2], rect[3]

    ax, ay = int(90 / 1.5), int(150 / 1.5)
    do_click(handle, x1 + ax, y1 + ay)

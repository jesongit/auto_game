import os
import time

import cv2
import pyautogui
import win32api
import win32con
import win32gui
import numpy as np
import pytesseract
import win32ui
from PIL import Image

from header import *


def init_data():

    init_global_data()

    os.environ['PATH'] += f';{TESSERACT_PATH}'
    print(pytesseract.get_languages(config=''))

    hwnd = win32gui.FindWindow(g(CLASS), g(NAME))

    x, y, w, h = get_location(hwnd)
    unit = w // ROW
    s([(X, x), (Y, y), (W, w), (H, h), (UNIT, unit)])
    return hwnd


def do_shot(x, y, w, h):
    """ 这里传入的是屏幕种的坐标 """
    print(x, y, w, h)
    img = pyautogui.screenshot(region=[x, y, w, h])
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def match(source, temp_path):
    template = cv2.imread(temp_path)
    res = cv2.matchTemplate(source, template, cv2.TM_SQDIFF_NORMED)
    print(f'match {temp_path} {cv2.minMaxLoc(res)[2]}')
    return cv2.minMaxLoc(res)[2]


def match_all(temp_path, show=False):
    x, y, w, h = shape()
    source = do_shot(x, y, w, h)
    template = cv2.imread(temp_path)
    th, tw, _ = template.shape

    res = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED)
    val, result = cv2.threshold(res, 0.9, 1.0, cv2.THRESH_BINARY)
    result = cv2.findNonZero(result)

    if result is None:
        return []

    # 结果去重
    match_locs = [tuple(result[0][0])]
    ix, iy = result[0][0][0], result[0][0][1]
    for match_loc in result[1:]:
        x, y = match_loc[0][0], match_loc[0][1]
        # print(ix, x, mx, iy, y, my)
        if abs(x - ix) > COND or abs(y - iy) > COND:
            ix, iy, mx, my = x, y, x + tw, y + th
            match_locs.append((x, y))

    print(f'match {temp_path} len: {len(result)}\nres: {match_locs}')
    if show:
        do_show(source, template, match_locs)
    return match_locs


def click_temp(hwnd, temp):
    x, y, w, h = shape()
    source = do_shot(x, y, w, h)
    x, y = match(source, temp)
    do_click(hwnd, x, y)


def get_temp_num(temp):
    return len(match_all(temp))


def do_move(x, y):
    win32api.SetCursorPos([x, y])


def do_slide(hwnd, type=SLIDE_UP):
    up = win32api.MAKELONG(W // 2, H // 3)
    dn = win32api.MAKELONG(W // 2, H * 2 // 3)
    sta, end = (dn, up) if type == SLIDE_UP else (up, dn)
    # todo


def do_click(hwnd, x, y):
    print(f'do_click {x} {x}')
    position = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, position)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, position)


def do_show(img, tp=None, match_locs=[]):
    for match_loc in match_locs:
        right_bottom = (match_loc[0] + tp.shape[1], match_loc[1] + tp.shape[0])
        cv2.rectangle(img, match_loc, right_bottom, (0, 255, 0), 5, 8, 0)
    cv2.imshow("img", img)
    cv2.waitKey(0)


def get_location(hwnd):
    assert hwnd, f'get_location hwnd no found.'

    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect[0], rect[1], rect[2], rect[3]

    return left, top, right - left, bottom - top


def get_handle_name(hwnd):
    title = win32gui.GetWindowText(hwnd)
    cls_name = win32gui.GetClassName(hwnd)
    return title, cls_name


def get_int_info(info):
    return int(ocr(get_info_img(info)))


def get_info_img(info):
    x, y, w, h = grid(info)
    x, y = g(X) + x, g(Y) + y
    return do_shot(x, y, w, h)


def show_shot(x, y, w, h, is_grid=False):
    if is_grid:
        x, y, w, h = grid((x, y, w, h))
    do_show(do_shot(x, y, w, h))


def ocr(img):
    return pytesseract.image_to_string(img, config='--psm 10')


def grid(grid):
    unit = g(UNIT)
    if isinstance(grid, tuple) or isinstance(grid, list):
        return [i * unit for i in grid]
    return grid * unit


if __name__ == '__main__':
    hwnd = init_data()
    # match_all(get('qw'), True)
    x, y, w, h = get_location(hwnd)
    show_shot(x, y, w, h)
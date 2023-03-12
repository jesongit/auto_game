import time

from tools import *
from header import *


def half_auto_hatch(hwnd):
    click_temp(hwnd, t('sdfd'))
    time.sleep(3)

    click_temp(hwnd, t('cs'))


def auto_hatch(hwnd):
    eggs = get_int_info(EGG_INFO)
    print(f'init eggs num: {eggs}')
    while True:
        try:
            time.sleep(5)
            new_eggs = get_int_info(EGG_INFO)
            if new_eggs == eggs:
                # 没变化 需要选择

                click_temp(hwnd, t('jg'))
                time.sleep(2)

                up_num = get_temp_num(t('up'))
                print(f'up: {up_num}')

                if up_num > 2:
                    click_temp(hwnd, t('sf'))
                else:
                    click_temp(hwnd, t('cs'))

            eggs = new_eggs
            print(f'cur eggs num: {eggs}')
        except Exception as e:
            # 兼容手动操作，1分钟后再检测
            print(e.args)
            time.sleep(60)


if __name__ == '__main__':
    hwnd = init_data()
    auto_hatch(hwnd)

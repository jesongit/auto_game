ROW = 13
COL = 24
COND = 10
SLIDE_UP = 0
SLIDE_DN = 1

TEMP_PATH = './template/'
TESSERACT_PATH = 'D:\Program Files\Tesseract-OCR'

# 预设图像位置
EGG_INFO = (5, 21.9, 3, 0.5)

X = 'x'
Y = 'y'
W = 'w'
H = 'h'
UNIT = 'unit'
NAME = 'name'
CLASS = "class"
CHILD = "child"

SET_KEYS = [X, Y, W, H, UNIT]
KEYS = SET_KEYS + [CHILD, NAME, CLASS]


def init_global_data():
    global _global_data
    _global_data = {
        CLASS: "Chrome_WidgetWin_0",
        # CHILD: "Intermediate D3D Window",
        CHILD: "Chrome_RenderWidgetHostHWND",
        NAME: "山海北荒卷",
    }


def g(key):
    assert key in KEYS
    return _global_data[key]


def s(key, val=None):
    if isinstance(key, list):
        for k, v in key:
            assert k in SET_KEYS
            _global_data[k] = v
    else:
        assert key in SET_KEYS
        _global_data[key] = val


def shape():
    return g(X), g(Y), g(W), g(H)


def t(tp: str):
    return f'{TEMP_PATH}{tp}.png'

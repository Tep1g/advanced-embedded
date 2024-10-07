import st7796 #Professor Glower's st7796 driver, renamed for clarity
from motor import BidirectionalMotor

_RGB_BLACK = st7796.RGB(0,0,0)
_RGB_WHITE = st7796.RGB(255, 255, 255)
_GRAPHIC_BAR_X1 = const(220)
_GRAPHIC_BAR_X2 = const(260)
_GRAPHIC_BAR_Y1 = const(160)
_GRAPHIC_BAR_Y2_MIN = _GRAPHIC_BAR_Y1-BidirectionalMotor.MIN_BI_SPEED_PCT
_GRAPHIC_BAR_Y2_MAX = _GRAPHIC_BAR_Y1-BidirectionalMotor.MAX_BI_SPEED_PCT

def init_display():
    st7796.Init()
    st7796.Clear(_RGB_BLACK)

def update_display_value(value: int):
    y2 = _GRAPHIC_BAR_Y1-value
    if value > 0:
        st7796.Solid_Box(_GRAPHIC_BAR_X1, _GRAPHIC_BAR_Y1, _GRAPHIC_BAR_X2, _GRAPHIC_BAR_Y2_MIN, _RGB_BLACK)
        st7796.Solid_Box(_GRAPHIC_BAR_X1, y2, _GRAPHIC_BAR_X2, _GRAPHIC_BAR_Y2_MAX, _RGB_BLACK)
    else:
        st7796.Solid_Box(_GRAPHIC_BAR_X1, _GRAPHIC_BAR_Y1, _GRAPHIC_BAR_X2, _GRAPHIC_BAR_Y2_MAX, _RGB_BLACK)
        st7796.Solid_Box(_GRAPHIC_BAR_X1, y2, _GRAPHIC_BAR_X2, _GRAPHIC_BAR_Y2_MIN, _RGB_BLACK)
    st7796.Solid_Box(_GRAPHIC_BAR_X1, _GRAPHIC_BAR_Y1, _GRAPHIC_BAR_X2, y2, _RGB_WHITE)

if __name__ == "__main__":
    """Test Script"""
    init_display()
    while (True):
        update_display_value(int(input("Enter new bar graph value: ")))
import st7796 #Professor Glower's st7796 driver, renamed for clarity
from motor import BidirectionalMotor

_RGB_BLACK = (0,0,0)
_RGB_WHITE = (255, 255, 255)
_GRAPHIC_BAR_X1 = const(220)
_GRAPHIC_BAR_X2 = const(260)
_GRAPHIC_BAR_Y1 = const(160)
_GRAPHIC_BAR_Y2_MIN = _GRAPHIC_BAR_Y1-BidirectionalMotor.MIN_BI_SPEED_PCT
_GRAPHIC_BAR_Y2_MAX = _GRAPHIC_BAR_Y1-BidirectionalMotor.MAX_BI_SPEED_PCT

class LCD():
    def __init__(self):
        self._bg_color = st7796.RGB(*_RGB_BLACK)
        self._fg_color = st7796.RGB(*_RGB_WHITE)
        self._last_y2 = 0

    def init(self):
        st7796.Init()
        st7796.Clear(self._bg_color)

    def update_motor_speed(self, value: int):
        y2 = _GRAPHIC_BAR_Y1-value
        if value > 0:
            st7796.Solid_Box(_GRAPHIC_BAR_X1, _GRAPHIC_BAR_Y1, _GRAPHIC_BAR_X2, _GRAPHIC_BAR_Y2_MIN, self._bg_color)
            st7796.Solid_Box(_GRAPHIC_BAR_X1, y2, _GRAPHIC_BAR_X2, _GRAPHIC_BAR_Y2_MAX, self._bg_color)
        else:
            st7796.Solid_Box(_GRAPHIC_BAR_X1, _GRAPHIC_BAR_Y1, _GRAPHIC_BAR_X2, _GRAPHIC_BAR_Y2_MAX, self._bg_color)
            st7796.Solid_Box(_GRAPHIC_BAR_X1, y2, _GRAPHIC_BAR_X2, _GRAPHIC_BAR_Y2_MIN, self._bg_color)
        st7796.Solid_Box(_GRAPHIC_BAR_X1, _GRAPHIC_BAR_Y1, _GRAPHIC_BAR_X2, y2, self._fg_color)

if __name__ == "__main__":
    """Test Script"""
    display = LCD()
    display.init()
    while (True):
        display.update_motor_speed(int(input("Enter new bar graph value: ")))
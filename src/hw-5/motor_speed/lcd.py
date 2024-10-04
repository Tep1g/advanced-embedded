import st7796 #Professor Glower's st7796 driver, renamed for clarity

RGB_BLACK = (0,0,0)
RGB_WHITE = (255, 255, 255)
GRAPHIC_BAR_X1 = const(220)
GRAPHIC_BAR_X2 = const(260)
GRAPHIC_BAR_Y1 = const(160)
POS_CHAR = const(" ")
NEG_CHAR = const("-")

class LCD():
    def __init__(self):
        self._bg_color = st7796.RGB(*RGB_BLACK)
        self._fg_color = st7796.RGB(*RGB_WHITE)
        self._last_y2 = 0

    def init(self):
        st7796.Init()
        st7796.Clear(self._bg_color)

    def update_motor_speed(self, value: int):
        st7796.Solid_Box(GRAPHIC_BAR_X1, GRAPHIC_BAR_Y1, GRAPHIC_BAR_X2, self._last_y2, self._bg_color)
        y2 = GRAPHIC_BAR_Y1-value
        st7796.Solid_Box(GRAPHIC_BAR_X1, GRAPHIC_BAR_Y1, GRAPHIC_BAR_X2, y2, self._fg_color)
        self._last_y2 = y2

if __name__ == "__main__":
    """Test Script"""
    display = LCD()
    display.init()
    while (True):
        display.update_motor_speed(int(input("Enter new bar graph value: ")))
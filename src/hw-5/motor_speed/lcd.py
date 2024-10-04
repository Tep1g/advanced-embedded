from lib import st7796 #Professor Glower's st7796 driver, renamed for clarity

RGB_BLACK = (0,0,0)
RGB_WHITE = (255, 255, 255)
GRAPH_TITLE = const("Motor Speed")
POS_CHAR = const(" ")
NEG_CHAR = const("-")

class LCD():
    def __init__(self):
        self._bg_color = st7796.RGB(*RGB_BLACK)
        self._fg_color = st7796.RGB(*RGB_WHITE)

    def init(self):
        st7796.Init()
        st7796.Clear(self._bg_color)
        st7796.Title(Message=GRAPH_TITLE, Color1=self._fg_color, Color0=self._bg_color)

    def update_motor_speed(self, value: int):
        self.init()
        st7796.BarChart(X=[value], color1=self._fg_color, color2=self._fg_color)

if __name__ == "__main__":
    """Test Script"""
    display = LCD()
    display.init()
    while (True):
        display.update_motor_speed(int(input("Enter new bar graph value: ")))
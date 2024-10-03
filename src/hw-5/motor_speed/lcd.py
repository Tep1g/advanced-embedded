from lib import st7796 #Professor Glower's st7796 driver, renamed for clarity

RGB_BLACK = const(st7796.RGB(0,0,0))
RGB_WHITE = const(st7796.RGB(255, 255, 255))
GRAPH_TITLE = const("Motor Speed")
POS_CHAR = const(" ")
NEG_CHAR = const("-")

def init():
    st7796.Init()
    st7796.Clear(RGB_BLACK)
    st7796.Title(Message=GRAPH_TITLE, Color1=RGB_WHITE, Color0=RGB_BLACK)

def update_motor_speed(value: int):
    st7796.BarChart(X=[value], color1=RGB_WHITE, color2=RGB_BLACK)

if __name__ == "__main__":
    """Test Script"""
    init()
    while (True):
        update_motor_speed(int(input("Enter new bar graph value: ")))
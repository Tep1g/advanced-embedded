import st7796
from machine import ADC, Pin

CHUNKS = [[],[]]

for i in range(0, 12):
    CHUNKS[0].append(i*40)

for j in range (0, 8):
    CHUNKS[1].append(280 - (j*40))

class LCD:
    def __init__(self, stick_x_gpio: int, stick_y_gpio: int):
        self._stick_x = ADC(Pin(stick_x_gpio, Pin.IN))
        self._stick_y = ADC(Pin(stick_y_gpio, Pin.IN))
        self._box_pos = [0,0]
        self._box_last_pos = [0,1]
        self._box_moved = [False, False]

    def init(self):
        st7796.Init()
        st7796.Clear(st7796.RGB(0, 0, 0))

    def tick(self):
        self._update_pos()
        self._update_lcd()

    def _update_pos(self):
        input_x = self._stick_x.read_u16()
        input_y = self._stick_y.read_u16()
        hor_move = 0
        ver_move = 0
        if input_x > 55000:
            hor_move = 1
        elif input_x < 10535:
            hor_move = -1

        if input_y > 55000:
            ver_move = 1
        elif input_y < 10535:
            ver_move = -1

        if not self._box_moved[0]:
            self._box_pos[0] = min(max(self._box_pos[0] + hor_move, 0), 11)

        if not self._box_moved[1]:
            self._box_pos[1] = min(max(self._box_pos[1] + ver_move, 0), 7)

        self._box_moved[0] = bool(hor_move)
        self._box_moved[1] = bool(ver_move)

    def _update_lcd(self):
        if ((self._box_pos[0] != self._box_last_pos[0]) or (self._box_pos[1] != self._box_last_pos[1])):
            st7796.Solid_Box(CHUNKS[0][self._box_last_pos[0]], CHUNKS[1][self._box_last_pos[1]], CHUNKS[0][self._box_last_pos[0]]+39, CHUNKS[1][self._box_last_pos[1]]+39, st7796.RGB(0, 0, 0))
            print(self._box_pos[0], self._box_pos[1])
            st7796.Solid_Box(CHUNKS[0][self._box_pos[0]], CHUNKS[1][self._box_pos[1]], CHUNKS[0][self._box_pos[0]]+39, CHUNKS[1][self._box_pos[1]]+39, st7796.RGB(255, 255, 255))
        self._box_last_pos[0] = self._box_pos[0]
        self._box_last_pos[1] = self._box_pos[1]

# Test script
if __name__ == "__main__":
    lcd = LCD(stick_x_gpio=26, stick_y_gpio=27)
    lcd.init()
    while True:
        try:
            lcd.tick()
        except KeyboardInterrupt:
            break
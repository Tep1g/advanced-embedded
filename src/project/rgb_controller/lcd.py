import st7796
from machine import ADC, Pin

CHUNKS = [[],[]]

for i in range(0, 12):
    CHUNKS[0].append(i*40)

for j in range (0, 8):
    CHUNKS[1].append(280 - (j*40))

RGB_VALUES = [st7796.RGB(255, 0, 0), st7796.RGB(0, 255, 0), st7796.RGB(0, 0, 255)]
DEFAULT_BOX_RGB = st7796.RGB(255, 255, 255)
BACKGROUND_RGB = st7796.RGB(0, 0, 0)

class LCD:
    def __init__(self, stick_x_gpio: int, stick_y_gpio: int):
        self._stick_x = ADC(Pin(stick_x_gpio, Pin.IN))
        self._stick_y = ADC(Pin(stick_y_gpio, Pin.IN))
        self._box_rgb = DEFAULT_BOX_RGB
        self._last_box_rgb = self._box_rgb
        self.box_pos = [0,0]
        self._box_last_pos = [0,1]
        self._box_moved = [False, False]
        self.vertically_constrained = False

    def init(self):
        st7796.Init()
        st7796.Clear(BACKGROUND_RGB)

    def tick(self):
        self._update_pos()
        self._update_lcd()

    def switch_box_rgb(self, pointer: int):
        self._last_box_rgb = self._box_rgb
        self._box_rgb = RGB_VALUES[pointer]

    def clear_box_rgb(self):
        self._last_box_rgb = self._box_rgb
        self._box_rgb = DEFAULT_BOX_RGB

    def _update_pos(self):
        input_x = self._stick_x.read_u16()
        input_y = self._stick_y.read_u16()
        hor_move = 0
        ver_move = 0
        if input_x > 55000:
            hor_move = 1
        elif input_x < 10535:
            hor_move = -1

        if not self.vertically_constrained:
            if input_y > 55000:
                ver_move = 1
            elif input_y < 10535:
                ver_move = -1

        if not self._box_moved[0]:
            self.box_pos[0] = min(max(self.box_pos[0] + hor_move, 0), 11)

        if not self._box_moved[1]:
            self.box_pos[1] = min(max(self.box_pos[1] + ver_move, 0), 7)

        self._box_moved[0] = bool(hor_move)
        self._box_moved[1] = bool(ver_move)

    def _update_lcd(self):
        if ((self.box_pos[0] != self._box_last_pos[0]) or (self.box_pos[1] != self._box_last_pos[1]) or (self._last_box_rgb != self._box_rgb)):
            st7796.Solid_Box(CHUNKS[0][self._box_last_pos[0]], CHUNKS[1][self._box_last_pos[1]], CHUNKS[0][self._box_last_pos[0]]+39, CHUNKS[1][self._box_last_pos[1]]+39, BACKGROUND_RGB)
            st7796.Solid_Box(CHUNKS[0][self.box_pos[0]], CHUNKS[1][self.box_pos[1]], CHUNKS[0][self.box_pos[0]]+39, CHUNKS[1][self.box_pos[1]]+39, self._box_rgb)
            
            if self._last_box_rgb != self._box_rgb:
                self._last_box_rgb = self._box_rgb

        self._box_last_pos[0] = self.box_pos[0]
        self._box_last_pos[1] = self.box_pos[1]

# Test script
if __name__ == "__main__":
    lcd = LCD(stick_x_gpio=26, stick_y_gpio=27)
    lcd.init()
    while True:
        try:
            lcd.tick()
        except KeyboardInterrupt:
            break
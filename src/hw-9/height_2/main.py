import st7796
from imu import MPU6050
from machine import I2C, Pin
from neopixel import NeoPixel
from time import ticks_ms, sleep_ms

DISTANCE_CONSTANT = 0.5*9.81
RGB_BLACK = st7796.RGB(0,0,0)
RGB_WHITE = st7796.RGB(255,255,255)
NUM_NEOPIXELS = const(8)

if __name__ == "__main__":
    st7796.Init()
    st7796.Clear(RGB_BLACK)
    i2c = I2C(id=0, scl=Pin(1), sda=Pin(0))
    gy521 = MPU6050(i2c)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    top_distances = [0.0, 0.0, 0.0]
    np = NeoPixel(Pin(11), NUM_NEOPIXELS, bpp=3, timing=1)
    clear_string = " "
    while True:
        for i in range(len(top_distances)):
            offset = 0+(50*i)
            st7796.Text2(clear_string, 0, offset, RGB_WHITE, RGB_BLACK)
            distance_str = str(top_distances[i])
            clear_string = " " * len(distance_str)
            st7796.Text2(distance_str, 0, offset, RGB_WHITE, RGB_BLACK)

        np.fill((0, 0, 0))
        np.write()

        while button.value() == 1:
            continue

        for i in range(NUM_NEOPIXELS):
            sleep_ms(350)
            np[i] = (0, 0, 50)
            np.write()

        while not (0 < gy521.accel.z < 0.1):
            continue
        start_time = ticks_ms()

        while gy521.accel.z < 0.3:
            continue
        air_time_s = (ticks_ms() - start_time)/1000.0
        distance = round(DISTANCE_CONSTANT * ((air_time_s)**2), 2)
        for i in range(len(top_distances)):
            if top_distances[i] < distance:
                top_distances[i] = distance
                break
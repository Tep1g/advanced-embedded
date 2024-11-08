import st7796
from imu import MPU6050
from machine import I2C, Pin
from time import ticks_ms

G_THRESHOLD = 0.1
RGB_BLACK = st7796.RGB(0,0,0)
RGB_WHITE = st7796.RGB(255,255,255)

if __name__ == "__main__":
    st7796.Init()
    st7796.Clear(RGB_BLACK)
    i2c = I2C(id=0, scl=Pin(1), sda=Pin(0))
    gy521 = MPU6050(i2c)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    top_times = [0, 0, 0]
    while True:
        for i in range(len(top_times)):
            time_str = str(top_times[i])
            clear_string = " " * len(time_str)
            offset = 0+(50*i)
            st7796.Text2(clear_string, 0, offset, RGB_WHITE, RGB_BLACK)
            st7796.Text2(time_str, 0, offset, RGB_WHITE, RGB_BLACK)

        while button.value() == 1:
            continue

        while not (0 < gy521.accel.z < 0.1):
            continue
        start_time = ticks_ms()

        while gy521.accel.z < 0.3:
            continue
        air_time = ticks_ms() - start_time

        for i in range(len(top_times)):
            if top_times[i] < air_time:
                top_times[i] = air_time
                break
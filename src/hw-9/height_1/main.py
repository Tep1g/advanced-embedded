from imu import MPU6050
from machine import I2C, Pin
from time import ticks_ms

G_THRESHOLD = 0.1

if __name__ == "__main__":
    i2c = I2C(device_id=0, scl=Pin(1), sda=Pin(0))
    gy521 = MPU6050(i2c)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    top_times = [0, 0, 0]
    while True:
        while button.value() == 1:
            while not (0 < gy521.accel.z < G_THRESHOLD):
                continue
            start_time = ticks_ms()

            while 0 < gy521.accel.z < G_THRESHOLD:
                continue
            air_time = ticks_ms() - start_time

        for i in range(len(top_times)):
            if top_times[i] < air_time:
                top_times[i] = air_time
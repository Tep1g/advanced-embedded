from gps6m import GPS6M
from machine import Pin, UART
from speed_tester import SpeedTester

if __name__ == "__main__":

    # Init peripherals
    gps_uart = UART(0, 9600)
    gps_uart.init(9600, bits=8, parity=None, stop=1, tx=0, rx=1)
    gps = GPS6M(uart=gps_uart)

    start_button = Pin(15, Pin.IN, Pin.PULL_UP)
    stop_button = Pin(14, Pin.IN, Pin.PULL_UP)

    # Instantiate speedtester object
    tester = SpeedTester(gps=gps, start_button=start_button, stop_button=stop_button)

    while True:
        continue
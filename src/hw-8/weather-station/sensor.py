import lcd
from machine import I2C, Pin, Timer
from bme280 import BME280

class EnvironmentSensor:
    def __init__(self, device_id: int, scl_gpio: int, sda_gpio: int, scl_freq_hz: int, sample_rate_hz: int, duration: int, print_data=False, graph_data=False, button=None):
        self._i2c = I2C(id=device_id, scl=Pin(scl_gpio), sda=Pin(sda_gpio), freq=scl_freq_hz)
        self._bme = BME280(i2c=self._i2c)
        self._data = [[],[],[]]
        self._data_set_ptr = 0
        self._done_collecting = False
        self._graph_data = graph_data
        self._time_s = 0
        self._print_data = print_data
        self._duration_s = duration
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, period=sample_rate_hz, callback=self._sample_handler)
        if (button != None) and (self._graph_data):
            self._button = button
            self._button.irq(trigger=Pin.IRQ_FALLING, handler=self._switch_set_handler)

    def _sample_handler(self, timer: Timer):
        self._time_s += 1

        temperature = self._bme.temperature
        humidity = self._bme.humidity
        pressure = self._bme.pressure

        self._data[0].append(temperature)
        self._data[1].append(humidity)
        self._data[2].append(pressure)

        if self._time_s >= self._duration_s:
            self._timer.deinit()
            self._done_collecting = True

            if self._print_data:
                for i in range(len(self._data)):
                    print("T: {}, Temp: {}, Humid: {}, Press: {}".format(
                        i, 
                        self._data[0][i], 
                        self._data[1][i], 
                        self._data[2][i]
                        )
                    )

            if self._graph_data:
                lcd.plot(self._data[self._data_set_ptr])


    def _switch_set_handler(self, pin: Pin):
        if self._done_collecting:
            self._data_set_ptr = (self._data_set_ptr + 1) % len(self._data)
            lcd.plot(self._data[self._data_set_ptr])
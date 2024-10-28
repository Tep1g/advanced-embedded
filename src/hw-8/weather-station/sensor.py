import lcd
from machine import I2C, Pin, Timer
from bme280 import BME280

class EnvironmentSensor:
    def __init__(self, device_id: int, scl_gpio: int, scl_freq_hz: int, sda_gpio: int, sample_rate_hz: int, duration_s: int, display_data_to_lcd: bool=False, print_data: bool=False, graph_data: bool=False, button_gpio=None):
        self._i2c = I2C(id=device_id, scl=Pin(scl_gpio), sda=Pin(sda_gpio), freq=scl_freq_hz)
        self._bme = BME280(i2c=self._i2c)
        self._data = [[],[],[]]
        self._data_set_ptr = 0
        self._display_data_to_lcd = display_data_to_lcd
        self.done_collecting = False
        self._graph_data = graph_data
        self._time_s = 0
        self._print_data = print_data
        self._duration_s = duration_s
        lcd.init(with_labels=display_data_to_lcd)
        self._timer = Timer(-1)
        self._timer.init(mode=Timer.PERIODIC, freq=sample_rate_hz, callback=self._sample_handler)
        if (button_gpio != None) and (self._graph_data):
            self._button = Pin(button_gpio, Pin.IN, Pin.PULL_UP)
            self._button.irq(trigger=Pin.IRQ_FALLING, handler=self._switch_set_handler)

    def _sample_handler(self, timer: Timer):
        self._time_s += 1

        temperature = self._bme.temperature
        humidity = self._bme.humidity
        pressure = self._bme.pressure

        if self._display_data_to_lcd:
            lcd.update_values(temperature=temperature, humidity=humidity, pressure=pressure)

        self._data[0].append(temperature)
        self._data[1].append(humidity)
        self._data[2].append(pressure)

        print("T: {}, Temp: {}, Humid: {}, Press: {}".format(
            self._time_s, 
            temperature, 
            humidity, 
            pressure
            )
        )

        if self._time_s >= self._duration_s:
            self._timer.deinit()
            self.done_collecting = True

            if self._graph_data:
                lcd.plot(self._data[self._data_set_ptr])


    def _switch_set_handler(self, pin: Pin):
        if self.done_collecting:
            self._data_set_ptr = (self._data_set_ptr + 1) % len(self._data)
            lcd.plot(self._data[self._data_set_ptr])
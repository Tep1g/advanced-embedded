import lcd
from machine import I2C, Pin, Timer
from bme280 import BME280

class EnvironmentSensor:
    def __init__(self, device_id: int, scl_gpio: int, sda_gpio: int, scl_freq_hz: int, sample_rate_hz: int, buffer_size: int, button=None):
        self._i2c = I2C(id=device_id, scl=Pin(scl_gpio), sda=Pin(sda_gpio), freq=scl_freq_hz)
        self._bme = BME280(i2c=self._i2c)
        self._circ_buffer = [[""] * buffer_size]*3
        self._timer = Timer(-1)
        self._buffer_ptr = 0
        self._set_num = 1
        self._set_label = "Set {}".format(self._set_num)
        self._current_set = {}
        self._meas_sets = {}
        lcd.init()
        self._timer.init(mode=Timer.PERIODIC, period=sample_rate_hz, callback=self._sample_handler)
        if button != None:
            self._button = button
            self._button.irq(trigger=Pin.IRQ_FALLING, handler=self._switch_set_handler)

    def _sample_handler(self, timer: Timer):
        temperature = self._bme.temperature
        humidity = self._bme.humidity
        pressure = self._bme.pressure

        self._circ_buffer[0][self._buffer_ptr] = temperature
        self._circ_buffer[1][self._buffer_ptr] = humidity
        self._circ_buffer[2][self._buffer_ptr] = pressure
        self._buffer_ptr += 1

        lcd.update(temperature=temperature, humidity=humidity, pressure=pressure)

    
    def _switch_set_handler(self, pin: Pin):
        self._meas_sets[self._set_label, {
            "temperature": [temp for temp in self._circ_buffer[0]],
            "humidity": [humid for humid in self._circ_buffer[1]],
            "pressure": [pres for pres in self._circ_buffer[2]]
            }
        ]
        self._set_label = "Set {}".format(self._set_num)
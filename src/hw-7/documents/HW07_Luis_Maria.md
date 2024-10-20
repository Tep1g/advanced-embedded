# Coffee Cup Tester
## 1) sensor.py
### Program
```py
import onewire
from ds18x20 import DS18X20
from machine import Pin
from time import sleep_ms

_ONEWIRE_GPIO = const(4)

class Sensor:
    def __init__(self, onewire_gpio: int):
        self._ds18b20 = DS18X20(onewire.OneWire(Pin(onewire_gpio)))
        addresses = self._ds18b20.scan()
        self._address = addresses[0]

        print('Found DS devices: {}'.format(addresses))
        print('Using address: {}'.format(self._address))

    def read_temp(self):
        self._ds18b20.convert_temp()
        sleep_ms(750)
        
        return self._ds18b20.read_temp(self._address)

if __name__ == "__main__":
    """Problem 1"""
    sensor = Sensor(onewire_gpio=_ONEWIRE_GPIO)

    while True:
        print(sensor.read_temp())
```

### Test

Cold water

![alt text](<images/cold water.png>)

<br>

Hot water

![alt text](<images/hot water.png>)

<br>

Ambient temperature

![alt text](images/Tamb.png)
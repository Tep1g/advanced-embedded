import onewire
from ds18x20 import DS18X20
from machine import Pin

_ONEWIRE_GPIO = const(4)

def ds18x20_init(onewire_gpio: int) -> tuple[DS18X20, int]:
    ds18b20 = DS18X20(onewire.OneWire(Pin(onewire_gpio)))
    addresses = ds18b20.scan()
    address = addresses[0]
    print('Found DS devices: {}'.format(addresses))
    print('Using address: {}'.format(address))

    return (ds18b20, address)

if __name__ == "__main__":
    """Problem 1"""
    (ds18b20, address) = ds18x20_init(onewire_gpio=_ONEWIRE_GPIO)

    while True:
        print(ds18b20.read_temp(address))
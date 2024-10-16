import onewire
from ds18x20 import DS18X20

_SENSOR_RX_GPIO = const(4)

def ds18x20_init() -> tuple[DS18X20, int]:
    ds18b20 = DS18X20(onewire.OneWire(_SENSOR_RX_GPIO))
    addresses = ds18b20.scan()
    address = addresses[0]
    print('Found DS devices: {}'.format(addresses))
    print('Using address: {}'.format(address))

    return (ds18b20, address)

if __name__ == "__main__":
    """Problem 1"""
    (ds18b20, address) = ds18x20_init()

    while True:
        print(ds18b20.read_temp(address))
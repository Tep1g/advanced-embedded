import ds18x20, onewire

SENSOR_RX_GPIO = const(4)

if __name__ == "__main__":
    """Problem 1"""
    ds18b20 = ds18x20.DS18X20(onewire.OneWire(SENSOR_RX_GPIO))
    addresses = ds18b20.scan()
    address = addresses[0]
    print('Found DS devices: {}'.format(addresses))
    print('Using address: {}'.format(address))

    while True:
        print(ds18b20.read_temp(address))
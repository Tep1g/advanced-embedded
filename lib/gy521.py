from machine import I2C

class GY521:
    def __init__(self, i2c: I2C):
        self._i2c = i2c
        self._addr = None

    def connect(self):
        # Print out any addresses found
        devices = self._i2c.scan()
        if devices:
            for d in devices:
                print('I2C Device Found:',hex(d))
        self._addr = devices[0]
        print('Communicating with ', hex(self._addr))

    def init(self):
        # Set bandwidth
        self._reg_write(0x1a, 3)

        # Set range
        self._reg_write(0x1c, 0x00)

        # Set clock frequency
        self._reg_write(0x6b, 0)

    def _reg_write(self, reg, data):
        msg = bytearray()
        msg.append(data)
        self._i2c.writeto_mem(self._addr, reg, msg)
        
    def _reg_read(self, i2c: I2C, reg, nbytes=1):
        if nbytes < 1:
            return bytearray()
        data = i2c.readfrom_mem(self._addr, reg, nbytes)
        return data

    def accel_read(self, reg):
        x = self._reg_read(self._i2c, reg, 2)
        y = (x[0] << 8) + x[1]
        if(y > 0x8000):
            y = y - 0x10000
        y = y / 0x8000
        return(y)
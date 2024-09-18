from machine import ADC

class LightSensor():
    """Light Sensor"""

    _VDD = 3.3
    _MAX_U16 = (2 ** 16) - 1

    _V_FACTOR = _VDD / _MAX_U16

    def __init__(self, adc_pin: int):
        """
        Initialize the LightSensor object

        :param int adc_port: The light sensor's corresponding ADC pin
        """
        self._adc = ADC(Pin(adc_pin, Pin.IN))

    def read_voltage(self) -> float:
        """Return the ADC voltage as a float"""
        return (self._adc.read_u16() * self._V_FACTOR)

if __name__ == "__main__":
    """Test Script"""
    while True:
        light_sensor = LightSensor(adc_pin=28)
        print(light_sensor.read_voltage())
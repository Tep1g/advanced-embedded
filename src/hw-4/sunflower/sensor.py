from machine import ADC

class LightSensor():
    """Light Sensor"""

    _VDD = 3.3
    _MAX_U16 = (2 ** 8) - 1

    _V_FACTOR = _VDD / _MAX_U16

    def __init__(self, adc_port: int):
        """
        Initialize the LightSensor object

        :param int adc_port: The light sensor's corresponding ADC port
        """
        self._adc = ADC(adc_port)

    def read_voltage(self) -> float:
        """Return the ADC voltage as a float"""
        return (self._adc.read_u16() * self._V_FACTOR)

if __name__ == "__main__":
    """Test Script"""
    while True:
        light_sensor = LightSensor(adc_port=2)
        print(light_sensor.read_voltage())
from machine import ADC

def read_voltage(adc: ADC):
    return (adc.read_u16() * 3.3 / 65535)

if __name__ == "__main__":
    """Test Script"""
    while True:
        light = ADC(2)
        print(read_voltage(light))
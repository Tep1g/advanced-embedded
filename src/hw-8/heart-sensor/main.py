from sensor import HeartSensor
from lcd import LCD

def test_graph():
    display = LCD()
    display.init_graph()

    heart_sensor = HeartSensor(adc_gpio=28)
    while True:
        continue
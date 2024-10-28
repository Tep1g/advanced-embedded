from sensor import HeartSensor
from lcd import LCD

if __name__ == "__main__":
    display = LCD()
    display.init_graph()
    display.init_bpm()
    display.init_pulse_period()
    heart_sensor = HeartSensor(adc_gpio=28, duration_ms=1_800, display=display)
    while heart_sensor.enabled:
        continue
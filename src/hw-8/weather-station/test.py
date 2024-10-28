from sensor import EnvironmentSensor

if __name__ == "__main__":
    sensor = EnvironmentSensor(
        device_id=0,
        scl_gpio=21,
        scl_freq_hz=10_000,
        sda_gpio=20,
        sample_rate_hz=1,
        duration_s=60,
        print_data=True,
        button_gpio=15
    )
    while not sensor.done_collecting:
        continue
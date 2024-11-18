import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from motor import BidirectionalMotor

motor = BidirectionalMotor(cw_gpio=16, ccw_gpio=17)

def on_rx(data):
    print("Data received: ", data)
    try:
        speed = int(data)
        motor.set_speed_pct(speed)
    except:
        print("Invalid data")

if __name__ == "__main__":
    ble = bluetooth.BLE()
    sp = BLESimplePeripheral(ble)

    while True:
        if sp.is_connected():
            sp.on_write(on_rx)
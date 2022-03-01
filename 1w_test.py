import time
from digitemp.master import UART_Adapter
from digitemp.device import TemperatureSensor
from digitemp.exceptions import OneWireException

bus = UART_Adapter("/dev/ttyUSB0")

class CenturioSensor():
    def __init__(self, name, rom):
        self.name = name
        self.rom = rom

sensors = []
for rom in bus.get_connected_ROMs():
    try:
        temp_sensor = TemperatureSensor(bus, rom)
        temp_sensor.name = input(f"Enter name for device {temp_sensor.rom}:\n")
        sensors.append(temp_sensor)
    except OneWireException:
        pass

print(55 * "=")
for sensor in sensors:
    sensor.info()
    print(55 * "=")
    
try:
    while True:
        for sensor in sensors:
            try:
                print(f"{sensor.name}: {sensor.get_temperature():.2f} °C")
            except OneWireException:
                print(f"{sensor.name}: ERROR")
                
        time.sleep(3)
except KeyboardInterrupt:
    pass
finally:
    bus.close()
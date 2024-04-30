import os
import utime
from machine import ADC, UART, Pin

#uart = UART(2, baudrate=9600, tx=3, rx=1)
uart = UART(1, baudrate=9600, tx=16, rx=17)
#uart = UART(0, baudrate=9600, tx=9, rx=10)
led = Pin(2, Pin.OUT)

def temperature():
    raw_sensor_data = ADC(4).read()
    sensor_voltage = raw_sensor_data / 4095 * 3.3
    temperature = (sensor_voltage - 0.706) / 0.001721
    return temperature

def process_command(command):
    if command.strip() == 'ON':
        led.on()
    elif command.strip() == 'OFF':
        led.off()

print("OS Name:", os.uname())
print("UART Info:", uart)
utime.sleep(3)

while True:
    temp = temperature()
    print("Temperature:", temp)
    uart.write(str(temp) + '\n')
    
    if uart.any():
        command = uart.readline()
        process_command(command.decode())

    utime.sleep(1)
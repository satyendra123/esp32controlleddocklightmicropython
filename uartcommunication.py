#EXAMPLE-1 in this we are checking that how the uart pin is working in esp32 in micropython
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

#EXAMPLE-2 isme humne 3 uarts ka use kiya hai. teeno jo hai data send karte hai. ye working project hai

import utime
from machine import ADC, UART, Pin

uart0 = UART(0, baudrate=9600, tx=3, rx=1)
uart1 = UART(1, baudrate=9600, tx=16, rx=17)
uart2 = UART(2, baudrate=9600, tx=32, rx=33)
led = Pin(2, Pin.OUT)

def temperature():
    raw_sensor_data = ADC(4).read()
    sensor_voltage = raw_sensor_data / 4095 * 3.3
    temperature = (sensor_voltage - 0.706) / 0.001721
    return temperature

def process_command(command):
    command = command.strip().decode()
    if command == 'ON':
        led.on()
    elif command == 'OFF':
        led.off()

print("UART0 Info:", uart0)
print("UART1 Info:", uart1)
print("UART2 Info:", uart2)
utime.sleep(3)

while True:
    temp = temperature()
    print("Temperature:", temp)
    uart0.write(str(temp) + '\n')
    uart1.write(str(temp) + '\n')
    uart2.write(str(temp) + '\n')

    # Add a delay between writes
    utime.sleep(0.5)  # Adjust this delay as needed

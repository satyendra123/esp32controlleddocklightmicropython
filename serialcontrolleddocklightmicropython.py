#EXAMPLE-1 this code simply blinks an builtin led of micropython. which simply means that we can check our esp32 is working or not
'''
from machine import Pin
import time

# Define LED pin
LED_PIN = 2  # Replace with your LED pin number
led = Pin(LED_PIN, Pin.OUT)

# Main loop
while True:
    led.value(1)  # Turn LED on
    time.sleep(1)  # Delay 1 second
    led.value(0)  # Turn LED off
    time.sleep(1)  # Delay
'''
#EXAMPLE-2 in this we are sending the internal temperature sensor value to docklight software. and this is working fine
'''
#this is the working code. i am sending the data to docklight software. i have connected rs485 to ttl module pin 1 and 3 and uart2.
import os
import utime
from machine import ADC, UART

uart = UART(2, baudrate=9600, tx=3, rx=1)

def temperature():
    raw_sensor_data = ADC(4).read()
    sensor_voltage = raw_sensor_data / 4095 * 3.3
    temperature = (sensor_voltage - 0.706) / 0.001721    
    return temperature

print("OS Name:", os.uname())
print("UART Info:", uart)
utime.sleep(3)

# Main loop
while True:
    temp = temperature()
    print("Temperature:", temp)
    uart.write(str(temp) + '\n') 
    utime.sleep(1)
'''
'''
#EXAMPLE-3 this code sends the temperature and also control the led using docklight software.
import os
import utime
from machine import ADC, UART, Pin

uart = UART(2, baudrate=9600, tx=3, rx=1)
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
'''
#EXAMPLE-4 this is the code which simply control the led of esp32 using rs485tottl module using docklight software
import os
import utime
from machine import UART, Pin

uart = UART(2, baudrate=9600, tx=3, rx=1)
led = Pin(2, Pin.OUT)

def process_command(command):
    if command.strip() == 'ON':
        led.on()
    elif command.strip() == 'OFF':
        led.off()

print("OS Name:", os.uname())
print("UART Info:", uart)
utime.sleep(3)

while True:
    if uart.any():
        command = uart.readline()
        process_command(command.decode())

    utime.sleep(1)

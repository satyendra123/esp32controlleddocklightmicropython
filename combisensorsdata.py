#Example-1 reading the sensor status data using esp32 and rs485tottl module using micropython. and sending the zone data with the protocol and reading it on the docklight software.
#maine ek rs485tottl module ka hi use kiya hai aur isme maine isi rs485tottl module me rs485tousb lagakar data read kiya hai docklight me. so ye mera full process hai. 
from machine import UART
import time

uart = UART(2, baudrate=9600, tx=3, rx=1)
uart1 = UART(1, baudrate=9600, tx=16, rx=17)
sensor_requests = ['FA0101F9', 'FA0201FA', 'FA0301FB']
sensor_status = []
zone_id = '01'  # Convert zone_id to a byte

def calculate_sensor_status(response):
    status_byte = response[2:3]
    if status_byte == b'\x01':
        return 1  # Engaged
    elif status_byte == b'\x02':
        return 2  # Disengaged
    elif status_byte == b'\x03':
        return 3  # Error
    else:
        return -1  # Invalid status

def process_sensor_requests():
    global sensor_status
    sensor_status = []
    for request in sensor_requests:
        if request.startswith('FA'):
            uart.write(bytes.fromhex(request))
            time.sleep(2)
            response = uart.read()
            if response and response[0:1] == b'\xF5':
                sensor_status.append(calculate_sensor_status(response))

    # Construct message
    total_sensors = len(sensor_status)
    total_engaged = sensor_status.count(1)
    total_disengaged = sensor_status.count(2)
    total_errors = sensor_status.count(3)
    total_vacancy = total_disengaged
    message = bytearray([0xAA, int(zone_id), total_sensors] + sensor_status + [total_engaged, total_disengaged, total_vacancy, total_errors, 0x55])
    uart1.write(message)

# Listen for slave ID from the floor controller
while True:
    process_sensor_requests()
#EXAMPLE-2 isme maine is project ko aange badhaya hai aur isme two rs485 to ttl module lagaya hai. ek rs485tottl module jo hai sensor se data lega means input ki tarah kaam karega aur dusra rs485tottl module jo hai wo output ki tarah kaam karega
#means sensor ka data kisi master controller ko send karega. so sensor se data lene ke liye humne pin 1 aur 3 ka use kiya tha aur pin 16,17 ka use humne rs485 to ttl se data ko master controller par send karne ke liye kiya hai
#aur rs485tottl output wale me humne rs485tousb lagakar check kiya ki hume docklight me data mil rha hai ya nahi. aur hume data mil rha tha iska is protocol me. humne iske liye khud ka ek protocol banaya hai
#AA(start frame), zone address(01), total sensor(05), 00(sensoraddress01 status) 01(sensoraddress02 status) 01(sensoraddress03 status) 00(sensoraddress04 status) 01(sensoraddress05 status) (Each sensor status), total engaged(03), total disengaged(02), total vacancy(02), total error(00), total no communication(00),55(End of protocol)

from machine import UART
import time

uart = UART(2, baudrate=9600, tx=3, rx=1)
uart1 = UART(1, baudrate=9600, tx=16, rx=17)
sensor_requests = ['FA0101F9', 'FA0201FA', 'FA0301FB']
sensor_status = []
zone_id = '01'  # Convert zone_id to a byte

def calculate_sensor_status(response):
    status_byte = response[2:3]
    if status_byte == b'\x01':
        return 1  # Engaged
    elif status_byte == b'\x02':
        return 2  # Disengaged
    elif status_byte == b'\x03':
        return 3  # Error
    else:
        return -1  # Invalid status

def process_sensor_requests():
    global sensor_status
    sensor_status = []
    for request in sensor_requests:
        if request.startswith('FA'):
            uart.write(bytes.fromhex(request))
            time.sleep(2)
            response = uart.read()
            if response and response[0:1] == b'\xF5':
                sensor_status.append(calculate_sensor_status(response))

    # Construct message
    total_sensors = len(sensor_status)
    total_engaged = sensor_status.count(1)
    total_disengaged = sensor_status.count(2)
    total_errors = sensor_status.count(3)
    total_vacancy = total_disengaged
    message = bytearray([0xAA, int(zone_id), total_sensors] + sensor_status + [total_engaged, total_disengaged, total_vacancy, total_errors, 0x55])
    uart1.write(message)

# Listen for slave ID from the floor controller
while True:
    process_sensor_requests()
#EXAMPLE-3 3rd process me maine ye kaam kiya hai ki hum sabse pahle request send karenge docklight se zone controller ko. request ke taur par hum zone controller ko uski id send karenge taki ye pahle receive kare aur agr zone id match hone ke bad ye sensor ko request send karega aur udhar se response 
# nikal kar hume docklight me send kar dega. humne python me code likh kar bhi is chiz ko test kar liya hai.
from machine import UART
import time

uart = UART(2, baudrate=9600, tx=3, rx=1)
uart1 = UART(1, baudrate=9600, tx=16, rx=17)
sensor_requests = ['FA0101F9', 'FA0201FA', 'FA0301FB']
sensor_status = []
zone_id = b'\x01'  # Convert zone_id to a byte

def calculate_sensor_status(response):
    status_byte = response[2:3]
    if status_byte == b'\x01':
        return 1  # Engaged
    elif status_byte == b'\x02':
        return 2  # Disengaged
    elif status_byte == b'\x03':
        return 3  # Error
    else:
        return -1  # Invalid status

def process_sensor_requests():
    global sensor_status
    sensor_status = []
    for request in sensor_requests:
        if request.startswith('FA'):
            uart.write(bytes.fromhex(request))
            time.sleep(2)
            response = uart.read()
            if response and response[0:1] == b'\xF5':
                sensor_status.append(calculate_sensor_status(response))

    # Construct message
    total_sensors = len(sensor_status)
    total_engaged = sensor_status.count(1)
    total_disengaged = sensor_status.count(2)
    total_errors = sensor_status.count(3)
    total_vacancy = total_disengaged
    message = bytearray([0xAA, int.from_bytes(zone_id, "little"), total_sensors] + sensor_status + [total_engaged, total_disengaged, total_vacancy, total_errors, 0x55])
    uart1.write(message)

# Listen for slave ID from the floor controller
while True:
    slave_id = uart1.read()
    if slave_id == zone_id:
        process_sensor_requests()

#EXAMPLE-4 this is my final complete zone controller code. 
from machine import UART, Pin
import time

# Disable REPL on UART0
import os
os.dupterm(None, 0)

# Initialize UARTs
uart0 = UART(0, baudrate=9600, tx=Pin(33), rx=Pin(32))
uart1 = UART(1, baudrate=9600, tx=Pin(16), rx=Pin(17))
uart2 = UART(2, baudrate=9600, tx=Pin(3), rx=Pin(1))

sensor_requests = ['FA0101F9', 'FA0201FA', 'FA0301FB']
zone_id = '01'  # Convert zone_id to a byte

def calculate_sensor_status(response):
    status_byte = response[2:3]
    if status_byte == b'\x01':
        return 1  # Engaged
    elif status_byte == b'\x02':
        return 2  # Disengaged
    elif status_byte == b'\x03':
        return 3  # Error
    else:
        return -1  # Invalid status

def process_sensor_requests():
    sensor_status = []
    
    for request in sensor_requests:
        if request.startswith('FA'):
            uart1.write(bytes.fromhex(request))
            time.sleep(2)
            response = uart1.read()
            if response and response[0:1] == b'\xF5':
                sensor_status.append(calculate_sensor_status(response))

    # Construct message
    total_sensors = len(sensor_status)
    total_engaged = sensor_status.count(1)
    total_disengaged = sensor_status.count(2)
    total_errors = sensor_status.count(3)
    total_vacancy = total_disengaged
    message = bytearray([0xAA, int(zone_id), total_sensors] + sensor_status + [total_engaged, total_disengaged, total_vacancy, total_errors, 0x55])
    
    # Print the hex data in the message
    print(' '.join('{:02x}'.format(byte) for byte in message))
    
    # Write message to UART2 (pins 3, 1) and UART0 (pins 25, 26)
    uart2.write(message)
    uart0.write(message)

# Main loop
while True:
    process_sensor_requests()

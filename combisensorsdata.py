#Example-1 reading the sensor status data using esp32 and rs485tottl module using micropython. and sending the zone data with the protocol and reading it on the docklight software.
#maine ek rs485tottl module ka hi use kiya hai aur isme maine isi rs485tottl module me rs485tousb lagakar data read kiya hai docklight me. so ye mera full process hai. 
from machine import UART
import time

uart = UART(2, baudrate=9600, tx=3, rx=1)
sensor_requests = ['FA0101F9', 'FA0201FA']
total_sensors = len(sensor_requests)
total_engaged = 0
total_disengaged = 0
total_vacancy = 0
zone_id = '01'

def calculate_sensor_status(response):
    global total_engaged, total_disengaged, total_vacancy
    status_byte = response[2:3]  # Convert to string
    if status_byte == b'\x01':
        total_engaged += 1
    elif status_byte == b'\x00':
        total_disengaged += 1

    return total_sensors, total_engaged, total_disengaged, total_vacancy

def process_sensor_requests():
    global total_engaged, total_disengaged, total_vacancy
    total_engaged = 0
    total_disengaged = 0
    for request in sensor_requests:
        if request.startswith('FA'):
            uart.write(bytes.fromhex(request))
            time.sleep(2)
            response = uart.read()
            if response and response[0:1] == b'\xF5':
                ts, te, td, tv = calculate_sensor_status(response)

    # Construct message
    message = bytearray([0xAA, int(zone_id, 16), total_sensors, 0x01 if total_engaged > 0 else 0x00, 0x01 if total_disengaged > 0 else 0x00, total_engaged, total_disengaged, total_vacancy, 0x55])
    uart.write(message)

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
sensor_requests = ['FA0101F9', 'FA0201FA']
sensor_status = []
zone_id = '01'

def calculate_sensor_status(response):
    status_byte = response[2:3]
    if status_byte == b'\x01':
        return 1  # Engaged
    elif status_byte == b'\x00':
        return 0  # Disengaged
    elif status_byte == b'\x02':
        return 2  # Error
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
    total_disengaged = sensor_status.count(0)
    total_errors = sensor_status.count(2)
    total_vacancy = total_disengaged
    message = bytearray([0xAA, int(zone_id, 16), total_sensors] + sensor_status + [total_engaged, total_disengaged, total_vacancy,total_errors, 0x55])
    uart1.write(message)

while True:
    process_sensor_requests()

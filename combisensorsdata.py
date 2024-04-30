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
'''
import serial
import time

ser = serial.Serial(port='COM1', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)

while True:
    floor_data = ser.readline()
    #floor_data = b'\xaa\x01\x03\x02\x01\x03\x01\x01\x01\x00U'
    print("data read")
    print(floor_data)
    floor_data_hex = ' '.join(format(byte, '02x').upper() for byte in floor_data)
    print(floor_data_hex)
    if floor_data and floor_data_hex.startswith('AA') and floor_data_hex.endswith('55'):
        zone_id = int.from_bytes(floor_data[1:2], byteorder='big')
        total_sensors = int.from_bytes(floor_data[2:3], byteorder='big') # that means 2 se start karega read karna aur 1 byte read karega. aur agar 3 ki jagah par 4 likhenge means 2 se start krega read karna aur 2 byte read karega
        sensor_status = []
        for i in range(total_sensors):
            sensor_status.append(int.from_bytes(floor_data[3+i:4+i], byteorder='big'))
        total_engaged = int.from_bytes(floor_data[3 + total_sensors:4 + total_sensors], byteorder='big')
        total_disengaged = int.from_bytes(floor_data[4 + total_sensors:5 + total_sensors], byteorder='big')
        total_vacancy = int.from_bytes(floor_data[5 + total_sensors:6 + total_sensors], byteorder='big')
        total_error = int.from_bytes(floor_data[6 + total_sensors:7 + total_sensors], byteorder='big')

        print("Zone ID:", zone_id)
        print("Total sensors:", total_sensors)
        print("Sensor Status:", sensor_status)
        print("Total Engaged:", total_engaged)
        print("Total Disengaged:", total_disengaged)
        print("Total Vacancy:", total_vacancy)
        print("Total Error:", total_error)
    else:
        print("Invalid sensor data format. Reading again...")

    time.sleep(0.1)

ser.close()
'''

#Example-2 
import serial
import time

ser = serial.Serial(port='COM1', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)

while True:
    request = b'01'  # Construct the request
    ser.write(request)  # Send the request
    time.sleep(2)  # Wait for the response

    floor_data = ser.readline()
    #floor_data = b'\xaa\x01\x03\x02\x01\x03\x01\x01\x01\x00U'
    print("data read")
    print(floor_data)
    floor_data_hex = ' '.join(format(byte, '02x').upper() for byte in floor_data)
    print(floor_data_hex)
    if floor_data and floor_data_hex.startswith('AA') and floor_data_hex.endswith('55'):
        zone_id = int.from_bytes(floor_data[1:2], byteorder='big')
        total_sensors = int.from_bytes(floor_data[2:3], byteorder='big')
        sensor_status = [int.from_bytes(floor_data[3+i:4+i], byteorder='big') for i in range(total_sensors)]
        total_engaged = int.from_bytes(floor_data[3 + total_sensors:4 + total_sensors], byteorder='big')
        total_disengaged = int.from_bytes(floor_data[4 + total_sensors:5 + total_sensors], byteorder='big')
        total_vacancy = int.from_bytes(floor_data[5 + total_sensors:6 + total_sensors], byteorder='big')
        total_error = int.from_bytes(floor_data[6 + total_sensors:7 + total_sensors], byteorder='big')

        print("Zone ID:", zone_id)
        print("Total sensors:", total_sensors)
        print("Sensor Status:", sensor_status)
        print("Total Engaged:", total_engaged)
        print("Total Disengaged:", total_disengaged)
        print("Total Vacancy:", total_vacancy)
        print("Total Error:", total_error)
    else:
        print("Invalid sensor data format. Reading again...")

ser.close()

# esp32controlleddocklightmicropython
from using the uart pin. i am sending the data to docklight and also receiving the command and control the led using micropython

#isme humne simply docklight se esp32 ke builtin led ko control kiya hai rs485tottl module ki madad se docklight software ka use karke in micropython. basically when i am using the pin 1 and pin 3 of rs tx then we should use uart 2. then only it work otherwise it won't work. so i have connected rs485to ttl rx pin to esp32 tx pin and rs485tottl tx pin to esp32 rx pin. and rs485tottl vcc to esp32 5v and gnd with esp32 gnd pin. uart = UART(2, baudrate=9600, tx=3, rx=1). basically for default rx and tx pin use the UART2 

zone protocol- #AA(start frame), zone address(01), total sensor(05), 00(sensoraddress01 status) 01(sensoraddress02 status) 01(sensoraddress03 status) 00(sensoraddress04 status) 01(sensoraddress05 status) (Each sensor status), total engaged(03), total disengaged(02), total vacancy(02), total error(00), total no communication(00),55(End of protocol)

floor protocol- FF(floor communication)01(floor address) 04(total zones connected) EE(end of floor) zone 1 data AA to 55 , zone 2 data, zone3 data, zone4 data, total sensor, total engaged, total disengaged, total vacancy, total error, BB. from the master controller.

master protocol- 

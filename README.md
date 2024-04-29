# esp32controlleddocklightmicropython
from using the uart pin. i am sending the data to docklight and also receiving the command and control the led using micropython

#isme humne simply docklight se esp32 ke builtin led ko control kiya hai rs485tottl module ki madad se docklight software ka use karke in micropython. basically when i am using the pin 1 and pin 3 of rs tx then we should use uart 2. then only it work otherwise it won't work. so i have connected rs485to ttl rx pin to esp32 tx pin and rs485tottl tx pin to esp32 rx pin. and rs485tottl vcc to esp32 5v and gnd with esp32 gnd pin. uart = UART(2, baudrate=9600, tx=3, rx=1). basically for default rx and tx pin use the UART2 

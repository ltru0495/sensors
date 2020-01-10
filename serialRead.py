import serial
import time

ser = serial.Serial('/dev/ttyUSB1')
print(ser.name)
counter = 0
while True:
    line = ser.readline().decode('utf-8')
    values = line.split(", ")
    print(values)
#   print(type(values[1]))
    time.sleep(1)
    if counter%10 == 2:
        b = "c".encode()
        ser.write(b)
    counter = counter +1

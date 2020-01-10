import serial
import time
from postRequest import *

def readGasSensor(ser):
    b = "\r".encode()
    ser.write(b)
    line = ser.readline().decode('utf-8')
    values = line.split(", ")
    return values[1]

def run():
    serials = []
    
    for x in range(5):
        serials.append(serial.Serial('/dev/ttyUSB'+str(x)))
    
    while True:
        print("Reading...")
        so2=readGasSensor(serials[0])
        no2=readGasSensor(serials[1])
        h2s=readGasSensor(serials[2])
        co=readGasSensor(serials[3])
        o3=readGasSensor(serials[4])

        data = {
            'dateObserved': {
                'type': 'Text',
                'value': datenow()
            },
            'so2':{
                'type': 'Float',
                'value': so2
            },
            'no2':{
                'type': 'Float',
                'value': no2
            },
            'h2s':{
                'type': 'Float',
                'value': h2s
            },
            'co':{
                'type': 'Float',
                'value': co
            },
            'o3':{
                'type': 'Float',
                'value': o3
            }
        }
        print(data)
        print(post(data))
        time.sleep(delay)

if __name__ == '__main__':
    try:
        run()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
        sys.exit(0)




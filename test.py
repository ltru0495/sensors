import smbus
import time

def readIndex(index):
    lowindex = index
    highindex = lowindex+1
    data = block[lowindex]*256 + block[highindex] 
    return data
    
if __name__ == "__main__":
    bus = smbus.SMBus(1)
    while(True):
        #block = bus.read_byte(0X10)
        block = bus.read_i2c_block_data(0X10, 0)
        print(block)
        #print("pm1.0 at: ", pm1_0_)
        #print("pm2.5 at: ", pm2_5_)
        #print("pm10  at: ", pm10_0_, "\n")
  
        time.sleep(1)


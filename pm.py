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
        block = bus.read_i2c_block_data(0x12, 0, 32)
        
        # Data1 -> 4, 5
        # Data2 -> 6 ,7
        # Data3 -> 8, 9
        pm1_0 = readIndex(4)
        pm2_5 = readIndex(6)
        pm10_0 = readIndex(8)
        
        pm1_0_ = readIndex(10)
        pm2_5_ = readIndex(12)
        pm10_0_ = readIndex(14)
        
        
        print("pm1.0:    ", pm1_0)
        print("pm2.5:    ", pm2_5)
        print("pm10:     ", pm10_0, "\n")
 
        #print("pm1.0 at: ", pm1_0_)
        #print("pm2.5 at: ", pm2_5_)
        #print("pm10  at: ", pm10_0_, "\n")
  
        time.sleep(1)

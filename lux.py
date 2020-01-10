import smbus
import time
import math
import sys

class adps9300(object):
    bus = None;
    addr = 0x39
    
    REG_CONTROL        = 0x00
    REG_TIMING         = 0x01
    REG_THRESHLOWLOW   = 0x02
    REG_THRESHLOWHIGH  = 0x03
    REG_THRESHHIGHLOW  = 0x04
    REG_THRESHHIGHHIGH = 0x05
    REG_INTERRUPT      = 0x06
    REG_CRC            = 0x08
    REG_ID             = 0x0A
    REG_DATA0LOW       = 0x0C
    REG_DATA0HIGH      = 0x0E
    REG_DATA1LOW       = 0x0E
    REG_DATA1HIGH      = 0x0F
    
    REG_CONTROL_CMD = 1<<7
    REG_CONTROL_IRQCLEAR = 1<<6
    REG_CONTROL_WORD = 1<<5
    REG_CONTROL_POWER_ON = 0x03
    
    REG_TIMING_GAIN_1  = 0<<4
    REG_TIMING_GAIN_16 = 1<<4
    REG_TIMING_START_CYCLE = 1<<3
    
    REG_TIMING_INTEGRATE_13_7MS = 0
    REG_TIMING_INTEGRATE_101MS = 1
    REG_TIMING_INTEGRATE_402MS = 2
    
    REG_TIMING_SCALE_13_7MS = 0.034
    REG_TIMING_SCALE_101MS = 0.252
    REG_TIMING_SCALE_402MS = 1
    
    _gain = 0
    _integration = 0
    
     
    def __init__(self):
        self.bus = smbus.SMBus(1);
        self.set_power(True)
        self.set_timing(True, 0);
    
    def set_power(self, on):
        regval = 0
        if on == True:
            regval = self.REG_CONTROL_POWER_ON
        
        self.bus.write_byte_data(self.addr, self.REG_CONTROL | self.REG_CONTROL_CMD, regval); #init
    
    def set_timing(self, highgain, integration):
        #print 'Settings: high gain', highgain, 'integration', integration
        regval = 0
        
        if highgain == True:
            regval = regval | self.REG_TIMING_GAIN_16
            self._gain = 1
        else:
            regval = regval | self.REG_TIMING_GAIN_1
            self._gain = 1 / 16.0
        
        if integration == 0:
            regval = regval | self.REG_TIMING_INTEGRATE_13_7MS
            self._integration = self.REG_TIMING_SCALE_13_7MS
        elif integration == 1:
            regval = regval | self.REG_TIMING_INTEGRATE_101MS
            self._integration = self.REG_TIMING_SCALE_101MS
        else:
            regval = regval | self.REG_TIMING_INTEGRATE_402MS
            self._integration = self.REG_TIMING_SCALE_402MS
            
        self.bus.write_byte_data(self.addr, self.REG_TIMING | self.REG_CONTROL_CMD, regval); #init
    
    def read_raw(self):
        #ch0 = self.bus.read_word_data(self.addr, self.REG_CONTROL_CMD | self.REG_CONTROL_WORD | self.REG_DATA0LOW); # 0xAC
        ch0 = self.bus.read_word_data(self.addr, 0xAC)
        ch1 = self.bus.read_word_data(self.addr, 0xAE)
        block = self.bus.read_i2c_block_data(self.addr, 0, 32)
        print block
        #ch1 = self.bus.read_word_data(self.addr, self.REG_CONTROL_CMD | self.REG_CONTROL_WORD | self.REG_DATA1LOW); # 0xAE
        #print ch0
        #print ch1
        return [ch0, ch1];
    
    def read_lux(self):
        ch0, ch1 = self.read_raw();
        return self.calc_lux(ch0, ch1)
    
    def calc_lux(self, ch0, ch1):
        
        ch0 = ch0 / self._gain / self._integration
        ch1 = ch1 / self._gain / self._integration
        
        if ch0 == 0:
            return None
        
        ch0 = float(ch0)
        ch1 = float(ch1)
        
        lux = 0
   
        d = ch1 / ch0
        if ch1 == ch0 == 65535:
            return float('nan') # out of range
        if d > 0 and d <= 0.5:
            lux = 0.0304 * ch0 - 0.062 * ch0 * math.pow(d, 1.4)
        elif d > 0.5 and d <= 0.61:
            lux = 0.0224 * ch0 - 0.031 * ch1
        elif d > 0.61 and d <= 0.80:
            lux = 0.0128 * ch0 - 0.0153 * ch1
        elif d > 0.80 and d <= 1.30:
            lux = 0.00146 * ch0 - 0.00112 * ch1
        elif d > 1.3:
            lux = 0
        
        return lux

        
if __name__ == "__main__":
    try:
        while(True):
            x = adps9300()
            print "Lux value is %s" % x.read_lux()
            time.sleep(1)
    except IOError, e:
        print e
        print "Error creating connection to i2c.  This must be run as root"

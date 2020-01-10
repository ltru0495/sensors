import time
from smbus import SMBus

bus = SMBus(1)


addr = 0x60
b = bus.read_byte(addr)
print(b)
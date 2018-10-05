import font16
import gxgde0213b1
import machine
import struct
from ohsbadge import epd
from ohsbadge import fb

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
i2c.writeto_mem(30,0x18,b'\x80')
ACCX = struct.unpack("h",i2c.readfrom_mem(30,0x6,2))
ACCY = struct.unpack("h",i2c.readfrom_mem(30,0x8,2))
ACCZ = struct.unpack("h",i2c.readfrom_mem(30,0x10,2))
print("accelerometer: x={0} y={1} z={2}".format(ACCX[0], ACCY[0], ACCZ[0]))

epd.clear_frame(fb)
epd.display_string_at(fb, 0, 0, "accelerometer:", font16, gxgde0213b1.COLORED)
epd.display_string_at(fb, 0, 24, "x={0} y={1} z={2}".format(ACCX[0], ACCY[0], ACCZ[0]), font16, gxgde0213b1.COLORED)
epd.display_frame(fb)

time.sleep(2)

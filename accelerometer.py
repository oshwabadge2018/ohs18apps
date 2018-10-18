# MicroPython demo for accelerometer on Open Hardware Summit badge
#
# WARNING: Make sure that R12 and R13 are populated
#
# R12 and R13 are 2.2K Ohm resistors for the I2C bus.
# This is needed for the accelerometer to work.
# If R12 or R13 are missing, then email: drew@oshpark.com
#
# Blog post:
# http://blog.oshpark.com/2018/10/18/open-hardware-summit-badge-accelerometer-demo/
# 
# Photo gallery:
# https://photos.app.goo.gl/SKBWbUtKghszr9Ns5

import gxgde0213b1
import font16
import font12
from machine import I2C, Pin, TouchPad
import struct
import time
import urandom
from ohsbadge import epd
from ohsbadge import fb

# from Magic 8-Ball app by Steve Pomeroy https://hackaday.io/xxv
# github.com/oshwabadge2018/ohs18apps/blob/master/magic8ball.py
class TouchButton(object):
   def __init__(self, pin, on_pressed, threshold=400, debounce_ms=50):
       self._touchpad = machine.TouchPad(pin)
       self._on_pressed = on_pressed
       self._threshold = threshold
       self._debounce_ms = debounce_ms
       self._down_ms = None
       self._pressed = False

   def read(self):
       if self._touchpad.read() < self._threshold:
           if not self._pressed:
               if not self._down_ms:
                   self._down_ms = time.ticks_ms()
               else:
                   if time.ticks_diff(time.ticks_ms(), self._down_ms) > self._debounce_ms:
                       self._on_pressed()
                       self._pressed = True
       else:
           self._pressed = False
           self._down_ms = None

# from accelerometer demo app
# github.com/oshwabadge2018/ohs18apps/blob/master/accelerometer.py
class Accelerometer():
   def clear_screen():
       epd.initPart()
       epd.clear_frame(fb)
       epd.display_frame(fb)

   def show_message(message):
       epd.init()
       epd.clear_frame(fb)
       epd.display_string_at(fb, 0, 52, message, font16, gxgde0213b1.COLORED)
       epd.display_frame(fb)

   def read_accel(i2c):
       i2c.writeto_mem(30, 0x18, b'\x80')
       x = struct.unpack("h", i2c.readfrom_mem(30, 0x6, 2))
       y = struct.unpack("h", i2c.readfrom_mem(30, 0x8, 2))
       z = struct.unpack("h", i2c.readfrom_mem(30, 0xA, 2))
       return (x[0], y[0], z[0])

   def get_orientation(i2c):
       pos = Accelerometer.read_accel(i2c)
       return pos

   def main(f):
       i2c = machine.I2C(scl=Pin(22), sda=Pin(21))
       epd.init()
       epd.set_rotate(gxgde0213b1.ROTATE_270)
       epd.clear_frame(fb)
       epd.display_frame(fb)
       keep_on = [True]

       def exit_loop():
           keep_on[0] = False

       exit_button = TouchButton(Pin(32), exit_loop)

       while keep_on[0]:
           exit_button.read()
           orientation = Accelerometer.get_orientation(i2c)
           x = "x={0}".format(orientation[0])
           y = "y={0}".format(orientation[1])
           z = "z={0}".format(orientation[2])
           print(x, y, z)
           epd.clear_frame(fb)
           epd.set_rotate(gxgde0213b1.ROTATE_270)
           epd.display_string_at(fb, 10,  0, x, font16, gxgde0213b1.COLORED)
           epd.display_string_at(fb, 10, 24, y, font16, gxgde0213b1.COLORED)
           epd.display_string_at(fb, 10, 48, z, font16, gxgde0213b1.COLORED)
           epd.display_frame(fb)
           time.sleep(1)

accel = Accelerometer()
accel.main()

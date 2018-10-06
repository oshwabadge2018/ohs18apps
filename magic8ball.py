# created by Steve Pomeroy https://hackaday.io/xxv
# modified by Drew Fustini to run once and exit
#
# blog post:
# http://blog.oshpark.com/2018/10/04/open-hardware-summit-badge-magic-8-ball-app/
#
# photo gallery:
# https://photos.app.goo.gl/f1y8PSHfYAaa4xTu7
#
# transfer to Open Hardware Summit badge using FTP:
# https://oshwabadge2018.github.io/docs.html#uploading-over-ftp

import gxgde0213b1
import font16
import font12
from machine import I2C, Pin, TouchPad
import struct
import time
import urandom
from ohsbadge import epd
from ohsbadge import fb


class TouchButton(object):
    def __init__(self, pin, on_pressed, threshold=400, debounce_ms=50):
        self._touchpad = TouchPad(pin)
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
    new_orientation = None

    pos = read_accel(i2c)

    if pos[2] > 13000:
        new_orientation = "upright"
    elif pos[2] < -13000:
        new_orientation = "prone"

    return new_orientation


def main():
    phrases = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    i2c = I2C(scl=Pin(22), sda=Pin(21))

    epd.init()
    epd.set_rotate(gxgde0213b1.ROTATE_270)
    epd.clear_frame(fb)
    epd.display_frame(fb)

    prev_orientation = None

    keep_on = [True]

    def exit_loop():
        keep_on[0] = False

    exit_button = TouchButton(Pin(32), exit_loop)

    while keep_on[0]:
        exit_button.read()
        orientation = get_orientation(i2c)

        if orientation and orientation != prev_orientation:
            if orientation == 'upright':
                show_message(urandom.choice(phrases))
            elif orientation == 'prone':
                clear_screen()
            prev_orientation = orientation

        time.sleep(0.1)

main()

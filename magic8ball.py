# created by Steve Pomeroy https://hackaday.io/xxv
# modified by Drew Fustini to run once and exit
#
# photo gallery:
# https://photos.app.goo.gl/f1y8PSHfYAaa4xTu7
#
# transfer to Open Hardware Summit badge using FTP:
# https://oshwabadge2018.github.io/docs.html#uploading-over-ftp

import gxgde0213b1
import font16
import font12
import urandom
import time

phrases = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]

epd.clear_frame(fb)
epd.set_rotate(gxgde0213b1.ROTATE_270)
epd.clear_frame(fb)
epd.display_string_at(fb, 0, 60, urandom.choice(phrases), font16, gxgde0213b1.COLORED)
epd.display_frame(fb)
time.sleep(2)

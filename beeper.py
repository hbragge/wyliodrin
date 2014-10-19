import os
import struct

from threading import Timer
from time import *

try:
  from wyliodrin import *
except:
  from wiringpi2 import *
  wiringPiSetup()

if os.getenv ("wyliodrin_board") == "raspberrypi":
  grove = 300
  grovepiSetup (grove, 4)
else:
  grove = 0

lcd = rgb_lcd()
lcd.begin(16, 1)

pinMode (2, 0)

buttons = {}

def buttonSwitched(button, expectedValue):
  value = digitalRead (button)
  stable = True
  for i in range (100):
    valuenext = digitalRead (button)
    if value != valuenext:
      stable = False
  if stable:
    if button in buttons and value != buttons[button]:
      buttons[button] = value
      return value == expectedValue
    elif not button in buttons:
      buttons[button] = value
      return False
    else:
      return False
  return False

buttons[2] = digitalRead (2)

def colorToRGB (color):
  return struct.unpack ('BBB', color[1:].decode('hex'))

def loopCode():
  if buttonSwitched (grove+2, 1):
    lcd.display()
    color = colorToRGB('#ff9900')
    lcd.setRGB(color[0], color[1], color[2] )
  Timer(0.1, loopCode).start()

def loopCode2():
  color2 = colorToRGB('#000000')
  lcd.setRGB(color2[0], color2[1], color2[2] )
  lcd.noDisplay()
  Timer(10, loopCode2).start()

def myFunction(__sender, __channel, __error, __message):
  analogWrite (grove+5, 0)
  digitalWrite (grove+5, 1)
  sleep (0.025)
  digitalWrite (grove+5, 0)
  lcd.display()
  color = colorToRGB('#ff9900')
  lcd.setRGB(color[0], color[1], color[2] )
  lcd.write(str(json.loads(__message)))

def main():
  lcd.display()
  lcd.write(str('no messages'))
  Timer(0.1, loopCode).start()
  Timer(5, loopCode2).start()
  openConnection('notification', myFunction)

if __name__ == "__main__":
  main()


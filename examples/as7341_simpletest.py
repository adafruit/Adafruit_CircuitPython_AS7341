# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
from time import sleep
import board
import adafruit_as7341
from adafruit_debug_i2c import DebugI2C

i2c = board.I2C()
i2c = DebugI2C(i2c)
sensor = adafruit_as7341.AS7341(i2c)
print("out of init!")
print("Current current is")
print(sensor.led_current)
print("Setting current")
sensor.led_current = 50
print("enabling led")
sensor.led = True
sleep(0.1)
print("disabling LED")
sensor.led = False

print("led status:", sensor.led)

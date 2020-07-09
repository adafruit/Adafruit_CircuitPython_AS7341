# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import board
import adafruit_as7341
from adafruit_debug_i2c import DebugI2C

i2c = board.I2C()
i2c = DebugI2C(i2c)
sensor = adafruit_as7341.AS7341(i2c)
print("out of init!")

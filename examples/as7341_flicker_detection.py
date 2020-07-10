# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
from time import sleep
import board
import busio
from adafruit_as7341 import AS7341, Gain

i2c = busio.I2C(board.SCL, board.SDA)
sensor = AS7341(i2c)
sensor.atime = 100
sensor.astep = 999
sensor.gain = Gain.GAIN_256X  # pylint:disable=no-member
while True:
    sensor.setup_1k_flicker_detection()
    status = sensor.flicker_detection_status()
    print("** 1k flicker test **")
    print("Status:", status)
    if status == 44:
        print("Unknown frequency")
    elif status == 45:
        print("1000 Hz detected")
    elif status == 46:
        print("1200 Hz detected")
    else:
        print("Status:", bin(status))
        print("Error in reading")

    sleep(1)

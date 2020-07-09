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

sensor.setup_f1_f4()

while True:

    sensor.wait_for_data()
    bulk_reads = sensor.all_channels
    print("ADC0/F1-", bulk_reads[0])
    print("ADC1/F2-", bulk_reads[1])
    print("ADC2/F3-", bulk_reads[2])
    print("ADC3/F4-", bulk_reads[3])
    print("ADC4/Clear-", bulk_reads[4])
    print("ADC5/NIR-", bulk_reads[5])

    print("*************************************************")
    sleep(0.3)

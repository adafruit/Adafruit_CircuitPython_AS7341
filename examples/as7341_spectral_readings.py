# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
from time import sleep
import board
import busio
from adafruit_as7341 import AS7341, Gain

# from adafruit_debug_i2c ix`mport DebugI2C
i2c = busio.I2C(board.SCL, board.SDA)
# i2c = DebugI2C(i2c)
sensor = AS7341(i2c)
sensor.atime = 100
sensor.astep = 999
sensor.gain = Gain.GAIN_256X  # pylint:disable=no-member

# sensor.setup_f1_f4()
sensor.setup_f5_f8()


def bar_graph(value):
    sm = int(value / 1000)
    return sm * "*"


while True:

    sensor.setup_f1_f4()
    sensor.wait_for_data()
    bulk_reads = sensor.all_channels

    sensor.setup_f5_f8()
    sensor.wait_for_data()
    bulk_reads2 = sensor.all_channels
    print("F1 - 415nm/Violet %s" % bar_graph(bulk_reads[0]))
    print("F2 - 445nm/Indigo %s" % bar_graph(bulk_reads[1]))
    print("F3 - 480nm/Blue   %s" % bar_graph(bulk_reads[2]))
    print("F4 - 515nm/Cyan   %s" % bar_graph(bulk_reads[3]))
    print("F5 - 555nm/Green  %s" % bar_graph(bulk_reads2[0]))
    print("F6 - 590nm/Yellow %s" % bar_graph(bulk_reads2[1]))
    print("F7 - 630nm/Orange %s" % bar_graph(bulk_reads2[2]))
    print("F8 - 680nm/Red    %s" % bar_graph(bulk_reads2[3]))
    # print("Clear-            %s"%bar(bulk_reads2[4]))
    print("NIR-              %s" % bar_graph(bulk_reads2[5]))
    print("")
    print("---------------------------------------------------")
    sleep(0.1)

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


def bar_graph(value):
    sm = int(value / 1000)
    return sm * "*"


while True:

    print("F1 - 415nm/Violet %s" % bar_graph(sensor.channel_415nm))
    print("F2 - 445nm/Violet %s" % bar_graph(sensor.channel_445nm))
    print("F3 - 480nm/Violet %s" % bar_graph(sensor.channel_480nm))
    print("F4 - 515nm/Violet %s" % bar_graph(sensor.channel_515nm))
    # print("F2 - 445nm/Indigo %s" % bar_graph(bulk_reads[1]))
    # print("F3 - 480nm/Blue   %s" % bar_graph(bulk_reads[2]))
    # print("F4 - 515nm/Cyan   %s" % bar_graph(bulk_reads[3]))
    
    # print("F5 - 555nm/Green  %s" % bar_graph(bulk_reads2[0]))
    # print("F6 - 590nm/Yellow %s" % bar_graph(bulk_reads2[1]))
    # print("F7 - 630nm/Orange %s" % bar_graph(bulk_reads2[2]))
    # print("F8 - 680nm/Red    %s" % bar_graph(bulk_reads2[3]))
    print("\n------------------------------------------------")

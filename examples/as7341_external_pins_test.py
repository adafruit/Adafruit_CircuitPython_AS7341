# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
from time import sleep
import board
import busio
from adafruit_as7341 import AS7341

i2c = busio.I2C(board.SCL, board.SDA)
sensor = AS7341(i2c)


def bar_graph(value):
    sm = int(value / 1000)
    print(value)
    return sm * "*"


sensor.configure_ext_pins()
while True:
    # sensor._wait_for_data()

    # print("F1 - 415nm/Violet %s" % bar_graph(sensor._channel_0_data))
    # print("ADC1              %s" % bar_graph(sensor._channel_1_data))
    # print("ADC2              %s" % bar_graph(sensor._channel_2_data))
    # print("ADC3              %s" % bar_graph(sensor._channel_3_data))
    # print("GPIO EXT          %s" % bar_graph(sensor._channel_4_data))
    # print("INT  EXT          %s" % bar_graph(sensor._channel_5_data))
    print("\n------------------------------------------------")
    sleep(1)

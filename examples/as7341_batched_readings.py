# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
from time import sleep

import board

from adafruit_as7341 import AS7341

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = AS7341(i2c)


def bar_graph(read_value):
    scaled = int(read_value / 1000)
    return f"[{read_value:5d}] " + (scaled * "*")


while True:
    sensor_channels = sensor.all_channels
    print(f"F1 - 415nm/Violet  {bar_graph(sensor_channels[0])}")
    print(f"F2 - 445nm//Indigo {bar_graph(sensor_channels[1])}")
    print(f"F3 - 480nm//Blue   {bar_graph(sensor_channels[2])}")
    print(f"F4 - 515nm//Cyan   {bar_graph(sensor_channels[3])}")
    print(f"F5 - 555nm/Green   {bar_graph(sensor_channels[4])}")
    print(f"F6 - 590nm/Yellow  {bar_graph(sensor_channels[5])}")
    print(f"F7 - 630nm/Orange  {bar_graph(sensor_channels[6])}")
    print(f"F8 - 680nm/Red     {bar_graph(sensor_channels[7])}")
    print("\n------------------------------------------------")

    sleep(1)

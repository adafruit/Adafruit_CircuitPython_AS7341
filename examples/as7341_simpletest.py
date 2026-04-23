# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
from time import sleep

import board

import adafruit_as7341

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_as7341.AS7341(i2c)

sensor.gain = adafruit_as7341.Gain.GAIN_0_5X  # Update the gain of the sensor


def bar_graph(read_value):
    scaled = int(read_value / 1000)
    return f"[{read_value:5d}] " + (scaled * "*")


while True:
    print(f"F1 - 415nm/Violet  {bar_graph(sensor.channel_415nm)}")
    print(f"F2 - 445nm//Indigo {bar_graph(sensor.channel_445nm)}")
    print(f"F3 - 480nm//Blue   {bar_graph(sensor.channel_480nm)}")
    print(f"F4 - 515nm//Cyan   {bar_graph(sensor.channel_515nm)}")
    print(f"F5 - 555nm/Green   {bar_graph(sensor.channel_555nm)}")
    print(f"F6 - 590nm/Yellow  {bar_graph(sensor.channel_590nm)}")
    print(f"F7 - 630nm/Orange  {bar_graph(sensor.channel_630nm)}")
    print(f"F8 - 680nm/Red     {bar_graph(sensor.channel_680nm)}")
    print(f"Clear              {bar_graph(sensor.channel_clear)}")
    print(f"Near-IR (NIR)      {bar_graph(sensor.channel_nir)}")
    print("\n------------------------------------------------")
    sleep(1)

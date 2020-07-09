from time import sleep
import board
from adafruit_as7341 import AS7341, Gain
from adafruit_debug_i2c import DebugI2C
import busio

i2c = busio.I2C(board.SCL, board.SDA)
# i2c = DebugI2C(i2c)
sensor = AS7341(i2c)
sensor.atime = 100
sensor.astep = 999
sensor.gain = Gain.GAIN_256X  # pylint:disable=no-member

sensor.setup_f1_f4()

while True:

    sensor.wait_for_data()

    # Steps defined to print out 6 channels F1, F2,F3,F4,NIR,Clear

    print("ADC0/F1-", sensor._channel_0_data)
    print("ADC1/F2-", sensor._channel_1_data)
    print("ADC2/F3-", sensor._channel_2_data)
    print("ADC3/F4-", sensor._channel_3_data)
    print("ADC4/Clear-", sensor._channel_4_data)
    print("ADC5/NIR-", sensor._channel_5_data)
    print("*************************************************")
    sleep(0.3)

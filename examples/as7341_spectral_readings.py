from time  import sleep
import board
from adafruit_as7341 import AS7341, Gain
from adafruit_debug_i2c import DebugI2C
import busio

i2c = busio.I2C(board.SCL, board.SDA)
i2c = DebugI2C(i2c)
sensor = AS7341(i2c)
sensor.atime = 100
sensor.astep = 999
sensor.gain = Gain.GAIN_256X
# F1 415 26
# F2 445 30
# F3 480 36
# F4 515 39
# F5 555 39
# F6 590 40
# F7 630 50
# F8 680 52


#disable SP_EN bit while  making config changes
sensor._color_meas_enabled = False
# as7341.readRawValuesMode1()
#   # Write SMUX configuration from RAM to set SMUX chain registers (Write 0x10
#   # to CFG6)

# sensor.SmuxConfigRAM()
sensor._smux_command = 2
# Write new configuration to all the 20 registers

# sensor.F1F4_Clear_NIR()
sensor.f1f4_clear_nir()
# Start SMUX command
sensor._smux_enabled = True

# Enable SP_EN bit
sensor._color_meas_enabled = True

# Reading and Polling the the AVALID bit in Status 2 Register 0xA3

while not sensor._data_ready_bit:
    sleep(0.001)

# Steps defined to print out 6 channels F1, F2,F3,F4,NIR,Clear

print("ADC0/F1-", sensor._channel_0_data
# print("ADC1/F2-", readChannel(AS7341_CHANNEL_1))
# print("ADC2/F3-", readChannel(AS7341_CHANNEL_2))
# print("ADC3/F4-", readChannel(AS7341_CHANNEL_3))
# print("ADC4/Clear-", readChannel(AS7341_CHANNEL_4))
# print("ADC5/NIR-", readChannel(AS7341_CHANNEL_5))

# while True:
#     print("light", sensor.band_415nm)
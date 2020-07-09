# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_as7341`
================================================================================

CircuitPython library for use with the Adafruit AS7341 breakout


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

* `Adafruit AS7341 Breakout <https://www.adafruit.com/products/45XX>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

 * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
 * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_AS7341.git"
from time import sleep, monotonic
from micropython import const
import adafruit_bus_device.i2c_device as i2c_device

from adafruit_register.i2c_struct import UnaryStruct, Struct  # , ROUnaryStruct
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import ROBits, RWBits

# pylint: disable=bad-whitespace
_AS7341_DEVICE_ID = const(0b001001)  # Correct content of WHO_AM_I register
_AS7341_I2CADDR_DEFAULT = const(0x39)  # AS7341 default i2c address
_AS7341_CHIP_ID = const(0x09)  # AS7341 default device id from WHOAMI
_AS7341_WHOAMI = const(0x92)  # Chip ID register
_AS7341_CONFIG = const(0x70)  # Enables LED control and sets light sensing mode
_AS7341_GPIO = const(0x73)  # Connects photo diode to GPIO or INT pins
_AS7341_LED = const(0x74)  # LED Register; Enables and sets current limit
_AS7341_ENABLE = const(
    0x80
)  # Main enable register. Controls SMUX, Flicker Detection,Spectral and Power
_AS7341_ATIME = const(0x81)  # Sets ADC integration step count
_AS7341_SP_LOW_TH_L = const(0x84)  # Spectral measurement Low Threshold low byte
_AS7341_SP_LOW_TH_H = const(0x85)  # 0 Spectral measurement Low Threshold high byte
_AS7341_SP_HIGH_TH_L = const(0x86)  # Spectral measurement High Threshold low byte
_AS7341_SP_HIGH_TH_H = const(0x87)  # Spectral measurement High Threshold low byte
_AS7341_STATUS = const(
    0x93
)  # Interrupt status registers. Indicates the occourance of an interrupt
_AS7341_CH0_DATA_L = const(0x95)  # ADC Channel 0 Data
_AS7341_CH0_DATA_H = const(0x96)  # ADC Channel 0 Data
_AS7341_CH1_DATA_L = const(0x97)  # ADC Channel 1 Data
_AS7341_CH1_DATA_H = const(0x98)  # ADC Channel 1 Data
_AS7341_CH2_DATA_L = const(0x99)  # ADC Channel 2 Data
_AS7341_CH2_DATA_H = const(0x9A)  # ADC Channel 2 Data
_AS7341_CH3_DATA_L = const(0x9B)  # ADC Channel 3 Data
_AS7341_CH3_DATA_H = const(0x9C)  # ADC Channel 3 Data
_AS7341_CH4_DATA_L = const(0x9D)  # ADC Channel 4 Data
_AS7341_CH4_DATA_H = const(0x9E)  # ADC Channel 4 Data
_AS7341_CH5_DATA_L = const(0x9F)  # ADC Channel 5 Data
_AS7341_CH5_DATA_H = const(0xA0)  # ADC Channel 5 Data
_AS7341_STATUS2 = const(0xA3)  # Measurement status flags; saturation, validity
_AS7341_STATUS3 = const(0xA4)  # Spectral interrupt source, high or low threshold
_AS7341_CFG0 = const(
    0xA9
)  # Sets Low power mode, Register bank, and Trigger lengthening
_AS7341_CFG1 = const(0xAA)  # Controls ADC Gain
_AS7341_CFG6 = const(0xAF)  # Used to configure Smux
_AS7341_CFG9 = const(0xB2)  # flicker detect and SMUX command system ints
_AS7341_CFG12 = const(0xB5)  # ADC channel for interrupts, persistence and auto-gain
_AS7341_PERS = const(
    0xBD
)  # number of measurements outside thresholds to trigger an interrupt
_AS7341_GPIO2 = const(
    0xBE
)  # GPIO Settings and status: polarity, direction, sets output, reads
_AS7341_ASTEP_L = const(0xCA)  # Integration step size ow byte
_AS7341_ASTEP_H = const(0xCB)  # Integration step size high byte
_AS7341_FD_TIME1 = const(0xD8)  # Flicker detection integration time low byte
_AS7341_FD_TIME2 = const(0xDA)  # Flicker detection gain and high nibble
_AS7341_FD_STATUS = const(
    0xDB
)  # Flicker detection status; measurement valid, saturation, flicker
_AS7341_INTENAB = const(0xF9)  # Enables individual interrupt types
_AS7341_CONTROL = const(0xFA)  # Auto-zero, fifo clear, clear SAI active


def _low_bank(func):
    # pylint:disable=protected-access
    def _decorator(self, *args, **kwargs):
        self._low_bank_active = True
        retval = func(self, *args, **kwargs)
        self._low_bank_active = False
        return retval

    return _decorator


class CV:
    """struct helper"""

    @classmethod
    def add_values(cls, value_tuples):
        """Add CV values to the class"""
        cls.string = {}
        cls.lsb = {}

        for value_tuple in value_tuples:
            name, value, string, lsb = value_tuple
            setattr(cls, name, value)
            cls.string[value] = string
            cls.lsb[value] = lsb

    @classmethod
    def is_valid(cls, value):
        """Validate that a given value is a member"""
        return value in cls.string


class Gain(CV):
    """Options for ``accelerometer_range``"""

    pass  # pylint: disable=unnecessary-pass


Gain.add_values(
    (
        ("GAIN_0_5X", 0, 0.5, None),
        ("GAIN_1X", 1, 1, None),
        ("GAIN_2X", 2, 2, None),
        ("GAIN_4X", 3, 4, None),
        ("GAIN_8X", 4, 8, None),
        ("GAIN_16X", 5, 16, None),
        ("GAIN_32X", 6, 32, None),
        ("GAIN_64X", 7, 64, None),
        ("GAIN_128X", 8, 128, None),
        ("GAIN_256X", 9, 256, None),
        ("GAIN_512X", 10, 512, None),
    )
)


class AS7341:  # pylint:disable=too-many-instance-attributes
    """Library for the AS7341 Sensor


        :param ~busio.I2C i2c_bus: The I2C bus the AS7341 is connected to.
        :param address: The I2C address of the sensor

    """

    _device_id = ROBits(6, _AS7341_WHOAMI, 2)

    _smux_enable_bit = RWBit(_AS7341_ENABLE, 4)
    _led_control_enabled = RWBit(_AS7341_CONFIG, 3)
    _color_meas_enabled = RWBit(_AS7341_ENABLE, 1)
    _power_enabled = RWBit(_AS7341_ENABLE, 0)

    _low_bank_active = RWBit(_AS7341_CFG0, 4)
    _smux_command = RWBits(2, _AS7341_CFG6, 3)

    _channel_0_data = UnaryStruct(_AS7341_CH0_DATA_L, "<H")
    _channel_1_data = UnaryStruct(_AS7341_CH1_DATA_L, "<H")
    _channel_2_data = UnaryStruct(_AS7341_CH2_DATA_L, "<H")
    _channel_3_data = UnaryStruct(_AS7341_CH3_DATA_L, "<H")
    _channel_4_data = UnaryStruct(_AS7341_CH4_DATA_L, "<H")
    _channel_5_data = UnaryStruct(_AS7341_CH5_DATA_L, "<H")

    _all_channels = Struct(_AS7341_CH0_DATA_L, "<HHHHHH")
    _led_current_bits = RWBits(7, _AS7341_LED, 0)
    _led_enabled = RWBit(_AS7341_LED, 7)
    _cfg0 = UnaryStruct(_AS7341_CFG0, "<B")
    atime = UnaryStruct(_AS7341_ATIME, "<B")
    """The integration time step count.
    Total integration time will be ``(ATIME + 1) * (ASTEP + 1) * 2.78µS``
    """
    astep = UnaryStruct(_AS7341_ASTEP_L, "<H")
    """ The integration time step size in 2.78 microsecond increments"""
    _gain = UnaryStruct(_AS7341_CFG1, "<B")
    """The ADC gain multiplier
    *
    * @param gain_value The gain amount. must be an `as7341_gain_t`
    * @return true: success false: failure
    */
    """
    _data_ready_bit = RWBit(_AS7341_STATUS2, 6)
    """
 * @brief
 *
 * @return true: success false: failure
    """

    def __init__(self, i2c_bus, address=_AS7341_I2CADDR_DEFAULT):

        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        if not self._device_id in [_AS7341_DEVICE_ID]:
            raise RuntimeError("Failed to find an AS7341 sensor - check your wiring!")
        self.reset()
        self.initialize()
        self._buffer = bytearray(2)

    def initialize(self):
        """Configure the sensors with the default settings. For use after calling `reset()`"""

        self._power_enabled = True
        self._led_control_enabled = True

    def reset(self):
        """Resets the internal registers and restores the default settings"""

    @property
    def all_channels(self):
        """The current readings for all six ADC channels"""
        return self._all_channels

    def wait_for_data(self, timeout=1.0):
        """Wait for sensor data to be ready"""
        start = monotonic()
        while not self._data_ready_bit:
            if monotonic() - start > timeout:
                raise RuntimeError("Timeout occoured waiting for sensor data")
            sleep(0.001)

    def _write_register(self, addr, data):

        self._buffer[0] = addr
        self._buffer[1] = data

        with self.i2c_device as i2c:
            i2c.write(self._buffer)

    def setup_f1_f4(self):
        """Configure the sensor to read from elements F1-F4, Clear, and NIR"""
        # disable SP_EN bit while  making config changes
        self._color_meas_enabled = False
        # as7341.readRawValuesMode1()

        # ENUM-ify
        self._smux_command = 2
        # Write new configuration to all the 20 registers

        self._f1f4_clear_nir()
        # Start SMUX command
        self._smux_enabled = True

        # Enable SP_EN bit
        self._color_meas_enabled = True

    def _f1f4_clear_nir(self):
        """Configure SMUX for sensors F1-F4, Clear and NIR"""
        self._write_register(0x00, 0x30)  # F3 left set to ADC2
        self._write_register(0x01, 0x01)  # F1 left set to ADC0
        self._write_register(0x02, 0x00)  # Reserved or disabled
        self._write_register(0x03, 0x00)  # F8 left disabled
        self._write_register(0x04, 0x00)  # F6 left disabled
        self._write_register(
            0x05, 0x42
        )  # F4 left connected to ADC3/f2 left connected to ADC1
        self._write_register(0x06, 0x00)  # F5 left disbled
        self._write_register(0x07, 0x00)  # F7 left disbled
        self._write_register(0x08, 0x50)  # CLEAR connected to ADC4
        self._write_register(0x09, 0x00)  # F5 right disabled
        self._write_register(0x0A, 0x00)  # F7 right disabled
        self._write_register(0x0B, 0x00)  # Reserved or disabled
        self._write_register(0x0C, 0x20)  # F2 right connected to ADC1
        self._write_register(0x0D, 0x04)  # F4 right connected to ADC3
        self._write_register(0x0E, 0x00)  # F6/F7 right disabled
        self._write_register(0x0F, 0x30)  # F3 right connected to AD2
        self._write_register(0x10, 0x01)  # F1 right connected to AD0
        self._write_register(0x11, 0x50)  # CLEAR right connected to AD4
        self._write_register(0x12, 0x00)  # Reserved or disabled
        self._write_register(0x13, 0x06)  # NIR connected to ADC5

    # F1 415 26
    # F2 445 30
    # F3 480 36
    # F4 515 39
    # F5 555 39
    # F6 590 40
    # F7 630 50
    # F8 680 52
    @property
    def gain(self):
        """The ADC gain multiplier. Must be a valid `adafruit_as7341.Gain`
        """
        return self._gain

    @gain.setter
    def gain(self, gain_value):
        if not Gain.is_valid(gain_value):
            raise AttributeError("`gain` must be a valid `adafruit_as7341.Gain`")
        self._gain = gain_value

    @property
    def _smux_enabled(self):
        return self._smux_enable_bit

    @_smux_enabled.setter
    def _smux_enabled(self, enable_smux):
        self._low_bank_active = False
        self._smux_enable_bit = enable_smux
        while self._smux_enable_bit is True:
            sleep(0.001)

    @property
    def led_current(self):
        """The maximum allowed current through the attached LED in milliamps.
        Odd numbered values will be rounded down to the next lowest even number due
        to the internal configuration restrictions"""
        self._low_bank_active = True
        current_val = self._led_current_bits
        self._low_bank_active = False
        return current_val

    @led_current.setter
    def led_current(self, led_curent):
        self._low_bank_active = True
        new_current = int((led_curent - 4) / 2)
        print("set current:", led_curent, "sending:", new_current)
        self._led_current_bits = new_current
        self._low_bank_active = False

    @property
    @_low_bank
    def led(self):
        """The  attached LED. Set to True to turn on, False to turn off"""
        return self._led_enabled

    @led.setter
    @_low_bank
    def led(self, led_on):
        """The  attached LED. Set to True to turn on, False to turn off"""
        self._led_enabled = led_on


# /**
#  * @brief ADC Channel specifiers for configuration
#  *
#  */
# typedef enum {
#   AS7341_CHANNEL_0,
#   AS7341_CHANNEL_1,
#   AS7341_CHANNEL_2,
#   AS7341_CHANNEL_3,
#   AS7341_CHANNEL_4,
#   AS7341_CHANNEL_5,
# } as7341_channel_t;

# /**
#  * @brief The number of measurement cycles with spectral data outside of a
#  * threshold required to trigger an interrupt
#  *
#  */
# typedef enum {
#   AS7341_INT_COUNT_ALL, 0
#   AS7341_INT_COUNT_1, 1
#   AS7341_INT_COUNT_2, 2
#   AS7341_INT_COUNT_3, 3
#   AS7341_INT_COUNT_5, 4
#   AS7341_INT_COUNT_10, 5
#   AS7341_INT_COUNT_15, 6
#   AS7341_INT_COUNT_20, 7
#   AS7341_INT_COUNT_25, 8
#   AS7341_INT_COUNT_30, 9
#   AS7341_INT_COUNT_35, 10
#   AS7341_INT_COUNT_40, 11
#   AS7341_INT_COUNT_45, 12
#   AS7341_INT_COUNT_50, 13
#   AS7341_INT_COUNT_55, 14
#   AS7341_INT_COUNT_60, 15
# } as7341_int_cycle_count_t;

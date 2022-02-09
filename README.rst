Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-as7341/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/as7341/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_AS7341/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_AS7341/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython library for use with the Adafruit AS7341 breakout.
**NOTE**: Due to the size of this library, it may not work on M0 (ex: Trinket M0) and other
low memory boards.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-as7341/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-as7341

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-as7341

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-as7341

Usage Example
=============

.. code-block:: python3

    from time import sleep
    import board
    from adafruit_as7341 import AS7341

    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = AS7341(i2c)


    def bar_graph(read_value):
        scaled = int(read_value / 1000)
        return "[%5d] " % read_value + (scaled * "*")


    while True:

        print("F1 - 415nm/Violet  %s" % bar_graph(sensor.channel_415nm))
        print("F2 - 445nm//Indigo %s" % bar_graph(sensor.channel_445nm))
        print("F3 - 480nm//Blue   %s" % bar_graph(sensor.channel_480nm))
        print("F4 - 515nm//Cyan   %s" % bar_graph(sensor.channel_515nm))
        print("F5 - 555nm/Green   %s" % bar_graph(sensor.channel_555nm))
        print("F6 - 590nm/Yellow  %s" % bar_graph(sensor.channel_590nm))
        print("F7 - 630nm/Orange  %s" % bar_graph(sensor.channel_630nm))
        print("F8 - 680nm/Red     %s" % bar_graph(sensor.channel_680nm))
        print("Clear              %s" % bar_graph(sensor.channel_clear))
        print("Near-IR (NIR)      %s" % bar_graph(sensor.channel_nir))
        print("\n------------------------------------------------")
        sleep(1)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/as7341/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_AS7341/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

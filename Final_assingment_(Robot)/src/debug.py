#!/usr/bin/env python3

"""
Module used to run the robot in "Debug" mode, where each button
is mapped to a function. The following diagram represents the
mapping of robot keys to functions:
 ____
|____\ -> Backspace (Print code read and prepare for next one)
             ____
          __|____|__ -> Up (Advance scroll using scroll_step())
         |* |    |  |
         |  | ** |  | -> Left (Scroll sensor using scroll_sensor())
         |__|____|__|
            |____| -> Down (Readjust barcode if failed to read red
                      at start using readjust_barcode())

* -> Right (Resets sensor position using reset_sensor())
** -> Enter (Saves current binary value read to list)
"""

from enum import IntEnum
from hamming_code import HammingCode, HCResult
from stack_machine import StackMachine, SMState
from robot import *


class Color(IntEnum):
    """
    Enum used to interact with values read from the sensor
    """
    RED = 0
    GREEN = 1
    BLUE = 2


def run():
    robot = Robot()
    decoder = HammingCode()
    sm = StackMachine()
    cs = ev3.ColorSensor("in4")
    cs.mode = 'RGB-RAW'
    btn = ev3.Button()
    word = []
    spk = ev3.Sound()
    spk.speak("Running on debug mode")
    while True:
        value = cs.bin_data("hhhh")
        print("value: " + str(value) + " / interpreted as: " + translate_raw(value))
        if btn.up:
            robot.scroll_step()
        if btn.right:
            robot.sensor_step()
        if btn.left:
            robot.sensor_reset()
        if btn.enter:
            word.append(bin_value(translate_raw(value)))
        if btn.backspace:
            print(str(word))
            word.append("-")
        if btn.down:
            robot.readjust_barcode()
        sleep(0.25)


def translate(value):
    """
    Translates value of color sensor to the color detected when in "COL-COLOR" mode
    """
    if value == 1:
        return "black"
    elif value == 2:
        return "blue"
    elif value == 3:
        return "green"
    elif value == 4:
        return "yellow"
    elif value == 5:
        return "red"
    elif value == 6:
        return "white"
    elif value == 7:
        return "brown"
    else:
        return "Error"


def translate_raw(value):
    """
    Translates value of color sensor to the color detected when in "RAW-RGB" mode
    """
    if value[Color.RED] < 200 and value[Color.GREEN] < 250 and value[Color.BLUE] < 200:
        return "black"
    elif value[Color.RED] > value[Color.GREEN] and value[Color.RED] > value[Color.BLUE]:
        return "red"
    elif value[Color.RED] < value[Color.GREEN] and value[Color.BLUE] < value[Color.GREEN]:
        return "white"
    else:
        return "Error"


def bin_value(color):
    """
    Gets the binary value of the color read
    """
    if color == "white":
        return 0
    elif color == "black":
        return 1
    else:
        return None

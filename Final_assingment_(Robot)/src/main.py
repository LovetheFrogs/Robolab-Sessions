#!/usr/bin/env python3

"""
This code has been developed by Marcos Ferrer Zalve, as well as
all other code files from the src/ folder other than hamming_code.py.

Note the import for the debug module is commented. This is because the
module's run function conflicts with the main program run, so only one 
of the two can be present. In case of executing in debug mode, use the
import and change the name to main.run() function.

Code has been developed using the modular design concepts of coed desing
"""

from hamming_code import HammingCode, HCResult
from stack_machine import StackMachine, SMState
from robot import *

# from debug import run


def run():
    # the execution of all code shall be started from within this function
    robot = Robot()
    decoder = HammingCode()
    sm = StackMachine()
    cs = ev3.ColorSensor("in4")
    cs.mode = 'RGB-RAW'
    btn = ev3.Button()
    spk = ev3.Sound()
    cont = True
    while cont:
        read_card(robot, decoder, sm, cs, spk, btn)
        
        cont = next_card(spk, btn)
        

if __name__ == '__main__':
    run()


def read_card(robot: Robot, decoder: HammingCode, sm: StackMachine, cs: ev3.ColorSensor, spk: ev3.Sound, btn: ev3.Button):
    for _ in range (10):
            value = cs.bin_data("hhhh")
            while not value[0] > value[1] and not value[0] > value[2]:
                robot.readjust_barcode()
                if not value[0] > value[1] and not value[0] > value[2]:
                    break
            
            encoded_word = read_line(robot)

            spk.speak("Encoded word is: " + str(encoded_word))
            sleep(12)
            
            res = decode_line(decoder, spk, encoded_word, robot, btn)

            spk.speak("Decoded word is: " + str(res[0]))
            sleep(10)

            operate(sm, spk, robot, res)

            spk_operation(sm, spk)
            
            if not isinstance(sm.top(), str) and sm.top() is not None:
                spk.speak("Top value is: " + str(to_int(sm.top())))
            elif sm.top() is not None:
                spk.speak("Top value is: " + sm.top())

            sleep(8)

            next(robot)


def read_line(robot: Robot) -> list:
    encoded_word = []
    robot.sensor_step()
    for _ in range(10):
        encoded_word.append(robot.read_value())
        robot.sensor_step()
    encoded_word.append(robot.read_value())
    return encoded_word


def decode_line(decoder: HammingCode, spk: ev3.Sound, encoded_word: list, robot: Robot, btn: ev3.Button) -> tuple:
    res = decoder.decode(tuple(encoded_word))
    if res[1] == HCResult.VALID:
        spk.speak("Valid code")
        sleep(3)
        return res
    elif res[1] == HCResult.CORRECTED:
        spk.speak("Corrected code")
        sleep(4)
        return res
    else:
        return uncorrectable(decoder, spk, encoded_word, robot, btn)


def uncorrectable(decoder: HammingCode, spk: ev3.Sound, encoded_word: list, robot: Robot, btn: ev3.Button) -> tuple:
    spk.speak("Uncorrectable code")
    sleep(8)
    encoded_word = repeat_lecture(robot)
    res = decoder.decode(tuple(encoded_word))
    if res[1] == HCResult.UNCORRECTABLE:
        robot.sensor_reset()
        spk.speak("Uncorrectable code, adjust card and press enter")
        sleep(8)
        while True:
            if btn.enter:
                spk.beep()
                break
            sleep(0.05)
        return decode_line(decoder, spk, encoded_word, robot, btn)
    else:
        return decode_line(decoder, spk, encoded_word, robot, btn)


def repeat_lecture(robot: Robot) -> list:
    robot.sensor_reset()
    sleep(3)
    robot.readjust_barcode()
    sleep(3)
    return read_line(robot)


def operate(sm: StackMachine, spk: ev3.Sound, robot: Robot, res: tuple):
    res = sm.do(res[0])
    if res == SMState.STOPPED:
        spk.speak("Stack machine stopped")
        robot.sensor_reset()
        exit(0)
    elif res == SMState.ERROR:
        spk.speak("Stack machine got an error for invalid operation")
        robot.sensor_reset()
        exit(2)


def spk_operation(sm: StackMachine, spk: ev3.Sound):
    if sm.op is not None:
        spk.speak("Instruction: " + sm.op)
        sleep(5)
    if sm.op == "SPEAK" and sm.spk is not None:
        spk.speak(sm.spk)
        sleep(len(sm.spk) * 0.8)


def to_int(res: tuple) -> int:
    return sum(bit * 2**(7 - i) for i, bit in enumerate(res))


def next(robot: Robot):
    robot.sensor_reset()
    robot.scroll_step()


def next_card(spk: ev3.Sound, btn: ev3.Button) -> bool:
    spk.speak("Press back to exit, enter to continue")
    sleep(5)
    while True:
        if btn.backspace:
            spk.beep()
            sleep(1)
            spk.beep()
            return False
        elif btn.enter:
            spk.beep()
            return True
        sleep(0.05)

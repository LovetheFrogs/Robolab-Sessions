#!/usr/bin/env python3

import ev3dev.ev3 as ev3
from time import sleep


class Robot:
    """
    This class provides logic for moving the sensor and scrolling the bar code cards
    """

    def sensor_step(self):
        """
        Moves the sensor one step to read the next bar code value
        """
        motor = ev3.MediumMotor("outD")
        motor.stop_action = "hold"
        motor.speed_sp = 100
        motor.position_sp = 22
        motor.run_to_rel_pos()
        sleep(0.5)

    def sensor_reset(self):
        """
        Resets the sensor position
        """
        motor = ev3.MediumMotor("outD")
        motor.stop_action = "hold"
        motor.speed_sp = 100
        motor.position_sp = 0
        motor.run_to_abs_pos()
        sleep(1)

    def scroll_step(self):
        """
        Moves the bar code card to the next line.
        """
        motor = ev3.LargeMotor("outA")
        motor.stop_action = "brake"
        motor.speed_sp = 100
        motor.position_sp = -90
        motor.run_to_rel_pos()
        sleep(2)


    def read_value(self) -> int:
        """
        Reads a single value, converts it and returns the binary expression
        :return: int
        """
        sensor = ev3.ColorSensor("in4")
        sensor.mode = 'RGB-RAW'
        value = sensor.bin_data("hhhh")
        if value[0] < 200 and value[1] < 250 and value[2] < 200:
            return 1
        elif value[1] > 200:
            return 0
        else:
            return None

    def readjust_barcode(self):
        """
        Moves back the bar code in case it has advanced too much
        """
        print("Readjusting")
        motor = ev3.LargeMotor("outA")
        rotator = ev3.MediumMotor("outD")
        motor.stop_action = "brake"
        rotator.stop_action = "brake"
        motor.speed_sp = 100
        motor.position_sp = -10
        rotator.speed_sp = 100
        rotator.position_sp = 5
        motor.run_to_rel_pos()
        rotator.run_to_rel_pos()
        sleep(1)

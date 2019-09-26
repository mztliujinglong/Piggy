# PYTHON3 ONLY
# Based on:
# https://www.dexterindustries.com/GoPiGo/
# https://github.com/DexterInd/GoPiGo3
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information see https://github.com/DexterInd/GoPiGo3/blob/master/LICENSE.md

import gopigo3, sys, time
from di_sensors.easy_distance_sensor import EasyDistanceSensor

class PiggyParent(gopigo3.GoPiGo3):

    '''
    UTILITIES
    '''

    def __init__(self, addr=8, detect=True):
        gopigo3.GoPiGo3.__init__(self)
        self.scan_data = {}
        self.distance_sensor = EasyDistanceSensor()

    def calibrate(self):
        """allows user to experiment on finding centered midpoint and even motor speeds"""
        print("Calibrating...")
        self.servo(self.MIDPOINT)
        response = str.lower(input("Am I looking straight ahead? (y/n): "))
        if response == 'n':
            while True:
                response = str.lower(input("Turn right, left, or am I done? (r/l/d): "))
                if response == "r":
                    self.MIDPOINT += 25
                    print("Midpoint: " + str(self.MIDPOINT))
                    self.servo(self.MIDPOINT)
                elif response == "l":
                    self.MIDPOINT -= 25
                    print("Midpoint: " + str(self.MIDPOINT))
                    self.servo(self.MIDPOINT)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break
        else:
            print('Okay, remember %d as the correct self.MIDPOINT' % self.MIDPOINT)
        response = str.lower(input("Do you want to check if I'm driving straight? (y/n)"))
        if 'y' in response:
            while True:
                self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
                self.fwd()
                time.sleep(.5)
                self.stop()
                response = str.lower(input("Reduce left, reduce right or drive? (l/r/d): "))
                if response == 'l':
                    self.LEFT_SPEED -= 5
                elif response == 'r':
                    self.RIGHT_SPEED -= 5
                elif response == 'd':
                    self.fwd()
                    time.sleep(.5)
                    self.stop()
                else:
                    break

    def quit(self):
        """Terminates robot movement and settings then closes app"""
        print("\nIt's been a pleasure.\n")
        self.reset_all()
        sys.exit(1)

    '''
    MOVEMENT
    '''

    def deg_fwd(self, deg):
        """Zeroes current encorder values then moves forward based on degrees given"""
        self.offset_motor_encoder(self.MOTOR_LEFT, self.get_motor_encoder(self.MOTOR_LEFT))
        self.offset_motor_encoder(self.MOTOR_RIGHT, self.get_motor_encoder(self.MOTOR_RIGHT))
        self.set_motor_position(self.MOTOR_LEFT + self.MOTOR_RIGHT, deg)

    def fwd(self, left=50, right=50):
        """Blindly charges your robot forward at default power which needs to be configured in child class"""
        if self.LEFT_DEFAULT and left == 50:
            left = self.LEFT_DEFAULT
        if self.RIGHT_DEFAULT and right == 50:
            right = self.RIGHT_DEFAULT
        self.set_motor_power(self.MOTOR_LEFT, left)
        self.set_motor_power(self.MOTOR_RIGHT, right)

    def right(self, primary=90, counter=0):
        """Rotates right by powering the left motor to default"""
        self.set_motor_power(self.MOTOR_LEFT, primary)
        self.set_motor_power(self.MOTOR_RIGHT, counter)

    def left(self, primary=90, counter=0):
        """Rotates left by powering the left motor to 90 by default and counter motion 0"""
        self.set_motor_power(self.MOTOR_LEFT, counter)
        self.set_motor_power(self.MOTOR_RIGHT, primary)      

    def back(self, left=-50, right=-50):
        if self.LEFT_DEFAULT and left == -50:
            left = -self.LEFT_DEFAULT
        if self.RIGHT_DEFAULT and right == -50:
            right = -self.RIGHT_DEFAULT
        self.set_motor_power(self.MOTOR_LEFT, left)
        self.set_motor_power(self.MOTOR_RIGHT, right)

    def servo(self, angle):
        """Moves the servo to the given angle"""
        print("Servo moving to: {} ".format(angle))
        self.set_servo(self.SERVO_1, angle)
        time.sleep(.05)

    def stop(self):
        """Cut power to the motors"""
        print("\n--STOPPING--\n")
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)

    '''
    SENSORS
    '''

    def read_distance(self):
        """Returns the GoPiGo3's distance sensor in MM over IC2"""
        d = self.distance_sensor.read_mm()
        print("Distance Sensor Reading: {} mm ".format(d))
        return d
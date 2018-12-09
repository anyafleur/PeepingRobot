import sys
sys.path.append('lib/')

import car_module as car
import servo_module as servo
import print_pose_listener as pose_listener
from myo import Myo
from vibration_type import VibrationType
import myo_interface_module as myo

import threading
from time import sleep
from time import time as current_time
import math

from device_listener import DeviceListener
from pose_type import PoseType

class WhileTrueThread(threading.Thread):
    def __init__(self, interval = 0):
        threading.Thread.__init__(self)
        self.__interval = interval
        self.__stop = False
    def stop(self):
        self.__stop = True
    def _prepare(self):
        pass
    def _end(self):
        pass
    def run(self):
        self._prepare()
        while not self.__stop :
            self._loop()
            sleep(self.__interval)
        self._end()


class CarThread(WhileTrueThread):
    def __init__(self, control_values):
        WhileTrueThread.__init__(self, 0.1)
        self.__control_values = control_values
    def _loop(self):
        control_values = self.__control_values
        current_direction = control_values.get_current_direction()
        current_duty_cycle = control_values.get_current_duty_cycle()
        if(current_direction == 'stop'):
            car.stop()
        if(current_direction == 'forward'):
            car.move_forward(current_duty_cycle)
        if(current_direction == 'backward'):
            car.move_backward(current_duty_cycle)
        if(current_direction == 'left'):
            car.turn_left(current_duty_cycle)
        if(current_direction == 'right'):
            car.turn_right(current_duty_cycle)
        else:
            pass
                
class ServoThread(WhileTrueThread):
    def __init__(self, control_values):
        WhileTrueThread.__init__(self, 0.0)
        self.__control_values = control_values
        self.horizontal_angle = self.__control_values.set_horizontal_angle(80)
        self.vertical_angle = self.__control_values.set_vertical_angle(0)
        
        servo.set_default_angle()
        
    def _loop(self):
        control_values = self.__control_values
        self.horizontal_angle = control_values.get_current_horizontal_angle()
        self.vertical_angle = control_values.get_current_vertical_angle()

        servo.setHorizontalAngle(self.horizontal_angle)
        servo.setVerticalAngle(self.vertical_angle)
        
    def _end(self):
        myo.deinit_servo()
        
class InputThread(WhileTrueThread):
    def __init__(self, control_values):
        WhileTrueThread.__init__(self, 0.0)
        self.__control_values = control_values
        myo.connect_myo(control_values)

    def _loop(self):
        myo.detect_myo_pose()
        current_direction = self.__control_values.get_current_direction()
        print("Current Direction: " + current_direction)
        
    def _end(self):
        myo.deinit_myo()

class VRThread(WhileTrueThread):
    def __init__(self, control_values):
        WhileTrueThread.__init__(self, 0.0)
        

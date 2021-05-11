import RPi.GPIO as GPIO          
from time import sleep
GPIO.setmode(GPIO.BCM)

import time
import board
import adafruit_bitbangio as bitbangio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

DUTY_HIGH = 0xffff
DUTY_LOW = 0
ACCELERATION = 10000

motor_i2c = bitbangio.I2C(board.SCL, board.SDA)
motor_hat = PCA9685(motor_i2c)
motor_hat.frequency = 60

servo_i2c = bitbangio.I2C(board.D9, board.D8)
servo_hat = ServoKit(channels=16, i2c = servo_i2c)

class Camera():

    def __init__(self):
        pass

class Wheel():

    def __init__(self, in1, in2, en):
        self.in1 = in1
        self.in2 = in2
        self.en = en
        self.v = 0

    def stop(self):
        self.in1.duty_cycle = DUTY_LOW
        self.in2.duty_cycle = DUTY_LOW
        self.v = 0
        self.en.duty_cycle = 0
        
    def forward(self):
        # if already going backwards, stop first
        if self.v < 0:
            self.stop()
        self.in1.duty_cycle = DUTY_HIGH
        self.in2.duty_cycle = DUTY_LOW
        self.v= min(self.v + ACCELERATION, DUTY_HIGH)
        self.en.duty_cycle = self.v

    def backward(self):
        # if already going forwards, stop first
        if self.v > 0:
            self.stop()
        self.in1.duty_cycle = DUTY_LOW
        self.in2.duty_cycle = DUTY_HIGH
        self.v = max(self.v - ACCELERATION, -1*DUTY_HIGH)
        self.en.duty_cycle = -1*self.v

class Car():

    def __init__(self):
        self.rear_passenger = Wheel(motor_hat.channels[8], motor_hat.channels[9], motor_hat.channels[5])
        self.front_passenger = Wheel(motor_hat.channels[11], motor_hat.channels[10], motor_hat.channels[4])
        self.rear_driver = Wheel(motor_hat.channels[1], motor_hat.channels[0], motor_hat.channels[6])
        self.front_driver = Wheel(motor_hat.channels[2], motor_hat.channels[3], motor_hat.channels[7])

        self.leg = servo_hat.servo[0]
        self.knee = servo_hat.servo[1]
        self.cam = servo_hat.servo[15]

        self.leg.angle = 110
        self.knee.angle = 45
        self.cam.angle = 0

    def kick(self):
        self.leg.angle = 150
        self.knee.angle = 0
        time.sleep(1)
        self.leg.angle = 0
        self.knee.angle = 45
        time.sleep(1)
        self.leg.angle = 100
        self.knee.angle = 45

    def stop(self):
        self.rear_passenger.stop()
        self.front_passenger.stop()
        self.rear_driver.stop()
        self.front_driver.stop()

    def forward(self):
        self.rear_passenger.forward()
        self.front_passenger.forward()
        self.rear_driver.forward()
        self.front_driver.forward()
            
    def backward(self):
        self.rear_passenger.backward()
        self.front_passenger.backward()
        self.rear_driver.backward()
        self.front_driver.backward()

    def left(self):
        self.rear_passenger.backward()
        self.front_passenger.forward()
        self.rear_driver.backward()
        self.front_driver.forward()
        
    def right(self):
        self.rear_passenger.forward()
        self.front_passenger.backward()
        self.rear_driver.forward()
        self.front_driver.backward()
        
    def forward_right(self):
        self.rear_passenger.forward()
        self.front_passenger.stop()
        self.rear_driver.forward()
        self.front_driver.stop()
        
    def forward_left(self):
        self.rear_passenger.stop()
        self.front_passenger.forward()
        self.rear_driver.stop()
        self.front_driver.forward()
        
    def rotate_right_back(self):
        self.rear_passenger.stop()
        self.front_passenger.stop()
        self.rear_driver.forward()
        self.front_driver.forward()
        
    def rotate_left_back(self):
        self.rear_passenger.forward()
        self.front_passenger.forward()
        self.rear_driver.stop()
        self.front_driver.stop()
        
    def clockwise(self):
        self.rear_passenger.backward()
        self.front_passenger.backward()
        self.rear_driver.forward()
        self.front_driver.forward()
        
    def counter_clockwise(self):
        self.rear_passenger.forward()
        self.front_passenger.forward()
        self.rear_driver.backward()
        self.front_driver.backward()
        
    def clockwise_back(self):
        self.rear_passenger.forward()
        self.front_passenger.stop()
        self.rear_driver.stop()
        self.front_driver.backward()
        
    def counter_clockwise_back(self):
        self.rear_passenger.backward()
        self.front_passenger.stop()
        self.rear_driver.stop()
        self.front_driver.forward()

    def cleanup(self):
        self.cam.angle = 0
        self.stop()
        GPIO.cleanup()


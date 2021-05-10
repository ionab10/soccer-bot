import RPi.GPIO as GPIO          
from time import sleep
GPIO.setmode(GPIO.BCM)

import time
import board
import adafruit_bitbangio as bitbangio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

DUTY_HIGH = 0xffff

motor_i2c = bitbangio.I2C(board.SCL, board.SDA)
motor_hat = PCA9685(motor_i2c)
motor_hat.frequency = 60
in1r = motor_hat.channels[8]
in2r = motor_hat.channels[9]
in3r = motor_hat.channels[11]
in4r = motor_hat.channels[10]
in1l = motor_hat.channels[1]
in2l = motor_hat.channels[0]
in3l = motor_hat.channels[2]
in4l = motor_hat.channels[3]
motors = [in1r, in2r, in3r, in4r, in1l, in2l, in3l, in4l]


servo_i2c = bitbangio.I2C(board.D9, board.D8)
servo_hat = ServoKit(channels=16, i2c = servo_i2c)
leg = servo_hat.servo[0]
knee = servo_hat.servo[1]
cam = servo_hat.servo[15]
leg.angle = 110
knee.angle = 45
cam.angle = 0
    
def kick():
    leg.angle = 150
    knee.angle = 0
    time.sleep(1)
    leg.angle = 0
    knee.angle = 45
    time.sleep(1)
    leg.angle = 100
    knee.angle = 45
    
def pan():
    pass

def turn(angle):
    #front_servo.angle += angle
    return

def start(forward=True):
    if forward:
        in1r.duty_cycle = DUTY_HIGH
        in2r.duty_cycle = 0
        in3r.duty_cycle = DUTY_HIGH
        in4r.duty_cycle = 0
        in1l.duty_cycle = DUTY_HIGH
        in2l.duty_cycle = 0
        in3l.duty_cycle = DUTY_HIGH
        in4l.duty_cycle = 0
        
    else:
        
        in1r.duty_cycle = 0
        in2r.duty_cycle = DUTY_HIGH
        in3r.duty_cycle = 0
        in4r.duty_cycle = DUTY_HIGH
        in1l.duty_cycle = 0
        in2l.duty_cycle = DUTY_HIGH
        in3l.duty_cycle = 0
        in4l.duty_cycle = DUTY_HIGH
    
def stop():
    for p in motors:
        p.duty_cycle = 0
        
def left():
    in1r.duty_cycle = 0
    in2r.duty_cycle = DUTY_HIGH
    in3r.duty_cycle = DUTY_HIGH
    in4r.duty_cycle = 0
    in1l.duty_cycle = 0
    in2l.duty_cycle = DUTY_HIGH
    in3l.duty_cycle = DUTY_HIGH
    in4l.duty_cycle = 0
    
def right():
    in1r.duty_cycle = DUTY_HIGH
    in2r.duty_cycle = 0
    in3r.duty_cycle = 0
    in4r.duty_cycle = DUTY_HIGH
    in1l.duty_cycle = DUTY_HIGH
    in2l.duty_cycle = 0
    in3l.duty_cycle = 0
    in4l.duty_cycle = DUTY_HIGH
    
def forward_right():
    in1r.duty_cycle = DUTY_HIGH
    in2r.duty_cycle = 0
    in3r.duty_cycle = 0
    in4r.duty_cycle = 0
    in1l.duty_cycle = DUTY_HIGH
    in2l.duty_cycle = 0
    in3l.duty_cycle = 0
    in4l.duty_cycle = 0
    
def forward_left():
    in1r.duty_cycle = 0
    in2r.duty_cycle = 0
    in3r.duty_cycle = DUTY_HIGH
    in4r.duty_cycle = 0
    in1l.duty_cycle = 0
    in2l.duty_cycle = 0
    in3l.duty_cycle = DUTY_HIGH
    in4l.duty_cycle = 0
    
def rotate_right_back():
    in1r.duty_cycle = 0
    in2r.duty_cycle = 0
    in3r.duty_cycle = 0
    in4r.duty_cycle = 0
    in1l.duty_cycle = DUTY_HIGH
    in2l.duty_cycle = 0
    in3l.duty_cycle = DUTY_HIGH
    in4l.duty_cycle = 0
    
def rotate_left_back():
    in1r.duty_cycle = DUTY_HIGH
    in2r.duty_cycle = 0
    in3r.duty_cycle = DUTY_HIGH
    in4r.duty_cycle = 0
    in1l.duty_cycle = 0
    in2l.duty_cycle = 0
    in3l.duty_cycle = 0
    in4l.duty_cycle = 0
    
def clockwise():
    in1r.duty_cycle = 0
    in2r.duty_cycle = DUTY_HIGH
    in3r.duty_cycle = 0
    in4r.duty_cycle = DUTY_HIGH
    in1l.duty_cycle = DUTY_HIGH
    in2l.duty_cycle = 0
    in3l.duty_cycle = DUTY_HIGH
    in4l.duty_cycle = 0
    
def counter_clockwise():
    in1r.duty_cycle = DUTY_HIGH
    in2r.duty_cycle = 0
    in3r.duty_cycle = DUTY_HIGH
    in4r.duty_cycle = 0
    in1l.duty_cycle = 0
    in2l.duty_cycle = DUTY_HIGH
    in3l.duty_cycle = 0
    in4l.duty_cycle = DUTY_HIGH
    
def clockwise_back():
    in1r.duty_cycle = DUTY_HIGH
    in2r.duty_cycle = 0
    in3r.duty_cycle = 0
    in4r.duty_cycle = 0
    in1l.duty_cycle = 0
    in2l.duty_cycle = 0
    in3l.duty_cycle = 0
    in4l.duty_cycle = DUTY_HIGH
    
def counter_clockwise_back():
    in1r.duty_cycle = 0
    in2r.duty_cycle = DUTY_HIGH
    in3r.duty_cycle = 0
    in4r.duty_cycle = 0
    in1l.duty_cycle = 0
    in2l.duty_cycle = 0
    in3l.duty_cycle = DUTY_HIGH
    in4l.duty_cycle = 0

def run(dist, forward=True):
    s = dist/MPS
    start(forward=forward)
    sleep(s)
    stop()
    
def change_speed(mps):
    MPS = mps
    #p_A.ChangeDutyCycle(PWM_FACTOR*MPS)
    #p_B.ChangeDutyCycle(PWM_FACTOR*MPS)


#front_servo.angle = 50 

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("s-stop k-kick p-pan e-exit")
print("\n")

stop()
    
    
while(1):

    x=input()
    
    if x=='w':
        print("run forward")
        start()
    
    elif x=='x':
        print("run backward")
        start(forward=False)
        
    elif x=='a':
        left()
        
    elif x=='d':
        right()

    elif x=='s':
        stop()
        
    elif x=='l':
        clockwise()

    elif x=='j':
        clockwise()

    elif x in ['1', '2', '3']:
        change_speed(int(x))
        
    elif x=='k':
        kick()
        
    elif x=='p':
        pan()

    elif x=='e':
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
    x=None

cam.angle = 0
stop()
GPIO.cleanup()
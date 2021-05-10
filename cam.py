from picamera import PiCamera
from time import sleep
import ball

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('/home/pi/Desktop/image.jpg')
image = ball.load_img('/home/pi/Desktop/image.jpg')
ball, center = ball.find_ball(image, plot=True)
if ball is not None:
    print(ball, center)
    if ball[0] < center[0]:
        print('left')
    elif ball[0] > center[0]:
        print('right')
        
camera.stop_preview()

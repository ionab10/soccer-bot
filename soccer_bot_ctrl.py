import sys
import picamera
import pygame
import io
import ball
import car
pygame.init()

car.stop()

#screen = pygame.display.set_mode((640,480),0)
screen = pygame.display.set_mode((0,0))


camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.crop = (0.0, 0.0, 1.0, 1.0)

x = (screen.get_width() - camera.resolution[0]) / 2
y = (screen.get_height() - camera.resolution[1]) / 2
rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)


while True:

    #screen.fill((255, 255, 255))
    screen.fill(0)
    
    stream = io.BytesIO()
    camera.capture(stream, use_video_port=True, format='rgb')
    stream.seek(0)
    stream.readinto(rgb)
    stream.close()
    img = pygame.image.frombuffer(rgb[0:
          (camera.resolution[0] * camera.resolution[1] * 3)],
           camera.resolution, 'RGB')

    if img:
        '''
        image = pygame.surfarray.array3d(img)
        ball, center = ball.find_ball(image, plot=True)
        if ball is not None:
            print(ball, center)
            if ball[0] < center[0]:
                print('left')
            elif ball[0] > center[0]:
                print('right')
        '''
        img = pygame.transform.scale(img, (640, 420))
        screen.blit(img, (x,y))
        # TODO draw circle around ball

    pygame.display.update()

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            car.cleanup()
            camera.close()
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.left()
            elif event.key == pygame.K_RIGHT:
                car.right()
            elif event.key == pygame.K_UP:
                car.forward()
            elif event.key == pygame.K_DOWN:
                car.backward()
            elif event.key == pygame.K_k:
                car.kick()
            elif event.key == 13:
                car.stop()
            else:
                print(event.key)
        #else:
        #    car.stop()

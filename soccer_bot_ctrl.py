import sys
import picamera
import pygame
import io
import ball
from car import Car

AI=False

def get_arrow_coords(x, y, d):
    if d == "right":
        return (
            (x+0, y+10),
            (x+0, y+20),
            (x+20, y+20),
            (x+20, y+30),
            (x+30, y+15),
            (x+20, y+0),
            (x+20, y+10)
            )
    elif d == "left":
        return (
            (x+30, y+10),
            (x+30, y+20),
            (x+10, y+20),
            (x+10, y+30),
            (x+0, y+15),
            (x+10, y+0),
            (x+10, y+10)
            )

pygame.init()

car = Car()
car.stop()

#screen = pygame.display.set_mode((640,480),0)
screen = pygame.display.set_mode((0,0))


camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.crop = (0.0, 0.0, 1.0, 1.0)
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
        
        img = pygame.transform.scale(img, (640, 420))
        image = pygame.surfarray.array3d(img) 
        ball_pos, center, mask = ball.find_ball(image)
        
        thumbnail = pygame.transform.scale(img, (128, 84))
        screen.blit(thumbnail, (640, 0))
        screen.blit(pygame.surfarray.make_surface(mask) , (0,0))
        
        # draw crosshair at centre
        pygame.draw.polygon(
            screen,
            (0,0,255),
            [
                (center[0], center[1]+10),
                (center[0], center[1]-10),
                (center[0]-10, center[1]),
                (center[0]+10, center[1]),
            ],
            1)
        
        if ball_pos is not None:
            x_ball = ball_pos[1]
            y_ball = ball_pos[0]
            r = ball_pos[2]
            print(ball_pos, center)
            if AI:
                
                if x_ball < center[0] - r:
                    pygame.draw.polygon(
                        screen,
                        (255,0,0),
                        get_arrow_coords(320, 420, "right")
                        )
                    car.clockwise()
                elif x_ball > center[0] + r:
                    pygame.draw.polygon(
                        screen,
                        (255,0,0),
                        get_arrow_coords(320, 420, "left")
                        )
                    car.counter_clockwise()
                elif r >= 40:
                    car.stop()
                else:
                    car.forward()
            # draw circle around ball
            pygame.draw.circle(screen, (255,0,0), (x_ball, y_ball), r, 1)
            
        elif AI:
            car.stop()

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
                car.counter_clockwise()
            elif event.key == pygame.K_RIGHT:
                car.clockwise()
            elif event.key == pygame.K_UP:
                car.forward()
            elif event.key == pygame.K_DOWN:
                car.backward()
            elif event.key == pygame.K_k:
                print('kick')
                car.kick()
            elif event.key == 13:
                car.stop()
            elif event.key == pygame.K_w:
                try:
                    car.cam.angle -= 5
                except:
                    pass
            elif event.key == pygame.K_s:
                try:
                    car.cam.angle += 5
                except:
                    pass
            elif event.key == pygame.K_a:
                AI = not AI
            else:
                print(event.key)
        #else:
        #    car.stop()

import sys
import picamera
import pygame
import io
import pygame.camera
pygame.init()
pygame.camera.init()

#screen = pygame.display.set_mode((640,480),0)
screen = pygame.display.set_mode((0,0))

'''
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(32,24))
cam.start()
'''

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.crop = (0.0, 0.0, 1.0, 1.0)

x = (screen.get_width() - camera.resolution[0]) / 2
y = (screen.get_height() - camera.resolution[1]) / 2

while True:

    #screen.fill((255, 255, 255))
    screen.fill(0)

    '''
    image1 = cam.get_image()
    image1 = pygame.transform.scale(image1,(640,480))
    screen.blit(image1,(0,0))
    '''

    stream = io.BytesIO()
    camera.capture(stream, use_video_port=True, format='rgb')
    stream.seek(0)
    stream.readinto(rgb)
    stream.close()
    img = pygame.image.frombuffer(rgb[0:
          (camera.resolution[0] * camera.resolution[1] * 3)],
           camera.resolution, 'RGB')
    if img:
        screen.blit(img, (x,y))

    pygame.display.update()

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #cam.stop()
            camera.close()
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                location -= 1
            if event.key == pygame.K_RIGHT:
                location += 1

'''






# Init buffer
rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)

# Main loop
exitFlag = True
while(exitFlag):
    for event in pygame.event.get():
        if(event.type is pygame.MOUSEBUTTONDOWN or 
           event.type is pygame.QUIT):
            exitFlag = False





'''
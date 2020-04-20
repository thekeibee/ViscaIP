import viscaip as vp
import pygame
import pygame.joystick
import pygame.camera

frame_size = (1280,720)
screen = pygame.display.set_mode(frame_size)
pygame.display.set_caption("PTZ Control")

clock = pygame.time.Clock()

vp.testCamera()
myJS = 0
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

frame = pygame.surface.Surface(frame_size, 0, screen)

pygame.camera.init()
camera = pygame.camera.Camera("/dev/video2", frame_size)
camera.start()
print(camera.get_size())

pygame.joystick.init()
for i in range(pygame.joystick.get_count()):
    js = pygame.joystick.Joystick(i)
    js.init()
    print("Joystick found: " + js.get_name())
    if "DragonRise Inc." in js.get_name():
        myJS = i
        break
js = pygame.joystick.Joystick(myJS)
js.init()

print(pygame.camera.list_cameras())


done = False

prevMovingState = False

counter = 0

while not done:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        elif event.type == pygame.JOYBUTTONDOWN:
            for i in range(js.get_numbuttons()):
                if js.get_button(i):
                    if i:
                        print("Zoom Tele")
                        vp.command("CAM_ZoomTELE")
                    else: 
                        print("Zoom Wide")
                        vp.command("CAM_ZoomWIDE")
        elif event.type == pygame.JOYBUTTONUP:
            print("Zoom Stop")
            vp.command("CAM_ZoomSTOP")

    myAxes = js.get_numaxes()
    moving = False
    for i in range(myAxes):
        # Vertical: 0 axis and Horizontal: 1 axis
        myAxis = js.get_axis(i) 
        #print("{} - {}".format(i,myAxis))
        if i == 0:
            if myAxis < 0:
                moving = True
                if not prevMovingState:
                    print("Right")
                    vp.command("CAM_DirectionRIGHT")
            if myAxis > 0:
                moving = True
                if not prevMovingState:
                    print("Left")
                    vp.command("CAM_DirectionLEFT")
        if i == 1:
            if myAxis < 0:
                moving = True
                if not prevMovingState:
                    print("Down")
                    vp.command("CAM_DirectionDOWN")
            if myAxis > 0:
                moving = True
                if not prevMovingState:
                    print("Up")
                    vp.command("CAM_DirectionUP")
    if not moving:
        if prevMovingState:
            print("Stop")
            vp.command("CAM_DirectionSTOP")
            prevMovingState = False
    else: prevMovingState = True

    if counter > 1 :
        counter = 0
        if camera.query_image():
            camera.get_image(frame)
            screen.blit(frame,(0,0))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

import pygame, math, time, cv2
from pygame.locals import *

import numpy as np
from cv_info import *
from obj_loader import *

from OpenGL.GL import *
from OpenGL.GLU import *

if __name__ == "__main__":
    i = 0
    
    c = Capture()
    def resetGL():
        glLoadIdentity()

        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

        #glRotatef(90, -1, 0, 0)
    
    pygame.init()
    display = (1000,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    resetGL()

    o = Object(filename =
       "/Users/arthurgarvin/Documents/Lonely Ping Pong/ShakehandStyle/ShakehandPaddleLowPoly.obj"
       )

    b = Cube()
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        cv_info = c.read()
        #print(cv_info.xyzCoords())
        
        x,y,z = cv_info.xyzCoords()
        angle = cv_info.xyAngle()
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        resetGL()        
        glTranslate(-((x / 64) - 10),-((y / 36) - 10),(z / 75) - (178 / 3))
        glRotatef(90, -1, 0, 0)
        glRotate(angle,0,1,0)
        o.boundingbox(True)
        o.render()

        resetGL()        
        glTranslate(0,0,-5)
        glRotatef(i,1,1,0)
        i += 5
        b.render()

        
        
        
        pygame.display.flip()
        pygame.time.wait(10)

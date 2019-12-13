import pygame, math, time, cv2
from pygame.locals import *

import numpy as np
from cv_info import *
from obj_loader import *
from math3D import *

from OpenGL.GL import *
from OpenGL.GLU import *

def resetGL():
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

#applies the vectors to the GL Perspective
def applyGL(vectors):
    resetGL()
    totalvector = Vector(Point(0,0,0), Point(0,0,0))
    for vector in vectors:
        totalvector = totalvector.add(vector)
    v = totalvector.get_points()
    dx = v[1][0] - v[0][0]
    dy = v[1][1] - v[0][1]
    dz = v[1][2] - v[0][2]
    glTranslate(dx,dy,dz)


def showVector(vector, color = (1,1,1)):
    v = vector.get_points()
    s = (v[0][0], v[0][1], v[0][2])
    e = (v[0][0] + v[1][0], v[0][1] + v[1][1], v[0][2] + v[1][2])
    glBegin(GL_LINES)
    glColor3f(1,1,1)
    glVertex3fv(s)
    glVertex3fv(e)
    glEnd()
    
    
if __name__ == "__main__":
    c = Capture()
    #
    i = -5
    pygame.init()
    display = (1000,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    resetGL()

    o = Object(filename =
       "/Users/arthurgarvin/Documents/Lonely Ping Pong/ShakehandStyle/ShakehandPaddleLowPoly.obj"
       )

    oldpos = Point(0,0,0)
    #
    rec = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    rec = not rec

                if event.key == K_UP:
                    i -= 1

                if event.key == K_DOWN:
                    i += 1
                    
                
        cv_info = c.read()
        #print(cv_info.xyzCoords())
        
        x,y,z = cv_info.xyzCoords()
        angle = cv_info.xyAngle()
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #render paddle
        resetGL()        
        glTranslate(-((x / 64) - 10),-((y / 36) - 10),(z / 75) - (178 / 3))
        glRotatef(90, -1, 0, 0)
        glRotate(angle,0,1,0)
        paddlebox = o.boundingbox(False)
        o.render()

        #render ball
        resetGL()
        glColor3f(1,1,1)
        sphere = Sphere(1)
        applyGL([Vector(Point(0,0,0), Point(0,0,i))])
        sphere.render()
        spherebox = sphere.boundingbox(False)
        print(sphere.collision(spherebox, paddlebox))


        #resetGL()
        newpos = Point(-((x / 64) - 10),-((y / 36) - 10),(z / 75) - (178 / 3))
        velocity = Vector(oldpos, newpos)
        showVector(velocity)
        if (rec):
               print(velocity.get_length())
        oldpos = newpos
        
        pygame.display.flip()
        pygame.time.wait(10)

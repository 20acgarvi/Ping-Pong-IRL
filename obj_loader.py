from operator import itemgetter
import math
from math3D import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

#a and b are 1D arrays
def swap_index(a,b,i):
    t = a[i]
    a[i] = b[i]
    b[i] = t
    return (a,b)
    
#Abstract class for object interactions (collision)
class Interactable:
    def __init__(self, *args, **kwargs):
        pass

    #Returns tuple in the form of
    #(furthest lowest left coordinate, nearest highest right coordinate)
    def boundingbox(self, *args, **kwargs):
        pass

    #collider and collidee are bounding boxes of two objects
    def collision(self, collider, collidee):
        l_b1, h_b1 = collider
        l_b2, h_b2 = collidee

        l_x1, l_y1, l_z1, l_s1 = l_b1
        h_x1, h_y1, h_z1, h_s1 = h_b1
        l_x2, l_y2, l_z2, l_s2 = l_b2
        h_x2, h_y2, h_z2, h_s2 = h_b2
        
        xCollision, yCollision, zCollision = False, False, False
        if ((l_x1 >= l_x2 and l_x1 <= h_x2) or (h_x1 >= h_x2 and l_x1 <= h_x2)):
            xCollision = True
        if ((l_y1 >= l_y2 and l_y1 <= h_y2) or (h_y1 >= h_y2 and l_y1 <= h_y2)):
            yCollision = True
        if ((l_z1 >= l_z2 and l_z1 <= h_z2) or (h_z1 >= h_z2 and l_z1 <= h_z2)):
            zCollision = True
        
        return xCollision and yCollision and zCollision
            
            
class Object(Interactable):
    def __init__(self, filename, *args, **kwargs):
        Interactable.__init__(self)
        self.file = open(filename, "r")
        self.load(self.file)

    #loads a 3D object from a file
    def load(self, file):
        self.verts = []
        self.faces = []
        for line in file:
            if line.startswith("#"):
                continue
            elif line.startswith("vn"):
                continue
            elif line.startswith("v"):
                s = line.split()
                xyztuple = (float(s[1]), float(s[2]), float(s[3]))
                self.verts.append(xyztuple)
            elif line.startswith("f"):
                s = line.split()
                temp = []
                for x in range(1, len(s)):
                    temp.append(int(s[x].split("//")[0]))
                quadtuple = (temp)
                self.faces.append(quadtuple)
        self.transform = self.verts
        self.file.close()

    #renders the object
    def render(self):
        for face in self.faces:
            glBegin(GL_POLYGON)
            for vertex in face:
                glColor3f(0,1,0)
                glVertex3fv(self.transform[vertex-1])
            glEnd()

        

    def boundingbox(self, render):
        upper = (float(max(self.transform,key=itemgetter(0))[0]),
                 float(max(self.transform,key=itemgetter(1))[1]),
                 float(max(self.transform,key=itemgetter(2))[2]), 1)
        lower = (float(min(self.transform,key=itemgetter(0))[0]),
                 float(min(self.transform,key=itemgetter(1))[1]),
                 float(min(self.transform,key=itemgetter(2))[2]), 1)

        if (render):
            bb1 = (upper[0],upper[1],upper[2])
            bb2 = (upper[0],upper[1],lower[2])
            bb3 = (upper[0],lower[1],upper[2])
            bb4 = (upper[0],lower[1],lower[2])
            bb5 = (lower[0],upper[1],upper[2])
            bb6 = (lower[0],upper[1],lower[2])
            bb7 = (lower[0],lower[1],upper[2])
            bb8 = (lower[0],lower[1],lower[2])
            glBegin(GL_LINES)
            glColor3f(1,0,0)
            glVertex3fv(bb1)
            glVertex3fv(bb2)
            glVertex3fv(bb3)
            glVertex3fv(bb4)
            glVertex3fv(bb5)
            glVertex3fv(bb6)
            glVertex3fv(bb7)
            glVertex3fv(bb8)
            glEnd()

        
        upper = [upper]
        lower = [lower]
        buf = glGetFloatv(GL_MODELVIEW_MATRIX)
        b = []
        for i in range(len(buf)):
            a = buf[i].tolist()
            for j in range(len(a)):
                a[j] = "%f" % a[j]
            b.append(a)            
        mat = Matrix(b)
        l = Matrix(lower).multiply(mat)
        u = Matrix(upper).multiply(mat)
            
        #.arr() returns a 2D array
        l = l.arr()[0]
        u = u.arr()[0]
        if(l[0] > u[0]):
            l,u = swap_index(l,u,0)
        if(l[1] > u[1]):
            l,u = swap_index(l,u,1)
        if(l[2] > u[2]):
            l,u = swap_index(l,u,2)
        if(l[3] > u[3]):
            l,u = swap_index(l,u,3)
        return (l, u)
        

class Cube(Interactable):
    def __init__(self, scalar = 1, *args, **kwargs):
        Interactable.__init__(self)
        self.verts = [(scalar, scalar, scalar),
                      (scalar, scalar, 0),
                      (scalar, 0, scalar),
                      (0, scalar, scalar),
                      (0,0,scalar),
                      (0,scalar,0),
                      (scalar,0,0),
                      (0,0,0)]
        self.faces = [(1,2,6,4),
                      (1,2,7,3),
                      (1,3,5,4),
                      (5,3,7,8),
                      (2,6,8,7),
                      (6,4,5,8)]


    def render(self):
        for face in self.faces:
            glBegin(GL_POLYGON)
            for vertex in face:
                glColor3f(1,1,1)
                glVertex3fv(self.verts[vertex-1])
            glEnd()

    def boundingbox(self, render):
        if(render):
            for face in self.faces:
                glBegin(GL_LINES)
                for vertex in face:
                    glColor3f(0,1,0)
                    glVertex3fv(self.verts[vertex-1])
                glEnd()
        return (self.verts[0], self.verts[7])


class Sphere(Interactable):
    def __init__(self, radius, slices = 100, stacks = 20, *args, **kwargs):
        Interactable.__init__(self)
        self.quadric = gluNewQuadric()
        self.radius = radius
        self.slices = slices
        self.stacks = stacks

        self.verts = [(-1*self.radius, -1*self.radius, -1*self.radius),
                      (self.radius, self.radius, self.radius),]

    def render(self):
        gluSphere(self.quadric, self.radius, self.slices, self.stacks)

    def boundingbox(self, render):
        upper = (float(max(self.verts,key=itemgetter(0))[0]),
                 float(max(self.verts,key=itemgetter(1))[1]),
                 float(max(self.verts,key=itemgetter(2))[2]), 1)
        lower = (float(min(self.verts,key=itemgetter(0))[0]),
                 float(min(self.verts,key=itemgetter(1))[1]),
                 float(min(self.verts,key=itemgetter(2))[2]), 1)

        if (render):
            bb1 = (upper[0],upper[1],upper[2])
            bb2 = (upper[0],upper[1],lower[2])
            bb3 = (upper[0],lower[1],upper[2])
            bb4 = (upper[0],lower[1],lower[2])
            bb5 = (lower[0],upper[1],upper[2])
            bb6 = (lower[0],upper[1],lower[2])
            bb7 = (lower[0],lower[1],upper[2])
            bb8 = (lower[0],lower[1],lower[2])
            glBegin(GL_LINES)
            glColor3f(1,0,0)
            glVertex3fv(bb1)
            glVertex3fv(bb2)
            glVertex3fv(bb3)
            glVertex3fv(bb4)
            glVertex3fv(bb5)
            glVertex3fv(bb6)
            glVertex3fv(bb7)
            glVertex3fv(bb8)
            glEnd()

        upper = [upper]
        lower = [lower]
        buf = glGetFloatv(GL_MODELVIEW_MATRIX)
        b = []
        for i in range(len(buf)):
            a = buf[i].tolist()
            for j in range(len(a)):
                a[j] = "%f" % a[j]
            b.append(a)            
        mat = Matrix(b)
        l = Matrix(lower).multiply(mat)
        u = Matrix(upper).multiply(mat)
        
        #.arr() returns a 2D array
        l = l.arr()[0]
        u = u.arr()[0]
        if(l[0] > u[0]):
            l,u = swap_index(l,u,0)
        if(l[1] > u[1]):
            l,u = swap_index(l,u,1)
        if(l[2] > u[2]):
            l,u = swap_index(l,u,2)
        if(l[3] > u[3]):
            l,u = swap_index(l,u,3)
        return (l, u)
        
    
if __name__ == "__main__":

    #Init Object
    o = Object(filename =
               "/Users/arthurgarvin/Documents/Lonely Ping Pong/ShakehandStyle/ShakehandPaddleLowPoly.obj"
               )

    c = Sphere(5)
    
    def resetGL():
        glLoadIdentity()

        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

        glTranslatef(-0, -0, -40.0)

        glRotatef(90, -1, 0, 0)

    def distance(point1, point2):
        return math.sqrt(
            ((point1[0] - point2[0])**2) + ((point1[1] - point2[1])**2)
            )

    
    #Example Usage
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    resetGL()

    #a = (GLfloat * 16)()
    #mvm = glGetFloatv(GL_MODELVIEW_MATRIX, a)
    #for f in a:
        #print(f)
    

    prevMouse = None
    xVector = 0
    yVector = 0
    scalar = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                prevMouse = pygame.mouse.get_pos()
                xVector = 0
                yVector = 0
                
            if event.type == pygame.MOUSEMOTION:
                if prevMouse != None:
                    xVector = pygame.mouse.get_pos()[0] - prevMouse[0]
                    yVector = pygame.mouse.get_pos()[1] - prevMouse[1]
                    scalar = distance(
                        pygame.mouse.get_pos(), prevMouse
                        ) / 10
                    
            if event.type == pygame.MOUSEBUTTONUP:
                prevMouse = None

            if event.type == pygame.KEYDOWN:
                if event.key == K_R:
                    pass
                
        if yVector != 0 and xVector != 0:
            glRotatef(scalar, 0, xVector, yVector * -1)
            scalar -= math.log(scalar) / 3
                
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        o.render()
        print(o.boundingbox(render=True))
        resetGL()
        c.render()
        pygame.display.flip()
        pygame.time.wait(10)
        resetGL()

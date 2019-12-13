import cv2
import math
import numpy as np

#suppresses warning with atan() in RotatedRectangle.getAngle()
import warnings
warnings.filterwarnings("ignore", category = RuntimeWarning)

def nothing(self):
    pass
    
class RotatedRectangle:
    def __init__(self, *args, **kwargs):
        if "contour" in kwargs:
            self.rectangle = cv2.minAreaRect(kwargs["contour"])
            self.points = cv2.boxPoints(self.rectangle)
            self.initwidth, self.initialheight = self.rectangle[1]
            
        if "points" in kwargs:
            try:
                raise Exception("This constructor is incomplete!")
            except Exception:
                pass

    def setInitialHeight(self, x):
        self.initheight = x

    def setInitialWidth(self, x):
        self.initwidth = x
        
    def xyAngle(self):
        width, height = self.rectangle[1]

        #finds angle of turn in range of -90 <= a <= 90
        box = cv2.boxPoints(self.rectangle)
        m1 = ((box[0][0] + box[1][0]) / 2, (box[0][1] + box[1][1]) / 2)
        m2 = ((box[2][0] + box[3][0]) / 2, (box[2][1] + box[3][1]) / 2)
        opp = m1[0] - m2[0]
        adj = m1[1] - m2[1]
        angle = math.degrees(math.atan(opp/adj))
        if (width < height):
            angle = angle - 90

        #converts angle to range of 0 <= a <= 180
        if (-90 <= angle <= 0):
            angle = 90 - abs(angle)
        elif (-180 <= angle < -90):
            angle = 180 + (90 - abs(angle))
            
        return angle

    def xyzCoords(self):
        x = (self.points[0][0] + self.points[2][0]) / 2
        y = (self.points[0][1] + self.points[2][1]) / 2
        z = (910 * 771.1338461) / self.rectangle[1][0]
        return (x,y,z)

            
class Capture:
    def __init__(self, *args, **kwargs):
        cv2.namedWindow("frame")
        self.vc = cv2.VideoCapture(0)

        if "lowerbound" in kwargs:
            self.l_b = kwargs["lowerbound"]
        else:
            self.l_b = (0,0,0)
        if "upperbound" in kwargs:
            self.u_b = kwargs["upperbound"]
        else:
            self.u_b = (255,255,255)

        cv2.namedWindow("Tracking")
        cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
        cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
        cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
        cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
        cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
        cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

        cv2.namedWindow("result", cv2.WINDOW_NORMAL)

        if self.vc.isOpened(): # try to get the first frame
            self.loop, frame = self.vc.read()
        else:
            self.loop = False
        #self.read()

    def read(self):
        self.record = False
        
        self.loop, frame = self.vc.read()
        #blur and convert to hsv colorspace
        blur = cv2.GaussianBlur(frame, (11,11), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        
        l_h = cv2.getTrackbarPos("LH", "Tracking")
        l_s = cv2.getTrackbarPos("LS", "Tracking")
        l_v = cv2.getTrackbarPos("LV", "Tracking")
        u_h = cv2.getTrackbarPos("UH", "Tracking")
        u_s = cv2.getTrackbarPos("US", "Tracking")
        u_v = cv2.getTrackbarPos("UV", "Tracking")
        if self.l_b != (0,0,0):
            l_b = self.l_b
        else:
            l_b = np.array([l_h, l_s, l_v])
        if self.u_b != (255,255,255):
            u_b = self.u_b
        else:
            u_b = np.array([u_h, u_s, u_v])

        #create a mask and bitwise and it with the frame
        mask = cv2.inRange(hsv, l_b, u_b)
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2)
        res = cv2.bitwise_and(frame, frame, mask = mask)

        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        contours = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        if (len(contours) > 0):
            c = max(contours, key = cv2.contourArea)
            self.rectangle = RotatedRectangle(contour = c)
            
            box = self.rectangle.points
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0,255,0), 2)
            #print(self.rectangle.xyzCoords())
        cv2.imshow("result", frame)

        #delays execution
        cv2.waitKey(1)
        
        return self.rectangle
        


if __name__ == "__main__":
    c = Capture()
    while True:
        print(c.read().xyzCoords())
    

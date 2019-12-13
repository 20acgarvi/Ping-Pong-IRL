import math

class Point:
    def __init__(self, x, y, z, *args, **kwargs):
        self.x = x
        self.y = y
        self.z = z
            
class Vector:
    #takes two Points
    def __init__(self, origin, endpoint, *args, **kwargs):
        self.origin = origin
        self.endpoint = endpoint

    def qf(self):
        print("(",self.endpoint.x,",",self.endpoint.y,",",self.endpoint.z,")")

    def get_points(self):
        return [(self.origin.x, self.origin.y, self.origin.z),
                (self.endpoint.x, self.endpoint.y, self.endpoint.z)]

    def get_length(self):
        return math.sqrt((self.origin.x - self.endpoint.x)**2 +
                         (self.origin.y - self.endpoint.y)**2 +
                         (self.origin.z - self.endpoint.z)**2)
        

    def add(self, vector):
        return Vector(self.origin,
                      Point(self.endpoint.x + vector.endpoint.x,
                      self.endpoint.y + vector.endpoint.y,
                      self.endpoint.z + vector.endpoint.z))
    
class Matrix:
    #takes a 2D array
    def __init__(self, arr, *args, **kwargs):
        self.matrix = arr
        
        

    def qf(self):
        if len(self.matrix) > 1:
            for i in range(len(self.matrix[0])):
                print(self.get_row(i))
        else:
            print(self.matrix)

    def arr(self):
        return self.matrix
        
    def get_row(self, i):
        return self.matrix[i]

    def get_column(self, i):
        arr = []
        for row in self.matrix:
            arr.append(row[i])
        return arr

    def multiply(self, matrix):
        result = []
        for i in range(len(self.matrix)):
            arr = []
            for j in range(len(matrix.matrix[0])):
                row = self.get_row(i)
                column = matrix.get_column(j)
                n = 0
                for k in range(len(column)):
                    n += float(row[k]) * float(column[k])
                arr.append(n)
            result.append(arr)
        return Matrix(result)

if __name__ == "__main__":
    m = Matrix([(1.1,2.2,3.3),
               (4,5,6)])
    n = Matrix([(7,8),
                (9,10),
                (11,12)])
    o = m.multiply(n)
    o.qf()

##    v = Vector(Point(1,2,1), Point(1,2,2))
##    w = Vector(Point(0,0,0), Point(2,0,1))
##    x = v.add(w)
##    x.qf()
##    print(v.get_length())

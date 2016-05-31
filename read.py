import numpy as np
import sys

class Readboard(object):
    
    def __init__(self, name):
        self.name = name
        self.field = np.zeros((6,6), dtype=np.int)

    def read(self):
        f = open(self.name, 'r')
        for i, line in enumerate(f.readlines()):
            for j, character in enumerate(line):
                #print "({0:3},{1:3}) = {2}".format(i, j, character)
                if character == 'A': value = 1
                elif character == 'B': value = 2
                elif character == 'C': value = 3
                elif character == 'D': value = 4
                elif character == 'E': value = 5
                elif character == 'F': value = 6
                elif character == 'G': value = 7
                elif character == 'H': value = 8
                elif character == 'I': value = 9
                elif character == 'J': value = 10
                elif character == 'r': value = -1
                elif character == '.': value = 0
                else:
                    break
                self.field[i][j] = value
        #print self.field
        f.close()

    def convert(self):
        for i in [-1, 1,2,3,4,5,6,7,8,9,10]:
            a = np.where(self.field==(i))
            size = len(a[0])
            if size>1:
                #cars with size 1 cannot have direction, should throw exception
                if a[0][0] == a[0][1]:
                    direction = 0
                else:
                    direction = 1
                crdy = a[0][0]
                crdx = a[1][0]
                #print "car a has size{0}, direction {1}, crd ({2},{3})".format(size, direction, crdx, crdy)
                yield (i, size, direction, crdx, crdy)

if __name__ == "__main__":
    
    brd = Readboard("./ini.txt")
    brd.read()
    cars = brd.convert()

    for i, car in enumerate(cars):
        print "car {0} a has size{1}, direction {2}, crd ({3},{4})".format(car[0],car[1],car[2],car[3], car[4])


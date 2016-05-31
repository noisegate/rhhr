import numpy as np
import copy
import sys
from read import Readboard

class Car(object):

    VERTICAL = 1
    HORIZONTAL = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8
    I = 9
    J = 10
    r = -1

    def __init__(self, name, crdx, crdy, direction, size):
        self.name = name
        self.crdx = crdx
        self.crdy = crdy
        self.direction = direction
        self.size = size

class NoredcarError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return repr("help, cant find the red car")

class Que(object):
    #FIFO
    boards = []

    current = 0
    
    @classmethod
    def add_board(cls, brd):
        #dont repeat
        for b in cls.boards:
            if b==brd:
                return -1
        cls.boards.append(brd)
        #print "added board {0} with nr {1}to que".format(len(cls.boards), brd.number)
        brd.clear()
        brd.occupy()
        #brd.plot()
        return 0

    @classmethod
    def size(cls):
        return len(cls.boards)

    @classmethod
    def pop(cls):
        #for i, b in enumerate(cls.boards):
        #    print "que {0}: brd number {1}".format(i, b.number)
        ans = cls.boards[cls.current]
        #print "current {0}".format(cls.current)
        cls.current += 1
        return ans

class Board(object):

    count = 0

    def __init__(self):
        self.cars = []
        self.field = None
        self.number = None
        self.parent = None
        Board.counter()

    @classmethod
    def counter(cls):
        cls.count += 1

    def clear(self):
        self.field = np.zeros((6,6), dtype = np.int)

    def add_car(self, car):
        self.cars.append(car)

    def __eq__(self, other):
        for x in range(6):
            for y in range(6):
                if (self.field[y,x] != other.field[y,x]):
                    return 
        return True

    def occupy(self):
        for car in self.cars:
            x = car.crdx
            y = car.crdy

            for i in range(car.size):
                if (car.direction == Car.HORIZONTAL):
                    self.field[y, x+i] = car.name
                else:
                    self.field[y+i, x] = car.name

    def make_board(self):
        new_board = copy.deepcopy(self)
        new_board.parent = self.number
        Board.counter()
        new_board.number = Board.count
        return new_board

    def find(self, parent):
        for b in Que.boards:
            if b.number == parent:
                return b

        return -1

    def moves(self):
        nbs = []
        for i, car in enumerate(self.cars):
            #print "car {0:3}".format(car.name)

            if car.direction == Car.HORIZONTAL:
                # 0,1,..car.crdx, car.crdx+1,.., car.crdx+size, ..5
                left_contiguous = car.crdx-1
                right_contiguous = car.crdx + (car.size)
                
                if left_contiguous>-1:
                    while self.field[car.crdy, left_contiguous] == 0:
                        #print left_contiguous,
                        new_board = self.make_board()
                        new_board.cars[i].crdx = left_contiguous
                        new_board.clear()
                        new_board.occupy()
                        left_contiguous -= 1
                        nbs.append(new_board)
                        if left_contiguous == -1: 
                            #print "break"
                            break
                    #print "\n----"

                if right_contiguous<6:
                    while self.field[car.crdy, right_contiguous] == 0:
                        #print right_contiguous,
                        new_board = self.make_board()
                        new_board.number = Board.count
                        new_board.cars[i].crdx = right_contiguous-car.size+1
                        new_board.clear()
                        new_board.occupy()
                        right_contiguous = right_contiguous + 1
                        nbs.append(new_board)
                        if right_contiguous == 6: 
                            #print "break"
                            break
                    #print "\n-----"

            if car.direction == Car.VERTICAL:
                #print "ever?"
                # 0,1,..car.crdx, car.crdx+1,.., car.crdx+size, ..5
                up_contiguous = car.crdy-1
                down_contiguous = car.crdy + (car.size)
                
                if up_contiguous>-1:
                    while self.field[up_contiguous, car.crdx] == 0:
                        #print up_contiguous,
                        new_board  = self.make_board()
                        new_board.cars[i].crdy = up_contiguous
                        new_board.clear()
                        new_board.occupy()
                        up_contiguous = up_contiguous - 1
                        nbs.append(new_board)
                        if up_contiguous == -1: break
                    #print "\n----"

                if down_contiguous<6:
                    while self.field[down_contiguous, car.crdx] == 0:
                        #print down_contiguous,
                        new_board = self.make_board()
                        new_board.cars[i].crdy = down_contiguous-car.size+1
                        new_board.clear()
                        new_board.occupy()
                        down_contiguous = down_contiguous + 1
                        nbs.append(new_board)
                        if down_contiguous ==6:
                            break
                    #print "\n-----"

        return nbs

    def findredcar(self):
        for x in range(6):
            for y in range(6):
                if self.field[y][x] == -1:
                    return y
        return -1

    def solved(self):
        row = self.findredcar()
        if row == -1:
            raise NoredcarError()
            sys.exit()
        for x in range(6):
            if (self.field[row][x] == -1) or (self.field[row][x] == 0):
                pass
            else:
                return False
        return True


    def test(self):
        cp = copy.deepcopy(self)
        cp.cars[0].crdx -= 1
        return cp

    def plot(self):
        self.clear()
        self.occupy()
        for y in range(6):
            for x in range(6):
                print "{0:3} ".format(self.field[y,x]),
            print

class Game(object):

    def __init__(self, filename):
        brd = Readboard(filename)
        brd.read()
        cars = brd.convert()

        self.root = Board()
        for i, car in enumerate(cars):
            self.root.add_car(Car(car[0], car[3], car[4], car[2], car[1]))

        self.root.plot()
        self.root.number = 0
        self.root.parent = -1
        Que.add_board(self.root)

        self.steps = []

    def solution(self):
        iteration =0
        noadded=1

        while True:
            iteration +=1
            board = Que.pop()
            board.clear()
            board.occupy()
            if board.solved():
                print "solved"
                nextbrd = board
                while True:
                    print 
                    self.steps.append(nextbrd)
                    for i in Que.boards:
                        if i.number == nextbrd.parent:
                            nextbrd = i
                            break
                    if nextbrd.number == 0: break                    

                return self.steps
            new_boards = board.moves()
            noadded=0
            for nb in new_boards:
                nb.clear()
                nb.occupy()
                if (Que.add_board(nb)==0): 
                    noadded +=1

class Niceplot():
    pass

if __name__ == "__main__":

    #import a board

    game = Game("./ini.txt")
    res = game.solution()
    
    for step in res:
        print
        step.plot()



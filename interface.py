import curses
from time import sleep
import rhhr

class Box(object):

    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen

    def draw(self):

        for x in range(self.width-1):
            self.screen.addch(self.y, self.x+x, curses.ACS_HLINE)
            self.screen.addch(self.y+self.height-1, self.x+x, curses.ACS_HLINE)
        for y in range(self.height-1):
            self.screen.addch(self.y+y, self.x, curses.ACS_VLINE)
            self.screen.addch(self.y+y, self.x+self.width-1, curses.ACS_VLINE)

        #self.screen.scrollok(True)
        self.screen.addch(self.y, self.x, curses.ACS_ULCORNER)
        self.screen.addch(self.y, self.x+self.width-1, curses.ACS_URCORNER)
        self.screen.addch(self.y+self.height-1, self.x+self.width-1, curses.ACS_LRCORNER)
        self.screen.addch(self.y+self.height-1, self.x, curses.ACS_LLCORNER)

class Field(object):

    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.board = Box(self.screen, x, y, width, height)
        
    def draw(self):

        self.screen.clear()
        self.board.draw()
        self.screen.addstr(0,0,"Rush Hour".center(self.width), curses.A_REVERSE)
        self.screen.addstr(2,0,"q=quit, s=solve, r=repeat solution")
        for x in range(6):
            for y in range(6):
                self.screen.addch(2+self.y+5*y,5+self.x+10*x, ".")

    def drawbox(self, x, y, w, h, color):

        for xp in range(w):
            for yp in range(h):
                self.screen.addstr(y+yp,x+xp," ", curses.color_pair(color)|curses.A_REVERSE)

    def drawcars(self, cars):
        for i, car in enumerate(cars):
            x = car.crdx    
            y = car.crdy
            size = car.size
            #self.screen.addch(self.y + 5*y, self.x + x*10, car.name)
            if car.name == -1:
                i = 11
            if car.direction ==0:
                self.drawbox(self.x+10*x+1, self.y + 5*y+1, car.size*10-2, 5-2, i)
            else:
                self.drawbox(self.x+10*x+1, self.y + 5*y+1, 10-2, 5*car.size-2, i)


class Interface(object):

    def __init__(self, game):
        self.screen = curses.initscr()
        curses.start_color()
        self.size = self.screen.getmaxyx()
        self.height = self.size[0]
        self.width = self.size[1]
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        self.screen.nodelay(1)#nonblocking fethc getch
        self.callback=None
                                           
        self.halfwidth = self.width/2
        self.halfheight = self.height/2

        self.field = Field(self.screen, self.halfwidth-30, self.halfheight-15, 60,30)
        self.game = game
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(9, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(10, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_WHITE)
        
        self.res = None

    def animate(self, delay):
        for step in reversed(self.res):
            sleep(delay)
            self.field.draw()
            self.field.drawcars(step.cars)
            self.screen.refresh()

    def loop(self):
        go = 1
        self.field.draw()
        self.field.drawcars(game.root.cars)
        self.screen.refresh() 
        while go:
            sleep(0.1)
            c = self.screen.getch()
            if (c==ord('q')):
                self.quit()
            if (c==ord('s')):
                self.screen.addstr(4,0, "Trying to solve, please wait...")
                self.screen.refresh()
                self.res = self.game.solution()
                self.animate(2)
            if (c==ord('r')):
                self.animate(1)
            self.screen.addstr(0,0,"Rush Hour".center(self.width), curses.A_REVERSE)

    def quit(self):
        self.screen.clear()
        self.screen.refresh()
        curses.endwin()
        ser.close()

if __name__ == "__main__":
   
    game = rhhr.Game("./ini.txt")

    i = Interface(game)
    i.loop()


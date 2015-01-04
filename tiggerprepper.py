import sys,tty,termios,os,random


class guy:
    x    = None
    y    = None
    look = None
    tnrg = None
    mnrg = None 
    foodlook = None
    alive = True

    def __init__(self, x, y, look, tnrg, mnrg, foodlook):
        self.x = x
        self.y = y
        self.look = look
        self.tnrg = tnrg
        self.mnrg = mnrg
        self.foodlook = foodlook

    def right(self):
        self.x +=1

    def left(self):
        self.x -= 1

    def up(self):
        self.y -=1
    def down(self):
         self.y +=1

    def constrain(self, minX, maxX, minY, maxY):
        self.x = posChange(self.x, minX, maxX)
        self.y = posChange(self.y, minY, maxY)

    def info(self):
        print "{0} X:{1} Y:{2} Te:{3} Me:{4}".format(
        self.look
        ,str(self.x)
        ,str(self.y)
        ,str(self.tnrg)
        ,str(self.mnrg))

    def eat(self, guys):
        for key in guys:
                if self.foodlook == guys[key].look and self.at(guys[key]) and guys[key].alive:
                        self.tnrg += guys[key].tnrg
                        guys[key].alive = False
                        guys[key].look = "x"
                        guys[key].tnrg =0

    def warp(self, xm, xM, ym, yM):
        self.x = random.randint(xm, xM)
        self.y = random.randint(ym, yM)

            
    def at(self, other):
        return self.x == other.x and self.y == other.y

                     
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def printWorld(X,Y,guys):
        global mousex
        global mousey

        os.system('clear')
        for y in range(-Y,Y+1):
            row =''

            for x in range(-X,X+1):
                point = '.'
                for dude in guys:
                    if guys[dude].x == x and guys[dude].y == y:
                        point = guys[dude].look
                row += point
            
            print row
        for dude in guys:
            guys[dude].info()

            
def get(X,Y,guys):
        global tiggerx
        global tiggery

        
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        #UP
        if k=='\x1b[A':
                guys['tiggy'].up()
                
        #DOWN
        elif k=='\x1b[B':
                guys['tiggy'].down()

        #RIGHT                        
        elif k=='\x1b[C':
                guys['tiggy'].right()

        #LEFT        
        elif k=='\x1b[D':
                guys['tiggy'].left()

        else:
                print "not an arrow key!"

        for dude in guys:
                guys[dude].constrain(-X,+X,-Y,+Y)
                guys[dude].eat(guys)
        printWorld(X,Y,guys)

def posChange(num, minipad, maxipad):
    if num > maxipad:
        num = num - maxipad + minipad -1
    elif num < minipad:
        num = num - minipad +maxipad +1
    return num
        
# 2-->2
# 1-->10(max)
# 0-->9


def main():
    
        X = 5
        Y = 5

        guys = {'m1'       : guy(0, 0, 'm', 10, 0, '<') ,
                'm2'       : guy(0, 0, 'm', 10, 0, '<') ,
                'c1'       : guy(0, 0, '8', 30, 0, '&' ),
                'tiggy'    : guy(0, 0, '&', 20, 0, 'm') }

        guys['m1'].warp(-X,X,-Y,Y)

        guys['m2'].warp(-X,X,-Y,Y)

        guys['c1'].warp(-X,X,-Y,Y)
                
        printWorld(X, Y, guys)
        
        while guys['tiggy'].tnrg > 0:
                get(X, Y, guys)
                guys['c1'].x += 1
                guys['tiggy'].tnrg -=1
              
if __name__=='__main__':
        main()



import pygame
import matplotlib.pyplot as plt
import time
import random


FRAME=0.07
Gravity=9.81
AirResistant=0

class flight:
    force=0
    KI=0.003
    KP=1.2
    KD=380
    MASS=30

    def __init__(self,screen,aim,Ki,Kp,Kd,color=None):
        self.KI,self.KP,self.KD=Ki,Kp,Kd
        self.aimLevel=aim
        self.DifferenceCounter=0
        self.x = 0
        self.__y = 0
        self.LastDifference=self.y - aim
        self.color=(random.randint(1,255),random.randint(1,255),random.randint(1,255)) if color==None else color
        self.screen=screen
        self.lineStroe=aim
        self.velocity=0 # Y axis
        self.differentList=[[0],[0]]
        self.maxForce=0
        self.Gradient=0
    @property
    def y(self):
        return 650-self.__y
    @y.setter
    def y(self,get):
        self.__y=get

    def pidGet(self):
        diff = self.y - self.aimLevel

        self.DifferenceCounter += diff
        Kp = self.KP * diff
        self.Gradient=diff - self.LastDifference
        Kd = self.KD * (self.Gradient)
        #print(diff , self.LastDifference)
        Ki = self.KI * self.DifferenceCounter
        self.LastDifference = diff
        self.force = Kp + Kd + Ki
        #print(self.force)
        if abs(self.force)>self.maxForce:
            #print(Kp,Ki,Kd)
            #print(self.force)
            self.maxForce=self.force
        self.differentList[0].append(diff)
        self.differentList[1].append(self.differentList[1][len(self.differentList[1])-1]+1)

    def move(self):
        self.pidGet()
        accele=(self.force-self.MASS*Gravity)/self.MASS
        self.velocity+=accele*FRAME

        self.y = self.velocity * FRAME + self.__y




    def startMove(self,x,y):
        self.aimLevel=y
        self.lineStroe=y
        self.DifferenceCounter = self.y - self.aimLevel
        self.LastDifference=self.y - self.aimLevel
        self.differentList = [[self.DifferenceCounter], [0]]

    def disPlay(self):
        # head=pygame.image.load("wrj.png")
        # bodysize = pygame.transform.scale(head, (70, 70))
        # bodyxy = bodysize.get_rect(center=(400, self.y))
        # self.screen.blit(bodysize, bodyxy)
        get=pygame.Rect(0,0,40,10)
        get.center=(400, self.y)
        pygame.draw.rect(self.screen,self.color,get)


        #print(1)
    def displayMatplotlib(self):

        #while True:
        plt.pause(0.000000000000001)
        plt.cla()
        plt.xlabel("time")
        plt.ylabel("difference")
        plt.grid(True)

        plt.plot(self.differentList[1],self.differentList[0])
    def __repr__(self):
        return "MaxForce:{}  kp:{}  ki:{}  kd:{}".format(self.maxForce,self.KP,self.KI,self.KD)
def flightMove(array,up,down):
    for getFlight in array:
        if getFlight.y>up or getFlight.y<down:
            array.remove(getFlight)
        else:
            getFlight.disPlay()
            getFlight.move()
def changeAim(array,pos):
    for getFlight in array:
        getFlight.startMove(0,pos)
def Select(object):
    return abs(object.LastDifference)*abs(object.Gradient)*(object.maxForce)**2


def train(array,screen,aimLevel):# 遗传算法
    sortArray=sorted(array,key=Select)

    Best=sortArray[0]
    newArray = [flight(screen,aimLevel,Best.KI,Best.KP,Best.KD,Best.color)]
    for clone in range(4):
        newArray.append(flight(screen,aimLevel,Best.KI *getRandom(0.5),Best.KP*getRandom(0.5),Best.KD*getRandom()))
    for another in range(5):
        newArray.append(flight(screen,aimLevel,getRandom(0.001),getRandom(5),getRandom(100)))
    newArray.append(flight(screen,aimLevel,0.003,10.2,380))
    print(Best)
    return newArray

def getRandom(di=1.0):
    return random.random()*di*random.randint(1,5)
def main():
    run = True
    outLineUp,outLineDown=700,0
    pygame.init()
    aimLevel=370
    clock=time.time()
    screen = pygame.display.set_mode((800, 700))
    getFlights=[flight(screen,aimLevel,0.005*getRandom(),1.2*getRandom(),380*getRandom()) for i in range(10)]
    timeChange=[12,24]
    while run:

        screen.fill((12, 0, 0))
        # getFlight.disPlay()
        # getFlight.move()
        # getFlight.displayMatplotlib()
        pygame.draw.line(screen, (0, 125, 205), [0, aimLevel + 10], [800, aimLevel + 10], 10)
        pygame.draw.line(screen, (255,0,0), [0, outLineUp + 10], [800, outLineUp + 10], 10)
        pygame.draw.line(screen, (255, 0, 0), [0, outLineDown ], [800, outLineDown], 10)
        outLineUp-=0.0006*(700-aimLevel)
        outLineDown+=0.0006*(aimLevel)
        for eve in pygame.event.get():
            if eve.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                #changeAim(getFlights, pos)
                # getFlight.startMove(*pos)
            if eve.type == pygame.QUIT:
                run = False
                pygame.quit()
        if int(time.time()-clock) in timeChange:
            timeChange.pop(0)
            outLineUp, outLineDown = 700, 0
            ran = random.randint(1, 600)
            aimLevel = ran
            changeAim(getFlights, ran)
        if time.time()-clock>=36 or len(getFlights)<=2:
            timeChange = [12, 24]
            outLineUp, outLineDown = 700, 0
            clock=time.time()
            ran=random.randint(1,600)
            aimLevel=ran
            getFlights=train(getFlights,screen,ran)
            print(1)
        flightMove(getFlights,outLineUp,outLineDown)
        pygame.display.flip()

if __name__=='__main__':
    main()
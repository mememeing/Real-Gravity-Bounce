import pygame
import os, sys
from pygame.locals import *
from pygame import draw
#Made by Julian -_-
#This is a 32bit game resulting in a window that is 32x16 blocks wide
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')
print (os.getcwd())
class Cube(pygame.sprite.Sprite):
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.coli = False
        self.botcol = False
        self.topcol = False
        self.rightcol = False
        self.leftcol = False
        pygame.sprite.Sprite.__init__(self)
        self.color = "red"
        self.image= pygame.image.load('resources/sprites/cube/red.png')
        self.rect = self.image.get_rect()
        self.x,self.y = self.width//4, self.height//2
        self.v = 0
        self.rect.topleft= (self.x, self.y)
        self.gravitydown = True
    def update(self):
        if self.gravitydown == True:
            if self.rect.bottom<self.height:
                self.v+=.4
                self.y+=self.v
            elif self.rect.bottom>= self.height:
                self.rect.bottom=self.height
        elif self.gravitydown == False:
            if self.rect.top>0:
                self.v-=.4
                self.y+=self.v
            elif self.rect.top<0:
                self.rect.top = 0
        self.rect.topleft = self.x,self.y
        if self.rect.bottom> self.height:
            self.rect.bottom=self.height
        elif self.rect.top<=0:
            self.rect.top = 0

    def cbc(self):
        if self.y>0:
            self.getblocktype
            
            
    def switchgrav(self):
        print("g switch")
        self.v = 0
        if self.gravitydown == True:
            self.gravitydown = False
        elif self.gravitydown == False:
            self.gravitydown = True

    def switchcol(self):
        print("c switch")
        if self.color == 'red':
            self.color = 'green'
            self.image= pygame.image.load('resources/sprites/cube/green.png')
        elif self.color == 'green':
            self.color = 'blue'
            self.image= pygame.image.load('resources/sprites/cube/blue.png')
        elif self.color == 'blue':
            self.color = 'red'
            self.image= pygame.image.load('resources/sprites/cube/red.png')

class rectsprite(pygame.sprite.Sprite):
    def __init__(self,rtype,x,y,length):
        self.x,self.y = x,y
        self.rtype = rtype
        if rtype == 'black':
            self.color = (0,0,0)
        elif rtype == 'red':
            self.color = (255,0,0)
        elif rtype == 'green':
            self.color = (0,255,0)
        elif rtype == 'blue':
            self.color = (0,0,255)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((length*32,32))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
    def update(self):
        print("help")
class mainG:
    def __init__(self,width =1024,height=512):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Real Gravity Bounce')
        
    def MainLoop(self):
        self.LoadGame()
        while 1:
            self.screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.cube.switchgrav()
                    if event.key == pygame.K_g:
                        self.cube.switchcol()
            if pygame.sprite.groupcollide(self.allsprites,self.level_s,False,False):
                self.detcode()
            self.allsprites.update()
            self.level_s.draw(self.screen)
            self.allsprites.draw(self.screen)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(60)
    def LoadGame(self):
        #load everything we need
        self.cube=Cube(self.width,self.height)
        self.allsprites = pygame.sprite.Group((self.cube))
        self.level_s = pygame.sprite.Group()
        self.GetLayout()
        self.drawMap()

    

    def GetLayout(self,lvln = 1):
        self.lvln=lvln
        print("getting layout")
        self.layout= open('resources/maps/' + str(self.lvln) + '/layout.rgb','r')
        self.mapar = []
        linen = 0
        for line in self.layout:
            self.mapar.append([])
            for unit in line:
                if unit != '\n':
                    self.mapar[linen].append(int(unit))
            linen+=1
    def detcode(self):
        collisions = pygame.sprite.spritecollide(self.cube,self.level_s,False)
        
        for i in collisions:
            if i.rtype == 'black':
                self.cube.cbc
                
            if i.rtype == 'red':
                if self.cube.color!= 'red':
                    self.cube.crc
            
    def getblocktype(self,x,y):
        bx=int(x/32)
        by=int(y/32)
        if self.mapar[bx][by] == 0:
            return 'white'
        elif self.mapar[bx][by] == 1:
            return 'black'
        elif self.mapar[bx][by] == 3:
            return 'red'
        else:
            return 'white'
    def drawMap(self,lvln = 1):
        length=0
        rownum = 0
        lastcolumn = False
        for row in self.mapar:
            column=0
            for num in self.mapar[rownum]:
                try:
                    self.mapar[rownum][(column+1)]
                except:
                    lastcolumn=True
                if length>=16:
                    lastcolumn = True
                if lastcolumn == False:
                    if self.mapar[rownum][column]==self.mapar[rownum][(column+1)]:
                        length+=1
                        
                    else:
                        self.drawrect(rownum,column,length,num)
                        length = 0
                else:
                    self.drawrect(rownum,column,length,num)
                    length=0
                    lastcolumn = False
                column+=1
            rownum+=1
                    
    def drawrect(self,row,column,length,colorcode):
        #This sends commands to build sprites for the map
        x=(column-length)*32
        y=row*32
        length+=1
        if colorcode == 0:
            pass
        if colorcode == 1:
            #print("black")
            brect=rectsprite('black',x,y,length)
            self.level_s.add(brect)
        if colorcode == 3:
            #print ("red")
            rrect=rectsprite('red',x,y,length)
            self.level_s.add(rrect)
        if colorcode == 4:
            #print ("green")
            grect=rectsprite('green',x,y,length)
            self.level_s.add(grect)
        if colorcode == 5:
            #print ("green")
            grect=rectsprite('blue',x,y,length)
            self.level_s.add(grect)

def main():
    maingame = mainG()
    maingame.MainLoop()
    
    

if __name__ == '__main__':
    main()

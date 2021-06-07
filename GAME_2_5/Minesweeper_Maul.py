import pygame
from pygame.constants import (QUIT, KEYDOWN, K_ESCAPE)
import os
import sys
import random
import time

class Settings(object):
    def __init__(self):
        self.width = 600
        self.height = 700
        self.fps = 60
        self.title = "Minesweeper"
        self.file_path = os.path.dirname(os.path.abspath(__file__))

    def get_size(self):
        return(self.width,self.height)

class Table():
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        #colors
        self.darkgrey= [100,100,100]
        self.black= [0,0,0]
        self.orange= [200,200,0]

    def grid(self,screen):  #tabelle gmalen
        a= 130
        b= 669
        c= 30
        d= 569
        pygame.draw.rect(screen, self.darkgrey,(30,a,541,541),0)
        pygame.draw.rect(screen,self.black,(30,a,541,541),1)
        #vertikal
        pygame.draw.line(screen,self.black,(90,a),(90,b),1)
        pygame.draw.line(screen,self.black,(150,a),(150,b),1)
        pygame.draw.line(screen,self.black,(210,a),(210,b),1)
        pygame.draw.line(screen,self.black,(270,a),(270,b),1)
        pygame.draw.line(screen,self.black,(330,a),(330,b),1)
        pygame.draw.line(screen,self.black,(390,a),(390,b),1)
        pygame.draw.line(screen,self.black,(450,a),(450,b),1)
        pygame.draw.line(screen,self.black,(510,a),(510,b),1)
        #horizontal
        pygame.draw.line(screen,self.black,(c,190),(d,190),1)
        pygame.draw.line(screen,self.black,(c,250),(d,250),1)
        pygame.draw.line(screen,self.black,(c,310),(d,310),1)
        pygame.draw.line(screen,self.black,(c,370),(d,370),1)
        pygame.draw.line(screen,self.black,(c,430),(d,430),1)
        pygame.draw.line(screen,self.black,(c,490),(d,490),1)
        pygame.draw.line(screen,self.black,(c,550),(d,550),1)
        pygame.draw.line(screen,self.black,(c,610),(d,610),1)

  #  def warning(self,screen,tz,zt):        nicht ganz geklappt
   #     pygame.draw.rect(screen,self.orange,(tz,zt,60,60),0)

class Box(pygame.sprite.Sprite):
    def __init__(self, pygame, settings,l,t):
        pygame.sprite.Sprite.__init__(self)
        self.pygame = pygame
        self.settings = settings
        self.image = pygame.image.load(os.path.join(
                    self.settings.file_path, "plate.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.mask.Mask.get_rect(self.mask)
        self.rect.left = l
        self.rect.top = t

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pygame, settings):
        pygame.sprite.Sprite.__init__(self)
        self.pygame = pygame
        self.settings = settings
        self.image = pygame.image.load(os.path.join(
                    self.settings.file_path, "boom.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.mask.Mask.get_rect(self.mask)
        left= [33,93,153,213,273,333,393,453,513]
        top= [133,193,253,313,373,433,493,553,613]
        self.rect.left = random.choice(left)                # zufällige stellen
        self.rect.top = random.choice(top)

class Flag(pygame.sprite.Sprite):
    def __init__(self, pygame, settings,left,top):
        pygame.sprite.Sprite.__init__(self)
        self.pygame = pygame
        self.settings = settings
        self.image = pygame.image.load(os.path.join(
                    self.settings.file_path, "flagy.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.mask.Mask.get_rect(self.mask)
        self.rect.left= left               
        self.rect.top= top

class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame     
        self.settings = settings
        #colors
        self.darkgrey= [100,100,100]
        self.black= [0,0,0]
        self.lightgrey= [150,150,150]
        self.red= [255,0,0]
        
        # --
        self.screen = pygame.display.set_mode(settings.get_size())                                      
        self.pygame.display.set_caption(self.settings.title)  
        self.background= self.screen.fill(self.lightgrey)
        self.clock = pygame.time.Clock()   
        self.done= False 
        #Tabelle
        self.table= Table(self.pygame,self.settings)
        #Koordinaten für die Boxs
        self.row1= 133
        self.row2= self.row1 + 60
        self.row3= self.row2 + 60
        self.row4= self.row3 + 60
        self.row5= self.row4 + 60
        self.row6= self.row5 + 60
        self.row7= self.row6 + 60
        self.row8= self.row7 + 60
        self.row9= self.row8 + 60
        self.column1= 33
        self.column2 = self.column1 + 60
        self.column3 = self.column2 + 60
        self.column4 = self.column3 + 60
        self.column5 = self.column4 + 60
        self.column6 = self.column5 + 60
        self.column7 = self.column6 + 60
        self.column8 = self.column7 + 60
        self.column9 = self.column8 + 60
        # Zeile 1
        self.box1_1= Box(pygame,settings,self.column1,self.row1)
        self.box1_2= Box(pygame,settings,self.column2,self.row1)
        self.box1_3= Box(pygame,settings,self.column3,self.row1)
        self.box1_4= Box(pygame,settings,self.column4,self.row1)
        self.box1_5= Box(pygame,settings,self.column5,self.row1)
        self.box1_6= Box(pygame,settings,self.column6,self.row1)
        self.box1_7= Box(pygame,settings,self.column7,self.row1)
        self.box1_8= Box(pygame,settings,self.column8,self.row1)
        self.box1_9= Box(pygame,settings,self.column9,self.row1)
        # Zeile 2
        self.box2_1= Box(pygame,settings,self.column1,self.row2)
        self.box2_2= Box(pygame,settings,self.column2,self.row2)
        self.box2_3= Box(pygame,settings,self.column3,self.row2)
        self.box2_4= Box(pygame,settings,self.column4,self.row2)
        self.box2_5= Box(pygame,settings,self.column5,self.row2)
        self.box2_6= Box(pygame,settings,self.column6,self.row2)
        self.box2_7= Box(pygame,settings,self.column7,self.row2)
        self.box2_8= Box(pygame,settings,self.column8,self.row2)
        self.box2_9= Box(pygame,settings,self.column9,self.row2)
        # Zeile 3
        self.box3_1= Box(pygame,settings,self.column1,self.row3)
        self.box3_2= Box(pygame,settings,self.column2,self.row3)
        self.box3_3= Box(pygame,settings,self.column3,self.row3)
        self.box3_4= Box(pygame,settings,self.column4,self.row3)
        self.box3_5= Box(pygame,settings,self.column5,self.row3)
        self.box3_6= Box(pygame,settings,self.column6,self.row3)
        self.box3_7= Box(pygame,settings,self.column7,self.row3)
        self.box3_8= Box(pygame,settings,self.column8,self.row3)
        self.box3_9= Box(pygame,settings,self.column9,self.row3)
        # Zeile 4
        self.box4_1= Box(pygame,settings,self.column1,self.row4)
        self.box4_2= Box(pygame,settings,self.column2,self.row4)
        self.box4_3= Box(pygame,settings,self.column3,self.row4)
        self.box4_4= Box(pygame,settings,self.column4,self.row4)
        self.box4_5= Box(pygame,settings,self.column5,self.row4)
        self.box4_6= Box(pygame,settings,self.column6,self.row4)
        self.box4_7= Box(pygame,settings,self.column7,self.row4)
        self.box4_8= Box(pygame,settings,self.column8,self.row4)
        self.box4_9= Box(pygame,settings,self.column9,self.row4)
        # Zeile 5
        self.box5_1= Box(pygame,settings,self.column1,self.row5)
        self.box5_2= Box(pygame,settings,self.column2,self.row5)
        self.box5_3= Box(pygame,settings,self.column3,self.row5)
        self.box5_4= Box(pygame,settings,self.column4,self.row5)
        self.box5_5= Box(pygame,settings,self.column5,self.row5)
        self.box5_6= Box(pygame,settings,self.column6,self.row5)
        self.box5_7= Box(pygame,settings,self.column7,self.row5)
        self.box5_8= Box(pygame,settings,self.column8,self.row5)
        self.box5_9= Box(pygame,settings,self.column9,self.row5)
        # Zeile 6
        self.box6_1= Box(pygame,settings,self.column1,self.row6)
        self.box6_2= Box(pygame,settings,self.column2,self.row6)
        self.box6_3= Box(pygame,settings,self.column3,self.row6)
        self.box6_4= Box(pygame,settings,self.column4,self.row6)
        self.box6_5= Box(pygame,settings,self.column5,self.row6)
        self.box6_6= Box(pygame,settings,self.column6,self.row6)
        self.box6_7= Box(pygame,settings,self.column7,self.row6)
        self.box6_8= Box(pygame,settings,self.column8,self.row6)
        self.box6_9= Box(pygame,settings,self.column9,self.row6)
        # Zeile 7
        self.box7_1= Box(pygame,settings,self.column1,self.row7)
        self.box7_2= Box(pygame,settings,self.column2,self.row7)
        self.box7_3= Box(pygame,settings,self.column3,self.row7)
        self.box7_4= Box(pygame,settings,self.column4,self.row7)
        self.box7_5= Box(pygame,settings,self.column5,self.row7)
        self.box7_6= Box(pygame,settings,self.column6,self.row7)
        self.box7_7= Box(pygame,settings,self.column7,self.row7)
        self.box7_8= Box(pygame,settings,self.column8,self.row7)
        self.box7_9= Box(pygame,settings,self.column9,self.row7)
        # Zeile 8
        self.box8_1= Box(pygame,settings,self.column1,self.row8)
        self.box8_2= Box(pygame,settings,self.column2,self.row8)
        self.box8_3= Box(pygame,settings,self.column3,self.row8)
        self.box8_4= Box(pygame,settings,self.column4,self.row8)
        self.box8_5= Box(pygame,settings,self.column5,self.row8)
        self.box8_6= Box(pygame,settings,self.column6,self.row8)
        self.box8_7= Box(pygame,settings,self.column7,self.row8)
        self.box8_8= Box(pygame,settings,self.column8,self.row8)
        self.box8_9= Box(pygame,settings,self.column9,self.row8)
        # Zeile 9
        self.box9_1= Box(pygame,settings,self.column1,self.row9)
        self.box9_2= Box(pygame,settings,self.column2,self.row9)
        self.box9_3= Box(pygame,settings,self.column3,self.row9)
        self.box9_4= Box(pygame,settings,self.column4,self.row9)
        self.box9_5= Box(pygame,settings,self.column5,self.row9)
        self.box9_6= Box(pygame,settings,self.column6,self.row9)
        self.box9_7= Box(pygame,settings,self.column7,self.row9)
        self.box9_8= Box(pygame,settings,self.column8,self.row9)
        self.box9_9= Box(pygame,settings,self.column9,self.row9)

        # Sprite Group für Boxs
        self.all_boxes= pygame.sprite.Group()

        # box in zeile 1
        self.all_boxes.add(self.box1_1)
        self.all_boxes.add(self.box1_2)
        self.all_boxes.add(self.box1_3)
        self.all_boxes.add(self.box1_4)
        self.all_boxes.add(self.box1_5)
        self.all_boxes.add(self.box1_6)
        self.all_boxes.add(self.box1_7)
        self.all_boxes.add(self.box1_8)
        self.all_boxes.add(self.box1_9)
        # box in zeile 2
        self.all_boxes.add(self.box2_1)
        self.all_boxes.add(self.box2_2)
        self.all_boxes.add(self.box2_3)
        self.all_boxes.add(self.box2_4)
        self.all_boxes.add(self.box2_5)
        self.all_boxes.add(self.box2_6)
        self.all_boxes.add(self.box2_7)
        self.all_boxes.add(self.box2_8)
        self.all_boxes.add(self.box2_9)
        # box in zeile 3
        self.all_boxes.add(self.box3_1)
        self.all_boxes.add(self.box3_2)
        self.all_boxes.add(self.box3_3)
        self.all_boxes.add(self.box3_4)
        self.all_boxes.add(self.box3_5)
        self.all_boxes.add(self.box3_6)
        self.all_boxes.add(self.box3_7)
        self.all_boxes.add(self.box3_8)
        self.all_boxes.add(self.box3_9)
        # box in zeile 4
        self.all_boxes.add(self.box4_1)
        self.all_boxes.add(self.box4_2)
        self.all_boxes.add(self.box4_3)
        self.all_boxes.add(self.box4_4)
        self.all_boxes.add(self.box4_5)
        self.all_boxes.add(self.box4_6)
        self.all_boxes.add(self.box4_7)
        self.all_boxes.add(self.box4_8)
        self.all_boxes.add(self.box4_9)
        # box in zeile 5
        self.all_boxes.add(self.box5_1)
        self.all_boxes.add(self.box5_2)
        self.all_boxes.add(self.box5_3)
        self.all_boxes.add(self.box5_4)
        self.all_boxes.add(self.box5_5)
        self.all_boxes.add(self.box5_6)
        self.all_boxes.add(self.box5_7)
        self.all_boxes.add(self.box5_8)
        self.all_boxes.add(self.box5_9)
        # box in zeile 6
        self.all_boxes.add(self.box6_1)
        self.all_boxes.add(self.box6_2)
        self.all_boxes.add(self.box6_3)
        self.all_boxes.add(self.box6_4)
        self.all_boxes.add(self.box6_5)
        self.all_boxes.add(self.box6_6)
        self.all_boxes.add(self.box6_7)
        self.all_boxes.add(self.box6_8)
        self.all_boxes.add(self.box6_9)
        # box in zeile 7
        self.all_boxes.add(self.box7_1)
        self.all_boxes.add(self.box7_2)
        self.all_boxes.add(self.box7_3)
        self.all_boxes.add(self.box7_4)
        self.all_boxes.add(self.box7_5)
        self.all_boxes.add(self.box7_6)
        self.all_boxes.add(self.box7_7)
        self.all_boxes.add(self.box7_8)
        self.all_boxes.add(self.box7_9)
        # box in zeile 8
        self.all_boxes.add(self.box8_1)
        self.all_boxes.add(self.box8_2)
        self.all_boxes.add(self.box8_3)
        self.all_boxes.add(self.box8_4)
        self.all_boxes.add(self.box8_5)
        self.all_boxes.add(self.box8_6)
        self.all_boxes.add(self.box8_7)
        self.all_boxes.add(self.box8_8)
        self.all_boxes.add(self.box8_9)
        # box in zeile 9
        self.all_boxes.add(self.box9_1)
        self.all_boxes.add(self.box9_2)
        self.all_boxes.add(self.box9_3)
        self.all_boxes.add(self.box9_4)
        self.all_boxes.add(self.box9_5)
        self.all_boxes.add(self.box9_6)
        self.all_boxes.add(self.box9_7)
        self.all_boxes.add(self.box9_8)
        self.all_boxes.add(self.box9_9)

        #6 bomben
        self.bomb1= Bomb(pygame,settings)
        self.bomb2= Bomb(pygame,settings)
        self.bomb3= Bomb(pygame,settings)
        self.bomb4= Bomb(pygame,settings)
        self.bomb5= Bomb(pygame,settings)
        self.bomb6= Bomb(pygame,settings)
        # Bomben Gruppe
        self.bombs= pygame.sprite.Group()
        # bomben in Gruppe
        self.bombs.add(self.bomb1)
        self.bombs.add(self.bomb2)
        self.bombs.add(self.bomb3)
        self.bombs.add(self.bomb4)
        self.bombs.add(self.bomb5)
        self.bombs.add(self.bomb6)
        # Flaggen Gruppe und variabeln
        self.flags= pygame.sprite.Group()
        self.flagnum= 6
        #clickzahlen pro feld
        self.pad1_1 = 0
        self.pad2_1 = 0
        self.pad3_1 = 0
        self.pad4_1 = 0
        self.pad5_1 = 0
        self.pad6_1 = 0
        self.pad7_1 = 0
        self.pad8_1 = 0
        self.pad9_1 = 0
        self.pad1_2 = 0
        self.pad2_2 = 0
        self.pad3_2 = 0
        self.pad4_2 = 0
        self.pad5_2 = 0
        self.pad6_2 = 0
        self.pad7_2 = 0
        self.pad8_2 = 0
        self.pad9_2 = 0
        self.pad1_3 = 0
        self.pad2_3 = 0
        self.pad3_3 = 0
        self.pad4_3 = 0
        self.pad5_3 = 0
        self.pad6_3 = 0
        self.pad7_3 = 0
        self.pad8_3 = 0
        self.pad9_3 = 0
        self.pad1_4 = 0
        self.pad2_4 = 0
        self.pad3_4 = 0
        self.pad4_4 = 0
        self.pad5_4 = 0
        self.pad6_4 = 0
        self.pad7_4 = 0
        self.pad8_4 = 0
        self.pad9_4 = 0
        self.pad1_5 = 0
        self.pad2_5 = 0
        self.pad3_5 = 0
        self.pad4_5 = 0
        self.pad5_5 = 0
        self.pad6_5 = 0
        self.pad7_5 = 0
        self.pad8_5 = 0
        self.pad9_5 = 0
        self.pad1_6 = 0
        self.pad2_6 = 0
        self.pad3_6 = 0
        self.pad4_6 = 0
        self.pad5_6 = 0
        self.pad6_6 = 0
        self.pad7_6 = 0
        self.pad8_6 = 0
        self.pad9_6 = 0
        self.pad1_7 = 0
        self.pad2_7 = 0
        self.pad3_7 = 0
        self.pad4_7 = 0
        self.pad5_7 = 0
        self.pad6_7 = 0
        self.pad7_7 = 0
        self.pad8_7 = 0
        self.pad9_7 = 0
        self.pad1_8 = 0
        self.pad2_8 = 0
        self.pad3_8 = 0
        self.pad4_8 = 0
        self.pad5_8 = 0
        self.pad6_8 = 0
        self.pad7_8 = 0
        self.pad8_8 = 0
        self.pad9_8 = 0
        self.pad1_9 = 0
        self.pad2_9 = 0
        self.pad3_9 = 0
        self.pad4_9 = 0
        self.pad5_9 = 0
        self.pad6_9 = 0
        self.pad7_9 = 0
        self.pad8_9 = 0
        self.pad9_9 = 0

        # sekunden
        self.ticks = pygame.time.get_ticks()
        self.spawn= ((pygame.time.get_ticks()-self.ticks)/1000)

        self.font = pygame.font.Font(None, 50)                                                        
        self.textsec = self.font.render("start", True, self.red)                     
        self.textRectsec = self.textsec.get_rect()                                                            
        self.textRectsec.center = 40,50
        # flagen anzahl
        self.textflag = self.font.render(str(self.flagnum), True, self.red)                     
        self.textRectflag = self.textflag.get_rect()                                                            
        self.textRectflag.center = 540,50
        #gameover
        self.font2 = pygame.font.Font(None, 100) 
        self.textgameover = self.font2.render(" ",True, self.red)                     
        self.textRectgameover = self.textgameover.get_rect()                                                            
        self.textRectgameover.center = 90,350
        #winning
        self.font3 = pygame.font.Font(None, 100) 
        self.textwin = self.font3.render(" ",True, self.red)                     
        self.textRectwin = self.textwin.get_rect()                                                            
        self.textRectwin.center = 110,350

        #flagen auf bomben zählen
        self.winnumb= 0
        # bool zum verlieren 
        self.lose= False


        
    def run(self):
        while not self.done: 
            self.clock.tick(self.settings.fps)    
            self.timef= (pygame.time.get_ticks()-self.ticks)/1000
            self.time= round(self.timef)  
            self.textsec = self.font.render(str(self.time), True, self.red) # Sekunden Zählung
            for event in self.pygame.event.get():       
                if event.type == QUIT:                                           
                    self.done = True                 
                elif event.type == KEYDOWN:            
                    if event.key == K_ESCAPE:
                        self.done = True
                    
                self.mouse = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #rechts click, Feld löschen
                    if event.button == 3:
                        for b in self.all_boxes:
                            if b.rect.collidepoint(self.mouse):
                                b.kill()
                        for p in self.bombs:
                            if p.rect.collidepoint(self.mouse):
                                self.lose= True
                            if (p.rect.left-60) <= self.mouse[0] <= p.rect.left and p.rect.top <= self.mouse[1] <= (p.rect.top+60):
                                #self.table.warning(self.screen,(p.rect.left-60),p.rect.top) ; Malen nicht auf Tabelle, sondern drunter
                                print("WARNING! BOMB ON THE RIGHT")
                            if (p.rect.left+60) <= self.mouse[0] <= (p.rect.left+120) and p.rect.top <= self.mouse[1] <= (p.rect.top+60):
                               # self.table.warning(self.screen,(p.rect.left+60),p.rect.top)
                               print("WARNING! BOMB ON THE LEFT")
                            if p.rect.left <= self.mouse[0] <= (p.rect.left+60) and (p.rect.top-60) <= self.mouse[1] <= p.rect.top:
                               # self.table.warning(self.screen,p.rect.left,(p.rect.top-60))
                               print("WARNING! BOMB BELOW")
                            if p.rect.left <= self.mouse[0] <= (p.rect.left+60) and (p.rect.top+60) <= self.mouse[1] <= (p.rect.top+120):
                               # self.table.warning(self.screen,p.rect.left,(p.rect.top+60))
                               print("WARNING! BOMB ABOVE")
                    #links click; Flagen, zählen ist buggy
                    if event.button == 1:
                        #feld 1_1
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad1_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_1 == 1:
                                    a= Flag(pygame,settings,self.column1,self.row1)
                                    self.flags.add(a)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_1 == 2:
                                    a.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_1 -= 2
                            if self.flagnum == 0:
                                self.pad1_1 = 0
                        #feld 2_1
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad2_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_1 == 1:
                                    b= Flag(pygame,settings,self.column2,self.row1)
                                    self.flags.add(b)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_1 == 2:
                                    b.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_1 -= 2
                            if self.flagnum == 0:
                                self.pad2_1 = 0
                        #feld 3_1
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad3_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_1 == 1:
                                    c= Flag(pygame,settings,self.column3,self.row1)
                                    self.flags.add(c)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_1 == 2:
                                    c.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_1 -= 2
                            if self.flagnum == 0:
                                self.pad3_1 = 0
                        #feld 4_1
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad4_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_1 == 1:
                                    d= Flag(pygame,settings,self.column4,self.row1)
                                    self.flags.add(d)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_1 == 2:
                                    d.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_1 -= 2
                            if self.flagnum == 0:
                                self.pad4_1 = 0
                        #feld 5_1
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad5_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_1 == 1:
                                    e= Flag(pygame,settings,self.column5,self.row1)
                                    self.flags.add(e)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_1 == 2:
                                    e.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_1 -= 2
                            if self.flagnum == 0:
                                self.pad5_1 = 0
                        #feld 6_1
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad6_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_1 == 1:
                                    f= Flag(pygame,settings,self.column6,self.row1)
                                    self.flags.add(f)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_1 == 2:
                                    f.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_1 -= 2
                            if self.flagnum == 0:
                                self.pad6_1 = 0
                        #feld 7_1
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad7_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_1 == 1:
                                    g= Flag(pygame,settings,self.column7,self.row1)
                                    self.flags.add(g)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_1 == 2:
                                    g.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_1 -= 2
                            if self.flagnum == 0:
                                self.pad7_1 = 0
                        #feld 8_1
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad8_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_1 == 1:
                                    h= Flag(pygame,settings,self.column8,self.row1)
                                    self.flags.add(h)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_1 == 2:
                                    h.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_1 -= 2
                            if self.flagnum == 0:
                                self.pad8_1 = 0
                        #feld 9_1
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row1 <= self.mouse[1] <= self.row2:
                            self.pad9_1 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_1 == 1:
                                    i= Flag(pygame,settings,self.column9,self.row1)
                                    self.flags.add(i)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_1 == 2:
                                    i.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_1 -= 2
                            if self.flagnum == 0:
                                self.pad9_1 = 0
                        #feld 1_2
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad1_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_2 == 1:
                                    onetwo= Flag(pygame,settings,self.column1,self.row2)
                                    self.flags.add(onetwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_2 == 2:
                                    onetwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_2 -= 2
                            if self.flagnum == 0:
                                self.pad1_2 = 0
                        #feld 2_2
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad2_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_2 == 1:
                                    twotwo= Flag(pygame,settings,self.column2,self.row2)
                                    self.flags.add(twotwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_2 == 2:
                                    twotwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_2 -= 2
                            if self.flagnum == 0:
                                self.pad2_2 = 0
                        #feld 3_2
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad3_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_2 == 1:
                                    threetwo= Flag(pygame,settings,self.column3,self.row2)
                                    self.flags.add(threetwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_2 == 2:
                                    threetwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_2 -= 2
                            if self.flagnum == 0:
                                self.pad3_2 = 0
                        #feld 4_2
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad4_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_2 == 1:
                                    fourtwo= Flag(pygame,settings,self.column4,self.row2)
                                    self.flags.add(fourtwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_2 == 2:
                                    fourtwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_2 -= 2
                            if self.flagnum == 0:
                                self.pad4_2 = 0
                        #feld 5_2
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad5_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_2 == 1:
                                    fivetwo= Flag(pygame,settings,self.column5,self.row2)
                                    self.flags.add(fivetwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_2 == 2:
                                    fivetwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_2 -= 2
                            if self.flagnum == 0:
                                self.pad5_2 = 0
                        #feld 6_2
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad6_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_2 == 1:
                                    sixtwo= Flag(pygame,settings,self.column6,self.row2)
                                    self.flags.add(sixtwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_2 == 2:
                                    sixtwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_2 -= 2
                            if self.flagnum == 0:
                                self.pad6_2 = 0
                        #feld 7_2
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad7_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_2 == 1:
                                    seventwo= Flag(pygame,settings,self.column7,self.row2)
                                    self.flags.add(seventwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_2 == 2:
                                    seventwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_2 -= 2
                            if self.flagnum == 0:
                                self.pad7_2 = 0
                        #feld 8_2
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad8_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_2 == 1:
                                    eighttwo= Flag(pygame,settings,self.column8,self.row2)
                                    self.flags.add(eighttwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_2 == 2:
                                    eighttwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_2 -= 2
                            if self.flagnum == 0:
                                self.pad8_2 = 0
                        #feld 9_2
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row2 <= self.mouse[1] <= self.row3:
                            self.pad9_2 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_2 == 1:
                                    ninetwo= Flag(pygame,settings,self.column9,self.row2)
                                    self.flags.add(ninetwo)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_2 == 2:
                                    ninetwo.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_2 -= 2
                            if self.flagnum == 0:
                                self.pad9_2 = 0
                        #feld 1_3
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad1_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_3 == 1:
                                    onethree= Flag(pygame,settings,self.column1,self.row3)
                                    self.flags.add(onethree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_3 == 2:
                                    onethree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_3 -= 2
                            if self.flagnum == 0:
                                self.pad1_3 = 0
                        #feld 2_3
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad2_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_3 == 1:
                                    twothree= Flag(pygame,settings,self.column2,self.row3)
                                    self.flags.add(twothree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_3 == 2:
                                    twothree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_3 -= 2
                            if self.flagnum == 0:
                                self.pad2_3 = 0
                        #feld 3_3
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad3_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_3 == 1:
                                    threethree= Flag(pygame,settings,self.column3,self.row3)
                                    self.flags.add(threethree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_3 == 2:
                                    threethree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_3 -= 2
                            if self.flagnum == 0:
                                self.pad3_3 = 0
                        #feld 4_3
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad4_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_3 == 1:
                                    fourthree= Flag(pygame,settings,self.column4,self.row3)
                                    self.flags.add(fourthree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_3 == 2:
                                    fourthree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_3 -= 2
                            if self.flagnum == 0:
                                self.pad4_3 = 0
                        #feld 5_3
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad5_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_3 == 1:
                                    fivethree= Flag(pygame,settings,self.column5,self.row3)
                                    self.flags.add(fivethree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_3 == 2:
                                    fivethree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_3 -= 2
                            if self.flagnum == 0:
                                self.pad5_3 = 0
                        #feld 6_3
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad6_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_3 == 1:
                                    sixthree= Flag(pygame,settings,self.column6,self.row3)
                                    self.flags.add(sixthree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_3 == 2:
                                    sixthree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_3 -= 2
                            if self.flagnum == 0:
                                self.pad6_3 = 0
                        #feld 7_3
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad7_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_3 == 1:
                                    seventhree= Flag(pygame,settings,self.column7,self.row3)
                                    self.flags.add(seventhree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_3 == 2:
                                    seventhree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_3 -= 2
                            if self.flagnum == 0:
                                self.pad7_3 = 0
                        #feld 8_3
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad8_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_3 == 1:
                                    eightthree= Flag(pygame,settings,self.column8,self.row3)
                                    self.flags.add(eightthree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_3 == 2:
                                    eightthree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_3 -= 2
                            if self.flagnum == 0:
                                self.pad8_3 = 0
                        #feld 9_3
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row3 <= self.mouse[1] <= self.row4:
                            self.pad9_3 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_3 == 1:
                                    ninethree= Flag(pygame,settings,self.column9,self.row3)
                                    self.flags.add(ninethree)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_3 == 2:
                                    ninethree.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_3 -= 2
                            if self.flagnum == 0:
                                self.pad9_3 = 0
                        #feld 1_4
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad1_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_4 == 1:
                                    onefour= Flag(pygame,settings,self.column1,self.row4)
                                    self.flags.add(onefour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_4 == 2:
                                    onefour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_4 -= 2
                            if self.flagnum == 0:
                                self.pad1_4 = 0
                        #feld 2_4
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad2_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_4 == 1:
                                    twofour= Flag(pygame,settings,self.column2,self.row4)
                                    self.flags.add(twofour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_4 == 2:
                                    twofour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_4 -= 2
                            if self.flagnum == 0:
                                self.pad2_4 = 0
                        #feld 3_4
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad3_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_4 == 1:
                                    threefour= Flag(pygame,settings,self.column3,self.row4)
                                    self.flags.add(threefour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_4 == 2:
                                    threefour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_4 -= 2
                            if self.flagnum == 0:
                                self.pad3_4 = 0
                        #feld 4_4
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad4_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_4 == 1:
                                    fourfour= Flag(pygame,settings,self.column4,self.row4)
                                    self.flags.add(fourfour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_4 == 2:
                                    fourfour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_4 -= 2
                            if self.flagnum == 0:
                                self.pad4_4 = 0
                        #feld 5_4
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad5_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_4 == 1:
                                    fivefour= Flag(pygame,settings,self.column5,self.row4)
                                    self.flags.add(fivefour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_4 == 2:
                                    fivefour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_4 -= 2
                            if self.flagnum == 0:
                                self.pad5_4 = 0
                        #feld 6_4
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad6_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_4 == 1:
                                    sixfour= Flag(pygame,settings,self.column6,self.row4)
                                    self.flags.add(sixfour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_4 == 2:
                                    sixfour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_4 -= 2
                            if self.flagnum == 0:
                                self.pad6_4 = 0
                        #feld 7_4
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad7_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_4 == 1:
                                    sevenfour= Flag(pygame,settings,self.column7,self.row4)
                                    self.flags.add(sevenfour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_4 == 2:
                                    sevenfour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_4 -= 2
                            if self.flagnum == 0:
                                self.pad7_4 = 0
                        #feld 8_4
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad8_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_4 == 1:
                                    eightfour= Flag(pygame,settings,self.column8,self.row4)
                                    self.flags.add(eightfour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_4 == 2:
                                    eightfour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_4 -= 2
                            if self.flagnum == 0:
                                self.pad8_4 = 0
                        #feld 9_4
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row4 <= self.mouse[1] <= self.row5:
                            self.pad9_4 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_4 == 1:
                                    ninefour= Flag(pygame,settings,self.column9,self.row4)
                                    self.flags.add(ninefour)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_4 == 2:
                                    ninefour.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_4 -= 2
                            if self.flagnum == 0:
                                self.pad9_4 = 0
                        #feld 1_5
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad1_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_5 == 1:
                                    onefive= Flag(pygame,settings,self.column1,self.row5)
                                    self.flags.add(onefive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_5 == 2:
                                    onefive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_5 -= 2
                            if self.flagnum == 0:
                                self.pad1_5 = 0
                        #feld 2_5
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad2_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_5 == 1:
                                    twofive= Flag(pygame,settings,self.column2,self.row5)
                                    self.flags.add(twofive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_5 == 2:
                                    twofive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_5 -= 2
                            if self.flagnum == 0:
                                self.pad2_5 = 0
                        #feld 3_5
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad3_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_5 == 1:
                                    threefive= Flag(pygame,settings,self.column3,self.row5)
                                    self.flags.add(threefive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_5 == 2:
                                    threefive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_5 -= 2
                            if self.flagnum == 0:
                                self.pad3_5 = 0
                        #feld 4_5
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad4_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_5 == 1:
                                    fourfive= Flag(pygame,settings,self.column4,self.row5)
                                    self.flags.add(fourfive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_5 == 2:
                                    fourfive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_5 -= 2
                            if self.flagnum == 0:
                                self.pad4_5 = 0
                        #feld 5_5
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad5_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_5 == 1:
                                    fivefive= Flag(pygame,settings,self.column5,self.row5)
                                    self.flags.add(fivefive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_5 == 2:
                                    fivefive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_5 -= 2
                            if self.flagnum == 0:
                                self.pad5_5 = 0
                        #feld 6_5
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad6_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_5 == 1:
                                    sixfive= Flag(pygame,settings,self.column6,self.row5)
                                    self.flags.add(sixfive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_5 == 2:
                                    sixfive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_5 -= 2
                            if self.flagnum == 0:
                                self.pad6_5 = 0
                        #feld 7_5
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad7_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_5 == 1:
                                    sevenfive= Flag(pygame,settings,self.column7,self.row5)
                                    self.flags.add(sevenfive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_5 == 2:
                                    sevenfive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_5 -= 2
                            if self.flagnum == 0:
                                self.pad7_5 = 0
                        #feld 8_5
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad8_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_5 == 1:
                                    eightfive= Flag(pygame,settings,self.column8,self.row5)
                                    self.flags.add(eightfive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_5 == 2:
                                    eightfive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_5 -= 2
                            if self.flagnum == 0:
                                self.pad8_5 = 0
                        #feld 9_5
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row5 <= self.mouse[1] <= self.row6:
                            self.pad9_5 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_5 == 1:
                                    ninefive= Flag(pygame,settings,self.column9,self.row5)
                                    self.flags.add(ninefive)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_5 == 2:
                                    ninefive.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_5 -= 2
                            if self.flagnum == 0:
                                self.pad9_5 = 0
                        #feld 1_6
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad1_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_6 == 1:
                                    onesix= Flag(pygame,settings,self.column1,self.row6)
                                    self.flags.add(onesix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_6 == 2:
                                    onesix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_6 -= 2
                            if self.flagnum == 0:
                                self.pad1_6 = 0
                        #feld 2_6
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad2_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_6 == 1:
                                    twosix= Flag(pygame,settings,self.column2,self.row6)
                                    self.flags.add(twosix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_6 == 2:
                                    twosix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_6 -= 2
                            if self.flagnum == 0:
                                self.pad2_6 = 0
                        #feld 3_6
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad3_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_6 == 1:
                                    threesix= Flag(pygame,settings,self.column3,self.row6)
                                    self.flags.add(threesix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_6 == 2:
                                    threesix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_6 -= 2
                            if self.flagnum == 0:
                                self.pad3_6 = 0
                        #feld 4_6
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad4_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_6 == 1:
                                    foursix= Flag(pygame,settings,self.column4,self.row6)
                                    self.flags.add(foursix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_6 == 2:
                                    foursix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_6 -= 2
                            if self.flagnum == 0:
                                self.pad4_6 = 0
                        #feld 5_6
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad5_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_6 == 1:
                                    fivesix= Flag(pygame,settings,self.column5,self.row6)
                                    self.flags.add(fivesix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_6 == 2:
                                    fivesix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_6 -= 2
                            if self.flagnum == 0:
                                self.pad5_6 = 0
                        #feld 6_6
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad6_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_6 == 1:
                                    sixsix= Flag(pygame,settings,self.column6,self.row6)
                                    self.flags.add(sixsix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_6 == 2:
                                    sixsix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_6 -= 2
                            if self.flagnum == 0:
                                self.pad6_6 = 0
                        #feld 7_6
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad7_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_6 == 1:
                                    sevensix= Flag(pygame,settings,self.column7,self.row6)
                                    self.flags.add(sevensix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_6 == 2:
                                    sevensix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_6 -= 2
                            if self.flagnum == 0:
                                self.pad7_6 = 0
                        #feld 8_6
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad8_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_6 == 1:
                                    eightsix= Flag(pygame,settings,self.column8,self.row6)
                                    self.flags.add(eightsix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_6 == 2:
                                    eightsix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_6 -= 2
                            if self.flagnum == 0:
                                self.pad8_6 = 0
                        #feld 9_6
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row6 <= self.mouse[1] <= self.row7:
                            self.pad9_6 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_6 == 1:
                                    ninesix= Flag(pygame,settings,self.column9,self.row6)
                                    self.flags.add(ninesix)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_6 == 2:
                                    ninesix.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_6 -= 2
                            if self.flagnum == 0:
                                self.pad9_6 = 0
                        #feld 1_7
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad1_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_7 == 1:
                                    oneseven= Flag(pygame,settings,self.column1,self.row7)
                                    self.flags.add(oneseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_7 == 2:
                                    oneseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_7 -= 2
                            if self.flagnum == 0:
                                self.pad1_7 = 0
                        #feld 2_7
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad2_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_7 == 1:
                                    twoseven= Flag(pygame,settings,self.column2,self.row7)
                                    self.flags.add(twoseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_7 == 2:
                                    twoseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_7 -= 2
                            if self.flagnum == 0:
                                self.pad2_7 = 0
                        #feld 3_7
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad3_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_7 == 1:
                                    threeseven= Flag(pygame,settings,self.column3,self.row7)
                                    self.flags.add(threeseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_7 == 2:
                                    threeseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_7 -= 2
                            if self.flagnum == 0:
                                self.pad3_7 = 0
                        #feld 4_7
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad4_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_7 == 1:
                                    fourseven= Flag(pygame,settings,self.column4,self.row7)
                                    self.flags.add(fourseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_7 == 2:
                                    fourseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_7 -= 2
                            if self.flagnum == 0:
                                self.pad4_7 = 0
                        #feld 5_7
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad5_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_7 == 1:
                                    fiveseven= Flag(pygame,settings,self.column5,self.row7)
                                    self.flags.add(fiveseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_7 == 2:
                                    fiveseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_7 -= 2
                            if self.flagnum == 0:
                                self.pad5_7 = 0
                        #feld 6_7
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad6_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_7 == 1:
                                    sixseven= Flag(pygame,settings,self.column6,self.row7)
                                    self.flags.add(sixseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_7 == 2:
                                    sixseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_7 -= 2
                            if self.flagnum == 0:
                                self.pad6_7 = 0
                        #feld 7_7
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad7_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_7 == 1:
                                    sevenseven= Flag(pygame,settings,self.column7,self.row7)
                                    self.flags.add(sevenseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_7 == 2:
                                    sevenseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_7 -= 2
                            if self.flagnum == 0:
                                self.pad7_7 = 0
                        #feld 8_7
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad8_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_7 == 1:
                                    eightseven= Flag(pygame,settings,self.column8,self.row7)
                                    self.flags.add(eightseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_7 == 2:
                                    eightseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_7 -= 2
                            if self.flagnum == 0:
                                self.pad8_7 = 0
                        #feld 9_7
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row7 <= self.mouse[1] <= self.row8:
                            self.pad9_7 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_7 == 1:
                                    nineseven= Flag(pygame,settings,self.column9,self.row7)
                                    self.flags.add(nineseven)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_7 == 2:
                                    nineseven.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_7 -= 2
                            if self.flagnum == 0:
                                self.pad9_7 = 0
                        #feld 1_8
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad1_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_8 == 1:
                                    oneeight= Flag(pygame,settings,self.column1,self.row8)
                                    self.flags.add(oneeight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_8 == 2:
                                    oneeight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_8 -= 2
                            if self.flagnum == 0:
                                self.pad1_8 = 0
                        #feld 2_8
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad2_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_8 == 1:
                                    twoeight= Flag(pygame,settings,self.column2,self.row8)
                                    self.flags.add(twoeight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_8 == 2:
                                    twoeight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_8 -= 2
                            if self.flagnum == 0:
                                self.pad2_8 = 0
                        #feld 3_8
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad3_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_8 == 1:
                                    threeeight= Flag(pygame,settings,self.column3,self.row8)
                                    self.flags.add(threeeight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_8 == 2:
                                    threeeight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_8 -= 2
                            if self.flagnum == 0:
                                self.pad3_8 = 0
                        #feld 4_8
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad4_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_8 == 1:
                                    foureight= Flag(pygame,settings,self.column4,self.row8)
                                    self.flags.add(foureight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_8 == 2:
                                    foureight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_8 -= 2
                            if self.flagnum == 0:
                                self.pad4_8 = 0
                        #feld 5_8
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad5_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_8 == 1:
                                    fiveeight= Flag(pygame,settings,self.column5,self.row8)
                                    self.flags.add(fiveeight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_8 == 2:
                                    fiveeight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_8 -= 2
                            if self.flagnum == 0:
                                self.pad5_8 = 0
                        #feld 6_8
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad6_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_8 == 1:
                                    sixeight= Flag(pygame,settings,self.column6,self.row8)
                                    self.flags.add(sixeight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_8 == 2:
                                    sixeight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_8 -= 2
                            if self.flagnum == 0:
                                self.pad6_8 = 0
                        #feld 7_8
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad7_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_8 == 1:
                                    seveneight= Flag(pygame,settings,self.column7,self.row8)
                                    self.flags.add(seveneight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_8 == 2:
                                    seveneight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_8 -= 2
                            if self.flagnum == 0:
                                self.pad7_8 = 0
                        #feld 8_8
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad8_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_8 == 1:
                                    eighteight= Flag(pygame,settings,self.column8,self.row8)
                                    self.flags.add(eighteight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_8 == 2:
                                    eighteight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_8 -= 2
                            if self.flagnum == 0:
                                self.pad8_8 = 0
                        #feld 9_8
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row8 <= self.mouse[1] <= self.row9:
                            self.pad9_8 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_8 == 1:
                                    nineeight= Flag(pygame,settings,self.column9,self.row8)
                                    self.flags.add(nineeight)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_8 == 2:
                                    nineeight.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_8 -= 2
                            if self.flagnum == 0:
                                self.pad9_8 = 0
                        #feld 1_9
                        if self.column1 <= self.mouse[0] <= self.column2 and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad1_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad1_9 == 1:
                                    onenine= Flag(pygame,settings,self.column1,self.row9)
                                    self.flags.add(onenine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad1_9 == 2:
                                    onenine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad1_9 -= 2
                            if self.flagnum == 0:
                                self.pad1_9 = 0
                        #feld 2_9
                        if self.column2 <= self.mouse[0] <= self.column3 and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad2_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad2_9 == 1:
                                    twonine= Flag(pygame,settings,self.column2,self.row9)
                                    self.flags.add(twonine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad2_9 == 2:
                                    twonine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad2_9 -= 2
                            if self.flagnum == 0:
                                self.pad2_9 = 0
                        #feld 3_9
                        if self.column3 <= self.mouse[0] <= self.column4 and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad3_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad3_9 == 1:
                                    threenine= Flag(pygame,settings,self.column3,self.row9)
                                    self.flags.add(threenine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad3_9 == 2:
                                    threenine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad3_9 -= 2
                            if self.flagnum == 0:
                                self.pad3_9 = 0
                        #feld 4_9
                        if self.column4 <= self.mouse[0] <= self.column5 and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad4_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad4_9 == 1:
                                    fournine= Flag(pygame,settings,self.column4,self.row9)
                                    self.flags.add(fournine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad4_9 == 2:
                                    fournine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad4_9 -= 2
                            if self.flagnum == 0:
                                self.pad4_9 = 0
                        #feld 5_9
                        if self.column5 <= self.mouse[0] <= self.column6 and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad5_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad5_9 == 1:
                                    fivenine= Flag(pygame,settings,self.column5,self.row9)
                                    self.flags.add(fivenine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad5_9 == 2:
                                    fivenine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad5_9 -= 2
                            if self.flagnum == 0:
                                self.pad5_9 = 0
                        #feld 6_9
                        if self.column6 <= self.mouse[0] <= self.column7 and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad6_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad6_9 == 1:
                                    sixnine= Flag(pygame,settings,self.column6,self.row9)
                                    self.flags.add(sixnine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad6_9 == 2:
                                    sixnine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad6_9 -= 2
                            if self.flagnum == 0:
                                self.pad6_9 = 0
                        #feld 7_9
                        if self.column7 <= self.mouse[0] <= self.column8 and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad7_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad7_9 == 1:
                                    sevennine= Flag(pygame,settings,self.column7,self.row9)
                                    self.flags.add(sevennine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad7_9 == 2:
                                    sevennine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad7_9 -= 2
                            if self.flagnum == 0:
                                self.pad7_9 = 0
                        #feld 8_9
                        if self.column8 <= self.mouse[0] <= self.column9 and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad8_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad8_9 == 1:
                                    eightnine= Flag(pygame,settings,self.column8,self.row9)
                                    self.flags.add(eightnine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad8_9 == 2:
                                    eightnine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad8_9 -= 2
                            if self.flagnum == 0:
                                self.pad8_9 = 0
                        #feld 9_9
                        if self.column9 <= self.mouse[0] <= (self.column9+60) and self.row9 <= self.mouse[1] <= (self.row9+60):
                            self.pad9_9 += 1
                            if 0 < self.flagnum <= 6:
                                if self.pad9_9 == 1:
                                    ninenine= Flag(pygame,settings,self.column9,self.row9)
                                    self.flags.add(ninenine)
                                    self.flagnum -= 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                if self.pad9_9 == 2:
                                    ninenine.kill()
                                    self.flagnum += 1
                                    self.textflag = self.font.render(str(self.flagnum), True, self.red)
                                    self.pad9_9 -= 2
                            if self.flagnum == 0:
                                self.pad9_9 = 0
                        #zählt nicht richtig
                        for boom in self.bombs:
                            if pygame.sprite.spritecollide(boom,self.flags,False):
                                self.winnumb += 1

      #      if self.winnumb == 6:
       #         self.textwin = self.font3.render("YOU WIN",True, self.red)   

            if self.lose == False:        
                self.draw()
                self.update()   

            if self.lose == True:
                self.textgameover = self.font2.render("GAME OVER",True, self.red)   
                self.loose() 
                self.update()                                          


    def update(self):
        self.pygame.display.flip()

    def loose(self):
        self.bombs.draw(self.screen)
        self.screen.blit(self.textgameover, self.textRectgameover.center)

    def draw(self):
        pygame.draw.rect(self.screen,self.black,(30,40,80,50),0) #Feld hinter sekunden
        self.screen.blit(self.textsec, self.textRectsec.center)
        pygame.draw.rect(self.screen,self.black,(490,40,80,50),0) #Feld hinter flagenanzahl
        self.screen.blit(self.textflag, self.textRectflag.center)
        self.table.grid(self.screen)
        self.bombs.draw(self.screen)
        self.all_boxes.draw(self.screen)
        self.flags.draw(self.screen)
       # self.screen.blit(self.textwin, self.textRectwin.center)

   

if __name__ == '__main__':                         
    settings = Settings()               # Fenstereinstellungen, pygame initialisieren, Spiel Objekt,                 
                                        # Hauptschleife des Spiels, und Ende des Programms
    pygame.init()                                    

    game = Game(pygame, settings)                      

    game.run()                
  
    pygame.quit()   
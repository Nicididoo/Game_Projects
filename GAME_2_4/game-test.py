import pygame
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN, MOUSEBUTTONUP)
import os
from random import *
pygame.mixer.init()

class Settings(object):                                                             #Programm Fenster
    def __init__(self):
        self.width = 800                                                   
        self.height = 700                                                   
        self.fps = 60                                                       
        self.title = "Pop the Bubble"                                          
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.softpop= pygame.mixer.Sound(os.path.join(self.app_path,"softpop.wav"))         #sounds
        self.pop= pygame.mixer.Sound(os.path.join(
                    self.app_path,"pop.wav"))
        self.blow= pygame.mixer.Sound(os.path.join(
                    self.app_path,'blow.wav'))       
        self.blowloud= pygame.mixer.Sound.set_volume(self.blow,0.1)        

    def size(self):                                                                  
        return (self.width, self.height)   

class Points():                                                                     # Bild worauf Punkte stehen werden
    def __init__(self, settings):
        self.settings= settings
        self.image = pygame.image.load(os.path.join(
                    self.settings.app_path, "scoreboard.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 50))

class Player(pygame.sprite.Sprite):                                                  # Sprite mit Maus position; Spieler
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(
                    self.settings.app_path, "cursor-1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.mask.Mask.get_rect(self.mask)
        self.rect.left, self.rect.top = pygame.mouse.get_pos()

    def update(self):                                                               # Update der Maus position
        self.rect.left, self.rect.top = pygame.mouse.get_pos()


class Bubble(pygame.sprite.Sprite):                                                 # Blasen(Gegner); Sprite an zufälliger Stelle
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.size= 10
        self.image = pygame.image.load(os.path.join(
                    self.settings.app_path, "bubblebubble.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.mask.Mask.get_rect(self.mask)
        self.rect.left = randint(110,self.settings.width-110-self.size)
        self.rect.top = randint(110,self.settings.height-110-self.size)
        self.grow = randint(1,4)

    def update(self):                                                               # Sprite wird größer
        if self.size < 221:
            center = self.rect.center
            self.size += self.grow
            self.image = pygame.image.load(os.path.join(
                        self.settings.app_path, "bubblebubble.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.mask.Mask.get_rect(self.mask)
            self.rect.center = center

    def newupdate(self):                                                        #neues Update für Blase nachdem anklicken
        self.size = 10
        self.rect.left = randint(110,self.settings.width-110-self.size)
        self.rect.top = randint(110,self.settings.height-110-self.size)
        if self.size < 221:
            center = self.rect.center
            self.size += self.grow
            self.image = pygame.image.load(os.path.join(
                        self.settings.app_path, "bubblebubble.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.mask.Mask.get_rect(self.mask)
            self.rect.center = center




class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame                                                          #Hintergrund
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.size())                                      
        self.pygame.display.set_caption(self.settings.title)                                                      
        self.background = self.pygame.image.load(os.path.join(
                        self.settings.app_path, "jellyfish_field.png")).convert()
        self.background = pygame.transform.scale(self.background, (800, 700))                            
        self.background_rect = self.background.get_rect()

        self.player = Player(settings)                                              # Objekte mit festen Koordinaten
        self.points = Points(settings)
        
        self.b1 = Bubble(self.settings)                                         #festgelegte Blasen
        self.b2 = Bubble(self.settings)
        self.b3 = Bubble(self.settings)
        self.b4 = Bubble(self.settings)
        self.b5 = Bubble(self.settings)
        self.b6 = Bubble(self.settings)
        self.b7 = Bubble(self.settings)
        self.b8 = Bubble(self.settings)

        self.pointscolor = [255,255,255]                                            # Einstellungen zur Punkte Anzeige
        self.pointsadd = 0
        self.font = pygame.font.Font(None, 35)                                                        
        self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)                     
        self.textRect = self.text.get_rect()                                                            
        self.textRect.center = 15, 18 

        self.clock = pygame.time.Clock()                                            # Zeit und boolean für Programm
        self.done = False

        self.bubblecount = 0                                                        # variabeln für das erstellen von Blasen

        pygame.mouse.set_visible(False)                                             # durchsichtige Maus, damit nur Sprite da ist 

        self.all_bubbles = pygame.sprite.Group()                                    # Sprite Gruppen für "Gegner" & "Spieler"
        self.the_mouse = pygame.sprite.Group()

        self.the_mouse.add(self.player)                                             # "Spieler" Objekt in der Gruppe


        self.ticks = pygame.time.get_ticks()                                        # zeit variabeln für die Zeit berechnung
        self.numb= 0
        self.spawn= ((pygame.time.get_ticks()-self.ticks)/1000) +self.numb

  #      self.softpop= pygame.mixer.Sound("softpop.wav")
   #     self.pop= pygame.mixer.Sound("pop.wav")
    #    self.blow= pygame.mixer.Sound('blow.wav')


    def pointcalc(self,bubblesize):                                                 #Punkteberechnung nach Größe der Blase
        self.bubblesize= bubblesize
        if self.bubblesize < 51:
            self.pointsadd += 10
            self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)
        if self.bubblesize > 50 and self.bubblesize < 101:
            self.pointsadd += 20
            self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)
        if self.bubblesize > 100 and self.bubblesize < 151:
            self.pointsadd += 50
            self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)
        if self.bubblesize > 150:
            self.pointsadd += 100
            self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)
    
    def run(self):                                                                  # Hauptprogrammschleife
        while not self.done:                         
            self.clock.tick(self.settings.fps)                              # zeit variabeln
            self.timef= (pygame.time.get_ticks()-self.ticks)/1000
            self.time= round(self.timef, 1)      
            for event in self.pygame.event.get():       
                if event.type == QUIT:                                              # Funktionen zum schließen des Programmes
                    self.done = True                 
                elif event.type == KEYDOWN:            
                    if event.key == K_ESCAPE:
                        self.done = True


                touchbubble= pygame.sprite.spritecollide(self.player, self.all_bubbles, False)          # ganz viele kollisionen
                touchb1= pygame.sprite.collide_mask(self.player, self.b1)
                touchb2= pygame.sprite.collide_mask(self.player, self.b2)
                touchb3= pygame.sprite.collide_mask(self.player, self.b3)
                touchb4= pygame.sprite.collide_mask(self.player, self.b4)
                touchb5= pygame.sprite.collide_mask(self.player, self.b5)
                touchb6= pygame.sprite.collide_mask(self.player, self.b6)
                touchb7= pygame.sprite.collide_mask(self.player, self.b7)
                touchb8= pygame.sprite.collide_mask(self.player, self.b8)  
                b1b2= pygame.sprite.collide_mask(self.b1, self.b2)
                b1b3= pygame.sprite.collide_mask(self.b1, self.b3)
                b1b4= pygame.sprite.collide_mask(self.b1, self.b4)
                b1b5= pygame.sprite.collide_mask(self.b1, self.b5)
                b1b6= pygame.sprite.collide_mask(self.b1, self.b6)
                b1b7= pygame.sprite.collide_mask(self.b1, self.b7)
                b1b8= pygame.sprite.collide_mask(self.b1, self.b8)
                b2b3= pygame.sprite.collide_mask(self.b2, self.b3)
                b2b4= pygame.sprite.collide_mask(self.b2, self.b4)
                b2b5= pygame.sprite.collide_mask(self.b2, self.b5)
                b2b6= pygame.sprite.collide_mask(self.b2, self.b6)
                b2b7= pygame.sprite.collide_mask(self.b2, self.b7)
                b2b8= pygame.sprite.collide_mask(self.b2, self.b8)
                b3b4= pygame.sprite.collide_mask(self.b3, self.b4)
                b3b5= pygame.sprite.collide_mask(self.b3, self.b5)
                b3b6= pygame.sprite.collide_mask(self.b3, self.b6)
                b3b7= pygame.sprite.collide_mask(self.b3, self.b7)
                b3b8= pygame.sprite.collide_mask(self.b3, self.b8)
                b4b5= pygame.sprite.collide_mask(self.b4, self.b5)
                b4b6= pygame.sprite.collide_mask(self.b4, self.b6)
                b4b7= pygame.sprite.collide_mask(self.b4, self.b7)
                b4b8= pygame.sprite.collide_mask(self.b4, self.b8)
                b5b6= pygame.sprite.collide_mask(self.b5, self.b6)
                b5b7= pygame.sprite.collide_mask(self.b5, self.b7)
                b5b8= pygame.sprite.collide_mask(self.b5, self.b8)
                b6b7= pygame.sprite.collide_mask(self.b6, self.b7)
                b6b8= pygame.sprite.collide_mask(self.b6, self.b8)
                b7b8= pygame.sprite.collide_mask(self.b7, self.b8)
                bubbletouch= [b1b2,b1b3,b1b4,b1b5,b1b6,b1b7,b1b8,b2b3,b2b4,b2b5,b2b6,b2b7,b2b8,
                b3b4,b3b5,b3b6,b3b7,b3b8,b4b5,b4b6,b4b7,b4b8,b5b6,b5b7,b5b8,b6b7,b6b8,b7b8]

                                                                                                        #Kollisionsabfragen ; cursor und klicken

                if touchb1 or touchb2 or touchb3 or touchb4 or touchb5 or touchb6 or touchb7 or touchb8:                  
                    self.player.image = pygame.image.load(os.path.join(
                                        self.settings.app_path, "cursor-2.png")).convert_alpha()
                    self.player.image = pygame.transform.scale(self.player.image, (45, 40))
                else:
                    self.player.image = pygame.image.load(os.path.join(
                                        self.settings.app_path, "cursor-1.png")).convert_alpha()
                    self.player.image = pygame.transform.scale(self.player.image, (45, 40))
                
                if event.type == MOUSEBUTTONDOWN and touchb1:  
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True)
                    self.pointcalc(self.b1.size)
                    self.bubblecount -= 1
                    self.b1.newupdate()
                if event.type == MOUSEBUTTONDOWN and touchb2:
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True) 
                    self.pointcalc(self.b2.size) 
                    self.bubblecount -= 1
                    self.b2.newupdate()
                if event.type == MOUSEBUTTONDOWN and touchb3: 
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True) 
                    self.pointcalc(self.b3.size)
                    self.bubblecount -= 1
                    self.b3.newupdate()
                if event.type == MOUSEBUTTONDOWN and touchb4: 
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True) 
                    self.pointcalc(self.b4.size)
                    self.bubblecount -= 1
                    self.b4.newupdate()
                if event.type == MOUSEBUTTONDOWN and touchb5: 
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True)
                    self.pointcalc(self.b5.size)
                    self.bubblecount -= 1
                    self.b5.newupdate()  
                if event.type == MOUSEBUTTONDOWN and touchb6: 
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True) 
                    self.pointcalc(self.b6.size)
                    self.bubblecount -= 1
                    self.b6.newupdate()  
                if event.type == MOUSEBUTTONDOWN and touchb7: 
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True)
                    self.pointcalc(self.b7.size)
                    self.bubblecount -= 1
                    self.b7.newupdate()
                if event.type == MOUSEBUTTONDOWN and touchb8: 
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True)
                    self.pointcalc(self.b8.size)
                    self.bubblecount -= 1
                    self.b8.newupdate()


            self.update()                                                 
            self.draw()  
                                               
 
    def draw(self):                                                         # hintergrund, blasen, spieler, punkte "malen"
        self.screen.blit(self.background, self.background_rect)
        self.all_bubbles.draw(self.screen)
        self.screen.blit(self.points.image,(5,5))
        self.screen.blit(self.text, self.textRect.center)
        self.the_mouse.draw(self.screen)
        self.pygame.display.flip()                                

    def update(self):                                       # "schwierigkeit",mehr blasen,wachsende blasen,spieler position updaten
        self.spawnbubbles() 
        self.all_bubbles.update() 
        self.the_mouse.update()

    def spawnbubbles(self):                             # 8 blasen hinzufügen
        self.faster() 
        if self.bubblecount < 9 :              
            if self.time == self.spawn:
                self.bubblecount += 1
                if self.bubblecount == 1:
                    self.all_bubbles.add(self.b1)
                    self.spawn += self.numb
                if self.bubblecount == 2:
                    self.all_bubbles.add(self.b2)
                    self.spawn += self.numb
                if self.bubblecount == 3:
                    self.all_bubbles.add(self.b3)
                    self.spawn += self.numb
                if self.bubblecount == 4:
                    self.all_bubbles.add(self.b4)
                    self.spawn += self.numb
                if self.bubblecount == 5:
                    self.all_bubbles.add(self.b5)
                    self.spawn += self.numb
                if self.bubblecount == 6:
                    self.all_bubbles.add(self.b6)
                    self.spawn += self.numb
                if self.bubblecount == 7:
                    self.all_bubbles.add(self.b7)
                    self.spawn += self.numb
                if self.bubblecount == 8:
                    self.all_bubbles.add(self.b8)
                    self.spawn += self.numb
        else:
            if self.time == self.spawn:
                self.spawn += self.numb

    def faster(self):                                    #schnelleres spawnen jede 20 sek
        if self.time < 21:
            self.numb= 1
        if self.time > 20 and self.time < 41:
            self.numb= 0.8 
            self.spawn= round(self.spawn,1)
        if self.time > 40 and self.time < 61:
            self.numb= 0.6  
            self.spawn= round(self.spawn,1)
        if self.time > 60 and self.time < 81:
            self.numb= 0.4
            self.spawn= round(self.spawn,1)
        if self.time > 80:
            self.numb= 0.2 
            self.spawn= round(self.spawn,1)
         
        


if __name__ == '__main__':                         
    settings = Settings()               # Fenstereinstellungen, pygame initialisieren, Spiel Objekt,                 
                                        # Hauptschleife des Spiels, und Ende des Programms
    pygame.init()                                    

    game = Game(pygame, settings)                      

    game.run()                
  
    pygame.quit()             


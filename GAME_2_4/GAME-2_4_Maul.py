import pygame
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, K_p)
import os
from random import *
from math import *
pygame.mixer.init()


class Settings(object):                                                             #Programm Fenster
    def __init__(self):
        self.width = 800                                                   
        self.height = 700                                                   
        self.fps = 60                                                       
        self.title = "Pop the Bubble"                                          
        self.app_path = os.path.dirname(os.path.abspath(__file__)) 
        self.softpop= pygame.mixer.Sound(os.path.join(self.app_path,"softpop.wav"))     #sounds
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
        self.rect.right= self.rect.left + self.size
        self.rect.bottom= self.rect.top + self.size
        self.grow = randint(1,4)

    def gone(self):                                                         #blase löschen mit sound
        pygame.mixer.Sound.play(self.settings.softpop)
        self.kill()

    def update(self):                                                       #wachsen der Blase
        if self.size < 221:
            center = self.rect.center
            self.size += self.grow
            self.image = pygame.image.load(os.path.join(
                        self.settings.app_path, "bubblebubble.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.mask.Mask.get_rect(self.mask)
            self.rect.center = center


    def newpos(self):                                                       # neue position
        self.rect.left = randint(110,self.settings.width-110-self.size)
        self.rect.top = randint(110,self.settings.height-110-self.size)

    def pointcalc(self):                                            # Punkteberechnung nach blasen Größe
        points= 0
        if self.size < 51:
            points= 10
        if self.size > 50 and self.size < 101:
            points= 20
        if self.size > 100 and self.size < 151:
            points= 50
        if self.size > 150:
            points= 100
        return points

class PauseMenu():                                              # Versuch von einem Pausenmenü
    def __init__(self,pygame,settings):
        self.pygame= pygame
        self.settings= settings
        self.screen = pygame.display.set_mode(settings.size())
        self.spongebob= self.pygame.image.load(os.path.join(
                        self.settings.app_path, "spongebob.png")).convert()
        self.spongebob= pygame.transform.scale(self.spongebob, (60, 80))  
        self.patrick= self.pygame.image.load(os.path.join(
                        self.settings.app_path, "patrick.png")).convert()
        self.patrick= pygame.transform.scale(self.patrick, (70, 80))
        self.color= (50,50,50,100)
        self.see_through= pygame.Surface((800,700)).convert_alpha()
        self.see_through.fill(self.color)

    def pause(self):                                        # wäre die update/draw funktion
        pygame.mixer.music.stop()
        self.screen.blit(self.see_through,(0,0))
        self.screen.blit(self.spongebob,(0,740))
        self.screen.blit(self.patrick, (630,740))
        pygame.display.flip()



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
        self.pausem= PauseMenu(pygame,settings)
        
        self.pointscolor = [255,255,255]                                            # Einstellungen zur Punkte Anzeige
        self.pointsadd = 0
        self.font = pygame.font.Font(None, 35)                                                        
        self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)                     
        self.textRect = self.text.get_rect()                                                            
        self.textRect.center = 15, 18 

        self.clock = pygame.time.Clock()                                            # Zeit und boolean für Programm
        self.done = False

        self.paused= False                                                          # wäre boolean für Pause

        self.bubblecount = 0                                                        # variabeln für das erstellen von Blasen

        pygame.mouse.set_visible(False)                                             # durchsichtige Maus, damit nur Sprite da ist 

        self.all_bubbles = pygame.sprite.Group()                                    # Sprite Gruppen für "Gegner" & "Spieler"
        self.the_mouse = pygame.sprite.Group()

        self.the_mouse.add(self.player)                                             # "Spieler" Objekt in der Gruppe



        self.ticks = pygame.time.get_ticks()                                        # zeit variabeln für die Zeit berechnung
        self.numb= 0
        self.spawn= ((pygame.time.get_ticks()-self.ticks)/1000) +self.numb


    def events(self):
        for event in self.pygame.event.get():       
            if event.type == QUIT:                                              # Funktionen zum schließen des Programmes
                self.done = True                 
            elif event.type == KEYDOWN:  
                if event.key == K_p:
                    self.paused= not self.paused                        # jedesmal p klicken ändert bollean
                    print(self.paused)
                if event.key == K_ESCAPE:
                    self.done = True

                                                                                                        #kollisionsabfrage; cursor und klicken
            touchbubble= pygame.sprite.spritecollide(self.player, self.all_bubbles, False)     

            if touchbubble:                                                                   
                self.player.image = pygame.image.load(os.path.join(
                                        self.settings.app_path, "cursor-2.png")).convert_alpha()
                self.player.image = pygame.transform.scale(self.player.image, (45, 40))
            if not touchbubble:
                self.player.image = pygame.image.load(os.path.join(
                                        self.settings.app_path, "cursor-1.png")).convert_alpha()
                self.player.image = pygame.transform.scale(self.player.image, (45, 40))

                
            if event.type == MOUSEBUTTONDOWN and touchbubble:               
                for s in touchbubble:
                    s.gone()
                    self.pointsadd += s.pointcalc()
                    self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)
                    self.bubblecount -= 1

    
    def run(self):                                                                  # Hauptprogrammschleife
        while not self.done:                         
            self.clock.tick(self.settings.fps)    
            self.timef= (pygame.time.get_ticks()-self.ticks)/1000
            self.time= round(self.timef, 1)  
            self.events()   
            
            if not self.paused:                                             # wenn p geglickt wird, updaten die blasen nicht mehr
                self.update() 
                self.draw() 

            if self.paused:
                self.pausem.pause()                         
                 

        self.gameover    # collison von bubbles fehlt zum ausführen                                             
 
    def draw(self):                                                         
        self.screen.blit(self.background, self.background_rect)
        self.all_bubbles.draw(self.screen)
        self.screen.blit(self.points.image,(5,5))
        self.screen.blit(self.text, self.textRect.center)
        self.the_mouse.draw(self.screen)
        self.pygame.display.flip()                                

    def update(self):                                       
        self.bubbles() 
        self.all_bubbles.update() 
        self.the_mouse.update()


    def bubbles(self):                               # erstellen der Blasen  
        self.faster()
        if self.bubblecount < 8:
            if self.time == self.spawn:
                b= Bubble(settings)
                if pygame.sprite.spritecollide(b, self.all_bubbles,False):
                    b.newpos()
                else:
                    pygame.mixer.Sound.play(self.settings.blow)
                    self.all_bubbles.add(b)
                    self.bubblecount += 1
                    self.spawn += self.numb
                    #if pygame.sprite.spritecollide(b, self.all_bubbles,False):
                     #   funktioniert nicht ganz
        else:
            if self.time == self.spawn:
                self.spawn += self.numb


    def faster(self):                                      # schnelleres spawnen jede 10 sek
        if self.time < 11:
            self.numb= 1
        if self.time > 10 and self.time < 21:
            self.numb= 0.8 
            self.spawn= round(self.spawn,1)
        if self.time > 20 and self.time < 31:
            self.numb= 0.6  
            self.spawn= round(self.spawn,1)
        if self.time > 30 and self.time < 41:
            self.numb= 0.4
            self.spawn= round(self.spawn,1)
        if self.time > 40:
            self.numb= 0.2 
            self.spawn= round(self.spawn,1)

    def gameover(self):                                                                 # nicht benutzter versuch für das game over
        self.gobackground = self.pygame.image.load(os.path.join(
                        self.settings.app_path, "squidward_screaming.png")).convert()
        self.gobackground= pygame.transform.scale(self.gobackground, (800, 700))                            
        self.gobackground_rect = self.background.get_rect()
        self.screen.blit(self.gobackground, self.gobackground_rect)
        pygame.display.flip()

if __name__ == '__main__':                         
    settings = Settings()               # Fenstereinstellungen, pygame initialisieren, Spiel Objekt,                 
                                        # Hauptschleife des Spiels, und Ende des Programms
    pygame.init()                                    

    game = Game(pygame, settings)                      

    game.run()                
  
    pygame.quit()             

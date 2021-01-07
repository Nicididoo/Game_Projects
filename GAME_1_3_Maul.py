import pygame
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE)
import os
from random import *

class Settings(object):
    def __init__(self):
        self.width = 800                                                   
        self.height = 700                                                   
        self.fps = 60                                                       # 60 fps
        self.title = "Dodgeball"                                          
        self.image_path = os.path.dirname(os.path.abspath(__file__))        # Bilder in dem selben Ordner wie das Programm

    def size(self):                                                        
        return (self.width, self.height)   

class Player(pygame.sprite.Sprite):                                                                # Die Spieler Klasse
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)                                                     
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.image_path, "dodger.png")).convert_alpha()    
        self.image = pygame.transform.scale(self.image, (120, 80))                                               
        self.rect = self.image.get_rect()                                                                   
        self.rect.left = (settings.width - self.rect.width) // 2                                                
        self.rect.top = settings.height - self.rect.height - 10                                                 
        self.left_or_right = 0
        self.up_or_down = 0
        self.speed = 6

    def jump(self):                                                                                 # Spieler kann "springen"
        self.rect.left = randint(0,(settings.width - self.rect.width))
        self.rect.top = randint(0,(settings.height - self.rect.height))

    def update(self):                                                                            # die Bewegung des Spielers
        newleft = self.rect.left + (self.left_or_right * self.speed)
        newright = newleft + self.rect.width
        if newleft > 0 and newright < settings.width:
            self.rect.left = newleft
        newtop = self.rect.top + (self.up_or_down * self.speed)
        newbottom = newtop + self.rect.height
        if newtop > 0 and newbottom < settings.height:
            self.rect.top = newtop


class Ball(pygame.sprite.Sprite):                                                               # Die Hinderniss Klasse
    def __init__(self, settings, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(self.settings.image_path, "ball.png")).convert_alpha()
        self.scale= scale
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.right = self.rect.left + self.rect.width
        self.rect.top = 0
        self.rect.bottom = self.rect.top + self.rect.height
        self.right_or_left = 1
        self.up_or_down = 1
        self.speed = speed
        self.faster= 0.2

    def update(self):                                                       #Bewegung der Hindernisse mit Verschnellerung
        newtop = self.rect.top + (self.up_or_down * self.speed)
        newbottom = self.rect.bottom + (self.up_or_down * self.speed)
        if newtop > (settings.height + self.rect.height):
            self.rect.top = 0 - self.rect.height
            self.rect.left = randint(1,750)
            self.speed += self.faster
        self.rect.top += (self.up_or_down * self.speed)
        if self.speed == 15:
            self.faster= 0

class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.size())                                      
        self.pygame.display.set_caption(self.settings.title)                                                      
        self.background = self.pygame.image.load(os.path.join(self.settings.image_path, "dodgefield.png")).convert()
        self.background = pygame.transform.scale(self.background, (800, 700))                             # Hintergrundbild wird angepasst
        self.background_rect = self.background.get_rect()
        self.player = Player(settings)                                                                      # Player Objekt wird erstellt
        self.ball1 = Ball(settings,60,2)
        self.ball2 = Ball(settings,75,3)
        self.ball3 = Ball(settings,90,4)
        self.pointscolor= [0,0,0]                                                                       #   Punkte Anzeige Kriterien
        self.pointszahl= 0                                                                              #   ...
        self.font = pygame.font.Font(None, 70)                                                          #   ...
        self.text = self.font.render(str(self.pointszahl), True, self.pointscolor)                      #   ...
        self.textRect = self.text.get_rect()                                                            #   ... 
        self.textRect.center = 10, 1                                                                    #   ...
        self.clock = pygame.time.Clock()
        self.done = False

        self.the_player = pygame.sprite.Group()              # Player Sprite Gruppe
        self.the_player.add(self.player)

        self.all_balls = pygame.sprite.Group()              # Bälle Sprite Gruppe
        self.all_balls.add(self.ball1)
        self.all_balls.add(self.ball2)
        self.all_balls.add(self.ball3)

    def score(self):                                                                    #nicht funktionierende Punkterhöhung
        if self.ball1.rect.top > (settings.height + self.ball1.rect.height):
            self.pointszahl += 1
            self.text = self.font.render(str(self.pointszahl), True, self.pointscolor)
        if self.ball2.rect.top > (settings.height + self.ball2.rect.height):
            self.pointszahl += 1
            self.text = self.font.render(str(self.pointszahl), True, self.pointscolor)
        if self.ball3.rect.top > (settings.height + self.ball3.rect.height):
            self.pointszahl += 1
            self.text = self.font.render(str(self.pointszahl), True, self.pointscolor)

    def run(self):
        while not self.done:                            # Hauptprogrammschleife   
            self.clock.tick(self.settings.fps)         
            for event in self.pygame.event.get():       
                if event.type == QUIT:                  # Wenn das X am Fenster geklickt, wird programm geschlossen
                    self.done = True                 
                elif event.type == KEYDOWN:            
                    if event.key == K_ESCAPE:
                        self.done = True
                    if event.key == K_LEFT:             # Nach links bewegen
                        self.player.left_or_right = -1
                    if event.key == K_RIGHT:            # Nach rechts bewegen
                        self.player.left_or_right = 1
                    if event.key == K_UP:               # Nach oben bewegen
                        self.player.up_or_down = -1
                    if event.key == K_DOWN:             # Nach unten bewegen
                        self.player.up_or_down = 1
                elif event.type == KEYUP:              
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        self.player.left_or_right = 0
                    if event.key == K_UP or event.key == K_DOWN:
                        self.player.up_or_down = 0
                    if event.key == K_SPACE:            # Spieler springt zu einer anderen position
                        self.player.jump()

            colision= pygame.sprite.spritecollide(self.player, self.all_balls, False)               # Kollision, schließt das Spiel, Game over
            if colision:
                self.done = True
        
            self.update()                               
            self.draw()                                
 
    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.screen.blit(self.text, self.textRect.center)
        self.the_player.draw(self.screen)                           
        self.all_balls.draw(self.screen)
        self.pygame.display.flip()                                

    def update(self):                                 
        self.the_player.update()
        self.all_balls.update()
        self.score()


if __name__ == '__main__':                                    
    settings = Settings()                               # Die Einstellungen des Fensters

    pygame.init()                                       # Pygame Module verfügbar gestellt

    game = Game(pygame, settings)                       # Spiel Objekt

    game.run()                                          # Die Spiel Hauptschleife; das Spiel ablaufen
  
    pygame.quit()                                       # beendet pygame


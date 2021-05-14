import pygame
import os
import random
import math
pygame.init()

szer = 600
wys = 600

screen = pygame.display.set_mode((szer, wys))           # tworzenie okna



def write(text, x, y, size):
    #cz = pygame.font.Font(pygame.font.get_default_font(), size)
    cz = pygame.font.SysFont('Arial', size)          # czcionka
    rend = cz.render(text, 1, (255, 100, 100))         # wygładzenie i kolor tekstu
    #x = (szer - rend.get_rect().width)/2                # wyśrodkowanie w osi x
    #y = (wys - rend.get_rect().height)/2                # wyśrodkowanie w osi y
    screen.blit(rend, (x, y))                           # wstawianie tekstu w odpowiednim miejscu

show = 'menu'

# Tworzenie przeszkód, definicja klasy

class obstacle(): # tworzenie przeszkód - prostokątów u góry i dołu
    def __init__(self, x, width): # tworzenie konstruktora klasy, self - odnoszenie się do samego siebie
        self.x = x
        self.width = width
        self.y_up = 0           # definiowanie wymiarów prostokątów (jeden obiekt jako dwa prostokąty góra-dół)
        self.height_up = random.randint(150,250)
        self.space = 200
        self.y_down = self.height_up + self.space
        self.height_down = wys - self.y_down
        self.color = (20, 0, 20)
        #self.color = (160, 140, 190)
        self.shape_up = pygame.Rect(self.x, self.y_up, self.width, self.height_up)
        self.shape_down = pygame.Rect(self.x, self.y_down, self.width, self.height_down)
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.shape_up, 0)
        pygame.draw.rect(screen, self.color, self.shape_down, 0)
        
    def motion(self, v):
        self.x -= v
        self.shape_up = pygame.Rect(self.x, self.y_up, self.width, self.height_up)
        self.shape_down = pygame.Rect(self.x, self.y_down, self.width, self.height_down)
        
    def colision(self, player):
        if self.shape_up.colliderect(player) or self.shape_down.colliderect(player):
            return True
        else:
            return False
        

class helicopter():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 30
        self.width = 50
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)
        self.graphic = pygame.image.load(os.path.join('helicopter.png'))
        
    def draw(self):
        screen.blit(self.graphic, (self.x, self.y))
        
    def motion(self, v):
        self.y += v
        self.shape = pygame.Rect(self.x, self.y, self.width, self.height)


        

obstacles = []
for i in range(21):
    obstacles.append(obstacle(i*szer/20, szer/20))


player = helicopter(250, 275)

dy = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -0.1
                
            if event.key == pygame.K_DOWN:
                dy = 0.1
                
            if event.key == pygame.K_SPACE:
                if show != 'gameplay':
                    player = helicopter(250, 275)
                    dy = 0
                    show = 'gameplay'
                    points = 0
    
    screen.fill((0, 0, 0))
    
    
    
    if show == 'menu':
        write('Press space to start.', 80, 450, 20)
        hel = pygame.image.load(os.path.join('menuhel.png')) # Wczytywanie i ładowanie obrazków
        cap = pygame.image.load(os.path.join('menunapis.png'))
        screen.blit(cap, (40, 30))
        screen.blit(hel, (125, 200))
        
    elif show == 'gameplay':
        screen.fill((0, 120, 255))
        for j in obstacles:
            j.motion(0.5)   # prędkosć przeszkód
            j.draw()
            
            if j.colision(player.shape):
                show = 'end'
            
        for j in obstacles:
            if j.x <= -j.width:
                obstacles.remove(j)
                obstacles.append((obstacle(szer, szer/20)))
                points += math.fabs(dy)
        
        player.draw()
        player.motion(dy)
        write('Score: ' + str(int(points)), 50, 50, 20)
        
    
    elif show == 'end':
        write('Press space to try again.', 80, 500, 20)
        hel = pygame.image.load(os.path.join('menuhel.png')) # Wczytywanie i ładowanie obrazków
        cap = pygame.image.load(os.path.join('menunapis.png'))
        screen.blit(cap, (40, 30))
        screen.blit(hel, (125, 200))
        write('You lost :(', 80, 400, 20)
        write('Your score: ' + str(int(points)), 80, 450, 20)
        
        
    pygame.display.update()

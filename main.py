import pygame
from sys import exit 
import random

GAME_WIDTH = 750
GAME_HEIGHT = 250

class Block(pygame.Rect):
    def __init__(self, coordinates, size, image):
        super().__init__(coordinates, size)
        self.image = image
        self.velocity_x = 0
        self.velocity_y = 0

#images
DINO_IMAGE = pygame.transform.scale(pygame.image.load("images/dino.png"), (88, 94))
DINO_DEAD_IMAGE = pygame.transform.scale(pygame.image.load("images/dino-dead.png"), (88, 94))
CACTUS1_IMAGE = pygame.transform.scale(pygame.image.load("images/cactus1.png"), (34, 70))
CACTUS2_IMAGE = pygame.transform.scale(pygame.image.load("images/cactus2.png"), (69, 70))
CACTUS3_IMAGE = pygame.transform.scale(pygame.image.load("images/cactus3.png"), (102, 70))
CACTUS_IMAGES = [CACTUS1_IMAGE, CACTUS2_IMAGE, CACTUS3_IMAGE]

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT)) #game window
pygame.display.set_caption("Adventurer Dino") #title
clock = pygame.time.Clock()
GAME_FONT = pygame.font.SysFont("Courier", 20)

VELOCITY_X = -8
VELOCITY_Y = -10
GRAVITY = 0.4

dino = Block((50, GAME_HEIGHT-DINO_IMAGE.height), DINO_IMAGE.get_size(), DINO_IMAGE)
cactus_list = []
last_place_cactus_time = 0
game_over = False
score = 0

def place_cactus():
    random_cactus_image = random.choice(CACTUS_IMAGES)
    random_cactus = Block((GAME_WIDTH, GAME_HEIGHT - random_cactus_image.height),
                          random_cactus_image.get_size(),
                          random_cactus_image)
    random_cactus.velocity_x = VELOCITY_X
    cactus_list.append(random_cactus)

def move():
    global cactus_list, game_over, score
    score += 1
    
    dino.velocity_y += GRAVITY
    dino.y += dino.velocity_y
    if dino.y >= GAME_HEIGHT - dino.height:
        dino.y = GAME_HEIGHT - dino.height
    
    for cactus in cactus_list:
        cactus.x += cactus.velocity_x
        if dino.colliderect(cactus):
            game_over = True
            dino.image = DINO_DEAD_IMAGE
    
    cactus_list = [cactus for cactus in cactus_list if cactus.x + cactus.width > 0]

def draw():
    window.fill("light blue")
    window.blit(dino.image, dino)
    
    for cactus in cactus_list:
        window.blit(cactus.image, cactus)
    
    text_render = GAME_FONT.render(str(score), True, "black")
    window.blit(text_render, (5, 20))

#game loop
while True:
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:       
            pygame.quit()
            exit()        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    cactus_list.clear()
                    game_over = False
                    score = 0
                    dino.y = GAME_HEIGHT - dino.height
                    dino.velocity_y = 0
                    dino.image = DINO_IMAGE
                
                elif dino.y >= GAME_HEIGHT - dino.height:
                    dino.velocity_y = VELOCITY_Y

    now = pygame.time.get_ticks()
    if now - last_place_cactus_time >= 1000:
        place_cactus()
        last_place_cactus_time = now
    
    if not game_over:
        move()
        draw()
        pygame.display.update()                     #refresh game window
        clock.tick(60)                              #60 fps

import pygame
from sys import exit 
import random
import time
import os
import sys

GAME_WIDTH = 750
GAME_HEIGHT = 250

#Pyinstaller Asset Helper
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    return os.path.join(base_path, relative_path)

class Block(pygame.Rect):
    def __init__(self, coordinates, size, image):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.width = size[0]
        self.height = size[1]
        self.image = image
        self.velocity_x = 0
        self.velocity_y = 0

#images
DINO_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/dino.png")), (88, 94))
DINO_DEAD_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/dino-dead.png")), (88, 94))
CACTUS1_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/cactus1.png")), (34, 70))
CACTUS2_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/cactus2.png")), (69, 70))
CACTUS3_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/cactus3.png")), (102, 70))
CACTUS_IMAGES = [CACTUS1_IMAGE, CACTUS2_IMAGE, CACTUS3_IMAGE]
GAME_OVER_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/game-over.png")), (300, 200))
RESET_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/reset.png")), (70, 70))
DINO_RUN1_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/dino-run1.png")), (88, 94))
DINO_RUN2_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/dino-run2.png")), (88, 94))
TRACK_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/track.png")), (750, 30))
BIRD1_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/bird1.png")), (50, 50))
BIRD2_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/bird2.png")), (50, 50))
DINO_DUCK1_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/dino-duck1.png")), (110, 52))
DINO_DUCK2_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/dino-duck2.png")), (110, 52))
CLOUD_IMAGE = pygame.transform.scale(pygame.image.load(resource_path("images/cloud.png")), (60, 30))
DARK_CLOUD_IMAGE = CLOUD_IMAGE.copy()
DARK_CLOUD_IMAGE.fill((100, 100, 130, 255), special_flags=pygame.BLEND_RGBA_MULT)

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT)) #game window
pygame.display.set_caption("Adventurer Dino") #title
clock = pygame.time.Clock()
GAME_FONT = pygame.font.SysFont("Lucida Console", 20)

VELOCITY_X = -8
VELOCITY_Y = -10
CLOUD_SPEED = -1
GRAVITY = 0.4

# Creates the images
dino = Block((50, GAME_HEIGHT-DINO_IMAGE.height), DINO_IMAGE.get_size(), DINO_IMAGE)
dino_run1 = Block((50, GAME_HEIGHT-DINO_RUN1_IMAGE.height), DINO_RUN1_IMAGE.get_size(), DINO_RUN1_IMAGE)
dino_run2 = Block((50, GAME_HEIGHT-DINO_RUN2_IMAGE.height), DINO_RUN2_IMAGE.get_size(), DINO_RUN2_IMAGE)
game_block = Block((225, 10), GAME_OVER_IMAGE.get_size(), GAME_OVER_IMAGE)
reset_block = Block((340, 150), RESET_IMAGE.get_size(), RESET_IMAGE)
track_block = Block((0, 220), TRACK_IMAGE.get_size(), TRACK_IMAGE)
track_block2 = Block((750, 220), TRACK_IMAGE.get_size(), TRACK_IMAGE)
cloud_block = Block((random.randint(750, 1000), 30), CLOUD_IMAGE.get_size(), CLOUD_IMAGE)
cloud_block2 = Block((random.randint(1000, 1300), 60), CLOUD_IMAGE.get_size(), CLOUD_IMAGE)
cloud_block3 = Block((random.randint(1100, 1400), 45), CLOUD_IMAGE.get_size(), CLOUD_IMAGE)

#Theme Variables
sky_color = "light blue"
text_color = "black"

#Variables
cactus_list = []
last_place_cactus_time = 0
game_over = False
use_first_image = True
walk_delay = 0
score = 0
is_ducking = False
wing_delay = 0
use_first_wing = True
high_score = 0
paused = False

def place_cactus():
    spawn_choice = random.randint(0, 1)
    
    if spawn_choice == 0:
        random_cactus_image = random.choice(CACTUS_IMAGES)
        random_cactus = Block((GAME_WIDTH, GAME_HEIGHT - random_cactus_image.height), random_cactus_image.get_size(), random_cactus_image)
# Sets the birds at different heights
    else:
        bird_height = random.choice([170, 140, 80])
        random_cactus = Block((GAME_WIDTH, bird_height), BIRD1_IMAGE.get_size(), BIRD1_IMAGE)

    random_cactus.velocity_x = VELOCITY_X
    cactus_list.append(random_cactus)
    

def move():
    global cactus_list, game_over, score, high_score, sky_color, text_color
    score += 1
    
    if is_ducking and dino.y < GAME_HEIGHT - dino.height:
        dino.velocity_y += GRAVITY * 4
    else:
        dino.velocity_y += GRAVITY
    dino.y += dino.velocity_y
    if dino.y >= GAME_HEIGHT - dino.height:
        dino.y = GAME_HEIGHT - dino.height
        dino.velocity_y = 0
    
    for cactus in cactus_list:
        cactus.x += cactus.velocity_x
        if dino.colliderect(cactus):
            game_over = True
            dino.image = DINO_DEAD_IMAGE
            if score > high_score:
                high_score = score

#Track moving animation
    track_block.x += VELOCITY_X
    track_block2.x += VELOCITY_X
    if(track_block.x<=-750):
        track_block.x = track_block2.x+750
    if(track_block2.x<=-750):
        track_block2.x = track_block.x+750
    
    cactus_list = [cactus for cactus in cactus_list if cactus.x + cactus.width > 0]

#Cloud 
    cloud_block.x += CLOUD_SPEED
    cloud_block2.x += CLOUD_SPEED
    cloud_block3.x += CLOUD_SPEED
    if cloud_block.x + cloud_block.width < 0:
        cloud_block.x = random.randint(250, 450)
    if cloud_block2.x + cloud_block2.width < 0:
        cloud_block2.x = cloud_block.x + random.randint(250, 450)
    if cloud_block3.x + cloud_block3.width < 0:
        cloud_block3.x = max(cloud_block.x +cloud_block.width, cloud_block2.x + cloud_block2.width) + random.randint(250, 450)

def reset_clouds():
    cloud_block.x = random.randint(750, 1000)
    cloud_block2.x = cloud_block.x + random.randint(250, 450)
    cloud_block3.x = random.randint(250, 450)

def draw_game_over():
    time.sleep(1)
    window.fill(sky_color)
    window.blit(game_block.image, game_block)
    window.blit(reset_block.image, reset_block)
    
    text_render = GAME_FONT.render(str(score), True, text_color)
    window.blit(text_render, (700, 20))
    
    high_score_text = GAME_FONT.render("HI " + str(high_score), True, text_color)
    window.blit(high_score_text, (580, 20))

def draw():
    window.fill(sky_color)
    
    window.blit(cloud_block.image, (cloud_block.x, cloud_block.y))
    window.blit(cloud_block2.image, (cloud_block2.x, cloud_block2.y))
    window.blit(cloud_block3.image, (cloud_block3.x, cloud_block3.y))
    window.blit(track_block.image, track_block)
    window.blit(track_block.image, track_block2)

    window.blit(dino.image, dino)
    
    for cactus in cactus_list:
        window.blit(cactus.image, cactus)
    
    text_render = GAME_FONT.render(str(score), True, text_color)
    window.blit(text_render, (700, 20))

    high_score_text = GAME_FONT.render("HI " + str(high_score), True, text_color)
    window.blit(high_score_text, (580, 20))

#game loop
while True:
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:       
            pygame.quit()
            exit()        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game_over:
                paused = not paused
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not paused:
                if game_over:
                    cactus_list.clear()
                    reset_clouds()
                    game_over = False
                    score = 0
                    #the ground collision
                    dino.y = GAME_HEIGHT - dino.height
                    dino.velocity_y = 0
                    dino.image = DINO_IMAGE
                #the gravity state
                elif dino.y >= GAME_HEIGHT - dino.height and not is_ducking:
                    dino.velocity_y = VELOCITY_Y
            if event.key == pygame.K_DOWN:
                is_ducking = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                is_ducking = False


# Running Animation
    if not paused:
        if is_ducking:
            dino.height = 52
            dino.width = 110
            dino.size = (110, 52)
            if dino.y >= GAME_HEIGHT - 94:
                dino.y = GAME_HEIGHT - 52
        else:
            dino.height = 94
            dino.width = 88
            dino.size = (88, 94)
    
        if dino.y < GAME_HEIGHT - dino.height and not game_over:
            dino.image = DINO_IMAGE
        if dino.y >= GAME_HEIGHT - dino.height:
            walk_delay += 1
        
            if walk_delay >= 5:
                use_first_image = not use_first_image
                walk_delay = 0
        
        # Ducking Animation
            if is_ducking:
                if use_first_image:
                    dino.image = DINO_DUCK1_IMAGE
                else:
                    dino.image = DINO_DUCK2_IMAGE
            else:
                if use_first_image:
                    dino.image = DINO_RUN1_IMAGE
                else:
                    dino.image = DINO_RUN2_IMAGE

#Wing Animation
    if not paused:
        wing_delay += 1
        if wing_delay >= 24:
            use_first_wing = not use_first_wing
            wing_delay = 0

            for cactus in cactus_list:
                if cactus.image == BIRD1_IMAGE or cactus.image == BIRD2_IMAGE:
                    if not use_first_wing:
                        cactus.y += 6
                    else:
                        cactus.y -= 6
    
        for cactus in cactus_list:
            if cactus.image == BIRD1_IMAGE or cactus.image == BIRD2_IMAGE:
                if use_first_wing:
                    cactus.image = BIRD1_IMAGE
                else:
                    cactus.image = BIRD2_IMAGE

#Day to Night Changing Every 1000 points
    if (score//1000) % 2 == 1:
        sky_color = "black"
        text_color = "white"
        
        cloud_block.image = DARK_CLOUD_IMAGE
        cloud_block2.image = DARK_CLOUD_IMAGE
        cloud_block3.image = DARK_CLOUD_IMAGE
    else:
        sky_color = "light blue"
        text_color = "black"
        
        cloud_block.image = CLOUD_IMAGE
        cloud_block2.image = CLOUD_IMAGE
        cloud_block3.image = CLOUD_IMAGE

    if not paused and not game_over:
        now = pygame.time.get_ticks()
        if now - last_place_cactus_time >= 1000:
            place_cactus()
            last_place_cactus_time = now
    
    if not game_over:
        if not paused:
            move()
        draw()
        if paused : 
            pause_text = GAME_FONT.render("PAUSED", True, text_color)
            window.blit(pause_text, (150, 110))
        pygame.display.update()
        clock.tick(60)
    
    else :
        draw_game_over()
        pygame.display.update() 

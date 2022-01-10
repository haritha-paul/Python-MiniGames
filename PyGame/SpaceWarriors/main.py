import pygame, sys
import random
import math
from pygame import mixer
pygame.init()
surface=pygame.display.set_mode((800,600))
black=(0,0,0)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('resources/ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('resources/background.png')
mixer.music.load('resources/background.wav')
mixer.music.play(-1)

playerimg = pygame.image.load('resources/player.png')
playerx = 370
playery = 480
playerchange=0

enemyimg = []
enemyx = []
enemyy = []
enemychangeX = []
enemychangeY = []
num_enemies =6
for i in range(num_enemies):
    enemyimg.append(pygame.image.load('resources/enemy.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemychangeX.append(4)
    enemychangeY.append(40)

bulletimg = pygame.image.load('resources/bullet.png')
bulletx = 0
bullety = 480
bulletchangeX = 0
bulletchangeY = 10
bullet_state = "ready"

score =0
font = pygame.font. Font("freesansbold.ttf",28)
textx=10
texty=10

def show_score(x,y):
    s = font.render("Score: " +str(score), True, (255,255,255))
    surface.blit(s,(x,y))

over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    surface.blit(over_text, (200, 250))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    surface.blit(bulletimg, (x + 16, y + 10))

def enemy(x,y,i):
    surface.blit(enemyimg[i], (x,y))


def player(x,y):
    surface.blit(playerimg,(x,y))


def isColllision (enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx-bulletx, 2) + math.pow(enemyy-bullety, 2))
    if distance < 27:
        return  True
    else:
        return False


running=True
while running:
    surface.fill(black)
    surface.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerchange = -5
            if event.key == pygame.K_RIGHT:
                playerchange = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletsound = mixer.Sound('resources/laser.wav')
                    bulletsound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame. K_RIGHT:
                playerchange = 5

    playerx += playerchange
    if playerx <=0:
        playerx=0
    elif playerx >= 736:
        playerx=736

    for i in range(num_enemies):

        if enemyy[i] > 440:
            for j in range(num_enemies):
                enemyy[j] = 2000
            game_over_text()
            break

        enemyx[i] += enemychangeX[i]
        if enemyx[i] <= 0:
            enemychangeX[i] = 4
            enemyy[i] += enemychangeY[i]
        elif enemyx[i] >= 736:
            enemychangeX[i] = -4
            enemyy[i] += enemychangeY[i]

        collision = isColllision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion = mixer.Sound('resources/explosion.wav')
            explosion.play()
            bullety = 480
            bullet_state = "ready"
            score += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i],i)




    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bulletchangeY


    player(playerx, playery)
    show_score(textx,texty)
    pygame.display.update()

import pygame
from pygame.locals import *
import random

pygame.init()

#set speed
clock = pygame.time.Clock()
fps = 60


width = 864 #864
height = 936 #936

surface = pygame.display.set_mode((width,height))

pygame.display.set_caption('Flappy Bird')

#load image
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
font=pygame.font.SysFont('Bauhaus 93',60)
white = (255, 255, 255)
button_img = pygame.image.load('img/restart.png')


ground_scroll = 0
scroll_speed =4
flying = False
game_over = False
gap = 150
pipe_freq = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() #time when game started
score = 0
pass_pipe=False

def draw_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    surface.blit(img,(x,y))

def reset_game():
    pipe_grp.empty()
    flappy.rect.x =100
    flappy.rect.y = int(height/2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index= 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel=0
        self.clicked = False

    def update(self):
        #gravity
        if flying==True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        if game_over == False:
        #jump
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked = False
            #animation
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter =0
                self.index +=1
                if self.index >= len(self.images):
                    self.index=0
            self.image=self.images[self.index]

            #rotate
            self.image =pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image =pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft =[x,y-int(gap/2)]
        if position == -1:
            self.rect.topleft =[x,y+int(gap/2)]

    def update(self):
        self.rect.x -= scroll_speed

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


bird_grp =pygame.sprite.Group()
pipe_grp = pygame.sprite.Group()

flappy = Bird(100, int(height/2))

bird_grp.add(flappy)

button = Button(width//2 - 50, height // 2 -100,button_img)


run=True
while run:
    clock.tick(fps)
    surface.blit(bg, (0,0))

    bird_grp.draw(surface)
    bird_grp.update()
    pipe_grp.draw(surface)

    # draw and scroll the ground
    surface.blit(ground_img, (ground_scroll, 768))

    #check score
    if len(pipe_grp) > 0:
        if bird_grp.sprites()[0].rect.left > pipe_grp.sprites()[0].rect.left and bird_grp.sprites()[0].rect.right < pipe_grp.sprites()[0].rect.right and pass_pipe==False:
            pass_pipe=True
        if pass_pipe == True:
            if bird_grp.sprites()[0].rect.left > pipe_grp.sprites()[0].rect.right:
                score +=1
                pass_pipe = False
    draw_text(str(score), font, white, int(width/2), 20)
    #collision
    if pygame.sprite.groupcollide(bird_grp,pipe_grp,False,False) or flappy.rect.top <0:
        game_over = True
    # check bird hit ground
    if flappy.rect.bottom > 768:
        game_over = True
        flying=False
    if game_over == False and flying == True:
        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now-last_pipe > pipe_freq:
            pipe_height = random.randint(-100, 100)
            b_pipe = Pipe(width, int(height / 2)+pipe_height, -1)
            t_pipe = Pipe(width, int(height / 2)+pipe_height, 1)
            pipe_grp.add(b_pipe)
            pipe_grp.add(t_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_grp.update()

    #check for gameover and reset
    if game_over ==True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and flying==False and game_over == False:
            flying = True
    pygame.display.update()

pygame.quit()
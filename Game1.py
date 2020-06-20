import pygame
import random
import math
from pygame import mixer
# runs the program

pygame.init()

# Screen setup

screen = pygame.display.set_mode((800, 600))

# background

background = pygame.image.load('1111.jpg')
mixer.music.load('background.mp3')
mixer.music.play(-1)
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf' , 32)
fx = 10
fy = 10

# End

end_font = pygame.font.Font('freesansbold.ttf' , 64)

def end():
    end_text = end_font.render(f'GAME OVER', True, (0, 0,0))
    screen.blit(end_text, (200,250))
def score(x , y):
    score1 = font.render(f'Score: {score_value}' , True , (255, 255 ,255))
    screen.blit(score1, (x , y))

# Title and Logo

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("1.png")
pygame.display.set_icon(icon)

# player

player1 = pygame.image.load('64.png')
px = 370
py = 480
p_change = 0

# enemy

enemy1 = []
ex = []
ey = []
ex_change = []
ey_change = []
num_enemies = 6
# enemy
for i in range(num_enemies):
    enemy1.append(pygame.image.load('space-invader-icon.png'))
    ex.append(random.randint(100, 700))
    ey.append(random.randint(20, 200))
    ex_change.append(3)
    ey_change.append(40)

# bullet

bullet = pygame.image.load("bullet.png")
bullet = pygame.transform.rotate(bullet, (45))
by = 480
bx = 0
by_change = 10
bullet_state = "ready"


# Functions of every character

def player(x, y):
    screen.blit(player1, (x, y))


def enemy(x, y, i):
    screen.blit(enemy1[i], (x, y))


def bullet_shoot(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 10, y - 30))


def collision(ex, ey, bx, by):
    distance = math.sqrt(math.pow(ex - px, 2) + math.pow(ey - by, 2))
    if distance < 70:
        return True
    else:
        return False

# Game loop

running = True
while running:
    for items in pygame.event.get():
        if items.type == pygame.QUIT:
            running = False
        if items.type == pygame.KEYDOWN:
            if items.key == pygame.K_LEFT:
                p_change = -3
            elif items.key == pygame.K_RIGHT:
                p_change = 3
            elif items.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    laser = mixer.Sound('laser.wav')
                    laser.play()
                    bx = px
                    bullet_shoot(bx, by)
        if items.type == pygame.KEYUP:
            if items.key == pygame.K_LEFT or items.key == pygame.K_RIGHT:
                p_change = 0

    # background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Characters updating

    player(px, py)
    px += p_change
    for i in range(num_enemies):

        # game over
        if ey[i] > 200:
            for j in range(num_enemies):
                ey[j] = 2000
            end()
            break

        ex[i] += ex_change[i]

        if ex[i] < 0:
            ey[i] += ey_change[i]
            ex_change[i] = 3
        elif ex[i] > 740:
            ey[i] += ey_change[i]
            ex_change[i] = -3

        if collision(ex[i], ey[i] , bx , by):
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            by = 480
            bullet_state = "ready"
            score_value += 1
            print(score)
            ex[i] = random.randint(100, 700)
            ey[i] = random.randint(20, 200)
        enemy(ex[i], ey[i] , i)
    if by <= 0:
        by = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        bullet_shoot( bx , by)
        by -= by_change

    score(fx , fy)

    pygame.display.update()

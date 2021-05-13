import random
import pygame, math
from pygame import font
from pygame import mixer
# initialize pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
# title and icon
pygame.display.set_caption("Space Invaders", )
icon = pygame.image.load('covwar.png')
pygame.display.set_icon(icon)
# Background
background = pygame.image.load('background.png')
#backgroundSound
mixer.music.load('background.wav')
mixer.music.play(-1)
# player
playerImg = pygame.image.load('002-rocket.png')
playerX = 370
playerY = 480
playerX_change = 0
# enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyXchange=[]
enemyYchange=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('covid.png'))
    enemyX.append( random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(4)  # default enemy change
    enemyYchange.append(50)

# bullet
# ready cant see bulllet
# fire bullet moving
bullet = pygame.image.load('syringe.png')
bulletX = 0
bulletY = 480
bulletX_change = 0  # default enemy change
bulletY_change = 12
bulletState = "ready"
#score

score_value=0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
#Game over text
over_font=pygame.font.Font('Baby Party.ttf',64)

def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))  # movement mechanics
# REady Cant see the bullet on the screen
# fire bullet is currently moving
def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bullet, (x + 16, y + 10))
def show_score(x,y):
    score=font.render("Score : " +str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x, y):
    screen.blit(playerImg, (x, y))  # movement mechanics

def game_over_text():
    over_text = over_font.render("GAME OVER" , True, (255, 255, 255))
    screen.blit(over_text, (250, 250))
def game_over_sound():
    gameoversound = mixer.Sound('gameeover.wav')
    gameoversound.play()



# Collision detection
def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow((enemyx - bulletx), 2) + math.pow((enemyy - bullety), 2))
    if distance < 27:
        return True
    return False


# game screen loop
running = True
while running:
    screen.fill((0, 0, 0))  # Rgb value
    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check right left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                print("Left arrow us pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                print("Right arrow us pressed")
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX  # continously changing pos of bullet as player is changing
                    fire_bullet(bulletX, bulletY)  # x is the position of the spaceship y is arbitary

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print("Keystroke released")
    # checking boundaries of spaceship so it doesnt go out of bound
    playerX += playerX_change #movement left right
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

        # enemy movement
    for i in range(num_of_enemies):
        #game over
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            mixer.music.stop()
            game_over_text()
            game_over_sound()
            bulletState="ready"
            break
        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 4
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >= 736:
            enemyXchange[i] = -4
            enemyY[i] += enemyYchange[i]

    # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bulletState = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i]= random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()

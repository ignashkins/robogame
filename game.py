#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import os
import threading
import random

pygame.init()

SCREEN_HEIGHT = 438
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

gameObjectsYPos = 300

pygame.display.set_caption('robot')

Ico = pygame.image.load('assets/bot.png')
pygame.display.set_icon(Ico)

RUNNING = []
for frame in range(718):
    if frame < 10:
        num = "00" + str(frame)
    elif 9 < frame < 100:
        num = "0" + str(frame)
    else:
        num = str(frame)
    RUNNING.append(pygame.image.load(os.path.join("assets/robot/run", "RobotRun." + num + ".png")))
JUMPING = pygame.image.load(os.path.join('assets/robot/run', 'RobotRun.021.png'))
DUCKING = []
for frame in range(9, 121):
    if frame < 10:
        num = "00" + str(frame)
    elif 9 < frame < 100:
        num = "0" + str(frame)
    else:
        num = str(frame)
    DUCKING.append(pygame.image.load(os.path.join("assets/robot/down", "Robo7." + num + ".png")))
MANS = [
    pygame.image.load(os.path.join('assets/people', 'man1.png')),
    pygame.image.load(os.path.join('assets/people', 'man2.png')),
    pygame.image.load(os.path.join('assets/people', 'man3.png'))
]

BIRD = [
    pygame.image.load(os.path.join('assets/bird', '63861472-0.png')),
    pygame.image.load(os.path.join('assets/bird', '63861472-1.png')),
    pygame.image.load(os.path.join('assets/bird', '63861472-2.png')),
    pygame.image.load(os.path.join('assets/bird', '63861472-3.png')),
]

CLOUD = pygame.image.load(os.path.join('assets/other', 'cloud.png'))

BG = [
    pygame.image.load(os.path.join('assets/other', 'road1-1.png')),
    pygame.image.load(os.path.join('assets/other', 'road1-2.png'))
]


class Robot:
    X_POS = 80
    Y_POS = gameObjectsYPos
    Y_POS_DUCK = gameObjectsYPos
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            if self.step_index >= 161:
                self.step_index = 100
            self.duck()
        if self.dino_run:
            self.run()
            if self.step_index >= 718:
                self.step_index = 0
        if self.dino_jump:
            if self.step_index >= 10:
                self.step_index = 0
            self.jump()

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK + 28
        self.step_index += 6

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 5

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):

        box = (
            self.dino_rect.x,
            self.dino_rect.y,
            self.image.get_width(),
            self.image.get_height()
        )
        # pygame.draw.rect(SCREEN, (255, 0, 0), box)

        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:

    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        box = (self.rect.x, self.rect.y, 100, 100)
        # pygame.draw.rect(SCREEN, (255, 255, 0), box)

        SCREEN.blit(self.image[self.type], self.rect)


class Man(Obstacle):

    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = gameObjectsYPos


class Bird(Obstacle):

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = gameObjectsYPos - 65
        self.index = 0
        self.image = image

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0

        box = (self.rect.x, self.rect.y, 68, 97)
        # pygame.draw.rect(SCREEN, (255, 0, 0), box)

        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Robot()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 0
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render('Очки: ' + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        bgr = BG[0]
        image_width = bgr.get_width()

        SCREEN.blit(bgr, (x_pos_bg, y_pos_bg))
        SCREEN.blit(bgr, (image_width + x_pos_bg, y_pos_bg))

        if x_pos_bg <= -image_width:
            print(str(x_pos_bg) + " <= " + str(image_width))
            SCREEN.blit(bgr, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        background()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Man(MANS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render('Ну давай уже начинай. Жми', True, (0, 0,
                                                                   0))
        elif death_count > 0:
            text = font.render('Еще разок? Жми', True, (0, 0,
                                                        0))
            score = font.render('Очки: ' + str(points), True, (0,
                                                               0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                                + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT
                                 // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()

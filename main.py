import pygame
import sys
import random
from math import *

pygame.init()

width = 500
height = 500

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Game")
clock = pygame.time.Clock()

margin = 20
lower_limit = margin

score = 0

white = (255, 255, 255)
light_blue = (0, 191, 255)
red = (255, 0, 0)
lightGreen = (0, 255, 0)
darkGray = (50, 50, 50)
darkBlue = (0, 0, 128)
green = (0, 128, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)
orange = (255, 165, 0)

font = pygame.font.SysFont("Snap ITC", 30)


class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randint(margin, width - self.a - margin)
        self.y = height - lower_limit
        self.angle = 90
        self.speed = -speed
        self.probPool = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, blue, yellow, purple, orange])

    def move(self):
        direct = random.choice(self.probPool)

        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))

        if (self.x + self.a) > width or (self.x < 0) < margin:
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a / 2, self.y + self.b),
                         (self.x + self.a / 2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a / 2 - 5, self.y + self.b - 3, 10, 10))

    def burst(self):
        global score
        pos = pygame.mouse.get_pos()

        if onBalloon(self.x, self.y, self.a, self.b, pos):
            score += 1
            self.reset()

    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randint(margin, width - self.a - margin)
        self.y = height - lower_limit
        self.angle = 90
        self.speed -= 0.002
        self.probPool = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, blue, yellow, purple, orange])


balloons = []
noBalloons = 10
for i in range(noBalloons):
    obj = Balloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
    balloons.append(obj)


def onBalloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False


def pointer():
    pos = pygame.mouse.get_pos()
    right = 25
    left = 20
    color = lightGreen
    for i in range(noBalloons):
        if onBalloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - right / 2, pos[1] - right / 2, right, right), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - left / 2), (pos[0], pos[1] - left), 4)
    pygame.draw.line(display, color, (pos[0] + left / 2, pos[1]), (pos[0] + left, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + left / 2), (pos[0], pos[1] + left), 4)
    pygame.draw.line(display, color, (pos[0] - left / 2, pos[1]), (pos[0] - left, pos[1]), 4)


def lowerPlatform():
    pygame.draw.rect(display, darkGray, (0, height - lower_limit, width, lower_limit))


def scoreBoard():
    text = font.render("Score: " + str(score), True, white)
    display.blit(text, (150, height - lower_limit + 50))


def close():
    pygame.quit()
    quit()


def gameLoop():
    global score
    loop = True

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_ESCAPE:
                    close()
                if event.type == pygame.K_r:
                    score = 0
                    gameLoop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(noBalloons):
                    balloons[i].burst()

        display.fill(light_blue)

        for i in range(noBalloons):
            balloons[i].show()

        pointer()

        for i in range(noBalloons):
            balloons[i].move()

        lowerPlatform()
        scoreBoard()
        pygame.display.update()
        clock.tick(60)


gameLoop()

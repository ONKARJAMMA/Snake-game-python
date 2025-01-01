import pygame
import sys
import os
import random
import math

pygame.init()
pygame.display.set_caption("Snake Game")
pygame.font.init()
random.seed()

# Global constants
SPEED = 0.36
SNAKE_SIZE = 15
APPLE_SIZE = SNAKE_SIZE
SEPARATION = 10
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
FPS = 25
KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE)

# Resources
score_font = pygame.font.Font(None, 38)
score_numb_font = pygame.font.Font(None, 28)
game_over_font = pygame.font.Font(None, 46)
play_again_font = score_numb_font
score_msg = score_font.render("Score:", 1, pygame.Color("green"))
score_msg_size = score_font.size("Score")
background_color = pygame.Color(0, 0, 0)

# Clock
gameClock = pygame.time.Clock()

def checkCollision(posA, As, posB, Bs):
    return posA.x < posB.x + Bs and posA.x + As > posB.x and posA.y < posB.y + Bs and posA.y + As > posB.y

def checkLimits(snake):
    """Check boundaries; end game if snake crosses."""
    if snake.x < 0 or snake.x >= SCREEN_WIDTH or snake.y < 0 or snake.y >= SCREEN_HEIGHT:
        return True
    return False

class Apple:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.Color("orange")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, APPLE_SIZE, APPLE_SIZE), 0)

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = "white"

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.stack = []
        self.stack.append(self)
        self.stack.append(Segment(self.x, self.y + SEPARATION))

    def move(self):
        last_element = len(self.stack) - 1
        while last_element != 0:
            self.stack[last_element].direction = self.stack[last_element - 1].direction
            self.stack[last_element].x = self.stack[last_element - 1].x
            self.stack[last_element].y = self.stack[last_element - 1].y
            last_element -= 1
        if len(self.stack) < 2:
            last_segment = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if self.stack[0].direction == KEY["UP"]:
            last_segment.y = self.stack[0].y - (SPEED * FPS)
        elif self.stack[0].direction == KEY["DOWN"]:
            last_segment.y = self.stack[0].y + (SPEED * FPS)
        elif self.stack[0].direction == KEY["LEFT"]:
            last_segment.x = self.stack[0].x - (SPEED * FPS)
        elif self.stack[0].direction == KEY["RIGHT"]:
            last_segment.x = self.stack[0].x + (SPEED * FPS)
        self.stack.insert(0, last_segment)

    def grow(self):
        last_segment = self.stack[-1]
        if last_segment.direction == KEY["UP"]:
            new_segment = Segment(last_segment.x, last_segment.y - SNAKE_SIZE)
        elif last_segment.direction == KEY["DOWN"]:
            new_segment = Segment(last_segment.x, last_segment.y + SNAKE_SIZE)
        elif last_segment.direction == KEY["LEFT"]:
            new_segment = Segment(last_segment.x - SNAKE_SIZE, last_segment.y)
        elif last_segment.direction == KEY["RIGHT"]:
            new_segment = Segment(last_segment.x + SNAKE_SIZE, last_segment.y)
        self.stack.append(new_segment)

    def checkCrashing(self):
        head = self.stack[0]
        for segment in self.stack[1:]:
            if checkCollision(head, SNAKE_SIZE, segment, SNAKE_SIZE):
                return True
        return False

    def draw(self, screen):
        for segment in self.stack:
            color = pygame.Color("green") if segment == self.stack[0] else pygame.Color("yellow")
            pygame.draw.rect(screen, color, (segment.x, segment.y, SNAKE_SIZE, SNAKE_SIZE), 0)

def getKey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        if event.type == pygame.QUIT:
            sys.exit(0)

def endGame():
    message = game_over_font.render("Game Over", 1, pygame.Color("white"))
    screen.blit(message, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
    pygame.display.flip()
    pygame.time.wait(2000)
    sys.exit(0)

def drawScore(score):
    score_numb = score_numb_font.render(str(score), 1, pygame.Color("red"))
    screen.blit(score_msg, (SCREEN_WIDTH - score_msg_size[0] - 60, 10))
    screen.blit(score_numb, (SCREEN_WIDTH - 45, 14))

def main():
    score = 0
    mySnake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    mySnake.setDirection(KEY["UP"])
    apples = [Apple(random.randint(0, SCREEN_WIDTH - APPLE_SIZE), random.randint(0, SCREEN_HEIGHT - APPLE_SIZE), 1)]

    while True:
        gameClock.tick(FPS)
        keyPress = getKey()
        if keyPress == "exit":
            break
        if keyPress:
            mySnake.setDirection(keyPress)

        mySnake.move()
        if checkLimits(mySnake.stack[0]):
            endGame()
        if mySnake.checkCrashing():
            endGame()

        for apple in apples:
            if apple.state == 1 and checkCollision(mySnake.stack[0], SNAKE_SIZE, apple, APPLE_SIZE):
                mySnake.grow()
                apple.state = 0
                score += 10

        screen.fill(background_color)
        for apple in apples:
            if apple.state == 1:
                apple.draw(screen)
        mySnake.draw(screen)
        drawScore(score)
        pygame.display.flip()

main()






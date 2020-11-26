# imports and initiates the pygame module
import pygame
pygame.init()
pygame.font.init()

# Imports random module for use in the apple location randomizer
from random import *

import sys
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Screen Size
screenWidth = 800
screenHeight = 704

# sets the window size and creates the window
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake")

# Creates a font object
font = pygame.font.SysFont('Comic Sans MS', 30)


class Player:
    def __init__(self, grid_x, grid_y, width, height, length):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.width = width
        self.height = height
        self.length = length


class Apple:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def randomizeLocation(self):
        self.x = round(randint(0, 768) / 32) * 32
        self.y = round(randint(0, 672) / 32) * 32


# Creates custom move event
MOVEEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVEEVENT, 200)

# Initializes the Player class
player = Player(384, 320, 32, 32, 1)

# Initializes the Apple class and picks a random position
apple = Apple(0, 0, 32, 32)
apple.randomizeLocation()

# Variable that tells the game which direction the snake is facing
snakeDirection = 0

# Variable that tells the game whether the snake has turned without moving afterwards first
justTurned = 0

# The score
score = 0

# List that holds the positions for the snake body
snakeBody = [[player.grid_x, player.grid_y]]

# Condition used for the main loop
run = True

# Main Loop
while run:

    # Controls the FPS for the Game (100 FPS)
    pygame.time.delay(10)

    # Event for loop that gets every event in the entire pygame module
    for event in pygame.event.get():
        # If statements that compares the current event to the event assigned
        if event.type == pygame.QUIT:
            run = False
        # This event is what moves the snake
        if event.type == MOVEEVENT:
            if snakeDirection == 1:
                player.grid_y += -32
            elif snakeDirection == 2:
                player.grid_y += 32
            elif snakeDirection == 3:
                player.grid_x += -32
            elif snakeDirection == 4:
                player.grid_x += 32

            # Gives the illusion of movement by removing the tail, and adding the new head position to the front
            snakeBody.pop(-1)
            snakeBody.insert(0, [player.grid_x, player.grid_y])

            justTurned = 0

    # Gets the key events and puts them into a variable
    keys = pygame.key.get_pressed()

    # This is what allows for the arrow keys to control the snake
    if keys[pygame.K_UP]:
        if snakeDirection != 2 and justTurned == 0:
            snakeDirection = 1
            justTurned = 1
    if keys[pygame.K_DOWN]:
        if snakeDirection != 1 and justTurned == 0:
            snakeDirection = 2
            justTurned = 1
    if keys[pygame.K_LEFT]:
        if snakeDirection != 4 and justTurned == 0:
            snakeDirection = 3
            justTurned = 1
    if keys[pygame.K_RIGHT]:
        if snakeDirection != 3 and justTurned == 0:
            snakeDirection = 4
            justTurned = 1

    # Checks to see if the snake has crashed into a wall
    if player.grid_x < 0 or player.grid_x > 768:
        run = False
    if player.grid_y < 0 or player.grid_y > 672:
        run = False

    # Checks to see if the snake has collided with itself
    if snakeBody[0] in snakeBody[1:]:
        run = False

    # Collision detection between the snake head and the apple
    if player.grid_x == apple.x and player.grid_y == apple.y:
        apple.randomizeLocation()
        player.length += 1
        snakeBody.append([1000, 1000])
        score += 1

    # fills the entire screen with black, erasing the old snake position
    win.fill((0, 0, 0))

    # Draws the apple to the screen
    pygame.draw.rect(win, (255, 0, 0), (apple.x, apple.y, apple.width, apple.height))

    # Draws the snake to the screen
    for segment in snakeBody:
        pygame.draw.rect(win, (0, 255, 0), (segment[0], segment[1], player.width, player.height))

    # Displays Score
    textSurface = font.render('Score: ' + str(score), False, (255, 255, 255))
    win.blit(textSurface, (650, 650))

    # Updates the Screen
    pygame.display.update()

# Close the window after the game is no longer running
pygame.quit()

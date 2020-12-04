import pygame
from random import *
import sys
import os
pygame.init()
pygame.font.init()


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Game:
    def __init__(self, screenwidth, screenheight, font, moveevent, score,):
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.win = pygame.display.set_mode((screenwidth, screenheight))
        self.font = font
        self.moveevent = moveevent
        self.score = score
        pygame.display.set_caption("Snake")
        pygame.time.set_timer(moveevent, 200)
        self.run = True

    def handleEvents(self):
        # Event for loop that gets every event in the entire pygame module
        for event in pygame.event.get():
            # If statements that compares the current event to the event assigned
            if event.type == pygame.QUIT:
                game.run = False
            # This event is what moves the snake
            if event.type == game.moveevent:
                if player.snakeDirection == 1:
                    player.grid_y += -32
                elif player.snakeDirection == 2:
                    player.grid_y += 32
                elif player.snakeDirection == 3:
                    player.grid_x += -32
                elif player.snakeDirection == 4:
                    player.grid_x += 32

                # Gives the illusion of movement by removing the tail, and adding the new head position to the front
                player.snakeBody.pop(-1)
                player.snakeBody.insert(0, [player.grid_x, player.grid_y])

                player.justTurned = 0

        # Gets the key events and puts them into a variable
        keys = pygame.key.get_pressed()

        # This is what allows for the arrow keys to control the snake
        if keys[pygame.K_UP]:
            if player.snakeDirection != 2 and player.justTurned == 0:
                player.snakeDirection = 1
                player.justTurned = 1
        if keys[pygame.K_DOWN]:
            if player.snakeDirection != 1 and player.justTurned == 0:
                player.snakeDirection = 2
                player.justTurned = 1
        if keys[pygame.K_LEFT]:
            if player.snakeDirection != 4 and player.justTurned == 0:
                player.snakeDirection = 3
                player.justTurned = 1
        if keys[pygame.K_RIGHT]:
            if player.snakeDirection != 3 and player.justTurned == 0:
                player.snakeDirection = 4
                player.justTurned = 1

        # Checks to see if the snake has crashed into a wall
        if player.grid_x < 0 or player.grid_x > 768:
            game.run = False
        if player.grid_y < 0 or player.grid_y > 672:
            game.run = False

        # Checks to see if the snake has collided with itself
        if player.snakeBody[0] in player.snakeBody[1:]:
            game.run = False

        # Collision detection between the snake head and the apple
        if player.grid_x == apple.x and player.grid_y == apple.y:
            apple.randomizeLocation()
            player.length += 1
            player.snakeBody.append([1000, 1000])
            game.score += 1

    def updateScreen(self):
        # Controls the FPS for the Game (100 FPS)
        pygame.time.delay(10)

        # fills the entire screen with black, erasing the old snake position
        game.win.fill((0, 0, 0))

        # Draws the apple to the screen
        pygame.draw.rect(game.win, (255, 0, 0), (apple.x, apple.y, apple.width, apple.height))

        # Draws the snake to the screen
        for segment in player.snakeBody:
            pygame.draw.rect(game.win, (0, 255, 0), (segment[0], segment[1], player.width, player.height))

        # Displays Score
        textSurface = game.font.render('Score: ' + str(game.score), False, (255, 255, 255))
        game.win.blit(textSurface, (650, 650))

        # Updates the Screen
        pygame.display.update()


class Player:
    def __init__(self, grid_x, grid_y, width, height, length, snakeDirection, justTurned,):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.width = width
        self.height = height
        self.length = length
        self.snakeDirection = snakeDirection
        self.justTurned = justTurned
        self.snakeBody = [[grid_x, grid_y]]


class Apple:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def randomizeLocation(self):
        self.x = round(randint(0, 768) / 32) * 32
        self.y = round(randint(0, 672) / 32) * 32


# Initializes the Game class
game = Game(800, 704, pygame.font.SysFont('Comic Sans MS', 30), pygame.USEREVENT + 1, 0)

# Initializes the Player class
player = Player(384, 320, 32, 32, 1, 0, 0,)

# Initializes the Apple class and picks a random position
apple = Apple(0, 0, 32, 32)
apple.randomizeLocation()

# Main Loop
while game.run:
    game.handleEvents()
    game.updateScreen()

# Close the window after the game is no longer running
pygame.quit()

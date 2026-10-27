# Draw & Create Screen
import pygame
import sys
import random
import threading
import time

# Colors
BG = (30, 30, 30)
WLL = (120, 120, 120)

# Board Variables
board = []
board_y = 31
board_x = 28

# Screen Variables
length = 10
gap = 2

tab_y = board_y * length + board_y * gap + gap
tab_x = board_x * length + board_x * gap + gap

def board_gen():
    # Map Generator
    for y in range(board_y):
        board.append([0] * board_x)
    # Boarders
    for y in range(board_y):
        board[y][0] = 1
        board[y][board_x - 1] = 1
    for x in range(board_x):
        board[0][x] = 1
        board[board_y - 1][x] = 1
    # Ghost Spawn
    for y in range(12, 17):
        for x in range(10, 18):
            board[y][x] = 1
    for y in range(13, 16):
        for x in range(11, 17):
            board[y][x] = 0
    # Door of Spawn
    board[12][13] = board[12][14] = 0 
    # Obstacles
    obstcl = [
        [2, 5, 2, 6, True], 
        [2, 5, 7, 13, True],
        [6, 9, 2, 5, True],
        [6, 9, 7, 10, True],
        [6, 9, 11, 15, False],
        [21, 24, 2, 6, True],
        [27, 30, 2, 11, True],
    ]
    for y1, y2, x1, x2, mirror in obstcl:
        for y in range(y1, y2):
            for x in range(x1, x2):
                board[y][x] = 1
                if mirror:
                    board[y][board_x - 1 - x] = 1

def draw(screen):
    for y in range(board_y):
        for x in range(board_x):
            X = x * (length + gap) + gap
            Y = y * (length + gap) + gap

            if board[y][x] == 0:
                pygame.draw.rect(screen, BG, [X, Y, length, length], border_radius = 5)
            if board[y][x] == 1:
                pygame.draw.rect(screen, WLL, [X, Y, length, length], border_radius = 5)


def main():
    global board, board_y, board_x, tab_y, tab_x
    pygame.init()
    pygame.display.set_caption("Pac-Man 002")
    screen = pygame.display.set_mode((tab_x, tab_y))
    clock = pygame.time.Clock()

    board_gen()

    font = pygame.font.Font(None, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BG)
        draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
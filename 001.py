# Raw Map
import pygame
import sys
import random
import threading
import time

# Board Variables
board = []
board_y = 31
board_x = 28
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

for y in range(board_y):
    print(board[y])
# Smoother Movement + Gaps
import pygame
import sys
import random
import threading
import time

# Colors
BG = (30, 30, 30)
WLL = (120, 120, 120)
ACTV = (0, 255, 255)
# Board Variables
board_y = 29
board_x = 28
# Screen Variables
length = 10
step = 1
gap = 2
scrn_y = board_y * length
scrn_x = board_x * length
tab_y = board_y * (length + gap) + gap
tab_x = board_x * (length + gap) + gap
# Player Variables
plyr = [0, 0]
scrn = []
drct = 0 # 3 = right, 6 = down, 9 = left, 12 = up
# Board - Maze Shape
for y in range(board_y * length):
    scrn.append([0] * (board_y * length))
board = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Bololean Values
def check(direction):
    if direction == 3:
        return (plyr[1] + 1 < tab_x) and all(scrn[plyr[0] + y][plyr[1] + x + step] != 1 for y in range(length) for x in range(length))
    elif direction == 6:
        return (plyr[0] + 1 < tab_y) and all(scrn[plyr[0] + y + step][plyr[1] + x] != 1 for y in range(length) for x in range(length))
    elif direction == 9:
        return (plyr[1] - 1 >= 0) and all(scrn[plyr[0] + y][plyr[1] + x - step] != 1 for y in range(length) for x in range(length))
    elif direction == 12:
        return (plyr[0] - 1 >= 0) and all(scrn[plyr[0] + y - step][plyr[1] + x] != 1 for y in range(length) for x in range(length))

def spawn():
    global plyr, drct, scrn
    plyr = [15 * length, 13 * length]
    for y in range(scrn_y):
        for x in range(scrn_x):
            scrn[y][x] = board[y//length][x//length]
    drct = 0

lock = threading.Lock()
def move():
    global plyr, drct
    while True:
        time.sleep(0.01)
        with lock:
            print(plyr)
            plyr_to_scrn(0)
            if (drct == 3 and plyr == [12 * length, 27 * length]): plyr = [12 * length, -1 * length]
            if (drct == 9 and plyr == [12 * length, 0 * length]): plyr = [12 * length, 27 * length]

            elif check(drct):
                if drct == 3:
                    plyr[1] += step
                elif drct == 6:
                    plyr[0] += step
                elif drct == 9:
                    plyr[1] -= step
                elif drct == 12:
                    plyr[0] -= step
            plyr_to_scrn(2)

def plyr_to_scrn(state):
    for y in range(length):
        for x in range(length):
            scrn[plyr[0] + y][plyr[1] + x] = state

def draw(screen):
    for y in range(scrn_y):
        for x in range(scrn_x):
            Y = y + gap * (y//length)
            X = x + gap * (x//length)

            if scrn[y][x] == 0:
                pygame.draw.rect(screen, BG, [X, Y, 1, 1], border_radius = 0)
            if scrn[y][x] == 1:
                pygame.draw.rect(screen, WLL, [X, Y, 1, 1], border_radius = 0)
            if scrn[y][x] == 2:
                pygame.draw.rect(screen, ACTV, [X, Y, 1, 1], border_radius = 0)


def main():
    global board, board_y, board_x, tab_y, tab_x, plyr, drct
    pygame.init()
    pygame.display.set_caption("Pac-Man 004")
    screen = pygame.display.set_mode((tab_x, tab_y))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 50)

    spawn()

    bg_thread = threading.Thread(target=move, daemon=True)
    bg_thread.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    drct = 3
                if event.key == pygame.K_DOWN:
                    drct = 6
                if event.key == pygame.K_LEFT:
                    drct = 9
                if event.key == pygame.K_UP:
                    drct = 12

        screen.fill(BG)

        with lock:
            draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

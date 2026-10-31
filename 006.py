# Red Ghost Added
import pygame
import sys
import random
import threading
import time
from collections import deque

# Colors
BG = (30, 30, 30)
WLL = (120, 120, 120)
PLYR = (0, 255, 255)
R_GHST = (255, 0, 0)

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
old_drct = 0
drct = 0  # 3 = right, 6 = down, 9 = left, 12 = up
ghost = []
ghst_drct = []
game_over = False

# Board - Maze Shape
for y in range(board_y * length): 
    scrn.append([0] * (board_y * length))
for id in range(4): 
    ghst_drct.append([0] * 5)
    ghost.append([0] * 2)

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
lock_plyr = threading.Lock()
lock_red = threading.Lock()

def check(direction, cord):
    if direction == 3: return (cord[1] + 1 < scrn_x) and all(scrn[cord[0] + y][cord[1] + x + step] != 1 for y in range(length) for x in range(length))
    elif direction == 6: return (cord[0] + 1 < scrn_y) and all(scrn[cord[0] + y + step][cord[1] + x] != 1 for y in range(length) for x in range(length))
    elif direction == 9: return (cord[1] - 1 >= 0) and all(scrn[cord[0] + y][cord[1] + x - step] != 1 for y in range(length) for x in range(length))
    elif direction == 12: return (cord[0] - 1 >= 0) and all(scrn[cord[0] + y - step][cord[1] + x] != 1 for y in range(length) for x in range(length))
    return False

def opposite_dir(d):
    if d == 3: return 9
    if d == 9: return 3
    if d == 6: return 12
    if d == 12: return 6
    return 0

def shortest_path(start_tile, target_tile):
    sr, sc = start_tile
    tr, tc = target_tile
    if (sr, sc) == (tr, tc):
        return None
    
    queue = deque([(sr, sc)])
    visited = {(sr, sc)}
    parent = {}
    
    directions = [
        (3, 0, 1),
        (6, 1, 0),
        (9, 0, -1),
        (12, -1, 0)
    ]
    
    found = False
    while queue:
        r, c = queue.popleft()
        if (r, c) == (tr, tc):
            found = True
            break
            
        for d, dr, dc in directions:
            nr, nc = r + dr, c + dc
            if nr == 12 and (nc < 0 or nc >= board_x):
                nc = nc % board_x
            if 0 <= nr < board_y and 0 <= nc < board_x and board[nr][nc] != 1:
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c, d)
                    queue.append((nr, nc))
                    
    if not found:
        return None
        
    curr = (tr, tc)
    first_step_dir = None
    while curr in parent:
        p_r, p_c, d = parent[curr]
        if (p_r, p_c) == (sr, sc):
            first_step_dir = d
            break
        curr = (p_r, p_c)
        
    return first_step_dir

def spawn():
    global plyr, drct, scrn, ghost
    plyr = [15 * length, 13 * length]
    for i in range(4):
        ghost[i] = [12 * length, (12 + i) * length]
    for y in range(scrn_y):
        for x in range(scrn_x):
            scrn[y][x] = board[y//length][x//length]
    drct = 0
    
def to_scrn(cord, state):
    for y in range(length):
        for x in range(length):
            scrn[cord[0] + y][cord[1] + x] = state

def draw(screen):
    for y in range(scrn_y):
        for x in range(scrn_x):
            Y = y + gap * (y//length)
            X = x + gap * (x//length)

            if scrn[y][x] == 0: # Empty
                pygame.draw.rect(screen, BG, [X, Y, step, step], border_radius = 0)
            if scrn[y][x] == 1: # Wall
                pygame.draw.rect(screen, WLL, [X, Y, step, step], border_radius = 0)
            if scrn[y][x] == 2: # Player
                pygame.draw.rect(screen, PLYR, [X, Y, step, step], border_radius = 1)
            if scrn[y][x] == 3: # Red Ghost
                pygame.draw.rect(screen, R_GHST, [X, Y, step, step], border_radius = 1)

def closest():
    global old_drct, drct
    if old_drct in (6, 12) and drct in (3, 9): 
        if plyr[0] % length <= gap or plyr[0] % length >= length - gap:
            plyr[0] = int(round(plyr[0], -1))
    if old_drct in (3, 9) and drct in (6, 12): 
        if plyr[1] % length <= gap or plyr[1] % length >= length - gap:
            plyr[1] = int(round(plyr[1], -1))

def move():
    global plyr, drct, game_over
    while not game_over:
        time.sleep(0.01)
        with lock_plyr and lock_red:
            if game_over: break
            to_scrn(plyr, 0)
            if drct == 3 and plyr == [12 * length, 27 * length]: 
                plyr = [12 * length, -1 * length]
            elif drct == 9 and plyr == [12 * length, 0 * length]: 
                plyr = [12 * length, 27 * length]
            else: 
                closest()
                if check(drct, plyr):
                    if drct == 3: plyr[1] += step
                    elif drct == 6: plyr[0] += step
                    elif drct == 9: plyr[1] -= step
                    elif drct == 12: plyr[0] -= step
            to_scrn(plyr, 2)

def red():
    global ghost, ghst_drct, game_over
    time.sleep(1)
    cnt = 40
    while not game_over:
        time.sleep(0.0175)
        with lock_plyr and lock_red:
            if game_over: break
            to_scrn(ghost[0], 0)
            if cnt > 0:
                if cnt > 30: ghost[0][0] -= step
                elif cnt > 20: ghost[0][1] += step
                elif cnt > 0: ghost[0][0] -= step
                cnt -= 1
                to_scrn(ghost[0], 3)
                continue
            
            id = 0
            
            if abs(ghost[id][0] - plyr[0]) < length and abs(ghost[id][1] - plyr[1]) < length:
                game_over = True
                break

            curr_d = ghst_drct[id][0]
            
            is_aligned = (ghost[id][0] % length == 0) and (ghost[id][1] % length == 0)
            all_valid_dirs = [d for d in [3, 6, 9, 12] if check(d, ghost[id])]
            opp_d = opposite_dir(curr_d)
            other_paths = [d for d in all_valid_dirs if d != opp_d]
            is_intersection = is_aligned and (len(other_paths) >= 2)
            
            if curr_d == 0 or not check(curr_d, ghost[id]) or is_intersection:
                start_tile = (ghost[id][0] // length, ghost[id][1] // length)
                target_tile = (plyr[0] // length, plyr[1] // length)
                
                best_d = shortest_path(start_tile, target_tile)
                
                if best_d is None or not check(best_d, ghost[id]):
                    forward_dirs = [d for d in all_valid_dirs if d != opp_d]
                    if not forward_dirs:
                        forward_dirs = all_valid_dirs
                    if forward_dirs:
                        best_d = forward_dirs[0]
                    else:
                        best_d = curr_d if curr_d != 0 else 3
                        
                curr_d = best_d
                ghst_drct[id][0] = curr_d
            
            if curr_d == 3 and ghost[id] == [12 * length, 27 * length]: 
                ghost[id] = [12 * length, -1 * length]
            elif curr_d == 9 and ghost[id] == [12 * length, 0 * length]: 
                ghost[id] = [12 * length, 27 * length]
            else:
                if check(curr_d, ghost[id]):
                    if curr_d == 3: ghost[id][1] += step
                    elif curr_d == 6: ghost[id][0] += step
                    elif curr_d == 9: ghost[id][1] -= step
                    elif curr_d == 12: ghost[id][0] -= step
                
            to_scrn(ghost[0], 3)

def main():
    global board, board_y, board_x, tab_y, tab_x, plyr, drct, old_drct, game_over
    pygame.init()
    pygame.display.set_caption("Pac-Man 005")
    screen = pygame.display.set_mode((tab_x, tab_y))
    clock = pygame.time.Clock()

    spawn()

    bg_plyr = threading.Thread(target=move, daemon=True)
    bg_red = threading.Thread(target=red, daemon=True)
    
    bg_plyr.start()
    bg_red.start()

    font_large = pygame.font.SysFont(None, 48)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    old_drct = drct
                    drct = 3
                if event.key == pygame.K_DOWN:
                    old_drct = drct
                    drct = 6
                if event.key == pygame.K_LEFT:
                    old_drct = drct
                    drct = 9
                if event.key == pygame.K_UP:
                    old_drct = drct
                    drct = 12

        screen.fill(BG)

        with lock_plyr and lock_red:
            draw(screen)

        if game_over:
            overlay = pygame.Surface((tab_x, tab_y), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 160))
            screen.blit(overlay, (0, 0))

            text_surf = font_large.render("GAME OVER", True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=(tab_x // 2, tab_y // 2))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

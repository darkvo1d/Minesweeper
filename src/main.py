import random
import math
import numpy as np
import os
import pygame

pygame.font.init()

WIDTH, HEIGHT = 500, 550
GRID_WIDTH, GRID_HEIGHT = 500, 500
FPS = 60
BOX_SIZE = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HEAD_BUFFER_SIZE = 50
X, Y = WIDTH // BOX_SIZE, (HEIGHT - 50) // BOX_SIZE
MINES = 50
SAFES = X * Y - MINES
LINEAR_DATA = [0] * (X * Y - MINES) + ['X'] * MINES

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "white.jpg")), (WIDTH, HEIGHT))
GAME_OVER = pygame.USEREVENT + 1
GAME_WON = pygame.USEREVENT + 2

MINES_FONT = pygame.font.SysFont('comicsans', 20)
SCORE_FONT = pygame.font.SysFont('comicsans', 20)
NUM_TEXT = [
    pygame.font.SysFont('arial', 12).render("0", 1, BLACK),
    pygame.font.SysFont('arial', 12).render("1", 1, BLACK),
    pygame.font.SysFont('arial', 12).render("2", 1, BLACK),
    pygame.font.SysFont('arial', 12).render("3", 1, BLACK),
    pygame.font.SysFont('arial', 12).render("4", 1, BLACK),
    pygame.font.SysFont('arial', 12).render("5", 1, BLACK),
    pygame.font.SysFont('arial', 12).render("6", 1, BLACK),
    pygame.font.SysFont('arial', 12).render("7", 1, BLACK),
    pygame.font.SysFont('arial', 12).render("8", 1, BLACK)
]


def get_corner(pos):
    row, col = pos
    return row * BOX_SIZE, HEAD_BUFFER_SIZE + col * BOX_SIZE


def get_index(pos):
    return math.floor(pos[0] / BOX_SIZE), math.floor((pos[1] - HEAD_BUFFER_SIZE) / BOX_SIZE)


def get_mine():
    mine_img = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'mine.png')), (20, 20))
    return mine_img


def get_flag():
    flag_img = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'flag.png')), (20, 20))
    return flag_img


def get_mine_locations(data):
    locations = np.argwhere(np.array(data) == "X")
    return locations


def draw_flags(flags_list):
    for flag in flags_list:
        WIN.blit(flag[1], get_corner(flag[0]))


def draw_mines(data, show_mines):
    if show_mines:
        mine_locs = get_mine_locations(data)
        for loc in mine_locs:
            mine = get_mine()
            WIN.blit(mine, get_corner(loc))


def draw_grid():
    """Draws the main game board grid"""
    for x in range(X):
        for y in range(Y):
            rect = pygame.Rect(x * BOX_SIZE, HEAD_BUFFER_SIZE + y * BOX_SIZE, BOX_SIZE, BOX_SIZE)
            pygame.draw.rect(WIN, BLACK, rect, 1)


def draw_visited_nodes(game_data):
    """
    :param game_data:
    """
    for x in range(X):
        for y in range(Y):
            # print(GAME_DATA[x][y])
            if type(game_data[x][y]) is int:
                rect = pygame.Rect(x * BOX_SIZE, HEAD_BUFFER_SIZE + y * BOX_SIZE, BOX_SIZE, BOX_SIZE)
                pygame.draw.rect(WIN, BLUE, rect, 1)
                WIN.blit(NUM_TEXT[game_data[x][y]], (5 + x * BOX_SIZE, 53 + (y * BOX_SIZE)))


def draw(data, game_data, num_of_flags, flags_list, show_mines, show_win):
    WIN.blit(BACKGROUND, (0, 0))
    draw_score(num_of_flags)
    draw_grid()
    draw_visited_nodes(game_data)
    draw_flags(flags_list)
    draw_mines(data, show_mines)
    if show_win:
        end_game(False)
    elif show_mines:
        end_game(True)
    pygame.display.update()
    if show_mines or show_win:
        pygame.time.delay(5000)


def set_hints(data):
    """Sets the game board
    :param data: actual game data
    """
    for x in range(X):
        for y in range(Y):
            if data[x][y] == "X":
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        try:
                            if x + dx >= 0 and y + dy >= 0 and data[x + dx][y + dy] != "X":
                                data[x + dx][y + dy] += 1
                        except IndexError:
                            continue


def set_my_8_clear(row, col, data, game_data, flags_list, num_of_flags):
    """ If an empty cell is hit keep on clearing adjacent cells till non empty cells are hit
    If a mine is hit end game
    If a non empty cell is hit reveal cell
    :param flags_list:
    :param num_of_flags:
    :param row: row id of the cell
    :param col: column id of the cell
    :param data: actual value of the cells
    :param game_data: the value player sees on the game board
    """

    if data[row][col] == "X":
        pygame.event.post(pygame.event.Event(GAME_OVER))
    else:
        if data[row][col] != 0:
            game_data[row][col] = data[row][col]
        else:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx or dy:
                        x, y = row + dx, col + dy
                        try:
                            if 0 <= x < X and 0 <= y < Y and data[x][y] != "X" and (game_data[x][y] == "NV" or game_data[x][y] == 'F'):
                                if game_data[x][y] == 'F':
                                    num_of_flags = remove_flag(x, y, game_data, flags_list, num_of_flags)
                                game_data[x][y] = data[x][y]
                                if game_data[x][y] == 0:
                                    num_of_flags = set_my_8_clear(x, y, data, game_data, flags_list, num_of_flags)
                        except IndexError:
                            continue
    return num_of_flags


def draw_score(num_of_flags):
    mines_text = MINES_FONT.render(f"Mines flagged: {num_of_flags}", 1, BLACK)
    WIN.blit(mines_text, (WIDTH - mines_text.get_width() - 20, 10))


def end_game(mines):
    if mines:
        text = "You Loose !!!"
    else:
        text = "You Win !!!"
    end_text = SCORE_FONT.render(text, 1, BLACK)
    WIN.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, 25))


def handle_left_click(pos, data, game_data, flags_list, num_of_flags):
    row, col = get_index(pos)
    num_of_flags = set_my_8_clear(row, col, data, game_data, flags_list, num_of_flags)
    if len(np.argwhere(np.array(game_data) == 'NV')) + len(np.argwhere(np.array(game_data) == 'F')) == MINES:
        pygame.event.post(pygame.event.Event(GAME_WON))
    return num_of_flags


def remove_flag(row, col, game_data, flags_list, num_of_flags):
    game_data[row][col] = 'NV'
    num_of_flags -= 1
    for index, content in enumerate(flags_list):
        if [row, col] == content[0]:
            del flags_list[index]
            break
    return num_of_flags


def handle_right_click(pos, game_data, num_of_flags, flags_list):
    row, col = get_index(pos)
    if game_data[row][col] == 'F':
        num_of_flags = remove_flag(row, col, game_data, flags_list, num_of_flags)
    elif game_data[row][col] == 'NV':
        game_data[row][col] = 'F'
        num_of_flags += 1
        flag = get_flag()
        flags_list.append(([row, col], flag))
    return num_of_flags


def main():
    run = True
    random.shuffle(LINEAR_DATA)  # Randomly shuffle mines on the board
    data = [[LINEAR_DATA.pop() for _ in range(X)] for _ in range(Y)]
    game_data = [['NV' for _ in range(X)] for _ in range(Y)]
    num_of_flags = 0
    set_hints(data)
    clock = pygame.time.Clock()
    flags_list = []
    show_mines = False
    show_win = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == GAME_OVER:
                show_mines = True
                run = False
            if event.type == GAME_WON:
                show_win = True
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:  # Left Click
                    num_of_flags = handle_left_click(pos, data, game_data, flags_list, num_of_flags)
                if event.button == 3:  # Right Click
                    num_of_flags = handle_right_click(pos, game_data, num_of_flags, flags_list)
        draw(data, game_data, num_of_flags, flags_list, show_mines, show_win)


if __name__ == '__main__':
    main()

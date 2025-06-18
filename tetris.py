import curses
import random
import time

WIDTH = 10
HEIGHT = 20

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

def check(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx = x + off_x
                ny = y + off_y
                if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
                    return True
                if ny >= 0 and board[ny][nx]:
                    return True
    return False

def merge(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and y + off_y >= 0:
                board[y + off_y][x + off_x] = cell

def clear_lines(board):
    new_board = [row for row in board if not all(row)]
    cleared = HEIGHT - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [0] * WIDTH)
    return new_board, cleared

def draw(stdscr, board, shape, offset, score):
    stdscr.clear()
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            ch = '#' if cell else '.'
            stdscr.addch(y, x, ch)
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and y + off_y >= 0:
                stdscr.addch(y + off_y, x + off_x, '#')
    stdscr.addstr(0, WIDTH + 2, f"Score: {score}")
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    board = [[0] * WIDTH for _ in range(HEIGHT)]
    shape = random.choice(SHAPES)
    offset = [WIDTH // 2 - len(shape[0]) // 2, 0]
    drop_time = 0.5
    next_drop = time.time() + drop_time
    score = 0

    while True:
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            new_offset = [offset[0] - 1, offset[1]]
            if not check(board, shape, new_offset):
                offset = new_offset
        elif key == curses.KEY_RIGHT:
            new_offset = [offset[0] + 1, offset[1]]
            if not check(board, shape, new_offset):
                offset = new_offset
        elif key == curses.KEY_DOWN:
            new_offset = [offset[0], offset[1] + 1]
            if not check(board, shape, new_offset):
                offset = new_offset
        elif key == curses.KEY_UP:
            new_shape = rotate(shape)
            if not check(board, new_shape, offset):
                shape = new_shape
        elif key == ord('q'):
            break

        now = time.time()
        if now > next_drop:
            new_offset = [offset[0], offset[1] + 1]
            if not check(board, shape, new_offset):
                offset = new_offset
            else:
                merge(board, shape, offset)
                board, cleared = clear_lines(board)
                score += cleared
                shape = random.choice(SHAPES)
                offset = [WIDTH // 2 - len(shape[0]) // 2, 0]
                if check(board, shape, offset):
                    break
            next_drop = now + drop_time

        draw(stdscr, board, shape, offset, score)
        time.sleep(0.05)

curses.wrapper(main)

import time
import curses
import asyncio
import random
from pathlib import Path
from itertools import cycle
from utils.curses_tools import draw_frame, get_frame_size

TIC_TIMEOUT = 0.1
SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258
with open(Path.cwd() / "shots" / "rocket_frame_1.txt", "r") as my_file1, \
     open(Path.cwd() / "shots" / "rocket_frame_2.txt", "r") as my_file2:
    rocket_frame_1 = my_file1.read()
    rocket_frame_2 = my_file2.read()


def draw(canvas):
    window = curses.initscr()
    h, w = window.getmaxyx()
    window.nodelay(True)
    stars = '+*.:'
    curses.curs_set(False)
    canvas.refresh()
    async def blink(canvas, row, column, symbol='*'):
        while True:
            canvas.addstr(row, column, symbol, curses.A_DIM)
            for _ in range(random.randint(1, 20)):
                await asyncio.sleep(0)
            canvas.addstr(row, column, symbol)
            for _ in range(random.randint(1, 20)):
                await asyncio.sleep(0)
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            for _ in range(random.randint(1, 20)):
                await asyncio.sleep(0)
            canvas.addstr(row, column, symbol)
            for _ in range(random.randint(1, 20)):
                await asyncio.sleep(0)

    async def fire(
        canvas,
        start_row,
        start_column,
        rows_speed=-0.3,
        columns_speed=0,
         ):
        row, column = 12, 40
        canvas.addstr(round(row), round(column), '*')
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), 'O')
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed
        symbol = '-' if columns_speed else '|'
        rows, columns = canvas.getmaxyx()
        max_row, max_column = rows - 1, columns - 1
        curses.beep()
        while 0 < row < max_row and 0 < column < max_column:
            canvas.addstr(round(row), round(column), symbol)
            await asyncio.sleep(0)
            canvas.addstr(round(row), round(column), ' ')
            row += rows_speed
            column += columns_speed

    async def animated_spaceship(canvas, h, w, rocket_frame_1, rocket_frame_2):
        while True:
            draw_frame(canvas, h, w, rocket_frame_1)
            canvas.refresh()
            time.sleep(0.1)
            draw_frame(canvas, h, w, rocket_frame_1, negative=True)
            draw_frame(canvas, h, w, rocket_frame_2)
            canvas.refresh()
            time.sleep(0.1)
            await asyncio.sleep(0)
            draw_frame(canvas, h, w, rocket_frame_2, negative=True)
            h, w, s = read_controls(canvas, h, w)

    def read_controls(canvas, h, w):
        rows_direction = h
        columns_direction = w
        space_pressed = False
        window = curses.initscr()
        h_max, w_max = window.getmaxyx()
        spaceships_h, spaceships_w = get_frame_size(rocket_frame_1)

        while True:
            pressed_key_code = canvas.getch()

            if pressed_key_code == -1:
                break
            if pressed_key_code == UP_KEY_CODE:
                if h != 0:
                    rows_direction = h - 1
            if pressed_key_code == DOWN_KEY_CODE:
                if h != (h_max - spaceships_h):
                    rows_direction = h + 1
            if pressed_key_code == RIGHT_KEY_CODE:
                if w != (w_max - spaceships_w):
                    columns_direction = w + 1
            if pressed_key_code == LEFT_KEY_CODE:
                if w != 0:
                    columns_direction = w - 1
            if pressed_key_code == SPACE_KEY_CODE:
                space_pressed = True
        return rows_direction, columns_direction, space_pressed
    coroutines = [blink(
        canvas,
        random.randrange(1, h - 1),
        random.randrange(1, w - 1),
        random.choice(stars)
     ) for i in range(70)]
    coroutines.append(fire(canvas, h/2, w/2))
    coroutines.append(animated_spaceship(
        canvas,
        h/2,
        w/2,
        rocket_frame_1,
        rocket_frame_2
    )
                      )
    while True:
        try:
            for coroutine in coroutines.copy():
                coroutine.send(None)
        except StopIteration:
            coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
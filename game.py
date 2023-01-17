import time
import curses
import asyncio
import random
import os
from pathlib import Path
from utils.curses_tools import draw_frame, get_frame_size, read_controls
from itertools import cycle


def draw(canvas, frames):

    height, width = canvas.getmaxyx()
    canvas.nodelay(True)
    simbols = '+*.:'
    curses.curs_set(False)
    canvas.border()

    offset_tics = 20
    stars_number = 70
    coroutines = [blink(
        canvas,
        random.randrange(height),
        random.randrange(width),
        offset_tics,
        random.choice(simbols),
    ) for _ in range(stars_number)]

    start_row_fire = 10
    start_column_fire = 40
    coroutines.append(fire(canvas, start_row_fire, start_column_fire))

    start_row_spaceship = 11
    start_column_spaceship = 38
    coroutines.append(animate_spaceship(
        canvas,
        start_row_spaceship,
        start_column_spaceship,
        frames,
    )
                      )

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(0.1)


async def blink(canvas, row, column, offset_tics, symbol='*'):

    while True:
        for _ in range(random.randrange(1, offset_tics)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):

    row, column = start_row, start_column

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


async def animate_spaceship(canvas, start_row, start_column, frames):

    h_max, w_max = canvas.getmaxyx()

    spaceships_h, spaceships_w = get_frame_size(frames[0])

    for frame in cycle(frames):
        draw_frame(canvas, start_row, start_column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, start_row, start_column, frame, negative=True)

        rows_direction, columns_direction, space = read_controls(canvas)
        if (start_row + rows_direction >= 0 and
                start_row + rows_direction <= (h_max - spaceships_h)):
            start_row += rows_direction
        if (start_column + columns_direction >= 0 and
                start_column + columns_direction <= (w_max - spaceships_w)):
            start_column += columns_direction


if __name__ == '__main__':

    frames = []
    spaceship_animate_tics = 2

    for root, dirs, files in os.walk(Path.cwd() / 'shots'):
        for filename in files:
            with open(Path.cwd() / 'shots' / filename, 'r') as file:
                frame = file.read()
                for _ in range(spaceship_animate_tics):
                    frames.append(frame)

    curses.update_lines_cols()
    curses.wrapper(draw, frames)

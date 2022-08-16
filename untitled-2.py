import time
import curses
import asyncio
import random
from pathlib import Path
from itertools import cycle
from utils.curses_tools import draw_frame

TIC_TIMEOUT = 0.1
with open(Path.cwd() / "shots" / "rocket_frame_1.txt", "r") as my_file1, \
     open(Path.cwd() / "shots" / "rocket_frame_2.txt", "r") as my_file2:
    rocket_frame_1 = my_file1.read()
    rocket_frame_2 = my_file2.read()

def draw(canvas):
    window = curses.initscr()
    h, w = window.getmaxyx()
    stars = '+*.:'
    canvas.border()
    curses.curs_set(False)
    canvas.refresh()
    #async def blink(canvas, row, column, symbol='*'):
        #while True:
            #canvas.addstr(row, column, symbol, curses.A_DIM)
            #for _ in range(random.randint(1, 20)):
                #await asyncio.sleep(0)
            
                                
            #canvas.addstr(row, column, symbol)
            #for _ in range(random.randint(1, 20)):
                #await asyncio.sleep(0)            
            
            
            
            #canvas.addstr(row, column, symbol, curses.A_BOLD)
            #for _ in range(random.randint(1, 20)):
                #await asyncio.sleep(0)
        
            
            #canvas.addstr(row, column, symbol)
            #for _ in range(random.randint(1, 20)):
                #await asyncio.sleep(0)
            
    
    #async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
        #"""Display animation of gun shot, direction and speed can be specified."""
    
        #row, column = start_row, start_column
    
        #canvas.addstr(round(row), round(column), '*')
        #await asyncio.sleep(0)
    
        #canvas.addstr(round(row), round(column), 'O')
        #await asyncio.sleep(0)
        #canvas.addstr(round(row), round(column), ' ')
    
        #row += rows_speed
        #column += columns_speed
    
        #symbol = '-' if columns_speed else '|'
    
        #rows, columns = canvas.getmaxyx()
        #max_row, max_column = rows - 1, columns - 1
    
        #curses.beep()
    
        #while 0 < row < max_row and 0 < column < max_column:
            #canvas.addstr(round(row), round(column), symbol)
            #await asyncio.sleep(0)
            #canvas.addstr(round(row), round(column), ' ')
            #row += rows_speed
            #column += columns_speed
            
    
    #shots_rocket_list = [
            #draw_frame(canvas, h/2, w/2, rocket_frame_1),
            #canvas.refresh(),
            #time.sleep(1),
            #draw_frame(canvas, h/2, w/2, rocket_frame_1, negative=True),
            #draw_frame(canvas, h/2, w/2, rocket_frame_2),
            #canvas.refresh(),
            #time.sleep(1),
         #]
       
    while True:
        
            draw_frame(canvas, h/2, w/2, rocket_frame_1)
            canvas.refresh()
            time.sleep(0.1)
            draw_frame(canvas, h/2, w/2, rocket_frame_1, negative=True)
            draw_frame(canvas, h/2, w/2, rocket_frame_2)
            canvas.refresh()
            time.sleep(0.1)
            draw_frame(canvas, h/2, w/2, rocket_frame_2, negative=True)
            
            
            
            
        
    
    #coroutines = [blink(
        #canvas,
        #random.randrange(1, h - 1),
        #random.randrange(1, w - 1),
        #random.choice(stars)
     #) for i in range(70)]
    #coroutines.append(fire(canvas, h/2, w/2))
    #coroutines.append(animated_spaceship(canvas, h/2, w/2, rocket_frame_1, rocket_frame_2))
       
    #while True:
        #try:
            #for coroutine in coroutines.copy():
                #coroutine.send(None)
        #except StopIteration:
            #coroutines.remove(coroutine)
        #canvas.refresh()
        #time.sleep(TIC_TIMEOUT)
            


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
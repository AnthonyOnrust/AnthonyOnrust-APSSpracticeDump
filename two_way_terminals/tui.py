import curses
from curses import wrapper

def main(stdscr):
    stdscr.clear() 
    stdscr.addstr(0, 0, "Hello")
    stdscr.getch()

wrapper(main)

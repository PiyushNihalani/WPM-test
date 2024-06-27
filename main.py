import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Typing Speed Test\n")
    stdscr.addstr("Press any key to start")
    stdscr.refresh()
    stdscr.getkey()


def text():
    with open("text.txt",'r') as f:
        lines=f.readlines()
        return random.choice(lines).strip()
    


def display(stdscr,target,current,wpm=0):
    stdscr.addstr(target)
    global incr
    incr=0
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    
    for i,char in enumerate(current):
        correct=target[i]
        color=curses.color_pair(1)
        if(char!=correct):
            incr+=1
            color=curses.color_pair(2)    
        
        stdscr.addstr(0,i,char,color)


def wpm_test(stdscr):
    target=text()
    curr=[]
    global wpm
    wpm=0
    
    stdscr.nodelay(True)
    start_time=time.time()
    while True:
        time_elapsed=max(time.time()-start_time,1)
        wpm=round((len(curr)/(time_elapsed/60)) /5)
        
        stdscr.clear()
        display(stdscr,target,curr,wpm)
        stdscr.refresh() 
        
        current=''.join(curr)
        if(current==target or len(current)==len(target)):
            stdscr.nodelay(False)
            return len(current)
        
        try:
            k=stdscr.get_wch()
        except:
            continue
        
        try:
            if ord(k) == 27:
                break
        
        
            if k in ("KEY_BACKSPACE",'\b',"\x7f"):#all three things in quotes are different ways backspace is represented on different OS
                if len(curr)>0 :
                    curr.pop()
            elif len(curr)<len(target):
                curr.append(k)
        except TypeError as e:
            continue
    
               


def main(stdscr):
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_WHITE)
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
    
    start_screen(stdscr)
    while True:
        letters=wpm_test(stdscr)
        stdscr.addstr("\nThankyou for using the app press any key to continue")
        stdscr.addstr(f"\nWPM : {wpm}")
        stdscr.addstr(f"\nIncorrect entries/Total entries = {incr}/{letters}")
        stdscr.addstr("\nYOU SUCK INCREASE YOUR SPEED")
        stdscr.addstr("\npress ESC to GIVE UP", curses.A_BOLD )
        
        try:
            key=stdscr.get_wch()
        except:
            continue
            
		
        try:
            if ord(key) == 27:
                break
        except TypeError as e:
            continue
    

wrapper(main)

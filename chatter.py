import argparse, os, random
from pynput.keyboard import Key, Controller, Listener
from collections import deque
import pyperclip

# BOILERPLATE
deduper = deque(['']*10)# FIFO-10
deduper_start = deque(['']*4)# FIFO-4
deduper_finish = deque(['']*4)# FIFO-4
kb = Controller()
line = ""
# PLATEBOILER

def on_press(key):
    if key is Key.f6:
        paste_txt()
    #elif key is Key.f7:
        # paste_harmony_txt()
    #elif key is Key.f8: 
        # paste_discord_txt()

def send_line():
    kb.press(Key.shift)
    kb.press(Key.enter)
    kb.release(Key.enter)
    kb.release(Key.shift)
    kb.press(Key.ctrl)
    kb.press('v')
    kb.release('v')
    kb.release(Key.ctrl)
    kb.press(Key.enter)
    kb.release(Key.enter)

def cp_random_line(type="",channel=""):
    global deduper, deduper_start, deduper_finish, line
    try:
        _lines = open('lines.txt').read().splitlines()
        _starters = open('starters.txt').read().splitlines()
        _finishers = open('finishers.txt').read().splitlines()

    except Exception as e:
        print("[FAILURE] UNABLE TO LOAD FILES (CHECK FILENAME)")
    line = "" + channel + " "

    # randomize starting words
    randstart = ""
    if random.randint(1, 100) <= 30:
        linefound = True
        while linefound:
            randstart = random.sample(_starters, 1)[0]
            if not randstart in deduper_start:
                deduper_start.appendleft(randstart)
                linefound = False
        deduper_start.pop()
    line += randstart

    # get random line from lines.txt
    randline = random.choice(_lines)
    if randline in deduper:
        linefound = True
        while linefound:
            randline = random.choice(_lines)
            if not randline in deduper: linefound = False

    deduper.pop()
    deduper.appendleft(randline)

    line += (" ") + randline

    # random chance for ending words
    randfinish = ""
    if random.randint(1,100) <= 25 :
        linefound = True
        while linefound:
            randfinish = random.sample(_finishers,1)[0]
            if not randfinish in deduper_finish:
                linefound = False
                deduper_finish.appendleft(randfinish)
        deduper_finish.pop()
    line += (" ") + randfinish

    pyperclip.copy(line)
    return

def paste_txt():
    cp_random_line()
    #cp_channel_switch()
    send_line()

if __name__ == '__main__':
    print("chatter.txt.exe loaded. Press F6 to paste a new line.")

    with Listener(
            on_press=on_press) as listener:
        listener.join()

import curses
import random
from collections import deque
import time


def load_words(path) -> list:
    try:
        with open(path, "r") as f:
            return [a.rstrip() for a in f.readlines()]
    except Exception:
        return []


def main(stdscr):
    curses.use_default_colors()

    words = []
    words += load_words("./english10k.wordlist")

    while (1):
        random.shuffle(words)
        typingtest(words, stdscr)


def typingtest(words: list, scr):
    q = deque()
    y, x = scr.getmaxyx()
    for i, w in enumerate(words):
        for wc in w + " ":
            q.append(wc)

            if len(q) > 20:
                scr.addstr(y//2, x//2, "".join([a for a in q]))
                scr.move(y//2, x//2)
                scr.refresh()
                c = chr(scr.getch())

                if c != (cc := q.popleft()):
                    return fail(scr, y, x, c, cc)


def fail(scr, y, x, c, cc):
    scr.move(y//2, x//2)
    scr.clrtoeol()
    scr.addstr("Oops! You fail")
    scr.addstr(y//2+1, x//2,
               f"You press {c.upper()} instead of {cc.upper()}"
               )
    scr.refresh()
    time.sleep(1)
    chr(scr.getch())
    scr.move(y//2, x//2)
    scr.clrtoeol()
    scr.move(y//2+1, x//2)
    scr.clrtoeol()


if __name__ == '__main__':
    curses.wrapper(main)

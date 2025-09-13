import curses
import random
from collections import deque
import os
import signal
import sys
import time

stop_at_words = True
max_words = 30
stop_at_time = True
max_time = 30  # seconds
last_failed_word = None


def sigint_handler(sig, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)


def load_words(path) -> list:
    try:
        with open(path, "r") as f:
            return [a.rstrip() for a in f.readlines()]
    except Exception:
        return []


def main(stdscr):
    curses.use_default_colors()

    words = []
    words += load_words(resource_path("./english10k.wordlist"))

    if (words == []):
        return 1

    while (1):
        random.shuffle(words)
        typingtest(words, stdscr)


def typingtest(words: list, scr):
    global last_failed_word
    q = deque()
    y, x = scr.getmaxyx()
    curses.flushinp()

    ii = 0
    if last_failed_word:
        words.insert(0, last_failed_word)
        last_failed_word = None

    t0 = time.time()
    for i, w in enumerate(words):
        for wc in w + " ":
            q.append(wc)

            if len(q) > 20:
                scr.addstr(y//2, x//2, "".join([a for a in q]))
                scr.move(y//2, x//2)
                scr.refresh()

                c = chr(scr.getch())
                cc = q.popleft()

                if cc == ' ':
                    ii += 1

                if c != cc:
                    last_failed_word = words[ii]
                    return fail(scr, y, x, c, cc, last_failed_word)

                if stop_at_time and (t := time.time()) - t0 >= max_time:
                    return report_wpm(scr, y, x, t0, t, i+1)

        if stop_at_words and i+1 == max_words:
            return report_wpm(scr, y, x, t0, time.time(), i+1)


def fail(scr, y, x, c, cc, word):
    scr.move(y//2, x//2)
    scr.clrtoeol()
    scr.addstr(f"Oops! You fail at {word}")
    scr.addstr(y//2+1, x//2, f"You press {c.upper()} instead of {cc.upper()}")
    scr.refresh()
    time.sleep(1)
    scr.move(y//2, x//2)
    scr.clrtoeol()
    scr.move(y//2+1, x//2)
    scr.clrtoeol()


def report_wpm(scr, y, x, t0, t1, i):
    scr.move(y//2, x//2)
    scr.clrtoeol()
    t = t1 - t0
    wpm = i * 60 / t
    scr.addstr(f"{round(wpm)} WPM")
    scr.addstr(y//2+1, x//2, f"You tipe {i} words in {round(t)} seconds!")
    scr.refresh()
    time.sleep(1)
    chr(scr.getch())
    scr.move(y//2, x//2)
    scr.clrtoeol()
    scr.move(y//2+1, x//2)
    scr.clrtoeol()


if __name__ == '__main__':
    curses.wrapper(main)

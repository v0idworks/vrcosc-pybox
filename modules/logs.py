import curses
import time
from datetime import datetime
from config import ENABLE_HARDWARE, ENABLE_COMMIT, ENABLE_RANDOM, ENABLE_WEATHER, ENABLE_WINDOW, ENABLE_MUSIC
from modules import hardware, gitinfo, weather, window, music
import random

ASCII_ART = r"""welcome to
                       _
  ______              | |                ______
 |______|  _ __  _   _| |__   _____  __ |______|
  ______  | '_ \| | | | '_ \ / _ \ \/ /  ______
 |______| | |_) | |_| | |_) | (_) >  <  |______|
          | .__/ \__, |_.__/ \___/_/\_\
          | |     __/ |
          |_|    |___/
"""

logs = []
#честно скажу, чуть чуть Bайбкода B логах имеется
def check_modules():
    logs.clear()
    for line in ASCII_ART.splitlines():
        logs.append(" " + line)
# TODO: Переделать логи
# а именно то что они делают(не просто чек Bключен ли модуль)
    def log_status(name, func, enabled=True):
        if not enabled:
            logs.append(f"[ОТКЛЮЧЕНО] {name}")
            return
        try:
            func()
            logs.append(f"[OK] {name} запущен")
        except Exception as e:
            logs.append(f"[ОШИБКА] {name}: {e}")

    log_status("HARDWARE", hardware.get_cpu_ram, ENABLE_HARDWARE)
    log_status("WEATHER", weather.get_weather, ENABLE_WEATHER)
    log_status("WINDOW", window.get_window, ENABLE_WINDOW)
    log_status("MUSIC", music.get_music, ENABLE_MUSIC)
    log_status("GIT", gitinfo.get_git_commit, ENABLE_COMMIT)

def curses_main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    max_y, max_x = stdscr.getmaxyx()
    log_height = max_y - 10
    log_win = curses.newwin(log_height, max_x, 0, 0)
    panel_win = curses.newwin(10, max_x, max_y - 10, 0)
    check_modules()

    while True:
        log_win.erase()
        log_win.border()
        log_win.attron(curses.color_pair(3))
        log_win.addstr(0, 2, " ЛОГИ ")
        log_win.attroff(curses.color_pair(3))
        for i, line in enumerate(logs[:log_height-2]):
            color = curses.color_pair(
                1 if "[OK]" in line else
                2 if "[ОТКЛЮЧЕНО]" in line else
                2 if "[ОШИБКА]" in line else
                4
            )
            log_win.attron(color)
            log_win.addstr(i + 1, 2, line[:max_x-4])
            log_win.attroff(color)
        log_win.refresh()
        panel_win.erase()
        panel_win.border()
        panel_win.attron(curses.color_pair(4))
        panel_win.addstr(0, 2, " ИНФО ")
        panel_win.attroff(curses.color_pair(4))

        row = 1
        if ENABLE_HARDWARE:
            try:
                cpu, ram = hardware.get_cpu_ram()
                gpu_util, vram_used, vram_total = hardware.get_gpu()
                msg = f"CPU {cpu}%  RAM {ram}%"
                if gpu_util is not None:
                    msg += f"  GPU {gpu_util}%  VRAM {vram_used}/{vram_total}MB"
                panel_win.addstr(row, 2, msg, curses.color_pair(1))
                row += 1
            except Exception as e:
                panel_win.addstr(row, 2, f"HARDWARE ERR: {e}", curses.color_pair(2))
                row += 1

        if ENABLE_COMMIT:
            try:
                commit = gitinfo.get_commit()
                panel_win.addstr(row, 2, f"GIT {commit}", curses.color_pair(4))
                row += 1
            except Exception as e:
                panel_win.addstr(row, 2, f"GIT ERR: {e}", curses.color_pair(2))
                row += 1
        if ENABLE_MUSIC:
            try:
                track = music.get_current_track()
                if track:
                    panel_win.addstr(row, 2, f"MUSIC {track}", curses.color_pair(1))
                else:
                    panel_win.addstr(row, 2, "MUSIC ничего не играет", curses.color_pair(4))
                row += 1
            except Exception as e:
                panel_win.addstr(row, 2, f"MUSIC ERR: {e}", curses.color_pair(2))
                row += 1
        if ENABLE_WINDOW:
            try:
                win = window.get_active_window()
                panel_win.addstr(row, 2, f"WIN {win}", curses.color_pair(4))
                row += 1
            except Exception as e:
                panel_win.addstr(row, 2, f"WIN ERR: {e}", curses.color_pair(2))
                row += 1
        if ENABLE_WEATHER:
            try:
                temp, status = weather.get_weather()
                panel_win.addstr(row, 2, f"WEATHER {temp}°C {status}", curses.color_pair(1))
                row += 1
            except Exception as e:
                panel_win.addstr(row, 2, f"WEATHER ERR: {e}", curses.color_pair(2))
                row += 1
        panel_win.addstr(row, 2, f"TIME {datetime.now().strftime('%H:%M:%S')}", curses.color_pair(4))
        panel_win.refresh()
        time.sleep(1)


def initui():
    curses.wrapper(curses_main)

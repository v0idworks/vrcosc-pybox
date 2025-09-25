import time, random
from datetime import datetime
from pythonosc.udp_client import SimpleUDPClient
from config import *
from . import hardware, gitinfo, weather, window, music

client1 = SimpleUDPClient(IP1, PORT)
client2 = SimpleUDPClient(IP2, PORT)

def main_loop():
    weather_info = weather.get_weather()
    last_weather_update = time.time()
    parts = []
    while True:
        if time.time() - last_weather_update > 120:
            weather_info = weather.get_weather()
            last_weather_update = time.time()

        parts.clear()
        if ENABLE_HARDWARE:
            cpu, ram = hardware.get_cpu_ram()
            gpu_util, vram_used, vram_total = hardware.get_gpu()
            msg = f"CPU {cpu}% RAM {ram}%"
            if gpu_util is not None:
                msg += f" GPU {gpu_util}% VRAM {vram_used}/{vram_total}MB"
            parts.append(msg)

        if weather_info:
            parts.append(weather_info)
        if ENABLE_RANDOM and CUSTOM_MESSAGES:
            random_msg = random.choice(CUSTOM_MESSAGES)
            parts.append(f"💬 {random_msg}")
        if ENABLE_COMMIT:
            parts.append("⚙pybox " + gitinfo.get_git_commit())
        if ENABLE_WINDOW:
            w = window.get_window()
            if w: parts.append(w)
        if ENABLE_MUSIC:
            m = music.get_music()
            if m: parts.append(m)
        parts.append(f"🕒 {datetime.now().strftime('%H:%M')}")
        final_msg = "\n".join(parts)
        client1.send_message("/chatbox/input", [final_msg, True])
        if ENABLE_2CLIENT:
            client2.send_message("/chatbox/input", [final_msg, True])
        time.sleep(2)

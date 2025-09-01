import time, psutil, requests, subprocess, random
from pythonosc.udp_client import SimpleUDPClient
from datetime import datetime

ip, port = "127.0.0.1", 9000
client = SimpleUDPClient(ip, port)

# --- Кастомизация ---
ENABLE_STATIC = True
ENABLE_RANDOM = True
ENABLE_WEATHER = True
ENABLE_HARDWARE = True

custom_messages = [
    "niko7227: аххх, мучай меня больше",
    "Длиннbiй текст это очень очень очень плохо",
    "VRChat кал 😎",
    "Stay comfy 🛋",
    "Не болейте ❤️",
    "сделано бургером",
    "Сделано бургерсракой",
    "made by burgerstruct",
    "by voidworks",
    "Winter:ну злой мерс ахуел короче да",
    "Niko:я потому что ты помог стриптиз зарейдить",
    "Niko: Я СКАЗАЛ НА МЕНЯ СЕСТЬ",
    "Sonrock:Я сын шлюхи вы знали?"
]


static_message = "⚙️ pybox v1.0.0"

# -можна менять иконочки-
weather_icons = {
    "sunny": "☀️","clear": "🌙","partly cloudy": "⛅","cloudy": "☁️",
    "overcast": "🌥","mist": "🌫","patchy rain possible": "🌦",
    "light rain": "🌧","heavy rain": "⛈","snow": "❄️","thunder": "🌩"
}
weather_translate = {
    "sunny": "Солнечно","clear": "Ясно","partly cloudy": "Перемен. облачность",
    "cloudy": "Облачно","overcast": "Пасмурн","mist": "Туман",
    "patchy rain possible": "Возможен дождь","light rain": "Небольш. дождь",
    "heavy rain": "Сильн. дождь","snow": "Снег","thunder": "Гроза", "light rain shower": "Моросящ. дождь"
}

# --- Город тут замени ---
city = "Москоу"

def get_gpu():
    try:
        out = subprocess.check_output(
            ["nvidia-smi","--query-gpu=utilization.gpu,memory.used,memory.total","--format=csv,noheader,nounits"], encoding="utf-8")
        u, used, total = out.strip().split(", ")
        return int(u), int(used), int(total)
    except: return None, None, None

def get_weather(city=city):
    try:
        data = requests.get(f"https://wttr.in/{city}?format=j1",timeout=5).json()
        t = data["current_condition"][0]["temp_C"]
        f = data["current_condition"][0]["FeelsLikeC"]
        desc_en = data["current_condition"][0]["weatherDesc"][0]["value"].lower()
        icon = next((e for k,e in weather_icons.items() if k in desc_en), "❓")
        desc_ru = weather_translate.get(desc_en, desc_en.capitalize())
        return f"{icon} {desc_ru} {t}°C (ощущае як {f}°C)"
    except: return "🌐 Упс!!! Не могу достучаца до wttr.in!!!"

# --- Кэш погоды ---
weather_info = get_weather()
last_weather_update = time.time()

while True:
    if time.time() - last_weather_update > 120:
        weather_info = get_weather()
        last_weather_update = time.time()

    cpu = psutil.cpu_percent(None)
    ram = psutil.virtual_memory().percent
    temp = psutil.sensors_temperatures()
    gpu_util, vram_used, vram_total = get_gpu()
    cpu_temp = temp["coretemp"][0].current if "coretemp" in temp else "?"

    parts = []
    if ENABLE_HARDWARE:
        hw_msg = f"🖥 {cpu}% | 🌡 {cpu_temp}°C | 🧠 {ram}%"
        if gpu_util is not None:
            hw_msg += f" | 🎮{gpu_util}% 💾{vram_used}/{vram_total}MB"
        parts.append(hw_msg)
    if ENABLE_WEATHER:
        parts.append(weather_info)
    if ENABLE_RANDOM:
        parts.append(f"💬 {random.choice(custom_messages)}")
    if ENABLE_STATIC:
        parts.append(f"{static_message}")
    local_time = datetime.now().strftime("%H:%M")
    parts.append(f"🕒 {local_time}")
    final_msg = "\n".join(parts)
    client.send_message("/chatbox/input",[final_msg, True])
    GPU_CHECK = gpu_util if gpu_util is not None else 0
    time.sleep(2)
